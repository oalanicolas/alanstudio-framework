# Handoff — integração dos PRs #2 e #3

**Nesta árvore, depois da integração:** `origins` lê o disco onde
`deliver.licensing` só lia a tabela. Percorre mídia embarcada (inclusive
`textures/`, `fonts/`, `models/`, `videos/`), cruza com recibos e o `next`
propõe `origins.undeclared`. Recibo não é licença válida — `granted` e
`validated` são sempre `false`.

**Ofício (`craft`)** lê os nove checklists da §7 do levantamento — conformidade
com o que o próprio projeto declarou, zero dígitos nos rótulos. `observed` e
`granted` são sempre `false`. `next` só levanta o gate que o projeto pediu.

**Primeiro ciclo:** `start` é o caminho ideia→jogo. Depois de um `init` fresco,
`next` propõe `playable.unplayed` (abrir o starter) antes de substituir os
sete rascunhos. `--idea` entra no brief como frase; o brief continua rascunho.
O harness não executa o jogo.

**Papéis de áudio (`roles`):** lê `const SOUNDS` e cruza com `public/sfx`.
`heard` é sempre falso. `next` propõe `audio.roles` quando o verbo dispara
um papel sem arquivo — depois da partida, antes dos rascunhos.

Esta árvore reúne produção, pacotes e memória persistente do PR #2 com os
critérios observáveis, perguntas de valor e regras de escopo do PR #3.
A integração preserva o trabalho de ambas as branches, inclusive os commits de
retomada adicionados durante a revisão.

Validação do conjunto: 178 testes Python aprovados; os 83 testes do starter e
seu orçamento de simulação também passaram. O starter não mudou na integração.
Foram corrigidos os exemplos e critérios apontados na revisão, o uso de foco
inválido no teste de gates e a consulta de contexto em ambientes sem Git.

Os registros abaixo descrevem o estado de cada linha antes da integração;
contagens, situação dos PRs e nomes de branches são históricos. As frentes
futuras continuam pendentes, sem implementação adicional neste merge.

- Produção, pacotes e memória persistente (PR #2): registro abaixo.
- Critérios observáveis e gates (PR #3): [registro preservado](HANDOFF-PR3.md).

## Registro da linha de produção e pacotes (PR #2)

# Handoff — branch `cursor/framework-0-9-aaa-facil-f6f6`

**PR:** [#2](https://github.com/oalanicolas/alanstudio-framework/pull/2) → `main`  
**Última atualização:** 2026-09-09  
**Testes:** `python3 -m unittest tests.test_game` → **160 OK**  
**Doctor:** `python3 scripts/game.py doctor --root <lab>` → `ready: true` (com framework completo)

---

## O que esta branch entrega (visão geral)

Integração das **três linhas paralelas de 0.9** que nasceram do mesmo pedido (“criar jogos com IA fácil e no acabamento AAA”) e divergiram em código e documentação:

| Linha | Origem | O que trouxe |
| --- | --- | --- |
| Facilidade e piso | `main` (PR #1, 0.9–0.9.3) | `feel`, `audio`, [ambição](references/ambition.md), checklist de piso (`--stage aaa`, `finish` no `context`) |
| Começar e acabar | PR #3 / `6f33` | `init`, `next`, `bar`, `gate`, `discover` revisado, `verify --proves`, starter `canvas-arcade`, receitas performance/acessibilidade/persistência/release, [gates](references/gates.md) |
| Produção e pacotes | esta branch (0.9.4) | `doctor`, `record`, `production`, marcos, 18 pacotes de plataforma, 23 de gênero (`--genre`), `game-design`, Cargo em `verify` |

O resultado é um **único `game.py`** (~2k linhas), **160 testes**, README e SKILL unificados, e vocabulário reconciliado: **marcos** (calendário), **barra** (degrau por dimensão), **gates** (dez recusas do ciclo) — três instrumentos, três perguntas ([receita de produção](recipes/production.md) §0).

---

## Commits já na branch (antes do handoff)

1. **Merge `origin/main`** — feel, áudio, ambição, checklist, `finish` no `context`.
2. **Merge `6f33`** — init/next/bar/gate, starter, suíte de testes expandida.
3. **Liga marcos, barra e gates** — “gate” deixa de significar “marco com evidência”; só as dez recusas de `gates.md`.

Mais ~30 commits da linha de produção/pacotes e da linha 6f33 (starters, barra, gates, discover revisado, etc.).

---

## Trabalho incluído na branch (Frente 1 — memória do agente)

Início da **Frente 1** do plano aprovado (“remediar problemas de desenvolvimento com IA”). **Não** inclui Frentes 2–5.

### Código (`scripts/game.py`)

- **`INSTRUCTION_FILES`** — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.cursor/rules`, `.github/copilot-instructions.md`, `.windsurfrules`.
- **`instruction_files(project)`** — lista da raiz do laboratório até o projeto (substitui só `AGENTS.md` no `context`).
- **`git_summary(project)`** — `head`, `branch`, `dirty_paths`, `recent` (5 commits); exposto em `context.git`.
- **`scan` → `foundation.agent_context`** — status `found` / `not_located` + arquivos na raiz do projeto.
- **`next`** — ramo `agent_context.not_located` (depois de áreas e continuidade, antes de validadores): propõe `template agents`.
- **`init`** — gera `AGENTS.md` na raiz do projeto novo (além dos rascunhos em `docs/`).
- **`doctor`** — check opcional `repository` (git na raiz).
- **Etapas:** `agents` em `STAGES` / `SUPPORT_STAGES`; template novo.

### Documentação

- [`assets/templates/agents.md`](assets/templates/agents.md) — rascunho de memória persistente do agente.
- [`README.md`](README.md) — ordem do `next` inclui “sem instruções para o agente”.

### Testes (+4)

- Instruções multi-host em `context.instructions`.
- `context.git` com e sem repositório.
- `next` propõe AGENTS; `init` entrega `AGENTS.md`.
- `doctor` reporta repositório.

---

## O que **não** foi feito (próxima sessão)

Plano acordado após merge; **nenhum código** destas frentes na branch ainda:

| Frente | Tema | Entregáveis previstos |
| --- | --- | --- |
| **2** | Spec + bug + subsistema único | template `spec` + stage, protocolo de bug em [process](references/process.md), entrega auditável no devlog/SKILL |
| **3** | Zonas de risco | [quality](references/quality.md), [network](recipes/network.md), [visual](recipes/visual.md), candidatos de netcode nos packs |
| **4** | Assets gerados por IA | disclosure no gate gold, receita de estilo, templates/production/sources |
| **5** | Gate 30 s / PoC / headless | PoC = vibe coding com prova de parada; simulação headless em alpha |

Também pendente da Frente 1 (menor): atualizar [SKILL](SKILL.md), [process](references/process.md) e [project-audit](references/project-audit.md) para citar `instructions`, `git` e `agent_context`; entrada em [adoption](adoption.md) (ex. 0.9.6).

---

## Como retomar

```sh
git checkout cursor/framework-0-9-aaa-facil-f6f6
python3 -m unittest tests.test_game          # 160 testes
python3 scripts/game.py doctor --root .      # integridade + pacotes
```

**Fluxos para validar manualmente:**

```sh
# Laboratório com jogos
python3 scripts/game.py discover --root /caminho/do/lab
python3 scripts/game.py next /caminho/do/lab/meu-jogo --focus create

# Jogo novo (starter)
python3 scripts/game.py init /caminho/do/lab/novo --starter canvas-arcade
# → docs/* + AGENTS.md na raiz

# Contexto com pacote e git
python3 scripts/game.py context /caminho/do/lab/novo --focus create --genre platformer --root /caminho/do/lab
```

**Decisão já tomada:** integrar tudo na branch antes de implementar Frentes 2–5; não fazer merge em `main` até revisão do PR #2.

---

## Riscos e limites (inalterados)

- Nenhum comando mede performance, atribui degrau da barra, concede passagem de gate, promove marco ou certifica acabamento.
- Pacotes são convenções — confirmar na engine e no código do projeto.
- `claimed` (`verify --proves`) não é `verified`.
- Links `#audio_mix--…` em receitas da linha 6f33 podem não bater com slugs do GitHub em `production-bar.md` (2 âncoras; teste de links do harness não cobre todos os casos).

---

## Arquivos tocados neste handoff (commit pendente)

- `scripts/game.py`
- `tests/test_game.py`
- `assets/templates/agents.md` (novo)
- `README.md`
- `HANDOFF.md` (este arquivo)
