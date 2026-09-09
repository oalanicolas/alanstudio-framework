#!/usr/bin/env python3
"""Games harness: contexto sob demanda, contrato de reuso e execução com recibo."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
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
FOCI = ("create", "mechanics", "lifecycle", "content", "visual", "audio", "feel", "network", "architecture")
STAGES = ("brief", "mda", "gdd", "poc", "prd", "tdd", "vertical-slice", "mvp", "qa", "art-bible", "devlog", "audit")
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
    references = [FRAMEWORK / "references/process.md", FRAMEWORK / "references/quality.md", FRAMEWORK / f"recipes/{focus}.md"]
    if stage == "tdd" and focus != "architecture":
        references.append(FRAMEWORK / "recipes/architecture.md")
    if stage or focus == "create":
        references.append(FRAMEWORK / "references/preproduction.md")
    if focus in ("create", "visual", "audio", "feel") or stage == "art-bible":
        references.append(FRAMEWORK / "references/game-design-system.md")
    if focus in ("create", "audio", "feel") or stage in ("brief", "vertical-slice"):
        references.append(FRAMEWORK / "references/ambition.md")
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
            "Feel e áudio são focos próprios (`--focus feel`, `--focus audio`). Sem observação em movimento, experience_status permanece not_assessed; scaffold não é vertical slice.",
            "“AAA” neste harness é piso de acabamento da slice, não tier de publisher. Sem feel sincronizado, pacing e repeatability, não use o adjetivo.",
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
    report.update(technical_status="passed" if all(item["exit_code"] == 0 for item in report["commands"]) else "failed", finished_at=datetime.now(timezone.utc).isoformat())
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="raiz para descobrir projetos e resolver caminhos")
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("discover")
    initial_scan = commands.add_parser("scan")
    initial_scan.add_argument("project")
    ctx = commands.add_parser("context")
    ctx.add_argument("project")
    ctx.add_argument("--focus", choices=FOCI, default="create")
    ctx.add_argument("--stage", choices=STAGES)
    ctx.add_argument("--event", choices=EVENTS, default="task", help="evento observado na conversa pelo agente; não concede aprovação")
    doc = commands.add_parser("template")
    doc.add_argument("stage", choices=STAGES)
    doc.add_argument("--project", required=True)
    doc.add_argument("--output", type=Path, help="sem output, imprime o rascunho sem escrever")
    plan = commands.add_parser("check-plan")
    plan.add_argument("plan", type=Path)
    run = commands.add_parser("verify")
    run.add_argument("project")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--timeout", type=float, default=300)
    run.add_argument("--script", action="append", default=[])
    run.add_argument("--command", nargs=argparse.REMAINDER)
    sfx = commands.add_parser("sfx", help="catálogo compartilhado de efeitos sonoros")
    sfx_cmd = sfx.add_subparsers(dest="sfx_action")
    sfx_cmd.add_parser("summary")
    sfx_search = sfx_cmd.add_parser("search")
    sfx_search.add_argument("query")
    sfx_search.add_argument("--limit", type=int, default=40)
    sfx_copy = sfx_cmd.add_parser("copy")
    sfx_copy.add_argument("id")
    sfx_copy.add_argument("--to", required=True)
    sfx_copy.add_argument("--sources")
    sfx_cmd.add_parser("verify")
    sfx_serve = sfx_cmd.add_parser("serve")
    sfx_serve.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if args.action == "discover":
            emit(discover(root))
        elif args.action == "scan":
            emit(scan(resolve(args.project, root)))
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
            report = verify(resolve(args.project, root), args.script, args.command, args.output.absolute(), args.timeout)
            emit(report)
            return int(report["technical_status"] != "passed")
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
