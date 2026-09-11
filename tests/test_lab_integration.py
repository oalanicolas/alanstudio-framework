import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


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

    def test_context_names_the_fill_the_binding_already_refuses(self):
        guide = (game.FRAMEWORK / "references/workspace-binding.md").read_text(encoding="utf-8")
        self.assertTrue(
            game.binding_refuses_starter_fill(guide),
            "a ligação já recusa preencher pasta não baixada com o starter",
        )
        self.assertEqual(game.workspace_module_fill_source(), "references/workspace-binding.md")
        payload = game.context(self.project, "feel", root=self.root)
        item = payload["workspace_module"]
        self.assertIn(
            "preencher pasta não baixada com o starter",
            item["scope"],
            "o context copiava o estado e calava a recusa",
        )
        self.assertIn("(`preenchida`)", item["scope"])
        self.assertNotIn("preenchida", item)
        self.assertFalse(game.binding_refuses_starter_fill(""))
        with mock.patch.object(game, "workspace_module_fill_source", return_value=None):
            silent = game.context(self.project, "feel", root=self.root)
        self.assertNotIn("preencher pasta não baixada com o starter", silent["workspace_module"]["scope"])
        skill = (game.FRAMEWORK / "SKILL.md").read_text(encoding="utf-8")
        readme = (game.FRAMEWORK / "README.md").read_text(encoding="utf-8")
        recipe = (game.FRAMEWORK / "recipes/create.md").read_text(encoding="utf-8")
        self.assertIn("nomeia a preenchida que a ligação já recusa", guide)
        self.assertIn("nomeia a preenchida que a ligação já recusa", skill)
        self.assertIn("nomeia a preenchida que a ligação já recusa", readme)
        self.assertIn("nomeia a preenchida que a ligação já recusa", recipe)
        self.assertNotIn("verified", item["scope"])
        self.assertNotIn("preencher pasta não baixada com o starter", payload["scope"])
        self.assertNotIn("preencher pasta não baixada com o starter", payload["documentation"]["scope"])
        self.assertNotIn("preencher pasta não baixada com o starter", game.next_scope())
        self.assertIsNone(game.workspace_module(self.project, self.root).get("scope"))

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

    def test_unregistered_new_game_still_uses_the_starter(self):
        new_game = self.root / "games/new-game"
        self.assertIsNone(game.workspace_module(new_game))
        game.init(new_game, "canvas-arcade")
        self.assertTrue((new_game / "package.json").is_file())


if __name__ == "__main__":
    unittest.main()
