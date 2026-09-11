# Handoff — fácil + AAA honesto

**Branch:** `cursor/runbook-telemetria-1083` (base `main`)
**PR:** [#6](https://github.com/oalanicolas/alanstudio-framework/pull/6) (draft)
**HEAD:** ver `git log -1` — vigente 0.9.524: o then do `start` nomeia a experiência que a receita já recusa. Nome no disco não é o ciclo jogado. Sem chave `experiência`. Nomear não observa.
**Goal:** ativo. Não marcar complete. AAA fácil ainda não está provado.

**Suítes:** confirmadas no HEAD (0.9.524): 585 / 516.

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

## O que o HEAD já entrega (0.9.91–0.9.524)

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
| 0.9.255 | O hitstop não come o perdão do avanço. O freeze também poupa a guarda. Não promove `felt`. |
| 0.9.256 | O hold leva o relógio da porta. Retomar no campo não devolve a frase nem o mover. Hold antigo sem o número não inventa ensino feito. Não promove `trusted`. |
| 0.9.257 | A região viva nomeia o aviso do primeiro ciclo que o canvas já pinta. O convite some a tabela. No fim a linha some. Não promove `verified`. |
| 0.9.258 | A escala veste a casca da página. O canvas já crescia; tabela, painel e convite ficavam em quinze pixels. Não promove `verified`. |
| 0.9.259 | O recado não dispara o verbo. O painel foca o campo no fim; Espaço e R ficavam no ofício. Não promove `felt`. |
| 0.9.260 | O toque que sai do campo ainda solta. Sem a captura o corpo seguia o último aim. Perder a captura não come o tap da porta. Não promove `felt`. |
| 0.9.261 | Os knobs vestem o look. Select e faixa ficavam no widget frio; o foco visível também chega. Não promove `consistent`. |
| 0.9.262 | A outra aba veste as preferências. Look e mix ficavam velhos até recarregar. O progresso em curso não. Não promove `trusted`. |
| 0.9.263 | O recibo sem origem não declara. JSON listava o arquivo e fingia recibo. Envelope do acervo ainda vale. CREDITS e sidecar ainda declaram. Não promove `granted`. |
| 0.9.264 | A tecla do remap não dispara o verbo. A escuta avançava enquanto a pessoa escolhia. Não promove `felt`. |
| 0.9.265 | O botão focado não dispara o verbo. Espaço ativava o controle e avançava. Não promove `felt`. |
| 0.9.266 | O verify nomeia o stem que o recibo perdeu. O WAV sumia e o relatório fingia que o papel não existia. Não promove `heard`. |
| 0.9.267 | A faixa nomeia a curva que o last-run já traçou. Seed e pontos ficavam; never_banked some. Não promove `outsider`. |
| 0.9.268 | O preset de uma mão não some o remap. Desligar devolvia o padrão e apagava o KeyZ. Save antigo sem o conjunto guardado não inventa remap. Não promove `trusted`. |
| 0.9.269 | A faixa nomeia o valor que o knob já guarda. O thumb andava; 75% some. Não promove `verified`. |
| 0.9.270 | O sistema que pede reduce no meio da sessão veste a caixa. O boot herdava; o pedido depois ficava no matchMedia. Desligar o SO não apaga. Não promove `verified`. |
| 0.9.271 | O convite nomeia o relógio da partida. Seed e eixos abriam no relógio cheio. 1 some. A faixa não leva o knob. Não promove `outsider`. |
| 0.9.272 | O pulso do fecho não come a legenda do verbo. Dez "últimos segundos" empurravam collect. O SFX continua. Não promove `heard`. |
| 0.9.273 | A porta nomeia a recuperação que o painel já mostra. O canvas da abertura e do fim pinta `settingsLine`. A pausa não. `persistLine` continua só sessão. Não promove `trusted`. |
| 0.9.274 | A receita não cala a porta que o canvas já pinta. `persistence` e `accessibility` ensinam `settingsLine` no canvas. A pausa não. Não promove `trusted`. |
| 0.9.275 | A aba escondida não deixa o verbo preso. O keyup some; o corpo não segue. O pad continua no poll. Não promove `felt`. |
| 0.9.276 | A perda de foco não deixa o ofício pendente. O blur solta hold e pressed. Voltar a focar ainda avança. O pad continua no poll. Não promove `felt`. |
| 0.9.277 | A perda de foco grava o hold. O blur senta o relógio no campo e no fim. Na porta só descarrega. Não promove `trusted`. |
| 0.9.278 | O orçamento cronometra a porta. `title.attract` entra ao lado de `playing.run`. Stub ≠ dispositivo. Não promove `measured`. |
| 0.9.279 | O playtest nomeia a política do candidato. `played` e `nearest-orb` deixam de ser a mesma origem. A simulação não apaga a jogada. Não promove `outsider`. |
| 0.9.280 | O contrato de alcance nomeia o pulso. `haptics` entra no `access`. A receita e o `docs/access.md` deixam de omitir o aparelho. Não promove `verified`. |
| 0.9.281 | O `art` nomeia a chuva que o disco já tem. `spawn`, `dusk` e `calm` deixam de ser só arquivo em `content`. Não promove `consistent`. |
| 0.9.282 | O `sfx info` nomeia o stem que o recibo lista e o disco perdeu. Não é id desconhecido. Não promove `heard`. |
| 0.9.283 | O `discover` nomeia o sinal de origem que o `next` já usa. Dois jogos deixam de parecer iguais quando um embarca sem recibo. Não promove `granted`. |
| 0.9.284 | O `content` não conta paleta como volume. `palettes.json` deixa de calar `content.inline`. Não promove `enough`. |
| 0.9.285 | O `discover` nomeia as lacunas de dimensão que o `next` já usa. `access_declared` deixa de esconder `haptics`. Não promove `verified`. |
| 0.9.286 | O controle que some não deixa a partida correr sozinha. `gamepaddisconnected` senta se a sessão falou no pad. Não promove `felt`. |
| 0.9.287 | A cama segue o relógio da sessão. O fecho sobe em cima do knob; coleta e guarda guardam o tom. Não promove `heard`. |
| 0.9.288 | A sessão simulada nomeia o look e o relógio que o convite já lê. `session --look` / `--speed` escrevem o candidato. Não promove `outsider`. |
| 0.9.289 | O ciclo nomeia o relógio que o jogo já lê. `CYCLE_KEYS` inclui `speed` depois de `seed`. O SKILL já pedia. Não promove `outsider`. |
| 0.9.290 | O banner do serve nomeia o relógio que o jogo já lê. Look, chuva e par deixam de calar `?speed=`. Não promove `outsider`. |
| 0.9.291 | A página de escuta nomeia o som que o catálogo lista e o disco perdeu. O player some. Não promove `heard`. |
| 0.9.292 | O convite não grava o look, a chuva nem o relógio que só vestiu. `flush` e o sistema não promovem candidato a preferência. Escolher no painel grava. Não promove `trusted`. |
| 0.9.293 | A query de chuva não retoma o hold de outra mesa. `?spawn=` e o par abrem a mesa nomeada. Look e relógio vestem o tick que já está. Não promove `trusted`. |
| 0.9.294 | Na pausa o toque retoma. A aba escondida no telefone sentava e Esc/P não existem no polegar. O tap não é o avanço. Não promove `felt`. |
| 0.9.295 | Na porta o telefone vê Jogar: toque sem ter apertado. lastSource continua teclado; o aviso não ensina cima. Não promove `felt`. |
| 0.9.296 | Depois do tap a porta não chama o avanço de cima. lastSource pointer preenchia o mapa das faixas e mente: o tap abre em qualquer faixa. O fim usa a mesma placa. Não promove `felt`. |
| 0.9.297 | `finding_href` abre o convite. Sem `invite=1` o âncora caía em `display:none`. Não promove `outsider`. |
| 0.9.298 | A pausa nomeia reiniciar. R e Select já saíam; a placa só ensinava continuar. Não promove `felt`. |
| 0.9.299 | A região viva nomeia como sair da pausa. O overlay do canvas não chega ao leitor. Não promove `verified`. |
| 0.9.300 | Na pausa o telefone vê Continuar: toque sem ter apertado. lastSource continua teclado; o aviso não ensina cima. Reiniciar continua R. Não promove `felt`. |
| 0.9.301 | O `next` unstructured nomeia a página do achado. SKILL e README já apontavam `/?invite=1#finding`; o comando mandava o serve nu. Não promove `outsider`. |
| 0.9.302 | Depois da partida o telefone pede seed nova embaixo. R não existe no polegar e o tap só repetia. A primeira visita continua abrindo na faixa. Não promove `felt`. |
| 0.9.303 | A região viva nomeia como abrir a porta. O overlay do canvas não chega ao leitor. Jogar, repetir, seed nova e o fim espelham a placa. Não promove `verified`. |
| 0.9.304 | O `feel` nomeia a partida do last-run. `play` / `guide` já apontavam `then.seed` e `then.invite`; o feel mandava só o serve nu. Não promove `felt`. |
| 0.9.305 | No campo o telefone pausa no relógio. Esc e P não existem no polegar; o toque só retomava. Na porta o canto continua abrindo. Não promove `felt`. |
| 0.9.306 | O `playtest` nomeia a página do achado. O `next` já apontava `finding_open`; o leitor mandava só o caminho relativo. Não promove `outsider`. |
| 0.9.307 | O relógio nomeia a pausa. O toque no canto já sentava; o canvas só mostrava o número e o convite some a tabela. Não promove `felt`. |
| 0.9.308 | O Copiar nomeia o destino. O Gravar já virava Achado no disco; o botão calava e o convite some a tabela. Não promove `outsider`. |
| 0.9.309 | A memória nomeia o playtest. O start já nomeava o serve e o note; a próxima sessão calava o leitor que o `next` já aponta. Não promove `outsider`. |
| 0.9.310 | Os rascunhos de hipótese nomeiam a porta. Brief e GDD já falavam; o MDA do `init` e os rascunhos de MVP/PRD começavam no campo. Não promove `observed`. |
| 0.9.311 | A região viva nomeia a lacuna do som. O painel já falava; o live calava e o convite some a tabela. Catálogo completo não entra. Não promove `heard`. |
| 0.9.312 | O aviso do campo nomeia a prática. O campo já contornava a janela orbe-só; o coach pedia coleta como se a ameaça já caísse. Dash, hit, miss e a superfície vencem. A porta não ensina. Copy 4. Não promove `felt`. |
| 0.9.313 | A receita do look nomeia o perigo. `--as` já preservava `danger`; a intenção e o art-bible calavam. Estilhaço e perigo permanecem. Não promove `consistent`. |
| 0.9.314 | `brief` não come a folga da guarda. A intenção prometia prática e rampa; o código encolhia `recoveryTicks` e o verbo mudava sem o ofício dizer. Não promove `enough` nem `felt`. |
| 0.9.315 | O corpo na recuperação do dash não veste a prática. A regra já dizia vulnerável; a tinta do orbe é a janela orbe-só. Agora veste o apoio. Não promove `felt`. |
| 0.9.316 | O `feel` nomeia as janelas da chuva. O campo já marcava prática, folga e fecho; o comando lia só o `CONFIG`. Não promove `felt`. |
| 0.9.317 | A prática que acaba nomeia a ameaça. O aviso já dizia ameaça; a faixa chamava orbe de chuva que começa. A porta reusa a voz e continua a mostra. Não promove `heard` nem `felt`. |
| 0.9.318 | A folga que acaba nomeia a folga. A chuva não some — só afrouxa; a faixa dizia que voltava. O campo já some o contorno. Não promove `heard` nem `felt`. |
| 0.9.319 | O `next` do feel anexa o candidato. `then.note` e o playtest já levavam `--from-run`; o ofício pedia a nota sem a partida. Não promove `felt` nem `outsider`. |
| 0.9.320 | O rastro do dash veste o avanço. O corpo já vestia a corrente; o rastro vestia o descanso. Não promove `felt`. |
| 0.9.321 | O coil do dash veste o avanço. A faixa já vestia a corrente; o corpo no coil vestia o descanso. Não promove `felt`. |
| 0.9.322 | O `-h` lista start antes de init. O ofício já era start → jogar → note; a ajuda listava o ADAPT primeiro. Não promove `executed`. |
| 0.9.323 | O coil da guarda veste a aposta. O arco já vestia a corrente; o corpo no sit vestia o descanso. Não promove `felt`. |
| 0.9.324 | A porta chove o risco da mesa. Cadência e queda já liam a mesa; o risco era meio a meio e dusk vestia o mesmo perigo que calm. Não promove `consistent`. |
| 0.9.325 | O compromisso da guarda veste a aposta. O arco do lock já vestia a corrente; o corpo no hold vestia o descanso. Não promove `felt`. |
| 0.9.326 | O `art` nomeia o risco da chuva. A porta já lia o teto; o comando listava a mesa e calava o perigo. Não promove `consistent`. |
| 0.9.327 | O `sfx export` nomeia o stem que o recibo lista e o disco perdeu. O info já lia a ficha; o export dizia id desconhecido. Exportar não inventa bytes. Não promove `heard`. |
| 0.9.328 | O rótulo do dash nomeia o avanço no travel. A faixa já enchia; o rótulo dizia recarregando e o verbo mentia a recarga. O sit da guarda continua sem prometer o dash. Não promove `felt`. |
| 0.9.329 | O `sfx verify` nomeia o som que o catálogo lista e o disco perdeu. A página de escuta já nomeava a ausência; o cruzamento despejava errno. Não promove `heard`. |
| 0.9.330 | A região viva nomeia a mesa e o look da porta. A chuva já vestia dusk e calm; o live só dizia abertura. Spawn e normal somem. Não promove `verified`. |
| 0.9.331 | O `feel` nomeia o rumble que a tabela já lista. As constantes já entravam; o scope e o `-h` calavam o pulso. Não promove `felt`. |
| 0.9.332 | O `sem destino` nomeia o `start --idea` que o README já imprime. A recusa explicava `--idea` e calava o comando. Nomear não cria. |
| 0.9.333 | No fim a região viva nomeia a mesa e o look que a partida já vestiu. O last-run já gravava; o live só dizia o placar. Spawn e normal somem. Não promove `verified`. |
| 0.9.334 | O sidecar sem origem, autor e licença não declara. O JSON já exigia os três campos; o arquivo ao lado declarava só por existir. CREDITS.md pela menção continua. Não promove `granted`. |
| 0.9.335 | O `feel` nomeia o peso do passo. O CONFIG já declarava `player.speed` e o avanço; o comando lia perdão e rumble e calava o passo. `halfWidth` continua de fora. Não promove `felt`. |
| 0.9.336 | O `playtest` nomeia a conta do last-run. A faixa e o recibo já tinham pontos e verbos; o leitor nomeava curva e origem e calava a conta. `dashes` e `ticks` ficam de fora. Não promove `outsider`. |
| 0.9.337 | O `start` nomeia `npm install` quando `node_modules` falta. O play mandava o serve e o disco ainda não tinha módulos. `play` continua `npm run serve`. O `feel` não ganha a chave. Nomear não instala. |
| 0.9.338 | O `origins` nomeia a mídia que o recibo lista e o disco perdeu. O JSON já cobria o arquivo presente; o WAV sumido calava. CREDITS.md pela menção continua. Nomear não devolve o arquivo. Não promove `granted`. |
| 0.9.339 | O `start` não nomeia `npm install` quando o `package.json` não tem dependências. O starter já recusava o passo; o harness pedia install sem ter o que instalar. Com dependências e sem `node_modules`, a chave permanece. `play` continua o serve. O `feel` não ganha a chave. Nomear não instala. |
| 0.9.340 | O `ship` nomeia a árvore que perdeu o `src/` que o projeto já tem. O export já copia o jogo; identidade e serve sozinhos diziam completa. Nomear não devolve o jogo. Não promove `elsewhere`. |
| 0.9.341 | O `roles` nomeia o `duckMs` que `SOUNDS` já declara. O comando já lia o papel; o aviso que abaixa a cama calava. Sem duck a chave some. Nomear não é mix ouvida. Não promove `heard`. |
| 0.9.342 | O prompt nomeia o serve que tenta abrir o navegador. O README do starter já recusava o passo manual; o harness pedia Abrir sempre. Sem o marcador, pede Abrir. Nomear não abre. Sem `then.browser`. |
| 0.9.343 | A faixa nomeia o last-run simulado. O `playtest` já lia `candidate_policy`; a faixa mostrava seed e curva como se alguém tivesse jogado. `nearest-orb` vira `simulada`; `played` some. Sem tally nem relógio. Não promove `outsider`. |
| 0.9.344 | O coil do dash marca o rumo no corpo. A faixa já enchia e o corpo já vestia a corrente; a antecipação calava a direção. Sem faixa no HUD. Sem chave `heading`. Não promove `felt`. |
| 0.9.345 | O achado copiado nomeia o last-run simulado. A faixa já dizia `simulada`; o markdown levava só os quatro nomes. Sem tally nem relógio. Não promove `outsider`. |
| 0.9.346 | O canvas da porta e do fim nomeia a lacuna do som. O painel e o live já falavam; o canvas calava. Sem faixa no HUD. A pausa não nomeia. Não promove `verified`. |
| 0.9.347 | O prompt nomeia o `playtest` que o `AGENTS.md` já cita. O caminho ideia→jogo calava o leitor. Só lê. Sem os quatro não é achado. Sem `then.playtest`. Não promove `outsider`. |
| 0.9.348 | O `access` nomeia o `:focus-visible` que a casca já declara. A receita já pedia foco visível; o comando calava. Sem chave `focus`. Não promove `verified`. |
| 0.9.349 | O `budget` nomeia a porta que a receita já cronometra. O tool já media `title.attract`; o comando calava. Sem chave `door`. Não promove `measured`. |
| 0.9.350 | O `save` nomeia a recuperação que o canvas já pinta. A receita já falava; o comando calava. A pausa não. Sem chave `recovery`. Não promove `trusted`. |
| 0.9.351 | O `feel` nomeia o corpo que a porta já desloca. O laço já corria `attractMove`; o comando calava a mostra. Sem chave `attract`. Não promove `felt`. |
| 0.9.352 | O `content` nomeia o par que `listMoods` já lista. O comando listava dusk e calm e calava o par. Sem chave `moods`. Não promove `enough`. |
| 0.9.353 | O `ship` nomeia o tamanho que a receita já relata. O tool já dizia sem teto; o comando calava. Sem chave `size`. Não promove `elsewhere`. |
| 0.9.354 | O `access` nomeia o contraste que a receita já amostra. O tool já lia o stub; o comando calava. Sem chave `contrast`. Não promove `verified`. |
| 0.9.355 | O `roles` nomeia a soma que a receita já relata. O tool já somava as vozes; o comando calava. Sem chave `mix`. Não promove `heard`. |
| 0.9.356 | O `playtest` nomeia a simulação que a receita já grava. O tool já gravava `nearest-orb` sem apagar `played`; o comando calava o nome. Sem chave `session`. Não promove `outsider`. |
| 0.9.357 | O `feel` nomeia o perdão que o probe já exercita. O tool já contava o buffer; o comando calava. Sem chave `probe`. Não promove `felt`. |
| 0.9.358 | O `art` nomeia o look que o disco já nasce. A receita já apontava `look --from`; o comando listava paletas e calava o tool. Sem chave `look`. Não promove `consistent`. |
| 0.9.359 | O `content` nomeia a mesa que o disco já nasce. A receita já apontava `table --from`; o comando listava dusk e calm e calava o tool. Sem chave `table`. Não promove `enough`. |
| 0.9.360 | O `budget` nomeia os bytes que o size já relata. A receita já apontava `npm run size`; o comando cronometrava a porta e calava o tool. Sem chave `size`. Não promove `measured`. |
| 0.9.361 | O `roles` nomeia a voz que o sfx já desloca. A receita já apontava `sfx --from/--as`; o comando somava o mix e calava o tool. Sem chave `sfx`. Não promove `heard`. |
| 0.9.362 | O `feel` nomeia a inclinação que o lookAhead já marca. A receita já inclinava o quadro; o comando lia `lookAheadX` e calava o laço. Sem chave `lookAhead`. Não promove `felt`. |
| 0.9.363 | O `ship` nomeia o banner que o serve já imprime. A receita já apontava a árvore exportada; o comando relatava dist/ e calava o tool. Sem chave `serve`. Não promove `elsewhere`. |
| 0.9.364 | O `access` nomeia o perigo que o live já anuncia. A receita já pedia `perigo à frente`; o comando lia região viva e calava o aviso. Sem chave `threat`. Não promove `verified`. |
| 0.9.365 | O `save` nomeia o fechamento que o disco já grava. A receita já apontava `beforeunload`; o comando lia persistLine e calava o gancho. Sem chave `beforeunload`. Não promove `trusted`. |
| 0.9.366 | O `art` nomeia o trilho que o telegraph já marca. A receita já apontava a mostra; o comando listava paletas e calava o aviso no canvas. Sem chave `telegraph`. Não promove `consistent`. |
| 0.9.367 | O `sfx info` nomeia o pico que o inspect já mede. O inspect já gravava `peak_dbfs`; o comando lia id e créditos e calava o número. Sem `rms`. Não promove `heard`. |
| 0.9.368 | O `access` nomeia as teclas que a tabela já lista. A receita já pedia `#commands`; o comando lia remap e calava o preenchimento. Sem chave `commands`. Não promove `verified`. |
| 0.9.369 | O `ship` nomeia o passo que o export já declara. A receita já apontava `npm run build`; o comando listava `build` e calava o tool. Sem chave `export`. Não promove `elsewhere`. |
| 0.9.370 | O `budget` nomeia o percentil que a receita já pede. O tool já relatava a distribuição; o comando cronometrava a porta e calava o pior quadro. Sem chave `percentile`. Não promove `measured`. |
| 0.9.371 | O `note` nomeia o last-run que o disco já guarda. A partida já gravava o candidato; o comando escrevia o recibo e calava o arquivo. Sem chave `last_run`. Não promove `observed`. |
| 0.9.372 | O `sfx summary` nomeia o pico que o peak já relata. A receita já apontava `npm run peak`; o comando listava stems e calava o tool. Sem chave `peak`. Não promove `heard`. |
| 0.9.373 | O `start` nomeia o par que o pair já nasce. O tool já nascia look e chuva; o comando apontava `then.pair` e calava o nascimento. Sem chave `pair`. Não promove `enough`. |
| 0.9.374 | O `access` nomeia a legenda que a porta já lê. A receita já pedia o canvas da abertura; o comando listava `captions` e calava a porta. Sem chave `caption`. Não promove `verified`. |
| 0.9.375 | O `sfx search` nomeia o deslocamento que o sfx já oferece. A receita já apontava `--from` / `--as`; o comando achava o stem e calava o tool. Sem chave `sfx`. Não promove `heard`. |
| 0.9.376 | O `feel` nomeia o sit que a guarda já senta. A receita já pedia o arco; o comando lia squash e calava o sit. Sem chave `bank`. Não promove `felt`. |
| 0.9.377 | O `playtest` nomeia o recado que o serve já grava. A página já pedia o POST; o comando dizia que a página escreve e calava a rota. Sem chave `note`. Não promove `outsider`. |
| 0.9.378 | O `save` nomeia a gravação que o storage já verifica. A receita já pedia o estágio; o comando lia persistLine e calava o `writeJson`. Sem chave `storage`. Não promove `trusted`. |
| 0.9.379 | O `feel` nomeia o land que o dash já emite. A receita já pedia o término; o comando lia squash e calava o `landDash`. Sem chave `land`. Não promove `felt`. |
| 0.9.380 | O `content` nomeia a migração que as mesas já compartilham. A receita já pedia o `migrateTable`; o comando listava dusk e calm e calava o loader. Sem chave `migrate`. Não promove `enough`. |
| 0.9.381 | O `art` nomeia a vinheta que o recorte já marca. A receita já pedia halo e vinheta; o comando listava paletas e calava o `drawVignette`. Sem chave `vignette`. Não promove `consistent`. |
| 0.9.382 | O `roles` nomeia o PCM que o wav já lê. O tool já lia o arquivo; o comando somava o mix e calava o decoder. Sem chave `wav`. Não promove `heard`. |
| 0.9.383 | O `origins` nomeia o consumidor que o sidecar já declara. O esqueleto já pedia `Consumidor:`; o comando lia os três rótulos e calava o sidecar. Sem chave `consumer`. Não promove `granted`. |
| 0.9.384 | O `doctor` nomeia o engines que o package já declara. O starter já pedia Node 20; o comando lia a major do PATH e calava o `engines`. Sem chave `engines`. Nomear não instala. |
| 0.9.385 | O `ship` nomeia o file:// que o export já recusa. O README do `dist/` já recusava o protocolo; o comando empacotava a árvore e calava o `file://`. Sem chave `file`. Não promove `elsewhere`. |
| 0.9.386 | O `sfx copy` nomeia os créditos que o copy já leva. O sidecar já declarava licença; o comando copiava o caminho e calava o arquivo. Sem chave `sidecar`. Não promove `heard`. |
| 0.9.387 | O `play` nomeia a produção que o serve já recusa. O serve já avisava que não é servidor de produção; o comando apontava o url e calava o aviso. Sem chave `produção`. Não promove `executed`. |
| 0.9.388 | O `sfx verify` nomeia a integridade que o check já cruza. O check já comparava hash e bytes; o comando lia `ok` e calava o cruzamento. Sem chave `sha256`. Não promove `heard`. |
| 0.9.389 | O `sfx export` nomeia o processamento que o export já recusa. O payload já preservava os bytes sem processamento; o comando copiava e calava a recusa. Sem chave `processamento`. Não promove `heard`. |
| 0.9.390 | O `bar` nomeia o mínimo que a barra já declara. A prosa já dizia que o degrau percebido é o mínimo; o comando lia a tabela e calava a regra. Sem chave `mínimo`. Não promove `assessed`. |
| 0.9.391 | O `guide` nomeia o relógio que o manifesto já declara. O `starter.json` já trazia `speed`; o comando lia o ciclo e calava o relógio no `scope`. Sem chave `speed` no recibo. Não promove `executed`. |
| 0.9.392 | O `craft` nomeia a saída de escopo que a tabela já declara. O README do starter já marcava `style_factor` como `out_of_scope`; o comando parseava a linha e calava o estado. Sem chave `out_of_scope` no recibo. Não promove `observed`. |
| 0.9.393 | O `art` nomeia o contraste que o look já recusa. O `new-look` já dizia que `contrast` é alcance, não look; o comando nascia a paleta e calava a recusa. Sem chave `contrast` no recibo. Não promove `consistent`. |
| 0.9.394 | O `doctor` nomeia as substituições que o manifesto já declara. O `starter.json` já listava as trocas; o comando validava o manifesto e calava o campo. Sem chave `substitutions` no recibo. Nomear não cria. |
| 0.9.395 | O `discover` nomeia os scripts que o package já declara. O `package.json` já listava `scripts`; o comando lia os validadores e calava o campo. Sem chave `scripts` no recibo. Nomear não executa. |
| 0.9.396 | O `init` nomeia o módulo que o package já declara. O `package.json` já trazia `"type": "module"`; o comando copiava o manifesto e calava o campo. Sem chave `type` no recibo. Nomear não instala. |
| 0.9.397 | O `gate` nomeia o gate que a tabela já declara. A linha já existia no parser; o comando lia a forma e calava o campo. Sem chave `gate` no recibo. Não promove `granted`. |
| 0.9.398 | O `scan` nomeia o serve que o README já aponta. O README já dizia `npm run serve`; o comando lia as áreas e calava o ciclo. Sem chave `serve` no recibo. Nomear não executa. |
| 0.9.399 | O convite nomeia o bind que o serve já prende. O serve já avisava `HOST=127.0.0.1 prende o bind`; o comando anunciava a rede e calava o HOST. Sem chave `HOST` no recibo. Não promove `outsider`. |
| 0.9.400 | O `template` nomeia a publicação que o molde já recusa. O molde já dizia que não autoriza publicar; o comando emitia rascunho e calava a recusa. Sem chave `publicar` no recibo. Não promove `elsewhere`. |
| 0.9.401 | O `context` nomeia o audit que o roteiro já pede. O roteiro já pedia documentar sem consentimento; o comando apontava o arquivo e calava a política. Sem chave `audit` no recibo. Nomear não escreve. |
| 0.9.402 | O `context` nomeia a PoC que o processo já nega. O processo já dizia que documentos prontos não são PoC executada; o comando apontava o arquivo e calava a recusa. Sem chave `process` no recibo. Nomear não executa. |
| 0.9.403 | O `scan` nomeia o AAA que a memória já recusa. A memória já dizia para não chamar o recorte de AAA; o comando listava `AGENTS.md` e calava a recusa. Sem chave `agents` no recibo. Nomear não observa. |
| 0.9.404 | O `context` nomeia o checklist que a guia já recusa preencher. A guia já dizia que o harness não preenche o checklist; o comando apontava o arquivo e calava a recusa. Sem chave `checklist` no recibo. Nomear não observa. |
| 0.9.405 | O `context` nomeia a promoção que a barra já recusa. A guia já dizia que nenhum comando promove um degrau; o comando apontava o arquivo e calava a recusa. Sem chave `promove` no recibo. Nomear não observa. |
| 0.9.406 | O `context` nomeia o navegador que o pacote já recusa provar. O pacote web já dizia que teste unitário não prova o navegador; o comando apontava o arquivo e calava a recusa. Sem chave `navegador` no recibo. Nomear não observa. |
| 0.9.407 | O `next` nomeia a ação que o processo já pede. O processo já pedia uma ação recomendada; o comando propunha e calava o pedido. Sem chave `ação` no recibo. Nomear não executa. |
| 0.9.408 | O `record` nomeia a medição que o roteiro já recusa. O roteiro já dizia que o harness não mede os critérios; o comando gravava o recibo e calava a recusa. Sem chave `mede` no recibo. Nomear não observa. |
| 0.9.409 | O `check-plan` nomeia o mérito que o processo já recusa. O processo já dizia que o contrato não garante mérito; o comando validava a forma e calava a recusa. Sem chave `mérito` no recibo. Nomear não valida. |
| 0.9.410 | O `verify` nomeia a criatividade que o roteiro já recusa. O roteiro já dizia que o verify não aprova criatividade; o comando executava e calava a recusa. Sem chave `criatividade` no recibo. Nomear não observa. |
| 0.9.411 | O `verify` nomeia a verificação que o processo já recusa. O processo já dizia que claimed não é verified; o comando alegava a capacidade e calava a recusa. Sem chave `verified` no recibo. Nomear não observa. |
| 0.9.412 | O `git` nomeia a leitura que o processo já recusa. O processo já dizia que hash prova identidade, não leitura; o comando relatava o HEAD e calava a recusa. Sem chave `leitura` no recibo. Nomear não observa. |
| 0.9.413 | O `doctor` nomeia o exemplo que o README já imprime. O README já imprimia a frase; o `then.guide` colava `<fantasia>` e calava o exemplo. Sem chave `exemplo` no recibo. Nomear não cria. |
| 0.9.414 | O `version` nomeia o julgamento que o roteiro já recusa. O roteiro já dizia que o HEAD não substitui o julgamento; o recibo relatava o hash e calava a recusa. Sem chave `julgamento` no recibo. Nomear não observa. |
| 0.9.415 | O `roles --fill` nomeia o reuso que o processo já recusa. O processo já dizia que asset no disco não é automaticamente reutilizável; o comando sugeria o primeiro match e calava a recusa. Sem chave `reuso` no recibo. Nomear não ouve. |
| 0.9.416 | O `audit` nomeia o daemon que o roteiro já recusa. O roteiro já dizia que a checagem não é daemon nem hook; o objeto apontava o arquivo e calava a recusa. Sem chave `daemon` no recibo. Nomear não escreve. |
| 0.9.417 | O `context` nomeia o progresso que o processo já recusa. O processo já dizia que `--stage` só seleciona contexto, não certifica progresso; o comando escolhia o recorte e calava a recusa. Sem chave `progresso` no recibo. Nomear não observa. |
| 0.9.418 | O `context` nomeia a escuta que o mapa já recusa. O mapa já dizia que o catálogo não ouve o starter; o comando apontava o acervo e calava a recusa. Sem chave `ouve` no recibo. Nomear não ouve. |
| 0.9.419 | O `scan` nomeia os tokens que o sistema já recusa. O contrato já dizia que o scanner localiza o documento e não certifica tokens; a área apontava o arquivo e calava a recusa. Sem chave `tokens` no recibo. Nomear não observa. |
| 0.9.420 | O `scan` nomeia as dependências que a receita já recusa. A receita já dizia que o harness não infere dependências; a área apontava o TDD e calava a recusa. Sem chave `dependências` no recibo. Nomear não observa. |
| 0.9.421 | O `scan` nomeia a inexistência que o roteiro já recusa. O roteiro já dizia que local não percorrido não equivale a conteúdo inexistente; a cobertura contava documentos e calava a recusa. Sem chave `inexistente` no recibo. Nomear não observa. |
| 0.9.422 | O `context` nomeia a capacidade que o índice já recusa. O índice já dizia que o pacote não certifica capacidade; a plataforma apontava o arquivo e calava a recusa. Sem chave `capacidade` no recibo. Nomear não observa. |
| 0.9.423 | O `guide` nomeia o onboarding que o roteiro já recusa. O roteiro já dizia que mural que bloqueia o jogo não é onboarding; o passo de jogar copiava o verbo e calava a recusa. Sem chave `onboarding` no recibo. Nomear não observa. |
| 0.9.424 | O `guide` nomeia o screenshot que a receita já recusa. A receita já dizia que screenshot não comprova feel; o passo de gravar copiava o note e calava a recusa. Sem chave `screenshot` no recibo. Nomear não observa. |
| 0.9.425 | O `context` nomeia a extração que o mapa já recusa. O mapa já dizia que os pacotes não são extração de repositório; o gênero apontava o arquivo e calava a recusa. Sem chave `extração` no recibo. Nomear não observa. |
| 0.9.426 | O `context` nomeia a API que a receita já recusa. A receita já dizia que os oito nomes não são uma API implementada; a menção apontava o arquivo e calava a recusa. Sem chave `api` no recibo. Nomear não observa. |
| 0.9.427 | O `next` nomeia a criação que o roteiro já recusa. O roteiro já dizia que o comando não cria um jogo; a proposta copiava a ação e calava a recusa. Sem chave `criação` no recibo. Nomear não cria. |
| 0.9.428 | O `gate` nomeia o silêncio que o roteiro já recusa. O roteiro já dizia que silêncio não é aprovação; o item listava o pendente e calava a recusa. Sem chave `silêncio` no recibo. Nomear não observa. |
| 0.9.429 | O `guide` nomeia a abertura que o processo já recusa. O processo já dizia que nomear o comando não abre o jogo; o passo de abrir copiava o start e calava a recusa. Sem chave `abertura` no recibo. Nomear não abre. |
| 0.9.430 | O `craft` nomeia a escada que a pesquisa já recusa. A pesquisa já dizia que não é escada de acabamento; o item listava o checklist e calava a recusa. Sem chave `escada` no recibo. Nomear não observa. |
| 0.9.431 | O `bar` nomeia os prazos que a barra já recusa. A barra já dizia que degraus não são prazos; o item listava o degrau e calava a recusa. Sem chave `prazos` no recibo. Nomear não observa. |
| 0.9.432 | O `doctor` nomeia o motor que a ambição já recusa. A ambição já dizia que o harness não é um motor AAA; o then apontava o mapa e calava a recusa. Sem chave `motor` no recibo. Nomear não cria. |
| 0.9.433 | O `next` nomeia a fabricação que o processo já recusa. O processo já dizia que não se fabrica tarefa para cumprir o formato; a alternativa copiava a ação e calava a recusa. Sem chave `fabricação` no recibo. Nomear não executa. |
| 0.9.434 | O `verify` nomeia a diversão que a ambição já recusa. A ambição já dizia que build verde não comprova diversão; o comando copiava o exit code e calava a recusa. Sem chave `diversão` no recibo. Nomear não observa. |
| 0.9.435 | O `scan` nomeia a licença que o roteiro já recusa. O roteiro já dizia que recibo presente não é licença válida; a área de proveniência apontava o CREDITS e calava a recusa. Sem chave `licença` no recibo. Nomear não observa. |
| 0.9.436 | O `scan` nomeia as pessoas que o roteiro já recusa. O roteiro já dizia que não prescreve quantas pessoas; a área de QA apontava o documento e calava a recusa. Sem chave `pessoas` no recibo. Nomear não observa. |
| 0.9.437 | O `discover` nomeia a qualidade que o roteiro já recusa. O roteiro já dizia que a existência de documentos não comprova qualidade; o item copiava a conta e calava a recusa. Sem chave `qualidade` no recibo. Nomear não observa. |
| 0.9.438 | O `record` nomeia a animação que o roteiro já recusa. O roteiro já dizia que screenshot isolada não comprova animação; o anexo copiava o hash e calava a recusa. Sem chave `animação` no recibo. Nomear não observa. |
| 0.9.439 | O `art` nomeia a paleta que o sistema já recusa. O contrato já dizia que o design system não é uma paleta compartilhada; o item copiava a chave e calava a recusa. Sem chave `paleta` no recibo. Nomear não observa. |
| 0.9.440 | O `doctor` nomeia o publisher que a skill já recusa. A skill já dizia que AAA não é tier de publisher; o atalho copiava o hash e calava a recusa. Sem chave `publisher` no recibo. Nomear não observa. |
| 0.9.441 | O `roles` nomeia a quantidade que a receita já recusa. A receita já dizia que áudio AAA não é quantidade de arquivos; o item copiava a lista e calava a recusa. Sem chave `quantidade` no recibo. Nomear não observa. |
| 0.9.442 | O `scan` nomeia as intenções que o roteiro já recusa. O roteiro já dizia que reconstruir documentos não comprova intenções autorais; o candidato copiava o path e calava a recusa. Sem chave `intenções` no recibo. Nomear não observa. |
| 0.9.443 | O `access` nomeia a certificação que a pesquisa já recusa. A pesquisa já dizia que acessibilidade não é gate de certificação; o item copiava a chave e calava a recusa. Sem chave `certificação` no recibo. Nomear não observa. |
| 0.9.444 | O `feel` nomeia o autor que a receita já recusa. A receita já dizia que o autor sugerido no comando não é quem jogou; o item copiava o autor e calava a recusa. Sem chave `autor` no recibo. Nomear não observa. |
| 0.9.445 | O `art` nomeia o volume que a receita já recusa. A receita já dizia que mesa no disco não é volume; o item copiava a chave e calava a recusa. Sem chave `volume` no recibo. Nomear não observa. |
| 0.9.446 | O `gate` nomeia a dispensa que o roteiro já recusa. O roteiro já dizia que must_meet não é dispensável; o critério copiava o tipo e calava a recusa. Sem chave `dispensa` no recibo. Nomear não observa. |
| 0.9.447 | O `feel` nomeia o universal que a receita já recusa. A receita já dizia que valores iniciais não são constantes universais; o item copiava o número e calava a recusa. Sem chave `universais` no recibo. Nomear não observa. |
| 0.9.448 | O `bar` nomeia a dimensão que a barra já recusa. A barra já dizia que o nome não é uma das dez; o problema copiava o achado e calava a recusa. Sem chave `dimensão` no recibo. Nomear não observa. |
| 0.9.449 | O `gate` nomeia o escopo que o roteiro já recusa. O roteiro já dizia que fora de escopo não é dispensa; o problema copiava o achado e calava a recusa. Sem chave `escopo` no recibo. Nomear não observa. |
| 0.9.450 | O `origins` nomeia os rótulos que o roteiro já recusa. O roteiro já dizia que sidecar sem os três rótulos não declara; o problema copiava o achado e calava a recusa. Sem chave `rótulos` no recibo. Nomear não observa. |
| 0.9.451 | O `craft` nomeia a definição que a pesquisa já recusa. A pesquisa já dizia que número sem definição declarada não é critério; o problema copiava o achado e calava a recusa. Sem chave `definição` no recibo. Nomear não observa. |
| 0.9.452 | O `doctor` nomeia a ausência que o mapa já recusa. O mapa já dizia que studies vazio não é evidência negativa; o check copiava o estado e calava a recusa. Sem chave `ausência` no recibo. Nomear não observa. |
| 0.9.453 | O `sources[n]` do continuity nomeia a fila que o processo já recusa. O processo já dizia que `sources_found` não comprova fila atual; a fonte copiava o caminho e calava a recusa. Sem chave `fila` no recibo. Nomear não executa. |
| 0.9.454 | O `genre_mentions[n]` nomeia a mecânica que o mapa já recusa. O mapa já dizia que nenhuma regra foi copiada como mecânica obrigatória; o campo copiava o valor e calava a recusa. Sem chave `mecânica` no recibo. Nomear não classifica. |
| 0.9.455 | O `issues[n]` da coverage nomeia o acidente que o mapa já recusa. O mapa já dizia que cobertura desigual não é acidente; o issue copiava o motivo e calava a recusa. Sem chave `acidente` no recibo. Nomear não inventaria. |
| 0.9.456 | O `tree` do ship nomeia a identidade que a receita já recusa. A receita já dizia que identidade do artefato não é outra máquina; a árvore copiava as partes e calava a recusa. Sem chave `identidade` no recibo. Nomear não executa. |
| 0.9.457 | O `capabilities` desconhecido nomeia o determinismo que a barra já recusa. A barra já dizia que determinismo não é uma capacidade nomeada; o item copiava o estado e calava a recusa. Sem chave `determinismo` no recibo. Nomear não prova. |
| 0.9.458 | O `artifact` do ship nomeia o editor que a receita já recusa. A receita já dizia que um teste no editor não demonstra o jogo exportado; o manifesto copiava nome e versão e calava a recusa. Sem chave `editor` no recibo. Nomear não executa. |
| 0.9.459 | O `candidate_tally` nomeia o cinco que a pesquisa já recusa. A pesquisa já dizia que cinco playtesters não é critério; a conta copiava os verbos e calava a recusa. Sem chave `cinco` no recibo. Nomear não observa. |
| 0.9.460 | O `non_current_documents[n]` nomeia as linhas que a guia já recusa. A guia já dizia que preencher linhas não certifica o jogo; o rascunho copiava o estado e calava a recusa. Sem chave `linhas` no recibo. Nomear não certifica. |
| 0.9.461 | O `metadata_issues[n]` nomeia o semântico que a guia já recusa. A guia já dizia que a checagem não é validador semântico de PRD/GDD; o issue copiava o parse e calava a recusa. Sem chave `semântico` no recibo. Nomear não valida. |
| 0.9.462 | O `candidate_curve` nomeia o aperto que a receita já recusa. A receita já dizia que aperto no disco não é curva observada; a curva copiava never_banked e calava a recusa. Sem chave `aperto` no recibo. Nomear não observa. |
| 0.9.463 | O `conflicts[n]` do `bar` nomeia a precedência que a barra já recusa. A barra já dizia que duas linhas discordantes não se resolvem por precedência; o conflito copiava as fontes e calava a recusa. Sem chave `precedência` no recibo. Nomear não observa. |
| 0.9.464 | O `sfx import` nomeia a improvisação que a receita já recusa. A receita já dizia que tocar na página não autoriza improvisar licença; o import copiava a conta e calava a recusa. Sem chave `improvisar` no recibo. Nomear não ouve. |
| 0.9.465 | O `sfx info` do stem nomeia o lixo que a receita já recusa. A receita já dizia que arquivo sem papel não é áudio do jogo; a ficha copiava licença e bytes e calava a recusa. Sem chave `lixo` no recibo. Nomear não ouve. |
| 0.9.466 | O `runbook` do `scan` nomeia a telemetria que a receita já recusa. A receita já dizia que telemetria não é padrão silencioso; a área copiava o rótulo e calava a recusa. Sem chave `telemetria` no recibo. Nomear não observa. |
| 0.9.467 | O `decisions` do `scan` nomeia o histórico que a receita já recusa. A receita já dizia que histórico não se promove a regra vigente; a área copiava o rótulo e calava a recusa. Sem chave `histórico` no recibo. Nomear não observa. |
| 0.9.468 | O `gdd` do `scan` nomeia o divertido que a guia já recusa. A guia já dizia que divertido isoladamente não basta; a área copiava o rótulo e calava a recusa. Sem chave `divertido` no recibo. Nomear não observa. |
| 0.9.469 | O `mda` do `scan` nomeia a pontuação que a guia já recusa. A guia já dizia que não há pontuação universal de diversão; a área copiava o rótulo e calava a recusa. Sem chave `pontuação` no recibo. Nomear não observa. |
| 0.9.470 | O `vision` do `scan` nomeia o público que a guia já recusa. A guia já dizia para não inventar público observado; a área copiava o rótulo e calava a recusa. Sem chave `público` no recibo. Nomear não observa. |
| 0.9.471 | O `scale_mentions[n]` do `scan` nomeia o marketing que a ambição já recusa. A ambição já dizia que AAA não é adjetivo de marketing; o campo copiava o valor e calava a recusa. Sem chave `marketing` no recibo. Nomear não observa. |
| 0.9.472 | O `options[n]` do `access` nomeia a opção que a receita já recusa. A receita já dizia que opção sem consumidor não é uma opção; o item copiava a chave e calava a recusa. Sem chave `opção` no recibo. Nomear não observa. |
| 0.9.473 | O `commands[n]` do catálogo nomeia o genérico que o menu já recusa. O menu já dizia que invocar sem carregar a referência produz trabalho genérico; a linha copiava o nome e calava a recusa. Sem chave `genérico` no recibo. Nomear não observa. |
| 0.9.474 | O `discover --plain` nomeia a listagem que o README já recusa. O README já dizia que listagem de caminho e tipo apagava o estado; o item copiava path e kind e calava a recusa. Sem chave `listagem` no recibo. Nomear não observa. |
| 0.9.475 | O `skipped[n]` do `pin` nomeia a própria que o README já recusa. O README já dizia que uma skill sua com o mesmo nome nunca é sobrescrita; o item copiava path e reason e calava a recusa. Sem chave `própria` no recibo. Nomear não observa. |
| 0.9.476 | O `workspace_module` do `context` nomeia a preenchida que a ligação já recusa. A ligação já dizia que pasta não baixada não é preenchida pelo starter; o módulo copiava estado e calava a recusa. Sem chave `preenchida` no recibo. Nomear não observa. |
| 0.9.477 | O `delivery_review` do `context` nomeia as regras que a entrega já recusa. A entrega já dizia que templates preenchidos não comprovam regras; o bloco copiava critérios e calava a recusa. Sem chave `regras` no recibo. Nomear não observa. |
| 0.9.478 | O `workspace` do `context` nomeia o inventado que a ligação já recusa. A ligação já dizia que conteúdo de referência ausente não é inventado; o bloco copiava caminhos e calava a recusa. Sem chave `inventado` no recibo. Nomear não observa. |
| 0.9.479 | O `prompt` do `continuity` nomeia a receita que o gauntlet já recusa. O gauntlet já dizia que o arquivo de prompts não é a fonte de status; o bloco copiava a política e calava a recusa. Sem chave `receita` no recibo. Nomear não observa. |
| 0.9.480 | O `initialization` do `context` nomeia a pergunta que o roteiro já recusa. O roteiro já dizia que o aviso não é uma pergunta; o bloco copiava o notice e calava a recusa. Sem chave `pergunta` no recibo. Nomear não observa. |
| 0.9.481 | O `capabilities[n]` do `verify` nomeia o suporte que a receita já recusa. A receita já dizia que registro declarado não prova suporte real; o item copiava claimed e calava a recusa. Sem chave `suporte` no recibo. Nomear não observa. |
| 0.9.482 | O contrato do `gauntlet` nomeia o infinito que o gauntlet já recusa. O gauntlet já dizia que horas nulas não são prazo infinito; o contrato copiava budget_hours e calava a recusa. Sem chave `infinito` no recibo. Nomear não observa. |
| 0.9.483 | O `limits` da coverage nomeia a prioridade que o roteiro já recusa. O roteiro já dizia que o recorte de estudo não toma a prioridade da base; os tetos copiavam os números e calavam a recusa. Sem chave `prioridade` no recibo. Nomear não observa. |
| 0.9.484 | O `template` do MVP nomeia o valor que a guia já recusa. A guia já dizia que um MVP não prova a hipótese de valor; o molde emitia o rascunho e calava a recusa. Sem chave `valor` no recibo. Nomear não observa. |
| 0.9.485 | O `template` da vertical-slice nomeia o acabamento que a guia já recusa. A guia já dizia que placeholders não certificam o acabamento da fatia; o molde emitia o rascunho e calava a recusa. Sem chave `acabamento` no recibo. Nomear não observa. |
| 0.9.486 | O `gate` close nomeia a hipótese que a guia já recusa. A guia já dizia que código que compila não prova hipótese criativa; o item listava o veredito e calava a recusa. Sem chave `hipótese` no recibo. Nomear não observa. |
| 0.9.487 | O `gate` deliver nomeia o lançamento que o fluxo já recusa. O fluxo já dizia que um teste local concluído não é lançamento; o item listava o runbook e calava a recusa. Sem chave `lançamento` no recibo. Nomear não observa. |
| 0.9.488 | O `content` nomeia a composição que a receita já recusa. A receita já dizia que mais módulos não provam composição natural; o comando listava arquivos e calava a recusa. Sem chave `composição` no recibo. Nomear não observa. |
| 0.9.489 | O `prompt` do continuity nomeia a prontidão que o processo já recusa. O processo já dizia que arquivos encontrados não comprovam prontidão; o bloco copiava readiness e calava a recusa. Sem chave `prontidão` no recibo. Nomear não observa. |
| 0.9.490 | O item da constante nomeia a posição que a receita já recusa. A receita já dizia que velocidade não nula não prova a posição integrada; o item copiava o número e calava a recusa. Sem chave `posição` no recibo. Nomear não observa. |
| 0.9.491 | A plataforma nomeia os quadros que o pacote já recusa. O pacote já dizia que métricas RAF não comprovam quadros da GPU; a plataforma apontava o arquivo e calava a recusa. Sem chave `quadros` no recibo. Nomear não observa. |
| 0.9.492 | O comando do verify nomeia o significado que a entrega já recusa. A entrega já dizia que o hash não comprova o significado; o comando copiava o sha256 e calava a recusa. Sem chave `significado` no recibo. Nomear não observa. |
| 0.9.493 | O ciclo nomeia o livre que a receita já recusa. A receita já dizia que estar em run não prova estar livre para atacar; o ciclo anunciava o verbo e calava a recusa. Sem chave `livre` no recibo. Nomear não observa. |
| 0.9.494 | O candidato da arquitetura nomeia a compreendida que a receita já recusa. A receita já dizia que contexto carregado não significa arquitetura compreendida; o candidato copiava o path e calava a recusa. Sem chave `compreendida` no recibo. Nomear não observa. |
| 0.9.495 | O `signals` do next nomeia a conclusão que a receita já recusa. A receita já dizia que nome de comando, arquivo ou fase não comprovam conclusão; o next copiava os sinais e calava a recusa. Sem chave `conclusão` no recibo. Nomear não observa. |
| 0.9.496 | O contrato do `gauntlet` nomeia a independência que o gauntlet já recusa. O gauntlet já dizia que papéis simulados não comprovam independência; o contrato copiava o objetivo e calava a recusa. Sem chave `independência` no recibo. Nomear não observa. |
| 0.9.497 | O `sfx info` do acervo nomeia o decode que a receita já recusa. A receita já dizia que teste técnico de decode não aprova mix; a ficha copiava id e créditos e calava a recusa. Sem chave `decode` no recibo. Nomear não observa. |
| 0.9.498 | O `tree` do ship nomeia a portabilidade que a receita já recusa. A receita já dizia que abrir o menu ou obter um ZIP não comprova portabilidade; a árvore copiava as partes e calava a recusa. Sem chave `portabilidade` no recibo. Nomear não observa. |
| 0.9.499 | O `artifact` do ship nomeia a atual que a receita já recusa. A receita já dizia que uma pasta de build existente não prova a fonte atual; o manifesto copiava o git_head e calava a recusa. Sem chave `atual` no recibo. Nomear não observa. |
| 0.9.500 | O `scan` nomeia o multiplayer que a receita já recusa. A receita já dizia que exemplares locais não comprovam comportamento multiplayer; a área localizava o TDD e calava a recusa. Sem chave `multiplayer` no recibo. Nomear não observa. |
| 0.9.501 | O `signals` do review nomeia a partida que o README já recusa. O README já dizia que sinal verdadeiro não é partida jogada; o signals copiava os flags e calava a recusa. Sem chave `partida` no recibo. Nomear não observa. |
| 0.9.502 | O `sfx copy` do acervo nomeia o ouvir que a receita já recusa. A receita já dizia que importar e exportar não é ouvir; o copy levava bytes e créditos e calava a recusa. Sem chave `ouvir` no recibo. Nomear não ouve. |
| 0.9.503 | O `local` do `sfx search` nomeia o adapt que a receita já recusa. A receita já dizia que o acervo compartilhado é ADAPT, não o primeiro ciclo; o local listava stems e calava a recusa. Sem chave `adapt` no recibo. Nomear não ouve. |
| 0.9.504 | O `sfx seed` nomeia a aprovação que a receita já recusa. A receita já dizia que avaliação do agente não é aprovação do usuário; o seed importava a seleção e calava a recusa. Sem chave `aprovação` no recibo. Nomear não ouve. |
| 0.9.505 | O `matches` do `sfx search` nomeia a triagem que a barra já recusa. A barra já dizia que triagem documental/técnica não é aprovação artística; o match listava licenças e calava a recusa. Sem chave `triagem` no recibo. Nomear não ouve. |
| 0.9.506 | O `sfx verify` vazio nomeia a lacuna que a receita já recusa. A receita já dizia que variante ausente não é lacuna; o verify vazio listava stems e calava a recusa. Sem chave `lacuna` no recibo. Nomear não ouve. |
| 0.9.507 | O `sfx export` do stem nomeia a invenção que a receita já recusa. A receita já dizia que exportar não inventa bytes; o export do stem copiava o WAV e calava a recusa. Sem chave `invenção` no recibo. Nomear não ouve. |
| 0.9.508 | O `missing` do `sfx verify` nomeia o 404 que a receita já recusa. A receita já dizia que nomear o 404 não é mix ouvido; o verify listava o stem ausente e calava a recusa. Sem chave `404` no recibo. Nomear não ouve. |
| 0.9.509 | A opção `captions` do `access` nomeia o número que a receita já recusa. A receita já dizia que número na legenda não é mix ouvido; a opção copiava a chave e calava a recusa. Sem chave `número` no recibo. Nomear não ouve. |
| 0.9.510 | O papel do x do campo nomeia o panner que a receita já recusa. A receita já dizia que número no panner não é mix ouvido; o papel copiava o id e calava a recusa. Sem chave `panner` no recibo. Nomear não ouve. |
| 0.9.511 | O `roles` nomeia o retomar que a receita já recusa. A receita já dizia que retomar, fila e paralelo não são mix ouvido; o comando lia SOUNDS e calava a recusa. Sem chave `retomar` no recibo. Nomear não ouve. |
| 0.9.512 | A opção `haptics` do `access` nomeia o controle que a receita já recusa. A receita já dizia que pulso no disco não é sessão no controle; a opção copiava a chave e calava a recusa. Sem chave `controle` no recibo. Nomear não observa. |
| 0.9.513 | A opção `remap` do `access` nomeia o botão que a receita já recusa. A receita já dizia que botão no disco não é sessão; a opção copiava a chave e calava a recusa. Sem chave `botão` no recibo. Nomear não observa. |
| 0.9.514 | A opção `reduced_motion` do `access` nomeia a causa que a receita já recusa. A receita já dizia que reduzir o movimento não apaga a causa; a opção copiava a chave e calava a recusa. Sem chave `causa` no recibo. Nomear não observa. |
| 0.9.515 | A opção `high_contrast` do `access` nomeia o neutro que a receita já recusa. A receita já dizia que contraste em fundo neutro não é o pior caso; a opção copiava a chave e calava a recusa. Sem chave `neutro` no recibo. Nomear não observa. |
| 0.9.516 | A opção `colorblind` do `access` nomeia o ícone que a receita já recusa. A receita já dizia que o estado não depende só da cor; a opção copiava a chave e calava a recusa. Sem chave `ícone` no recibo. Nomear não observa. |
| 0.9.517 | A opção `one_hand` do `access` nomeia a mão que a receita já recusa. A receita já dizia que o jogo se completa com uma das mãos; a opção copiava a chave e calava a recusa. Sem chave `mão` no recibo. Nomear não observa. |
| 0.9.518 | A opção `assist` do `access` nomeia o oculto que a receita já recusa. A receita já dizia que assistência não esconde conteúdo; a opção copiava a chave e calava a recusa. Sem chave `oculto` no recibo. Nomear não observa. |
| 0.9.519 | A opção `game_speed` do `access` nomeia a precisão que a receita já recusa. A receita já dizia que precisão sem alternativa não é alcance; a opção copiava a chave e calava a recusa. Sem chave `precisão` no recibo. Nomear não observa. |
| 0.9.520 | A opção `ui_scale` do `access` nomeia a tipografia que a receita já recusa. A receita já dizia que tipografia precisa ser legível no dispositivo; a opção copiava a chave e calava a recusa. Sem chave `tipografia` no recibo. Nomear não observa. |
| 0.9.521 | A opção `live` do `access` nomeia o leitor que a receita já recusa. A receita já dizia que o overlay do canvas não chega ao leitor; a opção copiava a chave e calava a recusa. Sem chave `leitor` no recibo. Nomear não observa. |
| 0.9.522 | O convite nomeia as sessões que a receita já recusa. A receita já dizia que compartilhar o endereço não é duas sessões reais; o convite anunciava a rede e calava a recusa. Sem chave `sessões` no recibo. Nomear não observa. |
| 0.9.523 | O `record` do `sfx copy` do acervo nomeia o consumido que a receita já recusa. A receita já dizia que arquivo gerado ou importado não comprova consumo; o record copiava autor e licença e calava a recusa. Sem chave `consumido` no recibo. Nomear não ouve. |
| 0.9.524 | O then do `start` nomeia a experiência que a receita já recusa. A receita já dizia que título e cores novos não demonstram experiência; o then apontava play e calava a recusa. Sem chave `experiência` no recibo. Nomear não observa. |

`python3 scripts/game.py` sem subcomando é o `guide`. Na raiz do
framework, sem `--idea` e sem caminho, recusa com `sem destino` —
e a recusa nomeia o `start --idea` do README. Nomear não cria.
`--idea` no parser principal também funciona sem subcomando.

---

## Barra vigente do starter

Piso percebido = **mínimo**. O `bar` nomeia o mínimo que a barra já declara. Só `release` está em `prototype`.

| Dimensão | Degrau | Lacuna seguinte |
| --- | --- | --- |
| feel | playable | o then do `start` nomeia a experiência que a receita já recusa; o contrato do `gauntlet` nomeia a independência que o gauntlet já recusa; o `signals` do next nomeia a conclusão que a receita já recusa; o candidato da arquitetura nomeia a compreendida que a receita já recusa; o ciclo nomeia o livre que a receita já recusa; o comando do verify nomeia o significado que a entrega já recusa; a plataforma nomeia os quadros que o pacote já recusa; o item da constante nomeia a posição que a receita já recusa; o `prompt` do continuity nomeia a prontidão que o processo já recusa; o `content` nomeia a composição que a receita já recusa; o `gate` deliver nomeia o lançamento que o fluxo já recusa; o `gate` close nomeia a hipótese que a guia já recusa; o `template` da vertical-slice nomeia o acabamento que a guia já recusa; o `template` do MVP nomeia o valor que a guia já recusa; o `limits` da coverage nomeia a prioridade que o roteiro já recusa; o contrato do `gauntlet` nomeia o infinito que o gauntlet já recusa; o `capabilities[n]` do `verify` nomeia o suporte que a receita já recusa; o `context` nomeia a pergunta que o roteiro já recusa; o `context` nomeia a receita que o gauntlet já recusa; o `context` nomeia o inventado que a ligação já recusa; o `context` nomeia as regras que a entrega já recusa; o `context` nomeia a preenchida que a ligação já recusa; o `pin` nomeia a própria que o README já recusa; o `discover` nomeia a listagem que o README já recusa; o `commands` nomeia o genérico que o menu já recusa; o `access` nomeia a opção que a receita já recusa; o `scan` nomeia o marketing que a ambição já recusa; o `scan` nomeia o público que a guia já recusa; o `scan` nomeia a pontuação que a guia já recusa; o `scan` nomeia o divertido que a guia já recusa; o `feel` nomeia o universal que a receita já recusa; o `feel` nomeia o autor que a receita já recusa; o passo de gravar nomeia o screenshot que a receita já recusa; o `feel` nomeia o land que o dash já emite; o `feel` nomeia o sit que a guarda já senta; o `feel` nomeia a inclinação que o lookAhead já marca; o `feel` nomeia o perdão que o probe já exercita; o `feel` nomeia o corpo que a porta já desloca; o `feel` nomeia o peso do passo que o CONFIG já declara; o `feel` nomeia o rumble que já lê; o rótulo do dash nomeia o avanço no travel; o compromisso da guarda veste a aposta; o coil da guarda veste a aposta; o coil do dash veste o avanço; o coil do dash marca o rumo no corpo; o rastro do dash veste o avanço; o `next` do feel anexa o candidato; a folga que acaba nomeia a folga; a prática que acaba nomeia a ameaça; o `feel` nomeia as janelas da chuva; o corpo na recuperação do dash não veste a prática; `brief` não come a folga da guarda; o aviso nomeia a prática; o relógio nomeia a pausa; no campo o telefone pausa no relógio; o feel nomeia a partida do last-run; depois da partida o baixo pede seed nova; na pausa o telefone vê toque; a região viva nomeia como sair da pausa; a pausa nomeia reiniciar; depois do tap a porta não chama cima; na porta o telefone vê toque; na pausa o toque retoma; o controle que some não deixa a partida correr; a perda de foco não deixa o ofício pendente; a aba escondida não deixa o verbo preso; o botão focado não dispara o verbo; a tecla do remap não dispara o verbo; o toque que sai do campo ainda solta; o recado não dispara o verbo; o hold leva o relógio da porta; o hitstop não come o perdão; a guarda espera o land; o tap na faixa da porta abre; o avanço é o aperto; peso no dispositivo; coil no disco ≠ felt |
| legibility | playable | stub ≠ dispositivo |
| art_direction | slice | o `art` nomeia o volume que a receita já recusa; o `art` nomeia a paleta que o sistema já recusa; o `scan` nomeia os tokens que o sistema já recusa; o `art` nomeia o contraste que o look já recusa; o `art` nomeia a vinheta que o recorte já marca; o `art` nomeia o trilho que o telegraph já marca; o `art` nomeia o look que o disco já nasce; o `art` nomeia o risco da chuva; o compromisso da guarda veste a aposta; a porta chove o risco da mesa; o coil da guarda veste a aposta; o coil do dash veste o avanço; o coil do dash marca o rumo no corpo; o rastro do dash veste o avanço; o corpo na recuperação do dash não veste a prática; a receita do look nomeia o perigo; o art-bible nomeia as janelas do campo; o `art` nomeia a chuva; os knobs vestem o look; tinta estável não esmaga dusk/calm; `consistent` falso |
| audio_mix | slice | o `record` do `sfx copy` do acervo nomeia o consumido que a receita já recusa; a opção `live` do `access` nomeia o leitor que a receita já recusa; a opção `ui_scale` do `access` nomeia a tipografia que a receita já recusa; a opção `game_speed` do `access` nomeia a precisão que a receita já recusa; a opção `assist` do `access` nomeia o oculto que a receita já recusa; a opção `one_hand` do `access` nomeia a mão que a receita já recusa; a opção `colorblind` do `access` nomeia o ícone que a receita já recusa; a opção `high_contrast` do `access` nomeia o neutro que a receita já recusa; a opção `reduced_motion` do `access` nomeia a causa que a receita já recusa; a opção `remap` do `access` nomeia o botão que a receita já recusa; a opção `haptics` do `access` nomeia o controle que a receita já recusa; o `roles` nomeia o retomar que a receita já recusa; o papel do x do campo nomeia o panner que a receita já recusa; a opção `captions` do `access` nomeia o número que a receita já recusa; o `missing` do `sfx verify` nomeia o 404 que a receita já recusa; o `sfx export` do stem nomeia a invenção que a receita já recusa; o `sfx verify` vazio nomeia a lacuna que a receita já recusa; o `matches` do `sfx search` nomeia a triagem que a barra já recusa; o `sfx seed` nomeia a aprovação que a receita já recusa; o `local` do `sfx search` nomeia o adapt que a receita já recusa; o `sfx copy` do acervo nomeia o ouvir que a receita já recusa; o `sfx info` do acervo nomeia o decode que a receita já recusa; o `sfx info` do stem nomeia o lixo que a receita já recusa; o `sfx import` nomeia a improvisação que a receita já recusa; o `roles` nomeia a quantidade que a receita já recusa; o `context` nomeia a escuta que o mapa já recusa; o `roles --fill` nomeia o reuso que o processo já recusa; o `sfx export` nomeia o processamento que o export já recusa; o `sfx verify` nomeia a integridade que o check já cruza; o `sfx copy` nomeia os créditos que o copy já leva; o `roles` nomeia o PCM que o wav já lê; o `sfx search` nomeia o deslocamento que o sfx já oferece; o `sfx summary` nomeia o pico que o peak já relata; o `sfx info` nomeia o pico que o inspect já mede; o `roles` nomeia a voz que o sfx já desloca; o `roles` nomeia a soma que a receita já relata; o `roles` nomeia o `duckMs` que `SOUNDS` já declara; o `sfx verify` nomeia o som que o catálogo perdeu; o `sfx export` nomeia o stem que o disco perdeu; a folga que acaba nomeia a folga; a prática que acaba nomeia a ameaça; a região viva nomeia a lacuna do som; a escuta nomeia o som que o catálogo perdeu; a cama segue o relógio da sessão; o `sfx info` nomeia o stem que o disco perdeu; o pulso do fecho não come a legenda do verbo; o painel relê a lacuna quando o fetch termina; decode nulo tenta a próxima extensão; o painel nomeia o 404 mesmo quando outro papel registrou; o fim leva o x do campo; o controle também pede o resume; o pedido suspenso espera o gesto; `heard` falso |
| pacing | slice | o `candidate_curve` nomeia o aperto que a receita já recusa; o `candidate_tally` nomeia o cinco que a pesquisa já recusa; o convite nomeia as sessões que a receita já recusa; o convite nomeia o bind que o serve já prende; o `playtest` nomeia o recado que o serve já grava; o `note` nomeia o last-run que o disco já guarda; o `playtest` nomeia a simulação que a receita já grava; o prompt nomeia o `playtest` que o `AGENTS.md` já cita; o achado copiado nomeia o last-run simulado; a faixa nomeia o last-run simulado; o `playtest` nomeia a conta do last-run; a porta chove o risco da mesa; o `next` do feel anexa o candidato; o `feel` nomeia as janelas da chuva; o aviso nomeia a prática; o Copiar nomeia o destino; o `playtest` nomeia a página do achado; o `next` unstructured nomeia a página do achado; finding_href abre o convite; o banner do serve nomeia o relógio que o jogo já lê; a sessão nomeia o look e o relógio que o convite já lê; o convite nomeia o relógio da partida; a faixa nomeia a curva que o last-run já traçou; fecho aperta intervalo e risco no disco; curva com outsider pendente |
| state_trust | slice | o `scan` nomeia o histórico que a receita já recusa; o `save` nomeia a gravação que o storage já verifica; o `save` nomeia o fechamento que o disco já grava; o `save` nomeia a recuperação que o canvas já pinta; a query de chuva não retoma o hold de outra mesa; o convite não grava o look, a chuva nem o relógio que só vestiu; o controle que some grava o hold; a perda de foco grava o hold; a receita não cala a porta que o canvas já pinta; a porta nomeia a recuperação que o painel já mostra; o preset de uma mão não some o remap; a outra aba veste as preferências; o hold leva o relógio da porta; live nomeia a mesma recuperação; `persistLine` continua só sessão; `save` relata `warned`; beforeunload no disco; aba fechada real não observada; `trusted` falso |
| performance | playable | a plataforma nomeia os quadros que o pacote já recusa; o `budget` nomeia o percentil que a receita já pede; o `budget` nomeia os bytes que o size já relata; o `budget` nomeia a porta que a receita já cronometra; o orçamento cronometra a porta; poços + stub ≠ dispositivo |
| accessibility | slice | a opção `live` do `access` nomeia o leitor que a receita já recusa; a opção `ui_scale` do `access` nomeia a tipografia que a receita já recusa; a opção `game_speed` do `access` nomeia a precisão que a receita já recusa; a opção `assist` do `access` nomeia o oculto que a receita já recusa; a opção `one_hand` do `access` nomeia a mão que a receita já recusa; a opção `colorblind` do `access` nomeia o ícone que a receita já recusa; a opção `high_contrast` do `access` nomeia o neutro que a receita já recusa; a opção `reduced_motion` do `access` nomeia a causa que a receita já recusa; a opção `remap` do `access` nomeia o botão que a receita já recusa; a opção `haptics` do `access` nomeia o controle que a receita já recusa; o `roles` nomeia o retomar que a receita já recusa; o papel do x do campo nomeia o panner que a receita já recusa; a opção `captions` do `access` nomeia o número que a receita já recusa; o contrato do `gauntlet` nomeia a independência que o gauntlet já recusa; o `signals` do next nomeia a conclusão que a receita já recusa; o candidato da arquitetura nomeia a compreendida que a receita já recusa; o ciclo nomeia o livre que a receita já recusa; o comando do verify nomeia o significado que a entrega já recusa; a plataforma nomeia os quadros que o pacote já recusa; o item da constante nomeia a posição que a receita já recusa; o `prompt` do continuity nomeia a prontidão que o processo já recusa; o `content` nomeia a composição que a receita já recusa; o `gate` deliver nomeia o lançamento que o fluxo já recusa; o `gate` close nomeia a hipótese que a guia já recusa; o `template` da vertical-slice nomeia o acabamento que a guia já recusa; o `template` do MVP nomeia o valor que a guia já recusa; o `limits` da coverage nomeia a prioridade que o roteiro já recusa; o contrato do `gauntlet` nomeia o infinito que o gauntlet já recusa; o `capabilities[n]` do `verify` nomeia o suporte que a receita já recusa; o `context` nomeia a pergunta que o roteiro já recusa; o `context` nomeia a receita que o gauntlet já recusa; o `context` nomeia o inventado que a ligação já recusa; o `context` nomeia as regras que a entrega já recusa; o `context` nomeia a preenchida que a ligação já recusa; o `pin` nomeia a própria que o README já recusa; o `discover` nomeia a listagem que o README já recusa; o `commands` nomeia o genérico que o menu já recusa; o `access` nomeia a opção que a receita já recusa; o `access` nomeia a certificação que a pesquisa já recusa; o `access` nomeia a legenda que a porta já lê; o `access` nomeia as teclas que a tabela já lista; o `access` nomeia o perigo que o live já anuncia; o `access` nomeia o contraste que a receita já amostra; o `access` nomeia o `:focus-visible` que a casca já declara; o canvas da porta e do fim nomeia a lacuna do som; a região viva nomeia a mesa e o look da porta e do fim; a folga que acaba nomeia a folga; a prática que acaba nomeia a ameaça; o aviso nomeia a prática; a região viva nomeia a lacuna do som; o Copiar nomeia o destino; o relógio nomeia a pausa; no campo o telefone pausa no relógio; a região viva nomeia como abrir a porta; depois da partida o baixo pede seed nova; na pausa o telefone vê toque; a região viva nomeia como sair da pausa; a pausa nomeia reiniciar; depois do tap a porta não chama cima; na porta o telefone vê toque; na pausa o toque retoma; a cama segue o relógio da sessão; o controle que some senta o relógio se a sessão falou no pad; o contrato nomeia o pulso que o código já tem; a porta nomeia a recuperação que o painel já mostra; o pulso do fecho não come a legenda do verbo; o sistema que pede reduce no meio da sessão veste a caixa; as faixas nomeiam o valor vigente; o preset de uma mão não some o remap; os knobs vestem o look e têm foco visível; a escala veste a casca da página; live nomeia o aviso do primeiro ciclo; live nomeia a mesma recuperação; tinta estável não esmaga dusk/calm; live nomeia o toque da mostra; sessão observada no controle pendente |
| content_scale | shippable | o `content` nomeia a composição que a receita já recusa; o `content` nomeia a migração que as mesas já compartilham; o `start` nomeia o par que o pair já nasce; o `content` nomeia a mesa que o disco já nasce; o `content` nomeia o par que `listMoods` já lista; `brief` não come a folga da guarda; paleta não finge volume; dusk+calm+pair; `enough` falso |
| release | **prototype** | o `record` do `sfx copy` do acervo nomeia o consumido que a receita já recusa; a opção `live` do `access` nomeia o leitor que a receita já recusa; a opção `ui_scale` do `access` nomeia a tipografia que a receita já recusa; a opção `game_speed` do `access` nomeia a precisão que a receita já recusa; a opção `assist` do `access` nomeia o oculto que a receita já recusa; a opção `one_hand` do `access` nomeia a mão que a receita já recusa; a opção `colorblind` do `access` nomeia o ícone que a receita já recusa; a opção `high_contrast` do `access` nomeia o neutro que a receita já recusa; a opção `reduced_motion` do `access` nomeia a causa que a receita já recusa; a opção `remap` do `access` nomeia o botão que a receita já recusa; a opção `haptics` do `access` nomeia o controle que a receita já recusa; o `roles` nomeia o retomar que a receita já recusa; o papel do x do campo nomeia o panner que a receita já recusa; a opção `captions` do `access` nomeia o número que a receita já recusa; o `missing` do `sfx verify` nomeia o 404 que a receita já recusa; o `sfx export` do stem nomeia a invenção que a receita já recusa; o `sfx verify` vazio nomeia a lacuna que a receita já recusa; o `matches` do `sfx search` nomeia a triagem que a barra já recusa; o `sfx seed` nomeia a aprovação que a receita já recusa; o `local` do `sfx search` nomeia o adapt que a receita já recusa; o `sfx copy` do acervo nomeia o ouvir que a receita já recusa; o `signals` do review nomeia a partida que o README já recusa; o `scan` nomeia o multiplayer que a receita já recusa; o `artifact` do ship nomeia a atual que a receita já recusa; o `tree` do ship nomeia a portabilidade que a receita já recusa; o `sfx info` do acervo nomeia o decode que a receita já recusa; o contrato do `gauntlet` nomeia a independência que o gauntlet já recusa; o `signals` do next nomeia a conclusão que a receita já recusa; o candidato da arquitetura nomeia a compreendida que a receita já recusa; o ciclo nomeia o livre que a receita já recusa; o comando do verify nomeia o significado que a entrega já recusa; a plataforma nomeia os quadros que o pacote já recusa; o item da constante nomeia a posição que a receita já recusa; o `prompt` do continuity nomeia a prontidão que o processo já recusa; o `content` nomeia a composição que a receita já recusa; o `gate` deliver nomeia o lançamento que o fluxo já recusa; o `gate` close nomeia a hipótese que a guia já recusa; o `template` da vertical-slice nomeia o acabamento que a guia já recusa; o `template` do MVP nomeia o valor que a guia já recusa; o `limits` da coverage nomeia a prioridade que o roteiro já recusa; o contrato do `gauntlet` nomeia o infinito que o gauntlet já recusa; o `capabilities[n]` do `verify` nomeia o suporte que a receita já recusa; o `context` nomeia a pergunta que o roteiro já recusa; o `context` nomeia a receita que o gauntlet já recusa; o `context` nomeia o inventado que a ligação já recusa; o `context` nomeia as regras que a entrega já recusa; o `context` nomeia a preenchida que a ligação já recusa; o `pin` nomeia a própria que o README já recusa; o `discover` nomeia a listagem que o README já recusa; o `commands` nomeia o genérico que o menu já recusa; o `access` nomeia a opção que a receita já recusa; o `scan` nomeia o marketing que a ambição já recusa; o `scan` nomeia o público que a guia já recusa; o `scan` nomeia a pontuação que a guia já recusa; o `scan` nomeia o divertido que a guia já recusa; o `scan` nomeia o histórico que a receita já recusa; o `scan` nomeia a telemetria que a receita já recusa; o `sfx info` do stem nomeia o lixo que a receita já recusa; o `sfx import` nomeia a improvisação que a receita já recusa; o `conflicts[n]` do `bar` nomeia a precedência que a barra já recusa; o `candidate_curve` nomeia o aperto que a receita já recusa; o `metadata_issues[n]` nomeia o semântico que a guia já recusa; o `non_current_documents[n]` nomeia as linhas que a guia já recusa; o `candidate_tally` nomeia o cinco que a pesquisa já recusa; o `artifact` do ship nomeia o editor que a receita já recusa; o `capabilities` desconhecido nomeia o determinismo que a barra já recusa; o `tree` do ship nomeia a identidade que a receita já recusa; o `issues[n]` da coverage nomeia o acidente que o mapa já recusa; o `genre_mentions[n]` nomeia a mecânica que o mapa já recusa; o `sources[n]` do continuity nomeia a fila que o processo já recusa; o `doctor` nomeia a ausência que o mapa já recusa; o `craft` nomeia a definição que a pesquisa já recusa; o `origins` nomeia os rótulos que o roteiro já recusa; o `gate` nomeia o escopo que o roteiro já recusa; o `bar` nomeia a dimensão que a barra já recusa; o `feel` nomeia o universal que a receita já recusa; o `gate` nomeia a dispensa que o roteiro já recusa; o `art` nomeia o volume que a receita já recusa; o `feel` nomeia o autor que a receita já recusa; o `discover` nomeia a listagem que o README já recusa; o `commands` nomeia o genérico que o menu já recusa; o `access` nomeia a opção que a receita já recusa; o `access` nomeia a certificação que a pesquisa já recusa; o `scan` nomeia as intenções que o roteiro já recusa; o `roles` nomeia a quantidade que a receita já recusa; o `doctor` nomeia o publisher que a skill já recusa; o `art` nomeia a paleta que o sistema já recusa; o `record` nomeia a animação que o roteiro já recusa; o `discover` nomeia a qualidade que o roteiro já recusa; o `scan` nomeia as pessoas que o roteiro já recusa; o `scan` nomeia a licença que o roteiro já recusa; o `verify` nomeia a diversão que a ambição já recusa; o `next` nomeia a fabricação que o processo já recusa; o `doctor` nomeia o motor que a ambição já recusa; o `bar` nomeia os prazos que a barra já recusa; o `craft` nomeia a escada que a pesquisa já recusa; o `guide` nomeia a abertura que o processo já recusa; o `gate` nomeia o silêncio que o roteiro já recusa; o `next` nomeia a criação que o roteiro já recusa; o `context` nomeia a API que a receita já recusa; o `context` nomeia a extração que o mapa já recusa; o `guide` nomeia o screenshot que a receita já recusa; o `guide` nomeia o onboarding que o roteiro já recusa; o `context` nomeia a capacidade que o índice já recusa; o `scan` nomeia a inexistência que o roteiro já recusa; o `scan` nomeia as dependências que a receita já recusa; o `scan` nomeia os tokens que o sistema já recusa; o `context` nomeia a escuta que o mapa já recusa; o `context` nomeia o progresso que o processo já recusa; o `audit` nomeia o daemon que o roteiro já recusa; o `roles --fill` nomeia o reuso que o processo já recusa; o `version` nomeia o julgamento que o roteiro já recusa; o `doctor` nomeia o exemplo que o README já imprime; o `git` nomeia a leitura que o processo já recusa; o `verify` nomeia a verificação que o processo já recusa; o `verify` nomeia a criatividade que o roteiro já recusa; o `check-plan` nomeia o mérito que o processo já recusa; o `record` nomeia a medição que o roteiro já recusa; o `next` nomeia a ação que o processo já pede; o `context` nomeia o navegador que o pacote já recusa provar; o `context` nomeia a promoção que a barra já recusa; o `context` nomeia o checklist que a guia já recusa preencher; o `scan` nomeia o AAA que a memória já recusa; o `context` nomeia a PoC que o processo já nega; o `context` nomeia o audit que o roteiro já pede; o `template` nomeia a publicação que o molde já recusa; o `scan` nomeia o serve que o README já aponta; o `gate` nomeia o gate que a tabela já declara; o `init` nomeia o módulo que o package já declara; o `discover` nomeia os scripts que o package já declara; o `play` nomeia a produção que o serve já recusa; o `ship` nomeia o file:// que o export já recusa; o `origins` nomeia o consumidor que o sidecar já declara; o `ship` nomeia o passo que o export já declara; o `ship` nomeia o banner que o serve já imprime; o `ship` nomeia o tamanho que a receita já relata; o `ship` nomeia a árvore que perdeu o `src/` que o projeto já tem; ninguém correu o `dist/` fora daqui; `elsewhere` falso |

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
  JSON incompleto (sem origem, autor e licença) não declara; sidecar
  sem os três rótulos também não. Menção em CREDITS.md ainda declara.
  Mídia que o recibo JSON lista e o disco perdeu é nomeada; menção
  em CREDITS.md de caminho ausente continua calada. Nomear não
  devolve o arquivo. Os três campos não validam a licença.
  `origins.scope` nomeia o consumidor se o sidecar
  declara `Consumidor:`. Sem o marcador, a frase some.
  Consumidor no disco não é licença válida. Sem chave
  `consumer` no recibo. Sem chave `consumidor`.
  `fields` continua origem, autor e licença.
  `granted` falso.
- `doctor.scope` nomeia o engines se o package do
  starter pede Node (`engines`). Sem o marcador, a
  frase some. Pedido no disco não é binário no PATH.
  Sem chave `engines` no recibo. Sem check
  `engines`. Nomear não instala. `ready` continua
  python / framework / root. O engines não
  muda `then.guide`.
- `bar.scope` nomeia o mínimo se a prosa
  do projeto declara `mínimo entre`. Sem o
  marcador, a frase some. Degrau no disco
  não é acabamento observado. Sem chave
  `mínimo` no recibo. `assessed` falso.
- `guide.scope` nomeia o relógio se o
  `starter.json` do starter escolhido
  declara `"speed": "`. Sem o marcador, a
  frase some. Frase no disco não é
  partida observada. Sem chave `speed`
  no recibo (`cycle.speed` já existe).
  Sem `then.speed`. Um leitor só: `guide`,
  não `start`. `executed` falso.
- `craft.scope` nomeia a saída de escopo
  se a tabela declara `` `out_of_scope` ``.
  Sem o marcador, a frase some. Linha no
  disco não é ofício observado. Sem chave
  `out_of_scope` no recibo. Um leitor só:
  `craft`, não `gate` nem `review`.
  `observed` e `granted` falsos.
- `art.scope` nomeia o contraste se o
  `tools/new-look.*` declara que contraste
  é alcance, não look. Sem o marcador, a
  frase some. Alcance no disco não é
  comparação em movimento. Sem chave
  `contrast` no recibo. Um leitor só:
  `art`, não `access`. `consistent` falso.
- `doctor.scope` nomeia as substituições se o
  `starter.json` declara `"substitutions": [`.
  Sem o marcador, a frase some. Manifesto no
  disco não é projeto criado. Sem chave
  `substitutions` no recibo. Sem check
  `substitutions`. Nomear não cria. Um leitor
  só: `doctor`, não `init`. `ready` continua
  python / framework / root.
- `review.scope` (`discover` sem `--plain`) nomeia
  os scripts se um jogo revisado declara
  `"scripts": {` no `package.json`. Sem o
  marcador, a frase some. Lista no disco não
  é passo executado. Sem chave `scripts` no
  recibo. Um leitor só: `discover`, não
  `next`. `observed` e `granted` continuam
  ausentes do recibo.
- `init.scope` nomeia o módulo se o package do
  starter declara `"type": "module"`. Sem o
  marcador, a frase some. Tipo no disco não
  é runtime instalado. Sem chave `type` no
  recibo. Um leitor só: `init`, não `start`
  nem `doctor`. `executed` falso.
- `gate.scope` nomeia o gate se um `GATE_SOURCES`
  declara uma linha `GATE_ROW`. Sem o
  marcador, a frase some. Linha no disco não
  é passagem concedida. Sem chave `gate` no
  recibo. Um leitor só: `gate`, não `next`
  nem `craft`. `granted` falso.
- `scan.scope` nomeia o serve se o `README.md`
  declara `npm run serve`. Sem o marcador, a
  frase some. Página no disco não é partida
  jogada. Sem chave `serve` no recibo. Um
  leitor só: `scan`, não `play` nem `next`.
  `executed` ausente do recibo.
- `invite.scope` nomeia o bind se o serve
  declara `HOST=127.0.0.1 prende o bind`. Sem
  o marcador, a frase some. Bind no disco
  não é alguém de fora. Sem chave `HOST` no
  recibo. Um leitor só: `invite`, não `play`
  nem `playtest` nem `next` nem `ship`.
  `outsider` falso.
  `invite.scope` nomeia as sessões se a
  receita declara `duas sessões reais`. Sem
  o marcador, a frase some. Endereço no
  disco não é duas sessões. Sem chave
  `sessões` no recibo. Sem nomear em
  `play` / `playtest` / `next` / `ship` /
  `feel`. `outsider` falso.
- `template.scope` nomeia a publicação se o
  molde declara `não autoriza publicar` ou
  `não concedida neste template`. Sem o
  marcador, a frase some. Molde no disco
  não é autorização. Sem chave `publicar` no
  recibo. Um leitor só: `template`, não
  `finish` nem `next` nem `ship`. `agents`
  não ganha a frase. `elsewhere` falso.
- `documentation.scope` nomeia o audit se
  `document_minimum` e o roteiro declara o
  pedido sem consentimento. Sem o marcador,
  a frase some. Roteiro no disco não é base
  escrita. Sem chave `audit` no recibo
  nested. Um leitor só: `documentation`,
  não `scan` nem `next` nem `template`.
  `executed` falso.
- `continuity.scope` nomeia a PoC se
  `process.md` declara `Documentos prontos
  não significam PoC executada`. Sem o
  marcador, a frase some. Fonte no disco
  não é jogo implementado. Sem chave
  `process` no recibo. Um leitor só:
  `continuity`, não `documentation` nem
  `scan` nem `next`. `executed` falso.
- `agent_context.scope` nomeia o AAA se
  `AGENTS.md` declara `Não chame o recorte
  de AAA`. Sem o marcador, a frase some.
  Memória no disco não é acabamento. Sem
  chave `agents` no recibo. Sem chave
  `aaa`. Um leitor só: `agent_context`,
  não `scan.scope` nem `next` nem
  `template` nem `start`. `enough` e
  `consistent` ausentes.
- `finish.scope` nomeia o checklist se
  `aaa-checklist.md` declara `O harness
  não preenche o checklist`. Sem o
  marcador, a frase some. Guia no disco
  não é observação. Sem chave `checklist`
  no recibo. Um leitor só: `finish`, não
  `template` nem `next` nem
  `documentation` nem `agent_context`.
  `executed` falso.
- `production_bar.scope` nomeia a promoção
  se `production-bar.md` declara `Nenhum
  comando promove um jogo a um degrau`.
  Sem o marcador, a frase some. Guia no
  disco não é acabamento. Sem chave
  `promove` no recibo. Um leitor só:
  `production_bar`, não `bar` nem `next`
  nem `finish`. `assessed` falso.
- `packs.scope` nomeia o navegador se o
  pacote de plataforma declara `teste
  unitário não prova comportamento no
  navegador`. Sem o marcador, a frase
  some. Pacote no disco não é
  comportamento no aparelho. Sem chave
  `navegador` no recibo. Um leitor só:
  `packs`, não `verify` nem `next` nem
  `play` nem `discover`. `verified`
  ausente.
- `next.scope` nomeia a ação se
  `process.md` declara `uma ação
  recomendada`. Sem o marcador, a frase
  some. Proposta no disco não é
  autorização. Sem chave `ação` no
  recibo. Um leitor só: `next`, não
  `continuity` nem `documentation` nem
  `finish` nem `scan`. `executed` falso.
- `proposal.scope` nomeia a criação se
  `preproduction.md` declara `não
  preenche design`. Sem o marcador, a
  frase some. Proposta no disco não é
  pasta criada. Sem chave `criação` no
  recibo. Um leitor só: `proposal`, não
  `next.scope` nem `alternatives` nem
  `context.scope` nem `guide` nem
  `init`. `executed` falso.
- `record.scope` nomeia a medição se
  `quality.md` declara `O harness não
  os mede`. Sem o marcador, a frase
  some. Recibo no disco não é
  observação. Sem chave `mede` no
  recibo. Um leitor só: `record`, não
  `verify` nem `budget` nem `next` nem
  `production_bar` nem `feel`.
  `measured` ausente.
- `attachments[n].scope` do `record` nomeia a
  animação se `quality.md` declara
  `não comprova animação`. Sem o
  marcador, a frase some. Anexo no
  disco não é controle. Sem chave
  `animação` no recibo. Um leitor
  só: o anexo, não `record.scope` nem
  o passo de gravar nem `feel` nem
  `next`. `felt` e `observed` falsos.
- `palettes[n].scope` do `art` nomeia a
  paleta se `game-design-system.md`
  declara `não é uma paleta
  compartilhada`. Sem o marcador, a
  frase some. Lista no disco não é
  contrato. Sem chave `paleta` no
  recibo. Um leitor só: o item da
  paleta, não `art.scope` nem
  `art_direction` nem `scan.scope`
  nem `next`. `consistent` falso.
- `skill_targets[n].scope` do `doctor`
  nomeia o publisher se `SKILL.md`
  declara `não tier de publisher`.
  Sem o marcador, a frase some.
  Atalho no disco não é orçamento.
  Sem chave `publisher` no recibo.
  Um leitor só: o atalho, não
  `doctor.scope` nem `then` nem
  `guide` nem `init` nem `next`.
  `executed` falso.
- `roles[n].scope` nomeia a quantidade
  se `audio.md` declara `não é
  quantidade de arquivos`. Sem o
  marcador, a frase some. Lista no
  disco não é mix. Sem chave
  `quantidade` no recibo. Um leitor
  só: o item do papel, não
  `roles.scope` nem `roles --fill`
  nem `feel` nem `next`. `heard`
  falso.
- `areas.*.candidates[n].scope` do `scan`
  nomeia as intenções se
  `project-audit.md` declara `não
  comprova intenções autorais`. Sem
  o marcador, a frase some. Candidato
  no disco não é autoria. Sem chave
  `intenções` no recibo. Um leitor
  só: o candidato, não `scan.scope`
  nem `audit` nem `coverage` nem
  `documentation` nem `next`.
  `executed` falso.
- `options[n].scope` do `access` nomeia a
  certificação se `gates-research.md`
  declara `não é gate de
  certificação`. Sem o marcador, a
  frase some. Opção no disco não é
  certificação. Sem chave
  `certificação` no recibo. Um
  leitor só: o item da opção, não
  `access.scope` nem `gate` nem
  `verify` nem `next`. `verified`
  falso.
- `observations[n].scope` do `feel` nomeia o
  autor se `feel.md` declara `autor
  sugerido no comando não é quem
  jogou`. Sem o marcador, a
  frase some. Recibo no disco não é
  sessão. Sem chave
  `autor` no recibo. Um
  leitor só: o item da observação, não
  `feel.scope` nem `note` nem
  `playtest` nem `record` nem `next`.
  `felt` falso.
- `rains[n].scope` do `art` nomeia o
  volume se `visual.md` declara `Mesa
  no disco não é volume`. Sem o
  marcador, a frase some. Lista no
  disco não é comparação. Sem chave
  `volume` no recibo. Um
  leitor só: o item da chuva, não
  `art.scope` nem `art_direction` nem
  `scan` nem `content` nem `next`.
  `consistent` falso.
- `gates[n].criteria[n].scope` do `gate`
  nomeia a dispensa se `gates.md`
  declara `não é dispensável`. Sem o
  marcador, a frase some. Linha no
  disco não é passagem. Sem chave
  `dispensa` no recibo. Um
  leitor só: o critério, não
  `gate.scope` nem `gates[n]` nem
  `next` nem `check-plan` nem `craft`.
  `granted` falso.
- `constants[n].scope` do `feel` nomeia o
  universal se `feel.md` declara `não
  constantes universais`. Sem o
  marcador, a frase some. Número no
  disco não é lei. Sem chave
  `universais` no recibo. Um
  leitor só: o item da constante, não
  `feel.scope` nem `observations` nem
  `note` nem `next`.
  `felt` falso.
- `constants[n].scope` do `feel` nomeia a
  posição se `feel.md` declara `não
  prova que a posição foi integrada`.
  Sem o marcador, a frase some. Número
  no disco não é a pose. Sem chave
  `posição` no recibo. Um leitor só:
  o item da constante, não `feel.scope`
  nem `observations` nem `note` nem
  `playtest` nem `next`.   `felt` falso.
- `packs.platform.scope` nomeia os
  quadros se `web.md` declara `não
  comprovam quadros apresentados pela
  GPU`. Sem o marcador, a frase some.
  Callback no disco não é quadro
  apresentado. Sem chave `quadros` no
  recibo. Um leitor só: a plataforma,
  não `packs.scope` nem o gênero nem
  `context.scope` nem `next` nem
  `play`. `measured` falso.
- `problems[n].scope` do `bar` nomeia a
  dimensão se `production-bar.md`
  declara `não é uma das dez`. Sem o
  marcador, a frase some. Linha no
  disco não é acabamento. Sem chave
  `dimensão` no recibo. Um
  leitor só: o problema, não
  `bar.scope` nem `dimensions[n]` nem
  `production_bar` nem `next`.
  `assessed` falso.
- `problems[n].scope` do `gate` nomeia o
  escopo se `gates.md` declara `Fora
  de escopo não é dispensa`. Sem o
  marcador, a frase some. Linha no
  disco não é passagem. Sem chave
  `escopo` no recibo. Um
  leitor só: o problema, não
  `gate.scope` nem `gates[n]` nem
  `criteria[n]` nem `next` nem
  `check-plan` nem `craft`.
  `granted` falso.
- `problems[n].scope` do `origins` nomeia
  os rótulos se `gates.md` declara
  `Sidecar sem os três rótulos`
  (`\s+`). Sem o
  marcador, a frase some. Recibo no
  disco não é licença. Sem chave
  `rótulos` no recibo. Um
  leitor só: o problema, não
  `origins.scope` nem `provenance` nem
  `scan` nem `gate` nem `next`.
  `granted` e `validated` falsos.
- `problems[n].scope` do `craft` nomeia a
  definição se `observable-criteria-research.md`
  declara `sem definição declarada não é
  critério`. Sem o marcador, a frase
  some. Pesquisa no disco não é
  ofício observado. Sem chave
  `definição` no recibo. Um
  leitor só: o problema, não
  `craft.scope` nem `checks[n]` nem
  `gate` nem `next` nem `bar`.
  `observed` e `granted` falsos.
- `checks[n].scope` do `doctor` nomeia a
  ausência se `sources.md` declara
  `não é evidência negativa` (`\s+`).
  Sem o marcador, a frase some. Lista
  no disco não é laboratório. Sem
  chave `ausência` no recibo. Um
  leitor só: o check, não
  `doctor.scope` nem `then` nem
  `skill_targets` nem `next` nem
  `guide` nem `init`.
  `executed` ausente.
- `sources[n].scope` do continuity nomeia a
  fila se `process.md` declara
  `sources_found não comprova fila
  atual` (`\s+`). Sem o marcador, a
  frase some. Fonte no disco não é
  backlog. Sem chave `fila` no
  recibo. Um leitor só: o item da
  fonte, não `continuity.scope` nem
  `documentation` nem `next` nem
  `check-plan` nem
  `scan.continuity_sources`.
  `executed` falso.
- `genre_mentions[n].scope` nomeia a
  mecânica se `sources.md` declara
  `mecânica obrigatória`. Sem o
  marcador, a frase some. Campo no
  disco não é regra do jogo. Sem
  chave `mecânica` no recibo. Um
  leitor só: o item da menção, não
  `packs.genre.scope` nem
  `packs.scope` nem `context.scope`
  nem `next` nem
  `packs.genre.mentions`.
  Nomear não classifica.
- `issues[n].scope` da coverage nomeia o
  acidente se `sources.md` declara
  `não é acidente`. Sem o
  marcador, a frase some. Recorte no
  disco não é falha. Sem chave
  `acidente` no recibo. Um
  leitor só: o item do issue, não
  `coverage.scope` nem `scan.scope`
  nem `audit` nem `next` nem
  `context.scope`.
  Nomear não inventaria.
- `non_current_documents[n].scope` nomeia as
  linhas se `preproduction.md` declara
  `preencher linhas não certifica o jogo`.
  Sem o marcador, a frase some. Documento
  no disco não é o jogo. Sem chave
  `linhas` no recibo. Um leitor só: o
  rascunho, não `coverage.scope` nem
  `scan.scope` nem `issues[n]` nem
  `audit` nem `next` nem
  `context.scope`.
  Nomear não certifica.
- `check-plan.scope` nomeia o mérito se
  `process.md` declara `não garantem
  mérito`. Sem o marcador, a frase
  some. Forma no disco não é
  adequação. Sem chave `mérito` no
  recibo. Um leitor só: `check-plan`,
  não `next` nem `continuity` nem
  `record` nem `documentation`.
  `verified` ausente.
- `metadata_issues[n].scope` nomeia o
  semântico se `preproduction.md`
  declara `não é validador semântico de
  PRD/GDD`. Sem o marcador, a frase
  some. Parse no disco não é o jogo.
  Sem chave `semântico` no recibo. Um
  leitor só: o issue, não
  `check-plan.scope` nem `context.scope`
  nem `next`. Nomear não valida.
- `verify.scope` nomeia a criatividade
  se `preproduction.md` declara `não
  aprova criatividade`. Sem o
  marcador, a frase some. Recibo
  verde não é aprovação. Sem chave
  `criatividade` no recibo. Um leitor
  só: `verify`, não `record` nem
  `check-plan` nem `next` nem
  `template`. `verified` ausente.
- `capabilities_scope` nomeia a
  verificação se `process.md` declara
  `claimed` não é `verified`. Sem o
  marcador, a frase some. Alegação no
  disco não é cobertura. Sem chave
  `verified` no recibo. Um leitor só:
  `capabilities_scope`, não
  `verify.scope` nem `record` nem
  `next` nem `check-plan`. Status
  continua `claimed`.
- `capabilities[n].scope` do `verify`
  nomeia o suporte se
  `architecture.md` declara `registro
  declarado não prova suporte real`.
  Sem o marcador, a frase some.
  Registro no disco não é o
  consumidor. Sem chave `suporte` no
  recibo. Um leitor só: o item da
  capacidade, não `capabilities_scope`
  nem `verify.scope` nem
  `commands[n]` nem a área de
  arquitetura nem `next`.
  `verified` ausente. Status continua
  `claimed`.
- o contrato do `gauntlet` nomeia o
  infinito se `gauntlet.md` declara
  `não significa prazo infinito`. Sem
  o marcador, a frase some. Contrato
  no disco não é o orçamento. Sem
  chave `infinito` no recibo. Um
  leitor só: o contrato, não o
  recibo do `--output` nem
  `continuity.prompt` nem
  `continuity.scope` nem `next`.
  `execution_started` continua falso.
- `coverage.limits.scope` nomeia a
  prioridade se `project-audit.md`
  declara `não toma a prioridade`.
  Sem o marcador, a frase some.
  Limite no disco não é a base. Sem
  chave `prioridade` no recibo. Um
  leitor só: os limites, não
  `coverage.scope` nem `scan.scope`
  nem `audit` nem `context.scope`
  nem `next`. Nomear não observa.
- `template.scope` do MVP nomeia o
  valor se `preproduction.md` declara
  `não prova que sua hipótese de
  valor`. Só na etapa `mvp`. Sem o
  marcador, a frase some. Molde no
  disco não é validação. Sem chave
  `valor` no recibo. Um leitor só: o
  template do MVP, não `brief` nem
  `aaa` nem `finish` nem `context`
  nem `next` nem `verify`.
  `verified` ausente.
- `template.scope` da vertical-slice
  nomeia o acabamento se
  `preproduction.md` declara `não
  certificam o acabamento`. Só na
  etapa `vertical-slice`. Sem o
  marcador, a frase some. Molde no
  disco não é a fatia. Sem chave
  `acabamento` no recibo. Um leitor
  só: o template da slice, não `mvp`
  nem `aaa` nem `finish` nem
  `context` nem `next` nem `verify`.
  `verified` ausente.
- `git.scope` nomeia a leitura se
  `process.md` declara `prova
  identidade, não leitura`. Sem o
  marcador, a frase some. Identidade
  no disco não é inspeção. Sem chave
  `leitura` no recibo. Um leitor só:
  `git`, não `verify.scope` nem
  `next` nem `documentation` nem
  `scan`. `verified` ausente.
- `doctor.then` nomeia o exemplo se
  o README declara a frase de
  `START_IDEA_EXAMPLE`. Sem o
  marcador, cola `<fantasia>`.
  Frase no then não é pasta
  criada. Sem chave `exemplo` no
  recibo. Um leitor só: `doctor`,
  não `next` nem `guide.scope` nem
  `play` nem `git`. Nomear não
  cria. `ready` continua python /
  framework / root.
- `version.scope` nomeia o julgamento se
  `quality.md` declara `não substitui
  o julgamento`. Sem o marcador, a
  frase some. Identidade no disco
  não é avaliação. Sem chave
  `julgamento` no recibo. Um leitor
  só: `version`, não `record.scope`
  nem `verify.scope` nem `git` nem
  `next`. `verified` ausente.
- `roles --fill.scope` nomeia o reuso
  se `process.md` declara `não é
  automaticamente reutilizável`. Sem
  o marcador, a frase some. Arquivo
  no disco não é licença. Sem chave
  `reuso` no recibo. Um leitor só:
  `roles --fill`, não `roles` nem
  `origins` nem `next` nem `record`.
  `heard` falso.
- `audit.scope` nomeia o daemon se
  `project-audit.md` declara `não é
  um daemon nem um hook`. Sem o
  marcador, a frase some. Roteiro
  no disco não é interceptação.
  Sem chave `daemon` no recibo.
  Sem chave `hook`. Um leitor só:
  `audit`, não `documentation` nem
  `scan.scope` nem `next`.
  `executed` falso.
- `context.scope` nomeia o progresso se
  `process.md` declara `não certifica
  progresso`. Sem o marcador, a
  frase some. Contexto no disco
  não é degrau. Sem chave
  `progresso` no recibo. Um leitor
  só: `context`, não
  `production_bar` nem `finish`
  nem `template` nem `next`.
  `executed` falso.
- `studio_assets.sfx.scope` nomeia a escuta se
  `sources.md` declara `não ouve o
  starter`. Sem o marcador, a
  frase some. Acervo no disco
  não é mix ouvida. Sem chave
  `ouve` no recibo. Um leitor
  só: `studio_assets`, não
  `roles` nem `context.scope`
  nem `next`.   `heard` ausente.
- `areas.art_direction.scope` nomeia os tokens se
  `game-design-system.md` declara `não
  certifica tokens`. Sem o
  marcador, a frase some.
  Documento no disco não é
  aprovação artística. Sem chave
  `tokens` no recibo. Um leitor
  só: `art_direction`, não
  `scan.scope` nem `art` nem
  `next`.   `consistent` ausente.
- `areas.architecture.scope` nomeia as dependências se
  `architecture.md` declara `não infere
  dependências`. Sem o marcador, a
  frase some. Receita no disco
  não é decisão. Sem chave
  `dependências` no recibo. Um
  leitor só: `architecture`, não
  `scan.scope` nem `art_direction`
  nem `context.scope` nem `next`.
- `areas.provenance.scope` nomeia a licença se
  `gates.md` declara `recibo presente
  não é licença`. Sem o marcador, a
  frase some. Área no disco não é
  concessão. Sem chave `licença` no
  recibo. Um leitor só: `provenance`,
  não `origins` nem `scan.scope` nem
  `gate` nem `next` nem
  `art_direction` nem `architecture`.
  `granted` e `validated` falsos.
- `areas.qa.scope` nomeia as pessoas se
  `quality.md` declara `não prescreve
  quantas pessoas`. Sem o marcador, a
  frase some. Área no disco não é
  censo. Sem chave `pessoas` no
  recibo. Um leitor só: `qa`, não
  `playtest` nem `record` nem
  `scan.scope` nem `next` nem
  `provenance`. `outsider` falso.
- `projects[n].scope` do `discover` nomeia a
  qualidade se `preproduction.md` declara
  `não comprova qualidade`. Sem o
  marcador, a frase some. Conta no
  disco não é acabamento. Sem chave
  `qualidade` no recibo. Um leitor
  só: o item do projeto, não
  `review.scope` nem `scan.scope` nem
  `documentation` nem `next`.
  `verified` ausente.
- `coverage.scope` nomeia a inexistência se
  `project-audit.md` declara `não
  equivale a conteúdo inexistente`.
  Sem o marcador, a frase some.
  Contagem no disco não é
  inventário. Sem chave
  `inexistente` no recibo. Um
  leitor só: `coverage`, não
  `scan.scope` nem `art_direction`
  nem `architecture` nem `audit`
  nem `next`.
- `packs.platform.scope` nomeia a capacidade se
  `packs/README.md` declara `não
  certifica capacidade`. Sem o
  marcador ou sem kind, a frase
  some. Pacote no disco não é
  comportamento. Sem chave
  `capacidade` no recibo. Um
  leitor só: `platform`, não
  `packs.scope` nem `next` nem
  `play` nem `context.scope`.
- `packs.genre.scope` nomeia a extração se
  `sources.md` declara `Não são
  extração de repositório`. Sem o
  marcador ou sem `--genre`, a
  frase some. Convenção no disco
  não é repositório executado.
  Sem chave `extração` no recibo.
  Um leitor só: `genre`, não
  `packs.scope` nem `platform`
  nem `next` nem `play` nem
  `context.scope`.
- `capabilities[nome].scope` nomeia a API se
  `lifecycle.md` declara `não uma
  API implementada` e o nome foi
  mencionado. Sem o marcador ou
  sem menção, a frase some.
  Vocabulário no disco não é
  runtime. Sem chave `api` no
  recibo. Um leitor só: a
  capacidade mencionada, não
  `capabilities_scope` nem
  `context.scope` nem `next` nem
  o nome desconhecido.
- `capabilities[nome].scope` desconhecido
  nomeia o determinismo se
  `production-bar.md` declara
  `Determinismo não é uma capacidade`.
  Sem o marcador, a frase some. Lista
  no disco não é ciclo demonstrado.
  Sem chave `determinismo` no recibo.
  Um leitor só: o item desconhecido,
  não a menção nem
  `capabilities_scope` nem
  `context.scope` nem `next` nem
  `production_bar` nem `bar`.
  Nomear não prova.
- `steps[1].scope` nomeia o onboarding se
  `quality.md` declara `não é
  onboarding`. Sem o marcador, a
  frase some. Texto no disco não
  é a primeira ação. Sem chave
  `onboarding` no recibo. Um
  leitor só: o passo de jogar,
  não `guide.scope` nem
  `play.scope` nem `next` nem
  os passos 1 e 3.
- `steps[2].scope` nomeia o screenshot se
  `feel.md` declara `Screenshot
  não comprova feel`. Sem o
  marcador, a frase some. Recibo
  no disco não é peso percebido.
  Sem chave `screenshot` no
  recibo. Um leitor só: o passo
  de gravar, não `feel.scope`
  nem `note` nem `guide.scope`
  nem `play.scope` nem `record`
  nem `playtest` nem `next` nem
  o passo de jogar.
- `gates[n].scope` nomeia o silêncio se
  `gates.md` declara `silêncio não é
  aprovação`. Sem o marcador, a
  frase some. Linha vazia no disco
  não é passagem. Sem chave
  `silêncio` no recibo. Um leitor
  só: o item do `gate`, não
  `gate.scope` nem `next` nem
  `check-plan` nem `craft`.
  `granted` falso.
- `gates[n].scope` do close nomeia a
  hipótese se `preproduction.md`
  declara `não prova hipótese
  criativa`. Só no gate `close`.
  Sem o marcador, a frase some.
  Linha no disco não é o
  experimento. Sem chave
  `hipótese` no recibo. Um leitor
  só: o item do close, não
  `design` nem `evaluate` nem
  `gate.scope` nem o critério nem
  o `template` poc nem `verify`
  nem `next` nem `context`.
  `verified` ausente.
- `gates[n].scope` do deliver nomeia o
  lançamento se `creative-workflow.md`
  declara `não significa lançamento`.
  Só no gate `deliver`. Sem o
  marcador, a frase some. Linha no
  disco não é outra máquina. Sem
  chave `lançamento` no recibo. Um
  leitor só: o item do deliver, não
  `close` nem `gate.scope` nem o
  critério nem o `template` release
  nem `ship` nem `next` nem
  `verify`. `verified` ausente.
- `steps[0].scope` nomeia a abertura se
  `process.md` declara `Nomear o
  comando não abre`. Sem o
  marcador, a frase some. Nome
  no disco não é partida. Sem
  chave `abertura` no recibo. Um
  leitor só: o passo de abrir,
  não `guide.scope` nem
  `play.scope` nem `start.scope`
  nem `init` nem `next` nem os
  passos de jogar e gravar.
  `executed` ausente; `done`
  continua o destino.
- `checks[n].scope` do `craft` nomeia a
  escada se `observable-criteria-research.md`
  declara `não é uma escada`. Sem o
  marcador, a frase some. Pesquisa
  no disco não é ofício observado.
  Sem chave `escada` no recibo. Um
  leitor só: o item do `craft`, não
  `craft.scope` nem `gate` nem
  `next` nem `bar`. `observed` e
  `granted` falsos.
- `dimensions[n].scope` do `bar` nomeia
  os prazos se `production-bar.md`
  declara `Degraus não são prazos`.
  Sem o marcador, a frase some.
  Linha no disco não é calendário.
  Sem chave `prazos` no recibo. Um
  leitor só: o item do `bar`, não
  `bar.scope` nem
  `production_bar.scope` nem `next`
  nem `context.scope`.   `assessed`
  falso.
- `then.scope` do `doctor` nomeia o
  motor se `ambition.md` declara
  `não é um motor AAA`. Sem o
  marcador, a frase some. Convite
  no then não é runtime. Sem
  chave `motor` no recibo. Um
  leitor só: `then`, não
  `doctor.scope` nem `init` nem
  `guide` nem `next`. `executed`
  falso.   Sem `then` o laboratório
  já tem jogo ou falta starter.
- `alternatives[n].scope` nomeia a
  fabricação se `process.md` declara
  `não fabrique uma tarefa`. Sem o
  marcador, a frase some. Lista no
  disco não é backlog. Sem chave
  `fabricação` no recibo. Um leitor
  só: a alternativa, não
  `proposal` nem `next.scope` nem
  `check-plan` nem `context.scope`.
  `executed` falso.
- `commands[n].scope` do `verify` nomeia a
  diversão se `ambition.md` declara
  `não comprova diversão`. Sem o
  marcador, a frase some. Log no
  disco não é experiência. Sem chave
  `diversão` no recibo. Um leitor
  só: o item do comando, não
  `verify.scope` nem
  `capabilities_scope` nem `record`
  nem `next` nem `doctor.then`.
  `verified` ausente.
  `experience_status` continua
  `not_assessed`.
- `commands[n].scope` do `verify` nomeia o
  significado se `delivery.md` declara
  `não comprova seu significado`. Sem
  o marcador, a frase some. Hash no
  disco não é o critério. Sem chave
  `significado` no recibo. Um leitor
  só: o item do comando, não
  `verify.scope` nem `git` nem o
  anexo do `record` nem `next`.
  `experience_status` continua
  `not_assessed`.
- `cycle.scope` nomeia o livre se
  `feel.md` declara `não prova estar
  livre para atacar`. Sem o
  marcador, a frase some. Estado no
  disco não é a janela. Sem chave
  `livre` no recibo. Não entra em
  `CYCLE_KEYS`. `starter_cycle` cru
  continua sem `scope`. Um leitor
  só: o ciclo do `start` / `play` /
  `guide` / `init`, não `feel.scope`
  nem `guide.scope` nem `play.scope`
  nem `start.scope` nem `next`.
  `felt` e `executed` falsos.
- `areas.architecture.candidates[n].scope` nomeia a
  compreendida se `architecture.md` declara
  `não significa … arquitetura compreendida`.
  Sem o marcador, a frase some. Candidato no
  disco não é a decisão. Sem chave
  `compreendida` no recibo. Um leitor só: o
  candidato da arquitetura, não
  `architecture.scope` nem os candidatos das
  outras áreas nem `scan.scope` nem `next`.
  `executed` ausente.
- `next.signals.scope` nomeia a conclusão se
  `architecture.md` declara `não comprovam
  conclusão nem aprovação`. Sem o
  marcador, a frase some. Sinal no disco
  não é o término. Sem chave `conclusão`
  no recibo. Um leitor só: o `signals` do
  `next`, não `next.scope` nem a proposta
  nem as alternativas nem o `signals` do
  `discover` nem `context.scope`.
  `executed` falso.
- `gauntlet` contrato nomeia a independência se
  `gauntlet.md` declara `não comprovam
  independência`. Sem o marcador, a
  frase some. Papel no disco não é
  crítico isolado. Sem chave
  `independência` no recibo. Um leitor
  só: o contrato, não o recibo do
  `--output` nem o `continuity.prompt`
  nem o `next` nem o `context`.
  `execution_started` falso.
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
  ensina pad, toque, dash, coleta, prática nem guarda.
- Não promover pacing/art/feel/a11y por convite, CSS, faixa, contorno,
  LAN, caption, marca de queda, botão de remap, panner, halo, vinheta,
  ponta, tela de título, chuva da porta, `gameSpeed` no disco, `hold` no stub,
  coil/windup no disco, `bank.windupTicks` no disco, `closeIntervalScale` no disco, `closeHazardScale` no disco, `closeBedRate` no disco, recorde no overlay do fim, aviso de guardar no fecho, `hint_hit` no disco, `hint_practice` no disco, pulso do corpo na graça, copiar ou gravar o achado, last-run,
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
  ou um painel que pinta a lacuna no boot e some o que o fetch trouxe
  ou um hitstop que queima o perdão do avanço
  ou um hold que some o relógio da porta e o campo repete o ensino
  ou uma região viva que some o aviso do primeiro ciclo
  ou um knob de escala que cresce o canvas e some a casca
  ou um recado que dispara o verbo
  ou um toque que sai do campo e deixa o corpo andando
  ou um look que veste o canvas e some o select
  ou uma outra aba que some as preferências desta página
  ou um JSON que lista o arquivo e declara sem origem
  ou uma tecla do remap que dispara o verbo
  ou um botão focado que ativa e avança
  ou um verify que some o stem que o recibo já nomeia
  ou uma faixa que some a curva que o last-run já traçou
  ou uma sessão que some o look e o relógio que o convite já lê
  ou um ciclo que some o relógio que o jogo já lê
  ou um banner do serve que some o relógio que o jogo já lê
  ou uma página de escuta que oferece o player do som que o disco perdeu
  ou um convite que grava o look, a chuva ou o relógio que só vestiu
  ou uma query de chuva que retoma o hold de outra mesa
  ou uma pausa que o toque não retoma
  ou uma porta que ensina Espaço no telefone
  ou uma porta que chama o tap de cima
  ou um `finding_href` que aponta um painel escondido
  ou uma pausa que cala o reinício que o comando já faz
  ou uma região viva que cala como sair da pausa
  ou uma pausa que ensina Esc no telefone
  ou um `next` unstructured que aponta o serve nu
  ou uma porta que cala a seed nova no telefone
  ou uma região viva que cala como abrir a porta
  ou um `feel` que cala a seed do last-run
  ou um telefone que só retoma e não pausa
  ou um `playtest` que cala a url do achado
  ou um relógio que cala a pausa
  ou um Copiar que cala o destino
  ou uma memória que cala o playtest
  ou um MDA que cala a porta
  ou uma região viva que cala a lacuna do som
  ou um aviso que some a prática enquanto o campo já
  contorna a janela orbe-só
  ou uma intenção que some o perigo que o `--as` já preserva
  ou um `brief` que come a folga da guarda
  ou um corpo na recuperação do dash que veste a tinta da prática
  ou um `feel` que cala as janelas da chuva que o campo já marca
  ou uma prática que acaba e chama orbe de chuva que começa
  ou uma folga que acaba e chama chuva que volta
  ou um `next` do feel que cala o candidato que o `then.note` já anexa
  ou um rastro do dash que veste o descanso
  ou um coil do dash que veste o descanso
  ou um coil do dash que veste a corrente e cala o rumo
  ou um feel que cala o corpo que a porta já desloca
  ou um content que lista dusk e calm e cala o par
  ou um ship que cala o tamanho que a receita já relata
  ou um access que cala o contraste que a receita já amostra
  ou um roles que cala a soma que a receita já relata
  ou um achado copiado que cala o last-run simulado
  ou um canvas da porta que cala a lacuna do som
  ou um `-h` que lista init antes de start
  ou um coil da guarda que veste o descanso
  ou uma porta que chove meio a meio e cala o risco da mesa
  ou um compromisso da guarda que veste o descanso
  ou um `art` que cala o risco da chuva que a porta já lê
  ou um `sfx export` que trata o stem perdido como id desconhecido
  ou um rótulo do dash que diz recarregando no travel
  ou um `sfx verify` que despeja errno do som que o catálogo perdeu
  ou uma região viva que cala a mesa e o look que a porta já veste
  ou um `feel` que cala o rumble que a tabela já lista.
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

- `CYCLE_KEYS` inclui `door` depois de `verb`, `seed` depois de
  `mood` e `speed` depois de `seed`. `cycle_line` nomeia `Fantasia:`
  antes de `Verbo:` quando há frase (`--idea` ou `copy.json`),
  `Porta:` antes de `Mover`, `Seed:` antes de `Relógio:` e
  `Relógio:` antes de `Convite`. Fantasia não entra em `CYCLE_KEYS`.
  A frase não muda o verbo. Sem frase a linha some.
- `cycle.scope` nomeia o livre se `feel.md`
  declara `não prova estar livre para
  atacar`. Sem o marcador, a frase some.
  Estado no disco não é a janela. Sem
  chave `livre`. Não entra em
  `CYCLE_KEYS`. `starter_cycle` cru
  continua sem `scope`.
- `CRAFT_EXAMPLES` ordem: pair → look → table → sfx. Look e chuva do
  exemplo compartilham o nome `noite`.
- `play` após `start` é `cd … && npm run serve`. Se o
  `package.json` tem dependências e `node_modules` falta,
  `then.install` nomeia `cd … && npm install`. Sem
  dependências a chave some. Nomear não instala. Não
  dobrar o install no `play`. O `feel` não ganha a chave.
- `start` não planta os rascunhos (`documents=False`). CLI `--docs`
  opta; `--no-docs` permanece e é o padrão. `init` continua
  plantando. `--idea` entra em `data/copy.json`; brief só com `--docs`.
  Os dois escrevem `AGENTS.md` com o comando que abre, o `note`,
  o `playtest` e o que o disco ainda não tem. Sem rascunhos a
  memória não lista GDD. O `playtest` só lê. Sem os quatro não
  é achado. Nomear o leitor não observa. O prompt de
  `start` / `play` / `guide` / `init` nomeia o mesmo
  `playtest`. Sem `then.playtest`. O passo 3 continua `note`.
  `len(steps) == 3` permanece. `template agents` e o
  `next` em `agent_context.not_located` geram o mesmo texto a
  partir do disco — play, url, note, playtest, fantasia,
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
  `ready`, `then.guide` é `guide --idea` com o exemplo que o
  README já imprime. Sem o marcador, cola `<fantasia>`. Sem a
  frase a raiz recusa. Com jogo, sem starter ou bloqueado,
  `then` é nulo. Sem `prompt` — o CLI não escreve stderr. O
  aviso de starter ausente nomeia `start --idea`, não `init`.
  Sem chave `exemplo`. Nomear não cria. Não cria e não executa.
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
  `start.scope` nomeia o par se o `tools/new-pair.*` nasce
  look e chuva. Sem o marcador, a frase some. Ferramenta
  no disco não é alguém de fora. Sem chave `pair` no
  recibo. Sem nomear `pair` no `art` nem extra no
  `content.scope`. `enough` falso.
  O `then` do `start` nomeia a experiência se
  `create.md` declara `não demonstram uma
  experiência nova`. Sem o marcador, a
  frase some. Nome no disco não é o ciclo
  jogado. Sem chave `experiência` no
  recibo. Um leitor só: `start.then`, não
  `play` nem `guide` nem `init` nem
  `feel.then`. `executed` falso.
  `guide` sem destino: `open` é o start. Na raiz do framework, sem
  `--idea`, o CLI recusa e o `sem destino` nomeia o `start --idea`
  do README — `guide_cycle(None)` continua o mapa. Nomear não cria.
  `guide.scope` nomeia o relógio se o manifesto
  declara `"speed": "`. Sem o marcador, a frase
  some. Frase no disco não é partida observada.
  Sem chave `speed` no recibo. Sem `then.speed`.
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
  não é achado. Se o disco tem last-run e o comando
  veio sem `--from-run`, o `note.scope` nomeia o
  arquivo. Sem o arquivo a frase some. Nomear não
  anexa. Sem chave `last_run`. Achar o jogo não
  sente, não assiste e não promove. `playtest` só lê.
  Sem os quatro campos, o recibo traz `finding_href`
  (`/?invite=1#finding` ou `/?invite=1&seed=<n>#finding`
  com os eixos — sem o convite o âncora some),
  `finding_open` (a url do serve com o convite, ou o
  mesmo endereço sem serve), `qa` se `docs/qa.md` existir,
  `form` (esqueleto canônico) e `fields`. Sem `then`. `next` em
  `playtest.unstructured` aponta o serve/`play`,
  o endereço do achado (`finding_open`: a url do
  serve com o convite, ou `finding_href` sem serve)
  e `note --field` dos quatro nomes — não relê `playtest`
  nem `feel` como se gravassem. O serve nu não abre
  o painel. Esqueleto no disco
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
  O `record` do `sfx copy` do acervo nomeia
  o consumido se `content.md` declara
  `não comprova que está sendo consumido`.
  Sem o marcador, a frase some. Recibo no
  disco não é mix. Sem chave `consumido`
  no recibo. Sem gravar `scope` no
  `sources.json`. Um leitor só: o `record`,
  não o `copy.scope` nem o stem local
  nem o `content` nem o `origins` nem o
  `next`. `heard` falso.
- `emit()` escreve `prompt` em stderr quando a chave existe e tem
  texto. stdout continua só o JSON. Falar a frase não executa.
  `next` / `doctor` / `feel` não têm `prompt` e não escrevem frase.
  `feel.then` tem `note` e, se o projeto declara o comando de
  abrir, `play`. Com last-run, `seed` e `invite` — os mesmos
  endereços do ciclo. Sem serve a chave some. Sem last-run,
  seed e invite somem. Não ganha `lost`.
  `feel.scope` nomeia rumble — as constantes já listavam
  `feel.rumble*`; o texto calava. Número no disco não é
  peso percebido. Com o traço no desenho, `feel.scope`
  nomeia o rumo que o coil do dash marca. Sem o
  marcador, a frase some. Traço no disco não é
  peso percebido. Sem chave `heading` no recibo.
  Com `function attractMove`, `feel.scope` nomeia
  o corpo que a porta desloca. Sem o marcador, a
  frase some. Pose no disco não é peso percebido.
  Sem chave `attract` no recibo.
  Com `function lookAhead`, `feel.scope` nomeia
  a inclinação que o quadro já marca. Sem o
  marcador, a frase some. Lean no disco não é
  peso percebido. Sem chave `lookAhead` no
  recibo. Sem `then.lookAhead`.
  Se o `tools/probe.*` exercita o perdão,
  `feel.scope` nomeia. Sem o marcador, a
  frase some. Conta no disco não é peso
  percebido. Sem chave `probe` no recibo.
  Sem `then.probe`.
  Se o laço declara `function landDash`,
  `feel.scope` nomeia o término. Sem o
  marcador, a frase some. Pose no disco
  não é peso percebido. Sem chave `land`
  no recibo. Sem `then.land`.
  `felt` falso.
  `save` relata `warned` / `warnings` se o disco tem
  `persistLine`, `title_volatile` ou `title_unsaved`. Nomear
  não é aba fechada. `trusted` falso. Sem `prompt`.
  `save.scope` nomeia a recuperação se o canvas pinta
  `settingsLine`. Sem o marcador, a frase some. A pausa
  não pinta. Texto no disco não é aba fechada. Sem
  chave `recovery` no recibo.
  `save.scope` nomeia o fechamento se o disco escuta
  `beforeunload`. Sem o marcador, a frase some. Gancho
  no disco não é aba fechada. Sem chave `beforeunload`
  no recibo. Sem chave `unload`.
  `trusted` falso.
  `access.scope` nomeia `:focus-visible` se a casca declara
  o outline. Sem o marcador, a frase some. Outline no
  disco não é sessão com o teclado. Sem chave `focus`
  no recibo. `access.scope` nomeia o contraste se o
  `tools/contrast.*` amostra o stub. Sem o marcador, a
  frase some. Stub no disco não é sessão com o modo
  ativo. Sem chave `contrast` no recibo.
  `access.scope` nomeia o perigo se o live anuncia
  `perigo à frente`. Sem o marcador, a frase some.
  Texto no DOM não é sessão. Sem chave `threat`
  no recibo. Sem chave `threatCue`.
  `access.scope` nomeia as teclas se o disco declara
  `paintCommands`. Sem o marcador, a frase some.
  Tabela no disco não é sessão. Sem chave `commands`
  no recibo. Sem outro remap na tabela.
  `access.scope` nomeia a legenda se a porta lê
  o que o mixer ainda guarda. Sem o marcador, a
  frase some. Texto no disco não é sessão. Sem
  chave `caption` no recibo.
  `verified` falso.
  `budget.scope` nomeia a porta (`title.attract`) se o
  `tools/budget.*` declara a cena. Sem o marcador, a
  frase some. Stub no disco não é dispositivo. Sem
  chave `door` no recibo. `budget.scope` nomeia os
  bytes se o `tools/size.*` declara sem teto. Sem o
  marcador, a frase some. Bytes no disco não são o
  quadro medido. Sem chave `size` no recibo. Sem
  nomear `playing.run`. `budget.scope` nomeia o
  percentil se o `tools/budget.*` relata a
  distribuição, não a média. Sem o marcador, a
  frase some. Relato no disco não é dispositivo.
  Sem chave `percentile` no recibo. Sem nomear
  `p99`. Sem limiar de quadro.
  `measured` falso.
  `content.scope` nomeia o par look+chuva se o disco
  declara `listMoods`. Sem o marcador, a frase some.
  Nome no disco não é volume. Sem chave `moods` no
  recibo. `content.scope` nomeia a mesa se o
  `tools/new-table.*` nasce o perfil. Sem o
  marcador, a frase some. Ferramenta no disco
  não é volume. Sem chave `table` no recibo.
  Sem nomear `pair`.
  `content.scope` nomeia a migração se o disco
  declara `function migrateTable`. Sem o
  marcador, a frase some. Arquivo no disco
  não é volume. Sem chave `migrate` no
  recibo. Sem chave `schema`. Sem nomear
  `pair`. `enough` falso.
  `content.scope` nomeia a composição se
  `content.md` declara `não prova
  composição natural`. Sem o
  marcador, a frase some. Arquivo
  no disco não é o mundo. Sem chave
  `composição` no recibo. Um leitor
  só: o `content`, não `art` nem
  `ship` nem `feel` nem o gate
  `scale` nem `next`. `enough`
  falso. `verified` ausente.
- `continuity.prompt.scope` nomeia a
  prontidão se `process.md` declara
  `não comprovam prontidão`. Sem o
  marcador, a frase some. Arquivo
  no disco não é o recorte. Sem
  chave `prontidão` no recibo. Um
  leitor só: o prompt, não
  `continuity.scope` nem as
  `sources` nem `documentation`
  nem `delivery_review` nem
  `context.scope` nem `next`.
  `executed` ausente.
  `art.scope` nomeia o look se o `tools/new-look.*`
  nasce a paleta. Sem o marcador, a frase some.
  Ferramenta no disco não é comparação em movimento.
  Sem chave `look` no recibo. Sem nomear `pair`.
  `art.scope` nomeia o trilho se o canvas declara
  `drawTelegraph`. Sem o marcador, a frase some.
  Marca no disco não é comparação em movimento.
  Sem chave `telegraph` no recibo. Sem chave `rail`.
  Sem nomear `pair`.
  `art.scope` nomeia a vinheta se o canvas
  declara `function drawVignette`. Sem o
  marcador, a frase some. Recorte no disco
  não é comparação em movimento. Sem chave
  `vignette` no recibo. Sem chave `halo`.
  Sem nomear `pair`.
  `consistent` falso.
  `ship.scope` nomeia o tamanho se o `tools/size.*`
  declara sem teto. Sem o marcador, a frase some.
  Bytes no disco não são outra máquina. Sem chave
  `size` no recibo. `ship.scope` nomeia o banner se
  o `tools/serve.*` nomeia a árvore exportada. Sem
  o marcador, a frase some. Banner no disco não é
  outra máquina. Sem chave `serve` no recibo.
  `ship.scope` nomeia o passo se o `tools/export.*`
  declara o empacote. Sem o marcador, a frase some.
  Empacotar no disco não é outra máquina. Sem chave
  `export` no recibo.
  `ship.scope` nomeia o file:// se o `tools/export.*`
  recusa o protocolo. Sem o marcador, a frase some.
  Recusar no disco não é outra máquina. Sem chave
  `file` no recibo.
  `tree.scope` do `ship` nomeia a
  identidade se `release.md` declara
  `Identidade do artefato não é outra
  máquina`. Sem o marcador, a frase
  some. Árvore no disco não é
  entrega. Sem chave `identidade` no
  recibo. Um leitor só: a árvore,
  não `ship.scope` nem `next` nem
  `play` nem `ship_tree` cru.
  `elsewhere` e `shipped` falsos.
  `artifact.scope` do `ship` nomeia o
  editor se `release.md` declara
  `Um teste no editor não demonstra o
  jogo exportado`. Sem o marcador, a
  frase some. Manifesto no disco não
  é o jogo exportado. Sem chave
  `editor` no recibo. Um leitor só:
  o artefato, não `ship.scope` nem
  `tree` nem `next` nem `play` nem
  `ship_artifact` cru.
  `elsewhere` e `shipped` falsos.
  `roles.scope` nomeia a soma se o `tools/mix.*` soma
  as vozes. Sem o marcador, a frase some. Soma no
  disco não é mix ouvida. Sem chave `mix` no recibo.
  `roles.scope` nomeia a voz se o `tools/design-sfx.*`
  desloca. Sem o marcador, a frase some. Arquivo no
  disco não é mix ouvida. Sem chave `sfx` no recibo.
  Sem nomear `peak`.
  `roles.scope` nomeia o PCM se o `tools/wav.*`
  lê o arquivo. Sem o marcador, a frase some.
  Bytes no disco não são mix ouvida. Sem
  chave `wav` no recibo. Sem chave `pcm`.
  Sem nomear `peak`. `heard` falso.
  `sfx info` nomeia o pico se o recibo
  já guarda `technical.peak_dbfs`. Sem o
  número, a chave some. Pico no recibo
  não é mix ouvida. Sem `rms`. Não
  mede de novo. `heard` falso.
  `sfx summary` nomeia o pico se o
  `tools/peak.*` relata o arquivo. Sem
  o marcador, a frase some. Relato no
  disco não é mix ouvida. Sem chave
  `peak` no recibo. Sem nomear `peak`
  no `roles`. `heard` falso.
  `sfx search` nomeia o deslocamento
  se o `tools/design-sfx.*` desloca a
  voz. Sem o marcador, a frase some.
  Arquivo no disco não é mix ouvida.
  Sem chave `sfx` no recibo. Sem
  nomear `peak`. Sem outra voz no
  `roles`. `heard` falso.
  `sfx verify` nomeia a integridade se
  o `audio.py` cruza hash e bytes.
  Sem o marcador, a frase some. Sem
  acervo a frase some. Hash no disco
  não é mix ouvida. Sem chave
  `sha256` no recibo. Sem chave
  `integridade`. Sem nomear `peak`.
  `heard` falso.
  `sfx export` do acervo nomeia o
  processamento se o `audio.py`
  recusa extra. Sem o marcador, a
  frase some. Sem acervo a frase
  some. Bytes no disco não são mix
  ouvida. Sem chave `processamento`
  no recibo. Sem chave `processing`.
  Sem nomear `sha256`. `heard` falso.
  `sfx export` do stem nomeia a
  invenção se a receita recusa que
  o export invente bytes. Sem o
  marcador, a frase some. Cópia no
  disco não é mix. Sem chave
  `invenção` no recibo. Sem nomear
  `processamento` no stem. `heard` falso.
  `sfx verify` `missing` nomeia o
  404 se a receita recusa que nomear
  o 404 seja mix. Sem o marcador, a
  frase some. Sem stem ausente a
  frase some. Lista no disco não é
  mix. Sem chave `404` no recibo.
  Sem nomear no `sfx summary`. `heard` falso.
  A opção `captions` do `access` nomeia
  o número se a receita recusa que o
  número na legenda seja mix. Sem o
  marcador, a frase some. Sem a opção
  a frase some. Número no disco não é
  mix. Sem chave `número` no recibo.
  Sem nomear no `access.scope`. `verified` falso.
  O papel do x do campo nomeia o
  panner se a receita recusa que o
  número no panner seja mix. Sem o
  marcador, a frase some. Sem o papel
  a frase some. Número no disco não é
  mix. Sem chave `panner` no recibo.
  Sem nomear no `roles.scope`. `heard` falso.
  O `roles` nomeia o retomar se a
  receita recusa que retomar, fila e
  paralelo sejam mix. Sem o
  marcador, a frase some. Pedido no
  disco não é mix. Sem chave `retomar`
  no recibo. Sem nomear no item do
  papel. `heard` falso.
  A opção `haptics` do `access` nomeia
  o controle se a receita recusa que o
  pulso seja sessão no controle. Sem o
  marcador, a frase some. Sem a opção
  a frase some. Pulso no disco não é
  sessão. Sem chave `controle` no
  recibo. Sem nomear no `access.scope`.
  `verified` falso.
  A opção `remap` do `access` nomeia o
  botão se a receita recusa que o
  botão seja sessão. Sem o marcador,
  a frase some. Sem a opção a frase
  some. Botão no disco não é sessão.
  Sem chave `botão` no recibo. Sem
  nomear no `access.scope`. `verified`
  falso.
  A opção `reduced_motion` do `access`
  nomeia a causa se a receita recusa
  que o movimento reduzido apague a
  causa. Sem o marcador, a frase some.
  Sem a opção a frase some. Causa no
  disco não é sessão. Sem chave
  `causa` no recibo. Sem nomear no
  `access.scope`. `verified` falso.
  A opção `high_contrast` do `access`
  nomeia o neutro se a receita recusa
  que o fundo neutro seja o pior caso.
  Sem o marcador, a frase some. Sem a
  opção a frase some. Neutro no disco
  não é sessão. Sem chave `neutro` no
  recibo. Sem nomear no `access.scope`.
  `verified` falso.
  A opção `colorblind` do `access`
  nomeia o ícone se a receita recusa
  que o estado dependa só da cor. Sem
  o marcador, a frase some. Sem a
  opção a frase some. Ícone no disco
  não é sessão. Sem chave `ícone` no
  recibo. Sem nomear no `access.scope`.
  `verified` falso.
  A opção `one_hand` do `access` nomeia
  a mão se a receita recusa que
  completar o jogo peça as duas mãos.
  Sem o marcador, a frase some. Sem a
  opção a frase some. Mão no disco não
  é sessão. Sem chave `mão` no recibo.
  Sem nomear no `access.scope`.
  `verified` falso.
  A opção `assist` do `access` nomeia
  o oculto se a receita recusa que a
  assistência esconda conteúdo. Sem o
  marcador, a frase some. Sem a opção
  a frase some. Oculto no disco não é
  sessão. Sem chave `oculto` no
  recibo. Sem nomear no `access.scope`.
  `verified` falso.
  A opção `game_speed` do `access`
  nomeia a precisão se a receita
  recusa que a precisão fique sem
  alternativa. Sem o marcador, a
  frase some. Sem a opção a frase
  some. Precisão no disco não é
  sessão. Sem chave `precisão` no
  recibo. Sem nomear no `access.scope`.
  `verified` falso.
  A opção `ui_scale` do `access` nomeia
  a tipografia se a receita recusa que
  a escala substitua a tipografia. Sem
  o marcador, a frase some. Sem a
  opção a frase some. Tipografia no
  disco não é sessão. Sem chave
  `tipografia` no recibo. Sem nomear
  no `access.scope`. `verified` falso.
  A opção `live` do `access` nomeia o
  leitor se a receita recusa que o
  overlay substitua o leitor. Sem o
  marcador, a frase some. Sem a opção
  a frase some. Overlay no disco não
  é sessão. Sem chave `leitor` no
  recibo. Sem nomear no `access.scope`.
  `verified` falso.
  `feel.scope` nomeia o sit se o laço
  atribui `bankWindup` a partir do
  windup. Sem o marcador, a frase some.
  Pose no disco não é peso percebido.
  Sem chave `bank` no recibo. Sem
  chave `sit`. Sem chave `windup`.
  `felt` falso.
  `playtest.scope` nomeia o recado se o
  `tools/serve.*` escuta `NOTE_ROUTE`.
  Sem o marcador, a frase some. Texto
  no disco não é alguém de fora. Sem
  chave `note` no recibo. Sem
  `then`. `outsider` falso.
  `candidate_tally.scope` nomeia o
  cinco se `observable-criteria-research.md`
  declara `"Cinco playtesters" não é
  critério`. Sem o marcador, a frase
  some. Conta no disco não é sessão
  observada. Sem chave `cinco` no
  recibo. Um leitor só: a conta, não
  `playtest.scope` nem `invite` nem
  `next` nem `note` nem `last_run_tally`
  cru. `observed` e `outsider` falsos.
  `candidate_curve.scope` nomeia o
  aperto se `recipes/content.md`
  declara `Aperto no disco não é
  curva observada`. Sem o marcador,
  a frase some. Número no disco não
  é sessão. Sem chave `aperto` no
  recibo. Um leitor só: a curva, não
  `playtest.scope` nem `content.scope`
  nem `candidate_tally` nem `invite`
  nem `next` nem `last_run_curve`
  cru. `observed` e `outsider` falsos.
  `conflicts[n].scope` do `bar` nomeia
  a precedência se `production-bar.md`
  declara `Duas linhas discordantes
  sobre a mesma dimensão não se
  resolvem por precedência`. Sem o
  marcador, a frase some. Linha no
  disco não é acabamento. Sem chave
  `precedência` no recibo. Um leitor
  só: o conflito, não `bar.scope` nem
  `problems[n]` nem `dimensions[n]`
  nem `production_bar` nem `next` nem
  `bar_declaration` cru. `assessed`
  falso.
  `sfx import.scope` nomeia a
  improvisação se `recipes/audio.md`
  declara `não autoriza improvisar
  licença`. Sem o marcador, a frase
  some. Importar no disco não é
  licença. Sem chave `improvisar` no
  recibo. Um leitor só: o import, não
  `sfx seed` nem `next` nem `summarize`
  nem `roles` nem `sfx copy`. `heard`
  falso.
  `sfx info` do stem nomeia o lixo se
  `recipes/audio.md` declara `sem papel
  e sem consumidor não é áudio`. Sem o
  marcador, a frase some. Arquivo no
  disco não é mix. Sem chave `lixo` no
  recibo. Um leitor só: a ficha do
  stem, não `local_stems` cru nem a
  ficha ausente nem o catálogo nem
  `summarize` nem `sfx search` nem
  `sfx import`. `heard` falso.
  `areas.runbook.scope` nomeia a
  telemetria se `recipes/release.md`
  declara `telemetria não é padrão
  silencioso`. Sem o marcador, a
  frase some. Área no disco não é
  consentimento. Sem chave `telemetria`
  no recibo. Um leitor só: o runbook,
  não `scan.scope` nem `qa` nem
  `architecture` nem `ship` nem
  `next`. `elsewhere` falso.
  `areas.decisions.scope` nomeia o
  histórico se `recipes/architecture.md`
  declara `histórico a regra vigente`.
  Sem o marcador, a frase some. Área
  no disco não é decisão atual. Sem
  chave `histórico` no recibo. Um
  leitor só: o decisions, não
  `scan.scope` nem `architecture` nem
  `runbook` nem `next`. `executed`
  falso.
  `areas.gdd.scope` nomeia o divertido
  se `references/preproduction.md`
  declara `isoladamente não basta`.
  Sem o marcador, a frase some. Área
  no disco não é o verbo. Sem chave
  `divertido` no recibo. Um leitor só:
  o gdd, não `scan.scope` nem
  `decisions` nem `mda` nem `feel` nem
  `next`. `felt` falso.
  `areas.mda.scope` nomeia a pontuação
  se `references/preproduction.md`
  declara `pontuação universal de
  diversão`. Sem o marcador, a frase
  some. Área no disco não é
  experiência. Sem chave `pontuação`
  no recibo. Um leitor só: o mda, não
  `scan.scope` nem `gdd` nem `feel` nem
  `verify` nem `next`. `felt` falso.
  `areas.vision.scope` nomeia o público
  se `references/preproduction.md`
  declara `público observado`. Sem o
  marcador, a frase some. Área no disco
  não é audiência. Sem chave `público`
  no recibo. Um leitor só: o vision, não
  `scan.scope` nem `gdd` nem `mda` nem
  `feel` nem `next`. `felt` falso.
  `scale_mentions[n].scope` nomeia o
  marketing se `references/ambition.md`
  declara `adjetivo de marketing`. Sem
  o marcador, a frase some. Campo no
  disco não é campanha. Sem chave
  `marketing` no recibo. `source` do
  `read_scale` continua `{path, line,
  value}`. Um leitor só: o item, não
  `read_scale.scope` nem `scan.scope`
  nem `vision` nem `context.scope` nem
  `next`. `felt` falso.
  `access.options[n].scope` nomeia a
  opção se `recipes/accessibility.md`
  declara `sem consumidor no código
  não é uma opção`. Sem o marcador, a
  frase some. Chave no disco não é
  alcance. Sem chave `opção` no
  recibo. Um leitor só: o item, não
  `access.scope` nem `origins` nem
  `gate` nem `verify` nem `next`.
  `verified` falso.
  `commands[n].scope` nomeia o genérico
  se `commands/README.md` declara
  `sem carregar a referência produz
  trabalho genérico`. Sem o marcador,
  a frase some. Linha no disco não é
  a skill. Sem chave `genérico` no
  recibo. Um leitor só: o item, não
  `commands.scope` nem `context` nem
  `doctor.then` nem `next`. `felt`
  falso.
  `discover[n].scope` nomeia a listagem
  se o `README.md` declara `listagem
  de caminho e tipo apagava`. Sem o
  marcador, a frase some. Caminho no
  disco não é o jogo. Sem chave
  `listagem` no recibo. Um leitor só:
  o item do `--plain`, não o
  `review` nem `review_item` nem
  `next` nem `context`. `felt` falso.
  `save.scope` nomeia a gravação se o
  disco declara o estágio `.tmp`.
  Sem o marcador, a frase some.
  Escrita no disco não é aba fechada.
  Sem chave `storage` no recibo. Sem
  chamar de atômico. `trusted` falso.
  `feel.scope` nomeia o land se o laço
  declara `function landDash`. Sem o
  marcador, a frase some. Pose no
  disco não é peso percebido. Sem
  chave `land` no recibo. Sem
  `then.land`. `felt` falso.
- `then` do ciclo (`guide` / `start` / `play`) sempre tem `play`, `note`, `lost`.
  Sem `playtest`. O prompt nomeia o comando; a chave não entra.
- Se `last_run_seed` devolver um `int` (não bool), `then.seed`
  é `seed_href` (`/?seed=<n>` ou, com chuva nomeada e ≠ `spawn`,
  `/?seed=<n>&spawn=<mesa>`, com look nomeado e ≠ `normal`/`contrast`,
  `&look=<paleta>`, e com relógio nomeado e ≠ 1, `&speed=<relógio>`)
  e `then.invite` é `invite_href` (`/?invite=1`
  mais os mesmos eixos). Sem last-run ou sem seed, as duas chaves
  somem. `then.seed` e `then.invite` **não** entram em
  `CRAFT_EXAMPLES` / `CRAFT_LABELS`. `next` não ganha basis nova
  na frente de `cycle.craft`.
- `seed_href` / banner `Seed:` do serve usam o mesmo endereço da
  partida. `invite_href` / `playtest --invite` / banner `Convite:` /
  `#note` usam o convite com os mesmos eixos. Página já escrita
  não é reescrita; o JSON aponta o href vigente.
- Sem caminho e sem ideia (ou ideia que não vira slug): `ValueError`
  “sem destino” que nomeia o `start --idea` do README. Nomear não cria.
- `ship` devolve `artifact_open` só se `dist/` está completo e o HEAD
  do VERSION.json é o checkout. Completo inclui o `src/` que o
  projeto já tem. O valor é
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
  do fecho depois da prática. `flashClose` no pulso. `--as brief`
  encurta prática e rampa; `recoveryTicks` permanece. Não promover
  `pacing`.
- `listMoods()` = interseção look ∩ spawn (hoje `calm`, `dusk`).
- `SOUNDS`: dash, land, graze, collect, missed, bank, hit, over, close, live, stir, bed.
  `live` também nasce uma vez na porta (`attractSpoke`). Sem cama.
  Sem rumble.   Coleta e guarda: `captionFor` junta `corrente N` quando
  `extra.chain > 0`. O erro lê `extra.lost`: aposta zero ou
  ausente fica `atingido`; `lost > 0` nomeia a corrente que
  caiu. Não herda `chain`.   Rajada do mesmo id fica com o
  texto vigente. Sem o número o tom falava e a faixa calava.
  O pulso do fecho refresca a linha que já está lá — dez
  "últimos segundos" não comem collect/bank/hit. A voz
  continua a cada segundo. `heard` falso.
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
  inclusive na faixa da guarda na primeira visita. Depois
  da partida a mesma faixa pede seed nova (`titleNewOnBank`
  quando `doorOpen()`; `door.reset` é baixo). O campo
  repete a última. No campo o down de cima
  continua o avanço; a faixa inferior continua guardando.
  O down pede `setPointerCapture`: sair do campo ainda
  solta. Perder a captura com o toque ativo solta; depois
  do up não come o tap. Sem dash, `attractMove` desloca o corpo, `attractTick` anda a
  chuva, decai squash/flash e emite `live` uma vez, e
  `attractTouch` acende quando a mostra cruza o corpo — sem
  pontuar, sem punch, sem seed. Sem cama. Sem rumble.
  `threatCue` na porta lê a mostra. A chuva lê a mesa vigente
  (cadência e queda), sem RNG, sem `entities`. A mostra do spawn
  continua quatro gotas. Reduced trava a queda. Reset na title sorteia seed nova
  e vai a `playing`.   Pause na title é ignorado. Hidden na porta só
  descarrega — não pausa o laço. Na pausa o toque
  retoma (`lastSource === "pointer"` e o tap); Espaço
  continua só intenção. O tap não é o avanço. No
  telefone a placa nomeia `Continuar: toque` sem
  promover lastSource (`pauseSurface` → pointer; o
  token é pause, não dash). Reiniciar continua R.
  No fim
  o tap abre a porta. Toque no disco não é felt. Com tela, `reset()` sem
  argumento no `over` volta à title; um avanço *novo* no over faz o
  mesmo. Dash ainda apertado no último tick não arma a porta.
  `reset(seed)` explícito joga.
- Continuar = **repetir `lastSeed`**, não restaurar o tick. `canContinue`
  exige `runs > 0` e `lastSeed`. `doorOpen()` relê o progresso — não
  congela o valor do boot.
- `hold` / `canResume` = tick interrompido (schema 3). Seed explícita
  (`options.seed` ou `?seed=`) ignora o hold. `?spawn=` e o par
  também — a mesa nomeada não retoma outra chuva. `?look=` e
  `?speed=` vestem o hold. Reset e `recordRun`
  limpam. Não chamar de Continuar. `?seed=` não é sessão observada.
  Não promover `state_trust`. `hold.player` leva `dashWindup`.
  `hold` leva `bankWindup` e `attractTick`. Sem o relógio
  o campo repetia a frase. Hold antigo sem o número restaura 0.
  Preferências ilegíveis: `#settings-gap` no painel;
  `liveText.settings` lê `settingsLine` na porta e no fim;
  o canvas da porta e do over pinta a mesma linha;
  `persistLine` continua só sessão. Jogando a
  chave some. Nomear não é aba fechada.
  `?look=` / `?spawn=` / `?speed=` vestem a sessão.
  `flush`, `pagehide` e o sistema não gravam esses
  eixos. `updateSettings` com a chave no patch grava.
  A outra aba apaga o overlay da query. Query no
  disco não é preferência; `trusted` continua falso.
  `liveText.coach` lê `coachText` na porta e no campo —
  o mesmo texto do canvas, teclas vivas. No fim a linha
  some. O convite some `#commands`; sem o live o aviso
  calava. Na porta `liveText` nomeia `chuva <mesa>` e
  `look <paleta>` quando não são o padrão (`spawn` /
  `normal`); `contrast` some. Texto no DOM não é sessão.
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
  `bankWindup` nem `hitstop` — o lock dura mais que o perdão;
  o freeze não queima o pedido; a recarga continua contando.
  `bankBuffer` também não decai no hitstop. Coleta e guarda no mesmo quadro continuam na hora. Orbe que cai no arco da guarda espera — o sit não inflama a aposta; depois do commit o orbe entra. `collect` lê o mesmo `committed` do raspo: no avanço, no land e no quadro da conversão não seta hitstop nem sit; treme e sobe a câmera. Parada continua com suco. O relógio não come o sit: se `bankWindup > 0` no último tick, `commitBank` corre antes do `over`. Sem sit a corrente continua caindo.   O hitstop no fim não alonga o relógio: se `hitstop > 0` no último tick, `endRun` corre no early-return do freeze. A queda longe não come o verbo: se `committed`, miss marca o chão e não senta squash nem puxa a câmera. Parado, a queda ainda senta. Raspo (`grazeContact`): estreita, punch na direção,
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
  Depois some. `beginRun` não zera `attractTick`. O hold
  leva o mesmo relógio. Se a porta
  já deu a frase (`attractTick >= 48`) o campo não a repete.
  Se a porta já fechou o ensino (`attractTick >= 108` com
  frase, ou `>= 60` sem) o campo não pede mover de novo —
  dash e coleta entram. Headless (`attractTick === 0`) ainda
  vê a frase nos primeiros 48 ticks. Hold antigo sem o
  número restaura 0 e não inventa ensino feito.
  `coachText` devolve a linha que o canvas pinta; `#live`
  a nomeia na porta e no campo. `over` continua mudo. Dash, coleta,
  guarda, queda, hit, prática e superfície ficam no campo.
  `hint_hit` nomeia o estilhaço quando `hits > 0` e `chain === 0`.
  `hint_practice` nomeia a janela orbe-só enquanto
  `practicingWindow`. Dash, hit, miss e a superfície vencem.
  Depois da prática o aviso pede o orbe. A porta não ensina.
  Dash no trilho vence. Texto no disco não é `felt`.
- `copy.fantasy` alimenta a abertura **e** os 48 ticks do aviso
  quando a porta ainda não deu a frase.
  Na porta o mover começa depois da frase, não no mesmo orçamento.
- `title_play` / `title_again` / `title_new` (`door.reset` é baixo) / `title_last` /
  `title_volatile` / `title_unsaved` /
  `over_door` / `over_door_inline` em `COPY_FIELDS` (default `{dash}`).
  Copy 3: `hint_hit` (default «O estilhaço come a corrente viva —
  atravesse ou guarde»). Copy 4: `hint_practice` (default
  «Só orbes — a borda some quando a ameaça começa»).
  Ausente ganha o padrão. Sem faixa nova. Schema continua 3.
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
  nomeado e ≠ `normal`/`contrast`, junta `&look=<paleta>`. Com
  relógio nomeado e ≠ 1, junta `&speed=<relógio>`. Spawn, look
  ou relógio inválido, e os nomes padrão, somem.
  `VERSION.json` na raiz (`readArtifactMark`) some `#finding-save`
  e `#note-save`. Copiar permanece. Sem clipboard, `offerFinding`
  baixa `achado.md`. `applyFindingOffer` nomeia o destino no
  botão e em `#finding-offer`. Baixar não grava. Nomear não é
  `outsider`. `#finding` aparece com `html.invite.finding` no
  `over` e na `title` se houver `lastRun`. `bringPanel` só no
  primeiro `over`. Título com last-run não rola. Copiar não
  grava. Gravar só se `playFinding` devolver texto. Esqueleto
  vazio não casa `FINDING_FIELDS`. Achado `.md` ≠ recibo
  `record.json`.
- Serve POST `/playtest/last-run` grava `docs/playtest/last-run.json`.
  Força `observed`/`felt` falsos e `policy: played`. Árvore
  exportada responde 403. Sem canvas o headless não posta.
- `npm run session` grava `nearest-orb`. `session --look` e
  `session --speed` nomeiam o que o convite já lê. Look fora
  da mesa e relógio fora de `[0.5, 1]` recusam. Simular no
  relógio cheio não observa. Não sobrescreve `played` sem
  `--force`. Nomear não é outsider.
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
  não entra. Na porta e no fim, `audioGapLive` espelha a
  lacuna que o painel já mostra. Catálogo completo some.
  Texto no DOM não é sessão nem mix ouvido. Não
  promover `accessibility` nem `trusted` nem `heard`.

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
**Não** mais um `sfx search` que acha o stem e cala o deslocamento que o sfx já oferece.
**Não** mais um `feel` que lê squash e cala o sit que a guarda já senta.
**Não** mais um `playtest` que diz que a página escreve e cala o recado que o serve já grava.
**Não** mais um `save` que lê persistLine e cala a gravação que o storage já verifica.
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
**Não** mais um hitstop que queima o perdão do avanço.
**Não** mais um hold que some o relógio da porta e o campo repete o ensino.
**Não** mais uma região viva que some o aviso do primeiro ciclo.
**Não** mais uma tecla do remap que dispara o verbo.
**Não** mais um botão focado que ativa e avança.
**Não** mais um verify que some o stem que o recibo já nomeia.
**Não** mais uma faixa que some a curva que o last-run já traçou.
**Não** mais um preset de uma mão que some o remap.
**Não** mais uma faixa que some o percentual do knob.
**Não** mais um sistema que pede reduce e some no meio da sessão.
**Não** mais um convite que abre a seed no relógio cheio.
**Não** mais um pulso do fecho que come a legenda do verbo.
**Não** mais uma porta que cala a recuperação que o painel já mostra.
**Não** mais uma receita que cala a porta que o canvas já pinta.
**Não** mais uma aba escondida que deixa o verbo preso.
**Não** mais uma perda de foco que deixa o ofício pendente.
**Não** mais uma perda de foco que deixa o tick só na RAM.
**Não** mais um orçamento que cronometra só o campo e some a porta.
**Não** mais um playtest que some a origem do candidato.
**Não** mais um contrato de alcance que omite o pulso que o código já tem.
**Não** mais um `art` que lê paleta e cala a chuva que o disco já tem.
**Não** mais um `sfx info` que trata o stem perdido como id desconhecido.
**Não** mais um `discover` que some o sinal de origem que o `next` já usa.
**Não** mais um `content` que conta paleta como volume extraído.
**Não** mais um `discover` que some as lacunas de dimensão que o `next` já usa.
**Não** mais um controle que some e deixa a partida correr sozinha.
**Não** mais uma cama que ignora o relógio da sessão.
**Não** mais uma sessão que some o look e o relógio que o convite já lê.
**Não** mais um ciclo que some o relógio que o jogo já lê.
**Não** mais um banner do serve que some o relógio que o jogo já lê.
**Não** mais uma página de escuta que oferece o player do som que o disco perdeu.
**Não** mais um convite que grava o look, a chuva ou o relógio que só vestiu.
**Não** mais uma query de chuva que retoma o hold de outra mesa.
**Não** mais uma pausa que o toque não retoma.
**Não** mais uma porta que ensina Espaço no telefone.
**Não** mais uma porta que chama o tap de cima.
**Não** mais um `finding_href` que aponta um painel escondido.
**Não** mais uma pausa que cala o reinício que o comando já faz.
**Não** mais uma região viva que cala como sair da pausa.
**Não** mais uma pausa que ensina Esc no telefone.
**Não** mais um `next` unstructured que aponta o serve nu.
**Não** mais uma porta que cala a seed nova no telefone.
**Não** mais uma região viva que cala como abrir a porta.
**Não** mais um `feel` que cala a seed do last-run.
**Não** mais um telefone que só retoma e não pausa.
**Não** mais um `playtest` que cala a url do achado.
**Não** mais um relógio que cala a pausa.
**Não** mais um Copiar que cala o destino.
**Não** mais uma memória que cala o playtest.
**Não** mais um MDA que cala a porta.
**Não** mais uma região viva que cala a lacuna do som.
**Não** mais um aviso que some a prática enquanto o campo já a marca.
**Não** mais uma intenção que some o perigo que o `--as` já preserva.
**Não** mais um `brief` que come a folga da guarda.
**Não** mais um corpo na recuperação do dash que veste a tinta da prática.
**Não** mais um `feel` que cala as janelas da chuva que o campo já marca.
**Não** mais uma prática que acaba e chama orbe de chuva que começa.
**Não** mais uma folga que acaba e chama chuva que volta.
**Não** mais um `next` do feel que cala o candidato que o `then.note` já anexa.
**Não** mais um rastro do dash que veste o descanso.
**Não** mais um coil do dash que veste o descanso.
**Não** mais um coil do dash que veste a corrente e cala o rumo.
**Não** mais um `-h` que lista init antes de start.
**Não** mais um coil da guarda que veste o descanso.
**Não** mais uma porta que chove meio a meio e cala o risco da mesa.
**Não** mais um compromisso da guarda que veste o descanso.
**Não** mais um `art` que cala o risco da chuva que a porta já lê.
**Não** mais um `sfx export` que trata o stem perdido como id desconhecido.
**Não** mais um rótulo do dash que diz recarregando no travel.
**Não** mais um `sfx verify` que despeja errno do som que o catálogo perdeu.
**Não** mais uma região viva que cala a mesa e o look da porta.
**Não** mais um `feel` que cala o rumble que a tabela já lista.
**Não** mais um `sem destino` que cala o `start --idea` do README.
**Não** mais uma região viva que cala a mesa e o look do fim.
**Não** mais um sidecar que declara só por existir.
**Não** mais um `feel` que cala o peso do passo que o CONFIG já declara.
**Não** mais um `playtest` que cala a conta que o last-run já conta.
**Não** mais um `start` que manda o serve e cala o `npm install`.
**Não** mais um `start` que nomeia `npm install` sem ter o que instalar.
**Não** mais um `origins` que cala a mídia que o recibo lista e o disco perdeu.
**Não** mais um `ship` que diz completa a dist sem o `src/` que o projeto já tem.
**Não** mais um `roles` que lê `SOUNDS` e cala o `duckMs`.
**Não** mais um prompt que pede Abrir quando o serve já tenta abrir o navegador.
**Não** mais uma faixa que mostra seed e curva e cala o last-run simulado.
**Não** mais um achado copiado que cala o last-run simulado que a faixa já mostra.
**Não** mais um canvas da porta que cala a lacuna do som que o painel já mostra.
**Não** mais um prompt que cala o `playtest` que o `AGENTS.md` já cita.
**Não** mais um `access` que cala o `:focus-visible` que a casca já declara.
**Não** mais um `budget` que cala a porta que a receita já cronometra.
**Não** mais um `save` que cala a recuperação que o canvas já pinta.
**Não** mais um `feel` que cala o corpo que a porta já desloca.
**Não** mais um `content` que lista dusk e calm e cala o par.
**Não** mais um `ship` que cala o tamanho que a receita já relata.
**Não** mais um `access` que cala o contraste que a receita já amostra.
**Não** mais um `roles` que cala a soma que a receita já relata.
**Não** mais um `playtest` que cala a simulação que a receita já grava.
**Não** mais um `feel` que cala o probe que o disco já exercita.
**Não** mais um `art` que lista paletas e cala o look que a receita já nasce.
**Não** mais um `content` que lista dusk e calm e cala a mesa que a receita já nasce.
**Não** mais um `budget` que cronometra a porta e cala o size que a receita já relata.
**Não** mais um `roles` que soma o mix e cala o sfx que a receita já desloca.
**Não** mais um `feel` que lê `lookAheadX` e cala o laço que já inclina o quadro.
**Não** mais um `ship` que relata dist/ e cala o banner que o serve já imprime.
**Não** mais um `access` que lê região viva e cala o perigo que o live já anuncia.
**Não** mais um `save` que lê persistLine e cala o fechamento que o disco já grava.
**Não** mais um `art` que lista paletas e cala o trilho que o telegraph já marca.
**Não** mais um `sfx info` que lê a ficha e cala o pico que o inspect já mede.
**Não** mais um `access` que lê remap e cala as teclas que a tabela já lista.
**Não** mais um `ship` que lista build e cala o passo que o export já declara.
**Não** mais um `budget` que cronometra a porta e cala o percentil que a receita já pede.

Candidatos, do que ainda dói:

1. **Release (define o piso):** outra máquina correr o `dist/`. Não
   promover. `ship` já nomeia árvore incompleta, HEAD velho,
   `artifact_open` e `elsewhere` falso; o comando colável não é a
   prova.
2. **Idéia→jogo:** o `-h` lista `start` antes de `init`. `start` devolve `open` e `url`; `play` / `open`
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
   Se o serve tenta abrir o navegador, o
   prompt nomeia a tentativa. Sem o
   marcador, pede Abrir. Nomear não
   abre.    Sem `then.browser`.
   Se o serve recusa produção, o `play` nomeia a produção que o serve já recusa. Serve no disco não é publicação. Sem chave `produção`.
   `runtime` lê o Node do PATH; sem 20+ o prompt avisa.
   O prompt nomeia `Sessão:` se o manifesto declara `session`.
   Sem destino, o `guide` também nomeia `Verbo:` / `Porta:` se o
   starter declara. Com `--idea` ou `copy.json`, o prompt nomeia
   `Fantasia:` antes de `Verbo:`. A frase não muda o verbo.
   `init_scope` só afirma rascunhos quando `documents` é verdadeiro;
   o `start` embute esse recibo.    Se o play pede npm, o `package.json`
   tem dependências e `node_modules` falta,
   `then.install` nomeia `npm install`. Sem
   dependências a chave some. Nomear não
   instala. `play` continua o serve.    Os dois escrevem `AGENTS.md` com
   o serve, o `note` e o `playtest`; sem rascunhos a memória não
   lista GDD. O `playtest` só lê. Sem os quatro não é achado.
   Nomear o leitor não observa. O prompt de `start` / `play` /
   `guide` / `init` nomeia o mesmo `playtest`. Sem
   `then.playtest`. O passo 3 continua `note`. `template agents`
   e o `next` sem memória geram o mesmo texto.    `preproduction.md` (injetado pelo
   `context` no foco create e em `--stage`) ensina `start --idea`.
   `process.md` (primeiro `read_next` de todo foco) nomeia a porta e o
   mapa start → jogar → `note` sem executar.
   `doctor` no lab vazio devolve `then.guide` com `--idea`; com jogo a chave some.
   Se o package do starter pede Node, o `doctor` nomeia o engines que o package já declara. Pedido no disco não é binário no PATH. Sem chave `engines`. Nomear não instala.
   Depois do `start` fresco o `context` adia a auditoria (`audit.deferred`);
   lacunas continuam listadas. Sem jogo que abre, o `scan` ainda pede documentar.
   O `init` também devolve `open`, `url` e `prompt`; o `prompt` sai em stderr.
   Sem starter o aviso nomeia `start --idea`. Sem `prompt`.
   `sfx search` nomeia o stem do starter que casa. Se o `tools/design-sfx.*` desloca a voz, o `sfx search` nomeia o deslocamento que o sfx já oferece. Arquivo no disco não é mix ouvida. Sem chave `sfx`. Se a receita recusa que o acervo compartilhado seja o primeiro ciclo, o `local` do `sfx search` nomeia o adapt que a receita já recusa. Stem no disco não é mix. Sem chave `adapt`. Se a barra recusa que triagem documental/técnica seja aprovação artística, o `matches` do `sfx search` nomeia a triagem que a barra já recusa. Ficha no disco não é mix. Sem chave `triagem`. `sfx info`
   lê a mesma chave e nomeia o stem que o recibo lista e o
   disco perdeu. Se o inspect já mediu o pico, o `sfx info`
   nomeia o pico que o inspect já mede. Pico no recibo
   não é mix ouvida. Sem `rms`.    `sfx copy` e `sfx export` levam
   bytes e créditos. Se o sidecar declara licença, o `sfx copy` nomeia os créditos que o copy já leva. Créditos no disco não são mix ouvida. Sem chave `sidecar`. Se a receita recusa que importar e exportar seja ouvir, o `sfx copy` do acervo nomeia o ouvir que a receita já recusa. Cópia no disco não é mix. Sem chave `ouvir`. Se a receita recusa que o arquivo importado esteja sendo consumido, o `record` do `sfx copy` do acervo nomeia o consumido que a receita já recusa. Recibo no disco não é mix. Sem chave `consumido`. `sfx export` nomeia o stem que o
   recibo lista e o disco perdeu — exportar não inventa
   bytes. Se a receita recusa que o export invente bytes, o `sfx export` do stem nomeia a invenção que a receita já recusa. Cópia no disco não é mix. Sem chave `invenção`. Se o export recusa processamento, o `sfx export` nomeia o processamento que o export já recusa. Bytes no disco não são mix ouvida. Sem chave `processamento`.    `sfx verify` nomeia os stems sem cruzar
   e nomeia o stem que o recibo lista e o disco perdeu.
   Se o check cruza a integridade, o `sfx verify` nomeia a integridade que o check já cruza. Hash no disco não é mix ouvida. Sem chave `sha256`. Se a receita recusa que variante ausente seja lacuna, o `sfx verify` vazio nomeia a lacuna que a receita já recusa. Lista no disco não é mix. Sem chave `lacuna`. Se a receita recusa que nomear o 404 seja mix, o `missing` do `sfx verify` nomeia o 404 que a receita já recusa. Lista no disco não é mix. Sem chave `404`.
   `sfx verify` nomeia o som que o catálogo lista e o
   disco perdeu. `count` continua o acervo.    Sem os quatro campos,
   `playtest` nomeia `finding_href`, `finding_open`,
   `qa`, `form`
   e `fields`. Com last-run, nomeia
   também `candidate_tally` se a
   conta dos verbos ficou no recibo.
   `dashes` e `ticks` ficam de fora.
   O Copiar e o Gravar levam a
   faixa do last-run quando
   `composeFinding` chama
   `runFacts`. Sem o marcador,
   o `playtest.scope` cala.
   Se o `tools/session.*` grava
   a simulação, o `playtest`
   nomeia. Traço no disco não
   é alguém de fora. Sem chave
   `session`. Sem `then.session`
   no leitor. Sem tally nem relógio no
   markdown. Markdown no disco
   não é alguém de fora.
   `next`
   aponta o serve, a página (`finding_open`) e `note --field`, não relê o
   leitor. Sem `then` no leitor.    `roles` nomeia o `duckMs` que
   `SOUNDS` já declara. Sem duck a
   chave some. Nomear não é mix
   ouvida. Se o `tools/mix.*` soma
   as vozes, o `roles` nomeia a
   soma. Se o `tools/design-sfx.*`
   desloca a voz, o `roles` nomeia
   a voz. Sem chave `mix`. Sem
   chave `sfx`. Sem acervo, `roles --fill` nomeia o stem
   do starter; `--apply` o copia — e recoloca o WAV se o
   recibo já está e origem e licença casam; `next` aponta
   `--apply`. `sfx copy` do acervo recoloca o WAV se o
   recibo casa origem e licença, e declara `heard` falso.
   `feel`
   nomeia `then.play` e `then.note` sem
   executar. Lê as janelas da chuva que o
   campo já marca, o rumble que a tabela
   já lista, o peso do passo que o
   CONFIG já declara, a inclinação que
   o `lookAhead` já marca e o land que
   o dash já emite. Sem chave
   `lookAhead`. Sem chave `land`. Com last-run, nomeia
   `then.seed` e `then.invite`. O `next`
   (`feel.unobserved`) aponta o mesmo
   `note` — com `--from-run` se o
   candidato existir. O `note` sem
   `--from-run` nomeia o last-run se
   o arquivo está no disco. Nomear
   não anexa. Sem chave `last_run`.
   Sem serve a
   chave some. Sem last-run, seed e invite
   somem. Sem
   `prompt`.    `discover` nomeia os mesmos
   sinais que o `next` usa, inclusive origem
   sem recibo, sem propor e
   sem ranquear. `origins` nomeia a
   mídia que o recibo lista e o
   disco perdeu. Nomear não
   devolve o arquivo. Sinal verdadeiro não é
   partida jogada. `len(steps) == 3`
   e `executed: false` continuam.
3. **Checkpoint do tick:** `hold` existe e leva o relógio da
   porta. A porta nomeia sessão
   volátil e gravação recusada. Preferências ilegíveis avisam no
   painel e preservam `settings.broken`. A região viva nomeia
   a mesma recuperação na porta e no fim; o canvas também.
   `save` relata `warned` se o disco tem essas chaves. A região
   viva também espelha o aviso da sessão na porta e no fim.
   Pausa, `pagehide`, `beforeunload` e o blur da janela
   gravam o hold. Na porta o blur só descarrega.
   Falta aba fechada real.
   Não promover. Não chamar `hold` de Continuar.
4. **Item 1 residual:** o mapa, as receitas de foco e os templates da
   primeira situação — brief, GDD, game-design, PoC, slice, QA e
   release — já nomeiam a porta. MDA, MVP e PRD também. Design system, ambição, barra,
   checklist, os pacotes de gênero e o processo comum (`process.md`,
   primeiro `read_next`) também. O rascunho de playtest traz a forma
   do achado, vazia. `preproduction.md` já ensina `start --idea`.
   A barra de `accessibility` do starter não atribui medição no
   dispositivo ao `contrast`. Referências que ainda falarem só do
   campo sem a abertura estão velhas.    `sfx serve` gera a página se
   `ui/` faltar e nomeia o som que o catálogo lista e o disco
   perdeu.    `sfx info` lê a chave do starter e nomeia o
   stem que o recibo lista e o disco perdeu. Se o
   inspect já mediu o pico, o `sfx info` nomeia o
   pico que o inspect já mede. Pico no recibo não
   é mix ouvida. Sem `rms`.    `sfx copy` e
   `sfx export` levam bytes e créditos. `sfx export` nomeia
   o stem que o recibo lista e o disco perdeu — exportar
   não inventa bytes. Se a receita recusa que o export invente bytes, o `sfx export` do stem nomeia a invenção que a receita já recusa. Cópia no disco não é mix. Sem chave `invenção`. Se o export recusa processamento, o `sfx export` nomeia o processamento que o export já recusa. Bytes no disco não são mix ouvida. Sem chave `processamento`. `roles --apply` também
   copia o stem do starter.    `sfx verify` nomeia os stems
   sem cruzar e nomeia o stem que o recibo lista e o disco
   perdeu. Se o check cruza a integridade, o `sfx verify` nomeia a integridade que o check já cruza. Hash no disco não é mix ouvida. Sem chave `sha256`. `sfx verify` nomeia o som que o catálogo lista
   e o disco perdeu — não despeja errno. Nomear não entrega. Copiar não é `heard`. Tocar não
   é `heard`.    `roles` já nomeia o `duckMs` que
   `SOUNDS` declara, a soma que o
   `mix` relata e a voz que o
   `sfx` desloca — não pôr o duck
   no `feel` (irmão, não o próximo
   salto). Não nomear `DUCK_BUSES`,
   `DUCK_LEVEL` nem `MIX_HEADROOM`
   no mesmo leitor (irmão, não o
   próximo salto). Não inventar
   chave `sfx` nem nomear `peak`
   no `roles` (irmão, não o
   próximo salto). `sfx copy` de stem local perdido ainda trata
   a ausência como id desconhecido — irmão, não o próximo
   salto. O rótulo do coil do dash ainda diz recarregando —
   irmão do travel, não o próximo salto. `sfx export` de
   id do acervo cujo arquivo sumiu ainda despeja errno —
   irmão do verify, não o próximo salto.    A região viva na
   porta e no fim já nomeia a mesa e o look — não pintar
   os eixos no canvas (irmão, não o próximo salto). Não
   nomear `gameSpeed` no live (irmão, não o próximo
   salto). O canvas da porta e do
   fim já nomeia a lacuna do som —
   não inventar chave `audio_gap`
   no `access` (irmão, não o
   próximo salto). Não nomear a
   lacuna na pausa. O `access`
   já nomeia o `:focus-visible`
   que a casca declara — não
   inventar chave `focus` no
   recibo (irmão, não o próximo
   salto). O `budget` já nomeia
   a porta que o tool cronometra
   — não inventar chave `door`
   no recibo (irmão, não o
   próximo salto). Não importar
   limiar de quadro. O `save` já
   nomeia a recuperação que o
   canvas pinta — não inventar
   chave `recovery` no recibo
   (irmão, não o próximo salto).
   Não pintar a recuperação na
   pausa.    O `feel`
   já nomeia o rumble e o peso do passo —
   não inventar chave `haptics` no
   recibo (irmão, não o próximo salto).
   O coil do dash já marca o rumo no
   corpo — não inventar chave
   `heading` no recibo (irmão, não
   o próximo salto). Não outro
   traço de rumo no coil.
   Não incluir `player.halfWidth` em
   `FEEL_KEY` (irmão, não o próximo
   salto).    `origins --declare`
   escreve o sidecar. Sidecar sem
   os três rótulos não declara.
   Recibo não é
   licença. O `origins` nomeia a
   mídia que o recibo lista e o
   disco perdeu. Nomear não
   devolve o arquivo. CREDITS.md
   pela menção ainda declara
   (irmão, não o próximo salto).
   Menção em CREDITS.md de
   caminho ausente continua
   calada (irmão, não o
   próximo salto). O `sem destino` do
   `start` e do `guide` na raiz
   nomeia o `start --idea` que o
   README já imprime. Nomear não
   cria. Não trocar a
   `description` do `-h` (irmão
   de 322) nem a ordem dos
   verbos. O `playtest` já nomeia
   a conta do last-run — não
   levar `candidate_tally` à faixa
   do convite (irmão, não o
   próximo salto). Não incluir
   `dashes` nem `ticks` na conta.
   O `start` nomeia `npm install`
   só quando o `package.json` tem
   dependências — não dobrar no
   `play` (irmão, não o próximo
   salto). Sem dependências a
   chave some. O `feel` não ganha
   `then.install`.
5. **Outsider / pacing / a11y real / feel no dispositivo:** não
   promover. Convite, LAN, stub, `gameSpeed` no disco, tinta
   estável no disco, pulso no disco, chuva no disco, estilhaço dusk no disco, intenção warmer no
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
  e um
  hitstop que
  queima o
  perdão do
  avanço
  e um
  hold que
  some o
  relógio da
  porta e o
  campo
  repete o
  ensino
  e uma
  região viva
  que some o
  aviso do
  primeiro
  ciclo
  e um
  knob de
  escala que
  cresce o
  canvas e
  some a
  casca
  e um
  recado que
  dispara o
  verbo
  e um
  toque que
  sai do
  campo e
  deixa o
  corpo
  andando
  e um
  look que
  veste o
  canvas e
  some o
  select
  e uma
  outra aba
  que some
  as
  preferências
  desta
  página
  e um
  preset de
  uma mão que
  some o
  remap
  e uma
  faixa que
  some o
  percentual
  do knob
  e um
  sistema que
  pede reduce
  e some no
  meio da
  sessão
  e um
  convite que
  abre a seed
  no relógio
  cheio
  e um
  pulso do
  fecho que
  come a
  legenda do
  verbo
  e uma
  porta que
  cala a
  recuperação
  que o
  painel já
  mostra
  e uma
  receita que
  cala a
  porta que
  o canvas
  já pinta
  e uma
  aba
  escondida
  que deixa
  o verbo
  preso
  e uma
  perda de
  foco que
  deixa o
  ofício
  pendente
  e uma
  perda de
  foco que
  deixa o
  tick só
  na RAM
  e um
  orçamento
  que
  cronometra
  só o
  campo
  e um
  playtest
  que some
  a origem
  do
  candidato
  e um
  contrato
  de
  alcance
  que
  omite
  o
  pulso
  e um
  art
  que
  lê
  paleta
  e
  cala
  a
  chuva
  e um
  sfx
  info
  que
  trata
  o
  stem
  perdido
  como
  id
  desconhecido
  e um
  discover
  que
  some
  o
  sinal
  de
  origem
  e um
  content
  que
  conta
  paleta
  como
  volume
  e um
  controle
  que
  some
  e
  deixa
  a
  partida
  correr
  e uma
  cama
  que
  ignora
  o
  relógio
  da
  sessão
  e um
  convite
  que
  grava
  o
  look
  que
  só
  vestiu
  e uma
  query
  de
  chuva
  que
  retoma
  o
  hold
  de
  outra
  mesa
  e uma
  pausa
  que
  o
  toque
  não
  retoma
  e uma
  porta
  que
  ensina
  Espaço
  no
  telefone
  e uma
  porta
  que
  chama
  o
  tap
  de
  cima
  e um
  finding_href
  que
  aponta
  um
  painel
  escondido
  e uma
  pausa
  que
  cala
  o
  reinício
  e uma
  região
  viva
  que
  cala
  como
  sair
  da
  pausa
  e uma
  pausa
  que
  ensina
  Esc
  no
  telefone
  e um
  next
  unstructured
  que
  aponta
  o
  serve
  nu
  e uma
  porta
  que
  cala
  a
  seed
  nova
  no
  telefone
  e uma
  região
  viva
  que
  cala
  como
  abrir
  a
  porta
  e um
  feel
  que
  cala
  a
  seed
  do
  last-run
  e um
  telefone
  que
  só
  retoma
  e
  não
  pausa
  e um
  playtest
  que
  cala
  a
  url
  do
  achado
  e um
  relógio
  que
  cala
  a
  pausa
  e um
  Copiar
  que
  cala
  o
  destino
  e uma
  memória
  que
  cala
  o
  playtest
  e um
  MDA
  que
  cala
  a
  porta
  e uma
  região
  viva
  que
  cala
  a
  lacuna
  do
  som
  e um
  aviso
  que
  some
  a
  prática
  enquanto
  o
  campo
  já
  a
  marca
  e uma
  intenção
  que
  some
  o
  perigo
  que
  o
  `--as`
  já
  preserva
  e um
  `brief`
  que
  come
  a
  folga
  da
  guarda
  e um
  corpo
  na
  recuperação
  do
  dash
  que
  veste
  a
  tinta
  da
  prática
  e um
  `feel`
  que
  cala
  as
  janelas
  da
  chuva
  que
  o
  campo
  já
  marca
  e uma
  prática
  que
  acaba
  e
  chama
  orbe
  de
  chuva
  que
  começa
  e uma
  folga
  que
  acaba
  e
  chama
  chuva
  que
  volta
  e um
  `next`
  do
  feel
  que
  cala
  o
  candidato
  que
  o
  `then.note`
  já
  anexa
  e um
  rastro
  do
  dash
  que
  veste
  o
  descanso
  e um
  coil
  do
  dash
  que
  veste
  o
  descanso
  e um
  `-h`
  que
  lista
  init
  antes
  de
  start
  e um
  coil
  da
  guarda
  que
  veste
  o
  descanso
  e uma
  porta
  que
  chove
  meio
  a
  meio
  e
  cala
  o
  risco
  da
  mesa
  e um
  compromisso
  da
  guarda
  que
  veste
  o
  descanso
  e um
  `art`
  que
  cala
  o
  risco
  da
  chuva
  que
  a
  porta
  já
  lê
  e um
  `sfx export`
  que
  trata
  o
  stem
  perdido
  como
  id
  desconhecido
  e um
  rótulo
  do
  dash
  que
  diz
  recarregando
  no
  travel
  e um
  `sfx verify`
  que
  despeja
  errno
  do
  som
  que
  o
  catálogo
  perdeu
  e uma
  região
  viva
  que
  cala
  a
  mesa
  e
  o
  look
  da
  porta
  e um
  `feel`
  que
  cala
  o
  rumble
  que
  a
  tabela
  já
  lista
  e um
  `sem destino`
  que
  cala
  o
  `start`
  do
  README
  e uma
  região
  viva
  que
  cala
  a
  mesa
  e
  o
  look
  do
  fim
  e um
  sidecar
  que
  declara
  só
  por
  existir
  e um
  `feel`
  que
  cala
  o
  peso
  do
  passo
  e um
  `playtest`
  que
  cala
  a
  conta
  do
  last-run
  e um
  `start`
  que
  manda
  o
  serve
  e
  cala
  o
  npm
  install
  e um
  `origins`
  que
  cala
  a
  mídia
  que
  o
  recibo
  lista
  e
  o
  disco
  perdeu
  e um
  `start`
  que
  nomeia
  npm
  install
  sem
  ter
  o
  que
  instalar
  e um
  `ship`
  que
  diz
  completa
  a
  dist
  sem
  o
  src
  do
  projeto
  e um
  `roles`
  que
  lê
  `SOUNDS`
  e
  cala
  o
  `duckMs`
  e um
  prompt
  que
  pede
  Abrir
  quando
  o
  serve
  já
  tenta
  abrir
  o
  navegador
  e uma
  faixa
  que
  mostra
  seed
  e
  curva
  e
  cala
  o
  last-run
  simulado
  e um
  `playtest`
  que
  cala
  a
  simulação
  que
  a
  receita
  já
  grava
  e um
  `feel`
  que
  cala
  o
  probe
  que
  o
  disco
  já
  exercita
  e um
  `art`
  que
  lista
  paletas
  e
  cala
  o
  look
  que
  a
  receita
  já
  nasce
  e um
  `content`
  que
  lista
  dusk
  e
  calm
  e
  cala
  a
  mesa
  que
  a
  receita
  já
  nasce
  e um
  `budget`
  que
  cronometra
  a
  porta
  e
  cala
  o
  size
  que
  a
  receita
  já
  relata
  e um
  `roles`
  que
  soma
  o
  mix
  e
  cala
  o
  sfx
  que
  a
  receita
  já
  desloca
  e um
  `feel`
  que
  lê
  `lookAheadX`
  e
  cala
  o
  laço
  que
  já
  inclina
  o
  quadro
  e um
  `ship`
  que
  relata
  dist/
  e
  cala
  o
  banner
  que
  o
  serve
  já
  imprime
  e um
  `access`
  que
  lê
  região
  viva
  e
  cala
  o
  perigo
  que
  o
  live
  já
  anuncia
  e um
  `save`
  que
  lê
  persistLine
  e
  cala
  o
  fechamento
  que
  o
  disco
  já
  grava
  e um
  `art`
  que
  lista
  paletas
  e
  cala
  o
  trilho
  que
  o
  telegraph
  já
  marca
  e um
  `sfx info`
  que
  lê
  a
  ficha
  e
  cala
  o
  pico
  que
  o
  inspect
  já
  mede
  e um
  `access`
  que
  lê
  remap
  e
  cala
  as
  teclas
  que
  a
  tabela
  já
  lista
  e um
  `ship`
  que
  lista
  build
  e
  cala
  o
  passo
  que
  o
  export
  já
  declara
  e um
  `budget`
  que
  cronometra
  a
  porta
  e
  cala
  o
  percentil
  que
  a
  receita
  já
  pede
  e um
  `sfx search`
  que
  acha
  o
  stem
  e
  cala
  o
  deslocamento
  que
  o
  sfx
  já
  oferece
  e um
  `feel`
  que
  lê
  squash
  e
  cala
  o
  sit
  que
  a
  guarda
  já
  senta
  e um
  `playtest`
  que
  diz
  que
  a
  página
  escreve
  e
  cala
  a
  rota
  que
  o
  serve
  já
  grava
  e um
  `save`
  que
  lê
  persistLine
  e
  cala
  a
  gravação
  que
  o
  storage
  já
  verifica
  não
  fecham. A receita
   de velocidade ajustável já tem knob e a cama o segue; sessão observada continua pendente.
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

Arquivos quentes da última sessão: o
`sfx info`
do stem nomeia o lixo que a
receita já recusa. A receita já
dizia que arquivo sem papel não é
áudio do jogo; a ficha copiava
licença e bytes e calava a recusa.
Arquivo no disco não é mix. Sem
chave `lixo`. Nomear não ouve.
A família recado/remap/botão está saturada.
A família curva do last-run está saturada.
A família curva que cala o aperto que a receita já recusa está saturada.
A família conflito que cala a precedência que a barra já recusa está saturada.
A família import que cala a improvisação de licença que a receita já recusa está saturada.
A família ficha do stem que cala o lixo que a receita já recusa está saturada.
A família oneHand/remap restore está saturada.
A família readout do knob está saturada.
A família matchMedia ao vivo está saturada.
A família eixo no convite está saturada.
A família close caption flood está saturada.
A família settings no canvas da porta está saturada.
A família receita vs canvas da porta está saturada.
A família visibility ghost hold / aba escondida está saturada.
A família blur ghost press / perda de foco deixa o ofício pendente está saturada.
A família blur grava o hold / perda de foco deixa o tick na RAM está saturada.
A família orçamento só o campo / porta some do budget está saturada.
A família política do candidato / session apaga played está saturada.
A família contrato de alcance omite o pulso está saturada.
A família art lê paleta e cala a chuva está saturada.
A família sfx info trata stem perdido como id desconhecido está saturada.
A família discover some o sinal de origem está saturada.
A família content conta paleta como volume está saturada.
A família discover some as lacunas de dimensão está saturada.
A família controle que some / pad disconnect deixa a partida correr está saturada.
A família cama ignora o relógio da sessão / gameSpeed sem cama está saturada.
A família sessão some look/speed que o convite já lê está saturada.
A família ciclo some o relógio que o jogo já lê está saturada.
A família banner do serve some o relógio que o jogo já lê está saturada.
A família página de escuta oferece o player do som perdido está saturada.
A família convite grava o look/chuva/relógio da query está saturada.
A família query de chuva retoma o hold de outra mesa está saturada.
A família pausa que o toque não retoma está saturada.
A família porta que ensina Espaço no telefone está saturada.
A família porta que chama o tap de cima está saturada.
A família finding_href aponta um painel escondido está saturada.
A família pausa que cala o reinício está saturada.
A família região viva que cala como sair da pausa está saturada.
A família pausa que ensina Esc no telefone está saturada.
A família next unstructured aponta o serve nu está saturada.
A família porta que cala a seed nova no telefone está saturada.
A família região viva que cala como abrir a porta está saturada.
A família feel que cala a seed do last-run está saturada.
A família telefone que só retoma e não pausa está saturada.
A família playtest que cala a url do achado está saturada.
A família relógio que cala a pausa está saturada.
A família Copiar que cala o destino está saturada.
A família memória que cala o playtest está saturada.
A família MDA que cala a porta está saturada.
A família região viva que cala a lacuna do som está saturada.
A família aviso que some a prática enquanto o campo já a marca está saturada.
A família intenção que some o perigo que o `--as` já preserva está saturada.
A família brief que come a folga da guarda está saturada.
A família corpo na recuperação do dash que veste a tinta da prática está saturada.
A família feel que cala as janelas da chuva que o campo já marca está saturada.
A família prática que acaba e chama orbe de chuva que começa está saturada.
A família folga que acaba e chama chuva que volta está saturada.
A família next do feel que cala o candidato que o then.note já anexa está saturada.
A família rastro do dash que veste o descanso está saturada.
A família coil do dash que veste o descanso está saturada.
A família -h que lista init antes de start está saturada.
A família coil da guarda que veste o descanso está saturada.
A família porta que chove meio a meio e cala o risco da mesa está saturada.
A família compromisso da guarda que veste o descanso está saturada.
A família art que cala o risco da chuva que a porta já lê está saturada.
A família sfx export trata stem perdido como id desconhecido está saturada.
A família rótulo do dash diz recarregando no travel está saturada.
A família sfx verify despeja errno do som que o catálogo perdeu está saturada.
A família região viva que cala a mesa e o look da porta está saturada.
A família feel que cala o rumble que a tabela já lista está saturada.
A família sem destino que cala o start do README está saturada.
A família região viva que cala a mesa e o look do fim está saturada.
A família sidecar que declara só por existir está saturada.
A família feel que cala o peso do passo que o CONFIG já declara está saturada.
A família playtest que cala a conta que o last-run já conta está saturada.
A família start que manda o serve e cala o npm install está saturada.
A família origins que cala a mídia que o recibo lista e o disco perdeu está saturada.
A família start que nomeia npm install sem ter o que instalar está saturada.
A família ship que diz completa a dist sem o src do projeto está saturada.
A família roles que lê SOUNDS e cala o duckMs está saturada.
A família prompt que pede Abrir quando o serve já tenta abrir está saturada.
A família faixa que cala o last-run simulado está saturada.
A família coil do dash que veste a corrente e cala o rumo está saturada.
A família achado copiado que cala o last-run simulado está saturada.
A família canvas da porta que cala a lacuna do som está saturada.
A família prompt que cala o playtest que o AGENTS.md já cita está saturada.
A família access que cala o focus-visible que a casca já declara está saturada.
A família budget que cala a porta que a receita já cronometra está saturada.
A família save que cala a recuperação que o canvas já pinta está saturada.
A família feel que cala o corpo que a porta já desloca está saturada.
A família content que lista dusk e calm e cala o par está saturada.
A família ship que cala o tamanho que a receita já relata está saturada.
A família access que cala o contraste que a receita já amostra está saturada.
A família roles que cala a soma que a receita já relata está saturada.
A família playtest que cala a simulação que a receita já grava está saturada.
A família feel que cala o probe que o disco já exercita está saturada.
A família art que lista paletas e cala o look que a receita já nasce está saturada.
A família content que lista dusk e calm e cala a mesa que a receita já nasce está saturada.
A família budget que cronometra a porta e cala o size que a receita já relata está saturada.
A família roles que soma o mix e cala o sfx que a receita já desloca está saturada.
A família feel que lê lookAheadX e cala o laço que já inclina o quadro está saturada.
A família ship que relata dist/ e cala o banner que o serve já imprime está saturada.
A família access que lê região viva e cala o perigo que o live já anuncia está saturada.
A família save que lê persistLine e cala o fechamento que o disco já grava está saturada.
A família art que lista paletas e cala o trilho que o telegraph já marca está saturada.
A família sfx info que lê a ficha e cala o pico que o inspect já mede está saturada.
A família access que lê remap e cala as teclas que a tabela já lista está saturada.
A família ship que lista build e cala o passo que o export já declara está saturada.
A família budget que cronometra a porta e cala o percentil que a receita já pede está saturada.
A família note que cala o last-run que o disco já guarda está saturada.
A família sfx summary que lista stems e cala o pico que o peak já relata está saturada.
A família start que aponta then.pair e cala o nascimento que o pair já declara está saturada.
A família access que lista captions e cala a legenda que a porta já lê está saturada.
A família sfx search que acha o stem e cala o deslocamento que o sfx já oferece está saturada.
A família feel que lê squash e cala o sit que a guarda já senta está saturada.
A família playtest que diz que a página escreve e cala o recado que o serve já grava está saturada.
A família save que lê persistLine e cala a gravação que o storage já verifica está saturada.
A família doctor que lê a major do PATH e cala o engines que o package já declara está saturada.
A família ship que empacota a árvore e cala o file:// que o export já recusa está saturada.
A família sfx copy que leva o caminho e cala os créditos que o sidecar já carrega está saturada.
A família sfx copy do acervo que leva bytes e cala o ouvir que a receita já recusa está saturada.
A família sfx search local que lista stems e cala o adapt que a receita já recusa está saturada.
A família sfx seed que importa a seleção e cala a aprovação que a receita já recusa está saturada.
A família sfx search matches que lista licenças e cala a triagem que a barra já recusa está saturada.
A família sfx verify vazio que lista stems e cala a lacuna que a receita já recusa está saturada.
A família sfx export do stem que copia o WAV e cala a invenção que a receita já recusa está saturada.
A família sfx verify missing que lista o stem ausente e cala o 404 que a receita já recusa está saturada.
A família access captions que copia a chave e cala o número que a receita já recusa está saturada.
A família roles do x do campo que copia o id e cala o panner que a receita já recusa está saturada.
A família roles que lê SOUNDS e cala o retomar que a receita já recusa está saturada.
A família access haptics que copia a chave e cala o controle que a receita já recusa está saturada.
A família access remap que copia a chave e cala o botão que a receita já recusa está saturada.
A família access reduced_motion que copia a chave e cala a causa que a receita já recusa está saturada.
A família access high_contrast que copia a chave e cala o neutro que a receita já recusa está saturada.
A família access colorblind que copia a chave e cala o ícone que a receita já recusa está saturada.
A família access one_hand que copia a chave e cala a mão que a receita já recusa está saturada.
A família access assist que copia a chave e cala o oculto que a receita já recusa está saturada.
A família access game_speed que copia a chave e cala a precisão que a receita já recusa está saturada.
A família access ui_scale que copia a chave e cala a tipografia que a receita já recusa está saturada.
A família access live que copia a chave e cala o leitor que a receita já recusa está saturada.
A família convite que anuncia o endereço e cala as sessões que a receita já recusa está saturada.
A família record do sfx copy do acervo que copia autor e licença e cala o consumido que a receita já recusa está saturada.
A família then do start que aponta play e cala a experiência que a receita já recusa está saturada.
A família play que aponta o url e cala a produção que o serve já recusa está saturada.
A família sfx verify que lê ok e cala a integridade que o check já cruza está saturada.
A família sfx export que copia bytes e cala o processamento que o export já recusa está saturada.
A família bar que lê a tabela e cala o mínimo que a prosa já declara está saturada.
A família guide que lê o ciclo e cala o relógio que o manifesto já declara está saturada.
A família craft que parseia a linha e cala a saída de escopo que a tabela já declara está saturada.
A família art que nasce a paleta e cala o contraste que o look já recusa está saturada.
A família doctor que valida o manifesto e cala as substituições que o starter.json já declara está saturada.
A família discover que lê os validadores e cala os scripts que o package já declara está saturada.
A família init que copia o package e cala o módulo que o manifesto já declara está saturada.
A família gate que lê a forma e cala o gate que a tabela já declara está saturada.
A família scan que lê as áreas e cala o serve que o README já aponta está saturada.
A família convite que anuncia a rede e cala o bind que o serve já prende está saturada.
A família template que emite rascunho e cala a publicação que o molde já recusa está saturada.
A família context que aponta o roteiro e cala o audit que o roteiro já pede está saturada.
A família continuity que aponta o processo e cala a PoC que o processo já nega está saturada.
A família agent_context que aponta a memória e cala o AAA que a memória já recusa está saturada.
A família finish que aponta a guia e cala o checklist que a guia já recusa preencher está saturada.
A família production_bar que aponta a guia e cala a promoção que a barra já recusa está saturada.
A família packs que aponta o pacote e cala o navegador que o pacote já recusa provar está saturada.
A família next que propõe e cala a ação que o processo já pede está saturada.
A família context que seleciona a etapa e cala o progresso que o processo já recusa está saturada.
A família studio_assets que aponta o acervo e cala a escuta que o mapa já recusa está saturada.
A família scan que localiza a direção e cala os tokens que o sistema já recusa está saturada.
A família scan que localiza o TDD e cala as dependências que a receita já recusa está saturada.
A família scan que conta documentos e cala a inexistência que o roteiro já recusa está saturada.
A família platform que aponta o pacote e cala a capacidade que o índice já recusa está saturada.
A família passo de jogar que copia o verbo e cala o onboarding que o roteiro já recusa está saturada.
Não incluir `player.halfWidth` em `FEEL_KEY`.
Não outro leaf do `player` no extrator.
Não levar `candidate_tally` à faixa do convite.
Não incluir `dashes` nem `ticks` na conta.
Não dobrar o install no `play`.
Não adicionar `then.install` ao `feel`.
CREDITS.md pela menção ainda declara — irmão de 334.
Menção em CREDITS.md de caminho ausente continua calada — irmão de 334 e 338.
Não exigir `data/` nem `public/` na árvore do ship — irmão de 340.
Não pôr o duck no `feel` — irmão de 341.
Não nomear `DUCK_BUSES`, `DUCK_LEVEL` nem `MIX_HEADROOM` no `roles` — irmão de 341.
Não adicionar `then.browser` — irmão de 342.
Não auto-servir nem abrir o navegador no harness — irmão de 342.
Não nomear a origem no live — irmão de 343.
Não levar `speed` a `runFacts` — invariante de 0.9.271 e irmão de 343.
Não inventar chave `heading` no recibo do feel — irmão de 344.
Não outro traço de rumo no coil — irmão de 344.
Não inventar chave `finding_run` no recibo do playtest — irmão de 345.
Não levar tally nem relógio ao markdown do achado — irmão de 345 e 343.
Não inventar chave `audio_gap` no recibo do access — irmão de 346.
Não nomear a lacuna do som na pausa — o live da pausa também cala; irmão de 346.
Não adicionar `then.playtest` — irmão de 347.
Não virar o passo 3 em `playtest` — irmão de 347.
Não pôr `finding_open` no prompt — irmão de 347.
Não inventar chave `focus` no recibo do access — irmão de 348.
Não outro outline de foco na casca — irmão de 348.
Não inventar chave `door` no recibo do budget — irmão de 349.
Não importar limiar de quadro no `budget` — irmão de 349.
Não inventar chave `recovery` no recibo do save — irmão de 350.
Não pintar a recuperação na pausa — irmão de 350 e 346.
Não inventar chave `attract` no recibo do feel — irmão de 351.
Não outro deslocamento do corpo na porta — irmão de 351 e 161.
Não inventar chave `moods` no recibo do content — irmão de 352.
Não contar o par como volume — irmão de 352 e 284.
Não inventar chave `size` no recibo do ship — irmão de 353.
Não importar teto de bytes no `ship` — irmão de 353 e 349.
Não inventar chave `contrast` no recibo do access — irmão de 354.
Não importar limiar de contraste no `access` — irmão de 354 e 215.
Não inventar chave `mix` no recibo do roles — irmão de 355.
Não nomear `peak` no `roles` — irmão de 355.
Não importar LUFS no `roles` — irmão de 355 e 341.
Não inventar chave `session` no recibo do playtest — irmão de 356.
Não adicionar `then.session` ao `playtest` — irmão de 356.
Não implementar `--mood` na sessão — irmão de 356 e 284.
Não inventar chave `probe` no recibo do feel — irmão de 357.
Não adicionar `then.probe` ao `feel` — irmão de 357.
Não importar limiar de buffer no `feel` — irmão de 357 e 349.
Não inventar chave `look` no recibo do art — irmão de 358.
Não nomear `pair` no `art` — irmão de 358 e 352.
Não nomear `LOOK_INTENTS` no `art` — irmão de 358 e 313.
Não inventar chave `table` no recibo do content — irmão de 359.
Não nomear `pair` no `content.scope` além do `listMoods` — irmão de 359 e 352.
Não nomear `SPAWN_INTENTS` no `content` — irmão de 359.
Não inventar chave `size` no recibo do budget — irmão de 360 e 353.
Não nomear `playing.run` no `budget` — irmão de 360 e 349.
Não importar teto de bytes no `budget` — irmão de 360 e 353.
Não inventar chave `sfx` no recibo do roles — irmão de 361 e 355.
Não nomear `peak` no `roles` — irmão de 361 e 355.
Não importar LUFS no `roles` — irmão de 361, 355 e 341.
Não inventar chave `lookAhead` no recibo do feel — irmão de 362 e 351.
Não inventar chave `lean` no recibo do feel — irmão de 362.
Não outro lean na porta — irmão de 362 e 351; a porta não inclina.
Não inventar chave `serve` no recibo do ship — irmão de 363 e 353.
Não inventar chave `banner` no recibo do ship — irmão de 363.
Não outro banner no `play` — irmão de 363 e 342.
Não inventar chave `threat` no recibo do access — irmão de 364 e 348.
Não inventar chave `threatCue` no recibo do access — irmão de 364.
Não pintar o perigo no canvas da pausa — irmão de 364 e 346.
Não inventar chave `beforeunload` no recibo do save — irmão de 365 e 350.
Não inventar chave `unload` no recibo do save — irmão de 365.
Não outro flush só no `pagehide` — irmão de 365 e 172.
Não inventar chave `telegraph` no recibo do art — irmão de 366 e 358.
Não inventar chave `rail` no recibo do art — irmão de 366.
Não nomear `pair` no `art` — irmão de 366, 358 e 352.
Não fatiar `intervalTicks`/`fallSpeed` no `art.rains` — irmão de 366 e 326.
Não inventar chave `rms` no recibo do `sfx info` — irmão de 367.
Não nomear `peak` no `roles` — irmão de 367, 361 e 355.
Não importar LUFS no `sfx info` — irmão de 367 e 355.
Não medir de novo no `sfx info` — irmão de 367; o inspect já mediu.
Não inventar pico no stem do starter — irmão de 367.
Não inventar chave `commands` no recibo do access — irmão de 368 e 348.
Não outro remap na tabela — irmão de 368; a família recado/remap/botão está saturada.
Não pintar as teclas no canvas — irmão de 368.
Não inventar chave `export` no recibo do ship — irmão de 369 e 363.
Não outro banner no `ship` — irmão de 369 e 363.
Não importar teto no `export` — irmão de 369 e 353.
Não inventar chave `percentile` no recibo do budget — irmão de 370 e 349.
Não nomear `p99` no `budget` — irmão de 370.
Não importar limiar de quadro no `budget` — irmão de 370 e 349.
Não nomear `playing.run` no `budget` — irmão de 370, 360 e 349.
Não inventar chave `last_run` no recibo do `note` — irmão de 371 e 340.
Não auto-anexar o last-run no `note` sem `--from-run` — irmão de 371.
Não adicionar `then` ao `note` — irmão de 371 e 209.
Não inventar chave `peak` no recibo do `sfx summary` — irmão de 372 e 367.
Não nomear `peak` no `roles` — irmão de 372, 367, 361 e 355.
Não outro pico no `sfx info` — irmão de 372 e 367.
Não importar LUFS no `sfx summary` — irmão de 372 e 367.
Não inventar chave `pair` no recibo do `start` — irmão de 373 e 352.
Não nomear `pair` no `art` — irmão de 373, 366, 358 e 352.
Não nomear `pair` no `content.scope` além do `listMoods` — irmão de 373, 359 e 352.
Não inventar chave `caption` no recibo do access — irmão de 374 e 368.
Não outra legenda no canvas da pausa — irmão de 374 e 346.
Não inventar chave `sfx` no recibo do `sfx search` — irmão de 375 e 361.
Não nomear `peak` no `sfx search` — irmão de 375, 372 e 367.
Não outra voz no `roles` — irmão de 375 e 361.
Não outro deslocamento no `sfx info` — irmão de 375 e 367.
Não inventar chave `bank` no recibo do feel — irmão de 376 e 351.
Não inventar chave `sit` no recibo do feel — irmão de 376.
Não inventar chave `windup` no recibo do feel — irmão de 376.
Não outro sit da guarda no canvas — irmão de 376; a família coil da guarda está saturada.
Não inventar chave `note` no recibo do playtest — irmão de 377 e 209.
Não adicionar `then` ao `playtest` — irmão de 377 e 209.
Não outro POST de achado no playtest — irmão de 377; a família prefixo no achado está saturada.
Não inventar chave `storage` no recibo do save — irmão de 378 e 365.
Não inventar chave `write` no recibo do save — irmão de 378.
Não chamar a gravação de atômica — irmão de 378; o estágio não é substituição.
Não outra linha de persistência no canvas — irmão de 378 e 350.
Não inventar chave `land` no recibo do feel — irmão de 379 e 376.
Não inventar chave `then.land` no recibo do feel — irmão de 379.
Não usar “senta” no scope do land — irmão de 379 e 376.
Não inventar chave `migrate` no recibo do content — irmão de 380 e 359.
Não inventar chave `schema` no recibo do content — irmão de 380.
Não nomear `pair` no `content.scope` além do `listMoods` — irmão de 380, 373, 359 e 352.
Não outro loader de mesa no content — irmão de 380; a família table/pair está saturada.
Não inventar chave `vignette` no recibo do art — irmão de 381 e 366.
Não inventar chave `halo` no recibo do art — irmão de 381.
Não outro recorte no canvas — irmão de 381; a família look/trilho está saturada.
Não inventar chave `wav` no recibo do roles — irmão de 382 e 361.
Não inventar chave `pcm` no recibo do roles — irmão de 382.
Não nomear `peak` no `roles` — irmão de 382, 372, 367, 361 e 355.
Não outra leitura no sfx info — irmão de 382 e 367.
Não inventar chave `consumer` no recibo do origins — irmão de 383 e 334.
Não inventar chave `consumidor` no recibo do origins — irmão de 383.
Não exigir consumidor para declarar — irmão de 383 e 334; os três rótulos continuam origem, autor e licença.
Não outra menção em CREDITS.md — irmão de 383, 334 e 338.
Não inventar chave `engines` no recibo do doctor — irmão de 384.
Não inventar check `engines` no doctor — irmão de 384.
Não outro Node no `runtime` do guide — irmão de 384 e 153.
Não outro install no doctor — irmão de 384 e 337.
Não inventar chave `file` no recibo do ship — irmão de 385 e 369.
Não outro passo no `ship` — irmão de 385 e 369.
Não outro banner no `ship` — irmão de 385, 369 e 363.
Não outro file:// no prompt do play — irmão de 385 e 342.
Não inventar chave `sidecar` no recibo do `sfx copy` — irmão de 386 e 383.
Não inventar chave `consumer` no `sfx copy` — irmão de 386 e 383.
Não outro crédito no `origins` — irmão de 386, 383 e 334.
Não outra menção em CREDITS.md — irmão de 386, 383, 334 e 338.
Não inventar chave `produção` no recibo do play — irmão de 387.
Não inventar chave `production` no recibo do play — irmão de 387.
Não outro banner no `ship` — irmão de 387, 385, 369 e 363.
Não outro file:// no prompt do play — irmão de 387, 385 e 342.
Não inventar chave `sha256` no recibo do `sfx verify` — irmão de 388.
Não inventar chave `integridade` no recibo do `sfx verify` — irmão de 388.
Não nomear `peak` no `sfx verify` — irmão de 388, 372 e 367.
Não outra leitura no sfx info — irmão de 388, 382 e 367.
Não outro crédito no `sfx copy` — irmão de 388 e 386.
Não inventar chave `processamento` no recibo do `sfx export` — irmão de 389.
Não inventar chave `processing` no recibo do `sfx export` — irmão de 389.
Não nomear `sha256` no `sfx export` — irmão de 389 e 388.
Não outro crédito no `sfx export` — irmão de 389 e 386.
Não inventar chave `mínimo` no recibo do `bar` — irmão de 390.
Não promover `assessed` no `bar` — irmão de 390.
Não outro piso no `next` — irmão de 390.
Não inventar chave `speed` no topo do recibo do `guide` — irmão de 391.
Não adicionar `then.speed` — irmão de 391; `then.speed` é last-run.
Não nomear o relógio no `start.scope` — irmão de 391; um leitor só.
Não promover `executed` nem `observed` no `guide` — irmão de 391.
Não inventar chave `out_of_scope` no recibo do `craft` — irmão de 392.
Não promover `observed` nem `granted` no `craft` — irmão de 392.
Não nomear a saída de escopo no `gate` nem no `review` — irmão de 392; um leitor só.
Não inventar chave `contrast` no recibo do `art` — irmão de 393 e 354.
Não nomear o contraste no `access` além do stub — irmão de 393 e 354.
Não promover `consistent` no `art` — irmão de 393.
Não nomear `LOOK_INTENTS` no `art` — irmão de 393, 358 e 313.
Não inventar chave `substitutions` no recibo do `doctor` — irmão de 394.
Não inventar check `substitutions` no doctor — irmão de 394.
Não nomear as trocas no `init.scope` — irmão de 394; um leitor só.
Não outro engines no doctor — irmão de 394 e 384.
Não inventar chave `scripts` no recibo do `discover` — irmão de 395.
Não nomear os scripts no `next.scope` — irmão de 395; um leitor só.
Não promover `observed` nem `granted` no `review` — irmão de 395.
Não outro validador no `discover` — irmão de 395 e 206.
Não inventar chave `type` no recibo do `init` — irmão de 396.
Não nomear o módulo no `start.scope` nem no `doctor` — irmão de 396; um leitor só.
Não outro engines no `init` — irmão de 396 e 384.
Não outras substituições no `init.scope` — irmão de 396 e 394.
Não inventar chave `gate` no recibo do `gate` — irmão de 397.
Não nomear o gate no `next.scope` nem no `craft` — irmão de 397; um leitor só.
Não nomear a saída de escopo no `gate` — irmão de 397 e 392.
Não promover `granted` no `gate` — irmão de 397.
Não inventar chave `serve` no recibo do `scan` — irmão de 398.
Não nomear o serve no `play.scope` nem no `next.scope` — irmão de 398; um leitor só.
Não outro Abrir no `scan` — irmão de 398 e 342.
Não outra produção no `scan` — irmão de 398 e 387.
Não inventar chave `HOST` no recibo do invite — irmão de 399.
Não inventar chave `bind` no recibo do invite — irmão de 399.
Não nomear o bind no `play.scope` nem no `playtest` nem no `next` nem no `ship` — irmão de 399; um leitor só.
Não outra produção no invite — irmão de 399 e 387.
Não outro serve no invite — irmão de 399 e 398.
Não promover `outsider` no invite — irmão de 399.
Não inventar chave `publicar` no recibo do `template` — irmão de 400.
Não inventar chave `template` no recibo do `template` — irmão de 400.
Não nomear a publicação no `finish` nem no `next` nem no `ship` — irmão de 400; um leitor só.
Não outro aaa no `finish` — irmão de 400.
Não promover `elsewhere` no `template` — irmão de 400.
Não inventar chave `audit` no recibo do `documentation` — irmão de 401.
Não nomear o audit no `scan.scope` nem no `next.scope` nem no `template` — irmão de 401; um leitor só.
Não outro serve no `context` — irmão de 401 e 398.
Não promover `executed` no `documentation` — irmão de 401.
Não inventar chave `process` no recibo do `continuity` — irmão de 402.
Não inventar chave `poc` no recibo do `continuity` — irmão de 402.
Não nomear a PoC no `documentation` nem no `scan.scope` nem no `next.scope` — irmão de 402; um leitor só.
Não outro audit no `context` — irmão de 402 e 401.
Não promover `executed` no `continuity` — irmão de 402.
Não inventar chave `agents` no recibo do `agent_context` — irmão de 403.
Não inventar chave `aaa` no recibo do `agent_context` — irmão de 403.
Não nomear o AAA no `scan.scope` nem no `next.scope` nem no `template` nem no `start` — irmão de 403; um leitor só.
Não outra PoC no `continuity` — irmão de 403 e 402.
Não promover `enough` nem `consistent` no `agent_context` — irmão de 403.
Não inventar chave `checklist` no recibo do `finish` — irmão de 404.
Não nomear o checklist no `template` nem no `next.scope` nem no `documentation` nem no `agent_context` — irmão de 404; um leitor só.
Não outro AAA no `finish` — irmão de 404, 403 e 400.
Não outra publicação no `finish` — irmão de 404 e 400.
Não promover `executed` no `finish` — irmão de 404.
Não inventar chave `promove` no recibo do `production_bar` — irmão de 405.
Não nomear a promoção no `bar.scope` nem no `next.scope` nem no `finish` — irmão de 405; um leitor só.
Não outro mínimo no `production_bar` — irmão de 405 e 390.
Não promover `assessed` no `production_bar` — irmão de 405 e 390.
Não inventar chave `navegador` no recibo do `packs` — irmão de 406.
Não nomear o navegador no `verify` nem no `next.scope` nem no `play` nem no `discover` — irmão de 406; um leitor só.
Não outro Abrir no `packs` — irmão de 406 e 342.
Não promover `verified` no `packs` — irmão de 406.
Não inventar chave `ação` no recibo do `next` — irmão de 407.
Não nomear a ação no `continuity` nem no `documentation` nem no `finish` nem no `scan.scope` — irmão de 407; um leitor só.
Não outra PoC no `next` — irmão de 407 e 402.
Não promover `executed` no `next` — irmão de 407.
Não inventar chave `mede` no recibo do `record` — irmão de 408.
Não inventar chave `quality` no recibo do `record` — irmão de 408.
Não nomear a medição no `verify` nem no `budget` nem no `next.scope` nem no `production_bar` nem no `feel` — irmão de 408; um leitor só.
Não outra ação no `record` — irmão de 408 e 407.
Não promover `measured` no `record` — irmão de 408.
Não inventar chave `mérito` no recibo do `check-plan` — irmão de 409.
Não inventar chave `plan` no recibo do `check-plan` — irmão de 409.
Não nomear o mérito no `next.scope` nem no `continuity` nem no `record` nem no `documentation` — irmão de 409; um leitor só.
Não outra PoC no `check-plan` — irmão de 409 e 402.
Não outra ação no `check-plan` — irmão de 409 e 407.
Não promover `verified` no `check-plan` — irmão de 409.
Não inventar chave `criatividade` no recibo do `verify` — irmão de 410.
Não inventar chave `creativity` no recibo do `verify` — irmão de 410.
Não nomear a criatividade no `record` nem no `check-plan` nem no `next.scope` nem no `template` — irmão de 410; um leitor só.
Não outro unitário no `verify` — irmão de 410 e 406.
Não outra medição no `verify` — irmão de 410 e 408.
Não promover `verified` no `verify` — irmão de 410.
Não inventar chave `verified` no recibo do `verify` — irmão de 411.
Não nomear a verificação no `verify.scope` nem no `record` nem no `next.scope` nem no `check-plan` — irmão de 411; um leitor só.
Não outra criatividade no `capabilities_scope` — irmão de 411 e 410.
Não promover `verified` como status — irmão de 411 e 410.
Não inventar chave `leitura` no recibo do `git` — irmão de 412.
Não inventar chave `hash` no recibo do `git` — irmão de 412.
Não nomear a leitura no `verify.scope` nem no `next.scope` nem no `documentation` nem no `scan.scope` — irmão de 412; um leitor só.
Não outra verificação no `git` — irmão de 412 e 411.
Não promover `verified` no `git` — irmão de 412.
Não inventar chave `exemplo` no recibo do `doctor` — irmão de 413.
Não inventar chave `fantasia` no recibo do `doctor` — irmão de 413.
Não nomear o exemplo no `next.scope` nem no `guide.scope` nem no `play` nem no `git` — irmão de 413; um leitor só.
Não outro `sem destino` no doctor — irmão de 413 e 332.
Não outro engines no `then.guide` — irmão de 413 e 384.
Não promover `executed` no `doctor` — irmão de 413.
Não inventar chave `julgamento` no recibo do `version` — irmão de 414.
Não inventar chave `judgment` no recibo do `version` — irmão de 414.
Não nomear o julgamento no `record.scope` nem no `verify.scope` nem no `git` nem no `next.scope` — irmão de 414; um leitor só.
Não outra medição no `version` — irmão de 414 e 408.
Não outra leitura no `version` — irmão de 414 e 412.
Não promover `verified` no `version` — irmão de 414.
Não inventar chave `reuso` no recibo do `roles --fill` — irmão de 415.
Não inventar chave `reuse` no recibo do `roles --fill` — irmão de 415.
Não nomear o reuso no `roles` nem no `origins` nem no `next.scope` nem no `record` — irmão de 415; um leitor só.
Não outro consumidor no `roles --fill` — irmão de 415.
Não promover `heard` no `roles --fill` — irmão de 415.
Não inventar chave `daemon` no recibo do `audit` — irmão de 416.
Não inventar chave `hook` no recibo do `audit` — irmão de 416.
Não nomear o daemon no `documentation` nem no `scan.scope` nem no `next.scope` — irmão de 416; um leitor só.
Não outro audit no `scan.scope` — irmão de 416 e 401.
Não promover `executed` no `audit` — irmão de 416.
Não inventar chave `progresso` no recibo do `context` — irmão de 417.
Não inventar chave `progress` no recibo do `context` — irmão de 417.
Não nomear o progresso no `production_bar` nem no `finish` nem no `template` nem no `next.scope` — irmão de 417; um leitor só.
Não outro audit no `context.scope` — irmão de 417 e 401.
Não outra PoC no `context.scope` — irmão de 417 e 402.
Não promover `executed` no `context` — irmão de 417.
Não inventar chave `ouve` no recibo do `studio_assets` — irmão de 418.
Não inventar chave `heard` no recibo do `studio_assets` — irmão de 418.
Não nomear a escuta no `roles` nem no `context.scope` nem no `next.scope` nem no `sfx search` — irmão de 418; um leitor só.
Não outro reuso no `studio_assets` — irmão de 418 e 415.
Não promover `heard` no `studio_assets` — irmão de 418.
Não inventar chave `tokens` no recibo da `art_direction` — irmão de 419.
Não inventar chave `token` no recibo da `art_direction` — irmão de 419.
Não nomear os tokens no `scan.scope` nem no `art` nem no `next.scope` nem no `documentation` — irmão de 419; um leitor só.
Não outro serve na `art_direction` — irmão de 419 e 398.
Não promover `consistent` na `art_direction` — irmão de 419.
Não inventar chave `dependências` no recibo da `architecture` — irmão de 420.
Não inventar chave `dependencies` no recibo da `architecture` — irmão de 420.
Não nomear as dependências no `scan.scope` nem na `art_direction` nem no `context.scope` nem no `next.scope` — irmão de 420; um leitor só.
Não outros tokens na `architecture` — irmão de 420 e 419.
Não promover `executed` na `architecture` — irmão de 420.
Não inventar chave `inexistente` no recibo do `coverage` — irmão de 421.
Não inventar chave `ausência` no recibo do `coverage` — irmão de 421.
Não nomear a inexistência no `scan.scope` nem na `art_direction` nem na `architecture` nem no `audit` nem no `next.scope` — irmão de 421; um leitor só.
Não outro daemon no `coverage` — irmão de 421 e 416.
Não promover `executed` no `coverage` — irmão de 421.
Não inventar chave `capacidade` no recibo da `platform` — irmão de 422.
Não inventar chave `aprova` no recibo da `platform` — irmão de 422.
Não nomear a capacidade no `packs.scope` nem no `next.scope` nem no `play` nem no `context.scope` — irmão de 422; um leitor só.
Não outro navegador na `platform` — irmão de 422 e 406.
Não promover `verified` na `platform` — irmão de 422 e 406.
Não inventar chave `onboarding` no recibo do passo de jogar — irmão de 423.
Não inventar chave `mural` no recibo do passo de jogar — irmão de 423.
Não nomear o onboarding no `guide.scope` nem no `play.scope` nem no `start.scope` nem no `next.scope` — irmão de 423; um leitor só.
Não outro relógio no passo de jogar — irmão de 423 e 391.
Não promover `executed` no passo de jogar — irmão de 423.
Não inventar chave `screenshot` no recibo do passo de gravar — irmão de 424.
Não inventar chave `comprovação` no recibo do passo de gravar — irmão de 424.
Não nomear o screenshot no `feel.scope` nem no `note` nem no `guide.scope` nem no `play.scope` nem no `record` nem no `playtest` nem no `next.scope` — irmão de 424; um leitor só.
Não outro onboarding no passo de gravar — irmão de 424 e 423.
Não promover `executed` no passo de gravar — irmão de 424.
Não nomear onboarding no passo 1 — irmão de 423 e 424; família dos passos saturada.
Não outra frase nos três passos do `guide` — irmão de 423, 424 e 429; cada passo já nomeia uma recusa.
Não inventar chave `extração` no recibo do `genre` — irmão de 425.
Não inventar chave `extração` no recibo da `platform` — irmão de 425 e 422.
Não nomear a extração no `packs.scope` nem na `platform` nem no `next.scope` nem no `play` nem no `context.scope` — irmão de 425; um leitor só.
Não outra capacidade no `genre` — irmão de 425 e 422.
Não promover `verified` no `genre` — irmão de 425 e 422.
Não inventar chave `api` no recibo da capacidade mencionada — irmão de 426.
Não inventar chave `API` no recibo da capacidade mencionada — irmão de 426.
Não nomear a API no `capabilities_scope` nem no `context.scope` nem no `next.scope` nem no `play` nem no nome desconhecido — irmão de 426; um leitor só.
Não outra verificação na menção — irmão de 426 e 411.
Não promover `verified` na menção — irmão de 426 e 411.
Não inventar chave `criação` no recibo da `proposal` — irmão de 427.
Não inventar chave `cria` no recibo da `proposal` — irmão de 427.
Não nomear a criação no `next.scope` nem nas `alternatives` nem no `context.scope` nem no `guide` nem no `init` — irmão de 427; um leitor só.
Não outra ação na `proposal` — irmão de 427 e 407.
Não promover `executed` na `proposal` — irmão de 427.
Não inventar chave `silêncio` no recibo do item do `gate` — irmão de 428.
Não inventar chave `aprovação` no recibo do item do `gate` — irmão de 428.
Não nomear o silêncio no `gate.scope` nem no `next` nem no `check-plan` nem no `craft` — irmão de 428; um leitor só.
Não outra linha no item do `gate` — irmão de 428 e 397.
Não promover `granted` no item do `gate` — irmão de 428.
Não inventar chave `abertura` no recibo do passo de abrir — irmão de 429.
Não inventar chave `abre` no recibo do passo de abrir — irmão de 429.
Não nomear a abertura no `guide.scope` nem no `play.scope` nem no `start.scope` nem no `init` nem no `next.scope` — irmão de 429; um leitor só.
Não outro onboarding no passo de abrir — irmão de 429 e 423.
Não outro screenshot no passo de abrir — irmão de 429 e 424.
Não promover `executed` no passo de abrir — irmão de 429.
Não inventar chave `escada` no recibo do item do `craft` — irmão de 430.
Não inventar chave `gates` no recibo do item do `craft` — irmão de 430.
Não nomear a escada no `craft.scope` nem no `gate` nem no `next` nem no `bar` — irmão de 430; um leitor só.
Não outra saída de escopo no item do `craft` — irmão de 430 e 392.
Não promover `observed` nem `granted` no item do `craft` — irmão de 430.
Não outra frase em `craft.scope` — irmão de 392.
Não inventar chave `prazos` no recibo do item do `bar` — irmão de 431.
Não inventar chave `prazo` no recibo do item do `bar` — irmão de 431.
Não nomear os prazos no `bar.scope` nem no `production_bar.scope` nem no `next` nem no `context.scope` — irmão de 431; um leitor só.
Não outro mínimo no item do `bar` — irmão de 431 e 390.
Não promover `assessed` no item do `bar` — irmão de 431.
Não outra frase em `bar.scope` — irmão de 390.
Não inventar chave `motor` no recibo do `then` — irmão de 432.
Não inventar chave `fábrica` no recibo do `then` — irmão de 432.
Não nomear o motor no `doctor.scope` nem no `init` nem no `guide` nem no `next` — irmão de 432; um leitor só.
Não outro exemplo no `then.scope` — irmão de 432 e 413.
Não promover `executed` no `then` — irmão de 432.
Não quarta frase em `doctor.scope` — irmão de 413, 394 e 384.
Não inventar chave `fabricação` no recibo da alternativa — irmão de 433.
Não inventar chave `tarefa` no recibo da alternativa — irmão de 433.
Não nomear a fabricação no `proposal` nem no `next.scope` nem no `check-plan` nem no `context.scope` — irmão de 433; um leitor só.
Não outra criação na alternativa — irmão de 433 e 427.
Não promover `executed` na alternativa — irmão de 433.
Não outro `process.md` no `next.scope` — irmão de 407.
Não inventar chave `diversão` no recibo do comando do `verify` — irmão de 434.
Não inventar chave `fun` no recibo do comando do `verify` — irmão de 434.
Não nomear a diversão no `verify.scope` nem no `capabilities_scope` nem no `record` nem no `next` nem no `doctor.then` — irmão de 434; um leitor só.
Não outra criatividade no item do comando — irmão de 434 e 410.
Não promover `verified` no item do comando — irmão de 434.
Não terceira frase em `verify.scope` — irmão de 410.
Não outro `ambition.md` no `then` — irmão de 432.
Não inventar chave `licença` no recibo da área de proveniência — irmão de 435.
Não inventar chave `license` no recibo da área de proveniência — irmão de 435.
Não nomear a licença no `origins` nem no `scan.scope` nem no `gate` nem no `next` nem em `art_direction` nem em `architecture` — irmão de 435; um leitor só.
Não outro consumidor na área de proveniência — irmão de 435.
Não outro CREDITS na área de proveniência — irmão de 435 e 334.
Não promover `granted` nem `validated` na área de proveniência — irmão de 435.
Não outra frase em `art_direction.scope` — irmão de 419.
Não outra frase em `architecture.scope` — irmão de 420.
Não inventar chave `pessoas` no recibo da área de QA — irmão de 436.
Não inventar chave `censo` no recibo da área de QA — irmão de 436.
Não nomear as pessoas no `playtest` nem no `record` nem no `scan.scope` nem no `next` nem em `provenance` — irmão de 436; um leitor só.
Não outra licença na área de QA — irmão de 436 e 435.
Não outro onboarding na área de QA — irmão de 436 e 423.
Não outra medição na área de QA — irmão de 436 e 408.
Não promover `outsider` na área de QA — irmão de 436.
Não outra frase em `provenance.scope` — irmão de 435.
Não inventar chave `qualidade` no recibo do item do `discover` — irmão de 437.
Não inventar chave `quality` no recibo do item do `discover` — irmão de 437.
Não nomear a qualidade no `review.scope` nem no `scan.scope` nem no `documentation` nem no `next` — irmão de 437; um leitor só.
Não outro script no item do `discover` — irmão de 437 e 395.
Não outra criatividade no item do `discover` — irmão de 437 e 410.
Não outra criação no item do `discover` — irmão de 437 e 427.
Não promover `verified` no item do `discover` — irmão de 437.
Não outra frase em `review.scope` — irmão de 395.
Não inventar chave `animação` no recibo do anexo do `record` — irmão de 438.
Não inventar chave `controle` no recibo do anexo do `record` — irmão de 438.
Não nomear a animação no `record.scope` nem no passo de gravar nem no `feel` nem no `next` — irmão de 438; um leitor só.
Não outro screenshot no anexo do `record` — irmão de 438 e 424.
Não outra medição no anexo do `record` — irmão de 438 e 408.
Não promover `felt` nem `observed` no anexo — irmão de 438.
Não outra frase em `record.scope` — irmão de 408.
Não inventar chave `paleta` no recibo do item do `art` — irmão de 439.
Não inventar chave `sistema` no recibo do item do `art` — irmão de 439.
Não nomear a paleta no `art.scope` nem na `art_direction` nem no `scan.scope` nem no `next` — irmão de 439; um leitor só.
Não outros tokens no item da paleta — irmão de 439 e 419.
Não outro look no item da paleta — irmão de 439 e 328.
Não promover `consistent` no item da paleta — irmão de 439.
Não inventar chave `publisher` no recibo do atalho da skill — irmão de 440.
Não inventar chave `orçamento` no recibo do atalho da skill — irmão de 440.
Não nomear o publisher no `doctor.scope` nem no `then` nem no `guide` nem no `init` nem no `next` — irmão de 440; um leitor só.
Não outro motor no atalho da skill — irmão de 440 e 432.
Não outro exemplo no atalho da skill — irmão de 440 e 413.
Não promover `executed` no atalho — irmão de 440.
Não inventar chave `quantidade` no recibo do item do `roles` — irmão de 441.
Não inventar chave `arquivos` no recibo do item do `roles` — irmão de 441.
Não nomear a quantidade no `roles.scope` nem no `roles --fill` nem no `feel` nem no `next` — irmão de 441; um leitor só.
Não outra soma no item do papel — irmão de 441 e 328.
Não outro PCM no item do papel — irmão de 441.
Não promover `heard` no item do papel — irmão de 441.
Não inventar chave `intenções` no recibo do candidato do `scan` — irmão de 442.
Não inventar chave `autoria` no recibo do candidato do `scan` — irmão de 442.
Não nomear as intenções no `scan.scope` nem no `audit` nem no `coverage` nem no `documentation` nem no `next` — irmão de 442; um leitor só.
Não outra qualidade no candidato — irmão de 442 e 437.
Não outro daemon no candidato — irmão de 442 e 416.
Não promover `executed` no candidato — irmão de 442.
Não inventar chave `certificação` no recibo do item do `access` — irmão de 443.
Não inventar chave `gate` no recibo do item do `access` — irmão de 443.
Não nomear a certificação no `access.scope` nem no `gate` nem no `verify` nem no `next` — irmão de 443; um leitor só.
Não outro foco no item da opção — irmão de 443.
Não outra legenda no item da opção — irmão de 443.
Não promover `verified` no item da opção — irmão de 443.
Não inventar chave `autor` no recibo do item da observação — irmão de 444.
Não inventar chave `jogador` no recibo do item da observação — irmão de 444.
Não nomear o autor no `feel.scope` nem no `note` nem no `playtest` nem no `record` nem no `next` — irmão de 444; um leitor só.
Não outro screenshot no item da observação — irmão de 444 e 424.
Não outra animação no item da observação — irmão de 444 e 438.
Não promover `felt` nem `observed` no item da observação — irmão de 444.
Não inventar chave `volume` no recibo do item da chuva — irmão de 445.
Não inventar chave `mesa` no recibo do item da chuva — irmão de 445.
Não nomear o volume no `art.scope` nem na `art_direction` nem no `scan` nem no `content` nem no `next` — irmão de 445; um leitor só.
Não outra paleta no item da chuva — irmão de 445 e 439.
Não outro look no item da chuva — irmão de 445 e 328.
Não promover `consistent` no item da chuva — irmão de 445.
Não inventar chave `dispensa` no recibo do critério do `gate` — irmão de 446.
Não inventar chave `must_meet` no recibo do critério do `gate` — irmão de 446.
Não nomear a dispensa no `gate.scope` nem no `gates[n]` nem no `next` nem no `check-plan` nem no `craft` — irmão de 446; um leitor só.
Não outro silêncio no critério — irmão de 446 e 428.
Não outra linha no critério — irmão de 446 e 428.
Não promover `granted` no critério — irmão de 446.
Não inventar chave `universais` no recibo do item da constante — irmão de 447.
Não inventar chave `lei` no recibo do item da constante — irmão de 447.
Não nomear o universal no `feel.scope` nem nas `observations` nem no `note` nem no `next` — irmão de 447; um leitor só.
Não outro autor no item da constante — irmão de 447 e 444.
Não outro land no item da constante — irmão de 447.
Não promover `felt` no item da constante — irmão de 447.
Não inventar chave `dimensão` no recibo do problema do `bar` — irmão de 448.
Não inventar chave `dez` no recibo do problema do `bar` — irmão de 448.
Não nomear a dimensão no `bar.scope` nem em `dimensions[n]` nem no `production_bar` nem no `next` — irmão de 448; um leitor só.
Não outro prazo no problema — irmão de 448 e 431.
Não outro mínimo no problema — irmão de 448 e 405.
Não promover `assessed` no problema — irmão de 448.
Não inventar chave `escopo` no recibo do problema do `gate` — irmão de 449.
Não inventar chave `dispensa` no recibo do problema do `gate` — irmão de 449 e 446.
Não nomear o escopo no `gate.scope` nem em `gates[n]` nem em `criteria[n]` nem no `next` nem no `check-plan` nem no `craft` — irmão de 449; um leitor só.
Não outra dispensa no critério — irmão de 449 e 446.
Não outro silêncio no problema — irmão de 449 e 428.
Não promover `granted` no problema — irmão de 449.
Não inventar chave `rótulos` no recibo do problema do `origins` — irmão de 450.
Não inventar chave `sidecar` no recibo do problema do `origins` — irmão de 450.
Não nomear os rótulos no `origins.scope` nem na `provenance` nem no `scan` nem no `gate` nem no `next` — irmão de 450; um leitor só.
Não outro consumidor no problema — irmão de 450 e 383.
Não outra mídia no problema — irmão de 450 e 338.
Não promover `granted` nem `validated` no problema — irmão de 450.
Não inventar chave `definição` no recibo do problema do `craft` — irmão de 451.
Não inventar chave `critério` no recibo do problema do `craft` — irmão de 451.
Não nomear a definição no `craft.scope` nem em `checks[n]` nem no `gate` nem no `next` nem no `bar` — irmão de 451; um leitor só.
Não outra escada no problema — irmão de 451 e 430.
Não outra saída de escopo no problema — irmão de 451 e 427.
Não promover `observed` nem `granted` no problema — irmão de 451.
Não inventar chave `ausência` no recibo do check do `doctor` — irmão de 452.
Não inventar chave `evidência` no recibo do check do `doctor` — irmão de 452.
Não nomear a ausência no `doctor.scope` nem no `then` nem nos `skill_targets` nem no `next` nem no `guide` nem no `init` — irmão de 452; um leitor só.
Não outro publisher no check — irmão de 452 e 440.
Não outro motor no check — irmão de 452 e 432.
Não promover `executed` no check — irmão de 452.
Não inventar chave `fila` no recibo da fonte do continuity — irmão de 453.
Não inventar chave `backlog` no recibo da fonte do continuity — irmão de 453.
Não nomear a fila no `continuity.scope` nem no `documentation` nem no `next` nem no `check-plan` nem em `scan.continuity_sources` — irmão de 453; um leitor só.
Não outra PoC no item da fonte — irmão de 453 e 402.
Não outro process no item da fonte — irmão de 453 e 402.
Não promover `executed` nem inventar `next_step` no item da fonte — irmão de 453.
Não outra frase em `continuity.scope` — irmão de 402.
Não inventar chave `mecânica` no recibo da menção de gênero — irmão de 454.
Não inventar chave `regra` no recibo da menção de gênero — irmão de 454.
Não nomear a mecânica no `packs.genre.scope` nem no `packs.scope` nem no `context.scope` nem no `next` nem em `packs.genre.mentions` — irmão de 454; um leitor só.
Não outra extração no item da menção — irmão de 454 e 425.
Não outra capacidade no item da menção — irmão de 454 e 426.
Não classificar nem carregar o pacote a partir da menção — irmão de 454.
Não inventar chave `acidente` no recibo do issue da coverage — irmão de 455.
Não inventar chave `falha` no recibo do issue da coverage — irmão de 455.
Não nomear o acidente no `coverage.scope` nem no `scan.scope` nem no `audit` nem no `next` nem no `context.scope` — irmão de 455; um leitor só.
Não outra inexistência no item do issue — irmão de 455 e 421.
Não outra mecânica no item do issue — irmão de 455 e 454.
Não promover inventário completo a partir do issue — irmão de 455.
Não inventar chave `identidade` no recibo da árvore do ship — irmão de 456.
Não inventar chave `entrega` no recibo da árvore do ship — irmão de 456.
Não nomear a identidade no `ship.scope` nem no `next` nem no `play` nem no `ship_tree` cru — irmão de 456; um leitor só.
Não outro file:// na árvore — irmão de 456.
Não outro export na árvore — irmão de 456.
Não quinta frase em `ship.scope` — irmão de 456.
Não promover `elsewhere` nem `shipped` na árvore — irmão de 456.
Não inventar chave `determinismo` no recibo da capacidade desconhecida — irmão de 457.
Não inventar chave `ciclo` no recibo da capacidade desconhecida — irmão de 457.
Não nomear o determinismo na menção nem no `capabilities_scope` nem no `context.scope` nem no `next` nem no `production_bar` nem no `bar` — irmão de 457; um leitor só.
Não outra API no item desconhecido — irmão de 457 e 426.
Não outra identidade no item desconhecido — irmão de 457 e 456.
Não promover `verified` na capacidade desconhecida — irmão de 457.
Não inventar chave `editor` no recibo do artifact do ship — irmão de 458.
Não inventar chave `exportado` no recibo do artifact do ship — irmão de 458.
Não nomear o editor no `ship.scope` nem no `tree` nem no `next` nem no `play` nem no `ship_artifact` cru — irmão de 458; um leitor só.
Não outra identidade no artifact — irmão de 458 e 456.
Não outro file:// no artifact — irmão de 458 e 456.
Não quinta frase em `ship.scope` — irmão de 458 e 456.
Não promover `elsewhere` nem `shipped` no artifact — irmão de 458.
Não inventar chave `cinco` no recibo da conta do playtest — irmão de 459.
Não inventar chave `playtesters` no recibo da conta do playtest — irmão de 459.
Não nomear o cinco no `playtest.scope` nem no `invite` nem no `next` nem no `note` nem no `last_run_tally` cru — irmão de 459; um leitor só.
Não outro recado na conta — irmão de 459.
Não outra simulação na conta — irmão de 459.
Não levar `candidate_tally` à faixa do convite — irmão de 459.
Não promover `outsider` nem `observed` na conta — irmão de 459.
Não inventar chave `linhas` no recibo do rascunho da coverage — irmão de 460.
Não inventar chave `certifica` no recibo do rascunho da coverage — irmão de 460.
Não nomear as linhas no `coverage.scope` nem no `scan.scope` nem em `issues[n]` nem no `audit` nem no `next` nem no `context.scope` — irmão de 460; um leitor só.
Não outro acidente no rascunho — irmão de 460 e 455.
Não outra inexistência no rascunho — irmão de 460 e 421.
Não outra qualidade no rascunho — irmão de 460 e 437.
Não promover inventário completo a partir do rascunho — irmão de 460.
Não inventar chave `semântico` no recibo do metadata_issues — irmão de 461.
Não inventar chave `PRD` no recibo do metadata_issues — irmão de 461.
Não nomear o semântico no `check-plan.scope` nem no `context.scope` nem no `next` — irmão de 461; um leitor só.
Não outro mérito no issue — irmão de 461 e 409.
Não outras linhas no issue — irmão de 461 e 460.
Não promover `verified` no metadata_issues — irmão de 461.
Não inventar chave `aperto` no recibo da curva do playtest — irmão de 462.
Não inventar chave `curva` no recibo da curva do playtest — irmão de 462.
Não nomear o aperto no `playtest.scope` nem no `content.scope` nem no `candidate_tally` nem no `invite` nem no `next` nem no `last_run_curve` cru — irmão de 462; um leitor só.
Não outro cinco na curva — irmão de 462 e 459.
Não outra simulação na curva — irmão de 462.
Não levar curva à faixa do convite — irmão de 462.
Não promover `outsider` nem `observed` na curva — irmão de 462.
Não inventar chave `precedência` no recibo do conflito do bar — irmão de 463.
Não inventar chave `conflito` no recibo do conflito do bar — irmão de 463.
Não nomear a precedência no `bar.scope` nem em `problems[n]` nem em `dimensions[n]` nem no `production_bar` nem no `next` nem no `bar_declaration` cru — irmão de 463; um leitor só.
Não outra dimensão no conflito — irmão de 463 e 448.
Não outro prazo no conflito — irmão de 463.
Não promover `assessed` no conflito — irmão de 463.
Não inventar chave `improvisar` no recibo do sfx import — irmão de 464.
Não inventar chave `licença` no recibo do sfx import — irmão de 464.
Não nomear a improvisação no `sfx seed` nem no `next` nem no `summarize` nem no `roles` nem no `sfx copy` — irmão de 464; um leitor só.
Não outro processamento no import — irmão de 464.
Não outra integridade no import — irmão de 464.
Não promover `heard` no import — irmão de 464.
Não inventar chave `lixo` no recibo do sfx info do stem — irmão de 465.
Não inventar chave `papel` no recibo do sfx info do stem — irmão de 465.
Não nomear o lixo no `local_stems` cru nem na ficha ausente nem no catálogo nem no `summarize` nem no `sfx search` nem no `sfx import` — irmão de 465; um leitor só.
Não outro pico na ficha do stem — irmão de 465.
Não outra improvisação na ficha do stem — irmão de 465 e 464.
Não promover `heard` na ficha do stem — irmão de 465.
Não inventar chave `telemetria` no recibo da área do runbook — irmão de 466.
Não inventar chave `consentimento` no recibo da área do runbook — irmão de 466.
Não nomear a telemetria no `scan.scope` nem no `qa` nem no `architecture` nem no `ship` nem no `next` — irmão de 466; um leitor só.
Não outras pessoas no runbook — irmão de 466 e 419.
Não outro editor no runbook — irmão de 466 e 458.
Não promover `elsewhere` na área do runbook — irmão de 466.
Não inventar chave `histórico` no recibo da área do decisions — irmão de 467.
Não inventar chave `decisão` no recibo da área do decisions — irmão de 467.
Não nomear o histórico no `scan.scope` nem no `architecture` nem no `runbook` nem no `next` — irmão de 467; um leitor só.
Não outra telemetria no decisions — irmão de 467 e 466.
Não outras dependências no decisions — irmão de 467 e 421.
Não promover `executed` na área do decisions — irmão de 467.
Não inventar chave `divertido` no recibo da área do gdd — irmão de 468.
Não inventar chave `imersivo` no recibo da área do gdd — irmão de 468.
Não nomear o divertido no `scan.scope` nem no `decisions` nem no `mda` nem no `feel` nem no `next` — irmão de 468; um leitor só.
Não outro histórico no gdd — irmão de 468 e 467.
Não outra diversão no gdd — irmão de 468 e 435.
Não promover `felt` na área do gdd — irmão de 468.
Não inventar chave `pontuação` no recibo da área do mda — irmão de 469.
Não inventar chave `diversão` no recibo da área do mda — irmão de 469.
Não nomear a pontuação no `scan.scope` nem no `gdd` nem no `feel` nem no `verify` nem no `next` — irmão de 469; um leitor só.
Não outro divertido no mda — irmão de 469 e 468.
Não outra diversão no mda — irmão de 469 e 435.
Não promover `felt` na área do mda — irmão de 469.
Não inventar chave `público` no recibo da área do vision — irmão de 470.
Não inventar chave `audiência` no recibo da área do vision — irmão de 470.
Não nomear o público no `scan.scope` nem no `gdd` nem no `mda` nem no `feel` nem no `next` — irmão de 470; um leitor só.
Não outra pontuação no vision — irmão de 470 e 469.
Não outro divertido no vision — irmão de 470 e 468.
Não promover `felt` na área do vision — irmão de 470.
Não inventar chave `marketing` no recibo do item da escala — irmão de 471.
Não inventar chave `campanha` no recibo do item da escala — irmão de 471.
Não nomear o marketing no `read_scale.scope` nem no `scan.scope` nem no `vision` nem no `context.scope` nem no `next` — irmão de 471; um leitor só.
Não outro AAA no item da escala — irmão de 471 e 404.
Não outro adjetivo no item da escala — irmão de 471.
Não vazar `scope` no `source` cru do `read_scale` — irmão de 471 e 416.
Não promover `felt` no item da escala — irmão de 471.
Não inventar chave `opção` no recibo do item do access — irmão de 472.
Não inventar chave `consumidor` no recibo do item do access — irmão de 472 e 416.
Não nomear a opção no `access.scope` nem no `origins` nem no `gate` nem no `verify` nem no `next` — irmão de 472; um leitor só.
Não outra certificação no item do access — irmão de 472 e 443.
Não promover `verified` no item do access — irmão de 472.
Não inventar chave `genérico` no recibo do item do commands — irmão de 473.
Não inventar chave `referência` no recibo do item do commands — irmão de 473.
Não nomear o genérico no `commands.scope` nem no `context` nem no `doctor.then` nem no `next` — irmão de 473; um leitor só.
Não outra opção no item do commands — irmão de 473 e 472.
Não promover `felt` no item do commands — irmão de 473.
Não inventar chave `listagem` no recibo do item do discover — irmão de 474.
Não inventar chave `tipo` no recibo do item do discover — irmão de 474.
Não nomear a listagem no `review` nem no `review_item` nem no `next` nem no `context` — irmão de 474; um leitor só.
Não outra qualidade no item do --plain — irmão de 474 e 409.
Não promover `felt` no item do discover — irmão de 474.
Não inventar chave `própria` no recibo do item do pin — irmão de 475.
Não inventar chave `sobrescrita` no recibo do item do pin — irmão de 475.
Não nomear a própria no `pin.scope` nem no `unpin.scope` nem no `created` nem no `commands` nem no `next` — irmão de 475; um leitor só.
Não outra listagem no item do pin — irmão de 475 e 474.
Não promover `felt` no item do pin — irmão de 475.
Não inventar chave `preenchida` no recibo do módulo do context — irmão de 476.
Não inventar chave `starter` no recibo do módulo do context — irmão de 476.
Não nomear a preenchida no `context.scope` nem no `documentation` nem no `workspace_module` cru nem no `next` nem no `init` — irmão de 476; um leitor só.
Não outra própria no módulo — irmão de 476 e 475.
Não promover `felt` no módulo do context — irmão de 476.
Não inventar chave `regras` no recibo do delivery_review — irmão de 477.
Não inventar chave `templates` no recibo do delivery_review — irmão de 477.
Não nomear as regras no `context.scope` nem no `documentation` nem no `finish` nem no `next` nem no `continuity` — irmão de 477; um leitor só.
Não outra preenchida no delivery_review — irmão de 477 e 476.
Não promover `verified` no delivery_review — irmão de 477.
Não inventar chave `inventado` no recibo do workspace — irmão de 478.
Não inventar chave `lacuna` no recibo do workspace — irmão de 478.
Não nomear o inventado no `context.scope` nem no `documentation` nem no `workspace_module` nem no `delivery_review` nem no `next` nem no `workspace_profile` cru — irmão de 478; um leitor só.
Não outras regras no workspace — irmão de 478 e 477.
Não promover `felt` no workspace — irmão de 478.
Não inventar chave `receita` no recibo do prompt do continuity — irmão de 479.
Não inventar chave `status` no recibo do prompt do continuity — irmão de 479.
Não nomear a receita no `continuity.scope` nem no `context.scope` nem no `documentation` nem no `delivery_review` nem no `next` nem nas `sources[n]` — irmão de 479; um leitor só.
Não outro inventado no prompt — irmão de 479 e 478.
Não promover `executed` no prompt do continuity — irmão de 479.
Não inventar chave `pergunta` no recibo da inicialização — irmão de 480.
Não inventar chave `aviso` no recibo da inicialização — irmão de 480.
Não nomear a pergunta no `documentation.scope` nem no `context.scope` nem no `continuity.prompt` nem no `delivery_review` nem no `next` nem no `audit` — irmão de 480; um leitor só.
Não outra receita na inicialização — irmão de 480 e 479.
Não promover `executed` na inicialização — irmão de 480.
Não inventar chave `suporte` no recibo do item da capacidade — irmão de 481.
Não inventar chave `registro` no recibo do item da capacidade — irmão de 481.
Não nomear o suporte no `capabilities_scope` nem no `verify.scope` nem no `commands[n]` nem na área de arquitetura nem no `next` — irmão de 481; um leitor só.
Não outra pergunta no item da capacidade — irmão de 481 e 480.
Não promover `verified` no item da capacidade — irmão de 481.
Não inventar chave `infinito` no recibo do contrato do gauntlet — irmão de 482.
Não inventar chave `prazo` no recibo do contrato do gauntlet — irmão de 482.
Não nomear o infinito no recibo do `--output` nem no `continuity.prompt` nem no `continuity.scope` nem no `next` — irmão de 482; um leitor só.
Não outro suporte no contrato do gauntlet — irmão de 482 e 481.
Não promover `executed` no contrato do gauntlet — irmão de 482.
Não inventar chave `prioridade` no recibo dos limites da coverage — irmão de 483.
Não inventar chave `estudo` no recibo dos limites da coverage — irmão de 483.
Não nomear a prioridade no `coverage.scope` nem no `scan.scope` nem no `audit` nem no `context.scope` nem no `next` — irmão de 483; um leitor só.
Não outro infinito nos limites da coverage — irmão de 483 e 482.
Não promover `felt` nos limites da coverage — irmão de 483.
Não inventar chave `valor` no recibo do template do MVP — irmão de 484.
Não inventar chave `hipótese` no recibo do template do MVP — irmão de 484.
Não nomear o valor no `template` de outra etapa nem no `finish` nem no `context` nem no `next` nem no `verify` — irmão de 484; um leitor só.
Não outra prioridade no template do MVP — irmão de 484 e 483.
Não promover `verified` no template do MVP — irmão de 484.
Não inventar chave `acabamento` no recibo do template da vertical-slice — irmão de 485.
Não inventar chave `placeholders` no recibo do template da vertical-slice — irmão de 485.
Não nomear o acabamento no `template` de outra etapa nem no `finish` nem no `context` nem no `next` nem no `verify` — irmão de 485; um leitor só.
Não outro valor no template da vertical-slice — irmão de 485 e 484.
Não promover `verified` no template da vertical-slice — irmão de 485.
Não inventar chave `hipótese` no recibo do gate close — irmão de 486.
Não inventar chave `compilação` no recibo do gate close — irmão de 486.
Não nomear a hipótese no `gate` de outra etapa nem no `gate.scope` nem no critério nem no `template` poc nem no `verify` nem no `next` nem no `context` — irmão de 486; um leitor só.
Não outro acabamento no gate close — irmão de 486 e 485.
Não promover `verified` no gate close — irmão de 486.
Não inventar chave `lançamento` no recibo do gate deliver — irmão de 487.
Não inventar chave `teste` no recibo do gate deliver — irmão de 487.
Não nomear o lançamento no `gate` de outra etapa nem no `gate.scope` nem no critério nem no `template` release nem no `ship` nem no `next` nem no `verify` — irmão de 487; um leitor só.
Não outra hipótese no gate deliver — irmão de 487 e 486.
Não promover `elsewhere` no gate deliver — irmão de 487.
Não inventar chave `composição` no recibo do content — irmão de 488.
Não inventar chave `módulos` no recibo do content — irmão de 488.
Não nomear a composição no `art` nem no `ship` nem no `feel` nem no gate `scale` nem no `next` — irmão de 488; um leitor só.
Não outro lançamento no content — irmão de 488 e 487.
Não promover `enough` no content — irmão de 488.
Não inventar chave `prontidão` no recibo do prompt do continuity — irmão de 489.
Não inventar chave `readiness` extra no recibo do prompt — irmão de 489.
Não nomear a prontidão no `continuity.scope` nem nas `sources` nem no `documentation` nem no `delivery_review` nem no `context.scope` nem no `next` — irmão de 489; um leitor só.
Não outra composição no prompt — irmão de 489 e 488.
Não promover `executed` no prompt do continuity — irmão de 489.
Não inventar chave `posição` no recibo do item da constante — irmão de 490.
Não inventar chave `integrada` extra no recibo da constante — irmão de 490.
Não nomear a posição no `feel.scope` nem nas `observations` nem no `note` nem no `playtest` nem no `next` — irmão de 490; um leitor só.
Não outra prontidão no item da constante — irmão de 490 e 489.
Não promover `felt` no item da constante — irmão de 490.
Não inventar chave `quadros` no recibo da plataforma — irmão de 491.
Não inventar chave `GPU` extra no recibo da plataforma — irmão de 491.
Não nomear os quadros no `packs.scope` nem no gênero nem no `context.scope` nem no `next` nem no `play` — irmão de 491; um leitor só.
Não outra posição na plataforma — irmão de 491 e 490.
Não promover `measured` na plataforma — irmão de 491.
Não inventar chave `significado` no recibo do comando do verify — irmão de 492.
Não inventar chave `hash` extra no recibo do comando — irmão de 492.
Não nomear o significado no `verify.scope` nem no `git` nem no anexo do `record` nem no `next` — irmão de 492; um leitor só.
Não outros quadros no comando do verify — irmão de 492 e 491.
Não promover `verified` no comando do verify — irmão de 492.
Não inventar chave `livre` no recibo do ciclo — irmão de 493.
Não inventar chave `janela` extra no recibo do ciclo — irmão de 493.
Não nomear o livre no `feel.scope` nem nas `observations` nem no `note` nem no `playtest` nem no `next` nem no `guide.scope` nem no `play.scope` nem no `start.scope` — irmão de 493; um leitor só.
Não outro significado no ciclo — irmão de 493 e 492.
Não promover `felt` no ciclo — irmão de 493.
Não inventar chave `compreendida` no recibo do candidato da arquitetura — irmão de 494.
Não inventar chave `entendida` extra no recibo do candidato — irmão de 494.
Não nomear a compreendida no `architecture.scope` nem nos candidatos das outras áreas nem no `scan.scope` nem no `context.scope` nem no `next` — irmão de 494; um leitor só.
Não outro livre no candidato da arquitetura — irmão de 494 e 493.
Não promover `executed` no candidato da arquitetura — irmão de 494.
Não inventar chave `conclusão` no recibo dos sinais do next — irmão de 495.
Não inventar chave `término` extra no recibo dos sinais — irmão de 495.
Não nomear a conclusão no `next.scope` nem na proposta nem nas alternativas nem no `signals` do `discover` nem no `context.scope` — irmão de 495; um leitor só.
Não outra compreendida nos sinais do next — irmão de 495 e 494.
Não promover `executed` nos sinais do next — irmão de 495.
Não inventar chave `independência` no recibo do contrato do gauntlet — irmão de 496.
Não inventar chave `crítico` extra no recibo do contrato — irmão de 496.
Não nomear a independência no recibo do `--output` nem no `continuity.prompt` nem no `next` nem no `context.scope` nem no `playtest` — irmão de 496; um leitor só.
Não outra conclusão no contrato do gauntlet — irmão de 496 e 495.
Não promover `execution_started` no contrato do gauntlet — irmão de 496.
Não inventar chave `decode` no recibo da ficha do catálogo do sfx info — irmão de 497.
Não inventar chave `técnica` extra no recibo da ficha — irmão de 497.
Não nomear o decode no sfx info do stem nem no sfx search nem no roles nem no summarize nem no next — irmão de 497; um leitor só.
Não outra independência na ficha do catálogo — irmão de 497 e 496.
Não promover `heard` na ficha do catálogo — irmão de 497.
Não inventar chave `portabilidade` no recibo da árvore do ship — irmão de 498.
Não inventar chave `destino` extra no recibo da árvore — irmão de 498.
Não nomear a portabilidade no `ship.scope` nem no `artifact` nem no `next` nem no `play` nem no `ship_tree` cru — irmão de 498; um leitor só.
Não outro decode na árvore do ship — irmão de 498 e 497.
Não promover `elsewhere` na árvore do ship — irmão de 498.
Não inventar chave `atual` no recibo do artifact do ship — irmão de 499.
Não inventar chave `HEAD` extra no recibo do artifact — irmão de 499.
Não nomear a atual no `ship.scope` nem no `tree` nem no `next` nem no `play` nem no `ship_artifact` cru — irmão de 499; um leitor só.
Não outra portabilidade no artifact do ship — irmão de 499 e 498.
Não promover `elsewhere` no artifact do ship — irmão de 499.
Não inventar chave `multiplayer` no recibo da área de arquitetura — irmão de 500.
Não inventar chave `sessão` extra no recibo da área — irmão de 500.
Não nomear o multiplayer no `architecture.candidates` nem no `scan.scope` nem no `art_direction` nem no `context.scope` nem no `next` — irmão de 500; um leitor só.
Não outra atual na área de arquitetura — irmão de 500 e 499.
Não promover `executed` na área de arquitetura — irmão de 500.
Não inventar chave `partida` no recibo dos sinais do review — irmão de 501.
Não inventar chave `jogada` extra no recibo dos sinais — irmão de 501.
Não nomear a partida no `review.scope` nem no `review_item` nem no `signals` do `next` nem no `next.scope` — irmão de 501; um leitor só.
Não outro multiplayer nos sinais do review — irmão de 501 e 500.
Não promover `outsider` nos sinais do review — irmão de 501.
Não inventar chave `ouvir` no recibo do sfx copy do acervo — irmão de 502.
Não inventar chave `mix` extra no recibo do copy — irmão de 502.
Não nomear o ouvir no sfx copy do stem nem no sfx export nem no sfx import nem no sfx info nem no next — irmão de 502; um leitor só.
Não outra partida no sfx copy do acervo — irmão de 502 e 501.
Não promover `heard` no sfx copy do acervo — irmão de 502.
Não inventar chave `adapt` no recibo do local do sfx search — irmão de 503.
Não inventar chave `ciclo` extra no recibo do local — irmão de 503.
Não nomear o adapt no sfx search.scope nem nos matches nem no summarize nem no verify nem no match_local_stems cru nem no next — irmão de 503; um leitor só.
Não outro ouvir no local do sfx search — irmão de 503 e 502.
Não promover `heard` no local do sfx search — irmão de 503.
Não inventar chave `aprovação` no recibo do sfx seed — irmão de 504.
Não inventar chave `usuário` extra no recibo do seed — irmão de 504.
Não nomear a aprovação no sfx import nem no summarize nem no sfx copy nem no sfx search nem no next — irmão de 504; um leitor só.
Não outro adapt no sfx seed — irmão de 504 e 503.
Não promover `heard` no sfx seed — irmão de 504.
Não inventar chave `triagem` no recibo dos matches do sfx search — irmão de 505.
Não inventar chave `artística` extra no recibo dos matches — irmão de 505.
Não nomear a triagem no sfx search.scope nem no local nem no quality_bar cru nem no summarize nem no sfx info nem no next — irmão de 505; um leitor só.
Não outra aprovação nos matches do sfx search — irmão de 505 e 504.
Não promover `heard` nos matches do sfx search — irmão de 505.
Não inventar chave `lacuna` no recibo do sfx verify vazio — irmão de 506.
Não inventar chave `variante` extra no recibo do verify vazio — irmão de 506.
Não nomear a lacuna no sfx verify com acervo nem no local nem no sfx info nem no sfx search nem no next — irmão de 506; um leitor só.
Não outra triagem no sfx verify vazio — irmão de 506 e 505.
Não promover `heard` no sfx verify vazio — irmão de 506.
Não inventar chave `invenção` no recibo do sfx export do stem — irmão de 507.
Não inventar chave `inventa` extra no recibo do export do stem — irmão de 507.
Não nomear a invenção no sfx export do acervo nem no sfx copy nem no sfx import nem no sfx info nem no next — irmão de 507; um leitor só.
Não outra lacuna no sfx export do stem — irmão de 507 e 506.
Não promover `heard` no sfx export do stem — irmão de 507.
Não inventar chave `404` no recibo do missing do sfx verify — irmão de 508.
Não inventar chave `nomear` extra no recibo do missing — irmão de 508.
Não nomear o 404 no sfx summary nem no local_stems cru nem no local_missing_card nem no sfx info nem no sfx search nem no next — irmão de 508; um leitor só.
Não outra invenção no missing do sfx verify — irmão de 508 e 507.
Não promover `heard` no missing do sfx verify — irmão de 508.
Não inventar chave `número` no recibo da opção captions — irmão de 509.
Não inventar chave `legenda` extra no recibo da opção captions — irmão de 509.
Não nomear o número no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 509; um leitor só.
Não outro 404 na opção captions — irmão de 509 e 508.
Não promover `verified` na opção captions — irmão de 509.
Não inventar chave `panner` no recibo do papel do x do campo — irmão de 510.
Não inventar chave `lugar` extra no recibo do papel — irmão de 510.
Não nomear o panner no roles.scope nem em bed/close/live/stir nem no access nem no feel nem no next — irmão de 510; um leitor só.
Não outro número no papel do x do campo — irmão de 510 e 509.
Não promover `heard` no papel do x do campo — irmão de 510.
Não inventar chave `retomar` no recibo do roles — irmão de 511.
Não inventar chave `fila` extra no recibo do roles — irmão de 511.
Não nomear o retomar no item do papel nem no roles --fill nem no access nem no feel nem no next — irmão de 511; um leitor só.
Não outro panner no roles.scope — irmão de 511 e 510.
Não promover `heard` no roles.scope do retomar — irmão de 511.
Não inventar chave `controle` no recibo da opção haptics — irmão de 512.
Não inventar chave `pulso` extra no recibo da opção haptics — irmão de 512.
Não nomear o controle no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 512; um leitor só.
Não outro retomar na opção haptics — irmão de 512 e 511.
Não promover `verified` na opção haptics — irmão de 512.
Não inventar chave `botão` no recibo da opção remap — irmão de 513.
Não inventar chave `casca` extra no recibo da opção remap — irmão de 513.
Não nomear o botão no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 513; um leitor só.
Não outro controle na opção remap — irmão de 513 e 512.
Não promover `verified` na opção remap — irmão de 513.
Não inventar chave `causa` no recibo da opção reduced_motion — irmão de 514.
Não inventar chave `estático` extra no recibo da opção reduced_motion — irmão de 514.
Não nomear a causa no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 514; um leitor só.
Não outro botão na opção reduced_motion — irmão de 514 e 513.
Não promover `verified` na opção reduced_motion — irmão de 514.
Não inventar chave `neutro` no recibo da opção high_contrast — irmão de 515.
Não inventar chave `fundo` extra no recibo da opção high_contrast — irmão de 515.
Não nomear o neutro no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 515; um leitor só.
Não outra causa na opção high_contrast — irmão de 515 e 514.
Não promover `verified` na opção high_contrast — irmão de 515.
Não inventar chave `ícone` no recibo da opção colorblind — irmão de 516.
Não inventar chave `forma` extra no recibo da opção colorblind — irmão de 516.
Não nomear o ícone no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 516; um leitor só.
Não outro neutro na opção colorblind — irmão de 516 e 515.
Não promover `verified` na opção colorblind — irmão de 516.
Não inventar chave `mão` no recibo da opção one_hand — irmão de 517.
Não inventar chave `gênero` extra no recibo da opção one_hand — irmão de 517.
Não nomear a mão no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 517; um leitor só.
Não outro ícone na opção one_hand — irmão de 517 e 516.
Não promover `verified` na opção one_hand — irmão de 517.
Não inventar chave `oculto` no recibo da opção assist — irmão de 518.
Não inventar chave `conteúdo` extra no recibo da opção assist — irmão de 518.
Não nomear o oculto no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 518; um leitor só.
Não outra mão na opção assist — irmão de 518 e 517.
Não promover `verified` na opção assist — irmão de 518.
Não inventar chave `precisão` no recibo da opção game_speed — irmão de 519.
Não inventar chave `gênero` extra no recibo da opção game_speed — irmão de 519.
Não nomear a precisão no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 519; um leitor só.
Não outro oculto na opção game_speed — irmão de 519 e 518.
Não promover `verified` na opção game_speed — irmão de 519.
Não inventar chave `tipografia` no recibo da opção ui_scale — irmão de 520.
Não inventar chave `interface` extra no recibo da opção ui_scale — irmão de 520.
Não nomear a tipografia no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 520; um leitor só.
Não outra precisão na opção ui_scale — irmão de 520 e 519.
Não promover `verified` na opção ui_scale — irmão de 520.
Não inventar chave `leitor` no recibo da opção live — irmão de 521.
Não inventar chave `overlay` extra no recibo da opção live — irmão de 521.
Não nomear o leitor no access.scope nem nas outras opções nem no feel nem no roles nem no next — irmão de 521; um leitor só.
Não outra tipografia na opção live — irmão de 521 e 520.
Não promover `verified` na opção live — irmão de 521.
Não inventar chave `sessões` no recibo do invite — irmão de 522.
Não inventar chave `autenticação` extra no recibo do invite — irmão de 522.
Não nomear as sessões no `play.scope` nem no `playtest` nem no `next` nem no `ship` nem no `feel` — irmão de 522; um leitor só.
Não outro bind no invite — irmão de 522 e 399.
Não promover `outsider` no invite — irmão de 522.
Não inventar chave `consumido` no recibo do record do sfx copy do acervo — irmão de 523.
Não inventar chave `consumidor` extra no record do sfx copy — irmão de 523 e 383.
Não gravar `scope` no sources.json — irmão de 523.
Não nomear o consumido no copy.scope nem no stem local nem no export nem no content.scope nem no origins nem no next — irmão de 523; um leitor só.
Não outro ouvir no record do copy — irmão de 523 e 502.
Não promover `heard` no record do sfx copy — irmão de 523.
Não inventar chave `experiência` no recibo do then do start — irmão de 524.
Não inventar chave `cores` extra no then do start — irmão de 524.
Não nomear a experiência no `play.then` nem no `guide.then` nem no `init.then` nem no `feel.then` nem no `start.scope` nem no `next` — irmão de 524; um leitor só.
Não outro consumido no then do start — irmão de 524 e 523.
Não promover `executed` no then do start — irmão de 524.
O rótulo do coil do dash ainda diz recarregando — irmão de 328.
Próxima ronda: superfície de entrada que não seja ordem/descrição do `-h` nem outro `sem destino` nem outro install nem outro Abrir nem outro `playtest` no prompt nem outro engines no doctor nem outras substituições no doctor nem outro exemplo no doctor nem outro Node no runtime nem outro file:// no play nem outra produção no play nem outro relógio no guide nem outros scripts no discover nem outro módulo no init nem outro gate no gate nem outro serve no scan; auditoria item 1 que não seja outro sfx de arquivo sumido nem CREDITS nem origins.missing nem data/public no ship nem outro campo do mixer nem outro foco visível nem outra cena do budget nem outros bytes no budget nem outro percentil no budget nem outra linha de persistência no canvas nem outro fechamento no save nem outro par no content nem outra mesa no content nem outro tamanho no ship nem outro banner no ship nem outro passo no ship nem outro file:// no ship nem outro stub de contraste nem outro perigo no access nem outra soma no roles nem outra voz no roles nem outra simulação no playtest nem outro probe no feel nem outro look no art nem outro trilho no art nem outro lean no feel nem outro pico no sfx info nem outro rms no sfx info nem outra tabela de teclas no access nem outro last-run no note nem auto-anexar no note nem outro pico no sfx summary nem outro pico no sfx info nem outro par no start nem extra pair no content nem pair no art nem outra legenda no access nem outro deslocamento no sfx search nem outra voz no sfx search nem outro sit no feel nem outra guarda no feel nem outro recado no playtest nem outro POST no playtest nem outra gravação no save nem outro storage no save nem outro land no feel nem outro término no feel nem outra migração no content nem outro loader no content nem outra vinheta no art nem outro recorte no art nem outro PCM no roles nem outro wav no roles nem outro consumidor no origins nem outro sidecar no origins nem outros créditos no copy nem outra integridade no sfx verify nem outro hash no sfx verify nem outro processamento no sfx export nem outros bytes no sfx export nem outro mínimo no bar nem outro piso no bar nem outro relógio no guide nem outra saída de escopo no craft nem outro contraste no art nem outras substituições no doctor nem outros scripts no discover nem outros scripts no next nem outro módulo no init nem outro gate no gate nem outro gate no next nem outro serve no scan nem outro serve no play nem outro serve no next nem outro bind no invite nem outro HOST no invite nem outras sessões no invite nem outra publicação no template nem outro molde no template nem outro audit no context nem outro consentimento no documentation nem outra PoC no continuity nem outro process no continuity nem outro AAA no agent_context nem outro agents no scan nem outro checklist no finish nem outro aaa no finish nem outra promoção no production_bar nem outro degrau no bar nem outro navegador no packs nem outro unitário no verify nem outra ação no next nem outra ação no continuity nem outra medição no record nem outro mede no verify nem outro critério no budget nem outro mérito no check-plan nem outro mérito no next nem outro mérito no continuity nem outra criatividade no verify nem outra criatividade no record nem outra criatividade no template nem outra verificação no verify.scope nem outro verified no record nem outro verified no next nem outra leitura no git nem outra leitura no verify nem outra leitura no next nem outro progresso no context nem outro progresso no production_bar nem outro progresso no finish nem outro progresso no template nem outro progresso no next nem outra escuta no studio_assets nem outra escuta no roles nem outra escuta no context.scope nem outra escuta no next nem outros tokens no scan.scope nem outros tokens no art nem outros tokens no next nem outras dependências no scan.scope nem outras dependências na art_direction nem outras dependências no context nem outras dependências no next nem outra inexistência no coverage nem outra ausência no coverage nem outra inexistência no scan.scope nem outra inexistência no audit nem outra inexistência no next nem outra capacidade na platform nem outra capacidade no packs.scope nem outra capacidade no next nem outro navegador na platform nem outro onboarding no passo de jogar nem outro onboarding no guide.scope nem outro mural no play.scope nem outro onboarding no next nem outro screenshot no passo de gravar nem outro screenshot no feel.scope nem outro screenshot no note nem outro screenshot no record nem outra extração no genre nem outra extração no packs.scope nem outra extração na platform nem outra extração no next nem outra API na menção nem outra API no capabilities_scope nem outra API no context.scope nem outra API no next nem outra criação na proposal nem outra criação no next.scope nem outra criação nas alternatives nem outra criação no init nem outro silêncio no item do gate nem outro silêncio no gate.scope nem outro silêncio no next nem outro silêncio no check-plan nem outro silêncio no craft nem outra abertura no passo de abrir nem outra abertura no guide.scope nem outra abertura no play.scope nem outra abertura no start.scope nem outra abertura no init nem outra abertura no next nem outra escada no item do craft nem outra escada no craft.scope nem outra escada no gate nem outra escada no next nem outra escada no bar nem outro prazo no item do bar nem outro prazo no bar.scope nem outro prazo no production_bar nem outro prazo no next nem outro prazo no context nem outro motor no then nem outro motor no doctor.scope nem outro motor no init nem outro motor no guide nem outro motor no next nem outra fabricação na alternativa nem outra fabricação na proposal nem outra fabricação no next.scope nem outra fabricação no check-plan nem outra fabricação no context nem outra diversão no comando do verify nem outra diversão no verify.scope nem outra diversão no capabilities_scope nem outra diversão no record nem outra diversão no next nem outra diversão no doctor.then nem outra licença na área de proveniência nem outra licença no origins nem outra licença no scan.scope nem outra licença no gate nem outra licença no next nem outra licença em art_direction nem outra licença em architecture nem outras pessoas na área de QA nem outras pessoas no playtest nem outras pessoas no record nem outras pessoas no scan.scope nem outras pessoas no next nem outras pessoas em provenance nem outra qualidade no item do discover nem outra qualidade no review.scope nem outra qualidade no scan.scope nem outra qualidade no documentation nem outra qualidade no next nem outra animação no anexo do record nem outra animação no record.scope nem outra animação no passo de gravar nem outra animação no feel nem outra animação no next nem outra paleta no item do art nem outra paleta no art.scope nem outra paleta na art_direction nem outra paleta no scan.scope nem outra paleta no next nem outro publisher no atalho da skill nem outro publisher no doctor.scope nem outro publisher no then nem outro publisher no guide nem outro publisher no init nem outro publisher no next nem outra quantidade no item do roles nem outra quantidade no roles.scope nem outra quantidade no roles --fill nem outra quantidade no feel nem outra quantidade no next nem outras intenções no candidato do scan nem outras intenções no scan.scope nem outras intenções no audit nem outras intenções no coverage nem outras intenções no documentation nem outras intenções no next nem outra certificação no item do access nem outra certificação no access.scope nem outra certificação no gate nem outra certificação no verify nem outra certificação no next nem outro autor no item da observação nem outro autor no feel.scope nem outro autor no note nem outro autor no playtest nem outro autor no record nem outro autor no next nem outro volume no item da chuva nem outro volume no art.scope nem outro volume na art_direction nem outro volume no scan nem outro volume no content nem outro volume no next nem outra dispensa no critério do gate nem outra dispensa no gate.scope nem outra dispensa no gates[n] nem outra dispensa no next nem outra dispensa no check-plan nem outra dispensa no craft nem outro universal no item da constante nem outro universal no feel.scope nem outro universal nas observations nem outro universal no note nem outro universal no next nem outra dimensão no problema do bar nem outra dimensão no bar.scope nem outra dimensão em dimensions[n] nem outra dimensão no production_bar nem outra dimensão no next nem outro escopo no problema do gate nem outro escopo no gate.scope nem outro escopo em gates[n] nem outro escopo em criteria[n] nem outro escopo no next nem outro escopo no check-plan nem outro escopo no craft nem outros rótulos no problema do origins nem outros rótulos no origins.scope nem outros rótulos na provenance nem outros rótulos no scan nem outros rótulos no gate nem outros rótulos no next nem outra definição no problema do craft nem outra definição no craft.scope nem outra definição em checks[n] nem outra definição no gate nem outra definição no next nem outra definição no bar nem outra ausência no check do doctor nem outra ausência no doctor.scope nem outra ausência no then nem outra ausência nos skill_targets nem outra ausência no next nem outra ausência no guide nem outra ausência no init nem outra fila no item da fonte do continuity nem outra fila no continuity.scope nem outra fila no documentation nem outra fila no next nem outra fila no check-plan nem outra fila em scan.continuity_sources nem outra mecânica no item da menção de gênero nem outra mecânica no packs.genre.scope nem outra mecânica no packs.scope nem outra mecânica no context.scope nem outra mecânica no next nem outra mecânica em packs.genre.mentions nem outro acidente no item do issue da coverage nem outro acidente no coverage.scope nem outro acidente no scan.scope nem outro acidente no audit nem outro acidente no next nem outro acidente no context.scope nem outra identidade na árvore do ship nem outra identidade no ship.scope nem outra identidade no next nem outra identidade no play nem outra identidade no ship_tree cru nem outro determinismo no item desconhecido do capabilities nem outro determinismo na menção nem outro determinismo no capabilities_scope nem outro determinismo no context.scope nem outro determinismo no next nem outro determinismo no production_bar nem outro determinismo no bar nem outro editor no artifact do ship nem outro editor no ship.scope nem outro editor no tree nem outro editor no next nem outro editor no play nem outro editor no ship_artifact cru nem outro cinco na conta do playtest nem outro cinco no playtest.scope nem outro cinco no invite nem outro cinco no next nem outro cinco no note nem outro cinco no last_run_tally cru nem outras linhas no rascunho da coverage nem outras linhas no coverage.scope nem outras linhas no scan.scope nem outras linhas em issues[n] nem outras linhas no audit nem outras linhas no next nem outras linhas no context.scope nem outro semântico no metadata_issues nem outro semântico no check-plan.scope nem outro semântico no context.scope nem outro semântico no next nem outro aperto na curva do playtest nem outro aperto no playtest.scope nem outro aperto no content.scope nem outro aperto no candidate_tally nem outro aperto no invite nem outro aperto no next nem outro aperto no last_run_curve cru nem outra precedência no conflito do bar nem outra precedência no bar.scope nem outra precedência em problems[n] nem outra precedência em dimensions[n] nem outra precedência no production_bar nem outra precedência no next nem outra precedência no bar_declaration cru nem outra improvisação no sfx import nem outra improvisação no sfx seed nem outra improvisação no next nem outra improvisação no summarize nem outra improvisação no roles nem outra improvisação no sfx copy nem outro lixo no sfx info do stem nem outro lixo no local_stems cru nem outro lixo na ficha ausente nem outro lixo no catálogo nem outro lixo no summarize nem outro lixo no sfx search nem outro lixo no sfx import nem outra telemetria na área do runbook nem outra telemetria no scan.scope nem outra telemetria no qa nem outra telemetria no architecture nem outra telemetria no ship nem outra telemetria no next nem outro histórico na área do decisions nem outro histórico no scan.scope nem outro histórico no architecture nem outro histórico no runbook nem outro histórico no next nem outro divertido na área do gdd nem outro divertido no scan.scope nem outro divertido no decisions nem outro divertido no mda nem outro divertido no feel nem outro divertido no next nem outra pontuação na área do mda nem outra pontuação no scan.scope nem outra pontuação no gdd nem outra pontuação no feel nem outra pontuação no verify nem outra pontuação no next nem outro público na área do vision nem outro público no scan.scope nem outro público no gdd nem outro público no mda nem outro público no feel nem outro público no next nem outro marketing no item da escala nem outro marketing no read_scale.scope nem outro marketing no scan.scope nem outro marketing no vision nem outro marketing no context.scope nem outro marketing no next nem outra opção no item do access nem outra opção no access.scope nem outra opção no origins nem outra opção no gate nem outra opção no verify nem outra opção no next nem outro genérico no item do commands nem outro genérico no commands.scope nem outro genérico no context nem outro genérico no doctor.then nem outro genérico no next nem outra listagem no item do discover nem outra listagem no review nem outra listagem no review_item nem outra listagem no next nem outra listagem no context nem outra própria no item do pin nem outra própria no pin.scope nem outra própria no unpin.scope nem outra própria no created nem outra própria no commands nem outra própria no next nem outra preenchida no módulo do context nem outra preenchida no context.scope nem outra preenchida no documentation nem outra preenchida no workspace_module cru nem outra preenchida no next nem outra preenchida no init nem outras regras no delivery_review nem outras regras no context.scope nem outras regras no documentation nem outras regras no finish nem outras regras no next nem outras regras no continuity nem outro inventado no workspace nem outro inventado no context.scope nem outro inventado no documentation nem outro inventado no workspace_module nem outro inventado no delivery_review nem outro inventado no next nem outro inventado no workspace_profile cru nem outra receita no prompt do continuity nem outra receita no continuity.scope nem outra receita no context.scope nem outra receita no documentation nem outra receita no delivery_review nem outra receita no next nem outra receita nas sources nem outra pergunta na inicialização nem outra pergunta no documentation.scope nem outra pergunta no context.scope nem outra pergunta no continuity.prompt nem outra pergunta no delivery_review nem outra pergunta no next nem outra pergunta no audit nem outro suporte no item da capacidade nem outro suporte no capabilities_scope nem outro suporte no verify.scope nem outro suporte no commands[n] nem outro suporte na área de arquitetura nem outro suporte no next nem outro infinito no contrato do gauntlet nem outro infinito no recibo do --output nem outro infinito no continuity.prompt nem outro infinito no continuity.scope nem outro infinito no next nem outra prioridade nos limites da coverage nem outra prioridade no coverage.scope nem outra prioridade no scan.scope nem outra prioridade no audit nem outra prioridade no context.scope nem outra prioridade no next nem outro valor no template do MVP nem outro valor no template de outra etapa nem outro valor no finish nem outro valor no context nem outro valor no next nem outro valor no verify nem outro acabamento no template da vertical-slice nem outro acabamento no template de outra etapa nem outro acabamento no finish nem outro acabamento no context nem outro acabamento no next nem outro acabamento no verify nem outra hipótese no gate close nem outra hipótese no gate de outra etapa nem outra hipótese no gate.scope nem outra hipótese no critério nem outra hipótese no template poc nem outra hipótese no verify nem outra hipótese no next nem outra hipótese no context nem outro lançamento no gate deliver nem outro lançamento no gate de outra etapa nem outro lançamento no gate.scope nem outro lançamento no critério nem outro lançamento no template release nem outro lançamento no ship nem outro lançamento no next nem outro lançamento no verify nem outra composição no content nem outra composição no art nem outra composição no ship nem outra composição no feel nem outra composição no gate scale nem outra composição no next nem outra prontidão no prompt do continuity nem outra prontidão no continuity.scope nem outra prontidão nas sources nem outra prontidão no documentation nem outra prontidão no delivery_review nem outra prontidão no context.scope nem outra prontidão no next nem outra posição no item da constante nem outra posição no feel.scope nem outra posição nas observations nem outra posição no note nem outra posição no playtest nem outra posição no next nem outros quadros na plataforma nem outros quadros no packs.scope nem outros quadros no gênero nem outros quadros no context.scope nem outros quadros no next nem outros quadros no play nem outro significado no comando do verify nem outro significado no verify.scope nem outro significado no git nem outro significado no anexo do record nem outro significado no next nem outro livre no ciclo nem outro livre no feel.scope nem outro livre no guide.scope nem outro livre no play.scope nem outro livre no start.scope nem outro livre no next nem outra compreendida no candidato da arquitetura nem outra compreendida no architecture.scope nem outra compreendida nos candidatos das outras áreas nem outra compreendida no scan.scope nem outra compreendida no next nem outra conclusão nos sinais do next nem outra conclusão no next.scope nem outra conclusão na proposta nem outra conclusão nas alternativas nem outra conclusão no discover nem outra conclusão no context.scope nem outra independência no contrato do gauntlet nem outra independência no recibo CLI nem outra independência no continuity.prompt nem outra independência no next nem outra independência no context.scope nem outro decode na ficha do catálogo do sfx info nem outro decode no sfx info do stem nem outro decode no sfx search nem outro decode no roles nem outro decode no summarize nem outro decode no next nem outra portabilidade na árvore do ship nem outra portabilidade no ship.scope nem outra portabilidade no artifact nem outra portabilidade no next nem outra portabilidade no play nem outra portabilidade no ship_tree cru nem outra atual no artifact do ship nem outra atual no ship.scope nem outra atual no tree nem outra atual no next nem outra atual no play nem outra atual no ship_artifact cru nem outro multiplayer na área de arquitetura nem outro multiplayer nos candidatos nem outro multiplayer no scan.scope nem outro multiplayer no art_direction nem outro multiplayer no context.scope nem outro multiplayer no next nem outra partida nos sinais do review nem outra partida no review.scope nem outra partida no review_item nem outra partida no signals do next nem outra partida no next.scope nem outro ouvir no sfx copy do acervo nem outro ouvir no sfx copy do stem nem outro ouvir no sfx export nem outro ouvir no sfx import nem outro ouvir no sfx info nem outro ouvir no next nem outro adapt no local do sfx search nem outro adapt no sfx search.scope nem outro adapt nos matches nem outro adapt no summarize nem outro adapt no verify nem outro adapt no next nem outra aprovação no sfx seed nem outra aprovação no sfx import nem outra aprovação no summarize nem outra aprovação no sfx copy nem outra aprovação no next nem outra triagem nos matches do sfx search nem outra triagem no sfx search.scope nem outra triagem no local nem outra triagem no summarize nem outra triagem no sfx info nem outra triagem no next nem outra lacuna no sfx verify vazio nem outra lacuna no sfx verify com acervo nem outra lacuna no local nem outra lacuna no sfx info nem outra lacuna no next nem outra invenção no sfx export do stem nem outra invenção no sfx export do acervo nem outra invenção no sfx copy nem outra invenção no sfx import nem outra invenção no next nem outro 404 no missing do sfx verify nem outro 404 no sfx summary nem outro 404 no local_stems cru nem outro 404 no local_missing_card nem outro 404 no next nem outro número na opção captions nem outro número no access.scope nem outro número nas outras opções nem outro número no feel nem outro número no next nem outro panner no papel do x do campo nem outro panner no roles.scope nem outro panner no bed nem outro panner no access nem outro panner no next nem outro retomar no roles.scope nem outro retomar no item do papel nem outro retomar no roles --fill nem outro retomar no access nem outro retomar no feel nem outro retomar no next nem outro controle na opção haptics nem outro controle no access.scope nem outro controle nas outras opções nem outro controle no feel nem outro controle no next nem outro botão na opção remap nem outro botão no access.scope nem outro botão nas outras opções nem outro botão no feel nem outro botão no next nem outra causa na opção reduced_motion nem outra causa no access.scope nem outra causa nas outras opções nem outra causa no feel nem outra causa no next nem outro neutro na opção high_contrast nem outro neutro no access.scope nem outro neutro nas outras opções nem outro neutro no feel nem outro neutro no next nem outro ícone na opção colorblind nem outro ícone no access.scope nem outro ícone nas outras opções nem outro ícone no feel nem outro ícone no next nem outra mão na opção one_hand nem outra mão no access.scope nem outra mão nas outras opções nem outra mão no feel nem outra mão no next nem outro oculto na opção assist nem outro oculto no access.scope nem outro oculto nas outras opções nem outro oculto no feel nem outro oculto no next nem outra precisão na opção game_speed nem outra precisão no access.scope nem outra precisão nas outras opções nem outra precisão no feel nem outra precisão no next nem outra tipografia na opção ui_scale nem outra tipografia no access.scope nem outra tipografia nas outras opções nem outra tipografia no feel nem outra tipografia no next nem outro leitor na opção live nem outro leitor no access.scope nem outro leitor nas outras opções nem outro leitor no feel nem outro leitor no next nem outras sessões no invite nem outras sessões no play.scope nem outras sessões no playtest nem outras sessões no next nem outras sessões no ship nem outras sessões no feel nem outro consumido no record do sfx copy nem outro consumido no copy.scope nem outro consumido no content.scope nem outro consumido no origins nem outro consumido no next nem outra experiência no then do start nem outra experiência no play.then nem outra experiência no guide.then nem outra experiência no init.then nem outra experiência no feel.then nem outra experiência no start.scope nem outra experiência no next; atrito ideia→jogo que não seja 332/337/339/342/347/373/384/387/391/394/395/396/397/398/399/400/401/402/403/404/405/406/407/408/409/410/411/412/413/414/415/416/417/418/419/420/421/422/423/424/425/426/427/428/429/430/431/432/433/434/435/436/437/438/439/440/441/442/443/444/445/446/447/448/449/450/451/452/453/454/455/456/457/458/459/460/461/462/463/464/465/466/467/468/469/470/471/472/473/474/475/476/477/478/479/480/481/482/483/484/485/486/487/488/489/490/491/492/493/494/495/496/497/498/499/500/501/502/503/504/505/506/507/508/509/510/511/512/513/514/515/516/517/518/519/520/521/522/523/524; feel visível/audível que não seja tinta nem rótulo do HUD do dash nem rumble de graze/miss nem outro leaf do player nem duck no feel nem outro traço de rumo no coil nem o corpo da porta nem outra linha de lacuna no canvas nem o exercício do perdão nem a inclinação do quadro nem o sit da guarda nem o land do dash nem o screenshot no passo de gravar nem o autor no item da observação nem a posição no item da constante nem o livre no ciclo; ou ferramenta de outsider que não seja tally na faixa nem outra origem na faixa nem outro prefixo no achado copiado nem o nome do `session` no playtest nem o last-run no note nem o recado no playtest nem o bind no invite nem as sessões no invite nem o consumido no record do sfx copy nem a experiência no then do start.
