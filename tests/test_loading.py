import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/game.py"
SPEC = importlib.util.spec_from_file_location("game_harness_loading", SCRIPT)
game = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(game)


class LoadingTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="games-loading-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.project = self.root / "jogo com espaço"
        self.project.mkdir()
        env = patch.dict(os.environ, {"GAMES_WORKSPACE_ROOT": str(self.root)})
        env.start()
        self.addCleanup(env.stop)

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "loading", str(self.project), *args, "--root", str(self.root)],
            capture_output=True, text=True,
        )

    def test_cli_preserves_files_and_never_runs_declared_loading_or_build(self):
        marker = self.project / "executed.txt"
        command = shlex.join([sys.executable, "-c", "from pathlib import Path; Path('executed.txt').write_text('ran')"])
        manifest = self.project / "package.json"
        manifest.write_text(json.dumps({"scripts": {
            "loading": command, "qa:loading": command, "build": command,
            "qa:combat": "node combat.mjs", "bench:entry": command,
        }}), encoding="utf-8")
        before = manifest.read_bytes()
        result = self.cli("--scenario", "menu → primeiro controle")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["scenario"], "menu → primeiro controle")
        self.assertEqual(set(payload["scripts"]), {"loading", "qa:loading", "build", "bench:entry"})
        self.assertEqual(payload["scripts"]["loading"]["body"], command)
        self.assertEqual(manifest.read_bytes(), before)
        self.assertFalse(marker.exists())
        self.assertEqual(set(self.project.iterdir()), {manifest})
        for field in ("executed", "measured", "optimized"):
            self.assertFalse(payload[field])
        self.assertFalse(payload["budget"]["measured"])
        args = shlex.split(payload["context_command"])
        self.assertIn(str(self.project), args)
        self.assertEqual(args[-2:], ["--root", str(self.root)])
        self.assertTrue(all(Path(item).is_file() for item in payload["read_next"]))

    def test_unity_marker_and_missing_tools_do_not_invent_a_web_runtime_or_a_gain(self):
        settings = self.project / "ProjectSettings"
        settings.mkdir()
        (settings / "ProjectVersion.txt").write_text("m_EditorVersion: 6000.0\n", encoding="utf-8")
        result = game.loading_reading(self.project, self.root)
        self.assertEqual(result["kind"], "unity")
        self.assertEqual(result["scripts"], {})
        self.assertIsNone(result["scenario"])
        self.assertFalse(result["optimized"])
        self.assertFalse((self.project / "package.json").exists())

    def test_missing_project_is_explicit_and_does_not_create_it(self):
        absent = self.root / "ausente"
        result = game.loading_reading(absent, self.root)
        self.assertFalse(result["exists"])
        self.assertIsNone(result["kind"])
        self.assertFalse(absent.exists())

    def test_malformed_manifest_reports_error_without_replacing_it(self):
        manifest = self.project / "package.json"
        manifest.write_text("{ broken", encoding="utf-8")
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Erro:", result.stderr)
        self.assertEqual(manifest.read_text(encoding="utf-8"), "{ broken")


if __name__ == "__main__":
    unittest.main()
