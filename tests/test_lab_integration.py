import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/game.py"
SPEC = importlib.util.spec_from_file_location("lab_harness", SCRIPT)
game = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(game)


class LabIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="optional-game-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / "games/existing"
        self.project.mkdir(parents=True)
        (self.root / "workspace.json").write_text(json.dumps({
            "version": 1,
            "modules": [{"id": "existing", "path": "games/existing",
                         "repository": "games-existing"}],
        }))

    def test_uninitialized_module_requests_download_without_documenting_or_recreating(self):
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        payload = game.context(self.project, "feel", root=self.root)
        self.assertEqual(payload["workspace_module"]["state"], "not_downloaded")
        self.assertFalse(payload["foundation"]["audit"]["required"])
        self.assertEqual(payload["documentation"]["action"], "obtain_workspace_module")
        proposal = game.next_step(self.project, "feel")["proposal"]
        self.assertEqual(proposal["basis"], "workspace_module.not_downloaded")
        self.assertIn("get existing", proposal["commands"][0])
        with self.assertRaisesRegex(ValueError, "módulo opcional"):
            game.init(self.project, "canvas-arcade")
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*")))

    def test_present_module_keeps_local_work_and_combines_packages_with_local_workflows(self):
        (self.project / ".git").write_text("gitdir: ../../.git/modules/existing\n")
        (self.project / "package.json").write_text('{"name":"existing","scripts":{}}')
        marker = self.project / "work-in-progress.txt"
        marker.write_text("unfinished user work")
        payload = game.context(self.project, "feel", event="initialize", genre="casual")
        self.assertEqual(payload["workspace_module"]["state"], "present")
        self.assertEqual(payload["documentation"]["action"], "audit_and_document")
        self.assertEqual(Path(payload["packs"]["platform"]["pack"]).name, "web.md")
        self.assertEqual(Path(payload["packs"]["genre"]["pack"]).name, "casual.md")
        self.assertTrue(payload["finish"]["core_groups"])
        self.assertEqual(payload["delivery_review"]["status"], "pending_agent_review")
        self.assertEqual(payload["continuity"]["prompt"]["policy"], "generate_when_defined")
        self.assertEqual(marker.read_text(), "unfinished user work")

    def write_modules(self, *modules):
        (self.root / "workspace.json").write_text(json.dumps({"version": 1, "modules": list(modules)}))
        for module in modules:
            (self.root / module["path"]).mkdir(parents=True, exist_ok=True)

    def test_project_resolves_by_id_folder_alias_and_suggests_on_typo(self):
        self.write_modules(
            {"id": "existing", "path": "games/existing", "repository": "games-existing"},
            {"id": "egg-raid", "path": "prototypes/egg-raid", "repository": "egg-raid",
             "aliases": ["steal the egg", "raid"]},
            {"id": "library-egg-raid", "path": "libraries/egg-raid", "repository": "library-egg-raid"},
        )
        path, resolution = game.resolve_project("games/existing", self.root)
        self.assertEqual(path, self.project)
        self.assertIsNone(resolution)
        for value in ("egg-raid", "Steal The Egg", "/protos/raid"):
            with self.subTest(value=value):
                path, resolution = game.resolve_project(value, self.root)
                self.assertEqual(path, self.root / "prototypes/egg-raid")
                self.assertEqual(resolution["module"], "egg-raid")
        path, resolution = game.resolve_project("eg-raid", self.root)
        self.assertFalse(path.exists())
        self.assertIsNone(resolution["module"])
        self.assertIn("prototypes/egg-raid", resolution["candidates"])

    def test_brief_context_prints_a_screen_and_writes_the_full_json(self):
        self.write_modules({"id": "existing", "path": "games/existing", "repository": "games-existing",
                            "aliases": ["the existing game"]})
        (self.project / "package.json").write_text('{"name":"existing","scripts":{"test":"node --test"}}')
        out = self.root / "full.json"
        run = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), "context",
                              "the existing game", "--brief", "--out", str(out)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        brief = json.loads(run.stdout)
        full = json.loads(out.read_text())
        self.assertEqual(brief["project"], "games/existing")
        self.assertEqual(brief["resolution"]["module"], "existing")
        self.assertEqual(brief["full"], "full.json")
        self.assertEqual(brief["scripts"], "test")
        self.assertIn("foundation", full)
        self.assertNotIn("foundation", brief)
        self.assertLess(len(run.stdout), len(out.read_text()) / 3)

    def test_unregistered_new_game_still_uses_the_starter(self):
        new_game = self.root / "games/new-game"
        self.assertIsNone(game.workspace_module(new_game))
        game.init(new_game, "canvas-arcade")
        self.assertTrue((new_game / "package.json").is_file())


if __name__ == "__main__":
    unittest.main()
