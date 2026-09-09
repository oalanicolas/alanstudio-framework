#!/usr/bin/env python3
"""Games harness: contexto sob demanda, contrato de reuso e execução com recibo."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timezone
from urllib.parse import unquote

FRAMEWORK = Path(__file__).resolve().parents[1]


def default_root():
    parent = FRAMEWORK.parent
    if FRAMEWORK.name == "framework" and (parent / "AGENTS.md").is_file():
        return parent
    return Path.cwd()


def default_studies_root(root=None):
    env = os.environ.get("GAMES_FRAMEWORKS_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    base = Path(root) if root is not None else default_root()
    for candidate in (base / "Games-Frameworks", base.parent / "Games-Frameworks"):
        if candidate.is_dir():
            return candidate
    return base.parent / "Games-Frameworks"


_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
import sfx_catalog

ROOT = default_root()
STUDIES_ROOT = default_studies_root(ROOT)
FOCI = (
    "create", "mechanics", "lifecycle", "content", "visual", "network", "architecture",
    "feel", "performance", "accessibility", "audio", "persistence", "release",
)
STAGES = (
    "brief", "mda", "gdd", "poc", "prd", "tdd", "vertical-slice", "mvp", "qa", "release",
    "art-bible", "devlog", "audit",
)
EVENTS = ("task", "direction-approved", "resume")
CONTINUITY_PATTERN = r"\b(continuidade|continuity|retomada|proxim[ao]s? (passos?|acoes|acao|tarefas?)|next steps?)\b"
CONTINUITY_FILES = {"production plan", "plano de producao", "roadmap", "backlog", "state", "decisions", "devlog"}
FOUNDATION_AREAS = (
    ("vision", "Visão e escopo / Brief ou PRD", r"\b(brief|prd|visao|vision|escopo|scope|publico|target audience)\b"),
    ("gdd", "Design do jogo / GDD", r"\b(gdd|game design|gameplay|mecanicas|regras|como jogar|core loop)\b"),
    ("mda", "Hipóteses de experiência / MDA", r"\b(mda|hipoteses de experiencia|experiencia pretendida|experiencia desejada|experience goals|emotional goals)\b"),
    ("architecture", "Arquitetura atual / TDD", r"\b(tdd|arquitetura|architecture|technical design|contratos tecnicos)\b"),
    ("art_direction", "Design system do jogo / Art Bible", r"^design$|\b(art bible|art-bible|art direction|design system|design-system|game design system|direcao de arte|direcao visual|direcao audiovisual|style guide|visual style|feel bible)\b"),
    ("decisions", "Decisões e histórico / Devlog", r"\b(devlog|decision log|decisions|decisoes|changelog|aprendizados|historico de decisoes|adr)\b"),
    ("qa", "QA e playtest", r"\b(qa|playtest|test plan|verification|verificacao|validacao|plano de testes)\b"),
    ("runbook", "Como executar e verificar", r"\b(runbook|getting started|setup|instalacao|executar|rodar|desenvolvimento|development|jogar|build|package)\b"),
    ("provenance", "Origem de código e assets", r"\b(licenses?|licences?|licencas?|copying|authors|sources|proveniencia|provenance|creditos|credits|asset sources)\b"),
)
CAPABILITIES = ("pause", "reset", "seed", "observe", "act", "advance", "capture", "dispose")
SKIP = {"node_modules", "dist", "build", "docs", "framework", "squads", "public", "assets", "Assets", "Library", "Temp", "outputs", "shared"}
FOCUS_STUDIES = {
    "create": (
        "outputs/decoded/games-bmad-game-dev-studio/study-2486f5f5f3b8/validate/rule-catalog.md",
    ),
    "lifecycle": (
        "outputs/decoded/games-phaser/study-02d8931b626d/validate/rule-catalog.md",
        "outputs/decoded/games-excalibur/study-4a23dd1674b1/validate/rule-catalog.md",
        "outputs/decoded/games-godot-demo-projects/study-0db80ca5fd22/validate/rule-catalog.md",
        "outputs/decoded/games-pettingzoo/study-a865c24671b2/validate/rule-catalog.md",
    ),
    "mechanics": (
        "outputs/decoded/games-boardgame-io/study-5e9a2c94bde8/validate/rule-catalog.md",
    ),
    "content": (
        "outputs/decoded/games-ink/study-35c63e52f1d3/validate/rule-catalog.md",
        "outputs/decoded/games-ldtk/study-6d69bd1d6be9/validate/rule-catalog.md",
    ),
    "visual": (
        "outputs/decoded/games-excalibur/study-4a23dd1674b1/validate/rule-catalog.md",
    ),
    "network": (
        "outputs/decoded/games-boardgame-io/study-5e9a2c94bde8/validate/rule-catalog.md",
        "outputs/decoded/games-pettingzoo/study-a865c24671b2/validate/rule-catalog.md",
    ),
}
HINT_FILES = (
    "game.mjs", "game.js", "game.test.mjs", "game.test.js",
    "src/main.js", "src/engine/core/loop.js", "src/core/loop.js", "src/game/rules.js",
    "tests/lifecycle.test.mjs", "tools/verify.py", "tools/verify.mjs", "headless/env_server.ts",
)
BAR_TIERS = ("prototype", "playable", "slice", "shippable", "flagship")
BAR_DIMENSIONS = {
    "feel": "Resposta da ação central",
    "legibility": "Legibilidade do estado",
    "art_direction": "Coerência audiovisual",
    "audio_mix": "Mixagem, não pasta de arquivos",
    "pacing": "Ritmo e aprendizado",
    "state_trust": "Confiança no estado",
    "performance": "Estabilidade sob orçamento",
    "accessibility": "Alcance",
    "content_scale": "Capacidade de produzir mais",
    "release": "Confiança operacional",
}
FOCUS_DIMENSIONS = {
    "create": ("feel", "legibility", "pacing", "state_trust"),
    "mechanics": ("feel", "legibility", "pacing"),
    "lifecycle": ("state_trust", "performance"),
    "content": ("content_scale", "art_direction", "legibility"),
    "visual": ("art_direction", "legibility", "performance"),
    "network": ("state_trust", "performance"),
    "architecture": ("state_trust", "performance", "content_scale"),
    "feel": ("feel", "legibility", "audio_mix"),
    "performance": ("performance", "art_direction"),
    "accessibility": ("accessibility", "legibility", "audio_mix"),
    "audio": ("audio_mix", "feel", "accessibility"),
    "persistence": ("state_trust", "content_scale"),
    "release": ("release", "performance", "accessibility", "state_trust"),
}
STAGE_TIERS = {
    "brief": "prototype", "mda": "prototype", "poc": "prototype",
    "gdd": "playable", "prd": "playable", "tdd": "playable",
    "vertical-slice": "slice", "art-bible": "slice",
    "mvp": "shippable", "qa": "shippable", "release": "shippable",
}
STARTERS_ROOT = FRAMEWORK / "assets/starters"
STARTER_MANIFEST = "starter.json"
STARTER_FIELDS = ("project", "project_slug", "project_title", "project_path", "framework_path")
INIT_DOCUMENTS = ("brief", "gdd", "mda", "tdd", "art-bible", "devlog", "qa")
INIT_TEXT_SUFFIXES = {".md", ".txt", ".html", ".css", ".js", ".mjs", ".json", ".svg"}
CAPABILITY_TOKENS = {
    "pause": ("pause", "paused"),
    "reset": ("reset", "restart"),
    "seed": ("seed",),
    "observe": ("observe", "observation"),
    "act": ("act",),
    "advance": ("advance", "tick"),
    "capture": ("capture",),
    "dispose": ("dispose", "teardown"),
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def resolve(value, root=ROOT):
    return (root / value).resolve()


def identify(project):
    if (project / "package.json").is_file():
        return "package.json"
    if (project / "ProjectSettings/ProjectVersion.txt").is_file():
        return "unity"
    if (project / "project.godot").is_file():
        return "godot"
    if (project / "index.html").is_file():
        return "static-web"
    return None


def discover(root, depth=3):
    projects = []
    for path in sorted(root.iterdir()):
        if not path.is_dir() or path.is_symlink() or path.name.startswith(".") or path.name in SKIP:
            continue
        kind = identify(path)
        if kind:
            projects.append({"project": str(path), "kind": kind})
        elif depth > 1:
            projects.extend(discover(path, depth - 1))
    return projects


def package_commands(project):
    path = project / "package.json"
    if not path.is_file():
        return {}, None
    data = read_json(path)
    if not isinstance(data, dict) or not isinstance(data.get("packageManager", ""), str):
        raise ValueError("package.json precisa ser objeto com packageManager textual, quando declarado")
    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict) or not all(isinstance(value, str) for value in scripts.values()):
        raise ValueError("scripts de package.json precisam ser um objeto de comandos textuais")
    declared = data.get("packageManager", "").split("@")[0]
    locks = {manager for file, manager in (("package-lock.json", "npm"), ("npm-shrinkwrap.json", "npm"), ("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lock", "bun"), ("bun.lockb", "bun")) if (project / file).exists()}
    manager = declared or (next(iter(locks)) if len(locks) == 1 else "npm" if not locks else None)
    if manager not in (None, "npm", "pnpm", "yarn", "bun"):
        manager = None
    return scripts, manager


def studies_for(focus, studies_root):
    if focus not in FOCUS_STUDIES:
        return []
    found = []
    for relative in FOCUS_STUDIES[focus]:
        path = studies_root / relative
        if path.is_file():
            found.append(str(path))
    return found


# A barra só fecha o ciclo se o projeto puder dizer onde está. Sem isso o
# harness nomeia dez dimensões e nunca sabe qual delas é a mais baixa — que é
# justamente a única informação capaz de virar a próxima tarefa.
#
# A tabela é a mesma do README do starter, em Markdown, porque documento é o
# formato canônico deste framework e a tabela já existia lá escrita à mão.
BAR_ROW = re.compile(r"^\|\s*`(\w+)`\s*\|\s*`(\w+)`\s*\|\s*(?:`(\w+)`\s*:)?\s*(.*?)\s*\|\s*$")
BAR_SOURCES = ("README.md", "docs/qa.md", "docs/devlog.md", "docs/gdd.md", "docs/art-bible.md")


def bar_declaration(project):
    declared = {}
    conflicts = []
    problems = []
    for relative in BAR_SOURCES:
        path = project / relative
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 400_000:
                continue
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            match = BAR_ROW.match(line)
            if not match:
                continue
            dimension, tier, target, gap = match.groups()
            source = f"{relative}:{number}"
            known_dimension = dimension in BAR_DIMENSIONS
            known_tier = tier in BAR_TIERS
            # Uma linha só é candidata a declaração se pelo menos uma das duas
            # células for reconhecível. Sem esse filtro, qualquer tabela de duas
            # colunas em crase entraria no relatório como problema da barra.
            if not known_dimension and not known_tier:
                continue
            if not known_dimension:
                problems.append({"source": source, "reason": "unknown_dimension", "found": dimension})
                continue
            if not known_tier:
                problems.append({"source": source, "reason": "unknown_tier", "dimension": dimension, "found": tier})
                continue
            # O degrau declarado é utilizável mesmo com o alvo errado, então o
            # problema é relatado sem descartar a linha. Descartar em silêncio era
            # o defeito: quem declarava `feel` recebia a instrução de declarar
            # `feel`, e a promessa de conferência não se cumpria em lugar nenhum.
            expected = BAR_TIERS[BAR_TIERS.index(tier) + 1] if tier != BAR_TIERS[-1] else None
            if target is not None and target != expected:
                problems.append({
                    "source": source, "reason": "target_not_next", "dimension": dimension,
                    "found": target, "expected": expected,
                })
            elif target is None and expected is not None:
                problems.append({
                    "source": source, "reason": "missing_target", "dimension": dimension,
                    "found": None, "expected": expected,
                })
            entry = {
                "tier": tier,
                "next_tier": target,
                "gap": gap or None,
                "source": source,
            }
            previous = declared.get(dimension)
            if previous is None:
                declared[dimension] = entry
            elif previous["tier"] != tier:
                # Duas declarações discordantes não se resolvem por precedência:
                # a mais baixa vale, e o conflito fica visível para ser resolvido.
                conflicts.append({"dimension": dimension, "sources": [previous["source"], entry["source"]]})
                if BAR_TIERS.index(tier) < BAR_TIERS.index(previous["tier"]):
                    declared[dimension] = entry
    undeclared = [key for key in BAR_DIMENSIONS if key not in declared]
    floor = min((item["tier"] for item in declared.values()), key=BAR_TIERS.index) if declared else None
    at_floor = [key for key, item in declared.items() if item["tier"] == floor]
    return {
        "declared": declared,
        "undeclared": undeclared,
        "conflicts": conflicts,
        "problems": problems,
        "floor": floor,
        "at_floor": at_floor,
        # Dimensão não declarada não é dimensão alta: enquanto faltar uma, o
        # mínimo entre as dez é desconhecido, e o degrau percebido não sai.
        "perceived_tier": None if undeclared or not declared else floor,
        "sources": list(BAR_SOURCES),
    }


def bar_reading(project):
    declaration = bar_declaration(project)
    declared = declaration["declared"]
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "tiers": list(BAR_TIERS),
        "dimensions": [
            {
                "key": key,
                "label": BAR_DIMENSIONS[key],
                **(declared.get(key) or {"tier": None, "next_tier": None, "gap": None, "source": None}),
            }
            for key in BAR_DIMENSIONS
        ],
        "floor": declaration["floor"],
        "at_floor": declaration["at_floor"],
        "undeclared": declaration["undeclared"],
        "conflicts": declaration["conflicts"],
        "problems": declaration["problems"],
        "perceived_tier": declaration["perceived_tier"],
        "rule": "O degrau percebido de um jogo é o mínimo entre suas dimensões, não a média.",
        "guide": str(FRAMEWORK / "references/production-bar.md"),
        "sources": declaration["sources"],
        "assessed": False,
        "scope": (
            "Lê a declaração do próprio projeto e confere só a forma dela, relatando em `problems`: dimensão "
            "fora das dez, degrau fora dos cinco e alvo que não é o degrau imediatamente seguinte. Não observa "
            "o jogo, não mede nada e não corrige a declaração — uma tabela bem formada e otimista sai daqui "
            "intacta, porque o degrau é afirmação de quem escreveu. `perceived_tier` só aparece quando as dez "
            "dimensões têm linha, porque dimensão não declarada não é dimensão alta."
        ),
    }


def production_bar(focus, stage=None, project=None):
    dimensions = FOCUS_DIMENSIONS.get(focus, ())
    declaration = bar_declaration(project) if project is not None else None
    return {
        "tiers": list(BAR_TIERS),
        "tier_target": STAGE_TIERS.get(stage),
        "dimensions": [
            {
                "key": key,
                "label": BAR_DIMENSIONS[key],
                "declared": (declaration["declared"].get(key) if declaration else None),
            }
            for key in dimensions
        ],
        "rule": "O degrau percebido de um jogo é o mínimo entre suas dimensões, não a média.",
        "guide": str(FRAMEWORK / "references/production-bar.md"),
        "declaration": declaration,
        "observed": None,
        "assessed": False,
        "scope": (
            "Seleção das dimensões pertinentes ao foco e à etapa, mais o degrau que o próprio projeto declara "
            "nos documentos listados em `declaration.sources`. O harness lê a declaração e confere só a forma "
            "dela: não atribui degrau, não mede acabamento e não aprova entrega. Declarar um degrau exige "
            "observação com condição, evidência e autor — a tabela é a afirmação, não a prova."
        ),
    }


def mention_capabilities(project):
    found = {name: {"status": "unknown"} for name in CAPABILITIES}
    if not project.is_dir():
        return found
    for relative in HINT_FILES:
        path = project / relative
        if not path.is_file():
            continue
        try:
            if path.stat().st_size > 400_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for name, tokens in CAPABILITY_TOKENS.items():
            if found[name]["status"] == "mentioned":
                continue
            if any(re.search(r"(?i)\b" + re.escape(token) + r"\b", text) for token in tokens):
                found[name] = {
                    "status": "mentioned",
                    "path": relative,
                    "scope": "Menção em arquivo local de inspeção; não executado, não comprovado.",
                }
    return found


def scan(project, max_entries=2000, max_documents=64, max_bytes=64000):
    project = Path(project).resolve()
    if project.exists() and not project.is_dir():
        raise ValueError("projeto precisa ser um diretório")
    areas = {key: {"label": label, "status": "not_located", "candidates": []} for key, label, _ in FOUNDATION_AREAS}
    issues, inspected, entries_seen = [], 0, 0
    pending = [(project, 0)] if project.is_dir() else []
    doc_roots = {"docs", "production", "design", "art", "audio", "documentation"}
    excluded_dirs = {"node_modules", "dist", "build", "evidence", "outputs", "archive", "archives", "templates", "validation", "baseline", "captures", "previews", "models", "textures", "fonts", "videos"}
    json_docs = {"brief.json", "state.json", "decisions.json", "sources.json", "licenses.json", "package.json"}
    text_docs = {"license", "licence", "copying", "credits", "authors"}
    indexes, documents, links, statuses = [], {}, {}, {}
    deferred, non_current, continuity_sources = [], [], []
    link_count, max_links, links_limited = 0, 128, False
    inline_link = re.compile(r'(?<!!)\[[^\]\n]+\]\((?:<([^>\n]+)>|([^\s)]+))(?:\s+"[^"]*")?\)')
    navigation = re.compile(r"^\s*(?:(?:[-*]|\d+[.)])\s+)?\[[^\]]+\](?:\(|\[)")

    def normalized(text):
        return "".join(c for c in unicodedata.normalize("NFKD", text.casefold()) if not unicodedata.combining(c)).replace("-", " ").replace("_", " ")

    def status_hint(text):
        text = normalized(text)
        if re.search(r"\b(documento historico|historical document|nao vigente|superseded|duplicata historica|variante historica|status[^\n]{0,20}(historico|archived|deprecated))\b", text):
            return "historical"
        if re.search(r"\b(material de referencia|reference material|status[^\n]{0,20}(referencia|reference))\b", text):
            return "reference"
        if re.search(r"\{\{|\[preencher|status[^\n]{0,30}(rascunho|draft)", text):
            return "draft"
        return "candidate"

    def document_priority(relative):
        path = Path(relative)
        if path.stem.casefold() in {"readme", "index"}:
            rank = 0
        elif relative in links and any(item["status"] == "candidate" for item in links[relative]):
            rank = 1
        elif normalized(path.stem) in CONTINUITY_FILES:
            rank = 2
        elif any(re.search(pattern, normalized(path.stem)) for _, _, pattern in FOUNDATION_AREAS) or path.stem.casefold() in {"plan", "assets", "production-plan", "state"}:
            rank = 3
        else:
            rank = 4
        return rank, len(path.parts), relative.casefold(), relative

    while pending:
        directory, depth = pending.pop(0)
        try:
            entries = sorted(directory.iterdir(), key=lambda path: document_priority(path.relative_to(project).as_posix()))
        except OSError:
            issues.append({"path": str(directory.relative_to(project)), "reason": "unreadable_directory"})
            continue
        for path in entries:
            if entries_seen >= max_entries:
                issues.append({"reason": "scan_limit", "limit": "entries"})
                pending.clear()
                break
            entries_seen += 1
            if path.name.startswith(".") or path.name.casefold().startswith(("secret", "credential")):
                continue
            if path.is_symlink():
                if path.name.casefold() in doc_roots | text_docs | json_docs or path.suffix.casefold() in {".md", ".txt", ".rst"}:
                    issues.append({"path": str(path.relative_to(project)), "reason": "symlink_not_followed"})
                continue
            if path.is_dir():
                if (depth == 0 and path.name.casefold() not in doc_roots) or path.name.casefold() in excluded_dirs:
                    continue
                if depth >= 4:
                    issues.append({"path": str(path.relative_to(project)), "reason": "depth_limit"})
                else:
                    pending.append((path, depth + 1))
                continue
            if path.suffix.casefold() not in {".md", ".txt", ".rst"} and path.name.casefold() not in json_docs | text_docs:
                continue
            if path.is_file():
                documents[path.relative_to(project).as_posix()] = path

    unread = set(documents)
    while unread and inspected < max_documents:
        relative = min(unread, key=document_priority)
        unread.remove(relative)
        path = documents[relative]
        inspected += 1
        try:
            with path.open("rb") as source:
                raw = source.read(max_bytes + 1)
            if len(raw) > max_bytes:
                issues.append({"path": relative, "reason": "document_size_limit"})
                continue
            text = raw.decode("utf-8")
        except (OSError, UnicodeError):
            issues.append({"path": relative, "reason": "unreadable_document"})
            continue
        lines = text.splitlines()
        status = status_hint("\n".join(line for line in lines[:12] if not navigation.match(line)))
        if status == "candidate" and re.search(r"\{\{|\[preencher|status[^\n]{0,30}(rascunho|draft)", normalized(text)):
            status = "draft"
        statuses[relative] = status
        if path.stem.casefold() in {"readme", "index"} and status == "candidate":
            indexes.append(relative)
            for number, line in enumerate(lines, 1):
                for match in inline_link.finditer(line):
                    if link_count >= max_links:
                        links_limited = True
                        break
                    link_count += 1
                    target = unquote((match.group(1) or match.group(2)).split("#", 1)[0].split("?", 1)[0])
                    if not target or re.match(r"^[a-zA-Z][\w+.-]*:", target) or target.startswith("/"):
                        continue
                    target = os.path.normpath(str(path.parent.relative_to(project) / target))
                    parts = Path(target).parts
                    if any(p.startswith(".") or p.casefold().startswith(("secret", "credential")) for p in parts):
                        continue
                    if any(p.casefold() in excluded_dirs for p in parts[:-1]) or (len(parts) > 1 and parts[0].casefold() not in doc_roots):
                        continue
                    if Path(target).suffix.casefold() not in {".md", ".txt", ".rst"} and Path(target).name.casefold() not in json_docs | text_docs:
                        continue
                    if target not in documents:
                        issues.append({"path": relative, "line": number, "target": target, "reason": "index_target_not_located"})
                        continue
                    label = match.group(0).split("](", 1)[0][1:]
                    links.setdefault(target, []).append({"path": relative, "line": number, "label": normalized(label), "status": status_hint(line)})

        body = [(number, line) for number, line in enumerate(lines, 1) if line.strip() and not line.lstrip().startswith("#") and not navigation.match(line)]
        if not body:
            continue
        if path.suffix.casefold() == ".json":
            try:
                values = [json.loads(text)]
            except (ValueError, RecursionError):
                issues.append({"path": relative, "reason": "invalid_json"})
                continue
            has_text = False
            while values:
                value = values.pop()
                if isinstance(value, dict):
                    values.extend(value.values())
                elif isinstance(value, list):
                    values.extend(value)
                elif isinstance(value, str) and value.strip():
                    has_text = True
            if not has_text:
                continue
        labels = [(1, normalized(path.stem), "filename")]
        for number, line in enumerate(lines, 1):
            if inline_link.search(line) or navigation.match(line):
                continue
            heading = re.match(r"^\s{0,3}#{1,6}\s+(.+)", line)
            field = re.match(r"^\s*(?:[-*]\s+)?([^:]{3,80}):", line)
            if heading:
                end = next((n for n in range(number + 1, len(lines) + 1) if re.match(r"^\s{0,3}#{1,6}\s+", lines[n - 1])), len(lines) + 1)
                if any(number < n < end for n, _ in body):
                    labels.append((number, normalized(heading.group(1)), "heading"))
            elif field:
                labels.append((number, normalized(field.group(1)), "field"))
        for key, _, pattern in FOUNDATION_AREAS:
            hits = [(number, basis) for number, label, basis in labels if re.search(pattern, label)]
            if hits:
                areas[key]["candidates"].append({"path": relative, "line": hits[0][0], "status": status, "basis": hits[0][1]})
        continuation = [(number, basis) for number, label, basis in labels if basis != "filename" and re.search(CONTINUITY_PATTERN, label)]
        if continuation or normalized(path.stem) in CONTINUITY_FILES:
            number, basis = continuation[0] if continuation else (1, "filename")
            continuity_sources.append({"path": relative, "line": number, "status": status, "basis": basis})

    if unread:
        deferred = sorted(unread, key=document_priority)
        issues.append({"reason": "scan_limit", "limit": "documents"})
    if links_limited:
        issues.append({"reason": "index_link_limit"})

    for relative, status in statuses.items():
        refs = links.get(relative, [])
        if status == "candidate" and refs and all(item["status"] != "candidate" for item in refs):
            statuses[relative] = refs[0]["status"]
        if statuses[relative] in {"historical", "reference"}:
            non_current.append({"path": relative, "status": statuses[relative]})

    for key, _, pattern in FOUNDATION_AREAS:
        area = areas[key]
        for item in area["candidates"]:
            item["status"] = statuses[item["path"]]
            refs = links.get(item["path"], [])
            item["via"] = [{"path": ref["path"], "line": ref["line"]} for ref in refs[:3]]
        area["candidates"].sort(key=lambda item: (
            {"candidate": 0, "draft": 1, "historical": 2, "reference": 3}[item["status"]],
            not any(re.search(pattern, ref["label"]) for ref in links.get(item["path"], [])),
            not bool(item["via"]), item["basis"] != "filename", document_priority(item["path"]),
        ))
        states = {item["status"] for item in area["candidates"]}
        area["status"] = next((result for state, result in (("candidate", "candidate_found"), ("draft", "draft_only"), ("historical", "historical_only"), ("reference", "reference_only")) if state in states), "not_located")
        area["candidate_count"] = len(area["candidates"])
        del area["candidates"][3:]
    continuity_sources = [dict(item, status=statuses[item["path"]]) for item in continuity_sources if statuses[item["path"]] in {"candidate", "draft"}]
    continuity_sources.sort(key=lambda item: (
        item["status"] == "draft",
        normalized(Path(item["path"]).stem) not in CONTINUITY_FILES - {"decisions", "devlog"},
        item["basis"] == "filename", document_priority(item["path"]),
    ))
    continuity_source_count = len(continuity_sources)
    continuity_sources = continuity_sources[:5]
    read_first = list(dict.fromkeys([
        *indexes,
        *(item["path"] for item in continuity_sources),
        *(item["path"] for area in areas.values() for item in area["candidates"] if item["status"] in {"candidate", "draft"}),
        *(relative for relative in links if statuses.get(relative) in {"candidate", "draft"}),
        *(relative for relative in statuses if relative.casefold() == "production/state.json"),
    ]))
    gaps = [key for key, area in areas.items() if area["status"] != "candidate_found"]
    needs_documentation = bool(gaps or issues)
    notice = None
    if needs_documentation:
        missing = "; ".join(areas[key]["label"] for key in gaps)
        findings = f"Não localizei documentação confirmável para: {missing}." if gaps else "A checagem documental teve cobertura incompleta."
        if gaps and issues:
            findings += " A cobertura da checagem também foi limitada."
        work = "Vou levantar o código e os registros e organizar a documentação mínima" if project.is_dir() else "Vou documentar a base disponível e a proposta, distinguindo o que ainda não foi implementado"
        notice = f"{project.name}: {findings} {work}, preservando os documentos canônicos e registrando as lacunas."
    return {
        "schema_version": 3, "project": str(project), "exists": project.is_dir(),
        "minimum_status": "needs_review" if needs_documentation else "candidates_found",
        "areas": areas, "gaps": gaps, "read_first": read_first,
        "continuity_sources": continuity_sources, "continuity_source_count": continuity_source_count,
        "coverage": {
            "documents_inspected": inspected, "documents_located": len(documents), "entries_seen": entries_seen,
            "documents_deferred": deferred[:20], "documents_deferred_count": len(deferred),
            "non_current_documents": non_current[:20], "non_current_document_count": len(non_current),
            "issues": issues[:20], "issue_count": len(issues), "issues_truncated": len(issues) > 20,
            "excluded_directory_names": sorted(excluded_dirs),
            "limits": {"entries": max_entries, "documents": max_documents, "bytes_per_document": max_bytes, "depth": 4, "index_links": max_links, "candidates_per_area": 3, "continuity_sources": 5},
        },
        "next_action": "notify_and_document" if needs_documentation else "continue_requested_task",
        "audit": {
            "policy": "notify_and_proceed", "executed": False,
            "required": needs_documentation,
            "notice": notice,
            "reason": "Direção do usuário: avisar e iniciar o levantamento/documentação automaticamente; respeitar restrição explícita na conversa atual.",
            "guide": str(FRAMEWORK / "references/project-audit.md"),
        },
        "scope": "Localização lexical limitada, priorizada por índices e nomes; links de navegação não são conteúdo. Marcadores de histórico/referência/rascunho são indícios, não certificação de atualidade. Não rastreia comportamento, executa código, escreve arquivos ou comprova suficiência e qualidade. Ausência significa não localizado neste recorte.",
    }


def context(project, focus, stage=None, studies_root=None, event="task"):
    if stage is not None and stage not in STAGES:
        raise ValueError("etapa desconhecida")
    if event not in EVENTS:
        raise ValueError("evento desconhecido")
    if project.exists() and not project.is_dir():
        raise ValueError("projeto precisa ser um diretório")
    metadata_issues = []
    try:
        scripts, manager = package_commands(project)
    except (OSError, ValueError, RecursionError) as error:
        scripts, manager = {}, None
        metadata_issues.append({"path": "package.json", "reason": str(error)})
    instructions = [str(parent / "AGENTS.md") for parent in reversed((project, *project.parents)) if (parent / "AGENTS.md").is_file()]
    foundation = scan(project)
    records = [str(project / relative) for relative in foundation["read_first"]]
    document_minimum = foundation["audit"]["required"] or event == "direction-approved" or stage == "audit"
    references = [
        FRAMEWORK / "references/process.md",
        FRAMEWORK / "references/quality.md",
        FRAMEWORK / "references/production-bar.md",
        FRAMEWORK / f"recipes/{focus}.md",
    ]
    if stage == "tdd" and focus != "architecture":
        references.append(FRAMEWORK / "recipes/architecture.md")
    if stage or focus == "create":
        references.append(FRAMEWORK / "references/preproduction.md")
    if focus in ("create", "visual") or stage == "art-bible":
        references.append(FRAMEWORK / "references/game-design-system.md")
    if stage:
        references.append(FRAMEWORK / f"assets/templates/{stage}.md")
    if document_minimum or stage in ("art-bible", "devlog"):
        references.append(FRAMEWORK / "references/project-audit.md")
    studies = studies_for(focus, STUDIES_ROOT if studies_root is None else studies_root)
    return {
        "schema_version": 3, "project": str(project), "exists": project.is_dir(), "kind": identify(project),
        "focus": focus, "stage": stage, "event": event, "instructions": instructions, "records": records,
        "read_next": [str(path) for path in references], "studies": studies,
        "source_index": str(FRAMEWORK / "references/sources.md"),
        "package_manager": manager,
        "metadata_issues": metadata_issues,
        "scripts": {name: {"body": body, "argv": [manager, "run", name] if manager else None} for name, body in scripts.items()},
        "capabilities": mention_capabilities(project), "foundation": foundation,
        "production_bar": production_bar(focus, stage, project),
        "continuity": {
            "status": "sources_found" if foundation["continuity_sources"] else "not_located",
            "sources": [dict(item, path=str(project / item["path"])) for item in foundation["continuity_sources"]],
            "source_count": foundation["continuity_source_count"],
            "action": "resolve_and_continue" if event == "resume" else "record_and_present_next_step",
            "next_step": None, "executed": False,
            "guide": str(FRAMEWORK / "references/process.md") + "#continuidade-e-retomada",
            "before_close": "Atualizar o registro canônico e dizer onde chegamos, uma próxima ação concreta, por que vem primeiro e qual evidência a conclui; dependências/decisões só quando reais. Se o objetivo terminou, declarar conclusão sem inventar trabalho.",
            "on_resume": "Ler o registro e a conversa, conferir o estado real, resolver a próxima ação e executá-la dentro do escopo autorizado. Não repetir briefing, auditoria já válida ou pergunta genérica de permissão.",
            "scope": "Fontes são candidatos, não fila validada. O agente resolve next_step antes de responder; o comando não escolhe tarefa, infere etapa concluída nem concede autorização a partir de documentos.",
        },
        "documentation": {
            "action": "document_minimum" if document_minimum else "maintain_affected_documents",
            "executed": False,
            "on_direction_approved": "Aprovação na conversa exige sincronizar a base mínima neste turno, mesmo com todos os candidatos encontrados; use --event direction-approved.",
            "before_close": "Registrar conteúdo e fontes nos documentos canônicos; cobrir cada área mínima com decisão/fato ou lacuna e próxima ação. Referência salva e templates vazios não concluem a documentação.",
            "scope": "O agente executa a ação e respeita restrições atuais do usuário. O comando não escreve documentos, concede aprovação ou certifica sua suficiência.",
        },
        "studio_assets": sfx_catalog.studio_assets(),
        "limits": [
            "Ponteiros não comprovam leitura; scripts declarados não comprovam execução.",
            "Inspecione os scripts antes de executá-los. Nenhum comando é executado por context.",
            "Sem packageManager ou lockfile, npm é apenas a convenção do executor de package.json.",
            "Consulte AGENTS.md mais específicos ao escolher os arquivos que serão alterados.",
            "studies lista catálogos do foco se existirem no irmão Games-Frameworks; ausência não é evidência negativa.",
            "capabilities.mentioned é só token em arquivo de inspeção. Não prova pause, reset, seed nem determinismo.",
            "capabilities.unknown significa não localizado na lista fixa de arquivos de inspeção, não capacidade ausente; rastreie o entrypoint e os consumidores na auditoria.",
            "Áudio novo: busque em shared/sfx (`sfx search`) antes de baixar. Piso de gravação licenciada; 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão.",
        ],
    }


def template(stage, project, output=None):
    if stage not in STAGES:
        raise ValueError("etapa desconhecida")
    text = (FRAMEWORK / f"assets/templates/{stage}.md").read_text(encoding="utf-8")
    text = text.replace("{{PROJECT}}", project.name).replace("{{PROJECT_PATH}}", str(project))
    if output is not None:
        if output.exists() or output.is_symlink():
            raise ValueError("documento existente; adapte a fonte canônica sem sobrescrever")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as document:
            document.write(text)
    return text


# Todo comando que o harness sugere existe para ser copiado e colado. Caminho de
# projeto com espaço é comum — "Farol do Sul" é um nome de jogo, não um caso de
# borda — e sem citação o shell o parte em dois argumentos. Construir tudo por
# aqui é o que impede a próxima sugestão de nascer quebrada: `shlex.quote` só
# acrescenta aspas quando são necessárias, então flags e literais passam intactos.
def harness_command(*parts):
    script = shlex.quote(str(FRAMEWORK / "scripts/game.py"))
    return " ".join(["python3", script, *(shlex.quote(str(part)) for part in parts)])


# Um servidor de desenvolvimento não termina: proposto como validador, ele espera
# o `--timeout` inteiro e sai como `failed`. E um benchmark não é o primeiro
# validador a rodar — só vinha na frente por ordem alfabética.
LONG_RUNNING = ("serve", "start", "dev", "watch", "preview", "storybook", "docs")
VALIDATOR_ORDER = ("test", "check", "lint", "typecheck", "types", "verify", "audit", "build", "budget", "bench")


def validators(names):
    def rank(name):
        for position, prefix in enumerate(VALIDATOR_ORDER):
            if name == prefix or name.startswith(f"{prefix}:") or name.startswith(f"{prefix}-"):
                return position
        return len(VALIDATOR_ORDER)

    kept = [name for name in names if not any(
        name == word or name.startswith(f"{word}:") or name.startswith(f"{word}-") for word in LONG_RUNNING
    )]
    return sorted(kept, key=lambda name: (rank(name), name))


def starters():
    if not STARTERS_ROOT.is_dir():
        return []
    return sorted(path.name for path in STARTERS_ROOT.iterdir() if path.is_dir() and not path.is_symlink())


def slugify(name):
    folded = "".join(c for c in unicodedata.normalize("NFKD", name.casefold()) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", folded).strip("-")[:200] or "jogo"


def readable_title(name):
    if " " in name or any(character.isupper() for character in name):
        return name
    words = " ".join(part for part in re.split(r"[-_]+", name) if part)
    return words[:1].upper() + words[1:] if words else name


# Um starter com `{{TOKEN}}` no lugar do nome não abre: quem serve a pasta lê o
# token na aba do navegador. Então o starter carrega valores reais e declara,
# em `starter.json`, quais deles `init` troca e em quais arquivos. O escopo por
# arquivo é o que impede a troca de um nome de alcançar um import ou um caminho
# relativo que só se parece com ele.
def starter_manifest(starter):
    source = STARTERS_ROOT / starter
    path = source / STARTER_MANIFEST
    if not path.is_file():
        raise ValueError(f"starter sem {STARTER_MANIFEST}: {starter}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError(f"{starter}/{STARTER_MANIFEST} ilegível: {error}") from error
    entries = manifest.get("substitutions") if isinstance(manifest, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{starter}/{STARTER_MANIFEST} sem `substitutions`")
    for entry in entries:
        field = entry.get("field") if isinstance(entry, dict) else None
        value = entry.get("value") if isinstance(entry, dict) else None
        files = entry.get("files") if isinstance(entry, dict) else None
        if not nonempty(field) or not nonempty(value) or not isinstance(files, list) or not files:
            raise ValueError(f"{starter}/{STARTER_MANIFEST}: substituição incompleta {entry!r}")
        if field not in STARTER_FIELDS:
            raise ValueError(
                f"{starter}/{STARTER_MANIFEST}: campo desconhecido {field!r}; conhecidos: {', '.join(STARTER_FIELDS)}"
            )
        for name in files:
            if not nonempty(name) or name != PurePosixPath(name).as_posix() or ".." in PurePosixPath(name).parts:
                raise ValueError(f"{starter}/{STARTER_MANIFEST}: caminho inválido {name!r}")
            declared = source / name
            if not declared.is_file() or declared.is_symlink():
                raise ValueError(f"{starter}/{STARTER_MANIFEST}: {name} não existe no starter")
            if value not in declared.read_text(encoding="utf-8"):
                raise ValueError(f"{starter}/{STARTER_MANIFEST}: {name} não contém {value!r}")
    return manifest


# Substituição em passo único, do valor mais longo para o mais curto, para que
# o texto recém-inserido nunca seja candidato da próxima troca.
def substitute(text, pairs):
    mapping = dict(pairs)
    pattern = re.compile("|".join(re.escape(old) for old in sorted(mapping, key=len, reverse=True)))
    counted = {}

    def swap(match):
        found = match.group(0)
        counted[found] = counted.get(found, 0) + 1
        return mapping[found]

    return pattern.sub(swap, text), counted


def init(destination, starter, title=None, documents=True):
    available = starters()
    if starter not in available:
        raise ValueError(f"starter desconhecido: {starter}; disponíveis: {', '.join(available) or 'nenhum'}")
    if destination.is_symlink() or destination.is_file():
        raise ValueError("destino existente; escolha um caminho novo")
    if destination.is_dir() and any(destination.iterdir()):
        raise ValueError("destino existente e não vazio; adapte o projeto atual em vez de sobrescrevê-lo")
    manifest = starter_manifest(starter)
    source = STARTERS_ROOT / starter
    entries = sorted(source.rglob("*"))
    for path in entries:
        if path.is_symlink():
            raise ValueError(f"starter contém symlink: {path.relative_to(source)}")
    values = {
        "project": destination.name,
        "project_slug": slugify(destination.name),
        "project_title": title if nonempty(title) else readable_title(destination.name),
        "project_path": str(destination),
        "framework_path": os.path.relpath(FRAMEWORK, destination),
    }
    plan = {}
    for entry in manifest["substitutions"]:
        for name in entry["files"]:
            plan.setdefault(name, []).append((entry["value"], values[entry["field"]]))
    applied = {}
    files = []
    for path in entries:
        relative = path.relative_to(source).as_posix()
        if relative == STARTER_MANIFEST:
            continue
        target = destination / path.relative_to(source)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        pairs = plan.get(relative)
        if pairs:
            text, counted = substitute(path.read_text(encoding="utf-8"), pairs)
            missed = [old for old, _ in pairs if not counted.get(old)]
            if missed:
                raise ValueError(f"{starter}/{STARTER_MANIFEST}: {relative} não contém {missed!r}")
            applied[relative] = counted
            with target.open("x", encoding="utf-8") as document:
                document.write(text)
        elif path.suffix.casefold() in INIT_TEXT_SUFFIXES:
            with target.open("x", encoding="utf-8") as document:
                document.write(path.read_text(encoding="utf-8"))
        else:
            with target.open("xb") as document:
                document.write(path.read_bytes())
        files.append(relative)
    drafts = []
    if documents:
        for stage in INIT_DOCUMENTS:
            output = destination / "docs" / f"{stage}.md"
            template(stage, destination, output)
            drafts.append(output.relative_to(destination).as_posix())
    manager = package_commands(destination)[1]
    return {
        "schema_version": 1,
        "project": str(destination),
        "starter": starter,
        "kind": identify(destination),
        "title": values["project_title"],
        "files": files,
        "documents": drafts,
        "document_status": "draft",
        "substitutions": applied,
        "read_next": [
            str(FRAMEWORK / "references/production-bar.md"),
            str(FRAMEWORK / "references/preproduction.md"),
            str(destination / "README.md"),
        ],
        "next_commands": [
            f"{manager or 'npm'} test" if manager else "node --test",
            harness_command("scan", destination),
            harness_command("next", destination),
        ],
        "scope": (
            "Copiou o starter, trocou os valores que `starter.json` declara e criou rascunhos a partir dos "
            "templates. Os documentos estão vazios de decisão: `scan` vai reportar `draft_only` até que cada área "
            "receba fato, hipótese ou lacuna com próxima ação. O starter é material de ADAPT, não uma engine nem "
            "uma base aprovada; o comando não executa o jogo, não instala dependências e não avalia a proposta."
        ),
    }


def tool_report(name, args=("--version",), timeout=15):
    path = shutil.which(name)
    if not path:
        return {"path": None, "version": None}
    try:
        run = subprocess.run([path, *args], capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError):
        return {"path": path, "version": None}
    lines = (run.stdout or run.stderr or "").strip().splitlines()
    return {"path": path, "version": lines[0].strip() if lines else None}


def skill_targets(root):
    return [root / ".agents/skills/game-dev/SKILL.md", root / ".claude/skills/game-dev/SKILL.md"]


def doctor(root):
    source = FRAMEWORK / "SKILL.md"
    digest = hashlib.sha256(source.read_bytes()).hexdigest() if source.is_file() else None
    available = starters()
    checks = []

    def add(name, required, ok, detail, fix=None):
        checks.append({
            "name": name, "required": required,
            "status": "ok" if ok else ("missing" if required else "optional"),
            "detail": detail,
            "fix": None if ok else fix,
        })

    version = sys.version_info
    add(
        "python", True, version >= (3, 10),
        f"{version.major}.{version.minor}.{version.micro}",
        None if version >= (3, 10) else "Instale Python 3.10 ou mais recente.",
    )
    node = tool_report("node")
    node_major = int(re.sub(r"^v?(\d+).*", r"\1", node["version"])) if node["version"] else 0
    add(
        "node", False, node_major >= 20,
        node["version"] or "ausente",
        None if node_major >= 20 else "Node 20+ é exigido pelo starter canvas-arcade e pelos validadores de package.json.",
    )
    git = tool_report("git")
    add("git", False, bool(git["path"]), git["version"] or "ausente", "Sem git, `verify` registra versão nula no recibo.")
    for binary in ("ffmpeg", "ffprobe"):
        found = tool_report(binary)
        add(binary, False, bool(found["path"]), found["version"] or "ausente", "Necessário só para importar e verificar áudio no acervo.")

    missing_recipes = [focus for focus in FOCI if not (FRAMEWORK / f"recipes/{focus}.md").is_file()]
    missing_templates = [stage for stage in STAGES if not (FRAMEWORK / f"assets/templates/{stage}.md").is_file()]
    missing_references = [
        name for name in ("process.md", "quality.md", "production-bar.md", "preproduction.md", "project-audit.md", "game-design-system.md", "sources.md")
        if not (FRAMEWORK / "references" / name).is_file()
    ]
    add(
        "framework", True, not (missing_recipes or missing_templates or missing_references),
        "receitas, templates e referências completos"
        if not (missing_recipes or missing_templates or missing_references)
        else f"faltando receitas={missing_recipes} templates={missing_templates} referências={missing_references}",
        "Um foco sem receita ou uma etapa sem template quebra `context`.",
    )
    add(
        "starters", False, bool(available),
        ", ".join(available) or "nenhum",
        "Sem starter, `init` não tem de onde partir e REUSE não tem candidato local.",
    )
    # `init` só falha na hora de copiar; aqui a divergência entre o manifesto e
    # os arquivos do starter é diagnosticável antes de alguém tentar criar um
    # projeto, que é quando ela custaria caro.
    broken = []
    for name in available:
        try:
            starter_manifest(name)
        except ValueError as error:
            broken.append(str(error))
    add(
        "starter_manifest", bool(available), not broken,
        f"{len(available) - len(broken)} de {len(available)} manifestos íntegros" if available else "nenhum starter",
        "; ".join(broken) or None,
    )

    installed = []
    for target in skill_targets(root):
        state = "absent"
        # Um symlink para o SKILL.md vigente é o atalho mais atualizado que existe,
        # porque não tem como ficar para trás. Contá-lo como fora de dia avisava
        # justamente quando estava em dia, e mandava trocá-lo por uma cópia que
        # pode envelhecer. Então o vínculo é reportado, e a comparação é do
        # conteúdo — inclusive para symlink apontando para outro arquivo.
        if target.is_symlink() or target.is_file():
            try:
                same = hashlib.sha256(target.read_bytes()).hexdigest() == digest
            except OSError:
                same = False  # link pendurado
            state = "current" if same else "outdated"
        installed.append({
            "path": str(target),
            "status": state,
            "link": target.is_symlink() or None,
        })
    current = [item for item in installed if item["status"] == "current"]
    stale = [item for item in installed if item["status"] != "current"]
    add(
        "skill", False, bool(current),
        f"{len(current)} de {len(installed)} atalhos com o conteúdo vigente"
        + (" · symlink conta como vigente enquanto aponta para ele" if any(item["link"] for item in current) else ""),
        # `cp` sozinho falha quando a pasta do atalho ainda não existe, que é o
        # caso mais comum: correção proposta tem de rodar como está.
        None if current or not stale else (
            f"mkdir -p {shlex.quote(str(Path(stale[0]['path']).parent))} && "
            f"cp {shlex.quote(str(source))} {shlex.quote(str(stale[0]['path']))}"
        ),
    )

    projects = discover(root) if root.is_dir() else []
    add(
        "root", True, root.is_dir(),
        f"{root} · {len(projects)} projeto(s) reconhecido(s)"
        + (" · AGENTS.md presente" if (root / "AGENTS.md").is_file() else ""),
        # Dizer "passe --root" a quem acabou de passar --root é instrução circular:
        # a ação que falta é criar o diretório, ou apontar para outro.
        # `mkdir -p` cria caminho aninhado, então ausência do pai não muda a ação.
        # Só quando o caminho existe e não é pasta é que criar não é a saída.
        None if root.is_dir() else (
            f"O caminho {root} existe e não é um diretório; aponte --root para o laboratório de jogos."
            if root.exists()
            else f"mkdir -p {shlex.quote(str(root))}"
        ),
    )
    library = root / "shared/sfx"
    add(
        "shared/sfx", False, library.is_dir(),
        str(library) if library.is_dir() else "ausente",
        "Sem esse acervo o catálogo vem vazio; `sfx search` não é erro, só não tem o que listar.",
    )

    blocking = [check["name"] for check in checks if check["required"] and check["status"] != "ok"]
    return {
        "schema_version": 1,
        "framework": str(FRAMEWORK),
        "root": str(root),
        "ready": not blocking,
        "blocking": blocking,
        "checks": checks,
        "skill_targets": installed,
        "starters": available,
        "foci": list(FOCI),
        "stages": list(STAGES),
        "scope": (
            "Presença e versão de ferramentas, integridade deste repositório e atalhos da skill no host. "
            "Não instala nada, não copia a skill, não executa o jogo e não comprova que um projeto funciona."
        ),
    }


def next_step(project, focus="create", studies_root=None):
    payload = context(project, focus, studies_root=studies_root)
    foundation = payload["foundation"]
    areas = foundation["areas"]
    drafts = [key for key, area in areas.items() if area["status"] == "draft_only"]
    stale = [key for key, area in areas.items() if area["status"] in ("historical_only", "reference_only")]
    scripts = validators(payload["scripts"])
    proposals = []

    def propose(action, why, done_when, commands, basis):
        proposals.append({
            "action": action, "why": why, "done_when": done_when,
            "commands": commands, "basis": basis,
        })

    if not payload["exists"]:
        propose(
            f"Criar o projeto em {project} a partir de um starter e adaptá-lo à proposta",
            "Sem destino no disco não há candidato para REUSE, e qualquer decisão de design fica sem consumidor.",
            "O jogo abre, `npm test` passa e o README descreve a decisão característica desta proposta.",
            [harness_command("init", project, "--starter", starters()[0] if starters() else "NOME_DO_STARTER")],
            "exists=false",
        )
    elif payload["kind"] is None:
        propose(
            "Identificar o ponto de entrada do jogo e registrar como executá-lo",
            "Sem entrypoint reconhecível não é possível rodar, verificar nem comparar nada — todo o resto fica sem prova.",
            "Um comando declarado no README inicia o jogo, e `scan` reconhece a área de execução.",
            [harness_command("scan", project)],
            "kind=null",
        )
    missing = [key for key, area in areas.items() if area["status"] == "not_located"]
    labels = lambda keys: ", ".join(areas[key]["label"] for key in keys)
    # Não localizado, rascunho e histórico são três problemas diferentes, e todos
    # aparecem em `gaps`. Propor os três de uma vez repetiria a mesma tarefa.
    if missing:
        propose(
            "Avisar as lacunas e documentar as áreas não localizadas: " + labels(missing),
            "A política do estúdio é documentar sem pedir um segundo consentimento; sem essa base as mesmas decisões se repetem a cada sessão.",
            "Cada área tem decisão com fonte, hipótese identificada ou lacuna com motivo e próxima ação.",
            [harness_command("context", project, "--focus", focus, "--event", "direction-approved")],
            "areas.not_located",
        )
    if drafts:
        propose(
            "Substituir rascunho por decisão em: " + labels(drafts),
            "Template com marcador de preenchimento não documenta nada; enquanto for rascunho, cada retomada recomeça do zero.",
            "Os documentos citam fonte, decisão e o que ainda é hipótese, sem marcador de preenchimento.",
            [harness_command("context", project, "--focus", focus, "--stage", "brief" if "vision" in drafts else "gdd")],
            "areas.draft_only",
        )
    if stale:
        propose(
            "Resolver documento sem versão vigente em: " + labels(stale),
            "Só há material histórico ou de referência para essas áreas, e histórico não é regra vigente.",
            "Existe um documento de trabalho vigente, e o histórico permanece marcado como histórico.",
            [harness_command("scan", project)],
            "areas.historical_or_reference_only",
        )
    # Campo de template ainda em rascunho é fonte de continuidade só na forma:
    # "Próxima ação: [uma tarefa concreta...]" não é passo registrado. Propor
    # retomá-lo mandava o agente continuar trabalho que nunca existiu.
    registered = [item for item in foundation["continuity_sources"] if item["status"] != "draft"]
    if registered:
        first = registered[0]
        propose(
            f"Conferir o estado real e retomar o passo registrado em {first['path']}:{first['line']}",
            "Existe fonte de continuidade; retomar evita refazer briefing ou auditoria ainda válida. Fonte encontrada não é tarefa validada.",
            "O passo registrado foi executado ou substituído, com o resultado no registro canônico.",
            [harness_command("context", project, "--focus", focus, "--event", "resume")],
            "continuity.sources",
        )
    if scripts:
        propose(
            f"Executar os validadores do projeto com recibo ({', '.join(scripts[:4])})",
            "Comando declarado não é comando executado; sem recibo não há evidência técnica para nenhuma decisão.",
            "Existe uma pasta de evidência com recibo e log de cada comando escolhido.",
            [harness_command("verify", project, "--script", scripts[0], "--output", "CAMINHO_NOVO")],
            "scripts",
        )
    bar = payload["production_bar"]
    dimensions = [item["key"] for item in bar["dimensions"]]
    declaration = bar["declaration"]
    # Sem declaração, a barra é um vocabulário; com ela, a dimensão mais baixa é
    # uma tarefa com nome. Linha malformada vem primeiro porque ela é a causa: uma
    # dimensão com erro de digitação aparece como não declarada, e propor declarar
    # o que já foi declarado manda a pessoa reescrever em vez de corrigir.
    if declaration["problems"]:
        propose(
            "Corrigir a forma da declaração de degrau em: "
            + ", ".join(f"{item['source']} ({item['reason']})" for item in declaration["problems"][:4]),
            "Linha malformada não entra na leitura, e a dimensão que ela pretendia declarar continua contando "
            "como não declarada — aqui o erro mais provável é o de digitação.",
            "Cada linha nomeia uma das dez dimensões, um dos cinco degraus e o degrau imediatamente seguinte.",
            [harness_command("bar", project)],
            "production_bar.problems",
        )
    elif declaration["undeclared"]:
        propose(
            "Declarar o degrau das dimensões ainda sem linha: " + ", ".join(declaration["undeclared"]),
            "Dimensão não declarada não é dimensão alta — enquanto faltar uma, o mínimo entre as dez é "
            "desconhecido e nenhuma leitura do acabamento se sustenta.",
            f"Cada dimensão tem uma linha em {declaration['sources'][0]} com degrau atual, degrau seguinte e "
            "o critério que falta, e o degrau percebido sai do mínimo.",
            [harness_command("context", project, "--focus", focus, "--stage", "qa")],
            "production_bar.undeclared",
        )
    elif declaration["conflicts"]:
        propose(
            "Resolver declaração de degrau em conflito: "
            + ", ".join(item["dimension"] for item in declaration["conflicts"]),
            "Duas linhas discordantes sobre a mesma dimensão não se resolvem por precedência; enquanto "
            "discordarem, a mais baixa é a que vale e a leitura do projeto fica em dúvida.",
            "Cada dimensão tem uma declaração vigente, e as demais estão marcadas como histórico.",
            [harness_command("scan", project)],
            "production_bar.conflicts",
        )
    else:
        lowest = declaration["at_floor"][0]
        entry = declaration["declared"][lowest]
        propose(
            f"Subir `{lowest}` de `{entry['tier']}` para `{entry['next_tier'] or 'o degrau seguinte'}`: "
            + (entry["gap"] or "critério declarado no próprio documento"),
            "O degrau percebido é o mínimo entre as dimensões; subir a que já está alta não muda a leitura do "
            f"jogo. Hoje o piso é `{declaration['floor']}` em {', '.join(declaration['at_floor'])}, "
            f"segundo {entry['source']}.",
            f"`{lowest}` cumpre o critério do degrau seguinte, com condição, evidência e autor declarados, e a "
            "linha correspondente é atualizada.",
            [harness_command("context", project, "--focus", focus)],
            "production_bar.floor",
        )
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": payload["exists"],
        "kind": payload["kind"],
        "focus": focus,
        "proposal": proposals[0],
        "alternatives": proposals[1:],
        "signals": {
            "minimum_status": foundation["minimum_status"],
            "gaps": foundation["gaps"],
            "draft_areas": drafts,
            "non_current_areas": stale,
            "continuity_source_count": foundation["continuity_source_count"],
            "scripts": scripts,
            "package_manager": payload["package_manager"],
            "production_bar_dimensions": dimensions,
            "production_bar_floor": declaration["floor"],
            "production_bar_undeclared": declaration["undeclared"],
            "production_bar_problems": declaration["problems"],
        },
        "context_command": harness_command("context", project, "--focus", focus),
        "authority": "agent_resolves",
        "executed": False,
        "scope": (
            "Proposta ordenada por dependência, derivada só do que é observável no disco. Não é fila validada, "
            "não conhece a conversa, a direção do usuário nem o backlog, e não concede autorização. "
            "O agente confronta a proposta com o pedido real e decide; `alternatives` existe para ser escolhida."
        ),
    }


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def check_plan(plan, root):
    errors = []
    if not isinstance(plan, dict):
        return ["plano deve ser um objeto JSON"]
    if plan.get("schema_version") != 1:
        errors.append("schema_version deve ser 1")
    for key in ("project", "need", "why", "visual_reference"):
        if not nonempty(plan.get(key)):
            errors.append(f"{key}: falta texto")
    for key in ("searches", "change", "acceptance"):
        value = plan.get(key)
        if not isinstance(value, list) or not value or not all(nonempty(item) for item in value):
            errors.append(f"{key}: exige lista de textos preenchidos")
    decision = plan.get("decision")
    if decision not in ("reuse", "adapt", "create"):
        errors.append("decision: escolha reuse, adapt ou create")
    candidates = plan.get("candidates")
    if not isinstance(candidates, list):
        return errors + ["candidates deve ser uma lista"]
    paths = []
    for item in candidates:
        if not isinstance(item, dict):
            errors.append("candidato deve ser um objeto")
            continue
        for key in ("path", "consumer", "fit"):
            if not nonempty(item.get(key)):
                errors.append(f"candidato: falta {key}")
        for key in ("path", "consumer"):
            if nonempty(item.get(key)) and not resolve(item[key], root).exists():
                errors.append(f"candidato: {key} não existe: {item[key]}")
        if nonempty(item.get("path")):
            paths.append(resolve(item["path"], root))
    if decision in ("reuse", "adapt"):
        if not nonempty(plan.get("selected")) or resolve(plan["selected"], root) not in paths:
            errors.append("reuse/adapt exige selected entre os candidatos lidos")
    if decision == "create" and not nonempty(plan.get("gap")):
        errors.append("create exige gap: por que reuso e adaptação não atendem")
    return errors


def git_version(project):
    result = {}
    for key, args in (("head", ["rev-parse", "HEAD"]), ("status", ["status", "--porcelain", "--", "."])):
        run = subprocess.run(["git", "-C", str(project), *args], capture_output=True, text=True, check=False)
        result[key] = run.stdout.strip() if run.returncode == 0 else None
    result["scope"] = "HEAD e nomes alterados; não é fingerprint completo das fontes."
    return result


def run_command(argv, project, log, timeout):
    started = time.monotonic()
    with log.open("x", encoding="utf-8") as output:
        try:
            process = subprocess.Popen(argv, cwd=project, stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                output.write(f"\nTimeout após {timeout}s; grupo de processos encerrado.\n")
                code = 124
        except OSError as error:
            output.write(f"{error}\n")
            code = 127
    return {"argv": argv, "exit_code": code, "seconds": round(time.monotonic() - started, 3), "log": log.name, "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest()}


def verify(project, scripts, command, output, timeout, proves=()):
    if not project.is_dir():
        raise ValueError("projeto ausente")
    if timeout <= 0:
        raise ValueError("timeout precisa ser positivo")
    if bool(scripts) == bool(command):
        raise ValueError("use --script (repetível) OU --command com argv explícito")
    unknown = [name for name in proves if name not in CAPABILITIES]
    if unknown:
        raise ValueError(f"capacidade fora do conjunto conhecido: {unknown}")
    claimed = list(dict.fromkeys(proves))
    declared, manager = package_commands(project)
    commands = []
    for name in scripts:
        if not manager or name not in declared or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.:-]*", name):
            raise ValueError(f"script ausente/inválido ou gerenciador ambíguo: {name}")
        commands.append([manager, "run", name])
    if command:
        commands.append(command)
    if output.exists() or output.is_symlink():
        raise ValueError("destino de evidência existente; escolha um novo")
    before = git_version(project)
    output.mkdir(parents=True, exist_ok=False)
    report = {"schema_version": 1, "project": str(project), "started_at": datetime.now(timezone.utc).isoformat(), "version": before, "technical_status": "running", "experience_status": "not_assessed", "commands": [], "scope": "Execução dos comandos solicitados. Não aprova arte, diversão, direitos, release nem capacidades do runtime."}
    receipt = output / "verification.json"
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for index, argv in enumerate(commands):
        print(f"Executando: {argv} em {project}", file=sys.stderr, flush=True)
        result = run_command(argv, project, output / f"{index + 1:02d}.log", timeout)
        report["commands"].append(result)
        if result["exit_code"]:
            break
    passed = all(item["exit_code"] == 0 for item in report["commands"]) and len(report["commands"]) == len(commands)
    report.update(technical_status="passed" if passed else "failed", finished_at=datetime.now(timezone.utc).isoformat())
    # `context` só sabe dizer `mentioned`: ele lê arquivos, não executa nada. Este
    # bloco não promove nada a verificado — o harness não tem como saber se os
    # comandos exercitam a capacidade. O que ele acrescenta é uma afirmação com
    # autor, data, argv e log: em vez de sumir na prosa, a alegação fica anexada
    # a um recibo e pode ser contestada por quem ler.
    report["capabilities"] = {
        name: {
            "status": "claimed" if passed else "unsupported",
            "commands_passed": passed,
            "by": [item["argv"] for item in report["commands"]],
            "logs": [item["log"] for item in report["commands"]],
            "claimed_by": "operator",
            "limit": "Alegação de quem executou, apoiada em recibo verde. Recibo verde não é cobertura da capacidade.",
        }
        for name in claimed
    }
    report["capabilities_scope"] = (
        "Capacidade só aparece aqui porque quem executou a declarou em --proves. O harness confere que o nome "
        "pertence ao conjunto conhecido e que os comandos passaram; não confere que eles a exercitam. "
        "`claimed` é alegação registrada, não verificação: continua valendo que mentioned não é verified."
    )
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


def main():
    # `--root` é aceito antes e depois do subcomando. A documentação sempre o
    # escreveu depois, e argparse só o aceitava antes: cada exemplo com `--root`
    # falhava com código 2. O parser comum abaixo herda a opção em todo
    # subcomando, com default suprimido para não sobrescrever o valor global.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=argparse.SUPPRESS, help="raiz para descobrir projetos e resolver caminhos")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="raiz para descobrir projetos e resolver caminhos")
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("discover", parents=[common])
    commands.add_parser("doctor", parents=[common], help="ambiente, integridade do framework e atalhos da skill")
    start = commands.add_parser("init", parents=[common], help="cria um projeto novo a partir de um starter, para ADAPT")
    start.add_argument("project")
    start.add_argument("--starter", default=starters()[0] if starters() else None, choices=starters() or None)
    start.add_argument("--title", help="título legível; por omissão, derivado do nome da pasta")
    start.add_argument("--no-docs", action="store_true", help="não criar os rascunhos em docs/")
    upcoming = commands.add_parser("next", parents=[common], help="proposta ordenada de próxima ação, a partir do estado no disco")
    upcoming.add_argument("project")
    upcoming.add_argument("--focus", choices=FOCI, default="create")
    initial_scan = commands.add_parser("scan", parents=[common])
    initial_scan.add_argument("project")
    reading = commands.add_parser("bar", parents=[common], help="degrau de acabamento que o projeto declara, e qual dimensão é o piso")
    reading.add_argument("project")
    ctx = commands.add_parser("context", parents=[common])
    ctx.add_argument("project")
    ctx.add_argument("--focus", choices=FOCI, default="create")
    ctx.add_argument("--stage", choices=STAGES)
    ctx.add_argument("--event", choices=EVENTS, default="task", help="evento observado na conversa pelo agente; não concede aprovação")
    doc = commands.add_parser("template", parents=[common])
    doc.add_argument("stage", choices=STAGES)
    doc.add_argument("--project", required=True)
    doc.add_argument("--output", type=Path, help="sem output, imprime o rascunho sem escrever")
    plan = commands.add_parser("check-plan", parents=[common])
    plan.add_argument("plan", type=Path)
    run = commands.add_parser("verify", parents=[common])
    run.add_argument("project")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--timeout", type=float, default=300)
    run.add_argument("--script", action="append", default=[])
    run.add_argument("--proves", action="append", default=[], choices=CAPABILITIES, help="capacidade que esta execução se propõe a demonstrar; a afirmação é de quem executa")
    run.add_argument("--command", nargs=argparse.REMAINDER)
    sfx = commands.add_parser("sfx", parents=[common], help="catálogo compartilhado de efeitos sonoros")
    sfx_cmd = sfx.add_subparsers(dest="sfx_action")
    sfx_cmd.add_parser("summary", parents=[common])
    sfx_search = sfx_cmd.add_parser("search", parents=[common])
    sfx_search.add_argument("query")
    sfx_search.add_argument("--limit", type=int, default=40)
    sfx_copy = sfx_cmd.add_parser("copy", parents=[common])
    sfx_copy.add_argument("id")
    sfx_copy.add_argument("--to", required=True)
    sfx_copy.add_argument("--sources")
    sfx_cmd.add_parser("verify", parents=[common])
    sfx_serve = sfx_cmd.add_parser("serve", parents=[common])
    sfx_serve.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if args.action == "discover":
            emit(discover(root))
        elif args.action == "doctor":
            report = doctor(root)
            emit(report)
            return int(not report["ready"])
        elif args.action == "init":
            if not args.starter:
                raise ValueError("nenhum starter disponível neste repositório")
            emit(init(resolve(args.project, root), args.starter, args.title, not args.no_docs))
        elif args.action == "next":
            emit(next_step(resolve(args.project, root), args.focus, studies_root=default_studies_root(root)))
        elif args.action == "scan":
            emit(scan(resolve(args.project, root)))
        elif args.action == "bar":
            emit(bar_reading(resolve(args.project, root)))
        elif args.action == "context":
            emit(context(resolve(args.project, root), args.focus, args.stage, studies_root=default_studies_root(root), event=args.event))
        elif args.action == "template":
            document = template(args.stage, resolve(args.project, root), args.output)
            if args.output:
                emit({"document": str(args.output.resolve()), "status": "draft", "scope": "Template inicial; decisões, revisão e prova continuam pendentes."})
            else:
                print(document, end="")
        elif args.action == "check-plan":
            errors = check_plan(read_json(args.plan), root)
            emit({"contract_valid": not errors, "errors": errors, "scope": "Estrutura e existência dos candidatos; busca, adequação e qualidade exigem revisão."})
            return int(bool(errors))
        elif args.action == "sfx":
            if args.sfx_action in (None, "summary"):
                emit(sfx_catalog.summarize(root))
            elif args.sfx_action == "search":
                emit(sfx_catalog.search_catalog(args.query, root, limit=args.limit))
            elif args.sfx_action == "copy":
                emit(sfx_catalog.copy_entry(args.id, args.to, root, sources=args.sources))
            elif args.sfx_action == "serve":
                sfx_catalog.serve_catalog(root, port=args.port)
            else:
                check = sfx_catalog.verify_catalog(root)
                emit(check)
                return int(not check["ok"])
        else:
            report = verify(resolve(args.project, root), args.script, args.command, args.output.absolute(), args.timeout, args.proves)
            emit(report)
            return int(report["technical_status"] != "passed")
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
