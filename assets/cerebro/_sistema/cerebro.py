#!/usr/bin/env python3
"""Ferramenta do segundo cérebro de jogos (vault Obsidian).

Só biblioteca padrão. Rode a partir da raiz do vault (esta pasta, depois de copiá-la):

  python3 _sistema/cerebro.py check              # metadados, links, grafo; código 1 se houver erro
  python3 _sistema/cerebro.py indice             # regenera Índice.md a partir do frontmatter
  python3 _sistema/cerebro.py buscar --jogo oficina [--tema combate] [--tipo estudo] [--texto peça]
  python3 _sistema/cerebro.py mover ORIGEM DESTINO [--dry-run] [--titulo]
  python3 _sistema/cerebro.py migrar mapa.json [--dry-run]    # reorganização em lote
  python3 _sistema/cerebro.py onde "estudos/Estudo Hexa Drop.md"  # caminho antigo → atual
  python3 _sistema/cerebro.py cores                            # cores do Graph + Legenda do grafo

O contrato (tipos, temas, status) está em `Processo.md`. As pastas excluídas vêm de
`.obsidian/app.json` (`userIgnoreFilters`), para o Obsidian e este script verem o mesmo vault.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote, unquote

VAULT = Path(__file__).resolve().parent.parent
# Cópia avulsa: o vault é a raiz. Vault em docs/ de um laboratório: o pai tem workspace.json.
_PAI = VAULT.parent
WORKSPACE = _PAI if (_PAI / "workspace.json").exists() else VAULT
NOS = "genealogia-jogos/nos/"
INDICE = VAULT / "Índice.md"
EXPORTADOR = VAULT / "genealogia-jogos" / "_kit" / "exportar_grafo.py"

TIPOS = {
    "hub": "porta de navegação curada ou gerada",
    "visao": "recorte do grafo de genealogia",
    "estudo": "dossiê sobre referência externa: jogo, plataforma, mercado, pessoa",
    "pesquisa": "avaliação de método, ferramenta ou tecnologia para o nosso fluxo",
    "aprendizado": "lições de casos nossos, com prova",
    "plano": "PRD, plano de execução, visão de produto",
    "identidade": "bíblia, design system, banco de referências de arte",
    "operacao": "workspace, acervo, publicação, analytics, catálogo",
    "aula": "material de ensino",
    "registro": "parecer, revisão, relato, story, experimento concluído",
    "evidencia": "ficha, inventário, fonte primária organizada",
    "padrao": "princípio que se repete em duas ou mais fontes (ou candidato com uma)",
    "processo": "método de trabalho do estúdio ou deste cérebro",
    "captura": "entrada crua em _entrada/, ainda não classificada",
}
STATUS = {"vigente", "em-andamento", "rascunho", "historico", "superado"}
TEMAS = {
    "design", "combate", "progressao", "economia", "level-design", "narrativa", "mitologia",
    "arte", "animacao", "audio", "feel", "performance", "engenharia", "multiplayer", "ia",
    "processo", "publicacao", "ugc", "juridico", "video", "ensino",
}
# Cada tipo mora numa pasta, como os nós do grafo. `hub` e `processo` ficam na raiz.
PASTA_DO_TIPO = {
    "estudo": "estudos", "pesquisa": "pesquisas", "aprendizado": "aprendizados", "plano": "planos",
    "identidade": "identidade", "operacao": "operacao", "aula": "aulas", "registro": "registros",
    "evidencia": "evidencias", "padrao": "padroes", "visao": "genealogia-jogos/visoes", "captura": "_entrada",
}
PASTAS_DO_VAULT = set(PASTA_DO_TIPO.values()) | {"", "genealogia-jogos", "_sistema", "_anexos"}
# Nome de arquivo diz o que a nota é. Estes não dizem nada.
NOMES_GENERICOS = {
    "readme", "leia-me", "leiame", "estudo", "index", "indice", "notes", "notas", "nota", "report", "relatorio",
    "mission", "resources", "protocol", "source", "plano", "parecer", "design", "claude", "grok", "todo",
    "draft", "rascunho", "doc", "docs", "brief", "resumo", "untitled", "sem título",
}
# Tipos que precisam dizer a que servem (temas) quando não são parte de outra nota.
PRECISA_TEMAS = {"estudo", "pesquisa", "aprendizado", "plano", "identidade", "operacao", "aula", "registro", "padrao"}
FAMILIAS = {"design", "metodo", "armadilha"}
FORCAS = {"confirmado", "candidato"}

# Notas cujo frontmatter pertence a outro repositório (symlink para o framework). O contrato delas
# vive aqui para o índice e a busca não perderem essas portas.
SIDECAR = {}

WIKILINK = re.compile(r"(!?)\[\[([^\]\n]+?)\]\]")
MDLINK = re.compile(r"(!?)\[([^\]\n]*)\]\((<[^>\n]+>|[^)\s]+)(\s+\"[^\"]*\")?\)")
CODE_FENCE = re.compile(r"^(```|~~~)")


# ───────────────────────── leitura do vault ─────────────────────────

def filtros_ignorados() -> list[str]:
    try:
        app = json.loads((VAULT / ".obsidian" / "app.json").read_text(encoding="utf-8"))
        return [f for f in app.get("userIgnoreFilters", []) if isinstance(f, str)]
    except (OSError, ValueError):
        return []


def ignorado(rel: str, filtros: list[str]) -> bool:
    partes = rel.split("/")
    if any(p.startswith(".") or p == "node_modules" for p in partes):
        return True
    for f in filtros:
        if f.startswith("/") and f.endswith("/") and len(f) > 2:
            if re.search(f[1:-1], rel):
                return True
        elif rel.startswith(f):
            return True
    return False


def parse_frontmatter(texto: str) -> tuple[dict, int]:
    """YAML mínimo: `chave: valor`, `chave: [a, b]` e listas `- item`. Chaves aninhadas ficam como ''.

    Devolve (dados, offset do corpo)."""
    if not texto.startswith("---\n"):
        return {}, 0
    fim = texto.find("\n---", 3)
    if fim == -1:
        return {}, 0
    dados: dict = {}
    chave = None
    for linha in texto[4:fim].splitlines():
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        if linha.startswith((" ", "\t")):
            item = linha.strip()
            if item.startswith("- ") and chave is not None and isinstance(dados.get(chave), list):
                dados[chave].append(_limpa(item[2:]))
            continue
        if ":" not in linha:
            continue
        k, _, v = linha.partition(":")
        chave, v = k.strip(), v.strip()
        if v == "":
            dados[chave] = []
        elif v.startswith("[") and v.endswith("]") and not v.startswith("[["):
            miolo = v[1:-1].strip()
            dados[chave] = [_limpa(x) for x in miolo.split(",")] if miolo else []
        else:
            dados[chave] = _limpa(v)
    corpo = texto.find("\n", fim + 1)
    return dados, (corpo + 1 if corpo != -1 else len(texto))


def _limpa(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v.replace('\\"', '"')


def lista(v) -> list[str]:
    if isinstance(v, list):
        return [x for x in v if x]
    return [v] if v else []


class Nota:
    def __init__(self, caminho: Path):
        self.caminho = caminho
        self.rel = caminho.relative_to(VAULT).as_posix()
        self.chave = self.rel[:-3] if self.rel.endswith(".md") else self.rel
        self.nome = caminho.stem
        self.texto = caminho.read_text(encoding="utf-8", errors="replace")
        self.meta, self.inicio_corpo = parse_frontmatter(self.texto) if caminho.suffix == ".md" else ({}, 0)
        for k, v in SIDECAR.get(self.rel, {}).items():
            self.meta.setdefault(k, v)
        self.no_grafo = self.rel.startswith(NOS)

    @property
    def titulo(self) -> str:
        m = re.search(r"^# (.+)$", self.texto[self.inicio_corpo:], re.M)
        t = m.group(1).strip() if m else self.nome
        return t if "{{" not in t else self.nome

    @property
    def tipo(self) -> str:
        return str(self.meta.get("tipo") or "")

    @property
    def resumo(self) -> str:
        """O `resumo` do frontmatter; nos nós do grafo, a frase em destaque (`> …`) logo após o título."""
        if self.meta.get("resumo"):
            return str(self.meta["resumo"])
        m = re.search(r"^> (.+)$", self.texto[self.inicio_corpo:], re.M)
        if m:
            return re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", m.group(1)).strip()[:280]
        return ""

    def link(self, ambiguos: set[str], tabela: bool = False) -> str:
        alvo = self.chave if unicodedata.normalize("NFC", self.nome).lower() in ambiguos else self.nome
        rotulo = self.titulo.replace("|", "-").replace("[", "(").replace("]", ")") if self.titulo != self.nome else ""
        barra = "\\|" if tabela else "|"
        return f"[[{alvo}{barra}{rotulo}]]" if rotulo else f"[[{alvo}]]"


def carregar() -> tuple[list[Nota], list[str]]:
    """Notas visíveis (fora das exclusões) e todos os arquivos que um link pode alcançar."""
    filtros = filtros_ignorados()
    notas, todos = [], []
    for p in sorted(VAULT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(VAULT).as_posix()
        if any(x.startswith(".") or x == "node_modules" for x in rel.split("/")):
            continue
        todos.append(rel)
        if p.suffix == ".md" and not ignorado(rel, filtros):
            notas.append(Nota(p))
    return notas, todos


class Resolvedor:
    """Resolve wikilinks como o Obsidian: caminho relativo ao vault ou nome único."""

    def __init__(self, notas: list[Nota], todos: list[str]):
        self.por_chave: dict[str, str] = {}
        self.por_nome: dict[str, list[str]] = defaultdict(list)
        for rel in todos:
            nome = rel.rsplit("/", 1)[-1]
            if rel.endswith(".md"):
                self._add(rel[:-3], nome[:-3])
            else:
                self._add(rel, nome)
                if rel.endswith((".canvas", ".base")):
                    self._add(rel.rsplit(".", 1)[0], nome.rsplit(".", 1)[0])
        self.ambiguos = {k for k, v in self.por_nome.items() if len(set(v)) > 1}  # chaves NFC minúsculas

    @staticmethod
    def _k(texto: str) -> str:
        return unicodedata.normalize("NFC", texto).lower()

    def _add(self, chave: str, nome: str) -> None:
        self.por_chave[self._k(chave)] = chave
        self.por_nome[self._k(nome)].append(chave)

    def resolver(self, alvo: str) -> tuple[str | None, str]:
        """Devolve (chave, situacao) com situacao em ok | ambiguo | quebrado."""
        alvo = alvo.split("|", 1)[0].split("#", 1)[0].strip().rstrip("\\").replace("\\", "/")
        if not alvo:
            return None, "ok"
        base = alvo[:-3] if alvo.lower().endswith(".md") else alvo
        k = self._k(base)
        if k in self.por_chave:
            return self.por_chave[k], "ok"
        if "/" in base:
            sufixo = [c for c in self.por_chave.values() if self._k(c).endswith("/" + k)]
            if len(sufixo) == 1:
                return sufixo[0], "ok"
            return None, "quebrado"
        opcoes = sorted(set(self.por_nome.get(k, [])))
        if len(opcoes) == 1:
            return opcoes[0], "ok"
        if opcoes:
            return min(opcoes, key=len), "ambiguo"
        return None, "quebrado"


def sem_codigo(texto: str) -> str:
    """Remove blocos e trechos de código para não contar links de exemplo."""
    saida, dentro = [], False
    for linha in texto.splitlines():
        if CODE_FENCE.match(linha.strip()):
            dentro = not dentro
            saida.append("")
            continue
        saida.append("" if dentro else re.sub(r"`[^`\n]*`", "", linha))
    return "\n".join(saida)


def wikilinks(texto: str) -> list[str]:
    return [m.group(2) for m in WIKILINK.finditer(sem_codigo(texto))]


def mdlinks(texto: str) -> list[str]:
    return [m.group(3) for m in MDLINK.finditer(sem_codigo(texto))]


def alvo_local(href: str) -> str | None:
    href = href[1:-1] if href.startswith("<") and href.endswith(">") else href
    if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) or href.startswith("#"):
        return None
    return unquote(href.split("#", 1)[0]) or None


# ───────────────────────── check ─────────────────────────

def _normal(p: Path) -> Path:
    """Caminho absoluto sem seguir symlinks (framework/core é um link)."""
    return Path(os.path.normpath(p))


def _modulo_vazio(destino: Path) -> str | None:
    """Se o link cai num módulo do workspace.json que está vazio (não baixado), devolve o caminho dele."""
    try:
        modulos = json.loads((WORKSPACE / "workspace.json").read_text(encoding="utf-8")).get("modules", [])
    except (OSError, ValueError):
        return None
    for m in modulos:
        raiz = WORKSPACE / str(m.get("path", ""))
        if raiz != WORKSPACE and (destino == raiz or raiz in destino.parents):
            if not raiz.exists() or not any(raiz.iterdir()):
                return str(m.get("path"))
    return None


def _limpo(titulo: str) -> str:
    """Título como o Obsidian compara em [[Nota#Título]]: sem # | ^ : [ ] %% e espaços repetidos."""
    t = re.sub(r"[#|^:\[\]]|%%", " ", unquote(titulo))
    return re.sub(r"\s+", " ", t).strip().lower()


def nossos_jogos(notas: list[Nota]) -> dict[str, Nota]:
    """Nós de jogo com a tag `nosso`; `projeto` aponta a pasta de código quando existe."""
    return {n.chave: n for n in notas if n.no_grafo and "nosso" in lista(n.meta.get("tags"))}


NIVEIS = {"erro": 0, "aviso": 1, "info": 2}


class Achados:
    """Diagnóstico endereçável: nível, código, arquivo e linha.

    O `check` imprime, o `--json` publica e o hook de pós-edição filtra pelo arquivo que
    acabou de mudar. Mensagem solta em lista de strings não permite nenhum dos três.
    """

    def __init__(self) -> None:
        self.itens: list[dict] = []

    def add(self, nivel: str, codigo: str, arquivo: str, msg: str, linha: int | None = None) -> None:
        self.itens.append({"nivel": nivel, "codigo": codigo, "arquivo": arquivo, "msg": msg, "linha": linha})

    def de(self, *niveis: str) -> list[dict]:
        return [i for i in self.itens if i["nivel"] in niveis]

    def do_codigo(self, codigo: str) -> list[dict]:
        return [i for i in self.itens if i["codigo"] == codigo]

    def do_arquivo(self, rel: str) -> list[dict]:
        return [i for i in self.itens if i["arquivo"] == rel]

    @staticmethod
    def linha_legivel(i: dict) -> str:
        onde = i["arquivo"] + (f":{i['linha']}" if i["linha"] else "")
        return f"[{i['codigo']}] {onde}: {i['msg']}"


def checar_skills(res: Resolvedor, ach: Achados) -> None:
    """Skills de agente em `.agents/skills/`: ficam fora do vault visível, então o check as valida aqui.

    Sem isso, um wikilink para nota que só existe no laboratório de origem apodrece em silêncio.
    """
    for pasta in sorted(VAULT.glob("**/.agents/skills")):
        if not pasta.is_dir():
            continue
        for arq in sorted(pasta.rglob("*.md")):
            rel = arq.relative_to(VAULT).as_posix()
            texto = arq.read_text(encoding="utf-8", errors="replace")
            if arq.name == "SKILL.md":
                meta, _ = parse_frontmatter(texto)
                faltando = [c for c in ("name", "description") if not str(meta.get(c) or "").strip()]
                if faltando:
                    ach.add("erro", "SKILL_META", rel, f"skill sem {' e '.join(faltando)} no frontmatter")
            for alvo in wikilinks(texto):
                chave, sit = res.resolver(alvo.split("|", 1)[0].rstrip("\\").partition("#")[0])
                if sit == "quebrado":
                    ach.add("erro", "SKILL_LINK", rel, f"[[{alvo}]] não existe neste vault "
                            "(nota do laboratório de origem? troque pelo exemplo daqui)")
                elif sit == "ambiguo":
                    ach.add("aviso", "SKILL_LINK", rel, f"[[{alvo}]] é ambíguo; use o caminho (ex.: [[{chave}]])")


def cmd_check(args) -> int:
    notas, outros = carregar()
    res = Resolvedor(notas, outros)
    jogos = nossos_jogos(notas)
    ach = Achados()
    entrada: Counter[str] = Counter()
    sem_meta: list[str] = []
    externos: list[str] = []
    nao_baixados: Counter[str] = Counter()
    titulos_por_nota = {n.chave: {_limpo(h) for h in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", sem_codigo(n.texto), re.M)}
                        for n in notas}
    nomes_visiveis = Counter(unicodedata.normalize("NFC", n.nome).lower() for n in notas)
    for n in notas:
        if nomes_visiveis[unicodedata.normalize("NFC", n.nome).lower()] > 1:
            ach.add("erro", "NOME_REPETIDO", n.rel, "outro arquivo tem o mesmo nome; nomes de nota são únicos no vault")

    for n in notas:
        # links no corpo e nas propriedades
        for alvo in wikilinks(n.texto):
            chave, sit = res.resolver(alvo)
            ancora = alvo.split("|", 1)[0].rstrip("\\").partition("#")[2]
            if chave and sit == "ok" and ancora and not ancora.startswith("^") and chave in titulos_por_nota:
                if _limpo(ancora) not in titulos_por_nota[chave]:
                    ach.add("aviso", "ANCORA", n.rel, f"[[{alvo.split('|')[0].rstrip(chr(92))}]] aponta para seção que não existe")
            if sit == "quebrado":
                ach.add("erro", "LINK", n.rel, f"[[{alvo}]] não existe")
            elif sit == "ambiguo":
                ach.add("aviso", "LINK_AMBIGUO", n.rel, f"[[{alvo}]] é ambíguo; use o caminho (ex.: [[{chave}]])")
            if chave and chave != n.chave:
                entrada[chave] += 1
        if n.caminho.is_symlink():
            continue  # nota canônica em outro repositório; os links dela valem lá
        for href in mdlinks(n.texto):
            alvo = alvo_local(href)
            if not alvo:
                continue
            destino = _normal(n.caminho.parent / alvo)
            dentro = destino == VAULT or VAULT in destino.parents
            if not destino.exists():
                if dentro:
                    ach.add("erro", "LINK_LOCAL", n.rel, f"link ({href}) aponta para arquivo inexistente no vault")
                elif (modulo := _modulo_vazio(destino)):
                    nao_baixados[modulo] += 1
                else:
                    externos.append(f"{n.rel}: ({href})")
                continue
            if dentro:
                rel = destino.relative_to(VAULT).as_posix()
                entrada[rel[:-3] if rel.endswith(".md") else rel] += 1

        if n.rel.startswith(NOS + "ludemas/") and "## Invariante" not in n.texto:
            ach.add("aviso", "SEM_INVARIANTE", n.rel,
                    "ludema sem seção Invariante: sem ela, regularidade observada (n=) passa por contrato")
        if n.no_grafo or n.rel.startswith("_sistema/") or n.rel.startswith("_entrada/"):
            continue
        pasta = n.rel.rsplit("/", 1)[0] if "/" in n.rel else ""
        if pasta not in PASTAS_DO_VAULT:
            ach.add("erro", "PASTA", n.rel, f"pasta fora do contrato; notas moram em {', '.join(sorted(p for p in PASTAS_DO_VAULT if p))} ou na raiz")
        if unicodedata.normalize("NFC", n.nome).lower() in NOMES_GENERICOS:
            ach.add("erro", "NOME_GENERICO", n.rel, "nome genérico; o nome do arquivo precisa dizer o que a nota é")
        elif pasta in set(PASTA_DO_TIPO.values()) - {"genealogia-jogos/visoes"} and len(n.nome.split()) < 2:
            ach.add("aviso", "NOME_CURTO", n.rel, "nome de uma palavra só; prefira 'Assunto — aspecto'")
        titulo_ok = {n.nome, f"Visão · {n.nome}"}
        if n.titulo not in titulo_ok and not n.caminho.is_symlink() and pasta in PASTAS_DO_VAULT - {"", "genealogia-jogos"}:
            ach.add("aviso", "TITULO", n.rel, f"o título (# {n.titulo[:50]}) difere do nome do arquivo")
        m = n.meta
        if not m.get("tipo"):
            sem_meta.append(n.rel)
            continue
        if n.tipo not in TIPOS:
            ach.add("erro", "TIPO", n.rel, f"tipo {n.tipo!r} fora do contrato ({', '.join(sorted(TIPOS))})")
        elif n.tipo in PASTA_DO_TIPO and pasta != PASTA_DO_TIPO[n.tipo]:
            ach.add("erro", "TIPO_PASTA", n.rel, f"tipo {n.tipo} mora em {PASTA_DO_TIPO[n.tipo]}/")
        elif n.tipo in {"hub", "processo"} and pasta not in {"", "genealogia-jogos", "_entrada"}:
            ach.add("erro", "TIPO_RAIZ", n.rel, f"{n.tipo} mora na raiz do vault")
        if not str(m.get("resumo") or "").strip():
            ach.add("aviso", "RESUMO", n.rel, "sem resumo")
        elif len(str(m.get("resumo"))) > 280:
            ach.add("aviso", "RESUMO_LONGO", n.rel, f"resumo com {len(str(m['resumo']))} caracteres (máx. 280)")
        st = str(m.get("status") or "")
        if st not in STATUS:
            ach.add("erro", "STATUS", n.rel, f"status {st!r} inválido ({', '.join(sorted(STATUS))})")
        for t in lista(m.get("temas")):
            if t not in TEMAS:
                ach.add("erro", "TEMA", n.rel, f"tema {t!r} fora do vocabulário ({', '.join(sorted(TEMAS))})")
        if n.tipo in PRECISA_TEMAS and not m.get("parte_de") and st != "superado" and not lista(m.get("temas")):
            ach.add("aviso", "TEMAS", n.rel, "sem temas")
        for j in lista(m.get("jogos")):
            chave, _ = res.resolver(j.strip("[]"))
            if chave not in jogos:
                ach.add("erro", "JOGOS", n.rel, f"jogos → {j} não é um nó nosso (nó em {NOS}jogos com tag `nosso`)")
        if m.get("data") and not re.fullmatch(r"20\d\d-\d\d-\d\d", str(m.get("data"))):
            ach.add("erro", "DATA", n.rel, f"data {m.get('data')!r} fora do formato AAAA-MM-DD")
        for r in lista(m.get("referencias")):
            chave, _ = res.resolver(r.strip("[]"))
            if not chave or not chave.startswith(NOS):
                ach.add("erro", "REFERENCIAS", n.rel, f"referencias → {r} não é um nó do grafo ({NOS})")
        if n.tipo == "padrao":
            if str(m.get("familia", "")) not in FAMILIAS:
                ach.add("erro", "FAMILIA", n.rel, f"familia {m.get('familia')!r} ({', '.join(sorted(FAMILIAS))})")
            if str(m.get("forca", "")) not in FORCAS:
                ach.add("erro", "FORCA", n.rel, f"forca {m.get('forca')!r} ({', '.join(sorted(FORCAS))})")
            if not re.search(r"^- Fronteira:", n.texto[n.inicio_corpo:], re.M):
                ach.add("aviso", "SEM_FRONTEIRA", n.rel,
                        "padrão sem fronteira: diga onde a regra deixa de valer, senão ela vira dogma")
        for campo in ("parte_de", "substituido_por"):
            for v in lista(m.get(campo)):
                if not v.startswith("[["):
                    ach.add("erro", "WIKILINK_CAMPO", n.rel, f"{campo} precisa ser wikilink, veio {v!r}")
        if st == "superado" and not m.get("substituido_por"):
            ach.add("aviso", "SUBSTITUIDO", n.rel, "status superado sem substituido_por")

    checar_skills(res, ach)

    for rel in sem_meta:
        ach.add("aviso", "FRONTMATTER", rel, "sem o frontmatter do contrato (tipo, resumo, status)")
    for n in notas:
        if (not n.no_grafo and not n.rel.startswith("_") and n.tipo != "evidencia"
                and not n.meta.get("parte_de") and entrada[n.chave] == 0
                and n.rel not in {"00 Comece Aqui.md", "AGENTS.md"}):
            ach.add("info", "ORFA", n.rel, "nenhuma nota linka para esta")
    for modulo, qtd in sorted(nao_baixados.items()):
        ach.add("info", "MODULO", modulo, f"{qtd} link(s) para módulo não baixado nesta máquina "
                                          "(não é defeito; `workspace.py` obtém)")
    if externos:
        ach.add("aviso", "LINK_EXTERNO", "(vault)",
                f"{len(externos)} link(s) para fora do vault sem arquivo no disco (ex.: {externos[0]})")
        if args.externos:
            for e in externos:
                rel, _, href = e.partition(": ")
                ach.add("aviso", "LINK_EXTERNO", rel, f"link {href} sem arquivo no disco")

    codigo = 1 if ach.de("erro") else 0
    saida_grafo = ""
    if EXPORTADOR.exists() and not args.sem_grafo:
        r = subprocess.run([sys.executable, str(EXPORTADOR), "--check"], capture_output=True, text=True)
        saida_grafo = (r.stdout.strip() + ("\n" + r.stderr.strip() if r.returncode else "")).strip()
        if r.returncode:
            ach.add("erro", "GRAFO", "genealogia-jogos/", "exportar_grafo.py --check falhou; veja a saída do grafo")
            codigo = 1
    try:
        atuais = json.loads(GRAPH.read_text(encoding="utf-8")).get("colorGroups", [])
    except (OSError, ValueError):
        atuais = []
    if atuais != grupos_de_cor():
        ach.add("info", "CORES", ".obsidian/graph.json",
                "cores do Graph fora do padrão (o Obsidian pode ter regravado): rode `cerebro.py cores`")
    if not codigo and INDICE.exists() and INDICE.read_text(encoding="utf-8") != gerar_indice(notas, res):
        ach.add("info", "INDICE", INDICE.name, "Índice.md desatualizado: rode `cerebro.py indice`")

    piso = NIVEIS[args.nivel]
    itens = [i for i in ach.itens if NIVEIS[i["nivel"]] <= piso]
    nomes = Counter(n.nome for n in notas)
    repetidos = sorted(k for k, v in nomes.items() if v > 1)
    resumo = {
        "notas": len(notas),
        "grafo": sum(n.no_grafo for n in notas),
        "nossos_jogos": len(jogos),
        "tipos": dict(sorted(Counter(n.tipo or "—" for n in notas if not n.no_grafo).items())),
        "nomes_repetidos": repetidos,
        "por_nivel": {k: len(ach.de(k)) for k in NIVEIS},
        "por_codigo": dict(sorted(Counter(i["codigo"] for i in ach.itens).items())),
    }
    if args.json:
        print(json.dumps({"vault": str(VAULT), "resumo": resumo, "itens": itens,
                          "grafo": saida_grafo, "codigo_de_saida": codigo},
                         ensure_ascii=False, indent=2))
        return codigo

    print(f"vault: {VAULT}")
    print(f"notas: {len(notas)}  (grafo: {resumo['grafo']}; nossos jogos: {len(jogos)})")
    print("tipos:", resumo["tipos"])
    print(f"nomes repetidos (use caminho no wikilink): {', '.join(repetidos) or 'nenhum'}")

    def bloco(titulo: str, lista: list[dict], limite: int | None) -> None:
        if not lista:
            return
        print(f"\n{titulo} ({len(lista)}):")
        for i in lista[:limite] if limite else lista:
            print("  -", Achados.linha_legivel(i))
        if limite and len(lista) > limite:
            print(f"  … e mais {len(lista) - limite}")

    info = [i for i in itens if i["nivel"] == "info"]
    bloco("atenção", info, args.limite)
    bloco("avisos", [i for i in itens if i["nivel"] == "aviso"], args.limite)
    bloco("ERROS", [i for i in itens if i["nivel"] == "erro"], None)
    if saida_grafo:
        print("\n── grafo (exportar_grafo.py --check) ──")
        print(saida_grafo)
    return codigo


# ───────────────────────── índice ─────────────────────────

def _celula(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def gerar_indice(notas: list[Nota], res: Resolvedor) -> str:
    jogos = nossos_jogos(notas)
    classificadas = [n for n in notas if not n.no_grafo and n.tipo and n.tipo != "captura"
                     and not n.rel.startswith("_sistema/") and n.rel != INDICE.name]
    partes_de: Counter[str] = Counter()
    for n in classificadas:
        for p in lista(n.meta.get("parte_de")):
            chave, _ = res.resolver(p.strip("[]"))
            if chave:
                partes_de[chave] += 1

    def linha(n: Nota) -> str:
        extra = f" · +{partes_de[n.chave]} partes" if partes_de[n.chave] else ""
        return (f"| {n.link(res.ambiguos, tabela=True)} | {n.tipo} | {n.meta.get('status', '')} | "
                f"{_celula(n.meta.get('resumo', ''))}{extra} |")

    cab = "| Nota | Tipo | Status | Resumo |\n|---|---|---|---|"
    out = [
        "---",
        "tipo: hub",
        'resumo: "Gerado a partir do frontmatter: notas por jogo nosso, por tema e por tipo. Não editar à mão."',
        "status: vigente",
        "---",
        "# Índice",
        "",
        "> Gerado por `python3 _sistema/cerebro.py indice`. Para mudar uma linha, edite o",
        "> frontmatter da nota (`tipo`, `resumo`, `jogos`, `temas`, `status`) e rode de novo.",
        "> Contrato em [[Processo]]. Navegação curada em [[00 Comece Aqui]].",
        "",
        "## Por jogo nosso",
        "",
    ]
    for chave, jogo in sorted(jogos.items(), key=lambda kv: kv[1].nome.lower()):
        ligadas = [n for n in classificadas
                   if any(res.resolver(j.strip("[]"))[0] == chave for j in lista(n.meta.get("jogos")))]
        out.append(f"### {jogo.nome}")
        out.append("")
        codigo = f" · código: `{jogo.meta['projeto']}`" if jogo.meta.get("projeto") else " · sem pasta de código"
        out.append(f"Nó: [[{jogo.nome}]]{codigo}")
        out.append("")
        if ligadas:
            out += [cab] + [linha(n) for n in sorted(ligadas, key=lambda n: (n.tipo, n.rel))]
        else:
            out.append("Nenhuma nota do cérebro declara este jogo em `jogos:` ainda.")
        out.append("")

    out += ["## Por tema", ""]
    por_tema: dict[str, list[Nota]] = defaultdict(list)
    for n in classificadas:
        for t in lista(n.meta.get("temas")):
            por_tema[t].append(n)
    for t in sorted(por_tema):
        itens = sorted(por_tema[t], key=lambda n: (n.tipo, n.rel))
        out.append(f"### {t}")
        out.append("")
        out += [f"- {n.link(res.ambiguos)} · {n.tipo} — {_celula(n.meta.get('resumo', ''))}" for n in itens]
        out.append("")

    out += ["## Por tipo", "", "Notas principais; as partes de um estudo aparecem na nota-mãe (`parte_de`).", ""]
    principais = [n for n in classificadas if not n.meta.get("parte_de")]
    for tipo in TIPOS:
        itens = sorted((n for n in principais if n.tipo == tipo), key=lambda n: n.rel)
        if not itens:
            continue
        out.append(f"### {tipo} — {TIPOS[tipo]}")
        out.append("")
        out += [cab] + [linha(n) for n in itens]
        out.append("")

    pendentes = [n for n in notas if not n.no_grafo and not n.tipo and not n.rel.startswith("_sistema/")]
    entrada = [n for n in notas if n.rel.startswith("_entrada/") and n.nome != "Entrada"]
    if pendentes or entrada:
        out += ["## A classificar", ""]
        out += [f"- {n.link(res.ambiguos)}" for n in sorted(pendentes + entrada, key=lambda n: n.rel)]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def cmd_indice(args) -> int:
    notas, outros = carregar()
    res = Resolvedor(notas, outros)
    texto = gerar_indice(notas, res)
    anterior = INDICE.read_text(encoding="utf-8") if INDICE.exists() else ""
    if texto == anterior:
        print("Índice.md já está atualizado.")
    else:
        INDICE.write_text(texto, encoding="utf-8")
        print(f"Índice.md regenerado ({texto.count(chr(10))} linhas).")
    return 0


# ───────────────────────── buscar ─────────────────────────

def cmd_buscar(args) -> int:
    notas, outros = carregar()
    res = Resolvedor(notas, outros)
    jogos = nossos_jogos(notas)
    alvo_jogo = None
    if args.jogo:
        q = args.jogo.lower().strip("/")
        for chave, n in jogos.items():
            projeto = str(n.meta.get("projeto", "")).lower().strip("/")
            if q in {n.nome.lower(), projeto, projeto.rsplit("/", 1)[-1]}:
                alvo_jogo = chave
        if not alvo_jogo:
            print(f"jogo {args.jogo!r} não encontrado. Nossos jogos: "
                  + ", ".join(f"{n.nome} ({n.meta.get('projeto') or 'sem pasta de código'})" for n in jogos.values()))
            return 1
    achadas = []
    for n in notas:
        if n.no_grafo and n.chave != alvo_jogo and not args.grafo:
            continue
        m = n.meta
        if args.tipo and n.tipo != args.tipo:
            continue
        if args.tema and args.tema not in lista(m.get("temas")):
            continue
        if alvo_jogo and n.chave != alvo_jogo:
            declarados = {res.resolver(j.strip("[]"))[0] for j in lista(m.get("jogos"))}
            menciona = alvo_jogo.rsplit("/", 1)[-1] in {res.resolver(w)[0].rsplit("/", 1)[-1]
                                                        for w in wikilinks(n.texto) if res.resolver(w)[0]}
            if alvo_jogo not in declarados and not (args.mencoes and menciona):
                continue
        if args.texto:
            q = args.texto.lower()
            if q not in n.titulo.lower() and q not in str(m.get("resumo", "")).lower() and \
                    (not args.corpo or q not in n.texto.lower()):
                continue
        achadas.append(n)
    if args.json:
        print(json.dumps([{"caminho": n.rel, "titulo": n.titulo, "tipo": n.tipo,
                           "status": n.meta.get("status", ""), "resumo": n.resumo,
                           "temas": lista(n.meta.get("temas")), "jogos": lista(n.meta.get("jogos")),
                           "referencias": lista(n.meta.get("referencias")), "data": n.meta.get("data", "")}
                          for n in achadas], ensure_ascii=False, indent=2))
        return 0
    for n in sorted(achadas, key=lambda n: (n.tipo, n.rel)):
        print(f"{n.rel}\n    {n.tipo or '—'} · {n.meta.get('status', '—')} · {n.resumo or n.titulo}")
    print(f"\n{len(achadas)} nota(s).")
    if alvo_jogo:
        secoes = padroes_do_jogo(jogos[alvo_jogo].nome)
        if secoes:
            print(f"\nPadrões que agem em {jogos[alvo_jogo].nome} (padroes/):")
            for s in secoes:
                print(f"  - {s}")
    return 0


def padroes_do_jogo(nome: str) -> list[str]:
    """Padrões (notas em padroes/) que declaram o jogo em `jogos`."""
    achados = []
    for arq in sorted((VAULT / "padroes").glob("*.md")):
        meta, _ = parse_frontmatter(arq.read_text(encoding="utf-8"))
        if any(j.strip("[]").split("|")[0] == nome for j in lista(meta.get("jogos"))):
            rotulo = "" if meta.get("forca") == "confirmado" else "(candidato) "
            achados.append(f"{rotulo}{arq.stem} [{meta.get('familia', '')}]")
    return achados


# ───────────────────────── mover e migrar ─────────────────────────

REDIRECIONAMENTOS = VAULT / "_sistema" / "redirecionamentos.json"
WIKI_CRU = re.compile(r"(!?)\[\[([^\]\n]+?)\]\]")


def _expandir(mapa: dict[str, str]) -> dict[Path, Path]:
    """Entradas de pasta viram uma entrada por arquivo, inclusive ocultos e ignorados pelo Git."""
    arquivos: dict[Path, Path] = {}
    for velho, novo in mapa.items():
        o, d = _normal(VAULT / velho), _normal(VAULT / novo)
        if o.is_dir() and not o.is_symlink():
            for p in sorted(o.rglob("*")):
                if p.is_file() or p.is_symlink():
                    arquivos[_normal(p)] = d / p.relative_to(o)
        elif o.exists() or o.is_symlink():
            arquivos[o] = d
        else:
            raise SystemExit(f"origem inexistente: {velho}")
    return arquivos


def _chave(p: Path) -> str:
    rel = p.relative_to(VAULT).as_posix()
    return rel[:-3] if rel.endswith(".md") else rel


def _alvos_de_reescrita(filtros: list[str]) -> list[Path]:
    """Notas visíveis, skills do grafo, canvases e bases. Recibos em pastas excluídas ficam intactos."""
    alvos = []
    for p in sorted(VAULT.rglob("*")):
        if not p.is_file() or p.is_symlink() or p.suffix not in {".md", ".canvas", ".base"}:
            continue
        rel = p.relative_to(VAULT).as_posix()
        if rel.startswith(".obsidian/"):
            continue
        if "/.agents/" in "/" + rel:
            alvos.append(p)
        elif not ignorado(rel, filtros):
            alvos.append(p)
    return alvos


def aplicar_mapa(mapa: dict[str, str], simular: bool = False, titulo_do_arquivo: bool = False) -> dict:
    """Move arquivos e pastas do vault e reescreve os links de todas as notas numa passada só.

    - Link Markdown para nota do vault vira wikilink pelo nome novo; para outros arquivos, caminho relativo novo.
    - Wikilink (com caminho ou nome único) para arquivo movido passa a usar o nome novo.
    - `.canvas` e `.base` recebem os caminhos novos.
    - Com `titulo_do_arquivo`, o primeiro `# título` das notas renomeadas passa a ser o nome do arquivo.
    - Grava `_sistema/redirecionamentos.json` (caminho antigo → novo).
    """
    filtros = filtros_ignorados()
    arquivos = _expandir(mapa)
    destinos = list(arquivos.values())
    if len(set(destinos)) != len(destinos):
        repetidos = [d for d, n in Counter(destinos).items() if n > 1]
        raise SystemExit(f"dois arquivos para o mesmo destino: {repetidos[:5]}")
    for o, d in arquivos.items():
        if (d.exists() or d.is_symlink()) and d not in arquivos:
            raise SystemExit(f"destino já existe: {d.relative_to(VAULT)}")

    notas, todos = carregar()
    antigo = Resolvedor(notas, todos)
    # nomes depois da migração, para decidir entre [[Nome]] e [[pasta/Nome]]
    novos_md = []
    for rel in todos:
        p = _normal(VAULT / rel)
        q = arquivos.get(p, p)
        if q.suffix == ".md" and not ignorado(q.relative_to(VAULT).as_posix(), filtros):
            novos_md.append(q)
    contagem = Counter(unicodedata.normalize("NFC", q.stem).lower() for q in novos_md)

    def novo_de(p: Path) -> Path:
        return arquivos.get(p, p)

    def wikilink_para(q: Path, ancora: str, rotulo: str | None, barra: str) -> str:
        nome = q.stem if q.suffix == ".md" else q.name
        alvo = nome if contagem[unicodedata.normalize("NFC", q.stem).lower()] <= 1 or q.suffix != ".md" \
            else _chave(q)
        if rotulo is not None and rotulo.strip() and rotulo.strip() != nome:
            return f"[[{alvo}{ancora}{barra}{rotulo}]]"
        return f"[[{alvo}{ancora}]]"

    def reescrever(texto: str, velho: Path, novo: Path) -> str:
        pasta_velha, pasta_nova = velho.parent, novo.parent

        def md(m: re.Match) -> str:
            bang, rotulo, href, titulo = m.group(1), m.group(2), m.group(3), m.group(4) or ""
            alvo = alvo_local(href)
            if not alvo:
                return m.group(0)
            ancora = "#" + href.split("#", 1)[1] if "#" in href else ""
            antes = _normal(pasta_velha / alvo)
            depois = novo_de(antes)
            if depois == antes:  # pasta movida inteira, ou arquivo que só existe dentro dela
                for o, d in mapa_pastas:
                    if antes == o or o in antes.parents:
                        depois = d / antes.relative_to(o)
                        break
            movido = depois != antes
            if not movido and velho == novo:
                return m.group(0)
            dentro = VAULT in depois.parents
            if (dentro and depois.suffix == ".md" and not bang
                    and not ignorado(depois.relative_to(VAULT).as_posix(), filtros)):
                return wikilink_para(depois, unquote(ancora), rotulo, "|")
            rel = os.path.relpath(depois, pasta_nova).replace(os.sep, "/")
            return f"{bang}[{rotulo}]({quote(rel, safe='/._-~()')}{ancora}{titulo})"

        def wiki(m: re.Match) -> str:
            bang, miolo = m.group(1), m.group(2)
            barra = "\\|" if "\\|" in miolo else "|"
            alvo_bruto, _, rotulo = miolo.replace("\\|", "|").partition("|")
            alvo, _, ancora = alvo_bruto.partition("#")
            chave, situacao = antigo.resolver(alvo)
            if not chave or situacao != "ok":
                return m.group(0)
            caminho = _normal(VAULT / (chave if "." in Path(chave).name and not chave.endswith(".md")
                                       and (VAULT / chave).exists() else chave + ".md"))
            depois = novo_de(caminho)
            if depois == caminho:
                return m.group(0)
            return bang + wikilink_para(depois, ("#" + ancora) if ancora else "", rotulo if _ else None, barra)

        texto = MDLINK.sub(md, texto)
        return WIKI_CRU.sub(wiki, texto)

    mapa_pastas = sorted(((_normal(VAULT / o), _normal(VAULT / d)) for o, d in mapa.items()
                          if (VAULT / o).is_dir()), key=lambda od: -len(str(od[0])))
    renomeadas = {o for o, d in arquivos.items() if o.suffix == ".md" and o.stem != d.stem}
    escritas: dict[Path, str] = {}
    importados = [o for o in arquivos if VAULT not in o.parents and o.suffix == ".md"]
    for p in _alvos_de_reescrita(filtros) + importados:
        texto = p.read_text(encoding="utf-8", errors="replace")
        q = novo_de(p)
        if p.suffix == ".md":
            novo = reescrever(texto, p, q)
            if titulo_do_arquivo and p in renomeadas:
                meta, inicio = parse_frontmatter(novo)
                corpo = novo[inicio:]
                corpo, n = re.subn(r"^# .+$", "# " + q.stem, corpo, count=1, flags=re.M)
                if not n:
                    corpo = f"# {q.stem}\n\n" + corpo
                novo = novo[:inicio] + corpo
        elif p.suffix == ".canvas":
            dados = json.loads(texto)
            for no in dados.get("nodes", []):
                if no.get("file"):
                    f = _normal(VAULT / no["file"])
                    no["file"] = novo_de(f).relative_to(VAULT).as_posix()
            novo = json.dumps(dados, ensure_ascii=False, indent="\t") + "\n" if json.loads(texto) != dados else texto
        else:
            novo = texto
            for o, d in mapa_pastas:
                if VAULT in o.parents and VAULT in d.parents:
                    novo = novo.replace(f'inFolder("{o.relative_to(VAULT).as_posix()}', f'inFolder("{d.relative_to(VAULT).as_posix()}')
        if novo != texto or q != p:
            escritas[p] = novo

    redirecionamentos = {}
    if REDIRECIONAMENTOS.exists():
        redirecionamentos = json.loads(REDIRECIONAMENTOS.read_text(encoding="utf-8"))
    for o, d in arquivos.items():
        redirecionamentos[o.relative_to(WORKSPACE).as_posix()] = d.relative_to(WORKSPACE).as_posix()
    for o, d in mapa_pastas:
        redirecionamentos[o.relative_to(WORKSPACE).as_posix() + "/"] = d.relative_to(WORKSPACE).as_posix() + "/"
    # uma cadeia A → B → C passa a apontar direto para C
    for k in list(redirecionamentos):
        v, vistos = redirecionamentos[k], {k}
        while v in redirecionamentos and v not in vistos:
            vistos.add(v)
            v = redirecionamentos[v]
        redirecionamentos[k] = v

    if not simular:
        for o, d in sorted(arquivos.items(), key=lambda od: str(od[0])):
            d.parent.mkdir(parents=True, exist_ok=True)
            if o in escritas:
                d.write_text(escritas.pop(o), encoding="utf-8")
                if d != o:
                    o.unlink()
            else:
                os.rename(o, d)
        for p, texto in escritas.items():
            p.write_text(texto, encoding="utf-8")
        def removivel(pasta: Path) -> bool:
            if pasta in (VAULT, WORKSPACE) or WORKSPACE not in pasta.parents:
                return False
            return VAULT in pasta.parents or len(pasta.relative_to(WORKSPACE).parts) > 2

        for o in sorted({o.parent for o in arquivos}, key=lambda p: -len(p.parts)):
            while removivel(o) and o.exists() and not [x for x in o.iterdir() if x.name != ".DS_Store"]:
                for x in o.iterdir():
                    x.unlink()
                o.rmdir()
                o = o.parent
        REDIRECIONAMENTOS.write_text(json.dumps(dict(sorted(redirecionamentos.items())), ensure_ascii=False,
                                                indent=1) + "\n", encoding="utf-8")
    return {"arquivos": len(arquivos), "reescritas": len(escritas) if simular else None, "mapa": arquivos}


def referencias_externas(velhos: list[str]) -> dict[str, list[str]]:
    """Arquivos fora de docs/ que ainda citam algum caminho antigo (`docs/...`)."""
    achados = subprocess.run(["grep", "-rIlF", "--exclude-dir=.git", "--exclude-dir=node_modules", "docs/",
                              str(WORKSPACE)], capture_output=True, text=True).stdout.splitlines()
    citantes: dict[str, list[str]] = defaultdict(list)
    alvos = sorted(set(velhos), key=len, reverse=True)
    for arq in achados:
        p = Path(arq)
        if VAULT in p.parents:
            continue
        try:
            texto = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for v in alvos:
            if v in texto:
                citantes[str(p.relative_to(WORKSPACE))].append(v)
    return citantes


def cmd_mover(args) -> int:
    origem = _normal(Path.cwd() / args.origem)
    destino = _normal(Path.cwd() / args.destino)
    for p in (origem, destino):
        if VAULT not in p.parents:
            print(f"{p} está fora do vault {VAULT}")
            return 1
    rel_o, rel_d = origem.relative_to(VAULT).as_posix(), destino.relative_to(VAULT).as_posix()
    r = aplicar_mapa({rel_o: rel_d}, simular=args.dry_run, titulo_do_arquivo=args.titulo)
    print(f"{'[simulação] ' if args.dry_run else ''}{rel_o} → {rel_d} ({r['arquivos']} arquivo(s))")
    externos = referencias_externas([rel_o, f"docs/{rel_o}"])
    if externos:
        print(f"\nfora do vault ainda citam `{rel_o}`. Recibos e manifestos históricos ficam como estão; "
              "atualize os documentos vivos. `cerebro.py onde` resolve o caminho antigo:")
        for arq in sorted(externos):
            print("  -", arq)
    return 0


def cmd_migrar(args) -> int:
    mapa = json.loads(Path(args.mapa).read_text(encoding="utf-8"))
    r = aplicar_mapa(mapa, simular=args.dry_run, titulo_do_arquivo=True)
    print(f"{'[simulação] ' if args.dry_run else ''}{r['arquivos']} arquivo(s) no mapa")
    if args.dry_run:
        print(f"{r['reescritas']} nota(s), canvas ou base teriam links reescritos")
    externos = referencias_externas(list(mapa) + [f"docs/{k}" for k in mapa])
    if externos:
        print(f"\n{len(externos)} arquivo(s) fora de docs/ citam caminhos antigos:")
        for arq, vs in sorted(externos.items()):
            print(f"  - {arq} ({len(vs)})")
    return 0


def cmd_onde(args) -> int:
    """Traduz um caminho antigo de docs/ para o atual."""
    if not REDIRECIONAMENTOS.exists():
        print("sem redirecionamentos registrados")
        return 1
    mapa = json.loads(REDIRECIONAMENTOS.read_text(encoding="utf-8"))
    q = unquote(args.caminho.strip()).lstrip("./")
    candidatos = [q, q.rstrip("/")]
    if q.startswith("docs/"):
        candidatos += [q[5:], q[5:].rstrip("/")]
    else:
        candidatos += ["docs/" + q, "docs/" + q.rstrip("/")]
    for cand in candidatos:
        if cand in mapa:
            print(mapa[cand])
            return 0
    for velho in sorted((k for k in mapa if k.endswith("/")), key=len, reverse=True):
        if q.startswith(velho):
            print(mapa[velho] + q[len(velho):])
            return 0
    parecidos = [k for k in mapa if Path(q).name.lower() in k.lower()]
    if parecidos:
        print("caminho exato não registrado; parecidos:")
        for k in parecidos[:10]:
            print(f"  {k} → {mapa[k]}")
        return 1
    print("não registrado; se existe hoje, está em", q)
    return 1


# ───────────────────────── referências fora do vault ─────────────────────────

HISTORICO = re.compile(r"(^|/)(evidence|validation|runs|results|outputs|dist|\.vercel|\.tmp|node_modules|\.git)(/|$)"
                       r"|CHANGELOG|changelog\.md$|SHA256SUMS|\.patch$|^prototypes/towerdefense/")
TOKEN_DOCS = re.compile(r"(?<![\w/.-])docs/[^\s)\]\"'`>|,;*]+")


def _traduzir(caminho: str, mapa: dict[str, str]) -> str | None:
    novo = _traduzir_bruto(caminho, mapa)
    if novo and not (WORKSPACE / novo.split("#", 1)[0]).exists():
        return None  # abreviação (docs/research/13) ou destino inexistente: não inventar caminho
    return novo


def _traduzir_bruto(caminho: str, mapa: dict[str, str]) -> str | None:
    c = unquote(caminho).split("#", 1)[0].rstrip(".:")
    if c.rstrip("/") in mapa:  # pasta citada inteira: a porta da nota (Estudo X), não os anexos
        return mapa[c.rstrip("/")]
    if c in mapa:
        return mapa[c]
    for velho in sorted((k for k in mapa if k.endswith("/")), key=len, reverse=True):
        if c.startswith(velho) and c != velho.rstrip("/"):
            return mapa[velho] + c[len(velho):]
    return None


def cmd_referencias(args) -> int:
    """Atualiza documentos vivos fora de docs/ que citam caminhos antigos do vault."""
    mapa = json.loads(REDIRECIONAMENTOS.read_text(encoding="utf-8")) if REDIRECIONAMENTOS.exists() else {}
    raizes = [WORKSPACE]
    nucleo = WORKSPACE / "framework" / "core"
    if nucleo.is_symlink() and nucleo.resolve().is_dir():
        raizes.append(nucleo.resolve())  # o framework central linka docs/ do laboratório
    candidatos = []
    for raiz_busca in raizes:
        saida = subprocess.run(["grep", "-rIl", "--exclude-dir=.git", "--exclude-dir=node_modules", "--exclude-dir=dist",
                                "--exclude-dir=outputs", "--exclude-dir=.tmp", "docs/", "."], cwd=raiz_busca,
                               capture_output=True, text=True).stdout.splitlines()
        candidatos += [(raiz_busca, x[2:] if x.startswith("./") else x) for x in saida]
    total = 0
    for raiz_busca, rel in sorted(candidatos):
        arq = raiz_busca / rel
        if VAULT in arq.parents or HISTORICO.search(rel) or arq.is_symlink():
            continue
        partes = rel.split("/")
        if raiz_busca == WORKSPACE and partes[0] in {"games", "demos", "prototypes", "apps", "swipe", "shared"} \
                and arq.suffix != ".md":
            continue  # nos projetos, só documentação; código e dados ficam como estão
        if raiz_busca != WORKSPACE:
            raiz = raiz_busca  # no framework, docs/ citado em texto é a pasta docs/ dele
        elif partes[0] in {"games", "demos", "prototypes", "apps", "swipe", "shared"}:
            raiz = WORKSPACE / "/".join(partes[:2])
        else:
            raiz = WORKSPACE
        texto = arq.read_text(encoding="utf-8", errors="replace")
        trocas: list[str] = []

        def link(m: re.Match) -> str:
            href = m.group(3)
            alvo = alvo_local(href)
            if not alvo:
                return m.group(0)
            absoluto = _normal(arq.parent / alvo)
            if WORKSPACE not in absoluto.parents or absoluto.exists():
                return m.group(0)
            novo = _traduzir(absoluto.relative_to(WORKSPACE).as_posix(), mapa)
            if not novo:
                return m.group(0)
            ancora = "#" + href.split("#", 1)[1] if "#" in href else ""
            r = os.path.relpath(WORKSPACE / novo, arq.parent).replace(os.sep, "/")
            trocas.append(f"{href} → {r}")
            return f"{m.group(1)}[{m.group(2)}]({quote(r, safe='/._-~()')}{ancora}{m.group(4) or ''})"

        def token(m: re.Match) -> str:
            t = m.group(0)
            limpo = unquote(t).split("#", 1)[0].rstrip(".:")
            if (raiz / limpo).exists():
                return t  # é a pasta docs/ do próprio projeto
            novo = _traduzir(t, mapa)
            if not novo and raiz not in (WORKSPACE, raiz_busca) or (not novo and raiz_busca == WORKSPACE and raiz != WORKSPACE):
                # caminho relativo ao projeto (docs/research/… dentro de games/<jogo>/) que foi importado
                traduzido = _traduzir(f"{raiz.relative_to(WORKSPACE).as_posix()}/{limpo}", mapa)
                if traduzido:
                    novo = os.path.relpath(WORKSPACE / traduzido, raiz).replace(os.sep, "/")
            if not novo:
                return t
            trocas.append(f"{t} → {novo}")
            return novo + t[len(limpo):] if t.startswith(limpo) else novo

        novo = MDLINK.sub(link, texto) if arq.suffix == ".md" else texto
        partes_texto = re.split(r"(\]\([^)]*\))", novo)  # não mexe dentro de (href) já tratados
        novo = "".join(p if p.startswith("](") else TOKEN_DOCS.sub(token, p) for p in partes_texto)
        if trocas:
            total += len(trocas)
            print(f"{rel if raiz_busca == WORKSPACE else raiz_busca.name + '/' + rel}: {len(trocas)}")
            for t in trocas[: args.limite]:
                print("   ", t)
            if args.aplicar:
                arq.write_text(novo, encoding="utf-8")
    print(f"\n{total} referência(s) {'atualizadas' if args.aplicar else 'a atualizar (use --aplicar)'}")
    return 0


# ───────────────────────── cores do grafo ─────────────────────────

# Uma cor por tipo de nó. A ordem importa: o Obsidian pinta com o primeiro grupo que casa.
# `cerebro.py cores` grava estes grupos em .obsidian/graph.json e gera a Legenda do grafo.
CORES = [
    # família, nome, cor, regra (tag | pasta | tipos), o que é
    ("Jogos", "Nossos jogos", "#FF3B30", {"tag": "nosso"}, "jogo do estúdio, com pasta em games/, demos/ ou apps/"),
    ("Jogos", "Jogos de referência", "#FF9500", {"pasta": "genealogia-jogos/nos/jogos"}, "jogo de outro estúdio que estudamos ou que influenciou"),
    ("Jogos", "Ludemas", "#FFD60A", {"pasta": "genealogia-jogos/nos/ludemas"}, "mecânica que viaja entre dois ou mais jogos"),
    ("Cultura e autoria", "Estúdios", "#A2845E", {"pasta": "genealogia-jogos/nos/estudios"}, "quem desenvolveu"),
    ("Cultura e autoria", "Pessoas", "#FF8FAB", {"pasta": "genealogia-jogos/nos/pessoas"}, "autor, diretor, compositor"),
    ("Cultura e autoria", "Mitos", "#BF5AF2", {"pasta": "genealogia-jogos/nos/mitos"}, "figura mítica entre o texto-fonte e o jogo"),
    ("Cultura e autoria", "Obras", "#D7B3FF", {"pasta": "genealogia-jogos/nos/obras"}, "livro, poema, filme que serviu de fonte"),
    ("Conhecimento", "Estudos", "#0A84FF", {"pasta": "estudos"}, "dossiê sobre referência externa"),
    ("Conhecimento", "Pesquisas", "#64D2FF", {"pasta": "pesquisas"}, "método, ferramenta ou tecnologia avaliada"),
    ("Conhecimento", "Aprendizados", "#30D158", {"pasta": "aprendizados"}, "lição de caso nosso, com prova"),
    ("Conhecimento", "Planos", "#B5E48C", {"pasta": "planos"}, "PRD, plano, desenho de jogo em estudo"),
    ("Conhecimento", "Visões do grafo", "#2EC4B6", {"pasta": "genealogia-jogos/visoes"}, "recorte curado do grafo"),
    ("Estúdio", "Identidade", "#E040FB", {"pasta": "identidade"}, "design system, bíblia e referências visuais"),
    ("Estúdio", "Aulas", "#FFB4A2", {"pasta": "aulas"}, "material de ensino"),
    ("Estúdio", "Operação", "#A3B18A", {"pasta": "operacao"}, "workspace, acervo, publicação, analytics"),
    ("Prova", "Registros", "#C7C7CC", {"pasta": "registros"}, "parecer, resultado, relato, story"),
    ("Prova", "Evidências", "#636366", {"pasta": "evidencias"}, "ficha, inventário, fonte organizada"),
    ("Padrões e portas", "Padrões", "#FFFFFF", {"pasta": "padroes"}, "o que se repete em duas ou mais fontes"),
    ("Padrões e portas", "Portas do cérebro", "#5E5CE6", {"tipos": ["hub", "processo"]}, "Comece Aqui, Padrões, Processo, Genealogia, Legenda"),
]
GRAPH = VAULT / ".obsidian" / "graph.json"
LEGENDA = VAULT / "Legenda do grafo.md"


def _consulta(regra: dict) -> str:
    if "tag" in regra:
        return f"tag:#{regra['tag']}"
    if "pasta" in regra:
        return f'path:"{regra["pasta"]}/"'
    return " OR ".join(f"[tipo:{t}]" for t in regra["tipos"])


def _casa(regra: dict, n: "Nota") -> bool:
    if "tag" in regra:
        return regra["tag"] in lista(n.meta.get("tags"))
    if "pasta" in regra:
        return n.rel.startswith(regra["pasta"] + "/")
    return n.tipo in regra["tipos"]


def grupos_de_cor() -> list[dict]:
    return [{"query": _consulta(regra), "color": {"a": 1, "rgb": int(cor[1:], 16)}}
            for _, _, cor, regra, _ in CORES]


def gerar_legenda(notas: list["Nota"]) -> str:
    contagem: Counter[str] = Counter()
    sem_cor = 0
    for n in notas:
        for _, nome, _, regra, _ in CORES:
            if _casa(regra, n):
                contagem[nome] += 1
                break
        else:
            sem_cor += 1
    out = [
        "---",
        "tipo: hub",
        'resumo: "Legenda de cores do Graph view: a cor de cada nó diz o que ele é. Gerada por cerebro.py cores."',
        "status: vigente",
        "---",
        "# Legenda do grafo",
        "",
        "> Gerada por `python3 _sistema/cerebro.py cores`, que também grava as cores no Graph.",
        "> Para mudar uma cor, edite `CORES` no `cerebro.py` e rode de novo. Contrato: [[Processo]].",
        "",
    ]
    familia_atual = None
    for familia, nome, cor, regra, desc in CORES:
        if familia != familia_atual:
            out += ["", f"## {familia}", "", "| | Nós | Quantos | O que é |", "|---|---|---|---|"]
            familia_atual = familia
        out.append(f'| <span style="color:{cor};font-size:1.6em">●</span> | **{nome}** | {contagem[nome]} | {desc} |')
    out += [
        "",
        "## Como ler",
        "",
        "- **Tamanho** do nó: quantas ligações ele tem. Hubs do grafo ficam grandes.",
        "- **Seta**: direção da ligação. Na genealogia, vai de quem influenciou para quem recebeu.",
        "- Nós em cinza sem cor de grupo: nota sem tipo reconhecido"
        + (f" (hoje: {sem_cor})." if sem_cor else " (hoje: nenhuma)."),
        "- O Graph esconde o [[Índice]], o `AGENTS` e a `_entrada/`, que linkam tudo e virariam um centro falso.",
        "",
        "## Filtros prontos",
        "",
        "Cole no campo de busca do Graph view:",
        "",
        "| Para ver | Filtro |",
        "|---|---|",
        "| só a genealogia (jogos, ludemas, cultura) | `path:\"genealogia-jogos/\"` |",
        "| só o conhecimento, sem as fichas de evidência | `-path:\"genealogia-jogos/\" -path:\"evidencias/\" -path:\"registros/\"` |",
        "| o que existe sobre um jogo nosso | abra o nó do jogo e use o *grafo local* (Ctrl/Cmd+P → Open local graph) |",
        "| sem mitos e obras | `-path:\"genealogia-jogos/nos/mitos/\" -path:\"genealogia-jogos/nos/obras/\"` |",
        "| só o que é nosso | `tag:#nosso OR path:\"planos/\" OR path:\"aprendizados/\" OR path:\"identidade/\"` |",
        "",
        "Depois de mudar as cores com o Obsidian aberto: Cmd/Ctrl+P → *Reload app without saving*. "
        "Sem isso, o Obsidian regrava o `graph.json` com o que tem na memória.",
    ]
    return "\n".join(out) + "\n"


def cmd_cores(args) -> int:
    notas, todos = carregar()
    dados = json.loads(GRAPH.read_text(encoding="utf-8")) if GRAPH.exists() else {}
    dados.update({
        "colorGroups": grupos_de_cor(),
        "collapse-color-groups": False,
        "search": '-file:"Índice" -file:"AGENTS" -path:"_entrada/"',
        "showArrow": True,
        "showTags": False,
        "showAttachments": False,
        "hideUnresolved": True,
        "showOrphans": True,
        "nodeSizeMultiplier": 1.3,
        "lineSizeMultiplier": 0.7,
        "linkDistance": 180,
        "repelStrength": 14,
        "centerStrength": 0.45,
    })
    GRAPH.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LEGENDA.write_text(gerar_legenda(notas), encoding="utf-8")
    print(f"{len(CORES)} grupos de cor em {GRAPH.relative_to(VAULT)}; legenda em {LEGENDA.name}.")
    print("Obsidian aberto: Cmd/Ctrl+P → Reload app without saving, senão ele regrava o graph.json.")
    return 0


# ───────────────────────── main ─────────────────────────

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="cerebro.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="valida metadados, links e o grafo")
    c.add_argument("--limite", type=int, default=40, help="máximo de avisos listados")
    c.add_argument("--sem-grafo", action="store_true", help="não rodar exportar_grafo.py --check")
    c.add_argument("--externos", action="store_true", help="lista cada link externo ausente")
    c.add_argument("--nivel", choices=("erro", "aviso", "info"), default="info",
                   help="mostra deste nível para cima (erro < aviso < info)")
    c.add_argument("--json", action="store_true", help="saída em JSON: resumo + itens com código, arquivo e linha")
    c.set_defaults(func=cmd_check)
    i = sub.add_parser("indice", help="regenera Índice.md")
    i.set_defaults(func=cmd_indice)
    b = sub.add_parser("buscar", help="lista notas por jogo, tema, tipo ou texto")
    b.add_argument("--jogo", help="nome do nó, pasta (games/rabisco-boom) ou slug (rabisco-boom)")
    b.add_argument("--tema", choices=sorted(TEMAS))
    b.add_argument("--tipo", choices=sorted(TIPOS))
    b.add_argument("--texto", help="procura no título e no resumo")
    b.add_argument("--corpo", action="store_true", help="com --texto, procura também no corpo")
    b.add_argument("--mencoes", action="store_true", help="com --jogo, inclui notas que só citam o jogo")
    b.add_argument("--grafo", action="store_true", help="inclui nós do grafo de genealogia")
    b.add_argument("--json", action="store_true")
    b.set_defaults(func=cmd_buscar)
    m = sub.add_parser("mover", help="move nota ou pasta e reescreve links no vault")
    m.add_argument("origem")
    m.add_argument("destino")
    m.add_argument("--dry-run", action="store_true")
    m.add_argument("--titulo", action="store_true", help="o # título da nota renomeada passa a ser o nome novo")
    m.set_defaults(func=cmd_mover)
    g = sub.add_parser("migrar", help="aplica um mapa JSON {antigo: novo} de uma vez (reorganização)")
    g.add_argument("mapa")
    g.add_argument("--dry-run", action="store_true")
    g.set_defaults(func=cmd_migrar)
    f = sub.add_parser("referencias", help="atualiza documentos vivos fora de docs/ que citam caminhos antigos")
    f.add_argument("--aplicar", action="store_true")
    f.add_argument("--limite", type=int, default=4)
    f.set_defaults(func=cmd_referencias)
    k = sub.add_parser("cores", help="grava as cores do Graph e gera a Legenda do grafo")
    k.set_defaults(func=cmd_cores)
    o = sub.add_parser("onde", help="traduz um caminho antigo de docs/ para o atual")
    o.add_argument("caminho")
    o.set_defaults(func=cmd_onde)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
