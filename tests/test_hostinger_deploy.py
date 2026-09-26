"""Static Hostinger publishing: vercel.json translation, build resolution and archive contents."""
import importlib.util
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

    def test_htaccess_shipped_in_build_wins(self):
        dist = self.project / "dist"
        self.write("dist/index.html")
        self.write("dist/.htaccess", "# do build")
        out = self.project / "a.zip"
        deploy.make_zip(dist, "# gerado", out)
        with zipfile.ZipFile(out) as z:
            self.assertEqual(z.read(".htaccess"), b"# do build")

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
        cli, calls = self.fake_cli([[{"domain": "central.rabisco.net", "username": "a"},
                                     {"domain": "arena.rabisco.net", "username": "a"}],
                                    [{"domain": "war.rabisco.net", "username": "u1"}]])
        with mock.patch.object(deploy, "cli", cli):
            self.assertEqual(deploy.resolve_username("war.rabisco.net"), "u1")
        self.assertEqual(len(calls), 2)
        self.assertIn("--domain", calls[0])

    def test_substring_match_is_not_accepted(self):
        cli, calls = self.fake_cli([[{"domain": "central.rabisco.net", "username": "a"}]])
        with mock.patch.object(deploy, "cli", cli), self.assertRaises(SystemExit):
            deploy.resolve_username("rabisco.net")
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
