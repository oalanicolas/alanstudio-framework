#!/usr/bin/env python3
"""Valida e exporta o grafo de influências do vault.

Fonte da verdade: as tabelas "## Recebeu de" das notas em `nos/<tipo>/`.
Cada linha da tabela é uma aresta dirigida  De ──relação──► (esta nota).
A propriedade `studio: "[[Estúdio]]"` gera arestas estruturais (desenvolveu / integra).

Uso, a partir de qualquer pasta:
  python3 _kit/exportar_grafo.py          # valida, grava campos derivados nas notas e escreve _kit/dados/
  python3 _kit/exportar_grafo.py --check  # só valida (código de saída 1 se houver erro)

Campos derivados gravados no frontmatter de cada nó (não edite à mão):
  entradas, saidas, melhor_confianca, pendentes

Saídas:
  nos.csv     -> Kumu (coluna Label) / planilha
  arestas.csv -> Kumu (colunas From, To, Type) / planilha
  grafo.dot   -> Graphviz (`dot -Tsvg grafo.dot > grafo.svg`) ou importar no Gephi
"""
from __future__ import annotations

import csv
import os
import re
import sys
from collections import Counter
from pathlib import Path

# abspath, não resolve: o script pode ser symlink para a implementação única.
VAULT = Path(os.path.abspath(__file__)).parent.parent
NOS = VAULT / "nos"
DADOS = VAULT / "_kit" / "dados"

PASTA_TIPOS = {
    "jogos": {"jogo"},
    "obras": {"filme", "texto", "livro", "pintura", "album", "serie", "quadrinho"},
    "mitos": {"mito"},
    "ludemas": {"ludema"},
    "pessoas": {"pessoa"},
    "estudios": {"estudio"},
}
RELACOES = {
    "inspirou",             # o time citou publicamente
    "sequencia_de",         # continuação oficial
    "sucessor_espiritual",  # mesmo time/ideia, sem ser sequência
    "mesmo_studio",         # linhagem interna do estúdio
    "mesmo_ludem",          # compartilha um mecanismo sem nó de ludema
    "tom",                  # referência de tom/voz/humor
    "fonte",                # mito, texto, obra-fonte adaptada
    "linhagem",             # desce da mesma árvore de gênero, sem citação
    "parece",               # semelhança apontada por terceiros
    "origem",               # jogo -> ludema: onde o mecanismo foi formulado
    "carrega",              # ludema -> jogo: o jogo adota o mecanismo
    "autoria",              # pessoa -> obra
    "desenvolveu",          # estúdio -> jogo (derivada de `studio`)
    "integra",              # pessoa -> estúdio (derivada de `studio`)
}
# Relações que afirmam intenção do autor: exigem fala pública (A ou B).
CITACAO = {"inspirou", "tom", "fonte", "sucessor_espiritual"}
# Relações estruturais: não contam como influência nas métricas.
ESTRUTURAIS = {"autoria", "desenvolveu", "integra"}
CONFIANCAS = ["A", "B", "C", "D"]
ORDEM = {c: i for i, c in enumerate(CONFIANCAS)}
DERIVADOS = ("entradas", "saidas", "melhor_confianca", "pendentes")

WIKILINK = re.compile(r"\[\[([^\]#|]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")
PIPE_SENTINELA = "\x00"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """YAML mínimo: `chave: valor`, `chave: [a, b]` e listas `- item`."""
    if not text.startswith("---"):
        return {}, text
    fim = text.find("\n---", 3)
    if fim == -1:
        return {}, text
    bruto, corpo = text[3:fim], text[fim + 4:]
    fm: dict = {}
    chave = None
    for linha in bruto.splitlines():
        if not linha.strip():
            continue
        if linha.lstrip().startswith("- ") and chave is not None:
            if not isinstance(fm.get(chave), list):
                fm[chave] = []
            fm[chave].append(linha.strip()[2:].strip().strip("\"'"))
            continue
        if ":" not in linha or linha.startswith(" "):
            continue
        k, _, v = linha.partition(":")
        chave, v = k.strip(), v.strip()
        if v == "":
            fm[chave] = []
        elif v.startswith("[") and v.endswith("]") and not v.startswith("[["):
            miolo = v[1:-1].strip()
            fm[chave] = [x.strip().strip("\"'") for x in miolo.split(",")] if miolo else []
        else:
            fm[chave] = v.strip("\"'")
    return fm, corpo


def valor(fm: dict, chave: str) -> str:
    v = fm.get(chave, "")
    if isinstance(v, list):
        return "; ".join(v)
    return str(v)


def sem_links(s: str) -> str:
    return WIKILINK.sub(lambda m: m.group(1), s)


def linhas_recebeu_de(corpo: str) -> list[list[str]]:
    """Células de cada linha de dados da tabela sob '## Recebeu de'."""
    linhas: list[list[str]] = []
    dentro = False
    for linha in corpo.splitlines():
        if linha.startswith("## "):
            dentro = linha.strip().lower().startswith("## recebeu de")
            continue
        s = linha.strip()
        if not dentro or not s.startswith("|"):
            continue
        s = re.sub(r"\[\[([^\]]*)\]\]", lambda m: "[[" + m.group(1).replace("|", PIPE_SENTINELA) + "]]", s)
        cels = [c.strip().replace(PIPE_SENTINELA, "|") for c in s.strip("|").split("|")]
        if not cels or cels[0].lower() == "de" or set(cels[0]) <= set("-: "):
            continue
        linhas.append(cels)
    return linhas


def atualizar_frontmatter(arq: Path, campos: dict[str, str]) -> bool:
    """Substitui ou acrescenta chaves escalares de nível raiz. Devolve True se gravou."""
    texto = arq.read_text(encoding="utf-8")
    if not texto.startswith("---"):
        return False
    fim = texto.find("\n---", 3)
    if fim == -1:
        return False
    bloco = texto[3:fim]
    novo, feitos = [], set()
    for linha in bloco.split("\n"):
        m = re.match(r"^([A-Za-z_]\w*):", linha)
        if m and m.group(1) in campos:
            novo.append(f"{m.group(1)}: {campos[m.group(1)]}")
            feitos.add(m.group(1))
        else:
            novo.append(linha)
    for k, v in campos.items():
        if k not in feitos:
            novo.append(f"{k}: {v}")
    novo_bloco = "\n".join(novo)
    if novo_bloco == bloco:
        return False
    arq.write_text("---" + novo_bloco + texto[fim:], encoding="utf-8")
    return True


def carregar():
    nos: dict[str, dict] = {}
    arestas: list[dict] = []
    erros: list[str] = []
    avisos: list[str] = []

    for pasta, tipos_ok in PASTA_TIPOS.items():
        for arq in sorted((NOS / pasta).glob("*.md")):
            fm, corpo = parse_frontmatter(arq.read_text(encoding="utf-8"))
            nome = arq.stem
            rel = str(arq.relative_to(VAULT))
            tipo = valor(fm, "tipo")
            if tipo not in tipos_ok:
                erros.append(f"{rel}: tipo {tipo!r} não combina com a pasta {pasta}/ (aceita: {', '.join(sorted(tipos_ok))})")
            if nome in nos:
                erros.append(f"{rel}: nome repetido em outra pasta ({nos[nome]['arquivo']})")
            nos[nome] = {
                "Label": nome,
                "Type": tipo or pasta,
                "pasta": pasta,
                "ano": valor(fm, "ano"),
                "studio": sem_links(valor(fm, "studio")),
                "genero": valor(fm, "genero"),
                "hub": valor(fm, "hub").lower() == "true",
                "status": valor(fm, "status"),
                "tags": valor(fm, "tags"),
                "arquivo": rel,
                "_corpo": corpo,
                "_studio_raw": valor(fm, "studio"),
                "_arq": arq,
            }

    indice_ci = {n.lower(): n for n in nos}

    def resolver(origem: str, onde: str) -> str:
        alvo = indice_ci.get(origem.lower())
        if alvo is None:
            erros.append(f"{onde}: [[{origem}]] não existe em nos/ (crie a nota ou corrija o link)")
            return origem
        return alvo

    for nome, no in nos.items():
        onde = no["arquivo"]
        for cels in linhas_recebeu_de(no.pop("_corpo")):
            if len(cels) < 5:
                erros.append(f"{onde}: linha com {len(cels)} colunas (esperado 5): {cels}")
                continue
            de_raw, relacao, o_que, evid, conf = cels[:5]
            relacao = relacao.strip().lower()
            conf = conf.strip().upper()
            origens = [o.strip() for o in WIKILINK.findall(de_raw)]
            if not origens:
                erros.append(f"{onde}: coluna 'De' sem [[wikilink]]: {de_raw!r}")
                continue
            if relacao not in RELACOES:
                erros.append(f"{onde}: relação desconhecida {relacao!r} (use: {', '.join(sorted(RELACOES))})")
            if conf not in ORDEM:
                erros.append(f"{onde}: confiança {conf!r} inválida (A, B, C ou D)")
            if relacao in CITACAO and conf in {"C", "D"}:
                avisos.append(f"{onde}: '{relacao}' de {origens} com confiança {conf} — sem fala pública do autor, vale como hipótese")
            m = MDLINK.search(evid)
            evid_texto = (m.group(1) if m else evid).strip()
            evid_url = m.group(2) if m else ""
            for origem in origens:
                de = resolver(origem, onde)
                if relacao == "carrega" and nos.get(de, {}).get("pasta") != "ludemas":
                    erros.append(f"{onde}: 'carrega' exige um ludema na coluna De, veio [[{de}]]")
                if relacao == "origem" and no["pasta"] != "ludemas":
                    erros.append(f"{onde}: 'origem' só faz sentido na nota de um ludema")
                arestas.append({
                    "From": de, "To": nome, "Type": relacao,
                    "o_que_passou": o_que, "evidencia": evid_texto, "url": evid_url, "confianca": conf,
                })
        # arestas estruturais derivadas da propriedade studio
        for est in WIKILINK.findall(no.pop("_studio_raw")):
            de = resolver(est, onde)
            if no["pasta"] == "jogos":
                arestas.append({"From": de, "To": nome, "Type": "desenvolveu", "o_que_passou": "",
                                "evidencia": "propriedade studio", "url": "", "confianca": "A"})
            elif no["pasta"] == "pessoas":
                arestas.append({"From": nome, "To": de, "Type": "integra", "o_que_passou": "",
                                "evidencia": "propriedade studio", "url": "", "confianca": "A"})

    vistos = Counter((a["From"], a["To"], a["Type"]) for a in arestas)
    for chave, n in vistos.items():
        if n > 1:
            avisos.append(f"aresta repetida {n}x: {chave[0]} ─{chave[2]}─► {chave[1]}")
    return nos, arestas, erros, avisos


def derivar(nos, arestas, avisos) -> None:
    carregam = Counter(a["From"] for a in arestas if a["Type"] == "carrega")
    for nome, no in nos.items():
        if no["pasta"] == "ludemas" and carregam[nome] < 2:
            avisos.append(f"{nome} é ludema com {carregam[nome]} jogo(s) carregando; "
                          "ludema só nasce com dois ou mais (senão é mecânica de um jogo)")
        ent = [a for a in arestas if a["To"] == nome and a["Type"] not in ESTRUTURAIS]
        sai = [a for a in arestas if a["From"] == nome and a["Type"] not in ESTRUTURAIS]
        no["entradas"] = len(ent)
        no["saidas"] = len(sai)
        no["melhor_confianca"] = min((a["confianca"] for a in ent if a["confianca"] in ORDEM), key=ORDEM.get, default="-")
        no["pendentes"] = sum(1 for a in ent if a["confianca"] == "D" or "conferir" in a["evidencia"].lower())
        if no["hub"] and no["saidas"] < 3:
            avisos.append(f"{nome} está marcado hub: true com só {no['saidas']} saída(s)")
        if no["entradas"] == 0 and no["saidas"] == 0 and no["pasta"] not in {"estudios", "pessoas"}:
            avisos.append(f"{nome} está órfã (sem arestas de influência)")


def relatorio(nos, arestas, erros, avisos) -> None:
    infl = [a for a in arestas if a["Type"] not in ESTRUTURAIS]
    print(f"nós: {len(nos)}  {dict(sorted(Counter(n['pasta'] for n in nos.values()).items()))}")
    print(f"arestas: {len(arestas)} (influência: {len(infl)}, estruturais: {len(arestas) - len(infl)})")
    print("confiança:", dict(sorted(Counter(a['confianca'] for a in infl).items())))
    print("relações:", dict(sorted(Counter(a['Type'] for a in arestas).items())))
    print("\nmais influentes (saídas de influência):")
    for nome, no in sorted(nos.items(), key=lambda kv: -kv[1]["saidas"])[:8]:
        if no["saidas"]:
            print(f"  {no['saidas']:2d}  {nome}{' #hub' if no['hub'] else ''}")
    if avisos:
        print("\navisos:")
        for a in avisos:
            print("  -", a)
    if erros:
        print("\nERROS:")
        for e in erros:
            print("  -", e)


def escrever(nos, arestas) -> None:
    DADOS.mkdir(parents=True, exist_ok=True)
    campos_no = ["Label", "Type", "pasta", "ano", "studio", "genero", "hub", "status",
                 "entradas", "saidas", "melhor_confianca", "pendentes", "tags", "arquivo"]
    with (DADOS / "nos.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos_no, extrasaction="ignore")
        w.writeheader()
        for no in nos.values():
            w.writerow({k: (str(v).lower() if isinstance(v, bool) else v) for k, v in no.items() if not k.startswith("_")})
    with (DADOS / "arestas.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["From", "To", "Type", "o_que_passou", "evidencia", "url", "confianca"])
        w.writeheader()
        w.writerows(arestas)

    forma = {"jogos": "box", "obras": "note", "mitos": "diamond", "ludemas": "hexagon", "pessoas": "ellipse", "estudios": "folder"}
    cor = {"A": "#1f8b4c", "B": "#2a6fb0", "C": "#c98a1b", "D": "#9a9a9a"}
    linhas = ["digraph influencias {",
              '  rankdir=LR; node [fontname="Helvetica", style=filled, fillcolor="#f4f1ea"]; edge [fontname="Helvetica", fontsize=9];']
    for pasta in PASTA_TIPOS:
        membros = [n for n in nos.values() if n["pasta"] == pasta]
        if not membros:
            continue
        linhas.append(f'  subgraph cluster_{pasta} {{ label="{pasta}"; color="#cccccc";')
        for no in membros:
            rot = no["Label"] + (f"\\n{no['ano']}" if no["ano"] else "")
            extra = ', penwidth=2, color="#b03a2e"' if no["hub"] else ""
            linhas.append(f'    "{no["Label"]}" [label="{rot}", shape={forma[pasta]}{extra}];')
        linhas.append("  }")
    for a in arestas:
        if a["Type"] in ESTRUTURAIS:
            estilo, c = "dotted", "#bbbbbb"
        elif a["Type"] in {"linhagem", "parece"}:
            estilo, c = "dashed", cor.get(a["confianca"], "#9a9a9a")
        else:
            estilo, c = "solid", cor.get(a["confianca"], "#9a9a9a")
        linhas.append(f'  "{a["From"]}" -> "{a["To"]}" [label="{a["Type"]}", color="{c}", style={estilo}];')
    linhas.append("}")
    (DADOS / "grafo.dot").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\nescrito: {DADOS.relative_to(VAULT)}/nos.csv, arestas.csv, grafo.dot")


def gravar_derivados(nos) -> int:
    n = 0
    for no in nos.values():
        campos = {k: str(no[k]) for k in DERIVADOS}
        if atualizar_frontmatter(no["_arq"], campos):
            n += 1
    return n


def main(argv: list[str]) -> int:
    nos, arestas, erros, avisos = carregar()
    derivar(nos, arestas, avisos)
    relatorio(nos, arestas, erros, avisos)
    if erros:
        return 1
    if "--check" not in argv:
        n = gravar_derivados(nos)
        print(f"campos derivados gravados em {n} nota(s)")
        escrever(nos, arestas)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
