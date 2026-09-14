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
    python3 scripts/slop_gate.py --diff-base main  # exige registro de execução
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

# Asserções que confirmam a presença de uma frase.
PHRASE_ASSERTS = {"assertIn", "assertNotIn", "assertRegex", "assertNotRegex"}


# Uma frase — o que uma asserção de texto confirma. Uma chave de dicionário ou
# um identificador (sem espaço) normalmente indica verificação estrutural.
def _is_phrase(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and " " in node.value.strip()
        and len(node.value.strip()) >= 8
    )


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def phrase_assertions() -> list[str]:
    """Asserções que confirmam que uma FRASE aparece em algum texto.

    Conta o sintoma diretamente, em vez de classificar o teste inteiro. Um
    teste do #6 mistura `assertEqual`, `assertRegex` e meia dúzia de
    `assertIn` de frase; qualquer classificação binária o descartava inteiro,
    e era justamente o caso que este gate precisa pegar.

    Uma frase tem espaço e ao menos 8 caracteres — um identificador ou chave
    de dicionário normalmente indica verificação estrutural, que é legítima.
    """
    found: list[str] = []
    for path in sorted(TESTS_DIR.glob("test_*.py")):
        try:
            tree = ast.parse(_read(path))
        except SyntaxError:
            continue
        rel = path.relative_to(ROOT)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not isinstance(func, ast.Attribute):
                continue
            if func.attr not in PHRASE_ASSERTS:
                continue
            if not (isinstance(func.value, ast.Name) and func.value.id == "self"):
                continue
            if node.args and _is_phrase(node.args[0]):
                found.append(f"{rel}:{node.lineno}")
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
        "phrase_assertions": len(phrase_assertions()),
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


# Um registro de sessão: docs/stories/<AAAA-MM-DD>-<assunto>.md
STORY_NAME = re.compile(r"^docs/stories/\d{4}-\d{2}-\d{2}-[^/]+\.md$")


def _record_is_valid(name: str) -> tuple[bool, str]:
    """O arquivo apontado como registro tem conteúdo verificável?

    Isto NÃO prova que alguém jogou — nada num diff prova isso. Prova que a
    sessão deixou um registro datado ou um recibo com carimbo, em vez de
    tocar um arquivo qualquer na pasta certa.
    """
    path = ROOT / name
    if not path.is_file():
        return False, "não existe na árvore"
    text = _read(path)
    if not text.strip():
        return False, "vazio"

    if name.endswith(".json"):
        try:
            doc = json.loads(text)
        except json.JSONDecodeError:
            return False, "JSON inválido"
        if not isinstance(doc, dict):
            return False, "recibo não é objeto"
        missing = [k for k in ("schema_version", "recorded_at") if k not in doc]
        if missing:
            return False, f"recibo sem {', '.join(missing)}"
        return True, "recibo com carimbo"

    if STORY_NAME.match(name):
        # Um registro de sessão precisa de corpo, não só de título.
        body = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
        if len(body) < 3:
            return False, "registro sem corpo"
        return True, "registro de sessão datado"

    return False, "não é recibo .json nem docs/stories/<data>-<assunto>.md"


def execution_record(base: str) -> tuple[bool, str]:
    """adoption.md só cresce acompanhado de um registro de execução.

    O nome é deliberadamente modesto: a checagem confirma que existe um
    registro verificável, não que o jogo foi jogado. Deletar um exemplo não
    conta — só arquivos adicionados ou modificados são candidatos.
    """
    try:
        merge_base = subprocess.run(
            ["git", "merge-base", base, "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        stat = subprocess.run(
            ["git", "diff", "--numstat", merge_base, "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
        # A/M apenas: uma exclusão nunca é registro de execução.
        written = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=AM", merge_base, "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split("\n")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return False, f"não foi possível comparar com {base}: {exc}"

    grew = False
    for line in stat.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, removed, name = parts
        # Crescimento é o saldo, não as linhas tocadas: reescrever um parágrafo
        # ou reflowar o arquivo adiciona linhas sem acrescentar changelog.
        if name == "adoption.md" and added.isdigit() and removed.isdigit():
            if int(added) - int(removed) > 0:
                grew = True

    if not grew:
        return True, "adoption.md não cresceu em saldo"

    # O que vale como registro é o tipo do artefato, não a pasta onde ele
    # está: exigir "um arquivo em examples/" aprovava até uma exclusão.
    rejected: list[str] = []
    for name in (n for n in written if n.strip()):
        if not (name.endswith(".json") or STORY_NAME.match(name)):
            continue
        ok, why = _record_is_valid(name)
        if ok:
            return True, f"registro de execução: {name} ({why})"
        rejected.append(f"{name}: {why}")

    detail = "; ".join(rejected[:3]) if rejected else "nenhum candidato"
    return False, (
        "adoption.md cresceu sem registro de execução. Adicione um recibo "
        "`.json` com `schema_version` e `recorded_at`, ou um "
        "`docs/stories/<AAAA-MM-DD>-<assunto>.md` com corpo. "
        f"Recusados — {detail}."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate anti-slop")
    parser.add_argument("--update", action="store_true", help="regrava o baseline")
    parser.add_argument(
        "--diff-base", metavar="REF",
        help="exige registro de execução quando adoption.md cresce, vs REF",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="lista arquivo:linha de cada asserção de frase",
    )
    args = parser.parse_args()

    current = measure()

    if args.list:
        for name in phrase_assertions():
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
        ok, detail = execution_record(args.diff_base)
        print(f"\nregistro de execução: {'ok' if ok else 'FALHA'} — {detail}")
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
