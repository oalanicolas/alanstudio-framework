import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/game.py"
SPEC = importlib.util.spec_from_file_location("game_harness", SCRIPT)
game = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(game)


class HarnessTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="games-harness-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.project = self.root / "jogo com espaços"
        self.project.mkdir()
        (self.project / "core.py").write_text("state = 0\n")
        (self.project / "consumer.py").write_text("import core\n")
        self.plan = {
            "schema_version": 1, "project": str(self.project), "need": "Corrigir reinício que mantém estado anterior",
            "searches": ["rg 'state' core.py consumer.py → estado encontrado em core.py; consumidor lido"],
            "candidates": [{"path": str(self.project / "core.py"), "consumer": str(self.project / "consumer.py"), "fit": "Estado canônico; reset pode ser acrescentado aqui"}],
            "selected": str(self.project / "core.py"), "decision": "adapt", "why": "Preserva o consumidor atual",
            "change": ["core.py e teste de reinício"], "acceptance": ["reiniciar após ação retorna estado inicial"],
            "visual_reference": "Sem alteração visual nesta fixture de teste"
        }

    def package(self, **extra):
        data = {"scripts": {"test": "node --test"}, **extra}
        (self.project / "package.json").write_text(json.dumps(data))

    def test_discovery_finds_native_nested_and_web_without_vendored_noise(self):
        self.package()
        for name, marker in (("unity", "ProjectSettings/ProjectVersion.txt"), ("godot", "project.godot"), ("nested/web", "index.html"), ("node_modules/vendor", "package.json")):
            path = self.root / name / marker
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}")
        (self.root / "loop").symlink_to(self.root, target_is_directory=True)
        projects = game.discover(self.root)
        self.assertEqual({item["kind"] for item in projects}, {"package.json", "unity", "godot", "static-web"})
        self.assertEqual(len(projects), 4)

    def test_context_loads_selected_recipe_and_never_executes_declared_script(self):
        self.package(scripts={"test": "touch should-not-exist"})
        (self.root / "AGENTS.md").write_text("root")
        (self.project / "AGENTS.md").write_text("local")
        before = set(self.project.iterdir())
        result = game.context(self.project, "visual")
        self.assertEqual(before, set(self.project.iterdir()))
        self.assertEqual(result["instructions"][-2:], [str(self.root / "AGENTS.md"), str(self.project / "AGENTS.md")])
        self.assertEqual([Path(p).name for p in result["read_next"]], ["process.md", "quality.md", "visual.md"])
        self.assertTrue(result["capabilities"])
        self.assertTrue(all(item["status"] in ("unknown", "mentioned") for item in result["capabilities"].values()))
        self.assertTrue(all(item["status"] != "verified" for item in result["capabilities"].values()))

    def test_context_lists_focus_studies_without_loading_other_catalogs(self):
        studies = self.root / "Games-Frameworks"
        phaser = studies / "outputs/decoded/games-phaser/study-02d8931b626d/validate/rule-catalog.md"
        bmad = studies / "outputs/decoded/games-bmad-game-dev-studio/study-2486f5f5f3b8/validate/rule-catalog.md"
        phaser.parent.mkdir(parents=True)
        bmad.parent.mkdir(parents=True)
        phaser.write_text("phaser")
        bmad.write_text("bmad")
        result = game.context(self.project, "lifecycle", studies_root=studies)
        self.assertEqual(result["studies"], [str(phaser)])
        self.assertNotIn(str(bmad), result["studies"])
        missing = game.context(self.project, "lifecycle", studies_root=self.root / "absent")
        self.assertEqual(missing["studies"], [])

    def test_context_records_local_mentions_and_never_marks_them_verified(self):
        (self.project / "game.test.mjs").write_text("test('pause and restart keep the story', () => {})\n")
        result = game.context(self.project, "lifecycle", studies_root=self.root / "absent")
        self.assertEqual(result["capabilities"]["pause"]["status"], "mentioned")
        self.assertEqual(result["capabilities"]["pause"]["path"], "game.test.mjs")
        self.assertEqual(result["capabilities"]["reset"]["status"], "mentioned")
        self.assertEqual(result["capabilities"]["seed"]["status"], "unknown")
        self.assertNotIn("path", result["capabilities"]["seed"])
        self.assertTrue(all(item["status"] != "verified" for item in result["capabilities"].values()))

    def test_context_accepts_new_game_without_creating_it(self):
        target = self.root / "novo"
        result = game.context(target, "create")
        self.assertFalse(result["exists"])
        self.assertEqual(result["scripts"], {})
        self.assertFalse(target.exists())

    def test_stage_context_finds_existing_design_without_loading_other_templates(self):
        (self.project / "production").mkdir()
        existing = self.project / "production/gdd.md"
        existing.write_text("design canônico em andamento")
        result = game.context(self.project, "mechanics", "gdd")
        self.assertIn(str(existing), result["records"])
        templates = [Path(path).name for path in result["read_next"] if "templates" in Path(path).parts]
        self.assertEqual(templates, ["gdd.md"])
        self.assertEqual(existing.read_text(), "design canônico em andamento")

    def test_stage_context_accepts_documents_combined_or_at_root(self):
        (self.project / "docs").mkdir()
        for relative in ("GDD.md", "PRD.md", "TDD.md", "docs/game-design.md"):
            (self.project / relative).write_text("existing decisions")
        result = game.context(self.project, "create", "prd")
        for relative in ("GDD.md", "PRD.md", "TDD.md", "docs/game-design.md"):
            self.assertIn(str(self.project / relative), result["records"])

    def test_template_cli_renders_every_artifact_as_draft_in_new_files(self):
        target = self.root / "new-game"
        for stage in game.STAGES:
            output = self.root / "planning" / f"{stage}.md"
            result = subprocess.run([sys.executable, str(SCRIPT), "template", stage, "--project", str(target), "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = json.loads(result.stdout)
            self.assertEqual(receipt["status"], "draft")
            self.assertEqual(Path(receipt["document"]), output)
            self.assertIn(str(target), output.read_text())
            self.assertNotIn("{{PROJECT", output.read_text())
        self.assertFalse(target.exists())

    def test_template_preview_does_not_write_or_create_project(self):
        target = self.root / "new-game"
        before = set(self.root.iterdir())
        result = subprocess.run([sys.executable, str(SCRIPT), "template", "prd", "--project", str(target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(target), result.stdout)
        self.assertEqual(before, set(self.root.iterdir()))

    def test_template_preserves_existing_canonical_document(self):
        output = self.project / "PRD.md"
        output.write_text("decisão atual do usuário")
        with self.assertRaisesRegex(ValueError, "existente"):
            game.template("prd", self.project, output)
        self.assertEqual(output.read_text(), "decisão atual do usuário")

    def test_template_refuses_dangling_symlink(self):
        output = self.project / "PRD.md"
        target = self.root / "absent.md"
        output.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "existente"):
            game.template("prd", self.project, output)
        self.assertFalse(target.exists())

    def test_unknown_stage_cannot_escape_templates_or_write(self):
        target = self.root / "absent/design.md"
        with self.assertRaisesRegex(ValueError, "desconhecida"):
            game.template("../../SKILL", self.project, target)
        self.assertFalse(target.parent.exists())
        with self.assertRaisesRegex(ValueError, "desconhecida"):
            game.context(self.project, "create", "missing")

    def test_manager_respects_declaration_and_refuses_ambiguous_locks(self):
        self.package(packageManager="pnpm@10.0.0")
        (self.project / "package-lock.json").write_text("{}")
        self.assertEqual(game.package_commands(self.project)[1], "pnpm")
        self.package()
        (self.project / "yarn.lock").write_text("")
        self.assertIsNone(game.package_commands(self.project)[1])
        with self.assertRaisesRegex(ValueError, "ambíguo"):
            game.verify(self.project, ["test"], None, self.root / "evidence", 5)
        self.assertFalse((self.root / "evidence").exists())

    def test_missing_plan_fields_cannot_pass(self):
        self.assertTrue(game.check_plan({}, self.root))
        self.assertTrue(game.check_plan([], self.root))
        for key in ("need", "searches", "change", "acceptance", "visual_reference"):
            plan = copy.deepcopy(self.plan)
            del plan[key]
            self.assertTrue(game.check_plan(plan, self.root), key)

    def test_reuse_requires_existing_candidate_consumer_and_selection(self):
        self.assertEqual(game.check_plan(self.plan, self.root), [])
        for key in ("path", "consumer"):
            plan = copy.deepcopy(self.plan)
            plan["candidates"][0][key] = "missing.py"
            self.assertTrue(game.check_plan(plan, self.root))
        plan = {**self.plan, "selected": "missing.py"}
        self.assertTrue(game.check_plan(plan, self.root))

    def test_create_requires_explicit_gap_after_search(self):
        plan = {**self.plan, "decision": "create", "candidates": [], "selected": None}
        self.assertTrue(game.check_plan(plan, self.root))
        plan["gap"] = "Busca não encontrou sistema que represente a ação; estender o consumidor acoplaria estado de outro jogo"
        self.assertEqual(game.check_plan(plan, self.root), [])
        plan["searches"] = []
        self.assertTrue(game.check_plan(plan, self.root))

    def test_native_command_records_real_failure_and_log(self):
        report = game.verify(self.project, [], [sys.executable, "-c", "print('observed failure'); raise SystemExit(7)"], self.root / "evidence", 5)
        self.assertEqual(report["technical_status"], "failed")
        self.assertEqual(report["experience_status"], "not_assessed")
        self.assertEqual(report["commands"][0]["exit_code"], 7)
        self.assertIn("observed failure", (self.root / "evidence/01.log").read_text())
        self.assertEqual(game.read_json(self.root / "evidence/verification.json"), report)

    def test_success_preserves_literal_arguments_and_does_not_approve_experience(self):
        literal = "$(touch injected); `touch injected2`"
        report = game.verify(self.project, [], [sys.executable, "-c", "import sys; print(sys.argv[1])", literal], self.root / "evidence", 5)
        self.assertEqual(report["technical_status"], "passed")
        self.assertEqual(report["experience_status"], "not_assessed")
        self.assertEqual((self.root / "evidence/01.log").read_text().strip(), literal)
        self.assertFalse((self.project / "injected").exists())

    def test_timeout_is_failure_with_receipt(self):
        report = game.verify(self.project, [], [sys.executable, "-c", "import time; time.sleep(10)"], self.root / "evidence", 0.05)
        self.assertEqual(report["technical_status"], "failed")
        self.assertEqual(report["commands"][0]["exit_code"], 124)
        self.assertIn("Timeout", (self.root / "evidence/01.log").read_text())

    def test_missing_executable_is_failure(self):
        report = game.verify(self.project, [], [str(self.root / "no-executable")], self.root / "evidence", 5)
        self.assertEqual(report["commands"][0]["exit_code"], 127)
        self.assertEqual(report["technical_status"], "failed")

    def test_existing_evidence_is_not_overwritten(self):
        output = self.root / "evidence"
        output.mkdir()
        (output / "keep").write_text("original")
        with self.assertRaisesRegex(ValueError, "existente"):
            game.verify(self.project, [], [sys.executable, "--version"], output, 5)
        self.assertEqual((output / "keep").read_text(), "original")
        self.assertEqual(len(list(output.iterdir())), 1)

    def test_unknown_script_refuses_before_writing(self):
        self.package()
        with self.assertRaisesRegex(ValueError, "ausente"):
            game.verify(self.project, ["not-declared"], None, self.root / "evidence", 5)
        self.assertFalse((self.root / "evidence").exists())

    def test_scripts_execute_in_order_and_stop_on_first_failure(self):
        self.package(scripts={"first": "node -e \"process.exit(3)\"", "second": "node -e \"require('fs').writeFileSync('unexpected', 'bad')\""})
        report = game.verify(self.project, ["first", "second"], None, self.root / "evidence", 10)
        self.assertEqual(len(report["commands"]), 1)
        self.assertEqual(report["commands"][0]["exit_code"], 3)
        self.assertFalse((self.project / "unexpected").exists())

    def test_cli_returns_failure_and_receipt_for_failed_command(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "verify", str(self.project), "--output", str(self.root / "cli"), "--command", sys.executable, "-c", "raise SystemExit(4)"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["commands"][0]["exit_code"], 4)

    def test_cli_rejects_malformed_json_without_traceback(self):
        plan = self.root / "broken.json"
        plan.write_text("{")
        result = subprocess.run([sys.executable, str(SCRIPT), "check-plan", str(plan)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
