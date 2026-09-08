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
from datetime import datetime, timezone

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


ROOT = default_root()
STUDIES_ROOT = default_studies_root(ROOT)
FOCI = ("create", "mechanics", "lifecycle", "content", "visual", "network")
STAGES = ("brief", "mda", "gdd", "poc", "prd", "tdd", "vertical-slice", "mvp", "qa")
CAPABILITIES = ("pause", "reset", "seed", "observe", "act", "advance", "capture", "dispose")
SKIP = {"node_modules", "dist", "build", "docs", "framework", "squads", "public", "assets", "Assets", "Library", "Temp", "outputs"}
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
    declared = data.get("packageManager", "").split("@")[0]
    locks = {manager for file, manager in (("package-lock.json", "npm"), ("npm-shrinkwrap.json", "npm"), ("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lock", "bun"), ("bun.lockb", "bun")) if (project / file).exists()}
    manager = declared or (next(iter(locks)) if len(locks) == 1 else "npm" if not locks else None)
    if manager not in (None, "npm", "pnpm", "yarn", "bun"):
        manager = None
    return data.get("scripts", {}), manager


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


def context(project, focus, stage=None, studies_root=None):
    if stage is not None and stage not in STAGES:
        raise ValueError("etapa desconhecida")
    if project.exists() and not project.is_dir():
        raise ValueError("projeto precisa ser um diretório")
    scripts, manager = package_commands(project)
    instructions = [str(parent / "AGENTS.md") for parent in reversed((project, *project.parents)) if (parent / "AGENTS.md").is_file()]
    records = [str(project / name) for name in ("README.md", "production/brief.json", "production/state.json", "production/decisions.md", "production/qa.md", "DESIGN.md") if (project / name).is_file()]
    for name in (*STAGES, "game-design"):
        for relative in (f"production/{name}.md", f"docs/{name}.md", f"{name.upper()}.md"):
            path = project / relative
            if path.is_file() and str(path) not in records:
                records.append(str(path))
    references = [FRAMEWORK / "references/process.md", FRAMEWORK / "references/quality.md", FRAMEWORK / f"recipes/{focus}.md"]
    if stage or focus == "create":
        references.append(FRAMEWORK / "references/preproduction.md")
    if stage:
        references.append(FRAMEWORK / f"assets/templates/{stage}.md")
    studies = studies_for(focus, STUDIES_ROOT if studies_root is None else studies_root)
    return {
        "schema_version": 1, "project": str(project), "exists": project.is_dir(), "kind": identify(project),
        "focus": focus, "stage": stage, "instructions": instructions, "records": records,
        "read_next": [str(path) for path in references], "studies": studies,
        "source_index": str(FRAMEWORK / "references/sources.md"),
        "package_manager": manager,
        "scripts": {name: {"body": body, "argv": [manager, "run", name] if manager else None} for name, body in scripts.items()},
        "capabilities": mention_capabilities(project),
        "limits": [
            "Ponteiros não comprovam leitura; scripts declarados não comprovam execução.",
            "Inspecione os scripts antes de executá-los. Nenhum comando é executado por context.",
            "Sem packageManager ou lockfile, npm é apenas a convenção do executor de package.json.",
            "Consulte AGENTS.md mais específicos ao escolher os arquivos que serão alterados.",
            "studies lista catálogos do foco se existirem no irmão Games-Frameworks; ausência não é evidência negativa.",
            "capabilities.mentioned é só token em arquivo de inspeção. Não prova pause, reset, seed nem determinismo.",
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
    ctx = commands.add_parser("context")
    ctx.add_argument("project")
    ctx.add_argument("--focus", choices=FOCI, default="create")
    ctx.add_argument("--stage", choices=STAGES)
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
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if args.action == "discover":
            emit(discover(root))
        elif args.action == "context":
            emit(context(resolve(args.project, root), args.focus, args.stage, studies_root=default_studies_root(root)))
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
