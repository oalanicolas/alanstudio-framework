#!/usr/bin/env python3
"""Gate anti-slop do Alan Studios Framework.

Mede os sinais de crescimento auto-referente — texto que só confirma texto — e
recusa qualquer aumento sobre o baseline versionado.

O baseline é um cliquet: desce por poda deliberada, e só sobe por edição
explícita de `scripts/slop_baseline.json`, que aparece no diff e é revisável.
Assim a árvore atual passa como está, mas o ciclo que gerou o PR #6 — uma
função, um teste e uma entrada de versão por palavra recusada — trava.

Uso:
    python3 scripts/slop_gate.py                   # verifica contra o baseline
    python3 scripts/slop_gate.py --update          # regrava o baseline
    python3 scripts/slop_gate.py --diff-base main  # exige prova jogável
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "scripts/slop_baseline.json"

ADOPTION = ROOT / "adoption.md"
SKILL = ROOT / "SKILL.md"
TESTS_DIR = ROOT / "tests"
SCRIPTS_DIR = ROOT / "scripts"

# Frases-molde: o texto que o ciclo autônomo multiplica sem tocar no jogo.
FORMULA = (
    re.compile(r"no disco não é"),
    re.compile(r"recusa que .{0,80}?\b(seja|prove|provem|baste)\b"),
)

# Asserções que apenas confirmam a presença de uma string.
TEXT_ASSERTS = {"assertIn", "assertNotIn"}

# Sinais de que o teste executa o harness de verdade, em vez de ler documento.
EXEC_ATTRS = {"run", "check_output", "check_call", "Popen", "call"}
EXEC_NAMES = {"subprocess", "tempfile", "TemporaryDirectory"}


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _is_doc_source(node: ast.AST) -> bool:
    """A expressão deriva da leitura de um arquivo?"""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Attribute) and sub.attr == "read_text":
            return True
    return False


class _TestScan(ast.NodeVisitor):
    """Classifica um `def test_*` como doc-only ou executável."""

    def __init__(self) -> None:
        self.doc_vars: set[str] = set()
        self.text_asserts = 0
        self.other_asserts = 0
        self.executes = False

    def visit_Assign(self, node: ast.Assign) -> None:
        if _is_doc_source(node.value):
            for target in node.targets:
                for sub in ast.walk(target):
                    if isinstance(sub, ast.Name):
                        self.doc_vars.add(sub.id)
        self.generic_visit(node)

    def _container_is_doc(self, node: ast.AST) -> bool:
        if _is_doc_source(node):
            return True
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and sub.id in self.doc_vars:
                return True
        return False

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Attribute):
            # self.assertX(...)
            if isinstance(func.value, ast.Name) and func.value.id == "self":
                if func.attr in TEXT_ASSERTS and len(node.args) >= 2:
                    if self._container_is_doc(node.args[1]):
                        self.text_asserts += 1
                    else:
                        self.other_asserts += 1
                elif func.attr.startswith("assert"):
                    self.other_asserts += 1
            # game.<func>(...) — o harness rodando de verdade
            elif isinstance(func.value, ast.Name) and func.value.id == "game":
                if not func.attr.isupper():
                    self.executes = True
            elif func.attr in EXEC_ATTRS:
                self.executes = True
        elif isinstance(func, ast.Name) and func.id in EXEC_NAMES:
            self.executes = True

        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and sub.id in EXEC_NAMES:
                self.executes = True
        self.generic_visit(node)


def doc_only_tests() -> list[str]:
    """Testes cuja única asserção é presença de string em arquivo lido."""
    found: list[str] = []
    for path in sorted(TESTS_DIR.glob("test_*.py")):
        try:
            tree = ast.parse(_read(path))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not node.name.startswith("test_"):
                continue
            scan = _TestScan()
            for stmt in node.body:
                scan.visit(stmt)
            if scan.executes or scan.other_asserts:
                continue
            if scan.text_asserts:
                found.append(f"{path.relative_to(ROOT)}::{node.name}")
    return found


def measure() -> dict[str, int]:
    adoption = _read(ADOPTION)
    formula = 0
    for path in sorted(SCRIPTS_DIR.glob("*.py")):
        if path.name == Path(__file__).name:
            continue
        text = _read(path)
        for pattern in FORMULA:
            formula += len(pattern.findall(text))
    return {
        "doc_only_tests": len(doc_only_tests()),
        "adoption_sections": len(re.findall(r"^## ", adoption, re.MULTILINE)),
        "adoption_one_word_lines": sum(
            1 for line in adoption.splitlines() if len(line.split()) == 1
        ),
        "formula_phrases": formula,
        "skill_entry_lines": len(_read(SKILL).splitlines()),
    }


def load_baseline() -> dict:
    if not BASELINE.is_file():
        return {"ratchet": {}, "ceiling": {}}
    return json.loads(_read(BASELINE))


def playable_proof(base: str) -> tuple[bool, str]:
    """adoption.md só cresce acompanhado de um recorte jogável."""
    try:
        merge_base = subprocess.run(
            ["git", "merge-base", base, "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        stat = subprocess.run(
            ["git", "diff", "--numstat", merge_base, "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return False, f"não foi possível comparar com {base}: {exc}"

    grew = False
    touched: list[str] = []
    for line in stat.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, removed, name = parts
        touched.append(name)
        # Crescimento é o saldo, não as linhas tocadas: reescrever um parágrafo
        # ou reflowar o arquivo adiciona linhas sem acrescentar changelog.
        if name == "adoption.md" and added.isdigit() and removed.isdigit():
            net = int(added) - int(removed)
            if net > 0:
                grew = True

    if not grew:
        return True, "adoption.md não cresceu em saldo"

    proof_dirs = ("examples/", "assets/starters/", "docs/stories/")
    proofs = [n for n in touched if n.startswith(proof_dirs)]
    if proofs:
        return True, f"prova jogável: {', '.join(proofs[:3])}"
    return False, (
        "adoption.md cresceu sem recorte jogável. Toque examples/, "
        "assets/starters/ ou docs/stories/ com a prova de execução."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate anti-slop")
    parser.add_argument("--update", action="store_true", help="regrava o baseline")
    parser.add_argument("--diff-base", metavar="REF", help="exige prova jogável vs REF")
    parser.add_argument("--list", action="store_true", help="lista os testes doc-only")
    args = parser.parse_args()

    current = measure()

    if args.list:
        for name in doc_only_tests():
            print(name)
        return 0

    if args.update:
        baseline = load_baseline()
        ceiling = baseline.get("ceiling") or {"skill_entry_lines": 160}
        payload = {
            "_comment": (
                "Cliquet anti-slop. Estes números só podem DESCER. "
                "Subir exige editar este arquivo no PR e justificar no corpo. "
                "Regenere com: python3 scripts/slop_gate.py --update"
            ),
            "ratchet": {k: v for k, v in current.items() if k != "skill_entry_lines"},
            "ceiling": ceiling,
        }
        BASELINE.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"baseline regravado em {BASELINE.relative_to(ROOT)}")
        for key, value in payload["ratchet"].items():
            print(f"  {key}: {value}")
        return 0

    baseline = load_baseline()
    ratchet = baseline.get("ratchet", {})
    ceiling = baseline.get("ceiling", {})
    failures: list[str] = []

    print("métrica                   atual   limite")
    for key, value in current.items():
        if key in ratchet:
            limit = ratchet[key]
            ok = value <= limit
            kind = "cliquet"
        elif key in ceiling:
            limit = ceiling[key]
            ok = value <= limit
            kind = "teto"
        else:
            print(f"  {key:<24} {value:>5}       —  (sem limite)")
            continue
        mark = "ok " if ok else "FALHA"
        print(f"  {key:<24} {value:>5}   {limit:>5}  {mark} ({kind})")
        if not ok:
            failures.append(
                f"{key}: {value} > {limit}. "
                + (
                    "A entrada da skill tem teto fixo; mova o conteúdo para uma referência."
                    if kind == "teto"
                    else "Este número só pode descer."
                )
            )

    if args.diff_base:
        ok, detail = playable_proof(args.diff_base)
        print(f"\nprova jogável: {'ok' if ok else 'FALHA'} — {detail}")
        if not ok:
            failures.append(detail)

    if failures:
        print("\nGate anti-slop RECUSOU:", file=sys.stderr)
        for item in failures:
            print(f"  - {item}", file=sys.stderr)
        print(
            "\nSe o aumento for deliberado, edite scripts/slop_baseline.json "
            "no mesmo PR e justifique no corpo.",
            file=sys.stderr,
        )
        return 1

    print("\nGate anti-slop: aprovado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
