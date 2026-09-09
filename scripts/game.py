#!/usr/bin/env python3
"""Games harness: contexto sob demanda, contrato de reuso e execução com recibo."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
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
FOCI = ("create", "mechanics", "lifecycle", "content", "visual", "audio", "feel", "network", "architecture", "production")
STAGES = ("brief", "mda", "gdd", "poc", "prd", "tdd", "vertical-slice", "mvp", "qa", "art-bible", "devlog", "audit", "aaa", "game-design", "production-plan", "milestone")
PRODUCTION_STAGES = ("production-plan", "milestone")
EVENTS = ("task", "direction-approved", "resume")
REFERENCES = ("process", "quality", "preproduction", "project-audit", "game-design-system", "sources", "ambition", "aaa-checklist")
# Pacotes: o núcleo é agnóstico; um pacote só entra quando a plataforma foi identificada ou o gênero foi declarado.
PLATFORM_PACKS = {
    "package.json": "web", "static-web": "web", "unity": "unity", "godot": "godot", "unreal": "unreal",
    "defold": "defold", "gamemaker": "gamemaker", "cargo": "cargo", "python": "python", "lua": "lua",
    "construct": "construct", "rpgmaker": "rpgmaker", "renpy": "renpy", "roblox": "roblox", "pico8": "pico8",
    "haxe": "haxe", "flutter": "flutter", "dotnet": "dotnet", "cpp": "cpp",
}
GENRES = (
    "narrative", "adventure", "platformer", "action-adventure", "shooter", "fighting", "stealth", "horror",
    "racing", "sports", "rhythm", "turn-based", "deckbuilder", "strategy", "tower-defense", "puzzle",
    "simulation", "survival-crafting", "rpg", "roguelike", "multiplayer-competitive", "idle", "casual",
)
GENRE_KEYWORDS = {
    "narrative": ("narrativ", "conto", "visual novel", "interactive fiction", "aventura textual", "historia interativa"),
    "adventure": ("point and click", "point n click", "aventura grafica", "adventure", "escape room"),
    "platformer": ("plataforma", "platformer", "metroidvania"),
    "action-adventure": ("acao aventura", "action adventure", "mundo aberto", "open world", "zelda", "soulslike", "hack and slash", "beat em up"),
    "shooter": ("fps", "tps", "shooter", "tiro", "shoot em up", "shmup"),
    "fighting": ("luta", "fighting", "versus"),
    "stealth": ("stealth", "furtiv", "infiltra"),
    "horror": ("horror", "terror", "survival horror"),
    "racing": ("corrida", "racing", "kart", "drift"),
    "sports": ("esporte", "sports", "futebol", "football", "basquete", "skate", "golf", "tenis"),
    "rhythm": ("ritmo", "rhythm", "musica", "music game", "dance"),
    "turn-based": ("turno", "turn based", "tabuleiro", "board game", "tatico", "tactics", "xcom"),
    "deckbuilder": ("deckbuild", "card battler", "cartas", "card game", "baralho", "tcg", "ccg"),
    "strategy": ("estrategia", "strategy", "rts", "4x", "grand strategy"),
    "tower-defense": ("tower defense", "defesa de torre"),
    "puzzle": ("puzzle", "quebra cabeca", "logica", "match 3"),
    "simulation": ("simula", "fabrica", "factory", "gestao", "management", "tycoon", "city builder", "automacao"),
    "survival-crafting": ("survival", "sobreviv", "crafting", "sandbox", "minecraft", "colonia"),
    "rpg": ("rpg", "jrpg", "arpg", "crpg"),
    "roguelike": ("roguelike", "roguelite", "run based", "permadeath"),
    "multiplayer-competitive": ("moba", "battle royale", "hero shooter", "arena", "competitiv", "esports", "pvp"),
    "idle": ("idle", "clicker", "incremental"),
    "casual": ("casual", "hypercasual", "hyper casual", "party game", "minigame"),
}
GENRE_FIELD = re.compile(r"^\s*(?:[-*]\s+)?(?:g[eê]nero(?: do jogo)?|genre)\s*:\s*(.+?)\s*$", re.IGNORECASE)
# Ordem importa: engines com marcador próprio primeiro (RPG Maker MZ e outras também trazem package.json),
# depois manifestos de ecossistema, por último marcadores genéricos.
ENGINE_MARKERS = (
    ("ProjectSettings/ProjectVersion.txt", "unity"),
    ("project.godot", "godot"),
    ("*.uproject", "unreal"),
    ("game.project", "defold"),
    ("*.yyp", "gamemaker"),
    ("*.c3proj", "construct"),
    ("*.rmmzproject", "rpgmaker"),
    ("*.rpgproject", "rpgmaker"),
    ("game/options.rpy", "renpy"),
    ("default.project.json", "roblox"),
    ("*.p8", "pico8"),
    ("Project.xml", "haxe"),
    ("*.hxml", "haxe"),
    ("pubspec.yaml", "flutter"),
    ("*.sln", "dotnet"),
    ("*.csproj", "dotnet"),
    ("package.json", "package.json"),
    ("Cargo.toml", "cargo"),
    ("CMakeLists.txt", "cpp"),
    ("pyproject.toml", "python"),
    ("main.lua", "lua"),
    ("index.html", "static-web"),
)
CONTINUITY_PATTERN = r"\b(continuidade|continuity|retomada|proxim[ao]s? (passos?|acoes|acao|tarefas?)|next steps?)\b"
CONTINUITY_FILES = {"production plan", "plano de producao", "roadmap", "backlog", "state", "decisions", "devlog"}
FOUNDATION_AREAS = (
    ("vision", "Visão e escopo / Brief ou PRD", r"\b(brief|prd|visao|vision|escopo|scope|publico|target audience)\b"),
    ("gdd", "Design do jogo / GDD", r"\b(gdd|game design|gameplay|mecanicas|regras|como jogar|core loop)\b"),
    ("mda", "Hipóteses de experiência / MDA", r"\b(mda|hipoteses de experiencia|experiencia pretendida|experiencia desejada|experience goals|emotional goals)\b"),
    ("architecture", "Arquitetura atual / TDD", r"\b(tdd|arquitetura|architecture|technical design|contratos tecnicos)\b"),
    ("art_direction", "Design system do jogo / Art Bible", r"^design$|\b(art bible|art-bible|art direction|design system|design-system|game design system|direcao de arte|direcao visual|direcao audiovisual|style guide|visual style|feel bible)\b"),
    ("decisions", "Decisões e histórico / Devlog", r"\b(devlog|decision log|decisions|decisoes|changelog|aprendizados|historico de decisoes|adr)\b"),
    ("qa", "QA e playtest", r"\b(qa|playtest|test plan|verification|verificacao|validacao|plano de testes|checklist de piso|piso de acabamento|chk-\d)\b"),
    ("runbook", "Como executar e verificar", r"\b(runbook|getting started|setup|instalacao|executar|rodar|desenvolvimento|development|jogar|build|package)\b"),
    ("provenance", "Origem de código e assets", r"\b(licenses?|licences?|licencas?|copying|authors|sources|proveniencia|provenance|creditos|credits|asset sources)\b"),
)
CAPABILITIES = ("pause", "reset", "seed", "observe", "act", "advance", "capture", "dispose")
FINISH_CORE = ("CHK-0", "CHK-1", "CHK-2", "CHK-4", "CHK-5", "CHK-6", "CHK-11")
FINISH_PRODUCT = ("CHK-3", "CHK-7", "CHK-8", "CHK-10", "CHK-14", "CHK-15")
FINISH_PROMISE = ("CHK-9", "CHK-12", "CHK-13")
FINISH_MARKET = ("CHK-16",)
SKIP = {
    "node_modules", "dist", "build", "docs", "framework", "squads", "public", "assets", "outputs", "shared",
    "Assets", "Library", "Temp", "Logs", "UserSettings",  # Unity
    "Binaries", "Intermediate", "Saved", "DerivedDataCache", "Content", "Plugins",  # Unreal
    "target", "__pycache__",  # Cargo / Python
    "bin", "obj", "export", "cmake-build-debug", "cmake-build-release",  # .NET / Haxe / CMake
}
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
    "src/engine/core/loop.js", "tools/verify.py", "headless/env_server.ts",
)
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


def normalize_text(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold()) if not unicodedata.combining(c)).replace("-", " ").replace("_", " ")


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def resolve(value, root=ROOT):
    return (root / value).resolve()


def identify(project):
    if not project.is_dir():
        return None
    for marker, kind in ENGINE_MARKERS:
        if "*" in marker:
            if any(path.is_file() for path in project.glob(marker)):
                return kind
        elif (project / marker).is_file():
            return kind
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


CARGO_TARGETS = ("check", "build", "test")


def project_commands(project):
    """Comandos declarados pelo projeto: scripts de package.json ou alvos convencionais do Cargo.

    Retorna ({nome: {"body", "argv"}}, executor). argv None significa executor ambíguo.
    Só entram comandos determinísticos a partir do manifesto; engines sem CLI padronizada
    (Unity, Godot, Unreal) continuam via --command explícito.
    """
    if (project / "package.json").is_file():
        scripts, manager = package_commands(project)
        return {name: {"body": body, "argv": [manager, "run", name] if manager else None} for name, body in scripts.items()}, manager
    if (project / "Cargo.toml").is_file():
        return {name: {"body": f"cargo {name}", "argv": ["cargo", name]} for name in CARGO_TARGETS}, "cargo"
    return {}, None


def studies_for(focus, studies_root):
    if focus not in FOCUS_STUDIES:
        return []
    found = []
    for relative in FOCUS_STUDIES[focus]:
        path = studies_root / relative
        if path.is_file():
            found.append(str(path))
    return found


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
    deferred, non_current, continuity_sources, genre_mentions = [], [], [], []
    link_count, max_links, links_limited = 0, 128, False
    inline_link = re.compile(r'(?<!!)\[[^\]\n]+\]\((?:<([^>\n]+)>|([^\s)]+))(?:\s+"[^"]*")?\)')
    navigation = re.compile(r"^\s*(?:(?:[-*]|\d+[.)])\s+)?\[[^\]]+\](?:\(|\[)")

    normalized = normalize_text

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
                genre = GENRE_FIELD.match(line)
                if genre and status in {"candidate", "draft"} and len(genre_mentions) < 5:
                    genre_mentions.append({"path": relative, "line": number, "value": genre.group(1)})
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
        "genre_mentions": genre_mentions,
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


def select_references(focus, stage, document_minimum):
    """Seleciona as leituras do framework para o foco/etapa; cada arquivo entra uma vez, na ordem de leitura."""
    references = [FRAMEWORK / "references/process.md", FRAMEWORK / "references/quality.md", FRAMEWORK / f"recipes/{focus}.md"]
    if stage == "tdd":
        references.append(FRAMEWORK / "recipes/architecture.md")
    if stage in PRODUCTION_STAGES:
        references.append(FRAMEWORK / "recipes/production.md")
    if stage or focus == "create":
        references.append(FRAMEWORK / "references/preproduction.md")
    if focus in ("create", "visual", "audio", "feel") or stage in ("art-bible", "aaa", "game-design"):
        references.append(FRAMEWORK / "references/game-design-system.md")
    if focus in ("create", "audio", "feel") or stage in ("brief", "vertical-slice", "aaa"):
        references.append(FRAMEWORK / "references/ambition.md")
    if focus in ("create", "feel", "audio", "production") or stage in ("aaa", "vertical-slice", "qa", "milestone"):
        references.append(FRAMEWORK / "references/aaa-checklist.md")
    if stage == "aaa":
        references.extend(FRAMEWORK / f"recipes/{extra}.md" for extra in ("feel", "audio"))
    if stage:
        references.append(FRAMEWORK / f"assets/templates/{stage}.md")
    if document_minimum or stage in ("art-bible", "devlog"):
        references.append(FRAMEWORK / "references/project-audit.md")
    return list(dict.fromkeys(references))


def suggest_genres(mentions):
    """Mapeia valores lexicais de um campo Gênero para pacotes; sugestão, não classificação."""
    suggested = []
    for mention in mentions:
        value = normalize_text(mention["value"])
        for genre, keywords in GENRE_KEYWORDS.items():
            if genre not in suggested and any(keyword in value for keyword in keywords):
                suggested.append(genre)
    return suggested


def select_packs(kind, genre, mentions):
    pack_name = PLATFORM_PACKS.get(kind)
    platform_path = FRAMEWORK / f"packs/platforms/{pack_name}.md" if pack_name else None
    genre_path = FRAMEWORK / f"packs/genres/{genre}.md" if genre else None
    suggested = suggest_genres(mentions)
    return {
        "platform": {
            "kind": kind, "pack": str(platform_path) if platform_path and platform_path.is_file() else None,
            "basis": "identify: marcador de manifesto/engine no diretório do projeto" if kind else "projeto sem marcador reconhecido; núcleo agnóstico apenas",
        },
        "genre": {
            "name": genre, "pack": str(genre_path) if genre_path and genre_path.is_file() else None,
            "basis": "--genre declarado na conversa" if genre else ("campo Gênero localizado em documento; confirme e passe --genre" if suggested else "não declarado; passe --genre quando o jogo tiver gênero definido"),
            "suggested": suggested, "mentions": mentions, "available": list(GENRES),
        },
        "scope": "Pacotes são convenções de plataforma/gênero para orientar leitura e verificação. Não substituem AGENTS, a documentação oficial nem o que o projeto realmente faz; confirme cada convenção no código.",
    }


def context(project, focus, stage=None, studies_root=None, event="task", root=None, genre=None):
    if focus not in FOCI:
        raise ValueError("foco desconhecido")
    if genre is not None and genre not in GENRES:
        raise ValueError("gênero desconhecido")
    if stage is not None and stage not in STAGES:
        raise ValueError("etapa desconhecida")
    if event not in EVENTS:
        raise ValueError("evento desconhecido")
    if project.exists() and not project.is_dir():
        raise ValueError("projeto precisa ser um diretório")
    metadata_issues = []
    try:
        scripts, manager = project_commands(project)
    except (OSError, ValueError, RecursionError) as error:
        scripts, manager = {}, None
        metadata_issues.append({"path": "package.json", "reason": str(error)})
    instructions = [str(parent / "AGENTS.md") for parent in reversed((project, *project.parents)) if (parent / "AGENTS.md").is_file()]
    foundation = scan(project)
    records = [str(project / relative) for relative in foundation["read_first"]]
    document_minimum = foundation["audit"]["required"] or event == "direction-approved" or stage == "audit"
    kind = identify(project)
    packs = select_packs(kind, genre, foundation["genre_mentions"])
    references = [str(path) for path in select_references(focus, stage, document_minimum)]
    recipe = str(FRAMEWORK / f"recipes/{focus}.md")
    for pack in (packs["genre"]["pack"], packs["platform"]["pack"]):  # inserção reversa: receita → plataforma → gênero
        if pack:
            references.insert(references.index(recipe) + 1 if recipe in references else len(references), pack)
    references = list(dict.fromkeys(references))
    studies = studies_for(focus, STUDIES_ROOT if studies_root is None else studies_root)
    return {
        "schema_version": 3, "project": str(project), "exists": project.is_dir(), "kind": kind,
        "focus": focus, "stage": stage, "event": event, "instructions": instructions, "records": records,
        "read_next": references, "packs": packs, "studies": studies,
        "source_index": str(FRAMEWORK / "references/sources.md"),
        "package_manager": manager,
        "metadata_issues": metadata_issues,
        "scripts": scripts,
        "capabilities": mention_capabilities(project), "foundation": foundation,
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
        "finish": {
            "guide": str(FRAMEWORK / "references/aaa-checklist.md"),
            "template": str(FRAMEWORK / "assets/templates/aaa.md"),
            "core_groups": list(FINISH_CORE),
            "product_groups": list(FINISH_PRODUCT),
            "promise_groups": list(FINISH_PROMISE),
            "market_groups": list(FINISH_MARKET),
            "action": "observe_core_on_slice" if stage in ("aaa", "vertical-slice", "qa", "milestone") or focus in ("feel", "audio", "production") else "defer_until_playable_cycle",
            "executed": False,
            "scope": "Núcleo em qualquer escala após um ciclo jogável. Produto/AA soma product_groups. Promessa só se o brief prometeu. Mercado (CHK-16) nunca reprova jam. Completar o template não certifica. O comando não observa o jogo.",
        },
        "studio_assets": sfx_catalog.studio_assets(root),
        "limits": [
            "Ponteiros não comprovam leitura; scripts declarados não comprovam execução.",
            "Inspecione os scripts antes de executá-los. Nenhum comando é executado por context.",
            "Sem packageManager ou lockfile, npm é apenas a convenção do executor de package.json.",
            "Consulte AGENTS.md mais específicos ao escolher os arquivos que serão alterados.",
            "studies lista catálogos do foco se existirem no irmão Games-Frameworks; ausência não é evidência negativa.",
            "capabilities.mentioned é só token em arquivo de inspeção. Não prova pause, reset, seed nem determinismo.",
            "capabilities.unknown significa não localizado na lista fixa de arquivos de inspeção, não capacidade ausente; rastreie o entrypoint e os consumidores na auditoria.",
            "Áudio novo: busque em shared/sfx (`sfx search`) antes de baixar. Piso de gravação licenciada; 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão.",
            "Feel e áudio são focos próprios (`--focus feel`, `--focus audio`). Sem observação em movimento, experience_status permanece not_assessed; scaffold não é vertical slice.",
            "“AAA” neste harness é piso de acabamento da slice, não tier de publisher. Sem feel sincronizado, pacing e repeatability, não use o adjetivo.",
            "Checklist: ver finish no JSON. Jam observa core_groups; produto/AA soma product_groups; promise_groups só se prometidos. `template aaa` não certifica; N/A exige motivo.",
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


def doctor(root, studies_root=None):
    """Autodiagnóstico do harness: instalação, integridade dos arquivos e caminhos resolvidos. Não executa jogos."""
    checks = []

    def check(name, ok, detail, required=True):
        status = "ok" if ok else ("missing" if required else "absent")
        checks.append({"check": name, "status": status, "required": required, "detail": detail})

    check("python", sys.version_info >= (3, 10), {"version": platform.python_version(), "minimum": "3.10"})
    expected = [
        FRAMEWORK / "SKILL.md", FRAMEWORK / "README.md", FRAMEWORK / "assets/work.example.json",
        *(FRAMEWORK / f"recipes/{focus}.md" for focus in FOCI),
        *(FRAMEWORK / f"assets/templates/{stage}.md" for stage in STAGES),
        *(FRAMEWORK / f"references/{name}.md" for name in REFERENCES),
        *(FRAMEWORK / f"packs/platforms/{name}.md" for name in sorted(set(PLATFORM_PACKS.values()))),
        *(FRAMEWORK / f"packs/genres/{name}.md" for name in GENRES),
    ]
    missing = [path.relative_to(FRAMEWORK).as_posix() for path in expected if not path.is_file()]
    check("framework_files", not missing, {"framework": str(FRAMEWORK), "expected": len(expected), "missing": missing})
    check("root", root.is_dir(), {"path": str(root), "hint": "passe --root com a raiz do laboratório de jogos"})
    check("root_instructions", (root / "AGENTS.md").is_file(), str(root / "AGENTS.md"), required=False)
    projects = discover(root) if root.is_dir() else []
    check("projects", bool(projects), {"count": len(projects), "kinds": sorted({item["kind"] for item in projects}), "known_markers": [marker for marker, _ in ENGINE_MARKERS]}, required=False)
    studies = default_studies_root(root) if studies_root is None else Path(studies_root)
    check("studies", studies.is_dir(), str(studies), required=False)
    sfx = sfx_catalog.studio_assets(root)["sfx"]
    check("sfx", sfx["exists"], sfx["catalog"], required=False)
    git = shutil.which("git")
    check("git", bool(git), git or "não encontrado no PATH; verify registra version.head = null", required=False)
    ok = all(item["status"] != "missing" for item in checks)
    if not ok:
        next_step = "Corrija os itens `missing` antes de usar context/verify."
    elif projects:
        next_step = "python3 scripts/game.py context <projeto> --focus create --root <raiz>; para jogo novo, template game-design --project <novo> --output <arquivo>."
    else:
        next_step = "Nenhum projeto reconhecido na raiz. Para um jogo novo: template game-design --project <novo> --output <arquivo>, depois context <novo> --focus create."
    return {
        "schema_version": 1, "ok": ok, "framework": str(FRAMEWORK), "root": str(root), "checks": checks,
        "next": next_step,
        "scope": "Verifica instalação, integridade dos arquivos do framework e caminhos resolvidos. Itens `absent` são opcionais. Não executa jogos, não avalia projetos nem aprova nada.",
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


def verify(project, scripts, command, output, timeout):
    if not project.is_dir():
        raise ValueError("projeto ausente")
    if timeout <= 0:
        raise ValueError("timeout precisa ser positivo")
    if bool(scripts) == bool(command):
        raise ValueError("use --script (repetível) OU --command com argv explícito")
    declared, _ = project_commands(project)
    commands = []
    for name in scripts:
        entry = declared.get(name) if re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.:-]*", name) else None
        if not entry or not entry["argv"]:
            raise ValueError(f"script ausente/inválido ou gerenciador ambíguo: {name}")
        commands.append(entry["argv"])
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
    report.update(technical_status="passed" if all(item["exit_code"] == 0 for item in report["commands"]) else "failed", finished_at=datetime.now(timezone.utc).isoformat())
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


def build_parser():
    # --root é aceito antes ou depois do subcomando; SUPPRESS evita que o subparser sobrescreva o valor global.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=argparse.SUPPRESS, help="raiz do laboratório para descobrir projetos e resolver caminhos (padrão: %s)" % ROOT)
    parser = argparse.ArgumentParser(description=__doc__, parents=[common])
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("discover", parents=[common], help="lista projetos reconhecidos na raiz")
    commands.add_parser("doctor", parents=[common], help="autodiagnóstico do harness: instalação, arquivos e caminhos")
    initial_scan = commands.add_parser("scan", parents=[common], help="checagem das nove áreas documentais")
    initial_scan.add_argument("project")
    ctx = commands.add_parser("context", parents=[common], help="recorte de leitura para um foco/etapa; inclui scan")
    ctx.add_argument("project")
    ctx.add_argument("--focus", choices=FOCI, default="create")
    ctx.add_argument("--stage", choices=STAGES)
    ctx.add_argument("--event", choices=EVENTS, default="task", help="evento observado na conversa pelo agente; não concede aprovação")
    ctx.add_argument("--genre", choices=GENRES, help="gênero declarado; carrega o pacote de gênero correspondente")
    doc = commands.add_parser("template", parents=[common], help="imprime ou grava um rascunho de documento")
    doc.add_argument("stage", choices=STAGES)
    doc.add_argument("--project", required=True)
    doc.add_argument("--output", type=Path, help="sem output, imprime o rascunho sem escrever")
    plan = commands.add_parser("check-plan", parents=[common], help="valida a forma do contrato de reuso")
    plan.add_argument("plan", type=Path)
    run = commands.add_parser("verify", parents=[common], help="executa validadores escolhidos com recibo")
    run.add_argument("project")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--timeout", type=float, default=300)
    run.add_argument("--script", action="append", default=[])
    run.add_argument("--command", nargs=argparse.REMAINDER)
    rec = commands.add_parser("record", parents=[common], help="recibo de observação, orçamento medido ou decisão de marco")
    rec.add_argument("project")
    rec.add_argument("--kind", choices=tuple(RECORD_KINDS), required=True)
    rec.add_argument("--author", required=True, help="quem assina o registro")
    rec.add_argument("--note", required=True, help="fato observado ou decisão, antes da interpretação")
    rec.add_argument("--field", action="append", default=[], metavar="CHAVE=VALOR", help="campos do tipo; repetível")
    rec.add_argument("--attach", action="append", default=[], metavar="ARQUIVO", help="evidência existente (vídeo, log, captura); repetível")
    rec.add_argument("--output", type=Path, required=True)
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
    return parser


RECORD_KINDS = {
    "observation": {"required": ("scenario", "role"), "enum": {"role": ("human", "agent")}},
    "budget": {"required": ("metric", "value", "unit", "platform", "tool"), "enum": {}},
    "milestone": {"required": ("milestone", "decision", "declared_by", "role"), "enum": {"decision": ("declared", "denied", "deferred"), "role": ("human", "agent")}},
}


def parse_fields(pairs):
    fields = {}
    for pair in pairs:
        key, separator, value = pair.partition("=")
        if not separator or not key.strip():
            raise ValueError(f"campo precisa ter a forma chave=valor: {pair}")
        fields[key.strip()] = value.strip()
    return fields


def record(project, kind, author, note, fields, attachments, output):
    """Recibo de evidência declarada (observação, orçamento medido ou decisão de marco), ligado à versão do projeto."""
    if not project.is_dir():
        raise ValueError("projeto ausente")
    if kind not in RECORD_KINDS:
        raise ValueError("tipo de registro desconhecido")
    if not nonempty(author) or not nonempty(note):
        raise ValueError("author e note precisam de texto")
    spec = RECORD_KINDS[kind]
    missing = [key for key in spec["required"] if not nonempty(fields.get(key))]
    if missing:
        raise ValueError(f"{kind} exige campos: {', '.join(missing)}")
    for key, allowed in spec["enum"].items():
        if fields[key] not in allowed:
            raise ValueError(f"{key} deve ser um de: {', '.join(allowed)}")
    if kind == "budget":
        try:
            fields["value"] = float(fields["value"])
        except ValueError:
            raise ValueError("value precisa ser numérico") from None
    files = []
    for item in attachments:
        path = Path(item)
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"anexo inexistente ou symlink: {item}")
        data = path.read_bytes()
        files.append({"path": str(path.resolve()), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    if output.exists() or output.is_symlink():
        raise ValueError("destino de evidência existente; escolha um novo")
    report = {
        "schema_version": 1, "kind": kind, "project": str(project), "recorded_at": datetime.now(timezone.utc).isoformat(),
        "version": git_version(project), "author": author, "note": note, "fields": fields, "attachments": files,
        "status": "declared",
        "scope": "Registro declarado por quem assina; o harness não valida o conteúdo, não mede e não aprova. role=agent é avaliação do agente, não aprovação do usuário.",
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / "record.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    args = build_parser().parse_args()
    try:
        root = getattr(args, "root", ROOT).resolve()
        if args.action == "discover":
            emit(discover(root))
        elif args.action == "doctor":
            report = doctor(root)
            emit(report)
            return int(not report["ok"])
        elif args.action == "scan":
            emit(scan(resolve(args.project, root)))
        elif args.action == "context":
            emit(context(resolve(args.project, root), args.focus, args.stage, studies_root=default_studies_root(root), event=args.event, root=root, genre=args.genre))
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
        elif args.action == "record":
            emit(record(resolve(args.project, root), args.kind, args.author, args.note, parse_fields(args.field), args.attach, args.output.absolute()))
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
            report = verify(resolve(args.project, root), args.script, args.command, args.output.absolute(), args.timeout)
            emit(report)
            return int(report["technical_status"] != "passed")
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
