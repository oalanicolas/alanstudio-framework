import copy
from functools import partial
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import zipfile


spec = importlib.util.spec_from_file_location("audio_catalog", Path(__file__).parents[1] / "scripts/audio.py")
audio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio)


class AudioCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "library"
        self.data = b"same source bytes"
        self.item = {
            "id": "passo-madeira-01", "title": "Passo em madeira", "category": "Passos",
            "tags": ["pé", "madeira"], "style": "recorded",
            "processing": "Corte do original; sem conversão adicional.",
            "sources": [{"title": "Original Footstep", "author": "Autora",
                         "url": "https://example.com/source", "license": "CC-BY-4.0"}],
            "sha256": audio.digest(self.data), "bytes": len(self.data),
            "file": f"files/{audio.digest(self.data)}.wav",
            "technical": {"sample_rate": 44100, "duration": 1, "warnings": []},
        }
        audio.save_imports([(copy.deepcopy(self.item), self.data)], self.root)

    def test_duplicates_reuse_bytes_but_preserve_authors_and_aliases(self):
        other = copy.deepcopy(self.item)
        other["id"] = "outro-passo"
        other["sources"][0]["author"] = "Outra autora"
        other["processing"] = "Histórico adicional de edição."
        result = audio.save_imports([(other, self.data)], self.root)
        self.assertEqual(result["total"], 1)
        self.assertEqual(len(list((self.root / "files").iterdir())), 1)
        sounds = audio.load_catalog(self.root)["sounds"]
        self.assertEqual(audio.select(sounds, ["outro-passo"])[0]["id"], self.item["id"])
        self.assertEqual(len(sounds[0]["sources"]), 2)
        self.assertIn("Histórico adicional de edição.", sounds[0]["processing_history"])

    def test_changed_id_aborts_before_writing_any_file(self):
        before = (self.root / "catalog.json").read_bytes()
        conflict = copy.deepcopy(self.item)
        conflict["sha256"] = "0" * 64
        new = copy.deepcopy(self.item)
        new.update(id="new-clip", sha256="1" * 64, file="files/" + "1" * 64 + ".wav")
        with self.assertRaisesRegex(ValueError, "ID já usado"):
            audio.save_imports([(new, b"new"), (conflict, b"changed")], self.root)
        self.assertEqual((self.root / "catalog.json").read_bytes(), before)
        self.assertEqual(len(list((self.root / "files").iterdir())), 1)

    def test_search_accents_and_combined_terms(self):
        sounds = audio.load_catalog(self.root)["sounds"]
        self.assertEqual(len(audio.search(sounds, "pe madeira")), 1)
        self.assertEqual(audio.search(sounds, "madeira metal"), [])
        self.assertEqual(audio.search(sounds, license_id="CC0-1.0"), [])

    def test_retro_and_unlicensed_input_rejected(self):
        for key, value in [("style", "chiptune"), ("title", "8-bit click")]:
            item = copy.deepcopy(self.item)
            item[key] = value
            with self.assertRaises(ValueError):
                audio.validate_metadata(item)
        item = copy.deepcopy(self.item)
        item["sources"][0]["license"] = "unknown"
        with self.assertRaisesRegex(ValueError, "licença"):
            audio.validate_metadata(item)

    def test_select_missing_id_fails(self):
        with self.assertRaisesRegex(ValueError, "desconhecidos"):
            audio.select([self.item], [self.item["id"], "missing"])

    def test_export_preserves_bytes_attribution_and_history(self):
        destination = Path(self.temp.name) / "game/public/audio"
        result = audio.export_files([self.item], destination, self.root)
        self.assertEqual(result["status"], "exported")
        self.assertEqual((destination / "passo-madeira-01.wav").read_bytes(), self.data)
        credits = (destination / "CREDITS.txt").read_text()
        for expected in ["Autora", "Original Footstep", "https://example.com/source",
                         "https://creativecommons.org/licenses/by/4.0/", "Corte do original"]:
            self.assertIn(expected, credits)
        self.assertEqual(audio.export_files([self.item], destination, self.root)["status"], "already_exported")

    def test_export_conflict_does_not_touch_existing_game(self):
        destination = Path(self.temp.name) / "game/audio"
        destination.mkdir(parents=True)
        (destination / "keep.wav").write_bytes(b"user work")
        with self.assertRaisesRegex(ValueError, "pasta nova"):
            audio.export_files([self.item], destination, self.root)
        self.assertEqual(list(destination.iterdir()), [destination / "keep.wav"])
        self.assertEqual((destination / "keep.wav").read_bytes(), b"user work")

    def test_export_corrupt_sound_fails_before_creating_destination(self):
        (self.root / self.item["file"]).write_bytes(b"corrupt")
        destination = Path(self.temp.name) / "game/audio"
        with self.assertRaisesRegex(ValueError, "Integridade"):
            audio.export_files([self.item], destination, self.root)
        self.assertFalse(destination.exists())
        self.assertFalse(audio.check(self.root)["ok"])

    def test_paths_and_library_export_are_bounded(self):
        for path in ["../secret", str(Path(self.temp.name) / "secret")]:
            with self.assertRaises(ValueError):
                audio.inside(self.root, path)
        with self.assertRaises(ValueError):
            audio.export_files([self.item], self.root / "files", self.root)

    def test_http_preview_ranges_zip_and_no_workspace_exposure(self):
        server = audio.ThreadingHTTPServer(("127.0.0.1", 0), partial(audio.CatalogHandler, root=self.root))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        base = f"http://127.0.0.1:{server.server_port}"
        request = Request(base + "/" + self.item["file"], headers={"Range": "bytes=2-5"})
        with urlopen(request, timeout=5) as response:
            self.assertEqual(response.status, 206)
            self.assertEqual(response.read(), self.data[2:6])
            self.assertEqual(response.headers["Content-Type"], "audio/wav")
        request = Request(base + "/" + self.item["file"], headers={"Range": "bytes=-4"})
        with urlopen(request, timeout=5) as response:
            self.assertEqual(response.read(), self.data[-4:])
        for route in ["/files/../../AGENTS.md", "/selection.json", "/.env", "/files/"]:
            with self.assertRaises(HTTPError) as error:
                urlopen(base + route, timeout=5)
            self.assertEqual(error.exception.code, 404)
            error.exception.close()
        with urlopen(base + "/export?ids=" + self.item["id"], timeout=5) as response:
            with zipfile.ZipFile(io.BytesIO(response.read())) as archive:
                self.assertEqual(archive.read("passo-madeira-01.wav"), self.data)
                manifest = json.loads(archive.read("manifest.json"))
                self.assertEqual(manifest["files"][0]["src"], "passo-madeira-01.wav")
                self.assertIn(b"Autora", archive.read("CREDITS.txt"))

    def test_http_preview_page_lists_sounds_without_claiming_to_hear_them(self):
        self.assertFalse((self.root / "ui" / "index.html").exists())
        page = audio.preview_page(self.root).decode()
        self.assertIn(self.item["id"], page)
        self.assertIn(self.item["file"], page)
        self.assertIn("<audio", page)
        self.assertIn("não é mix", page.casefold())
        self.assertNotIn("aprovado", page)
        self.assertNotIn("verified", page)
        server = audio.ThreadingHTTPServer(("127.0.0.1", 0), partial(audio.CatalogHandler, root=self.root))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        base = f"http://127.0.0.1:{server.server_port}"
        with urlopen(base + "/", timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("text/html", response.headers.get("Content-Type", ""))
            listed = response.read().decode()
        self.assertIn(self.item["id"], listed)
        self.assertIn("<audio", listed)
        self.assertNotIn("aprovado", listed)
        self.assertNotIn("verified", listed)
        with self.assertRaises(HTTPError) as error:
            urlopen(base + "/catalog.js", timeout=5)
        self.assertEqual(error.exception.code, 404)
        error.exception.close()

    def test_preview_names_the_catalog_sound_the_disk_lost(self):
        lost = self.root / self.item["file"]
        self.assertTrue(lost.is_file())
        lost.unlink()
        page = audio.preview_page(self.root).decode()
        self.assertIn(self.item["id"], page)
        self.assertIn("o disco perdeu", page.casefold())
        self.assertNotIn("<audio", page)
        self.assertNotIn("aprovado", page)
        self.assertNotIn("verified", page)
        self.assertFalse(audio.catalog_bytes_present(self.root, self.item["file"]))


if __name__ == "__main__":
    unittest.main()
