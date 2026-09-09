# {{PROJECT_TITLE}}

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

Pela [barra de acabamento]({{FRAMEWORK_PATH}}/references/production-bar.md), o degrau
percebido de um jogo é o **mínimo** entre suas dimensões. Este starter começa
assim, e a coluna “o que falta” é o mapa das próximas tarefas:

| Dimensão | Degrau | O que falta para o próximo |
| --- | --- | --- |
| `feel` | jogável | som de contato e observação em movimento |
| `legibility` | jogável | leitura confirmada em cena cheia, no dispositivo alvo |
| `art_direction` | protótipo | design system preenchido, com tokens que têm consumidor |
| `audio_mix` | protótipo | os seis papéis sonoros declarados ainda estão vazios |
| `pacing` | protótipo | playtest com alguém que nunca viu o jogo |
| `state_trust` | fatia | interrupção abrupta real, além do teste de dado inválido |
| `performance` | jogável | orçamento de quadro medido na plataforma alvo |
| `accessibility` | fatia | contraste verificado e opções de dificuldade |
| `content_scale` | protótipo | conteúdo como dado, fora do código |
| `release` | protótipo | build exportável verificado fora desta máquina |

**Leitura honesta: este projeto é um protótipo**, porque quatro dimensões estão
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
áudio desligado, e precisa continuar sendo.

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
