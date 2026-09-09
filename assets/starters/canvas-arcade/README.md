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
npm test           # regras, determinismo, ciclo de vida, save e mixagem
npm run budget     # custo da simulação, por percentil, sem apresentação
```

A partir da raiz do framework, com recibo:

```sh
python3 scripts/game.py verify . --script test --output /tmp/qa-01 \
  --proves pause --proves reset --proves seed --proves observe \
  --proves act --proves advance --proves capture --proves dispose
```

`--proves` anexa ao recibo a alegação de que a execução exercita essas capacidades,
com autor, argv e log. Aqui a alegação se sustenta porque `tests/lifecycle.test.mjs`
e `tests/determinism.test.mjs` cobrem exatamente essas oito — não porque o harness
tenha conferido. Em um projeto adaptado, só declare o que os seus testes cobrirem:
o recibo sai como `claimed`, nunca como verificado.

Recibo verde comprova os comandos executados. Não comprova arte, ritmo,
diversão nem que o jogo é bom.

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

- [Game Brief](docs/brief.md) · [GDD](docs/gdd.md) · [MDA](docs/mda.md)
- [Arquitetura / TDD](docs/tdd.md) · [Design system](docs/art-bible.md)
- [Devlog](docs/devlog.md) · [QA e playtest](docs/qa.md)
- [Origem de código e assets](CREDITS.md)

Os documentos vêm dos templates do framework e estão em rascunho: preenchê-los
com decisão, fato ou lacuna é o primeiro trabalho real do projeto.

## Degrau de acabamento declarado

Pela [barra de acabamento](../../../references/production-bar.md), o degrau
percebido de um jogo é o **mínimo** entre suas dimensões. O projeto nasce assim, e
a última coluna é o mapa das próximas tarefas: cada linha nomeia o critério do
degrau **imediatamente** seguinte, não o de um degrau distante — é isso que a
torna uma tarefa em vez de uma aspiração.

`python3 <framework>/scripts/game.py bar .` lê esta tabela e devolve o piso, as
dimensões que estão nele e o degrau percebido. Ela é a **afirmação** deste
projeto; o harness confere a forma dela e nada mais. Ao subir uma linha, escreva
junto a condição: dispositivo, versão, cena e quem observou.

| Dimensão | Degrau | Critério do degrau seguinte |
| --- | --- | --- |
| `feel` | `playable` | `slice`: cada ação com sinal próprio de partida, contato e término — falta o som, e o perdão de entrada precisa ser medido, não só anotado |
| `legibility` | `playable` | `slice`: leitura em movimento, na resolução e no dispositivo alvo — o que existe hoje é medição de placa e faixa em quadro estático |
| `art_direction` | `prototype` | `playable`: escala, pivot e linguagem consistentes por decisão registrada; hoje são primitivas que se assumem placeholder |
| `audio_mix` | `prototype` | `playable`: som licenciado nas ações centrais, com origem registrada — os seis papéis estão declarados e vazios |
| `pacing` | `prototype` | `playable`: o primeiro ciclo ensinar a ação sem depender da tabela de comandos da página |
| `state_trust` | `slice` | `shippable`: interrupção abrupta real — aba fechada, perda de foco — além do teste de dado inválido |
| `performance` | `playable` | `slice`: orçamento de quadro declarado e cena representativa medida nele; `npm run budget` mede só a simulação, sem apresentação |
| `accessibility` | `slice` | `shippable`: contraste verificado por medição e opções de dificuldade ou assistência |
| `content_scale` | `prototype` | `playable`: conteúdo como dado, separado da regra e fora do código |
| `release` | `prototype` | `playable`: build ou export que outra pessoa execute a partir do runbook |

**Leitura honesta: este projeto é um protótipo**, porque cinco dimensões estão
nesse degrau. Nenhuma quantidade de acabamento visual muda essa leitura antes
delas subirem.

## Som

O starter **não embarca arquivos de áudio**. `src/game/audio.js` traz a mixagem
— barramentos, prioridade, ducking, legenda — com os seis papéis declarados e
vazios. `audioGaps()`, exposto em `src/main.js`, transforma isso em lacuna
observável: a página a exibe e `tests/lifecycle.test.mjs` a confere. O piso do estúdio
é gravação licenciada ou design contemporâneo; sintetizar bipes aqui escolheria
a estética errada por conveniência.

Para preencher, a partir da raiz do framework:

```sh
python3 scripts/game.py sfx search passos --root <laboratorio>
python3 scripts/game.py sfx copy <id> --to <projeto>/public/sfx --root <laboratorio>
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
src/game/     regras puras, apresentação, mixagem
src/main.js   montagem e contrato de ciclo de vida
tools/        servidor local e medição de orçamento
tests/        regras, determinismo, ciclo de vida, save, mixagem
```

`src/game/rules.js` não conhece DOM, relógio nem aleatoriedade externa: é isso
que permite rodar a partida headless, repetir um replay a partir de uma seed e
comparar duas execuções. `src/core/input.js` reduz teclado, ponteiro e gamepad a
uma intenção — as regras nunca veem eventos.

`src/main.js` implementa `pause`, `resume`, `reset`, `seed`, `observe`, `act`,
`advance`, `capture` e `dispose`. Esses nomes são o vocabulário de inspeção do
harness; aqui `tests/lifecycle.test.mjs` e `tests/determinism.test.mjs` os
provam. No navegador, o mesmo contrato está em `window.__game`.
