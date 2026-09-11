# Distill

Cortar até o que sustenta o verbo: remover sistemas, conteúdo, opções e telas que
não mudam decisão nem consequência. Cortar escopo é uma das três saídas legítimas
de um gate; abandonar é a terceira, e costuma ser a que falta. Use quando o jogo
ficou grande e irregular — lido como protótipo apesar da quantidade.

## Escala

`jam`: um verbo, uma decisão, um ciclo; tudo que não serve a isso sai. `product`:
o MVP é a menor entrega que testa a hipótese de valor; quantidade menor preserva o
acabamento aprovado. `aa`: escopo focado é a própria definição da escala; reduza
conteúdo, nunca o piso.

## Avaliar

1. `context <projeto> --focus mechanics`; `gate <projeto>` e `bar <projeto>`.
   Os três critérios `must_meet` (`close.decision`, `implement.worth_building`,
   `scale.worth_scaling`) perguntam se isto ainda vale o que custa; pendência neles
   não se resolve trabalhando mais ([gates](../references/gates.md)).
2. Qual é o **único** objetivo do jogador aqui? Para cada sistema, tela, opção e
   família de conteúdo: muda a decisão? muda a consequência? Se não, é candidato.
3. Onde está o piso da barra e quantas dimensões estão abaixo dele? Um jogo grande
   com feel de protótipo perde mais cortando conteúdo do que subindo feel em tudo.
4. Pergunte só a decisão indispensável: o que o usuário exige manter (critério
   `user_requirements`, não dispensável) e o que está disposto a abandonar.

## Executar

Corte por causa, não por lista: consolide sistemas que competem pela mesma decisão;
esconda complexidade atrás de um ponto de entrada quando precisa existir; remova
opções sem consequência; uma ação principal, poucas secundárias. Conteúdo removido
fica registrado com motivo e o que precisaria mudar para voltar. Regras e recusa:
[mecânicas](../recipes/mechanics.md); contrato de escala: [ambição](../references/ambition.md).

## Verificar

O ciclo ainda atravessa perceber → decidir → agir → consequência → reinício; a
decisão característica continua existindo; o piso da barra subiu porque há menos
dimensões abaixo dele, não porque a média melhorou. A saída escolhida (cortar ou
abandonar) está no devlog com autor.

## Nunca

- Remover o que o usuário exigiu explicitamente.
- Cortar o piso do verbo (feel, áudio, pacing) para caber no prazo: isso é
  rebaixar, não destilar.
- Simplificar até o mistério: a alternativa e a consequência continuam legíveis.
- Fingir que abandonar é falha do processo.

## Entregar

O que saiu, por quê, o que ficou, e a nova fronteira registrada no brief e no
plano. Se a resposta honesta foi abandonar, diga isso. Sequência: [`polish`](polish.md)
no que ficou.
