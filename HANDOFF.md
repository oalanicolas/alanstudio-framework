# Handoff — integração dos PRs #2 e #3

**Nesta árvore, depois da integração:** `origins` lê o disco onde
`deliver.licensing` só lia a tabela. Percorre mídia embarcada (inclusive
`textures/`, `fonts/`, `models/`, `videos/`), cruza com recibos e o `next`
propõe `origins.undeclared`. Recibo não é licença válida — `granted` e
`validated` são sempre `false`.

**Ofício (`craft`)** lê os nove checklists da §7 do levantamento — conformidade
com o que o próprio projeto declarou, zero dígitos nos rótulos. `observed` e
`granted` são sempre `false`. `next` só levanta o gate que o projeto pediu.

**Primeiro ciclo:** `guide` (também sem subcomando) mapeia start →
jogar → note sem executar. `open` é o comando de agora; `prompt` o
nomeia. Sem destino, `--idea` nomeia a pasta no
comando do start — ao lado do framework se o mapa corre de dentro
desta árvore — e não grava a frase. Sem destino, se o diretório atual é um
jogo fora do framework, o mapa usa esse caminho. `start` cria o projeto e devolve `play` +
`then.note`. Se o starter declara `cycle`, o prompt nomeia o verbo,
as teclas, o cluster de uma mão (`hand`), o toque, o controle e as queries de look, chuva, par e convite. Se o projeto — ou o starter, antes do destino existir — declara as ferramentas, `then` nomeia look, chuva e voz; se declara `session`, `then` a aponta. Depois de um recibo, o prompt e o `next` (`cycle.craft`) apontam o ofício. O autor do `note` é sugestão do git ou do ambiente, não quem jogou. Nomear o ofício não pinta. `next` continua em `then.lost`, para quando você não sabe o que falta. Depois de um `init` fresco,
`next` ainda propõe `playable.unplayed` se você estiver perdido. O
starter ensina mover, avançar, coletar e guardar no campo; toque e
controle ganham passo quando falam. O art-bible vigente
não é reescrito. `--idea` entra no brief e, se houver `data/copy.json`,
na tela do primeiro ciclo. O brief continua rascunho. A frase na tela
não muda o verbo. Depois do `init`, `?look=dusk` ou `?look=calm` troca a paleta
(campo e a página), `?spawn=dusk` ou `?spawn=calm` troca a chuva e
`?mood=calm` ou `?mood=dusk` troca o par. Look ou chuva explícitos
vencem o mood no próprio eixo. A página nomeia o mesmo par no
select. O harness não
executa o jogo.

**Papéis de áudio (`roles`):** lê `const SOUNDS` e cruza com `public/sfx`.
`--fill` sugere o acervo; `--apply` copia com o nome do papel. Sem
acervo a busca aponta o starter e `sfx serve` recusa. Crescer o
acervo é `sfx import` / `sfx seed` (ffmpeg); `sfx info` lê a ficha
e `sfx export` copia bytes e créditos. Importar e exportar não é ouvir.
O starter
já traz design original e variante (`-b`) nos papéis do verbo, no orbe
perdido, no fecho, na prática, na guarda e na cama e carrega no mixer. A cama entra em loop no barramento de música.
`npm run mix` soma cama e vozes na partida simulada com o mesmo palco,
folga e taxa da corrente do mixer. `sfx --from` / `--as` desloca a voz
no papel que o mixer já toca. Coleta e guarda sobem de tom com a
corrente; o erro não herda. `heard` é sempre falso.

**Feel (`feel`):** lê `const CONFIG` (perdão, graça, hitstop, punch,
telegraph, flash, rumble) e `record.json` de observação. `note` grava o recibo
curto. `felt` é sempre falso. `next` propõe `feel.unobserved` quando há
constante e não há recibo. O starter bufferiza guardar no hitstop,
desloca a câmera por verbo, achata o corpo numa medida por verbo,
marca a ameaça no trilho, distingue a
recuperação do dash, enche a faixa do HUD no tempo de espera,
contorna o campo na prática, na guarda e no fecho da partida,
aterrissa o avanço com squash e rastro próprios,
pulsa o controle no impacto, deixa um rastro
por verbo e põe a corrente em órbita no corpo. A coleta leva o
orbe ao slot; no erro os pips quebram para fora; na guarda eles
voam para o placar; no fim a aposta não guardada cai e o overlay
nomeia o que caiu — a queda vence a cortina, que reusa a
placa do look. As legendas nascem depois da cortina; o texto
do overlay segue `uiScale`. O raspo
risca o campo sem pulsar o controle. O orbe que cai marca o
lugar da queda, sem pulsar o controle. O pulso some na pausa e no
descarte.

**Alcance, save, orçamento:** `access`, `save` e `budget` leem o que o
código declara — `access` inclui assistência. `verified`/`trusted`/`measured` são sempre falsos. `next`
só levanta quando falta a declaração. O starter expõe assistência,
`uiScale` (o overlay também), preset de uma mão (o aviso, o overlay e o `cycle.hand`
nomeiam IJKL + P/O; o stub coleta, guarda, pausa e reinicia nesse
cluster) e `docs/access.md`. O HUD do dash enche a faixa no tempo
de recuperação e cooldown; faixa no stub não é peso percebido. O aviso do primeiro ciclo nomeia teclado,
toque e controle; o dash e o mapa da superfície que falou também
ganham passo; overlay e HUD confirmam o aparelho que falou por
último. `npm run contrast`
amostra pixels do stub após `draw()` e, em cinza, o que só
o orbe ou só o estilhaço pinta. `pagehide` descarrega
o save. A chuva compacta o array vivo e reusa o poço; evento, rastro,
telegraph e o gerador da chuva também reusam; `npm run budget`
cronometra a cena `playing.run` (simulação e `draw` no stub) e
relata o reuso.

**Arte, conteúdo, empacotar:** `art`, `content` e `ship` leem paleta ou
art-bible vigente, dado fora do código e passo de build/export.
`consistent`/`enough`/`shipped` são sempre falsos. O starter declara
paleta em `data/palettes.json` (looks `dusk` e `calm` por `?look=` / `settings.look`;
a página também veste esses tokens; `contrast` é alcance, não look;
`look --from` / `--as` nasce o próximo),
extrai a chuva (`spawn`, `dusk` e `calm`), nasce mesa com `npm run table`
(`--from spawn|dusk|calm --as` já entra no consumidor; `session --spawn`
traça) e empacota com `npm run build`.
`ship` relata `dist/VERSION.json` quando existe; o artefato declara
Node 20 e recusa `npm install` e `file://`. `npm run size` relata
bytes sem teto.

**Playtest:** `playtest` lê o formato problema/evidência/hipótese/medição.
`observed` e `outsider` são sempre falsos. `--invite` escreve a página
e aponta `/?invite=1`, onde a tabela some; `next` a aponta depois do
recibo de quem fez. O serve anuncia a URL da rede se a máquina
tiver outro endereço IPv4. Esconder a tabela e anunciar a rede
não são alguém de fora.
Nota de partida sem os quatro campos vira
`playtest.unstructured`. O starter grava `docs/playtest/last-run.json`
com `npm run session` (totais e curva); `note --from-run` anexa o
candidato. Número no disco não é causa. `docs/release.md` vigente não
torna `shipped` verdadeiro.

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
