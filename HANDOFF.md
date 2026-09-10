# Handoff — fácil + AAA honesto

**Branch:** `cursor/framework-0-9-facil-e-aaa-1083` (base `main`)
**PR:** [#4](https://github.com/oalanicolas/alanstudio-framework/pull/4) (draft)
**HEAD:** ver `git log -1` — vigente 0.9.130: a seed também leva chuva e look.
**Goal:** ativo. Não marcar complete. AAA fácil ainda não está provado.

**Testes no HEAD:** `python3 -m unittest discover -s tests` → 252 OK.
`cd assets/starters/canvas-arcade && npm test` → 297 OK.

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

## O que o HEAD já entrega (0.9.91–0.9.130)

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
| 0.9.106 | `start` devolve `open` (= `play`) e os mesmos `steps` do guide. |
| 0.9.107 | Schema 3: `hold` é o tick interrompido. `canResume` ≠ Continuar. |
| 0.9.108 | `ship` nomeia árvore incompleta, HEAD velho e `elsewhere` falso. |
| 0.9.109 | `cycle.door` entra no prompt: com tela o avanço abre a porta. |
| 0.9.110 | O avanço senta dois ticks antes de alongar. A porta continua imediata. |
| 0.9.111 | `play` / `open` apontam o serve sem executar. Perder o JSON não recomeça. |
| 0.9.112 | Depois do fim no convite, a página oferece os quatro nomes para copiar. Esqueleto vazio não é achado. `outsider` continua falso. |
| 0.9.113 | A partida no serve grava `last-run.json`. A simulação continua à parte. `observed` continua falso. |
| 0.9.114 | Depois do fim, a página grava o recibo de `note` se você escrever. Convite não oferece. `felt` continua falso. |
| 0.9.115 | No convite, a página grava `docs/playtest/<utc>-achado.md` se os quatro tiverem texto. Copiar não grava. Esqueleto vazio não é achado. `outsider` continua falso. |
| 0.9.116 | O término do dash declara `land` no mixer (voz curta, x do campo, legenda). Recipes de mecânica/visual nomeiam a porta. `felt`/`heard` continuam falsos. |
| 0.9.117 | Um avanço *novo* no fim volta à porta. Dash apertado no último tick não pula o overlay. `#note`/`#finding` também na abertura se houver partida. `felt` continua falso. |
| 0.9.118 | `guide` / `start` / `play` escrevem o `prompt` em stderr. O JSON fica no stdout. `executed` continua falso. |
| 0.9.119 | O achado da página anexa `last-run` em `<utc>-achado.run.json` se a partida deixou candidato. `playtest` relata `finding_attachments`. `outsider` continua falso. |
| 0.9.120 | `?seed=<n>` abre essa partida. Seed explícita (query ou construtor) ignora o hold. `playtest` relata `candidate_seed`. `CYCLE_KEYS` inclui `seed`. `observed` continua falso. |
| 0.9.121 | A porta desenha a legenda que o mixer ainda guarda. `captions: false` some a linha. `verified` continua falso. |
| 0.9.122 | Depois de um last-run no disco, `then.seed` aponta `/?seed=<n>`. O prompt nomeia o número. Sem last-run, a chave some. `then.seed` não é ofício. `observed` continua falso. |
| 0.9.123 | Com seed no last-run, o convite aponta `/?invite=1&seed=<n>`. `then.invite`, `invite_href` e o banner do serve juntam o número. Sem last-run, continua `/?invite=1`. `then.invite` não é ofício. `outsider` continua falso. |
| 0.9.124 | A porta chove a mesa vigente: dusk mais denso e rápido, calm mais folgado e lento. Sem RNG, sem `entities`. A mostra do spawn continua a chuva de quatro. `consistent` continua falso. |
| 0.9.125 | Depois do fim, `#note` aponta `/?invite=1&seed=<n>` e copia o endereço. Sem seed, a linha some. Copiar o endereço não grava. `outsider` continua falso. |
| 0.9.126 | Com chuva no last-run, o convite junta `/?invite=1&seed=<n>&spawn=<mesa>`. `then.invite`, `invite_href`, `#note` e o banner do serve levam a mesa. Spawn padrão ou inválido some. Sem last-run, continua `/?invite=1`. `playtest` relata `candidate_spawn`. `outsider` continua falso. |
| 0.9.127 | `production.md`, `architecture.md` e `release.md` nomeiam a porta. Nomear a abertura não entrega o artefato nem fecha marco. `elsewhere` continua falso. |
| 0.9.128 | Com look no last-run, o convite junta `&look=<paleta>`. `then.invite`, `invite_href`, `#note` e o banner do serve levam a paleta. Look `normal` ou `contrast` some. Sem last-run, continua `/?invite=1`. `playtest` relata `candidate_look`. `outsider` continua falso. |
| 0.9.129 | `colorblind` fixa orbe azul e estilhaço laranja sem trocar o campo do look. Não é look. Alto contraste vence. `access` relata a chave. `verified` continua falso. |
| 0.9.130 | Com chuva ou look no last-run, `then.seed` junta `&spawn=` e `&look=`. `seed_href`, o banner do serve e o prompt usam o mesmo endereço. Sem mesa ou paleta nomeada, continua `/?seed=<n>`. `then.seed` não é ofício. `observed` continua falso. |

`python3 scripts/game.py` sem subcomando é o `guide`. `--idea` no parser
principal também funciona sem subcomando.

---

## Barra vigente do starter

Piso percebido = **mínimo**. Só `release` está em `prototype`.

| Dimensão | Degrau | Lacuna seguinte |
| --- | --- | --- |
| feel | playable | peso no dispositivo; coil no disco ≠ felt |
| legibility | playable | stub ≠ dispositivo |
| art_direction | slice | `consistent` falso |
| audio_mix | slice | `heard` falso |
| pacing | slice | curva com outsider pendente |
| state_trust | slice | `hold` no stub; aba fechada real não observada; `trusted` falso |
| performance | playable | poços + stub ≠ dispositivo |
| accessibility | slice | nove opções + remap + relógio; sessão real pendente |
| content_scale | shippable | dusk+calm+pair; `enough` falso |
| release | **prototype** | ninguém correu o `dist/` fora daqui; `elsewhere` falso |

---

## Invariantes — não violar

- Nenhum comando observa/joga/ouve/sente/mede o jogo no dispositivo.
- Nunca emitir `verified` como status. `verify --proves` → `claimed`.
- `granted` / `validated` / `observed` / `heard` / `approved` / `felt` /
  `trusted` / `measured` / `consistent` / `enough` / `shipped` /
  `elsewhere` / `outsider` sempre `false` nos leitores correspondentes.
- Não importar limiares (16 ms, 100 ms, 4,5:1, 93%, “cinco usuários”,
  draw calls, −14 LUFS) como critério/aprovação.
- Relatórios (`peak`, `mix`, `budget`, `contrast`, `probe`, `size`,
  `session`) não podem conter `aprovado|verified|LUFS|-14|4.5` no stdout
  do que o relatório afirma. `size.test.mjs` exclui o campo `directory`.
  `budget.test.mjs` recusa `16 ms|16ms`. Contrast recusa `WCAG`.
  Dizer “sem LUFS” no scope **quebra** teste — use “sem limiar”.
- Não promover degraus sem a observação que o critério pede.
- `release` não sobe sem outra máquina. `ship.incomplete` / `ship.stale`
  / banner do artefato / `elsewhere` falso não promovem. Não nascer
  `ship.unbuilt` — o starter não commita `dist/`. `content_scale` não sobe a
  flagship sem outsider. `feel`/`legibility`/`performance` não sobem
  por código headless. `accessibility` não sobe por stub. `pacing` não
  sobe por sessão simulada, `invite.md` nem `?invite=1`. `art_direction`
  não sobe por JSON/CSS/halo/vinheta/ponta/chuva da porta no disco.
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
  ponta, tela de título, chuva da porta, `gameSpeed` no disco, `hold` no stub,
  coil/windup no disco, copiar ou gravar o achado, last-run,
  anexo do achado, recibo da página, `?seed=`, `then.seed`,
  `then.invite`, `invite_href`, copiar o endereço do convite,
  levar a chuva ou o look na URL, tinta estável no disco
  ou avanço no overlay.
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

- `CYCLE_KEYS` inclui `door` depois de `verb` e `seed` depois de
  `mood`. `cycle_line` nomeia `Porta:` antes de `Mover` e `Seed:`
  antes de `Convite`.
- `CRAFT_EXAMPLES` ordem: pair → look → table → sfx. Look e chuva do
  exemplo compartilham o nome `noite`.
- `play` após `start` é `cd … && npm run serve`. Não há `npm install`.
- `start` devolve `open` (= `play`) e `steps` (3, passo 1 feito).
  `guide` sem destino: `open` é o start. Os dois: `executed` falso.
- `play` / `open` (CLI) apontam o serve do projeto existente. Não
  criam, não executam. Sem caminho: `here_project` ou “sem destino”.
- `emit()` escreve `prompt` em stderr quando a chave existe e tem
  texto. stdout continua só o JSON. Falar a frase não executa.
  `next` / `doctor` / `feel` não têm `prompt` e não escrevem frase.
- `then` sempre tem `play`, `note`, `lost`.
- Se `last_run_seed` devolver um `int` (não bool), `then.seed`
  é `seed_href` (`/?seed=<n>` ou, com chuva nomeada e ≠ `spawn`,
  `/?seed=<n>&spawn=<mesa>`, e com look nomeado e ≠ `normal`/`contrast`,
  `&look=<paleta>`) e `then.invite` é `invite_href` (`/?invite=1`
  mais os mesmos eixos). Sem last-run ou sem seed, as duas chaves
  somem. `then.seed` e `then.invite` **não** entram em
  `CRAFT_EXAMPLES` / `CRAFT_LABELS`. `next` não ganha basis nova
  na frente de `cycle.craft`.
- `seed_href` / banner `Seed:` do serve usam o mesmo endereço da
  partida. `invite_href` / `playtest --invite` / banner `Convite:` /
  `#note` usam o convite com os mesmos eixos. Página já escrita
  não é reescrita; o JSON aponta o href vigente.
- Sem caminho e sem ideia (ou ideia que não vira slug): `ValueError` “sem destino”.

**Starter**

- Looks first-party: `normal`, `dusk`, `calm`. Contrast é alcance.
- Chuvas first-party: `spawn`, `dusk`, `calm`.
- `listMoods()` = interseção look ∩ spawn (hoje `calm`, `dusk`).
- `SOUNDS`: dash, land, graze, collect, missed, bank, hit, over, close, live, stir, bed.
- Jogador: `fillRect` do squash **permanece** (testes `playerFill` /
  `playerBox`). A ponta é path (`lineTos`). Halo do estilhaço **não**
  é `arc` (`orb.arcs > shard.arcs`).
- `player.dir` default `1`. Ponta some? Não — é forma, não brilho.
- Fase `title` só com canvas (ou `options.entry === "title"`). Headless
  e `createState()` default = `playing`. `advance` em title não anda o
  tick. A porta desenha `drawCaptions` se `captions !== false`.
  Legenda na abertura não sobe `accessibility`. Dash em `step` chama `beginRun` (squash, punch, `dash` sem
  incrementar `stats.dashes`). Sem dash, `attractTick` anda a chuva da
  porta — lê a mesa vigente (cadência e queda), sem RNG, sem
  `entities`. A mostra do spawn continua quatro gotas. Reduced trava a queda. Reset na title sorteia seed nova
  e vai a `playing`. Pause na title é ignorado. Com tela, `reset()` sem
  argumento no `over` volta à title; um avanço *novo* no over faz o
  mesmo. Dash ainda apertado no último tick não arma a porta.
  `reset(seed)` explícito joga.
- Continuar = **repetir `lastSeed`**, não restaurar o tick. `canContinue`
  exige `runs > 0` e `lastSeed`. `doorOpen()` relê o progresso — não
  congela o valor do boot.
- `hold` / `canResume` = tick interrompido (schema 3). Seed explícita
  (`options.seed` ou `?seed=`) ignora o hold. Reset e `recordRun`
  limpam. Não chamar de Continuar. `?seed=` não é sessão observada.
  Não promover `state_trust`. `hold.player` leva `dashWindup`.
- Avanço na partida: `dashWindupTicks` (2) senta com `squashCoil`
  antes de `fireDash`. A porta (`beginRun`) continua imediata.
  Não promover `feel`.
- Coach: fantasy → move → dash → miss → touch/pad → collect → null após
  1ª guarda. `coachHint` some se `phase !== "playing"`.
- `copy.fantasy` alimenta a abertura **e** os 48 ticks do aviso.
- `title_play` / `title_again` / `title_new` / `title_last` /
  `over_door` / `over_door_inline` em `COPY_FIELDS` (default `{dash}`).
  `migrateCopy` preenche default se a mesa antiga não tiver.
- Invite (`?invite=1`) some `#commands`, não `#remap`. Com seed no
  last-run, `/?invite=1&seed=<n>` some a tabela e abre essa partida.
  Com chuva nomeada e ≠ `spawn`, junta `&spawn=<mesa>`. Com look
  nomeado e ≠ `normal`/`contrast`, junta `&look=<paleta>`. Spawn
  ou look inválido, e os nomes padrão, somem.
  `#finding` aparece com `html.invite.finding` no `over` e na `title`
  se houver `lastRun`. Copiar não grava. Gravar só se `playFinding`
  devolver texto. Esqueleto vazio não casa `FINDING_FIELDS`. Achado
  `.md` ≠ recibo `record.json`.
- Serve POST `/playtest/last-run` grava `docs/playtest/last-run.json`.
  Força `observed`/`felt` falsos e `policy: played`. Árvore
  exportada responde 403. Sem canvas o headless não posta.
- Serve POST `/playtest/note` grava `docs/playtest/<utc>/record.json`.
  Nota vazia é 400. Autor vazio vira `página`. Anexa last-run se
  existir. `#note` no `over` e na `title` se houver `lastRun`, fora
  do convite. Com seed, `#note-invite` aponta o endereço e copia —
  com a chuva e o look se o last-run os nomeou. Sem seed, a linha some.
  Copiar o endereço não grava. `felt` falso.
- Serve POST `/playtest/finding` grava `docs/playtest/<utc>-achado.md`.
  Quatro vazios → 400. Árvore exportada → 403. Se `last-run.json`
  existir, grava `<utc>-achado.run.json` (`kind: finding-attachment`,
  `outsider`/`observed` falsos). Não é `record.json` e não limpa
  `playable.unplayed` sozinho. `playtest` relata o anexo em
  `finding_attachments`.
- `pagehide` flush; hidden pausa.
- `gameSpeed` (0.5–1, padrão 1) dilata o acumulador do laço.
  `advance()` ignora. Assistência não é este knob.
- `colorblind` é alcance, não look. `dressPalette` aplica
  `COLORBLIND_INKS` (orbe/estilhaço/corrente/perigo do `normal`)
  sobre o look vigente. Alto contraste vence. Não entra no href.
  Não promover `accessibility`.

---

## Lacunas ainda abertas (priorizar alinhamento, não facilidade de teste)

Saltos alinhados: feel visível/audível, ferramenta de outsider, superfície
de entrada, auditoria item 1, ou atrito ideia→jogo. **Não** mais um
script de medição.

Candidatos, do que ainda dói:

1. **Release (define o piso):** outra máquina correr o `dist/`. Não
   promover. `ship` já nomeia árvore incompleta, HEAD velho e
   `elsewhere` falso; isso não é a prova.
2. **Idéia→jogo:** `start` devolve `open`; `play` / `open` o
   reimprimem. O `prompt` também sai em stderr. A partida no serve
   grava o candidato e, se você escrever, o recibo. No convite a
   página grava o achado se os quatro tiverem texto e anexa o
   candidato se last-run existir. `?seed=` abre a seed do
   candidato. Depois de um last-run, `then.seed` aponta o
   endereço da partida (número, chuva e look quando o
   candidato os nomeia) e o convite junta os mesmos eixos.
   O comando `note` continua. Não auto-servir.
   `len(steps) == 3` e `executed: false` continuam.
3. **Checkpoint do tick:** `hold` existe. Falta aba fechada real.
   Não promover. Não chamar `hold` de Continuar.
4. **Item 1 residual:** o mapa e as receitas de foco — inclusive
   `production.md`, `architecture.md` e `release.md` — já nomeiam a
   porta ou o convite. Templates e referências que ainda falarem só
   do campo sem a abertura estão velhos. Nomear não entrega.
5. **Outsider / pacing / a11y real / feel no dispositivo:** não
   promover. Convite, LAN, stub, `gameSpeed` no disco, tinta
   estável no disco, copiar o achado, gravar os quatro nomes e
   anexar last-run não fecham. A receita de velocidade ajustável
   já tem knob; falta a sessão.
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

Arquivos quentes da última sessão: `dressPalette` / `colorblind`.
Tinta estável não é look. Alto contraste vence. Não entra no href.
Chave no disco não é sessão observada.
