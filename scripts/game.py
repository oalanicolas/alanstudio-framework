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
EVENTS = ("task", "direction-approved", "resume")
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
# Conformidade com o que o próprio projeto declarou. Não são os critérios de
# `preproduction.md` — esses já estão nos gates — e não são limiares importados.
# A lista vem de references/observable-criteria-research.md §7, o único conjunto
# que a pesquisa chamou de "não precisa de autoridade externa". Um teste exige
# que cada rótulo continue sem dígito e que a frase-âncora ainda exista no
# levantamento. Cada item pende do gate em que a pergunta passa a doer.
CRAFT_CHECKS = {
    "canvas_scale": {
        "gate": "build",
        "label": "A resolução de apresentação está declarada, e a escala tela sobre canvas é inteira ou o fallback está escrito",
        "anchor": "resolução de canvas está declarada",
    },
    "forgiveness": {
        "gate": "build",
        "label": "Cada janela de perdão tem constante nomeada, num só lugar, com unidade declarada",
        "anchor": "janela de perdão tem constante nomeada",
    },
    "palette": {
        "gate": "scale",
        "label": "Cada cor usada consta da paleta declarada",
        "anchor": "cor usada consta da paleta declarada",
    },
    "style_factor": {
        "gate": "scale",
        "label": "Todo asset do mesmo mundo de estilo usa o mesmo fator inteiro, e nenhum asset aparece em dois mundos",
        "anchor": "mesmo fator inteiro",
    },
    "percentile_def": {
        "gate": "scale",
        "label": "O percentil de tempo de quadro está definido pela definição, não pelo apelido",
        "anchor": "Percentil está declarado por definição",
    },
    "budget_delta": {
        "gate": "scale",
        "label": "Tempo de quadro por cena está registrado por build e comparado com o anterior",
        "anchor": "comparados com o build anterior",
    },
    "playtest_stop": {
        "gate": "evaluate",
        "label": "A rodada de playtest tem regra de parada declarada, em vez de conta de participantes",
        "anchor": "regra de parada declarada",
    },
    "playtest_finding": {
        "gate": "evaluate",
        "label": "Cada achado de playtest nomeia problema, evidência, hipótese e medição",
        "anchor": "problema, a evidência, a hipótese e a medição",
    },
    "evidence_kind": {
        "gate": "conclude",
        "label": "Cada evidência diz se o lastro é log de comando ou observação de pessoa",
        "anchor": "log de comando",
    },
}

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
# O ciclo fresco pede rascunho só no que ainda é decisão em aberto. Art-bible
# vigente do starter não entra: direção já escrita não é atrito de template.
FRESH_DRAFTS = ("brief", "gdd", "mda", "tdd", "devlog", "qa")
INIT_TEXT_SUFFIXES = {".md", ".txt", ".html", ".css", ".js", ".mjs", ".json", ".svg"}
# Marcador que o `init` deixa nos templates. Um documento com ele não é
# decisão vigente — nem art-bible, nem release, nem brief.
DRAFT_MARKERS = re.compile(r"\{\{|\[preencher|status[^\n]{0,30}(rascunho|draft)", re.IGNORECASE)
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
        origins = origins_reading(path)
        roles = roles_reading(path, root)
        feel_report = feel_reading(path)
        access_report = access_reading(path)
        persist_report = save_reading(path)
        perf_report = budget_reading(path)
        art_report = art_reading(path)
        content_report = content_reading(path)
        ship_report = ship_reading(path)
        playtest_report = playtest_reading(path)
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
            origins_embedded=len(origins["embedded"]),
            origins_undeclared=len(origins["undeclared"]),
            audio_roles=len(roles["roles"]),
            audio_roles_empty=len(roles["empty"]),
            feel_constants=len(feel_report["constants"]),
            feel_observations=len(feel_report["observations"]),
            access_declared=access_report["declared"],
            save_unversioned=persist_report["unversioned"],
            performance_unbudgeted=perf_report["unbudgeted"],
            art_declared=art_report["declared"],
            content_files=len(content_report["files"]),
            content_inline=content_report["inline"],
            ship_unpacked=ship_report["unpacked"],
            playtest_expected=playtest_report["expected"],
            playtest_structured=playtest_report["structured"],
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


CRAFT_ROW = re.compile(r"^\|\s*`([\w-]+)`\s*\|\s*`(\w+)`\s*\|\s*(.*?)\s*\|\s*$")
CRAFT_SOURCES = GATE_SOURCES


def craft_declaration(project):
    declared = {}
    problems = []
    sources = []
    for relative in CRAFT_SOURCES:
        path = project / relative
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        seen_here = False
        for number, line in enumerate(text.splitlines(), start=1):
            match = CRAFT_ROW.match(line)
            if not match:
                continue
            check, state, note = match.groups()
            source = f"{relative}:{number}"
            known_check = check in CRAFT_CHECKS
            known_state = state in GATE_STATES
            if not known_check and not known_state:
                continue
            if not known_check:
                problems.append({"source": source, "reason": "unknown_check", "found": check})
                continue
            if not known_state:
                problems.append({
                    "source": source, "reason": "unknown_state",
                    "gate": CRAFT_CHECKS[check]["gate"], "found": state,
                })
                continue
            if state in ("waived", "out_of_scope", "met") and not note:
                reason = {
                    "waived": "waiver_without_reason",
                    "out_of_scope": "scope_without_reason",
                    "met": "met_without_evidence",
                }[state]
                problems.append({
                    "source": source, "reason": reason,
                    "gate": CRAFT_CHECKS[check]["gate"], "found": check,
                })
                continue
            previous = declared.get(check)
            rank = {"unmet": 0, "waived": 1, "met": 2, "out_of_scope": 3}
            entry = {"state": state, "note": note or None, "source": source}
            if previous is None or rank[state] < rank[previous["state"]]:
                declared[check] = entry
            if previous is not None and previous["state"] != state:
                problems.append({
                    "source": source, "reason": "conflicting_state",
                    "gate": CRAFT_CHECKS[check]["gate"], "found": check,
                })
            seen_here = True
        if seen_here:
            sources.append(relative)
    return {"declared": declared, "problems": problems, "sources": sources}


def craft_reading(project, gate=None):
    declaration = craft_declaration(project)
    wanted = tuple(
        key for key, spec in CRAFT_CHECKS.items()
        if gate is None or spec["gate"] == gate
    )
    checks = []
    for key in wanted:
        spec = CRAFT_CHECKS[key]
        row = declaration["declared"].get(key)
        checks.append({
            "key": key,
            "check": spec["label"],
            "gate": spec["gate"],
            "state": row["state"] if row else "undeclared",
            "evidence": row["note"] if row else None,
            "source": row["source"] if row else None,
        })
    pending = [item["key"] for item in checks if item["state"] in ("undeclared", "unmet")]
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "checks": checks,
        "pending": pending,
        "problems": declaration["problems"],
        "sources": declaration["sources"],
        "granted": False,
        "observed": False,
        "guide": str(FRAMEWORK / "references/observable-criteria-research.md"),
        "rule": (
            "Checklist de ofício pergunta se o projeto corresponde ao que ele mesmo "
            "declarou. Não importa limiar externo: paleta, constante de perdão, "
            "definição de percentil, regra de parada. Um dígito aqui seria a escada "
            "afirmando, para este jogo, o que ninguém verificou."
        ),
        "scope": (
            "Lê a declaração do próprio projeto e confere só a forma. Não observa o "
            "jogo, não mede contraste nem tempo de quadro e **não concede passagem**. "
            "`observed` é sempre falso: tabela bem formada e otimista sai intacta."
        ),
    }


# Papéis de áudio: o starter declara SOUNDS e, neste recorte, já traz
# arquivo por papel. Mixagem AAA não é pasta cheia — é cada papel do
# verbo ter arquivo ou silêncio deliberado (papel removido). O harness
# só vê declaração e arquivo no disco. Não ouve, não aprova estética e
# não confunde arquivo presente com mixagem boa.
ROLE_FOLDERS = ("public/sfx", "assets/sfx", "sfx", "audio", "public/audio")
ROLE_EXTENSIONS = {".wav", ".ogg", ".mp3", ".flac", ".m4a", ".webm"}
SOUNDS_OPEN = re.compile(r"(?:export\s+)?const\s+SOUNDS\s*=\s*\{")
ROLE_OBJECT = re.compile(r"^([A-Za-z_][\w]*)\s*:\s*\{")
ROLE_CODE_SUFFIXES = {".js", ".mjs", ".ts"}
ROLE_MANIFESTS = ("sounds.json", "audio-roles.json", "docs/audio-roles.json")
ROLE_WALK_SKIP = {
    "node_modules", "dist", "build", ".git", "__pycache__", "coverage",
    "library", "temp", ".venv", "venv", "target",
}


def _role_names_from_manifest(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(data, list):
        return [item for item in data if isinstance(item, str) and item.strip()]
    if not isinstance(data, dict):
        return []
    listed = data.get("roles")
    if isinstance(listed, list):
        return [item for item in listed if isinstance(item, str) and item.strip()]
    return [
        key for key, value in data.items()
        if key != "schema_version" and isinstance(value, (dict, str, bool, int))
    ]


def _role_names_from_code(text):
    start = SOUNDS_OPEN.search(text)
    if not start:
        return []
    names = []
    for line in text[start.end():].splitlines():
        stripped = line.strip()
        if stripped.startswith("}"):
            break
        match = ROLE_OBJECT.match(stripped)
        if match:
            names.append(match.group(1))
    return names


def declared_sound_roles(project, max_files=80, max_bytes=64000):
    found = []
    sources = []
    seen = set()

    def add(names, source):
        added = False
        for name in names:
            if name in seen:
                continue
            seen.add(name)
            found.append(name)
            added = True
        if added:
            sources.append(source)

    for relative in ROLE_MANIFESTS:
        path = project / relative
        if not path.is_file() or path.is_symlink():
            continue
        add(_role_names_from_manifest(path), relative)
    pending = [(project, 0)] if project.is_dir() else []
    inspected = 0
    while pending and inspected < max_files:
        directory, depth = pending.pop(0)
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError:
            continue
        for path in entries:
            if inspected >= max_files:
                break
            if path.name.startswith(".") or path.name in ROLE_WALK_SKIP:
                continue
            if path.is_symlink():
                continue
            if path.is_dir():
                if depth >= 4:
                    continue
                pending.append((path, depth + 1))
                continue
            if path.suffix.casefold() not in ROLE_CODE_SUFFIXES:
                continue
            inspected += 1
            try:
                if path.stat().st_size > max_bytes:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            names = _role_names_from_code(text)
            if names:
                add(names, path.relative_to(project).as_posix())
    return found, sources


def role_files(project, role):
    present = []
    for folder in ROLE_FOLDERS:
        directory = project / folder
        if not directory.is_dir() or directory.is_symlink():
            continue
        try:
            entries = directory.iterdir()
        except OSError:
            continue
        for path in entries:
            if path.is_symlink() or not path.is_file():
                continue
            if path.stem == role and path.suffix.casefold() in ROLE_EXTENSIONS:
                present.append(f"{folder}/{path.name}")
    return present


def roles_reading(project, root=None):
    project = Path(project)
    names, sources = declared_sound_roles(project)
    roles = []
    for name in names:
        files = role_files(project, name)
        roles.append({
            "id": name,
            "files": files,
            "state": "present" if files else "empty",
        })
    empty = [item["id"] for item in roles if item["state"] == "empty"]
    catalog = sfx_catalog.catalog_dir(root)
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "roles": roles,
        "empty": empty,
        "sources": sources,
        "catalog_exists": (catalog / "catalog.json").is_file(),
        "heard": False,
        "approved": False,
        "guide": str(FRAMEWORK / "recipes/audio.md"),
        "rule": (
            "Papel declarado sem arquivo é lacuna do verbo, não silêncio deliberado. "
            "Silêncio deliberado é o papel ausente da declaração."
        ),
        "scope": (
            "Lê `const SOUNDS` e manifestos de papéis, e cruza com arquivos em "
            "public/sfx e equivalentes. Não toca o som, não valida mixagem e não "
            "aprova estética. `heard` e `approved` são sempre falsos: arquivo "
            "presente não é mixagem ouvida."
        ),
    }


def roles_fill(project, root=None, apply=False):
    project = Path(project)
    reading = roles_reading(project, root)
    suggestions = []
    copied = []
    for role in reading["empty"]:
        match = None
        if reading["catalog_exists"]:
            try:
                found = sfx_catalog.search_catalog(role, root, limit=1)
            except ValueError:
                found = {"matches": []}
            if found["matches"]:
                match = {
                    "id": found["matches"][0]["id"],
                    "title": found["matches"][0]["title"],
                    "src": found["matches"][0]["src"],
                }
        item = {"role": role, "query": role, "match": match, "copied": False}
        if apply and match:
            result = sfx_catalog.copy_entry(
                match["id"], project / "public" / "sfx", root, as_name=role,
            )
            item["copied"] = True
            item["file"] = Path(result["copied"]).relative_to(project).as_posix()
            copied.append(role)
        suggestions.append(item)
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "empty": reading["empty"],
        "catalog_exists": reading["catalog_exists"],
        "suggestions": suggestions,
        "applied": bool(apply),
        "copied": copied,
        "heard": False,
        "approved": False,
        "guide": str(FRAMEWORK / "recipes/audio.md"),
        "rule": (
            "Primeiro resultado da busca não é o som certo e não é mixagem "
            "ouvida. `--apply` copia bytes e recibo; não toca e não aprova."
        ),
        "scope": (
            "Para cada papel vazio, busca o id no acervo shared/sfx e, com "
            "`--apply`, copia para public/sfx com o nome do papel. Sem "
            "acervo, a sugestão vem vazia. `heard` é sempre falso."
        ),
    }


# Feel: o starter nomeia perdão, graça e hitstop no CONFIG. Até aqui o harness
# só via a tabela de ofício, não as constantes. A pergunta é estreita — o
# projeto declara janelas de feel, e alguém registrou uma observação no disco?
# O harness não joga e não atribui peso.
CONFIG_OPEN = re.compile(r"(?:export\s+)?const\s+CONFIG\s*=\s*\{")
CONFIG_NESTED = re.compile(r"^([A-Za-z_][\w]*)\s*:\s*\{")
CONFIG_LEAF = re.compile(r"^([A-Za-z_][\w]*)\s*:\s*(-?[\d.]+)\s*,?\s*(?://\s*(.*))?")
FEEL_KEY = re.compile(
    r"(buffer|invuln|pad|reach|lock|hitstop|shake|squash|punch|grace|forgiv|cooldown|recovery|dashticks|flash|telegraph)",
    re.IGNORECASE,
)
FEEL_NOTE = re.compile(r"(perd[aã]o|gra[cç]a|contato|peso|feel|juice)", re.IGNORECASE)


def _feel_constants_from_code(text):
    start = CONFIG_OPEN.search(text)
    if not start:
        return []
    constants = []
    stack = []
    depth = 1
    for line in text[start.end():].splitlines():
        stripped = line.strip()
        opens = stripped.count("{")
        closes = stripped.count("}")
        nested = CONFIG_NESTED.match(stripped)
        leaf = CONFIG_LEAF.match(stripped)
        if nested:
            stack.append(nested.group(1))
            if closes >= opens and stack:
                stack.pop()
        elif leaf and stack:
            name, value, note = leaf.group(1), leaf.group(2), (leaf.group(3) or "").strip()
            if stack[0] == "feel" or FEEL_KEY.search(name) or FEEL_NOTE.search(note):
                constants.append({
                    "key": ".".join([*stack, name]),
                    "declared": value,
                    "note": note or None,
                })
        elif stripped.startswith("}") and stack:
            stack.pop()
        depth += opens - closes
        if depth <= 0:
            break
    return constants


def declared_feel_constants(project, max_files=80, max_bytes=64000):
    found = []
    sources = []
    seen = set()
    pending = [(project, 0)] if project.is_dir() else []
    inspected = 0
    while pending and inspected < max_files:
        directory, depth = pending.pop(0)
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError:
            continue
        for path in entries:
            if inspected >= max_files:
                break
            if path.name.startswith(".") or path.name in ROLE_WALK_SKIP:
                continue
            if path.is_symlink():
                continue
            if path.is_dir():
                if depth >= 4:
                    continue
                pending.append((path, depth + 1))
                continue
            if path.suffix.casefold() not in ROLE_CODE_SUFFIXES:
                continue
            inspected += 1
            try:
                if path.stat().st_size > max_bytes:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            constants = _feel_constants_from_code(text)
            if not constants:
                continue
            relative = path.relative_to(project).as_posix()
            for item in constants:
                if item["key"] in seen:
                    continue
                seen.add(item["key"])
                found.append(dict(item, source=relative))
            sources.append(relative)
    return found, sources


def observation_receipts(project, max_files=80):
    found = []
    pending = [(project, 0)] if project.is_dir() else []
    inspected = 0
    while pending and inspected < max_files:
        directory, depth = pending.pop(0)
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError:
            continue
        for path in entries:
            if inspected >= max_files:
                break
            if path.name.startswith(".") or path.name in ROLE_WALK_SKIP:
                continue
            if path.is_symlink():
                continue
            if path.is_dir():
                if depth >= 4:
                    continue
                pending.append((path, depth + 1))
                continue
            if path.name != "record.json":
                continue
            inspected += 1
            try:
                data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            except (OSError, json.JSONDecodeError):
                continue
            if not isinstance(data, dict) or data.get("kind") != "observation":
                continue
            found.append({
                "path": path.relative_to(project).as_posix(),
                "author": data.get("author"),
                "note": data.get("note"),
            })
    return found


def feel_reading(project):
    project = Path(project)
    constants, sources = declared_feel_constants(project)
    observations = observation_receipts(project)
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "constants": constants,
        "sources": sources,
        "observations": observations,
        "unobserved": bool(constants) and not observations,
        "felt": False,
        "guide": str(FRAMEWORK / "recipes/feel.md"),
        "rule": (
            "Constante nomeada não é peso percebido. Recibo de observação no "
            "projeto é o que o harness consegue ver; ele não joga."
        ),
        "scope": (
            "Lê `const CONFIG` (perdão, graça, hitstop, shake, squash, punch) e "
            "`record.json` com kind=observation. Não executa o jogo, não mede "
            "latência e não atribui degrau. `felt` é sempre falso: tabela de "
            "constantes e recibo otimista saem intactos."
        ),
    }


SURFACE_SUFFIXES = {".js", ".mjs", ".ts", ".html", ".css"}
A11Y_OPTIONS = {
    "high_contrast": re.compile(r"highContrast|high-contrast|prefersHighContrast|prefers-contrast"),
    "reduced_motion": re.compile(r"reducedMotion|reduced-motion|prefersReducedMotion"),
    "captions": re.compile(r"\bcaptions\b|captionLimit|\blegendas?\b"),
    "remap": re.compile(r"\bbindings\b|remap|rebind"),
    "ui_scale": re.compile(r"uiScale|ui-scale|interfaceScale"),
    "one_hand": re.compile(r"ONE_HAND_BINDINGS|oneHand|one-hand|umaMao|uma-mao"),
    "assist": re.compile(r"\bassist\b|assistMode|assistencia|assistência"),
}
PERSIST_USE = re.compile(
    r"localStorage|sessionStorage|indexedDB|saveProgress|loadProgress|PROGRESS_KEY|SETTINGS_KEY"
)
PERSIST_VERSION = re.compile(r"PROGRESS_SCHEMA|SETTINGS_SCHEMA|SAVE_VERSION|function migrate\b|\bmigrate\s*\(")
BUDGET_FILES = ("tools/budget.mjs", "tools/budget.js", "tools/budget.py")


def walk_project_files(project, suffixes, max_files=80, max_bytes=64000):
    pending = [(project, 0)] if project.is_dir() else []
    inspected = 0
    while pending and inspected < max_files:
        directory, depth = pending.pop(0)
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError:
            continue
        for path in entries:
            if inspected >= max_files:
                return
            if path.name.startswith(".") or path.name in ROLE_WALK_SKIP:
                continue
            if path.is_symlink():
                continue
            if path.is_dir():
                if depth < 4:
                    pending.append((path, depth + 1))
                continue
            if path.suffix.casefold() not in suffixes:
                continue
            inspected += 1
            try:
                if path.stat().st_size > max_bytes:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            yield path.relative_to(project).as_posix(), text


def access_reading(project):
    project = Path(project)
    found = {key: [] for key in A11Y_OPTIONS}
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        for key, pattern in A11Y_OPTIONS.items():
            if pattern.search(text):
                found[key].append(relative)
    options = [key for key, sources in found.items() if sources]
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "options": [
            {"key": key, "sources": found[key][:4]}
            for key in A11Y_OPTIONS if found[key]
        ],
        "missing": [key for key in A11Y_OPTIONS if not found[key]],
        "declared": bool(options),
        "verified": False,
        "guide": str(FRAMEWORK / "recipes/accessibility.md"),
        "rule": (
            "Opção declarada no código não é opção observada. Uma chave sem "
            "consumidor também não é alcance."
        ),
        "scope": (
            "Procura highContrast, reducedMotion, captions, remapeamento, "
            "uiScale, preset de uma mão e assistência no código. Não mede "
            "contraste, não joga com o modo ativo e não aprova alcance. "
            "`verified` é sempre falso."
        ),
    }


def save_reading(project):
    project = Path(project)
    used, versioned, sources = [], [], []
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES | {".py"}):
        if PERSIST_USE.search(text):
            used.append(relative)
        if PERSIST_VERSION.search(text):
            versioned.append(relative)
        if PERSIST_USE.search(text) or PERSIST_VERSION.search(text):
            sources.append(relative)
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "used": bool(used),
        "versioned": bool(versioned),
        "unversioned": bool(used) and not versioned,
        "sources": sources[:8],
        "trusted": False,
        "guide": str(FRAMEWORK / "recipes/persistence.md"),
        "rule": (
            "Uso de armazenamento sem versão e sem migração é contrato sem data. "
            "O harness não abre o save e não confirma escrita."
        ),
        "scope": (
            "Procura localStorage/saveProgress e PROGRESS_SCHEMA/migrate. Não "
            "executa migração, não interrompe a aba e não chama o save de "
            "atômico. `trusted` é sempre falso."
        ),
    }


def budget_receipts(project):
    found = []
    for relative, text in walk_project_files(project, {".json"}):
        if not relative.endswith("record.json"):
            continue
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and data.get("kind") == "budget":
            found.append(relative)
    return found


def budget_reading(project):
    project = Path(project)
    try:
        scripts, _ = project_commands(project)
    except (OSError, ValueError):
        scripts = {}
    named = [
        name for name in scripts
        if name == "budget" or name.startswith("budget:") or name.startswith("budget-")
        or name == "bench" or name.startswith("bench:")
    ]
    files = [name for name in BUDGET_FILES if (project / name).is_file() and not (project / name).is_symlink()]
    receipts = budget_receipts(project)
    expected = bool(scripts) or (project / "Cargo.toml").is_file()
    declared = bool(named or files or receipts)
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "expected": expected,
        "scripts": named,
        "files": files,
        "receipts": receipts,
        "declared": declared,
        "unbudgeted": expected and not declared,
        "measured": False,
        "guide": str(FRAMEWORK / "recipes/performance.md"),
        "rule": (
            "Script de orçamento não é medição no dispositivo alvo. Sem artefato "
            "que meça, não existe ‘rápido o suficiente’."
        ),
        "scope": (
            "Procura script `budget`/`bench`, tools/budget.* e record kind=budget. "
            "Não executa o orçamento e não compara com build anterior. "
            "`measured` é sempre falso."
        ),
    }


# Direção de arte, conteúdo em escala e o passo de empacotar: o starter já
# declara paleta, admite conteúdo no código e serve sem export. Até aqui o
# harness só via a tabela da barra. Os três leitores abaixo perguntam o que
# o disco tem — não se a paleta é consistente, se o conteúdo basta ou se
# alguém recebeu um build.
PALETTES_OPEN = re.compile(r"(?:export\s+)?const\s+PALETTES?\s*=\s*\{")
PALETTE_KEY = re.compile(r"^([A-Za-z_][\w]*)\s*:\s*\{")
ART_MANIFESTS = (
    "palettes.json", "tokens.json", "art-tokens.json", "design-tokens.json",
    "docs/palettes.json", "docs/tokens.json",
    "data/palettes.json", "data/tokens.json",
)
ART_BIBLE = "docs/art-bible.md"
CONTENT_DIRS = ("data", "content", "levels", "maps", "tables")
CONTENT_SUFFIXES = {".json", ".ldtk", ".tmx", ".csv", ".ink"}
CONTENT_LOOSE_SUFFIXES = {".ldtk", ".tmx", ".ink"}
SHIP_WORDS = ("build", "export", "dist", "package", "release")
SHIP_CI = (".gitlab-ci.yml", ".circleci/config.yml", "azure-pipelines.yml")
SHIP_RELEASE = "docs/release.md"
SHIP_VERSION = "dist/VERSION.json"


def optional_text(value):
    return value if isinstance(value, str) and value else None


def ship_artifact(project):
    path = Path(project) / SHIP_VERSION
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return {"path": SHIP_VERSION, "readable": False}
    if not isinstance(data, dict):
        return {"path": SHIP_VERSION, "readable": False}
    return {
        "path": SHIP_VERSION,
        "readable": True,
        "name": optional_text(data.get("name")),
        "version": optional_text(data.get("version")),
        "git_head": optional_text(data.get("git_head")),
    }


def document_is_current(path):
    if not path.is_file() or path.is_symlink():
        return False
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return not DRAFT_MARKERS.search(text)


def _palette_names_from_code(text):
    start = PALETTES_OPEN.search(text)
    if not start:
        return None
    names = []
    depth = 1
    for line in text[start.end():].splitlines():
        stripped = line.strip()
        match = PALETTE_KEY.match(stripped)
        # Só a chave no nível da paleta. Objeto numa linha dentro de `normal`
        # (`glow: { color: "#fff" }`) não vira uma paleta nova.
        if match and depth == 1:
            names.append(match.group(1))
        depth += stripped.count("{") - stripped.count("}")
        if depth <= 0:
            break
    return names


def _palette_names_from_manifest(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(data, dict):
        palettes = data.get("palettes")
        if isinstance(palettes, dict):
            return [key for key in palettes if isinstance(key, str)]
        return [key for key in data if key != "schema_version" and isinstance(key, str)]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, str) and item.strip()]
    return []


def art_reading(project):
    project = Path(project)
    palettes = []
    sources = []
    found_const = False
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        names = _palette_names_from_code(text)
        if names is None:
            continue
        found_const = True
        sources.append(relative)
        for name in names:
            if name not in {item["key"] for item in palettes}:
                palettes.append({"key": name, "source": relative})
    manifests = []
    for relative in ART_MANIFESTS:
        path = project / relative
        if not path.is_file() or path.is_symlink():
            continue
        names = _palette_names_from_manifest(path)
        manifests.append(relative)
        sources.append(relative)
        for name in names:
            if name not in {item["key"] for item in palettes}:
                palettes.append({"key": name, "source": relative})
    bible = project / ART_BIBLE
    bible_present = bible.is_file() and not bible.is_symlink()
    bible_current = document_is_current(bible)
    declared = bool(found_const or manifests or bible_current)
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "palettes": palettes,
        "manifests": manifests,
        "sources": sources[:8],
        "bible": ART_BIBLE if bible_present else None,
        "bible_current": bible_current,
        "bible_draft": bible_present and not bible_current,
        "declared": declared,
        "missing": not declared,
        "consistent": False,
        "guide": str(FRAMEWORK / "recipes/visual.md"),
        "rule": (
            "Paleta no código ou art-bible vigente é direção declarada, não "
            "direção consistente. Moodboard e rascunho do `init` não contam."
        ),
        "scope": (
            "Procura `const PALETTES`, tokens.json, data/palettes.json e docs/art-bible.md sem "
            "marcador de rascunho. Não compara silhueta, não mede contraste "
            "e não aprova estilo. `consistent` é sempre falso."
        ),
    }


def content_files(project):
    found = []
    seen = set()

    def add(relative):
        if relative not in seen:
            seen.add(relative)
            found.append(relative)

    for folder in CONTENT_DIRS:
        root = project / folder
        if not root.is_dir() or root.is_symlink():
            continue
        pending = [(root, 0)]
        while pending:
            directory, depth = pending.pop(0)
            try:
                entries = sorted(directory.iterdir(), key=lambda item: item.name)
            except OSError:
                continue
            for path in entries:
                if path.name.startswith(".") or path.name in ROLE_WALK_SKIP:
                    continue
                if path.is_symlink():
                    continue
                if path.is_dir():
                    if depth < 3:
                        pending.append((path, depth + 1))
                    continue
                if path.suffix.casefold() in CONTENT_SUFFIXES:
                    add(path.relative_to(project).as_posix())
    for relative, _ in walk_project_files(project, CONTENT_LOOSE_SUFFIXES):
        add(relative)
    return found


def content_reading(project):
    project = Path(project)
    files = content_files(project)
    kind = identify(project) if project.is_dir() else None
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "kind": kind,
        "files": files[:24],
        "external": bool(files),
        "inline": bool(kind) and not files,
        "enough": False,
        "guide": str(FRAMEWORK / "recipes/content.md"),
        "rule": (
            "Conteúdo no código não escala. Arquivo em data/levels não é "
            "volume suficiente nem consumidor comprovado."
        ),
        "scope": (
            "Procura .json/.csv em data/, content/, levels/, maps/, tables/ e "
            ".ldtk/.tmx/.ink em qualquer pasta do projeto. Não carrega o "
            "formato e não conta itens. `enough` é sempre falso."
        ),
    }


def ship_ci(project):
    found = []
    workflows = project / ".github" / "workflows"
    if workflows.is_dir() and not workflows.is_symlink():
        try:
            entries = sorted(workflows.iterdir(), key=lambda item: item.name)
        except OSError:
            entries = []
        for path in entries:
            if path.is_symlink() or not path.is_file():
                continue
            if path.suffix.casefold() in {".yml", ".yaml"}:
                found.append(path.relative_to(project).as_posix())
    for relative in SHIP_CI:
        path = project / relative
        if path.is_file() and not path.is_symlink():
            found.append(relative)
    return found


def ship_reading(project):
    project = Path(project)
    try:
        scripts, _ = project_commands(project)
    except (OSError, ValueError):
        scripts = {}
    named = []
    for name in scripts:
        for word in SHIP_WORDS:
            if name == word or name.startswith(f"{word}:") or name.startswith(f"{word}-"):
                if name not in named:
                    named.append(name)
    ci = ship_ci(project)
    release = project / SHIP_RELEASE
    release_current = document_is_current(release)
    artifact = ship_artifact(project)
    expected = (project / "package.json").is_file() or (project / "Cargo.toml").is_file()
    declared = bool(named or ci or release_current)
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "expected": expected,
        "scripts": named,
        "ci": ci,
        "release": SHIP_RELEASE if release.is_file() and not release.is_symlink() else None,
        "release_current": release_current,
        "artifact": artifact,
        "declared": declared,
        "unpacked": expected and not declared,
        "shipped": False,
        "guide": str(FRAMEWORK / "recipes/release.md"),
        "rule": (
            "Script de build não é artefato que outra pessoa executou. HTML "
            "estático sem manifesto já é o artefato; manifesto sem passo de "
            "empacotar é o que este leitor nomeia."
        ),
        "scope": (
            "Procura script build/export/dist/package/release, docs/release.md "
            "vigente e CI. Se dist/VERSION.json existe, relata nome e versão. "
            "Não executa o export, não instala o artefato e não autoriza "
            "publicar. `shipped` é sempre falso."
        ),
    }


# Playtest com métricas: a tabela de ofício já pede problema, evidência,
# hipótese e medição. Até aqui o harness só via se o projeto declarava o
# checklist. Uma observação solta ("o dash não tem peso") não é achado.
# O leitor abaixo pergunta se a forma está no disco — não se alguém jogou.
FINDING_FIELDS = re.compile(
    r"(?is)(?:^|\n)\s*(?:[-*]|\d+\.)?\s*\*?\*?(?:problema|problem)\*?\*?\s*[:—]"
    r".{2,400}?"
    r"(?:^|\n)\s*(?:[-*]|\d+\.)?\s*\*?\*?(?:evid[eê]ncia|evidence)\*?\*?\s*[:—]"
    r".{2,400}?"
    r"(?:^|\n)\s*(?:[-*]|\d+\.)?\s*\*?\*?(?:hip[oó]tese|hypothesis)\*?\*?\s*[:—]"
    r".{2,400}?"
    r"(?:^|\n)\s*(?:[-*]|\d+\.)?\s*\*?\*?(?:medi[cç][aã]o|measurement)\*?\*?\s*[:—]"
)
FINDING_TABLE = re.compile(
    r"(?i)\|\s*(?:problema|problem)\s*\|\s*(?:evid[eê]ncia|evidence)\s*\|\s*"
    r"(?:hip[oó]tese|hypothesis)\s*\|\s*(?:medi[cç][aã]o|measurement)\s*\|"
)
FINDING_FIELD_KEYS = {
    "problem": {"problem", "problema"},
    "evidence": {"evidence", "evidencia"},
    "hypothesis": {"hypothesis", "hipotese"},
    "measurement": {"measurement", "medicao", "metrica"},
}


def fold_key(value):
    return "".join(
        char for char in unicodedata.normalize("NFKD", str(value).casefold())
        if not unicodedata.combining(char)
    )


def fields_have_finding(fields):
    if not isinstance(fields, dict):
        return False
    present = {fold_key(key) for key, value in fields.items() if nonempty(str(value or ""))}
    return all(names & present for names in FINDING_FIELD_KEYS.values())


def playtest_findings(project):
    found = []
    seen = set()

    def add(relative):
        if relative not in seen:
            seen.add(relative)
            found.append(relative)

    for relative, text in walk_project_files(project, {".md", ".txt"}):
        if FINDING_TABLE.search(text) or FINDING_FIELDS.search(text):
            add(relative)
    for item in observation_receipts(project):
        path = project / item["path"]
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        fields = data.get("fields") or {}
        blob = "\n".join(
            str(value) for value in (data.get("note"), *fields.values()) if value
        )
        if fields_have_finding(fields) or FINDING_TABLE.search(blob) or FINDING_FIELDS.search(blob):
            add(item["path"])
    return found


LAST_RUN = "docs/playtest/last-run.json"
INVITE = "docs/playtest/invite.md"
INIT_COPY_SKIP = {"dist", "node_modules", ".git"}


def last_run_path(project):
    path = Path(project) / LAST_RUN
    if path.is_file() and not path.is_symlink():
        return LAST_RUN
    return None


def attach_run_candidate(project, fields=None, source=None):
    project = Path(project)
    path = Path(source) if source else project / LAST_RUN
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"sem partida no disco: {path.as_posix()}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"partida ilegível: {path.as_posix()}") from error
    if not isinstance(data, dict):
        raise ValueError(f"partida ilegível: {path.as_posix()}")
    run = data["run"] if isinstance(data.get("run"), dict) else data
    payload = dict(fields or {})
    payload["run"] = json.dumps(run, ensure_ascii=False, separators=(",", ":"))
    curve = data.get("curve")
    if isinstance(curve, dict):
        payload["curve"] = json.dumps(curve, ensure_ascii=False, separators=(",", ":"))
    return payload, path


def playtest_reading(project):
    project = Path(project)
    observations = observation_receipts(project)
    findings = playtest_findings(project)
    qa = project / "docs/qa.md"
    qa_current = document_is_current(qa)
    expected = bool(observations) or qa_current
    structured = bool(findings)
    candidate = last_run_path(project)
    invite = invite_path(project)
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "observations": [item["path"] for item in observations],
        "findings": findings,
        "candidate": candidate,
        "invite": invite,
        "qa_current": qa_current,
        "expected": expected,
        "structured": structured,
        "unstructured": expected and not structured,
        "observed": False,
        "outsider": False,
        "guide": str(FRAMEWORK / "recipes/feel.md"),
        "rule": (
            "Recibo de observação sem problema, evidência, hipótese e medição "
            "é impressão. Os quatro no disco não são playtest observado. "
            "last-run.json é candidato, não causa. Convite no disco não é "
            "alguém de fora."
        ),
        "scope": (
            "Procura os quatro campos num documento ou num record de "
            "observação, e se docs/qa.md deixou de ser rascunho. Relata "
            f"`{LAST_RUN}` e `{INVITE}` quando existem. Não assiste a sessão, não conta "
            "jogadores e não atribui causa. `observed` e `outsider` são sempre falsos."
        ),
    }


def invite_path(project):
    path = Path(project) / INVITE
    if path.is_file() and not path.is_symlink():
        return INVITE
    return None


def invite_playtest(project):
    project = Path(project)
    if not project.is_dir() or project.is_symlink():
        raise ValueError("projeto inexistente")
    path = project / INVITE
    created = not path.exists()
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError(f"convite inválido: {INVITE}")
    if created:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(invite_page(project), encoding="utf-8")
    reading = playtest_reading(project)
    return {
        "schema_version": 1,
        "project": str(project),
        "path": INVITE,
        "created": created,
        "observed": False,
        "outsider": False,
        "reading": reading,
        "scope": (
            "Escreve a página para quem nunca viu o jogo e aponta "
            "`/?invite=1`, onde a tabela some. O serve anuncia a URL "
            "da rede se a máquina tiver outro endereço IPv4. Não ensina "
            "o verbo, não assiste e não sobe pacing. outsider continua falso."
        ),
    }


def invite_page(project):
    project = Path(project)
    try:
        scripts, manager = project_commands(project)
    except (OSError, ValueError):
        scripts, manager = {}, None
    play = play_command(project, scripts, manager) or f"cd {shlex.quote(str(project))} && npm run serve"
    return (
        "# Convite — quem nunca viu o jogo\n"
        "\n"
        "Esta página não é playtest observado. `observed` e `outsider`\n"
        "continuam falsos até alguém que **não fez** o jogo jogar e\n"
        "escrever o achado noutro arquivo.\n"
        "\n"
        "## Abrir\n"
        "\n"
        "```\n"
        f"{play}\n"
        "```\n"
        "\n"
        "## Superfície\n"
        "\n"
        "No navegador, abra `/?invite=1`. A tabela de comandos some.\n"
        "Quem fez o jogo fica em `/`. O serve anuncia localhost e, se a\n"
        "máquina tiver outro endereço IPv4, a URL da rede. Compartilhar\n"
        "essa URL não é alguém de fora.\n"
        "\n"
        "## Instrução\n"
        "\n"
        "Jogue uma partida. Quem fez o jogo não ensina o verbo e não\n"
        "fica atrás da cadeira.\n"
        "\n"
        "## Depois\n"
        "\n"
        "Grave o achado em `docs/playtest/` com os quatro nomes que o\n"
        "harness já sabe ler — sem preenchê-los aqui, senão o arquivo\n"
        "finge forma. Quem escreveu precisa ser quem jogou.\n"
        "\n"
        "Convite no disco não sobe `pacing` e não conta jogador.\n"
    )


# `scan` lê documentos e, de propósito, não entra em textures/fonts/models/videos.
# É exatamente aí que mora o asset embarcado. O gate `deliver.licensing` recusa
# dispensa e, até este comando, ninguém lia o disco: uma linha otimista fechava
# a tabela. Aqui a pergunta é outra e mais estreita — o arquivo tem recibo de
# origem? — e a resposta negativa não é "licença inválida". Validar licença
# exigiria titular, texto e jurisdição, e nada disso cabe num walk.
EMBEDDED_SUFFIXES = {
    ".wav", ".ogg", ".mp3", ".flac", ".m4a", ".aac",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".ico",
    ".ttf", ".otf", ".woff", ".woff2",
    ".mp4", ".webm", ".mov",
    ".glb", ".gltf", ".fbx", ".obj",
}
ORIGIN_SKIP = {
    "node_modules", "dist", "build", ".git", "__pycache__", "evidence", "outputs",
    "library", "temp", "coverage", ".venv", "venv", "archives", "archive",
}
ORIGIN_RECEIPTS = {
    "sources.json", "licenses.json", "credits.md", "credits.txt", "licence",
    "license", "copying", "authors",
}
ORIGIN_ROW = re.compile(r"`([^`]+)`")
ORIGIN_LINK = re.compile(r"\[[^\]]+\]\((?:<([^>\n]+)>|([^\s)]+))")


def origins_reading(project, max_entries=2000):
    project = Path(project).resolve()
    embedded, receipts, problems = [], [], []
    mentioned = set()
    pending = [(project, 0)] if project.is_dir() else []
    seen = 0
    stopped = False

    def remember(name):
        text = str(name).replace("\\", "/").strip().lstrip("./")
        if text:
            mentioned.add(text)
            mentioned.add(Path(text).name)

    def ingest_json(path, relative):
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            problems.append({"source": relative, "reason": "unreadable_receipt"})
            return
        records = data.get("files") if isinstance(data, dict) else data
        if not isinstance(records, list):
            problems.append({"source": relative, "reason": "receipt_without_files"})
            return
        for record in records:
            if not isinstance(record, dict):
                continue
            for key in ("src", "path", "file", "id", "key"):
                if isinstance(record.get(key), str):
                    remember(record[key])

    def ingest_text(path, relative):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            problems.append({"source": relative, "reason": "unreadable_receipt"})
            return
        for match in ORIGIN_ROW.findall(text):
            remember(match)
        for first, second in ORIGIN_LINK.findall(text):
            remember(unquote(first or second).split("#", 1)[0])

    while pending:
        directory, depth = pending.pop(0)
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name.casefold())
        except OSError:
            problems.append({
                "source": str(directory.relative_to(project)) if directory != project else ".",
                "reason": "unreadable_directory",
            })
            continue
        for path in entries:
            if seen >= max_entries:
                problems.append({"reason": "scan_limit", "limit": "entries"})
                pending.clear()
                stopped = True
                break
            seen += 1
            if path.name.startswith("."):
                continue
            if path.is_symlink():
                continue
            if path.is_dir():
                if path.name.casefold() in ORIGIN_SKIP:
                    continue
                if depth >= 6:
                    problems.append({
                        "source": str(path.relative_to(project)), "reason": "depth_limit",
                    })
                else:
                    pending.append((path, depth + 1))
                continue
            if not path.is_file():
                continue
            relative = path.relative_to(project).as_posix()
            suffix = path.suffix.casefold()
            stem = path.name.casefold()
            if suffix in EMBEDDED_SUFFIXES:
                embedded.append(relative)
                sidecar = path.with_name(path.name + ".credits.txt")
                alt = path.with_suffix(path.suffix + ".credits.txt")
                near = path.with_name(path.stem + ".credits.txt")
                if any(candidate.is_file() and not candidate.is_symlink()
                       for candidate in (sidecar, alt, near)):
                    remember(relative)
                    remember(path.name)
            if stem in ORIGIN_RECEIPTS or stem.endswith(".credits.txt"):
                receipts.append(relative)
                if suffix == ".json":
                    ingest_json(path, relative)
                else:
                    ingest_text(path, relative)

    declared, undeclared = [], []
    for relative in embedded:
        name = Path(relative).name
        if relative in mentioned or name in mentioned:
            declared.append(relative)
        else:
            undeclared.append(relative)

    licensing = gate_declaration(project)["declared"].get("deliver", {}).get("licensing")
    contradicts = bool(
        licensing and licensing["state"] == "met" and undeclared
    )
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "embedded": embedded,
        "declared": declared,
        "undeclared": undeclared,
        "receipts": receipts,
        "problems": problems,
        "contradicts_licensing": contradicts,
        "truncated": stopped,
        "granted": False,
        "validated": False,
        "guide": str(FRAMEWORK / "references/gates.md"),
        "rule": (
            "Arquivo embarcado sem recibo de origem conta como licença desconhecida. "
            "O recibo declara origem, autor e condição de uso; não prova que a condição vale."
        ),
        "scope": (
            "Percorre o projeto, lista arquivos de mídia embarcados e cruza com recibos "
            "(sources.json, licenses.json, CREDITS, sidecar `.credits.txt`). Relata ausência "
            "de recibo, recibo ilegível e declaração `deliver.licensing` = `met` que o disco "
            "contradiz. Não consulta titular, não interpreta texto de licença, não distingue "
            "licença válida de inválida e **não concede passagem**."
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
    json_docs = {"brief.json", "state.json", "decisions.json", "sources.json", "licenses.json", "package.json"}
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
        "git": git_summary(project) if project.is_dir() else None,
        "source_index": str(FRAMEWORK / "references/sources.md"),
        "package_manager": manager,
        "metadata_issues": metadata_issues,
        "scripts": scripts,
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
            "Áudio novo: se shared/sfx tiver sons, busque (`sfx search`) antes de baixar. Sem acervo, o starter já fala em public/sfx e sfx serve recusa. Crescer o acervo é `sfx import ARQUIVO --metadata JSON` (ffmpeg); `sfx info` lê a ficha e `sfx export ID --to PASTA` copia bytes e créditos. Importar e exportar não é ouvir. Piso de gravação licenciada; 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão.",
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
PLAY_SCRIPTS = ("serve", "start", "dev", "preview")
VALIDATOR_ORDER = ("test", "check", "lint", "typecheck", "types", "verify", "audit", "build", "budget", "bench")
BRIEF_IDEA_MARKER = "[quem o jogador é e o que realiza]"


def play_script_names(scripts):
    names = list(scripts)
    found = []
    for word in PLAY_SCRIPTS:
        for name in names:
            if name == word or name.startswith(f"{word}:") or name.startswith(f"{word}-"):
                if name not in found:
                    found.append(name)
    return found


def play_command(project, scripts, manager):
    names = play_script_names(scripts)
    if not names or not manager:
        return None
    name = names[0]
    info = scripts[name] if isinstance(scripts, dict) else {}
    argv = info.get("argv") if isinstance(info, dict) else None
    body = " ".join(shlex.quote(str(part)) for part in argv) if argv else f"{manager} run {shlex.quote(name)}"
    return f"cd {shlex.quote(str(project))} && {body}"


def note_author(project=None):
    # Sugestão para o comando colar. Não é quem jogou e não fecha o achado.
    targets = []
    if project is not None:
        path = Path(project)
        if path.is_dir() and not path.is_symlink():
            targets.append(["git", "-C", str(path), "config", "user.name"])
    targets.append(["git", "config", "user.name"])
    for argv in targets:
        try:
            run = subprocess.run(argv, capture_output=True, text=True, timeout=5, check=False)
        except (OSError, subprocess.TimeoutExpired):
            continue
        name = (run.stdout or "").strip()
        if run.returncode == 0 and nonempty(name):
            return name
    env = os.environ.get("GIT_AUTHOR_NAME") or os.environ.get("USER") or os.environ.get("USERNAME")
    if nonempty(env):
        return env.strip()
    return "NOME"


def session_command(project, starter=None):
    project = Path(project)
    scripts, manager = {}, None
    if project.is_dir() and not project.is_symlink():
        try:
            scripts, manager = project_commands(project)
        except (OSError, ValueError):
            scripts, manager = {}, None
    elif starter:
        scripts, manager = starter_package_commands(starter)
    if not manager or "session" not in scripts:
        return None
    return project_run_command(project, manager, "session")


def note_command(project):
    parts = ["note", project, "--author", note_author(project), "--note", "o que o verbo sentiu"]
    if last_run_path(project):
        parts.append("--from-run")
    return harness_command(*parts)


# Exemplos coláveis do segundo ciclo. Os nomes não existem no starter:
# nascer o par `noite` (look e chuva no mesmo nome) ou deslocar `dash`
# é o que o `next` deixa de apontar quando o disco já tem um look, uma
# chuva ou uma voz deslocada. Look e chuva sozinhos continuam no disco;
# o par é o caminho que vira `?mood=`.
CRAFT_EXAMPLES = {
    "pair": ("noite", "--from", "dusk", "--look", "warmer", "--spawn", "denser"),
    "look": ("noite", "--from", "dusk", "--as", "warmer"),
    "table": ("noite", "--from", "spawn", "--as", "denser"),
    "sfx": ("--from", "dash", "--as", "brighter"),
}
STARTER_LOOKS = frozenset({"normal", "contrast", "dusk", "calm"})
STARTER_TABLES = frozenset({"copy", "palettes", "spawn", "dusk", "calm"})
CRAFT_LABELS = {"pair": "Par", "look": "Look", "table": "Chuva", "sfx": "Voz"}


def project_run_command(project, manager, name, extra=()):
    argv = [manager, "run", name]
    if extra:
        argv.append("--")
        argv.extend(extra)
    body = " ".join(shlex.quote(str(part)) for part in argv)
    return f"cd {shlex.quote(str(project))} && {body}"


def starter_package_commands(starter):
    source = STARTERS_ROOT / starter
    if not source.is_dir() or source.is_symlink():
        return {}, None
    try:
        return package_commands(source)
    except (OSError, ValueError):
        return {}, None


def craft_from_scripts(project, scripts, manager):
    if not manager or not scripts:
        return {}
    found = {}
    for name, extra in CRAFT_EXAMPLES.items():
        if name in scripts:
            found[name] = project_run_command(project, manager, name, extra)
    return found


def craft_commands(project, starter=None):
    project = Path(project)
    if project.is_dir() and not project.is_symlink():
        try:
            scripts, manager = project_commands(project)
        except (OSError, ValueError):
            return {}
        return craft_from_scripts(project, scripts, manager)
    if not starter:
        return {}
    scripts, manager = starter_package_commands(starter)
    return craft_from_scripts(project, scripts, manager)


def cycle_crafted(project):
    project = Path(project)
    palettes = project / "data/palettes.json"
    if palettes.is_file() and not palettes.is_symlink():
        try:
            data = json.loads(palettes.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        mapping = data.get("palettes") if isinstance(data, dict) else None
        if isinstance(mapping, dict) and set(mapping) - STARTER_LOOKS:
            return True
    folder = project / "data"
    if folder.is_dir() and not folder.is_symlink():
        try:
            entries = list(folder.iterdir())
        except OSError:
            entries = []
        for path in entries:
            if path.is_symlink() or not path.is_file() or path.suffix != ".json":
                continue
            if path.stem not in STARTER_TABLES:
                return True
    sources = project / "public/sfx/sources.json"
    if sources.is_file() and not sources.is_symlink():
        try:
            data = json.loads(sources.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        files = data.get("files") if isinstance(data, dict) else None
        if isinstance(files, list):
            for item in files:
                note = item.get("note") if isinstance(item, dict) else None
                if isinstance(note, str) and "intenção" in note:
                    return True
    return False


def cycle_then(project, play, starter=None):
    then = {
        "play": play,
        "note": note_command(project),
        "lost": harness_command("next", project, "--focus", "feel"),
    }
    then.update(craft_commands(project, starter))
    session = session_command(project, starter)
    if session:
        then["session"] = session
    return then


def cycle_prompt(play, then, cycle, noted=False):
    if not play:
        return (
            "Sem comando de abrir: identifique o entrypoint e rode `next`. "
            "O harness não executa o jogo."
        )
    craft = [key for key in CRAFT_EXAMPLES if then.get(key)]
    if noted and craft:
        parts = ["O ciclo já tem um recibo."]
        for key in craft:
            parts.append(f"{CRAFT_LABELS[key]}: {then[key]}.")
        parts.append("O harness não pinta, não chove e não ouve.")
        parts.append(f"`next` só se você não sabe o que falta: {then['lost']}.")
        return " ".join(parts)
    how = cycle_line(cycle)
    return (
        f"O jogo não foi aberto. Cole e rode: {play}. "
        + (f"{how} " if how else "")
        + f"Depois de uma partida, no harness: {then['note']}. "
        "`next` só se o ciclo já correu e você não sabe o que falta."
    )


def guide_prompt(exists, start_command, play, then, cycle, noted=False):
    if exists:
        return cycle_prompt(play, then, cycle, noted)
    return (
        f"O ciclo ainda não existe. Cole e rode: {start_command}. "
        f"Depois, no próprio dispositivo: {play}. "
        f"Depois de uma partida, no harness: {then['note']}. "
        "O harness não cria a pasta, não abre o jogo e não joga."
    )


def fresh_starter_cycle(project, missing, play):
    if missing or not play:
        return False
    docs = project / "docs"
    if not docs.is_dir() or docs.is_symlink():
        return False
    drafted = 0
    for stage in FRESH_DRAFTS:
        path = docs / f"{stage}.md"
        if not path.is_file() or path.is_symlink():
            return False
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return False
        if not DRAFT_MARKERS.search(text):
            return False
        drafted += 1
    return drafted == len(FRESH_DRAFTS)


SURFACE_IDEA_LIMIT = 72


def seed_brief_idea(project, phrase):
    path = Path(project) / "docs/brief.md"
    if not path.is_file() or path.is_symlink():
        return None
    text = path.read_text(encoding="utf-8")
    if BRIEF_IDEA_MARKER in text:
        text = text.replace(BRIEF_IDEA_MARKER, phrase, 1)
    else:
        text = text.replace("## Visão e jogador", f"## Visão e jogador\n\n- Fantasia em uma frase: {phrase}.", 1)
    path.write_text(text, encoding="utf-8")
    return "docs/brief.md"


def seed_copy_fantasy(project, phrase):
    path = Path(project) / "data/copy.json"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    surface = phrase if len(phrase) <= SURFACE_IDEA_LIMIT else f"{phrase[: SURFACE_IDEA_LIMIT - 3].rstrip()}..."
    data["fantasy"] = surface
    schema = data.get("schema")
    if not isinstance(schema, int) or schema < 2:
        data["schema"] = 2
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return "data/copy.json"


def seed_idea(project, idea):
    if not nonempty(idea):
        return {"brief": None, "surface": None}
    phrase = idea.strip()
    return {
        "brief": seed_brief_idea(project, phrase),
        "surface": seed_copy_fantasy(project, phrase),
    }


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


CYCLE_KEYS = ("verb", "move", "dash", "bank", "hand", "touch", "pad", "look", "spawn", "mood", "invite")


def starter_cycle(starter):
    if not nonempty(starter):
        return None
    try:
        manifest = starter_manifest(starter)
    except ValueError:
        return None
    raw = manifest.get("cycle") if isinstance(manifest, dict) else None
    if not isinstance(raw, dict):
        return None
    cycle = {}
    for key in CYCLE_KEYS:
        value = raw.get(key)
        if nonempty(value) and isinstance(value, str):
            cycle[key] = value.strip()
    return cycle if "verb" in cycle else None


def cycle_line(cycle):
    if not cycle:
        return ""
    parts = [f"Verbo: {cycle['verb']}."]
    if cycle.get("move"):
        parts.append(f"Mover {cycle['move']}.")
    if cycle.get("dash"):
        parts.append(f"Avançar {cycle['dash']}.")
    if cycle.get("bank"):
        parts.append(f"Guardar {cycle['bank']}.")
    if cycle.get("hand"):
        parts.append(f"Uma mão: {cycle['hand']}.")
    if cycle.get("touch"):
        parts.append(f"Toque: {cycle['touch']}.")
    if cycle.get("pad"):
        parts.append(f"Controle: {cycle['pad']}.")
    if cycle.get("look"):
        parts.append(f"Look: {cycle['look']}.")
    if cycle.get("spawn"):
        parts.append(f"Chuva: {cycle['spawn']}.")
    if cycle.get("mood"):
        parts.append(f"Par: {cycle['mood']}.")
    if cycle.get("invite"):
        parts.append(f"Convite: {cycle['invite']}.")
    return " ".join(parts)


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


def init(destination, starter, title=None, documents=True, idea=None):
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
        if any(part in INIT_COPY_SKIP for part in path.relative_to(source).parts):
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
            # O starter pode trazer um documento vigente (art-bible). Sobrescrever
            # com o template apagaria a decisão e o `template` já recusa destino
            # existente — pular é o que impede o init de quebrar e de rebaixar.
            if output.exists():
                continue
            template(stage, destination, output)
            drafts.append(output.relative_to(destination).as_posix())
        if not (destination / "AGENTS.md").exists():
            template("agents", destination, destination / "AGENTS.md")
            drafts.append("AGENTS.md")
    planted = seed_idea(destination, idea)
    scripts, manager = package_commands(destination)
    play = play_command(destination, {name: {"argv": [manager, "run", name]} for name in scripts} if manager else scripts, manager)
    commands = []
    if play:
        commands.append(play)
    commands.append(harness_command("next", destination, "--focus", "feel"))
    return {
        "schema_version": 1,
        "project": str(destination),
        "starter": starter,
        "kind": identify(destination),
        "title": values["project_title"],
        "files": files,
        "documents": drafts,
        "document_status": "draft",
        "idea": idea.strip() if nonempty(idea) else None,
        "brief": planted["brief"],
        "surface": planted["surface"],
        "substitutions": applied,
        "read_next": [
            str(FRAMEWORK / "references/production-bar.md"),
            str(FRAMEWORK / "references/preproduction.md"),
            str(destination / "README.md"),
        ],
        "next_commands": commands,
        "scope": (
            "Copiou o starter, trocou os valores que `starter.json` declara e criou rascunhos a partir dos "
            "templates. O ciclo já abre: o primeiro comando apontado é o que serve o jogo, não o que preenche "
            "os rascunhos. Documento vigente que o starter já trouxe (art-bible) não é reescrito. "
            "`scan` ainda reporta `draft_only` nas áreas sem decisão. `--idea` entra no brief como frase "
            "e, se houver `data/copy.json`, na abertura e no aviso do primeiro ciclo. O brief continua rascunho. "
            "A frase na tela não muda o verbo. O starter é material de "
            "ADAPT, não uma engine nem uma base aprovada; o comando não executa o jogo, não instala "
            "dependências e não avalia a proposta."
        ),
    }


def start_project(destination=None, starter=None, title=None, idea=None, documents=True, cwd=None):
    named = destination is None
    if destination is None:
        destination = start_destination_from_idea(idea, cwd=cwd)
    else:
        destination = Path(destination)
    available = starters()
    chosen = starter or (available[0] if available else None)
    created = False
    init_report = None
    planted = {"brief": None, "surface": None}
    if not destination.exists() or (
        destination.is_dir() and not destination.is_symlink() and not any(destination.iterdir())
    ):
        if not chosen:
            raise ValueError("nenhum starter disponível neste repositório")
        init_report = init(destination, chosen, title, documents, idea)
        created = True
        planted = {"brief": init_report.get("brief"), "surface": init_report.get("surface")}
    elif destination.exists() and not destination.is_dir():
        raise ValueError("destino existente; escolha um caminho novo")
    elif nonempty(idea):
        planted = seed_idea(destination, idea)
    proposal = next_step(destination, "feel")
    try:
        scripts, manager = project_commands(destination)
    except (OSError, ValueError):
        scripts, manager = {}, None
    play = play_command(destination, scripts, manager)
    then = cycle_then(destination, play, chosen)
    cycle = starter_cycle(chosen)
    noted = bool(observation_receipts(destination))
    return {
        "schema_version": 1,
        "project": str(destination),
        "created": created,
        "starter": init_report["starter"] if init_report else None,
        "idea": idea.strip() if nonempty(idea) else None,
        "brief": planted["brief"],
        "surface": planted["surface"],
        "cycle": cycle,
        "play": play,
        "init": init_report,
        "next": proposal,
        "then": then,
        "noted": noted,
        "named": named,
        "suggest": str(suggested_start_target(idea, cwd=cwd)) if named else None,
        "prompt": cycle_prompt(play, then, cycle, noted),
        "executed": False,
        "scope": (
            "Caminho ideia→ciclo: cria o projeto se o destino estiver livre e "
            "aponta o comando que abre o jogo. Sem caminho, `--idea` nomeia "
            "a pasta — ao lado do framework se o start corre de dentro desta "
            "árvore — e cria. `guide --idea` continua só no comando, não no "
            "disco. Se o starter declara o verbo e "
            "as teclas, o prompt as nomeia — inclusive o cluster de uma mão, "
            "o toque, o controle e as queries de look, chuva, par e convite, se o starter as declara. Não "
            "executa o jogo. Depois de uma "
            "partida, o próximo comando do harness é `note`, não `next`. "
            "`then` já nomeia par, look, chuva e voz se o projeto declara essas "
            "ferramentas; depois de um recibo, o prompt as aponta. Ferramenta "
            "no disco não é alguém de fora nem mix ouvido. Não "
            "instala dependências e não avalia a proposta. `--idea` entra no "
            "brief como frase e, se houver `data/copy.json`, na abertura e no aviso do "
            "primeiro ciclo. O brief continua rascunho. A frase na tela não "
            "muda o verbo."
        ),
    }


def here_project(explicit=None, root=None):
    # Sem destino, o mapa usa o diretório atual só se ele for um jogo
    # fora desta árvore. Dentro do framework o comando sem argumentos
    # continua o convite a começar — não o starter como se fosse o seu.
    if explicit is not None:
        return resolve(explicit, root or ROOT)
    cwd = Path.cwd().resolve()
    framework = FRAMEWORK.resolve()
    if cwd == framework or cwd.is_relative_to(framework):
        return None
    if cwd.is_dir() and not cwd.is_symlink() and (cwd / "package.json").is_file():
        return cwd
    return None


# Teto do nome derivado da frase. Mais que isso vira caminho ilegível;
# menos obriga a inventar o resto. A pasta só existe depois do `start`.
IDEA_SLUG_LIMIT = 48


def idea_slug(idea, limit=IDEA_SLUG_LIMIT):
    if not isinstance(idea, str) or not idea.strip():
        return None
    folded = unicodedata.normalize("NFKD", idea.strip().casefold())
    folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", "-", folded).strip("-")
    if not text:
        return None
    return text[:limit].strip("-") or None


def suggested_start_target(idea, cwd=None, framework=None):
    slug = idea_slug(idea)
    if not slug:
        return None
    here = Path(cwd or Path.cwd()).resolve()
    root = Path(framework or FRAMEWORK).resolve()
    # Dentro desta árvore o mapa sem destino não usa o chão, e uma pasta
    # filha também não vira `here`. O nome fica ao lado do framework.
    if here == root or here.is_relative_to(root):
        return Path("..") / slug
    return Path(slug)


def start_destination_from_idea(idea, cwd=None, framework=None):
    target = suggested_start_target(idea, cwd=cwd, framework=framework)
    if target is None:
        raise ValueError(
            "sem destino: passe o caminho ou --idea com uma frase que nomeie a pasta"
        )
    here = Path(cwd or Path.cwd()).resolve()
    return (here / target).resolve()


def guide_cycle(destination=None, starter=None, idea=None, cwd=None):
    available = starters()
    chosen = starter or (available[0] if available else "canvas-arcade")
    dest = Path(destination) if destination is not None else None
    exists = bool(
        dest is not None
        and dest.is_dir()
        and not dest.is_symlink()
        and (dest / "package.json").is_file()
    )
    phrase = idea.strip() if nonempty(idea) else None
    suggested = suggested_start_target(phrase, cwd=cwd) if dest is None else None
    start_target = dest if dest is not None else (suggested or Path("<destino>"))
    start_parts = ["start", start_target, "--starter", chosen]
    if phrase:
        start_parts.extend(["--idea", phrase])
    play = None
    nxt = None
    if exists:
        try:
            scripts, manager = project_commands(dest)
        except (OSError, ValueError):
            scripts, manager = {}, None
        play = play_command(dest, scripts, manager)
        nxt = next_step(dest, "feel")
    named = dest if dest is not None else suggested
    play_fallback = (
        f"cd {shlex.quote(str(named))} && npm run serve"
        if named is not None
        else "npm run serve"
    )
    next_target = named if named is not None else Path("<destino>")
    play_cmd = play or play_fallback
    then = cycle_then(next_target, play_cmd, chosen)
    cycle = starter_cycle(chosen)
    start_command = harness_command(*start_parts)
    noted = bool(exists and observation_receipts(dest))
    play_step = {
        "n": 2,
        "do": "jogar no próprio dispositivo",
        "command": play_cmd,
        "kind": nxt["proposal"]["basis"] if nxt else "playable.unplayed",
        "executed": False,
    }
    if cycle:
        play_step["verb"] = cycle["verb"]
        play_step["controls"] = {
            key: cycle[key]
            for key in CYCLE_KEYS
            if key != "verb" and key in cycle
        }
    return {
        "schema_version": 1,
        "command": "guide",
        "executed": False,
        "here": False,
        "idea": phrase,
        "starter": chosen,
        "path": str(dest) if dest is not None else None,
        "suggest": str(suggested) if suggested is not None else None,
        "exists": exists,
        "cycle": cycle,
        "then": then,
        "noted": noted,
        "open": start_command if not exists else play_cmd,
        "prompt": guide_prompt(exists, start_command, play_cmd, then, cycle, noted),
        "steps": [
            {
                "n": 1,
                "do": "abrir o ciclo",
                "command": start_command,
                "done": exists,
            },
            play_step,
            {
                "n": 3,
                "do": "gravar o que o verbo sentiu",
                "command": then["note"],
                "executed": False,
            },
        ],
        "scope": (
            "Três passos ideia→ciclo: start, jogar, note. `open` é o comando "
            "de agora — o start se o destino ainda não existe, o play se "
            "já existe. `prompt` o nomeia para colar. Se o starter declara "
            "o verbo e as teclas, o passo 2 as nomeia — inclusive o par. Sem destino, a frase "
            "nomeia a pasta no comando do start — ao lado do framework se o "
            "mapa corre de dentro desta árvore; no diretório atual se corre "
            "de fora. `guide --idea` continua só no comando, não no disco. "
            "`then` nomeia par, look, chuva e voz quando o projeto — ou o "
            "starter, se o destino ainda não existe — declara essas "
            "ferramentas. Se declara `session`, `then` a aponta. Nomear o "
            "ofício não pinta, não chove e não ouve. O autor do `note` é "
            "sugestão do git ou do ambiente, não quem jogou. "
            "`next` fica para quando o ciclo já correu e você não sabe o "
            "que falta. Sem destino, se o diretório atual é um jogo fora "
            "do framework, o mapa usa esse caminho. Não cria o projeto, "
            "não abre o jogo e não avalia a proposta. Passos 2 e 3 "
            "permanecem `executed` falsos mesmo quando o destino já existe."
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

    if not payload["exists"]:
        propose(
            f"Criar o projeto em {project} a partir de um starter e abrir o ciclo",
            "Sem destino no disco não há candidato para REUSE, e qualquer decisão de design fica sem consumidor.",
            "O jogo abre, o verbo da proposta foi jogado uma vez e o brief registra o que muda — ou a lacuna.",
            [harness_command("start", project, "--starter", starters()[0] if starters() else "NOME_DO_STARTER")],
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
    play = play_command(project, payload["scripts"], payload["package_manager"])
    noted = bool(observation_receipts(project))
    fresh = fresh_starter_cycle(project, missing, play) and not noted
    if fresh:
        propose(
            "Abrir o ciclo do starter e escrever o que a proposta muda no verbo",
            "O destino já é um jogo que abre. Sete rascunhos antes da primeira partida "
            "são o atrito que este passo existe para cortar. O harness não executa o jogo.",
            "O ciclo correu uma vez, e o brief (ou um recibo de observação) registra o que "
            "esta proposta muda no verbo — ou a lacuna, se ainda não souber.",
            [play, harness_command("next", project, "--focus", "feel")],
            "playable.unplayed",
        )
    craft_cmds = craft_commands(project)
    wants_craft = bool(noted and craft_cmds and not cycle_crafted(project))
    if wants_craft:
        propose(
            "Deslocar o par, o look, a chuva ou a voz com as ferramentas que o projeto já declara",
            "O ciclo já tem um recibo. O par nasce look e chuva no mesmo nome "
            "e vira ?mood=. Look, chuva e voz sozinhos continuam no disco. "
            "Ferramenta no disco não é alguém de fora nem mix ouvido. "
            "O harness não pinta, não chove e não ouve.",
            "Nasceu um look, uma chuva ou uma voz deslocada — ou a lacuna está "
            "escrita. consistent, enough e heard continuam pendentes.",
            [craft_cmds[key] for key in CRAFT_EXAMPLES if key in craft_cmds],
            "cycle.craft",
        )
    roles = roles_reading(project)
    if roles["empty"]:
        sample = ", ".join(f"`{name}`" for name in roles["empty"][:4])
        extra = " e mais" if len(roles["empty"]) > 4 else ""
        commands = [harness_command("roles", project, "--fill")]
        if roles["catalog_exists"]:
            commands.append(harness_command("roles", project, "--fill", "--apply"))
        propose(
            f"Preencher os papéis de áudio declarados e vazios: {sample}{extra}",
            "O verbo já dispara esses papéis. Arquivo ausente não é silêncio "
            "deliberado — silêncio deliberado é o papel fora da declaração. "
            "O harness não ouve o som e não aprova mixagem.",
            "Cada papel declarado tem um arquivo no disco (public/sfx ou "
            "equivalente), ou o papel saiu da declaração.",
            commands,
            "audio.roles",
        )
    feel = feel_reading(project)
    if feel["unobserved"]:
        sample = ", ".join(f"`{item['key']}`" for item in feel["constants"][:4])
        extra = " e mais" if len(feel["constants"]) > 4 else ""
        propose(
            f"Registrar o que o verbo sentiu numa partida ({sample}{extra})",
            "Há constantes de feel no código e nenhum recibo de observação no "
            "projeto. Constante nomeada não é peso percebido. O harness não joga.",
            "Existe um `note` (ou `record --kind observation`) sob o projeto, "
            "com cenário, role e o que mudou (ou não) no verbo — ou a lacuna, "
            "se ainda não souber.",
            [
                harness_command("feel", project),
                harness_command("note", project, "--author", note_author(project), "--note", "o que o verbo sentiu"),
            ],
            "feel.unobserved",
        )
    playtest = playtest_reading(project)
    wants_invite = bool(noted and not playtest.get("invite"))
    if wants_invite:
        propose(
            "Escrever o convite para quem nunca viu o jogo",
            "O ciclo já tem um recibo de quem fez. A curva com quem nunca "
            "viu o jogo continua pendente. `/?invite=1` some a tabela. "
            "Página no disco não é alguém de fora e não sobe pacing. "
            "O harness não assiste.",
            "Existe docs/playtest/invite.md. observed e outsider continuam "
            "falsos até alguém que não fez o jogo jogar e escrever o achado.",
            [harness_command("playtest", project, "--invite")],
            "playtest.invite",
        )
    if playtest["unstructured"]:
        propose(
            "Escrever o achado de playtest no formato problema, evidência, hipótese e medição",
            "Há observação (ou um qa.md vigente) e nenhum achado com os quatro "
            "campos. Nota de partida não é métrica. last-run.json é candidato, "
            "não causa. O harness não assistiu à sessão e não conta jogadores.",
            "Um documento ou o próprio recibo nomeia problema, evidência, "
            "hipótese e medição — a causa e o tamanho do efeito continuam "
            "pendentes.",
            [
                harness_command("playtest", project),
                harness_command("feel", project),
                *(
                    [harness_command(
                        "note", project, "--author", note_author(project),
                        "--note", "o que o verbo sentiu", "--from-run",
                    )]
                    if playtest.get("candidate")
                    else []
                ),
            ],
            "playtest.unstructured",
        )
    access = access_reading(project)
    if payload["kind"] and not access["declared"]:
        propose(
            "Declarar no código as opções de alcance que o recorte precisa",
            "O jogo já tem ponto de entrada e nenhuma opção de contraste, "
            "movimento, legenda ou remapeamento aparece no código. Opção só "
            "existe com consumidor. O harness não mede contraste.",
            "highContrast, reducedMotion, captions ou remapeamento têm "
            "consumidor no código — ou a ausência está escrita no canônico.",
            [harness_command("access", project)],
            "access.missing",
        )
    persist = save_reading(project)
    if persist["unversioned"]:
        propose(
            "Versionar o save e escrever a migração junto do formato",
            "O projeto grava progresso ou preferência e não declara schema nem "
            "migrate. Atualização sem migração é perda de progresso. O harness "
            "não abre o save.",
            "O formato tem versão nomeada e uma migração que a acompanha, ou o "
            "armazenamento sai do recorte.",
            [harness_command("save", project)],
            "save.unversioned",
        )
    perf = budget_reading(project)
    if perf["unbudgeted"]:
        propose(
            "Declarar um orçamento mensurável (script budget/bench ou tools/budget)",
            "Há manifesto de execução e nenhum artefato que meça tempo de quadro "
            "ou simulação. Sem orçamento, ‘rápido o suficiente’ é opinião. O "
            "harness não mede.",
            "Existe `budget`/`bench` no manifesto, um tools/budget.* ou um "
            "`record --kind budget` — a medição em si continua pendente.",
            [harness_command("budget", project)],
            "performance.unbudgeted",
        )
    art = art_reading(project)
    if payload["kind"] and not art["declared"]:
        propose(
            "Declarar a direção de arte no código (PALETTES) ou num art-bible vigente",
            "O jogo já tem ponto de entrada e nenhuma paleta, token ou art-bible "
            "vigente aparece no disco. Rascunho do `init` não é direção. O "
            "harness não compara silhueta e não aprova estilo.",
            "Existe `const PALETTES`, um tokens.json, data/palettes.json ou docs/art-bible.md sem "
            "marcador de rascunho — a consistência em movimento continua pendente.",
            [harness_command("art", project)],
            "art.missing",
        )
    inventory = content_reading(project)
    if inventory["inline"]:
        propose(
            "Extrair o conteúdo do código para dado (data/, levels/ ou .ldtk/.tmx/.ink)",
            "O verbo já tem ponto de entrada e o conteúdo ainda mora no código. "
            "Conteúdo no código não escala. O harness não carrega o formato e "
            "não conta itens.",
            "Há arquivo em data/, content/, levels/, maps/ ou tables/, ou um "
            ".ldtk/.tmx/.ink no projeto — volume e consumo continuam pendentes.",
            [harness_command("content", project)],
            "content.inline",
        )
    pack = ship_reading(project)
    if pack["unpacked"]:
        propose(
            "Declarar o passo que empacota o jogo (script build/export ou docs/release.md)",
            "Há manifesto de execução e nenhum passo de build, export, release "
            "vigente ou CI. Servir na máquina de quem construiu não é entregar. "
            "O harness não executa o export e não autoriza publicar.",
            "Existe script `build`/`export`/`package`/`release`, um "
            "docs/release.md vigente ou um workflow de CI — o artefato em "
            "outra máquina continua pendente.",
            [harness_command("ship", project)],
            "ship.unpacked",
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
    origins = origins_reading(project)
    if origins["undeclared"]:
        sample = ", ".join(f"`{path}`" for path in origins["undeclared"][:4])
        extra = " e mais" if len(origins["undeclared"]) > 4 else ""
        why = (
            "Arquivo embarcado sem recibo conta como licença desconhecida, e o critério "
            "`deliver.licensing` não se dispensa. O harness não valida a licença: só vê "
            "que a origem não foi declarada."
        )
        if origins["contradicts_licensing"]:
            why = (
                "O projeto declara `deliver.licensing` como `met`, e o disco ainda tem "
                "arquivo embarcado sem recibo. A linha da tabela não sobrevive à leitura "
                "do próprio projeto."
            )
        propose(
            f"Declarar origem dos arquivos embarcados sem recibo: {sample}{extra}",
            why,
            "Cada arquivo listado tem recibo ao lado (sources.json, CREDITS ou "
            "`.credits.txt`) com origem, autor e condição de uso — ou sai do embarque.",
            [harness_command("origins", project)],
            "origins.undeclared",
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
    craft = craft_declaration(project)
    if craft["problems"]:
        propose(
            "Corrigir a forma da declaração de ofício em: "
            + ", ".join(f"{item['source']} ({item['reason']})" for item in craft["problems"][:4]),
            "Linha malformada não entra na leitura, e o checklist que ela pretendia "
            "declarar continua pendente.",
            "Cada linha nomeia um dos checklists de ofício, um estado e o que sustenta o estado.",
            [harness_command("craft", project)],
            "craft.problems",
        )
    else:
        reading = craft_reading(project)
        live = [item for item in reading["checks"] if item["gate"] in gates["declared"]]
        blocked = next((item for item in live if item["state"] in ("undeclared", "unmet")), None)
        if blocked:
            propose(
                f"Declarar o checklist `{blocked['key']}` do gate `{blocked['gate']}`: {blocked['check']}",
                "Isto não pergunta se um número externo se cumpriu. Pergunta se o projeto "
                "corresponde ao que ele mesmo declarou — paleta, constante, definição, "
                "regra de parada. O harness não observa o jogo.",
                "A linha sai de `undeclared`/`unmet` com o que sustenta o estado, ou é "
                "dispensada com motivo e autor, ou marcada fora de escopo com motivo.",
                [harness_command("craft", project, "--gate", blocked["gate"])],
                "craft.pending",
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
            "origins_undeclared": origins["undeclared"],
            "origins_contradicts_licensing": origins["contradicts_licensing"],
            "playable_unplayed": fresh,
            "cycle_craft": wants_craft,
            "audio_roles_empty": roles["empty"],
            "feel_unobserved": feel["unobserved"],
            "playtest_unstructured": playtest["unstructured"],
            "playtest_invite": wants_invite,
            "playtest_candidate": playtest.get("candidate"),
            "access_missing": access["missing"] if payload["kind"] else [],
            "save_unversioned": persist["unversioned"],
            "performance_unbudgeted": perf["unbudgeted"],
            "art_missing": bool(payload["kind"]) and not art["declared"],
            "content_inline": inventory["inline"],
            "ship_unpacked": pack["unpacked"],
            "craft_pending": [
                key for key, spec in CRAFT_CHECKS.items()
                if spec["gate"] in gates["declared"]
                and craft["declared"].get(key, {}).get("state", "undeclared") in ("undeclared", "unmet")
            ],
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


def note_observation(project, author, note, fields=None, output=None, role="human", scenario="primeira partida", from_run=False):
    project = Path(project)
    payload = dict(fields or {})
    attached = None
    if from_run:
        source = from_run if from_run is not True else None
        payload, attached = attach_run_candidate(project, payload, source)
    if nonempty(scenario) and not nonempty(payload.get("scenario")):
        payload["scenario"] = scenario
    if nonempty(role) and not nonempty(payload.get("role")):
        payload["role"] = role
    dest = Path(output) if output else project / "docs" / "playtest" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    report = record(project, "observation", author, note, payload, [], dest)
    report["command"] = "note"
    report["felt"] = False
    report["observed"] = False
    if attached is not None:
        report["from_run"] = attached.as_posix() if attached.is_absolute() else attached.as_posix()
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
    parser.add_argument(
        "--idea",
        default=None,
        help="frase da fantasia; sem subcomando, só entra no comando do start, não no disco",
    )
    commands = parser.add_subparsers(dest="action", required=False)
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
    start.add_argument("--idea", help="frase da fantasia; entra no brief, na abertura e no aviso do primeiro ciclo, sem mudar o verbo")
    start.add_argument("--no-docs", action="store_true", help="não criar os rascunhos em docs/")
    begin = commands.add_parser(
        "start", parents=[common],
        help="caminho ideia→ciclo: cria se o destino estiver livre e aponta o comando que abre o jogo",
    )
    begin.add_argument("project", nargs="?", default=None)
    begin.add_argument("--starter", default=starters()[0] if starters() else None, choices=starters() or None)
    begin.add_argument("--title", help="título legível; por omissão, derivado do nome da pasta")
    begin.add_argument("--idea", help="frase da fantasia; entra no brief, na abertura e no aviso do primeiro ciclo, sem mudar o verbo. Sem caminho, nomeia e cria a pasta")
    begin.add_argument("--no-docs", action="store_true", help="não criar os rascunhos em docs/")
    guided = commands.add_parser(
        "guide",
        parents=[common],
        help="três passos ideia→ciclo sem executar: start, jogar, note",
    )
    guided.add_argument("project", nargs="?", default=None)
    guided.add_argument("--starter", default=starters()[0] if starters() else None, choices=starters() or None)
    guided.add_argument("--idea", help="frase da fantasia; só entra no comando do start, não no disco")
    upcoming = commands.add_parser("next", parents=[common], help="proposta ordenada de próxima ação, a partir do estado no disco")
    upcoming.add_argument("project")
    upcoming.add_argument("--focus", choices=FOCI, default="create")
    initial_scan = commands.add_parser("scan", parents=[common])
    initial_scan.add_argument("project")
    reading = commands.add_parser("bar", parents=[common], help="degrau de acabamento que o projeto declara, e qual dimensão é o piso")
    reading.add_argument("project")
    origins_cmd = commands.add_parser(
        "origins", parents=[common],
        help="arquivos embarcados e o recibo de origem que o projeto declara",
    )
    origins_cmd.add_argument("project")
    craft_cmd = commands.add_parser(
        "craft", parents=[common],
        help="checklists de ofício que o projeto declara cumprir, sem limiar importado",
    )
    craft_cmd.add_argument("project")
    craft_cmd.add_argument("--gate", choices=sorted(GATES), help="só os checklists daquele gate")
    roles_cmd = commands.add_parser(
        "roles", parents=[common],
        help="papéis de áudio que o projeto declara e os arquivos que os preenchem",
    )
    roles_cmd.add_argument("project")
    roles_cmd.add_argument(
        "--fill", action="store_true",
        help="sugere um candidato do acervo para cada papel vazio; não copia",
    )
    roles_cmd.add_argument(
        "--apply", action="store_true",
        help="com --fill, copia a sugestão para public/sfx; não ouve e não aprova",
    )
    feel_cmd = commands.add_parser(
        "feel", parents=[common],
        help="constantes de feel que o projeto declara e o recibo de observação no disco",
    )
    feel_cmd.add_argument("project")
    access_cmd = commands.add_parser(
        "access", parents=[common],
        help="opções de alcance que o código declara, sem medição",
    )
    access_cmd.add_argument("project")
    save_cmd = commands.add_parser(
        "save", parents=[common],
        help="uso de persistência e se o formato tem versão e migração",
    )
    save_cmd.add_argument("project")
    budget_cmd = commands.add_parser(
        "budget", parents=[common],
        help="artefato de orçamento que o projeto declara, sem medir",
    )
    budget_cmd.add_argument("project")
    art_cmd = commands.add_parser(
        "art", parents=[common],
        help="paleta, tokens e art-bible vigentes, sem aprovar estilo",
    )
    art_cmd.add_argument("project")
    content_cmd = commands.add_parser(
        "content", parents=[common],
        help="conteúdo fora do código (data/levels ou .ldtk/.tmx/.ink), sem contar volume",
    )
    content_cmd.add_argument("project")
    ship_cmd = commands.add_parser(
        "ship", parents=[common],
        help="passo de empacotar que o projeto declara, sem exportar nem publicar",
    )
    ship_cmd.add_argument("project")
    playtest_cmd = commands.add_parser(
        "playtest", parents=[common],
        help="achado de playtest no formato problema/evidência/hipótese/medição, sem assistir",
    )
    playtest_cmd.add_argument("project")
    playtest_cmd.add_argument(
        "--invite", action="store_true",
        help="escreve docs/playtest/invite.md para quem nunca viu o jogo; não é alguém de fora",
    )
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
    noted = commands.add_parser(
        "note",
        parents=[common],
        help="recibo curto de observação: o que o verbo sentiu, sem jogar",
    )
    noted.add_argument("project")
    noted.add_argument("--author", required=True)
    noted.add_argument("--note", required=True)
    noted.add_argument("--role", choices=("human", "agent"), default="human")
    noted.add_argument("--scenario", default="primeira partida")
    noted.add_argument("--field", action="append", default=[], help="chave=valor extra; problema/evidência/hipótese/medição fecham o achado")
    noted.add_argument(
        "--from-run", nargs="?", const=True, default=False, metavar="ARQUIVO",
        help="anexa docs/playtest/last-run.json (resumo e, se houver, a curva) como candidato de medição; não fecha o achado",
    )
    noted.add_argument("--output", type=Path, help="pasta nova; por omissão, docs/playtest/<utc>")
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
    sfx_import = sfx_cmd.add_parser("import", parents=[common])
    sfx_import.add_argument("file", type=Path)
    sfx_import.add_argument("--metadata", type=Path, required=True)
    sfx_cmd.add_parser("seed", parents=[common])
    sfx_info = sfx_cmd.add_parser("info", parents=[common])
    sfx_info.add_argument("id")
    sfx_export = sfx_cmd.add_parser("export", parents=[common])
    sfx_export.add_argument("ids", nargs="+")
    sfx_export.add_argument("--to", required=True, type=Path)
    sfx_serve = sfx_cmd.add_parser("serve", parents=[common])
    sfx_serve.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if args.action is None:
            dest = here_project()
            report = guide_cycle(dest, idea=args.idea)
            report["here"] = dest is not None
            emit(report)
        elif args.action == "discover":
            emit(discover(root) if args.plain else review(root))
        elif args.action == "doctor":
            report = doctor(root)
            emit(report)
            return int(not report["ready"])
        elif args.action == "init":
            if not args.starter:
                raise ValueError("nenhum starter disponível neste repositório")
            emit(init(resolve(args.project, root), args.starter, args.title, not args.no_docs, args.idea))
        elif args.action == "start":
            dest = None if args.project is None else resolve(args.project, root)
            emit(start_project(dest, args.starter, args.title, args.idea, not args.no_docs))
        elif args.action == "guide":
            dest = here_project(args.project, root)
            report = guide_cycle(dest, args.starter, args.idea)
            report["here"] = args.project is None and dest is not None
            emit(report)
        elif args.action == "next":
            emit(next_step(resolve(args.project, root), args.focus, studies_root=default_studies_root(root)))
        elif args.action == "scan":
            emit(scan(resolve(args.project, root)))
        elif args.action == "bar":
            emit(bar_reading(resolve(args.project, root)))
        elif args.action == "origins":
            emit(origins_reading(resolve(args.project, root)))
        elif args.action == "craft":
            emit(craft_reading(resolve(args.project, root), args.gate))
        elif args.action == "roles":
            target = resolve(args.project, root)
            if args.fill or args.apply:
                emit(roles_fill(target, root, apply=args.apply))
            else:
                emit(roles_reading(target, root))
        elif args.action == "feel":
            emit(feel_reading(resolve(args.project, root)))
        elif args.action == "access":
            emit(access_reading(resolve(args.project, root)))
        elif args.action == "save":
            emit(save_reading(resolve(args.project, root)))
        elif args.action == "budget":
            emit(budget_reading(resolve(args.project, root)))
        elif args.action == "art":
            emit(art_reading(resolve(args.project, root)))
        elif args.action == "content":
            emit(content_reading(resolve(args.project, root)))
        elif args.action == "ship":
            emit(ship_reading(resolve(args.project, root)))
        elif args.action == "playtest":
            dest = resolve(args.project, root)
            emit(invite_playtest(dest) if args.invite else playtest_reading(dest))
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
        elif args.action == "check-plan":
            errors = check_plan(read_json(args.plan), root)
            emit({"contract_valid": not errors, "errors": errors, "scope": "Estrutura e existência dos candidatos; busca, adequação e qualidade exigem revisão."})
            return int(bool(errors))
        elif args.action == "note":
            emit(note_observation(
                resolve(args.project, root), args.author, args.note,
                parse_fields(args.field), args.output, args.role, args.scenario,
                args.from_run,
            ))
        elif args.action == "record":
            emit(record(resolve(args.project, root), args.kind, args.author, args.note, parse_fields(args.field), args.attach, args.output.absolute()))
        elif args.action == "sfx":
            if args.sfx_action in (None, "summary"):
                emit(sfx_catalog.summarize(root))
            elif args.sfx_action == "search":
                emit(sfx_catalog.search_catalog(args.query, root, limit=args.limit))
            elif args.sfx_action == "copy":
                emit(sfx_catalog.copy_entry(args.id, args.to, root, sources=args.sources))
            elif args.sfx_action == "import":
                emit(sfx_catalog.import_entry(args.file, args.metadata, root))
            elif args.sfx_action == "seed":
                emit(sfx_catalog.seed_catalog(root))
            elif args.sfx_action == "info":
                emit(sfx_catalog.info_entry(args.id, root))
            elif args.sfx_action == "export":
                emit(sfx_catalog.export_entries(args.ids, args.to, root))
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
