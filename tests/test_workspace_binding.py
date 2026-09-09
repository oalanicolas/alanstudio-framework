import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


CORE = Path(__file__).resolve().parents[1]


class WorkspaceBindingTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bound workspace ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.workspace = self.base / "laboratorio"
        self.framework = self.workspace / "framework"
        self.scripts = self.framework / "scripts"
        self.scripts.mkdir(parents=True)
        self.launcher = self.scripts / "game.py"
        shutil.copy2(CORE / "assets/workspace/game.py", self.launcher)
        (self.framework / "core").symlink_to(CORE, target_is_directory=True)
        self.project = self.workspace / "games/demo"
        self.project.mkdir(parents=True)
        (self.project / "package.json").write_text('{"name":"demo","scripts":{}}')
        (self.workspace / "AGENTS.md").write_text("Preserve a direção deste laboratório.\n")
        self.workflow = self.workspace / "docs/workflow.md"
        self.workflow.parent.mkdir()
        self.workflow.write_text("Regra específica do laboratório.\n")
        (self.framework / "config.json").write_text(json.dumps({
            "version": 1, "context_files": ["docs/workflow.md"],
        }))
        self.env = {key: value for key, value in os.environ.items() if key != "GAMES_WORKSPACE_ROOT"}

    def run_cli(self, *args, script=None):
        return subprocess.run([sys.executable, str(script or self.launcher), *map(str, args)],
                              cwd=self.base, env=self.env, capture_output=True, text=True)

    def test_launcher_uses_central_packages_and_local_context_from_another_directory(self):
        result = self.run_cli("context", "games/demo", "--focus", "feel", "--genre", "casual")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["project"], str(self.project))
        self.assertEqual(data["packs"]["platform"]["pack"], str(CORE / "packs/platforms/web.md"))
        self.assertEqual(data["packs"]["genre"]["pack"], str(CORE / "packs/genres/casual.md"))
        self.assertIn(str(self.workflow), data["read_next"])
        self.assertIn(str(self.workspace / "AGENTS.md"), data["instructions"])
        self.assertEqual(data["studio_assets"]["sfx"]["catalog"], str(self.workspace / "shared/sfx/catalog.json"))
        self.assertEqual(data["workspace"]["context_files"], [str(self.workflow)])

    def test_suggested_command_keeps_workspace_when_run_without_the_launcher(self):
        result = self.run_cli("next", "games/demo", "--focus", "feel")
        self.assertEqual(result.returncode, 0, result.stderr)
        command = shlex.split(json.loads(result.stdout)["context_command"])
        command[0] = sys.executable
        rerun = subprocess.run(command, cwd=self.base, env=self.env, capture_output=True, text=True)
        self.assertEqual(rerun.returncode, 0, rerun.stderr)
        self.assertEqual(json.loads(rerun.stdout)["workspace"]["root"], str(self.workspace))

    def test_verify_runs_in_the_game_and_writes_only_the_requested_receipt(self):
        proof = self.workspace / "proof"
        result = self.run_cli("verify", "games/demo", "--output", proof, "--command",
                              sys.executable, "-c", "from pathlib import Path; print(Path.cwd())")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["technical_status"], "passed")
        self.assertEqual(data["project"], str(self.project))
        self.assertIn(str(self.project), (proof / "01.log").read_text())
        self.assertFalse((CORE / "proof").exists())

    def test_audio_commands_keep_the_local_catalog_when_run_elsewhere(self):
        result = self.run_cli("sfx", "summary")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["catalog"], str(self.workspace / "shared/sfx/catalog.json"))
        for key in ("search", "listen", "copy"):
            command = shlex.split(data[key])
            self.assertEqual(command[command.index("--root") + 1], str(self.workspace))
        command = shlex.split(data["search"])
        command[0], command[-1] = sys.executable, "passos"
        rerun = subprocess.run(command, cwd=self.base, env=self.env, capture_output=True, text=True)
        self.assertEqual(rerun.returncode, 0, rerun.stderr)
        self.assertEqual(json.loads(rerun.stdout)["count"], 0)

    def test_changes_at_the_single_source_are_used_without_copying_again(self):
        alternate = self.base / "shared-core"
        (alternate / "scripts").mkdir(parents=True)
        (self.framework / "core").unlink()
        (self.framework / "core").symlink_to(alternate, target_is_directory=True)
        source = alternate / "scripts/game.py"
        for value in ("first", "updated"):
            source.write_text(f'print({value!r})\n')
            result = self.run_cli()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), value)

    def test_missing_core_fails_without_creating_another_copy(self):
        (self.framework / "core").unlink()
        result = self.run_cli("context", "games/demo")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Framework compartilhado ausente", result.stderr)
        self.assertFalse((self.framework / "core").exists())

    def test_explicit_root_overrides_the_launcher_default_in_followup_commands(self):
        other = self.base / "other-workspace"
        project = other / "games/second"
        project.mkdir(parents=True)
        (project / "package.json").write_text('{"name":"second","scripts":{}}')
        result = self.run_cli("next", "games/second", "--root", other)
        self.assertEqual(result.returncode, 0, result.stderr)
        command = shlex.split(json.loads(result.stdout)["context_command"])
        command[0] = sys.executable
        rerun = subprocess.run(command, cwd=self.base, env=self.env, capture_output=True, text=True)
        self.assertEqual(rerun.returncode, 0, rerun.stderr)
        self.assertEqual(json.loads(rerun.stdout)["workspace"]["root"], str(other))

    def test_local_reference_escape_is_rejected(self):
        (self.framework / "config.json").write_text(json.dumps({
            "version": 1, "context_files": ["../outside.md"],
        }))
        result = self.run_cli("context", "games/demo")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fora do workspace", result.stderr)


if __name__ == "__main__":
    unittest.main()
