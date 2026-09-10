# Canvas Arcade

Arcade de uma tela em Canvas. O jogador atravessa uma chuva de orbes e
estilhaços e decide, a cada instante, **guardar a corrente ou continuar**.

Este projeto nasceu do starter `canvas-arcade` do Alan Studios Framework. Ele é
material de **ADAPT**: existe para ser modificado, renomeado e substituído, não
para ser preservado. O que vale a pena manter é o contrato — passo fixo,
determinismo verificável, ciclo de vida sem vazamento, save versionado e acesso
desde o início.

## Como executar

Requer Node 20 ou mais recente. Não há dependências a instalar.

```sh
npm run serve      # serve em http://localhost:8080; no terminal, tenta abrir o navegador
```

`?look=dusk` ou `?look=calm` troca a paleta (campo e a página), `?spawn=dusk` ou
`?spawn=calm` troca a chuva e `?mood=calm` ou `?mood=dusk` troca o par.
`?seed=<n>` abre essa partida e ignora o hold.
`?invite=1` some a tabela; com last-run, o endereço junta a seed e,
se a partida nomeou a chuva ou o look, a mesa e a paleta.
A página nomeia o mesmo par no select. Look ou chuva explícitos vencem o mood no
próprio eixo. Trocar a chuva do par recomeça a partida; trocar só o look não. O `start` do harness nomeia as queries quando o manifesto
as declara. Depois de um `note`, `start` e `next` apontam
`pair --from`, `look --from`, `table --from` e `sfx --from` — o segundo ciclo. O par nasce look e chuva no mesmo nome e vira `?mood=`. Ferramenta
no disco não é alguém de fora nem mix ouvido. No campo, o aviso do
primeiro ciclo nomeia teclado, toque e controle; `npm run serve` tenta
abrir o navegador quando o terminal é interativo. Abrir a janela não é
jogar. Com tela, o boot espera o avanço: a abertura recebe o
movimento, o aviso pede mover, e nomeia a fantasia, a última
pontuação, o recorde e repetir a última seed. O fim
volta à porta com um avanço novo; R também. Sem tela o headless começa jogando. Repetir não
é o tick interrompido.

Módulos ES não carregam por `file://`, então abrir `index.html` direto no
navegador não funciona; o servidor local existe só por isso.

Como starter, esta pasta serve e abre antes de qualquer `init`: os arquivos
carregam valores reais, não marcadores. `starter.json` declara quais deles `init`
troca pelo nome do projeto — e em quais arquivos, para que uma troca de nome não
alcance um import ou um caminho relativo que só se parece com ele. Em um projeto
já criado, `starter.json` não existe: ele é metadado do starter, não do jogo.

## Como verificar

```sh
npm test           # regras, determinismo, ciclo de vida, save, mixagem e export
npm run budget     # custo da simulação e do draw num canvas stub
npm run peak       # pico de cada WAV no disco; não é mix ouvido
npm run mix        # soma as vozes de uma partida simulada; não é mix ouvido
npm run probe      # dispara o buffer declarado; não é peso percebido
npm run contrast   # pares hex + pixels do stub após draw(); em cinza, forma sem cor; não é dispositivo
npm run session    # partida simulada → totais e curva; `--spawn` escolhe a chuva; não é sessão observada
# a partida no `npm run serve` grava o mesmo candidato; depois do fim a página grava o recibo se você escrever; no convite grava o achado se os quatro tiverem texto; nenhum observa
npm run size       # bytes de dist/; sem teto e sem aprovação
npm run build      # copia a árvore jogável para dist/; não prova outra máquina
```

Com recibo, a partir da raiz do framework — o caminho é este starter, não `.`,
porque a raiz do framework não tem `package.json`:

```sh
python3 scripts/game.py verify assets/starters/canvas-arcade \
  --script test --output /tmp/qa-01 \
  --proves pause --proves reset --proves seed --proves observe \
  --proves act --proves advance --proves capture --proves dispose
```

Em um projeto criado pelo `init`, troque o caminho pelo do projeto. Cada execução
quer um `--output` inédito: destino existente é recusado, de propósito.

`--proves` anexa ao recibo a alegação de que a execução exercita essas capacidades,
com autor, argv e log. Aqui a alegação se sustenta porque `tests/lifecycle.test.mjs`
e `tests/determinism.test.mjs` cobrem essas oito — com uma ressalva honesta:
`capture` só é exercitada na guarda de ausência de tela, porque `toDataURL` não
existe em headless. Nada disso é conferido pelo harness. Em um projeto adaptado,
só declare o que os seus testes cobrirem: o recibo sai como `claimed`, nunca como
verificado.

Recibo verde registra os comandos executados e o que saiu deles. Não diz nada
sobre arte, ritmo, diversão nem sobre o jogo ser bom.

## A decisão do jogo

Cada orbe coletado aumenta a **corrente**. Guardar converte a corrente em
`corrente²` pontos, mas trava o dash por um instante e zera o acúmulo. Ser
atingido por um estilhaço zera a corrente inteira. Corrente não guardada quando
o tempo termina é perdida.

Isso produz a tensão que sustenta a partida: guardar cedo é seguro e barato,
guardar tarde vale muito mais e pode custar tudo. O dash atravessa estilhaços,
então a pergunta real não é “desviar ou não”, e sim **quando parar de acumular**.

Os valores de perdão de entrada — buffer de dash, janela de graça após o dano,
alcance de coleta maior que o desenho — estão em `CONFIG`, em
`src/game/rules.js`, cada um com o motivo. Alterar sem registrar é perdê-los.

## Documentos

- Origem de código e assets: [CREDITS.md](CREDITS.md) — existe aqui, desde já
- `docs/brief.md` · `docs/gdd.md` · `docs/mda.md`
- `docs/tdd.md` · `docs/art-bible.md`
- `docs/devlog.md` · `docs/qa.md`

`docs/art-bible.md` já vem escrito: primitivas por decisão, não placeholder.
Os outros seis de `docs/` nascem rascunho no `init`. O `start` não os planta;
`--docs` no start ou o próprio `init` os cria. O primeiro trabalho real
do projeto é **jogar o ciclo** — `npm run serve` — e escrever o que a proposta
muda no verbo. Preencher templates antes da primeira partida é o atrito que o
`next` recusa. Com `init --no-docs`, os rascunhos também não nascem.

## Degrau de acabamento declarado

Pela [barra de acabamento](../../../references/production-bar.md), o degrau
percebido de um jogo é o **mínimo** entre suas dimensões. O projeto nasce assim, e
a última coluna diz o que falta em cada uma: o critério do degrau
**imediatamente** seguinte, nunca o de um degrau distante — é isso que a torna
trabalho em vez de aspiração.

`python3 <framework>/scripts/game.py bar .` lê esta tabela e devolve o piso, as
dimensões que estão nele e o degrau percebido. Ela é a **afirmação** deste
projeto; o harness confere a forma dela e nada mais. Ao subir uma linha, escreva
junto a condição: dispositivo, versão, cena e quem observou.

| Dimensão | Degrau | Critério do degrau seguinte |
| --- | --- | --- |
| `feel` | `playable` | `slice`: cada ação com sinal próprio de partida, contato e término — dash, coleta, guarda e dano já têm squash/hitstop/tremor/câmera, rumble e rastro distintos; o avanço senta dois ticks antes de alongar; a guarda que já tem corrente senta os mesmos dois ticks e também atravessa o estilhaço; o dash agora aterrissa (senta, câmera, puff, tap e voz próprios); a porta fecha o mesmo arco (`dash`+`land`) sem contar o ofício e sem recovery; a corrente mora no corpo em pips, não só no HUD; a coleta leva o orbe ao slot, o erro espalha, a guarda deposita e o fim derruba a aposta não guardada — o corpo senta (`squashOver`), o quadro senta (tremor, flash e punch do último verbo não atravessam o overlay); na pausa o quadro senta do mesmo jeito e o corpo fica na pose congelada, larga a pose de jogo e o overlay nomeia o que caiu e o recorde que o HUD já mostrava; no fim a cortina do over vence a pausa — P e aba escondida não comem a aposta — recorde zero some — e a queda vence a cortina, que reusa a placa do look; as legendas nascem depois da cortina; o raspo risca o campo, estreita o corpo, empurra a câmera na direção e acende menos que a queda, sem hitstop e sem pulso; a ameaça marca o trilho e a câmera inclina para o mesmo aviso, a recuperação do dash muda a tinta; o corpo aponta para o último avanço; a porta recebe o movimento e o aviso pede mover antes do avanço; a mostra toca o corpo — acende e estreita sem pontuar — o trilho marca a mostra e o live nomeia o perigo na porta; a porta fala `live` uma vez quando a mostra começa, sem ligar a cama; a porta senta e fala sem contar o ofício e o erro acende o campo; o orbe que cai acende o campo, marca o lugar, desloca a câmera para baixo e senta o corpo, sem pulsar o controle; o aviso nomeia a queda enquanto a corrente é zero; a prática contorna o campo na tinta do orbe e some quando a ameaça começa; a guarda contorna o campo na tinta da corrente enquanto a chuva folga; o fecho contorna o campo, pulsa o controle a cada segundo, o dado `closeIntervalScale` aperta o intervalo e `closeHazardScale` sobe o estilhaço, sem faixa no HUD; com corrente viva o aviso pede guardar de novo — pad e toque continuam calados depois da primeira guarda; `npm run probe` conta os buffers, não o peso percebido; o harness não jogou |
| `legibility` | `playable` | `slice`: leitura em movimento, na resolução e no dispositivo alvo — a sequência de quadros no stub cobre o HUD; halo e vinheta marcam a chuva e o recorte; `npm run contrast` amostra a cena montada e, em cinza, pixels que só o orbe ou só o estilhaço pintam; o dispositivo alvo ainda não foi observado |
| `art_direction` | `slice` | `shippable`: um implementador que não participou da direção produz o próximo item dentro do piso, e a comparação em movimento confirma — a receita está no art-bible; a paleta é mesa e `dusk` e `calm` são o segundo e o terceiro look (`?look=` / `settings.look`); a página também veste esses tokens; halo e vinheta dão volume ao recorte geométrico; o corpo aponta, o orbe é círculo e o estilhaço é losango; a porta chove a mesa vigente sem comer a seed; `look --from` / `--as` nasce o próximo; três looks não aprovam direção; `consistent` é falso |
| `audio_mix` | `slice` | `shippable`: faixa dinâmica controlada, sem clipping que obrigue a baixar o volume — o palco tem folga, a cama ocupa o barramento de música e o mixer limita o master; coleta e guarda sobem de tom com a corrente; coleta, queda, raspo, impacto, avanço e o término levam o x do campo; o término fala no barramento de sfx; o orbe perdido fala no barramento de sfx; o fecho, a prática e a guarda falam no barramento de UI com legenda; no fecho a cama sobe o tom com o pulso (`closeBedRate`); no `over` a cama solta com fade (`BED_FADE_MS`); pause, title e aba escondida continuam cortando a cama seco; no campo a pausa `hush` corta as vozes do verbo; no fim e na porta o `hush` não corre — o stinger atravessa; `sfx --from` / `--as` nasce a próxima voz no papel que o mixer já toca; `npm run mix` soma cama e vozes na simulação com a mesma taxa, não no dispositivo; loudness percebido não foi medido; `heard` é falso |
| `pacing` | `slice` | `shippable`: a curva foi observada com quem nunca viu o jogo — a prática é orbe-só e o campo a marca; guardar recupera o intervalo e o campo marca a folga; o fecho aperta o intervalo e sobe o risco a partir do dado; a sessão relata never_banked e erro repetido na simulação; `/?invite=1` some a tabela de comandos; com last-run, `/?invite=1&seed=<n>` abre essa partida e `&spawn=<mesa>` / `&look=<paleta>` juntam chuva e look se o candidato os nomeou; depois do fim a página mostra seed, pontos e eixos e oferece os quatro nomes para copiar ou gravar; número na faixa não preenche os quatro; copiar não grava; gravado não fecha a curva; a curva com quem nunca viu o jogo continua pendente |
| `state_trust` | `slice` | `shippable`: interrupção abrupta real — aba fechada — além do teste de dado inválido; `pagehide`, `beforeunload` e perda de foco já descarregam o save; na porta a aba escondida só descarrega — não congela a mostra; schema 3 guarda `hold` (o tick interrompido) e `canResume` o lê — Continuar continua sendo repetir `lastSeed`; a abertura lê `lastSeed`, a última pontuação e o recorde; a porta e o fim nomeiam sessão volátil e gravação que não ficou; stub, `pagehide` e `beforeunload` no teste não são aba fechada real; `trusted` é falso |
| `performance` | `playable` | `slice`: orçamento de quadro declarado e cena representativa medida nele; cada tick compacta a chuva no mesmo array e reusa o poço; evento, telegraph, rastro e o gerador da chuva também reusam; `npm run budget` cronometra a cena `playing.run` (simulação + `draw` num canvas stub) e relata o reuso — não o compositor nem o dispositivo alvo |
| `accessibility` | `slice` | `shippable`: contraste verificado por medição em cena no dispositivo — `npm run contrast` amostra pixels do stub após `draw()`; o aviso do primeiro ciclo nomeia teclado, toque e controle; o dash e o mapa da superfície que falou também ganham passo no campo; o overlay confirma o mapa da superfície que falou por último e segue `uiScale`; o `cycle.hand` nomeia IJKL + P/O; a página remapeia as seis ações do teclado e a tabela nomeia as teclas vigentes; `gameSpeed` dilata o relógio da partida (não a queda da chuva, nem a mostra da porta, nem o fim); `assist` cede queda e alcance também na mostra da porta; `colorblind` fixa orbe azul e estilhaço laranja sem trocar o campo do look; a região viva nomeia a pausa (`pausado`) só quando o overlay diz Pausado — no fim e na porta a palavra some; no fim, na porta e na pausa no campo, o placar e o recorde que o canvas já mostra — no fim também a corrente que caiu se o overlay a nomeia; na porta e no fim também o aviso da sessão se o canvas o mostra — jogando sem pausa o número não entra; o overlay da pausa reusa o placar (`Pausado — N`) e o recorde se houver, como o fim; `docs/access.md` declara o que o recorte não atende; sessão com uma mão ainda não foi observada |
| `content_scale` | `shippable` | `flagship`: a ferramenta é boa o bastante para alguém de fora produzir no piso — `dusk` e `calm` são a segunda e a terceira chuva e o jogo as consome por `?spawn=` / `settings.spawnProfile`; `table --from` de spawn, dusk ou calm com `--as denser` nasce chuva distinta; `pair --from` nasce look e chuva no mesmo nome e `?mood=` aplica; `session --spawn` traça essa chuva; três chuvas e um comando não são volume; `enough` é falso |
| `release` | `prototype` | `playable`: outra pessoa executou o artefato a partir do runbook; `dist/VERSION.json` nomeia a versão; o `package.json` do artefato declara Node 20 e o README recusa `npm install` e `file://`; ninguém correu o artefato fora daqui |

**Leitura honesta: este projeto é um protótipo**, porque uma dimensão está
nesse degrau. Nenhuma quantidade de acabamento visual muda essa leitura antes
dela subir.

## Ofício declarado

Checklists da [§7 do levantamento](../../../references/observable-criteria-research.md):
conformidade com o que **este** projeto declara, sem limiar importado.
`python3 <framework>/scripts/game.py craft .` lê a tabela. `observed` continua
falso — a linha é afirmação de quem escreveu.

| Check | Estado | Evidência |
| --- | --- | --- |
| `canvas_scale` | `met` | FIELD em src/game/rules.js; canvas em index.html; o resize em render.js usa a escala calculada quando a divisão não é inteira — starter |
| `forgiveness` | `met` | dashBufferTicks, bank.bufferTicks, invulnTicks, collect.pad e collect.reachY em CONFIG, src/game/rules.js, unidade em ticks — starter |
| `percentile_def` | `met` | tools/budget.mjs declara o percentil por definição, não por apelido — starter |
| `palette` | `met` | tokens em docs/art-bible.md e data/palettes.json; o desenho consome PALETTES via tables.js — starter |
| `style_factor` | `out_of_scope` | sem assets de mundo de estilo; só primitivas — starter |
| `budget_delta` | `unmet` | npm run budget cronometra simulação e draw no stub; comparação com o build anterior ainda não existe — starter |
| `playtest_stop` | `unmet` | regra de parada ainda não escrita — starter |
| `playtest_finding` | `unmet` | nenhum achado no formato problema/evidência/hipótese/medição — starter |
| `evidence_kind` | `unmet` | lastro ainda não classificado como log ou observação — starter |

Por que `legibility` não é `slice`, com um caso concreto: as placas do HUD
existiam, os testes provavam que cobriam cada linha de texto, e os orbes
realmente desapareciam atrás delas. Ainda assim, dois revisores que assistiram ao
vídeo relataram que não havia placa nenhuma — e estavam certos no que importa.
Preenchida com `rgba(7,9,13,0.86)` sobre o campo `#171b26`, a placa resolvia em
algo perto de `#0a0c10`: diferença real que a compressão apaga. Em alto
contraste, campo preto e placa preta eram a mesma cor, então ela era invisível por
construção. A correção foi dar borda à placa; a lição é que **teste de cobertura
geométrica não é teste de percepção**, e é exatamente essa a distância entre
`playable` e `slice` nesta dimensão.

## Som

Os papéis do verbo, o orbe perdido, o fecho, a prática, a guarda e a cama têm design original em `public/sfx/<papel>.wav` e uma
variante `public/sfx/<papel>-b.wav` (CC0-1.0, `tools/design-sfx.py`):
seno e ruído filtrado, sem quadrada, sem jsfxr, sem Kenney. Origem em
`public/sfx/sources.json` e nos sidecars `.credits.txt`. `src/game/audio.js`
traz a mixagem — barramentos, prioridade, ducking, rodízio, legenda.
`heard` continua falso: arquivo no disco não é mixagem ouvida. O
pedido que chega antes do WAV fica na fila e toca quando o buffer
entra; os stems sobem juntos — collect não espera dash terminar;
wav no lugar não pede ogg; o gesto retoma o contexto suspenso.
Fila, paralelo e resume não são mix ouvido. Variação no disco
não é faixa dinâmica medida.

Toda informação sonora já tem legenda equivalente: o jogo é completável
com o áudio desligado, e precisa continuar sendo. A legenda tem faixa
própria — encostada à direita, abaixo do relógio, posicionada a partir
dos retângulos que o HUD reserva — e junta repetições consecutivas em
uma linha com contagem. No centro inferior, onde nascia, ela caía sobre
o jogador e sobre o rótulo do dash: `tests/render.test.mjs` mede isso
em vez de confiar no olho.

## Estrutura

```
src/core/     laço de passo fixo, entrada, RNG, impressão, armazenamento, save, preferências, rótulo das teclas vivas
src/game/     regras, apresentação, mixagem, mesas, carga de sfx e ensino do ciclo
src/main.js   montagem e contrato de ciclo de vida
data/         conteúdo separado da regra (chuva, HUD, avisos e paleta)
docs/         art-bible vigente — o init não o reescreve
public/sfx/   design original dos papéis do verbo e da cama, com recibo
tools/        servidor, orçamento, mix, sessão, tamanho, export, nascer mesa, nascer look e nascer voz
tests/        regras, determinismo, ciclo de vida, save, mixagem, ensino, export
```

`src/game/rules.js` não conhece DOM, relógio nem aleatoriedade externa: é isso
que permite rodar a partida headless, repetir um replay a partir de uma seed e
comparar duas execuções. `src/core/input.js` reduz teclado, ponteiro e gamepad a
uma intenção — as regras nunca veem eventos.

A paleta vive em `data/palettes.json` e o contrato está em
`docs/art-bible.md`. O desenho consome `PALETTES` via `tables.js`.
`?look=` / `settings.look` escolhem `normal`, `dusk` ou `calm`; alto contraste
vence o look. O harness lê os três; consistência em movimento continua
pendente. Chuva e texto do HUD passam por `src/game/tables.js`.
`npm run table -- <nome> --from spawn --as denser` nasce a próxima chuva
no mesmo carregador e no mesmo consumidor (`?spawn=` /
`settings.spawnProfile`). `--from dusk` parte da chuva densa; `--from calm`
parte da prática longa; sem `--as` a cópia é idêntica nos knobs.
`npm run session -- --spawn <nome>` traça essa chuva. Sem `--from`, o
custo variável continua sendo ligar a regra.
`dusk` e `calm` compartilham o nome entre chuva e look —
as mesas não. `npm run pair -- <nome> --from dusk|calm --look warmer --spawn denser`
nasce os dois no mesmo nome e `?mood=` passa a aplicar. `npm run look -- <nome> --from dusk|calm --as warmer` nasce só o
próximo look no mesmo consumidor. Ferramenta que desloca knobs ou
tokens não é volume, direção consistente nem alguém de fora no piso. `npm run sfx -- --from dash --as brighter` desloca a voz no papel que o mixer já toca; sem `--from` o banco inteiro nasce de novo. Intenção não é mix ouvido. Os papéis do verbo e a cama em `public/sfx` entram no mixer;
`heard` continua falso. `npm run build` copia a árvore jogável para
`dist/`; isso não é outra pessoa tendo jogado o artefato.

`src/main.js` implementa `pause`, `resume`, `reset`, `seed`, `observe`, `act`,
`advance`, `capture` e `dispose`. Esses nomes são o vocabulário de inspeção do
harness; aqui `tests/lifecycle.test.mjs` e `tests/determinism.test.mjs` os
exercitam — `capture` apenas na guarda de ausência de tela. No navegador, o mesmo
contrato está em `window.__game`.
