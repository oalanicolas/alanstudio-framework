"""Static Hostinger publishing: vercel.json translation, build resolution and archive contents."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
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

    def test_ai_bot_block_goes_on_top_of_the_shipped_htaccess_and_extends_robots(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        self.write("dist/.htaccess", "# do build\n")
        self.write("dist/robots.txt", "User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nDisallow: /\n")
        out = self.project / "a.zip"
        self.assertEqual(deploy.make_zip(dist, "# gerado", out, block_ai_bots=True), 3)
        with zipfile.ZipFile(out) as z:
            names = z.namelist()
            htaccess, robots = z.read(".htaccess").decode(), z.read("robots.txt").decode()
        self.assertEqual(sorted(names), [".htaccess", "index.html", "robots.txt"])
        self.assertTrue(htaccess.startswith("# Robôs de IA"))
        self.assertTrue(htaccess.endswith("# do build\n"))
        self.assertLess(htaccess.index("RewriteRule !^robots\\.txt$ - [F,L]"), htaccess.index("# do build"))
        for agent in deploy.AI_BOTS:
            self.assertIn(agent, htaccess)
            self.assertEqual(robots.count(f"User-agent: {agent}\nDisallow: /"), 1, agent)
        self.assertTrue(robots.startswith("User-agent: *\nAllow: /\n"))

    def test_ai_bot_block_without_shipped_files_uses_the_generated_htaccess(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        out = self.project / "a.zip"
        self.assertEqual(deploy.make_zip(dist, "# gerado", out, block_ai_bots=True), 3)
        with zipfile.ZipFile(out) as z:
            self.assertTrue(z.read(".htaccess").decode().endswith("# gerado"))
            self.assertEqual(z.read("robots.txt").decode(),
                             "\n\n".join(f"User-agent: {a}\nDisallow: /" for a in deploy.AI_BOTS) + "\n")
        deploy.make_zip(dist, "# gerado", out)
        with zipfile.ZipFile(out) as z:
            self.assertNotIn("robots.txt", z.namelist())
            self.assertEqual(z.read(".htaccess"), b"# gerado")

    def test_ai_bot_check_wants_403_no_store_and_robots_for_every_agent(self):
        def served(blocked):
            def fetch(domain, path, origin, agent="x"):
                if path == "robots.txt":
                    return 200, {}, deploy.ai_bots_robots().encode()
                name = next((a for a in deploy.AI_BOTS if a in agent), None)
                return (403, {"cache-control": "no-store"}, b"") if name in blocked else (200, {}, b"ok")
            return fetch
        with mock.patch("builtins.print"):
            with mock.patch.object(deploy, "fetch", served(set(deploy.AI_BOTS))):
                self.assertEqual(deploy.verify_ai_bots("a.test", None), [])
            with mock.patch.object(deploy, "fetch", served(set(deploy.AI_BOTS) - {"ClaudeBot"})):
                self.assertEqual(deploy.verify_ai_bots("a.test", None), ["ClaudeBot: / respondeu 200, esperado 403"])

    def test_sample_starts_with_index_and_spreads(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        for i in range(20):
            self.write(f"dist/assets/{i:02}.js")
        picked = deploy.sample(deploy.build_files(dist), dist, 4)
        self.assertEqual(picked[0], "index.html")
        self.assertEqual(len(picked), 5)
        self.assertEqual(len(set(picked)), 5)


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


if __name__ == "__main__":
    unittest.main()
