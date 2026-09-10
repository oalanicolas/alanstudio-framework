# Handoff — fácil + AAA honesto

**Branch:** `cursor/framework-0-9-facil-e-aaa-1083` (base `main`)
**PR:** [#4](https://github.com/oalanicolas/alanstudio-framework/pull/4) (draft)
**HEAD:** ver `git log -1` — vigente 0.9.159: a cama sobe o tom no fecho.
**Goal:** ativo. Não marcar complete. AAA fácil ainda não está provado.

**Testes no HEAD:** `python3 -m unittest discover -s tests` → 264 OK.
`cd assets/starters/canvas-arcade && npm test` → conferir após o 0.9.159.

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

## O que o HEAD já entrega (0.9.91–0.9.159)

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
| 0.9.131 | O look dusk pinta orbe âmbar e estilhaço índigo. O campo continua quente. `colorblind` ainda troca a chuva pelo par do padrão. `consistent` e `verified` continuam falsos. |
| 0.9.132 | Guardar uma corrente que já existe senta dois ticks (`bank.windupTicks`) antes de converter. Coleta e guarda no mesmo quadro continuam na hora. `felt` continua falso. |
| 0.9.133 | Brief, GDD, game-design, PoC, slice, QA e release nomeiam a porta. O rascunho de playtest traz os quatro campos vazios. Esqueleto vazio não é achado. `observed` continua falso. |
| 0.9.134 | `--as warmer` / `--as cooler` deslocam campo e orbe; o estilhaço permanece. `dusk --as warmer` não devolve o losango ao rosa. O orbe dusk já é o âmbar da intenção. `consistent` continua falso. |
| 0.9.135 | Perder o orbe desloca a câmera para baixo e treme menos que a coleta. Sem hitstop, squash ou rumble. `init` não copia `__pycache__`. `felt` continua falso. |
| 0.9.136 | Depois do fim, `#finding-run` e `#note-run` mostram seed, pontos e eixos. Não preenche os quatro. `outsider` continua falso. |
| 0.9.137 | `play` / `open` sem caminho usam o único jogo do laboratório. Dois listam os nomes e pedem o caminho. O starter não é o jogo. Não varre a raiz do disco. `executed` continua falso. |
| 0.9.138 | `note`, `next`, `feel` e `playtest` sem caminho usam o mesmo resolvedor. Achar o único jogo não sente e não assiste. `felt` / `observed` / `outsider` continuam falsos. |
| 0.9.139 | O pedido que chega antes do WAV fica na fila e toca quando o buffer entra. Sem segunda legenda. `heard` continua falso. |
| 0.9.140 | A porta e o fim nomeiam sessão volátil e gravação que não ficou. `handle.persist` expõe o estado. `trusted` continua falso. |
| 0.9.141 | Tecla ligada e toque retomam o `AudioContext` suspenso no gesto. Resume no quadro chega tarde. `heard` continua falso. |
| 0.9.142 | Os stems SFX começam o fetch juntos. Collect não espera dash+land+graze. Wav no lugar não pede ogg. `heard` continua falso. |
| 0.9.143 | O raspo estreita o corpo, empurra a câmera na direção e acende menos que a queda. Sem hitstop. Sem pulso. `felt` continua falso. |
| 0.9.144 | `start` / `play` / `guide` devolvem `url` (`http://localhost:8080/` no serve). O prompt pede o navegador. Sem script `serve`, a chave some. `executed` continua falso. |
| 0.9.145 | `ship` devolve `artifact_open` quando `dist/` está completo no HEAD atual. O convite usa esse comando. `elsewhere` continua falso. |
| 0.9.146 | `VERSION.json` na raiz some o Gravar do achado e do recibo. Copiar permanece. `outsider` continua falso. |
| 0.9.147 | Sem clipboard, ou se `writeText` recusa, o Copiar baixa `achado.md`. Baixar não grava. `outsider` continua falso. |
| 0.9.148 | No primeiro `over` a página rola até `#finding` / `#note` e foca o primeiro campo. Título com last-run não rola. `outsider` continua falso. |
| 0.9.149 | Estilhaço no trilho do corpo vira `perigo à frente` na região viva, com a última legenda. Sem SFX novo. `verified` continua falso. |
| 0.9.150 | `duckMs` abaixa só `music`. Hit e guarda não somem sob o próprio aviso. `heard` continua falso. |
| 0.9.151 | `dashWindup` também é graça: o coil atravessa o estilhaço. Sem punch novo. `felt` continua falso. |
| 0.9.152 | `start` não planta os seis rascunhos. `fresh_starter_cycle` aceita zero do ciclo. `areas.not_located` só bloqueia quem ainda não abre. `init` e `--docs` continuam plantando. |
| 0.9.153 | `start` / `play` / `guide` devolvem `runtime`: Node no PATH se o play pede npm ou node. Sem 20+ o prompt avisa. Não executa o serve. `usable` é só o binário. |
| 0.9.154 | O prompt nomeia `Sessão:` quando o manifesto declara `session`. `start` / `play` / `guide` devolvem a chave. Não executa. Simulação não é partida observada. |
| 0.9.155 | Spawn 3: `closeIntervalScale` aperta o intervalo nos últimos 10 s. Ausente fica `1`. dusk aperta mais que spawn; calm menos. Recuperação e fecho se multiplicam. Não promove pacing. |
| 0.9.156 | O fecho com corrente viva pede guardar de novo. Reusa `hint_bank`. Pad e toque continuam calados depois da primeira guarda. Sem corrente o aviso some. Não promove feel. |
| 0.9.157 | O `guide` sem destino nomeia `Verbo:` / `Porta:` no prompt. Starter mudo continua sem. `process.md` aponta `start`, não só `init`. Não executa. |
| 0.9.158 | Spawn 4: `closeHazardScale` sobe o estilhaço nos últimos 10 s. Ausente fica `1`. dusk sobe mais que spawn; calm menos. O pulso acende o campo (`flashClose`). Não promove pacing. |
| 0.9.159 | `closeBedRate` desloca o tom da cama com o pulso do fecho. Sem pedido a cama fica em `1`. Não é duck. Não promove `heard`. |

`python3 scripts/game.py` sem subcomando é o `guide`. `--idea` no parser
principal também funciona sem subcomando.

---

## Barra vigente do starter

Piso percebido = **mínimo**. Só `release` está em `prototype`.

| Dimensão | Degrau | Lacuna seguinte |
| --- | --- | --- |
| feel | playable | fecho pede guardar no disco; peso no dispositivo; coil no disco ≠ felt |
| legibility | playable | stub ≠ dispositivo |
| art_direction | slice | `consistent` falso |
| audio_mix | slice | cama sobe o tom no disco; `heard` falso |
| pacing | slice | fecho aperta intervalo e risco no disco; curva com outsider pendente |
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
- Após `init` ou `start`, `next` exige `playable.unplayed` primeiro (enquanto não
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
- `INIT_DOCUMENTS` permanece 7. `start` não os planta (padrão
  `documents=False`; CLI `--docs` opta). `fresh_starter_cycle` aceita
  zero rascunhos do ciclo **ou** os seis com marcador. Qualquer um dos
  seis sem marcador encerra o atalho. `areas.not_located` só bloqueia
  projeto **sem** comando de jogar.
- `INIT_COPY_SKIP` inclui `dist`, `node_modules`, `.git` e
  `__pycache__`. Bytecode no starter vivo não entra no projeto.
- Não ensinar pad/touch no coach **antes** de `lastSource` nem
  **depois** da primeira guarda. O fecho com corrente viva pede
  `bank` (reusa `hint_bank`); sem corrente, ou fora do fecho,
  a primeira guarda continua encerrando o ensino.
- Não promover pacing/art/feel/a11y por convite, CSS, faixa, contorno,
  LAN, caption, marca de queda, botão de remap, panner, halo, vinheta,
  ponta, tela de título, chuva da porta, `gameSpeed` no disco, `hold` no stub,
  coil/windup no disco, `bank.windupTicks` no disco, `closeIntervalScale` no disco, `closeHazardScale` no disco, `closeBedRate` no disco, aviso de guardar no fecho, copiar ou gravar o achado, last-run,
  anexo do achado, recibo da página, `?seed=`, `then.seed`,
  `then.invite`, `invite_href`, copiar o endereço do convite,
  levar a chuva ou o look na URL, tinta estável no disco,
  estilhaço dusk no disco, intenção warmer no disco,
  punch da queda no disco, números da partida na
  faixa do achado, `play` achar o único jogo do
  laboratório, `note` / `next` / `feel` / `playtest`
  acharem o mesmo jogo, fila do mixer no primeiro
  WAV, aviso de save na porta, resume do
  contexto no gesto, stems SFX em
  paralelo, punch do raspo no disco,
  `url` da abertura, `artifact_open`
  do dist/, some o Gravar no
  artefato, fallback do Copiar,
  rolar o painel no over,
  região viva do perigo,
  duck só na cama, graça no coil
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
- `start` não planta os rascunhos (`documents=False`). CLI `--docs`
  opta; `--no-docs` permanece e é o padrão. `init` continua
  plantando. `--idea` entra em `data/copy.json`; brief só com `--docs`.
- `start` / `play` / `guide` devolvem `runtime` (`node`, `major`,
  `need`, `asked`, `usable`, `executed` falso). `asked` se o play
  casa `npm|node`. `usable` é major ≥ 20 ou o play não pede Node.
  Sem usable o prompt avisa. Não executa o serve.
-   Se `then.session` existe, o recibo sobe `session` e o prompt do
  primeiro ciclo nomeia `Sessão:`. Sem script, a chave é nula e a
  linha some. Não entra em `CYCLE_KEYS`. Depois de um recibo o
  prompt de ofício não repete a sessão. Não executa. Simulação
  não é partida observada. Sem destino, `guide_prompt` também
  cola `cycle_line` (Verbo / Porta / teclas) se o starter declara.
  Starter mudo não inventa.
- `start` devolve `open` (= `play`), `url` e `steps` (3, passo 1 feito).
  `guide` sem destino: `open` é o start. Os dois: `executed` falso.
  `url` é `http://localhost:<PORT>/` só se o script for `serve`
  (`PORT` positivo; vazio → 8080; `PORT=0` → sem url). Não é
  `then.url`. Nomear não serve.
- `play` / `open` (CLI) apontam o serve do projeto existente e a
  mesma `url`. Não criam, não executam. Sem caminho: `here_project`,
  o único vizinho jogável do laboratório, a lista dos nomes se
  houver dois, ou “sem destino”. Não escolhe o starter. Não varre `/`.
- `note` / `next` / `feel` / `playtest` (CLI) usam
  `require_project_destination` — o mesmo resolvedor. `note`
  continua exigindo `--author` e `--note`. Achar o jogo não
  sente, não assiste e não promove.
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
- `ship` devolve `artifact_open` só se `dist/` está completo e o HEAD
  do VERSION.json é o checkout. O valor é
  `cd <dist> && node tools/serve.mjs`. Incompleto ou stale some a
  chave. Não é `url`. Nomear não executa. `elsewhere` falso.
  `next` nomeia `ship.artifact_open` depois de stale, nunca na
  frente de `cycle.craft` / `playable.unplayed`.

**Starter**

- Looks first-party: `normal`, `dusk`, `calm`. Contrast é alcance.
- Chuvas first-party: `spawn`, `dusk`, `calm`. Spawn 4: `closeIntervalScale`
  (spawn 0.72, dusk 0.58, calm 0.86) e `closeHazardScale` (spawn 1.22,
  dusk 1.36, calm 1.12). Ausente ou ≤ 0 vira `1`. `spawnIntervalScale`
  multiplica recuperação e fecho. `spawnHazardChance` aplica o risco
  do fecho depois da prática. `flashClose` no pulso. Não promover
  `pacing`.
- `listMoods()` = interseção look ∩ spawn (hoje `calm`, `dusk`).
- `SOUNDS`: dash, land, graze, collect, missed, bank, hit, over, close, live, stir, bed.
  Pedido sem buffer: last-wins na fila; `register` toca sem segunda
  legenda. `dispose` esquece. Tecla ligada e toque chamam
  `audio.unlock()` no gesto. Stems sobem juntos (`Promise.all`);
  extensão seguinte só se a atual falhou.   `duckMs` abaixa só
  `music` (`DUCK_BUSES`). `update({ bedRate })` desloca o tom da
  cama; `bedRateFor` lê o pulso do fecho. Não é duck. `heard` falso.
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
  `hold` leva `bankWindup`.
- Avanço na partida: `dashWindupTicks` (2) senta com `squashCoil`
  antes de `fireDash`. Esses ticks também são graça: o coil
  atravessa o estilhaço. A porta (`beginRun`) continua imediata.
  Guardar corrente já existente: `bank.windupTicks` (2) senta
  antes de converter. Coleta e guarda no mesmo quadro continuam
  na hora. Raspo (`grazeContact`): estreita, punch na direção,
  flash menor que a queda. Sem hitstop. Sem rumble.
  Não promover `feel`.
- Coach: fantasy → move → dash → miss → touch/pad → collect → null após
  1ª guarda. Exceção: `closingWindow` e `chain > 0` devolve `bank`
  mesmo depois da primeira guarda. Sem corrente o fecho não ensina.
  Pad/touch não voltam. `coachHint` some se `phase !== "playing"`.
- `copy.fantasy` alimenta a abertura **e** os 48 ticks do aviso.
- `title_play` / `title_again` / `title_new` / `title_last` /
  `title_volatile` / `title_unsaved` /
  `over_door` / `over_door_inline` em `COPY_FIELDS` (default `{dash}`).
  A porta e o fim leem `persistLine`. Nomear não é `trusted`.
  `migrateCopy` preenche default se a mesa antiga não tiver.
- Invite (`?invite=1`) some `#commands`, não `#remap`. Com seed no
  last-run, `/?invite=1&seed=<n>` some a tabela e abre essa partida.
  Com chuva nomeada e ≠ `spawn`, junta `&spawn=<mesa>`. Com look
  nomeado e ≠ `normal`/`contrast`, junta `&look=<paleta>`. Spawn
  ou look inválido, e os nomes padrão, somem.
  `VERSION.json` na raiz (`readArtifactMark`) some `#finding-save`
  e `#note-save`. Copiar permanece. Sem clipboard, `offerFinding`
  baixa `achado.md`. Baixar não grava. Nomear não é `outsider`.
  `#finding` aparece com `html.invite.finding` no `over` e na `title`
  se houver `lastRun`. `bringPanel` só no primeiro `over`. Título com
  last-run não rola. Copiar não grava. Gravar só se `playFinding`
  devolver texto. Esqueleto vazio não casa `FINDING_FIELDS`. Achado
  `.md` ≠ recibo `record.json`.
- Serve POST `/playtest/last-run` grava `docs/playtest/last-run.json`.
  Força `observed`/`felt` falsos e `policy: played`. Árvore
  exportada responde 403. Sem canvas o headless não posta.
- Serve POST `/playtest/note` grava `docs/playtest/<utc>/record.json`.
  Nota vazia é 400. Autor vazio vira `página`. Anexa last-run se
  existir. `#note` no `over` e na `title` se houver `lastRun`, fora
  do convite. `bringPanel` só no primeiro `over`. Título com last-run
  não rola. Com seed, `#note-invite` aponta o endereço e copia —
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
  `threatCue` é estilhaço no x do corpo dentro do telegraph.
  `#live` espelha fase, perigo e a última legenda. Texto no DOM
  não é sessão. Não promover `accessibility`.

---

## Lacunas ainda abertas (priorizar alinhamento, não facilidade de teste)

Saltos alinhados: feel visível/audível, ferramenta de outsider, superfície
de entrada, auditoria item 1, ou atrito ideia→jogo. **Não** mais um
script de medição. **Não** mais um `play` sem caminho. **Não** mais
um `note` sem caminho. **Não** mais a fila do mixer. **Não** mais
aviso de save na porta. **Não** mais resume do contexto.
**Não** mais waterfall ou paralelo do SFX.
**Não** mais punch/shake em outro verbo.
**Não** mais um `url` / href de abertura.
**Não** mais um comando de servir o `dist/`.
**Não** mais some o Gravar no artefato.
**Não** mais fallback de clipboard do achado.
**Não** mais rolar o painel no over.
**Não** mais região viva do perigo.
**Não** mais duck só na cama.
**Não** mais graça no coil do avanço.
**Não** mais plantar os seis rascunhos no `start`.
**Não** mais exigir `FRESH_DRAFTS` para o atalho do primeiro ciclo.
**Não** mais um campo que só relê o `doctor` sem mudar o prompt.
**Não** mais esconder a sessão no `then` enquanto o prompt só cola o serve.
**Não** mais um fecho que só pisca enquanto o dado já nomeia o aperto.
**Não** mais um fecho que come a corrente viva sem pedir guardar.
**Não** mais um `guide` que esconde a porta no JSON enquanto o stderr só cola o start.
**Não** mais um fecho que só enche a chuva enquanto o risco fica no teto da rampa.
**Não** mais uma cama que ignora o fecho enquanto o campo grita.

Candidatos, do que ainda dói:

1. **Release (define o piso):** outra máquina correr o `dist/`. Não
   promover. `ship` já nomeia árvore incompleta, HEAD velho,
   `artifact_open` e `elsewhere` falso; o comando colável não é a
   prova.
2. **Idéia→jogo:** `start` devolve `open` e `url`; `play` / `open`
   os reimprimem. Sem caminho, o único jogo do laboratório basta;
   dois pedem o caminho. `note`, `next`, `feel` e `playtest`
   usam o mesmo resolvedor. O `prompt` também sai em stderr. A
   partida no serve grava o candidato e, se você escrever, o
   recibo. No convite a página grava o achado se os quatro
   tiverem texto e anexa o candidato se last-run existir.
   `?seed=` abre a seed do candidato. Depois de um last-run,
   `then.seed` aponta o endereço da partida (número, chuva e
   look quando o candidato os nomeia) e o convite junta os
   mesmos eixos.    Nomear `url` não serve. Não auto-servir.
   `runtime` lê o Node do PATH; sem 20+ o prompt avisa.
   O prompt nomeia `Sessão:` se o manifesto declara `session`.
   Sem destino, o `guide` também nomeia `Verbo:` / `Porta:` se o
   starter declara. `len(steps) == 3` e `executed: false` continuam.
3. **Checkpoint do tick:** `hold` existe. A porta nomeia sessão
   volátil e gravação recusada. Falta aba fechada real.
   Não promover. Não chamar `hold` de Continuar.
4. **Item 1 residual:** o mapa, as receitas de foco e os templates da
   primeira situação — brief, GDD, game-design, PoC, slice, QA e
   release — já nomeiam a porta. O rascunho de playtest traz a forma
   do achado, vazia. Referências que ainda falarem só do campo sem a
   abertura estão velhas. Nomear não entrega.
5. **Outsider / pacing / a11y real / feel no dispositivo:** não
   promover. Convite, LAN, stub, `gameSpeed` no disco, tinta
   estável no disco, estilhaço dusk no disco, intenção warmer no
   disco, copiar o achado,
   gravar os quatro nomes, mostrar seed/pontos/eixos na faixa,
   anexar last-run, `play` achar o único jogo, `note` achar
   o mesmo jogo, a fila do mixer no primeiro WAV, o aviso
   de save na porta, o resume no gesto e o
   paralelo dos stems SFX, o punch do raspo
   no disco, o `url` da abertura e o
   `artifact_open` do dist/ e some
   o Gravar no artefato e o
   fallback do Copiar e rolar
   o painel no over e a
   região viva do perigo e o
   duck só na cama e a graça
  no coil do avanço e o
  aperto do fecho no
  disco e o aviso de
  guardar no fecho e o
  risco do fecho no
  disco e o tom da
  cama no fecho não
  fecham. A receita
   de velocidade ajustável já tem knob; falta a sessão.
6. **Volume de conteúdo:** três chuvas + `pair` ainda não são volume.
   Não nascer look/chuva first-party novo como craft.

`init` ainda cria 6 rascunhos de propósito (`fresh_starter_cycle`).
O `start` não. `--docs` no start ou o `init` os planta.

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

Arquivos quentes da última sessão: `bedRateFor` + `audio.update({
bedRate })`. Sem pedido a cama fica em 1. Não é duck.
Não promover heard.
