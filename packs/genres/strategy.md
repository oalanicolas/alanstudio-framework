# Gênero — Estratégia (RTS, 4X, grand strategy, auto battler)

Aplicabilidade: `--genre strategy`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: alocar sob incerteza. Decisões: economia vs militar, expansão vs
  consolidação, informação (scouting, fog of war), tempo (RTS: APM e prioridade;
  4X: turnos e planejamento longo).
- Modelo: RTS (tempo real, micro/macro), 4X (explorar, expandir, explorar, exterminar),
  grand strategy (simulação histórica, sistemas em rede), auto battler (composição,
  economia por rodada). Registre e defina a duração da partida.

## Feel que importa

- Seleção e ordens instantâneas: hitbox generosa, feedback de ordem (marcador, voz),
  pathfinding que não trava grupos; hotkeys e control groups.
- Legibilidade: silhuetas por facção, ícones sobre a arte, minimapa que é jogável,
  fog of war claro. UI é o jogo — orçamento de arte para ela.

## Riscos habituais

- Simulação não determinística (RTS multiplayer usa lockstep: floats, ordem de
  iteração, RNG por partida); dessincronização silenciosa.
- IA que trapaceia visivelmente ou não desafia; snowball sem contrajogo;
  microgerenciamento tedioso no late game (4X); UI que esconde estado crítico.
- Balanceamento com muitas unidades/tecnologias: teste combinatório explode.

## Orçamentos e medições típicas

- Quadro p99 com máximo de unidades em combate + pathfinding; tempo de turno da IA
  (4X); tamanho e tempo de save em late game; deriva de estado em lockstep (hash por
  tick); duração média de partida por modo.

## QA e playtest específicos

- Replays por inputs com hash de estado por tick (detecta dessincronização); IA×IA
  headless para win rate por facção/mapa; pathfinding com formações em corredores;
  stress de unidades.
- Playtest: a pessoa toma decisão nos primeiros 2 minutos? Entende por que perdeu?
  Late game continua interessante ou só demora?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md) (determinismo, economia), [arquitetura](../../recipes/architecture.md),
[rede](../../recipes/network.md) (lockstep), [produção](../../recipes/production.md).
Ver [turn-based](turn-based.md) para tático e [tower defense](tower-defense.md).
