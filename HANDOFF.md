# Handoff — fácil + AAA honesto

**Branch:** `cursor/framework-0-9-facil-e-aaa-1083` (base `main`)
**PR:** [#4](https://github.com/oalanicolas/alanstudio-framework/pull/4) (draft)
**HEAD:** ver `git log -1` — vigente 0.9.254: o painel relê a lacuna quando o fetch termina. Pintar só no boot some o que chegou. Não promove `heard`.
**Goal:** ativo. Não marcar complete. AAA fácil ainda não está provado.

**Testes no HEAD:** `python3 -m unittest discover -s tests` → 288 OK.
`cd assets/starters/canvas-arcade && npm test` → 429 OK.

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

## O que o HEAD já entrega (0.9.91–0.9.254)

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
| 0.9.160 | O overlay do fim reusa `record` com `extra.best`. Recorde 0 some. Sem faixa nova. Não promove feel. |
| 0.9.161 | `attractMove` desloca o corpo na porta sem comer o tick. O aviso pede fantasia e mover no relógio da mostra. Dash, coleta e guarda ficam no campo. `advance` na porta continua no-op. Não promove feel. |
| 0.9.162 | `attractTouch` acende e estreita quando a mostra cruza o corpo. Sem pontuar, sem punch, sem seed. `threatCue` lê a mostra; o live nomeia o perigo. O pulso vence a cortina. Não promove feel. |
| 0.9.163 | `attractTick` emite `live` uma vez na porta. Mesma voz do campo. Sem cama. Sem rumble. O laço toca o evento sem abrir o ciclo. Não promove `heard`. |
| 0.9.164 | `cycle_line` nomeia `Fantasia:` antes de `Verbo:` quando `--idea` ou `copy.json` têm frase. O guide não grava. A frase não muda o verbo. Não entra em `CYCLE_KEYS`. |
| 0.9.165 | `init_scope` distingue rascunhos plantados. Sem docs não afirma brief nem `draft_only`. `preproduction.md` ensina `start --idea`; `init` continua o que planta. O `context` injeta esse arquivo. Não promove. |
| 0.9.166 | `doctor` no laboratório vazio devolve `then.guide`. Sem starter o aviso nomeia `start --idea`, não `init`. Com jogo a chave some. Sem `prompt`. Não cria e não executa. |
| 0.9.167 | O aviso do primeiro ciclo nomeia o estilhaço quando a corrente voltou a zero (`hint_hit`). Dash no trilho vence. A porta não ensina. Copy 3. Não promove feel. |
| 0.9.168 | Na graça do erro o corpo some e volta no relógio do contorno. `fillRect` permanece. Reduced trava o tijolo. Não promove feel. |
| 0.9.169 | O `over` pede fade na cama. Pause, title e aba escondida cortam seco. Play no meio do fade nasce de novo. Não promove `heard`. |
| 0.9.170 | O `over` senta o corpo (`squashOver`). Larga dash, graça e arco da guarda. `fillRect` permanece. Não promove feel. |
| 0.9.171 | A região viva nomeia `pausado`. Overlay do canvas não chega ao leitor. Não promove `accessibility`. |
| 0.9.172 | `beforeunload` descarrega o mesmo hold do `pagehide`. Não pausa. Stub não é aba fechada. Não promove `trusted`. |
| 0.9.173 | `sfx summary` lista stems, licença e origem do starter. Acervo vazio não some o que já fala. Não promove `heard`. |
| 0.9.174 | `sfx search` nomeia o stem do starter que casa (chave, arquivo, licença, origem). `count` continua o acervo. Não promove `heard`. |
| 0.9.175 | A região viva nomeia placar e recorde no fim e na porta. Overlay do canvas não chega ao leitor. Não promove `accessibility`. |
| 0.9.176 | O `over` senta tremor, flash e punch. O corpo já sentava. Pose no disco não é felt. Não promove feel. |
| 0.9.177 | `sfx serve` gera a página de escuta se `shared/sfx/ui` faltar. Tocar não é `heard`. Catálogo vazio continua recusado. |
| 0.9.178 | A pausa corta as vozes do verbo (`hush`). A cama continua no stop seco. Overlay Pausado com hit no ar era a mesma partida. Não promove `heard`. |
| 0.9.179 | `sfx info` lê a ficha do stem do starter que casa (chave, arquivo, licença, origem). Id do acervo continua na frente. Não promove `heard`. |
| 0.9.180 | A pausa senta tremor, flash e punch. O over já sentava o quadro. Overlay Pausado com câmera no golpe era a mesma partida. Não promove feel. |
| 0.9.181 | A pausa nomeia o placar no overlay e na região viva. Recorde 0 some. Jogando sem pausa o número não entra. Não promove `accessibility`. |
| 0.9.182 | No fim a cortina do over vence a pausa. P e aba escondida não comem Fim, corrente nem porta. Não promove feel. |
| 0.9.183 | `sfx verify` nomeia os stems do starter quando o acervo está vazio. Não cruza. `ok` fica falso. Não promove `heard`. |
| 0.9.184 | A região viva só diz `pausado` quando o overlay diz Pausado. No fim e na porta a palavra some. Não promove `accessibility`. |
| 0.9.185 | No fim a pausa não come o stinger. No campo o `hush` continua. Não promove `heard`. |
| 0.9.186 | Na porta a aba escondida só descarrega. Não congela a mostra. Não promove `trusted`. |
| 0.9.187 | `playtest` unstructured aponta `#finding` e `note --field`. O leitor não finge gravar. Não promove `outsider`. |
| 0.9.188 | `roles --fill` nomeia o stem do starter quando o acervo está vazio. `--apply` não copia o starter. Não promove `heard`. |
| 0.9.189 | Na porta o avanço também aterrisa. Sem contar o ofício, sem recovery. Não promove feel. |
| 0.9.190 | No fim a região viva nomeia a corrente que o overlay já mostra. Sem corrente o rótulo some. Não promove `accessibility`. |
| 0.9.191 | No arco da guarda o corpo também atravessa o estilhaço. Sem punch novo. Não promove feel. |
| 0.9.192 | Perder o orbe também senta o corpo. Menor que a coleta. Sem rumble. Não promove feel. |
| 0.9.193 | `feel` nomeia `then.play` e `then.note` sem executar. Sem serve a chave some. Sem `prompt`. Não promove `felt`. |
| 0.9.194 | `save` relata `warned` se o disco nomeia sessão volátil. Nomear não é aba fechada. Não promove `trusted`. |
| 0.9.195 | Na porta e no fim a região viva nomeia o aviso da sessão que o canvas já mostra. Jogando a chave some. Não promove `trusted`. |
| 0.9.196 | Na porta o telegraph marca a mostra. O live já nomeava o perigo; o trilho calava. Sem faixa nova. Não promove feel. |
| 0.9.197 | A câmera inclina para o que o trilho já marca (`lookAheadX`). Menor que o punch do dash. Sem punch novo. Não promove feel. |
| 0.9.198 | `sfx export` / `sfx copy` levam bytes e créditos do stem do starter. `--apply` continua só o acervo. `next` aponta `sfx copy`. Não promove `heard`. |
| 0.9.199 | `gameSpeed` só dilata o relógio em `playing`. Porta e fim ficam no relógio cheio. `advance()` continua ignorando. Não promove `accessibility`. |
| 0.9.200 | `assist` cede queda e alcance também na mostra da porta. Graça extra fica no campo. Não promove `accessibility`. |
| 0.9.201 | `reducedMotion` na porta trava toque e live na mesma mostra que o canvas já para. O campo continua caindo. Não promove `accessibility`. |
| 0.9.202 | O quadro que converte a guarda também atravessa o estilhaço. Sem punch novo. Não promove feel. |
| 0.9.203 | Design system, ambição, barra, checklist e os pacotes de gênero nomeiam a porta. O `context` já os injeta. Não promove feel. |
| 0.9.204 | O quadro do `land` também atravessa. A recuperação depois continua vulnerável. Sem punch novo. Não promove feel. |
| 0.9.205 | O segundo estilhaço do mesmo quadro já é graça. Relê `invuln` depois do `hit()`. Sem janela nova. Não promove feel. |
| 0.9.206 | `discover` / `review` nomeiam os mesmos sinais que o `next` usa. Sem proposta. Sem urgência. Não promove `observed`. |
| 0.9.207 | `playtest` nomeia `form` e `fields`. Sem `then`. Esqueleto no disco não é achado. Não promove `outsider`. |
| 0.9.208 | `origins --declare` escreve o sidecar. `next` aponta o declare, não relê o leitor. Recibo no disco não é licença. Não promove `granted`. |
| 0.9.209 | `note` nomeia `finding`, `form` e `needed`. Sem `then`. Recibo sem os quatro não é achado. Não promove `observed`. |
| 0.9.210 | Dois orbes no mesmo quadro não inflam a corrente. O segundo espera o próximo tick. Sem suco empilhado. Não promove feel. |
| 0.9.211 | A legenda da coleta e da guarda nomeia a corrente que o tom já sobe. Sem o número o tom falava e a faixa calava. Não promove `heard` nem `accessibility`. |
| 0.9.212 | Orbe e estilhaço no mesmo quadro: o estilhaço letal resolve; o orbe espera. Ordem do array não decide a aposta. No dash os dois atravessam. Não promove feel. |
| 0.9.213 | Na raiz do framework, `guide` / harness sem `--idea` recusam — não devolvem `start '<destino>'`. Subpasta e `guide_cycle` continuam o mapa. Não executa. |
| 0.9.214 | `doctor.then.guide` aponta `guide --idea <fantasia>`. O comando nu quebrava na raiz depois do 0.9.213. Não cria e não executa. |
| 0.9.215 | A barra de `accessibility` do starter não atribui medição no dispositivo ao `contrast`. O critério nomeia o stub; o aparelho continua pendente. Não promove `accessibility`. |
| 0.9.216 | Na porta o `#live` nomeia o toque da mostra (`a mostra toca` / `a mostra raspa`). Sem fingir coleta. Sem voz nova. Não promove `accessibility`. |
| 0.9.217 | `roles --apply` copia o stem do starter com créditos. Sem acervo, `next` aponta `--apply`, não `sfx copy`. Não promove `heard`. |
| 0.9.218 | A legenda do erro lê `lost`. Aposta zero ou ausente fica `atingido`; `lost > 0` nomeia a corrente que caiu. Não herda `chain`. Não promove `heard` nem `accessibility`. |
| 0.9.219 | O arco da guarda senta com `squashBankCoil`. O coil do avanço continua estreitando. Sem voz nova. Não promove feel. |
| 0.9.220 | O coil do avanço não some quando a guarda pede no mesmo tick. A guarda com corrente espera; coleta e guarda no mesmo quadro continuam na hora. Não promove feel. |
| 0.9.221 | A tinta estável não esmaga a chuva do look que já separa quente e frio. O par do padrão continua o fallback. Não promove `accessibility` nem `art_direction`. |
| 0.9.222 | Orbe que cai no arco da guarda espera. O sit não inflama a aposta; depois do commit o orbe entra. Coleta e guarda no mesmo quadro continuam na hora. Não promove feel. |
| 0.9.223 | O relógio não come a guarda que já sentou. O sit converte antes do `over`. Sem sit a corrente continua caindo. Não promove feel. |
| 0.9.224 | O hitstop não alonga o relógio no fim. O limite encerra mesmo durante o congelamento. Não promove feel. |
| 0.9.225 | A queda não come o verbo em curso. Marca o chão; não senta avanço, coil nem sit da guarda. Não promove feel. |
| 0.9.226 | A guarda leva o x do campo. A aposta não fala no centro. Não promove `heard`. |
| 0.9.227 | A fantasia na porta não come o aviso de mover. Depois da frase a porta ainda ensina a abrir. Não promove feel. |
| 0.9.228 | Depois da porta o campo não repete a frase nem o mover. Dash e coleta entram. Headless ainda vê a frase. Não promove feel. |
| 0.9.229 | O `context` não manda documentar um `start` fresco. `audit.deferred`; o `next` já pedia jogar. `--event direction-approved` e `--stage audit` continuam pedindo a base. Não promove. |
| 0.9.230 | O `init` aponta a mesma superfície do `start`: `open`, `url`, `prompt` no stderr. Não executa. Não promove. |
| 0.9.231 | O arco da guarda não mente que o dash está pronto. `dashCharge` trava como no `bankLock`. Não promove feel. |
| 0.9.232 | O raspo no avanço não come a pose do dash. A graça parada continua pinçando. Não promove feel. |
| 0.9.233 | A coleta no avanço não congela nem senta o dash. Parada continua com hitstop e sit. Não promove feel. |
| 0.9.234 | O `next` do ciclo fresco aponta `note`, não um segundo `next --focus feel`. `init.next_commands` também. `then.lost` continua o next. Não executa. |
| 0.9.235 | A coleta no land e no quadro da conversão não come o sit do compromisso. Parada continua com hitstop e sit. Não promove feel. |
| 0.9.236 | Na porta o arraste move sem abrir; o tap abre. No campo o down de cima continua o avanço. Não promove feel. |
| 0.9.237 | O pedido de dash sobrevive ao lock da guarda. A recarga continua contando o perdão. Não promove feel. |
| 0.9.238 | O rumble do quadro toca o verbo mais pesado, não o último. Porta fala dash; commit fala guarda. Não promove feel. |
| 0.9.239 | O avanço é o aperto, não o segurar. Segurar na porta não dispara o ofício; no campo o cooldown não metralha. A guarda continua nível. Não promove feel. |
| 0.9.240 | O `start` escreve `AGENTS.md` com o comando que abre. Sem rascunhos, a memória não lista GDD. `documents` continua vazio. Não executa. |
| 0.9.241 | O pedido no contexto suspenso espera o gesto. A porta e o primeiro avanço não disparam no vazio. Não promove `heard`. |
| 0.9.242 | `template agents` e o `next` sem AGENTS geram a memória do disco. Sem rascunhos não listam GDD. Não executa. |
| 0.9.243 | Na porta o tap na faixa da guarda também abre. O polegar no primeiro gesto não cala a abertura. Não promove feel. |
| 0.9.244 | O controle também pede o resume. Tecla e toque já pediam; o pad falava e a porta ia para a fila. Não promove `heard`. |
| 0.9.245 | O fim leva o x do campo. O stinger da partida não fala no centro. Não promove `heard`. |
| 0.9.246 | O processo comum nomeia a porta. O mapa start → jogar → `note` aponta sem executar. Não observa. |
| 0.9.247 | A guarda espera o land do avanço. O sit não come a pose do dash; o pedido não decai no travel. Coleta no mesmo quadro continua na hora. Não promove feel. |
| 0.9.248 | Preferências ilegíveis avisam. `settingsLoad` espelha o progresso; o painel nomeia a recuperação; a porta não. Não promove `trusted`. |
| 0.9.249 | `roles --apply` recoloca o stem quando o recibo já está. Origem e licença diferentes recusam. Não promove `heard`. |
| 0.9.250 | O painel nomeia o papel que o fetch perdeu. O loader marca o primário; variante ausente não é lacuna. Não promove `heard`. |
| 0.9.251 | Decode nulo tenta a próxima extensão. Wav ilegível não esconde o ogg nem o pedido. Não promove `heard`. |
| 0.9.252 | A região viva nomeia a recuperação que o painel já mostra. A porta não. Jogando a chave some. Não promove `trusted`. |
| 0.9.253 | `sfx copy` do acervo recoloca o WAV quando origem e licença casam, e declara `heard` falso. Recibo diferente recusa. Não promove `heard`. |
| 0.9.254 | O painel relê a lacuna quando o fetch termina. Pintar só no boot some o que chegou. Não promove `heard`. |

`python3 scripts/game.py` sem subcomando é o `guide`. Na raiz do
framework, sem `--idea` e sem caminho, recusa com `sem destino`.
`--idea` no parser principal também funciona sem subcomando.

---

## Barra vigente do starter

Piso percebido = **mínimo**. Só `release` está em `prototype`.

| Dimensão | Degrau | Lacuna seguinte |
| --- | --- | --- |
| feel | playable | a guarda espera o land; o tap na faixa da porta abre; o avanço é o aperto; peso no dispositivo; coil no disco ≠ felt |
| legibility | playable | stub ≠ dispositivo |
| art_direction | slice | tinta estável não esmaga dusk/calm; `consistent` falso |
| audio_mix | slice | o painel relê a lacuna quando o fetch termina; decode nulo tenta a próxima extensão; o painel nomeia o 404 mesmo quando outro papel registrou; o fim leva o x do campo; o controle também pede o resume; o pedido suspenso espera o gesto; `heard` falso |
| pacing | slice | fecho aperta intervalo e risco no disco; curva com outsider pendente |
| state_trust | slice | live nomeia a recuperação que o painel já mostra; a porta não; `save` relata `warned`; beforeunload no disco; aba fechada real não observada; `trusted` falso |
| performance | playable | poços + stub ≠ dispositivo |
| accessibility | slice | live nomeia a recuperação das preferências; tinta estável não esmaga dusk/calm; live nomeia o toque da mostra; sessão real pendente |
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
  a primeira guarda continua encerrando o ensino. A porta não
  ensina pad, toque, dash, coleta nem guarda.
- Não promover pacing/art/feel/a11y por convite, CSS, faixa, contorno,
  LAN, caption, marca de queda, botão de remap, panner, halo, vinheta,
  ponta, tela de título, chuva da porta, `gameSpeed` no disco, `hold` no stub,
  coil/windup no disco, `bank.windupTicks` no disco, `closeIntervalScale` no disco, `closeHazardScale` no disco, `closeBedRate` no disco, recorde no overlay do fim, aviso de guardar no fecho, `hint_hit` no disco, pulso do corpo na graça, copiar ou gravar o achado, last-run,
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
  ou avanço no overlay, recorde no overlay do fim
  ou movimento na porta ou toque da mostra ou voz da mostra
  ou quadro sentado na pausa ou placar na pausa ou fim que vence a pausa
  ou verify dos stems do starter ou live que some pausado no fim
  ou hush no over que poupa o stinger
  ou hidden na porta que poupa a mostra
  ou playtest que aponta o painel do achado
  ou fill que nomeia o stem do starter
  ou porta que fecha o arco do avanço
  ou live que nomeia a corrente no fim
  ou graça no arco da guarda
  ou queda que senta o corpo
  ou feel que nomeia o serve
  ou save que nomeia o aviso
  ou live que nomeia o aviso
  ou porta que marca a mostra no trilho
  ou câmera que confirma o trilho
  ou export que some o stem do starter
  ou relógio da partida que some a mostra
  ou assistência que some a mostra
  ou reduced que some o toque da mostra
  ou conversão da guarda que é janela de hit
  ou mapa canônico que some a porta
  ou processo comum que some a porta
  ou land que é janela de hit
  ou segundo estilhaço do mesmo quadro que é segundo hit
  ou dois orbes no mesmo quadro que inflam a corrente
  ou orbe e estilhaço no mesmo quadro que decidem pela ordem
  ou guide na raiz que devolve start '<destino>'
  ou doctor.then.guide que aponta o guide nu
  ou legenda da coleta que some a corrente que o tom já sobe
  ou discover que some o sinal do next
  ou playtest que some o esqueleto dos quatro
  ou next que declara origem relendo origins
  ou note que some se o recibo fechou o achado
  ou barra de accessibility que atribui medição no dispositivo ao contrast
  ou live que nomeia o toque da mostra
  ou roles --apply que some o stem que o fill já nomeia
  ou legenda do erro que mente corrente perdida com aposta zero
  ou arco da guarda que copia o coil do avanço
  ou coil do avanço que some quando a guarda pede
  ou tinta estável que esmaga a chuva do look que já separa
  ou orbe no arco da guarda que inflama a aposta
  ou relógio que come a guarda que já sentou
  ou hitstop no fim que alonga o relógio
  ou queda longe que senta o verbo em curso
  ou guarda que fala no centro
  ou fantasia na porta que come o aviso de mover
  ou campo que repete a frase e o mover da porta
  ou context que manda documentar um start fresco
  ou init que planta e some a superfície
  ou arco da guarda que mente que o dash está pronto
  ou raspo no avanço que come a pose do dash
  ou coleta no avanço que congela e senta o dash
  ou next do ciclo fresco que aponta um segundo next
  ou coleta no land ou no quadro da conversão que come o sit do compromisso
  ou toque na porta que abre no down e some o arraste
  ou pedido de dash que morre no lock da guarda
  ou rumble do quadro que toca o último verbo e some o peso
  ou avanço que lê o hold e metralha no cooldown
  ou o mesmo aperto da porta que dispara o ofício no campo
  ou o `start` que deixa a próxima sessão sem memória
  ou o AGENTS do start que lista GDD que não plantou
  ou o pedido no contexto suspenso que dispara no vazio
  ou o template agents que lista GDD que o disco não tem
  ou o tap na faixa da porta que some o abrir
  ou o controle que fala e some o resume
  ou o fim que fala no centro
  ou o processo comum que some a porta
  ou a guarda que senta no travel e come a pose do dash
  ou preferências ilegíveis que voltam ao padrão em silêncio
  ou um roles --apply que recusa o stem porque o recibo do init tem note
  ou um painel que some o 404 quando outro papel já registrou
  ou um wav ilegível que esconde o ogg e some o pedido
  ou uma região viva que some a recuperação que o painel já mostra
  ou um `sfx copy` do acervo que recusa o WAV porque o recibo tem `note` e some `heard`
  ou um painel que pinta a lacuna no boot e some o que o fetch trouxe.
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
  `mood`. `cycle_line` nomeia `Fantasia:` antes de `Verbo:` quando
  há frase (`--idea` ou `copy.json`), `Porta:` antes de `Mover` e
  `Seed:` antes de `Convite`. Fantasia não entra em `CYCLE_KEYS`.
  A frase não muda o verbo. Sem frase a linha some.
- `CRAFT_EXAMPLES` ordem: pair → look → table → sfx. Look e chuva do
  exemplo compartilham o nome `noite`.
- `play` após `start` é `cd … && npm run serve`. Não há `npm install`.
- `start` não planta os rascunhos (`documents=False`). CLI `--docs`
  opta; `--no-docs` permanece e é o padrão. `init` continua
  plantando. `--idea` entra em `data/copy.json`; brief só com `--docs`.
  Os dois escrevem `AGENTS.md` com o comando que abre e o que o
  disco ainda não tem. Sem rascunhos a memória não lista GDD.
  `template agents` e o `next` em `agent_context.not_located`
  geram o mesmo texto a partir do disco — play, url, fantasia,
  ciclo do `starter.json` do projeto, rascunhos só se brief/GDD
  (os seis do start) existirem. O molde em `assets/templates/agents.md`
  é a referência; o comando não o preenche com caminhos inventados.
  `documents` só ganha `AGENTS.md` quando `documents` é verdadeiro.
  `init_scope(documents, idea)` é o `scope` do `init` e do
  `start.init`. Sem docs: `sem plantar`, sem `criou rascunhos`,
  sem `draft_only`, sem brief. Com docs: afirma os três. Sem
  `--idea` a linha da frase some. `preproduction.md` ensina
  `start --idea`; `init` fica o caminho que planta.
- Depois de um `start` fresco (o mesmo atalho `playable.unplayed`
  do `next`), a proposta é `play` + `note`, não um segundo
  `next --focus feel`. O `init.next_commands` usa o mesmo par.
  `then.lost` continua o next para quando o ciclo já correu.
  `scan` / `context` não pedem auditoria:
  `audit.required` falso, `audit.deferred` verdadeiro,
  `next_action` e `documentation.action` são
  `defer_until_playable_cycle`. Lacunas continuam listadas.
  `project-audit.md` some do `read_next`. Sem jogo que abre,
  lacuna continua `notify_and_document`. `--event
  direction-approved` e `--stage audit` continuam
  `document_minimum`. O harness não executa o jogo.
- `init` devolve `open` (= `play`), `url`, `runtime`, `then`,
  `fantasy`, `cycle` e `prompt`. O `prompt` também sai em stderr.
  `next_commands` é `play` + `note`. Sem serve a `url` some. Não executa.
- `doctor` devolve `empty` e `then`. Sem jogo, com starter e
  `ready`, `then.guide` é `guide --idea <fantasia>`. Sem a
  frase a raiz recusa. Com jogo, sem starter ou bloqueado,
  `then` é nulo. Sem `prompt` — o CLI não escreve stderr. O
  aviso de starter ausente nomeia `start --idea`, não `init`.
  Não cria e não executa.
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
  `guide` sem destino: `open` é o start. Na raiz do framework, sem
  `--idea`, o CLI recusa — `guide_cycle(None)` continua o mapa.
  Os dois: `executed` falso.
  `url` é `http://localhost:<PORT>/` só se o script for `serve`
  (`PORT` positivo; vazio → 8080; `PORT=0` → sem url). Não é
  `then.url`. Nomear não serve.
- `play` / `open` (CLI) apontam o serve do projeto existente e a
  mesma `url`. Não criam, não executam. Sem caminho: `here_project`,
  o único vizinho jogável do laboratório, a lista dos nomes se
  houver dois, ou “sem destino”. Não escolhe o starter. Não varre `/`.
-   `note` / `next` / `feel` / `playtest` (CLI) usam
  `require_project_destination` — o mesmo resolvedor. `note`
  continua exigindo `--author` e `--note`. Nomeia `finding`,
  `form` e `needed`. Sem `then`. Recibo sem os quatro
  não é achado. Achar o jogo não
  sente, não assiste e não promove. `playtest` só lê.
  Sem os quatro campos, o recibo traz `finding_href`
  (`/#finding` ou `/?seed=<n>#finding` com os eixos),
  `qa` se `docs/qa.md` existir, `form` (esqueleto
  canônico) e `fields`. Sem `then`. `next` em
  `playtest.unstructured` aponta o serve/`play` e
  `note --field` dos quatro nomes — não relê `playtest`
  nem `feel` como se gravassem. Esqueleto no disco
  não é achado. Escrever não é sessão.
  Sem acervo, `roles --fill` nomeia o stem do starter
  (`kind: starter`, licença, origem). `--apply` copia o
  id do acervo ou o stem do starter com créditos. Sem
  catálogo, `next` em `audio.roles` aponta `--apply`,
  não `sfx copy`. `sfx export` / `sfx copy` continuam
  o caminho explícito. `sfx copy` do acervo recoloca o
  WAV se origem e licença casam — também em `sources` —
  e declara `heard` falso. Recibo diferente recusa.
  Copiar não ouve.
- `emit()` escreve `prompt` em stderr quando a chave existe e tem
  texto. stdout continua só o JSON. Falar a frase não executa.
  `next` / `doctor` / `feel` não têm `prompt` e não escrevem frase.
  `feel.then` tem `note` e, se o projeto declara o comando de
  abrir, `play`. Sem serve a chave some. Não ganha `lost`.
  `save` relata `warned` / `warnings` se o disco tem
  `persistLine`, `title_volatile` ou `title_unsaved`. Nomear
  não é aba fechada. `trusted` falso. Sem `prompt`.
- `then` do ciclo (`guide` / `start` / `play`) sempre tem `play`, `note`, `lost`.
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
  `live` também nasce uma vez na porta (`attractSpoke`). Sem cama.
  Sem rumble.   Coleta e guarda: `captionFor` junta `corrente N` quando
  `extra.chain > 0`. O erro lê `extra.lost`: aposta zero ou
  ausente fica `atingido`; `lost > 0` nomeia a corrente que
  caiu. Não herda `chain`. Rajada do mesmo id fica com o
  texto vigente. Sem o número o tom falava e a faixa calava.
  `heard` falso.
  A guarda emite `x` no campo — sem isto a aposta falava no centro.
  O `over` emite `x` do corpo — sem isto o stinger da partida
  falava no centro. Fecho, prática e cama continuam no centro.
  Pedido sem buffer: last-wins na fila; `register` toca sem segunda
  legenda. Pedido com buffer no contexto suspenso também espera;
  `unlock` / o resume toca sem segunda legenda. Disparar no
  vazio comia a mostra da porta e o primeiro avanço. `dispose`
  esquece. Tecla ligada, toque e o controle
  que fala chamam `audio.unlock()` no gesto. Zona morta
  não pede.   Stems sobem juntos (`Promise.all`);
  extensão seguinte só se a atual falhou.
  O loader marca o primário que esgota as extensões (`fail`);
  variante ausente não é lacuna. Decode nulo continua o stem;
  só marca o pedido se nenhuma extensão falar. `register` apaga o pedido.
  O painel (`audioGapLine`) nomeia os vazios mesmo quando
  outro papel já registrou. Sem registro, a frase antiga
  permanece. `whenSfx` resolve quando o loader termina;
  o painel relê. Pintar só no boot some o que chegou.
  Nomear o 404 não é `heard`.
  `duckMs` abaixa só
  `music` (`DUCK_BUSES`). `update({ bedRate })` desloca o tom da
  cama; `bedRateFor` lê o pulso do fecho. Não é duck. O `over`
  pede `stop("bed", { fadeMs: BED_FADE_MS })`; pause, title e aba
  escondida cortam a cama seco. No campo a pausa `hush()` corta
  as vozes do verbo; no fim e na porta o `hush` não corre.
  `lift()` no resume. Play no meio do fade corta o leftover.
  `heard` falso.
- Jogador: `fillRect` do squash **permanece** (testes `playerFill` /
  `playerBox`). Na graça (`invuln`) o corpo pulsa com
  `globalAlpha` no relógio do contorno; o tijolo não some.
  Reduced trava o tijolo e o contorno. No `over` o corpo senta
  (`squashOver`) e o quadro senta (tremor, flash, punch). Na pausa
  o quadro senta; o corpo fica na pose congelada. Larga
  dash, graça e arco da guarda. A ponta é
  path (`lineTos`). Halo do estilhaço **não** é `arc`
  (`orb.arcs > shard.arcs`). Luz no disco não é `felt`.
- `player.dir` default `1`. Ponta some? Não — é forma, não brilho.
- Fase `title` só com canvas (ou `options.entry === "title"`). Headless
  e `createState()` default = `playing`. `advance` em title não anda o
  tick. A porta desenha `drawCaptions` se `captions !== false`.
  Legenda na abertura não sobe `accessibility`. Dash em `step` chama
  `beginRun`: dispara `dash`, fecha com `land` no mesmo tick
  (`squashLand`, punch Y, puff). Sem `dashTicks`, sem recovery,
  sem incrementar `stats.dashes`. O avanço lê a borda, não o
  hold: teclado, toque e A do controle. Segurar na porta não
  dispara o ofício no campo; segurar no campo não dispara de
  novo. A guarda continua nível. Na porta o toque não avança no
  down (`setDashOnPress(false)`): o arraste move; o tap abre,
  inclusive na faixa da guarda. No campo o down de cima
  continua o avanço; a faixa inferior continua guardando. Sem dash, `attractMove` desloca o corpo, `attractTick` anda a
  chuva, decai squash/flash e emite `live` uma vez, e
  `attractTouch` acende quando a mostra cruza o corpo — sem
  pontuar, sem punch, sem seed. Sem cama. Sem rumble.
  `threatCue` na porta lê a mostra. A chuva lê a mesa vigente
  (cadência e queda), sem RNG, sem `entities`. A mostra do spawn
  continua quatro gotas. Reduced trava a queda. Reset na title sorteia seed nova
  e vai a `playing`. Pause na title é ignorado. Hidden na porta só
  descarrega — não pausa o laço. Com tela, `reset()` sem
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
  Preferências ilegíveis: `#settings-gap` no painel;
  `liveText.settings` lê `settingsLine` na porta e no fim;
  `persistLine` na porta continua sem settings. Jogando a
  chave some. Nomear não é aba fechada.
- Avanço na partida: `dashWindupTicks` (2) senta com `squashCoil`
  antes de `fireDash`. Esses ticks também são graça: o coil
  atravessa o estilhaço. O quadro do `land` (`events` tem
  `land`) também atravessa — `dashTicks` já é 0. A
  recuperação depois continua vulnerável. A porta
  (`beginRun`) continua imediata e fecha o arco (`land`)
  no mesmo tick.
  Guardar corrente já existente: `bank.windupTicks` (2) senta
  com `squashBankCoil` antes de converter — senta, não estreita;
  o coil do avanço permanece `squashCoil`. Esses ticks também
  são graça: o arco atravessa o estilhaço. O quadro da conversão (`events`
  tem `bank`) também atravessa — `bankWindup` já é 0.
  Pedido de guarda com corrente já existente espera o coil
  do avanço: os dois arcos no mesmo tick comiam o disparo
  (`canDash` lia `bankWindup`). `dashCharge` também lê o sit:
  `bankWindup > 0` é `lock`, como o `bankLock` — a faixa não
  diz pronto. `dashBuffer` não decai durante `bankLock` nem
  `bankWindup` — o lock dura mais que o perdão; a recarga
  continua contando. Coleta e guarda no mesmo quadro continuam na hora. Orbe que cai no arco da guarda espera — o sit não inflama a aposta; depois do commit o orbe entra. `collect` lê o mesmo `committed` do raspo: no avanço, no land e no quadro da conversão não seta hitstop nem sit; treme e sobe a câmera. Parada continua com suco. O relógio não come o sit: se `bankWindup > 0` no último tick, `commitBank` corre antes do `over`. Sem sit a corrente continua caindo.   O hitstop no fim não alonga o relógio: se `hitstop > 0` no último tick, `endRun` corre no early-return do freeze. A queda longe não come o verbo: se `committed`, miss marca o chão e não senta squash nem puxa a câmera. Parado, a queda ainda senta. Raspo (`grazeContact`): estreita, punch na direção,
  flash menor que a queda. Sem hitstop. Sem rumble.
  Rumble do quadro: `rumbleRole` toca o verbo mais pesado,
  não o último. Porta (`dash`+`land`) fala dash; commit
  (`bank`+`collect`) fala guarda. Graça, queda, live e cama
  continuam sem pulso. Pulso no disco não é felt.
  Queda (`squashMiss`): senta menos que a coleta quando o verbo está parado. Sem rumble.
  Sem hitstop. Graça pós-dano: `hit()` concede `invuln` e o
  loop relê a cada entidade — o segundo estilhaço do mesmo
  quadro raspa, não empilha impacto. Sem janela nova. Dois
  orbes no mesmo quadro: o primeiro collect já emitiu; o
  segundo fica para o próximo tick. Não inflam a corrente
  nem empilham suco. Orbe e estilhaço no mesmo quadro: se
  o estilhaço é letal, o orbe espera — ordem do array não
  decide a aposta. No dash os dois atravessam. A
  recuperação do dash continua vulnerável. Não promover `feel`.
- Coach: fantasy → move → dash → hit → miss → touch/pad → collect → null após
  1ª guarda. Exceção: `closingWindow` e `chain > 0` devolve `bank`
  mesmo depois da primeira guarda. Sem corrente o fecho não ensina.
  Pad/touch não voltam.   Na porta (`phase === "title"`) o relógio
  é `attractTick`: fantasia e mover; a frase não come o aviso
  de abrir — depois dos 48 ticks de fantasia vem uma janela
  inteira de mover. Sem frase o mover continua os 60 ticks.
  Depois some. `beginRun` não zera `attractTick`. Se a porta
  já deu a frase (`attractTick >= 48`) o campo não a repete.
  Se a porta já fechou o ensino (`attractTick >= 108` com
  frase, ou `>= 60` sem) o campo não pede mover de novo —
  dash e coleta entram. Headless (`attractTick === 0`) ainda
  vê a frase nos primeiros 48 ticks. Dash, coleta,
  guarda, queda, hit e superfície ficam no campo. `over` continua mudo.
  `hint_hit` nomeia o estilhaço quando `hits > 0` e `chain === 0`.
  Dash no trilho vence. Texto no disco não é `felt`.
- `copy.fantasy` alimenta a abertura **e** os 48 ticks do aviso
  quando a porta ainda não deu a frase.
  Na porta o mover começa depois da frase, não no mesmo orçamento.
- `title_play` / `title_again` / `title_new` / `title_last` /
  `title_volatile` / `title_unsaved` /
  `over_door` / `over_door_inline` em `COPY_FIELDS` (default `{dash}`).
  Copy 3: `hint_hit` (default «O estilhaço come a corrente viva —
  atravesse ou guarde»). Ausente ganha o padrão. Sem faixa nova.
  A porta e o fim leem `persistLine`. O overlay do fim reusa
  `record` com `extra.best` quando `best > 0`. Recorde 0 some.
  O overlay da pausa reusa o placar (`Pausado — N`) e o mesmo
  `record` no hint. Recorde 0 some. No `over`, a cortina do fim
  vence `frame.paused` — P e aba escondida não comem Fim,
  corrente nem porta. Jogando sem pausa o número
  não entra na região viva. Sem faixa nova. Nomear não é `felt`
  nem sessão.
  `migrateCopy` preenche default se a mesa antiga não tiver.
- `attractMove` desloca `player.x` na porta com a mesma velocidade
  do campo. Não come `tick`, seed, `entities` nem eventos.
  `advance()` na porta continua no-op — o passo mora no `step()`.
  O aviso da porta reusa `drawCoach` sem faixa nova. Andar no
  disco não é `felt`.
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
- `pagehide` e `beforeunload` flush; hidden pausa no campo e no fim.
  Na porta só descarrega. Stub não é aba fechada.
- `gameSpeed` (0.5–1, padrão 1) dilata o acumulador do laço
  só em `playing`. Porta e over ficam em 1. `advance()`
  ignora. Assistência não é este knob. Knob no disco
  não é sessão observada.
- `assist` cede queda e alcance na partida e na mostra da
  porta (`fallSpeedScale`, `collectPad`, `collectReachY`).
  A graça extra (`extraInvulnTicks`) fica no campo. Não
  esconde orbe nem pontuação. Knob no disco não é sessão.
- `colorblind` é alcance, não look. `dressPalette` aplica
  `COLORBLIND_INKS` só quando a chuva ainda compartilha o eixo
  (orbe e estilhaço os dois quentes ou os dois frios). dusk e
  calm já separam; a tinta não esmaga. Alto contraste vence. Não entra no href.
  `threatCue` é estilhaço no x do corpo dentro do telegraph —
  na porta lê a mostra, não `entities`. `approaching` na porta
  lê a mesma mostra (`attractEntities`) e o canvas marca o
  trilho. `attractTouch` e o live leem a mesma chuva.
  Reduced trava canvas, toque e aviso. O campo continua
  caindo. A porta não lê `entities`. `lookAhead` no campo inclina a câmera para o
  mesmo aviso (`lookAheadX` < `punchDashX`). Não grava no
  `state.camera`. Porta, pausa, over e reduced some o lean.
  Lean no disco não é felt.   `#live` espelha fase,
  perigo, a última legenda e, no fim, na porta e na pausa no campo,
  o placar e o recorde que o canvas já mostra. No fim, se
  `chain > 0`, também a corrente que o overlay nomeia. Sem
  corrente o rótulo some. Na porta e no fim, se
  `persistLine` tem texto, também o aviso da sessão.
  Jogando e na pausa do campo a linha some. `pausado` só entra
  quando o overlay diz Pausado — no fim a cortina do over vence;
  na porta a placa nem nasce. Jogando sem pausa o número
  não entra. Texto no DOM não é sessão. Não
  promover `accessibility` nem `trusted`.

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
**Não** mais um fim que esconde o recorde que o HUD mostrou a partida inteira.
**Não** mais uma porta que ignora o movimento enquanto o convite some a tabela.
**Não** mais uma mostra que atravessa o corpo enquanto a mesa já cai na porta.
**Não** mais uma porta muda enquanto a mostra já cai e o campo já tem `live`.
**Não** mais um prompt que esconde a fantasia enquanto `--idea` já gravou a abertura.
**Não** mais um `init.scope` que afirma rascunhos, brief ou `draft_only` quando `start` não os plantou.
**Não** mais um `preproduction.md` que ensina `init` como a entrada de jogo novo.
**Não** mais um `doctor` que ensina `init` e some o mapa quando o laboratório está vazio.
**Não** mais um aviso que some o custo do estilhaço enquanto o miss já nomeia a queda.
**Não** mais um corpo sólido enquanto a graça do erro só pisca o contorno.
**Não** mais uma cama que some seco no over enquanto o loop já tem ganho.
**Não** mais um corpo em pose de jogo enquanto o relógio já derrubou a aposta.
**Não** mais uma região viva que some a pausa enquanto o overlay já a nomeia.
**Não** mais um tick que some no reload enquanto só o `pagehide` descarregava.
**Não** mais um `sfx summary` que some os stems do starter enquanto o acervo está vazio.
**Não** mais um `sfx search` que some o stem do starter que casa com o termo.
**Não** mais uma região viva que some o placar enquanto o overlay já o nomeia.
**Não** mais uma câmera em pose de golpe enquanto o relógio já derrubou a aposta.
**Não** mais um `sfx serve` que promete ouvir e devolve 400 porque `ui/` não embarcou.
**Não** mais um overlay Pausado com o hit ainda no ar.
**Não** mais um `sfx info` que some o stem do starter que casa.
**Não** mais um overlay Pausado com o tremor do último verbo.
**Não** mais um overlay Pausado que some o placar que o HUD mostrou.
**Não** mais um overlay Pausado no fim que come a aposta.
**Não** mais um `sfx verify` que some os stems do starter.
**Não** mais uma região viva que diz pausado enquanto o overlay diz Fim.
**Não** mais um hush no over que come o stinger.
**Não** mais um hidden na porta que congela a mostra sem P para retomar.
**Não** mais um `next` que manda escrever o achado relendo `playtest`.
**Não** mais um `roles --fill` que some o stem que `sfx search` já nomeia.
**Não** mais uma porta que dispara o avanço e some o término.
**Não** mais uma região viva que some a corrente enquanto o overlay já a nomeia.
**Não** mais um arco da guarda que é janela de hit enquanto o coil já atravessa.
**Não** mais uma queda que acende o campo e some o corpo.
**Não** mais um `feel` que some o serve enquanto lista as constantes.
**Não** mais um `save` que some o aviso que a porta já nomeia.
**Não** mais uma região viva que some o aviso enquanto o canvas já o nomeia.
**Não** mais uma porta que some o telegraph enquanto a mostra já cai e o live já nomeia o perigo.
**Não** mais uma câmera que some a antecipação enquanto o trilho já marca.
**Não** mais um `sfx export` que recusa o stem que `sfx info` já nomeia.
**Não** mais um relógio da partida que dilata a mostra da porta.
**Não** mais uma assistência que some a queda e o alcance na porta.
**Não** mais um reduced que trava o canvas e deixa o toque e o live lerem a chuva que some.
**Não** mais um quadro da conversão que mata depois do arco já ter atravessado.
**Não** mais um mapa que o `context` injeta ensinando o verbo só no campo.
**Não** mais um quadro do land que mata depois do dash já ter atravessado.
**Não** mais um segundo estilhaço do mesmo quadro que mata depois da graça já ter nascido.
**Não** mais um `discover` que some o sinal que o `next` já usa para escolher o jogo.
**Não** mais um `playtest` que some o esqueleto dos quatro enquanto o `next` já aponta `--field`.
**Não** mais um `next` que manda declarar origem relendo `origins`.
**Não** mais um `note` que grava e some se os quatro fecharam o achado.
**Não** mais dois orbes no mesmo quadro que inflam a corrente.
**Não** mais uma legenda da coleta que some a corrente que o tom já sobe.
**Não** mais orbe e estilhaço no mesmo quadro que decidem a corrente pela ordem do array.
**Não** mais um `guide` na raiz do framework que devolve `start '<destino>'`.
**Não** mais um `doctor.then.guide` que aponta o `guide` nu na raiz.
**Não** mais uma barra de `accessibility` que atribui medição no dispositivo ao `contrast`.
**Não** mais uma região viva que some o toque da mostra enquanto o canvas já acende.
**Não** mais um `roles --apply` que some o stem que o `--fill` já nomeia.
**Não** mais uma legenda do erro que mente corrente perdida com aposta zero.
**Não** mais um arco da guarda que copia o coil do avanço.
**Não** mais um coil do avanço que some quando a guarda pede.
**Não** mais uma tinta estável que esmaga a chuva do look que já separa.
**Não** mais um orbe no arco da guarda que inflama a aposta.
**Não** mais um relógio que come a guarda que já sentou.
**Não** mais um hitstop no fim que alonga o relógio.
**Não** mais uma queda longe que senta o verbo em curso.
**Não** mais uma guarda que fala no centro.
**Não** mais um fim que fala no centro.
**Não** mais uma fantasia na porta que come o aviso de mover.
**Não** mais um campo que repete a frase e o mover que a porta já deu.
**Não** mais um `context` que manda documentar um `start` fresco.
**Não** mais um `init` que planta e some a superfície que o `start` já nomeia.
**Não** mais um arco da guarda que mente que o dash está pronto.
**Não** mais um raspo no avanço que come a pose do dash.
**Não** mais uma coleta no avanço que congela e senta o dash.
**Não** mais um `next` do ciclo fresco que aponta um segundo `next`.
**Não** mais uma coleta no land ou no quadro da conversão que come o sit do compromisso.
**Não** mais um toque na porta que abre no down e some o arraste.
**Não** mais um pedido de dash que morre no lock da guarda.
**Não** mais um rumble do quadro que toca o último verbo e some o peso.
**Não** mais um avanço que lê o hold e metralha no cooldown.
**Não** mais o mesmo aperto da porta que dispara o ofício no campo.
**Não** mais um `start` que deixa a próxima sessão sem memória.
**Não** mais um AGENTS do start que lista GDD que não plantou.
**Não** mais um pedido no contexto suspenso que dispara no vazio.
**Não** mais um template agents que lista GDD que o disco não tem.
**Não** mais um tap na faixa da porta que some o abrir.
**Não** mais um controle que fala e some o resume.
**Não** mais um fim que fala no centro.
**Não** mais um processo comum que some a porta.
**Não** mais uma guarda que senta no travel e come a pose do dash.
**Não** mais preferências ilegíveis que voltam ao padrão em silêncio.
**Não** mais um `roles --apply` que recusa o stem porque o recibo do init tem `note`.
**Não** mais um painel que some o 404 quando outro papel já registrou.
**Não** mais um wav ilegível que esconde o ogg e some o pedido.
**Não** mais uma região viva que some a recuperação que o painel já mostra.
**Não** mais um `sfx copy` do acervo que recusa o WAV porque o recibo tem `note` e some `heard`.
**Não** mais um painel que pinta a lacuna no boot e some o que o fetch trouxe.

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
   starter declara. Com `--idea` ou `copy.json`, o prompt nomeia
   `Fantasia:` antes de `Verbo:`. A frase não muda o verbo.
   `init_scope` só afirma rascunhos quando `documents` é verdadeiro;
   o `start` embute esse recibo.    Os dois escrevem `AGENTS.md` com
   o serve; sem rascunhos a memória não lista GDD. `template agents`
   e o `next` sem memória geram o mesmo texto.    `preproduction.md` (injetado pelo
   `context` no foco create e em `--stage`) ensina `start --idea`.
   `process.md` (primeiro `read_next` de todo foco) nomeia a porta e o
   mapa start → jogar → `note` sem executar.
   `doctor` no lab vazio devolve `then.guide` com `--idea`; com jogo a chave some.
   Depois do `start` fresco o `context` adia a auditoria (`audit.deferred`);
   lacunas continuam listadas. Sem jogo que abre, o `scan` ainda pede documentar.
   O `init` também devolve `open`, `url` e `prompt`; o `prompt` sai em stderr.
   Sem starter o aviso nomeia `start --idea`. Sem `prompt`.
   `sfx search` nomeia o stem do starter que casa; `sfx info`
   lê a mesma chave. `sfx copy` e `sfx export` levam
   bytes e créditos. `sfx verify` nomeia os stems sem cruzar.
   `count` continua o acervo.    Sem os quatro campos,
   `playtest` nomeia `finding_href`, `qa`, `form`
   e `fields`; `next`
   aponta a página e `note --field`, não relê o
   leitor. Sem `then` no leitor.    Sem acervo, `roles --fill` nomeia o stem
   do starter; `--apply` o copia — e recoloca o WAV se o
   recibo já está e origem e licença casam; `next` aponta
   `--apply`. `sfx copy` do acervo recoloca o WAV se o
   recibo casa origem e licença, e declara `heard` falso.
   `feel`
   nomeia `then.play` e `then.note` sem
   executar. Sem serve a chave some. Sem
   `prompt`. `discover` nomeia os mesmos
   sinais que o `next` usa, sem propor e
   sem ranquear. Sinal verdadeiro não é
   partida jogada. `len(steps) == 3`
   e `executed: false` continuam.
3. **Checkpoint do tick:** `hold` existe. A porta nomeia sessão
   volátil e gravação recusada. Preferências ilegíveis avisam no
   painel e preservam `settings.broken`. A região viva nomeia
   a mesma recuperação na porta e no fim; a porta não.
   `save` relata `warned` se o disco tem essas chaves. A região
   viva também espelha o aviso da sessão na porta e no fim.
   Falta aba fechada real.
   Não promover. Não chamar `hold` de Continuar.
4. **Item 1 residual:** o mapa, as receitas de foco e os templates da
   primeira situação — brief, GDD, game-design, PoC, slice, QA e
   release — já nomeiam a porta. Design system, ambição, barra,
   checklist, os pacotes de gênero e o processo comum (`process.md`,
   primeiro `read_next`) também. O rascunho de playtest traz a forma
   do achado, vazia. `preproduction.md` já ensina `start --idea`.
   A barra de `accessibility` do starter não atribui medição no
   dispositivo ao `contrast`. Referências que ainda falarem só do
   campo sem a abertura estão velhas. `sfx serve` gera a página se
   `ui/` faltar. `sfx info` lê a chave do starter.    `sfx copy` e
   `sfx export` levam bytes e créditos. `roles --apply` também
   copia o stem do starter. `sfx verify` nomeia os stems
   sem cruzar. Nomear não entrega. Copiar não é `heard`. Tocar não
   é `heard`. `origins --declare` escreve o sidecar. Recibo não é
   licença.
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
  no coil do avanço e a
  graça no arco da
  guarda e a
  queda que senta
  o corpo e o
  feel que nomeia
  o serve e o
  save que nomeia
  o aviso e a
  live que nomeia
  o aviso e o
  aperto do fecho no
  disco e o aviso de
  guardar no fecho e o
  risco do fecho no
  disco e o tom da
  cama no fecho e o
  recorde no overlay
  do fim e o
  movimento na
  porta e o
  toque da mostra
  e a
  voz da mostra
  e o fade
  da cama no
  over e o
  corpo sentado
  no over e a
  pausa na
  região viva e o
  beforeunload
  do tick e o
  summary dos
  stems do
  starter e o
  search do
  stem que
  casa e o
  info da
  chave que
  casa e o
  placar na
  região viva e o
  quadro sentado
  no over e a
  página gerada
  do serve e o
  hush da
  pausa e a
  ficha do
  stem que
  casa e o
  quadro
  sentado
  na pausa e o
  placar
  na pausa e o
  fim que
  vence a
  pausa e o
  verify dos
  stems e a
  live que
  some
  pausado no
  fim e o
  hush que
  poupa o
  stinger no
  fim e o
  hidden que
  poupa a
  mostra na
  porta e o
  playtest que
  aponta o
  painel e o
  fill que
  nomeia o
  stem e a
  porta que
  fecha o
  arco e a
  live que
  nomeia a
  corrente e a
  graça no
  arco da
  guarda e a
  queda que
  senta o
  corpo e o
  feel que
  nomeia o
  serve e o
  save que
  nomeia o
  aviso e a
  live que
  nomeia o
  aviso e a
  porta que
  marca a
  mostra no
  trilho e a
  câmera que
  confirma o
  trilho e o
  export que
  leva o
  stem e o
  relógio da
  partida que
  some a
  mostra e a
  assistência
  que some a
  mostra e o
  reduced que
  some o toque
  da mostra e a
  conversão da
  guarda que é
  janela de hit e o
  mapa canônico
  que some a
  porta e o
  land que é
  janela de hit
  e o
  segundo
  estilhaço do
  mesmo quadro
  que é
  segundo hit
  e o
  discover que
  some o sinal
  do next
  e o
  playtest que
  some o
  esqueleto dos
  quatro
  e o
  next que
  declara origem
  relendo
  origins
  e o
  note que
  some se o
  recibo fechou
  o achado
  e os
  dois orbes
  do mesmo
  quadro que
  inflam a
  corrente
  e a
  legenda da
  coleta que
  some a
  corrente que
  o tom já
  sobe
  e o
  orbe e o
  estilhaço do
  mesmo quadro
  que decidem
  pela ordem
  e o
  guide na
  raiz que
  devolve
  start
  '<destino>'
  e o
  doctor que
  aponta o
  guide nu
  e a
  barra de
  accessibility
  que atribui
  medição no
  dispositivo
  ao contrast
  e a
  região viva
  que some o
  toque da
  mostra
  e o
  roles --apply
  que some o
  stem que o
  fill já
  nomeia
  e a
  legenda do
  erro que
  mente
  corrente
  perdida com
  aposta zero
  e o
  arco da
  guarda que
  copia o
  coil do
  avanço
  e o
  coil do
  avanço que
  some quando
  a guarda
  pede
  e a
  tinta
  estável que
  esmaga a
  chuva do
  look que já
  separa
  e o
  orbe no
  arco da
  guarda que
  inflama a
  aposta
  e o
  relógio que
  come a
  guarda que
  já sentou
  e o
  hitstop no
  fim que
  alonga o
  relógio
  e a
  queda longe
  que senta o
  verbo em
  curso
  e a
  guarda que
  fala no
  centro
  e a
  fantasia na
  porta que
  come o aviso
  de mover
  e o
  campo que
  repete a
  frase e o
  mover da
  porta
  e o
  context que
  manda
  documentar
  um start
  fresco
  e o
  init que
  planta e
  some a
  superfície
  e o
  arco da
  guarda que
  mente que o
  dash está
  pronto
  e o
  raspo no
  avanço que
  come a
  pose do
  dash
  e a
  coleta no
  avanço que
  congela e
  senta o
  dash
  e o
  next do
  ciclo fresco
  que aponta
  um segundo
  next
  e a
  coleta no
  land ou no
  quadro da
  conversão
  que come o
  sit do
  compromisso
  e o
  toque na
  porta que
  abre no
  down e some
  o arraste
  e o
  pedido de
  dash que
  morre no
  lock da
  guarda
  e o
  rumble do
  quadro que
  toca o
  último
  verbo e some
  o peso
  e o
  avanço que
  lê o hold
  e metralha
  no cooldown
  e o
  mesmo
  aperto da
  porta que
  dispara o
  ofício no
  campo
  e o
  start que
  deixa a
  próxima
  sessão sem
  memória
  e o
  AGENTS do
  start que
  lista GDD
  que não
  plantou
  e o
  pedido no
  contexto
  suspenso que
  dispara no
  vazio
  e o
  template
  agents que
  lista GDD
  que o
  disco não
  tem
  e o
  tap na
  faixa da
  porta que
  some o
  abrir
  e o
  controle que
  fala e some
  o resume
  e o
  fim que
  fala no
  centro
  e o
  processo
  comum que
  some a
  porta
  e a
  guarda que
  senta no
  travel e
  come a
  pose do
  dash
  e as
  preferências
  ilegíveis que
  voltam ao
  padrão em
  silêncio
  e o
  roles --apply
  que recusa o
  stem porque o
  recibo do init
  tem note
  e um
  painel que
  some o 404
  quando outro
  papel já
  registrou
  e um
  wav ilegível
  que esconde
  o ogg
  e uma
  região viva
  que some a
  recuperação
  que o painel
  já mostra
  e um
  sfx copy
  do acervo
  que recusa
  o WAV
  porque o
  recibo tem
  note
  e some
  heard
  e um
  painel que
  pinta a
  lacuna no
  boot e some
  o que o
  fetch trouxe
  não
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

Arquivos quentes da última sessão: o painel
relê a lacuna quando o fetch termina.
Pintar só no boot some o que chegou. Não
promove `heard`.
