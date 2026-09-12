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
    return workspace.default_root()


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
import workspace

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
# Escala de ambição (references/ambition.md): governa quantidade de artefatos e de
# conteúdo, nunca o piso do verbo. É o "register" da skill: o brief declara uma,
# a conversa pode sobrescrever por tarefa, e o harness só lê o campo.
SCALES = ("jam", "product", "aa")
SCALE_KEYWORDS = {
    "jam": ("jam", "conto", "game jam", "protótipo de uma sessão", "prototipo de uma sessao"),
    "product": ("produto", "product"),
    "aa": ("aa", "triple-i", "triple i", "aaa-shaped", "piso de acabamento", "aaa"),
}
SCALE_FIELD = re.compile(r"^\s*(?:[-*]\s+)?(?:escala(?: de ambi[cç][aã]o)?|scale)\s*:\s*(.+?)\s*$", re.IGNORECASE)
# Sub-comandos da skill: o catálogo vive ao lado das referências que ele aponta.
COMMANDS_PATH = FRAMEWORK / "commands/commands.json"
PIN_MARKER = "<!-- game-dev-pinned-skill -->"
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
    # A frase de agora sai em stderr para quem cola. O JSON fica no
    # stdout para quem encana. Falar a frase não executa o jogo.
    if isinstance(value, dict):
        prompt = value.get("prompt")
        if isinstance(prompt, str) and prompt.strip():
            print(prompt, file=sys.stderr, flush=True)
    print(json.dumps(value, ensure_ascii=False, indent=2), flush=True)


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


# O processo já recusa que o hash seja leitura. Sem isto o
# git relatava o HEAD e calava a recusa.
# Identidade no disco não é inspeção.
PROCESS_READING = re.compile(r"prova identidade, não leitura")


def process_refuses_hash_as_reading(text):
    return bool(text and PROCESS_READING.search(text))


def git_identity_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_hash_as_reading(text):
        return "references/process.md"
    return None


def git_summary_scope():
    scope = (
        "Estado do repositório na hora do comando; commits não provam que a mudança "
        "funciona nem que foi revisada."
    )
    if git_identity_source():
        scope += (
            " O disco recusa que o hash seja leitura (`leitura`). "
            "Identidade no disco não é inspeção."
        )
    aged = git_stale_scope()
    if aged:
        scope += aged
    return scope


# O processo já recusa que estados
# salvos estejam atualizados. Sem
# isto o git relatava o HEAD e
# calava a recusa. Snapshot no
# disco não é o estado.
PROCESS_STALE = re.compile(r"estados salvos podem estar desatualizados")


def process_refuses_saved_states_as_current(text):
    return bool(text and PROCESS_STALE.search(text))


def git_stale_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_saved_states_as_current(text):
        return "references/process.md"
    return None


def git_stale_scope():
    if not git_stale_source():
        return None
    return (
        " O disco recusa que nomes de comandos, arquivos ou estados "
        "salvos estejam atualizados (`desatualizados`). "
        "Snapshot no disco não é o estado."
    )


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
        "scope": git_summary_scope(),
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
            projects.append({
                "project": str(path),
                "kind": kind,
                "scope": discover_item_scope(),
            })
        elif depth > 1:
            projects.extend(discover(path, depth - 1))
    return projects


# O README já recusa que listagem de caminho e tipo apague o estado. Sem
# isto o --plain copiava o path e calava a recusa.
# Caminho no disco não é o jogo.
DISCOVER_PLAIN = re.compile(r"listagem de caminho e tipo apagava")


def readme_refuses_plain_listing(text):
    return bool(text and DISCOVER_PLAIN.search(text))


def discover_plain_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_plain_listing(text):
        return "README.md"
    return None


# O README já recusa que a lista
# de chave ausente seja alcance
# observado. Sem isto o item do
# discover copiava o path e
# calava a recusa. Lista no
# disco não é o alcance.
DISCOVER_REACH = re.compile(
    r"Lista de chave ausente não é alcance observado"
)


def readme_refuses_missing_key_list_as_observed_reach(text):
    return bool(text and DISCOVER_REACH.search(text))


def discover_item_reach_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_missing_key_list_as_observed_reach(text):
        return "README.md"
    return None


def discover_item_reach_scope():
    if not discover_item_reach_source():
        return None
    return (
        " O disco recusa que a lista de chave ausente seja alcance observado "
        "(`alcance`). Lista no disco não é o alcance."
    )


def discover_item_scope():
    scope = (
        "Caminho e tipo do jogo. Não lê documento e não distingue o "
        "estado."
    )
    if discover_plain_source():
        scope += (
            " O disco recusa que listagem de caminho e tipo apague o estado "
            "(`listagem`). Caminho no disco não é o jogo."
        )
    reach = discover_item_reach_scope()
    if reach:
        scope += reach
    return scope


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
            reviewed.append(dict(entry, unreadable=str(error), scope=review_item_scope()))
            continue
        areas = found["areas"]
        located = [key for key, area in areas.items() if area["status"] == "candidate_found"]
        drafts = [key for key, area in areas.items() if area["status"] == "draft_only"]
        declaration = bar_declaration(path)
        # Fonte em rascunho não é passo registrado, pelo mesmo motivo que vale no
        # `next`: campo de template em branco não é trabalho interrompido.
        registered = [item for item in found["continuity_sources"] if item["status"] != "draft"]
        try:
            commands, manager = project_commands(path)
            scripts = validators(commands)
        except ValueError:
            commands, manager = {}, None
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
        # Contar constantes e rascunhos não diz qual jogo o `next` abriria.
        # Sem estes sinais, dois destinos com a mesma conta saíam iguais e
        # o laboratório pedia `next` em cada um só para escolher. Sinal no
        # disco não é partida jogada. `access_declared` também esconde a
        # lista: um jogo com legendas e sem pulso saía igual ao starter.
        play = play_command(path, commands, manager)
        missing = [key for key, area in areas.items() if area["status"] == "not_located"]
        observations = feel_observation_items(feel_report)
        noted = bool(observations)
        kind = entry.get("kind")
        signals = {
            "playable_unplayed": fresh_starter_cycle(path, missing, play) and not noted,
            "cycle_craft": bool(noted and craft_commands(path) and not cycle_crafted(path)),
            "feel_unobserved": feel_unobserved_flag(feel_report),
            "playtest_unstructured": playtest_report["unstructured"],
            "playtest_invite": bool(noted and not playtest_report.get("invite")),
            "origins_undeclared": origin_undeclared_paths(origins),
            "origins_contradicts_licensing": origins["contradicts_licensing"],
            "access_missing": access_missing_keys(access_report) if kind else [],
            "save_unversioned": save_unversioned_flag(persist_report),
            "performance_unbudgeted": budget_unbudgeted_flag(perf_report),
            "art_missing": bool(kind) and not art_report["declared"],
            "content_inline": content_inline_flag(content_report),
            "ship_unpacked": ship_unpacked_flag(ship_report),
            "audio_roles_empty": roles_empty_ids(roles),
            "playtest_candidate": playtest_report.get("candidate"),
        }
        named = review_signals_scope()
        if named:
            signals["scope"] = named
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
            origins_embedded=len(origin_embedded_paths(origins)),
            origins_undeclared=len(origin_undeclared_paths(origins)),
            audio_roles=len(roles["roles"]),
            audio_roles_empty=len(roles_empty_ids(roles)),
            feel_constants=len(feel_constant_items(feel_report)),
            feel_observations=len(observations),
            access_declared=access_declared_flag(access_report),
            save_unversioned=save_unversioned_flag(persist_report),
            performance_unbudgeted=budget_unbudgeted_flag(perf_report),
            art_declared=art_report["declared"],
            content_files=len(content_files(path)),
            content_inline=content_inline_flag(content_report),
            ship_unpacked=ship_unpacked_flag(ship_report),
            playtest_expected=playtest_report["expected"],
            playtest_structured=playtest_structured_flag(playtest_report),
            signals=signals,
            scope=review_item_scope(),
        ))
    return {
        "schema_version": 1,
        "root": str(root),
        "project_count": len(projects),
        "reviewed": len(reviewed),
        "projects": reviewed,
        "limit": limit,
        "truncated": review_truncated_reading(len(projects) > limit),
        # Ordenar por urgência exigiria julgar qual jogo importa mais, e nada aqui
        # observa isso. A ordem é a do disco, e a escolha continua sendo de quem lê.
        "order": "caminho, em ordem determinística; o harness não classifica os jogos por urgência",
        "scope": _review_scope(reviewed),
    }


# O package já declara os scripts. Sem isto o
# review lia os validadores e calava o campo.
# Lista no disco não é passo executado.
PACKAGE_SCRIPTS = re.compile(r'"scripts"\s*:\s*\{')


def package_declares_scripts(text):
    return bool(text and PACKAGE_SCRIPTS.search(text))


def review_scripts_source(project):
    project = Path(project)
    path = project / "package.json"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        if path.stat().st_size > 400_000:
            return None
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if package_declares_scripts(text):
        return "package.json"
    return None


def _review_scope(projects):
    scope = (
        "Conta documentos por localização e lê a declaração de degrau de cada projeto. "
        "Relata os mesmos sinais que o `next` usa para o primeiro ciclo, o ofício, "
        "o feel sem recibo, o achado sem forma, o convite, a origem sem recibo "
        "e as lacunas de dimensão. "
        "Não executa jogo "
        "nenhum, não mede acabamento e não diz qual merece atenção primeiro. "
        "Sinal verdadeiro não é partida jogada nem alguém de fora. "
        "Lista de arquivo sem recibo não é licença. "
        "Lista de chave ausente não é alcance observado. "
        "Área localizada é candidato "
        "por nome ou título, não conteúdo aprovado; degrau é o que o projeto afirma de si."
    )
    if any(review_scripts_source(entry.get("project", "")) for entry in projects):
        scope += (
            " O disco declara os scripts (`scripts`). "
            "Lista no disco não é passo executado."
        )
    return scope


# O roteiro já recusa que o documento comprove qualidade. Sem isto o
# item do review copiava a conta e calava a recusa.
# Conta no disco não é acabamento.
PREPRODUCTION_QUALITY = re.compile(r"não comprova qualidade")


def preproduction_refuses_document_quality(text):
    return bool(text and PREPRODUCTION_QUALITY.search(text))


def review_item_quality_source():
    path = FRAMEWORK / "references/preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if preproduction_refuses_document_quality(text):
        return "references/preproduction.md"
    return None


def review_item_scope():
    scope = (
        "Conta deste jogo. Não mede acabamento e não "
        "aprova o documento."
    )
    if review_item_quality_source():
        scope += (
            " O disco recusa que o documento comprove qualidade (`qualidade`). "
            "Conta no disco não é acabamento."
        )
    paper = review_item_authorize_scope()
    if paper:
        scope += paper
    return scope


# A guia já recusa que gerar o
# documento autorize. Sem isto o
# item copiava a conta e calava a
# recusa. Documento no disco não é
# a autorização.
PREPRODUCTION_AUTHORIZE = re.compile(r"gerar o\s+documento não é autorizar")


def guide_refuses_generating_document_as_authorize(text):
    return bool(text and PREPRODUCTION_AUTHORIZE.search(text))


def review_item_authorize_source():
    path = FRAMEWORK / "references" / "preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_generating_document_as_authorize(text):
        return "references/preproduction.md"
    return None


def review_item_authorize_scope():
    if not review_item_authorize_source():
        return ""
    return (
        " O disco recusa que gerar o documento seja autorizar "
        "(`autorizar`). Documento no disco não é a autorização."
    )


# O README já recusa que sinal verdadeiro seja partida jogada. Sem
# isto o signals copiava os flags e calava a recusa.
# Sinal no disco não é alguém de fora.
README_PLAYED = re.compile(r"não é partida jogada")


def readme_refuses_signal_as_played(text):
    return bool(text and README_PLAYED.search(text))


def review_signals_play_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_signal_as_played(text):
        return "README.md"
    return None


def review_signals_scope():
    if not review_signals_play_source():
        return None
    return (
        "O disco recusa que sinal verdadeiro seja partida jogada (`partida`). "
        "Sinal no disco não é alguém de fora."
    )


# O README já recusa que o recorte
# classifique por urgência. Sem
# isto o review relatava o
# truncated e calava a recusa.
# Recorte no disco não é o
# inventário.
REVIEW_URGENCY = re.compile(r"não classifica os jogos por\s+urgência")


def readme_refuses_truncated_as_urgency(text):
    return bool(text and REVIEW_URGENCY.search(text))


def review_truncated_urgency_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_truncated_as_urgency(text):
        return "README.md"
    return None


def review_truncated_urgency_scope():
    if not review_truncated_urgency_source():
        return None
    return (
        " O disco recusa que o recorte classifique por urgência "
        "(`urgência`). Recorte no disco não é o inventário."
    )


def review_truncated_scope():
    scope = (
        "leitura parou no limite. "
        "O review não classifica os jogos por urgência."
    )
    named = review_truncated_urgency_scope()
    if named:
        scope += named
    return scope


def review_truncated_flag(reading):
    truncated = (reading or {}).get("truncated") if isinstance(reading, dict) else reading
    if isinstance(truncated, dict):
        return bool(truncated.get("truncated"))
    return bool(truncated)


def review_truncated_reading(truncated):
    if not truncated:
        return False
    return {
        "truncated": True,
        "scope": review_truncated_scope(),
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
# A prosa já declara o mínimo. Sem isto o
# bar lia a tabela e calava a regra.
# Degrau no disco não é acabamento observado.
BAR_FLOOR_MARK = re.compile(r"mínimo\*{0,2}\s+entre", re.IGNORECASE)


def bar_declares_floor(text):
    return bool(text and BAR_FLOOR_MARK.search(text))


def bar_floor_source(project):
    project = Path(project)
    for name in BAR_SOURCES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 400_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if bar_declares_floor(text):
            return name
    return None


DECLARATION_DEPTH = 4
# `SKIP` serve à descoberta de projetos e exclui `docs`; aqui `docs` é justamente onde procurar.
DECLARATION_SKIP = SKIP - {"docs"}


def declaration_sources(project, fixed):
    """Documentos onde uma declaração (barra, gate) pode viver: os caminhos fixos e os
    homônimos em qualquer subpasta de documentação.

    O Rabisco Boom guarda o QA em `docs/planning/qa.md`; `scan` o localizava e `bar` não,
    então a tabela declarada ficava invisível para o harness. A busca é pelo mesmo nome de
    arquivo (`qa.md`, `devlog.md`…), até quatro níveis, fora das pastas de build.
    """
    # Os caminhos fixos entram sempre, existindo ou não: `sources[0]` é onde `next`
    # manda declarar quando ainda não há tabela. README só conta na raiz — um
    # README por pasta de validação de arte não é documento de declaração.
    names = {Path(item).name.casefold() for item in fixed} - {"readme.md"}
    found = list(fixed)
    if not project.is_dir():
        return found
    base_depth = len(project.parts)
    for current, dirs, files in os.walk(project):
        here = Path(current)
        if len(here.parts) - base_depth >= DECLARATION_DEPTH:
            dirs[:] = []
        dirs[:] = sorted(d for d in dirs if d not in DECLARATION_SKIP and not d.startswith("."))
        for name in sorted(files):
            if name.casefold() in names:
                relative = (here / name).relative_to(project).as_posix()
                if relative not in found:
                    found.append(relative)
    return found


def bar_declaration(project):
    declared = {}
    conflicts = []
    problems = []
    sources_read = declaration_sources(project, BAR_SOURCES)
    for relative in sources_read:
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
        "sources": sources_read,
    }


GATE_ROW = re.compile(
    r"^\|\s*`([\w-]+)`\s*\|\s*`([\w-]+)`\s*\|\s*`(\w+)`\s*\|\s*(.*?)\s*\|\s*$"
)
GATE_SOURCES = ("README.md", "docs/qa.md", "docs/devlog.md", "docs/release.md", "docs/prd.md")
# A tabela já declara o gate. Sem isto o
# gate lia a linha e calava o campo.
# Linha no disco não é passagem concedida.


def gate_declaration(project):
    declared = {}
    problems = []
    sources = []
    for relative in declaration_sources(project, GATE_SOURCES):
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
    problems = [dict(item) for item in declaration["problems"]]
    problem_scope = gate_problem_scope()
    for item in problems:
        item["scope"] = problem_scope
    wanted = (gate,) if gate else tuple(GATES)
    gates = []
    for key in wanted:
        spec = GATES[key]
        rows = declaration["declared"].get(key, {})
        criteria = []
        criterion_scope = gate_criterion_scope()
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
                "scope": criterion_scope,
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
            "held_by_declaration": (
                {
                    "held_by_declaration": True,
                    "scope": gate_held_scope(),
                }
                if not pending else False
            ),
            "scope": gate_item_scope(key),
        })
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "gates": gates,
        "problems": problems,
        "sources": (
            {
                "paths": declaration["sources"],
                "scope": gate_sources_scope(),
            }
            if declaration["sources"] else []
        ),
        "granted": False,
        "guide": str(FRAMEWORK / "references/gates.md"),
        "rule": (
            "Um gate recusa avanço enquanto um critério estiver pendente. Passar, cortar escopo e abandonar "
            "são as três saídas legítimas — abandonar não é falha do gate, é uma das respostas dele. "
            "Critério de `readiness` pendente diz que falta trabalho; `must_meet` pendente pergunta se "
            "isto ainda vale o que custa, e é a essa pergunta que abandonar responde."
        ),
        "scope": _gate_scope(project),
    }


def gate_declares_row(text):
    return bool(text and any(GATE_ROW.match(line) for line in text.splitlines()))


def gate_row_source(project):
    project = Path(project)
    for name in GATE_SOURCES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 400_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if gate_declares_row(text):
            return name
    return None


# O roteiro já recusa que o silêncio seja aprovação. Sem isto o
# item do gate listava o pendente e calava a recusa.
# Linha vazia no disco não é passagem.
GATES_SILENCE = re.compile(r"silêncio não é aprovação")


def gates_refuse_silence(text):
    return bool(text and GATES_SILENCE.search(text))


def gate_item_silence_source():
    path = FRAMEWORK / "references/gates.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gates_refuse_silence(text):
        return "references/gates.md"
    return None


def gate_item_scope(key=None):
    scope = (
        "Critérios do gate segundo a declaração do projeto. "
        "Não observa e não concede passagem."
    )
    if gate_item_silence_source():
        scope += (
            " O disco recusa que o silêncio seja aprovação (`silêncio`). "
            "Linha vazia no disco não é passagem."
        )
    if key == "close" and gate_close_hypothesis_source():
        scope += (
            " O disco recusa que código que compila prove a hipótese "
            "(`hipótese`). Linha no disco não é o experimento."
        )
    if key == "deliver" and gate_deliver_launch_source():
        scope += (
            " O disco recusa que um teste local concluído seja lançamento "
            "(`lançamento`). Linha no disco não é outra máquina."
        )
    if key == "scale" and gate_scale_repeatability_source():
        scope += (
            " O disco recusa que a slice sem repeatability esteja pronta "
            "para ampliar (`repeatability`). Linha no disco não é o próximo trecho."
        )
    return scope


# A guia já recusa que código que compila prove a hipótese criativa.
# Sem isto o gate de encerrar listava o veredito e calava a recusa.
# Linha no disco não é o experimento.
PREPRODUCTION_HYPOTHESIS = FRAMEWORK / "references/preproduction.md"
CLOSE_HYPOTHESIS = re.compile(r"não prova hipótese criativa")


def preproduction_refuses_compile_as_hypothesis(text):
    return bool(text and CLOSE_HYPOTHESIS.search(text))


def gate_close_hypothesis_source():
    path = PREPRODUCTION_HYPOTHESIS
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if preproduction_refuses_compile_as_hypothesis(text):
        return "references/preproduction.md"
    return None


# O fluxo já recusa que um teste local concluído seja lançamento.
# Sem isto o gate de entregar listava o runbook e calava a recusa.
# Linha no disco não é outra máquina.
CREATIVE_WORKFLOW = FRAMEWORK / "references/creative-workflow.md"
DELIVER_LAUNCH = re.compile(r"não significa lançamento")


def workflow_refuses_local_test_as_launch(text):
    return bool(text and DELIVER_LAUNCH.search(text))


def gate_deliver_launch_source():
    path = CREATIVE_WORKFLOW
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if workflow_refuses_local_test_as_launch(text):
        return "references/creative-workflow.md"
    return None


# A receita já recusa que a slice sem repeatability esteja pronta para ampliar.
# Sem isto o gate de ampliar listava o readiness e calava a recusa.
# Linha no disco não é o próximo trecho.
CREATE_REPEATABILITY = FRAMEWORK / "recipes/create.md"
SCALE_REPEATABILITY = re.compile(r"não demonstra\s+repeatability")


def recipe_refuses_slice_without_repeatability(text):
    return bool(text and SCALE_REPEATABILITY.search(text))


def gate_scale_repeatability_source():
    path = CREATE_REPEATABILITY
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_slice_without_repeatability(text):
        return "recipes/create.md"
    return None


# O roteiro já recusa que must_meet seja dispensável. Sem isto o
# critério copiava o tipo e calava a recusa.
# Linha no disco não é passagem.
GATES_GUIDE = FRAMEWORK / "references/gates.md"
GATES_WAIVE = re.compile(r"não é dispensável")


def prose_refuses_must_meet_waiver(text):
    return bool(text and GATES_WAIVE.search(text))


def gate_criterion_waiver_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if prose_refuses_must_meet_waiver(text):
        return "references/gates.md"
    return None


def gate_criterion_scope():
    scope = (
        "Chave, tipo e estado do critério declarado. Não observa "
        "e não concede passagem."
    )
    if gate_criterion_waiver_source():
        scope += (
            " O disco recusa que must_meet seja dispensável (`dispensa`). "
            "Linha no disco não é passagem."
        )
    return scope


# O roteiro já recusa que fora de escopo seja dispensa. Sem
# isto o problema copiava o achado e calava a recusa.
# Linha no disco não é passagem.
GATES_OUT = re.compile(r"Fora de escopo não é dispensa")


def gates_refuse_scope_waiver(text):
    return bool(text and GATES_OUT.search(text))


def gate_problem_scope_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gates_refuse_scope_waiver(text):
        return "references/gates.md"
    return None


def gate_problem_scope():
    scope = (
        "Motivo e fonte do problema de forma. Não observa e não "
        "concede passagem."
    )
    if gate_problem_scope_source():
        scope += (
            " O disco recusa que fora de escopo seja dispensa (`escopo`). "
            "Linha no disco não é passagem."
        )
    return scope


# O roteiro já recusa que a lista de
# entrega seja um gate. Sem isto o
# gate listava o fonte e calava a
# recusa. Linha no disco não é passagem.
GATE_LIST = re.compile(r"lista de entrega com nome pomposo")


def gates_refuse_delivery_list(text):
    return bool(text and GATE_LIST.search(text))


def gate_list_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gates_refuse_delivery_list(text):
        return "references/gates.md"
    return None


def gate_list_scope():
    if not gate_list_source():
        return None
    return (
        " O disco recusa que a lista de entrega seja um gate "
        "(`lista`). Linha no disco não é passagem."
    )


def gate_sources_scope():
    scope = (
        "documento onde o gate pode viver. "
        "Não concede passagem."
    )
    named = gate_list_scope()
    if named:
        scope += named
    return scope


def gate_source_files(project):
    return list(gate_declaration(project)["sources"])


def gate_source_paths(gate):
    sources = (gate or {}).get("sources") or []
    if isinstance(sources, dict):
        return list(sources.get("paths") or [])
    return list(sources)


# O roteiro já recusa que a declaração
# seja passed. Sem isto o gate relatava
# o bool e calava a recusa. Tabela no
# disco não é passagem.
GATE_PASSED = re.compile(r"não `passed`")


def guide_refuses_declaration_as_passed(text):
    return bool(text and GATE_PASSED.search(text))


def gate_held_passed_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_declaration_as_passed(text):
        return "references/gates.md"
    return None


def gate_held_passed_scope():
    if not gate_held_passed_source():
        return None
    return (
        " O disco recusa que a declaração seja passed "
        "(`passou`). Tabela no disco não é passagem."
    )


def gate_held_scope():
    scope = (
        "declaração no disco. "
        "Não concede passagem."
    )
    named = gate_held_passed_scope()
    if named:
        scope += named
    return scope


def gate_held_flag(item):
    held = (item or {}).get("held_by_declaration")
    if isinstance(held, dict):
        return bool(held.get("held_by_declaration"))
    return bool(held)


def _gate_scope(project):
    scope = (
        "Lê a declaração do próprio projeto e confere só a forma dela, relatando em `problems`: gate "
        "desconhecido, critério que não pertence ao gate, estado fora de met/unmet/waived/out_of_scope, "
        "dispensa ou saída de escopo de critério que a prosa não deixa dispensar, met/waived/out_of_scope "
        "sem nada escrito ao lado, e duas linhas discordantes. Não observa o jogo, não executa nada e "
        "**não concede passagem**: `held_by_declaration` diz que o projeto afirma cumprir, não que alguém "
        "conferiu."
    )
    if gate_row_source(project):
        scope += (
            " O disco declara o gate (`gate`). "
            "Linha no disco não é passagem concedida."
        )
    named = gate_abandon_scope()
    if named:
        scope += named
    return scope


# O roteiro já recusa que abandonar
# seja falha do gate. Sem isto o
# gate lia a declaração e calava a
# recusa. Roteiro no disco não é
# passagem.
GATE_ABANDON = re.compile(r"não é falha do gate")


def gates_refuse_abandon_as_failure(text):
    return bool(text and GATE_ABANDON.search(text))


def gate_abandon_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gates_refuse_abandon_as_failure(text):
        return "references/gates.md"
    return None


def gate_abandon_scope():
    if not gate_abandon_source():
        return None
    return (
        " O disco recusa que abandonar seja falha do gate "
        "(`abandono`). Roteiro no disco não é passagem."
    )


CRAFT_ROW = re.compile(r"^\|\s*`([\w-]+)`\s*\|\s*`(\w+)`\s*\|\s*(.*?)\s*\|\s*$")
CRAFT_SOURCES = GATE_SOURCES
# A tabela já declara saída de escopo. Sem isto o
# craft lia a linha e calava o estado.
# Linha no disco não é ofício observado.
CRAFT_OUT_MARK = re.compile(r"`out_of_scope`")


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
            "scope": craft_item_scope(),
        })
    pending = [item["key"] for item in checks if item["state"] in ("undeclared", "unmet")]
    problems = [dict(item) for item in declaration["problems"]]
    problem_scope = craft_problem_scope()
    for item in problems:
        item["scope"] = problem_scope
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "checks": checks,
        "pending": (
            {
                "keys": pending,
                "scope": craft_pending_scope(),
            }
            if pending else []
        ),
        "problems": problems,
        "sources": (
            {
                "paths": declaration["sources"],
                "scope": craft_sources_scope(),
            }
            if declaration["sources"] else []
        ),
        "granted": False,
        "observed": False,
        "guide": str(FRAMEWORK / "references/observable-criteria-research.md"),
        "rule": (
            "Checklist de ofício pergunta se o projeto corresponde ao que ele mesmo "
            "declarou. Não importa limiar externo: paleta, constante de perdão, "
            "definição de percentil, regra de parada. Um dígito aqui seria a escada "
            "afirmando, para este jogo, o que ninguém verificou."
        ),
        "scope": _craft_scope(project),
    }


# A pesquisa já recusa ser escada de acabamento. Sem isto o
# item do craft listava o checklist e calava a recusa.
# Pesquisa no disco não é ofício observado.
CRAFT_LADDER = re.compile(r"não é\s+uma escada")


def research_refuses_ladder(text):
    return bool(text and CRAFT_LADDER.search(text))


# A pesquisa já recusa que o número
# folclórico seja critério observável.
# Sem isto o item do craft listava o
# checklist e calava a recusa.
# Folclore no disco não é o critério.
CRAFT_FOLK = re.compile(r"Número folclórico")


def research_refuses_folk_number_as_observable_criterion(text):
    return bool(text and CRAFT_FOLK.search(text))


def craft_item_folk_source():
    path = FRAMEWORK / "references/observable-criteria-research.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if research_refuses_folk_number_as_observable_criterion(text):
        return "references/observable-criteria-research.md"
    return None


def craft_item_folk_scope():
    if not craft_item_folk_source():
        return None
    return (
        " O disco recusa que o número folclórico seja critério observável "
        "(`folclore`). Folclore no disco não é o critério."
    )


def craft_item_ladder_source():
    path = FRAMEWORK / "references/observable-criteria-research.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if research_refuses_ladder(text):
        return "references/observable-criteria-research.md"
    return None


def craft_item_scope():
    scope = (
        "Checklist de ofício segundo a declaração do projeto. "
        "Não observa e não concede passagem."
    )
    if craft_item_ladder_source():
        scope += (
            " O disco recusa que o checklist seja escada (`escada`). "
            "Pesquisa no disco não é ofício observado."
        )
    folk = craft_item_folk_scope()
    if folk:
        scope += folk
    return scope


# A pesquisa já recusa ser um conjunto de
# gates. Sem isto o craft listava o fonte
# e calava a recusa. Pesquisa no disco
# não é ofício observado.
CRAFT_GATES_SET = re.compile(r"conjunto de gates")


def research_refuses_gates_set(text):
    return bool(text and CRAFT_GATES_SET.search(text))


def craft_set_source():
    path = FRAMEWORK / "references/observable-criteria-research.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if research_refuses_gates_set(text):
        return "references/observable-criteria-research.md"
    return None


def craft_set_scope():
    if not craft_set_source():
        return None
    return (
        " O disco recusa que o levantamento seja um conjunto de gates "
        "(`conjunto`). Pesquisa no disco não é ofício observado."
    )


def craft_sources_scope():
    scope = (
        "documento onde o ofício pode viver. "
        "Não observa o jogo."
    )
    named = craft_set_scope()
    if named:
        scope += named
    return scope


def craft_source_files(project):
    return list(craft_declaration(project)["sources"])


def craft_source_paths(craft):
    sources = (craft or {}).get("sources") or []
    if isinstance(sources, dict):
        return list(sources.get("paths") or [])
    return list(sources)


# A pesquisa já recusa que a pendência
# seja medição em jogo. Sem isto o
# craft listava o checklist e calava
# a recusa. Pesquisa no disco não é
# ofício observado.
CRAFT_MEASURE = re.compile(r"Não é medição em jogo")


def research_refuses_pending_as_measurement(text):
    return bool(text and CRAFT_MEASURE.search(text))


def craft_pending_measure_source():
    path = FRAMEWORK / "references/observable-criteria-research.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if research_refuses_pending_as_measurement(text):
        return "references/observable-criteria-research.md"
    return None


def craft_pending_measure_scope():
    if not craft_pending_measure_source():
        return None
    return (
        " O disco recusa que a pendência seja medição em jogo "
        "(`medição`). Pesquisa no disco não é ofício observado."
    )


def craft_pending_scope():
    scope = (
        "checklist ainda undeclared ou unmet. "
        "Não observa o jogo."
    )
    named = craft_pending_measure_scope()
    if named:
        scope += named
    return scope


def craft_pending_keys(craft):
    pending = (craft or {}).get("pending") or []
    if isinstance(pending, dict):
        return list(pending.get("keys") or [])
    return list(pending)


# A pesquisa já recusa que o número sem definição seja
# critério. Sem isto o problema copiava o achado e
# calava a recusa. Pesquisa no disco não é ofício.
CRAFT_RESEARCH = FRAMEWORK / "references/observable-criteria-research.md"
CRAFT_DEFINITION = re.compile(r"sem definição declarada não é critério")


def research_refuses_undefined_number(text):
    return bool(text and CRAFT_DEFINITION.search(text))


def craft_problem_definition_source():
    path = CRAFT_RESEARCH
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if research_refuses_undefined_number(text):
        return "references/observable-criteria-research.md"
    return None


def craft_problem_scope():
    scope = (
        "Motivo e fonte do problema de forma. Não observa e não "
        "concede passagem."
    )
    if craft_problem_definition_source():
        scope += (
            " O disco recusa que o número sem definição seja critério (`definição`). "
            "Pesquisa no disco não é ofício observado."
        )
    return scope


def craft_declares_out(text):
    return bool(text and CRAFT_OUT_MARK.search(text))


def craft_out_source(project):
    project = Path(project)
    for name in CRAFT_SOURCES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 400_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if craft_declares_out(text):
            return name
    return None


def _craft_scope(project):
    scope = (
        "Lê a declaração do próprio projeto e confere só a forma. Não observa o "
        "jogo, não mede contraste nem tempo de quadro e **não concede passagem**. "
        "`observed` é sempre falso: tabela bem formada e otimista sai intacta."
    )
    if craft_out_source(project):
        scope += (
            " O disco declara a saída de escopo (`out_of_scope`). "
            "Linha no disco não é ofício observado."
        )
    named = craft_precision_scope()
    if named:
        scope += named
    skip = craft_skip_scope()
    if skip:
        scope += skip
    envoy = craft_delegate_scope()
    if envoy:
        scope += envoy
    return scope


# O craft já recusa que shape
# confirmado seja licença para
# pular feel e áudio. Sem isto o
# craft lia a declaração e calava
# a recusa. Confirmação no disco
# não é o ofício.
CRAFT_SKIP = re.compile(r"não é licença para pular feel e áudio")


def craft_refuses_shape_as_license_to_skip(text):
    return bool(text and CRAFT_SKIP.search(text))


def craft_skip_source():
    path = FRAMEWORK / "commands" / "craft.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if craft_refuses_shape_as_license_to_skip(text):
        return "commands/craft.md"
    return None


def craft_skip_scope():
    if not craft_skip_source():
        return ""
    return (
        " O disco recusa que shape confirmado seja licença para pular "
        "feel e áudio (`pular`). Confirmação no disco não é o ofício."
    )


# O craft já recusa que uma
# confirmação autorize delegar.
# Sem isto o craft lia a
# declaração e calava a recusa.
# Confirmação no disco não é
# delegar.
CRAFT_DELEGATE = re.compile(r"não autoriza publicar nem delegar")


def craft_refuses_confirmation_as_delegate(text):
    return bool(text and CRAFT_DELEGATE.search(text))


def craft_delegate_source():
    path = FRAMEWORK / "commands" / "craft.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if craft_refuses_confirmation_as_delegate(text):
        return "commands/craft.md"
    return None


def craft_delegate_scope():
    if not craft_delegate_source():
        return None
    return (
        " O disco recusa que uma confirmação autorize delegar "
        "(`delegar`). Confirmação no disco não é delegar."
    )


# O mapa já recusa que o número com
# casa decimal e sem origem seja mais
# preciso. Sem isto o craft lia a
# declaração e calava a recusa.
# Mapa no disco não é ofício observado.
SOURCES_PRECISION = re.compile(
    r"número com casa decimal e sem origem não é mais preciso"
)


def map_refuses_unsourced_decimal(text):
    return bool(text and SOURCES_PRECISION.search(text))


def craft_precision_source():
    path = FRAMEWORK / "references/sources.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if map_refuses_unsourced_decimal(text):
        return "references/sources.md"
    return None


def craft_precision_scope():
    if not craft_precision_source():
        return None
    return (
        " O disco recusa que o número com casa decimal e sem origem "
        "seja mais preciso (`preciso`). Mapa no disco não é ofício observado."
    )


# Papéis de áudio: o starter declara SOUNDS e, neste recorte, já traz
# arquivo por papel. Mixagem AAA não é pasta cheia — é cada papel do
# verbo ter arquivo ou silêncio deliberado (papel removido). O harness
# só vê declaração e arquivo no disco. Não ouve, não aprova estética e
# não confunde arquivo presente com mixagem boa.
ROLE_FOLDERS = ("public/sfx", "assets/sfx", "sfx", "audio", "public/audio")
ROLE_EXTENSIONS = {".wav", ".ogg", ".mp3", ".flac", ".m4a", ".webm"}
SOUNDS_OPEN = re.compile(r"(?:export\s+)?const\s+SOUNDS\s*=\s*\{")
ROLE_OBJECT = re.compile(r"^([A-Za-z_][\w]*)\s*:\s*\{")
# O mixer já abaixa a cama no aviso. Sem isto o roles
# lia o papel e calava o duck. Número no disco não é mix ouvida.
ROLE_DUCK = re.compile(r"\bduckMs\s*:\s*(\d+)")
ROLE_CODE_SUFFIXES = {".js", ".mjs", ".ts"}
ROLE_MANIFESTS = ("sounds.json", "audio-roles.json", "docs/audio-roles.json")
ROLE_WALK_SKIP = {
    "node_modules", "dist", "build", ".git", "__pycache__", "coverage",
    "library", "temp", ".venv", "venv", "target",
}


def role_duck_ms(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if isinstance(value, float) and (not value == value or not value.is_integer()):
        return None
    if value < 0:
        return None
    return int(value)


def _role_entry(name, duck=None):
    entry = {"id": name}
    if duck is not None:
        entry["duckMs"] = duck
    return entry


def _role_entries_from_manifest(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(data, list):
        return [_role_entry(item) for item in data if isinstance(item, str) and item.strip()]
    if not isinstance(data, dict):
        return []
    listed = data.get("roles")
    if isinstance(listed, list):
        entries = []
        for item in listed:
            if isinstance(item, str) and item.strip():
                entries.append(_role_entry(item))
                continue
            if not isinstance(item, dict):
                continue
            name = item.get("id") or item.get("role") or item.get("key")
            if not isinstance(name, str) or not name.strip():
                continue
            entries.append(_role_entry(name.strip(), role_duck_ms(item.get("duckMs"))))
        return entries
    return [
        _role_entry(key, role_duck_ms(value.get("duckMs")) if isinstance(value, dict) else None)
        for key, value in data.items()
        if key != "schema_version" and isinstance(value, (dict, str, bool, int))
    ]


def _role_entries_from_code(text):
    start = SOUNDS_OPEN.search(text)
    if not start:
        return []
    entries = []
    current = None
    depth = 0
    for line in text[start.end():].splitlines():
        stripped = line.strip()
        if current is None:
            if stripped.startswith("}"):
                break
            match = ROLE_OBJECT.match(stripped)
            if not match:
                continue
            found = ROLE_DUCK.search(stripped)
            current = _role_entry(
                match.group(1),
                role_duck_ms(int(found.group(1))) if found else None,
            )
            depth = stripped.count("{") - stripped.count("}")
            if depth <= 0:
                entries.append(current)
                current = None
            continue
        found = ROLE_DUCK.search(stripped)
        if found and "duckMs" not in current:
            duck = role_duck_ms(int(found.group(1)))
            if duck is not None:
                current["duckMs"] = duck
        depth += stripped.count("{") - stripped.count("}")
        if depth <= 0:
            entries.append(current)
            current = None
    return entries


def _role_names_from_code(text):
    return [item["id"] for item in _role_entries_from_code(text)]


def declared_sound_roles(project, max_files=80, max_bytes=64000):
    found = []
    sources = []
    seen = set()

    def add(entries, source):
        added = False
        for entry in entries:
            name = entry["id"]
            if name in seen:
                continue
            seen.add(name)
            found.append(entry)
            added = True
        if added:
            sources.append(source)

    for relative in ROLE_MANIFESTS:
        path = project / relative
        if not path.is_file() or path.is_symlink():
            continue
        add(_role_entries_from_manifest(path), relative)
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
            entries = _role_entries_from_code(text)
            if entries:
                add(entries, path.relative_to(project).as_posix())
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


# A receita já soma as vozes. Sem isto o roles
# lia SOUNDS e calava o mix. Soma no disco não é
# mix ouvida.
MIX_FILES = ("tools/mix.mjs", "tools/mix.js", "tools/mix.py")
MIX_SUM = re.compile(r"soma as vozes", re.IGNORECASE)


def mix_sums_voices(text):
    return bool(text and MIX_SUM.search(text))


def mix_sum_source(project):
    project = Path(project)
    for name in MIX_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if mix_sums_voices(text):
            return name
    return None


# A receita já desloca a voz. Sem isto o roles
# lia SOUNDS e calava o sfx. Arquivo no disco
# não é mix ouvida.
SFX_FILES = (
    "tools/design-sfx.py",
    "tools/sfx.py",
    "tools/design-sfx.js",
    "tools/sfx.js",
)
SFX_SHIFT = re.compile(r"desloca a voz", re.IGNORECASE)


def sfx_shifts_voice(text):
    return bool(text and SFX_SHIFT.search(text))


def sfx_shift_source(project):
    project = Path(project)
    for name in SFX_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if sfx_shifts_voice(text):
            return name
    return None


# O tool já lê o PCM. Sem isto o roles
# somava o mix e calava o wav. Bytes no
# disco não são mix ouvida.
WAV_FILES = ("tools/wav.mjs", "tools/wav.js", "tools/wav.py")
WAV_READ = re.compile(r"Não decodifica compressão e não ouve", re.IGNORECASE)


def wav_reads_pcm(text):
    return bool(text and WAV_READ.search(text))


def wav_read_source(project):
    project = Path(project)
    for name in WAV_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if wav_reads_pcm(text):
            return name
    return None


# A receita já recusa que áudio AAA seja quantidade de arquivos. Sem isto o
# item copiava a lista e calava a recusa.
# Lista no disco não é mix.
AUDIO_RECIPE = FRAMEWORK / "recipes/audio.md"
AUDIO_QUANTITY = re.compile(r"não é quantidade de arquivos")


def audio_refuses_file_quantity(text):
    return bool(text and AUDIO_QUANTITY.search(text))


def role_item_quantity_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audio_refuses_file_quantity(text):
        return "recipes/audio.md"
    return None


def role_item_scope():
    scope = (
        "Id, arquivos e estado do papel. Não toca o som e não "
        "aprova a mixagem."
    )
    if role_item_quantity_source():
        scope += (
            " O disco recusa que áudio AAA seja quantidade de arquivos (`quantidade`). "
            "Lista no disco não é mix."
        )
    return scope


# A receita já recusa que o número no panner seja mix. Sem isto o
# papel do x do campo copiava o id e calava a recusa.
# Número no disco não é mix.
AUDIO_PANNER = re.compile(r"Número no panner não é mix")
PANNER_ROLES = frozenset({
    "collect", "missed", "graze", "hit", "dash", "land", "bank", "over",
})


def recipe_refuses_panner_number_as_mix(text):
    return bool(text and AUDIO_PANNER.search(text))


def role_panner_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_panner_number_as_mix(text):
        return "recipes/audio.md"
    return None


def role_panner_scope():
    if not role_panner_source():
        return None
    return (
        "O disco recusa que o número no panner seja mix "
        "(`panner`). Número no disco não é mix."
    )


# A receita já recusa que retomar, fila e paralelo sejam mix. Sem isto o
# roles lia SOUNDS e calava a recusa.
# Pedido no disco não é mix.
AUDIO_RESUME = re.compile(r"Retomar,\s+fila e\s+paralelo não são mix")


def recipe_refuses_resume_queue_parallel_as_mix(text):
    return bool(text and AUDIO_RESUME.search(text))


def roles_resume_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_resume_queue_parallel_as_mix(text):
        return "recipes/audio.md"
    return None


def roles_resume_scope():
    if not roles_resume_source():
        return None
    return (
        "O disco recusa que retomar, fila e paralelo sejam mix "
        "(`retomar`). Pedido no disco não é mix."
    )


# A receita já recusa que o heap sozinho
# meça PCM ou VRAM. Sem isto o roles
# nomeava o PCM e calava a recusa.
# Contador no disco não é o mix.
AUDIO_HEAP = re.compile(r"heap JavaScript sozinho não mede PCM")


def recipe_refuses_heap_as_pcm(text):
    return bool(text and AUDIO_HEAP.search(text))


def roles_heap_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_heap_as_pcm(text):
        return "recipes/performance.md"
    return None


def roles_heap_scope():
    if not roles_heap_source():
        return None
    return (
        "O disco recusa que o heap JavaScript sozinho meça PCM ou VRAM "
        "(`heap`). Contador no disco não é o mix."
    )


# A receita já recusa que desconectar,
# liberar e fechar comprovem coleta
# imediata. Sem isto o roles listava
# o fonte e calava a recusa. Sinal no
# disco não é o sistema.
AUDIO_IMMEDIATE = re.compile(r"comprova coleta imediata")


def recipe_refuses_signals_as_immediate_gc(text):
    return bool(text and AUDIO_IMMEDIATE.search(text))


def roles_immediate_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_signals_as_immediate_gc(text):
        return "recipes/audio.md"
    return None


def roles_immediate_scope():
    if not roles_immediate_source():
        return None
    return (
        " O disco recusa que desconectar, liberar e fechar comprovem "
        "coleta imediata (`imediata`). Sinal no disco não é o sistema."
    )


def roles_sources_scope():
    scope = (
        "arquivo de papel no disco. "
        "Não ouve o mix."
    )
    named = roles_immediate_scope()
    if named:
        scope += named
    return scope


def roles_source_files(project):
    _entries, sources = declared_sound_roles(project)
    return sources


# A receita já recusa que o arquivo
# ausente seja silêncio deliberado.
# Sem isto o roles listava o vazio
# e calava a recusa. Lista no disco
# não é mix.
AUDIO_ABSENT = re.compile(r"Arquivo ausente é lacuna do verbo,\s+não silêncio deliberado")


def recipe_refuses_absent_as_deliberate_silence(text):
    return bool(text and AUDIO_ABSENT.search(text))


def roles_empty_absent_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_absent_as_deliberate_silence(text):
        return "recipes/audio.md"
    return None


def roles_empty_absent_scope():
    if not roles_empty_absent_source():
        return None
    return (
        " O disco recusa que o arquivo ausente seja silêncio deliberado "
        "(`ausente`). Lista no disco não é mix."
    )


def roles_empty_scope():
    scope = (
        "papel declarado sem arquivo. "
        "Não ouve o mix."
    )
    named = roles_empty_absent_scope()
    if named:
        scope += named
    return scope


def roles_empty_ids(roles):
    empty = (roles or {}).get("empty") or []
    if isinstance(empty, dict):
        return list(empty.get("ids") or [])
    return list(empty)


# A receita já recusa que o catálogo
# completo entre. Sem isto o roles
# relatava o acervo e calava a
# recusa. Acervo no disco não é mix.
AUDIO_CATALOG = re.compile(r"Catálogo completo não entra")


def recipe_refuses_complete_catalog_as_entering(text):
    return bool(text and AUDIO_CATALOG.search(text))


def roles_catalog_enter_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_complete_catalog_as_entering(text):
        return "recipes/audio.md"
    return None


def roles_catalog_enter_scope():
    if not roles_catalog_enter_source():
        return None
    return (
        " O disco recusa que o catálogo completo entre "
        "(`entra`). Acervo no disco não é mix."
    )


def roles_catalog_exists_scope():
    scope = (
        "acervo no disco. "
        "Não é mix ouvida."
    )
    named = roles_catalog_enter_scope()
    if named:
        scope += named
    return scope


def roles_catalog_exists_flag(reading):
    catalog_exists = (reading or {}).get("catalog_exists")
    if isinstance(catalog_exists, dict):
        return bool(catalog_exists.get("catalog_exists"))
    return bool(catalog_exists)


def roles_reading(project, root=None):
    project = Path(project)
    entries, sources = declared_sound_roles(project)
    roles = []
    for entry in entries:
        files = role_files(project, entry["id"])
        row = {
            "id": entry["id"],
            "files": files,
            "state": "present" if files else "empty",
        }
        if "duckMs" in entry:
            row["duckMs"] = entry["duckMs"]
        row["scope"] = role_item_scope()
        if entry["id"] in PANNER_ROLES:
            named = role_panner_scope()
            if named:
                row["scope"] += " " + named
        roles.append(row)
    empty = [item["id"] for item in roles if item["state"] == "empty"]
    if empty:
        empty = {
            "ids": empty,
            "scope": roles_empty_scope(),
        }
    if sources:
        sources = {
            "paths": sources,
            "scope": roles_sources_scope(),
        }
    catalog = sfx_catalog.catalog_dir(root)
    scope = (
        "Lê `const SOUNDS` e manifestos de papéis, e cruza com arquivos em "
        "public/sfx e equivalentes. Nomeia o `duckMs` que a tabela já "
        "declara. Sem duck a chave some. Nomear não é mix ouvida. Não toca "
        "o som, não valida mixagem e não aprova estética. `heard` e "
        "`approved` são sempre falsos: arquivo presente não é mixagem ouvida."
    )
    if mix_sum_source(project):
        scope += (
            " O disco soma as vozes (`mix`). Soma no disco não é mix ouvida."
        )
    if sfx_shift_source(project):
        scope += (
            " O disco desloca a voz (`sfx`). Arquivo no disco não é mix ouvida."
        )
    if wav_read_source(project):
        scope += (
            " O disco lê o PCM (`wav`). Bytes no disco não são mix ouvida."
        )
    named = roles_resume_scope()
    if named:
        scope += " " + named
    heap = roles_heap_scope()
    if heap:
        scope += " " + heap
    catalog_exists = (catalog / "catalog.json").is_file()
    if catalog_exists:
        catalog_exists = {
            "catalog_exists": True,
            "scope": roles_catalog_exists_scope(),
        }
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "roles": roles,
        "empty": empty,
        "sources": sources,
        "catalog_exists": catalog_exists,
        "heard": False,
        "approved": False,
        "guide": str(FRAMEWORK / "recipes/audio.md"),
        "rule": (
            "Papel declarado sem arquivo é lacuna do verbo, não silêncio deliberado. "
            "Silêncio deliberado é o papel ausente da declaração."
        ),
        "scope": scope,
    }


# O processo já recusa o reuso automático. Sem isto o
# roles --fill sugeria o primeiro match e calava a recusa.
# Arquivo no disco não é licença.
PROCESS_REUSE_GUIDE = FRAMEWORK / "references/process.md"
PROCESS_REUSE = re.compile(r"não é automaticamente reutilizável")


def process_refuses_automatic_reuse(text):
    return bool(text and PROCESS_REUSE.search(text))


def roles_reuse_source():
    path = PROCESS_REUSE_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_automatic_reuse(text):
        return "references/process.md"
    return None


def roles_fill_scope():
    scope = (
        "Para cada papel vazio, busca o id no acervo shared/sfx e, com "
        "`--apply`, copia para public/sfx com o nome do papel. Sem "
        "acervo, ou sem id que case, nomeia o stem do starter que casa "
        "(`kind: starter`) e o `--apply` também o copia com créditos. "
        "Se o recibo já está e o WAV sumiu, recoloca os bytes quando "
        "origem e licença casam; recibo diferente recusa. "
        "`sfx copy` / `sfx export` continuam o caminho explícito. "
        "`heard` é sempre falso."
    )
    if roles_reuse_source():
        scope += (
            " O disco recusa o reuso automático (`reuso`). "
            "Arquivo no disco não é licença."
        )
    return scope


# A receita já recusa que o apply
# seja mix ouvido. Sem isto o
# roles --fill relatava o applied
# e calava a recusa. Cópia no
# disco não é mix.
AUDIO_APPLY_HEARD = re.compile(r"--apply` não é mix ouvido")


def recipe_refuses_apply_as_heard_mix(text):
    return bool(text and AUDIO_APPLY_HEARD.search(text))


def roles_fill_applied_mix_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_apply_as_heard_mix(text):
        return "recipes/audio.md"
    return None


def roles_fill_applied_mix_scope():
    if not roles_fill_applied_mix_source():
        return None
    return (
        " O disco recusa que o apply seja mix ouvido "
        "(`aplica`). Cópia no disco não é mix."
    )


def roles_fill_applied_scope():
    scope = (
        "--apply copiou o stem para o papel. "
        "Não é mix ouvido."
    )
    named = roles_fill_applied_mix_scope()
    if named:
        scope += named
    return scope


def roles_fill_applied_flag(reading):
    applied = (reading or {}).get("applied") if isinstance(reading, dict) else reading
    if isinstance(applied, dict):
        return bool(applied.get("applied"))
    return bool(applied)


def roles_fill_applied_reading(applied):
    if not applied:
        return False
    return {
        "applied": True,
        "scope": roles_fill_applied_scope(),
    }


def roles_fill(project, root=None, apply=False):
    project = Path(project)
    reading = roles_reading(project, root)
    suggestions = []
    copied = []
    empty_ids = roles_empty_ids(reading)
    catalog_exists = roles_catalog_exists_flag(reading)
    for role in empty_ids:
        match = None
        if catalog_exists:
            try:
                found = sfx_catalog.search_catalog(role, root, limit=1)
            except ValueError:
                found = {"matches": []}
            if found["matches"]:
                hit = found["matches"][0]
                match = {
                    "id": hit["id"],
                    "title": hit["title"],
                    "src": hit["src"],
                    "kind": "catalog",
                }
        if match is None:
            local = sfx_catalog.find_local_stem(role)
            if local:
                match = {
                    "id": local["key"],
                    "key": local["key"],
                    "title": local.get("title") or local["key"],
                    "src": local["src"],
                    "license": local.get("license"),
                    "origin": local.get("origin"),
                    "kind": "starter",
                    "heard": False,
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
        "empty": empty_ids,
        "catalog_exists": catalog_exists,
        "suggestions": suggestions,
        "applied": roles_fill_applied_reading(bool(apply)),
        "copied": copied,
        "heard": False,
        "approved": False,
        "guide": str(FRAMEWORK / "recipes/audio.md"),
        "rule": (
            "Primeiro resultado da busca não é o som certo e não é mixagem "
            "ouvida. `--apply` copia o id do acervo ou o stem do starter "
            "com créditos. Não toca e não aprova."
        ),
        "scope": roles_fill_scope(),
    }


# Feel: o starter nomeia perdão, graça e hitstop no CONFIG. Até aqui o harness
# só via a tabela de ofício, não as constantes. A pergunta é estreita — o
# projeto declara janelas de feel, e alguém registrou uma observação no disco?
# O harness não joga e não atribui peso.
CONFIG_OPEN = re.compile(r"(?:export\s+)?const\s+CONFIG\s*=\s*\{")
CONFIG_NESTED = re.compile(r"^([A-Za-z_][\w]*)\s*:\s*\{")
CONFIG_LEAF = re.compile(r"^([A-Za-z_][\w]*)\s*:\s*(-?[\d.]+)\s*,?\s*(?://\s*(.*))?")
FEEL_KEY = re.compile(
    r"(buffer|invuln|pad|reach|lock|hitstop|shake|squash|punch|grace|forgiv|cooldown|recovery|dashticks|flash|telegraph|windup|dashspeed|\bspeed\b)",
    re.IGNORECASE,
)
FEEL_NOTE = re.compile(r"(perd[aã]o|gra[cç]a|contato|peso|feel|juice)", re.IGNORECASE)
# O coil do dash já veste a corrente. Sem isto o feel
# lia squash e calava o rumo que o corpo já marca.
# Traço no disco não é peso percebido.
HEADING_MARK = re.compile(
    r"if\s*\(\s*winding\s*\)[\s\S]{0,1200}?\.lineTo\([\s\S]{0,240}?\.stroke\("
)


def dash_aims_heading(text):
    return bool(text and HEADING_MARK.search(text))


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


# A receita já recusa que o autor sugerido seja quem jogou. Sem isto o
# item copiava o autor e calava a recusa.
# Recibo no disco não é sessão.
FEEL_RECIPE = FRAMEWORK / "recipes/feel.md"
FEEL_AUTHOR = re.compile(r"autor sugerido no comando não é quem jogou")


def recipe_refuses_suggested_author(text):
    return bool(text and FEEL_AUTHOR.search(text))


def observation_author_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_suggested_author(text):
        return "recipes/feel.md"
    return None


def observation_item_scope():
    scope = (
        "Caminho, autor e nota do recibo. Não joga e não "
        "atribui peso percebido."
    )
    if observation_author_source():
        scope += (
            " O disco recusa que o autor sugerido seja quem jogou (`autor`). "
            "Recibo no disco não é sessão."
        )
    markup = observation_dom_scope()
    if markup:
        scope += markup
    talk = observation_session_scope()
    if talk:
        scope += talk
    return scope


# A receita já recusa que o
# texto no DOM seja direção
# observada. Sem isto o item
# copiava a nota e calava a
# recusa. Texto no DOM não é
# a direção.
A11Y_DOM = re.compile(r"Texto no DOM\s+não é direção observada")


def recipe_refuses_dom_text_as_observed_direction(text):
    return bool(text and A11Y_DOM.search(text))


def observation_dom_source():
    path = FRAMEWORK / "recipes/accessibility.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_dom_text_as_observed_direction(text):
        return "recipes/accessibility.md"
    return None


def observation_dom_scope():
    if not observation_dom_source():
        return None
    return (
        " O disco recusa que o texto no DOM seja direção observada "
        "(`dom`). Texto no DOM não é a direção."
    )


# A receita já recusa que o
# texto no DOM seja sessão.
# Sem isto o item copiava a
# nota e calava a recusa.
# Texto no DOM não é a sessão.
A11Y_SESSION = re.compile(r"Texto no\s+DOM não é sessão")


def recipe_refuses_dom_text_as_session(text):
    return bool(text and A11Y_SESSION.search(text))


def observation_session_source():
    path = FRAMEWORK / "recipes/accessibility.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_dom_text_as_session(text):
        return "recipes/accessibility.md"
    return None


def observation_session_scope():
    if not observation_session_source():
        return None
    return (
        " O disco recusa que o texto no DOM seja sessão "
        "(`sessão`). Texto no DOM não é a sessão."
    )


# A receita já recusa que o soltar
# no disco seja sessão observada.
# Sem isto o feel listava o recibo
# e calava a recusa. Arquivo no
# disco não é a sessão.
FEEL_RELEASE = re.compile(r"Soltar no disco não é\s+sessão observada")


def recipe_refuses_disk_release_as_session(text):
    return bool(text and FEEL_RELEASE.search(text))


def feel_release_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_disk_release_as_session(text):
        return "recipes/feel.md"
    return None


def feel_release_scope():
    if not feel_release_source():
        return None
    return (
        " O disco recusa que o soltar no disco seja sessão observada "
        "(`soltar`). Arquivo no disco não é a sessão."
    )


# A receita já recusa que animar
# demais substitua a regra. Sem
# isto o feel listava o recibo
# e calava a recusa. Animar no
# disco não é a regra.
FEEL_ANIMATE = re.compile(r"Animar demais não substitui a regra")


def recipe_refuses_over_animating_as_the_rule(text):
    return bool(text and FEEL_ANIMATE.search(text))


def feel_observations_animate_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_over_animating_as_the_rule(text):
        return "recipes/feel.md"
    return None


def feel_observations_animate_scope():
    if not feel_observations_animate_source():
        return None
    return (
        " O disco recusa que animar demais substitua a regra "
        "(`animar`). Animar no disco não é a regra."
    )


# A receita já recusa que a
# recovery invisível ou
# infinita seja o retorno.
# Sem isto o feel listava o
# recibo e calava a recusa.
# Recovery no disco não é o
# controle.
FEEL_JUST = re.compile(r"Recovery\s+invisível ou infinito quebra confiança")


def recipe_refuses_invisible_recovery_as_return(text):
    return bool(text and FEEL_JUST.search(text))


def feel_observations_just_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_invisible_recovery_as_return(text):
        return "recipes/feel.md"
    return None


def feel_observations_just_scope():
    if not feel_observations_just_source():
        return None
    return (
        " O disco recusa que a recovery invisível ou infinita seja o retorno "
        "(`justo`). Recovery no disco não é o controle."
    )


def feel_observations_scope():
    scope = (
        "recibo de observação no disco. "
        "Não joga e não atribui peso percebido."
    )
    named = feel_release_scope()
    if named:
        scope += named
    motion = feel_observations_animate_scope()
    if motion:
        scope += motion
    fair = feel_observations_just_scope()
    if fair:
        scope += fair
    return scope


def feel_observation_items(feel):
    observations = (feel or {}).get("observations") or []
    if isinstance(observations, dict):
        return list(observations.get("items") or [])
    return list(observations)


# O README já recusa que a constante
# nomeada seja peso percebido. Sem
# isto o feel listava o CONFIG e
# calava a recusa. Número no disco
# não é o verbo.
FEEL_WEIGHT = re.compile(r"Constante nomeada não é peso percebido")


def readme_refuses_constant_as_weight(text):
    return bool(text and FEEL_WEIGHT.search(text))


def feel_constants_weight_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_constant_as_weight(text):
        return "README.md"
    return None


def feel_constants_weight_scope():
    if not feel_constants_weight_source():
        return None
    return (
        " O disco recusa que a constante nomeada seja peso percebido "
        "(`peso`). Número no disco não é o verbo."
    )


def feel_constants_scope():
    scope = (
        "constantes nomeadas no disco. "
        "Não atribui peso percebido."
    )
    named = feel_constants_weight_scope()
    if named:
        scope += named
    windup = feel_constants_window_scope()
    if windup:
        scope += windup
    return scope


# A receita já recusa que o coil
# seja janela de hit. Sem isto o
# feel listava o CONFIG e calava
# a recusa. Coil no disco não é
# a janela.
FEEL_WINDOW = re.compile(r"o coil não é janela de hit")


def recipe_refuses_coil_as_hit_window(text):
    return bool(text and FEEL_WINDOW.search(text))


def feel_constants_window_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_coil_as_hit_window(text):
        return "recipes/feel.md"
    return None


def feel_constants_window_scope():
    if not feel_constants_window_source():
        return ""
    return (
        " O disco recusa que o coil seja janela de hit "
        "(`janela`). Coil no disco não é a janela."
    )


def feel_constant_items(feel):
    constants = (feel or {}).get("constants") or []
    if isinstance(constants, dict):
        return list(constants.get("items") or [])
    return list(constants)


# A receita já recusa que o valor seja constante universal. Sem isto o
# item copiava o número e calava a recusa.
# Número no disco não é lei.
FEEL_UNIVERSAL = re.compile(r"não\s+constantes universais")


def recipe_refuses_universal_constants(text):
    return bool(text and FEEL_UNIVERSAL.search(text))


def feel_constant_universal_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_universal_constants(text):
        return "recipes/feel.md"
    return None


def feel_constant_scope():
    scope = (
        "Chave e valor da constante nomeada. Não joga e não "
        "atribui peso percebido."
    )
    if feel_constant_universal_source():
        scope += (
            " O disco recusa que o valor seja constante universal (`universais`). "
            "Número no disco não é lei."
        )
    if feel_constant_position_source():
        scope += (
            " O disco recusa que velocidade não nula prove a posição "
            "(`posição`). Número no disco não é a pose."
        )
    return scope


# A receita já recusa que velocidade não nula prove a posição.
# Sem isto o item copiava o número e calava a recusa.
# Número no disco não é a pose.
FEEL_POSITION = re.compile(r"não prova que a posição foi integrada")


def recipe_refuses_velocity_as_position(text):
    return bool(text and FEEL_POSITION.search(text))


def feel_constant_position_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_velocity_as_position(text):
        return "recipes/feel.md"
    return None


# A receita já recusa que os testes demonstrem
# qualidade artística. Sem isto o then do feel
# apontava play e calava a recusa. Número no
# disco não é direção.
FEEL_ARTISTIC = re.compile(r"não demonstram qualidade artística")


def recipe_refuses_tests_as_artistic_quality(text):
    return bool(text and FEEL_ARTISTIC.search(text))


def feel_then_artistic_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_tests_as_artistic_quality(text):
        return "recipes/feel.md"
    return None


def feel_then_scope():
    if not feel_then_artistic_source():
        return None
    return (
        "O disco recusa que esses testes demonstrem qualidade artística "
        "(`artística`). Número no disco não é direção."
    )


def feel_then(project):
    project = Path(project)
    then = {"note": note_command(project)}
    try:
        scripts, manager = project_commands(project)
    except (OSError, ValueError):
        scripts, manager = {}, None
    play = play_command(project, scripts, manager)
    if play:
        then["play"] = play
    # O play/guide já nomeiam a partida do last-run.
    # Sem isto o feel mandava só o serve nu — a seed
    # do candidato ficava no disco e o comando calava.
    # Endereço no disco não é peso percebido.
    href = seed_href(project)
    if href:
        then["seed"] = href
        then["invite"] = invite_href(project)
    return then


# A receita já recusa que captura no
# disco seja sessão observada. Sem
# isto o feel listava o fonte e
# calava a recusa. Arquivo no disco
# não é a sessão.
FEEL_CAPTURE = re.compile(r"Captura no disco não é sessão observada")


def recipe_refuses_disk_capture_as_session(text):
    return bool(text and FEEL_CAPTURE.search(text))


def feel_capture_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_disk_capture_as_session(text):
        return "recipes/feel.md"
    return None


def feel_capture_scope():
    if not feel_capture_source():
        return None
    return (
        " O disco recusa que captura no disco seja sessão observada "
        "(`captura`). Arquivo no disco não é a sessão."
    )


def feel_sources_scope():
    scope = (
        "arquivo de constante no disco. "
        "Não observa a sessão."
    )
    named = feel_capture_scope()
    if named:
        scope += named
    return scope


def feel_source_files(project):
    _constants, sources = declared_feel_constants(project)
    _windows, rain_sources = rain_window_constants(project)
    for relative in rain_sources:
        if relative not in sources:
            sources.append(relative)
    return sources


# A receita já recusa que achar o jogo
# seja ter sentido. Sem isto o feel
# relatava o unobserved e calava a
# recusa. Arquivo no disco não é o
# verbo.
FEEL_SENSE = re.compile(r"Achar o jogo\s+não é ter sentido")


def recipe_refuses_finding_game_as_feeling(text):
    return bool(text and FEEL_SENSE.search(text))


def feel_unobserved_sense_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_finding_game_as_feeling(text):
        return "recipes/feel.md"
    return None


def feel_unobserved_sense_scope():
    if not feel_unobserved_sense_source():
        return None
    return (
        " O disco recusa que achar o jogo seja ter sentido "
        "(`sentido`). Arquivo no disco não é o verbo."
    )


def feel_unobserved_scope():
    scope = (
        "constante no disco sem recibo de observação. "
        "Não é peso percebido."
    )
    named = feel_unobserved_sense_scope()
    if named:
        scope += named
    bank = feel_unobserved_guard_scope()
    if bank:
        scope += bank
    return scope


# A receita já recusa que a guarda
# seja janela de hit. Sem isto o
# feel relatava o unobserved e
# calava a recusa. Guarda no disco
# não é a janela.
FEEL_GUARD = re.compile(r"guarda não é janela de hit")


def recipe_refuses_guard_as_hit_window(text):
    return bool(text and FEEL_GUARD.search(text))


def feel_unobserved_guard_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_guard_as_hit_window(text):
        return "recipes/feel.md"
    return None


def feel_unobserved_guard_scope():
    if not feel_unobserved_guard_source():
        return None
    return (
        " O disco recusa que a guarda seja janela de hit "
        "(`guarda`). Guarda no disco não é a janela."
    )


def feel_unobserved_flag(reading):
    unobserved = (reading or {}).get("unobserved")
    if isinstance(unobserved, dict):
        return bool(unobserved.get("unobserved"))
    return bool(unobserved)


def feel_reading(project):
    project = Path(project)
    constants, sources = declared_feel_constants(project)
    # O campo já marca prática, folga e fecho. Sem isto o
    # comando lia só o CONFIG e calava as janelas da chuva.
    # Número no disco não é peso percebido.
    windows, rain_sources = rain_window_constants(project)
    seen = {item["key"] for item in constants}
    for item in windows:
        if item["key"] in seen:
            continue
        seen.add(item["key"])
        constants.append(item)
    for relative in rain_sources:
        if relative not in sources:
            sources.append(relative)
    observations = observation_receipts(project)
    item_scope = observation_item_scope()
    for item in observations:
        item["scope"] = item_scope
    constant_scope = feel_constant_scope()
    for item in constants:
        item["scope"] = constant_scope
    then = feel_then(project)
    artistic = feel_then_scope()
    if artistic:
        then = dict(then, scope=artistic)
    if sources:
        sources = {
            "paths": sources,
            "scope": feel_sources_scope(),
        }
    unobserved = bool(constants) and not observations
    if unobserved:
        unobserved = {
            "unobserved": True,
            "scope": feel_unobserved_scope(),
        }
    if observations:
        observations = {
            "items": observations,
            "scope": feel_observations_scope(),
        }
    if constants:
        constants = {
            "items": constants,
            "scope": feel_constants_scope(),
        }
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "constants": constants,
        "sources": sources,
        "observations": observations,
        "unobserved": unobserved,
        "felt": False,
        "then": then,
        "guide": str(FRAMEWORK / "recipes/feel.md"),
        "rule": (
            "Constante nomeada não é peso percebido. Recibo de observação no "
            "projeto é o que o harness consegue ver; ele não joga."
        ),
        "scope": _feel_scope(project),
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
    "game_speed": re.compile(r"gameSpeed|game-speed|velocidade da partida"),
    "colorblind": re.compile(r"colorblind|COLORBLIND_INKS|dressPalette|tinta estável"),
    "live": re.compile(r"aria-live|liveText|applyLive|região viva"),
    "haptics": re.compile(r"createHaptics|rumbleRole|vibrationActuator|navigator\.vibrate"),
}
PERSIST_USE = re.compile(
    r"localStorage|sessionStorage|indexedDB|saveProgress|loadProgress|PROGRESS_KEY|SETTINGS_KEY"
)
PERSIST_VERSION = re.compile(r"PROGRESS_SCHEMA|SETTINGS_SCHEMA|SAVE_VERSION|function migrate\b|\bmigrate\s*\(")
PERSIST_WARN = re.compile(r"persistLine|title_volatile|title_unsaved|settings_recovered|settings\.broken")
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


def heading_mark_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, ROLE_CODE_SUFFIXES):
        if dash_aims_heading(text):
            return relative
    return None


# A porta já desloca o corpo. Sem isto o feel
# lia CONFIG e calava a mostra. Pose no disco
# não é peso percebido.
ATTRACT_MOVE = re.compile(r"(?:export\s+)?function\s+attractMove\b")


def door_moves_body(text):
    return bool(text and ATTRACT_MOVE.search(text))


def attract_move_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, ROLE_CODE_SUFFIXES):
        if door_moves_body(text):
            return relative
    return None


# A receita já inclina o quadro. Sem isto o feel
# lia lookAheadX e calava o laço. Lean no disco
# não é peso percebido.
LOOK_AHEAD = re.compile(r"(?:export\s+)?function\s+lookAhead\b")


def camera_leans(text):
    return bool(text and LOOK_AHEAD.search(text))


def look_ahead_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, ROLE_CODE_SUFFIXES):
        if camera_leans(text):
            return relative
    return None


# O tool já exercita o perdão. Sem isto o feel
# lia CONFIG e calava o probe. Conta no disco
# não é peso percebido.
PROBE_FILES = ("tools/probe.mjs", "tools/probe.js", "tools/probe.py")
PROBE_BUFFERS = re.compile(
    r"não atribui peso percebido|janelas de perdão",
    re.IGNORECASE,
)


def probe_counts_buffers(text):
    return bool(text and PROBE_BUFFERS.search(text))


def probe_buffer_source(project):
    project = Path(project)
    for name in PROBE_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if probe_counts_buffers(text):
            return name
    return None


# A receita já senta a guarda. Sem isto o feel
# lia squash e calava o sit. Pose no disco
# não é peso percebido.
BANK_SIT = re.compile(r"bankWindup\s*=\s*windup")


def guard_sits_body(text):
    return bool(text and BANK_SIT.search(text))


def bank_sit_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, ROLE_CODE_SUFFIXES):
        if "tests" in Path(relative).parts:
            continue
        if guard_sits_body(text):
            return relative
    return None


# A receita já emite o land. Sem isto o feel
# lia squash e calava o término. Pose no disco
# não é peso percebido.
LAND_DASH = re.compile(r"(?:export\s+)?function\s+landDash\b")


def dash_emits_land(text):
    return bool(text and LAND_DASH.search(text))


def land_dash_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, ROLE_CODE_SUFFIXES):
        if "tests" in Path(relative).parts:
            continue
        if dash_emits_land(text):
            return relative
    return None


def _feel_scope(project):
    scope = (
        "Lê `const CONFIG` (perdão, graça, hitstop, shake, squash, punch, "
        "rumble e o peso do passo) e as janelas da chuva (`practiceTicks`, "
        "`recoveryTicks`, o fecho) em data/, tables/ e content/. Lê "
        "`record.json` com kind=observation. Nomeia `then.play` e "
        "`then.note` sem executar. Com last-run, nomeia `then.seed` e "
        "`then.invite`. O `next` (`feel.unobserved`) aponta o mesmo `note` "
        "— com `--from-run` se o candidato existir. Sem "
        "comando de abrir, a chave some. Sem last-run, seed e invite somem. "
        "Não tem `prompt`. Não mede latência, não segura o controle e não "
        "atribui degrau. `felt` é "
        "sempre falso: tabela de constantes e recibo otimista saem intactos."
    )
    if heading_mark_source(project):
        scope += (
            " O coil do dash marca o rumo no corpo — traço no disco não é "
            "peso percebido."
        )
    if attract_move_source(project):
        scope += (
            " A porta desloca o corpo (`attractMove`). Pose no disco não é "
            "peso percebido."
        )
    if look_ahead_source(project):
        scope += (
            " O disco inclina o quadro (`lookAhead`). Lean no disco não é "
            "peso percebido."
        )
    if probe_buffer_source(project):
        scope += (
            " O disco exercita o perdão (`probe`). Conta no disco não é "
            "peso percebido."
        )
    if bank_sit_source(project):
        scope += (
            " A guarda senta o corpo (`bankWindup`). Pose no disco não é "
            "peso percebido."
        )
    if land_dash_source(project):
        scope += (
            " O dash emite o término (`landDash`). Pose no disco não é "
            "peso percebido."
        )
    named = feel_tween_scope()
    if named:
        scope += named
    freeze = feel_swallow_scope()
    if freeze:
        scope += freeze
    rule = feel_rule_scope()
    if rule:
        scope += rule
    stance = feel_pose_scope()
    if stance:
        scope += stance
    sense = feel_perceived_scope()
    if sense:
        scope += sense
    return scope


# A receita já recusa que um tween
# genérico sem dono seja feel
# reutilizável. Sem isto o feel lia
# as constantes e calava a recusa.
# Receita no disco não é peso percebido.
FEEL_TWEEN = re.compile(r"não é feel reutilizável")


def recipe_refuses_generic_tween_as_reusable_feel(text):
    return bool(text and FEEL_TWEEN.search(text))


def feel_tween_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_generic_tween_as_reusable_feel(text):
        return "recipes/feel.md"
    return None


def feel_tween_scope():
    if not feel_tween_source():
        return None
    return (
        " O disco recusa que um tween genérico sem dono seja feel reutilizável "
        "(`tween`). Receita no disco não é peso percebido."
    )


# A receita já recusa que guardar no
# hitstop seja engolido. Sem isto o
# feel lia o CONFIG e calava a
# recusa. Hitstop no disco não é o
# perdão.
FEEL_SWALLOW = re.compile(r"Guardar no hitstop não é engolido")


def recipe_refuses_guard_during_hitstop_as_swallowed(text):
    return bool(text and FEEL_SWALLOW.search(text))


def feel_swallow_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_guard_during_hitstop_as_swallowed(text):
        return "recipes/feel.md"
    return None


def feel_swallow_scope():
    if not feel_swallow_source():
        return None
    return (
        " O disco recusa que guardar no hitstop seja engolido "
        "(`engolido`). Hitstop no disco não é o perdão."
    )


# A receita já recusa que
# corrigir a regra substitua o
# feel. Sem isto o feel lia o
# CONFIG e calava a recusa.
# Regra no disco não é o feel.
FEEL_RULE = re.compile(r"Corrigir a regra não substitui o feel")


def recipe_refuses_rule_fix_as_feel(text):
    return bool(text and FEEL_RULE.search(text))


def feel_rule_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_rule_fix_as_feel(text):
        return "recipes/feel.md"
    return None


def feel_rule_scope():
    if not feel_rule_source():
        return None
    return (
        " O disco recusa que corrigir a regra substitua o feel "
        "(`regra`). Regra no disco não é o feel."
    )


# A receita já recusa que pose e
# arquivo no disco sejam peso
# percebido. Sem isto o feel lia
# o CONFIG e calava a recusa.
# Arquivo no disco não é o peso.
FEEL_POSE = re.compile(r"Pose e\s+arquivo no disco não são peso percebido")


def recipe_refuses_pose_file_as_felt_weight(text):
    return bool(text and FEEL_POSE.search(text))


def feel_pose_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_pose_file_as_felt_weight(text):
        return "recipes/feel.md"
    return None


def feel_pose_scope():
    if not feel_pose_source():
        return None
    return (
        " O disco recusa que pose e arquivo no disco sejam peso percebido "
        "(`pose`). Arquivo no disco não é o peso."
    )


# A receita já recusa que o
# aperto no disco seja peso
# percebido. Sem isto o feel
# lia o CONFIG e calava a
# recusa. Aperto no disco não
# é o percebido.
FEEL_PERCEIVED = re.compile(r"Aperto no disco não é peso\s+percebido")


def recipe_refuses_squeeze_as_felt_weight(text):
    return bool(text and FEEL_PERCEIVED.search(text))


def feel_perceived_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_squeeze_as_felt_weight(text):
        return "recipes/feel.md"
    return None


def feel_perceived_scope():
    if not feel_perceived_source():
        return None
    return (
        " O disco recusa que o aperto no disco seja peso percebido "
        "(`percebido`). Aperto no disco não é o percebido."
    )


# O painel e o live já nomeiam o vazio. Sem isto o
# access lia região viva e calava o canvas da porta.
# Texto no disco não é mix ouvido.
CANVAS_AUDIO_GAP = re.compile(r"extra\.audio[\s\S]{0,400}?fillText\(\s*audio\b")


def canvas_names_audio_gap(text):
    return bool(text and CANVAS_AUDIO_GAP.search(text))


def canvas_audio_gap_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if canvas_names_audio_gap(text):
            return relative
    return None


# A receita já pede foco visível. Sem isto o access
# lia knobs e calava o outline que a casca já declara.
# Outline no disco não é sessão com o teclado.
FOCUS_VISIBLE = re.compile(r":focus-visible")


def page_names_focus(text):
    return bool(text and FOCUS_VISIBLE.search(text))


def focus_visible_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if page_names_focus(text):
            return relative
    return None


# A receita já amostra o stub. Sem isto o access
# lia highContrast e calava o tool. Stub no disco
# não é sessão com o modo ativo.
CONTRAST_FILES = ("tools/contrast.mjs", "tools/contrast.js", "tools/contrast.py")
CONTRAST_STUB = re.compile(r"pixels depois do\s+draw\(\)|não aprova contraste", re.IGNORECASE)


def contrast_samples_stub(text):
    return bool(text and CONTRAST_STUB.search(text))


def contrast_stub_source(project):
    project = Path(project)
    for name in CONTRAST_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if contrast_samples_stub(text):
            return name
    return None


# A receita já recusa que tamanho CSS igual
# garanta pixels. Sem isto o access amostrava
# o stub e calava a recusa. Tamanho no disco
# não é o buffer.
PERF_PIXELS = re.compile(r"Tamanho CSS igual não garante pixels")


def recipe_refuses_css_size_as_pixels(text):
    return bool(text and PERF_PIXELS.search(text))


def access_contrast_pixels_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_css_size_as_pixels(text):
        return "recipes/performance.md"
    return None


def access_contrast_pixels_scope():
    if not access_contrast_pixels_source():
        return None
    return (
        " O disco recusa que tamanho CSS igual garanta pixels "
        "(`pixels`). Tamanho no disco não é o buffer."
    )


# A receita já pede o aviso. Sem isto o access
# lia região viva e calava o perigo que o live
# já anuncia. Texto no DOM não é sessão.
THREAT_LIVE = re.compile(r"perigo à frente")


def live_names_threat(text):
    return bool(text and THREAT_LIVE.search(text))


def threat_live_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if "tests" in Path(relative).parts:
            continue
        if live_names_threat(text):
            return relative
    return None


# A receita já pede a tabela viva. Sem isto o access
# lia remap e calava o preenchimento. Tabela no
# disco não é sessão.
COMMANDS_PAINT = re.compile(r"(?:export\s+)?function\s+paintCommands\b")


def page_lists_keys(text):
    return bool(text and COMMANDS_PAINT.search(text))


def commands_table_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if "tests" in Path(relative).parts:
            continue
        if page_lists_keys(text):
            return relative
    return None


# A receita já pede a legenda na porta. Sem isto o
# access lia captions e calava o canvas da abertura.
# Texto no disco não é sessão.
CAPTION_DOOR = re.compile(r"drawTitle[\s\S]{0,1200}?drawCaptions")


def door_reads_caption(text):
    return bool(text and CAPTION_DOOR.search(text))


def caption_door_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if "tests" in Path(relative).parts:
            continue
        if door_reads_caption(text):
            return relative
    return None


# A pesquisa já recusa que acessibilidade seja gate de certificação. Sem isto o
# item copiava a chave e calava a recusa.
# Opção no disco não é certificação.
A11Y_RESEARCH = FRAMEWORK / "references/gates-research.md"
A11Y_CERT = re.compile(r"não é gate de certificação")


def research_refuses_a11y_certification(text):
    return bool(text and A11Y_CERT.search(text))


def access_option_cert_source():
    path = A11Y_RESEARCH
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if research_refuses_a11y_certification(text):
        return "references/gates-research.md"
    return None


def access_option_scope():
    scope = (
        "Chave e fontes da opção declarada. Não joga com o modo "
        "ativo e não aprova alcance."
    )
    if access_option_cert_source():
        scope += (
            " O disco recusa que acessibilidade seja gate de certificação (`certificação`). "
            "Opção no disco não é certificação."
        )
    if access_option_consumer_source():
        scope += (
            " O disco recusa que opção sem consumidor seja opção (`opção`). "
            "Chave no disco não é alcance."
        )
    return scope


# A receita já recusa que o número na legenda seja mix. Sem isto a
# opção captions copiava a chave e calava a recusa.
# Número no disco não é mix.
AUDIO_CAPTION_NUMBER = re.compile(r"Número na legenda não é mix")


def recipe_refuses_caption_number_as_mix(text):
    return bool(text and AUDIO_CAPTION_NUMBER.search(text))


def access_caption_number_source():
    path = AUDIO_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_caption_number_as_mix(text):
        return "recipes/audio.md"
    return None


def access_caption_number_scope():
    if not access_caption_number_source():
        return None
    return (
        "O disco recusa que o número na legenda seja mix "
        "(`número`). Número no disco não é mix."
    )


def access_captions_option_scope():
    scope = access_option_scope()
    named = access_caption_number_scope()
    if named:
        scope += " " + named
    muted = access_caption_muted_scope()
    if muted:
        scope += " " + muted
    return scope


# A receita já recusa que a legenda prove o
# jogo completável sem áudio. Sem isto a
# opção captions nomeava o número e calava
# a recusa. Texto no disco não é a partida
# muda.
A11Y_MUTED = re.compile(r"completável com o áudio desligado")


def recipe_refuses_caption_as_muted_completable(text):
    return bool(text and A11Y_MUTED.search(text))


def access_caption_muted_source():
    path = FRAMEWORK / "recipes/accessibility.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_caption_as_muted_completable(text):
        return "recipes/accessibility.md"
    return None


def access_caption_muted_scope():
    if not access_caption_muted_source():
        return None
    return (
        "O disco recusa que a legenda prove o jogo completável sem "
        "áudio (`mudo`). Texto no disco não é a partida muda."
    )


# A receita já recusa opção sem consumidor. Sem isto o
# item copiava a chave e calava a recusa.
# Chave no disco não é alcance.
A11Y_OPTION = re.compile(r"sem consumidor no código não é uma opção")
A11Y_RECIPE = FRAMEWORK / "recipes/accessibility.md"


def recipe_refuses_option_without_consumer(text):
    return bool(text and A11Y_OPTION.search(text))


def access_option_consumer_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_option_without_consumer(text):
        return "recipes/accessibility.md"
    return None


# A receita já recusa que o pulso seja sessão no controle. Sem isto a
# opção haptics copiava a chave e calava a recusa.
# Pulso no disco não é sessão.
A11Y_HAPTICS_CONTROL = re.compile(r"Pulso no disco\s+não é sessão no controle")


def recipe_refuses_pulse_as_controller_session(text):
    return bool(text and A11Y_HAPTICS_CONTROL.search(text))


def access_haptics_control_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_pulse_as_controller_session(text):
        return "recipes/accessibility.md"
    return None


def access_haptics_control_scope():
    if not access_haptics_control_source():
        return None
    return (
        "O disco recusa que o pulso seja sessão no controle "
        "(`controle`). Pulso no disco não é sessão."
    )


def access_haptics_option_scope():
    scope = access_option_scope()
    named = access_haptics_control_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que o botão seja sessão. Sem isto a
# opção remap copiava a chave e calava a recusa.
# Botão no disco não é sessão.
A11Y_REMAP_BUTTON = re.compile(r"Botão no disco não é sessão")


def recipe_refuses_button_as_session(text):
    return bool(text and A11Y_REMAP_BUTTON.search(text))


def access_remap_button_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_button_as_session(text):
        return "recipes/accessibility.md"
    return None


def access_remap_button_scope():
    if not access_remap_button_source():
        return None
    return (
        "O disco recusa que o botão seja sessão "
        "(`botão`). Botão no disco não é sessão."
    )


def access_remap_option_scope():
    scope = access_option_scope()
    named = access_remap_button_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que o movimento reduzido apague a causa. Sem isto a
# opção reduced_motion copiava a chave e calava a recusa.
# Causa no disco não é sessão.
A11Y_REDUCED_CAUSE = re.compile(r"sem remover o\s+feedback de causa")


def recipe_refuses_reduced_motion_erasing_cause(text):
    return bool(text and A11Y_REDUCED_CAUSE.search(text))


def access_reduced_motion_cause_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_reduced_motion_erasing_cause(text):
        return "recipes/accessibility.md"
    return None


def access_reduced_motion_cause_scope():
    if not access_reduced_motion_cause_source():
        return None
    return (
        "O disco recusa que o movimento reduzido apague a causa "
        "(`causa`). Causa no disco não é sessão."
    )


def access_reduced_motion_option_scope():
    scope = access_option_scope()
    named = access_reduced_motion_cause_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que o fundo neutro seja o pior caso. Sem isto a
# opção high_contrast copiava a chave e calava a recusa.
# Neutro no disco não é sessão.
A11Y_CONTRAST_NEUTRAL = re.compile(r"não em\s+fundo neutro")


def recipe_refuses_neutral_as_worst_case(text):
    return bool(text and A11Y_CONTRAST_NEUTRAL.search(text))


def access_high_contrast_neutral_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_neutral_as_worst_case(text):
        return "recipes/accessibility.md"
    return None


def access_high_contrast_neutral_scope():
    if not access_high_contrast_neutral_source():
        return None
    return (
        "O disco recusa que o fundo neutro seja o pior caso "
        "(`neutro`). Neutro no disco não é sessão."
    )


def access_high_contrast_option_scope():
    scope = access_option_scope()
    named = access_high_contrast_neutral_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que o estado dependa só da cor. Sem isto a
# opção colorblind copiava a chave e calava a recusa.
# Ícone no disco não é sessão.
A11Y_COLORBLIND_ICON = re.compile(r"forma,\s+ícone")


def recipe_refuses_color_only_state(text):
    return bool(text and A11Y_COLORBLIND_ICON.search(text))


def access_colorblind_icon_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_color_only_state(text):
        return "recipes/accessibility.md"
    return None


def access_colorblind_icon_scope():
    if not access_colorblind_icon_source():
        return None
    return (
        "O disco recusa que o estado dependa só da cor "
        "(`ícone`). Ícone no disco não é sessão."
    )


def access_colorblind_option_scope():
    scope = access_option_scope()
    named = access_colorblind_icon_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que completar o jogo peça as duas mãos. Sem isto a
# opção one_hand copiava a chave e calava a recusa.
# Mão no disco não é sessão.
A11Y_ONE_HAND = re.compile(r"uma das mãos")


def recipe_refuses_two_hands_to_finish(text):
    return bool(text and A11Y_ONE_HAND.search(text))


def access_one_hand_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_two_hands_to_finish(text):
        return "recipes/accessibility.md"
    return None


def access_one_hand_scope():
    if not access_one_hand_source():
        return None
    return (
        "O disco recusa que completar o jogo peça as duas mãos "
        "(`mão`). Mão no disco não é sessão."
    )


def access_one_hand_option_scope():
    scope = access_option_scope()
    named = access_one_hand_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que a assistência esconda conteúdo. Sem isto a
# opção assist copiava a chave e calava a recusa.
# Oculto no disco não é sessão.
A11Y_ASSIST_HIDDEN = re.compile(r"escondem conteúdo")


def recipe_refuses_assist_hiding_content(text):
    return bool(text and A11Y_ASSIST_HIDDEN.search(text))


def access_assist_hidden_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_assist_hiding_content(text):
        return "recipes/accessibility.md"
    return None


def access_assist_hidden_scope():
    if not access_assist_hidden_source():
        return None
    return (
        "O disco recusa que a assistência esconda conteúdo "
        "(`oculto`). Oculto no disco não é sessão."
    )


def access_assist_option_scope():
    scope = access_option_scope()
    named = access_assist_hidden_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que a precisão fique sem alternativa. Sem isto a
# opção game_speed copiava a chave e calava a recusa.
# Precisão no disco não é sessão.
A11Y_SPEED_PRECISION = re.compile(r"exigência de precisão")


def recipe_refuses_precision_without_alternative(text):
    return bool(text and A11Y_SPEED_PRECISION.search(text))


def access_game_speed_precision_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_precision_without_alternative(text):
        return "recipes/accessibility.md"
    return None


def access_game_speed_precision_scope():
    if not access_game_speed_precision_source():
        return None
    return (
        "O disco recusa que a precisão fique sem alternativa "
        "(`precisão`). Precisão no disco não é sessão."
    )


def access_game_speed_option_scope():
    scope = access_option_scope()
    named = access_game_speed_precision_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que a escala substitua a tipografia. Sem isto a
# opção ui_scale copiava a chave e calava a recusa.
# Tipografia no disco não é sessão.
A11Y_SCALE_TYPE = re.compile(r"tipografia legível")


def recipe_refuses_scale_as_typography(text):
    return bool(text and A11Y_SCALE_TYPE.search(text))


def access_ui_scale_type_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_scale_as_typography(text):
        return "recipes/accessibility.md"
    return None


def access_ui_scale_type_scope():
    if not access_ui_scale_type_source():
        return None
    return (
        "O disco recusa que a escala substitua a tipografia "
        "(`tipografia`). Tipografia no disco não é sessão."
    )


def access_ui_scale_option_scope():
    scope = access_option_scope()
    named = access_ui_scale_type_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que o overlay substitua o leitor. Sem isto a
# opção live copiava a chave e calava a recusa.
# Overlay no disco não é sessão.
A11Y_LIVE_READER = re.compile(r"não chega ao\s+leitor")


def recipe_refuses_overlay_as_reader(text):
    return bool(text and A11Y_LIVE_READER.search(text))


def access_live_reader_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_overlay_as_reader(text):
        return "recipes/accessibility.md"
    return None


def access_live_reader_scope():
    if not access_live_reader_source():
        return None
    return (
        "O disco recusa que o overlay substitua o leitor "
        "(`leitor`). Overlay no disco não é sessão."
    )


def access_live_option_scope():
    scope = access_option_scope()
    named = access_live_reader_scope()
    if named:
        scope += " " + named
    return scope


# A receita já recusa que se declare
# cobertura não observada. Sem isto o
# access listava a chave e calava a
# recusa. Lista no disco não é sessão.
A11Y_COVERAGE = re.compile(r"Não declare cobertura")


def recipe_refuses_unobserved_coverage(text):
    return bool(text and A11Y_COVERAGE.search(text))


def access_coverage_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_unobserved_coverage(text):
        return "recipes/accessibility.md"
    return None


def access_coverage_scope():
    if not access_coverage_source():
        return None
    return (
        " O disco recusa que a cobertura não observada seja declaração "
        "(`cobertura`). Lista no disco não é sessão."
    )


def access_missing_scope():
    scope = (
        "chave que o código ainda não declara. "
        "Não observa o modo ativo."
    )
    named = access_coverage_scope()
    if named:
        scope += named
    return scope


def access_missing_keys(access):
    missing = (access or {}).get("missing") or []
    if isinstance(missing, dict):
        return list(missing.get("keys") or [])
    return list(missing)


# A receita já recusa que a chave no
# fonte seja sessão. Sem isto o
# access relatava a declaração e
# calava a recusa. Chave no disco
# não é o modo ativo.
A11Y_SOURCE_KEY = re.compile(r"chave no fonte não é sessão")


def recipe_refuses_source_key_as_session(text):
    return bool(text and A11Y_SOURCE_KEY.search(text))


def access_declared_source_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_source_key_as_session(text):
        return "recipes/accessibility.md"
    return None


def access_declared_source_scope():
    if not access_declared_source_source():
        return None
    return (
        " O disco recusa que a chave no fonte seja sessão "
        "(`fonte`). Chave no disco não é o modo ativo."
    )


def access_declared_scope():
    scope = (
        "opção declarada no código. "
        "Não é sessão com o modo ativo."
    )
    named = access_declared_source_scope()
    if named:
        scope += named
    return scope


def access_declared_flag(reading):
    declared = (reading or {}).get("declared")
    if isinstance(declared, dict):
        return bool(declared.get("declared"))
    return bool(declared)


def access_reading(project):
    project = Path(project)
    found = {key: [] for key in A11Y_OPTIONS}
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        for key, pattern in A11Y_OPTIONS.items():
            if pattern.search(text):
                found[key].append(relative)
    options = [key for key, sources in found.items() if sources]
    scope = (
        "Procura highContrast, reducedMotion, captions, remapeamento, "
        "uiScale, preset de uma mão, assistência, velocidade da partida, "
        "tinta estável, região viva e pulso no aparelho no código. Não "
        "mede contraste, não joga com o modo ativo e não aprova alcance. "
        "`verified` é sempre falso."
    )
    if canvas_audio_gap_source(project):
        scope += (
            " Na porta e no fim o canvas nomeia a lacuna do som que o "
            "painel já mostra. Texto no disco não é mix ouvido."
        )
    if focus_visible_source(project):
        scope += (
            " A casca declara foco visível (`:focus-visible`) que a "
            "receita já pede. Outline no disco não é sessão com o teclado."
        )
    if contrast_stub_source(project):
        scope += (
            " O disco amostra o contraste no stub (`contrast`). "
            "Stub no disco não é sessão com o modo ativo."
        )
        named = access_contrast_pixels_scope()
        if named:
            scope += named
    if threat_live_source(project):
        scope += (
            " A região viva nomeia o perigo à frente que a receita já "
            "pede. Texto no DOM não é sessão."
        )
    if commands_table_source(project):
        scope += (
            " A tabela nomeia as teclas vigentes (`#commands`). "
            "Tabela no disco não é sessão."
        )
    if caption_door_source(project):
        scope += (
            " A porta lê a legenda que o mixer ainda guarda. "
            "Texto no disco não é sessão."
        )
    named = access_automatic_scope()
    if named:
        scope += named
    option_scope = access_option_scope()
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "options": [
            {
                "key": key,
                "sources": found[key][:4],
                "scope": (
                    access_captions_option_scope() if key == "captions"
                    else access_haptics_option_scope() if key == "haptics"
                    else access_remap_option_scope() if key == "remap"
                    else access_reduced_motion_option_scope() if key == "reduced_motion"
                    else access_high_contrast_option_scope() if key == "high_contrast"
                    else access_colorblind_option_scope() if key == "colorblind"
                    else access_one_hand_option_scope() if key == "one_hand"
                    else access_assist_option_scope() if key == "assist"
                    else access_game_speed_option_scope() if key == "game_speed"
                    else access_ui_scale_option_scope() if key == "ui_scale"
                    else access_live_option_scope() if key == "live"
                    else option_scope
                ),
            }
            for key in A11Y_OPTIONS if found[key]
        ],
        "missing": (
            {
                "keys": [key for key in A11Y_OPTIONS if not found[key]],
                "scope": access_missing_scope(),
            }
            if any(not found[key] for key in A11Y_OPTIONS) else []
        ),
        "declared": (
            {
                "declared": True,
                "scope": access_declared_scope(),
            }
            if options else False
        ),
        "verified": False,
        "guide": str(FRAMEWORK / "recipes/accessibility.md"),
        "rule": (
            "Opção declarada no código não é opção observada. Uma chave sem "
            "consumidor também não é alcance."
        ),
        "scope": scope,
    }


# A receita já recusa que a verificação
# automática substitua uma sessão. Sem
# isto o access lia as opções e calava
# a recusa. Checagem no disco não é o
# modo ativo.
A11Y_AUTOMATIC = re.compile(r"não substitui uma sessão")


def recipe_refuses_automatic_check_as_session(text):
    return bool(text and A11Y_AUTOMATIC.search(text))


def access_automatic_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_automatic_check_as_session(text):
        return "recipes/accessibility.md"
    return None


def access_automatic_scope():
    if not access_automatic_source():
        return None
    return (
        " O disco recusa que a verificação automática substitua uma sessão "
        "(`automática`). Checagem no disco não é o modo ativo."
    )


# A receita e o canvas já pintam a recuperação. Sem isto o
# save lia persistLine e calava a porta. Texto no disco
# não é aba fechada.
CANVAS_RECOVERY = re.compile(r"settingsLine[\s\S]{0,800}?fillText\(\s*recovered\b")


def canvas_names_recovery(text):
    return bool(text and CANVAS_RECOVERY.search(text))


def canvas_recovery_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if canvas_names_recovery(text):
            return relative
    return None


# A receita já grava o hold no fechamento. Sem isto o
# save lia persistLine e calava o gancho. Gancho no
# disco não é aba fechada.
UNLOAD_HOLD = re.compile(
    r"addEventListener\(\s*[\"']beforeunload[\"']",
    re.IGNORECASE,
)


def disk_flushes_unload(text):
    return bool(text and UNLOAD_HOLD.search(text))


def unload_hold_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES | {".py"}):
        if "tests" in Path(relative).parts:
            continue
        if disk_flushes_unload(text):
            return relative
    return None


# A receita já verifica a gravação. Sem isto o
# save lia persistLine e calava o estágio. Escrita
# no disco não é aba fechada.
VERIFIED_WRITE = re.compile(r"const staging = `\$\{key\}\.tmp`")


def storage_verifies_write(text):
    return bool(text and VERIFIED_WRITE.search(text))


def verified_write_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES | {".py"}):
        if "tests" in Path(relative).parts:
            continue
        if storage_verifies_write(text):
            return relative
    return None


# A receita já recusa que o estágio seja
# atomicidade. Sem isto o save nomeava o
# storage e calava a recusa. Estágio no
# disco não é substituição.
PERSIST_RECIPE = FRAMEWORK / "recipes/persistence.md"
PERSIST_ATOMIC = re.compile(r"não atomicidade")


def recipe_refuses_staging_as_atomicity(text):
    return bool(text and PERSIST_ATOMIC.search(text))


def save_atomicity_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_staging_as_atomicity(text):
        return "recipes/persistence.md"
    return None


def save_atomicity_scope():
    if not save_atomicity_source():
        return None
    return (
        " O disco recusa que o estágio seja atomicidade (`atomicidade`). "
        "Estágio no disco não é substituição."
    )


# A receita já recusa que um único
# número una a versão do conteúdo e
# a do save. Sem isto o save listava
# o schema e calava a recusa. Schema
# no disco não é a história.
PERSIST_CONTRACTS = re.compile(r"Versão do conteúdo e versão do save são contratos")


def recipe_refuses_one_number_as_both_contracts(text):
    return bool(text and PERSIST_CONTRACTS.search(text))


def save_contracts_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_one_number_as_both_contracts(text):
        return "recipes/persistence.md"
    return None


def save_contracts_scope():
    if not save_contracts_source():
        return None
    return (
        " O disco recusa que um único número una a versão do conteúdo "
        "e a do save (`contratos`). Schema no disco não é a história."
    )


# A receita já recusa que o hold
# sem o número invente ensino
# feito. Sem isto o save lia o
# schema e calava a recusa. Hold
# no disco não é o ensino.
FEEL_TEACHING = re.compile(r"não\s+inventa ensino feito")


def recipe_refuses_hold_without_number_as_teaching(text):
    return bool(text and FEEL_TEACHING.search(text))


def save_teaching_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_hold_without_number_as_teaching(text):
        return "recipes/feel.md"
    return None


def save_teaching_scope():
    if not save_teaching_source():
        return None
    return (
        " O disco recusa que o hold sem o número invente ensino feito "
        "(`ensino`). Hold no disco não é o ensino."
    )


# A receita já recusa que o teste
# de dado inválido prove a
# interrupção abrupta. Sem isto
# o save lia o schema e calava a
# recusa. Teste no disco não é
# a interrupção.
PERSIST_CUT = re.compile(
    r"interrupção abrupta real,\s+ninguém exercitou"
)


def recipe_refuses_invalid_data_test_as_real_interruption(text):
    return bool(text and PERSIST_CUT.search(text))


def save_interrupt_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_invalid_data_test_as_real_interruption(text):
        return "recipes/persistence.md"
    return None


def save_interrupt_scope():
    if not save_interrupt_source():
        return None
    return (
        " O disco recusa que o teste de dado inválido prove a interrupção abrupta "
        "(`interrupção`). Teste no disco não é a interrupção."
    )


# A receita já recusa que o
# derivado seja o save. Sem isto
# o save lia o schema e calava a
# recusa. Derivado no disco não
# é o progresso.
PERSIST_DERIVED = re.compile(r"Derivado não se salva")


def recipe_refuses_derived_as_save(text):
    return bool(text and PERSIST_DERIVED.search(text))


def save_derived_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_derived_as_save(text):
        return "recipes/persistence.md"
    return None


def save_derived_scope():
    if not save_derived_source():
        return None
    return (
        " O disco recusa que o derivado seja o save "
        "(`derivado`). Derivado no disco não é o progresso."
    )


# A receita já recusa que listar o
# fonte prove a cadeia inteira. Sem
# isto o save listava o arquivo e
# calava a recusa. Arquivo no disco
# não é a migração.
PERSIST_CHAIN = re.compile(r"cadeia\s+inteira")


def recipe_refuses_listed_files_as_full_chain(text):
    return bool(text and PERSIST_CHAIN.search(text))


def save_chain_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_listed_files_as_full_chain(text):
        return "recipes/persistence.md"
    return None


def save_chain_scope():
    if not save_chain_source():
        return None
    return (
        " O disco recusa que listar o fonte prove a cadeia inteira "
        "(`cadeia`). Arquivo no disco não é a migração."
    )


def save_sources_scope():
    scope = (
        "arquivo de persistência no disco. "
        "Não executa a migração."
    )
    named = save_chain_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que o aviso
# volátil seja aba fechada. Sem
# isto o save listava o arquivo e
# calava a recusa. Arquivo no
# disco não é a aba.
PERSIST_VOLATILE = re.compile(r"Nomear\s+não é aba fechada")


def recipe_refuses_volatile_warning_as_closed_tab(text):
    return bool(text and PERSIST_VOLATILE.search(text))


def save_volatile_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_volatile_warning_as_closed_tab(text):
        return "recipes/persistence.md"
    return None


def save_volatile_scope():
    if not save_volatile_source():
        return None
    return (
        " O disco recusa que o aviso volátil seja aba fechada "
        "(`volátil`). Arquivo no disco não é a aba."
    )


def save_warnings_scope():
    scope = (
        "arquivo de aviso volátil no disco. "
        "Não fecha a aba."
    )
    named = save_volatile_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que o harness
# abra o save. Sem isto o save
# relatava o uso e calava a recusa.
# Texto no disco não é a aba.
PERSIST_OPEN = re.compile(r"não abre o save")


def recipe_refuses_harness_as_open_save(text):
    return bool(text and PERSIST_OPEN.search(text))


def save_used_open_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_harness_as_open_save(text):
        return "recipes/persistence.md"
    return None


def save_used_open_scope():
    if not save_used_open_source():
        return None
    return (
        " O disco recusa que o harness abra o save "
        "(`abre`). Texto no disco não é a aba."
    )


def save_used_scope():
    scope = (
        "uso de armazenamento no disco. "
        "Não abre o save."
    )
    named = save_used_open_scope()
    if named:
        scope += named
    listen = save_used_listen_scope()
    if listen:
        scope += listen
    tab = save_used_tab_scope()
    if tab:
        scope += tab
    keep = save_used_keep_scope()
    if keep:
        scope += keep
    idx = save_used_index_scope()
    if idx:
        scope += idx
    return scope


# A receita já recusa que ouvir
# seja aba fechada. Sem isto o
# save relatava o uso e calava
# a recusa. Ouvir no disco não
# é a aba.
PERSIST_LISTEN = re.compile(r"Ouvir não é aba fechada")


def recipe_refuses_listening_as_closed_tab(text):
    return bool(text and PERSIST_LISTEN.search(text))


def save_used_listen_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_listening_as_closed_tab(text):
        return "recipes/persistence.md"
    return None


def save_used_listen_scope():
    if not save_used_listen_source():
        return ""
    return (
        " O disco recusa que ouvir seja aba fechada "
        "(`audição`). Ouvir no disco não é a aba."
    )


# A receita já recusa que o
# número no disco seja aba
# fechada. Sem isto o save
# relatava o uso e calava a
# recusa. Número no disco
# não é a aba.
FEEL_TAB = re.compile(r"Número no disco não é aba fechada")


def recipe_refuses_number_as_closed_tab(text):
    return bool(text and FEEL_TAB.search(text))


def save_used_tab_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_number_as_closed_tab(text):
        return "recipes/feel.md"
    return None


def save_used_tab_scope():
    if not save_used_tab_source():
        return None
    return (
        " O disco recusa que o número no disco seja aba fechada "
        "(`aba`). Número no disco não é a aba."
    )


# A receita já recusa que apagar
# o save real faça um teste
# passar. Sem isto o save
# relatava o uso e calava a
# recusa. Teste no disco não
# é o save.
PERSIST_KEEP = re.compile(
    r"Não apague save real para fazer um teste passar"
)


def recipe_refuses_deleting_real_save_to_pass_a_test(text):
    return bool(text and PERSIST_KEEP.search(text))


def save_used_keep_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_deleting_real_save_to_pass_a_test(text):
        return "recipes/persistence.md"
    return None


def save_used_keep_scope():
    if not save_used_keep_source():
        return None
    return (
        " O disco recusa que apagar o save real faça um teste passar "
        "(`original`). Teste no disco não é o save."
    )


# A receita já recusa que o
# índice ou o nome de arquivo
# preserve o save. Sem isto o
# save relatava o uso e calava
# a recusa. Índice no disco
# não é a entidade.
PERSIST_INDEX = re.compile(
    r"referenciados por índice ou por nome de arquivo"
)


def recipe_refuses_index_as_stable_identity(text):
    return bool(text and PERSIST_INDEX.search(text))


def save_used_index_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_index_as_stable_identity(text):
        return "recipes/persistence.md"
    return None


def save_used_index_scope():
    if not save_used_index_source():
        return None
    return (
        " O disco recusa que o índice ou o nome de arquivo preserve o save "
        "(`índice`). Índice no disco não é a entidade."
    )


def save_used_flag(reading):
    used = (reading or {}).get("used")
    if isinstance(used, dict):
        return bool(used.get("used"))
    return bool(used)


# A receita já recusa que nomear
# seja trusted. Sem isto o save
# relatava o aviso e calava a
# recusa. Arquivo no disco não é
# a aba.
PERSIST_TRUST = re.compile(r"nem `trusted`")


def recipe_refuses_naming_as_trusted(text):
    return bool(text and PERSIST_TRUST.search(text))


def save_warned_trust_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_naming_as_trusted(text):
        return "recipes/persistence.md"
    return None


def save_warned_trust_scope():
    if not save_warned_trust_source():
        return None
    return (
        " O disco recusa que o nomear seja trusted "
        "(`confiança`). Arquivo no disco não é a aba."
    )


def save_warned_scope():
    scope = (
        "aviso volátil no disco. "
        "Não é aba fechada."
    )
    named = save_warned_trust_scope()
    if named:
        scope += named
    query = save_warned_query_scope()
    if query:
        scope += query
    return scope


# A receita já recusa que query no
# disco seja aba fechada. Sem isto
# o save relatava o aviso e calava
# a recusa. Endereço no disco não
# é a aba.
PERSIST_QUERY = re.compile(r"Query no disco não é")


def recipe_refuses_query_as_closed_tab(text):
    return bool(text and PERSIST_QUERY.search(text))


def save_warned_query_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_query_as_closed_tab(text):
        return "recipes/persistence.md"
    return None


def save_warned_query_scope():
    if not save_warned_query_source():
        return None
    return (
        " O disco recusa que query no disco seja aba fechada "
        "(`query`). Endereço no disco não é a aba."
    )


def save_warned_flag(reading):
    warned = (reading or {}).get("warned")
    if isinstance(warned, dict):
        return bool(warned.get("warned"))
    return bool(warned)


# A receita já recusa que uma
# versão sem migração preserve o
# progresso. Sem isto o save
# relatava o vigente e calava a
# recusa. Schema no disco não é
# a atualização.
PERSIST_VERSION_LOSS = re.compile(r"Uma versão sem migração")


def recipe_refuses_version_without_migration(text):
    return bool(text and PERSIST_VERSION_LOSS.search(text))


def save_versioned_version_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_version_without_migration(text):
        return "recipes/persistence.md"
    return None


def save_versioned_version_scope():
    if not save_versioned_version_source():
        return None
    return (
        " O disco recusa que uma versão sem migração preserve o progresso "
        "(`versão`). Schema no disco não é a atualização."
    )


def save_versioned_scope():
    scope = (
        "schema ou migrate no disco. "
        "Não é atualização preservada."
    )
    named = save_versioned_version_scope()
    if named:
        scope += named
    return scope


def save_versioned_flag(reading):
    versioned = (reading or {}).get("versioned")
    if isinstance(versioned, dict):
        return bool(versioned.get("versioned"))
    return bool(versioned)


# A receita já recusa que o
# armazenamento sem versão seja
# o formato. Sem isto o save
# relatava o unversioned e calava
# a recusa. Disco sem schema não
# é o contrato.
PERSIST_FORMAT = re.compile(r"Armazenamento sem versão não é o formato")


def recipe_refuses_unversioned_storage_as_format(text):
    return bool(text and PERSIST_FORMAT.search(text))


def save_unversioned_format_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_unversioned_storage_as_format(text):
        return "recipes/persistence.md"
    return None


def save_unversioned_format_scope():
    if not save_unversioned_format_source():
        return None
    return (
        " O disco recusa que o armazenamento sem versão seja o formato "
        "(`formato`). Disco sem schema não é o contrato."
    )


def save_unversioned_scope():
    scope = (
        "uso sem schema nem migrate. "
        "Não é o formato."
    )
    named = save_unversioned_format_scope()
    if named:
        scope += named
    return scope


def save_unversioned_flag(reading):
    unversioned = (reading or {}).get("unversioned") if isinstance(reading, dict) else reading
    if isinstance(unversioned, dict):
        return bool(unversioned.get("unversioned"))
    return bool(unversioned)


def save_unversioned_reading(unversioned):
    if not unversioned:
        return False
    return {
        "unversioned": True,
        "scope": save_unversioned_scope(),
    }


def save_warning_files(project):
    project = Path(project)
    found = []
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES | {".py"}):
        if PERSIST_WARN.search(text):
            found.append(relative)
            if len(found) == 8:
                break
    return found


def save_persist_sources(project):
    project = Path(project)
    found = []
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES | {".py"}):
        if (
            PERSIST_USE.search(text)
            or PERSIST_VERSION.search(text)
            or PERSIST_WARN.search(text)
        ):
            found.append(relative)
            if len(found) == 8:
                break
    return found


def save_reading(project):
    project = Path(project)
    used, versioned = [], []
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES | {".py"}):
        if PERSIST_USE.search(text):
            used.append(relative)
        if PERSIST_VERSION.search(text):
            versioned.append(relative)
    warned = save_warning_files(project)
    sources = save_persist_sources(project)
    if sources:
        sources = {
            "paths": sources,
            "scope": save_sources_scope(),
        }
    warnings = warned
    if warnings:
        warnings = {
            "paths": warnings,
            "scope": save_warnings_scope(),
        }
    scope = (
        "Procura localStorage/saveProgress, PROGRESS_SCHEMA/migrate e se o "
        "disco nomeia sessão volátil (`persistLine`, `title_volatile`, "
        "`title_unsaved`) e preferências ilegíveis (`settings_recovered`, "
        "`settings.broken`). Relata `warned`. Nomear não é aba fechada. Não "
        "executa migração, não interrompe a aba e não chama o save de "
        "atômico. `trusted` é sempre falso."
    )
    if canvas_recovery_source(project):
        scope += (
            " Na porta e no fim o canvas pinta a recuperação que o "
            "painel já mostra. A pausa não. Texto no disco não é aba fechada."
        )
    if unload_hold_source(project):
        scope += (
            " O disco grava o hold no fechamento (`beforeunload`). "
            "Gancho no disco não é aba fechada."
        )
    if verified_write_source(project):
        scope += (
            " O disco verifica a gravação (`storage`). "
            "Escrita no disco não é aba fechada."
        )
    named = save_atomicity_scope()
    if named:
        scope += named
    contracts = save_contracts_scope()
    if contracts:
        scope += contracts
    lesson = save_teaching_scope()
    if lesson:
        scope += lesson
    halt = save_interrupt_scope()
    if halt:
        scope += halt
    derived = save_derived_scope()
    if derived:
        scope += derived
    used_flag = bool(used)
    if used_flag:
        used_flag = {
            "used": True,
            "scope": save_used_scope(),
        }
    warned_flag = bool(warned)
    if warned_flag:
        warned_flag = {
            "warned": True,
            "scope": save_warned_scope(),
        }
    versioned_flag = bool(versioned)
    unversioned = bool(used) and not versioned_flag
    if versioned_flag:
        versioned_flag = {
            "versioned": True,
            "scope": save_versioned_scope(),
        }
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "used": used_flag,
        "versioned": versioned_flag,
        "unversioned": save_unversioned_reading(unversioned),
        "warned": warned_flag,
        "warnings": warnings,
        "sources": sources,
        "trusted": False,
        "guide": str(FRAMEWORK / "recipes/persistence.md"),
        "rule": (
            "Uso de armazenamento sem versão e sem migração é contrato sem data. "
            "Nomear sessão volátil no disco não é aba fechada. "
            "O harness não abre o save e não confirma escrita."
        ),
        "scope": scope,
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


# A receita e o tool já cronometram a porta. Sem isto o
# budget lia o script e calava o primeiro quadro.
# Stub no disco não é dispositivo.
BUDGET_DOOR = re.compile(r"title\.attract")


def budget_times_door(text):
    return bool(text and BUDGET_DOOR.search(text))


def budget_door_source(project):
    project = Path(project)
    for name in BUDGET_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if budget_times_door(text):
            return name
    return None


# A receita já pede a distribuição. Sem isto o budget
# cronometrava a porta e calava o pior quadro.
# Relato no disco não é dispositivo.
BUDGET_PERCENTILE = re.compile(r"não a média|pior percentil", re.IGNORECASE)


def budget_names_percentile(text):
    return bool(text and BUDGET_PERCENTILE.search(text))


def budget_percentile_source(project):
    project = Path(project)
    for name in BUDGET_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if budget_names_percentile(text):
            return name
    return None


# A receita já recusa que um jogo
# estável a 30 seja instável. Sem
# isto o budget cronometrava a
# porta e calava a recusa. Média
# no disco não é o quadro.
PERF_STABLE = re.compile(r"um jogo estável a 30 não é")


def recipe_refuses_stable_thirty_as_unstable(text):
    return bool(text and PERF_STABLE.search(text))


def budget_stable_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_stable_thirty_as_unstable(text):
        return "recipes/performance.md"
    return None


def budget_stable_scope():
    if not budget_stable_source():
        return None
    return (
        " O disco recusa que um jogo estável a 30 seja instável "
        "(`estável`). Média no disco não é o quadro."
    )


# A receita já recusa que menos
# chamadas de desenho garantam
# menos trabalho total. Sem isto
# o budget cronometrava a porta
# e calava a recusa. Chamadas no
# disco não são o trabalho.
PERF_DRAWS = re.compile(r"menos chamadas de desenho não garantem menos trabalho total")


def recipe_refuses_fewer_draws_as_less_work(text):
    return bool(text and PERF_DRAWS.search(text))


def budget_draws_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_fewer_draws_as_less_work(text):
        return "recipes/performance.md"
    return None


def budget_draws_scope():
    if not budget_draws_source():
        return None
    return (
        " O disco recusa que menos chamadas de desenho garantam menos trabalho total "
        "(`chamadas`). Chamadas no disco não são o trabalho."
    )


# A receita já recusa que
# aquecimento, cache e perfil
# deixem o resultado intacto.
# Sem isto o budget
# cronometrava a porta e
# calava a recusa. Perfil no
# disco não é a medição.
PERF_PROFILE = re.compile(
    r"Aquecimento, cache e ferramentas de perfil\s+alteram o próprio resultado"
)


def recipe_refuses_profile_as_intact_result(text):
    return bool(text and PERF_PROFILE.search(text))


def budget_profile_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_profile_as_intact_result(text):
        return "recipes/performance.md"
    return None


def budget_profile_scope():
    if not budget_profile_source():
        return None
    return (
        " O disco recusa que o aquecimento, o cache e o perfil deixem o resultado intacto "
        "(`perfil`). Perfil no disco não é a medição."
    )


# A receita já recusa que custos de
# build e serialização sejam FPS.
# Sem isto o budget listava o tool
# e calava a recusa. Custo no disco
# não é o quadro.
PERF_FPS = re.compile(r"serialização não são FPS")


def recipe_refuses_build_cost_as_fps(text):
    return bool(text and PERF_FPS.search(text))


def budget_fps_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_build_cost_as_fps(text):
        return "recipes/performance.md"
    return None


def budget_fps_scope():
    if not budget_fps_source():
        return None
    return (
        " O disco recusa que custos de build, compilação aquecida e "
        "serialização sejam FPS (`fps`). Custo no disco não é o quadro."
    )


def budget_files_scope():
    scope = (
        "arquivo de orçamento no disco. "
        "Não executa o orçamento."
    )
    named = budget_fps_scope()
    if named:
        scope += named
    return scope


def budget_tool_files(project):
    project = Path(project)
    return [
        name for name in BUDGET_FILES
        if (project / name).is_file() and not (project / name).is_symlink()
    ]


# A receita já recusa que uma
# melhoria visual seja otimização.
# Sem isto o budget listava o
# recibo e calava a recusa. Recibo
# no disco não é os dois lados.
PERF_OPTIMIZATION = re.compile(r"melhoria visual pode aumentar o custo")


def recipe_refuses_visual_gain_as_optimization(text):
    return bool(text and PERF_OPTIMIZATION.search(text))


def budget_optimization_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_visual_gain_as_optimization(text):
        return "recipes/performance.md"
    return None


def budget_optimization_scope():
    if not budget_optimization_source():
        return None
    return (
        " O disco recusa que uma melhoria visual seja otimização "
        "(`otimização`). Recibo no disco não é os dois lados."
    )


def budget_receipts_scope():
    scope = (
        "recibo de orçamento no disco. "
        "Não mede o quadro."
    )
    named = budget_optimization_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que a
# ferramenta de medição deixe o
# resultado intacto. Sem isto o
# budget listava o script e calava
# a recusa. Script no disco não é
# o quadro limpo.
PERF_RESULT = re.compile(r"desenhar na cena e falsificar")


def recipe_refuses_tool_as_intact_result(text):
    return bool(text and PERF_RESULT.search(text))


def budget_result_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_tool_as_intact_result(text):
        return "recipes/performance.md"
    return None


def budget_result_scope():
    if not budget_result_source():
        return None
    return (
        " O disco recusa que a ferramenta de medição deixe o resultado "
        "intacto (`resultado`). Script no disco não é o quadro limpo."
    )


def budget_scripts_scope():
    scope = (
        "script de orçamento no disco. "
        "Não executa o orçamento."
    )
    named = budget_result_scope()
    if named:
        scope += named
    return scope


def budget_script_names(project):
    try:
        scripts, _ = project_commands(project)
    except (OSError, ValueError):
        scripts = {}
    return [
        name for name in scripts
        if name == "budget" or name.startswith("budget:") or name.startswith("budget-")
        or name == "bench" or name.startswith("bench:")
    ]


# A receita já recusa que o harness
# execute a medição. Sem isto o
# budget relatava o artefato e
# calava a recusa. Script no disco
# não é o quadro.
PERF_MEASURE = re.compile(r"não executa a\s+medição")


def recipe_refuses_harness_as_running_measure(text):
    return bool(text and PERF_MEASURE.search(text))


def budget_declared_measure_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_harness_as_running_measure(text):
        return "recipes/performance.md"
    return None


def budget_declared_measure_scope():
    if not budget_declared_measure_source():
        return None
    return (
        " O disco recusa que o harness execute a medição "
        "(`medida`). Script no disco não é o quadro."
    )


def budget_declared_scope():
    scope = (
        "artefato de orçamento no disco. "
        "Não executa a medição."
    )
    named = budget_declared_measure_scope()
    if named:
        scope += named
    return scope


def budget_declared_flag(reading):
    declared = (reading or {}).get("declared")
    if isinstance(declared, dict):
        return bool(declared.get("declared"))
    return bool(declared)


# A receita já recusa que sem
# orçamento exista rápido o
# suficiente. Sem isto o budget
# relatava o pacote e calava a
# recusa. Pacote no disco não é
# o quadro.
PERF_ENOUGH = re.compile(r"rápido o suficiente")


def recipe_refuses_package_as_fast_enough(text):
    return bool(text and PERF_ENOUGH.search(text))


def budget_expected_enough_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_package_as_fast_enough(text):
        return "recipes/performance.md"
    return None


def budget_expected_enough_scope():
    if not budget_expected_enough_source():
        return None
    return (
        " O disco recusa que sem orçamento exista rápido o suficiente "
        "(`suficiente`). Pacote no disco não é o quadro."
    )


def budget_expected_scope():
    scope = (
        "package ou Cargo no disco. "
        "Não é o quadro medido."
    )
    named = budget_expected_enough_scope()
    if named:
        scope += named
    return scope


def budget_expected_flag(reading):
    expected = (reading or {}).get("expected")
    if isinstance(expected, dict):
        return bool(expected.get("expected"))
    return bool(expected)


# A receita já recusa que o
# pacote sem orçamento seja o
# dispositivo. Sem isto o budget
# relatava o unbudgeted e calava
# a recusa. Manifesto no disco
# não é o quadro medido.
PERF_DEVICE = re.compile(r"Pacote sem orçamento não é o dispositivo")


def recipe_refuses_package_without_budget_as_device(text):
    return bool(text and PERF_DEVICE.search(text))


def budget_unbudgeted_device_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_package_without_budget_as_device(text):
        return "recipes/performance.md"
    return None


def budget_unbudgeted_device_scope():
    if not budget_unbudgeted_device_source():
        return None
    return (
        " O disco recusa que o pacote sem orçamento seja o dispositivo "
        "(`dispositivo`). Manifesto no disco não é o quadro medido."
    )


def budget_unbudgeted_scope():
    scope = (
        "package ou Cargo sem artefato de orçamento. "
        "Não é o dispositivo."
    )
    named = budget_unbudgeted_device_scope()
    if named:
        scope += named
    return scope


def budget_unbudgeted_flag(reading):
    unbudgeted = (reading or {}).get("unbudgeted") if isinstance(reading, dict) else reading
    if isinstance(unbudgeted, dict):
        return bool(unbudgeted.get("unbudgeted"))
    return bool(unbudgeted)


def budget_unbudgeted_reading(unbudgeted):
    if not unbudgeted:
        return False
    return {
        "unbudgeted": True,
        "scope": budget_unbudgeted_scope(),
    }


def budget_reading(project):
    project = Path(project)
    try:
        scripts, _ = project_commands(project)
    except (OSError, ValueError):
        scripts = {}
    named = budget_script_names(project)
    files = budget_tool_files(project)
    receipts = budget_receipts(project)
    expected = bool(scripts) or (project / "Cargo.toml").is_file()
    declared_flag = bool(named or files or receipts)
    unbudgeted = expected and not declared_flag
    if expected:
        expected = {
            "expected": True,
            "scope": budget_expected_scope(),
        }
    if declared_flag:
        declared_flag = {
            "declared": True,
            "scope": budget_declared_scope(),
        }
    if files:
        files = {
            "paths": files,
            "scope": budget_files_scope(),
        }
    if receipts:
        receipts = {
            "paths": receipts,
            "scope": budget_receipts_scope(),
        }
    if named:
        named = {
            "names": named,
            "scope": budget_scripts_scope(),
        }
    scope = (
        "Procura script `budget`/`bench`, tools/budget.* e record kind=budget. "
        "Não executa o orçamento e não compara com build anterior. "
        "`measured` é sempre falso."
    )
    if budget_door_source(project):
        scope += (
            " O orçamento cronometra a porta (`title.attract`). "
            "Stub no disco não é dispositivo."
        )
    # A receita já relata os bytes. Sem isto o budget
    # cronometrava a porta e calava o size. Bytes no
    # disco não são dispositivo.
    if ship_size_source(project):
        scope += (
            " O disco relata os bytes (`size`) sem teto. "
            "Bytes no disco não são o quadro medido."
        )
    if budget_percentile_source(project):
        scope += (
            " O disco relata o pior percentil, não a média. "
            "Relato no disco não é dispositivo."
        )
    stable = budget_stable_scope()
    if stable:
        scope += stable
    draws = budget_draws_scope()
    if draws:
        scope += draws
    probe = budget_profile_scope()
    if probe:
        scope += probe
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "expected": expected,
        "scripts": named,
        "files": files,
        "receipts": receipts,
        "declared": declared_flag,
        "unbudgeted": budget_unbudgeted_reading(unbudgeted),
        "measured": False,
        "guide": str(FRAMEWORK / "recipes/performance.md"),
        "rule": (
            "Script de orçamento não é medição no dispositivo alvo. Sem artefato "
            "que meça, não existe ‘rápido o suficiente’."
        ),
        "scope": scope,
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
RAIN_DIRS = ("data", "tables", "content")
RAIN_CORE_FIELDS = (
    "intervalTicks",
    "minIntervalTicks",
    "rampTicks",
    "hazardChanceStart",
    "hazardChanceEnd",
    "fallSpeedMin",
    "fallSpeedMax",
)
# Janelas que o campo já marca. Sem isto o `feel` lia só o
# CONFIG e calava prática, folga e fecho. Número no disco
# não é peso percebido.
RAIN_WINDOW_FIELDS = (
    "practiceTicks",
    "recoveryTicks",
    "recoveryIntervalScale",
    "closeIntervalScale",
    "closeHazardScale",
)
CONTENT_DIRS = ("data", "content", "levels", "maps", "tables")
CONTENT_SUFFIXES = {".json", ".ldtk", ".tmx", ".csv", ".ink"}
CONTENT_LOOSE_SUFFIXES = {".ldtk", ".tmx", ".ink"}
CONTENT_ART_SKIP = frozenset({
    "palettes.json", "tokens.json", "art-tokens.json", "design-tokens.json",
})
SHIP_WORDS = ("build", "export", "dist", "package", "release")
SHIP_CI = (".gitlab-ci.yml", ".circleci/config.yml", "azure-pipelines.yml")
SHIP_RELEASE = "docs/release.md"
SHIP_VERSION = "dist/VERSION.json"
SHIP_TREE = (
    ("index", "index.html"),
    ("serve", "tools/serve.mjs"),
    ("package", "package.json"),
    ("version", "VERSION.json"),
)
SHIP_TREE_NEEDED = ("index", "serve", "package", "version")
# O export já copia src/. Sem isto o ship dizia completa
# uma dist/ que perdeu o jogo. Nomear não executa.
SHIP_PAYLOAD_DIRS = ("src",)
# A receita e o tool já relatam os bytes. Sem isto o
# ship lia a árvore e calava o tamanho. Bytes no disco
# não são outra máquina.
SIZE_FILES = ("tools/size.mjs", "tools/size.js", "tools/size.py")
SIZE_BYTES = re.compile(r"sem teto", re.IGNORECASE)
# A receita já declara o passo. Sem isto o ship
# listava build e calava o tool. Empacotar no
# disco não é outra máquina.
EXPORT_FILES = ("tools/export.mjs", "tools/export.js", "tools/export.py")
EXPORT_PACK = re.compile(r"não prova execução em outra máquina", re.IGNORECASE)


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
        "readable": ship_artifact_readable_reading(True),
        "name": optional_text(data.get("name")),
        "version": optional_text(data.get("version")),
        "git_head": optional_text(data.get("git_head")),
    }


# A receita já recusa que o JSON
# legível seja outra máquina. Sem
# isto o ship relatava o readable
# e calava a recusa. Manifesto no
# disco não é outra máquina.
SHIP_READABLE = re.compile(r"JSON legível não é outra máquina")


def recipe_refuses_readable_json_as_elsewhere(text):
    return bool(text and SHIP_READABLE.search(text))


def ship_artifact_readable_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_readable_json_as_elsewhere(text):
        return "recipes/release.md"
    return None


def ship_artifact_readable_json_scope():
    if not ship_artifact_readable_source():
        return None
    return (
        " O disco recusa que o JSON legível seja outra máquina "
        "(`legível`). Manifesto no disco não é outra máquina."
    )


def ship_artifact_readable_scope():
    scope = (
        "dist/VERSION.json abriu como objeto. "
        "Não é outra máquina."
    )
    named = ship_artifact_readable_json_scope()
    if named:
        scope += named
    return scope


def ship_artifact_readable_flag(reading):
    readable = (reading or {}).get("readable") if isinstance(reading, dict) else reading
    if isinstance(readable, dict):
        return bool(readable.get("readable"))
    return bool(readable)


def ship_artifact_readable_reading(readable):
    if not readable:
        return False
    return {
        "readable": True,
        "scope": ship_artifact_readable_scope(),
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


def _rain_table_name(path):
    # Paleta e copy moram no mesmo data/. Só a mesa com o núcleo da
    # chuva conta. Arquivo sem os sete campos não é perfil jogável.
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or "palettes" in data:
        return None
    if any(field not in data for field in RAIN_CORE_FIELDS):
        return None
    return path.stem


def rain_tables(project):
    found = []
    seen = set()
    for folder in RAIN_DIRS:
        root = project / folder
        if not root.is_dir() or root.is_symlink():
            continue
        try:
            entries = sorted(root.iterdir(), key=lambda item: item.name)
        except OSError:
            continue
        for path in entries:
            if path.is_symlink() or not path.is_file():
                continue
            if path.suffix.casefold() != ".json":
                continue
            name = _rain_table_name(path)
            if not name or name in seen:
                continue
            seen.add(name)
            # A porta já lê o teto do risco. Sem isto o art
            # listava a mesa e calava o perigo que dusk e
            # calm já separam. Número no disco não é
            # comparação em movimento.
            row = {
                "key": name,
                "source": path.relative_to(project).as_posix(),
            }
            try:
                data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            except (OSError, json.JSONDecodeError):
                data = {}
            hazard = data.get("hazardChanceEnd") if isinstance(data, dict) else None
            if isinstance(hazard, (int, float)) and not isinstance(hazard, bool) and hazard == hazard:
                row["hazard"] = hazard
            found.append(row)
    return found


def rain_window_constants(project):
    found = []
    sources = []
    seen = set()
    for item in rain_tables(project):
        path = Path(project) / item["source"]
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        listed = False
        for field in RAIN_WINDOW_FIELDS:
            value = data.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            if isinstance(value, float) and not (value == value):
                continue
            key = f"{item['key']}.{field}"
            if key in seen:
                continue
            seen.add(key)
            declared = str(int(value)) if isinstance(value, int) else (
                str(int(value)) if value.is_integer() else str(value)
            )
            found.append({
                "key": key,
                "declared": declared,
                "note": None,
                "source": item["source"],
            })
            listed = True
        if listed:
            sources.append(item["source"])
    return found, sources


# A receita já nasce o look. Sem isto o art
# listava paletas e calava o tool. Ferramenta
# no disco não é comparação em movimento.
LOOK_FILES = (
    "tools/new-look.mjs",
    "tools/new-look.js",
    "tools/look.mjs",
    "tools/look.js",
    "tools/new-look.py",
)
LOOK_BIRTH = re.compile(r"Nasce um look|não inventa consumidor", re.IGNORECASE)
# O look já recusa contraste. Sem isto o art
# nascia a paleta e calava o alcance.
# Alcance no disco não é comparação em movimento.
LOOK_REACH = re.compile(r"é alcance,\s+não look", re.IGNORECASE)


def look_births_palette(text):
    return bool(text and LOOK_BIRTH.search(text))


def look_refuses_contrast(text):
    return bool(text and LOOK_REACH.search(text))


def look_birth_source(project):
    project = Path(project)
    for name in LOOK_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if look_births_palette(text):
            return name
    return None


def look_reach_source(project):
    project = Path(project)
    for name in LOOK_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if look_refuses_contrast(text):
            return name
    return None


# A receita já marca o trilho. Sem isto o art
# listava paletas e calava o telegraph. Marca no
# disco não é comparação em movimento.
TELEGRAPH_DRAW = re.compile(r"(?:function\s+drawTelegraph)\b")


def canvas_marks_rail(text):
    return bool(text and TELEGRAPH_DRAW.search(text))


def telegraph_rail_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if "tests" in Path(relative).parts:
            continue
        if canvas_marks_rail(text):
            return relative
    return None


# A receita já pinta a vinheta. Sem isto o art
# listava paletas e calava o recorte. Recorte no
# disco não é comparação em movimento.
VIGNETTE_DRAW = re.compile(r"(?:function\s+drawVignette)\b")


def canvas_marks_cut(text):
    return bool(text and VIGNETTE_DRAW.search(text))


def vignette_cut_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if "tests" in Path(relative).parts:
            continue
        if canvas_marks_cut(text):
            return relative
    return None


# A receita já recusa que paleta no
# código ou em palettes.json seja
# direção consistente. Sem isto o
# art listava o fonte e calava a
# recusa. Arquivo no disco não é
# comparação.
VISUAL_DIRECTION = re.compile(r"não é direção consistente")


def recipe_refuses_palette_as_consistent_direction(text):
    return bool(text and VISUAL_DIRECTION.search(text))


def art_direction_source():
    path = FRAMEWORK / "recipes/visual.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_palette_as_consistent_direction(text):
        return "recipes/visual.md"
    return None


def art_direction_refusal_scope():
    if not art_direction_source():
        return None
    return (
        " O disco recusa que paleta no código ou em palettes.json seja "
        "direção consistente (`direção`). Arquivo no disco não é comparação."
    )


def art_sources_scope():
    scope = (
        "fonte de paleta no disco. "
        "Não compara silhueta."
    )
    named = art_direction_refusal_scope()
    if named:
        scope += named
    return scope


def art_source_files(project):
    project = Path(project)
    found = []
    for relative, text in walk_project_files(project, SURFACE_SUFFIXES):
        if _palette_names_from_code(text) is None:
            continue
        found.append(relative)
    found.extend(art_manifest_files(project))
    return found[:8]


# A receita já recusa que o rascunho
# do init conte. Sem isto o art
# relatava o art-bible e calava a
# recusa. Arquivo no disco não é
# comparação.
VISUAL_DRAFT = re.compile(r"Rascunho\s+do `init` não conta")


def recipe_refuses_init_draft_as_declaration(text):
    return bool(text and VISUAL_DRAFT.search(text))


def art_bible_draft_source():
    path = FRAMEWORK / "recipes/visual.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_init_draft_as_declaration(text):
        return "recipes/visual.md"
    return None


def art_bible_draft_scope():
    if not art_bible_draft_source():
        return None
    return (
        " O disco recusa que o rascunho do init conte "
        "(`rascunho`). Arquivo no disco não é comparação."
    )


def art_bible_scope():
    scope = (
        "art-bible no disco. "
        "Não compara silhueta."
    )
    named = art_bible_draft_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que o
# art-bible com marcador de
# rascunho seja comparação. Sem
# isto o art relatava o bible_draft
# e calava a recusa. Arquivo no
# disco não é o quadro.
VISUAL_SKETCH = re.compile(r"Art-bible com marcador de rascunho não é comparação")


def recipe_refuses_draft_bible_as_comparison(text):
    return bool(text and VISUAL_SKETCH.search(text))


def art_bible_draft_sketch_source():
    path = FRAMEWORK / "recipes/visual.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_draft_bible_as_comparison(text):
        return "recipes/visual.md"
    return None


def art_bible_draft_sketch_scope():
    if not art_bible_draft_sketch_source():
        return None
    return (
        " O disco recusa que o art-bible com marcador de rascunho seja comparação "
        "(`esboço`). Arquivo no disco não é o quadro."
    )


def art_draft_scope():
    scope = (
        "art-bible com marcador de rascunho. "
        "Não é comparação em movimento."
    )
    named = art_bible_draft_sketch_scope()
    if named:
        scope += named
    return scope


def art_bible_draft_flag(reading):
    draft = (reading or {}).get("bible_draft") if isinstance(reading, dict) else reading
    if isinstance(draft, dict):
        return bool(draft.get("bible_draft"))
    return bool(draft)


def art_bible_draft_reading(draft):
    if not draft:
        return False
    return {
        "bible_draft": True,
        "scope": art_draft_scope(),
    }


# A receita já recusa que isso seja
# direção consistente. Sem isto o
# art relatava o vigente e calava a
# recusa. Arquivo no disco não é
# comparação.
VISUAL_CURRENT = re.compile(r"Isso não é direção consistente")


def recipe_refuses_that_as_consistent_direction(text):
    return bool(text and VISUAL_CURRENT.search(text))


def art_bible_current_consistent_source():
    path = FRAMEWORK / "recipes/visual.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_that_as_consistent_direction(text):
        return "recipes/visual.md"
    return None


def art_bible_current_consistent_scope():
    if not art_bible_current_consistent_source():
        return None
    return (
        " O disco recusa que isso seja direção consistente "
        "(`vigente`). Arquivo no disco não é comparação."
    )


def art_bible_current_scope():
    scope = (
        "docs/art-bible.md vigente no disco. "
        "Não é direção consistente."
    )
    named = art_bible_current_consistent_scope()
    if named:
        scope += named
    return scope


def art_bible_current_flag(reading):
    current = (reading or {}).get("bible_current")
    if isinstance(current, dict):
        return bool(current.get("bible_current"))
    return bool(current)


def art_bible_path(project):
    path = Path(project) / ART_BIBLE
    if path.is_file() and not path.is_symlink():
        return ART_BIBLE
    return None


def art_bible(reading):
    bible = (reading or {}).get("bible")
    if isinstance(bible, dict):
        return bible.get("path")
    return bible


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
    manifests = art_manifest_files(project)
    for relative in manifests:
        names = _palette_names_from_manifest(project / relative)
        sources.append(relative)
        for name in names:
            if name not in {item["key"] for item in palettes}:
                palettes.append({"key": name, "source": relative})
    rains = rain_tables(project)
    bible = project / ART_BIBLE
    bible_present = bible.is_file() and not bible.is_symlink()
    bible_current = document_is_current(bible)
    declared = bool(found_const or manifests or bible_current)
    bible_draft = bible_present and not bible_current
    scope = (
        "Procura `const PALETTES`, tokens.json, data/palettes.json, "
        "docs/art-bible.md sem marcador de rascunho e mesas de chuva "
        "(intervalTicks, fallSpeed e hazardChance) em data/, tables/ e content/. Não "
        "compara silhueta, não mede contraste e não aprova estilo. "
        "`consistent` é sempre falso."
    )
    if look_birth_source(project):
        scope += (
            " O disco nasce o look (`look`). Ferramenta no disco não é "
            "comparação em movimento."
        )
    if look_reach_source(project):
        scope += (
            " O disco recusa contraste como look (`contrast`). "
            "Alcance no disco não é comparação em movimento."
        )
    if telegraph_rail_source(project):
        scope += (
            " O disco marca o trilho (`telegraph`). Marca no disco não é "
            "comparação em movimento."
        )
    if vignette_cut_source(project):
        scope += (
            " O disco marca o recorte (`drawVignette`). Recorte no disco "
            "não é comparação em movimento."
        )
    named = art_appearance_scope()
    if named:
        scope += named
    framed = art_framing_scope()
    if framed:
        scope += framed
    geometry = art_geometry_scope()
    if geometry:
        scope += geometry
    blow = art_punch_scope()
    if blow:
        scope += blow
    if manifests:
        manifests = {
            "paths": manifests,
            "scope": art_manifests_scope(),
        }
    palette_scope = art_palette_scope()
    for item in palettes:
        item["scope"] = palette_scope
    rain_scope = art_rain_scope()
    for item in rains:
        item["scope"] = rain_scope
    if rains:
        rains = {
            "items": rains,
            "scope": art_rains_scope(),
        }
    if sources:
        sources = {
            "paths": sources[:8],
            "scope": art_sources_scope(),
        }
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "palettes": palettes,
        "rains": rains,
        "manifests": manifests,
        "sources": sources,
        "bible": (
            {
                "path": ART_BIBLE,
                "scope": art_bible_scope(),
            }
            if bible_present else None
        ),
        "bible_current": (
            {
                "bible_current": True,
                "scope": art_bible_current_scope(),
            }
            if bible_current else False
        ),
        "bible_draft": art_bible_draft_reading(bible_draft),
        "declared": declared,
        "missing": not declared,
        "consistent": False,
        "guide": str(FRAMEWORK / "recipes/visual.md"),
        "rule": (
            "Paleta no código ou art-bible vigente é direção declarada, não "
            "direção consistente. Moodboard e rascunho do `init` não contam. "
            "Mesa de chuva no disco não é volume nem comparação em movimento."
        ),
        "scope": scope,
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
                    if path.name.casefold() in CONTENT_ART_SKIP:
                        continue
                    add(path.relative_to(project).as_posix())
    for relative, _ in walk_project_files(project, CONTENT_LOOSE_SUFFIXES):
        add(relative)
    return found


# A receita e o jogo já nomeiam o par. Sem isto o
# content listava dusk e calm e calava `listMoods`.
# Nome no disco não é volume.
LIST_MOODS = re.compile(r"(?:export\s+)?function\s+listMoods\b")


def names_mood_pair(text):
    return bool(text and LIST_MOODS.search(text))


def mood_pair_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, ROLE_CODE_SUFFIXES):
        if names_mood_pair(text):
            return relative
    return None


# A receita já nasce a mesa. Sem isto o content
# listava dusk e calm e calava o table. Ferramenta
# no disco não é volume.
TABLE_FILES = (
    "tools/new-table.mjs",
    "tools/new-table.js",
    "tools/table.mjs",
    "tools/table.js",
    "tools/new-table.py",
)
TABLE_BIRTH = re.compile(r"Nasce uma mesa", re.IGNORECASE)


def table_births_profile(text):
    return bool(text and TABLE_BIRTH.search(text))


def table_birth_source(project):
    project = Path(project)
    for name in TABLE_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if table_births_profile(text):
            return name
    return None


# A receita já compartilha o migrate. Sem isto o
# content listava dusk e calm e calava o loader.
# Arquivo no disco não é volume.
MIGRATE_TABLE = re.compile(r"(?:export\s+)?function\s+migrateTable\b")


def tables_share_migrate(text):
    return bool(text and MIGRATE_TABLE.search(text))


def migrate_table_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, ROLE_CODE_SUFFIXES):
        if "tests" in Path(relative).parts:
            continue
        if tables_share_migrate(text):
            return relative
    return None


# A receita já nasce look e chuva. Sem isto o
# start apontava then.pair e calava o tool.
# Ferramenta no disco não é alguém de fora.
PAIR_FILES = (
    "tools/new-pair.mjs",
    "tools/new-pair.js",
    "tools/pair.mjs",
    "tools/pair.js",
    "tools/new-pair.py",
)
PAIR_BIRTH = re.compile(r"Nasce look e chuva", re.IGNORECASE)


def pair_births_mood(text):
    return bool(text and PAIR_BIRTH.search(text))


def pair_birth_source(project):
    project = Path(project)
    for name in PAIR_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if pair_births_mood(text):
            return name
    return None


# A receita já recusa que mais módulos provem composição natural.
# Sem isto o content listava arquivos e calava a recusa.
# Arquivo no disco não é o mundo.
CONTENT_RECIPE = FRAMEWORK / "recipes/content.md"
CONTENT_COMPOSITION = re.compile(r"não prova composição natural")


def recipe_refuses_modules_as_composition(text):
    return bool(text and CONTENT_COMPOSITION.search(text))


def content_composition_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_modules_as_composition(text):
        return "recipes/content.md"
    return None


# A receita já recusa que variação
# de material substitua detalhe
# funcional de forma. Sem isto o
# content listava arquivos e
# calava a recusa. Material no
# disco não é a forma.
CONTENT_MATERIAL = re.compile(
    r"Variação de material não substitui detalhe funcional de forma"
)


def recipe_refuses_material_as_functional_form(text):
    return bool(text and CONTENT_MATERIAL.search(text))


def content_material_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_material_as_functional_form(text):
        return "recipes/content.md"
    return None


def content_material_scope():
    if not content_material_source():
        return None
    return (
        " O disco recusa que a variação de material substitua detalhe funcional de forma "
        "(`material`). Material no disco não é a forma."
    )


# A receita já recusa que o alerta
# autorize apagar pixels, quantizar
# cores ou redimensionar. Sem isto
# o content listava arquivos e
# calava a recusa. Alerta no disco
# não é a correção.
CONTENT_ALERT = re.compile(
    r"não são consequência automática de\s+um alerta"
)


def recipe_refuses_alert_as_automatic_fix(text):
    return bool(text and CONTENT_ALERT.search(text))


def content_alert_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_alert_as_automatic_fix(text):
        return "recipes/content.md"
    return None


def content_alert_scope():
    if not content_alert_source():
        return None
    return (
        " O disco recusa que o alerta autorize apagar pixels, quantizar cores ou redimensionar "
        "(`alerta`). Alerta no disco não é a correção."
    )


# A receita já recusa que mais
# resolução mude as dimensões no
# mundo. Sem isto o content
# listava arquivos e calava a
# recusa. Resolução no disco
# não é a escala.
CONTENT_RESOLUTION = re.compile(
    r"Mais resolução não\s+exige mudar dimensões no mundo"
)


def recipe_refuses_resolution_as_world_scale(text):
    return bool(text and CONTENT_RESOLUTION.search(text))


def content_resolution_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_resolution_as_world_scale(text):
        return "recipes/content.md"
    return None


def content_resolution_scope():
    if not content_resolution_source():
        return None
    return (
        " O disco recusa que mais resolução mude as dimensões no mundo "
        "(`resolução`). Resolução no disco não é a escala."
    )


# A receita já recusa que o tamanho
# codificado meça custo decodificado
# ou GPU. Sem isto o content listava
# arquivos e calava a recusa. Arquivo
# no disco não é o quadro.
CONTENT_ENCODED = re.compile(r"Tamanho codificado não mede custo decodificado")


def recipe_refuses_encoded_as_gpu(text):
    return bool(text and CONTENT_ENCODED.search(text))


def content_encoded_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_encoded_as_gpu(text):
        return "recipes/content.md"
    return None


def content_encoded_scope():
    if not content_encoded_source():
        return None
    return (
        " O disco recusa que o tamanho codificado meça custo decodificado "
        "ou GPU (`codificado`). Arquivo no disco não é o quadro."
    )


# A receita já recusa que dusk e
# calm sejam volume. Sem isto o
# content listava o par e calava
# a recusa. Chuva no disco não é
# volume.
CONTENT_RAIN = re.compile(r"terceira chuva, não volume")


def recipe_refuses_dusk_calm_as_volume(text):
    return bool(text and CONTENT_RAIN.search(text))


def content_rain_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_dusk_calm_as_volume(text):
        return "recipes/content.md"
    return None


def content_rain_scope():
    if not content_rain_source():
        return None
    return (
        " O disco recusa que dusk e calm sejam volume "
        "(`chuva`). Chuva no disco não é volume."
    )


# A receita já recusa que o arquivo
# de dados seja volume. Sem isto o
# content listava o arquivo e calava
# a recusa. Arquivo no disco não é
# volume.
CONTENT_DATA = re.compile(r"Arquivo de dados não é volume")


def recipe_refuses_data_file_as_volume(text):
    return bool(text and CONTENT_DATA.search(text))


def content_data_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_data_file_as_volume(text):
        return "recipes/content.md"
    return None


def content_data_scope():
    if not content_data_source():
        return None
    return (
        " O disco recusa que o arquivo de dados seja volume "
        "(`dados`). Arquivo no disco não é volume."
    )


def content_files_scope():
    scope = (
        "arquivo de dados no disco. "
        "Não conta o mundo."
    )
    named = content_data_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que o baixado
# seja o consumido. Sem isto o
# content relatava o arquivo e
# calava a recusa. Arquivo no
# disco não é o recurso integrado.
CONTENT_STATES = re.compile(r"são estados diferentes")


def recipe_refuses_downloaded_as_consumed(text):
    return bool(text and CONTENT_STATES.search(text))


def content_external_state_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_downloaded_as_consumed(text):
        return "recipes/content.md"
    return None


def content_external_state_scope():
    if not content_external_state_source():
        return None
    return (
        " O disco recusa que o baixado seja o consumido "
        "(`baixado`). Arquivo no disco não é o recurso integrado."
    )


def content_external_scope():
    scope = (
        "arquivo de dados no disco. "
        "Não é o recurso integrado."
    )
    named = content_external_state_scope()
    if named:
        scope += named
    return scope


def content_external_flag(reading):
    external = (reading or {}).get("external")
    if isinstance(external, dict):
        return bool(external.get("external"))
    return bool(external)


# A receita já recusa que o conteúdo
# no código escale. Sem isto o
# content relatava o inline e calava
# a recusa. Código no disco não é
# volume.
CONTENT_CODE = re.compile(r"Conteúdo no código não escala")


def recipe_refuses_code_as_scale(text):
    return bool(text and CONTENT_CODE.search(text))


def content_inline_code_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_code_as_scale(text):
        return "recipes/content.md"
    return None


def content_inline_code_scope():
    if not content_inline_code_source():
        return None
    return (
        " O disco recusa que o conteúdo no código escale "
        "(`código`). Código no disco não é volume."
    )


def content_inline_scope():
    scope = (
        "conteúdo ainda no código. "
        "Não é volume extraído."
    )
    named = content_inline_code_scope()
    if named:
        scope += named
    return scope


def content_inline_flag(reading):
    inline = (reading or {}).get("inline")
    if isinstance(inline, dict):
        return bool(inline.get("inline"))
    return bool(inline)


def content_reading(project):
    project = Path(project)
    files = content_files(project)
    kind = identify(project) if project.is_dir() else None
    scope = (
        "Procura .json/.csv em data/, content/, levels/, maps/, tables/ e "
        ".ldtk/.tmx/.ink em qualquer pasta do projeto. Não conta "
        "palettes.json nem tokens.json — o `art` lê esses manifestos. "
        "Não carrega o formato e não conta itens. `enough` é sempre falso."
    )
    if mood_pair_source(project):
        scope += (
            " O disco nomeia o par look+chuva (`listMoods`). "
            "Nome no disco não é volume."
        )
    if table_birth_source(project):
        scope += (
            " O disco nasce a mesa (`table`). "
            "Ferramenta no disco não é volume."
        )
    if migrate_table_source(project):
        scope += (
            " O disco migra a mesa (`migrateTable`). "
            "Arquivo no disco não é volume."
        )
    if content_composition_source():
        scope += (
            " O disco recusa que mais módulos provem a composição "
            "(`composição`). Arquivo no disco não é o mundo."
        )
    skin = content_material_scope()
    if skin:
        scope += skin
    warn = content_alert_scope()
    if warn:
        scope += warn
    res = content_resolution_scope()
    if res:
        scope += res
    encoded = content_encoded_scope()
    if encoded:
        scope += encoded
    named = content_rain_scope()
    if named:
        scope += named
    listed = files[:24]
    if listed:
        listed = {
            "paths": listed,
            "scope": content_files_scope(),
        }
    external = bool(files)
    if external:
        external = {
            "external": True,
            "scope": content_external_scope(),
        }
    inline = bool(kind) and not files
    if inline:
        inline = {
            "inline": True,
            "scope": content_inline_scope(),
        }
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "kind": kind,
        "files": listed,
        "external": external,
        "inline": inline,
        "enough": False,
        "guide": str(FRAMEWORK / "recipes/content.md"),
        "rule": (
            "Conteúdo no código não escala. Arquivo em data/levels não é "
            "volume suficiente nem consumidor comprovado. Paleta e token "
            "não extraem conteúdo."
        ),
        "scope": scope,
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


def ship_expects_web_tree(project):
    project = Path(project)
    return (project / "index.html").is_file() and (project / "package.json").is_file()


def ship_dir_present(path):
    if not path.is_dir() or path.is_symlink():
        return False
    try:
        for item in path.iterdir():
            if item.name.startswith(".") or item.is_symlink():
                continue
            if item.is_file() or item.is_dir():
                return True
    except OSError:
        return False
    return False


def ship_payload_dirs(project):
    # Só o que o projeto já tem. HTML sem src não ganha a
    # exigência. Pasta vazia no disco de desenvolvimento
    # não pede pasta vazia no artefato.
    found = []
    root = Path(project)
    for name in SHIP_PAYLOAD_DIRS:
        if ship_dir_present(root / name):
            found.append(name)
    return found


def ship_tree(project):
    dist = Path(project) / "dist"
    if not dist.is_dir() or dist.is_symlink():
        return None
    if not ship_expects_web_tree(project):
        return None
    parts = {}
    for key, relative in SHIP_TREE:
        path = dist / relative
        parts[key] = path.is_file() and not path.is_symlink()
    needed = list(SHIP_TREE_NEEDED)
    for name in ship_payload_dirs(project):
        parts[name] = ship_dir_present(dist / name)
        needed.append(name)
    return {
        "parts": parts,
        "complete": all(parts.get(key) for key in needed),
    }


def ship_stale(artifact, project):
    if not artifact or not ship_artifact_readable_flag(artifact):
        return False
    head = artifact.get("git_head")
    if not nonempty(head):
        return False
    current = git_version(project).get("head")
    if not nonempty(current):
        return False
    return head != current


def artifact_open_command(project):
    # Superfície do artefato, não a de desenvolvimento. Árvore incompleta
    # ou HEAD velho não ganham comando. Nomear não executa.
    project = Path(project)
    tree = ship_tree(project)
    if not tree or not tree.get("complete"):
        return None
    if ship_stale(ship_artifact(project), project):
        return None
    serve = project / "dist" / "tools" / "serve.mjs"
    if not serve.is_file() or serve.is_symlink():
        return None
    return f"cd {shlex.quote(str(project / 'dist'))} && node tools/serve.mjs"


def size_names_bytes(text):
    return bool(text and SIZE_BYTES.search(text))


def ship_size_source(project):
    project = Path(project)
    for name in SIZE_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if size_names_bytes(text):
            return name
    return None


# A receita já imprime o banner. Sem isto o ship
# relata dist/ e calava o serve. Banner no disco
# não é outra máquina.
SERVE_FILES = ("tools/serve.mjs", "tools/serve.js", "tools/serve.py")
SERVE_EXPORT = re.compile(
    r"Árvore exportada\. Servir aqui não é outra máquina",
    re.IGNORECASE,
)


def serve_names_export(text):
    return bool(text and SERVE_EXPORT.search(text))


def ship_serve_source(project):
    project = Path(project)
    for name in SERVE_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if serve_names_export(text):
            return name
    return None


# O serve já recusa produção. Sem isto o play
# apontava o url e calava o aviso. Serve no
# disco não é publicação.
SERVE_PRODUCTION = re.compile(r"Não é servidor de produção", re.IGNORECASE)


def serve_refuses_production(text):
    return bool(text and SERVE_PRODUCTION.search(text))


def play_production_source(project):
    project = Path(project)
    for name in SERVE_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if serve_refuses_production(text):
            return name
    return None


def export_packs_tree(text):
    return bool(text and EXPORT_PACK.search(text))


def ship_export_source(project):
    project = Path(project)
    for name in EXPORT_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if export_packs_tree(text):
            return name
    return None


# O export já recusa file://. Sem isto o ship
# empacotava a árvore e calava o protocolo.
# Recusar no disco não é outra máquina.
EXPORT_FILE = re.compile(r"file://")


def export_refuses_file(text):
    return bool(text and EXPORT_FILE.search(text))


def ship_file_source(project):
    project = Path(project)
    for name in EXPORT_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if export_refuses_file(text):
            return name
    return None


# A receita já recusa que a identidade seja outra máquina.
# Sem isto a árvore copiava as partes e calava a recusa.
# Árvore no disco não é entrega.
SHIP_IDENTITY = re.compile(r"Identidade do artefato não é outra máquina")


def recipe_refuses_identity_as_elsewhere(text):
    return bool(text and SHIP_IDENTITY.search(text))


def ship_tree_identity_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_identity_as_elsewhere(text):
        return "recipes/release.md"
    return None


def ship_tree_scope():
    scope = (
        "Partes e completeza da pasta dist/. Não executa o serve "
        "e não entrega o artefato."
    )
    if ship_tree_identity_source():
        scope += (
            " O disco recusa que a identidade seja outra máquina (`identidade`). "
            "Árvore no disco não é entrega."
        )
    if ship_tree_portability_source():
        scope += (
            " O disco recusa que abrir o menu ou obter um ZIP comprove "
            "portabilidade (`portabilidade`). ZIP no disco não é o destino."
        )
    return scope


# A receita já recusa que um ZIP comprove portabilidade. Sem isto a
# árvore copiava as partes e calava a recusa.
# ZIP no disco não é o destino.
SHIP_PORTABILITY = re.compile(r"não\s+comprova portabilidade")


def recipe_refuses_zip_as_portable(text):
    return bool(text and SHIP_PORTABILITY.search(text))


def ship_tree_portability_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_zip_as_portable(text):
        return "recipes/release.md"
    return None


# A receita já recusa que o teste no editor demonstre o exportado.
# Sem isto o manifesto copiava nome e versão e calava a recusa.
# Manifesto no disco não é o jogo exportado.
SHIP_EDITOR = re.compile(r"Um teste no editor não demonstra o jogo exportado")


def recipe_refuses_editor_as_export(text):
    return bool(text and SHIP_EDITOR.search(text))


def ship_artifact_editor_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_editor_as_export(text):
        return "recipes/release.md"
    return None


def ship_artifact_scope():
    scope = (
        "Nome, versão e HEAD do dist/VERSION.json. Não executa o serve "
        "e não demonstra o jogo exportado."
    )
    if ship_artifact_editor_source():
        scope += (
            " O disco recusa que o teste no editor demonstre o jogo exportado (`editor`). "
            "Manifesto no disco não é o jogo exportado."
        )
    if ship_artifact_current_source():
        scope += (
            " O disco recusa que uma pasta de build existente corresponda "
            "à fonte atual (`atual`). Manifesto no disco não é o HEAD."
        )
    return scope


# A receita já recusa que a pasta de build seja a fonte atual. Sem
# isto o manifesto copiava o git_head e calava a recusa.
# Manifesto no disco não é o HEAD.
SHIP_SOURCE = re.compile(r"não prova que corresponde à fonte atual")


def recipe_refuses_build_as_current_source(text):
    return bool(text and SHIP_SOURCE.search(text))


def ship_artifact_current_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_build_as_current_source(text):
        return "recipes/release.md"
    return None


# A receita já recusa que link não listado
# comprove controle de acesso. Sem isto o
# ship listava o passo e calava a recusa.
# Link no disco não é outra máquina.
SHIP_ACCESS = re.compile(r"link não listado não comprova controle de acesso")


def recipe_refuses_link_as_access(text):
    return bool(text and SHIP_ACCESS.search(text))


def ship_access_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_link_as_access(text):
        return "recipes/release.md"
    return None


def ship_access_scope():
    if not ship_access_source():
        return None
    return (
        " O disco recusa que link não listado comprove controle de "
        "acesso (`acesso`). Link no disco não é outra máquina."
    )


# A receita já recusa que o tamanho sem
# teto seja o orçamento de entrega. Sem
# isto o ship relatava os bytes e calava
# a recusa. Relato no disco não é a
# plataforma alvo.
RELEASE_CEILING = re.compile(r"têm teto\s+declarado e medido")


def recipe_refuses_size_without_ceiling_as_budget(text):
    return bool(text and RELEASE_CEILING.search(text))


def ship_ceiling_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_size_without_ceiling_as_budget(text):
        return "recipes/release.md"
    return None


def ship_ceiling_scope():
    if not ship_ceiling_source():
        return None
    return (
        " O disco recusa que o relato de bytes cumpra o orçamento de "
        "entrega (`teto`). Relato no disco não é a plataforma alvo."
    )


# A receita já recusa que a CI seja
# a primeira execução. Sem isto o
# ship listava o fluxo e calava a
# recusa. Fluxo no disco não é
# instalação limpa.
RELEASE_FIRST = re.compile(r"instalação\s+limpa")


def recipe_refuses_ci_as_first_run(text):
    return bool(text and RELEASE_FIRST.search(text))


def ship_ci_first_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_ci_as_first_run(text):
        return "recipes/release.md"
    return None


def ship_ci_first_scope():
    if not ship_ci_first_source():
        return None
    return (
        " O disco recusa que a CI seja a primeira execução "
        "(`primeira`). Fluxo no disco não é instalação limpa."
    )


def ship_ci_scope():
    scope = (
        "fluxo de CI no disco. "
        "Não executa o artefato e não instala limpo."
    )
    named = ship_ci_first_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que emulação e
# redimensionar uma janela substituam
# a plataforma real. Sem isto o ship
# listava o script e calava a recusa.
# Script no disco não é o dispositivo.
RELEASE_EMULATION = re.compile(r"Emulação e redimensionar\s+uma janela")


def recipe_refuses_emulation_as_real_platform(text):
    return bool(text and RELEASE_EMULATION.search(text))


def ship_emulation_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_emulation_as_real_platform(text):
        return "recipes/release.md"
    return None


def ship_emulation_scope():
    if not ship_emulation_source():
        return None
    return (
        " O disco recusa que emulação e redimensionar uma janela "
        "substituam a plataforma real (`emulação`). Script no disco "
        "não é o dispositivo."
    )


def ship_scripts_scope():
    scope = (
        "script de empacote no disco. "
        "Não executa o artefato."
    )
    named = ship_emulation_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que nomear o
# comando execute. Sem isto o ship
# relatava a linha e calava a recusa.
# Comando no disco não é outra máquina.
RELEASE_EXECUTE = re.compile(r"Nomear não executa")


def recipe_refuses_naming_as_execution(text):
    return bool(text and RELEASE_EXECUTE.search(text))


def ship_execute_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_naming_as_execution(text):
        return "recipes/release.md"
    return None


def ship_execute_scope():
    if not ship_execute_source():
        return None
    return (
        " O disco recusa que nomear o comando execute "
        "(`execução`). Comando no disco não é outra máquina."
    )


def ship_open_scope():
    scope = (
        "comando que serve dist/ no disco. "
        "Não executa o artefato."
    )
    named = ship_execute_scope()
    if named:
        scope += named
    return scope


def ship_open_command(pack):
    opened = (pack or {}).get("artifact_open")
    if isinstance(opened, dict):
        return opened.get("command")
    return opened


# A receita já recusa que compartilhar
# o convite seja elsewhere. Sem isto
# o ship relatava o release e calava
# a recusa. Arquivo no disco não é
# outra máquina.
RELEASE_SHARE = re.compile(r"Compartilhar o convite não é")


def recipe_refuses_invite_share_as_elsewhere(text):
    return bool(text and RELEASE_SHARE.search(text))


def ship_release_share_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_invite_share_as_elsewhere(text):
        return "recipes/release.md"
    return None


def ship_release_share_scope():
    if not ship_release_share_source():
        return None
    return (
        " O disco recusa que compartilhar o convite seja elsewhere "
        "(`compartilhar`). Arquivo no disco não é outra máquina."
    )


def ship_release_scope():
    scope = (
        "docs/release.md no disco. "
        "Não entrega o artefato."
    )
    named = ship_release_share_scope()
    if named:
        scope += named
    return scope


def ship_release_path(pack):
    release = (pack or {}).get("release")
    if isinstance(release, dict):
        return release.get("path")
    return release


# A receita já recusa autorizar
# publicar. Sem isto o ship
# relatava o vigente e calava a
# recusa. Arquivo no disco não é
# outra máquina.
RELEASE_AUTHORIZE = re.compile(r"Nada nesta receita autoriza publicar")


def recipe_refuses_text_as_authorizing_publish(text):
    return bool(text and RELEASE_AUTHORIZE.search(text))


def ship_release_current_authorize_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_text_as_authorizing_publish(text):
        return "recipes/release.md"
    return None


def ship_release_current_authorize_scope():
    if not ship_release_current_authorize_source():
        return None
    return (
        " O disco recusa que a receita autorize publicar "
        "(`autoriza`). Arquivo no disco não é outra máquina."
    )


def ship_release_current_scope():
    scope = (
        "docs/release.md vigente no disco. "
        "Não autoriza publicar."
    )
    named = ship_release_current_authorize_scope()
    if named:
        scope += named
    return scope


def ship_release_current_flag(reading):
    current = (reading or {}).get("release_current")
    if isinstance(current, dict):
        return bool(current.get("release_current"))
    return bool(current)


# A receita já recusa que o
# ambiente de desenvolvimento
# seja o artefato. Sem isto o
# ship relatava o pacote e
# calava a recusa. Pacote no
# disco não é outra máquina.
RELEASE_ENVIRONMENT = re.compile(r"não o ambiente de desenvolvimento")


def recipe_refuses_environment_as_artifact(text):
    return bool(text and RELEASE_ENVIRONMENT.search(text))


def ship_expected_environment_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_environment_as_artifact(text):
        return "recipes/release.md"
    return None


def ship_expected_environment_scope():
    if not ship_expected_environment_source():
        return None
    return (
        " O disco recusa que o ambiente de desenvolvimento seja o artefato "
        "(`ambiente`). Pacote no disco não é outra máquina."
    )


def ship_expected_scope():
    scope = (
        "package ou Cargo no disco. "
        "Não é o artefato exportado."
    )
    named = ship_expected_environment_scope()
    if named:
        scope += named
    return scope


def ship_expected_flag(reading):
    expected = (reading or {}).get("expected")
    if isinstance(expected, dict):
        return bool(expected.get("expected"))
    return bool(expected)


# A receita já recusa que a árvore
# sem os quatro seja jogável. Sem
# isto o ship relatava o bool e
# calava a recusa. Arquivo no
# disco não é outra máquina.
RELEASE_PLAYABLE = re.compile(r"Árvore sem esses\s+quatro")


def recipe_refuses_tree_without_four_as_playable(text):
    return bool(text and RELEASE_PLAYABLE.search(text))


def ship_incomplete_playable_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_tree_without_four_as_playable(text):
        return "recipes/release.md"
    return None


def ship_incomplete_playable_scope():
    if not ship_incomplete_playable_source():
        return None
    return (
        " O disco recusa que a árvore sem os quatro seja jogável "
        "(`jogável`). Arquivo no disco não é outra máquina."
    )


def ship_incomplete_scope():
    scope = (
        "árvore incompleta no disco. "
        "Não é árvore jogável."
    )
    named = ship_incomplete_playable_scope()
    if named:
        scope += named
    return scope


def ship_incomplete_flag(reading):
    incomplete = (reading or {}).get("incomplete")
    if isinstance(incomplete, dict):
        return bool(incomplete.get("incomplete"))
    return bool(incomplete)


# A receita já recusa que o HEAD
# diferente seja outra máquina.
# Sem isto o ship relatava o stale
# e calava a recusa. Arquivo no
# disco não é outra máquina.
SHIP_STALE_OLD = re.compile(r"HEAD diferente não é outra máquina")


def recipe_refuses_different_head_as_another_machine(text):
    return bool(text and SHIP_STALE_OLD.search(text))


def ship_stale_old_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_different_head_as_another_machine(text):
        return "recipes/release.md"
    return None


def ship_stale_old_scope():
    if not ship_stale_old_source():
        return None
    return (
        " O disco recusa que o HEAD diferente seja outra máquina "
        "(`velho`). Arquivo no disco não é outra máquina."
    )


def ship_stale_scope():
    scope = (
        "HEAD do artefato diferente do checkout. "
        "Não é outra máquina."
    )
    named = ship_stale_old_scope()
    if named:
        scope += named
    return scope


def ship_stale_flag(reading):
    stale = (reading or {}).get("stale") if isinstance(reading, dict) else reading
    if isinstance(stale, dict):
        return bool(stale.get("stale"))
    return bool(stale)


def ship_stale_reading(stale):
    if not stale:
        return False
    return {
        "stale": True,
        "scope": ship_stale_scope(),
    }


# A receita já recusa que o
# pacote sem passo seja o
# empacote. Sem isto o ship
# relatava o unpacked e calava
# a recusa. Manifesto no disco
# não é outra máquina.
SHIP_UNPACKED = re.compile(r"Pacote sem passo não é o empacote")


def recipe_refuses_package_without_step_as_pack(text):
    return bool(text and SHIP_UNPACKED.search(text))


def ship_unpacked_pack_source():
    path = FRAMEWORK / "recipes/release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_package_without_step_as_pack(text):
        return "recipes/release.md"
    return None


def ship_unpacked_pack_scope():
    if not ship_unpacked_pack_source():
        return None
    return (
        " O disco recusa que o pacote sem passo seja o empacote "
        "(`empacote`). Manifesto no disco não é outra máquina."
    )


def ship_unpacked_scope():
    scope = (
        "package ou Cargo sem passo de empacotar. "
        "Não é outra máquina."
    )
    named = ship_unpacked_pack_scope()
    if named:
        scope += named
    return scope


def ship_unpacked_flag(reading):
    unpacked = (reading or {}).get("unpacked") if isinstance(reading, dict) else reading
    if isinstance(unpacked, dict):
        return bool(unpacked.get("unpacked"))
    return bool(unpacked)


def ship_unpacked_reading(unpacked):
    if not unpacked:
        return False
    return {
        "unpacked": True,
        "scope": ship_unpacked_scope(),
    }


def ship_script_names(project):
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
    return named


def ship_reading(project):
    project = Path(project)
    named = ship_script_names(project)
    ci = ship_ci(project)
    release = project / SHIP_RELEASE
    release_current = document_is_current(release)
    if ci:
        ci = {
            "paths": ci,
            "scope": ship_ci_scope(),
        }
    artifact = ship_artifact(project)
    if artifact is not None:
        artifact = dict(artifact, scope=ship_artifact_scope())
    tree = ship_tree(project)
    if tree is not None:
        tree = dict(tree, scope=ship_tree_scope())
    stale = ship_stale(artifact, project)
    expected = (project / "package.json").is_file() or (project / "Cargo.toml").is_file()
    declared = bool(named or ci or release_current)
    unpacked = expected and not declared
    if expected:
        expected = {
            "expected": True,
            "scope": ship_expected_scope(),
        }
    if named:
        named = {
            "names": named,
            "scope": ship_scripts_scope(),
        }
    incomplete = bool(tree) and not tree["complete"]
    if incomplete:
        incomplete = {
            "incomplete": True,
            "scope": ship_incomplete_scope(),
        }
    artifact_open = artifact_open_command(project)
    if artifact_open:
        artifact_open = {
            "command": artifact_open,
            "scope": ship_open_scope(),
        }
    scope = (
        "Procura script build/export/dist/package/release, docs/release.md "
        "vigente e CI. Se dist/VERSION.json existe, relata nome e versão. "
        "Se a pasta dist/ de um jogo web existe, relata se index, serve, "
        "package e VERSION estão lá, e se o HEAD do artefato é o HEAD "
        "atual. Nomeia a árvore que perdeu o `src/` que o projeto já tem. "
        "Nomear não devolve o jogo. Árvore completa no HEAD atual ganha "
        "`artifact_open` — o comando que serve dist/. Nomear não executa. "
        "Não executa o export, não instala o artefato e não autoriza "
        "publicar. `shipped` e `elsewhere` são sempre falsos."
    )
    if ship_size_source(project):
        scope += (
            " O disco relata os bytes (`size`) sem teto. "
            "Bytes no disco não são outra máquina."
        )
    if ship_serve_source(project):
        scope += (
            " O disco nomeia a árvore exportada (`serve`). "
            "Banner no disco não é outra máquina."
        )
    if ship_export_source(project):
        scope += (
            " O disco empacota a árvore (`export`). "
            "Empacotar no disco não é outra máquina."
        )
    if ship_file_source(project):
        scope += (
            " O disco recusa o file:// (`file://`). "
            "Recusar no disco não é outra máquina."
        )
    access = ship_access_scope()
    if access:
        scope += access
    ceiling = ship_ceiling_scope()
    if ceiling:
        scope += ceiling
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "expected": expected,
        "scripts": named,
        "ci": ci,
        "release": (
            {
                "path": SHIP_RELEASE,
                "scope": ship_release_scope(),
            }
            if release.is_file() and not release.is_symlink()
            else None
        ),
        "release_current": (
            {
                "release_current": True,
                "scope": ship_release_current_scope(),
            }
            if release_current else False
        ),
        "artifact": artifact,
        "tree": tree,
        "incomplete": incomplete,
        "stale": ship_stale_reading(stale),
        "artifact_open": artifact_open,
        "elsewhere": False,
        "declared": declared,
        "unpacked": ship_unpacked_reading(unpacked),
        "shipped": False,
        "guide": str(FRAMEWORK / "recipes/release.md"),
        "rule": (
            "Script de build não é artefato que outra pessoa executou. HTML "
            "estático sem manifesto já é o artefato; manifesto sem passo de "
            "empacotar é o que este leitor nomeia. VERSION.json sozinho não "
            "é árvore jogável. dist/ sem o src/ que o projeto já tem também "
            "não. HEAD diferente não é outra máquina."
        ),
        "scope": scope,
    }


# Playtest com métricas: a tabela de ofício já pede problema, evidência,
# hipótese e medição. Até aqui o harness só via se o projeto declarava o
# checklist. Uma observação solta ("o dash não tem peso") não é achado.
# O leitor abaixo pergunta se a forma está no disco — não se alguém jogou.
FINDING_FIELDS = re.compile(
    r"(?is)(?:^|\n)\s*(?:[-*]|\d+\.)?\s*\*?\*?(?:problema|problem)\*?\*?\s*[:—]\s*\S"
    r".{0,400}?"
    r"(?:^|\n)\s*(?:[-*]|\d+\.)?\s*\*?\*?(?:evid[eê]ncia|evidence)\*?\*?\s*[:—]\s*\S"
    r".{0,400}?"
    r"(?:^|\n)\s*(?:[-*]|\d+\.)?\s*\*?\*?(?:hip[oó]tese|hypothesis)\*?\*?\s*[:—]\s*\S"
    r".{0,400}?"
    r"(?:^|\n)\s*(?:[-*]|\d+\.)?\s*\*?\*?(?:medi[cç][aã]o|measurement)\*?\*?\s*[:—]\s*\S"
)
# O Copiar já levava os quatro nomes. Sem isto o markdown
# calava a faixa que a página já mostra. Número no disco
# não é alguém de fora.
FINDING_RUN_MARK = re.compile(
    r"(?:function\s+)?composeFinding\([\s\S]{0,800}?runFacts\("
)


def finding_carries_run_facts(text):
    return bool(text and FINDING_RUN_MARK.search(text))


def finding_run_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, ROLE_CODE_SUFFIXES):
        if finding_carries_run_facts(text):
            return relative
    return None


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
# Os quatro nomes que `note --field` grava. O esqueleto mora no
# template; `guide` continua a receita. Sem `then`: este leitor só lê.
PLAYTEST_FIELDS = ("problema", "evidencia", "hipotese", "medicao")
PLAYTEST_FORM = FRAMEWORK / "assets/templates/qa.md"


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


# A receita já recusa que o esqueleto
# no disco seja achado. Sem isto o
# playtest listava o arquivo e calava
# a recusa. Arquivo no disco não é
# a sessão.
FEEL_SKELETON = re.compile(r"Esqueleto no disco não é achado")


def recipe_refuses_skeleton_as_finding(text):
    return bool(text and FEEL_SKELETON.search(text))


def playtest_skeleton_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_skeleton_as_finding(text):
        return "recipes/feel.md"
    return None


def playtest_skeleton_scope():
    if not playtest_skeleton_source():
        return None
    return (
        " O disco recusa que o esqueleto no disco seja achado "
        "(`esqueleto`). Arquivo no disco não é a sessão."
    )


def playtest_findings_scope():
    scope = (
        "achado no disco. "
        "Não assiste a sessão."
    )
    named = playtest_skeleton_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que o gravado
# seja alguém de fora. Sem isto o
# playtest listava o anexo e calava
# a recusa. Arquivo no disco não é
# a sessão.
FEEL_RECORDED = re.compile(r"Gravado\s+não é alguém de fora")


def recipe_refuses_recorded_as_outsider(text):
    return bool(text and FEEL_RECORDED.search(text))


def playtest_recorded_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_recorded_as_outsider(text):
        return "recipes/feel.md"
    return None


def playtest_recorded_scope():
    if not playtest_recorded_source():
        return None
    return (
        " O disco recusa que o gravado seja alguém de fora "
        "(`gravado`). Arquivo no disco não é a sessão."
    )


def playtest_attachments_scope():
    scope = (
        "anexo no disco. "
        "Não assiste a sessão."
    )
    named = playtest_recorded_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que nomear o
# leitor observe. Sem isto o
# playtest listava o recibo e calava
# a recusa. Arquivo no disco não é
# a sessão.
FEEL_READER = re.compile(r"Nomear o leitor não observa")


def recipe_refuses_naming_reader_as_observation(text):
    return bool(text and FEEL_READER.search(text))


def playtest_reader_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_naming_reader_as_observation(text):
        return "recipes/feel.md"
    return None


def playtest_reader_scope():
    if not playtest_reader_source():
        return None
    return (
        " O disco recusa que nomear o leitor observe "
        "(`recibo`). Arquivo no disco não é a sessão."
    )


def playtest_observations_scope():
    scope = (
        "recibo de observação no disco. "
        "Não assiste a sessão."
    )
    named = playtest_reader_scope()
    if named:
        scope += named
    return scope


LAST_RUN = "docs/playtest/last-run.json"
INVITE = "docs/playtest/invite.md"
INIT_COPY_SKIP = {"dist", "node_modules", ".git", "__pycache__"}


def last_run_path(project):
    path = Path(project) / LAST_RUN
    if path.is_file() and not path.is_symlink():
        return LAST_RUN
    return None


# A receita já recusa que ?seed=
# no disco seja Continuar. Sem isto
# o playtest relatava o last-run e
# calava a recusa. Arquivo no disco
# não é a sessão.
PERSIST_CONTINUE = re.compile(r"não é Continuar")


def recipe_refuses_seed_as_continue(text):
    return bool(text and PERSIST_CONTINUE.search(text))


def playtest_candidate_continue_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_seed_as_continue(text):
        return "recipes/persistence.md"
    return None


def playtest_candidate_continue_scope():
    if not playtest_candidate_continue_source():
        return None
    return (
        " O disco recusa que o last-run seja Continuar "
        "(`continuar`). Arquivo no disco não é a sessão."
    )


def playtest_candidate_scope():
    scope = (
        "last-run no disco. "
        "Não observa a sessão."
    )
    named = playtest_candidate_continue_scope()
    if named:
        scope += named
    return scope


def playtest_candidate_path(reading):
    candidate = (reading or {}).get("candidate")
    if isinstance(candidate, dict):
        return candidate.get("path")
    return candidate


def last_run_seed(project):
    path = Path(project) / LAST_RUN
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    seed = data.get("seed")
    if seed is None and isinstance(data.get("run"), dict):
        seed = data["run"].get("seed")
    if isinstance(seed, int) and not isinstance(seed, bool):
        return seed
    return None


# A receita já recusa que o número
# no disco seja causa. Sem isto o
# playtest relatava a seed e calava
# a recusa. Número no disco não é
# a sessão.
FEEL_CAUSE = re.compile(r"Número\s+no disco não é causa")


def recipe_refuses_number_as_cause(text):
    return bool(text and FEEL_CAUSE.search(text))


def playtest_seed_cause_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_number_as_cause(text):
        return "recipes/feel.md"
    return None


def playtest_seed_cause_scope():
    if not playtest_seed_cause_source():
        return None
    return (
        " O disco recusa que o número no disco seja causa "
        "(`atribuição`). Número no disco não é a sessão."
    )


def playtest_seed_scope():
    scope = (
        "seed no last-run. "
        "Não observa a sessão."
    )
    named = playtest_seed_cause_scope()
    if named:
        scope += named
    return scope


SPAWN_NAME = re.compile(r"^[a-z][a-z0-9]{0,31}$")


def last_run_spawn(project):
    path = Path(project) / LAST_RUN
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    spawn = data.get("spawn")
    if not nonempty(spawn) and isinstance(data.get("run"), dict):
        spawn = data["run"].get("spawn")
    if isinstance(spawn, str) and SPAWN_NAME.fullmatch(spawn) and spawn != "spawn":
        return spawn
    return None


# A receita já recusa que a chuva
# da outra mesa retome o hold. Sem
# isto o playtest relatava a mesa e
# calava a recusa. Mesa no disco
# não é a sessão.
LIFECYCLE_RESUME = re.compile(r"não retoma o hold")


def recipe_refuses_spawn_as_resume(text):
    return bool(text and LIFECYCLE_RESUME.search(text))


def playtest_spawn_resume_source():
    path = FRAMEWORK / "recipes/lifecycle.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_spawn_as_resume(text):
        return "recipes/lifecycle.md"
    return None


def playtest_spawn_resume_scope():
    if not playtest_spawn_resume_source():
        return None
    return (
        " O disco recusa que a chuva da outra mesa retome o hold "
        "(`retoma`). Mesa no disco não é a sessão."
    )


def playtest_spawn_scope():
    scope = (
        "mesa no last-run. "
        "Não observa a sessão."
    )
    named = playtest_spawn_resume_scope()
    if named:
        scope += named
    return scope


def playtest_candidate_spawn(reading):
    spawn = (reading or {}).get("candidate_spawn")
    if isinstance(spawn, dict):
        return spawn.get("spawn")
    return spawn


def last_run_curve(project):
    # A faixa e o leitor viam seed e some a curva.
    # last-run.json já a traçou. Número não é outsider.
    path = Path(project) / LAST_RUN
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    curve = data.get("curve")
    if not isinstance(curve, dict) and isinstance(data.get("run"), dict):
        curve = data["run"].get("curve")
    if not isinstance(curve, dict):
        return None
    facts = {}
    if isinstance(curve.get("never_banked"), bool):
        facts["never_banked"] = curve["never_banked"]
    unbanked = curve.get("unbanked_at_end")
    if isinstance(unbanked, (int, float)) and not isinstance(unbanked, bool) and unbanked > 0:
        facts["unbanked_at_end"] = unbanked
    return facts or None


# A receita já recusa que o aperto seja curva observada.
# Sem isto a curva copiava never_banked e calava a recusa.
# Número no disco não é sessão.
CONTENT_SQUEEZE = re.compile(r"Aperto no disco não é curva observada")


def recipe_refuses_squeeze_as_curve(text):
    return bool(text and CONTENT_SQUEEZE.search(text))


def playtest_curve_squeeze_source():
    path = FRAMEWORK / "recipes/content.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_squeeze_as_curve(text):
        return "recipes/content.md"
    return None


def playtest_curve_scope():
    scope = (
        "never_banked e a aposta que ficou no last-run. "
        "Não observa a sessão e não mede o fecho."
    )
    if playtest_curve_squeeze_source():
        scope += (
            " O disco recusa que o aperto seja curva observada (`aperto`). "
            "Número no disco não é sessão."
        )
    close = playtest_curve_close_scope()
    if close:
        scope += close
    return scope


# A receita já recusa que o fecho
# seja faixa no HUD. Sem isto a
# curva copiava never_banked e
# calava a recusa. Fecho no disco
# não é a faixa.
FEEL_CLOSE = re.compile(r"não é faixa no HUD")


def recipe_refuses_close_as_hud_bar(text):
    return bool(text and FEEL_CLOSE.search(text))


def playtest_curve_close_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_close_as_hud_bar(text):
        return "recipes/feel.md"
    return None


def playtest_curve_close_scope():
    if not playtest_curve_close_source():
        return None
    return (
        " O disco recusa que o fecho seja faixa no HUD "
        "(`fecho`). Fecho no disco não é a faixa."
    )


TALLY_FIELDS = ("score", "collected", "missed", "hits", "banks")


def last_run_tally(project):
    # A faixa e o last-run já têm a conta. Sem isto o
    # playtest nomeava curva e origem e calava os verbos.
    # Número no disco não é alguém de fora.
    path = Path(project) / LAST_RUN
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    run = data["run"] if isinstance(data.get("run"), dict) else data
    if not isinstance(run, dict):
        return None
    facts = {}
    for field in TALLY_FIELDS:
        value = run.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        if isinstance(value, float) and not (value == value):
            continue
        facts[field] = int(value) if isinstance(value, int) or value.is_integer() else value
    return facts or None


# A pesquisa já recusa que cinco playtesters sejam critério.
# Sem isto a conta copiava os verbos e calava a recusa.
# Conta no disco não é sessão observada.
PLAYTEST_FIVE = re.compile(r'"Cinco playtesters"\s+não\s+é\s+critério')


def research_refuses_five_as_criterion(text):
    return bool(text and PLAYTEST_FIVE.search(text))


def playtest_tally_five_source():
    path = FRAMEWORK / "references/observable-criteria-research.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if research_refuses_five_as_criterion(text):
        return "references/observable-criteria-research.md"
    return None


def playtest_tally_scope():
    scope = (
        "Pontos, coletas, quedas, erros e guardas do last-run. "
        "Não conta jogadores e não observa a sessão."
    )
    if playtest_tally_five_source():
        scope += (
            " O disco recusa que cinco playtesters sejam critério (`cinco`). "
            "Conta no disco não é sessão observada."
        )
    named = playtest_tally_four_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que o número na faixa
# preencha os quatro. Sem isto a conta
# copiava os verbos e calava a recusa.
# Conta no disco não é achado.
FEEL_FOUR = re.compile(r"Número na faixa não\s+preenche os quatro")


def recipe_refuses_band_as_four(text):
    return bool(text and FEEL_FOUR.search(text))


def playtest_tally_four_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_band_as_four(text):
        return "recipes/feel.md"
    return None


def playtest_tally_four_scope():
    if not playtest_tally_four_source():
        return None
    return (
        " O disco recusa que o número na faixa preencha os quatro "
        "(`quatro`). Conta no disco não é achado."
    )


# A receita já recusa que a origem no last-run
# seja sessão observada. Sem isto o playtest
# relatava played/nearest-orb e calava a recusa.
# Texto no disco não é alguém de fora.
FEEL_ORIGIN = re.compile(r"Nenhum dos dois é sessão observada")


def recipe_refuses_policy_as_observed_session(text):
    return bool(text and FEEL_ORIGIN.search(text))


def playtest_policy_origin_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_policy_as_observed_session(text):
        return "recipes/feel.md"
    return None


def playtest_policy_origin_scope():
    if not playtest_policy_origin_source():
        return None
    return (
        " O disco recusa que a origem no last-run seja sessão "
        "observada (`origem`). Texto no disco não é alguém de fora."
    )


def playtest_policy_scope():
    scope = (
        "played ou nearest-orb no last-run. "
        "Não observa a sessão e não atribui causa."
    )
    named = playtest_policy_origin_scope()
    if named:
        scope += named
    return scope


def last_run_speed(project):
    # O convite abria a seed no relógio cheio. last-run já
    # guarda o knob. 1 some. Número não é outsider.
    path = Path(project) / LAST_RUN
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    speed = data.get("speed")
    if speed is None and isinstance(data.get("run"), dict):
        speed = data["run"].get("speed")
    if (
        isinstance(speed, (int, float))
        and not isinstance(speed, bool)
        and 0.5 <= speed <= 1
        and speed != 1
    ):
        return speed
    return None


# A receita já recusa que simular no
# relógio cheio observe. Sem isto o
# playtest relatava o knob e calava a recusa.
# Número no disco não é alguém de fora.
FEEL_FULL_CLOCK = re.compile(r"Simular\s+no relógio cheio não observa")


def recipe_refuses_full_clock_as_observation(text):
    return bool(text and FEEL_FULL_CLOCK.search(text))


def playtest_speed_full_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_full_clock_as_observation(text):
        return "recipes/feel.md"
    return None


def playtest_speed_full_scope():
    if not playtest_speed_full_source():
        return None
    return (
        " O disco recusa que simular no relógio cheio observe "
        "(`cheio`). Número no disco não é alguém de fora."
    )


def playtest_speed_scope():
    scope = (
        "relógio no last-run diferente de 1. "
        "Não observa a sessão e não atribui causa."
    )
    named = playtest_speed_full_scope()
    if named:
        scope += named
    return scope


def last_run_policy(project):
    # Serve grava played; session grava nearest-orb.
    # Sem a chave o leitor fingia a mesma origem.
    # Nomear não é sessão observada.
    path = Path(project) / LAST_RUN
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    policy = data.get("policy")
    if policy is None and isinstance(data.get("run"), dict):
        policy = data["run"].get("policy")
    if policy in {"played", "nearest-orb"}:
        return policy
    return None


def last_run_look(project):
    path = Path(project) / LAST_RUN
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    look = data.get("look")
    if not nonempty(look) and isinstance(data.get("run"), dict):
        look = data["run"].get("look")
    if isinstance(look, str) and SPAWN_NAME.fullmatch(look) and look not in {"normal", "contrast"}:
        return look
    return None


# A receita já recusa que o contrast
# seja look de arte. Sem isto o
# playtest relatava a paleta e
# calava a recusa. Paleta no disco
# não é a sessão.
ACCESS_ART_LOOK = re.compile(r"contrast não é look de arte")


def recipe_refuses_contrast_as_art_look(text):
    return bool(text and ACCESS_ART_LOOK.search(text))


def playtest_look_art_source():
    path = A11Y_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_contrast_as_art_look(text):
        return "recipes/accessibility.md"
    return None


def playtest_look_art_scope():
    if not playtest_look_art_source():
        return None
    return (
        " O disco recusa que o contrast seja look de arte "
        "(`arte`). Paleta no disco não é a sessão."
    )


def playtest_look_scope():
    scope = (
        "look no last-run diferente de normal e contrast. "
        "Não observa a sessão."
    )
    named = playtest_look_art_scope()
    if named:
        scope += named
    return scope


def playtest_candidate_look(reading):
    look = (reading or {}).get("candidate_look")
    if isinstance(look, dict):
        return look.get("look")
    return look


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
    policy = data.get("policy")
    if policy is None and isinstance(run, dict):
        policy = run.get("policy")
    if policy in {"played", "nearest-orb"}:
        payload["policy"] = policy
    return payload, path


# A receita já grava a simulação. Sem isto o playtest
# lia last-run e calava o tool. Traço no disco não é
# alguém de fora.
SESSION_FILES = ("tools/session.mjs", "tools/session.js", "tools/session.py")
SESSION_TRACE = re.compile(
    r"não some sob a simulação|não é sessão observada",
    re.IGNORECASE,
)


def session_records_sim(text):
    return bool(text and SESSION_TRACE.search(text))


def session_sim_source(project):
    project = Path(project)
    for name in SESSION_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if session_records_sim(text):
            return name
    return None


# A página já pede o recado. Sem isto o playtest
# dizia que a página escreve e calava a rota.
# Texto no disco não é alguém de fora.
NOTE_POST = re.compile(r"pathname === NOTE_ROUTE")


def serve_writes_note(text):
    return bool(text and NOTE_POST.search(text))


def note_post_source(project):
    project = Path(project)
    for name in SERVE_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if serve_writes_note(text):
            return name
    return None


# A receita já recusa que os quatro
# no disco sejam playtest observado.
# Sem isto o playtest relatava o
# structured e calava a recusa.
# Arquivo no disco não é a sessão.
PLAYTEST_OBSERVED = re.compile(r"quatro no disco não são playtest observado")


def recipe_refuses_four_fields_as_observed_playtest(text):
    return bool(text and PLAYTEST_OBSERVED.search(text))


def playtest_structured_observed_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_four_fields_as_observed_playtest(text):
        return "recipes/feel.md"
    return None


def playtest_structured_observed_scope():
    if not playtest_structured_observed_source():
        return None
    return (
        " O disco recusa que os quatro no disco sejam playtest observado "
        "(`observado`). Arquivo no disco não é a sessão."
    )


def playtest_structured_scope():
    scope = (
        "achado com os quatro no disco. "
        "O playtest não observa a sessão."
    )
    named = playtest_structured_observed_scope()
    if named:
        scope += named
    return scope


def playtest_structured_flag(reading):
    structured = (reading or {}).get("structured") if isinstance(reading, dict) else reading
    if isinstance(structured, dict):
        return bool(structured.get("structured"))
    return bool(structured)


def playtest_structured_reading(structured):
    if not structured:
        return False
    return {
        "structured": True,
        "scope": playtest_structured_scope(),
    }


def playtest_reading(project):
    project = Path(project)
    observations = observation_receipts(project)
    findings = playtest_findings(project)
    qa = project / "docs/qa.md"
    qa_current = document_is_current(qa)
    expected = bool(observations) or qa_current
    structured = bool(findings)
    unstructured = expected and not structured
    candidate = last_run_path(project)
    if candidate:
        candidate = {
            "path": candidate,
            "scope": playtest_candidate_scope(),
        }
    candidate_seed = last_run_seed(project) if candidate else None
    if candidate_seed is not None:
        candidate_seed = {
            "seed": candidate_seed,
            "scope": playtest_seed_scope(),
        }
    candidate_spawn = last_run_spawn(project) if candidate else None
    if candidate_spawn is not None:
        candidate_spawn = {
            "spawn": candidate_spawn,
            "scope": playtest_spawn_scope(),
        }
    candidate_look = last_run_look(project) if candidate else None
    if candidate_look is not None:
        candidate_look = {
            "look": candidate_look,
            "scope": playtest_look_scope(),
        }
    candidate_speed = last_run_speed(project) if candidate else None
    if candidate_speed is not None:
        candidate_speed = {
            "speed": candidate_speed,
            "scope": playtest_speed_scope(),
        }
    candidate_curve = last_run_curve(project) if candidate else None
    if candidate_curve is not None:
        candidate_curve = dict(candidate_curve, scope=playtest_curve_scope())
    candidate_policy = last_run_policy(project) if candidate else None
    if candidate_policy is not None:
        candidate_policy = {
            "policy": candidate_policy,
            "scope": playtest_policy_scope(),
        }
    candidate_tally = last_run_tally(project) if candidate else None
    if candidate_tally is not None:
        candidate_tally = dict(candidate_tally, scope=playtest_tally_scope())
    invite = invite_path(project)
    if invite:
        invite = {
            "path": invite,
            "scope": playtest_invite_scope(),
        }
    qa_file = qa.is_file() and not qa.is_symlink()
    try:
        scripts, _manager = project_commands(project)
    except (OSError, ValueError):
        scripts = {}
    # O next já apontava finding_open. Sem isto o
    # playtest mandava só o caminho relativo — o
    # serve ficava no disco e o leitor calava.
    # Endereço no disco não é alguém de fora.
    opened = finding_open(project, scripts)
    scope = (
        "Procura os quatro campos num documento ou num record de "
        "observação, e se docs/qa.md deixou de ser rascunho. Relata "
        f"`{LAST_RUN}` e `{INVITE}` quando existem. A partida no serve "
        "pode gravar o candidato; a simulação também. No convite a "
        "página pode gravar o markdown dos quatro nomes e anexar o "
        "candidato que estava em last-run.json. Anexo não é sessão "
        "observada. Se o candidato nomeia a seed, `candidate_seed` "
        "a relata; se nomeia a chuva, `candidate_spawn` a relata; "
        "se nomeia o look, `candidate_look` o relata; "
        "se nomeia o relógio, `candidate_speed` o relata; "
        "se nomeia a curva, `candidate_curve` relata "
        "`never_banked` e a aposta que ficou; "
        "se nomeia a origem, `candidate_policy` relata "
        "`played` ou `nearest-orb`; "
        "se nomeia a conta, `candidate_tally` relata "
        "pontos, coletas, quedas, erros e guardas. "
        "`invite_href` junta convite, número, mesa, paleta e relógio — "
        "`?invite=1&seed=&spawn=&look=&speed=` abre essa partida e ignora o hold. "
        "`finding_href` junta o convite e o painel `#finding` — "
        "sem `invite=1` o âncora some. "
        "`finding_open` é a url do serve com o convite, ou o "
        "mesmo endereço sem serve. O `next` aponta o mesmo "
        "endereço. O serve nu não abre o painel. "
        "com seed no disco junta o número e os eixos. "
        "`qa` nomeia `docs/qa.md` se o arquivo existir. "
        "`form` aponta o esqueleto dos quatro nomes; `fields` os lista. "
        "Esqueleto no disco não é achado. "
        "`playtest` só lê. Sem `then`. A página e `note --field` escrevem. "
        "Escrever não é sessão observada. "
        "Não assiste a sessão, não conta jogadores e não "
        "atribui causa. `observed` e `outsider` são sempre falsos."
    )
    if finding_run_source(project):
        scope += (
            " O Copiar e o Gravar levam a faixa do last-run — markdown "
            "no disco não é alguém de fora."
        )
    if session_sim_source(project):
        scope += (
            " O disco grava a simulação (`session`). "
            "Traço no disco não é alguém de fora."
        )
    if note_post_source(project):
        scope += (
            " O disco grava o recado (`note`). "
            "Texto no disco não é alguém de fora."
        )
    attachments = playtest_finding_attachments(project, findings)
    if findings:
        findings = {
            "paths": findings,
            "scope": playtest_findings_scope(),
        }
    if attachments:
        attachments = {
            "paths": attachments,
            "scope": playtest_attachments_scope(),
        }
    observed_paths = [item["path"] for item in observations]
    if observed_paths:
        observed_paths = {
            "paths": observed_paths,
            "scope": playtest_observations_scope(),
        }
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "observations": observed_paths,
        "findings": findings,
        "finding_attachments": attachments,
        "candidate": candidate,
        "candidate_seed": candidate_seed,
        "candidate_spawn": candidate_spawn,
        "candidate_look": candidate_look,
        "candidate_speed": candidate_speed,
        "candidate_curve": candidate_curve,
        "candidate_policy": candidate_policy,
        "candidate_tally": candidate_tally,
        "invite": invite,
        "invite_href": invite_href(project),
        "finding_href": finding_href(project),
        "finding_open": opened,
        "qa": (
            {
                "path": "docs/qa.md",
                "scope": playtest_qa_scope(),
            }
            if qa_file
            else None
        ),
        "qa_current": (
            {
                "qa_current": True,
                "scope": playtest_qa_current_scope(),
            }
            if qa_current else False
        ),
        "expected": expected,
        "structured": playtest_structured_reading(structured),
        "unstructured": unstructured,
        "observed": False,
        "outsider": False,
        "form": {
            "path": str(PLAYTEST_FORM),
            "scope": playtest_form_scope(),
        },
        "fields": {
            "names": list(PLAYTEST_FIELDS),
            "scope": playtest_fields_scope(),
        },
        "guide": str(FRAMEWORK / "recipes/feel.md"),
        "rule": (
            "Recibo de observação sem problema, evidência, hipótese e medição "
            "é impressão. Os quatro no disco não são playtest observado. "
            "last-run.json é candidato, não causa — venha da simulação ou "
            "da partida no serve. Convite no disco não é alguém de fora."
        ),
        "scope": scope,
    }


def playtest_finding_attachments(project, findings=None):
    project = Path(project)
    attached = []
    names = findings if findings is not None else playtest_findings(project)
    for relative in names:
        if not relative.endswith("-achado.md"):
            continue
        companion = f"{relative[:-len('.md')]}.run.json"
        path = project / companion
        if not path.is_file() or path.is_symlink():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and isinstance(data.get("run"), dict):
            attached.append(companion)
    return attached


def invite_path(project):
    path = Path(project) / INVITE
    if path.is_file() and not path.is_symlink():
        return INVITE
    return None


# A receita já recusa que o convite
# seja preferência. Sem isto o
# playtest relatava a página e
# calava a recusa. Convite no disco
# não é a sessão.
PERSIST_PREFERENCE = re.compile(r"não\s+preferência")


def recipe_refuses_invite_as_preference(text):
    return bool(text and PERSIST_PREFERENCE.search(text))


def playtest_invite_preference_source():
    path = PERSIST_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_invite_as_preference(text):
        return "recipes/persistence.md"
    return None


def playtest_invite_preference_scope():
    if not playtest_invite_preference_source():
        return None
    return (
        " O disco recusa que o convite seja preferência "
        "(`preferência`). Convite no disco não é a sessão."
    )


def playtest_invite_scope():
    scope = (
        "página do convite no disco. "
        "Não observa a sessão."
    )
    named = playtest_invite_preference_scope()
    if named:
        scope += named
    return scope


def playtest_invite_path(reading):
    invite = (reading or {}).get("invite")
    if isinstance(invite, dict):
        return invite.get("path")
    return invite


# A receita já recusa que a
# simulação seja alguém de fora.
# Sem isto o playtest relatava o
# qa.md e calava a recusa. Arquivo
# no disco não é a sessão.
FEEL_SIMULATED = re.compile(r"Simulada não é alguém de\s+fora")


def recipe_refuses_sim_as_outsider(text):
    return bool(text and FEEL_SIMULATED.search(text))


def playtest_qa_sim_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_sim_as_outsider(text):
        return "recipes/feel.md"
    return None


def playtest_qa_sim_scope():
    if not playtest_qa_sim_source():
        return None
    return (
        " O disco recusa que a simulação seja alguém de fora "
        "(`simulada`). Arquivo no disco não é a sessão."
    )


def playtest_qa_scope():
    scope = (
        "docs/qa.md no disco. "
        "Não observa a sessão."
    )
    named = playtest_qa_sim_scope()
    if named:
        scope += named
    return scope


def playtest_qa_path(reading):
    qa = (reading or {}).get("qa")
    if isinstance(qa, dict):
        return qa.get("path")
    return qa


# A receita já recusa que o harness
# assista à sessão. Sem isto o
# playtest relatava o vigente e
# calava a recusa. Arquivo no disco
# não é a sessão.
FEEL_ATTEND = re.compile(r"não assiste à sessão")


def recipe_refuses_harness_as_attending_session(text):
    return bool(text and FEEL_ATTEND.search(text))


def playtest_qa_current_attend_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_harness_as_attending_session(text):
        return "recipes/feel.md"
    return None


def playtest_qa_current_attend_scope():
    if not playtest_qa_current_attend_source():
        return None
    return (
        " O disco recusa que o harness assista à sessão "
        "(`assiste`). Arquivo no disco não é a sessão."
    )


def playtest_qa_current_scope():
    scope = (
        "docs/qa.md vigente no disco. "
        "Não assiste à sessão."
    )
    named = playtest_qa_current_attend_scope()
    if named:
        scope += named
    return scope


def playtest_qa_current_flag(reading):
    qa_current = (reading or {}).get("qa_current")
    if isinstance(qa_current, dict):
        return bool(qa_current.get("qa_current"))
    return bool(qa_current)


# O molde já recusa que a regra de
# parada seja número de participantes.
# Sem isto o playtest apontava o
# esqueleto e calava a recusa.
# Arquivo no disco não é a sessão.
PLAYTEST_PARTICIPANTS = re.compile(r"não é número de participantes")


def form_refuses_stop_as_participants(text):
    return bool(text and PLAYTEST_PARTICIPANTS.search(text))


def playtest_form_participants_source():
    path = PLAYTEST_FORM
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if form_refuses_stop_as_participants(text):
        return "assets/templates/qa.md"
    return None


def playtest_form_participants_scope():
    if not playtest_form_participants_source():
        return None
    return (
        " O disco recusa que a regra de parada seja número de participantes "
        "(`participantes`). Arquivo no disco não é a sessão."
    )


def playtest_form_scope():
    scope = (
        "esqueleto de playtest no disco. "
        "Não observa a sessão."
    )
    named = playtest_form_participants_scope()
    if named:
        scope += named
    return scope


def playtest_form_path(reading):
    form = (reading or {}).get("form")
    if isinstance(form, dict):
        return form.get("path")
    return form


# O molde já recusa que os quatro
# no disco observem. Sem isto o
# playtest listava os nomes e
# calava a recusa. Arquivo no
# disco não é a sessão.
PLAYTEST_FOUR = re.compile(r"os quatro no disco não observam")


def form_refuses_four_as_observation(text):
    return bool(text and PLAYTEST_FOUR.search(text))


def playtest_fields_four_source():
    path = PLAYTEST_FORM
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if form_refuses_four_as_observation(text):
        return "assets/templates/qa.md"
    return None


def playtest_fields_four_scope():
    if not playtest_fields_four_source():
        return None
    return (
        " O disco recusa que os quatro no disco observem "
        "(`campos`). Arquivo no disco não é a sessão."
    )


def playtest_fields_scope():
    scope = (
        "os quatro nomes que o achado exige. "
        "Não observa a sessão."
    )
    named = playtest_fields_four_scope()
    if named:
        scope += named
    return scope


def playtest_field_names(reading):
    fields = (reading or {}).get("fields")
    if isinstance(fields, dict):
        return list(fields.get("names") or [])
    return list(fields or [])


def last_run_axes(project):
    parts = []
    spawn = last_run_spawn(project)
    if spawn:
        parts.append(f"spawn={spawn}")
    look = last_run_look(project)
    if look:
        parts.append(f"look={look}")
    speed = last_run_speed(project)
    if speed is not None:
        parts.append(f"speed={speed}")
    return parts


def seed_href(project):
    seed = last_run_seed(project)
    if not (isinstance(seed, int) and not isinstance(seed, bool)):
        return None
    return "/?" + "&".join([f"seed={seed}", *last_run_axes(project)])


def invite_href(project):
    parts = ["invite=1"]
    seed = last_run_seed(project)
    if isinstance(seed, int) and not isinstance(seed, bool):
        parts.append(f"seed={seed}")
    parts.extend(last_run_axes(project))
    return "/?" + "&".join(parts)


def finding_href(project):
    # O painel só nasce no convite. Sem invite=1 o
    # âncora cai em display:none. Endereço no disco
    # não é alguém de fora.
    return f"{invite_href(project)}#finding"


def finding_open(project, scripts=None, play=None, env=None):
    # O next apontava o serve nu. Sem o convite o
    # âncora some. SKILL e README já nomeiam a
    # página; o comando tem de apontá-la. Endereço
    # no disco não é alguém de fora.
    href = finding_href(project)
    base = serve_url(scripts, play, env)
    if not base:
        return href
    return f"{base.rstrip('/')}{href}"


# O serve já prende o bind. Sem isto o
# convite anunciava a rede e calava o HOST.
# Bind no disco não é alguém de fora.
SERVE_BIND = re.compile(r"HOST=127\.0\.0\.1 prende o bind")


def serve_pins_bind(text):
    return bool(text and SERVE_BIND.search(text))


def invite_bind_source(project):
    project = Path(project)
    for name in SERVE_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if serve_pins_bind(text):
            return name
    return None


# A receita já recusa duas sessões reais. Sem
# isto o convite anunciava o endereço e calava
# as sessões. Convite no disco não é alguém
# de fora.
NETWORK_RECIPE = FRAMEWORK / "recipes/network.md"
NETWORK_SESSIONS = re.compile(r"duas sessões reais")


def recipe_refuses_address_as_two_sessions(text):
    return bool(text and NETWORK_SESSIONS.search(text))


def invite_sessions_source():
    path = NETWORK_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if recipe_refuses_address_as_two_sessions(text):
        return "recipes/network.md"
    return None


def invite_sessions_scope():
    if not invite_sessions_source():
        return None
    return (
        "O disco recusa que o endereço seja duas sessões "
        "(`sessões`). Convite no disco não é alguém de fora."
    )


# A receita já recusa que rolar seja alguém
# de fora. Sem isto o convite anunciava o
# painel e calava a recusa. Página no disco
# não é a sessão.
FEEL_SCROLL = re.compile(r"Rolar não é alguém de fora")


def recipe_refuses_scroll_as_outsider(text):
    return bool(text and FEEL_SCROLL.search(text))


def invite_scroll_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_scroll_as_outsider(text):
        return "recipes/feel.md"
    return None


def invite_scroll_scope():
    if not invite_scroll_source():
        return None
    return (
        "O disco recusa que rolar seja alguém de fora "
        "(`rolar`). Página no disco não é a sessão."
    )


# A receita já recusa que nomear o
# endereço observe. Sem isto o
# invite relatava o created e
# calava a recusa. Arquivo no
# disco não é a sessão.
FEEL_ADDRESS = re.compile(r"Nomear o endereço não observa")


def recipe_refuses_naming_address_as_observing(text):
    return bool(text and FEEL_ADDRESS.search(text))


def invite_created_address_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_naming_address_as_observing(text):
        return "recipes/feel.md"
    return None


def invite_created_address_scope():
    if not invite_created_address_source():
        return None
    return (
        " O disco recusa que nomear o endereço observe "
        "(`endereço`). Arquivo no disco não é a sessão."
    )


def invite_created_scope():
    scope = (
        "página de convite escrita neste chamado. "
        "Não observa a sessão."
    )
    named = invite_created_address_scope()
    if named:
        scope += named
    return scope


def invite_created_flag(reading):
    created = (reading or {}).get("created")
    if isinstance(created, dict):
        return bool(created.get("created"))
    return bool(created)


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
    scope = (
        "Escreve a página para quem nunca viu o jogo e aponta "
        "`href`. Sem last-run é `/?invite=1`; com seed no disco "
        "junta o número; com chuva no disco junta a mesa; com look "
        "no disco junta a paleta. A tabela "
        "some. Depois do fim a página "
        "oferece os quatro nomes para copiar ou gravar. Copiar não "
        "grava. Esqueleto vazio não é achado. Gravado anexa o "
        "candidato se last-run existir — não é alguém de fora. "
        "Nomear o endereço não observa. O serve anuncia a URL da rede se a "
        "máquina tiver outro endereço IPv4. Não ensina o verbo, "
        "não assiste e não sobe pacing. outsider continua falso."
    )
    if invite_bind_source(project):
        scope += (
            " O disco prende o bind (`HOST`). "
            "Bind no disco não é alguém de fora."
        )
    named = invite_sessions_scope()
    if named:
        scope += " " + named
    scroll = invite_scroll_scope()
    if scroll:
        scope += " " + scroll
    return {
        "schema_version": 1,
        "project": str(project),
        "path": INVITE,
        "created": (
            {
                "created": True,
                "scope": invite_created_scope(),
            }
            if created else False
        ),
        "href": invite_href(project),
        "observed": False,
        "outsider": False,
        "reading": reading,
        "scope": scope,
    }


def invite_page(project):
    project = Path(project)
    try:
        scripts, manager = project_commands(project)
    except (OSError, ValueError):
        scripts, manager = {}, None
    artifact_open = artifact_open_command(project)
    play = artifact_open or play_command(project, scripts, manager) or (
        f"cd {shlex.quote(str(project))} && npm run serve"
    )
    href = invite_href(project)
    seed = last_run_seed(project)
    seed_line = (
        f"Esta partida abre em `/?seed={seed}` e ignora o hold."
        if isinstance(seed, int) and not isinstance(seed, bool)
        else "Se a partida deixou seed, `/?seed=<n>` abre essa partida e ignora o hold."
    )
    page = (
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
    )
    if artifact_open:
        page += (
            "Esse comando serve `dist/`, não a árvore de desenvolvimento.\n"
            "Na árvore exportada o serve recusa gravar o achado: copie os\n"
            "quatro nomes e devolva ao maker. Sem a área de transferência,\n"
            "o Copiar baixa o markdown. Recusar não é alguém de fora.\n"
            "\n"
        )
    page += (
        "## Superfície\n"
        "\n"
        f"No navegador, abra `{href}`. A tabela de comandos some.\n"
        "Quem fez o jogo fica em `/`. O serve anuncia localhost e, se a\n"
        "máquina tiver outro endereço IPv4, a URL da rede. Compartilhar\n"
        "essa URL não é alguém de fora.\n"
        "\n"
        "## Instrução\n"
        "\n"
        "Jogue uma partida. Com tela, o avanço abre a porta — a tabela\n"
        f"some, a abertura não. {seed_line} Quem fez o jogo não ensina\n"
        "o verbo e não fica atrás da cadeira.\n"
        "\n"
        "## Depois\n"
        "\n"
        "A página oferece os quatro nomes para copiar ou gravar.\n"
        "Depois do fim ela rola até o painel e foca o primeiro campo.\n"
        "Rolar não é alguém de fora. Trazer o painel não observa.\n"
        "Depois do fim ela mostra seed, pontos e eixos da partida.\n"
        "Número na faixa não preenche os quatro nomes. Copiar não grava.\n"
        "Sem a área de transferência, o Copiar baixa o markdown.\n"
        "Grave só se os quatro tiverem texto. Esqueleto vazio não é\n"
        "achado. Se a partida deixou last-run, o serve anexa o candidato\n"
        "ao lado do markdown. Anexo não é sessão observada. Gravado não\n"
        "sobe pacing.\n"
        "Quem escreveu precisa ser quem jogou.\n"
        "\n"
        "Convite no disco não sobe `pacing` e não conta jogador.\n"
    )
    return page


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
# Os três nomes que o sidecar declara. Recibo no disco não é licença válida.
ORIGIN_FIELDS = ("origin", "author", "license")
ORIGIN_FORM = FRAMEWORK / "assets/templates/credits.txt"
ORIGIN_ROW = re.compile(r"`([^`]+)`")
ORIGIN_LINK = re.compile(r"\[[^\]]+\]\((?:<([^>\n]+)>|([^\s)]+))")
# O molde já recusa que o crédito
# seja licença válida. Sem isto o
# origins apontava o form e calava
# a recusa. Arquivo no disco não é
# a concessão.
ORIGIN_CREDIT = re.compile(r"não é licença válida")


def form_refuses_credit_as_valid_license(text):
    return bool(text and ORIGIN_CREDIT.search(text))


def origins_form_credit_source():
    path = ORIGIN_FORM
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if form_refuses_credit_as_valid_license(text):
        return "assets/templates/credits.txt"
    return None


def origins_form_credit_scope():
    if not origins_form_credit_source():
        return None
    return (
        " O disco recusa que o crédito seja licença válida "
        "(`crédito`). Arquivo no disco não é a concessão."
    )


def origins_form_scope():
    scope = (
        "esqueleto de crédito no disco. "
        "Não concede licença."
    )
    named = origins_form_credit_scope()
    if named:
        scope += named
    return scope


def origins_form_path(reading):
    form = (reading or {}).get("form")
    if isinstance(form, dict):
        return form.get("path")
    return form


# O roteiro já recusa que o JSON sem
# os três campos declare. Sem isto o
# origins listava os nomes e calava
# a recusa. Recibo no disco não é
# a concessão.
ORIGIN_THREE = re.compile(r"JSON sem origem,\s+autor e licença não declara")


def guide_refuses_json_without_three_as_declaration(text):
    return bool(text and ORIGIN_THREE.search(text))


def origins_fields_three_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_json_without_three_as_declaration(text):
        return "references/gates.md"
    return None


def origins_fields_three_scope():
    if not origins_fields_three_source():
        return None
    return (
        " O disco recusa que o JSON sem os três campos declare "
        "(`três`). Recibo no disco não é a concessão."
    )


def origins_fields_scope():
    scope = (
        "os três nomes que o recibo exige. "
        "Não concede licença."
    )
    named = origins_fields_three_scope()
    if named:
        scope += named
    return scope


def origins_field_names(reading):
    fields = (reading or {}).get("fields")
    if isinstance(fields, dict):
        return list(fields.get("names") or [])
    return list(fields or [])


def origin_record_complete(record):
    # O JSON listava o arquivo e declarava. Sem origem o
    # harness fingia recibo. Os três campos são o que
    # `--declare` já exige. Nome no disco não é licença.
    if not isinstance(record, dict):
        return False
    return all(nonempty(sfx_catalog.receipt_field(record, field)) for field in ORIGIN_FIELDS)


# O esqueleto já pede o consumidor. Sem isto o
# origins lia os três rótulos e calava o sidecar.
# Consumidor no disco não é licença válida.
SIDECAR_CONSUMER = re.compile(r"Consumidor\s*:", re.IGNORECASE)


def sidecar_names_consumer(text):
    return bool(text and SIDECAR_CONSUMER.search(text))


# O roteiro já recusa que o sidecar sem rótulos declare. Sem
# isto o problema copiava o achado e calava a recusa.
# Recibo no disco não é licença.
ORIGIN_LABELS = re.compile(r"Sidecar sem\s+os três rótulos")


def gates_refuse_unlabeled_sidecar(text):
    return bool(text and ORIGIN_LABELS.search(text))


def origin_problem_label_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gates_refuse_unlabeled_sidecar(text):
        return "references/gates.md"
    return None


def origin_problem_scope():
    scope = (
        "Motivo e fonte do problema de forma. Não consulta titular "
        "e não concede licença."
    )
    if origin_problem_label_source():
        scope += (
            " O disco recusa que o sidecar sem rótulos declare (`rótulos`). "
            "Recibo no disco não é licença."
        )
    return scope


# O roteiro já recusa que o recibo
# presente seja licença válida. Sem
# isto o origins listava o recibo e
# calava a recusa. Arquivo no disco
# não é a concessão.
ORIGIN_VALID = re.compile(r"recibo presente não é licença válida")


def gates_refuse_present_receipt_as_valid_license(text):
    return bool(text and ORIGIN_VALID.search(text))


def origins_valid_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gates_refuse_present_receipt_as_valid_license(text):
        return "references/gates.md"
    return None


def origins_valid_scope():
    if not origins_valid_source():
        return None
    return (
        " O disco recusa que o recibo presente seja licença válida "
        "(`válida`). Arquivo no disco não é a concessão."
    )


def origins_receipts_scope():
    scope = (
        "recibo de origem no disco. "
        "Não concede licença."
    )
    named = origins_valid_scope()
    if named:
        scope += named
    return scope


# A guia já recusa que o embarcado
# sem recibo seja licença conhecida.
# Sem isto o origins listava o
# arquivo e calava a recusa. Arquivo
# no disco não é a concessão.
PREPRODUCTION_UNKNOWN = FRAMEWORK / "references/preproduction.md"
ORIGIN_UNKNOWN = re.compile(r"Licença desconhecida bloqueia a entrega")


def guide_refuses_undeclared_as_known_license(text):
    return bool(text and ORIGIN_UNKNOWN.search(text))


def origins_unknown_source():
    path = PREPRODUCTION_UNKNOWN
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_undeclared_as_known_license(text):
        return "references/preproduction.md"
    return None


def origins_unknown_scope():
    if not origins_unknown_source():
        return None
    return (
        " O disco recusa que o embarcado sem recibo seja licença conhecida "
        "(`desconhecida`). Arquivo no disco não é a concessão."
    )


def origins_undeclared_scope():
    scope = (
        "arquivo embarcado sem recibo. "
        "Não concede licença."
    )
    named = origins_unknown_scope()
    if named:
        scope += named
    return scope


def origin_undeclared_paths(origins):
    undeclared = (origins or {}).get("undeclared") or []
    if isinstance(undeclared, dict):
        return list(undeclared.get("paths") or [])
    return list(undeclared)


# O roteiro já recusa que nomear
# devolva o arquivo. Sem isto o
# origins listava o sumido e calava
# a recusa. Recibo no disco não é
# a concessão.
ORIGIN_RETURN = re.compile(r"Nomear não devolve o arquivo")


def guide_refuses_naming_as_file_return(text):
    return bool(text and ORIGIN_RETURN.search(text))


def origins_missing_return_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_naming_as_file_return(text):
        return "references/gates.md"
    return None


def origins_missing_return_scope():
    if not origins_missing_return_source():
        return None
    return (
        " O disco recusa que nomear devolva o arquivo "
        "(`devolve`). Recibo no disco não é a concessão."
    )


def origins_missing_scope():
    scope = (
        "mídia que o recibo lista e o disco perdeu. "
        "Não devolve o arquivo."
    )
    named = origins_missing_return_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que o
# conteúdo baixado receba uma
# licença nova pelo simples
# reuso. Sem isto o origins
# listava o embarcado e calava
# a recusa. Arquivo no disco
# não é a concessão.
CONTENT_REUSE = re.compile(r"licença nova pelo simples reuso")


def recipe_refuses_reuse_as_new_license(text):
    return bool(text and CONTENT_REUSE.search(text))


def origins_embedded_reuse_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_reuse_as_new_license(text):
        return "recipes/content.md"
    return None


def origins_embedded_reuse_scope():
    if not origins_embedded_reuse_source():
        return None
    return (
        " O disco recusa que o conteúdo baixado receba uma licença nova "
        "pelo simples reuso (`nova`). Arquivo no disco não é a concessão."
    )


def origins_embedded_scope():
    scope = (
        "arquivo de mídia embarcado no disco. "
        "Não concede licença."
    )
    named = origins_embedded_reuse_scope()
    if named:
        scope += named
    return scope


def origin_embedded_paths(origins):
    embedded = (origins or {}).get("embedded") or []
    if isinstance(embedded, dict):
        return list(embedded.get("paths") or [])
    return list(embedded)


def origins_missing_paths(reading):
    missing = (reading or {}).get("missing") or []
    if isinstance(missing, dict):
        return list(missing.get("paths") or [])
    return list(missing)


def origins_receipt_files(project, max_entries=2000):
    project = Path(project).resolve()
    found = []
    pending = [(project, 0)] if project.is_dir() else []
    seen = 0
    while pending:
        directory, depth = pending.pop(0)
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name.casefold())
        except OSError:
            continue
        for path in entries:
            if seen >= max_entries:
                pending.clear()
                break
            seen += 1
            if path.name.startswith("."):
                continue
            if path.is_symlink():
                continue
            if path.is_dir():
                if path.name.casefold() in ORIGIN_SKIP:
                    continue
                if depth < 6:
                    pending.append((path, depth + 1))
                continue
            if not path.is_file():
                continue
            stem = path.name.casefold()
            if stem in ORIGIN_RECEIPTS or stem.endswith(".credits.txt"):
                found.append(path.relative_to(project).as_posix())
    return found


def sidecar_consumer_source(project):
    project = Path(project)
    for relative, text in walk_project_files(project, {".txt"}):
        if "tests" in Path(relative).parts:
            continue
        if sidecar_names_consumer(text):
            return relative
    return None


def sidecar_declares(text):
    # O JSON já exigia os três campos. O sidecar ao lado
    # declarava só por existir — inclusive vazio. Nome no
    # disco não é licença.
    if not isinstance(text, str) or not text.strip():
        return False
    folded = text.casefold()
    return bool(
        re.search(r"\b(?:origem|origin)\s*:", folded)
        and re.search(r"\b(?:autor|author)\s*:", folded)
        and re.search(r"\b(?:licen[cç]a|license)\s*:", folded)
    )


def sidecar_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def origin_ref(name):
    return str(name).replace("\\", "/").strip().lstrip("./")


def local_media_ref(name):
    # O JSON listava o arquivo e o scan só via o que
    # ainda estava no disco. URL e id sem sufixo não
    # são mídia embarcada. Nomear não devolve o arquivo.
    text = origin_ref(name)
    if not text or "://" in text:
        return None
    parts = Path(text).parts
    if not parts or ".." in parts:
        return None
    if Path(text).suffix.casefold() not in EMBEDDED_SUFFIXES:
        return None
    return text


# O roteiro já recusa que a
# varredura incompleta seja a
# concessão. Sem isto o origins
# relatava o truncated e calava
# a recusa. Recorte no disco
# não é a concessão.
GATES_TRUNCATED_GRANT = re.compile(r"Varredura incompleta não é a concessão")


def guide_refuses_incomplete_scan_as_grant(text):
    return bool(text and GATES_TRUNCATED_GRANT.search(text))


def origins_truncated_scan_source():
    path = GATES_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_incomplete_scan_as_grant(text):
        return "references/gates.md"
    return None


def origins_truncated_scan_scope():
    if not origins_truncated_scan_source():
        return None
    return (
        " O disco recusa que a varredura incompleta seja a concessão "
        "(`varredura`). Recorte no disco não é a concessão."
    )


def origins_truncated_scope():
    scope = (
        "varredura parou no limite de entradas. "
        "Não concede a licença."
    )
    named = origins_truncated_scan_scope()
    if named:
        scope += named
    return scope


def origins_truncated_flag(reading):
    truncated = (reading or {}).get("truncated") if isinstance(reading, dict) else reading
    if isinstance(truncated, dict):
        return bool(truncated.get("truncated"))
    return bool(truncated)


def origins_truncated_reading(truncated):
    if not truncated:
        return False
    return {
        "truncated": True,
        "scope": origins_truncated_scope(),
    }


def origins_reading(project, max_entries=2000):
    project = Path(project).resolve()
    embedded, receipts, problems = [], [], []
    mentioned = set()
    listed = []
    pending = [(project, 0)] if project.is_dir() else []
    seen = 0
    stopped = False

    def remember(name, receipt=None):
        text = origin_ref(name)
        if not text:
            return
        mentioned.add(text)
        mentioned.add(Path(text).name)
        if receipt is None:
            return
        ref = local_media_ref(text)
        if ref is None or any(item["path"] == ref for item in listed):
            return
        listed.append({"source": receipt, "path": ref})

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
            if not origin_record_complete(record):
                continue
            for key in ("src", "path", "file", "id", "key"):
                if isinstance(record.get(key), str):
                    remember(record[key], receipt=relative)

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
                for candidate in (sidecar, alt, near):
                    if not candidate.is_file() or candidate.is_symlink():
                        continue
                    text = sidecar_text(candidate)
                    if text is None or not sidecar_declares(text):
                        continue
                    remember(relative)
                    remember(path.name)
                    break
            if stem in ORIGIN_RECEIPTS or stem.endswith(".credits.txt"):
                receipts.append(relative)
                if suffix == ".json":
                    ingest_json(path, relative)
                elif stem.endswith(".credits.txt") and stem not in ORIGIN_RECEIPTS:
                    text = sidecar_text(path)
                    if text is None:
                        problems.append({"source": relative, "reason": "unreadable_receipt"})
                    elif not sidecar_declares(text):
                        problems.append({"source": relative, "reason": "incomplete_sidecar"})
                    else:
                        ingest_text(path, relative)
                else:
                    ingest_text(path, relative)

    declared, undeclared = [], []
    for relative in embedded:
        name = Path(relative).name
        if relative in mentioned or name in mentioned:
            declared.append(relative)
        else:
            undeclared.append(relative)

    embedded_names = {Path(item).name for item in embedded}
    missing = []
    for item in listed:
        ref = item["path"]
        if Path(ref).name in embedded_names:
            continue
        candidate = project / ref
        try:
            present = candidate.is_file() and not candidate.is_symlink()
        except OSError:
            present = False
        if present:
            continue
        missing.append(ref)
        problems.append({
            "source": item["source"],
            "reason": "missing_media",
            "path": ref,
        })

    licensing = gate_declaration(project)["declared"].get("deliver", {}).get("licensing")
    contradicts = bool(
        licensing and licensing["state"] == "met" and undeclared
    )
    scope = (
        "Percorre o projeto, lista arquivos de mídia embarcados e cruza com recibos "
        "(sources.json, licenses.json, CREDITS, sidecar `.credits.txt`). Relata ausência "
        "de recibo, recibo ilegível e declaração `deliver.licensing` = `met` que o disco "
        "contradiz. Nomeia a mídia que o recibo lista e o disco perdeu. "
        "Nomear não devolve o arquivo. JSON sem origem, autor e licença — no topo ou "
        "em `sources[0]` — não cobre o arquivo. Sidecar sem os três rótulos também não. "
        "`form` aponta o esqueleto; `fields` lista origem, autor e licença. "
        "`--declare` escreve o sidecar. Sem `then`. Recibo no disco não é licença "
        "válida. Não consulta titular, não interpreta texto de licença, não distingue "
        "licença válida de inválida e **não concede passagem**."
    )
    if sidecar_consumer_source(project):
        scope += (
            " O disco nomeia o consumidor (`Consumidor`). "
            "Consumidor no disco não é licença válida."
        )
    problems = [dict(item) for item in problems]
    problem_scope = origin_problem_scope()
    for item in problems:
        item["scope"] = problem_scope
    if receipts:
        receipts = {
            "paths": receipts,
            "scope": origins_receipts_scope(),
        }
    if undeclared:
        undeclared = {
            "paths": undeclared,
            "scope": origins_undeclared_scope(),
        }
    if missing:
        missing = {
            "paths": missing,
            "scope": origins_missing_scope(),
        }
    if embedded:
        embedded = {
            "paths": embedded,
            "scope": origins_embedded_scope(),
        }
    return {
        "schema_version": 1,
        "project": str(project),
        "exists": project.is_dir(),
        "embedded": embedded,
        "declared": declared,
        "undeclared": undeclared,
        "missing": missing,
        "receipts": receipts,
        "problems": problems,
        "contradicts_licensing": contradicts,
        "truncated": origins_truncated_reading(stopped),
        "granted": False,
        "validated": False,
        "form": {
            "path": str(ORIGIN_FORM),
            "scope": origins_form_scope(),
        },
        "fields": {
            "names": list(ORIGIN_FIELDS),
            "scope": origins_fields_scope(),
        },
        "guide": str(FRAMEWORK / "references/gates.md"),
        "rule": (
            "Arquivo embarcado sem recibo de origem conta como licença desconhecida. "
            "O recibo declara origem, autor e condição de uso; não prova que a condição vale. "
            "JSON sem os três campos não declara. "
            "Sidecar sem origem, autor e licença também não. "
            "Mídia que o recibo lista e o disco perdeu não some."
        ),
        "scope": scope,
    }


# A receita já recusa que o recibo comprove a consistência do gerador.
# Sem isto o declare copiava origem e licença e calava a recusa.
# Recibo no disco não é o asset.
CONTENT_CONSISTENCY = re.compile(r"não comprova consistência")


def recipe_refuses_receipt_as_generator_consistency(text):
    return bool(text and CONTENT_CONSISTENCY.search(text))


def origins_declare_consistency_source():
    path = CONTENT_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_receipt_as_generator_consistency(text):
        return "recipes/content.md"
    return None


def origins_declare_fields_scope():
    if not origins_declare_consistency_source():
        return None
    return (
        "O disco recusa que o recibo comprove a consistência do gerador "
        "(`consistência`). Recibo no disco não é o asset."
    )


def origins_declare(project, relative, origin, author, license_name):
    # O `next` pedia `origins` de novo. Relê não declara. Este caminho
    # escreve o sidecar; não valida titular nem texto jurídico.
    project = Path(project)
    if not project.is_dir() or project.is_symlink():
        raise ValueError("projeto ausente")
    if not all(nonempty(value) for value in (relative, origin, author, license_name)):
        raise ValueError("declare exige arquivo, origem, autor e licença")
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("arquivo precisa ser relativo ao projeto")
    path = (project / rel).resolve()
    try:
        path.relative_to(project.resolve())
    except ValueError as error:
        raise ValueError("arquivo precisa ficar dentro do projeto") from error
    if path.is_symlink() or not path.is_file():
        raise ValueError("arquivo embarcado inexistente")
    if path.suffix.casefold() not in EMBEDDED_SUFFIXES:
        raise ValueError("arquivo não é mídia embarcada")
    posix = path.relative_to(project.resolve()).as_posix()
    reading = origins_reading(project)
    if posix not in origin_undeclared_paths(reading):
        raise ValueError("arquivo já tem recibo ou não está sem origem")
    sidecar = path.with_name(path.name + ".credits.txt")
    if sidecar.exists() or sidecar.is_symlink():
        if sidecar.is_symlink() or not sidecar.is_file():
            raise ValueError("sidecar já existe")
        existing = sidecar_text(sidecar)
        if existing is not None and sidecar_declares(existing):
            raise ValueError("sidecar já existe")
    sidecar.write_text(
        f"{path.name} — origem: {origin.strip()}.\n"
        f"Autor: {author.strip()}. Licença: {license_name.strip()}.\n",
        encoding="utf-8",
    )
    after = origins_reading(project)
    fields = {
        "origin": origin.strip(),
        "author": author.strip(),
        "license": license_name.strip(),
    }
    named = origins_declare_fields_scope()
    if named:
        fields = dict(fields, scope=named)
    return {
        "schema_version": 1,
        "command": "origins",
        "project": str(project),
        "declared": posix,
        "sidecar": sidecar.relative_to(project.resolve()).as_posix(),
        "fields": fields,
        "undeclared": after["undeclared"],
        "granted": False,
        "validated": False,
        "scope": (
            "Escreveu o sidecar ao lado do arquivo. Recibo no disco não é "
            "licença válida. `granted` e `validated` continuam falsos."
        ),
    }


def _bar_scope(project):
    scope = (
        "Lê a declaração do próprio projeto e confere só a forma dela, relatando em `problems`: dimensão "
        "fora das dez, degrau fora dos cinco e alvo que não é o degrau imediatamente seguinte. Não observa "
        "o jogo, não mede nada e não corrige a declaração — uma tabela bem formada e otimista sai daqui "
        "intacta, porque o degrau é afirmação de quem escreveu. `perceived_tier` só aparece quando as dez "
        "dimensões têm linha, porque dimensão não declarada não é dimensão alta."
    )
    if bar_floor_source(project):
        scope += (
            " O disco declara o mínimo (`mínimo`). "
            "Degrau no disco não é acabamento observado."
        )
    named = bar_score_scope()
    if named:
        scope += named
    return scope


# O mapa já recusa que o checklist
# seja um score. Sem isto o bar lia
# a declaração e calava a recusa.
# Mapa no disco não é acabamento.
SOURCES_SCORE = re.compile(r"não é um\s+score")


def map_refuses_checklist_as_score(text):
    return bool(text and SOURCES_SCORE.search(text))


def bar_score_source():
    path = FRAMEWORK / "references/sources.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if map_refuses_checklist_as_score(text):
        return "references/sources.md"
    return None


def bar_score_scope():
    if not bar_score_source():
        return None
    return (
        " O disco recusa que o checklist seja um score "
        "(`score`). Mapa no disco não é acabamento."
    )


# A barra já recusa que dimensão não
# declarada seja dimensão alta. Sem
# isto o bar listava a chave e calava
# a recusa. Linha no disco não é
# acabamento.
BAR_HIGH = re.compile(r"dimensão não declarada não é dimensão\s+alta")


def bar_refuses_undeclared_as_high_dimension(text):
    return bool(text and BAR_HIGH.search(text))


def bar_high_source():
    path = FRAMEWORK / "references/production-bar.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_undeclared_as_high_dimension(text):
        return "references/production-bar.md"
    return None


def bar_high_scope():
    if not bar_high_source():
        return None
    return (
        " O disco recusa que dimensão não declarada seja dimensão alta "
        "(`alta`). Linha no disco não é acabamento."
    )


def bar_undeclared_scope():
    scope = (
        "dimensão sem linha na barra. "
        "Não observa o degrau."
    )
    named = bar_high_scope()
    if named:
        scope += named
    return scope


def bar_undeclared_keys(bar):
    undeclared = (bar or {}).get("undeclared") or []
    if isinstance(undeclared, dict):
        return list(undeclared.get("keys") or [])
    return list(undeclared)


# A barra já recusa que a declaração
# seja um selo. Sem isto o bar
# listava o fonte e calava a recusa.
# Linha no disco não é acabamento.
BAR_SEAL = re.compile(r"Não é um selo")


def bar_refuses_declaration_as_seal(text):
    return bool(text and BAR_SEAL.search(text))


def bar_seal_source():
    path = FRAMEWORK / "references/production-bar.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_declaration_as_seal(text):
        return "references/production-bar.md"
    return None


def bar_seal_scope():
    if not bar_seal_source():
        return None
    return (
        " O disco recusa que a declaração seja um selo "
        "(`selo`). Linha no disco não é acabamento."
    )


def bar_sources_scope():
    scope = (
        "documento onde a barra pode viver. "
        "Não observa o degrau."
    )
    named = bar_seal_scope()
    if named:
        scope += named
    return scope


def bar_source_files(project):
    return list(bar_declaration(project)["sources"])


def bar_source_paths(bar):
    sources = (bar or {}).get("sources") or []
    if isinstance(sources, dict):
        return list(sources.get("paths") or [])
    return list(sources)


# A barra já recusa que a tabela
# otimista seja observação. Sem isto
# o bar listava o piso e calava a
# recusa. Linha no disco não é
# acabamento.
BAR_OPTIMIST = re.compile(r"otimista sai de lá\s+intacta")


def bar_refuses_optimistic_table_as_observation(text):
    return bool(text and BAR_OPTIMIST.search(text))


def bar_optimist_source():
    path = FRAMEWORK / "references/production-bar.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_optimistic_table_as_observation(text):
        return "references/production-bar.md"
    return None


def bar_optimist_scope():
    if not bar_optimist_source():
        return None
    return (
        " O disco recusa que a tabela otimista seja observação "
        "(`otimista`). Linha no disco não é acabamento."
    )


def bar_floor_scope():
    scope = (
        "dimensão no piso declarado. "
        "Não observa o degrau."
    )
    named = bar_optimist_scope()
    if named:
        scope += named
    return scope


def bar_at_floor_keys(bar):
    at_floor = (bar or {}).get("at_floor") or []
    if isinstance(at_floor, dict):
        return list(at_floor.get("keys") or [])
    return list(at_floor)


# A barra já recusa que o piso seja
# uma nota. Sem isto o bar relatava
# o mínimo e calava a recusa. Linha
# no disco não é acabamento.
BAR_NOTE = re.compile(r"Não é uma nota")


def bar_refuses_floor_as_note(text):
    return bool(text and BAR_NOTE.search(text))


def bar_floor_note_source():
    path = FRAMEWORK / "references/production-bar.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_floor_as_note(text):
        return "references/production-bar.md"
    return None


def bar_floor_note_scope():
    if not bar_floor_note_source():
        return None
    return (
        " O disco recusa que o piso seja uma nota "
        "(`nota`). Linha no disco não é acabamento."
    )


def bar_declared_floor_scope():
    scope = (
        "mínimo entre as dimensões declaradas. "
        "Não observa o acabamento."
    )
    named = bar_floor_note_scope()
    if named:
        scope += named
    return scope


def bar_floor_tier(reading):
    floor = (reading or {}).get("floor")
    if isinstance(floor, dict):
        return floor.get("tier")
    return floor


def bar_reading(project):
    declaration = bar_declaration(project)
    declared = declaration["declared"]
    problems = [dict(item) for item in declaration["problems"]]
    problem_scope = bar_problem_scope()
    for item in problems:
        item["scope"] = problem_scope
    conflicts = [dict(item) for item in declaration["conflicts"]]
    conflict_scope = bar_conflict_scope()
    for item in conflicts:
        item["scope"] = conflict_scope
    undeclared = declaration["undeclared"]
    if undeclared:
        undeclared = {
            "keys": undeclared,
            "scope": bar_undeclared_scope(),
        }
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
                "scope": bar_item_scope(),
            }
            for key in BAR_DIMENSIONS
        ],
        "floor": (
            {
                "tier": declaration["floor"],
                "scope": bar_declared_floor_scope(),
            }
            if declaration["floor"] is not None
            else None
        ),
        "at_floor": (
            {
                "keys": declaration["at_floor"],
                "scope": bar_floor_scope(),
            }
            if declaration["at_floor"] else []
        ),
        "undeclared": undeclared,
        "conflicts": conflicts,
        "problems": problems,
        "perceived_tier": declaration["perceived_tier"],
        "rule": "O degrau percebido de um jogo é o mínimo entre suas dimensões, não a média.",
        "guide": str(FRAMEWORK / "references/production-bar.md"),
        "sources": (
            {
                "paths": declaration["sources"],
                "scope": bar_sources_scope(),
            }
            if declaration["sources"] else []
        ),
        "assessed": False,
        "scope": _bar_scope(project),
    }


# A barra já recusa que duas linhas se resolvam por precedência.
# Sem isto o conflito copiava as fontes e calava a recusa.
# Linha no disco não é acabamento.
BAR_PRECEDENCE = re.compile(
    r"Duas linhas discordantes sobre a mesma dimensão não se resolvem por\s+precedência"
)


def bar_refuses_precedence(text):
    return bool(text and BAR_PRECEDENCE.search(text))


def bar_conflict_precedence_source():
    path = FRAMEWORK / "references/production-bar.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_precedence(text):
        return "references/production-bar.md"
    return None


def bar_conflict_scope():
    scope = (
        "Duas declarações da mesma dimensão. "
        "Não observa e não resolve a discordância."
    )
    if bar_conflict_precedence_source():
        scope += (
            " O disco recusa que duas linhas discordantes se resolvam por precedência (`precedência`). "
            "Linha no disco não é acabamento."
        )
    return scope


# A barra já recusa que o degrau seja prazo. Sem isto o
# item listava o degrau e calava a recusa.
# Linha no disco não é calendário.
BAR_DEADLINE = re.compile(r"Degraus não são prazos")


def bar_refuses_deadline(text):
    return bool(text and BAR_DEADLINE.search(text))


def bar_item_deadline_source():
    path = FRAMEWORK / "references/production-bar.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_deadline(text):
        return "references/production-bar.md"
    return None


def bar_item_scope():
    scope = (
        "Degrau da dimensão segundo a declaração do projeto. "
        "Não observa e não atribui calendário."
    )
    if bar_item_deadline_source():
        scope += (
            " O disco recusa que o degrau seja prazo (`prazos`). "
            "Linha no disco não é calendário."
        )
    return scope


# A barra já recusa que o nome seja uma das dez. Sem isto o
# problema copiava o achado e calava a recusa.
# Linha no disco não é acabamento.
BAR_TEN = re.compile(r"não é uma das dez")


def bar_refuses_unknown_dimension(text):
    return bool(text and BAR_TEN.search(text))


def bar_problem_dimension_source():
    path = FRAMEWORK / "references/production-bar.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_unknown_dimension(text):
        return "references/production-bar.md"
    return None


def bar_problem_scope():
    scope = (
        "Motivo e fonte do problema de forma. Não observa e não "
        "corrige a declaração."
    )
    if bar_problem_dimension_source():
        scope += (
            " O disco recusa que o nome seja uma das dez (`dimensão`). "
            "Linha no disco não é acabamento."
        )
    return scope


# A barra já recusa promover o degrau. Sem isto o
# context apontava a guia e calava a recusa.
# Guia no disco não é acabamento.
BAR_GUIDE = FRAMEWORK / "references/production-bar.md"
BAR_PROMOTE = re.compile(r"Nenhum comando promove um jogo a um degrau")


def bar_guide_refuses_promote(text):
    return bool(text and BAR_PROMOTE.search(text))


def production_bar_promote_source():
    path = BAR_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_guide_refuses_promote(text):
        return "references/production-bar.md"
    return None


def production_bar_scope():
    scope = (
        "Seleção das dimensões pertinentes ao foco e à etapa, mais o degrau que o próprio projeto declara "
        "nos documentos listados em `declaration.sources`. O harness lê a declaração e confere só a forma "
        "dela: não atribui degrau, não mede acabamento e não aprova entrega. Declarar um degrau exige "
        "observação com condição, evidência e autor — a tabela é a afirmação, não a prova."
    )
    if production_bar_promote_source():
        scope += (
            " O disco recusa promover o degrau (`promove`). "
            "Guia no disco não é acabamento."
        )
    named = production_bar_team_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que AAA seja
# orçamento ou tamanho de equipe.
# Sem isto o production_bar apontava
# as dimensões e calava a recusa.
# Receita no disco não é acabamento.
PRODUCTION_TEAM = re.compile(r"não é orçamento nem tamanho de equipe")


def recipe_refuses_aaa_as_team_budget(text):
    return bool(text and PRODUCTION_TEAM.search(text))


def production_bar_team_source():
    path = FRAMEWORK / "recipes/production.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_aaa_as_team_budget(text):
        return "recipes/production.md"
    return None


def production_bar_team_scope():
    if not production_bar_team_source():
        return None
    return (
        " O disco recusa que AAA seja orçamento ou tamanho de equipe "
        "(`equipe`). Receita no disco não é acabamento."
    )


# A barra já recusa que o degrau sem condição
# seja observação. Sem isto o item copiava o
# degrau e calava a recusa. Linha no disco
# não é acabamento.
BAR_OPINION = re.compile(r"Degrau sem condição é opinião")


def bar_refuses_tier_without_condition(text):
    return bool(text and BAR_OPINION.search(text))


def production_bar_dimension_opinion_source():
    path = BAR_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_tier_without_condition(text):
        return "references/production-bar.md"
    return None


def production_bar_dimension_scope(key=None):
    parts = []
    if production_bar_dimension_opinion_source():
        parts.append(
            "O disco recusa que o degrau sem condição seja observação "
            "(`opinião`). Linha no disco não é acabamento."
        )
    if key == "pacing":
        named = production_bar_interest_scope()
        if named:
            parts.append(named.lstrip())
    return " ".join(parts) or None


# O onboard já recusa que tempo
# de sessão seja interesse. Sem
# isto o item pacing copiava o
# degrau e calava a recusa.
# Relógio no disco não é o
# interesse.
ONBOARD_INTEREST = re.compile(r"Tempo de sessão não é interesse")


def onboard_refuses_session_time_as_interest(text):
    return bool(text and ONBOARD_INTEREST.search(text))


def production_bar_interest_source():
    path = FRAMEWORK / "commands/onboard.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if onboard_refuses_session_time_as_interest(text):
        return "commands/onboard.md"
    return None


def production_bar_interest_scope():
    if not production_bar_interest_source():
        return None
    return (
        " O disco recusa que tempo de sessão seja interesse "
        "(`interesse`). Relógio no disco não é o interesse."
    )


def production_bar(focus, stage=None, project=None):
    dimensions = FOCUS_DIMENSIONS.get(focus, ())
    declaration = bar_declaration(project) if project is not None else None
    items = []
    for key in dimensions:
        item = {
            "key": key,
            "label": BAR_DIMENSIONS[key],
            "declared": (declaration["declared"].get(key) if declaration else None),
        }
        named = production_bar_dimension_scope(key)
        if named:
            item["scope"] = named
        items.append(item)
    return {
        "tiers": list(BAR_TIERS),
        "tier_target": STAGE_TIERS.get(stage),
        "dimensions": items,
        "rule": "O degrau percebido de um jogo é o mínimo entre suas dimensões, não a média.",
        "guide": str(FRAMEWORK / "references/production-bar.md"),
        "declaration": declaration,
        "observed": None,
        "assessed": False,
        "scope": production_bar_scope(),
    }


# A receita já recusa que o nome seja API. Sem isto a
# menção apontava o arquivo e calava a recusa.
# Vocabulário no disco não é runtime.
LIFECYCLE_API = re.compile(r"não uma API\s+implementada")


def lifecycle_refuses_api(text):
    return bool(text and LIFECYCLE_API.search(text))


def capability_api_source():
    path = FRAMEWORK / "recipes/lifecycle.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if lifecycle_refuses_api(text):
        return "recipes/lifecycle.md"
    return None


def capability_mention_scope():
    scope = (
        "Menção em arquivo local de inspeção; não executado, não comprovado."
    )
    if capability_api_source():
        scope += (
            " O disco recusa que o nome seja API (`api`). "
            "Vocabulário no disco não é runtime."
        )
    tracking = capability_tracking_scope()
    if tracking:
        scope += tracking
    return scope


# O roteiro já recusa que menções
# locais sejam rastreamento de
# comportamento. Sem isto a menção
# apontava o arquivo e calava a
# recusa. Menção no disco não é
# o gesto.
AUDIT_TRACKING = re.compile(r"não é rastreamento de comportamento")


def audit_refuses_mentions_as_tracking(text):
    return bool(text and AUDIT_TRACKING.search(text))


def capability_tracking_source():
    path = FRAMEWORK / "references/project-audit.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_refuses_mentions_as_tracking(text):
        return "references/project-audit.md"
    return None


def capability_tracking_scope():
    if not capability_tracking_source():
        return None
    return (
        " O disco recusa que menções locais sejam rastreamento de comportamento "
        "(`rastreamento`). Menção no disco não é o gesto."
    )


# A barra já recusa que o determinismo seja capacidade.
# Sem isto o item desconhecido copiava o estado e calava a recusa.
# Lista no disco não é ciclo demonstrado.
BAR_DETERMINISM = re.compile(r"Determinismo não é uma capacidade")


def bar_refuses_determinism_capability(text):
    return bool(text and BAR_DETERMINISM.search(text))


def capability_unknown_determinism_source():
    path = FRAMEWORK / "references/production-bar.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if bar_refuses_determinism_capability(text):
        return "references/production-bar.md"
    return None


def capability_unknown_scope():
    scope = (
        "Capacidade ainda não mencionada neste recorte. Não executa "
        "e não anexa determinismo."
    )
    if capability_unknown_determinism_source():
        scope += (
            " O disco recusa que o determinismo seja capacidade (`determinismo`). "
            "Lista no disco não é ciclo demonstrado."
        )
    return scope


def mention_capabilities(project):
    found = {name: {"status": "unknown", "scope": capability_unknown_scope()} for name in CAPABILITIES}
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
                    "scope": capability_mention_scope(),
                }
    return found


def playable_unplayed(project, areas):
    # O mesmo atalho do `next`. Jogo que já abre e ainda
    # não tem recibo não pede auditoria de rascunho.
    # Lacuna no disco não some — só deixa de mandar
    # preencher template antes do serve.
    try:
        scripts, manager = project_commands(project)
    except (OSError, ValueError, RecursionError):
        scripts, manager = {}, None
    play = play_command(project, scripts, manager)
    missing = [key for key, area in areas.items() if area["status"] == "not_located"]
    return fresh_starter_cycle(project, missing, play) and not observation_receipts(project)


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
    deferred, non_current, continuity_sources, genre_mentions, scale_mentions = [], [], [], [], []
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
                scale = SCALE_FIELD.match(line)
                if scale and status in {"candidate", "draft"} and len(scale_mentions) < 5:
                    scale_mentions.append({"path": relative, "line": number, "value": scale.group(1)})
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
    waiting = playable_unplayed(project, areas) if project.is_dir() else False
    require_audit = needs_documentation and not waiting
    notice = None
    if needs_documentation:
        missing = "; ".join(areas[key]["label"] for key in gaps)
        findings = f"Não localizei documentação confirmável para: {missing}." if gaps else "A checagem documental teve cobertura incompleta."
        if gaps and issues:
            findings += " A cobertura da checagem também foi limitada."
        if waiting:
            work = "O destino já abre. Jogue primeiro; rascunhos de template antes da primeira partida são o atrito. O harness não executa o jogo"
        elif project.is_dir():
            work = "Vou levantar o código e os registros e organizar a documentação mínima"
        else:
            work = "Vou documentar a base disponível e a proposta, distinguindo o que ainda não foi implementado"
        notice = f"{project.name}: {findings} {work}, preservando os documentos canônicos e registrando as lacunas."
    areas["art_direction"]["scope"] = art_direction_scope()
    areas["architecture"]["scope"] = architecture_area_scope()
    areas["provenance"]["scope"] = provenance_area_scope()
    areas["qa"]["scope"] = qa_area_scope()
    areas["runbook"]["scope"] = runbook_area_scope()
    areas["decisions"]["scope"] = decisions_area_scope()
    areas["gdd"]["scope"] = gdd_area_scope()
    areas["mda"]["scope"] = mda_area_scope()
    areas["vision"]["scope"] = vision_area_scope()
    candidate_scope = scan_candidate_scope()
    understood = architecture_candidate_understood_scope()
    for key, area in areas.items():
        for item in area["candidates"]:
            item["scope"] = candidate_scope
            if key == "architecture" and understood:
                item["scope"] += understood
    mention_scope = genre_mention_scope()
    scale_scope = scale_mention_scope()
    issue_scope = coverage_issue_scope()
    draft_scope = coverage_draft_scope()
    return {
        "schema_version": 3, "project": str(project), "exists": project.is_dir(),
        "minimum_status": "needs_review" if needs_documentation else "candidates_found",
        "areas": areas, "gaps": gaps, "read_first": read_first,
        "continuity_sources": continuity_sources, "continuity_source_count": continuity_source_count,
        "genre_mentions": [dict(item, scope=mention_scope) for item in genre_mentions],
        "scale_mentions": [dict(item, scope=scale_scope) for item in scale_mentions],
        "agent_context": {
            "status": "found" if local_instructions else "not_located",
            "files": local_instructions,
            "scope": agent_context_scope(project),
        },
        "coverage": {
            "documents_inspected": inspected, "documents_located": len(documents), "entries_seen": entries_seen,
            "documents_deferred": deferred[:20], "documents_deferred_count": len(deferred),
            "non_current_documents": [dict(item, scope=draft_scope) for item in non_current[:20]], "non_current_document_count": len(non_current),
            "issues": [dict(item, scope=issue_scope) for item in issues[:20]],
            "issue_count": len(issues),
            "issues_truncated": coverage_issues_truncated_reading(len(issues) > 20),
            "excluded_directory_names": sorted(excluded_dirs),
            "limits": {"entries": max_entries, "documents": max_documents, "bytes_per_document": max_bytes, "depth": 4, "index_links": max_links, "candidates_per_area": 3, "continuity_sources": 5, "scope": coverage_limits_scope()},
            "scope": coverage_scope(),
        },
        "next_action": (
            "defer_until_playable_cycle" if waiting
            else "notify_and_document" if needs_documentation
            else "continue_requested_task"
        ),
        "audit": {
            "policy": "notify_and_proceed", "executed": False,
            "required": audit_required_reading(require_audit),
            "deferred": audit_deferred_reading(waiting),
            "notice": notice,
            "reason": (
                "O next já pede jogar primeiro. Lacuna de rascunho depois do start não é auditoria neste turno. --event direction-approved e --stage audit continuam pedindo a base."
                if waiting else
                "Direção do usuário: avisar e iniciar o levantamento/documentação automaticamente; respeitar restrição explícita na conversa atual."
            ),
            "guide": str(FRAMEWORK / "references/project-audit.md"),
            "scope": audit_scope(),
        },
        "scope": _scan_scope(project),
    }


# O README já aponta o serve. Sem isto o
# scan lia as áreas e calava o ciclo.
# Página no disco não é partida jogada.
SCAN_CYCLE_FILES = ("README.md",)
SCAN_CYCLE_MARK = re.compile(r"npm run serve")


def readme_points_serve(text):
    return bool(text and SCAN_CYCLE_MARK.search(text))


def scan_serve_source(project):
    project = Path(project)
    for name in SCAN_CYCLE_FILES:
        path = project / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 400_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if readme_points_serve(text):
            return name
    return None


def _scan_scope(project):
    scope = (
        "Localização lexical limitada, priorizada por índices e nomes; links de navegação não são conteúdo. "
        "Marcadores de histórico/referência/rascunho são indícios, não certificação de atualidade. "
        "Não rastreia comportamento, executa código, escreve arquivos ou comprova suficiência e qualidade. "
        "Ausência significa não localizado neste recorte."
    )
    if scan_serve_source(project):
        scope += (
            " O disco aponta o serve (`serve`). "
            "Página no disco não é partida jogada."
        )
    named = scan_discarded_scope()
    if named:
        scope += named
    return scope


# O roteiro já recusa que a pasta
# references seja descartada. Sem isto
# o scan lia as áreas e calava a recusa.
# Roteiro no disco não é inventário.
AUDIT_DISCARDED = re.compile(r"não é descartada")


def project_audit_refuses_references_as_discarded(text):
    return bool(text and AUDIT_DISCARDED.search(text))


def scan_discarded_source():
    path = FRAMEWORK / "references/project-audit.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if project_audit_refuses_references_as_discarded(text):
        return "references/project-audit.md"
    return None


def scan_discarded_scope():
    if not scan_discarded_source():
        return None
    return (
        " O disco recusa que a pasta references seja descartada "
        "(`descartada`). Roteiro no disco não é inventário."
    )


# A memória já recusa o adjetivo. Sem isto o scan
# listava AGENTS.md e calava a recusa.
# Memória no disco não é acabamento.
AGENT_MEMORY = "AGENTS.md"
AGENT_AAA = re.compile(r"Não chame o recorte de AAA")


def agents_memory_refuses_aaa(text):
    return bool(text and AGENT_AAA.search(text))


def agent_aaa_source(project):
    path = Path(project) / AGENT_MEMORY
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if agents_memory_refuses_aaa(text):
        return AGENT_MEMORY
    return None


def agent_context_scope(project):
    scope = (
        "Instruções persistentes para o agente na raiz do projeto. "
        "Não é uma das nove áreas; sem elas, cada sessão reaprende convenções. "
        "`template agents` gera a memória a partir do disco — o comando que abre e o que não foi plantado."
    )
    if agent_aaa_source(project):
        scope += (
            " O disco recusa chamar o recorte de AAA (`agents`). "
            "Memória no disco não é acabamento."
        )
    return scope


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


# O pacote já recusa que teste unitário prove o navegador. Sem isto o
# context apontava o arquivo e calava a recusa.
# Pacote no disco não é comportamento no aparelho.
PACK_BROWSER = re.compile(
    r"teste unitário não prova\s+comportamento no navegador",
    re.IGNORECASE,
)


def pack_refuses_unit_as_browser(text):
    return bool(text and PACK_BROWSER.search(text))


def packs_browser_source(kind):
    pack_name = PLATFORM_PACKS.get(kind)
    if not pack_name:
        return None
    path = FRAMEWORK / f"packs/platforms/{pack_name}.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if pack_refuses_unit_as_browser(text):
        return f"packs/platforms/{pack_name}.md"
    return None


def packs_scope(kind):
    scope = (
        "Pacotes são convenções de plataforma/gênero para orientar leitura e verificação. "
        "Não substituem AGENTS, a documentação oficial nem o que o projeto realmente faz; "
        "confirme cada convenção no código."
    )
    if packs_browser_source(kind):
        scope += (
            " O disco recusa que teste unitário prove o navegador (`navegador`). "
            "Pacote no disco não é comportamento no aparelho."
        )
    return scope


def read_scale(mentions, declared=None):
    """Escala de ambição: declarada na conversa vence; senão, o campo `Escala:` de um documento sugere.

    A palavra "aaa" num brief é lida como a terceira escala (piso de acabamento em escopo
    focado), porque é o único sentido que este harness aceita para ela; a nota diz isso.
    """
    if declared is not None and declared not in SCALES:
        raise ValueError("escala desconhecida")
    suggested, source = None, None
    for mention in mentions:
        raw = mention["value"].strip()
        # Um template traz o campo com as três opções entre colchetes; isso é a
        # pergunta, não a resposta, e lê-lo como "jam" faria todo rascunho parecer
        # decidido. Placeholder é ignorado; o valor real vem de outro documento.
        if raw.startswith(("[", "{{", "<")) or "preencher" in normalize_text(raw):
            continue
        value = normalize_text(raw)
        tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", value)
        for scale, keywords in SCALE_KEYWORDS.items():
            if any(keyword in tokens or (" " in keyword and keyword in value) for keyword in keywords):
                suggested, source = scale, {
                    "path": mention["path"],
                    "line": mention["line"],
                    "value": mention["value"],
                }
                break
        if suggested:
            break
    chosen = declared or suggested
    report = {
        "name": chosen,
        "available": list(SCALES),
        "basis": (
            "--scale declarado na conversa" if declared
            else "campo Escala localizado em documento; confirme na conversa" if suggested
            else "não declarada; infira uma vez pelo pedido e pelo estado, e registre no brief com `teach`"
        ),
        "source": None if declared else source,
        "guide": str(FRAMEWORK / "references/ambition.md"),
        "scope": "Governa quantidade de artefatos e de conteúdo, nunca o piso do verbo. 'aaa' em documento é lido como a escala aa (piso de acabamento), não como tier de publisher. O comando lê o campo; não classifica o jogo.",
    }
    named = read_scale_optional_scope()
    if named:
        report["scope"] += named
    return report


# A receita já recusa que o
# piso do verbo seja opcional.
# Sem isto o scale copiava a
# quantidade e calava a recusa.
# Escala no disco não é o piso.
CREATE_OPTIONAL = re.compile(r"não é\s+opcional em nenhuma")


def recipe_refuses_verb_floor_as_optional(text):
    return bool(text and CREATE_OPTIONAL.search(text))


def read_scale_optional_source():
    path = FRAMEWORK / "recipes/create.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_verb_floor_as_optional(text):
        return "recipes/create.md"
    return None


def read_scale_optional_scope():
    if not read_scale_optional_source():
        return None
    return (
        " O disco recusa que o piso do verbo seja opcional "
        "(`opcional`). Escala no disco não é o piso."
    )


def command_catalog():
    """Catálogo dos sub-comandos da skill, lido do JSON ao lado das referências."""
    data = read_json(COMMANDS_PATH)
    if not isinstance(data.get("commands"), dict) or not isinstance(data.get("categories"), dict):
        raise ValueError(f"catálogo de comandos malformado: {COMMANDS_PATH}")
    return data


def command_listing():
    catalog = command_catalog()
    row_scope = command_row_scope()
    rows = []
    for name, entry in catalog["commands"].items():
        reference = FRAMEWORK / f"commands/{name}.md"
        rows.append({
            "name": name,
            "category": entry["category"],
            "category_label": catalog["categories"].get(entry["category"], entry["category"]),
            "description": entry["description"],
            "argument_hint": entry.get("argument_hint", ""),
            "reference": str(reference),
            "reference_present": command_reference_present_reading(reference.is_file()),
            "foci": list(entry.get("foci", ())),
            "scope": row_scope,
        })
    return {
        "schema_version": 1,
        "skill": str(FRAMEWORK / "SKILL.md"),
        "categories": catalog["categories"],
        "commands": rows,
        "pinned_marker": PIN_MARKER,
        "scope": catalog.get("scope", ""),
    }


# O menu já recusa invocar sem carregar a referência. Sem isto a
# linha copiava o nome e calava a recusa.
# Linha no catálogo não é a skill carregada.
COMMANDS_GUIDE = FRAMEWORK / "commands/README.md"
COMMAND_GENERIC = re.compile(r"sem carregar a referência produz trabalho genérico")


def menu_refuses_generic_work(text):
    return bool(text and COMMAND_GENERIC.search(text))


def command_row_generic_source():
    path = COMMANDS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if menu_refuses_generic_work(text):
        return "commands/README.md"
    return None


def command_row_scope():
    scope = (
        "Nome, categoria e referência do sub-comando. Não carrega a "
        "skill e não executa o fluxo."
    )
    if command_row_generic_source():
        scope += (
            " O disco recusa invocar sem carregar a referência (`genérico`). "
            "Linha no catálogo não é a skill carregada."
        )
    return scope


# O menu já recusa que o arquivo
# presente seja a referência
# carregada. Sem isto o commands
# relatava o reference_present e
# calava a recusa. Arquivo no
# disco não é a skill.
COMMAND_LOADED = re.compile(r"arquivo presente não é a referência carregada")


def menu_refuses_present_file_as_loaded_reference(text):
    return bool(text and COMMAND_LOADED.search(text))


def command_reference_present_loaded_source():
    path = COMMANDS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if menu_refuses_present_file_as_loaded_reference(text):
        return "commands/README.md"
    return None


def command_reference_present_loaded_scope():
    if not command_reference_present_loaded_source():
        return None
    return (
        " O disco recusa que o arquivo presente seja a referência carregada "
        "(`carregada`). Arquivo no disco não é a skill."
    )


def command_reference_present_scope():
    scope = (
        "arquivo da referência no disco. "
        "O commands não carrega a skill."
    )
    named = command_reference_present_loaded_scope()
    if named:
        scope += named
    return scope


def command_reference_present_flag(reading):
    present = reading
    if isinstance(reading, dict) and "reference_present" in reading:
        present = reading.get("reference_present")
    if isinstance(present, dict):
        return bool(present.get("reference_present"))
    return bool(present)


def command_reference_present_reading(present):
    if not present:
        return False
    return {
        "reference_present": True,
        "scope": command_reference_present_scope(),
    }


def command_problems():
    """Catálogo, arquivos e SKILL.md precisam andar juntos; a lista sai vazia quando andam."""
    problems = []
    try:
        catalog = command_catalog()
    except (OSError, ValueError) as error:
        return [str(error)]
    names = list(catalog["commands"])
    for name, entry in catalog["commands"].items():
        if entry.get("category") not in catalog["categories"]:
            problems.append(f"{name}: categoria desconhecida {entry.get('category')!r}")
        if not (FRAMEWORK / f"commands/{name}.md").is_file():
            problems.append(f"{name}: referência commands/{name}.md ausente")
        for relative in entry.get("reads", ()):
            if not (FRAMEWORK / relative).is_file():
                problems.append(f"{name}: leitura {relative} ausente")
    for path in sorted((FRAMEWORK / "commands").glob("*.md")):
        if path.stem != "README" and path.stem not in names:
            problems.append(f"commands/{path.name} sem entrada no catálogo")
    skill = FRAMEWORK / "SKILL.md"
    text = skill.read_text(encoding="utf-8") if skill.is_file() else ""
    for name in names:
        if f"commands/{name}.md" not in text:
            problems.append(f"SKILL.md não lista `{name}`")
    return problems


def harness_skill_dirs(root):
    """Diretórios de skills do host onde a game-dev está instalada: só neles faz sentido fixar atalho."""
    return [target.parent.parent for target in skill_targets(root) if target.parent.is_dir()]


def pinned_skill(name, entry):
    description = entry["description"].replace('"', "'")
    hint = entry.get("argument_hint", "")
    reference = FRAMEWORK / f"commands/{name}.md"
    return (
        f"---\nname: {name}\ndescription: \"{description}\"\nargument-hint: \"{hint}\"\nuser-invocable: true\n---\n\n"
        f"{PIN_MARKER}\n\n"
        f"Atalho fixado para `$game-dev {name}`.\n\n"
        f"Invoque `$game-dev {name}` passando os argumentos recebidos aqui: leia a skill em `{FRAMEWORK / 'SKILL.md'}`, "
        f"cumpra a preparação (contexto, escala) e siga a referência do comando em `{reference}`.\n"
    )


def pin(root, name):
    catalog = command_catalog()
    if name not in catalog["commands"]:
        raise ValueError(f"comando desconhecido: {name}. Disponíveis: {', '.join(catalog['commands'])}")
    targets = harness_skill_dirs(root)
    if not targets:
        raise ValueError(
            f"nenhum diretório de skills com game-dev instalada em {root} "
            f"({', '.join(str(t.parent) for t in skill_targets(root))}); instale a skill antes de fixar atalhos."
        )
    created, skipped = [], []
    for skills_dir in targets:
        skill_dir = skills_dir / name
        skill_file = skill_dir / "SKILL.md"
        if skill_file.is_file() and PIN_MARKER not in skill_file.read_text(encoding="utf-8"):
            skipped.append({
                "path": str(skill_file),
                "reason": "skill_not_pinned_by_game_dev",
                "scope": pin_skipped_scope(),
            })
            continue
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(pinned_skill(name, catalog["commands"][name]), encoding="utf-8")
        created.append(str(skill_file))
    return {
        "command": name, "created": pin_created_reading(created), "skipped": skipped,
        "invoke": f"/{name}" if created else None,
        "scope": "Cria um atalho que redireciona para `$game-dev <comando>`; não copia a skill nem altera a referência do comando.",
    }


def unpin(root, name):
    catalog = command_catalog()
    if name not in catalog["commands"]:
        raise ValueError(f"comando desconhecido: {name}. Disponíveis: {', '.join(catalog['commands'])}")
    removed, skipped = [], []
    for skills_dir in harness_skill_dirs(root):
        skill_file = skills_dir / name / "SKILL.md"
        if not skill_file.is_file():
            continue
        if PIN_MARKER not in skill_file.read_text(encoding="utf-8"):
            skipped.append({
                "path": str(skill_file),
                "reason": "skill_not_pinned_by_game_dev",
                "scope": pin_skipped_scope(),
            })
            continue
        shutil.rmtree(skill_file.parent)
        removed.append(str(skill_file))
    return {
        "command": name, "removed": removed, "skipped": skipped,
        "scope": "Remove só atalhos com o marcador deste harness; uma skill própria do usuário com o mesmo nome fica intacta.",
    }


# O README já recusa sobrescrever skill sua com o mesmo nome. Sem
# isto o skipped copiava o path e calava a recusa.
# Atalho no disco não é a skill.
PIN_OWN = re.compile(r"uma skill sua com o mesmo nome nunca é\s+sobrescrita")


def readme_refuses_own_skill_overwrite(text):
    return bool(text and PIN_OWN.search(text))


def pin_own_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_own_skill_overwrite(text):
        return "README.md"
    return None


def pin_skipped_scope():
    scope = (
        "Caminho e motivo do atalho recusado. Não lê a skill e não "
        "altera o arquivo."
    )
    if pin_own_source():
        scope += (
            " O disco recusa sobrescrever uma skill sua com o mesmo nome "
            "(`própria`). Atalho no disco não é a skill."
        )
    mark = pin_skipped_mark_scope()
    if mark:
        scope += mark
    return scope


# O README já recusa que o unpin
# remova o que não tem o marcador.
# Sem isto o skipped copiava o path
# e calava a recusa.
# Skill no disco não é o atalho.
PIN_MARK = re.compile(r"`unpin` remove só o que tem o marcador")


def readme_refuses_unpin_without_marker(text):
    return bool(text and PIN_MARK.search(text))


def pin_skipped_mark_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_unpin_without_marker(text):
        return "README.md"
    return None


def pin_skipped_mark_scope():
    if not pin_skipped_mark_source():
        return None
    return (
        " O disco recusa que o unpin remova o que não tem o marcador "
        "(`marcador`). Skill no disco não é o atalho."
    )


# O README já recusa que o pin
# copie a skill. Sem isto o pin
# relatava o created e calava a
# recusa. Atalho no disco não é
# a skill.
PIN_COPY = re.compile(r"não copia a skill")


def readme_refuses_pin_as_copying_skill(text):
    return bool(text and PIN_COPY.search(text))


def pin_created_copy_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_pin_as_copying_skill(text):
        return "README.md"
    return None


def pin_created_copy_scope():
    if not pin_created_copy_source():
        return None
    return (
        " O disco recusa que o pin copie a skill "
        "(`cópia`). Atalho no disco não é a skill."
    )


# O processo já recusa que a
# neutralidade de interface
# prove substitutibilidade. Sem
# isto o pin relatava o created
# e calava a recusa. Neutralidade
# no disco não é a skill.
PIN_SWAP = re.compile(r"neutralidade de interface não prova substitutibilidade")


def process_refuses_neutrality_as_substitutable(text):
    return bool(text and PIN_SWAP.search(text))


def pin_created_swap_source():
    path = FRAMEWORK / "references/process.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_neutrality_as_substitutable(text):
        return "references/process.md"
    return None


def pin_created_swap_scope():
    if not pin_created_swap_source():
        return None
    return (
        " O disco recusa que a neutralidade de interface prove substitutibilidade "
        "(`substitutibilidade`). Neutralidade no disco não é a skill."
    )


# O README já recusa que a
# referência de comando seja
# uma receita nova. Sem isto
# o pin relatava o created e
# calava a recusa. Atalho no
# disco não é a receita.
PIN_ORCH = re.compile(r"orquestrador fino, não uma receita nova")


def readme_refuses_command_ref_as_new_recipe(text):
    return bool(text and PIN_ORCH.search(text))


def pin_created_orch_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_command_ref_as_new_recipe(text):
        return "README.md"
    return None


def pin_created_orch_scope():
    if not pin_created_orch_source():
        return None
    return (
        " O disco recusa que a referência de comando seja uma receita nova "
        "(`orquestrador`). Atalho no disco não é a receita."
    )


def pin_created_scope():
    scope = (
        "atalho escrito no host. "
        "O pin não copia a skill."
    )
    named = pin_created_copy_scope()
    if named:
        scope += named
    swap = pin_created_swap_scope()
    if swap:
        scope += swap
    thin = pin_created_orch_scope()
    if thin:
        scope += thin
    return scope


def pin_created_paths(reading):
    created = (reading or {}).get("created") if isinstance(reading, dict) else reading
    if isinstance(created, dict):
        return list(created.get("created") or [])
    return list(created or [])


def pin_created_reading(created):
    if not created:
        return created
    return {
        "created": list(created),
        "scope": pin_created_scope(),
    }


def select_packs(kind, genre, mentions):
    pack_name = PLATFORM_PACKS.get(kind)
    platform_path = FRAMEWORK / f"packs/platforms/{pack_name}.md" if pack_name else None
    genre_path = FRAMEWORK / f"packs/genres/{genre}.md" if genre else None
    suggested = suggest_genres(mentions)
    return {
        "platform": {
            "kind": kind, "pack": str(platform_path) if platform_path and platform_path.is_file() else None,
            "basis": "identify: marcador de manifesto/engine no diretório do projeto" if kind else "projeto sem marcador reconhecido; núcleo agnóstico apenas",
            "scope": platform_scope(kind),
        },
        "genre": {
            "name": genre, "pack": str(genre_path) if genre_path and genre_path.is_file() else None,
            "basis": "--genre declarado na conversa" if genre else ("campo Gênero localizado em documento; confirme e passe --genre" if suggested else "não declarado; passe --genre quando o jogo tiver gênero definido"),
            "suggested": suggested,
            "mentions": [
                {"path": item["path"], "line": item["line"], "value": item["value"]}
                for item in mentions
            ],
            "available": list(GENRES),
            "scope": genre_scope(genre),
        },
        "scope": packs_scope(kind),
    }


# O índice já recusa que o pacote certifique capacidade. Sem isto a
# plataforma apontava o arquivo e calava a recusa.
# Pacote no disco não é comportamento.
PACKS_INDEX = FRAMEWORK / "packs/README.md"
PACKS_CAPACITY = re.compile(r"não certifica capacidade")


def packs_refuse_capacity(text):
    return bool(text and PACKS_CAPACITY.search(text))


def platform_capacity_source(kind):
    if not kind or kind not in PLATFORM_PACKS:
        return None
    path = PACKS_INDEX
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if packs_refuse_capacity(text):
        return "packs/README.md"
    return None


def platform_scope(kind):
    scope = (
        "Seleciona o pacote pelo marcador do projeto. "
        "Não substitui o que o código faz."
    )
    if platform_capacity_source(kind):
        scope += (
            " O disco recusa que o pacote certifique capacidade (`capacidade`). "
            "Pacote no disco não é comportamento."
        )
    if platform_gpu_source(kind):
        scope += (
            " O disco recusa que métricas RAF comprovem os quadros "
            "(`quadros`). Callback no disco não é quadro apresentado."
        )
    return scope


# O pacote já recusa que RAF prove quadro da GPU. Sem isto a
# plataforma apontava o arquivo e calava a recusa.
# Callback no disco não é quadro apresentado.
WEB_GPU = re.compile(r"não comprovam quadros apresentados pela GPU")


def pack_refuses_raf_as_gpu(text):
    return bool(text and WEB_GPU.search(text))


def platform_gpu_source(kind):
    pack_name = PLATFORM_PACKS.get(kind)
    if not pack_name:
        return None
    path = FRAMEWORK / f"packs/platforms/{pack_name}.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if pack_refuses_raf_as_gpu(text):
        return f"packs/platforms/{pack_name}.md"
    return None


# O mapa já recusa que o pacote seja extração. Sem isto o
# gênero apontava o arquivo e calava a recusa.
# Convenção no disco não é repositório executado.
SOURCES_EXTRACTION = re.compile(r"Não são extração\s+de repositório")


def sources_refuse_extraction(text):
    return bool(text and SOURCES_EXTRACTION.search(text))


def genre_extraction_source(genre):
    if not genre or genre not in GENRES:
        return None
    path = FRAMEWORK / "references/sources.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if sources_refuse_extraction(text):
        return "references/sources.md"
    return None


def genre_scope(genre):
    scope = (
        "Seleciona o pacote pelo --genre declarado. "
        "Não substitui o GDD nem o que o código faz."
    )
    if genre_extraction_source(genre):
        scope += (
            " O disco recusa que o pacote seja extração (`extração`). "
            "Convenção no disco não é repositório executado."
        )
    return scope


# O mapa já recusa que a menção seja mecânica obrigatória.
# Sem isto o campo copiava o valor e calava a recusa.
# Campo no disco não é regra do jogo.
SOURCES_MECHANIC = re.compile(r"mecânica obrigatória")


def sources_refuse_obligatory_mechanic(text):
    return bool(text and SOURCES_MECHANIC.search(text))


def genre_mention_mechanic_source():
    path = FRAMEWORK / "references/sources.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if sources_refuse_obligatory_mechanic(text):
        return "references/sources.md"
    return None


def genre_mention_scope():
    scope = (
        "Campo Gênero localizado no documento. Não classifica e não "
        "carrega o pacote."
    )
    if genre_mention_mechanic_source():
        scope += (
            " O disco recusa que a menção seja mecânica obrigatória (`mecânica`). "
            "Campo no disco não é regra do jogo."
        )
    return scope


# A ambição já recusa AAA como adjetivo de marketing. Sem isto o
# campo copiava o valor e calava a recusa.
# Campo no disco não é campanha.
AMBITION_GUIDE = FRAMEWORK / "references/ambition.md"
SCALE_MARKETING = re.compile(r"adjetivo de marketing")


def ambition_refuses_marketing_adjective(text):
    return bool(text and SCALE_MARKETING.search(text))


def scale_mention_marketing_source():
    path = AMBITION_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if ambition_refuses_marketing_adjective(text):
        return "references/ambition.md"
    return None


def scale_mention_scope():
    scope = (
        "Campo Escala localizado no documento. Não classifica e não "
        "promove o recorte."
    )
    if scale_mention_marketing_source():
        scope += (
            " O disco recusa AAA como adjetivo de marketing (`marketing`). "
            "Campo no disco não é campanha."
        )
    return scope


# O roteiro já pede documentar sem consentimento. Sem isto o
# context apontava o arquivo e calava a política.
# Roteiro no disco não é base escrita.
AUDIT_GUIDE = FRAMEWORK / "references/project-audit.md"
AUDIT_CONSENT = re.compile(
    r"avisar e começar a documentar,\s*sem pedir\s+consentimento",
    re.IGNORECASE,
)


def audit_guide_declares(text):
    return bool(text and AUDIT_CONSENT.search(text))


def documentation_audit_source(document_minimum):
    if not document_minimum:
        return None
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_guide_declares(text):
        return "references/project-audit.md"
    return None


# O roteiro já recusa que a checagem seja daemon. Sem isto o
# audit apontava o arquivo e calava a recusa.
# Roteiro no disco não é interceptação.
AUDIT_DAEMON = re.compile(r"não é um daemon nem um hook")


def project_audit_refuses_daemon(text):
    return bool(text and AUDIT_DAEMON.search(text))


def audit_daemon_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if project_audit_refuses_daemon(text):
        return "references/project-audit.md"
    return None


def audit_scope():
    scope = (
        "Aviso e levantamento documental. Não executa o jogo e não "
        "intercepta o host."
    )
    if audit_daemon_source():
        scope += (
            " O disco recusa que a checagem seja daemon (`daemon`). "
            "Roteiro no disco não é interceptação."
        )
    named = audit_stop_scope()
    if named:
        scope += named
    return scope


# O roteiro já recusa que executed
# falso seja uma instrução para
# parar. Sem isto o audit relatava
# o comando e calava a recusa.
# Roteiro no disco não é espera.
AUDIT_STOP = re.compile(r"não é uma instrução para parar")


def project_audit_refuses_false_as_stop(text):
    return bool(text and AUDIT_STOP.search(text))


def audit_stop_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if project_audit_refuses_false_as_stop(text):
        return "references/project-audit.md"
    return None


def audit_stop_scope():
    if not audit_stop_source():
        return None
    return (
        " O disco recusa que executed falso seja uma instrução para parar "
        "(`parar`). Roteiro no disco não é espera."
    )


# O roteiro já recusa que a lacuna de
# rascunho seja auditoria neste turno.
# Sem isto o scan relatava o deferred
# e calava a recusa. Sinal no disco
# não é o levantamento.
AUDIT_DRAFT = re.compile(r"não é auditoria neste\s+turno")


def project_audit_refuses_draft_gap_as_audit(text):
    return bool(text and AUDIT_DRAFT.search(text))


def audit_deferred_audit_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if project_audit_refuses_draft_gap_as_audit(text):
        return "references/project-audit.md"
    return None


def audit_deferred_audit_scope():
    if not audit_deferred_audit_source():
        return None
    return (
        " O disco recusa que a lacuna de rascunho seja auditoria neste turno "
        "(`auditoria`). Sinal no disco não é o levantamento."
    )


def audit_deferred_scope():
    scope = (
        "ciclo fresco que já abre. "
        "Lacuna de rascunho não é auditoria neste turno."
    )
    named = audit_deferred_audit_scope()
    if named:
        scope += named
    return scope


def audit_deferred_flag(reading):
    deferred = (reading or {}).get("deferred")
    if isinstance(deferred, dict):
        return bool(deferred.get("deferred"))
    return bool(deferred)


def audit_deferred_reading(waiting):
    if not waiting:
        return False
    return {
        "deferred": True,
        "scope": audit_deferred_scope(),
    }


# O roteiro já recusa que o scanner
# comece a auditoria. Sem isto o
# scan relatava o required e calava
# a recusa. JSON no disco não é o
# levantamento.
AUDIT_BEGIN = re.compile(r"começar auditoria")


def project_audit_refuses_scanner_as_starting_audit(text):
    return bool(text and AUDIT_BEGIN.search(text))


def audit_required_begin_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if project_audit_refuses_scanner_as_starting_audit(text):
        return "references/project-audit.md"
    return None


def audit_required_begin_scope():
    if not audit_required_begin_source():
        return None
    return (
        " O disco recusa que o scanner comece a auditoria "
        "(`começo`). JSON no disco não é o levantamento."
    )


def audit_required_scope():
    scope = (
        "base documental pedida neste turno. "
        "Não começa a auditoria."
    )
    named = audit_required_begin_scope()
    if named:
        scope += named
    return scope


def audit_required_flag(reading):
    required = (reading or {}).get("required")
    if isinstance(required, dict):
        return bool(required.get("required"))
    return bool(required)


def audit_required_reading(required):
    if not required:
        return False
    return {
        "required": True,
        "scope": audit_required_scope(),
    }


# O roteiro já recusa que reconstruir documentos comprove intenções. Sem isto o
# candidato copiava o path e calava a recusa.
# Candidato no disco não é autoria.
AUDIT_INTENT = re.compile(r"não comprova intenções autorais")


def audit_refuses_rebuilt_intent(text):
    return bool(text and AUDIT_INTENT.search(text))


def scan_candidate_intent_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_refuses_rebuilt_intent(text):
        return "references/project-audit.md"
    return None


def scan_candidate_scope():
    scope = (
        "Path, linha e estado do documento candidato. Não observa o "
        "jogo e não atribui autoria."
    )
    if scan_candidate_intent_source():
        scope += (
            " O disco recusa que reconstruir documentos comprove intenções (`intenções`). "
            "Candidato no disco não é autoria."
        )
    return scope


# A receita já recusa que contexto carregado prove a arquitetura
# compreendida. Sem isto o candidato copiava o path e calava a recusa.
# Candidato no disco não é a decisão.
ARCHITECTURE_UNDERSTOOD = re.compile(
    r"n[aã]o significa.{0,4}arquitetura compreendida",
)


def recipe_refuses_loaded_as_understood(text):
    return bool(text and ARCHITECTURE_UNDERSTOOD.search(text))


def architecture_understood_source():
    path = ARCHITECTURE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_loaded_as_understood(text):
        return "recipes/architecture.md"
    return None


def architecture_candidate_understood_scope():
    if not architecture_understood_source():
        return ""
    return (
        " O disco recusa que contexto carregado prove a arquitetura compreendida "
        "(`compreendida`). Candidato no disco não é a decisão."
    )


# O roteiro já recusa que o local não percorrido seja inexistente. Sem isto o
# scan contava documentos e calava a recusa.
# Contagem no disco não é inventário.
AUDIT_ABSENCE = re.compile(r"não percorrido não equivale\s+a conteúdo inexistente")


def audit_refuses_unwalked_absence(text):
    return bool(text and AUDIT_ABSENCE.search(text))


def coverage_absence_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_refuses_unwalked_absence(text):
        return "references/project-audit.md"
    return None


def coverage_scope():
    scope = (
        "Conta documentos localizados, lidos e adiados no recorte. "
        "Não afirma suficiência nem qualidade."
    )
    if coverage_absence_source():
        scope += (
            " O disco recusa que o local não percorrido seja inexistente (`inexistente`). "
            "Contagem no disco não é inventário."
        )
    named = coverage_lexical_scope()
    if named:
        scope += named
    return scope


# O teach já recusa que cobertura
# lexical seja a prova. Sem isto
# o coverage contava documentos e
# calava a recusa. Varredura no
# disco não é o rastro.
TEACH_LEXICAL = re.compile(r"cobertura lexical não é a prova")


def teach_refuses_lexical_coverage_as_proof(text):
    return bool(text and TEACH_LEXICAL.search(text))


def coverage_lexical_source():
    path = FRAMEWORK / "commands/teach.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if teach_refuses_lexical_coverage_as_proof(text):
        return "commands/teach.md"
    return None


def coverage_lexical_scope():
    if not coverage_lexical_source():
        return None
    return (
        " O disco recusa que cobertura lexical seja a prova "
        "(`lexical`). Varredura no disco não é o rastro."
    )


# O roteiro já recusa que o recorte de estudo tome a prioridade.
# Sem isto os limites copiavam os tetos e calavam a recusa.
# Limite no disco não é a base.
AUDIT_PRIORITY = re.compile(r"não toma a prioridade")


def audit_refuses_study_priority(text):
    return bool(text and AUDIT_PRIORITY.search(text))


def coverage_limits_priority_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_refuses_study_priority(text):
        return "references/project-audit.md"
    return None


def coverage_limits_scope():
    scope = (
        "Tetos do recorte documental. Não afirma que o inventário "
        "está completo e não lê o que ficou de fora."
    )
    if coverage_limits_priority_source():
        scope += (
            " O disco recusa que o recorte de estudo tome a prioridade "
            "(`prioridade`). Limite no disco não é a base."
        )
    return scope


# O mapa já recusa que a cobertura desigual seja acidente.
# Sem isto o issue copiava o motivo e calava a recusa.
# Recorte no disco não é falha.
SOURCES_ACCIDENT = re.compile(r"não é acidente")


def sources_refuse_uneven_accident(text):
    return bool(text and SOURCES_ACCIDENT.search(text))


def coverage_issue_accident_source():
    path = FRAMEWORK / "references/sources.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if sources_refuse_uneven_accident(text):
        return "references/sources.md"
    return None


def coverage_issue_scope():
    scope = (
        "Limite, leitura ou ligação que o recorte não cobriu. Não "
        "completa o inventário e não observa o jogo."
    )
    if coverage_issue_accident_source():
        scope += (
            " O disco recusa que a cobertura desigual seja acidente (`acidente`). "
            "Recorte no disco não é falha."
        )
    return scope


# O roteiro já recusa que a lista
# cortada seja a cobertura. Sem
# isto o scan relatava o truncated
# e calava a recusa. Recorte no
# disco não é o inventário.
COVERAGE_TRUNCATED = re.compile(r"Lista cortada não é a cobertura")


def recipe_refuses_cut_issue_list_as_coverage(text):
    return bool(text and COVERAGE_TRUNCATED.search(text))


def coverage_issues_truncated_lack_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_cut_issue_list_as_coverage(text):
        return "references/project-audit.md"
    return None


def coverage_issues_truncated_lack_scope():
    if not coverage_issues_truncated_lack_source():
        return None
    return (
        " O disco recusa que a lista cortada seja a cobertura "
        "(`falta`). Recorte no disco não é o inventário."
    )


def coverage_issues_truncated_scope():
    scope = (
        "a lista de issues parou no vigésimo. "
        "O scan não completa o inventário."
    )
    named = coverage_issues_truncated_lack_scope()
    if named:
        scope += named
    return scope


def coverage_issues_truncated_flag(reading):
    truncated = reading
    if isinstance(reading, dict):
        if "issues_truncated" in reading:
            truncated = reading.get("issues_truncated")
        elif "coverage" in reading and isinstance(reading.get("coverage"), dict):
            truncated = reading["coverage"].get("issues_truncated")
    if isinstance(truncated, dict):
        return bool(truncated.get("issues_truncated"))
    return bool(truncated)


def coverage_issues_truncated_reading(truncated):
    if not truncated:
        return False
    return {
        "issues_truncated": True,
        "scope": coverage_issues_truncated_scope(),
    }


# A guia já recusa que preencher linhas certifique o jogo.
# Sem isto o rascunho copiava o estado e calava a recusa.
# Documento no disco não é o jogo.
PREPRODUCTION_LINES = re.compile(r"preencher linhas não certifica o jogo")


def guide_refuses_lines_as_game(text):
    return bool(text and PREPRODUCTION_LINES.search(text))


def coverage_draft_lines_source():
    path = FRAMEWORK / "references/preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_lines_as_game(text):
        return "references/preproduction.md"
    return None


def coverage_draft_scope():
    scope = (
        "Caminho e estado do documento que deixou de ser vigente. "
        "Não certifica o jogo e não observa a sessão."
    )
    if coverage_draft_lines_source():
        scope += (
            " O disco recusa que preencher linhas certifique o jogo (`linhas`). "
            "Documento no disco não é o jogo."
        )
    return scope


# O contrato já recusa que o scanner certifique tokens. Sem isto a
# área localizava o documento e calava a recusa.
# Documento no disco não é aprovação artística.
SYSTEM_GUIDE = FRAMEWORK / "references/game-design-system.md"
SYSTEM_TOKENS = re.compile(r"não\s+certifica tokens")


def system_refuses_token_certification(text):
    return bool(text and SYSTEM_TOKENS.search(text))


def art_direction_tokens_source():
    path = SYSTEM_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if system_refuses_token_certification(text):
        return "references/game-design-system.md"
    return None


def art_direction_scope():
    scope = (
        "Localiza o documento da direção. Não compara silhueta e não "
        "aprova estilo."
    )
    if art_direction_tokens_source():
        scope += (
            " O disco recusa que o scanner certifique tokens (`tokens`). "
            "Documento no disco não é aprovação artística."
        )
    image = art_direction_image_scope()
    if image:
        scope += image
    return scope


# O visual já recusa que salvar
# a imagem seja o trabalho. Sem
# isto a área localizava o bible
# e calava a recusa. Imagem no
# disco não é a aprovação.
VISUAL_IMAGE = re.compile(r"Salvar a imagem não é o trabalho")


def visual_refuses_saving_image_as_the_work(text):
    return bool(text and VISUAL_IMAGE.search(text))


def art_direction_image_source():
    path = FRAMEWORK / "commands/visual.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if visual_refuses_saving_image_as_the_work(text):
        return "commands/visual.md"
    return None


def art_direction_image_scope():
    if not art_direction_image_source():
        return None
    return (
        " O disco recusa que salvar a imagem seja o trabalho "
        "(`imagem`). Imagem no disco não é a aprovação."
    )


# O contrato já recusa que a paleta compartilhada seja o sistema. Sem isto o
# item copiava a chave e calava a recusa.
# Lista no disco não é contrato.
SYSTEM_PALETTE = re.compile(r"não é uma paleta compartilhada")


def system_refuses_shared_palette(text):
    return bool(text and SYSTEM_PALETTE.search(text))


def art_palette_system_source():
    path = SYSTEM_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if system_refuses_shared_palette(text):
        return "references/game-design-system.md"
    return None


def art_palette_scope():
    scope = (
        "Nome e origem da paleta listada. Não compara silhueta e não "
        "aprova o sistema."
    )
    if art_palette_system_source():
        scope += (
            " O disco recusa que a paleta compartilhada seja o sistema (`paleta`). "
            "Lista no disco não é contrato."
        )
    return scope


# A receita já recusa que a mesa seja volume. Sem isto o
# item copiava a chave e calava a recusa.
# Lista no disco não é comparação.
VISUAL_RECIPE = FRAMEWORK / "recipes/visual.md"
VISUAL_VOLUME = re.compile(r"Mesa no disco não é volume")


def recipe_refuses_table_volume(text):
    return bool(text and VISUAL_VOLUME.search(text))


def art_rain_volume_source():
    path = VISUAL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_table_volume(text):
        return "recipes/visual.md"
    return None


def art_rain_scope():
    scope = (
        "Chave e fonte da mesa de chuva. Não compara em "
        "movimento e não conta volume."
    )
    if art_rain_volume_source():
        scope += (
            " O disco recusa que a mesa seja volume (`volume`). "
            "Lista no disco não é comparação."
        )
    return scope


# A receita já recusa que a mesa no
# disco seja comparação em movimento.
# Sem isto o art listava as mesas e
# calava a recusa. Mesa no disco não
# é o quadro.
VISUAL_MOTION = re.compile(r"volume nem comparação em movimento")


def recipe_refuses_table_as_motion(text):
    return bool(text and VISUAL_MOTION.search(text))


def art_rains_motion_source():
    path = VISUAL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_table_as_motion(text):
        return "recipes/visual.md"
    return None


def art_rains_motion_scope():
    if not art_rains_motion_source():
        return None
    return (
        " O disco recusa que a mesa no disco seja comparação em movimento "
        "(`movimento`). Mesa no disco não é o quadro."
    )


def art_rains_scope():
    scope = (
        "mesas de chuva no disco. "
        "Não compara em movimento."
    )
    named = art_rains_motion_scope()
    if named:
        scope += named
    return scope


def art_rain_items(reading):
    rains = (reading or {}).get("rains") or []
    if isinstance(rains, dict):
        return list(rains.get("items") or [])
    return list(rains)


# A receita já recusa que importação sem
# erro comprove aparência equivalente.
# Sem isto o art listava paletas e calava
# a recusa. Importar no disco não é o
# renderer.
VISUAL_APPEAR = re.compile(r"importação sem erro não comprova aparência")


def recipe_refuses_import_as_appearance(text):
    return bool(text and VISUAL_APPEAR.search(text))


def art_appearance_source():
    path = VISUAL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_import_as_appearance(text):
        return "recipes/visual.md"
    return None


def art_appearance_scope():
    if not art_appearance_source():
        return None
    return (
        " O disco recusa que importação sem erro comprove aparência "
        "equivalente (`aparência`). Importar no disco não é o renderer."
    )


# A receita já recusa que uma correção local
# valide o enquadramento. Sem isto o art
# listava paletas e calava a recusa.
# Correção no disco não é o conjunto.
VISUAL_FRAME = re.compile(r"correção local não valida o enquadramento")


def recipe_refuses_local_as_framing(text):
    return bool(text and VISUAL_FRAME.search(text))


def art_framing_source():
    path = VISUAL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_local_as_framing(text):
        return "recipes/visual.md"
    return None


def art_framing_scope():
    if not art_framing_source():
        return None
    return (
        " O disco recusa que uma correção local valide o enquadramento "
        "(`enquadramento`). Correção no disco não é o conjunto."
    )


# A receita já recusa que câmera próxima
# e geometria numericamente correta
# provem leitura. Sem isto o art listava
# paletas e calava a recusa. Número no
# disco não é a silhueta.
FEEL_GEOMETRY = re.compile(r"geometria numericamente correta não provam leitura")


def recipe_refuses_geometry_as_reading(text):
    return bool(text and FEEL_GEOMETRY.search(text))


def art_geometry_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_geometry_as_reading(text):
        return "recipes/feel.md"
    return None


def art_geometry_scope():
    if not art_geometry_source():
        return None
    return (
        " O disco recusa que câmera próxima e geometria numericamente "
        "correta provem leitura (`geometria`). Número no disco não é a "
        "silhueta."
    )


# A receita já recusa que o lean
# seja punch. Sem isto o art
# listava paletas e calava a
# recusa. Lean no disco não é
# o punch.
VISUAL_PUNCH = re.compile(r"já marca; não é punch")


def recipe_refuses_lean_as_punch(text):
    return bool(text and VISUAL_PUNCH.search(text))


def art_punch_source():
    path = VISUAL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_lean_as_punch(text):
        return "recipes/visual.md"
    return None


def art_punch_scope():
    if not art_punch_source():
        return None
    return (
        " O disco recusa que o lean seja punch "
        "(`punch`). Lean no disco não é o punch."
    )


# A receita já recusa que a qualidade
# visual aprovada seja moeda de troca
# por número. Sem isto o art listava
# o manifesto e calava a recusa.
# Manifesto no disco não é comparação.
VISUAL_CURRENCY = re.compile(r"moeda\s+de troca")


def recipe_refuses_quality_as_currency(text):
    return bool(text and VISUAL_CURRENCY.search(text))


def art_currency_source():
    path = VISUAL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_quality_as_currency(text):
        return "recipes/visual.md"
    return None


def art_currency_scope():
    if not art_currency_source():
        return None
    return (
        " O disco recusa que a qualidade visual aprovada seja moeda "
        "de troca por número (`moeda`). Manifesto no disco não é comparação."
    )


def art_manifests_scope():
    scope = (
        "manifesto de paleta no disco. "
        "Não compara silhueta."
    )
    named = art_currency_scope()
    if named:
        scope += named
    return scope


def art_manifest_files(project):
    project = Path(project)
    found = []
    for relative in ART_MANIFESTS:
        path = project / relative
        if path.is_file() and not path.is_symlink():
            found.append(relative)
    return found


# A receita já recusa que o harness infira dependências. Sem isto a
# área localizava o TDD e calava a recusa.
# Receita no disco não é decisão.
ARCHITECTURE_RECIPE = FRAMEWORK / "recipes/architecture.md"
ARCHITECTURE_DEPS = re.compile(r"não infere dependências")


def architecture_refuses_inference(text):
    return bool(text and ARCHITECTURE_DEPS.search(text))


def architecture_deps_source():
    path = ARCHITECTURE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if architecture_refuses_inference(text):
        return "recipes/architecture.md"
    return None


def architecture_area_scope():
    scope = (
        "Localiza o documento técnico. Não escolhe stack e não "
        "aprova a decisão."
    )
    if architecture_deps_source():
        scope += (
            " O disco recusa que o harness infira dependências (`dependências`). "
            "Receita no disco não é decisão."
        )
    if architecture_multiplayer_source():
        scope += (
            " O disco recusa que exemplares locais comprovem comportamento "
            "multiplayer (`multiplayer`). Receita no disco não é sessão real."
        )
    named = architecture_estimate_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que a estimativa
# implícita seja discutível. Sem isto a
# área localizava o TDD e calava a
# recusa. Receita no disco não é decisão.
ARCHITECTURE_ESTIMATE = re.compile(r"estimativa implícita não é nem discutível")


def recipe_refuses_implicit_estimate(text):
    return bool(text and ARCHITECTURE_ESTIMATE.search(text))


def architecture_estimate_source():
    path = ARCHITECTURE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_implicit_estimate(text):
        return "recipes/architecture.md"
    return None


def architecture_estimate_scope():
    if not architecture_estimate_source():
        return None
    return (
        " O disco recusa que a estimativa implícita seja discutível "
        "(`estimativa`). Receita no disco não é decisão."
    )


# A receita já recusa que exemplares locais comprovem multiplayer.
# Sem isto a área localizava o TDD e calava a recusa.
# Receita no disco não é sessão real.
ARCHITECTURE_MULTIPLAYER = re.compile(r"não comprovam comportamento multiplayer")


def recipe_refuses_local_as_multiplayer(text):
    return bool(text and ARCHITECTURE_MULTIPLAYER.search(text))


def architecture_multiplayer_source():
    path = ARCHITECTURE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_local_as_multiplayer(text):
        return "recipes/architecture.md"
    return None


# A receita já recusa promover histórico a regra vigente. Sem
# isto a área localizava o devlog e calava a recusa.
# Área no disco não é decisão atual.
ARCHITECTURE_HISTORY = re.compile(r"histórico a regra vigente")


def recipe_refuses_history_as_rule(text):
    return bool(text and ARCHITECTURE_HISTORY.search(text))


def decisions_history_source():
    path = ARCHITECTURE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_history_as_rule(text):
        return "recipes/architecture.md"
    return None


def decisions_area_scope():
    scope = (
        "Localiza o documento de decisões. Não promove histórico e não "
        "inventa aprovação."
    )
    if decisions_history_source():
        scope += (
            " O disco recusa promover histórico a regra vigente (`histórico`). "
            "Área no disco não é decisão atual."
        )
    efficacy = decisions_efficacy_scope()
    if efficacy:
        scope += efficacy
    return scope


# O mapa já recusa que alegar
# eficácia comprovada seja
# evidência. Sem isto a área
# localizava o devlog e calava
# a recusa. Mapa no disco não
# é o ensaio.
SOURCES_EFFICACY = re.compile(r"alegar eficácia\s+comprovada não é")


def sources_refuse_claimed_efficacy(text):
    return bool(text and SOURCES_EFFICACY.search(text))


def decisions_efficacy_source():
    path = FRAMEWORK / "references/sources.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if sources_refuse_claimed_efficacy(text):
        return "references/sources.md"
    return None


def decisions_efficacy_scope():
    if not decisions_efficacy_source():
        return None
    return (
        " O disco recusa que alegar eficácia comprovada seja evidência "
        "(`eficácia`). Mapa no disco não é o ensaio."
    )


# A guia já recusa que divertido isolado baste. Sem isto a
# área localizava o GDD e calava a recusa.
# Área no disco não é o verbo.
GDD_FUN = re.compile(r"isoladamente não basta")


def guide_refuses_isolated_fun(text):
    return bool(text and GDD_FUN.search(text))


def gdd_fun_source():
    path = FRAMEWORK / "references/preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_isolated_fun(text):
        return "references/preproduction.md"
    return None


def gdd_area_scope():
    scope = (
        "Localiza o documento de design. Não joga e não aprova o verbo."
    )
    if gdd_fun_source():
        scope += (
            " O disco recusa que divertido isolado baste (`divertido`). "
            "Área no disco não é o verbo."
        )
    brief = gdd_brief_scope()
    if brief:
        scope += brief
    return scope


# O craft já recusa que contexto do
# projeto seja brief da tarefa. Sem
# isto a área localizava o GDD e
# calava a recusa.
# Contexto no disco não é o brief.
CRAFT_BRIEF = re.compile(r"Contexto do projeto não é brief da tarefa")


def craft_refuses_context_as_task_brief(text):
    return bool(text and CRAFT_BRIEF.search(text))


def gdd_brief_source():
    path = FRAMEWORK / "commands" / "craft.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if craft_refuses_context_as_task_brief(text):
        return "commands/craft.md"
    return None


def gdd_brief_scope():
    if not gdd_brief_source():
        return ""
    return (
        " O disco recusa que contexto do projeto seja brief da tarefa (`brief`). "
        "Contexto no disco não é o brief."
    )


# A guia já recusa pontuação universal de diversão. Sem isto a
# área localizava o MDA e calava a recusa.
# Área no disco não é experiência.
MDA_SCORE = re.compile(r"pontuação universal\s+de diversão")


def guide_refuses_universal_fun_score(text):
    return bool(text and MDA_SCORE.search(text))


def mda_score_source():
    path = FRAMEWORK / "references/preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_universal_fun_score(text):
        return "references/preproduction.md"
    return None


def mda_area_scope():
    scope = (
        "Localiza o documento de hipóteses. Não observa a sessão e não "
        "pontua diversão."
    )
    if mda_score_source():
        scope += (
            " O disco recusa pontuação universal de diversão (`pontuação`). "
            "Área no disco não é experiência."
        )
    tool = mda_required_scope()
    if tool:
        scope += tool
    return scope


# A guia já recusa que a ferramenta de
# raciocínio seja documento obrigatório.
# Sem isto a área localizava o MDA e
# calava a recusa.
# Ferramenta no disco não é a obrigação.
MDA_REQUIRED = re.compile(r"não documento obrigatório")


def guide_refuses_mda_as_required_document(text):
    return bool(text and MDA_REQUIRED.search(text))


def mda_required_source():
    path = FRAMEWORK / "references" / "preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_mda_as_required_document(text):
        return "references/preproduction.md"
    return None


def mda_required_scope():
    if not mda_required_source():
        return ""
    return (
        " O disco recusa que a ferramenta de raciocínio seja documento "
        "obrigatório (`obrigatório`). Ferramenta no disco não é a obrigação."
    )


# A guia já recusa inventar público observado. Sem isto a
# área localizava o brief e calava a recusa.
# Área no disco não é audiência.
VISION_AUDIENCE = re.compile(r"público observado")


def guide_refuses_invented_audience(text):
    return bool(text and VISION_AUDIENCE.search(text))


def vision_audience_source():
    path = FRAMEWORK / "references/preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_invented_audience(text):
        return "references/preproduction.md"
    return None


def vision_area_scope():
    scope = (
        "Localiza o documento de visão. Não observa o público e não "
        "inventa aprovação."
    )
    if vision_audience_source():
        scope += (
            " O disco recusa inventar público observado (`público`). "
            "Área no disco não é audiência."
        )
    filled = vision_executed_scope()
    if filled:
        scope += filled
    return scope


# O shape já recusa que documento
# preenchido seja PoC executada.
# Sem isto a área localizava o
# brief e calava a recusa.
# Documento no disco não é o
# experimento.
SHAPE_EXECUTED = re.compile(r"Documento preenchido não é PoC executada")


def shape_refuses_filled_doc_as_executed_poc(text):
    return bool(text and SHAPE_EXECUTED.search(text))


def vision_executed_source():
    path = FRAMEWORK / "commands/shape.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if shape_refuses_filled_doc_as_executed_poc(text):
        return "commands/shape.md"
    return None


def vision_executed_scope():
    if not vision_executed_source():
        return None
    return (
        " O disco recusa que documento preenchido seja PoC executada "
        "(`executada`). Documento no disco não é o experimento."
    )


# O roteiro já recusa que o recibo presente seja licença. Sem isto a
# área localizava CREDITS e calava a recusa.
# Área no disco não é concessão.
GATES_LICENSE = re.compile(r"recibo presente não é licença")


def gates_refuse_present_receipt(text):
    return bool(text and GATES_LICENSE.search(text))


def provenance_license_source():
    path = FRAMEWORK / "references/gates.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gates_refuse_present_receipt(text):
        return "references/gates.md"
    return None


def provenance_area_scope():
    scope = (
        "Localiza o documento de origem. Não consulta titular e não "
        "valida licença."
    )
    if provenance_license_source():
        scope += (
            " O disco recusa que o recibo presente seja licença válida (`licença`). "
            "Área no disco não é concessão."
        )
    located = provenance_location_scope()
    if located:
        scope += located
    return scope


# O release já recusa que localização
# atribua autoria. Sem isto a área
# localizava o CREDITS e calava a
# recusa. Localização no disco não é
# o titular.
RELEASE_LOCATION = re.compile(r"localização não atribui autoria")


def release_refuses_location_as_authorship(text):
    return bool(text and RELEASE_LOCATION.search(text))


def provenance_location_source():
    path = FRAMEWORK / "commands" / "release.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if release_refuses_location_as_authorship(text):
        return "commands/release.md"
    return None


def provenance_location_scope():
    if not provenance_location_source():
        return ""
    return (
        " O disco recusa que localização atribua autoria (`localização`). "
        "Localização no disco não é o titular."
    )


# O roteiro já recusa prescrever quantas pessoas. Sem isto a
# área localizava o QA e calava a recusa.
# Área no disco não é censo.
QUALITY_PEOPLE = re.compile(r"não prescreve quantas pessoas")


def quality_refuses_people_count(text):
    return bool(text and QUALITY_PEOPLE.search(text))


def qa_people_source():
    path = FRAMEWORK / "references/quality.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if quality_refuses_people_count(text):
        return "references/quality.md"
    return None


def qa_area_scope():
    scope = (
        "Localiza o documento de QA. Não assiste a sessão e não "
        "conta jogadores."
    )
    if qa_people_source():
        scope += (
            " O disco recusa prescrever quantas pessoas (`pessoas`). "
            "Área no disco não é censo."
        )
    named = qa_tenth_scope()
    if named:
        scope += named
    return scope


# A guia já recusa que o checklist
# seja uma décima área. Sem isto a
# área localizava o QA e calava a
# recusa. Área no disco não é o
# inventário.
CHECKLIST_TENTH = re.compile(r"não uma décima área")


def guide_refuses_checklist_as_tenth_area(text):
    return bool(text and CHECKLIST_TENTH.search(text))


def qa_tenth_source():
    path = FRAMEWORK / "references/aaa-checklist.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_checklist_as_tenth_area(text):
        return "references/aaa-checklist.md"
    return None


def qa_tenth_scope():
    if not qa_tenth_source():
        return None
    return (
        " O disco recusa que o checklist seja uma décima área "
        "(`décima`). Área no disco não é o inventário."
    )


# A receita já recusa telemetria como padrão silencioso. Sem
# isto a área localizava o runbook e calava a recusa.
# Área no disco não é consentimento.
RELEASE_RECIPE = FRAMEWORK / "recipes/release.md"
RELEASE_TELEMETRY = re.compile(r"telemetria não é padrão silencioso")


def recipe_refuses_silent_telemetry(text):
    return bool(text and RELEASE_TELEMETRY.search(text))


def runbook_telemetry_source():
    path = RELEASE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_silent_telemetry(text):
        return "recipes/release.md"
    return None


def runbook_area_scope():
    scope = (
        "Localiza o documento de execução. Não executa o artefato e não "
        "abre outra máquina."
    )
    if runbook_telemetry_source():
        scope += (
            " O disco recusa que telemetria seja padrão silencioso (`telemetria`). "
            "Área no disco não é consentimento."
        )
    server = runbook_init_scope()
    if server:
        scope += server
    return scope


# O processo já recusa que servidor
# aberto conclua inicialização
# documental. Sem isto a área
# localizava o runbook e calava a
# recusa. Servidor no disco não é
# o documento.
PROCESS_SERVER = re.compile(r"Servidor aberto não conclui inicialização documental")


def process_refuses_open_server_as_documentary_init(text):
    return bool(text and PROCESS_SERVER.search(text))


def runbook_init_source():
    path = FRAMEWORK / "references" / "process.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_open_server_as_documentary_init(text):
        return "references/process.md"
    return None


def runbook_init_scope():
    if not runbook_init_source():
        return ""
    return (
        " O disco recusa que servidor aberto conclua inicialização "
        "documental (`inicialização`). Servidor no disco não é o documento."
    )


def documentation_scope(document_minimum):
    scope = (
        "O agente executa a ação e respeita restrições atuais do usuário. "
        "O comando não escreve documentos, concede aprovação ou certifica sua suficiência."
    )
    if documentation_audit_source(document_minimum):
        scope += (
            " O disco pede documentar sem consentimento (`audit`). "
            "Roteiro no disco não é base escrita."
        )
    return scope


# O roteiro já recusa que o aviso seja uma pergunta. Sem isto a
# inicialização copiava o notice e calava a recusa.
# Aviso no disco não é espera.
AUDIT_QUESTION = re.compile(r"o aviso não é uma pergunta")


def audit_refuses_notice_as_question(text):
    return bool(text and AUDIT_QUESTION.search(text))


def documentation_initialization_question_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_refuses_notice_as_question(text):
        return "references/project-audit.md"
    return None


def documentation_initialization_scope():
    scope = (
        "Aviso e evidência da inicialização. Não pergunta e não espera "
        "resposta."
    )
    if documentation_initialization_question_source():
        scope += (
            " O disco recusa que o aviso seja uma pergunta (`pergunta`). "
            "Aviso no disco não é espera."
        )
    named = documentation_initialization_scanner_scope()
    if named:
        scope += named
    return scope


# O roteiro já recusa que o resultado
# seja inferido pelo scanner. Sem isto a
# inicialização copiava o aviso e calava
# a recusa. Sinal no disco não é o
# resultado.
AUDIT_SCANNER = re.compile(r"não é inferido pelo scanner")


def audit_refuses_result_as_scanner_inference(text):
    return bool(text and AUDIT_SCANNER.search(text))


def documentation_initialization_scanner_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_refuses_result_as_scanner_inference(text):
        return "references/project-audit.md"
    return None


def documentation_initialization_scanner_scope():
    if not documentation_initialization_scanner_source():
        return None
    return (
        " O disco recusa que o resultado seja inferido pelo scanner "
        "(`scanner`). Sinal no disco não é o resultado."
    )


# O processo já nega que documento pronto seja PoC. Sem isto o
# context apontava o arquivo e calava a recusa.
# Fonte no disco não é jogo implementado.
PROCESS_GUIDE = FRAMEWORK / "references/process.md"
PROCESS_POC = re.compile(r"Documentos prontos não significam PoC executada")


def process_denies_ready_docs_are_poc(text):
    return bool(text and PROCESS_POC.search(text))


def continuity_poc_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_denies_ready_docs_are_poc(text):
        return "references/process.md"
    return None


def continuity_scope():
    scope = (
        "Fontes são candidatos, não fila validada. "
        "O agente resolve next_step antes de responder; o comando não escolhe "
        "tarefa, infere etapa concluída nem concede autorização a partir de documentos."
    )
    if continuity_poc_source():
        scope += (
            " O disco nega que documento pronto seja PoC (`process`). "
            "Fonte no disco não é jogo implementado."
        )
    return scope


# O processo já recusa que sources_found comprove a fila.
# Sem isto a fonte copiava o caminho e calava a recusa.
# Fonte no disco não é backlog.
CONTINUITY_QUEUE = re.compile(r"`sources_found`\s+não\s+comprova\s+fila\s+atual")


def process_refuses_found_as_queue(text):
    return bool(text and CONTINUITY_QUEUE.search(text))


def continuity_source_queue_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_found_as_queue(text):
        return "references/process.md"
    return None


def continuity_source_scope():
    scope = (
        "Caminho, linha, estado e base da fonte candidata. Não resolve "
        "a fila e não executa o passo."
    )
    if continuity_source_queue_source():
        scope += (
            " O disco recusa que sources_found comprove fila (`fila`). "
            "Fonte no disco não é backlog."
        )
    draft = continuity_source_step_scope()
    if draft:
        scope += draft
    return scope


# O next já recusa que fonte em rascunho
# seja passo. Sem isto a fonte copiava o
# caminho e calava a recusa.
# Rascunho no disco não é o passo.
NEXT_DRAFT_STEP = re.compile(r"fonte em rascunho não é passo")


def next_refuses_draft_source_as_step(text):
    return bool(text and NEXT_DRAFT_STEP.search(text))


def continuity_source_step_source():
    path = FRAMEWORK / "commands" / "next.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if next_refuses_draft_source_as_step(text):
        return "commands/next.md"
    return None


def continuity_source_step_scope():
    if not continuity_source_step_source():
        return ""
    return (
        " O disco recusa que fonte em rascunho seja passo (`passo`). "
        "Rascunho no disco não é o passo."
    )


# O gauntlet já recusa que o arquivo de prompts seja a fonte de status.
# Sem isto o prompt copiava a política e calava a recusa.
# Prompt no disco não é o estado.
GAUNTLET_GUIDE = FRAMEWORK / "references/gauntlet.md"
GAUNTLET_RECIPE = re.compile(r"permanece uma receita;\s+não é a fonte de status")


def gauntlet_refuses_prompt_as_status(text):
    return bool(text and GAUNTLET_RECIPE.search(text))


def continuity_prompt_recipe_source():
    path = GAUNTLET_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gauntlet_refuses_prompt_as_status(text):
        return "references/gauntlet.md"
    return None


def continuity_prompt_scope():
    scope = (
        "Política e prontidão do prompt de continuidade. Não inicia "
        "relógio e não registra o estado."
    )
    if continuity_prompt_recipe_source():
        scope += (
            " O disco recusa que o arquivo de prompts seja a fonte de "
            "status (`receita`). Prompt no disco não é o estado."
        )
    if continuity_prompt_readiness_source():
        scope += (
            " O disco recusa que arquivos encontrados comprovem prontidão "
            "(`prontidão`). Arquivo no disco não é o recorte."
        )
    named = continuity_prompt_pocs_scope()
    if named:
        scope += named
    return scope


# O roteiro já recusa que uma lista de
# PoCs baste. Sem isto o prompt copiava
# a prontidão e calava a recusa. Lista
# no disco não é o prompt.
AUDIT_POCS = re.compile(r"lista de PoCs não basta")


def audit_refuses_poc_list_as_next_task(text):
    return bool(text and AUDIT_POCS.search(text))


def continuity_prompt_pocs_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_refuses_poc_list_as_next_task(text):
        return "references/project-audit.md"
    return None


def continuity_prompt_pocs_scope():
    if not continuity_prompt_pocs_source():
        return None
    return (
        " O disco recusa que uma lista de PoCs baste "
        "(`pocs`). Lista no disco não é o prompt."
    )


# O processo já recusa que arquivos encontrados comprovem prontidão.
# Sem isto o prompt copiava readiness e calava a recusa.
# Arquivo no disco não é o recorte.
PROCESS_READY = re.compile(r"não comprovam prontidão")


def process_refuses_found_as_readiness(text):
    return bool(text and PROCESS_READY.search(text))


def continuity_prompt_readiness_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_found_as_readiness(text):
        return "references/process.md"
    return None


# A guia já recusa preencher o checklist. Sem isto o
# context apontava o arquivo e calava a recusa.
# Guia no disco não é observação.
FINISH_GUIDE = FRAMEWORK / "references/aaa-checklist.md"
FINISH_FILL = re.compile(r"O harness não preenche o checklist")


def finish_guide_refuses_fill(text):
    return bool(text and FINISH_FILL.search(text))


def finish_checklist_source():
    path = FINISH_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if finish_guide_refuses_fill(text):
        return "references/aaa-checklist.md"
    return None


def finish_scope():
    scope = (
        "Núcleo em qualquer escala após um ciclo jogável. "
        "Produto/AA soma product_groups. Promessa só se o brief prometeu. "
        "Mercado (CHK-16) nunca reprova jam. Completar o template não certifica. "
        "O comando não observa o jogo."
    )
    if finish_checklist_source():
        scope += (
            " O disco recusa preencher o checklist (`checklist`). "
            "Guia no disco não é observação."
        )
    named = finish_grade_scope()
    if named:
        scope += named
    return scope


# A ambição já recusa que o
# checklist completo seja nota AAA.
# Sem isto o finish apontava a guia
# e calava a recusa. Guia no disco
# não é observação.
AMBITION_GRADE = re.compile(r"Completar o checklist não é nota AAA")


def ambition_refuses_checklist_as_aaa_grade(text):
    return bool(text and AMBITION_GRADE.search(text))


def finish_grade_source():
    path = AMBITION_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if ambition_refuses_checklist_as_aaa_grade(text):
        return "references/ambition.md"
    return None


def finish_grade_scope():
    if not finish_grade_source():
        return None
    return (
        " O disco recusa que o checklist completo seja nota AAA "
        "(`grau`). Guia no disco não é observação."
    )


# O processo já recusa que a etapa certifique o progresso. Sem isto o
# context selecionava o recorte e calava a recusa.
# Contexto no disco não é degrau.
PROCESS_PROGRESS = re.compile(r"não certifica progresso")


def process_refuses_stage_progress(text):
    return bool(text and PROCESS_PROGRESS.search(text))


def context_progress_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_stage_progress(text):
        return "references/process.md"
    return None


def context_scope():
    scope = (
        "Seleciona leituras do framework para o foco e a etapa. "
        "Não executa o jogo e não escreve documentos."
    )
    if context_progress_source():
        scope += (
            " O disco recusa que a etapa certifique o progresso (`progresso`). "
            "Contexto no disco não é degrau."
        )
    named = context_event_scope()
    if named:
        scope += named
    return scope


# O roteiro já recusa que o evento
# seja inferido do nome de um arquivo.
# Sem isto o context copiava o evento
# e calava a recusa. Arquivo no disco
# não é a conversa.
AUDIT_EVENT = re.compile(r"não é inferido do")


def audit_refuses_filename_as_event(text):
    return bool(text and AUDIT_EVENT.search(text))


def context_event_source():
    path = AUDIT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if audit_refuses_filename_as_event(text):
        return "references/project-audit.md"
    return None


def context_event_scope():
    if not context_event_source():
        return None
    return (
        " O disco recusa que o evento seja inferido do nome de um arquivo "
        "(`inferido`). Arquivo no disco não é a conversa."
    )


# A guia já recusa que a checagem seja validador semântico.
# Sem isto o issue copiava o parse e calava a recusa.
# Parse no disco não é o jogo.
PREPRODUCTION_SEMANTIC = re.compile(r"não é validador semântico de\s+PRD/GDD")


def guide_refuses_semantic_validator(text):
    return bool(text and PREPRODUCTION_SEMANTIC.search(text))


def metadata_issue_semantic_source():
    path = FRAMEWORK / "references/preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_semantic_validator(text):
        return "references/preproduction.md"
    return None


def metadata_issue_scope():
    scope = (
        "Caminho e motivo do manifesto ilegível. Não valida o "
        "desenho e não executa o jogo."
    )
    if metadata_issue_semantic_source():
        scope += (
            " O disco recusa que a checagem seja validador semântico (`semântico`). "
            "Parse no disco não é o jogo."
        )
    return scope


def workspace_module(project, root=None):
    """Locate an optional workspace module without treating an empty checkout as a new game."""
    project = Path(project).resolve()
    if root is None:
        root = next((parent for parent in (project, *project.parents)
                     if (parent / "workspace.json").is_file()), default_root())
    root = Path(root).resolve()
    if not (root / "workspace.json").is_file():
        return None
    manifest = workspace.load_manifest(root, resolve_urls=False)
    for module in manifest["modules"]:
        relative = PurePosixPath(module["path"])
        target = (root / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not target.is_relative_to(root):
            raise ValueError("Módulo fora do workspace")
        if target == project:
            return {
                "id": module["id"], "path": module["path"],
                "state": "present" if (target / ".git").exists() else "not_downloaded",
                "get_command": shlex.join(["python3", str(FRAMEWORK / "scripts/workspace.py"),
                                            "--root", str(root), "get", module["id"]]),
            }
    return None


# A ligação já recusa preencher pasta não baixada com o starter.
# Sem isto o context copiava o estado e calava a recusa.
# Módulo no disco não é o jogo.
WORKSPACE_GUIDE = FRAMEWORK / "references/workspace-binding.md"
WORKSPACE_FILL = re.compile(r"não é preenchida pelo\s+starter")
WORKSPACE_INVENTED = re.compile(r"seu conteúdo não é inventado")


def binding_refuses_starter_fill(text):
    return bool(text and WORKSPACE_FILL.search(text))


def workspace_module_fill_source():
    path = WORKSPACE_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if binding_refuses_starter_fill(text):
        return "references/workspace-binding.md"
    return None


def workspace_module_scope():
    scope = (
        "Id, caminho e estado do módulo opcional. Não baixa e não "
        "cria a pasta."
    )
    if workspace_module_fill_source():
        scope += (
            " O disco recusa preencher pasta não baixada com o starter "
            "(`preenchida`). Módulo no disco não é o jogo."
        )
    return scope


def binding_refuses_invented_content(text):
    return bool(text and WORKSPACE_INVENTED.search(text))


def workspace_profile_invented_source():
    path = WORKSPACE_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if binding_refuses_invented_content(text):
        return "references/workspace-binding.md"
    return None


def workspace_profile_scope():
    scope = (
        "Arquivos locais de personalização encontrados ou ausentes. "
        "Não inventa o texto e não cria a referência."
    )
    if workspace_profile_invented_source():
        scope += (
            " O disco recusa inventar o conteúdo da referência ausente "
            "(`inventado`). Lacuna no disco não é a regra."
        )
    return scope


# A entrega já recusa que templates preenchidos comprovem regras.
# Sem isto o delivery_review copiava os critérios e calava a recusa.
# Critério no disco não é a entrega.
DELIVERY_GUIDE = FRAMEWORK / "references/delivery.md"
DELIVERY_RULES = re.compile(r"templates preenchidos não comprovam regras")


def delivery_refuses_filled_templates(text):
    return bool(text and DELIVERY_RULES.search(text))


def delivery_rules_source():
    path = DELIVERY_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if delivery_refuses_filled_templates(text):
        return "references/delivery.md"
    return None


def delivery_review_scope():
    scope = (
        "Critérios da conferência do pedido. Não lê a conversa e não "
        "certifica a entrega."
    )
    if delivery_rules_source():
        scope += (
            " O disco recusa que templates preenchidos comprovem regras "
            "(`regras`). Critério no disco não é a entrega."
        )
    return scope


def workspace_profile(root):
    """Read local context references; all reusable rules remain in this repository."""
    root = Path(root).resolve()
    config = root / "framework/config.json"
    result = {"root": str(root), "config": None, "context_files": [], "missing": []}
    if not config.is_file():
        return result
    data = workspace.load_config(root)
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


def context(project, focus, stage=None, studies_root=None, event="task", root=None, genre=None, scale=None):
    if focus not in FOCI:
        raise ValueError("foco desconhecido")
    if genre is not None and genre not in GENRES:
        raise ValueError("gênero desconhecido")
    if scale is not None and scale not in SCALES:
        raise ValueError("escala desconhecida")
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
        metadata_issues.append({
            "path": "package.json",
            "reason": str(error),
            "scope": metadata_issue_scope(),
        })
    instructions = instruction_files(project)
    foundation = scan(project)
    module = workspace_module(project, root)
    if module is not None:
        module = dict(module, scope=workspace_module_scope())
    module_pending = module is not None and module["state"] == "not_downloaded"
    if module_pending:
        foundation["audit"]["required"] = False
        foundation["audit"]["deferred_reason"] = "workspace_module_not_downloaded"
    records = [str(project / relative) for relative in foundation["read_first"]]
    deferred = bool(foundation["audit"].get("deferred"))
    initializing = event == "initialize"
    document_minimum = audit_required_flag(foundation["audit"]) or event in ("direction-approved", "initialize") or stage == "audit"
    kind = identify(project)
    packs = select_packs(kind, genre, foundation["genre_mentions"])
    references = [str(path) for path in select_references(focus, stage, document_minimum)]
    recipe = str(FRAMEWORK / f"recipes/{focus}.md")
    for pack in (packs["genre"]["pack"], packs["platform"]["pack"]):  # inserção reversa: receita → plataforma → gênero
        if pack:
            references.insert(references.index(recipe) + 1 if recipe in references else len(references), pack)
    references = list(dict.fromkeys(references))
    profile = workspace_profile(root if root is not None else default_root())
    profile = dict(profile, scope=workspace_profile_scope())
    references.extend(path for path in profile["context_files"] if path not in references)
    if initializing and str(FRAMEWORK / "recipes/architecture.md") not in references:
        references.append(str(FRAMEWORK / "recipes/architecture.md"))
    studies = studies_for(focus, STUDIES_ROOT if studies_root is None else studies_root)
    source_scope = continuity_source_scope()
    return {
        "schema_version": 3, "project": str(project), "exists": project.is_dir(), "kind": kind,
        "workspace_module": module,
        "workspace": profile,
        "focus": focus, "stage": stage, "event": event, "instructions": instructions, "records": records,
        "scale": read_scale(foundation["scale_mentions"], scale),
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
            "scope": delivery_review_scope(),
        },
        "production_bar": production_bar(focus, stage, project),
        "continuity": {
            "status": "sources_found" if foundation["continuity_sources"] else "not_located",
            "sources": [
                dict(item, path=str(project / item["path"]), scope=source_scope)
                for item in foundation["continuity_sources"]
            ],
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
                "scope": continuity_prompt_scope(),
            },
            "guide": str(FRAMEWORK / "references/process.md") + "#continuidade-e-retomada",
            "before_close": "Atualizar o registro canônico e dizer onde chegamos, uma próxima ação concreta, por que vem primeiro e qual evidência a conclui. Quando esse recorte estiver definido, gerar e apresentar automaticamente seu prompt de continuidade pronto para copiar; sem jargão, variáveis ou pedido de horas. Continuar trabalho já autorizado. Se o objetivo terminou, declarar conclusão sem inventar trabalho.",
            "on_resume": "Ler o registro e a conversa, conferir o estado real, resolver a próxima ação e executá-la dentro do escopo autorizado. Não repetir briefing, auditoria já válida ou pergunta genérica de permissão.",
            "scope": continuity_scope(),
        },
        "documentation": {
            "action": (
                "obtain_workspace_module" if module_pending
                else "audit_and_document" if initializing
                else "document_minimum" if document_minimum
                else "defer_until_playable_cycle" if deferred
                else "maintain_affected_documents"
            ),
            "executed": False,
            "on_initialize": "Iniciar/inicializar o projeto, sem alvo operacional explícito, pede análise profunda e documentação: use --event initialize. Iniciar servidor, partida ou uma fase já definida segue esse alvo e a conversa; não decidir só pelo verbo.",
            "initialization": {
                "status": "pending_agent_audit",
                "notice": f"Vou iniciar a análise de {project.name}: levantar a implementação disponível, confrontar os documentos e organizar a base e o próximo passo com evidências.",
                "required_evidence": ["source_traces_and_consumers", "canonical_documents_or_explicit_gaps", "prioritized_findings", "next_action_with_ready_prompt_or_actual_blocker"],
                "not_sufficient": ["server_running", "http_ok", "tests_passed", "documents_found"],
                "guide": str(FRAMEWORK / "references/project-audit.md") + "#inicializar-o-projeto",
                "runtime_role": "Observar o jogo pode apoiar o diagnóstico; abrir navegador ou servidor não é a entrega da inicialização. Não alterar gameplay apenas por esse pedido.",
                "scope": documentation_initialization_scope(),
            } if initializing else None,
            "on_direction_approved": "Aprovação na conversa exige sincronizar a base mínima neste turno, mesmo com todos os candidatos encontrados; use --event direction-approved.",
            "before_close": "Registrar conteúdo e fontes nos documentos canônicos; cobrir cada área mínima com decisão/fato ou lacuna e próxima ação. Referência salva e templates vazios não concluem a documentação.",
            "scope": documentation_scope(document_minimum),
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
            "scope": finish_scope(),
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
            "Áudio novo: se shared/sfx tiver sons, busque (`sfx search`) antes de baixar. Sem acervo, o starter já fala em public/sfx; sfx search nomeia o stem que casa, sfx info lê a chave e nomeia o stem que o recibo lista e o disco perdeu, roles --fill nomeia o mesmo stem, roles --apply e sfx copy levam bytes e créditos, sfx verify nomeia os stems sem cruzar o que não existe, nomeia o stem que o recibo lista e o disco perdeu e sfx serve recusa. Com sons, sfx serve abre a página de escuta — se ui/ faltar, o harness gera a lista — e sfx verify nomeia o som que o catálogo lista e o disco perdeu. Tocar nessa página não é mix ouvida. Crescer o acervo é `sfx import ARQUIVO --metadata JSON` (ffmpeg); `sfx info` lê a ficha do acervo ou a chave do stem — o recibo que lista um stem e o disco perdeu não é id desconhecido; se o inspect já mediu o pico, o sfx info nomeia o pico que o inspect já mede — e `sfx export ID --to PASTA` copia bytes e créditos do acervo ou do stem e nomeia o stem que o recibo lista e o disco perdeu; exportar não inventa bytes. Importar e exportar não é ouvir. Piso de gravação licenciada; 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão.",
            "Direção sonora é do projeto; restrições locais estão em studio_assets.sfx.policy. Origem e licença continuam obrigatórias.",
            "Feel e áudio são focos próprios (`--focus feel`, `--focus audio`). Sem observação em movimento, experience_status permanece not_assessed; scaffold não é vertical slice.",
            "“AAA” neste harness é piso de acabamento da slice, não tier de publisher. Sem feel sincronizado, pacing e repeatability, não use o adjetivo.",
            "Checklist: ver finish no JSON. Jam observa core_groups; produto/AA soma product_groups; promise_groups só se prometidos. `template aaa` não certifica; N/A exige motivo.",
        ],
        "scope": context_scope(),
    }




def template(stage, project, output=None):
    if stage not in STAGES:
        raise ValueError("etapa desconhecida")
    if stage == "agents":
        text = agents_template_text(project)
    else:
        text = (FRAMEWORK / f"assets/templates/{stage}.md").read_text(encoding="utf-8")
        text = text.replace("{{PROJECT}}", project.name).replace("{{PROJECT_PATH}}", str(project))
    if output is not None:
        if output.exists() or output.is_symlink():
            raise ValueError("documento existente; adapte a fonte canônica sem sobrescrever")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as document:
            document.write(text)
    return text


# O molde já recusa publicar. Sem isto o
# template emitia rascunho e calava a recusa.
# Molde no disco não é autorização.
TEMPLATE_PUBLISH = re.compile(
    r"não autoriza publicar|não concedida neste template",
    re.IGNORECASE,
)


def template_refuses_publish(text):
    return bool(text and TEMPLATE_PUBLISH.search(text))


def template_refusal_source(stage):
    if stage == "agents" or stage not in STAGES:
        return None
    path = FRAMEWORK / f"assets/templates/{stage}.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if template_refuses_publish(text):
        return f"assets/templates/{stage}.md"
    return None


def template_scope(stage):
    scope = "Template inicial; decisões, revisão e prova continuam pendentes."
    if template_refusal_source(stage):
        scope += (
            " O disco recusa a publicação (`publicar`). "
            "Molde no disco não é autorização."
        )
    if stage == "mvp" and template_mvp_value_source():
        scope += (
            " O disco recusa que o MVP prove a hipótese de valor "
            "(`valor`). Molde no disco não é validação."
        )
    if stage == "vertical-slice" and template_slice_finish_source():
        scope += (
            " O disco recusa que placeholders certifiquem o acabamento "
            "(`acabamento`). Molde no disco não é a fatia."
        )
    named = template_parallel_scope(stage)
    if named:
        scope += named
    return scope


# A guia já recusa que o checklist
# seja um ciclo paralelo. Sem isto o
# template emitia o rascunho e calava
# a recusa. Guia no disco não é o molde.
CHECKLIST_PARALLEL = re.compile(r"não é um ciclo paralelo")


def guide_refuses_checklist_as_parallel_cycle(text):
    return bool(text and CHECKLIST_PARALLEL.search(text))


def template_parallel_source(stage):
    if stage != "aaa":
        return None
    path = FINISH_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if guide_refuses_checklist_as_parallel_cycle(text):
        return "references/aaa-checklist.md"
    return None


def template_parallel_scope(stage):
    if not template_parallel_source(stage):
        return None
    return (
        " O disco recusa que o checklist seja um ciclo paralelo "
        "(`paralelo`). Guia no disco não é o molde."
    )


# A guia já recusa que o MVP prove a hipótese de valor.
# Sem isto o template emitia o rascunho e calava a recusa.
# Molde no disco não é validação.
PREPRODUCTION_VALUE = FRAMEWORK / "references/preproduction.md"
MVP_VALUE = re.compile(r"não prova que sua hipótese de valor")


def preproduction_refuses_mvp_value(text):
    return bool(text and MVP_VALUE.search(text))


def template_mvp_value_source():
    path = PREPRODUCTION_VALUE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if preproduction_refuses_mvp_value(text):
        return "references/preproduction.md"
    return None


# A guia já recusa que placeholders certifiquem o acabamento da slice.
# Sem isto o template emitia o rascunho e calava a recusa.
# Molde no disco não é a fatia.
SLICE_FINISH = re.compile(r"não certificam o acabamento")


def preproduction_refuses_placeholder_finish(text):
    return bool(text and SLICE_FINISH.search(text))


def template_slice_finish_source():
    path = PREPRODUCTION_VALUE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if preproduction_refuses_placeholder_finish(text):
        return "references/preproduction.md"
    return None


# O gauntlet já recusa que horas nulas sejam prazo infinito.
# Sem isto o contrato copiava budget_hours e calava a recusa.
# Contrato no disco não é o orçamento.
GAUNTLET_INFINITE = re.compile(r"não significa prazo infinito")


def gauntlet_refuses_null_as_infinite(text):
    return bool(text and GAUNTLET_INFINITE.search(text))


def gauntlet_contract_infinite_source():
    path = GAUNTLET_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gauntlet_refuses_null_as_infinite(text):
        return "references/gauntlet.md"
    return None


def gauntlet_contract_scope():
    scope = (
        "Contrato do pacote de continuidade. Não inicia execução e "
        "não inventa orçamento."
    )
    if gauntlet_contract_infinite_source():
        scope += (
            " O disco recusa que horas nulas sejam prazo infinito "
            "(`infinito`). Contrato no disco não é o orçamento."
        )
    if gauntlet_contract_independence_source():
        scope += (
            " O disco recusa que papéis simulados comprovem independência "
            "(`independência`). Papel no disco não é crítico isolado."
        )
    return scope


# O gauntlet já recusa que papéis simulados comprovem independência.
# Sem isto o contrato copiava o objetivo e calava a recusa.
# Papel no disco não é crítico isolado.
GAUNTLET_INDEPENDENCE = re.compile(r"não comprovam independência")


def gauntlet_refuses_roles_as_independent(text):
    return bool(text and GAUNTLET_INDEPENDENCE.search(text))


def gauntlet_contract_independence_source():
    path = GAUNTLET_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if gauntlet_refuses_roles_as_independent(text):
        return "references/gauntlet.md"
    return None


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
        "scope": gauntlet_contract_scope(),
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


PACKAGE_INSTALL_KEYS = ("dependencies", "devDependencies", "optionalDependencies")


def package_has_dependencies(project):
    # O start nomeava npm install no starter sem
    # dependências. O README já recusava o passo.
    # Lista vazia não é o que instalar. Nomear não instala.
    package = Path(project) / "package.json"
    if not package.is_file() or package.is_symlink():
        return False
    try:
        data = json.loads(package.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError):
        return False
    if not isinstance(data, dict):
        return False
    for key in PACKAGE_INSTALL_KEYS:
        value = data.get(key)
        if isinstance(value, dict) and value:
            return True
    return False


def install_command(project, play=None):
    # O play pede npm. Sem isto o start mandava o serve
    # e o disco ainda não tinha módulos. Sem dependências
    # o passo some — o starter não tem o que instalar.
    # Nomear não instala.
    if not isinstance(play, str) or not re.search(r"\bnpm\b", play):
        return None
    root = Path(project)
    package = root / "package.json"
    modules = root / "node_modules"
    if not package.is_file() or package.is_symlink():
        return None
    if not package_has_dependencies(root):
        return None
    if modules.is_dir() and not modules.is_symlink():
        return None
    return f"cd {shlex.quote(str(root))} && npm install"


# A superfície pedida, não a que o sistema abriu. PORT=0 e listen
# dinâmico continuam no banner do serve. Nomear não serve.
DEFAULT_SERVE_PORT = 8080


def default_serve_port(env=None):
    env = os.environ if env is None else env
    raw = env.get("PORT")
    if raw in (None, ""):
        return DEFAULT_SERVE_PORT
    try:
        port = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_SERVE_PORT
    if port <= 0:
        return None
    return port


def serve_script_name(scripts=None, play=None):
    names = play_script_names(scripts or {})
    if names:
        return names[0]
    if isinstance(play, str) and re.search(r"\bserve\b", play):
        return "serve"
    return None


def serve_url(scripts=None, play=None, env=None):
    name = serve_script_name(scripts, play)
    if name is None:
        return None
    if name != "serve" and not name.startswith("serve:") and not name.startswith("serve-"):
        return None
    port = default_serve_port(env)
    if port is None:
        return None
    return f"http://localhost:{port}/"


# O prompt pedia Abrir sempre. O serve do starter já
# tenta no terminal. Pedir de novo é cargo-cult.
# Nomear não abre e não serve.
SERVE_OPEN_FILES = ("tools/serve.mjs", "tools/serve.js")
SERVE_OPEN_MARK = ("shouldOpenBrowser", "xdg-open")


def serve_opens_browser(project):
    root = Path(project)
    if not root.is_dir() or root.is_symlink():
        return False
    for relative in SERVE_OPEN_FILES:
        path = root / relative
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 64000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if any(mark in text for mark in SERVE_OPEN_MARK):
            return True
    return False


def cycle_opens_browser(project=None, starter=None):
    if project is not None:
        return serve_opens_browser(project)
    if nonempty(starter):
        return serve_opens_browser(STARTERS_ROOT / starter)
    return False


def browser_surface(url, opens=False):
    if not url:
        return ""
    if opens:
        return (
            f"No terminal o serve tenta abrir o navegador. "
            f"Se não abrir, o endereço é {url} — file:// não carrega. "
        )
    return f"Abra {url} no navegador — file:// não carrega. "


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


def playtest_command(project):
    return harness_command("playtest", project)


def playtest_line(playtest):
    if not playtest:
        return ""
    return f"O achado: {playtest}. Só lê. Sem os quatro não é achado. "


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
    href = seed_href(project)
    if href:
        then["seed"] = href
        then["invite"] = invite_href(project)
    install = install_command(project, play)
    if install:
        then["install"] = install
    return then


# O roteiro já recusa que o mural seja onboarding. Sem isto o
# passo de jogar copiava o verbo e calava a recusa.
# Texto no disco não é a primeira ação.
QUALITY_ONBOARDING = re.compile(r"bloqueia o jogo não é onboarding")


def quality_refuses_mural_onboarding(text):
    return bool(text and QUALITY_ONBOARDING.search(text))


def play_step_onboarding_source():
    path = QUALITY_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if quality_refuses_mural_onboarding(text):
        return "references/quality.md"
    return None


def play_step_scope():
    scope = (
        "Jogar no próprio dispositivo. Não executa o serve e não observa."
    )
    if play_step_onboarding_source():
        scope += (
            " O disco recusa que o mural seja onboarding (`onboarding`). "
            "Texto no disco não é a primeira ação."
        )
    return scope


# A receita já recusa que o screenshot comprove feel. Sem isto o
# passo de gravar copiava o note e calava a recusa.
# Recibo no disco não é peso percebido.
FEEL_SCREENSHOT = re.compile(r"Screenshot não comprova feel")


def feel_refuses_screenshot(text):
    return bool(text and FEEL_SCREENSHOT.search(text))


def note_step_screenshot_source():
    path = FRAMEWORK / "recipes/feel.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if feel_refuses_screenshot(text):
        return "recipes/feel.md"
    return None


def note_step_scope():
    scope = (
        "Gravar o que o verbo sentiu. Não executa o note e não observa."
    )
    if note_step_screenshot_source():
        scope += (
            " O disco recusa que o screenshot comprove feel (`screenshot`). "
            "Recibo no disco não é peso percebido."
        )
    return scope


# O processo já recusa que o comando abra o jogo. Sem isto o
# passo de abrir copiava o start e calava a recusa.
# Nome no disco não é partida.
PROCESS_OPEN = re.compile(r"Nomear o comando não abre")


def process_refuses_open(text):
    return bool(text and PROCESS_OPEN.search(text))


def open_step_source():
    path = FRAMEWORK / "references/process.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_open(text):
        return "references/process.md"
    return None


def open_step_scope():
    scope = (
        "Abrir o ciclo. Não executa o start e não observa."
    )
    if open_step_source():
        scope += (
            " O disco recusa que o comando abra o jogo (`abertura`). "
            "Nome no disco não é partida."
        )
    return scope


def cycle_steps(start_command, play_cmd, then, cycle, nxt=None, exists=False, url=None):
    play_step = {
        "n": 2,
        "do": "jogar no próprio dispositivo",
        "command": play_cmd,
        "kind": nxt["proposal"]["basis"] if nxt else "playable.unplayed",
        "executed": False,
        "scope": play_step_scope(),
    }
    if url:
        play_step["url"] = url
    if cycle:
        play_step["verb"] = cycle["verb"]
        play_step["controls"] = {
            key: cycle[key]
            for key in CYCLE_KEYS
            if key != "verb" and key in cycle
        }
    return [
        {
            "n": 1,
            "do": "abrir o ciclo",
            "command": start_command,
            "done": exists,
            "scope": open_step_scope(),
        },
        play_step,
        {
            "n": 3,
            "do": "gravar o que o verbo sentiu",
            "command": then["note"],
            "executed": False,
            "scope": note_step_scope(),
        },
    ]


def cycle_prompt(play, then, cycle, noted=False, url=None, runtime=None, fantasy=None, opens=False, playtest=None):
    hole = runtime_line(runtime)
    simulated = session_line(then)
    if not play:
        return (
            hole
            + simulated
            + "Sem comando de abrir: identifique o entrypoint e rode `next`. "
            "O harness não executa o jogo."
        )
    seed_line = (
        f"A última partida no disco abre em {then['seed']}. Seed explícita ignora o hold."
        if then.get("seed")
        else ""
    )
    invite_line = (
        f"O convite desta partida abre em {then['invite']}. Nomear o endereço não observa."
        if then.get("invite")
        else ""
    )
    found = playtest_line(playtest)
    craft = [key for key in CRAFT_EXAMPLES if then.get(key)]
    if noted and craft:
        parts = ["O ciclo já tem um recibo."]
        for key in craft:
            parts.append(f"{CRAFT_LABELS[key]}: {then[key]}.")
        if seed_line:
            parts.append(seed_line)
        if invite_line:
            parts.append(invite_line)
        if found:
            parts.append(found.strip())
        parts.append("O harness não pinta, não chove e não ouve.")
        parts.append(f"`next` só se você não sabe o que falta: {then['lost']}.")
        return hole + " ".join(parts)
    how = cycle_line(cycle, fantasy)
    extra = " ".join(part for part in (seed_line, invite_line) if part)
    surface = browser_surface(url, opens)
    modules = (
        f"As dependências ainda não estão no disco. Cole e rode: {then['install']}. "
        if then.get("install")
        else ""
    )
    return (
        hole
        + modules
        + f"O jogo não foi aberto. Cole e rode: {play}. "
        + simulated
        + surface
        + (f"{how} " if how else "")
        + (f"{extra} " if extra else "")
        + f"Depois de uma partida, a página grava o recibo se você escrever; no harness: {then['note']}. "
        + found
        + "`next` só se o ciclo já correu e você não sabe o que falta."
    )


def guide_prompt(exists, start_command, play, then, cycle, noted=False, url=None, runtime=None, fantasy=None, opens=False, playtest=None):
    if exists:
        return cycle_prompt(play, then, cycle, noted, url, runtime, fantasy, opens, playtest)
    hole = runtime_line(runtime)
    simulated = session_line(then)
    surface = browser_surface(url, opens)
    how = cycle_line(cycle, fantasy)
    return (
        hole
        + f"O ciclo ainda não existe. Cole e rode: {start_command}. "
        f"Depois, no próprio dispositivo: {play}. "
        + simulated
        + surface
        + (f"{how} " if how else "")
        + f"Depois de uma partida, a página grava o recibo se você escrever; no harness: {then['note']}. "
        + playtest_line(playtest)
        + "O harness não cria a pasta, não abre o jogo e não joga."
    )


def fresh_starter_cycle(project, missing, play):
    # Dois jeitos de nascer jogável: o `init` planta os seis rascunhos do
    # ciclo (e some as lacunas) ou o `start` não planta nenhum. Exigir os
    # seis só para o `next` dizer "não os preencha" era o atrito. Qualquer
    # rascunho já escrito — ou um dos seis sem marcador — encerra o atalho.
    if not play:
        return False
    docs = project / "docs"
    present = []
    drafted = 0
    if docs.is_dir() and not docs.is_symlink():
        for stage in FRESH_DRAFTS:
            path = docs / f"{stage}.md"
            if not path.is_file() or path.is_symlink():
                continue
            present.append(stage)
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                return False
            if not DRAFT_MARKERS.search(text):
                return False
            drafted += 1
    if not present:
        return True
    if missing:
        return False
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


def surface_fantasy(phrase):
    if not nonempty(phrase):
        return None
    text = phrase.strip()
    if len(text) <= SURFACE_IDEA_LIMIT:
        return text
    return f"{text[: SURFACE_IDEA_LIMIT - 3].rstrip()}..."


def read_copy_fantasy(project):
    path = Path(project) / "data/copy.json"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    return surface_fantasy(data.get("fantasy"))


def resolve_fantasy(idea=None, project=None):
    if nonempty(idea):
        return surface_fantasy(idea)
    if project is not None:
        return read_copy_fantasy(project)
    return None


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
    surface = surface_fantasy(phrase)
    if surface is None:
        return None
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


CYCLE_KEYS = ("verb", "door", "move", "dash", "bank", "hand", "touch", "pad", "look", "spawn", "mood", "seed", "speed", "invite")
# O manifesto já declara o relógio. Sem isto o
# guide lia o ciclo e calava o `speed`.
# Frase no disco não é partida observada.
CYCLE_SPEED_MARK = re.compile(r'"speed"\s*:\s*"')


def cycle_names_speed(text):
    return bool(text and CYCLE_SPEED_MARK.search(text))


def guide_speed_source(starter):
    if not nonempty(starter):
        return None
    path = STARTERS_ROOT / starter / STARTER_MANIFEST
    if not path.is_file() or path.is_symlink():
        return None
    try:
        if path.stat().st_size > 400_000:
            return None
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if cycle_names_speed(text):
        return f"assets/starters/{starter}/{STARTER_MANIFEST}"
    return None


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


# A receita já recusa que estar em run prove estar livre.
# Sem isto o ciclo anunciava o verbo e calava a recusa.
# Estado no disco não é a janela.
FEEL_FREEDOM = re.compile(r"n[aã]o prova estar livre para\s+atacar")


def recipe_refuses_run_as_free(text):
    return bool(text and FEEL_FREEDOM.search(text))


def cycle_freedom_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_run_as_free(text):
        return "recipes/feel.md"
    return None


def cycle_scope():
    scope = ""
    if cycle_freedom_source():
        scope += (
            "O disco recusa que estar em run prove estar livre para atacar (`livre`). "
            "Estado no disco não é a janela."
        )
    named = cycle_tap_scope()
    if named:
        scope += named
    hold = cycle_lock_scope()
    if hold:
        scope += hold
    fx = cycle_effects_scope()
    if fx:
        scope += fx
    press = cycle_hold_scope()
    if press:
        scope += press
    return scope or None


# A receita já recusa que o
# tap seja o avanço. Sem isto
# o ciclo anunciava o verbo e
# calava a recusa. Polegar no
# disco não é o dash.
FEEL_TAP = re.compile(r"o tap não é o avanço")


def recipe_refuses_tap_as_dash(text):
    return bool(text and FEEL_TAP.search(text))


def cycle_tap_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_tap_as_dash(text):
        return "recipes/feel.md"
    return None


def cycle_tap_scope():
    if not cycle_tap_source():
        return None
    return (
        " O disco recusa que o tap seja o avanço "
        "(`tap`). Polegar no disco não é o dash."
    )


# A receita já recusa que o lock
# seja o descanso. Sem isto o
# ciclo anunciava o verbo e
# calava a recusa. Lock no disco
# não é o descanso.
FEEL_LOCK = re.compile(r"o lock não é o descanso")


def recipe_refuses_lock_as_rest(text):
    return bool(text and FEEL_LOCK.search(text))


def cycle_lock_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_lock_as_rest(text):
        return "recipes/feel.md"
    return None


def cycle_lock_scope():
    if not cycle_lock_source():
        return None
    return (
        " O disco recusa que o lock seja o descanso "
        "(`lock`). Lock no disco não é o descanso."
    )


# A receita já recusa que três
# efeitos no impacto compensem
# input que ignora o botão. Sem
# isto o ciclo anunciava o verbo
# e calava a recusa. Efeitos no
# disco não são o input.
FEEL_EFFECTS = re.compile(
    r"Três efeitos no\s+impacto não compensam input que ignora o botão"
)


def recipe_refuses_effects_as_ignored_input(text):
    return bool(text and FEEL_EFFECTS.search(text))


def cycle_effects_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_effects_as_ignored_input(text):
        return "recipes/feel.md"
    return None


def cycle_effects_scope():
    if not cycle_effects_source():
        return None
    return (
        " O disco recusa que três efeitos no impacto compensem input que ignora o botão "
        "(`efeitos`). Efeitos no disco não são o input."
    )


# A receita já recusa que o
# segurar seja o avanço. Sem
# isto o ciclo anunciava o
# verbo e calava a recusa.
# Segurar no disco não é o
# dash.
FEEL_HOLD = re.compile(r"o aperto, não o segurar")


def recipe_refuses_hold_as_dash(text):
    return bool(text and FEEL_HOLD.search(text))


def cycle_hold_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_hold_as_dash(text):
        return "recipes/feel.md"
    return None


def cycle_hold_scope():
    if not cycle_hold_source():
        return None
    return (
        " O disco recusa que o segurar seja o avanço "
        "(`segurar`). Segurar no disco não é o dash."
    )


def named_cycle(cycle):
    if cycle is None:
        return None
    named = dict(cycle)
    scope = cycle_scope()
    if scope:
        named["scope"] = scope
    return named


def cycle_line(cycle, fantasy=None):
    parts = []
    phrase = surface_fantasy(fantasy)
    if phrase:
        parts.append(f"Fantasia: {phrase}.")
    if not cycle:
        return " ".join(parts)
    parts.append(f"Verbo: {cycle['verb']}.")
    if cycle.get("door"):
        parts.append(f"Porta: {cycle['door']}.")
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
    if cycle.get("seed"):
        parts.append(f"Seed: {cycle['seed']}.")
    if cycle.get("speed"):
        parts.append(f"Relógio: {cycle['speed']}.")
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


# Os seis rascunhos que o `start` não copia. art-bible do starter
# sozinho não conta — o start fresco já o traz e a memória não
# afirma que o ciclo foi plantado.
CYCLE_DRAFT_FILES = ("brief.md", "gdd.md", "mda.md", "tdd.md", "devlog.md", "qa.md")


def cycle_drafts_planted(project):
    docs = Path(project) / "docs"
    return any((docs / name).is_file() for name in CYCLE_DRAFT_FILES)


def project_cycle(project):
    path = Path(project) / STARTER_MANIFEST
    if not path.is_file():
        return None
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
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


def agents_template_text(project):
    # O esqueleto listava GDD. O `start` já escreve a memória
    # honesta; o `next` em not_located ainda gerava o molde.
    # Template não é rascunho do ciclo.
    destination = Path(project)
    try:
        scripts, manager = project_commands(destination)
    except (OSError, ValueError):
        scripts, manager = {}, None
    play = play_command(destination, scripts, manager)
    url = serve_url(scripts, play)
    fantasy = resolve_fantasy(project=destination) if destination.is_dir() else None
    return agents_memory_text(
        destination,
        play,
        documents=cycle_drafts_planted(destination),
        url=url,
        cycle=project_cycle(destination),
        fantasy=fantasy,
    )


def agents_memory_text(destination, play=None, starter=None, documents=False, idea=None, url=None, cycle=None, fantasy=None, opens=False):
    # O `start` não planta brief/GDD. O molde antigo listava esses
    # caminhos como canônicos — na pasta do start isso mentia. Memória
    # do agente não é rascunho do ciclo.
    destination = Path(destination)
    cycle = cycle or starter_cycle(starter) or {}
    fantasy = fantasy if fantasy is not None else resolve_fantasy(idea, destination)
    verb = cycle.get("verb") or cycle.get("door")
    lines = [
        f"# AGENTS — {destination.name}",
        "",
        f"Projeto: {destination}",
        "Status: memória do agente. Não é GDD nem rascunho do ciclo.",
        "",
        "## Executar e verificar",
        "",
    ]
    if nonempty(play):
        install = install_command(destination, play)
        if install:
            lines.append(f"- Antes de rodar: `{install}`. Nomear não instala.")
        lines.append(f"- Rodar o jogo: `{play}`.")
        if nonempty(url):
            lines.append(f"- Superfície: {url}. Nomear não serve.")
            if opens:
                lines.append("- No terminal o serve tenta abrir o navegador. Nomear não abre.")
    else:
        lines.append("- Rodar o jogo: o manifesto do projeto declara o comando.")
    lines.append(f"- De novo, sem executar: `{harness_command('play', destination)}`.")
    lines.append(f"- O que o verbo sentiu: `{note_command(destination)}`.")
    # O start já nomeava o serve e o note. Sem isto a
    # próxima sessão calava o leitor que o `next` já
    # aponta. Só lê. Sem os quatro não é achado.
    lines.append(
        f"- O achado: `{playtest_command(destination)}`. Só lê. Sem os quatro não é achado."
    )
    if destination.joinpath("package.json").is_file():
        lines.append(f"- Validadores: `cd {shlex.quote(str(destination))} && npm test`. Build verde não prova diversão.")
    lines.append("- Não publicar, não apagar saves e não rodar `python3 tools/design-sfx.py` sem `--from`.")
    lines.extend(["", "## O que este jogo já é", ""])
    if starter:
        lines.append(f"- Starter: `{starter}`. Partir dele é REUSE.")
    if nonempty(verb):
        lines.append(f"- Verbo: {verb}")
    if nonempty(cycle.get("door")) and cycle.get("door") != verb:
        lines.append(f"- Porta: {cycle['door']}")
    if nonempty(fantasy):
        lines.append(f"- Fantasia: {fantasy} — a frase não muda o verbo.")
    if documents:
        lines.append(
            "- Rascunhos do ciclo estão em `docs/` com marcador de preenchimento. "
            "Template não é decisão."
        )
    else:
        lines.append(
            "- Brief, GDD, QA e os outros rascunhos do ciclo não foram plantados. "
            "`start --docs` ou `init` os cria. Não os invente para fechar auditoria."
        )
    lines.extend([
        "",
        "## Como trabalhar",
        "",
        "- Um salto por vez. REUSE → ADAPT → CREATE. CREATE pede lacuna escrita.",
        "- Nenhum comando do harness joga, ouve ou sente o jogo no dispositivo.",
        "- Leitores de observação continuam falsos. Não chame o recorte de AAA.",
        "",
    ])
    return "\n".join(lines)


def write_agents_memory(destination, play=None, starter=None, documents=False, idea=None, url=None, cycle=None, fantasy=None, opens=False):
    path = Path(destination) / "AGENTS.md"
    if path.exists() or path.is_symlink():
        return None
    path.write_text(
        agents_memory_text(destination, play, starter, documents, idea, url, cycle, fantasy, opens),
        encoding="utf-8",
    )
    return "AGENTS.md"


def init_scope(documents, idea=None):
    # O `start` chama `init` com documents=False. Afirmar rascunhos, brief ou
    # draft_only nesse ramo mentia no JSON que o agente lê depois de criar.
    copied = (
        "Copiou o starter, trocou os valores que `starter.json` declara"
    )
    if documents:
        drafts = (
            " e criou rascunhos a partir dos templates. Escreveu AGENTS.md "
            "com o comando que abre, o note e o playtest; não é GDD. "
            "O playtest só lê. O ciclo já abre: o primeiro "
            "comando apontado é o que serve o jogo, não o que preenche os rascunhos. "
            "`open` e `url` nomeiam o mesmo serve; o `prompt` também sai em stderr. "
        )
        scan = "`scan` ainda reporta `draft_only` nas áreas sem decisão. "
        planted = (
            "`--idea` entra no brief como frase e, se houver `data/copy.json`, na "
            "abertura e no aviso do primeiro ciclo. O brief continua rascunho. "
            if nonempty(idea)
            else ""
        )
    else:
        drafts = (
            " sem plantar os rascunhos do ciclo. Escreveu AGENTS.md com o "
            "comando que abre, o note e o playtest; não é GDD nem rascunho. "
            "O playtest só lê. `start` faz o mesmo; "
            "`init` sem `--no-docs` ou `start --docs` cria os rascunhos. O ciclo "
            "já abre: o primeiro comando apontado é o que serve o jogo. "
            "`open` e `url` nomeiam o mesmo serve; o `prompt` também sai em stderr. "
        )
        scan = (
            "`scan` ainda reporta lacuna nas áreas sem candidato; "
            "`areas.not_located` não bloqueia quem já abre. "
        )
        planted = (
            "`--idea` entra na abertura se houver `data/copy.json`; o brief só nasce "
            "se os rascunhos forem plantados. "
            if nonempty(idea)
            else ""
        )
    scope = (
        copied + drafts
        + "Documento vigente que o starter já trouxe (art-bible) não é reescrito. "
        + scan + planted
        + "A frase na tela não muda o verbo. O starter é material de "
        "ADAPT, não uma engine nem uma base aprovada; o comando não executa o jogo, não instala "
        "dependências e não avalia a proposta."
    )
    if starter_module_source():
        scope += (
            " O disco declara o módulo (`type`). "
            "Tipo no disco não é runtime instalado."
        )
    named = init_references_scope()
    if named:
        scope += named
    return scope


# O processo já recusa que se copie
# runtime de referência só para
# absorver um contrato. Sem isto o
# init copiava o starter e calava a
# recusa. Runtime no disco não é o
# contrato.
PROCESS_REFERENCES = re.compile(
    r"runtime de referência só para absorver um contrato"
)


def process_refuses_reference_runtime_as_contract(text):
    return bool(text and PROCESS_REFERENCES.search(text))


def init_references_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_reference_runtime_as_contract(text):
        return "references/process.md"
    return None


def init_references_scope():
    if not init_references_source():
        return None
    return (
        " O disco recusa que se copie runtime de referência só para "
        "absorver um contrato (`referências`). Runtime no disco não é "
        "o contrato."
    )


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


# A receita já recusa que o rascunho
# plantado seja GDD. Sem isto o init
# relatava o documents e calava a
# recusa. Rascunho no disco não é
# o documento.
INIT_GDD = re.compile(r"rascunho plantado não é GDD")


def recipe_refuses_planted_draft_as_gdd(text):
    return bool(text and INIT_GDD.search(text))


def init_documents_gdd_source():
    path = FRAMEWORK / "recipes/create.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_planted_draft_as_gdd(text):
        return "recipes/create.md"
    return None


def init_documents_gdd_scope():
    if not init_documents_gdd_source():
        return None
    return (
        " O disco recusa que o rascunho plantado seja GDD "
        "(`gdd`). Rascunho no disco não é o documento."
    )


def init_documents_scope():
    scope = (
        "rascunhos escritos no destino. "
        "O init não planta GDD."
    )
    named = init_documents_gdd_scope()
    if named:
        scope += named
    return scope


def init_documents_paths(reading):
    documents = (reading or {}).get("documents") if isinstance(reading, dict) else reading
    if isinstance(documents, dict):
        return list(documents.get("documents") or [])
    return list(documents or [])


def init_documents_reading(documents):
    if not documents:
        return documents
    return {
        "documents": list(documents),
        "scope": init_documents_scope(),
    }


def init(destination, starter, title=None, documents=True, idea=None):
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
        if any(part in INIT_COPY_SKIP for part in path.relative_to(source).parts):
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
            # O starter pode trazer um documento vigente (art-bible). Sobrescrever
            # com o template apagaria a decisão e o `template` já recusa destino
            # existente — pular é o que impede o init de quebrar e de rebaixar.
            if output.exists():
                continue
            template(stage, destination, output)
            drafts.append(output.relative_to(destination).as_posix())
    planted = seed_idea(destination, idea)
    try:
        scripts, manager = project_commands(destination)
    except (OSError, ValueError):
        scripts, manager = {}, None
    play = play_command(destination, scripts, manager)
    url = serve_url(scripts)
    cycle = starter_cycle(starter)
    fantasy = resolve_fantasy(idea, destination)
    opens = cycle_opens_browser(destination, starter)
    # O start não planta brief. Sem isto a próxima sessão
    # reaprendia o serve e o template agents listava GDD
    # que não existia. Memória do agente não é rascunho.
    memory = write_agents_memory(
        destination, play, starter, documents, idea, url, cycle, fantasy, opens,
    )
    if memory and documents:
        drafts.append(memory)
    commands = []
    if play:
        commands.append(play)
    # O mapa é start → jogar → note. Sem isto o init
    # apontava um segundo `next --focus feel` e o
    # passo 3 sumia. O `play` já diz que o próximo
    # comando é note. then.lost continua o next.
    commands.append(note_command(destination))
    then = cycle_then(destination, play, starter)
    scaffold = init_then_scope()
    if scaffold:
        then = dict(then, scope=scaffold)
    runtime = node_runtime(play)
    # O start já nomeava a superfície. Sem isto o init
    # plantava e calava — quem segue o caminho com
    # rascunhos tinha de achar o play depois. Nomear
    # não serve e não observa.
    prompt = cycle_prompt(
        play, then, cycle, False, url, runtime, fantasy, opens,
        playtest_command(destination),
    )
    return {
        "schema_version": 1,
        "project": str(destination),
        "starter": starter,
        "kind": identify(destination),
        "title": values["project_title"],
        "files": files,
        "documents": init_documents_reading(drafts),
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
        "play": play,
        "open": play,
        "url": url,
        "runtime": runtime,
        "then": then,
        "fantasy": fantasy,
        "cycle": named_cycle(cycle),
        "prompt": prompt,
        "executed": False,
        "scope": init_scope(documents, idea),
    }


# A receita já recusa que título e cores novos
# sejam experiência. Sem isto o then do start
# apontava play e calava a recusa. Nome no
# disco não é o ciclo jogado.
CREATE_RECIPE = FRAMEWORK / "recipes/create.md"
CREATE_EXPERIENCE = re.compile(r"não demonstram uma experiência nova")


def recipe_refuses_title_as_new_experience(text):
    return bool(text and CREATE_EXPERIENCE.search(text))


def start_then_experience_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_title_as_new_experience(text):
        return "recipes/create.md"
    return None


def start_then_scope():
    if not start_then_experience_source():
        return None
    return (
        "O disco recusa que título e cores novos sejam experiência "
        "(`experiência`). Nome no disco não é o ciclo jogado."
    )


# A receita já recusa que o scaffold ou a cópia
# que inicia seja mais que ponto de partida.
# Sem isto o then do init apontava play e
# calava a recusa. Cópia no disco não é a slice.
CREATE_SCAFFOLD = re.compile(r"continua sendo ponto de partida")


def recipe_refuses_scaffold_as_more_than_start(text):
    return bool(text and CREATE_SCAFFOLD.search(text))


def init_then_scaffold_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_scaffold_as_more_than_start(text):
        return "recipes/create.md"
    return None


def init_then_scope():
    if not init_then_scaffold_source():
        return None
    return (
        "O disco recusa que o scaffold ou a cópia que inicia seja mais que "
        "ponto de partida (`scaffold`). Cópia no disco não é a slice."
    )


# A receita já recusa que mostrar a estrutura
# seja a slice. Sem isto o then do guide
# apontava play e calava a recusa. Mapa no
# disco não é a fatia.
CREATE_STRUCTURE = re.compile(r"mostra\s+estrutura")


def recipe_refuses_showing_structure_as_slice(text):
    return bool(text and CREATE_STRUCTURE.search(text))


def guide_then_structure_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_showing_structure_as_slice(text):
        return "recipes/create.md"
    return None


def guide_then_scope():
    if not guide_then_structure_source():
        return None
    return (
        "O disco recusa que mostrar a estrutura seja a slice "
        "(`estrutura`). Mapa no disco não é a fatia."
    )


# A receita já recusa que o start
# execute e observe. Sem isto o
# start relatava o created e calava
# a recusa. Pasta no disco não é a
# partida.
CREATE_EXECUTE = re.compile(r"Não executa e não observa")


def recipe_refuses_start_as_execute_and_observe(text):
    return bool(text and CREATE_EXECUTE.search(text))


def start_created_execute_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_start_as_execute_and_observe(text):
        return "recipes/create.md"
    return None


def start_created_execute_scope():
    if not start_created_execute_source():
        return None
    return (
        " O disco recusa que o start execute e observe "
        "(`executa`). Pasta no disco não é a partida."
    )


def start_created_scope():
    scope = (
        "pasta criada no disco. "
        "Não executa e não observa."
    )
    named = start_created_execute_scope()
    if named:
        scope += named
    return scope


def start_created_flag(reading):
    created = (reading or {}).get("created")
    if isinstance(created, dict):
        return bool(created.get("created"))
    return bool(created)


# A receita já recusa que nomear a
# pasta grave a frase. Sem isto o
# start relatava o named e calava
# a recusa. Slug no disco não é
# o documento.
CREATE_NAMED_PHRASE = re.compile(r"não grava a frase")


def recipe_refuses_naming_folder_as_writing_the_phrase(text):
    return bool(text and CREATE_NAMED_PHRASE.search(text))


def start_named_phrase_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_naming_folder_as_writing_the_phrase(text):
        return "recipes/create.md"
    return None


def start_named_phrase_scope():
    if not start_named_phrase_source():
        return None
    return (
        " O disco recusa que nomear a pasta grave a frase "
        "(`frase`). Slug no disco não é o documento."
    )


def start_named_scope():
    scope = (
        "pasta nomeada pela ideia. "
        "Não grava a frase."
    )
    named = start_named_phrase_scope()
    if named:
        scope += named
    return scope


def start_named_flag(reading):
    named = (reading or {}).get("named") if isinstance(reading, dict) else reading
    if isinstance(named, dict):
        return bool(named.get("named"))
    return bool(named)


def start_named_reading(named):
    if not named:
        return False
    return {
        "named": True,
        "scope": start_named_scope(),
    }


def start_project(destination=None, starter=None, title=None, idea=None, documents=False, cwd=None):
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
    url = serve_url(scripts)
    then = cycle_then(destination, play, chosen)
    experience = start_then_scope()
    if experience:
        then = dict(then, scope=experience)
    cycle = starter_cycle(chosen)
    noted = bool(observation_receipts(destination))
    start_parts = ["start", destination]
    if chosen:
        start_parts.extend(["--starter", chosen])
    if nonempty(idea):
        start_parts.extend(["--idea", idea.strip()])
    start_command = harness_command(*start_parts)
    steps = cycle_steps(start_command, play, then, cycle, proposal, exists=True, url=url)
    runtime = node_runtime(play)
    fantasy = resolve_fantasy(idea, destination)
    created_flag = created
    if created_flag:
        created_flag = {
            "created": True,
            "scope": start_created_scope(),
        }
    report = {
        "schema_version": 1,
        "project": str(destination),
        "created": created_flag,
        "starter": init_report["starter"] if init_report else None,
        "idea": idea.strip() if nonempty(idea) else None,
        "fantasy": fantasy,
        "brief": planted["brief"],
        "surface": planted["surface"],
        "cycle": named_cycle(cycle),
        "play": play,
        "open": play,
        "url": url,
        "session": then.get("session"),
        "runtime": runtime,
        "steps": steps,
        "init": init_report,
        "next": proposal,
        "then": then,
        "noted": noted,
        "named": start_named_reading(named),
        "suggest": str(suggested_start_target(idea, cwd=cwd)) if named else None,
        "prompt": cycle_prompt(
            play, then, cycle, noted, url, runtime, fantasy,
            cycle_opens_browser(destination, chosen),
            playtest_command(destination),
        ),
        "executed": False,
        "scope": (
            "Caminho ideia→ciclo: cria o projeto se o destino estiver livre e "
            "aponta o comando que abre o jogo. `open` é o play — o comando de "
            "agora, depois do start. `play` continua o mesmo valor, para quem "
            "já lia essa chave. `url` nomeia a superfície pedida; nomear não "
            "serve, não abre e não observa. Se o serve tenta abrir o "
            "navegador, o prompt nomeia a tentativa. Sem o marcador, pede "
            "Abrir. Nomear não abre. O banner do serve continua a "
            "porta depois do listen. `steps` é o mesmo mapa de três passos do "
            "guide, com o passo 1 feito. Sem caminho, `--idea` nomeia "
            "a pasta — ao lado do framework se o start corre de dentro desta "
            "árvore — e cria. `guide --idea` continua só no comando, não no "
            "disco. Se o starter declara o verbo e "
            "as teclas, o prompt as nomeia — inclusive a porta, o cluster de "
            "uma mão, o toque, o controle e as queries de look, chuva, par, "
            "seed e convite, se o starter as declara. Não "
            "executa o jogo. O `prompt` também sai em stderr; o JSON "
            "fica no stdout. Depois de uma "
            "partida, a página grava o recibo se você escrever; o próximo "
            "comando do harness continua `note`, não `next`. "
            "O prompt nomeia o `playtest` que o `AGENTS.md` já cita. Só lê. "
            "Sem os quatro não é achado. Sem `then.playtest`. Nomear o "
            "leitor não observa. "
            "`then` já nomeia par, look, chuva e voz se o projeto declara essas "
            "ferramentas; depois de um recibo, o prompt as aponta. Se o disco "
            "tem last-run com seed, `then` aponta a seed e o convite; "
            "nomear o endereço não observa. Ferramenta "
            "no disco não é alguém de fora nem mix ouvido. Não "
            "instala dependências e não avalia a proposta. Se o play pede "
            "npm, o `package.json` tem dependências e `node_modules` falta, "
            "`then.install` nomeia `npm install`. Sem dependências a chave "
            "some. Nomear não instala. `--idea` entra na "
            "abertura se houver `data/copy.json` e o prompt nomeia `Fantasia:` "
            "à parte de `Verbo:`. O brief só nasce com `--docs`; "
            "sem ele o `start` não planta rascunhos. A frase na tela não "
            "muda o verbo. `runtime` lê o `node` do PATH se o play pede "
            "npm ou node; não executa o serve. `usable` é só o binário. "
            "`session` aponta a partida simulada se o manifesto a declara; "
            "o prompt a nomeia. Não executa e não observa."
        ),
    }
    if pair_birth_source(destination):
        report["scope"] += (
            " O disco nasce look e chuva no mesmo nome (`pair`). "
            "Ferramenta no disco não é alguém de fora."
        )
    named = start_empty_scope()
    if named:
        report["scope"] += named
    return report


# A receita já recusa que nove
# arquivos vazios aumentem a
# qualidade. Sem isto o start
# copiava o caminho e calava a
# recusa. Arquivo no disco não é
# a fatia.
CREATE_EMPTY = re.compile(r"Nove arquivos vazios não\s+aumentam a qualidade")


def recipe_refuses_empty_files_as_quality(text):
    return bool(text and CREATE_EMPTY.search(text))


def start_empty_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_empty_files_as_quality(text):
        return "recipes/create.md"
    return None


def start_empty_scope():
    if not start_empty_source():
        return None
    return (
        " O disco recusa que nove arquivos vazios aumentem a qualidade "
        "(`vazios`). Arquivo no disco não é a fatia."
    )


# A receita já recusa que aceitar o parâmetro prove que ele afeta o RNG.
# Sem isto o then do play apontava a seed e calava a recusa.
# Endereço no disco não é a simulação.
LIFECYCLE_RECIPE = FRAMEWORK / "recipes/lifecycle.md"
PLAY_THEN_RNG = re.compile(r"não prova que ele afeta RNG")


def recipe_refuses_parameter_as_rng(text):
    return bool(text and PLAY_THEN_RNG.search(text))


def play_then_rng_source():
    path = LIFECYCLE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_parameter_as_rng(text):
        return "recipes/lifecycle.md"
    return None


def play_then_scope(then=None):
    if not play_then_rng_source():
        return None
    if not then or not then.get("seed"):
        return None
    return (
        "O disco recusa que aceitar o parâmetro prove que ele afete "
        "o RNG (`RNG`). Endereço no disco não é a simulação."
    )


# A receita já recusa que oferecer o recibo
# seja observação. Sem isto o then do play
# sem seed apontava note e calava a recusa.
# Recibo no disco não é a sessão.
PLAY_THEN_OBSERVATION = re.compile(r"isso não é observação")


def recipe_refuses_receipt_as_observation(text):
    return bool(text and PLAY_THEN_OBSERVATION.search(text))


def play_then_observation_source():
    path = LIFECYCLE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_receipt_as_observation(text):
        return "recipes/lifecycle.md"
    return None


def play_then_observation_scope(then=None):
    if not play_then_observation_source():
        return None
    if then and then.get("seed"):
        return None
    return (
        "O disco recusa que oferecer o recibo seja observação "
        "(`observação`). Recibo no disco não é a sessão."
    )


# A receita já recusa que o recibo
# escrito observe. Sem isto o play
# relatava o noted e calava a
# recusa. Arquivo no disco não é
# a sessão.
PLAY_WRITTEN = re.compile(r"o recibo escrito não observa")


def recipe_refuses_written_receipt_as_observing(text):
    return bool(text and PLAY_WRITTEN.search(text))


def play_noted_written_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_written_receipt_as_observing(text):
        return "recipes/create.md"
    return None


def play_noted_written_scope():
    if not play_noted_written_source():
        return None
    return (
        " O disco recusa que o recibo escrito observe "
        "(`escrito`). Arquivo no disco não é a sessão."
    )


def play_noted_scope():
    scope = (
        "recibo de observação no disco. "
        "O recibo escrito não observa."
    )
    named = play_noted_written_scope()
    if named:
        scope += named
    return scope


def play_noted_flag(reading):
    noted = (reading or {}).get("noted")
    if isinstance(noted, dict):
        return bool(noted.get("noted"))
    return bool(noted)


def play_noted_reading(noted):
    if not noted:
        return False
    return {
        "noted": True,
        "scope": play_noted_scope(),
    }


def play_cycle(destination=None, starter=None):
    if destination is None:
        raise ValueError(missing_destination_hint())
    dest = Path(destination)
    if dest.is_symlink() or not dest.is_dir() or not (dest / "package.json").is_file():
        raise ValueError(missing_game_hint())
    available = starters()
    chosen = starter or (available[0] if available else "canvas-arcade")
    try:
        scripts, manager = project_commands(dest)
    except (OSError, ValueError):
        scripts, manager = {}, None
    asked = play_command(dest, scripts, manager)
    play = asked or (
        f"cd {shlex.quote(str(dest))} && npm run serve"
    )
    url = serve_url(scripts)
    then = cycle_then(dest, play, chosen)
    rng = play_then_scope(then)
    seen = play_then_observation_scope(then)
    named = rng or seen
    if named:
        then = dict(then, scope=named)
    cycle = starter_cycle(chosen)
    noted = bool(observation_receipts(dest))
    proposal = next_step(dest, "feel")
    start_command = harness_command("start", dest, "--starter", chosen)
    steps = cycle_steps(start_command, play, then, cycle, proposal, exists=True, url=url)
    runtime = node_runtime(play)
    fantasy = resolve_fantasy(project=dest)
    return {
        "schema_version": 1,
        "command": "play",
        "project": str(dest),
        "play": play,
        "open": play,
        "url": url,
        "session": then.get("session"),
        "runtime": runtime,
        "then": then,
        "cycle": named_cycle(cycle),
        "fantasy": fantasy,
        "prompt": cycle_prompt(
            play, then, cycle, noted, url, runtime, fantasy,
            cycle_opens_browser(dest, chosen),
            playtest_command(dest),
        ),
        "steps": steps,
        "noted": play_noted_reading(noted),
        "executed": False,
        "scope": play_scope(dest),
    }


def play_scope(project):
    scope = (
        "Aponta o comando que abre o jogo e a superfície pedida. Não "
        "executa, não cria e não joga. Sem caminho, o único jogo do "
        "laboratório basta; dois pedem o caminho. `open` é o play. "
        "`url` nomeia localhost e a porta pedida; nomear não serve. "
        "Se o serve tenta abrir o navegador, o prompt nomeia a "
        "tentativa. Sem o marcador, pede Abrir. Nomear não abre. "
        "Com tela, o avanço abre a porta. Depois "
        "de uma partida, a página grava o recibo se você escrever; o "
        "próximo comando do harness continua `note`, não `next`. "
        "O prompt nomeia o `playtest` que o `AGENTS.md` já cita. Só lê. "
        "Sem os quatro não é achado. Sem `then.playtest`. Nomear o "
        "leitor não observa. "
        "Se o disco tem last-run com seed, `then` aponta a seed e o "
        "convite; nomear o endereço não observa. `session` aponta a "
        "partida simulada se o manifesto a declara; o prompt a nomeia. "
        "Não executa e não observa. Se o play pede npm, o "
        "`package.json` tem dependências e `node_modules` falta, "
        "`then.install` nomeia `npm install`. Sem dependências a chave "
        "some. Nomear não instala. `runtime` lê o `node` "
        "do PATH se o play pede npm ou node; não executa o serve. "
        "O `prompt` também "
        "sai em stderr; o JSON fica no stdout. `executed` fica falso."
    )
    if play_production_source(project):
        scope += (
            " O disco recusa produção (`produção`). "
            "Serve no disco não é publicação."
        )
    named = play_verb_scope()
    if named:
        scope += named
    arc = play_arc_scope()
    if arc:
        scope += arc
    return scope


# A receita já recusa que
# verbo mudo ou sem peso
# seja. Sem isto o play
# apontava o url e calava
# a recusa. Abrir no disco
# não é o verbo.
CREATE_VERB = re.compile(r"verbo mudo ou sem peso não é")


def recipe_refuses_mute_weightless_verb(text):
    return bool(text and CREATE_VERB.search(text))


def play_verb_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_mute_weightless_verb(text):
        return "recipes/create.md"
    return None


def play_verb_scope():
    if not play_verb_source():
        return None
    return (
        " O disco recusa que verbo mudo ou sem peso seja "
        "(`verbo`). Abrir no disco não é o verbo."
    )


# A receita já recusa que o arco
# prometa o dash. Sem isto o play
# apontava o url e calava a
# recusa. Arco no disco não é o
# dash.
FEEL_ARC = re.compile(r"o arco não promete\s+o dash")


def recipe_refuses_arc_as_dash_promise(text):
    return bool(text and FEEL_ARC.search(text))


def play_arc_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_arc_as_dash_promise(text):
        return "recipes/feel.md"
    return None


def play_arc_scope():
    if not play_arc_source():
        return None
    return (
        " O disco recusa que o arco prometa o dash "
        "(`arco`). Arco no disco não é o dash."
    )


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


def is_fs_root(path):
    path = Path(path).resolve()
    return path.parent == path


def playable_neighbors(root, framework=None):
    # Filhos diretos do laboratório. Não entra no framework — o starter
    # não é o seu jogo — e não varre a raiz do disco.
    framework = Path(framework or FRAMEWORK).resolve()
    root = Path(root).resolve()
    if is_fs_root(root):
        return []
    if root == framework or root.is_relative_to(framework):
        home = framework.parent
        if is_fs_root(home):
            return []
    else:
        home = root
    found = []
    try:
        children = sorted(home.iterdir(), key=lambda item: item.name)
    except OSError:
        return []
    for path in children:
        if not path.is_dir() or path.is_symlink() or path.name.startswith("."):
            continue
        target = path.resolve()
        if target == framework or target.is_relative_to(framework):
            continue
        if path.name in SKIP:
            continue
        if not (path / "package.json").is_file():
            continue
        if identify(path) != "package.json":
            continue
        found.append(target)
    return found


def resolve_project_destination(explicit=None, root=None):
    dest = here_project(explicit, root)
    if explicit is not None or dest is not None:
        return dest
    found = playable_neighbors(root or ROOT)
    if len(found) == 1:
        return found[0]
    if len(found) > 1:
        names = ", ".join(path.name for path in found)
        raise ValueError(missing_destination_hint(names))
    return None


# O 0.9.137 nasceu neste nome. Os verbos do ciclo depois do play
# usam o mesmo resolvedor; o alias evita partir os testes que já o leem.
resolve_play_destination = resolve_project_destination


def require_project_destination(explicit=None, root=None):
    dest = resolve_project_destination(explicit, root)
    if dest is None:
        raise ValueError(missing_destination_hint())
    return dest


# Teto do nome derivado da frase. Mais que isso vira caminho ilegível;
# menos obriga a inventar o resto. A pasta só existe depois do `start`.
IDEA_SLUG_LIMIT = 48
# A recusa explicava --idea e calava o comando que o README
# já imprime. Nomear não cria.
START_IDEA_EXAMPLE = "atravessar estilhaços para guardar a corrente"


def start_idea_command(idea=None):
    phrase = idea.strip() if isinstance(idea, str) and idea.strip() else START_IDEA_EXAMPLE
    return harness_command("start", "--idea", phrase)


def missing_destination_hint(names=None):
    command = start_idea_command()
    if names:
        return f"sem destino: {names}. passe o caminho ou rode {command}"
    return f"sem destino: passe o caminho ou rode {command}"


def missing_game_hint():
    return f"sem jogo: rode {start_idea_command()} ou passe o caminho do projeto"


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
        raise ValueError(missing_destination_hint())
    here = Path(cwd or Path.cwd()).resolve()
    return (here / target).resolve()


def require_guide_idea(project, idea, cwd=None):
    # O mapa sem destino devolvia `start '<destino>'` com saída 0 na raiz
    # do framework — o primeiro passo quebrava. A recusa explicava
    # --idea e calava o comando que o README já imprime. Subpastas
    # (starter incluído) e a API `guide_cycle` continuam pedindo o
    # mapa sem frase. Recusar cedo não cria e não executa.
    if project is not None:
        return
    here = Path(cwd or Path.cwd()).resolve()
    if here != FRAMEWORK.resolve():
        return
    if suggested_start_target(idea, cwd=cwd, framework=FRAMEWORK) is not None:
        return
    raise ValueError(missing_destination_hint())


# O README já recusa que o guide
# crie o projeto. Sem isto o
# guide relatava o exists e calava
# a recusa. Destino no disco não é
# criação do mapa.
GUIDE_CREATE = re.compile(r"não cria o projeto")


def readme_refuses_guide_as_creating_project(text):
    return bool(text and GUIDE_CREATE.search(text))


def guide_exists_project_source():
    path = FRAMEWORK / "README.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_refuses_guide_as_creating_project(text):
        return "README.md"
    return None


def guide_exists_project_scope():
    if not guide_exists_project_source():
        return None
    return (
        " O disco recusa que o guide crie o projeto "
        "(`projeto`). Destino no disco não é criação do mapa."
    )


def guide_exists_scope():
    scope = (
        "destino com package.json no disco. "
        "O guide não cria o projeto."
    )
    named = guide_exists_project_scope()
    if named:
        scope += named
    return scope


def guide_exists_flag(reading):
    exists = (reading or {}).get("exists")
    if isinstance(exists, dict):
        return bool(exists.get("exists"))
    return bool(exists)


def guide_exists_reading(exists):
    if not exists:
        return False
    return {
        "exists": True,
        "scope": guide_exists_scope(),
    }


# A receita já recusa que o
# diretório atual seja o ciclo
# jogado. Sem isto o guide
# relatava o here e calava a
# recusa. Pasta no disco não é
# a partida.
CREATE_HERE_PLAYED = re.compile(r"Diretório atual não é o ciclo jogado")


def recipe_refuses_current_directory_as_played_cycle(text):
    return bool(text and CREATE_HERE_PLAYED.search(text))


def guide_here_aqui_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_current_directory_as_played_cycle(text):
        return "recipes/create.md"
    return None


def guide_here_aqui_scope():
    if not guide_here_aqui_source():
        return None
    return (
        " O disco recusa que o diretório atual seja o ciclo jogado "
        "(`aqui`). Pasta no disco não é a partida."
    )


def guide_here_scope():
    scope = (
        "diretório atual é o jogo. "
        "Não é o ciclo jogado."
    )
    named = guide_here_aqui_scope()
    if named:
        scope += named
    return scope


def guide_here_flag(reading):
    here = (reading or {}).get("here") if isinstance(reading, dict) else reading
    if isinstance(here, dict):
        return bool(here.get("here"))
    return bool(here)


def guide_here_reading(here):
    if not here:
        return False
    return {
        "here": True,
        "scope": guide_here_scope(),
    }


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
    url = None
    if exists:
        try:
            scripts, manager = project_commands(dest)
        except (OSError, ValueError):
            scripts, manager = {}, None
        play = play_command(dest, scripts, manager)
        url = serve_url(scripts)
        nxt = next_step(dest, "feel")
    else:
        starter_scripts, _starter_manager = starter_package_commands(chosen)
        url = serve_url(starter_scripts)
    named = dest if dest is not None else suggested
    play_fallback = (
        f"cd {shlex.quote(str(named))} && npm run serve"
        if named is not None
        else "npm run serve"
    )
    next_target = named if named is not None else Path("<destino>")
    play_cmd = play or play_fallback
    then = cycle_then(next_target, play_cmd, chosen)
    structure = guide_then_scope()
    if structure:
        then = dict(then, scope=structure)
    cycle = starter_cycle(chosen)
    start_command = harness_command(*start_parts)
    noted = bool(exists and observation_receipts(dest))
    steps = cycle_steps(start_command, play_cmd, then, cycle, nxt, exists, url)
    runtime = node_runtime(play_cmd)
    fantasy = resolve_fantasy(phrase, dest if exists else None)
    return {
        "schema_version": 1,
        "command": "guide",
        "executed": False,
        "here": False,
        "idea": phrase,
        "fantasy": fantasy,
        "starter": chosen,
        "path": str(dest) if dest is not None else None,
        "suggest": str(suggested) if suggested is not None else None,
        "exists": guide_exists_reading(exists),
        "cycle": named_cycle(cycle),
        "then": then,
        "noted": noted,
        "open": start_command if not exists else play_cmd,
        "url": url,
        "session": then.get("session"),
        "runtime": runtime,
        "prompt": guide_prompt(
            exists, start_command, play_cmd, then, cycle, noted, url, runtime, fantasy,
            cycle_opens_browser(dest if exists else None, chosen),
            playtest_command(next_target),
        ),
        "steps": steps,
        "scope": guide_scope(chosen),
    }


def guide_scope(starter):
    scope = (
        "Três passos ideia→ciclo: start, jogar, note. `open` é o comando "
        "de agora — o start se o destino ainda não existe, o play se "
        "já existe. `url` nomeia a superfície pedida; nomear não serve. "
        "Se o serve tenta abrir o navegador, o prompt nomeia a "
        "tentativa. Sem o marcador, pede Abrir. Nomear não abre. "
        "`prompt` o nomeia para colar e também sai em "
        "stderr; o JSON fica no stdout. Se o starter declara "
        "o verbo e as teclas, o prompt e o passo 2 as nomeiam — inclusive a porta. Sem destino, a frase "
        "nomeia a pasta no comando do start — ao lado do framework se o "
        "mapa corre de dentro desta árvore; no diretório atual se corre "
        "de fora. `guide --idea` continua só no comando, não no disco. "
        "O prompt nomeia `Fantasia:` à parte de `Verbo:` quando há frase "
        "ou `copy.json`; a frase não muda o verbo. "
        "`then` nomeia par, look, chuva e voz quando o projeto — ou o "
        "starter, se o destino ainda não existe — declara essas "
        "ferramentas. Se declara `session`, `then` a aponta. Se o disco "
        "tem last-run com seed, `then` aponta a seed e o convite; "
        "nomear o endereço não observa. Nomear o ofício não pinta, não chove e não ouve. O autor do `note` é "
        "sugestão do git ou do ambiente, não quem jogou. "
        "`next` fica para quando o ciclo já correu e você não sabe o "
        "que falta. O prompt nomeia o `playtest` que o `AGENTS.md` já "
        "cita. Só lê. Sem os quatro não é achado. Sem `then.playtest`. "
        "Nomear o leitor não observa. Sem destino, se o diretório atual é um jogo fora "
        "do framework, o mapa usa esse caminho. Não cria o projeto, "
        "não abre o jogo e não avalia a proposta. `session` aponta a "
        "partida simulada se o manifesto a declara; o prompt a nomeia. "
        "Não executa e não observa. Se o play pede npm, o "
        "`package.json` tem dependências e `node_modules` falta, "
        "`then.install` nomeia `npm install`. Sem dependências a chave "
        "some. Nomear não instala. `runtime` lê o `node` "
        "do PATH se o play pede npm ou node; não executa o serve. "
        "Passos 2 e 3 "
        "permanecem `executed` falsos mesmo quando o destino já existe."
    )
    if guide_speed_source(starter):
        scope += (
            " O disco nomeia o relógio (`speed`). "
            "Frase no disco não é partida observada."
        )
    named = guide_steps_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que passos
# textuais sejam uma garantia de
# execução. Sem isto o guide copiava
# os três passos e calava a recusa.
# Texto no disco não é a partida.
CREATE_STEPS = re.compile(r"textuais não são uma garantia de execução")


def recipe_refuses_textual_steps_as_execution(text):
    return bool(text and CREATE_STEPS.search(text))


def guide_steps_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_textual_steps_as_execution(text):
        return "recipes/create.md"
    return None


def guide_steps_scope():
    if not guide_steps_source():
        return None
    return (
        " O disco recusa que passos textuais sejam uma garantia de "
        "execução (`passos`). Texto no disco não é a partida."
    )


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


STARTER_NODE_MAJOR = 20

# O package já pede Node. Sem isto o doctor
# lia a major do PATH e calava o engines.
# Pedido no disco não é binário no PATH.
STARTER_PACKAGE = "package.json"
STARTER_ENGINES = re.compile(
    r'"engines"\s*:\s*\{[^{}]*"node"\s*:',
    re.DOTALL,
)


def package_asks_node(text):
    return bool(text and STARTER_ENGINES.search(text))


def starter_engines_source():
    if not STARTERS_ROOT.is_dir() or STARTERS_ROOT.is_symlink():
        return None
    for name in starters():
        path = STARTERS_ROOT / name / STARTER_PACKAGE
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if package_asks_node(text):
            return f"assets/starters/{name}/{STARTER_PACKAGE}"
    return None


# O manifesto já declara as trocas. Sem isto o
# doctor lia a integridade e calava o campo.
# Manifesto no disco não é projeto criado.
STARTER_SUBSTITUTIONS = re.compile(r'"substitutions"\s*:\s*\[')
# O package já declara o módulo. Sem isto o
# init copiava o manifesto e calava o `type`.
# Tipo no disco não é runtime instalado.
PACKAGE_MODULE = re.compile(r'"type"\s*:\s*"module"')


def manifest_declares_substitutions(text):
    return bool(text and STARTER_SUBSTITUTIONS.search(text))


def package_declares_module(text):
    return bool(text and PACKAGE_MODULE.search(text))


def starter_module_source():
    if not STARTERS_ROOT.is_dir() or STARTERS_ROOT.is_symlink():
        return None
    for name in starters():
        path = STARTERS_ROOT / name / STARTER_PACKAGE
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 400_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if package_declares_module(text):
            return f"assets/starters/{name}/{STARTER_PACKAGE}"
    return None


def starter_substitutions_source():
    if not STARTERS_ROOT.is_dir() or STARTERS_ROOT.is_symlink():
        return None
    for name in starters():
        path = STARTERS_ROOT / name / STARTER_MANIFEST
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 400_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if manifest_declares_substitutions(text):
            return f"assets/starters/{name}/{STARTER_MANIFEST}"
    return None


def node_major(version):
    if not isinstance(version, str) or not version.strip():
        return 0
    match = re.match(r"^v?(\d+)", version.strip())
    return int(match.group(1)) if match else 0


# A receita já recusa que o usable
# seja mais que o binário. Sem
# isto o runtime relatava o usable
# e calava a recusa. Node no PATH
# não é o dispositivo.
RUNTIME_BINARY = re.compile(r"só o binário")


def recipe_refuses_usable_as_more_than_binary(text):
    return bool(text and RUNTIME_BINARY.search(text))


def runtime_usable_binary_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_usable_as_more_than_binary(text):
        return "recipes/create.md"
    return None


def runtime_usable_binary_scope():
    if not runtime_usable_binary_source():
        return None
    return (
        " O disco recusa que o usable seja mais que o binário "
        "(`binário`). Node no PATH não é o dispositivo."
    )


def runtime_usable_scope():
    scope = (
        "binário no PATH. "
        "`usable` é só o binário."
    )
    named = runtime_usable_binary_scope()
    if named:
        scope += named
    return scope


def runtime_usable_flag(reading):
    usable = (reading or {}).get("usable")
    if isinstance(usable, dict):
        return bool(usable.get("usable"))
    return bool(usable)


def runtime_usable_reading(usable):
    if not usable:
        return False
    return {
        "usable": True,
        "scope": runtime_usable_scope(),
    }


def node_runtime(play=None):
    asked = bool(isinstance(play, str) and re.search(r"\b(npm|node)\b", play))
    report = tool_report("node")
    version = report["version"]
    major = node_major(version)
    usable = (not asked) or major >= STARTER_NODE_MAJOR
    return {
        "schema_version": 1,
        "node": version,
        "major": major or None,
        "need": STARTER_NODE_MAJOR if asked else None,
        "asked": asked,
        "usable": runtime_usable_reading(usable),
        "executed": False,
        "scope": (
            "Presença e major do `node` no PATH. Não executa o serve, não "
            "instala e não observa o jogo. `usable` é só o binário; não é "
            "partida, mix nem dispositivo."
        ),
    }


def runtime_line(runtime):
    if not runtime or not runtime.get("asked") or runtime.get("usable"):
        return ""
    need = runtime.get("need") or STARTER_NODE_MAJOR
    if not runtime.get("node"):
        return f"Node {need}+ ausente: o serve não sobe. "
    return f"Node {runtime['node']} no PATH: o starter pede {need}+. "


def session_line(then):
    command = then.get("session") if then else None
    if not nonempty(command):
        return ""
    return f"Sessão: {command}. Simulação não é partida observada. "


def skill_targets(root):
    return [root / ".agents/skills/game-dev/SKILL.md", root / ".claude/skills/game-dev/SKILL.md"]


# A skill já recusa que AAA seja tier de publisher. Sem isto o
# atalho copiava o hash e calava a recusa.
# Atalho no disco não é orçamento.
SKILL_FILE = FRAMEWORK / "SKILL.md"
SKILL_PUBLISHER = re.compile(r"não tier de publisher")


def skill_refuses_publisher_tier(text):
    return bool(text and SKILL_PUBLISHER.search(text))


def skill_target_publisher_source():
    path = SKILL_FILE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if skill_refuses_publisher_tier(text):
        return "SKILL.md"
    return None


def skill_target_scope():
    scope = (
        "Caminho, vigência e symlink do atalho da skill. Não copia a "
        "skill e não cria o projeto."
    )
    if skill_target_publisher_source():
        scope += (
            " O disco recusa que AAA seja tier de publisher (`publisher`). "
            "Atalho no disco não é orçamento."
        )
    return scope


# O mapa já recusa que a ausência seja evidência negativa.
# Sem isto o check copiava o estado e calava a recusa.
# Lista no disco não é laboratório.
SOURCES_MAP = FRAMEWORK / "references/sources.md"
STUDIES_ABSENCE = re.compile(r"não é evidência\s+negativa")


def map_refuses_absence_as_evidence(text):
    return bool(text and STUDIES_ABSENCE.search(text))


def doctor_check_absence_source():
    path = SOURCES_MAP
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if map_refuses_absence_as_evidence(text):
        return "references/sources.md"
    return None


def doctor_check_scope():
    scope = (
        "Nome, exigência e estado da ferramenta. Não instala e não "
        "cria o projeto."
    )
    if doctor_check_absence_source():
        scope += (
            " O disco recusa que a ausência seja evidência negativa (`ausência`). "
            "Lista no disco não é laboratório."
        )
    return scope


# O README já imprime o exemplo. Sem isto o
# doctor.then colava <fantasia> e calava a frase.
# Frase no then não é pasta criada.
README_FILE = FRAMEWORK / "README.md"


def readme_prints_idea_example(text):
    return bool(text and START_IDEA_EXAMPLE and START_IDEA_EXAMPLE in text)


def doctor_idea_source():
    path = README_FILE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if readme_prints_idea_example(text):
        return "README.md"
    return None


def doctor_guide_idea():
    return START_IDEA_EXAMPLE if doctor_idea_source() else "<fantasia>"


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
    major = node_major(node["version"])
    add(
        "node", False, major >= STARTER_NODE_MAJOR,
        node["version"] or "ausente",
        None if major >= STARTER_NODE_MAJOR else "Node 20+ é exigido pelo starter canvas-arcade e pelos validadores de package.json.",
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
    # Os sub-comandos da skill são três coisas que precisam concordar: o catálogo,
    # um arquivo de referência por comando e a tabela do SKILL.md. Um comando no
    # menu sem referência manda o agente ler um arquivo que não existe.
    command_issues = command_problems()
    try:
        command_names = list(command_catalog()["commands"])
    except (OSError, ValueError):
        command_names = []
    add(
        "commands", True, not command_issues,
        f"{len(command_names)} sub-comandos com catálogo, referência e linha no SKILL.md" if not command_issues else "; ".join(command_issues),
        "Alinhe commands/commands.json, commands/<nome>.md e a tabela de comandos do SKILL.md.",
    )
    add(
        "starters", False, bool(available),
        ", ".join(available) or "nenhum",
        "Sem starter, `start --idea` não tem de onde partir e REUSE não tem candidato local.",
    )
    # O primeiro comando da skill não ensina `init`: o laboratório vazio
    # segue `start --idea`. `init` só falha na hora de copiar; aqui a
    # divergência entre o manifesto e os arquivos do starter é
    # diagnosticável antes de alguém tentar criar um projeto.
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
            "scope": skill_target_scope(),
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
        "Sem esse acervo o catálogo vem vazio; `sfx search` nomeia o stem do starter que casa com o termo. Arquivo no disco não é mix ouvido.",
    )

    blocking = [check["name"] for check in checks if check["required"] and check["status"] != "ok"]
    ready = not blocking
    blocking = doctor_blocking_reading(blocking)
    empty = not projects
    then = doctor_then(ready, available, empty)
    check_scope = doctor_check_scope()
    for item in checks:
        item["scope"] = check_scope
    scope = (
        "Presença e versão de ferramentas, presença dos arquivos deste repositório e conteúdo dos atalhos da skill no host. "
        "Com starter e laboratório sem jogo, `then.guide` aponta o mapa "
        "com `--idea`. Sem frase a raiz recusa. "
        "Não instala nada, não copia a skill, não cria o projeto, não executa o jogo e não comprova que um projeto funciona."
    )
    if starter_engines_source():
        scope += (
            " O disco nomeia o engines (`engines`). "
            "Pedido no disco não é binário no PATH."
        )
    if starter_substitutions_source():
        scope += (
            " O disco declara as substituições (`substitutions`). "
            "Manifesto no disco não é projeto criado."
        )
    if doctor_idea_source():
        scope += (
            " O disco imprime o exemplo que o then cola (`exemplo`). "
            "Frase no then não é pasta criada."
        )
    return {
        "schema_version": 1,
        "framework": str(FRAMEWORK),
        "root": str(root),
        "ready": ready,
        "blocking": blocking,
        "empty": (
            {
                "empty": True,
                "scope": doctor_empty_scope(),
            }
            if empty else False
        ),
        "then": then,
        "checks": checks,
        "skill_targets": installed,
        "starters": available,
        "commands": command_names,
        "foci": list(FOCI),
        "stages": list(STAGES),
        "genres": list(GENRES),
        "scales": list(SCALES),
        "known_markers": [marker for marker, _ in ENGINE_MARKERS],
        "scope": scope,
    }


# A receita já recusa que o mapa
# crie a pasta. Sem isto o doctor
# relatava o vazio e calava a
# recusa. Lista no disco não é
# projeto criado.
CREATE_FOLDER = re.compile(r"não cria a pasta")


def recipe_refuses_map_as_creating_folder(text):
    return bool(text and CREATE_FOLDER.search(text))


def doctor_empty_folder_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_map_as_creating_folder(text):
        return "recipes/create.md"
    return None


def doctor_empty_folder_scope():
    if not doctor_empty_folder_source():
        return None
    return (
        " O disco recusa que o mapa crie a pasta "
        "(`pasta`). Lista no disco não é projeto criado."
    )


def doctor_empty_scope():
    scope = (
        "laboratório sem jogo reconhecido. "
        "Não cria a pasta."
    )
    named = doctor_empty_folder_scope()
    if named:
        scope += named
    return scope


def doctor_empty_flag(reading):
    empty = (reading or {}).get("empty")
    if isinstance(empty, dict):
        return bool(empty.get("empty"))
    return bool(empty)


# A receita já recusa que a lista
# bloqueante comprove que um
# projeto funciona. Sem isto o
# doctor relatava o blocking e
# calava a recusa. Checagem no
# disco não é o jogo.
DOCTOR_WORKS = re.compile(r"não comprova que um projeto funciona")


def recipe_refuses_blocking_as_proving_game(text):
    return bool(text and DOCTOR_WORKS.search(text))


def doctor_blocking_game_source():
    path = CREATE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_blocking_as_proving_game(text):
        return "recipes/create.md"
    return None


def doctor_blocking_game_scope():
    if not doctor_blocking_game_source():
        return None
    return (
        " O disco recusa que a lista bloqueante comprove que um projeto funciona "
        "(`funciona`). Checagem no disco não é o jogo."
    )


def doctor_blocking_scope():
    scope = (
        "checagens obrigatórias que falharam. "
        "O doctor não comprova que um projeto funciona."
    )
    named = doctor_blocking_game_scope()
    if named:
        scope += named
    return scope


def doctor_blocking_names(reading):
    blocking = (reading or {}).get("blocking") if isinstance(reading, dict) else reading
    if isinstance(blocking, dict):
        return list(blocking.get("blocking") or [])
    return list(blocking or [])


def doctor_blocking_reading(blocking):
    if not blocking:
        return blocking
    return {
        "blocking": list(blocking),
        "scope": doctor_blocking_scope(),
    }


# A ambição já recusa que o harness seja motor. Sem isto o
# then apontava o mapa e calava a recusa.
# Convite no then não é runtime.
AMBITION_ENGINE = re.compile(r"não é um motor AAA")


def ambition_refuses_engine(text):
    return bool(text and AMBITION_ENGINE.search(text))


def doctor_then_engine_source():
    path = FRAMEWORK / "references/ambition.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if ambition_refuses_engine(text):
        return "references/ambition.md"
    return None


def doctor_then_scope():
    scope = (
        "Convite ao mapa ideia→ciclo. Não cria o projeto e não executa o jogo."
    )
    if doctor_then_engine_source():
        scope += (
            " O disco recusa que o harness seja motor (`motor`). "
            "Convite no then não é runtime."
        )
    return scope


def doctor_then(ready, starters, empty):
    # Sem jogo e com starter, o primeiro comando aponta o mapa. Com jogo,
    # `play` sem caminho já resolve. Sem starter não há o que mapear.
    # Sem `prompt`: o CLI do doctor não escreve stderr.
    if not ready or not starters or not empty:
        return None
    # Sem --idea o guide na raiz do framework recusa. Apontar o
    # comando nu era o primeiro passo quebrado depois do doctor.
    # O README já imprime o exemplo; <fantasia> calava a frase.
    report = {"guide": harness_command("guide", "--idea", doctor_guide_idea())}
    report["scope"] = doctor_then_scope()
    return report


# O processo já pede uma ação recomendada. Sem isto o
# next propunha e calava o pedido.
# Proposta no disco não é autorização.
NEXT_PROCESS = FRAMEWORK / "references/process.md"
NEXT_ACTION = re.compile(r"uma ação recomendada")


def process_asks_one_action(text):
    return bool(text and NEXT_ACTION.search(text))


def next_action_source():
    path = NEXT_PROCESS
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_asks_one_action(text):
        return "references/process.md"
    return None


def next_scope():
    scope = (
        "Proposta ordenada por dependência, derivada só do que é observável no disco. "
        "Não é fila validada, não conhece a conversa, a direção do usuário nem o backlog, "
        "e não concede autorização. "
        "O agente confronta a proposta com o pedido real e decide; `alternatives` existe para ser escolhida."
    )
    if next_action_source():
        scope += (
            " O disco pede uma ação recomendada (`ação`). "
            "Proposta no disco não é autorização."
        )
    named = next_round_scope()
    if named:
        scope += named
    return scope


# O fluxo já recusa que melhorar o
# jogo seja uma rodada executável.
# Sem isto o next propunha e calava
# a recusa. Pedido no disco não é
# o recorte.
WORKFLOW_ROUND = re.compile(r"não é uma rodada executável")


def workflow_refuses_improve_as_round(text):
    return bool(text and WORKFLOW_ROUND.search(text))


def next_round_source():
    path = CREATIVE_WORKFLOW
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if workflow_refuses_improve_as_round(text):
        return "references/creative-workflow.md"
    return None


def next_round_scope():
    if not next_round_source():
        return None
    return (
        " O disco recusa que melhorar o jogo seja uma rodada executável "
        "(`rodada`). Pedido no disco não é o recorte."
    )


# A receita já recusa que nome de comando prove a conclusão.
# Sem isto o next copiava os sinais e calava a recusa.
# Sinal no disco não é o término.
ARCHITECTURE_CONCLUSION = re.compile(r"não comprovam conclusão nem aprovação")


def recipe_refuses_name_as_conclusion(text):
    return bool(text and ARCHITECTURE_CONCLUSION.search(text))


def next_signals_conclusion_source():
    path = ARCHITECTURE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_name_as_conclusion(text):
        return "recipes/architecture.md"
    return None


def next_signals_scope():
    if not next_signals_conclusion_source():
        return None
    return (
        "O disco recusa que nome de comando, arquivo ou fase prove a conclusão "
        "(`conclusão`). Sinal no disco não é o término."
    )


# O roteiro já recusa que o comando crie o jogo. Sem isto a
# proposta copiava a ação e calava a recusa.
# Proposta no disco não é pasta criada.
PREPRODUCTION_CREATE = re.compile(r"não preenche design")


def preproduction_refuses_create(text):
    return bool(text and PREPRODUCTION_CREATE.search(text))


def proposal_create_source():
    path = FRAMEWORK / "references/preproduction.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if preproduction_refuses_create(text):
        return "references/preproduction.md"
    return None


# O next já recusa que fonte encontrada seja
# tarefa validada. Sem isto a proposta
# copiava a ação e calava a recusa.
# Fonte no disco não é a tarefa.
NEXT_VALIDATED = re.compile(r"fonte encontrada não é tarefa validada")


def next_refuses_found_source_as_validated_task(text):
    return bool(text and NEXT_VALIDATED.search(text))


def proposal_validated_source():
    path = FRAMEWORK / "commands" / "next.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if next_refuses_found_source_as_validated_task(text):
        return "commands/next.md"
    return None


def proposal_validated_scope():
    if not proposal_validated_source():
        return ""
    return (
        " O disco recusa que fonte encontrada seja tarefa validada (`validada`). "
        "Fonte no disco não é a tarefa."
    )


def proposal_scope():
    scope = (
        "Uma ação derivada do disco. Não executa o comando e não cria o projeto."
    )
    if proposal_create_source():
        scope += (
            " O disco recusa que o comando crie o jogo (`criação`). "
            "Proposta no disco não é pasta criada."
        )
    validated = proposal_validated_scope()
    if validated:
        scope += validated
    return scope


# O processo já recusa fabricar tarefa para cumprir o formato.
# Sem isto a alternativa copiava a ação e calava a recusa.
# Lista no disco não é backlog.
PROCESS_TASK = re.compile(r"não fabrique uma tarefa")


def process_refuses_task(text):
    return bool(text and PROCESS_TASK.search(text))


def alternative_task_source():
    path = FRAMEWORK / "references/process.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_task(text):
        return "references/process.md"
    return None


def alternative_scope():
    scope = (
        "Outra ação derivada do disco. Não executa o comando e não "
        "fabrica backlog."
    )
    if alternative_task_source():
        scope += (
            " O disco recusa que a alternativa fabrique tarefa (`fabricação`). "
            "Lista no disco não é backlog."
        )
    stage = alternative_stage_scope()
    if stage:
        scope += stage
    return scope


# O processo já recusa que comando
# registrado com falha ou proposta
# rejeitada conclua a etapa. Sem
# isto a alternativa copiava a
# ação e calava a recusa. Proposta
# no disco não é a etapa.
PROCESS_STAGE = re.compile(
    r"Um comando registrado com falha ou uma proposta rejeitada não conclui a etapa"
)


def process_refuses_failed_command_as_stage(text):
    return bool(text and PROCESS_STAGE.search(text))


def alternative_stage_source():
    path = FRAMEWORK / "references" / "process.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_failed_command_as_stage(text):
        return "references/process.md"
    return None


def alternative_stage_scope():
    if not alternative_stage_source():
        return ""
    return (
        " O disco recusa que comando registrado com falha ou uma proposta "
        "rejeitada conclua a etapa (`etapa`). Proposta no disco não é a etapa."
    )


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
    play = play_command(project, payload["scripts"], payload["package_manager"])
    # Não localizado, rascunho e histórico são três problemas diferentes, e todos
    # aparecem em `gaps`. Propor os três de uma vez repetiria a mesma tarefa.
    # Jogo que já abre não espera template: o buraco só bloqueia quem ainda
    # não tem comando de jogar. Senão o `start` teria de plantar sete
    # rascunhos só para o `next` recusar preenchê-los.
    if missing and not play:
        propose(
            "Avisar as lacunas e documentar as áreas não localizadas: " + labels(missing),
            "A política do estúdio é documentar sem pedir um segundo consentimento; sem essa base as mesmas decisões se repetem a cada sessão.",
            "Cada área tem decisão com fonte, hipótese identificada ou lacuna com motivo e próxima ação.",
            [harness_command("context", project, "--focus", focus, "--event", "direction-approved")],
            "areas.not_located",
        )
    noted = bool(observation_receipts(project))
    fresh = fresh_starter_cycle(project, missing, play) and not noted
    if fresh:
        propose(
            "Abrir o ciclo do starter e escrever o que a proposta muda no verbo",
            "O destino já é um jogo que abre. Com tela, o avanço abre a porta; "
            "sem tela o headless já joga. Rascunhos de template antes da primeira "
            "partida são o atrito que este passo existe para cortar. O `start` "
            "não os planta. O harness não executa o jogo.",
            "O ciclo correu uma vez, e o brief (ou um recibo de observação) registra o que "
            "esta proposta muda no verbo — ou a lacuna, se ainda não souber.",
            [play, note_command(project)],
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
    empty_roles = roles_empty_ids(roles)
    if empty_roles:
        sample = ", ".join(f"`{name}`" for name in empty_roles[:4])
        extra = " e mais" if len(empty_roles) > 4 else ""
        commands = [harness_command("roles", project, "--fill")]
        can_apply = roles_catalog_exists_flag(roles) or any(
            sfx_catalog.find_local_stem(name) for name in empty_roles
        )
        if can_apply:
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
        named = feel_constant_items(feel)
        sample = ", ".join(f"`{item['key']}`" for item in named[:4])
        extra = " e mais" if len(named) > 4 else ""
        propose(
            f"Registrar o que o verbo sentiu numa partida ({sample}{extra})",
            "Há constantes de feel no código e nenhum recibo de observação no "
            "projeto. Constante nomeada não é peso percebido. O harness não joga.",
            "Existe um `note` (ou `record --kind observation`) sob o projeto, "
            "com cenário, role e o que mudou (ou não) no verbo — ou a lacuna, "
            "se ainda não souber.",
            [
                harness_command("feel", project),
                # O then.note já anexa o candidato. Sem isto o next
                # do feel calava o last-run e o ofício pedia a nota
                # sem a partida. Recibo sem corrida não é felt.
                note_command(project),
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
            "campos. `playtest` só lê. A página do convite (`/?invite=1#finding`) e "
            "`note --field` escrevem. Sem o convite o âncora some. "
            "O serve nu não abre o painel. O comando nomeia o endereço. "
            "Nota de partida não é métrica. "
            "last-run.json é candidato, não causa. O harness não assistiu "
            "à sessão e não conta jogadores.",
            "Um documento ou o próprio recibo nomeia problema, evidência, "
            "hipótese e medição — a causa e o tamanho do efeito continuam "
            "pendentes.",
            [
                play or harness_command("play", project),
                finding_open(project, payload["scripts"], play),
                harness_command(
                    "note", project, "--author", note_author(project),
                    "--note", "o achado com os quatro nomes",
                    "--field", "problema=o que quebrou o verbo",
                    "--field", "evidencia=o que a partida mostrou",
                    "--field", "hipotese=por que isso acontece",
                    "--field", "medicao=como repetir o recorte",
                    *(["--from-run"] if playtest_candidate_path(playtest) else []),
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
    if save_unversioned_flag(persist):
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
    if budget_unbudgeted_flag(perf):
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
    if ship_unpacked_flag(pack):
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
    elif pack.get("incomplete"):
        parts = (pack.get("tree") or {}).get("parts") or {}
        listed = "index, serve, package e VERSION"
        if "src" in parts:
            listed = "index, serve, package, VERSION e o src que o projeto já tem"
        propose(
            f"Completar a árvore jogável em dist/ ({listed})",
            "Há identidade do artefato ou uma pasta dist/ e falta o que outra "
            "pessoa serve. VERSION.json sozinho não abre o jogo. dist/ sem o "
            "src/ que o projeto já tem também não. O harness "
            "não executa o export e não autoriza publicar.",
            "dist/ tem index.html, tools/serve.mjs, package.json, "
            "VERSION.json e o src/ que o desenvolvimento já tem — outra "
            "máquina e shipped continuam pendentes."
            if "src" in parts else
            "dist/ tem index.html, tools/serve.mjs, package.json e "
            "VERSION.json — outra máquina e shipped continuam pendentes.",
            [harness_command("ship", project)],
            "ship.incomplete",
        )
    elif pack.get("stale"):
        propose(
            "Gerar de novo o artefato a partir do HEAD atual",
            "dist/VERSION.json nomeia um HEAD que não é o deste checkout. "
            "Artefato de outro commit não é esta entrega. O harness não "
            "executa o export e não autoriza publicar.",
            "O git_head do VERSION.json é o HEAD atual — outra máquina e "
            "shipped continuam pendentes.",
            [harness_command("ship", project)],
            "ship.stale",
        )
    elif ship_open_command(pack):
        propose(
            "Servir a árvore em dist/ no próprio dispositivo",
            "A árvore exportada está completa e no HEAD atual. "
            "Servir aqui não é outra máquina. O harness não executa o "
            "artefato e não autoriza publicar.",
            "Alguém correu o dist/ fora daqui — elsewhere e shipped "
            "continuam pendentes.",
            [ship_open_command(pack), harness_command("ship", project)],
            "ship.artifact_open",
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
            "AGENTS.md cita o comando que abre, o note, o playtest e o que o disco ainda não tem. Sem rascunhos plantados, não lista GDD.",
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
    undeclared = origin_undeclared_paths(origins)
    if undeclared:
        sample = ", ".join(f"`{path}`" for path in undeclared[:4])
        extra = " e mais" if len(undeclared) > 4 else ""
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
        first = undeclared[0]
        propose(
            f"Declarar origem dos arquivos embarcados sem recibo: {sample}{extra}",
            why,
            "Cada arquivo listado tem recibo ao lado (sources.json, CREDITS ou "
            "`.credits.txt`) com origem, autor e condição de uso — ou sai do embarque.",
            [harness_command(
                "origins", project, "--declare", first,
                "--origin", "de onde veio o arquivo",
                "--author", note_author(project),
                "--license", "condição de uso",
            )],
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
    report = {
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
            "origins_undeclared": origin_undeclared_paths(origins),
            "origins_contradicts_licensing": origins["contradicts_licensing"],
            "playable_unplayed": fresh,
            "cycle_craft": wants_craft,
            "audio_roles_empty": roles_empty_ids(roles),
            "feel_unobserved": feel_unobserved_flag(feel),
            "playtest_unstructured": playtest["unstructured"],
            "playtest_invite": wants_invite,
            "playtest_candidate": playtest_candidate_path(playtest),
            "access_missing": access_missing_keys(access) if payload["kind"] else [],
            "save_unversioned": save_unversioned_flag(persist),
            "performance_unbudgeted": budget_unbudgeted_flag(perf),
            "art_missing": bool(payload["kind"]) and not art["declared"],
            "content_inline": content_inline_flag(inventory),
            "ship_unpacked": ship_unpacked_flag(pack),
            "craft_pending": [
                key for key, spec in CRAFT_CHECKS.items()
                if spec["gate"] in gates["declared"]
                and craft["declared"].get(key, {}).get("state", "undeclared") in ("undeclared", "unmet")
            ],
        },
        "context_command": harness_command("context", project, "--focus", focus),
        "authority": "agent_resolves",
        "executed": False,
        "scope": next_scope(),
    }
    if report["proposal"]:
        report["proposal"]["scope"] = proposal_scope()
    for item in report["alternatives"]:
        item["scope"] = alternative_scope()
    named = next_signals_scope()
    if named:
        report["signals"]["scope"] = named
    return report


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


# O processo já recusa garantir o mérito. Sem isto o
# check-plan validava a forma e calava a recusa.
# Forma no disco não é adequação.
PROCESS_MERIT = re.compile(r"não garantem mérito")


def process_refuses_merit(text):
    return bool(text and PROCESS_MERIT.search(text))


def check_plan_merit_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_merit(text):
        return "references/process.md"
    return None


def check_plan_scope():
    scope = (
        "Estrutura e existência dos candidatos; busca, adequação e qualidade exigem revisão."
    )
    if check_plan_merit_source():
        scope += (
            " O disco recusa garantir o mérito (`mérito`). "
            "Forma no disco não é adequação."
        )
    named = check_plan_names_scope()
    if named:
        scope += named
    return scope


# O processo já recusa que três nomes
# parecidos bastem. Sem isto o
# check-plan validava a forma e calava
# a recusa. Nome no disco não é a
# camada.
PROCESS_NAMES = re.compile(r"três nomes parecidos não bastam")


def process_refuses_similar_names_as_extraction(text):
    return bool(text and PROCESS_NAMES.search(text))


def check_plan_names_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_similar_names_as_extraction(text):
        return "references/process.md"
    return None


def check_plan_names_scope():
    if not check_plan_names_source():
        return None
    return (
        " O disco recusa que três nomes parecidos bastem "
        "(`nomes`). Nome no disco não é a camada."
    )


# O processo já recusa que o contrato
# válido garanta obediência. Sem isto
# o check-plan relatava o
# contract_valid e calava a recusa.
# Forma no disco não é o processo.
PROCESS_OBEY = re.compile(r"mérito ou obediência")


def process_refuses_valid_contract_as_obedience(text):
    return bool(text and PROCESS_OBEY.search(text))


def check_plan_valid_obedience_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_valid_contract_as_obedience(text):
        return "references/process.md"
    return None


def check_plan_valid_obedience_scope():
    if not check_plan_valid_obedience_source():
        return None
    return (
        " O disco recusa que o contrato válido garanta obediência "
        "(`obediência`). Forma no disco não é o processo."
    )


def check_plan_valid_scope():
    scope = (
        "forma e caminhos do contrato. "
        "O check-plan não garante obediência."
    )
    named = check_plan_valid_obedience_scope()
    if named:
        scope += named
    return scope


def check_plan_valid_flag(reading):
    valid = (reading or {}).get("contract_valid") if isinstance(reading, dict) else reading
    if isinstance(valid, dict):
        return bool(valid.get("contract_valid"))
    return bool(valid)


def check_plan_valid_reading(valid):
    if not valid:
        return False
    return {
        "contract_valid": True,
        "scope": check_plan_valid_scope(),
    }


def check_plan_report(plan, root):
    errors = check_plan(plan, root)
    return {
        "contract_valid": check_plan_valid_reading(not errors),
        "errors": errors,
        "scope": check_plan_scope(),
    }


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


# O roteiro já recusa que o HEAD substitua o julgamento. Sem isto
# o version relatava o HEAD e calava a recusa.
# Identidade no disco não é avaliação.
JUDGMENT_GUIDE = FRAMEWORK / "references/quality.md"
VERSION_JUDGMENT = re.compile(r"não substitui o julgamento")


def quality_refuses_judgment(text):
    return bool(text and VERSION_JUDGMENT.search(text))


def git_judgment_source():
    path = JUDGMENT_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if quality_refuses_judgment(text):
        return "references/quality.md"
    return None


def git_version_scope():
    scope = "HEAD e nomes alterados; não é fingerprint completo das fontes."
    if git_judgment_source():
        scope += (
            " O disco recusa que o HEAD substitua o julgamento (`julgamento`). "
            "Identidade no disco não é avaliação."
        )
    return scope


def git_version(project):
    result = {}
    for key, args in (("head", ["rev-parse", "HEAD"]), ("status", ["status", "--porcelain", "--", "."])):
        run = subprocess.run(["git", "-C", str(project), *args], capture_output=True, text=True, check=False)
        result[key] = run.stdout.strip() if run.returncode == 0 else None
    result["scope"] = git_version_scope()
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


# O roteiro já recusa aprovar a criatividade. Sem isto o
# verify executava o comando e calava a recusa.
# Recibo verde não é aprovação.
PREPRODUCTION_GUIDE = FRAMEWORK / "references/preproduction.md"
VERIFY_CREATIVITY = re.compile(r"não aprova criatividade")


def preproduction_refuses_creativity(text):
    return bool(text and VERIFY_CREATIVITY.search(text))


def verify_creativity_source():
    path = PREPRODUCTION_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if preproduction_refuses_creativity(text):
        return "references/preproduction.md"
    return None


def verify_scope():
    scope = (
        "Execução dos comandos solicitados. Não aprova arte, diversão, direitos, "
        "release nem capacidades do runtime."
    )
    if verify_creativity_source():
        scope += (
            " O disco recusa aprovar a criatividade (`criatividade`). "
            "Recibo verde não é aprovação."
        )
    named = verify_connectivity_scope()
    if named:
        scope += named
    return scope


# A receita já recusa que teste unitário
# de serialização prove conectividade real.
# Sem isto o verify executava o comando e
# calava a recusa. Recibo verde não é
# sessão real.
NETWORK_CONNECTIVITY = re.compile(r"não prova conectividade real")


def recipe_refuses_unit_test_as_connectivity(text):
    return bool(text and NETWORK_CONNECTIVITY.search(text))


def verify_connectivity_source():
    path = FRAMEWORK / "recipes/network.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_unit_test_as_connectivity(text):
        return "recipes/network.md"
    return None


def verify_connectivity_scope():
    if not verify_connectivity_source():
        return None
    return (
        " O disco recusa que teste unitário de serialização prove "
        "conectividade real (`conectividade`). Recibo verde não é sessão real."
    )


# A ambição já recusa que o recibo comprove diversão. Sem isto o
# comando copiava o exit code e calava a recusa.
# Log no disco não é experiência.
AMBITION_FUN = re.compile(r"não comprova diversão")


def ambition_refuses_fun(text):
    return bool(text and AMBITION_FUN.search(text))


def verify_command_fun_source():
    path = FRAMEWORK / "references/ambition.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if ambition_refuses_fun(text):
        return "references/ambition.md"
    return None


def verify_command_scope():
    scope = (
        "Saída de um comando técnico. Não observa o jogo e não avalia "
        "experiência."
    )
    if verify_command_fun_source():
        scope += (
            " O disco recusa que o recibo comprove diversão (`diversão`). "
            "Log no disco não é experiência."
        )
    if verify_command_meaning_source():
        scope += (
            " O disco recusa que o hash comprove o significado "
            "(`significado`). Hash no disco não é o critério."
        )
    return scope


# A entrega já recusa que o hash comprove o significado. Sem isto o
# comando copiava o sha256 e calava a recusa.
# Hash no disco não é o critério.
DELIVERY_MEANING = re.compile(r"não comprova seu significado")


def delivery_refuses_hash_as_meaning(text):
    return bool(text and DELIVERY_MEANING.search(text))


def verify_command_meaning_source():
    path = DELIVERY_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if delivery_refuses_hash_as_meaning(text):
        return "references/delivery.md"
    return None


# O processo já recusa que claimed seja verified. Sem isto o
# verify alegava a capacidade e calava a recusa.
# Alegação no disco não é cobertura.
PROCESS_CLAIMED = re.compile(r"claimed` não é `verified")


def process_refuses_claimed_as_verified(text):
    return bool(text and PROCESS_CLAIMED.search(text))


def verify_claimed_source():
    path = PROCESS_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if process_refuses_claimed_as_verified(text):
        return "references/process.md"
    return None


def capabilities_scope():
    scope = (
        "Capacidade só aparece aqui porque quem executou a declarou em --proves. O harness confere que o nome "
        "pertence ao conjunto conhecido e que os comandos passaram; não confere que eles a exercitam. "
        "`claimed` é alegação registrada, não verificação: continua valendo que mentioned não é verified."
    )
    if verify_claimed_source():
        scope += (
            " O disco recusa que claimed seja verified (`verified`). "
            "Alegação no disco não é cobertura."
        )
    return scope


# A receita já recusa que o registro declarado prove suporte real.
# Sem isto o item copiava claimed e calava a recusa.
# Registro no disco não é o consumidor.
ARCHITECTURE_SUPPORT = re.compile(r"registro declarado não prova suporte real")


def architecture_refuses_declared_support(text):
    return bool(text and ARCHITECTURE_SUPPORT.search(text))


def capability_claim_support_source():
    path = ARCHITECTURE_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if architecture_refuses_declared_support(text):
        return "recipes/architecture.md"
    return None


def capability_claim_scope():
    scope = (
        "Alegação desta capacidade no recibo. Não confirma o "
        "consumidor e não exercita o runtime."
    )
    if capability_claim_support_source():
        scope += (
            " O disco recusa que o registro declarado prove suporte "
            "real (`suporte`). Registro no disco não é o consumidor."
        )
    return scope


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
    report = {"schema_version": 1, "project": str(project), "started_at": datetime.now(timezone.utc).isoformat(), "version": before, "technical_status": "running", "experience_status": "not_assessed", "commands": [], "scope": verify_scope()}
    receipt = output / "verification.json"
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for index, argv in enumerate(commands):
        print(f"Executando: {argv} em {project}", file=sys.stderr, flush=True)
        result = run_command(argv, project, output / f"{index + 1:02d}.log", timeout)
        result["scope"] = verify_command_scope()
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
            "scope": capability_claim_scope(),
        }
        for name in claimed
    }
    report["capabilities_scope"] = capabilities_scope()
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


# O roteiro já recusa medir os critérios. Sem isto o
# record gravava o recibo e calava a recusa.
# Recibo no disco não é observação.
QUALITY_GUIDE = FRAMEWORK / "references/quality.md"
QUALITY_MEASURE = re.compile(r"O harness não os\s+mede")


def quality_refuses_measure(text):
    return bool(text and QUALITY_MEASURE.search(text))


def quality_measure_source():
    path = QUALITY_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if quality_refuses_measure(text):
        return "references/quality.md"
    return None


def record_scope():
    scope = (
        "Registro declarado por quem assina; o harness não valida o conteúdo, não mede e não aprova. "
        "role=agent é avaliação do agente, não aprovação do usuário."
    )
    if quality_measure_source():
        scope += (
            " O disco recusa medir os critérios (`mede`). "
            "Recibo no disco não é observação."
        )
    kernel = record_solver_scope()
    if kernel:
        scope += kernel
    grid = record_matrix_scope()
    if grid:
        scope += grid
    aim = record_target_scope()
    if aim:
        scope += aim
    return scope


# A receita já recusa que um
# grande ganho no caso
# rejeitado seja ganho
# equivalente no solver ativo.
# Sem isto o record gravava o
# recibo e calava a recusa.
# Ganho rejeitado no disco
# não é o solver.
PERF_SOLVER = re.compile(r"não é ganho equivalente no solver ativo")


def recipe_refuses_rejected_gain_as_active_solver(text):
    return bool(text and PERF_SOLVER.search(text))


def record_solver_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_rejected_gain_as_active_solver(text):
        return "recipes/performance.md"
    return None


def record_solver_scope():
    if not record_solver_source():
        return None
    return (
        " O disco recusa que o ganho no caso rejeitado seja ganho equivalente no solver ativo "
        "(`solver`). Ganho rejeitado no disco não é o solver."
    )


# A receita já recusa que cenas
# dinâmicas virem estáticas
# porque a matriz local ficou
# igual. Sem isto o record
# gravava o recibo e calava a
# recusa. Matriz no disco não
# é a cena.
PERF_MATRIX = re.compile(
    r"Cenas dinâmicas não viram estáticas porque a matriz local ficou igual"
)


def recipe_refuses_equal_matrix_as_static_scene(text):
    return bool(text and PERF_MATRIX.search(text))


def record_matrix_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_equal_matrix_as_static_scene(text):
        return "recipes/performance.md"
    return None


def record_matrix_scope():
    if not record_matrix_source():
        return None
    return (
        " O disco recusa que cenas dinâmicas virem estáticas porque a matriz local ficou igual "
        "(`matriz`). Matriz no disco não é a cena."
    )


# A receita já recusa que o
# editor seja build exportado.
# Sem isto o record gravava o
# recibo e calava a recusa.
# Editor no disco não é o
# build.
PERF_TARGET = re.compile(r"Editor não é build exportado")


def recipe_refuses_editor_as_exported_build(text):
    return bool(text and PERF_TARGET.search(text))


def record_target_source():
    path = FRAMEWORK / "recipes/performance.md"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_editor_as_exported_build(text):
        return "recipes/performance.md"
    return None


def record_target_scope():
    if not record_target_source():
        return None
    return (
        " O disco recusa que o editor seja build exportado "
        "(`alvo`). Editor no disco não é o build."
    )


# A receita já recusa que ganho na média
# demonstre redução de engasgos. Sem isto o
# fields do budget copiava o número e calava
# a recusa. Número no disco não é o quadro
# estável.
PERF_RECIPE = FRAMEWORK / "recipes/performance.md"
PERF_STUTTER = re.compile(r"não demonstra redução de engasgos")


def recipe_refuses_average_as_stutter_reduction(text):
    return bool(text and PERF_STUTTER.search(text))


def record_budget_stutter_source():
    path = PERF_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_average_as_stutter_reduction(text):
        return "recipes/performance.md"
    return None


def record_budget_fields_scope(kind):
    if kind != "budget":
        return None
    scope = None
    if record_budget_stutter_source():
        scope = (
            "O disco recusa que ganho na média demonstre redução de engasgos "
            "(`engasgos`). Número no disco não é o quadro estável."
        )
    named = record_budget_hot_scope()
    if named:
        scope = (scope + " " + named) if scope else named
    return scope


# A receita já recusa que a máquina
# quente seja a máquina do jogador
# fria. Sem isto o fields do budget
# copiava a plataforma e calava a
# recusa. Plataforma no disco não é
# a máquina fria.
PERF_HOT = re.compile(r"máquina de desenvolvimento\s+quente não é máquina do jogador fria")


def recipe_refuses_hot_as_cold_player(text):
    return bool(text and PERF_HOT.search(text))


def record_budget_hot_source():
    path = PERF_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_hot_as_cold_player(text):
        return "recipes/performance.md"
    return None


def record_budget_hot_scope():
    if not record_budget_hot_source():
        return None
    return (
        "O disco recusa que a máquina de desenvolvimento quente seja a "
        "máquina do jogador fria (`quente`). Plataforma no disco não é a "
        "máquina fria."
    )


# A receita já recusa que o recibo feche o
# marco. Sem isto o fields do milestone
# copiava a decisão e calava a recusa.
# Recibo no disco não é a passagem.
PROD_RECIPE = FRAMEWORK / "recipes/production.md"
PROD_MILESTONE = re.compile(r"não fecham marco nem certificam")


def recipe_refuses_receipt_as_milestone(text):
    return bool(text and PROD_MILESTONE.search(text))


def record_milestone_gate_source():
    path = PROD_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_receipt_as_milestone(text):
        return "recipes/production.md"
    return None


def record_milestone_fields_scope(kind):
    if kind != "milestone":
        return None
    if not record_milestone_gate_source():
        return None
    return (
        "O disco recusa que o recibo feche o marco "
        "(`marco`). Recibo no disco não é a passagem."
    )


# A receita já recusa que o recibo sem os
# quatro seja achado. Sem isto o fields da
# observation copiava cenário e papel e
# calava a recusa. Recibo no disco não é
# playtest.
FEEL_IMPRESSION = re.compile(r"Recibo sem os quatro é\s+impressão")


def recipe_refuses_receipt_as_finding(text):
    return bool(text and FEEL_IMPRESSION.search(text))


def record_observation_impression_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_receipt_as_finding(text):
        return "recipes/feel.md"
    return None


def record_observation_fields_scope(kind):
    if kind != "observation":
        return None
    if not record_observation_impression_source():
        return None
    return (
        "O disco recusa que o recibo sem os quatro seja achado "
        "(`impressão`). Recibo no disco não é playtest."
    )


# O roteiro já recusa que o screenshot isolado comprove animação. Sem isto o
# anexo copiava o hash e calava a recusa.
# Anexo no disco não é controle.
QUALITY_STILL = re.compile(r"não comprova animação")


def quality_refuses_isolated_still(text):
    return bool(text and QUALITY_STILL.search(text))


def record_attachment_still_source():
    path = QUALITY_GUIDE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if quality_refuses_isolated_still(text):
        return "references/quality.md"
    return None


def record_attachment_scope():
    scope = (
        "Bytes e hash do arquivo anexado. Não observa o jogo e não "
        "aprova o movimento."
    )
    if record_attachment_still_source():
        scope += (
            " O disco recusa que o screenshot isolado comprove animação (`animação`). "
            "Anexo no disco não é controle."
        )
    fidelity = record_attachment_fidelity_scope()
    if fidelity:
        scope += fidelity
    return scope


# A receita já recusa que bytes menores
# provem fidelidade. Sem isto o anexo
# copiava os bytes e calava a recusa.
# Anexo no disco não é a trajetória.
PERF_FIDELITY = re.compile(r"Bytes menores não provam fidelidade")


def recipe_refuses_smaller_bytes_as_fidelity(text):
    return bool(text and PERF_FIDELITY.search(text))


def record_attachment_fidelity_source():
    path = PERF_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_smaller_bytes_as_fidelity(text):
        return "recipes/performance.md"
    return None


def record_attachment_fidelity_scope():
    if not record_attachment_fidelity_source():
        return None
    return (
        " O disco recusa que bytes menores provem fidelidade (`fidelidade`). "
        "Anexo no disco não é a trajetória."
    )


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
    named = (
        record_budget_fields_scope(kind)
        or record_milestone_fields_scope(kind)
        or record_observation_fields_scope(kind)
    )
    if named:
        fields = dict(fields, scope=named)
    files = []
    for item in attachments:
        path = Path(item)
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"anexo inexistente ou symlink: {item}")
        data = path.read_bytes()
        files.append({
            "path": str(path.resolve()),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "scope": record_attachment_scope(),
        })
    if output.exists() or output.is_symlink():
        raise ValueError("destino de evidência existente; escolha um novo")
    report = {
        "schema_version": 1, "kind": kind, "project": str(project), "recorded_at": datetime.now(timezone.utc).isoformat(),
        "version": git_version(project), "author": author, "note": note, "fields": fields, "attachments": files,
        "status": "declared",
        "scope": record_scope(),
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / "record.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


# A receita já recusa que o recibo
# com os quatro seja achado. Sem
# isto o note relatava o finding e
# calava a recusa. Arquivo no disco
# não é a sessão.
NOTE_FINDING = re.compile(r"recibo com os quatro não é achado")


def recipe_refuses_complete_receipt_as_finding(text):
    return bool(text and NOTE_FINDING.search(text))


def note_finding_found_source():
    path = FEEL_RECIPE
    if not path.is_file() or path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if recipe_refuses_complete_receipt_as_finding(text):
        return "recipes/feel.md"
    return None


def note_finding_found_scope():
    if not note_finding_found_source():
        return None
    return (
        " O disco recusa que o recibo com os quatro seja achado "
        "(`achado`). Arquivo no disco não é a sessão."
    )


def note_finding_scope():
    scope = (
        "os quatro campos no recibo. "
        "O recibo com os quatro não é achado."
    )
    named = note_finding_found_scope()
    if named:
        scope += named
    return scope


def note_finding_flag(reading):
    finding = (reading or {}).get("finding")
    if isinstance(finding, dict):
        return bool(finding.get("finding"))
    return bool(finding)


def note_finding_reading(finding):
    if not finding:
        return False
    return {
        "finding": True,
        "scope": note_finding_scope(),
    }


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
    # O playtest já nomeia o esqueleto. Sem isto o note gravava e
    # some se os quatro fecharam o achado. Recibo sem forma não é
    # achado. Sem `then`: este comando escreve, não aponta o leitor.
    complete = fields_have_finding(payload)
    report["finding"] = note_finding_reading(complete)
    report["form"] = str(PLAYTEST_FORM)
    report["needed"] = [] if complete else list(PLAYTEST_FIELDS)
    if attached is not None:
        report["from_run"] = attached.as_posix() if attached.is_absolute() else attached.as_posix()
    # A partida já grava o candidato. Sem isto o note
    # escrevia o recibo e calava o arquivo.
    # Nomear não anexa. Disco não é sessão.
    if not from_run and last_run_path(project):
        report["scope"] += (
            " O disco tem um last-run. Sem --from-run o recibo não anexa o candidato."
        )
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
    # O ofício já é start → jogar → note. Sem isto o -h
    # listava init primeiro e quem lia a ajuda via o
    # ADAPT antes do ciclo. Listar não é criar.
    begin = commands.add_parser(
        "start", parents=[common],
        help="caminho ideia→ciclo: cria se o destino estiver livre e aponta o comando que abre o jogo",
    )
    begin.add_argument("project", nargs="?", default=None)
    begin.add_argument("--starter", default=starters()[0] if starters() else None, choices=starters() or None)
    begin.add_argument("--title", help="título legível; por omissão, derivado do nome da pasta")
    begin.add_argument("--idea", help="frase da fantasia; entra na abertura se houver data/copy.json, sem mudar o verbo. Sem caminho, nomeia e cria a pasta. Brief só com --docs")
    begin.add_argument("--docs", action="store_true", help="criar os rascunhos em docs/; o padrão do start é não plantá-los")
    begin.add_argument("--no-docs", action="store_true", help="não criar os rascunhos em docs/ (já é o padrão do start)")
    guided = commands.add_parser(
        "guide",
        parents=[common],
        help="três passos ideia→ciclo sem executar: start, jogar, note",
    )
    guided.add_argument("project", nargs="?", default=None)
    guided.add_argument("--starter", default=starters()[0] if starters() else None, choices=starters() or None)
    guided.add_argument("--idea", help="frase da fantasia; só entra no comando do start, não no disco")
    played = commands.add_parser(
        "play",
        aliases=["open"],
        parents=[common],
        help="aponta o comando que abre o jogo, sem executar; sem caminho, o único jogo do laboratório basta",
    )
    played.add_argument("project", nargs="?", default=None)
    start = commands.add_parser("init", parents=[common], help="cria um projeto novo a partir de um starter, para ADAPT")
    start.add_argument("project")
    start.add_argument("--starter", default=starters()[0] if starters() else None, choices=starters() or None)
    start.add_argument("--title", help="título legível; por omissão, derivado do nome da pasta")
    start.add_argument("--idea", help="frase da fantasia; entra no brief, na abertura e no aviso do primeiro ciclo, sem mudar o verbo")
    start.add_argument("--no-docs", action="store_true", help="não criar os rascunhos em docs/")
    upcoming = commands.add_parser("next", parents=[common], help="proposta ordenada de próxima ação, a partir do estado no disco")
    upcoming.add_argument("project", nargs="?", default=None)
    upcoming.add_argument("--focus", choices=FOCI, default="create")
    initial_scan = commands.add_parser("scan", parents=[common])
    initial_scan.add_argument("project")
    reading = commands.add_parser("bar", parents=[common], help="degrau de acabamento que o projeto declara, e qual dimensão é o piso")
    reading.add_argument("project")
    origins_cmd = commands.add_parser(
        "origins", parents=[common],
        help="arquivos embarcados, o recibo de origem e a mídia que o recibo lista e o disco perdeu",
        description=(
            "arquivos embarcados, o recibo de origem e a mídia que o recibo lista e o disco perdeu"
        ),
    )
    origins_cmd.add_argument("project")
    origins_cmd.add_argument(
        "--declare", metavar="ARQUIVO",
        help="escreve o sidecar .credits.txt do arquivo embarcado; não valida licença",
    )
    origins_cmd.add_argument("--origin", help="de onde veio o arquivo")
    origins_cmd.add_argument("--author", help="quem fez o arquivo")
    origins_cmd.add_argument("--license", dest="license_name", help="condição de uso declarada")
    craft_cmd = commands.add_parser(
        "craft", parents=[common],
        help="checklists de ofício que o projeto declara cumprir, sem limiar importado",
    )
    craft_cmd.add_argument("project")
    craft_cmd.add_argument("--gate", choices=sorted(GATES), help="só os checklists daquele gate")
    roles_cmd = commands.add_parser(
        "roles", parents=[common],
        help="papéis de áudio que o projeto declara — inclusive o duck — e os arquivos que os preenchem",
        description=(
            "Lê papéis e o duckMs que SOUNDS já declara; nomear não é heard."
        ),
    )
    roles_cmd.add_argument("project")
    roles_cmd.add_argument(
        "--fill", action="store_true",
        help="sugere id do acervo ou a ficha do stem do starter; não copia",
    )
    roles_cmd.add_argument(
        "--apply", action="store_true",
        help="com --fill, copia o id do acervo ou o stem do starter com créditos",
    )
    feel_cmd = commands.add_parser(
        "feel", parents=[common],
        help="constantes de feel que o projeto declara — inclusive rumble, o peso do passo, as janelas da chuva e o rumo que o coil do dash marca — e o recibo de observação no disco",
        description=(
            "Lê constantes de feel (inclusive rumble e o peso do passo), as "
            "janelas da chuva e o rumo que o coil do dash marca; nomear não é felt."
        ),
    )
    feel_cmd.add_argument("project", nargs="?", default=None)
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
        help="lê se o achado tem problema/evidência/hipótese/medição; não grava e não assiste",
    )
    playtest_cmd.add_argument("project", nargs="?", default=None)
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
    ctx.add_argument("--scale", choices=SCALES, help="escala de ambição declarada na conversa (jam, product, aa); sem ela, o campo Escala: do brief só sugere")
    commands.add_parser("commands", parents=[common], help="catálogo dos sub-comandos da skill, com categoria, descrição e referência")
    pin_cmd = commands.add_parser("pin", parents=[common], help="fixa um sub-comando como skill própria do host (/<comando>) nos diretórios onde a game-dev está instalada")
    pin_cmd.add_argument("command")
    unpin_cmd = commands.add_parser("unpin", parents=[common], help="remove o atalho fixado por `pin`; skills próprias do usuário ficam intactas")
    unpin_cmd.add_argument("command")
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
    noted = commands.add_parser(
        "note",
        parents=[common],
        help="recibo curto de observação: o que o verbo sentiu, sem jogar; sem caminho, o único jogo do laboratório basta",
    )
    noted.add_argument("project", nargs="?", default=None)
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
        os.environ["GAMES_WORKSPACE_ROOT"] = str(root)
        if args.action is None:
            dest = here_project()
            require_guide_idea(None, args.idea)
            report = guide_cycle(dest, idea=args.idea)
            report["here"] = guide_here_reading(dest is not None)
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
            emit(init((root / args.project).absolute(), args.starter, args.title, not args.no_docs, args.idea))
        elif args.action == "start":
            dest = None if args.project is None else resolve(args.project, root)
            emit(start_project(dest, args.starter, args.title, args.idea, args.docs and not args.no_docs))
        elif args.action == "guide":
            dest = here_project(args.project, root)
            require_guide_idea(args.project, args.idea)
            report = guide_cycle(dest, args.starter, args.idea)
            report["here"] = guide_here_reading(
                args.project is None and dest is not None
            )
            emit(report)
        elif args.action in ("play", "open"):
            dest = resolve_play_destination(args.project, root)
            emit(play_cycle(dest))
        elif args.action == "next":
            emit(next_step(require_project_destination(args.project, root), args.focus, studies_root=default_studies_root(root)))
        elif args.action == "scan":
            emit(scan(resolve(args.project, root)))
        elif args.action == "bar":
            emit(bar_reading(resolve(args.project, root)))
        elif args.action == "origins":
            target = resolve(args.project, root)
            declared = getattr(args, "declare", None)
            origin = getattr(args, "origin", None)
            author = getattr(args, "author", None)
            license_name = getattr(args, "license_name", None)
            if declared or origin or author or license_name:
                emit(origins_declare(target, declared, origin, author, license_name))
            else:
                emit(origins_reading(target))
        elif args.action == "craft":
            emit(craft_reading(resolve(args.project, root), args.gate))
        elif args.action == "roles":
            target = resolve(args.project, root)
            if args.fill or args.apply:
                emit(roles_fill(target, root, apply=args.apply))
            else:
                emit(roles_reading(target, root))
        elif args.action == "feel":
            emit(feel_reading(require_project_destination(args.project, root)))
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
            dest = require_project_destination(args.project, root)
            emit(invite_playtest(dest) if args.invite else playtest_reading(dest))
        elif args.action == "gate":
            emit(gate_reading(resolve(args.project, root), args.gate))
        elif args.action == "context":
            emit(context(resolve(args.project, root), args.focus, args.stage, studies_root=default_studies_root(root), event=args.event, root=root, genre=args.genre, scale=args.scale))
        elif args.action == "commands":
            emit(command_listing())
        elif args.action == "pin":
            emit(pin(root, args.command))
        elif args.action == "unpin":
            emit(unpin(root, args.command))
        elif args.action == "template":
            document = template(args.stage, resolve(args.project, root), args.output)
            if args.output:
                emit({"document": str(args.output.resolve()), "status": "draft", "scope": template_scope(args.stage)})
            else:
                print(document, end="")
        elif args.action == "gauntlet":
            document = gauntlet(resolve(args.project, root), args.objective, args.hours, args.focus, args.output)
            if args.output:
                emit({"document": str(args.output.resolve()), "status": "prepared", "execution_started": False, "scope": "Prompts preparados; execução, controle do prazo e retomada pertencem à sessão do agente."})
            else:
                print(document, end="")
        elif args.action == "check-plan":
            report = check_plan_report(read_json(args.plan), root)
            emit(report)
            return int(bool(report["errors"]))
        elif args.action == "note":
            emit(note_observation(
                require_project_destination(args.project, root), args.author, args.note,
                parse_fields(args.field), args.output, args.role, args.scenario,
                args.from_run,
            ))
        elif args.action == "record":
            emit(record(resolve(args.project, root), args.kind, args.author, args.note, parse_fields(args.field), args.attach, args.output.absolute()))
        elif args.action == "sfx":
            if (root / "workspace.json").is_file() and not (sfx_catalog.catalog_dir(root) / "catalog.json").is_file():
                command = shlex.join(["python3", str(FRAMEWORK / "scripts/workspace.py"),
                                      "--root", str(root), "get", "sfx"])
                raise ValueError(f"Acervo sfx não baixado. Execute {command} antes de consultar sons.")
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
