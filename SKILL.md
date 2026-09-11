---
name: game-dev
description: Criar, evoluir, avaliar, produzir e verificar jogos com IA, partindo do acervo existente, até o acabamento pretendido. Roteia por intenção (craft, shape, critique, polish, feel, audio, next…) sobre um harness thin que recorta contexto, lê declarações e registra evidência.
metadata:
  version: 0.10.1
---

# Game Dev

Use esta skill em qualquer engine. O objetivo é uma experiência jogável no
acabamento pretendido, preservando a direção do usuário e a qualidade já aprovada.
O arquivo de entrada orienta; detalhes operacionais vivem nas referências.
“AAA” aqui significa piso observável de acabamento, não tier de publisher.

## Preparação

1. **Resolva o contexto uma vez.** Para um jogo identificável, execute
   `python3 scripts/game.py context <projeto> --focus <foco>` a partir do diretório
   desta skill e consuma o JSON inteiro. Num workspace ligado, use
   `python3 framework/scripts/game.py context ...`. Não repita na mesma sessão, salvo
   após mudança de base (`teach`, `document`, `direction-approved`) ou retomada.
2. **Carregue a rota certa.** Com subcomando explícito, leia
   `commands/<comando>.md`. Sem subcomando, siga
   [navegação contextual](references/routing.md). Para jogo ou direção realmente
   novos, leia [trabalho novo](references/new-work.md). A verdade já aprovada vence
   qualquer default.
3. **Carregue o piso no momento certo.** Imediatamente antes de editar design,
   código, conteúdo, arte ou áudio, leia [piso de execução](references/craft-floor.md).
   Não o carregue para simples triagem, planejamento ou leitura.

Se a raiz ou a ligação estiver em dúvida, rode `doctor --root <laboratório>`. O
`doctor` relata drift; nunca repare binding, dependências ou contexto como efeito
colateral. O [manual operacional](references/operations.md) preserva a semântica
minuciosa do harness e deve ser consultado quando uma distinção de evidência ou de
comando não estiver resolvida pela rota específica.

## Como decidir

O pedido e o brief vigente vencem. Refinar preserva a direção; substituir ou
redesenhar exige autorização explícita. Ausência de documento não transforma jogo
existente em tela em branco. Pergunte apenas pelo que mudaria materialmente fantasia,
verbo, escala, plataforma, restrição ou prova de conclusão.
As escalas canônicas do harness são `jam`, `product` e `aa`; elas controlam volume
de entrega, nunca o piso de qualidade do verbo.

Escolha a lente pela superfície pedida, não pelo projeto inteiro:

- **Jogar:** o jogador percebe, decide, age, recebe consequência e consegue recomeçar.
- **Criar:** o autor constrói, importa, combina, testa ou remixa conteúdo com retorno claro.
- **Operar:** o estúdio diagnostica, valida, empacota, publica ou sustenta o jogo.
- **Aprender:** alguém entende regras, controles, decisões ou documentação sem adivinhar.

## Comandos

| Comando | Categoria | Uso | Referência |
| --- | --- | --- | --- |
| `craft [projeto] [mudança]` | Construir | Shape confirmado e fatia jogável de ponta a ponta | [craft](commands/craft.md) |
| `shape [projeto] [mudança]` | Construir | Brief da rodada antes de código | [shape](commands/shape.md) |
| `teach [projeto]` | Construir | Base documental por análise profunda | [teach](commands/teach.md) |
| `document [projeto]` | Construir | Design system extraído do jogo existente | [document](commands/document.md) |
| `init [destino]` | Construir | Jogo novo a partir de starter | [init](commands/init.md) |
| `critique [projeto] [recorte]` | Avaliar | Revisão em movimento pela barra de acabamento | [critique](commands/critique.md) |
| `audit [projeto]` | Avaliar | Checagem técnica e de forma, sem corrigir | [audit](commands/audit.md) |
| `playtest [projeto] [cenário]` | Avaliar | Observação estruturada com pessoas | [playtest](commands/playtest.md) |
| `polish [projeto]` | Refinar | Elevar a dimensão mais baixa da barra | [polish](commands/polish.md) |
| `feel [projeto] [verbo]` | Refinar | Peso, timing e recuperação da ação central | [feel](commands/feel.md) |
| `audio [projeto] [ação]` | Refinar | Mix informativo, origem e licença | [audio](commands/audio.md) |
| `harden [projeto]` | Refinar | Estado, saves, interrupção e pior caso | [harden](commands/harden.md) |
| `onboard [projeto]` | Refinar | Primeiro minuto que ensina o verbo | [onboard](commands/onboard.md) |
| `distill [projeto]` | Refinar | Cortar até o que sustenta o verbo | [distill](commands/distill.md) |
| `juice [projeto] [ação]` | Ampliar | Tornar a consequência perceptível no impacto | [juice](commands/juice.md) |
| `visual [projeto] [alvo]` | Ampliar | Direção de arte, mundo, HUD e câmera | [visual](commands/visual.md) |
| `content [projeto] [família]` | Ampliar | Receita e pipeline repetíveis de conteúdo | [content](commands/content.md) |
| `adapt [projeto] [dispositivo]` | Corrigir | Entrada, dispositivo e acessibilidade | [adapt](commands/adapt.md) |
| `optimize [projeto] [cena]` | Corrigir | Estabilidade sob orçamento sem degradar arte | [optimize](commands/optimize.md) |
| `clarify [projeto] [cena]` | Corrigir | Legibilidade do estado por forma e movimento | [clarify](commands/clarify.md) |
| `next [projeto]` | Produzir | Próxima ação derivada do estado no disco | [next](commands/next.md) |
| `produce [projeto] [marco]` | Produzir | Plano e gates da fatia até o marco | [produce](commands/produce.md) |
| `release [projeto]` | Produzir | Caminho repetível do repositório ao jogador | [release](commands/release.md) |

O catálogo executável é [commands/commands.json](commands/commands.json). As regras
para criar ou alterar comandos estão em [commands/README.md](commands/README.md).

## Roteamento

- **Sem argumento:** siga `references/routing.md`; inspecione sinais uma vez, lidere
  com duas ou três recomendações justificadas e só então mostre o menu completo.
- **Primeira palavra é comando:** leia a referência correspondente e trate o resto
  como alvo e recorte. A preparação não se reinvoca dentro do comando.
- **Primeira palavra não é comando:** escolha a intenção mais próxima. Para criação
  ou substituição de direção, use `references/new-work.md`; para trabalho incumbente,
  preserve a verdade existente e roteie ao comando mais específico.
- **Contexto stale ou binding divergente:** informe o problema e o comando de reparo;
  não altere a instalação silenciosamente.

## Fixar e desafixar

`python3 scripts/game.py pin <comando> --root <lab>` cria um atalho do host;
`unpin` remove apenas atalhos marcados pela Game Dev. Nunca sobrescreva uma skill do
usuário. Relate o resultado em uma linha.

## Encerramento

Faça a [revisão de entrega](references/delivery.md): pedido → aceite → artefato →
prova → continuidade. Use uma passagem agrupada de verificação, corrija problemas
materiais e faça uma confirmação final; não transforme QA em loop infinito. Entregue
resultado, evidência, limitação material e próxima ação em linguagem de produto.
