"""O kit em assets/cerebro replica-se: copiar a pasta, check sem erros, buscar o jogo de exemplo."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parents[1]
KIT = FRAMEWORK / "assets" / "cerebro"
IGNORE = shutil.ignore_patterns(
    "__pycache__",
    ".DS_Store",
    "workspace.json",
    "workspace-mobile.json",
    "workspaces.json",
)


def _run(vault: Path, *args: str) -> subprocess.CompletedProcess[str]:
    script = vault / "_sistema" / "cerebro.py"
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=vault,
        capture_output=True,
        text=True,
    )


class CerebroKitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="cerebro-kit-")
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name) / "vault"
        shutil.copytree(KIT, self.vault, ignore=IGNORE)

    def test_kit_tem_contrato_e_exemplo(self) -> None:
        for rel in (
            "Processo.md",
            "AGENTS.md",
            "Como replicar.md",
            "00 Comece Aqui.md",
            "_sistema/cerebro.py",
            "genealogia-jogos/_kit/exportar_grafo.py",
            "genealogia-jogos/nos/jogos/Oficina.md",
            "Como crescer.md",
            "Métodos herdados.md",
            "_sistema/hook_pos_edicao.py",
            ".claude/settings.json",
            "padroes/Rotular cada afirmação pela origem.md",
            "genealogia-jogos/nos/mitos/O Anel.md",
            "genealogia-jogos/nos/obras/Anel e Centro.md",
            "genealogia-jogos/Mapa de queda.canvas",
        ):
            self.assertTrue((KIT / rel).is_file(), rel)

    def test_check_na_origem(self) -> None:
        r = _run(KIT, "check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("\nERROS", r.stdout)

    def test_copia_passa_check_buscar_e_grafo(self) -> None:
        r = _run(self.vault, "check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(str(self.vault.resolve()), r.stdout)
        self.assertNotIn("\nERROS", r.stdout)

        b = _run(self.vault, "buscar", "--jogo", "oficina")
        self.assertEqual(b.returncode, 0, b.stdout + b.stderr)
        self.assertIn("padroes/O tabuleiro pune o encaixe tardio.md", b.stdout)
        self.assertRegex(b.stdout, r"\d+ nota\(s\)\.")

        exportador = self.vault / "genealogia-jogos" / "_kit" / "exportar_grafo.py"
        g = subprocess.run(
            [sys.executable, str(exportador), "--check"],
            cwd=self.vault,
            capture_output=True,
            text=True,
        )
        self.assertEqual(g.returncode, 0, g.stdout + g.stderr)
        self.assertRegex(g.stdout, r"nós: \d+")
        self.assertIn("inspirou", g.stdout)
        self.assertIn("linhagem", g.stdout)
        self.assertIn("parece", g.stdout)
        self.assertIn("fonte", g.stdout)

    def test_segunda_copia_ainda_passa(self) -> None:
        outra = Path(self.tmp.name) / "vault2"
        shutil.copytree(self.vault, outra, ignore=IGNORE)
        r = _run(outra, "check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_indice_na_copia_fica_estavel(self) -> None:
        i = _run(self.vault, "indice")
        self.assertEqual(i.returncode, 0, i.stdout + i.stderr)
        r = _run(self.vault, "check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("Índice.md desatualizado", r.stdout)

    def test_todos_os_tipos_tem_exemplo(self) -> None:
        pastas = {
            "estudo": "estudos",
            "pesquisa": "pesquisas",
            "aprendizado": "aprendizados",
            "plano": "planos",
            "identidade": "identidade",
            "operacao": "operacao",
            "aula": "aulas",
            "registro": "registros",
            "evidencia": "evidencias",
            "padrao": "padroes",
            "visao": "genealogia-jogos/visoes",
            "captura": "_entrada",
        }
        for tipo, pasta in pastas.items():
            notas = [p for p in (KIT / pasta).glob("*.md") if p.name != "Entrada.md"]
            self.assertTrue(notas, f"sem exemplo de {tipo} em {pasta}/")

    def test_wikilink_quebrado_falha(self) -> None:
        alvo = self.vault / "Processo.md"
        alvo.write_text(alvo.read_text(encoding="utf-8") + "\n[[Nota inexistente]]\n", encoding="utf-8")
        r = _run(self.vault, "check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Nota inexistente", r.stdout)


REGRAS_HERDADAS = (
    "Ler o disco antes da wiki",
    "Todo estudo tem o mesmo esqueleto",
    "Copiar a regra, não o IP",
    "Pareceres independentes, depois consolidação",
    "A regra sobe; o caso fica",
    "Base antes de expansão",
    "Qualidade aprovada é o piso",
    "Hipótese vira fato no caminho",
    "O contador de FPS esconde o tranco",
)
PORTAS_DA_REGRA = ("00 Comece Aqui.md", "Padrões.md", "Como crescer.md", "AGENTS.md")


class MetodosHerdadosTest(unittest.TestCase):
    """O método vem pronto; a prova não vem. Regra herdada não se disfarça de padrão."""

    def setUp(self) -> None:
        self.nota = KIT / "Métodos herdados.md"
        self.texto = self.nota.read_text(encoding="utf-8")

    def test_nove_regras_com_tipo_processo(self) -> None:
        self.assertIn("tipo: processo", self.texto)
        for regra in REGRAS_HERDADAS:
            self.assertIn(regra, self.texto, regra)

    def test_regra_herdada_nao_e_padrao(self) -> None:
        """Sem evidência local não há nota em padroes/ — senão o kit forjaria a prova."""
        for regra in REGRAS_HERDADAS:
            self.assertFalse((KIT / "padroes" / f"{regra}.md").exists(), regra)

    def test_as_portas_apontam_para_a_nota(self) -> None:
        for porta in PORTAS_DA_REGRA:
            self.assertIn("[[Métodos herdados]]", (KIT / porta).read_text(encoding="utf-8"), porta)

    def test_diz_como_promover(self) -> None:
        self.assertIn("## Promover a padrão", self.texto)
        self.assertIn("forca: confirmado", self.texto)


class SkillsDoVaultTest(unittest.TestCase):
    """As skills ficam em .agents/, fora do vault visível; o check tem de alcançá-las."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="cerebro-skills-")
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name) / "vault"
        shutil.copytree(KIT, self.vault, ignore=IGNORE)
        self.skills = self.vault / "genealogia-jogos" / ".agents" / "skills"

    def test_cinco_skills_vieram_na_copia(self) -> None:
        nomes = sorted(p.name for p in self.skills.iterdir() if p.is_dir())
        self.assertEqual(nomes, ["build-moc", "capture-source", "connect-notes",
                                 "genealogia-grafo", "review-vault"])

    def test_wikilink_de_skill_para_nota_inexistente_falha(self) -> None:
        alvo = self.skills / "build-moc" / "SKILL.md"
        alvo.write_text(alvo.read_text(encoding="utf-8") + "\n[[Máquina Worms Armageddon]]\n",
                        encoding="utf-8")
        r = _run(self.vault, "check")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("Máquina Worms Armageddon", r.stdout)
        self.assertIn("build-moc/SKILL.md", r.stdout)

    def test_skill_sem_description_falha(self) -> None:
        alvo = self.skills / "review-vault" / "SKILL.md"
        texto = alvo.read_text(encoding="utf-8")
        alvo.write_text("\n".join(l for l in texto.splitlines()
                                  if not l.startswith("description:")) + "\n", encoding="utf-8")
        r = _run(self.vault, "check")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("description", r.stdout)


class DiagnosticoEstruturadoTest(unittest.TestCase):
    """check com código, nível e linha: é o que o hook filtra e o que o --json publica."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="cerebro-diag-")
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name) / "vault"
        shutil.copytree(KIT, self.vault, ignore=IGNORE)

    def _json(self, *args: str) -> dict:
        r = _run(self.vault, "check", "--json", "--sem-grafo", *args)
        return json.loads(r.stdout)

    def test_json_traz_resumo_e_itens(self) -> None:
        d = self._json()
        self.assertEqual(d["codigo_de_saida"], 0)
        self.assertEqual(d["itens"], [])
        self.assertEqual(d["resumo"]["nossos_jogos"], 2)
        self.assertIn("padrao", d["resumo"]["tipos"])

    def test_item_tem_codigo_arquivo_e_nivel(self) -> None:
        alvo = self.vault / "Processo.md"
        alvo.write_text(alvo.read_text(encoding="utf-8") + "\n[[Nota inexistente]]\n", encoding="utf-8")
        d = self._json()
        self.assertEqual(d["codigo_de_saida"], 1)
        item = next(i for i in d["itens"] if i["codigo"] == "LINK")
        self.assertEqual(item["arquivo"], "Processo.md")
        self.assertEqual(item["nivel"], "erro")
        self.assertIn("Nota inexistente", item["msg"])

    def test_nivel_erro_esconde_aviso(self) -> None:
        alvo = self.vault / "padroes" / "Clonar o que se vê.md"
        alvo.write_text(alvo.read_text(encoding="utf-8").replace("- Fronteira:", "- Limite:"), encoding="utf-8")
        todos = self._json()
        self.assertTrue(any(i["codigo"] == "SEM_FRONTEIRA" for i in todos["itens"]))
        so_erro = self._json("--nivel", "erro")
        self.assertFalse(any(i["nivel"] != "erro" for i in so_erro["itens"]))

    def test_hook_devolve_so_o_arquivo_editado(self) -> None:
        alvo = self.vault / "padroes" / "Clonar o que se vê.md"
        alvo.write_text(alvo.read_text(encoding="utf-8") + "\n[[Nota que não existe]]\n", encoding="utf-8")
        (self.vault / "Processo.md").write_text(
            (self.vault / "Processo.md").read_text(encoding="utf-8") + "\n[[Outra ausente]]\n", encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(self.vault / "_sistema" / "hook_pos_edicao.py")],
            input=json.dumps({"tool_input": {"file_path": "padroes/Clonar o que se vê.md"}}),
            cwd=self.vault, capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        ctx = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Clonar o que se vê.md", ctx)
        self.assertIn("Nota que não existe", ctx)
        self.assertNotIn("Outra ausente", ctx)

    def test_hook_cala_em_nota_limpa_e_em_lixo(self) -> None:
        hook = str(self.vault / "_sistema" / "hook_pos_edicao.py")
        for entrada in (json.dumps({"tool_input": {"file_path": "Processo.md"}}),
                        json.dumps({"tool_input": {"file_path": "/fora/do/vault/nota.md"}}),
                        "não é json"):
            r = subprocess.run([sys.executable, hook], input=entrada, cwd=self.vault,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, entrada)
            self.assertEqual(r.stdout.strip(), "", entrada)


class InvarianteEFronteiraTest(unittest.TestCase):
    """Contrato separado da regularidade observada; regra com o limite declarado."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="cerebro-inv-")
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name) / "vault"
        shutil.copytree(KIT, self.vault, ignore=IGNORE)

    def test_modelos_pedem_invariante_e_fronteira(self) -> None:
        ludema = (KIT / "_sistema" / "modelos" / "grafo" / "Ludema.md").read_text(encoding="utf-8")
        self.assertIn("## Invariante", ludema)
        self.assertIn("## Observado (n=)", ludema)
        estudo = (KIT / "_sistema" / "modelos" / "Estudo.md").read_text(encoding="utf-8")
        self.assertIn("Invariante e observado", estudo)
        padrao = (KIT / "_sistema" / "modelos" / "Padrão.md").read_text(encoding="utf-8")
        self.assertIn("- Fronteira:", padrao)

    def test_todo_padrao_do_kit_declara_fronteira(self) -> None:
        for nota in (KIT / "padroes").glob("*.md"):
            self.assertRegex(nota.read_text(encoding="utf-8"), r"(?m)^- Fronteira:", nota.name)

    def test_ludema_sem_invariante_vira_aviso(self) -> None:
        alvo = self.vault / "genealogia-jogos" / "nos" / "ludemas" / "Peça que encaixa.md"
        alvo.write_text(alvo.read_text(encoding="utf-8").replace("## Invariante", "## Contrato"), encoding="utf-8")
        d = json.loads(_run(self.vault, "check", "--json", "--sem-grafo").stdout)
        self.assertTrue(any(i["codigo"] == "SEM_INVARIANTE" for i in d["itens"]), d["itens"])

    def test_ludema_com_um_jogo_vira_aviso_no_grafo(self) -> None:
        linha = re.compile(r"^\|\s*\[\[Peça que encaixa\]\]\s*\|\s*carrega\s*\|.*$", re.M)
        portadores = [n for n in sorted((self.vault / "genealogia-jogos" / "nos" / "jogos").glob("*.md"))
                      if linha.search(n.read_text(encoding="utf-8"))]
        self.assertGreaterEqual(len(portadores), 2)
        for nota in portadores[1:]:  # deixa um só carregando
            nota.write_text(linha.sub("", nota.read_text(encoding="utf-8")), encoding="utf-8")
        g = subprocess.run(
            [sys.executable, str(self.vault / "genealogia-jogos" / "_kit" / "exportar_grafo.py"), "--check"],
            cwd=self.vault, capture_output=True, text=True,
        )
        self.assertIn("ludema só nasce com dois ou mais", g.stdout + g.stderr)


if __name__ == "__main__":
    unittest.main()
