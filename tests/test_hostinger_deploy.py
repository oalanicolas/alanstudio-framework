"""Static Hostinger publishing: vercel.json translation, build resolution and archive contents."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from urllib.robotparser import RobotFileParser
import zipfile

SPEC = importlib.util.spec_from_file_location("hostinger_deploy", Path(__file__).resolve().parents[1] / "scripts/hostinger_deploy.py")
deploy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(deploy)

VERCEL = {
    "outputDirectory": "dist/client",
    "cleanUrls": True,
    "trailingSlash": False,
    "rewrites": [{"source": "/elenco", "destination": "/elenco.html"}],
    "headers": [
        {"source": "/fonts/(.*)", "headers": [
            {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"},
            {"key": "X-Content-Type-Options", "value": "nosniff"},
        ]},
    ],
}


class HtaccessTests(unittest.TestCase):
    def test_headers_rewrites_and_clean_urls(self):
        text = deploy.htaccess_from_vercel(VERCEL)
        self.assertIn('SetEnvIf Request_URI "^/fonts/(.*)" VRC0', text)
        self.assertIn('Header set Cache-Control "public, max-age=31536000, immutable" env=VRC0', text)
        self.assertEqual(text.count("X-Content-Type-Options"), 1, "nosniff is set once, globally")
        self.assertIn("RewriteRule ^elenco$ /elenco.html [L]", text)
        self.assertIn("RewriteRule ^(.+)/$ /$1 [R=308,L]", text)
        self.assertIn("RewriteCond %{THE_REQUEST} \\s/+(.+)\\.html[\\s?] [NC]", text)
        self.assertLess(text.index("THE_REQUEST"), text.index("RewriteRule ^elenco$"), "redirects run before rewrites")
        self.assertIn("RewriteRule ^(.+)$ /$1.html [L]", text)
        self.assertIn('<FilesMatch "\\.html?$">', text)

    def test_data_files_are_never_immutable(self):
        cfg = {"headers": [{"source": "/(audio|sfx|music)/(.*)", "headers": [
            {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}]}
        text = deploy.htaccess_from_vercel(cfg)
        block = '<FilesMatch "\\.(json|md|txt|webmanifest)$">\n    Header set Cache-Control "no-cache"'
        self.assertIn(block, text)
        # <FilesMatch> merges after the .htaccess-level Header lines, so it overrides the folder rule
        self.assertGreater(text.index(block), text.index("env=VRC0"))

    def test_spa_fallback_only_when_asked(self):
        self.assertNotIn("RewriteEngine", deploy.htaccess_from_vercel({}))
        self.assertIn("RewriteRule ^ /index.html [L]", deploy.htaccess_from_vercel({}, spa=True))


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def write(self, rel, text="x"):
        path = self.project / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_dist_follows_vercel_output_directory(self):
        self.assertEqual(deploy.resolve_dist(self.project, VERCEL, None), (self.project / "dist/client").resolve())
        self.assertEqual(deploy.resolve_dist(self.project, {}, None), (self.project / "dist").resolve())
        self.assertEqual(deploy.resolve_dist(self.project, VERCEL, "out"), (self.project / "out").resolve())

    def test_zip_injects_generated_htaccess_and_skips_ds_store(self):
        dist = self.project / "dist"
        self.write("dist/index.html", "<title>x</title>")
        self.write("dist/assets/a.js")
        self.write("dist/.DS_Store")
        out = self.project / "a.zip"
        self.assertEqual(deploy.make_zip(dist, "# gerado", out), 3)
        with zipfile.ZipFile(out) as z:
            self.assertEqual(sorted(z.namelist()), [".htaccess", "assets/a.js", "index.html"])
            self.assertEqual(z.read(".htaccess"), b"# gerado")

    def test_project_root_build_never_ships_git_env_dependencies_or_ignored_files(self):
        for rel in ("index.html", "js/game.js", ".git", ".env", ".env.local", "node_modules/x/i.js",
                    ".vercel/project.json", "docs/notas.md", "AGENTS.md", "art/fonte.psd",
                    "assets/audio/musica.mp3", "assets/audio/efeito.mp3"):
            self.write(rel)
        self.write(".vercelignore", "# comentário\ndocs/\nAGENTS.md\n*.psd\nassets/audio/musica.mp3\n")
        names = [p.relative_to(self.project).as_posix() for p in deploy.build_files(self.project, self.project)]
        self.assertEqual(names, ["assets/audio/efeito.mp3", "index.html", "js/game.js"])
        self.write("dist/index.html")
        self.write("dist/docs/manual.md")
        dist_names = [p.relative_to(self.project / "dist").as_posix()
                      for p in deploy.build_files(self.project / "dist", self.project)]
        self.assertEqual(dist_names, ["docs/manual.md", "index.html"], "o .vercelignore só vale para a raiz")

    def test_htaccess_shipped_in_build_wins(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        self.write("dist/.htaccess", "# do build")
        out = self.project / "a.zip"
        deploy.make_zip(dist, "# gerado", out)
        with zipfile.ZipFile(out) as z:
            self.assertEqual(z.read(".htaccess"), b"# do build")

    def test_ai_policy_preserves_auth_routes_and_robots_without_mutating_build(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        auth = 'RewriteEngine On\nRewriteRule ^private/ guard.php [L]\n'
        original = 'User-agent: *\nAllow: /\nDisallow: /admin/\n'
        self.write("dist/.htaccess", auth)
        self.write("dist/robots.txt", original)
        self.write("dist/assets/game.js", "game")
        out = self.project / "a.zip"
        self.assertEqual(deploy.make_zip(dist, "# generated", out, block_ai_bots=True), 4)
        with zipfile.ZipFile(out) as z:
            self.assertEqual(len(z.namelist()), len(set(z.namelist())))
            rules = z.read(".htaccess").decode()
            self.assertIn(auth, rules)
            self.assertLess(rules.index("HTTP_USER_AGENT"), rules.index("guard.php"))
            self.assertGreater(rules.index('Header always set Cache-Control "no-store"'), rules.index("guard.php"))
            self.assertNotIn("# generated", rules)
            robots = z.read("robots.txt").decode()
            self.assertTrue(robots.startswith(original))
            for bot in deploy.AI_BOTS:
                self.assertIn(f"User-agent: {bot}\nDisallow: /", robots)
            self.assertEqual(z.read("assets/game.js"), b"game")
        self.assertEqual((dist / ".htaccess").read_text(), auth)
        self.assertEqual((dist / "robots.txt").read_text(), original)

    def test_ai_policy_adds_missing_rules_and_robots(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        out = self.project / "a.zip"
        self.assertEqual(deploy.make_zip(dist, "# generated", out, block_ai_bots=True), 3)
        with zipfile.ZipFile(out) as z:
            self.assertIn("# generated", z.read(".htaccess").decode())
            self.assertIn(b"User-agent: GPTBot\nDisallow: /", z.read("robots.txt"))
        self.assertFalse((dist / "robots.txt").exists())

    def test_ai_policy_does_not_publish_ignored_local_configuration(self):
        self.write("index.html")
        self.write(".htaccess", "PRIVATE_LOCAL_SERVER_CONFIG")
        self.write("robots.txt", "Sitemap: https://private-local.test/secrets\n")
        self.write(".vercelignore", ".htaccess\nrobots.txt\n")
        out = self.project / "package.zip"
        deploy.make_zip(self.project, "# public generated rules", out, self.project, block_ai_bots=True)
        with zipfile.ZipFile(out) as archive:
            rules = archive.read(".htaccess").decode()
            self.assertIn("# public generated rules", rules)
            self.assertNotIn("PRIVATE_LOCAL", rules)
            self.assertNotIn("private-local", archive.read("robots.txt").decode())

    def test_nested_application_rules_keep_the_filter_before_their_rewrites(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        own = 'RewriteEngine On\nRewriteRule ^ - [L]\n'
        self.write("dist/assets/.htaccess", own)
        out = self.project / "package.zip"
        deploy.make_zip(dist, "# root generated", out, block_ai_bots=True)
        with zipfile.ZipFile(out) as archive:
            rules = archive.read("assets/.htaccess").decode()
            self.assertIn(own, rules)
            self.assertLess(rules.index("HTTP_USER_AGENT"), rules.index(own))
            self.assertIn('RewriteCond %{REQUEST_URI} ^/robots\\.txt$', rules)
            self.assertGreater(rules.index('Header always set Cache-Control "no-store"'), rules.index(own))
        deploy.make_zip(dist, "# root generated", out)
        with zipfile.ZipFile(out) as archive:
            self.assertEqual(archive.read("assets/.htaccess").decode(), own)

    def test_conflicting_engine_and_conditional_sections_are_refused_before_packaging(self):
        for rel, rules in [
            (".htaccess", "RewriteEngine Off\n"),
            ("assets/.htaccess", 'RewriteEngine "Off"\n'),
            ("assets/.htaccess", "RewriteEngine 'Off'\n"),
            ("assets/.htaccess", "RewriteEngine \\\nOff\n"),
            ("assets/.htaccess", "RewriteEngine ${LOCAL_MODE}\n"),
            (".htaccess", '<If "%{REQUEST_URI} =~ m#^/assets/#">\nHeader always set Cache-Control "public"\n</If>\n'),
        ]:
            with self.subTest(rel=rel, rules=rules), tempfile.TemporaryDirectory() as folder:
                dist = Path(folder)
                (dist / "index.html").write_text("fixture")
                path = dist / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(rules)
                out = dist / "site.zip"
                with self.assertRaisesRegex(ValueError, "incompatível"):
                    deploy.make_zip(dist, "# generated", out, block_ai_bots=True)
                self.assertFalse(out.exists())
                deploy.make_zip(dist, "# generated", out)
                with zipfile.ZipFile(out) as archive:
                    self.assertEqual(archive.read(rel).decode(), rules)

    def test_sample_starts_with_index_and_spreads(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        for i in range(20):
            self.write(f"dist/assets/{i:02}.js")
        picked = deploy.sample(deploy.build_files(dist), dist, 4)
        self.assertEqual(picked[0], "index.html")
        self.assertEqual(len(picked), 5)
        self.assertEqual(len(set(picked)), 5)


class RobotsPolicyTests(unittest.TestCase):
    def test_comment_only_preamble_is_preserved_and_remote_verification_is_idempotent(self):
        for original in ["# Allow crawling\n", "# Allow crawling\nSitemap: https://alpha.test/sitemap.xml\n"]:
            with self.subTest(original=original):
                text = deploy.block_ai_robots(original)
                self.assertTrue(text.startswith(original))
                self.assertEqual(deploy.block_ai_robots(text), text)

    def test_selected_groups_are_replaced_while_shared_search_rules_and_sitemap_survive(self):
        for agents in [("GPTBot", "Googlebot"), ("Googlebot", "GPTBot")]:
            with self.subTest(agents=agents):
                original = ("User-agent: *\nDisallow: /admin/\n\n"
                            "User-agent: gPtBoT # old policy\nAllow: /assets/\n\n"
                            + "\n".join(f"User-agent: {agent}" for agent in agents)
                            + "\nAllow: /assets/\nDisallow: /private/\nSitemap: https://alpha.test/sitemap.xml\n")
                text = deploy.block_ai_robots(original)
                robots = RobotFileParser()
                robots.parse(text.splitlines())
                for bot in deploy.AI_BOTS:
                    self.assertFalse(robots.can_fetch(bot, "https://alpha.test/assets/game.js"))
                self.assertTrue(robots.can_fetch("Googlebot", "https://alpha.test/assets/game.js"))
                self.assertFalse(robots.can_fetch("Googlebot", "https://alpha.test/private/data"))
                self.assertFalse(robots.can_fetch("UnknownBot", "https://alpha.test/admin/"))
                self.assertEqual(robots.site_maps(), ["https://alpha.test/sitemap.xml"])

    def test_final_empty_group_does_not_inherit_the_added_ai_deny_rule(self):
        text = deploy.block_ai_robots("User-agent: Googlebot\nSitemap: https://alpha.test/sitemap.xml\n")
        robots = RobotFileParser()
        robots.parse(text.splitlines())
        self.assertTrue(robots.can_fetch("Googlebot", "https://alpha.test/assets/game.js"))
        self.assertFalse(robots.can_fetch("GPTBot", "https://alpha.test/assets/game.js"))


class ResolveUsernameTests(unittest.TestCase):
    """A lista de sites da Hostinger é paginada; o site pode estar depois da primeira página."""

    def fake_cli(self, pages, per_page=2):
        calls = []

        def cli(*args):
            calls.append(args)
            page = int(args[args.index("--page") + 1])
            total = sum(len(p) for p in pages)
            return {"data": pages[page - 1] if page <= len(pages) else [],
                    "meta": {"current_page": page, "per_page": per_page, "total": total}}
        return cli, calls

    def test_finds_site_on_a_later_page_filtering_by_domain(self):
        cli, calls = self.fake_cli([[{"domain": "central.example.com", "username": "a"},
                                     {"domain": "arena.example.com", "username": "a"}],
                                    [{"domain": "war.example.com", "username": "u1"}]])
        with mock.patch.object(deploy, "cli", cli):
            self.assertEqual(deploy.resolve_username("war.example.com"), "u1")
        self.assertEqual(len(calls), 2)
        self.assertIn("--domain", calls[0])

    def test_substring_match_is_not_accepted(self):
        cli, calls = self.fake_cli([[{"domain": "central.example.com", "username": "a"}]])
        with mock.patch.object(deploy, "cli", cli), self.assertRaises(SystemExit):
            deploy.resolve_username("example.com")
        self.assertEqual(len(calls), 1)


class ExpectTests(unittest.TestCase):
    """Nada vai para a Hostinger sem a configuração pública declarada."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "games/alpha"
        (self.project / "dist/assets").mkdir(parents=True)
        (self.project / "dist/index.html").write_text("<title>x</title>")
        (self.project / "dist/assets/a.js").write_text('const e={VITE_API:"https://api.test"};')
        (self.root / "workspace.json").write_text(json.dumps({"modules": [{"id": "alpha", "path": "games/alpha",
            "deploy": {"domain": "alpha.test", "env": {"VITE_API": None, "FIXO": "1"}}}]}))

    def run_main(self, *extra, root=None):
        argv = ["--domain", "alpha.test", "--project", str(self.project), "--dry-run", *extra]
        with mock.patch.dict(deploy.os.environ, {"GAMES_WORKSPACE_ROOT": str(root or self.root)}), \
                mock.patch.object(deploy, "make_zip", wraps=deploy.make_zip) as zipped, \
                mock.patch("builtins.print"):
            deploy.os.environ.pop("VITE_API", None)
            return deploy.main(argv), zipped.called

    def test_build_without_the_expected_value_is_refused_before_the_zip(self):
        self.assertEqual(self.run_main("--expect", "VITE_API=https://outra.test"), (3, False))
        self.assertEqual(self.run_main("--expect", "VITE_API=https://api.test"), (0, True))

    def test_npm_shortcut_reads_the_declaration_and_the_project_env_files(self):
        self.assertEqual(deploy.declared_expectations("alpha.test", self.project, str(self.root)), ({}, ["VITE_API"]))
        self.assertEqual(self.run_main(), (3, False))
        (self.project / ".env.local").write_text("VITE_API=https://api.test\n")
        self.assertEqual(deploy.declared_expectations("alpha.test", self.project, str(self.root)),
                         ({"VITE_API": "https://api.test"}, []))
        self.assertEqual(self.run_main(), (0, True))
        (self.project / ".env.local").write_text("VITE_API=https://outra.test\n")
        self.assertEqual(self.run_main(), (3, False))

    def test_without_the_hub_wrapper_the_workspace_is_found_above_the_project(self):
        with mock.patch.dict(deploy.os.environ):
            deploy.os.environ.pop("GAMES_WORKSPACE_ROOT", None)
            deploy.os.environ.pop("VITE_API", None)
            self.assertEqual(deploy.declared_expectations("alpha.test", self.project), ({}, ["VITE_API"]))

    def test_undeclared_domain_or_missing_workspace_checks_nothing(self):
        self.assertEqual(deploy.declared_expectations("outro.test", self.project, str(self.root)), ({}, []))
        self.assertEqual(self.run_main(root=self.root / "sem-workspace"), (0, True))

    def test_dry_run_accepts_a_project_root_build_with_ignored_htaccess(self):
        (self.project / "index.html").write_text("root-build")
        (self.project / ".htaccess").write_text("ignored")
        (self.project / ".vercelignore").write_text(".htaccess\n")
        self.assertEqual(self.run_main("--dist", ".", root=self.root / "sem-workspace"), (0, True))

    def test_direct_shortcut_inherits_ai_policy_even_with_explicit_public_values(self):
        manifest = self.root / "workspace.json"
        data = json.loads(manifest.read_text())
        data["modules"][0]["deploy"]["block_ai_bots"] = True
        manifest.write_text(json.dumps(data))
        with mock.patch.object(deploy, "make_zip", wraps=deploy.make_zip) as zipped:
            self.assertEqual(self.run_main("--expect", "VITE_API=https://api.test"), (0, True))
        self.assertTrue(zipped.call_args.kwargs["block_ai_bots"])

    def test_invalid_ai_policy_is_refused_before_packaging(self):
        manifest = self.root / "workspace.json"
        data = json.loads(manifest.read_text())
        data["modules"][0]["deploy"]["block_ai_bots"] = "false"
        manifest.write_text(json.dumps(data))
        with mock.patch.object(deploy, "make_zip") as zipped, mock.patch("sys.stderr"), self.assertRaises(SystemExit):
            self.run_main("--expect", "VITE_API=https://api.test")
        zipped.assert_not_called()

    def test_verify_only_checks_policy_without_comparing_original_robots_bytes(self):
        (self.project / "dist/robots.txt").write_text("User-agent: *\nDisallow: /admin/\n")
        with mock.patch.object(deploy, "verify", return_value=[]) as verify, \
                mock.patch.object(deploy, "verify_ai_bots", return_value=["assets are public"]) as bots, \
                mock.patch("builtins.print"):
            result = deploy.main(["--domain", "alpha.test", "--project", str(self.project),
                                  "--verify-only", "--block-ai-bots"])
        self.assertEqual(result, 2)
        self.assertNotIn("robots.txt", verify.call_args.args[2])
        bots.assert_called_once()


class BotVerificationTests(unittest.TestCase):
    def test_direct_asset_access_cannot_hide_behind_a_blocked_root(self):
        def fetch(domain, path, origin, user_agent="hostinger-deploy/2"):
            if path == "robots.txt":
                return 200, {}, deploy.block_ai_robots("").encode()
            return (403 if path == "/" else 200), {"cache-control": "no-store", "vary": "User-Agent"}, b""
        with mock.patch.object(deploy, "fetch", side_effect=fetch), mock.patch("builtins.print"):
            problems = deploy.verify_ai_bots("alpha.test", ["index.html", "assets/game.js"], None)
        self.assertEqual(len(problems), len(deploy.AI_BOTS))
        self.assertTrue(all("assets/game.js" in problem for problem in problems))

    def test_missing_robot_directives_are_reported(self):
        with mock.patch.object(deploy, "fetch", return_value=(403, {"cache-control": "no-store", "vary": "User-Agent"}, b"")), mock.patch("builtins.print"):
            problems = deploy.verify_ai_bots("alpha.test", ["index.html"], None)
        self.assertEqual(len(problems), 1)
        self.assertIn("robots.txt", problems[0])

    def test_cacheable_denials_are_not_accepted_as_verified_protection(self):
        body = deploy.block_ai_robots("").encode()
        def fetch(domain, path, origin, user_agent="hostinger-deploy/2"):
            return (200, {}, body) if path == "robots.txt" else (403, {"cache-control": "public"}, b"")
        with mock.patch.object(deploy, "fetch", side_effect=fetch), mock.patch("builtins.print"):
            problems = deploy.verify_ai_bots("alpha.test", ["index.html", "assets/game.js"], None)
        self.assertEqual(len(problems), len(deploy.AI_BOTS) * 2)
        self.assertTrue(all("no-store" in problem for problem in problems))

    def test_remote_robot_allow_groups_cannot_hide_behind_appended_denials(self):
        body = ("User-agent: GPTBot\nAllow: /assets/\n\n" + deploy.block_ai_robots("")).encode()
        def fetch(domain, path, origin, user_agent="hostinger-deploy/2"):
            return (200, {}, body) if path == "robots.txt" else (403, {"cache-control": "no-store", "vary": "User-Agent"}, b"")
        with mock.patch.object(deploy, "fetch", side_effect=fetch), mock.patch("builtins.print"):
            problems = deploy.verify_ai_bots("alpha.test", ["index.html"], None)
        self.assertEqual(len(problems), 1)
        self.assertIn("conflitantes", problems[0])


if __name__ == "__main__":
    unittest.main()
