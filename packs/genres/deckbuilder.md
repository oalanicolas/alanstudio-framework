# Gênero — Cartas e deckbuilding (card battler, TCG/CCG, roguelike de cartas)

Aplicabilidade: `--genre deckbuilder`. Orientação de gênero para direcionar
perguntas, riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: compor e sequenciar. Decisões: qual carta adicionar/remover, ordem de
  jogada com recurso limitado (mana/energia), quando comprar/descartar, gestão de
  variância.
- Modelo: roguelike de cartas (run, deck cresce, permadeath), TCG/CCG (coleção,
  construção fora da partida, PvP), deckbuilder de tabuleiro digital. Registre as
  regras de zona (mão, deck, descarte, exílio) e a fonte de aleatoriedade.

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Manipulação física das cartas: arrastar com inércia, hover que amplia e lê,
  alvo com seta/highlight de válidos, ordem visível do descarte; animação de efeito
  rápida e pulável (segurar para acelerar).
- Cálculo visível: dano previsto no alvo, bloqueio, intenção do inimigo; efeitos
  encadeados com log legível.

## Riscos habituais

- Motor de regras sem ordem de resolução clara (triggers, pilha); exceções por carta
  hardcoded; texto de carta ambíguo vs implementação; sinergias infinitas não
  intencionais (ou intencionais sem teto).
- Variância que decide a run (sem mitigação: compra, remoção, reroll); cartas
  inúteis que só diluem; TCG: economia de coleção e pity; PvP: sincronia de estado
  oculto (mão do adversário no cliente).

## Orçamentos e medições típicas

- Tempo por turno da IA; tempo de animação por carta (pulável); win rate por
  arquétipo e por carta em milhares de runs headless; taxa de pick por carta em
  oferta; duração de run/partida.

## QA e playtest específicos

- Motor de regras com testes por carta e por interação (tabela de casos); replays
  com seed; fuzzing de sequências de jogadas; simulação headless com IA gulosa para
  outliers de balanceamento; estado oculto só no servidor (PvP).
- Playtest: a pessoa lê a carta e prevê o efeito? Sente que o deck é "dela"? A
  derrota vem de decisão ou de compra?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md) (regras, RNG com seed), [arquitetura](../../recipes/architecture.md)
(dados de cartas), [feel](../../recipes/feel.md), [produção](../../recipes/production.md).
Vizinhos: [roguelike](roguelike.md), [turn-based](turn-based.md), [multiplayer competitivo](multiplayer-competitive.md).
