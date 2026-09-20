#!/usr/bin/env python3
"""hook_pos_edicao.py — hook PostToolUse (Edit|Write) para agentes que escrevem neste vault.

Lê o JSON do hook na entrada padrão, roda `cerebro.py check --json` e devolve ao agente, como
contexto, só os problemas **do arquivo que ele acabou de editar**. Assim o contrato responde na
hora, em vez de esperar que alguém rode o check no fim da tarefa.

Nunca bloqueia a edição e nunca falha: qualquer problema do próprio hook é engolido em silêncio.

Teste manual:
  echo '{"tool_input":{"file_path":"Processo.md"}}' | python3 _sistema/hook_pos_edicao.py
"""
from __future__ import annotations

import os
import json
import subprocess
import sys
from pathlib import Path

VAULT = Path(os.path.abspath(__file__)).parent.parent
CHECK = VAULT / "_sistema" / "cerebro.py"
EXPORTADOR = VAULT / "genealogia-jogos" / "_kit" / "exportar_grafo.py"
NOS = "genealogia-jogos/nos/"
IGNORAR = ("_sistema/", ".claude/", ".codex/", ".obsidian/")


def contexto(rel: str) -> str:
    r = subprocess.run([sys.executable, str(CHECK), "check", "--json", "--sem-grafo"],
                       cwd=VAULT, capture_output=True, text=True, timeout=120)
    itens = [i for i in json.loads(r.stdout).get("itens", [])
             if i["arquivo"] == rel and i["nivel"] in ("erro", "aviso")]
    linhas = [f"- [{i['nivel'].upper()} {i['codigo']}]"
              f"{' linha ' + str(i['linha']) if i.get('linha') else ''} {i['msg']}" for i in itens]
    if rel.startswith(NOS) and EXPORTADOR.exists():
        g = subprocess.run([sys.executable, str(EXPORTADOR), "--check"],
                           cwd=VAULT, capture_output=True, text=True, timeout=120)
        alvo = rel.rsplit("/", 1)[-1]
        linhas += [f"- [GRAFO] {l.strip().lstrip('- ')}" for l in (g.stdout + g.stderr).splitlines()
                   if alvo in l or Path(alvo).stem in l]
    if not linhas:
        return ""
    return (f"cerebro.py apontou em {rel}:\n" + "\n".join(linhas)
            + "\nCorrija o que esta edição causou antes de encerrar. Aresta ou nó novo pede "
              "`python3 genealogia-jogos/_kit/exportar_grafo.py`; nota nova pede `indice`.")


def main() -> None:
    dados = json.load(sys.stdin)
    caminho = ((dados.get("tool_input") or {}).get("file_path")
               or (dados.get("tool_response") or {}).get("filePath") or "")
    if not caminho.endswith(".md"):
        return
    # O caminho pode vir absoluto, relativo à raiz do projeto (vault dentro de docs/) ou ao vault.
    candidatos = [caminho] if os.path.isabs(caminho) else [
        os.path.join(os.getcwd(), caminho), str(VAULT / caminho)]
    # A comparação usa realpath nos dois lados (em macOS /var é link para /private/var);
    # o caminho relativo resultante continua valendo para o VAULT não resolvido.
    raiz = os.path.realpath(VAULT)
    rel = ""
    for c in candidatos:
        r = os.path.relpath(os.path.realpath(c), raiz)
        if not r.startswith("..") and (VAULT / r).exists():
            rel = Path(r).as_posix()
            break
    if not rel:
        return  # arquivo fora deste vault
    if rel.startswith(IGNORAR):
        return
    msg = contexto(rel)
    if msg:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                 "additionalContext": msg}}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
