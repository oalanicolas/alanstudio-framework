# Handoff — fácil + AAA honesto

**Branch:** `cursor/framework-0-9-facil-e-aaa-1083` (base `main`)
**PR:** [#4](https://github.com/oalanicolas/alanstudio-framework/pull/4) (draft)
**HEAD:** ver `git log -1` — vigente 0.9.105: o relógio também cede.
**Goal:** ativo. Não marcar complete. AAA fácil ainda não está provado.

**Testes no HEAD:** `python3 -m unittest discover -s tests` → 240 OK.
`cd assets/starters/canvas-arcade && npm test` → 266 OK.

O histórico de versões fica em [`adoption.md`](adoption.md). Este arquivo
é o contrato para a próxima sessão, não o arquivo de 0.9.4 / PRs #2 e #3.

---

## Objetivo que permanece

Evoluir o Alan Studios Framework para que criar jogos com IA seja **fácil**
e o resultado alcance qualidade **AAA**, com honestidade epistêmica:
não prometer o que o harness não verifica.

1. Auditar promessa vs entrega (SKILL, README, references/, recipes/,
   templates, `scripts/game.py`, `scripts/audio.py`, `scripts/sfx_catalog.py`,
   tests/).
2. Reduzir atrito ideia → jogo jogável.
3. Endereçar no disco as dimensões que separam protótipo de AAA.
4. Implementar com as duas suítes verdes.
5. Não promover o que ninguém observou.

Não redefinir sucesso pelo que já passou nos testes. O piso do starter
continua **protótipo** porque só `release` está em `prototype`.

---

## O que o HEAD já entrega (0.9.91–0.9.105)

| Ver | Salto |
| --- | --- |
| 0.9.91 | `guide` devolve `open` + `prompt`. `len(steps) == 3`. `--idea` no guide não grava. |
| 0.9.93–94 | `#remap` na página; `#commands` lê teclas vivas. Invite some só `#commands`. |
| 0.9.95 | `npm run pair` nasce look + chuva no mesmo nome. `then`/`next` apontam par primeiro. |
| 0.9.96 | `start --idea` sem caminho cria a pasta. Guide não cria. |
| 0.9.97 | Coach nomeia orbe perdido enquanto `chain === 0`. |
| 0.9.98 | Panner no x do campo (coleta, queda, raspo, impacto, avanço). |
| 0.9.99 | Halo na forma + vinheta. Reduced some os dois. |
| 0.9.100 | Corpo aponta o último avanço. Orbe círculo, estilhaço losango. |
| 0.9.101 | Com tela, fase `title`. Lê `lastSeed` e recorde. Sem tela, headless joga. |
| 0.9.102 | Com tela, R no fim volta à abertura. Última pontuação na porta. |
| 0.9.103 | Abrir a porta senta, desloca e fala sem contar o dash. Overlay nomeia a abertura. |
| 0.9.104 | A porta chove (orbe e estilhaço) sem comer a seed. Reduced trava, não some. |
| 0.9.105 | `gameSpeed` dilata o relógio. `advance()` não. Assistência ≠ este knob. |

`python3 scripts/game.py` sem subcomando é o `guide`. `--idea` no parser
principal também funciona sem subcomando.

---

## Barra vigente do starter

Piso percebido = **mínimo**. Só `release` está em `prototype`.

| Dimensão | Degrau | Lacuna seguinte |
| --- | --- | --- |
| feel | playable | peso no dispositivo; stub ≠ felt |
| legibility | playable | stub ≠ dispositivo |
| art_direction | slice | `consistent` falso |
| audio_mix | slice | `heard` falso |
| pacing | slice | curva com outsider pendente |
| state_trust | slice | aba fechada real não observada; repetir seed ≠ tick interrompido |
| performance | playable | poços + stub ≠ dispositivo |
| accessibility | slice | oito opções + remap + relógio; sessão real pendente |
| content_scale | shippable | dusk+calm+pair; `enough` falso |
| release | **prototype** | ninguém correu o `dist/` fora daqui |

---

## Invariantes — não violar

- Nenhum comando observa/joga/ouve/sente/mede o jogo no dispositivo.
- Nunca emitir `verified` como status. `verify --proves` → `claimed`.
- `granted` / `validated` / `observed` / `heard` / `approved` / `felt` /
  `trusted` / `measured` / `consistent` / `enough` / `shipped` / `outsider`
  sempre `false` nos leitores correspondentes.
- Não importar limiares (16 ms, 100 ms, 4,5:1, 93%, “cinco usuários”,
  draw calls, −14 LUFS) como critério/aprovação.
- Relatórios (`peak`, `mix`, `budget`, `contrast`, `probe`, `size`,
  `session`) não podem conter `aprovado|verified|LUFS|-14|4.5` no stdout
  do que o relatório afirma. `size.test.mjs` exclui o campo `directory`.
  `budget.test.mjs` recusa `16 ms|16ms`. Contrast recusa `WCAG`.
  Dizer “sem LUFS” no scope **quebra** teste — use “sem limiar”.
- Não promover degraus sem a observação que o critério pede.
- `release` não sobe sem outra máquina. `content_scale` não sobe a
  flagship sem outsider. `feel`/`legibility`/`performance` não sobem
  por código headless. `accessibility` não sobe por stub. `pacing` não
  sobe por sessão simulada, `invite.md` nem `?invite=1`. `art_direction`
  não sobe por JSON/CSS/halo/vinheta/ponta no disco.
- Não implementar should-meet de Cooper.
- Após `init`, `next` exige `playable.unplayed` primeiro (enquanto não
  houver `note`). Depois de um `note`, `playable.unplayed` some e `next`
  pode ser `cycle.craft` (par primeiro).
- Recibo otimista ainda passa em `origins` e `feel` de propósito.
- **Não só adicionar mais um script de medição** se o salto alinhado
  for feel visível/audível, ferramenta de outsider, superfície de
  entrada, auditoria original (item 1) ou facilidade ideia→jogo.
- `len(steps) == 3` do `guide` é invariante.
- `--idea` no `guide` **não grava** nem cria pasta; no `start` grava e,
  sem caminho, cria a pasta.
- `contrast` não é look escolhível.
- Trocar look **não** recomeça; trocar spawn **recomeça**.
- Não rodar `python3 tools/design-sfx.py` **sem `--from`** no repo —
  regenera os WAV commitados.
- `emit()` já chama `burst()` — não duplicar. `close`, `live`, `stir`
  e `missed` **não** estão em `MOTE_COUNTS`.
- Não zerar `state.chain` no `over`.
- Não reduzir `INIT_DOCUMENTS` sem mudar `fresh_starter_cycle` /
  `areas.not_located`.
- Não ensinar pad/touch no coach **antes** de `lastSource` nem
  **depois** da primeira guarda.
- Não promover pacing/art/feel/a11y por convite, CSS, faixa, contorno,
  LAN, caption, marca de queda, botão de remap, panner, halo, vinheta,
  ponta, tela de título ou `gameSpeed` no disco.
- Não fazer **mais uma faixa de HUD** (`height===2` e `y<20` e não é placa).
- Não tratar mesa/look first-party novo como craft (atualizar
  `STARTER_TABLES` / `STARTER_LOOKS` + RESERVED).
- Não regenerar o banco SFX.
- Se nascer chave nova no cycle: `CYCLE_KEYS` + `cycle_line` + testes.
- Se nascer papel SFX novo: entrar em `ROLES`/`VOICES`/`SOUNDS` **antes**
  de `--from`.
- Contornos de campo já usam insets 2/4/6.
- Stdout de ferramentas **não pode** conter `enough|consistent|aprovado|verified`
  mesmo em frases de negação.
- Não criar segundo PR. Atualizar o #4 com `ManagePullRequest`.
- Respostas ao usuário em português.
- Commits em português, presente, sem período no título.
  `Co-authored-by: Alan Nicolas <oalanicolas@users.noreply.github.com>`

---

## Contratos que a próxima sessão precisa acertar

**Guide / start**

- `CRAFT_EXAMPLES` ordem: pair → look → table → sfx. Look e chuva do
  exemplo compartilham o nome `noite`.
- `play` após `start` é `cd … && npm run serve`. Não há `npm install`.
- `then` sempre tem `play`, `note`, `lost`.
- Sem caminho e sem ideia (ou ideia que não vira slug): `ValueError` “sem destino”.

**Starter**

- Looks first-party: `normal`, `dusk`, `calm`. Contrast é alcance.
- Chuvas first-party: `spawn`, `dusk`, `calm`.
- `listMoods()` = interseção look ∩ spawn (hoje `calm`, `dusk`).
- `SOUNDS`: dash, graze, collect, missed, bank, hit, over, close, live, stir, bed.
- Jogador: `fillRect` do squash **permanece** (testes `playerFill` /
  `playerBox`). A ponta é path (`lineTos`). Halo do estilhaço **não**
  é `arc` (`orb.arcs > shard.arcs`).
- `player.dir` default `1`. Ponta some? Não — é forma, não brilho.
- Fase `title` só com canvas (ou `options.entry === "title"`). Headless
  e `createState()` default = `playing`. `advance` em title não anda o
  tick. Dash em `step` chama `beginRun` (squash, punch, `dash` sem
  incrementar `stats.dashes`). Sem dash, `attractTick` anda a chuva da
  porta — sem RNG, sem `entities`. Reduced trava a queda. Reset na title sorteia seed nova
  e vai a `playing`. Pause na title é ignorado. Com tela, `reset()` sem
  argumento no `over` volta à title; `reset(seed)` explícito joga.
- Continuar = **repetir `lastSeed`**, não restaurar o tick. `canContinue`
  exige `runs > 0` e `lastSeed`. `doorOpen()` relê o progresso — não
  congela o valor do boot.
- Coach: fantasy → move → dash → miss → touch/pad → collect → null após
  1ª guarda. `coachHint` some se `phase !== "playing"`.
- `copy.fantasy` alimenta a abertura **e** os 48 ticks do aviso.
- `title_play` / `title_again` / `title_new` / `title_last` /
  `over_door` / `over_door_inline` em `COPY_FIELDS`. `migrateCopy`
  preenche default se a mesa antiga não tiver.
- Invite (`?invite=1`) some `#commands`, não `#remap`.
- `pagehide` flush; hidden pausa.
- `gameSpeed` (0.5–1, padrão 1) dilata o acumulador do laço.
  `advance()` ignora. Assistência não é este knob.

---

## Lacunas ainda abertas (priorizar alinhamento, não facilidade de teste)

Saltos alinhados: feel visível/audível, ferramenta de outsider, superfície
de entrada, auditoria item 1, ou atrito ideia→jogo. **Não** mais um
script de medição.

Candidatos, do que ainda dói:

1. **Release (define o piso):** outra máquina correr o `dist/`. Não
   promover. Um runbook mais honesto ou um `ship` que nomeie o buraco
   sem fingir `shipped` ainda pode ajudar o caminho.
2. **Idéia→jogo:** `start --idea` cria; ainda falta colar `play` e
   `note`. O harness não deve auto-servir sem o usuário pedir — mas o
   prompt pode ficar mais curto/colar-único se isso não quebrar
   `len(steps) == 3` nem `executed: false`.
3. **Checkpoint do tick:** a abertura e o fim repetem a seed; o save
   não guarda o meio da chuva. Mid-run resume é schema novo + contrato
   observe/advance. Não chamar isso de Continuar.
4. **Item 1 residual:** recipes/templates vs código. O HANDOFF antigo
   (PRs #2/#3) está obsoleto; recipes ainda falam “tela do primeiro
   ciclo” em alguns sítios — a abertura agora é a porta.
5. **Outsider / pacing / a11y real / feel no dispositivo:** não
   promover. Convite, LAN, stub e `gameSpeed` no disco não fecham.
   A receita de velocidade ajustável já tem knob; falta a sessão.
6. **Volume de conteúdo:** três chuvas + `pair` ainda não são volume.
   Não nascer look/chuva first-party novo como craft.

`init` ainda cria 6 rascunhos de propósito (`fresh_starter_cycle`).

---

## Como retomar

```sh
git checkout cursor/framework-0-9-facil-e-aaa-1083
python3 -m unittest discover -s tests
cd assets/starters/canvas-arcade && npm test
```

Inspecionar o working tree **antes** de confiar neste texto. Melhorar,
trocar ou apagar o que estiver velho. Um salto por vez, commit
descritivo, push, atualizar o PR #4. Não marcar o goal complete.

Arquivos quentes da última sessão: `src/core/loop.js` (`setSpeed`),
`src/core/settings.js` (`gameSpeed`), `src/main.js` (`updateSettings`),
`index.html` (`#gameSpeed`), `scripts/game.py` (`A11Y_OPTIONS`),
`docs/access.md`, `adoption.md`.
