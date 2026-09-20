"""Behavior of the static delivery check, with real local HTTP responses."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
from pathlib import Path
import tempfile
from threading import Thread
import unittest

SPEC = importlib.util.spec_from_file_location("web_delivery", Path(__file__).resolve().parents[1] / "scripts/check_web_delivery.py")
delivery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(delivery)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class WebDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("index.html", '<script type="module" src="src/main.js"></script>')
        self.write("src/main.js", 'import "./rules.js"; new Audio("/sound.wav");')
        self.write("src/rules.js", 'export const value = 1;')
        self.write("sound.wav", 'fixture; HTTP verification does not decode audio')
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(self.root)))
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop)
        self.url = f"http://127.0.0.1:{self.server.server_port}/"

    def stop(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value)

    def test_follows_the_served_entrypoint_and_imported_resources(self):
        result = delivery.check(self.root, self.url)
        self.assertTrue(result["ok"])
        self.assertEqual(len(result["checks"]), 4)

    def test_reports_a_missing_sound_used_by_the_real_entrypoint(self):
        (self.root / "sound.wav").unlink()
        result = delivery.check(self.root, self.url)
        self.assertFalse(result["ok"])
        self.assertEqual(next(c for c in result["checks"] if c["url"].endswith("sound.wav"))["status"], 404)

    def test_checks_font_urls_inside_inline_css(self):
        self.write("index.html", '<style>@font-face{src:url(/fonts/hand.woff2)}</style>')
        self.assertFalse(delivery.check(self.root, self.url)["ok"])

    def test_refuses_another_projects_page_at_the_same_address(self):
        other = self.root / "other"
        self.write("other/index.html", '<h1>A different game</h1>')
        result = delivery.check(other, self.url)
        self.assertFalse(result["ok"])
        self.assertIn("entry differs", result["checks"][0]["error"])

    def test_does_not_load_external_assets(self):
        self.write("index.html", '<img src="https://example.invalid/hero.png">')
        result = delivery.check(self.root, self.url)
        self.assertEqual(result["skipped_external"], ["https://example.invalid/hero.png"])
        self.assertEqual(len(result["checks"]), 1)

    def test_stops_cycles_and_reports_an_incomplete_limit(self):
        self.write("src/rules.js", 'import "./main.js";')
        self.assertEqual(len(delivery.check(self.root, self.url)["checks"]), 4)
        self.assertFalse(delivery.check(self.root, self.url, limit=2)["ok"])

    def test_does_not_require_orphan_resources(self):
        self.write("orphan.js", 'new Audio("/missing.wav");')
        self.assertTrue(delivery.check(self.root, self.url)["ok"])

    def test_canvas_export_mime_is_not_a_css_resource_url(self):
        self.write("src/main.js", 'canvas.toDataURL("image/png");')
        result = delivery.check(self.root, self.url)
        self.assertTrue(result["ok"])
        self.assertEqual(len(result["checks"]), 2)

    def test_html_fallback_is_not_a_loaded_sound(self):
        original = QuietHandler.guess_type
        QuietHandler.guess_type = lambda handler, path: "text/html" if path.endswith("sound.wav") else original(handler, path)
        self.addCleanup(setattr, QuietHandler, "guess_type", original)
        result = delivery.check(self.root, self.url)
        sound = next(c for c in result["checks"] if c["url"].endswith("sound.wav"))
        self.assertEqual(sound["status"], 200)
        self.assertIn("returned HTML", sound["error"])


if __name__ == "__main__":
    unittest.main()
