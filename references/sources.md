# Mapa dos estudos utilizados

Consulta sob demanda. As fontes externas pertencem aos commits estudados em
8 de setembro de 2026. Confira a fonte atual antes de aplicar uma conclusão
histórica. Catálogos locais enriquecem a consulta quando existem; não são
dependência do executor Python.

Defina `GAMES_FRAMEWORKS_ROOT` ou mantenha um irmão `Games-Frameworks` ao lado
do laboratório de jogos. Ausência deixa `studies` vazio; isso não é evidência
negativa.

## Recortes estudados

57 rastros; 150 candidatos: 115 observados em fonte, 22 precisam de confirmação,
13 excluídos, zero promovidos a testados. Integridade dos catálogos foi
verificada no laboratório; testes dos frameworks externos não foram executados.
Cada regra herda o limite do recorte, não descreve necessariamente o framework
inteiro.

| Recorte | Commit | O que entrou no harness |
|---|---|---|
| [BMad Game Dev Studio](https://github.com/bmad-code-org/bmad-module-game-dev-studio) | `2486f5f5f3b8` | leitura por etapa e retomada em **create** |
| [Phaser](https://github.com/phaserjs/phaser) | `02d8931b626d` | pausa, visibilidade e operações em **lifecycle** |
| [Excalibur](https://github.com/excaliburjs/Excalibur) | `4a23dd1674b1` | tempo controlado e limite de prova em **lifecycle/visual** |
| [Godot Demo Projects](https://github.com/godotengine/godot-demo-projects) | `0db80ca5fd22` | reinício, colisão e timers em **lifecycle** |
| [boardgame.io](https://github.com/boardgameio/boardgame.io) | `5e9a2c94bde8` | ações recusadas e identidade em **mechanics/network** |
| [Ink](https://github.com/inkle/ink) | `35c63e52f1d3` | histórico e versões em **content** |
| [LDtk](https://github.com/deepnight/ldtk) | `6d69bd1d6be9` | IDs, migração e níveis externos em **content** |
| [PettingZoo](https://github.com/Farama-Foundation/PettingZoo) | `a865c24671b2` | observação, término e seed em **lifecycle/network** |

Nenhuma regra foi copiada como mecânica obrigatória para todos os gêneros.
`context --focus` lista os catálogos deste mapa que existirem no irmão.

**A cobertura não é uniforme, e isso não é acidente.** Só seis focos têm catálogo:
`create`, `mechanics`, `lifecycle`, `content`, `visual` e `network` — os que
correspondem aos recortes efetivamente estudados. Em `architecture`, `feel`,
`performance`, `accessibility`, `audio`, `persistence` e `release`, `studies` vem
vazio, porque não houve extração para eles. Vazio aqui significa **não estudado**,
não “nada relevante existe”. Preencher esses focos exigiria novos recortes com o
mesmo rigor; inventar citações para emparelhar a lista seria o oposto do que este
mapa existe para fazer.

## Pré-produção e checagem

Na versão 0.2, leitura adicional dos templates no mesmo commit BMad
`2486f5f5f3b8870baa6cee4615a870c0330f441c`. Não foi uma nova extração Code
Anatomist nem execução dos workflows BMad.

- Game Brief, GDD, PRD, arquitetura e playtest do módulo BMad, adaptados aos
  templates em [assets/templates](../assets/templates).
- [MDA, artigo original](https://www.cs.northwestern.edu/~hunicke/MDA.pdf).
- Distinção varredura × inspeção profunda, adaptada do fluxo document-project
  do BMad, no [roteiro de auditoria](project-audit.md).

Os templates foram redigidos em português. Não importam a hierarquia de agentes,
instalação, publicação ou cerimônias BMad.

## Arquitetura (0.8)

A receita [architecture](../recipes/architecture.md) adapta processo transversal
observado no Architect AIOX, sem copiar o runtime, o roteador de engines nem a
hierarquia de agentes. Estudo e hashes ficam no laboratório.

## Barra de acabamento (0.9)

A [escada](production-bar.md) **não** vem de uma fonte externa citável. Ela é uma
síntese redigida neste repositório a partir de três origens, e é honesto separá-las:

- **Critérios já presentes aqui**, reorganizados por dimensão e degrau: o roteiro
  de [qualidade](quality.md), o contrato do
  [design system do jogo](game-design-system.md) e as regras de ciclo de vida
  vindas dos recortes de Phaser, Excalibur, Godot Demo Projects e PettingZoo.
- **Vocabulário corrente da indústria** — protótipo, vertical slice, publicável —
  usado no sentido de dependência entre etapas, não como certificação.
- **Julgamento editorial deste estúdio** sobre o que o jogador percebe primeiro,
  em especial a regra do mínimo entre dimensões.

O formato de declaração que `bar` lê — tabela em Markdown, uma linha por dimensão
— também não vem de fora: ele foi extraído da tabela que o README do starter já
tinha escrita à mão, e o comando passou a ler o que já existia em vez de pedir um
arquivo novo. Nenhuma das dez dimensões ganhou limiar numérico nessa passagem: o
que o harness confere é a forma da linha, e a escada continua sem calibração
contra uma amostra de jogos publicados.

Nenhum degrau foi calibrado contra uma amostra de jogos publicados, e nenhuma
medição foi repetida para produzir esta escada. Os limites numéricos que aparecem
nas dimensões `performance` e `audio_mix` são pontos de partida a confirmar no
dispositivo alvo, não constantes verificadas. Trate a escada como linguagem
compartilhada para observar, não como aferição.

## Gates de produção (0.9)

Os dez gates de [gates.md](gates.md) têm procedência interna e verificável: cada
critério é extraído de uma linha `**Pronto para…**` que já estava escrita em
[preproduction.md](preproduction.md), uma por etapa. Nada ali foi inventado na
passagem, e um teste do harness exige que cada gate continue apontando para a
prosa de origem. A regra de quais critérios **não** são dispensáveis também não é
escolha do harness: são os quatro em que a prosa da etapa não deixa terceira
opção, com a frase citada na tabela do próprio `gates.md`.

O que **não** vem de dentro é a estrutura de três saídas — passar, cortar escopo,
abandonar. Ela vem de uma única fonte, e é preciso dizer o que essa fonte é:

| Fonte | O que é | O que sustenta |
| --- | --- | --- |
| [20 Game Dev Tips](https://youtu.be/fqb9MfRqK9I) | Vídeo de um desenvolvedor indie, patrocinado, dirigido a iniciantes, sem citação de estudo ou dado | Que praticantes tratam abandonar como decisão legítima, e que decidir cedo é melhor que decidir tarde |

Isso é **conselho de praticante**, não evidência. Sustenta “há quem defenda isso e
por quê”; não sustenta “isso funciona”. Peguei dela uma coisa só: a legitimação de
abandonar como saída de gate, que o ciclo já tinha na etapa `poc` (“continuar,
ajustar ou abandonar”) e que passou a valer nas dez. A generalização é julgamento
editorial deste estúdio, apoiada numa coerência interna, não na autoridade do
vídeo.

A segunda coisa que veio de lá é menor e está na [receita de
arquitetura](../recipes/architecture.md): o repositório já dizia para não
generalizar cedo e não dizia nada sobre o erro contrário, o de seguir improvisando
depois que as cópias se acumularam. O vídeo trata os dois lados e admite que a
escolha é um palpite. A adaptação — declarar a contagem-limite no TDD, com data e
autor, em vez de mantê-la na cabeça — é deste repositório, e segue a mesma lógica
que já vale para a barra e para os gates: transformar julgamento implícito em
declaração contestável. Nenhum número foi importado.

O que recusei da mesma fonte, para não dar a impressão de que absorvi o material
inteiro: o limiar de “80% pronto, então termine” é número sem origem, e não entrou
em critério nenhum. “Sua engine não importa” contradiz a receita de arquitetura
deste repositório e é simplificação para iniciante. Os conselhos sobre sorte,
dinheiro e tutoriais não são critério de avanço de nada. E cerca de metade do
vídeo descreve práticas que este framework já tinha — feel antes de conteúdo,
prototipar antes de decidir, documento de design, consistência de estilo, reusar
o que existe, definir público e sensação pretendida —, o que serve como
convergência independente, não como fonte nova.

## Starter `canvas-arcade` (0.9)

Escrito neste repositório, sem dependências de terceiros. `mulberry32`, em
`src/core/rng.js`, é algoritmo de domínio público amplamente publicado; o
embaralhamento de bits em `src/core/hash.js` pertence à mesma família. O starter
não embarca imagem, som nem fonte — proveniência completa em
[CREDITS.md](../assets/starters/canvas-arcade/CREDITS.md).

Seus testes rodam neste repositório e exercitam o ciclo de vida, o determinismo e
a migração de save do próprio starter — com duas exceções ditas: `capture` só é
exercitada na guarda de ausência de tela, e nenhum teste interrompe a gravação no
meio. Nada disso alcança um jogo derivado depois que ele for adaptado.

## Áudio

O acervo `shared/sfx` é do laboratório, não deste repositório. O harness expõe
`sfx search` / `sfx copy` quando essa pasta existir na raiz de `--root`.

## Playground

Os jogos públicos da Alan Studios ficam em [games.alanicolas.com](https://games.alanicolas.com/).
Cada um usa a própria engine. Este harness não reivindica tê-los produzido.
