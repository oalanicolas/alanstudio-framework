#!/usr/bin/env python3
"""Games harness: contexto sob demanda, contrato de reuso e execução com recibo."""
import argparse
import hashlib
from html import escape
import json
import math
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
    configured = os.environ.get("GAMES_WORKSPACE_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
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
    "create", "mechanics", "lifecycle", "content", "visual", "audio", "feel", "network", "architecture",
    "performance", "accessibility", "persistence", "release", "production",
)
STAGES = (
    "brief", "mda", "gdd", "poc", "prd", "tdd", "vertical-slice", "mvp", "qa", "release",
    "art-bible", "devlog", "audit", "aaa", "game-design", "production-plan", "milestone", "agents",
)
PRODUCTION_STAGES = ("production-plan", "milestone")
# Etapas que não são fase do ciclo: geram um documento de apoio pelo `template`.
SUPPORT_STAGES = ("agents",)
# Arquivos que assistentes de código leem como instrução persistente. AGENTS.md é o
# canônico deste harness; os demais entram porque o laboratório pode misturar hosts,
# e uma instrução que o agente não lê é memória perdida na próxima sessão.
INSTRUCTION_FILES = (
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules", ".cursor/rules",
    ".github/copilot-instructions.md", ".windsurfrules",
)
EVENTS = ("task", "direction-approved", "resume", "initialize")
REFERENCES = (
    "process", "quality", "preproduction", "project-audit", "game-design-system", "sources",
    "ambition", "aaa-checklist", "production-bar", "gates",
)
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
    ("provenance", "Origem de código e assets", r"\b(licenses?|licences?|licencas?|copying|authors|sources|proveniencia|provenance|origem de codigo e assets|creditos|credits|asset sources)\b"),
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
    "production": ("content_scale", "performance", "release", "state_trust"),
}
# A barra descreve onde o jogo está; um gate diz o que ainda não pode passar. Os
# dez já existiam como prosa em references/preproduction.md, uma linha "Pronto
# para…" por etapa, que nada lia e nada recusava — a mesma forma que a barra tinha
# antes do comando `bar`. Os critérios abaixo são extraídos dessas linhas, não
# inventados aqui, e um teste exige que cada gate continue tendo a sua.
#
# O terceiro campo de cada critério é `waivable`. Ele é falso só onde a prosa da
# etapa não deixa terceira opção — "prioridade não permite remover exigências
# explícitas do usuário", "não registre teste com pessoa quando houve somente
# simulação", "licença desconhecida bloqueia a entrega", e origem declarada ou
# ausência explícita, que já traz a própria saída. Nos demais, dispensar é decisão
# de quem assina, com motivo e autor, em vez de eu decidir por todo mundo o que é
# negociável.
#
# O quarto campo é `kind`, e vem de fora: Cooper separa `readiness` ("o trabalho
# está feito?", falhar devolve para a etapa anterior) de `must_meet` ("isto ainda
# vale o que custa?", falhar mata o escopo). Os dez gates nasceram todos readiness,
# e a pergunta de valor existia só como a saída `abandonar`, que dependia de
# alguém levantá-la. Os três `must_meet` abaixo a fazem: `close.decision` já estava
# na prosa do ciclo, e os dois de custo entram nos dois gates que comprometem
# produção — a procedência deles está em references/gates-research.md, §2.2.
# Um `must_meet` não é dispensável, porque um "No" decide sozinho e não há
# compensação por outro critério estar ótimo.
GATES = {
    "design": {
        "asks": "desenhar e experimentar",
        "stage": "brief",
        "readiness": "Pronto para desenhar/experimentar",
        "criteria": (
            ("match", "Uma partida curta pode ser descrita do início ao fim", True, "readiness"),
            ("feeling", "A sensação pretendida está escrita, não implícita", True, "readiness"),
            ("uncertainty", "A maior incerteza a aprender primeiro está nomeada", True, "readiness"),
            ("reference_origin", "Cada referência visual tem origem e autoridade declaradas, ou ausência explícita", False, "readiness"),
        ),
    },
    "test": {
        "asks": "testar a hipótese",
        "stage": "mda",
        "readiness": "Pronto para testar",
        "criteria": (
            ("chain", "Cada hipótese liga regra → comportamento → experiência", True, "readiness"),
            ("distinguishing", "Existe uma situação observável que distingue a hipótese da alternativa", True, "readiness"),
            ("refutation", "A observação capaz de contradizer a hipótese está definida", True, "readiness"),
        ),
    },
    "prototype": {
        "asks": "prototipar",
        "stage": "gdd",
        "readiness": "Pronto para prototipar",
        "criteria": (
            ("verbs", "O que o jogador faz, quais alternativas tem e o que acontece está descrito", True, "readiness"),
            ("end_and_restart", "Como a partida termina e reinicia está descrito", True, "readiness"),
            ("pillars", "Cada pilar resolve uma escolha concreta, não um adjetivo", True, "readiness"),
        ),
    },
    "close": {
        "asks": "encerrar o experimento",
        "stage": "poc",
        "readiness": "Pronto para encerrar",
        "criteria": (
            ("verdict", "O resultado distingue a hipótese, ou o motivo da inconclusão está escrito", True, "readiness"),
            ("conditions", "As condições da observação estão registradas", True, "readiness"),
            # A pergunta de valor que o ciclo já fazia num lugar só. Dispensá-la
            # seria dispensar a decisão, isto é, seguir por inércia.
            ("decision", "A decisão está registrada: continuar, ajustar ou abandonar", False, "must_meet"),
            ("effort_limit", "O limite de esforço foi definido antes do experimento", True, "readiness"),
        ),
    },
    "implement": {
        "asks": "implementar o recorte",
        "stage": "prd",
        "readiness": "Pronto para implementar o recorte",
        "criteria": (
            ("acceptance", "Cada requisito necessário tem condição, resultado esperado e método de verificação", True, "readiness"),
            ("dependencies", "Dependências e lacunas que podem mudar o escopo estão resolvidas ou delimitam um experimento", True, "readiness"),
            ("user_requirements", "Nenhuma exigência explícita do usuário foi removida por prioridade", False, "readiness"),
            ("worth_building", "O que custa construir o recorte está estimado, e o recorte ainda vale esse custo", False, "must_meet"),
        ),
    },
    "build": {
        "asks": "construir",
        "stage": "tdd",
        "readiness": "Pronto para construir",
        "criteria": (
            ("consumers", "Caminhos canônicos e consumidores afetados foram lidos", True, "readiness"),
            ("coverage", "As decisões cobrem os requisitos do recorte", True, "readiness"),
            ("risk_to_poc", "Risco sem prova virou PoC explícita", True, "readiness"),
        ),
    },
    "scale": {
        "asks": "ampliar a produção",
        "stage": "vertical-slice",
        "readiness": "Pronto para ampliar",
        "criteria": (
            ("repeatable", "O cenário é jogável e repetível", True, "readiness"),
            ("integrations", "As integrações foram verificadas com recibo", True, "readiness"),
            ("in_motion", "A comparação foi feita em movimento, não em quadro estático", True, "readiness"),
            ("regressions", "As regressões encontradas foram resolvidas", True, "readiness"),
            ("no_placeholder", "Nenhum placeholder está contado como acabamento", True, "readiness"),
            ("worth_scaling", "O que custa ampliar está estimado, e a fatia pronta justifica pagar esse custo", False, "must_meet"),
        ),
    },
    "evaluate": {
        "asks": "avaliar a entrega",
        "stage": "mvp",
        "readiness": "Pronto para avaliar a entrega",
        "criteria": (
            ("full_cycle", "O ciclo do jogo está completo, do início ao fim", True, "readiness"),
            ("essentials", "Os requisitos essenciais estão atendidos", True, "readiness"),
            ("access", "Existe acesso ao jogo para quem vai observar", True, "readiness"),
            ("observation", "O método de observação está definido", True, "readiness"),
        ),
    },
    "conclude": {
        "asks": "concluir o escopo",
        "stage": "qa",
        "readiness": "Pronto para concluir o escopo",
        "criteria": (
            ("evidence", "Cada critério aplicável tem evidência correspondente", True, "readiness"),
            ("retested", "Falhas relevantes foram resolvidas e retestadas", True, "readiness"),
            ("declared_gaps", "As lacunas restantes estão explícitas", True, "readiness"),
            ("human_vs_agent", "Teste com pessoa não está registrado onde houve só simulação ou avaliação do agente", False, "readiness"),
        ),
    },
    "deliver": {
        "asks": "entregar",
        "stage": "release",
        "readiness": "Pronto para entregar",
        "criteria": (
            ("runbook", "Outra pessoa constrói a partir do runbook", True, "readiness"),
            ("foreign_machine", "O artefato roda em máquina que não é a de desenvolvimento", True, "readiness"),
            ("save_migration", "Save migra da versão anterior", True, "readiness"),
            # A prosa é explícita: licença desconhecida bloqueia a entrega.
            ("licensing", "Nenhum recurso embarcado tem licença desconhecida", False, "readiness"),
            ("rollback", "Existe procedimento de reversão", True, "readiness"),
        ),
    },
}
# `out_of_scope` não é dispensa e existe para não ser confundida com ela: dispensar
# é deixar de cumprir o que incide, e um critério que nunca incidiu não tem o que
# dispensar. Contar os dois juntos inflaria a conta de dispensas justamente onde
# ela deveria doer. A forma vem dos XAGs, que decidem aplicabilidade com perguntas
# de escopo antes de cobrar qualquer coisa, e da TRC histórica, que marcava seção
# como "Applicable" — references/gates-research.md, §3.4 e §4.2.
GATE_STATES = ("met", "unmet", "waived", "out_of_scope")
GATE_KINDS = ("readiness", "must_meet")

STAGE_TIERS = {
    "brief": "prototype", "mda": "prototype", "poc": "prototype",
    "gdd": "playable", "prd": "playable", "tdd": "playable",
    "vertical-slice": "slice", "art-bible": "slice",
    "mvp": "shippable", "qa": "shippable", "release": "shippable",
    "game-design": "prototype", "aaa": "slice", "production-plan": "slice", "milestone": "shippable",
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


def normalize_text(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold()) if not unicodedata.combining(c)).replace("-", " ").replace("_", " ")


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def resolve(value, root=ROOT):
    return (root / value).resolve()


def instruction_files(project):
    """Instruções persistentes para agentes, da raiz mais externa à mais específica. Só localiza; não lê."""
    found = []
    for parent in reversed((project, *project.parents)):
        for name in INSTRUCTION_FILES:
            path = parent / name
            if path.is_file() or (name == ".cursor/rules" and path.is_dir() and any(path.iterdir())):
                found.append(str(path))
    return found


def git_summary(project):
    """Versão, sujeira e últimos assuntos do repositório que contém o projeto; None fora de um repositório."""
    def run(*args):
        try:
            result = subprocess.run(["git", "-C", str(project), *args], capture_output=True, text=True, check=False, timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            return ""
        return result.stdout.strip() if result.returncode == 0 else ""
    if run("rev-parse", "--is-inside-work-tree") != "true":
        return None
    dirty = [line for line in run("status", "--porcelain", "--", ".").splitlines() if line.strip()]
    return {
        "head": run("rev-parse", "HEAD") or None,
        "branch": run("rev-parse", "--abbrev-ref", "HEAD") or None,
        "dirty_paths": len(dirty),
        "recent": run("log", "-5", "--format=%h %s", "--", ".").splitlines(),
        "scope": "Estado do repositório na hora do comando; commits não provam que a mudança funciona nem que foi revisada.",
    }


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


# Um laboratório de trabalho já tem jogos, e é por isso que o primeiro movimento
# aqui é revisar o que existe. Caminho e tipo não bastam para isso: quatro jogos
# em estados muito diferentes saem iguais numa listagem, e quem abre o estúdio
# precisa saber onde o trabalho está antes de escolher um.
REVIEW_LIMIT = 48


def review(root, limit=REVIEW_LIMIT):
    projects = discover(root)
    reviewed = []
    for entry in projects[:limit]:
        path = Path(entry["project"])
        try:
            found = scan(path)
        except (OSError, ValueError) as error:
            reviewed.append(dict(entry, unreadable=str(error)))
            continue
        areas = found["areas"]
        located = [key for key, area in areas.items() if area["status"] == "candidate_found"]
        drafts = [key for key, area in areas.items() if area["status"] == "draft_only"]
        declaration = bar_declaration(path)
        # Fonte em rascunho não é passo registrado, pelo mesmo motivo que vale no
        # `next`: campo de template em branco não é trabalho interrompido.
        registered = [item for item in found["continuity_sources"] if item["status"] != "draft"]
        try:
            scripts = validators(project_commands(path)[0])
        except ValueError:
            scripts = []
        reviewed.append(dict(
            entry,
            areas_located=len(located),
            areas_total=len(areas),
            areas_draft=len(drafts),
            missing_areas=[key for key, area in areas.items() if area["status"] == "not_located"],
            continuity=f"{registered[0]['path']}:{registered[0]['line']}" if registered else None,
            bar_floor=declaration["floor"],
            bar_undeclared=len(declaration["undeclared"]),
            bar_problems=len(declaration["problems"]),
            validators=scripts,
        ))
    return {
        "schema_version": 1,
        "root": str(root),
        "project_count": len(projects),
        "reviewed": len(reviewed),
        "projects": reviewed,
        "limit": limit,
        "truncated": len(projects) > limit,
        # Ordenar por urgência exigiria julgar qual jogo importa mais, e nada aqui
        # observa isso. A ordem é a do disco, e a escolha continua sendo de quem lê.
        "order": "caminho, em ordem determinística; o harness não classifica os jogos por urgência",
        "scope": (
            "Conta documentos por localização e lê a declaração de degrau de cada projeto. Não executa jogo "
            "nenhum, não mede acabamento e não diz qual merece atenção primeiro. Área localizada é candidato "
            "por nome ou título, não conteúdo aprovado; degrau é o que o projeto afirma de si."
        ),
    }


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


GATE_ROW = re.compile(
    r"^\|\s*`([\w-]+)`\s*\|\s*`([\w-]+)`\s*\|\s*`(\w+)`\s*\|\s*(.*?)\s*\|\s*$"
)
GATE_SOURCES = ("README.md", "docs/qa.md", "docs/devlog.md", "docs/release.md", "docs/prd.md")


def gate_declaration(project):
    declared = {}
    problems = []
    sources = []
    for relative in GATE_SOURCES:
        path = project / relative
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        seen_here = False
        for number, line in enumerate(text.splitlines(), start=1):
            match = GATE_ROW.match(line)
            if not match:
                continue
            gate, criterion, state, note = match.groups()
            source = f"{relative}:{number}"
            known_gate = gate in GATES
            known_state = state in GATE_STATES
            # Mesmo filtro da barra: sem nenhuma das células reconhecível, a linha
            # não é da tabela de gates e não vira ruído no relatório.
            if not known_gate and not known_state:
                continue
            if not known_gate:
                problems.append({"source": source, "reason": "unknown_gate", "found": gate})
                continue
            keys = [item[0] for item in GATES[gate]["criteria"]]
            if criterion not in keys:
                problems.append({"source": source, "reason": "unknown_criterion", "gate": gate, "found": criterion})
                continue
            if not known_state:
                problems.append({"source": source, "reason": "unknown_state", "gate": gate, "found": state})
                continue
            waivable = dict((item[0], item[2]) for item in GATES[gate]["criteria"])[criterion]
            if state == "waived" and not waivable:
                problems.append({
                    "source": source, "reason": "not_waivable", "gate": gate, "found": criterion,
                })
                continue
            # Um critério que a prosa não deixa dispensar também não sai da conta
            # por escopo: seria a mesma remoção com outro nome.
            if state == "out_of_scope" and not waivable:
                problems.append({
                    "source": source, "reason": "always_applies", "gate": gate, "found": criterion,
                })
                continue
            # Dispensa sem motivo escrito é dispensa sem autor: o que sobra é um
            # critério apagado da lista, que é justamente o que um gate impede.
            if state == "waived" and not note:
                problems.append({"source": source, "reason": "waiver_without_reason", "gate": gate, "found": criterion})
                continue
            if state == "out_of_scope" and not note:
                problems.append({"source": source, "reason": "scope_without_reason", "gate": gate, "found": criterion})
                continue
            if state == "met" and not note:
                problems.append({"source": source, "reason": "met_without_evidence", "gate": gate, "found": criterion})
                continue
            previous = declared.setdefault(gate, {}).get(criterion)
            # Duas linhas discordantes não se resolvem por precedência, como na
            # barra: a mais fraca vale, e o conflito fica visível. `out_of_scope` é
            # a mais permissiva das quatro, porque tira o critério da conta em vez
            # de responder a ele, então qualquer linha que discorde dela prevalece.
            rank = {"unmet": 0, "waived": 1, "met": 2, "out_of_scope": 3}
            entry = {"state": state, "note": note or None, "source": source}
            if previous is None or rank[state] < rank[previous["state"]]:
                declared[gate][criterion] = entry
            if previous is not None and previous["state"] != state:
                problems.append({
                    "source": source, "reason": "conflicting_state", "gate": gate, "found": criterion,
                })
            seen_here = True
        if seen_here:
            sources.append(relative)
    return {"declared": declared, "problems": problems, "sources": sources}


def gate_reading(project, gate=None):
    declaration = gate_declaration(project)
    wanted = (gate,) if gate else tuple(GATES)
    gates = []
    for key in wanted:
        spec = GATES[key]
        rows = declaration["declared"].get(key, {})
        criteria = []
        for criterion, label, waivable, kind in spec["criteria"]:
            row = rows.get(criterion)
            criteria.append({
                "key": criterion,
                "criterion": label,
                "waivable": waivable,
                "kind": kind,
                "state": row["state"] if row else "undeclared",
                "evidence": row["note"] if row else None,
                "source": row["source"] if row else None,
            })
        pending = [item["key"] for item in criteria if item["state"] in ("undeclared", "unmet")]
        waived = [item["key"] for item in criteria if item["state"] == "waived"]
        gates.append({
            "key": key,
            "asks": spec["asks"],
            "stage": spec["stage"],
            "readiness": spec["readiness"],
            "criteria": criteria,
            "pending": pending,
            "waived": waived,
            "out_of_scope": [item["key"] for item in criteria if item["state"] == "out_of_scope"],
            # A pergunta de valor separada da pergunta de trabalho: pendência de
            # readiness devolve para a etapa anterior, pendência de must-meet é
            # candidata a abandono. Quem responde não é o mesmo, nem a resposta.
            "value_pending": [
                item["key"] for item in criteria
                if item["kind"] == "must_meet" and item["state"] in ("undeclared", "unmet")
            ],
            # Não é "passou". É o que a declaração do projeto sustenta hoje.
            "held_by_declaration": not pending,
        })
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "gates": gates,
        "problems": declaration["problems"],
        "sources": declaration["sources"],
        "granted": False,
        "guide": str(FRAMEWORK / "references/gates.md"),
        "rule": (
            "Um gate recusa avanço enquanto um critério estiver pendente. Passar, cortar escopo e abandonar "
            "são as três saídas legítimas — abandonar não é falha do gate, é uma das respostas dele. "
            "Critério de `readiness` pendente diz que falta trabalho; `must_meet` pendente pergunta se "
            "isto ainda vale o que custa, e é a essa pergunta que abandonar responde."
        ),
        "scope": (
            "Lê a declaração do próprio projeto e confere só a forma dela, relatando em `problems`: gate "
            "desconhecido, critério que não pertence ao gate, estado fora de met/unmet/waived/out_of_scope, "
            "dispensa ou saída de escopo de critério que a prosa não deixa dispensar, met/waived/out_of_scope "
            "sem nada escrito ao lado, e duas linhas discordantes. Não observa o jogo, não executa nada e "
            "**não concede passagem**: `held_by_declaration` diz que o projeto afirma cumprir, não que alguém "
            "conferiu."
        ),
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
    json_docs = {"brief.json", "state.json", "decisions.json", "sources.json", "licenses.json", "provenance.json", "package.json"}
    text_docs = {"license", "licence", "copying", "credits", "authors"}
    indexes, documents, links, statuses = [], {}, {}, {}
    deferred, non_current, continuity_sources, genre_mentions = [], [], [], []
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
        fence = None
        for number, line in enumerate(lines, 1):
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if marker:
                delimiter, suffix = marker.groups()
                if fence is None:
                    if delimiter[0] != "`" or "`" not in suffix:
                        fence = delimiter
                elif delimiter[0] == fence[0] and len(delimiter) >= len(fence) and not suffix.strip():
                    fence = None
                continue
            if fence is not None:
                continue
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
    local_instructions = [name for name in INSTRUCTION_FILES if (project / name).is_file() or (project / name).is_dir()] if project.is_dir() else []
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
        "agent_context": {
            "status": "found" if local_instructions else "not_located",
            "files": local_instructions,
            "scope": "Instruções persistentes para o agente na raiz do projeto. Não é uma das nove áreas; sem elas, cada sessão reaprende convenções. `template agents` gera um rascunho.",
        },
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
    references = [
        FRAMEWORK / "references/process.md", FRAMEWORK / "references/quality.md",
        FRAMEWORK / "references/production-bar.md", FRAMEWORK / f"recipes/{focus}.md",
    ]
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


def workspace_module(project, root=None):
    """Locate an optional workspace module without treating an empty checkout as a new game."""
    project = Path(project).resolve()
    if root is None:
        root = next((parent for parent in (project, *project.parents)
                     if (parent / "workspace.json").is_file()), default_root())
    root = Path(root).resolve()
    if not (root / "workspace.json").is_file():
        return None
    manifest = read_json(root / "workspace.json")
    if not isinstance(manifest, dict) or manifest.get("version") != 1 or not isinstance(manifest.get("modules"), list):
        raise ValueError("workspace.json precisa declarar version 1 e uma lista modules")
    for module in manifest["modules"]:
        if not isinstance(module, dict) or not all(isinstance(module.get(key), str) and module[key] for key in ("id", "path")):
            raise ValueError("Módulo precisa de id e path textuais")
        relative = PurePosixPath(module["path"])
        target = (root / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not target.is_relative_to(root):
            raise ValueError("Módulo fora do workspace")
        if target == project:
            return {
                "id": module["id"], "path": module["path"],
                "state": "present" if (target / ".git").exists() else "not_downloaded",
                "get_command": shlex.join(["python3", str(root / "framework/scripts/workspace.py"),
                                            "--root", str(root), "get", module["id"]]),
            }
    return None


def workspace_profile(root):
    """Read local context references; all reusable rules remain in this repository."""
    root = Path(root).resolve()
    config = root / "framework/config.json"
    result = {"root": str(root), "config": None, "context_files": [], "missing": []}
    if not config.is_file():
        return result
    data = read_json(config)
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("framework/config.json precisa declarar version 1")
    files = data.get("context_files", [])
    if not isinstance(files, list) or not all(isinstance(name, str) and name for name in files):
        raise ValueError("context_files precisa ser uma lista de caminhos")
    result["config"] = str(config)
    for name in files:
        path = (root / name).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Referência de personalização fora do workspace")
        collection = result["context_files"] if path.is_file() else result["missing"]
        if str(path) not in collection:
            collection.append(str(path))
    return result


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
    instructions = instruction_files(project)
    foundation = scan(project)
    module = workspace_module(project, root)
    module_pending = module is not None and module["state"] == "not_downloaded"
    if module_pending:
        foundation["audit"]["required"] = False
        foundation["audit"]["deferred_reason"] = "workspace_module_not_downloaded"
    records = [str(project / relative) for relative in foundation["read_first"]]
    initializing = event == "initialize"
    document_minimum = foundation["audit"]["required"] or event in ("direction-approved", "initialize") or stage == "audit"
    kind = identify(project)
    packs = select_packs(kind, genre, foundation["genre_mentions"])
    references = [str(path) for path in select_references(focus, stage, document_minimum)]
    recipe = str(FRAMEWORK / f"recipes/{focus}.md")
    for pack in (packs["genre"]["pack"], packs["platform"]["pack"]):  # inserção reversa: receita → plataforma → gênero
        if pack:
            references.insert(references.index(recipe) + 1 if recipe in references else len(references), pack)
    references = list(dict.fromkeys(references))
    profile = workspace_profile(root if root is not None else default_root())
    references.extend(path for path in profile["context_files"] if path not in references)
    if initializing and str(FRAMEWORK / "recipes/architecture.md") not in references:
        references.append(str(FRAMEWORK / "recipes/architecture.md"))
    studies = studies_for(focus, STUDIES_ROOT if studies_root is None else studies_root)
    return {
        "schema_version": 3, "project": str(project), "exists": project.is_dir(), "kind": kind,
        "workspace_module": module,
        "workspace": profile,
        "focus": focus, "stage": stage, "event": event, "instructions": instructions, "records": records,
        "read_next": references, "packs": packs, "studies": studies,
        "git": git_summary(project) if project.is_dir() else None,
        "source_index": str(FRAMEWORK / "references/sources.md"),
        "package_manager": manager,
        "metadata_issues": metadata_issues,
        "scripts": scripts,
        "capabilities": mention_capabilities(project), "foundation": foundation,
        "delivery_review": {
            "status": "pending_agent_review",
            "criteria": ["intent", "artifact", "evidence", "continuity"],
            "guide": str(FRAMEWORK / "references/delivery.md"),
            "before_close": "Confrontar pedido e aceite com artefatos, localizadores, prova e resposta final no QA/plano existente. Corrigir divergências; critério desconhecido não está atendido.",
            "limits": "Context não lê a conversa, executa a revisão ou certifica a entrega. Testes do harness não comprovam comportamento do agente.",
        },
        "production_bar": production_bar(focus, stage, project),
        "continuity": {
            "status": "sources_found" if foundation["continuity_sources"] else "not_located",
            "sources": [dict(item, path=str(project / item["path"])) for item in foundation["continuity_sources"]],
            "source_count": foundation["continuity_source_count"],
            "action": "resolve_and_continue" if event == "resume" else "record_and_present_next_step",
            "next_step": None, "executed": False,
            "prompt": {
                "policy": "generate_when_defined",
                "readiness": "agent_review_required",
                "required_inputs": ["project", "next_action", "scope", "acceptance", "canonical_source"],
                "text": None,
                "presentation": "Um prompt pronto para copiar, em linguagem comum, preenchido com o próximo recorte real; não exigir gauntlet, skill, comandos ou variáveis do usuário.",
                "budget": "Opcional, somente se informado na conversa; sem horas, concluir o recorte definido. Retomada preserva prazo já vigente.",
                "guide": str(FRAMEWORK / "references/gauntlet.md"),
            },
            "guide": str(FRAMEWORK / "references/process.md") + "#continuidade-e-retomada",
            "before_close": "Atualizar o registro canônico e dizer onde chegamos, uma próxima ação concreta, por que vem primeiro e qual evidência a conclui. Quando esse recorte estiver definido, gerar e apresentar automaticamente seu prompt de continuidade pronto para copiar; sem jargão, variáveis ou pedido de horas. Continuar trabalho já autorizado. Se o objetivo terminou, declarar conclusão sem inventar trabalho.",
            "on_resume": "Ler o registro e a conversa, conferir o estado real, resolver a próxima ação e executá-la dentro do escopo autorizado. Não repetir briefing, auditoria já válida ou pergunta genérica de permissão.",
            "scope": "Fontes são candidatos, não fila validada. O agente resolve next_step e a prontidão do prompt antes de responder; o comando não escolhe tarefa, gera prompt semântico, infere etapa concluída nem concede autorização a partir de documentos.",
        },
        "documentation": {
            "action": "obtain_workspace_module" if module_pending else "audit_and_document" if initializing else "document_minimum" if document_minimum else "maintain_affected_documents",
            "executed": False,
            "on_initialize": "Iniciar/inicializar o projeto, sem alvo operacional explícito, pede análise profunda e documentação: use --event initialize. Iniciar servidor, partida ou uma fase já definida segue esse alvo e a conversa; não decidir só pelo verbo.",
            "initialization": {
                "status": "pending_agent_audit",
                "notice": f"Vou iniciar a análise de {project.name}: levantar a implementação disponível, confrontar os documentos e organizar a base e o próximo passo com evidências.",
                "required_evidence": ["source_traces_and_consumers", "canonical_documents_or_explicit_gaps", "prioritized_findings", "next_action_with_ready_prompt_or_actual_blocker"],
                "not_sufficient": ["server_running", "http_ok", "tests_passed", "documents_found"],
                "guide": str(FRAMEWORK / "references/project-audit.md") + "#inicializar-o-projeto",
                "runtime_role": "Observar o jogo pode apoiar o diagnóstico; abrir navegador ou servidor não é a entrega da inicialização. Não alterar gameplay apenas por esse pedido.",
            } if initializing else None,
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
            "Inspecione os scripts antes de executá-los. context consulta o Git em modo de leitura, mas não executa o jogo nem seus validadores.",
            "Sem packageManager ou lockfile, npm é apenas a convenção do executor de package.json.",
            "Consulte as instruções mais específicas (AGENTS.md e equivalentes em instructions) ao escolher os arquivos que serão alterados; git.recent é histórico, não prova.",
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


def gauntlet(project, objective, hours=None, focus="create", output=None):
    if not nonempty(objective):
        raise ValueError("objetivo deve conter texto")
    if hours is not None and (isinstance(hours, bool) or not isinstance(hours, (int, float)) or not math.isfinite(hours) or hours <= 0):
        raise ValueError("horas devem ser um número finito maior que zero")
    if focus not in FOCI:
        raise ValueError("foco desconhecido")
    project = project.resolve()
    if project.exists() and not project.is_dir():
        raise ValueError("projeto deve ser um diretório")
    contract = {
        "schema_version": 1,
        "status": "prepared",
        "execution_started": False,
        "project": str(project),
        "objective": objective,
        "budget_hours": hours,
        "focus": focus,
        "skill": str(FRAMEWORK / "SKILL.md"),
        "guide": str(FRAMEWORK / "references/gauntlet.md"),
        "context_argv": shlex.split(harness_command("context", project, "--focus", focus, "--event", "resume")),
    }
    document = (FRAMEWORK / "assets/gauntlet.md").read_text(encoding="utf-8")
    document = document.replace("{{CONTRACT}}", json.dumps(contract, ensure_ascii=False, indent=2))
    if output is not None:
        if output.exists() or output.is_symlink():
            raise ValueError("documento existente; escolha um novo destino para o gauntlet")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as target:
            target.write(document)
    return document


# Todo comando que o harness sugere existe para ser copiado e colado. Caminho de
# projeto com espaço é comum — "Farol do Sul" é um nome de jogo, não um caso de
# borda — e sem citação o shell o parte em dois argumentos. Construir tudo por
# aqui é o que impede a próxima sugestão de nascer quebrada: `shlex.quote` só
# acrescenta aspas quando são necessárias, então flags e literais passam intactos.
def harness_command(*parts):
    script = shlex.quote(str(FRAMEWORK / "scripts/game.py"))
    workspace = ["--root", str(default_root())]
    return " ".join(["python3", script, *(shlex.quote(str(part)) for part in (*workspace, *parts))])


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


def substitute_document(path, pairs):
    text = path.read_text(encoding="utf-8")
    if path.suffix.casefold() == ".json":
        counted = {}

        def replace(value):
            if isinstance(value, str):
                result, counts = substitute(value, pairs)
                for old, count in counts.items():
                    counted[old] = counted.get(old, 0) + count
                return result
            if isinstance(value, list):
                return [replace(item) for item in value]
            if isinstance(value, dict):
                return {replace(key): replace(item) for key, item in value.items()}
            return value

        return json.dumps(replace(json.loads(text)), ensure_ascii=False, indent=2) + "\n", counted
    if path.suffix.casefold() in (".html", ".htm"):
        pairs = [(old, escape(new, quote=True)) for old, new in pairs]
    return substitute(text, pairs)


def init(destination, starter, title=None, documents=True):
    module = workspace_module(destination)
    if module and module["state"] == "not_downloaded":
        raise ValueError(f"Projeto é um módulo opcional existente. Use {module['get_command']}")
    available = starters()
    if starter not in available:
        raise ValueError(f"starter desconhecido: {starter}; disponíveis: {', '.join(available) or 'nenhum'}")
    if destination.is_symlink() or destination.is_file():
        raise ValueError("destino existente; escolha um caminho novo")
    if destination.is_dir() and any(destination.iterdir()):
        raise ValueError("destino existente e não vazio; adapte o projeto atual em vez de sobrescrevê-lo")
    destination = destination.resolve()
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
    rendered = {}
    # Prepare e valide as substituições antes de criar qualquer arquivo.
    for relative, pairs in plan.items():
        text, counted = substitute_document(source / relative, pairs)
        missed = [old for old, _ in pairs if not counted.get(old)]
        if missed:
            raise ValueError(f"{starter}/{STARTER_MANIFEST}: {relative} não contém {missed!r}")
        rendered[relative] = text
        applied[relative] = counted
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
        if relative in rendered:
            with target.open("x", encoding="utf-8") as document:
                document.write(rendered[relative])
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
        if not (destination / "AGENTS.md").exists():
            template("agents", destination, destination / "AGENTS.md")
            drafts.append("AGENTS.md")
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
    missing_references = [name for name in REFERENCES if not (FRAMEWORK / f"references/{name}.md").is_file()]
    missing_packs = [
        name for name in (
            *(f"platforms/{name}" for name in sorted(set(PLATFORM_PACKS.values()))),
            *(f"genres/{name}" for name in GENRES), "README",
        ) if not (FRAMEWORK / f"packs/{name}.md").is_file()
    ]
    complete = not (missing_recipes or missing_templates or missing_references or missing_packs)
    add(
        "framework", True, complete,
        f"receitas ({len(FOCI)}), templates ({len(STAGES)}), referências ({len(REFERENCES)}) e pacotes "
        f"({len(set(PLATFORM_PACKS.values()))} plataformas, {len(GENRES)} gêneros) completos"
        if complete
        else f"faltando receitas={missing_recipes} templates={missing_templates} referências={missing_references} pacotes={missing_packs}",
        "Um foco sem receita, uma etapa sem template ou um kind sem pacote quebra `context`.",
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
    studies = default_studies_root(root)
    add(
        "studies", False, studies.is_dir(), str(studies) if studies.is_dir() else f"ausente: {studies}",
        "Sem Games-Frameworks (ou GAMES_FRAMEWORKS_ROOT), `studies` vem vazio; ausência não é evidência negativa.",
    )
    # Num laboratório de trabalho os jogos já existem, e contá-los sem nomeá-los
    # obriga quem chega a adivinhar os caminhos que este comando acabou de ler.
    named = ", ".join(Path(item["project"]).name for item in projects[:6])
    add(
        "root", True, root.is_dir(),
        f"{root} · {len(projects)} projeto(s) reconhecido(s)"
        + (f": {named}" if named else "")
        + (", …" if len(projects) > 6 else "")
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
    repository = git_summary(root) if root.is_dir() and git["path"] else None
    add(
        "repository", False, repository is not None,
        f"{repository['branch']} · {repository['dirty_paths']} caminho(s) alterado(s)" if repository else "raiz fora de um repositório git",
        "Sem git, `record` e `verify` gravam version.head nulo e a memória entre sessões fica só nos documentos.",
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
        "genres": list(GENRES),
        "known_markers": [marker for marker, _ in ENGINE_MARKERS],
        "scope": (
            "Presença e versão de ferramentas, presença dos arquivos deste repositório e conteúdo dos atalhos da skill no host. "
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

    module = payload.get("workspace_module")
    if module and module["state"] == "not_downloaded":
        propose(
            f"Baixar o módulo existente {module['id']} para continuar o jogo",
            "O workspace já declara este jogo; a pasta vazia é um módulo opcional ainda não baixado.",
            "O módulo está disponível na versão registrada e seu contexto pode ser lido, sem recriar o jogo.",
            [module["get_command"]],
            "workspace_module.not_downloaded",
        )
    elif not payload["exists"]:
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
    # Sem instrução persistente, cada sessão reaprende convenções e o agente repete
    # os mesmos erros de contexto. Vem depois das áreas e da continuidade porque é
    # delas que o AGENTS.md fala; antes dos validadores porque é ali que se diz como rodá-los.
    if payload["exists"] and foundation["agent_context"]["status"] == "not_located":
        propose(
            "Escrever as instruções para o agente na raiz do projeto (AGENTS.md)",
            "Sem AGENTS.md, convenções, comandos e limites ficam só na conversa e se perdem na próxima sessão; é a causa mais barata de retrabalho com IA.",
            "AGENTS.md cita como executar e verificar, os documentos canônicos, o que não mudar e onde registrar continuidade.",
            [harness_command("template", "agents", "--project", project, "--output", project / "AGENTS.md")],
            "agent_context.not_located",
        )
    if scripts:
        propose(
            f"Executar os validadores do projeto com recibo ({', '.join(scripts[:4])})",
            "Comando declarado não é comando executado; sem recibo não há evidência técnica para nenhuma decisão.",
            "Existe uma pasta de evidência com recibo e log de cada comando escolhido.",
            [harness_command("verify", project, "--script", scripts[0], "--output", "CAMINHO_NOVO")],
            "scripts",
        )
    # Um gate só está em jogo quando o projeto o declara: ninguém pede uma
    # permissão que não mencionou, e listar os dez num projeto que declarou um
    # transformaria a recusa em ruído.
    gates = gate_declaration(project)
    if gates["problems"]:
        propose(
            "Corrigir a forma da declaração de gate em: "
            + ", ".join(f"{item['source']} ({item['reason']})" for item in gates["problems"][:4]),
            "Linha malformada não entra na leitura, e o critério que ela pretendia declarar continua pendente. "
            "Dispensa sem motivo escrito é critério apagado da lista, que é justamente o que um gate impede.",
            "Cada linha nomeia um dos dez gates, um critério dele, um estado entre "
            "met/unmet/waived/out_of_scope e o que sustenta o estado.",
            [harness_command("gate", project)],
            "gates.problems",
        )
    else:
        reading = gate_reading(project)
        live = [item for item in reading["gates"] if item["key"] in gates["declared"]]
        blocked = next((item for item in live if item["pending"]), None)
        if blocked:
            criteria = dict((item["key"], item) for item in blocked["criteria"])
            # A pergunta de valor vem antes da de trabalho quando as duas estão
            # abertas no mesmo gate: terminar o que talvez não devesse existir é o
            # desperdício que um gate existe para interromper.
            if blocked["value_pending"]:
                first = blocked["value_pending"][0]
                propose(
                    f"Responder `{first}` no gate `{blocked['key']}`: {criteria[first]['criterion']}",
                    "Este critério não pergunta se o trabalho está feito, e sim se ainda vale o que custa. "
                    "Pendência aqui não se resolve trabalhando mais, e ele não é dispensável: as saídas são "
                    "passar com a estimativa escrita, cortar escopo até caber, ou abandonar.",
                    "O custo está estimado por escrito, e a linha do critério diz qual das três saídas foi "
                    "escolhida, com autor.",
                    [harness_command("gate", project, "--gate", blocked["key"])],
                    "gates.value",
                )
            else:
                first = blocked["pending"][0]
                propose(
                    f"Resolver o critério `{first}` do gate `{blocked['key']}`: {criteria[first]['criterion']}",
                    f"O gate `{blocked['key']}` pede {blocked['asks']} e recusa enquanto "
                    f"{len(blocked['pending'])} critério(s) estiver(em) pendente(s). "
                    + ("Este não é dispensável: a etapa não deixa terceira opção."
                       if not criteria[first]["waivable"] else
                       "Cortar escopo e abandonar também são saídas legítimas deste gate."),
                    "A linha do critério sai de `undeclared`/`unmet` com o que sustenta o estado ao lado, "
                    "ou é dispensada com motivo e autor.",
                    [harness_command("gate", project, "--gate", blocked["key"])],
                    "gates.pending",
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
            "agent_context": foundation["agent_context"]["status"],
            "scripts": scripts,
            "package_manager": payload["package_manager"],
            "production_bar_dimensions": dimensions,
            "production_bar_floor": declaration["floor"],
            "production_bar_undeclared": declaration["undeclared"],
            "production_bar_problems": declaration["problems"],
            "gates_declared": sorted(gates["declared"]),
            "gates_problems": gates["problems"],
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
    declared, manager = project_commands(project)
    commands = []
    for name in scripts:
        if not manager or name not in declared or declared[name]["argv"] is None or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.:-]*", name):
            raise ValueError(f"script ausente/inválido ou gerenciador ambíguo: {name}")
        commands.append(list(declared[name]["argv"]))
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
    # `--root` é aceito antes e depois do subcomando. A documentação sempre o
    # escreveu depois, e argparse só o aceitava antes: cada exemplo com `--root`
    # falhava com código 2. O parser comum abaixo herda a opção em todo
    # subcomando, com default suprimido para não sobrescrever o valor global.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=argparse.SUPPRESS, help="raiz para descobrir projetos e resolver caminhos")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="raiz para descobrir projetos e resolver caminhos")
    commands = parser.add_subparsers(dest="action", required=True)
    gate_cmd = commands.add_parser(
        "gate", parents=[common],
        help="critérios que o projeto declara cumprir para pedir a próxima permissão",
    )
    gate_cmd.add_argument("project")
    gate_cmd.add_argument("--gate", choices=sorted(GATES), help="um gate só, em vez dos dez")

    discover_cmd = commands.add_parser("discover", parents=[common])
    discover_cmd.add_argument(
        "--plain", action="store_true",
        help="só caminho e tipo, sem ler os documentos de cada projeto",
    )
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
    ctx.add_argument("--genre", choices=GENRES, help="gênero declarado na conversa; carrega o pacote de gênero após o de plataforma")
    doc = commands.add_parser("template", parents=[common])
    doc.add_argument("stage", choices=STAGES)
    doc.add_argument("--project", required=True)
    doc.add_argument("--output", type=Path, help="sem output, imprime o rascunho sem escrever")
    prompts = commands.add_parser("gauntlet", parents=[common], help="preparar prompts de continuidade; não inicia execução")
    prompts.add_argument("project")
    prompts.add_argument("--objective", required=True)
    prompts.add_argument("--hours", type=float, help="teto opcional informado pelo usuário; sem horas, trabalhar até concluir o recorte")
    prompts.add_argument("--focus", choices=FOCI, default="create")
    prompts.add_argument("--output", type=Path, help="arquivo novo; sem output, imprime os prompts")
    plan = commands.add_parser("check-plan", parents=[common])
    plan.add_argument("plan", type=Path)
    run = commands.add_parser("verify", parents=[common])
    run.add_argument("project")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--timeout", type=float, default=300)
    run.add_argument("--script", action="append", default=[])
    run.add_argument("--proves", action="append", default=[], choices=CAPABILITIES, help="capacidade que esta execução se propõe a demonstrar; a afirmação é de quem executa")
    run.add_argument("--command", nargs=argparse.REMAINDER)
    rec = commands.add_parser("record", parents=[common], help="recibo de observação, orçamento medido ou decisão de marco, ligado ao HEAD do projeto")
    rec.add_argument("project")
    rec.add_argument("--kind", required=True, choices=sorted(RECORD_KINDS))
    rec.add_argument("--author", required=True)
    rec.add_argument("--note", required=True)
    rec.add_argument("--field", action="append", default=[], help="chave=valor; campos obrigatórios variam por tipo")
    rec.add_argument("--attach", action="append", default=[], help="arquivo anexado por caminho; o recibo guarda o SHA-256")
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
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        os.environ["GAMES_WORKSPACE_ROOT"] = str(root)
        if args.action == "discover":
            emit(discover(root) if args.plain else review(root))
        elif args.action == "doctor":
            report = doctor(root)
            emit(report)
            return int(not report["ready"])
        elif args.action == "init":
            if not args.starter:
                raise ValueError("nenhum starter disponível neste repositório")
            emit(init((root / args.project).absolute(), args.starter, args.title, not args.no_docs))
        elif args.action == "next":
            emit(next_step(resolve(args.project, root), args.focus, studies_root=default_studies_root(root)))
        elif args.action == "scan":
            emit(scan(resolve(args.project, root)))
        elif args.action == "bar":
            emit(bar_reading(resolve(args.project, root)))
        elif args.action == "gate":
            emit(gate_reading(resolve(args.project, root), args.gate))
        elif args.action == "context":
            emit(context(resolve(args.project, root), args.focus, args.stage, studies_root=default_studies_root(root), event=args.event, root=root, genre=args.genre))
        elif args.action == "template":
            document = template(args.stage, resolve(args.project, root), args.output)
            if args.output:
                emit({"document": str(args.output.resolve()), "status": "draft", "scope": "Template inicial; decisões, revisão e prova continuam pendentes."})
            else:
                print(document, end="")
        elif args.action == "gauntlet":
            document = gauntlet(resolve(args.project, root), args.objective, args.hours, args.focus, args.output)
            if args.output:
                emit({"document": str(args.output.resolve()), "status": "prepared", "execution_started": False, "scope": "Prompts preparados; execução, controle do prazo e retomada pertencem à sessão do agente."})
            else:
                print(document, end="")
        elif args.action == "check-plan":
            errors = check_plan(read_json(args.plan), root)
            emit({"contract_valid": not errors, "errors": errors, "scope": "Estrutura e existência dos candidatos; busca, adequação e qualidade exigem revisão."})
            return int(bool(errors))
        elif args.action == "record":
            emit(record(resolve(args.project, root), args.kind, args.author, args.note, parse_fields(args.field), args.attach, args.output.absolute()))
        elif args.action == "sfx":
            if (root / "workspace.json").is_file() and not (sfx_catalog.catalog_dir(root) / "catalog.json").is_file():
                raise ValueError("Acervo sfx não baixado. Execute "
                                 "python3 framework/scripts/workspace.py get sfx antes de consultar sons.")
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
