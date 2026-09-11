# Gênero — Tower defense (fixo, livre, híbrido com ação)

Aplicabilidade: `--genre tower-defense`. Orientação de gênero para direcionar
perguntas, riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: preparar para a onda. Decisões: onde e o que construir, quando melhorar vs
  expandir, quando vender, como moldar o caminho (maze), como gastar entre ondas.
- Modelo: caminho fixo (posições de torre), construção livre (o jogador cria o
  labirinto), híbrido (herói controlável ou ação em tempo real). Registre e defina o
  tempo entre ondas (pausa, acelerar, iniciar cedo por bônus).

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Colocação: preview com alcance, snap, validação instantânea de caminho bloqueado;
  som e animação de construção; venda com feedback.
- Ondas legíveis: preview da próxima onda, contagem, inimigos com silhueta por tipo
  (voador, blindado, rápido); projéteis que acertam visualmente (homing ou
  antecipação).
- Acelerar tempo (2×/3×) sem quebrar física ou som.

## Riscos habituais

- Uma torre dominante (DPS/custo); ondas que só escalam HP; pathfinding com labirinto
  livre (recalcular sem travar; inimigos presos ao bloquear); vazamento de dano por
  projétil perdido.
- Sem informação: alcance real, prioridade de alvo, DPS não visíveis; ondas finais
  decididas pela economia das primeiras (sem recuperação).

## Orçamentos e medições típicas

- Quadro p99 na onda final com máximo de inimigos + projéteis + torres em velocidade
  3×; tempo de recálculo de caminho ao construir; balanceamento por simulação: taxa
  de vitória por estratégia simples/ótima por mapa.

## QA e playtest específicos

- Simulação headless de ondas com builds fixas (a "build óbvia" deve perder em
  algum ponto e a "build boa" deve vencer); validação de caminho em labirintos;
  determinismo em 1×/3×; pausa entre ondas.
- Playtest: a pessoa lê o alcance antes de construir? Reage à onda preview? Repete
  o mapa com outra estratégia?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md) (economia, passo fixo), [feel](../../recipes/feel.md),
[visual](../../recipes/visual.md) (legibilidade), [produção](../../recipes/production.md).
Vizinhos: [strategy](strategy.md), [idle](idle.md) (TD incremental).
