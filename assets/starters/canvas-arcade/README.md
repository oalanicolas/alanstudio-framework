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
npm run serve      # abre em http://localhost:8080
```

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
npm run budget     # custo da simulação, por percentil, sem apresentação
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

Os sete de `docs/` são escritos pelo `init` a partir dos templates do framework:
neste starter lido no lugar eles ainda não existem, e é por isso que estão em
código e não em link. Nascem em rascunho. O primeiro trabalho real do projeto é
**jogar o ciclo** — `npm run serve` — e escrever o que a proposta muda no verbo.
Preencher os sete templates antes da primeira partida é o atrito que o `next`
depois do `init` recusa. Com `init --no-docs`, os rascunhos não nascem.

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
| `feel` | `playable` | `slice`: cada ação com sinal próprio de partida, contato e término — falta o som, e o perdão de entrada precisa ser medido, não só anotado |
| `legibility` | `playable` | `slice`: leitura em movimento, na resolução e no dispositivo alvo — o que existe hoje é medição de placa, borda e faixa em quadro estático |
| `art_direction` | `prototype` | `playable`: escala, pivot e linguagem consistentes por decisão registrada; hoje são primitivas que se assumem placeholder |
| `audio_mix` | `prototype` | `playable`: som licenciado nas ações centrais, com origem registrada — os seis papéis estão declarados e vazios |
| `pacing` | `prototype` | `playable`: o primeiro ciclo ensinar a ação sem depender da tabela de comandos da página |
| `state_trust` | `slice` | `shippable`: interrupção abrupta real — aba fechada, perda de foco — além do teste de dado inválido |
| `performance` | `playable` | `slice`: orçamento de quadro declarado e cena representativa medida nele; `npm run budget` mede só a simulação, sem apresentação |
| `accessibility` | `slice` | `shippable`: contraste verificado por medição e opções de dificuldade ou assistência |
| `content_scale` | `playable` | `slice`: receita do próximo item da família com o mesmo carregador — hoje são a chuva e o texto do HUD |
| `release` | `prototype` | `playable`: outra pessoa executou o artefato a partir do runbook; `npm run build` existe e ninguém o correu fora daqui |

**Leitura honesta: este projeto é um protótipo**, porque quatro dimensões estão
nesse degrau. Nenhuma quantidade de acabamento visual muda essa leitura antes
delas subirem.

## Ofício declarado

Checklists da [§7 do levantamento](../../../references/observable-criteria-research.md):
conformidade com o que **este** projeto declara, sem limiar importado.
`python3 <framework>/scripts/game.py craft .` lê a tabela. `observed` continua
falso — a linha é afirmação de quem escreveu.

| Check | Estado | Evidência |
| --- | --- | --- |
| `canvas_scale` | `met` | FIELD em src/game/rules.js; canvas em index.html; o resize em render.js usa a escala calculada quando a divisão não é inteira — starter |
| `forgiveness` | `met` | dashBufferTicks, invulnTicks, collect.pad e collect.reachY em CONFIG, src/game/rules.js, unidade em ticks — starter |
| `percentile_def` | `met` | tools/budget.mjs declara o percentil por definição, não por apelido — starter |
| `palette` | `unmet` | primitivas; paleta ainda não é contrato — starter |
| `style_factor` | `out_of_scope` | sem assets de mundo de estilo; só primitivas — starter |
| `budget_delta` | `unmet` | npm run budget mede a simulação; comparação com o build anterior ainda não existe — starter |
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

O starter **não embarca arquivos de áudio**. `src/game/audio.js` traz a mixagem
— barramentos, prioridade, ducking, legenda — com os seis papéis declarados e
vazios. `audioGaps()`, exposto em `src/main.js`, transforma isso em lacuna
observável: a página a exibe e `tests/lifecycle.test.mjs` a confere. O piso do estúdio
é gravação licenciada ou design contemporâneo; sintetizar bipes aqui escolheria
a estética errada por conveniência.

Para preencher, a partir da raiz do framework:

```sh
python3 scripts/game.py roles <projeto> --fill --root <laboratorio>
python3 scripts/game.py roles <projeto> --fill --apply --root <laboratorio>
```

Toda informação sonora já tem legenda equivalente: o jogo é completável com o
áudio desligado, e precisa continuar sendo. Enquanto os papéis estão vazios, a
legenda **é** a informação sonora, então ela tem faixa própria — encostada à
direita, abaixo do relógio, posicionada a partir dos retângulos que o HUD
reserva — e junta repetições consecutivas em uma linha com contagem. No centro
inferior, onde nascia, ela caía sobre o jogador e sobre o rótulo do dash:
`tests/render.test.mjs` mede isso em vez de confiar no olho.

## Estrutura

```
src/core/     laço de passo fixo, entrada, RNG, impressão, armazenamento, save, preferências
src/game/     regras puras, apresentação, mixagem, mesas e carga de sfx
src/main.js   montagem e contrato de ciclo de vida
data/         conteúdo separado da regra (chuva e texto do HUD)
tools/        servidor local, medição de orçamento e export
tests/        regras, determinismo, ciclo de vida, save, mixagem, export
```

`src/game/rules.js` não conhece DOM, relógio nem aleatoriedade externa: é isso
que permite rodar a partida headless, repetir um replay a partir de uma seed e
comparar duas execuções. `src/core/input.js` reduz teclado, ponteiro e gamepad a
uma intenção — as regras nunca veem eventos.

A paleta vive em `src/game/render.js` (`PALETTES`). O harness a lê; consistência
em movimento continua pendente. Chuva e texto do HUD passam por
`src/game/tables.js`. Duas mesas não são uma família. `public/sfx/<papel>`
entra no mixer quando o arquivo existe; copiar sem consumidor deixava o
jogo mudo. `npm run build` copia a árvore jogável para `dist/`; isso não é
outra pessoa tendo jogado o artefato.

`src/main.js` implementa `pause`, `resume`, `reset`, `seed`, `observe`, `act`,
`advance`, `capture` e `dispose`. Esses nomes são o vocabulário de inspeção do
harness; aqui `tests/lifecycle.test.mjs` e `tests/determinism.test.mjs` os
exercitam — `capture` apenas na guarda de ausência de tela. No navegador, o mesmo
contrato está em `window.__game`.
