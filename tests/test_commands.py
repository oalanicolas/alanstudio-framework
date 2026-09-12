"""Sub-comandos da skill: catálogo, referências, SKILL.md, atalhos fixados e escala.

A skill passou a rotear por comando (craft, shape, critique, polish…), no modelo
da skill impeccable: o menu, os atalhos e a leitura de contexto precisam concordar
com os arquivos que existem, e o harness precisa recusar o que não conhece.
"""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/game.py"
SPEC = importlib.util.spec_from_file_location("game_harness_commands", SCRIPT)
game = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(game)

HEADING = re.compile(r"^##\s+(.*?)\s*$", re.MULTILINE)
# Cada referência de comando tem a mesma forma: o agente sabe onde procurar a
# entrada, a prova e o que não fazer, em qualquer comando.
REQUIRED_SECTIONS = ("Escala", "Avaliar", "Executar", "Verificar", "Nunca", "Entregar")


class CommandCatalogTest(unittest.TestCase):
    def setUp(self):
        self.catalog = game.command_catalog()
        self.names = list(self.catalog["commands"])

    def test_catalog_references_and_skill_table_agree(self):
        self.assertEqual(game.command_problems(), [])
        self.assertGreaterEqual(len(self.names), 20)
        for name in self.names:
            self.assertTrue((game.FRAMEWORK / f"commands/{name}.md").is_file(), name)

    def test_every_command_uses_a_known_category_focus_and_reading(self):
        for name, entry in self.catalog["commands"].items():
            with self.subTest(command=name):
                self.assertIn(entry["category"], self.catalog["categories"])
                self.assertTrue(entry["description"].strip())
                self.assertTrue(entry["argument_hint"].strip())
                self.assertTrue(set(entry["foci"]) <= set(game.FOCI), entry["foci"])
                self.assertTrue(entry["reads"], "um comando sem leitura canônica duplicaria conteúdo em vez de apontá-lo")
        self.assertEqual(set(self.catalog["categories"]), {"build", "evaluate", "refine", "enhance", "fix", "produce"})

    def test_every_reference_has_the_shared_shape_and_points_at_canon(self):
        for name, entry in self.catalog["commands"].items():
            text = (game.FRAMEWORK / f"commands/{name}.md").read_text(encoding="utf-8")
            headings = [heading.split("(")[0].strip() for heading in HEADING.findall(text)]
            with self.subTest(command=name):
                for section in REQUIRED_SECTIONS:
                    self.assertTrue(any(h.startswith(section) for h in headings), f"{name} sem seção {section}: {headings}")
                for relative in entry["reads"]:
                    self.assertIn(Path(relative).name, text, f"{name} não aponta {relative}")
                # Nenhuma referência de comando pode conceder o que o harness recusa.
                self.assertNotIn("verified", text.casefold().replace("não é `verified`", "").replace("claimed` não é verified", ""))

    def test_skill_carries_setup_laws_bans_and_routing(self):
        text = (game.FRAMEWORK / "SKILL.md").read_text(encoding="utf-8")
        for marker in ("## Preparação", "## Leis compartilhadas", "## Recusas absolutas", "## Comandos", "### Regras de roteamento", "## Fixar e desafixar"):
            self.assertIn(marker, text, marker)
        for scale in game.SCALES:
            self.assertIn(f"`{scale}`", text)
        # Cada categoria do catálogo aparece como grupo na tabela.
        for label in self.catalog["categories"].values():
            self.assertIn(label, text)

    def test_readme_documents_the_commands_and_the_pin(self):
        text = (game.FRAMEWORK / "README.md").read_text(encoding="utf-8")
        self.assertIn("commands/commands.json", text)
        for name in ("pin", "unpin", "commands", "--scale"):
            self.assertIn(f"`{name}`" if name != "--scale" else "`--scale`", text)


class CommandCliTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="games-commands-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        workspace = patch.dict(os.environ, {"GAMES_WORKSPACE_ROOT": str(self.root)})
        workspace.start()
        self.addCleanup(workspace.stop)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args, "--root", str(self.root)],
            capture_output=True, text=True, check=False,
        )

    def install_skill(self, harness):
        target = self.root / harness / "skills/game-dev/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text((game.FRAMEWORK / "SKILL.md").read_text(encoding="utf-8"), encoding="utf-8")
        return target.parent.parent

    def test_commands_lists_the_catalog_with_references_present(self):
        run = self.run_cli("commands")
        self.assertEqual(run.returncode, 0, run.stderr)
        payload = json.loads(run.stdout)
        names = [row["name"] for row in payload["commands"]]
        self.assertEqual(names, list(game.command_catalog()["commands"]))
        self.assertTrue(all(row["reference_present"] for row in payload["commands"]))
        self.assertEqual(payload["pinned_marker"], game.PIN_MARKER)

    def test_pin_writes_a_redirect_only_where_game_dev_is_installed(self):
        skills = self.install_skill(".claude")
        (self.root / ".agents").mkdir()  # host presente, skill ausente: não recebe atalho
        result = game.pin(self.root, "critique")
        pinned = skills / "critique/SKILL.md"
        self.assertEqual(game.pin_created_paths(result), [str(pinned)])
        self.assertEqual(result["invoke"], "/critique")
        self.assertFalse((self.root / ".agents/skills/critique").exists())
        text = pinned.read_text(encoding="utf-8")
        self.assertIn(game.PIN_MARKER, text)
        self.assertIn("name: critique", text)
        self.assertIn(str(game.FRAMEWORK / "commands/critique.md"), text)
        self.assertIn(str(game.FRAMEWORK / "SKILL.md"), text)
        # Fixar de novo é idempotente: sobrescreve o próprio atalho, sem duplicar.
        again = game.pin(self.root, "critique")
        self.assertEqual(game.pin_created_paths(again), [str(pinned)])

    def test_pin_created_names_the_copy_the_readme_already_refuses(self):
        readme = (game.FRAMEWORK / "README.md").read_text(encoding="utf-8")
        self.assertTrue(
            game.readme_refuses_pin_as_copying_skill(readme),
            "o README já recusa que o pin copie a skill",
        )
        self.assertEqual(game.pin_created_copy_source(), "README.md")
        skills = self.install_skill(".agents")
        own = skills / "polish/SKILL.md"
        own.parent.mkdir()
        own.write_text("---\nname: polish\n---\nskill própria do usuário\n", encoding="utf-8")
        empty = game.pin(self.root, "polish")
        self.assertEqual(empty["created"], [])
        self.assertEqual(game.pin_created_paths(empty), [])
        result = game.pin(self.root, "critique")
        pinned = skills / "critique/SKILL.md"
        item = result["created"]
        self.assertEqual(item["created"], [str(pinned)], "o pin já escreve o atalho neste chamado")
        self.assertEqual(item["created"], game.pin_created_paths(result))
        self.assertIn(
            "o pin copie a skill",
            item["scope"],
            "o pin relatava o created e calava a recusa",
        )
        self.assertIn("(`cópia`)", item["scope"])
        self.assertNotIn("cópia", item)
        self.assertEqual(result["invoke"], "/critique")
        self.assertFalse(game.readme_refuses_pin_as_copying_skill(""))
        with patch.object(game, "pin_created_copy_source", return_value=None):
            silent = game.pin(self.root, "feel")
        self.assertNotIn(
            "o pin copie a skill",
            silent["created"]["scope"],
        )
        skill = (game.FRAMEWORK / "SKILL.md").read_text(encoding="utf-8")
        guide = (game.FRAMEWORK / "commands/README.md").read_text(encoding="utf-8")
        self.assertIn("nomeia a cópia que o README já recusa", readme)
        self.assertIn("nomeia a cópia que o README já recusa", skill)
        self.assertIn("nomeia a cópia que o README já recusa", guide)
        self.assertNotIn("verified", item["scope"])
        self.assertNotIn("aprovado", item["scope"])
        self.assertNotIn("4.5", item["scope"])
        self.assertNotIn("o pin copie a skill", result["scope"])
        self.assertNotIn("o pin copie a skill", empty["skipped"][0]["scope"])
        self.assertNotIn("o pin copie a skill", game.unpin(self.root, "critique")["scope"])
        self.assertNotIn("o pin copie a skill", game.command_listing()["scope"])
        self.assertNotIn("o pin copie a skill", game.next_scope())
        removed = game.unpin(self.root, "feel")
        self.assertIsInstance(removed["removed"], list)
        self.assertNotIsInstance(removed["removed"], dict)

    def test_pin_never_overwrites_a_skill_the_user_wrote(self):
        skills = self.install_skill(".agents")
        own = skills / "polish/SKILL.md"
        own.parent.mkdir()
        own.write_text("---\nname: polish\n---\nskill própria do usuário\n", encoding="utf-8")
        result = game.pin(self.root, "polish")
        self.assertEqual(result["created"], [])
        self.assertEqual(result["skipped"][0]["reason"], "skill_not_pinned_by_game_dev")
        self.assertEqual(own.read_text(encoding="utf-8"), "---\nname: polish\n---\nskill própria do usuário\n")
        # E desafixar também deixa a skill própria intacta.
        removed = game.unpin(self.root, "polish")
        self.assertEqual(removed["removed"], [])
        self.assertTrue(own.is_file())

    def test_pin_names_the_own_skill_the_readme_already_refuses(self):
        readme = (game.FRAMEWORK / "README.md").read_text(encoding="utf-8")
        self.assertTrue(
            game.readme_refuses_own_skill_overwrite(readme),
            "o README já recusa sobrescrever skill sua com o mesmo nome",
        )
        self.assertEqual(game.pin_own_source(), "README.md")
        skills = self.install_skill(".agents")
        own = skills / "polish/SKILL.md"
        own.parent.mkdir()
        own.write_text("---\nname: polish\n---\nskill própria do usuário\n", encoding="utf-8")
        result = game.pin(self.root, "polish")
        self.assertTrue(result["skipped"], "o pin já recusa a skill própria")
        item = result["skipped"][0]
        self.assertIn(
            "sobrescrever uma skill sua com o mesmo nome",
            item["scope"],
            "o skipped copiava o path e calava a recusa",
        )
        self.assertIn("(`própria`)", item["scope"])
        self.assertNotIn("própria", item)
        self.assertFalse(game.readme_refuses_own_skill_overwrite(""))
        with patch.object(game, "pin_own_source", return_value=None):
            silent = game.pin(self.root, "polish")
        self.assertNotIn("sobrescrever uma skill sua com o mesmo nome", silent["skipped"][0]["scope"])
        skill = (game.FRAMEWORK / "SKILL.md").read_text(encoding="utf-8")
        guide = (game.FRAMEWORK / "commands/README.md").read_text(encoding="utf-8")
        self.assertIn("nomeia a própria que o README já recusa", readme)
        self.assertIn("nomeia a própria que o README já recusa", skill)
        self.assertIn("nomeia a própria que o README já recusa", guide)
        self.assertNotIn("verified", item["scope"])
        self.assertNotIn("sobrescrever uma skill sua com o mesmo nome", result["scope"])
        self.assertNotIn("sobrescrever uma skill sua com o mesmo nome", game.unpin(self.root, "polish")["scope"])
        self.assertNotIn("sobrescrever uma skill sua com o mesmo nome", game.command_listing()["scope"])
        self.assertNotIn("sobrescrever uma skill sua com o mesmo nome", game.next_scope())
        self.assertNotIn("sobrescrever uma skill sua com o mesmo nome", game.context_scope())
        unpinned = game.unpin(self.root, "polish")
        self.assertIn("sobrescrever uma skill sua com o mesmo nome", unpinned["skipped"][0]["scope"])
        self.assertNotIn("própria", unpinned["skipped"][0])

    def test_unpin_removes_only_pinned_shortcuts_and_is_idempotent(self):
        skills = self.install_skill(".claude")
        game.pin(self.root, "feel")
        self.assertTrue((skills / "feel/SKILL.md").is_file())
        first = game.unpin(self.root, "feel")
        self.assertEqual(first["removed"], [str(skills / "feel/SKILL.md")])
        self.assertFalse((skills / "feel").exists())
        self.assertEqual(game.unpin(self.root, "feel")["removed"], [])

    def test_pin_refuses_unknown_commands_and_hosts_without_the_skill(self):
        with self.assertRaises(ValueError):
            game.pin(self.root, "dance")
        with self.assertRaises(ValueError):
            game.pin(self.root, "critique")
        run = self.run_cli("pin", "dance")
        self.assertEqual(run.returncode, 1)
        self.assertIn("comando desconhecido", run.stderr)

    def test_doctor_reports_command_integrity_and_lists_commands(self):
        report = game.doctor(self.root)
        check = next(item for item in report["checks"] if item["name"] == "commands")
        self.assertEqual(check["status"], "ok", check)
        self.assertEqual(report["commands"], list(game.command_catalog()["commands"]))
        self.assertEqual(report["scales"], list(game.SCALES))


class ScaleTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="games-scale-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        workspace = patch.dict(os.environ, {"GAMES_WORKSPACE_ROOT": str(self.root)})
        workspace.start()
        self.addCleanup(workspace.stop)
        self.project = self.root / "jogo"
        (self.project / "docs").mkdir(parents=True)

    def test_scale_field_in_a_document_only_suggests(self):
        (self.project / "docs/brief.md").write_text("# Brief\n\n- Escala: AA / Triple-I (piso de acabamento)\n", encoding="utf-8")
        payload = game.context(self.project, "create")
        self.assertEqual(payload["scale"]["name"], "aa")
        self.assertEqual(payload["scale"]["source"], {"path": "docs/brief.md", "line": 3, "value": "AA / Triple-I (piso de acabamento)"})
        self.assertIn("confirme", payload["scale"]["basis"])

    def test_scale_declared_in_conversation_wins_over_the_document(self):
        (self.project / "docs/brief.md").write_text("# Brief\nEscala: jam\n", encoding="utf-8")
        payload = game.context(self.project, "create", scale="product")
        self.assertEqual(payload["scale"]["name"], "product")
        self.assertIsNone(payload["scale"]["source"])
        self.assertIn("--scale", payload["scale"]["basis"])

    def test_aaa_in_a_brief_is_read_as_the_finish_floor_scale_and_unknown_stays_null(self):
        (self.project / "docs/brief.md").write_text("# Brief\nEscala: AAA\n", encoding="utf-8")
        self.assertEqual(game.context(self.project, "create")["scale"]["name"], "aa")
        (self.project / "docs/brief.md").write_text("# Brief\nEscala: [preencher]\n", encoding="utf-8")
        payload = game.context(self.project, "create")
        self.assertIsNone(payload["scale"]["name"])
        self.assertIn("teach", payload["scale"]["basis"])
        with self.assertRaises(ValueError):
            game.context(self.project, "create", scale="blockbuster")

    def test_template_placeholders_never_count_as_a_declared_scale(self):
        # O template do Art Bible traz `Escala: [jam / produto / AA–Triple-I; …]`:
        # é a pergunta. Um rascunho recém-criado não pode sair como "jam" decidido.
        (self.project / "docs/art-bible.md").write_text(
            "# Art Bible\nEscala: [jam / produto / AA–Triple-I; a slice precisa demonstrar o piso escolhido].\n", encoding="utf-8",
        )
        self.assertIsNone(game.context(self.project, "create")["scale"]["name"])
        (self.project / "docs/brief.md").write_text("# Brief\nEscala: produto\n", encoding="utf-8")
        payload = game.context(self.project, "create")
        self.assertEqual(payload["scale"]["name"], "product")
        self.assertEqual(payload["scale"]["source"]["path"], "docs/brief.md")

    def test_scale_cli_flag_is_validated(self):
        run = subprocess.run(
            [sys.executable, str(SCRIPT), "context", str(self.project), "--scale", "blockbuster", "--root", str(self.root)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(run.returncode, 2)


if __name__ == "__main__":
    unittest.main()
