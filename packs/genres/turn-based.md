# Gênero — Turno (tabuleiro, cartas, tático, estratégia por turnos)

Aplicabilidade: `--genre turn-based`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: planejar e comprometer-se. Decisão sob informação parcial, com custo de
  oportunidade legível. Toda ação tem recusa definida: recurso insuficiente, alvo
  inválido, fora do turno, após o término.
- Estrutura: fases por turno, ordem de iniciativa, fim de partida e desempate. O
  estado deve ser serializável e a regra determinística dada a seed.

## Feel que importa

- Confirmação e cancelamento claros; previsão do resultado antes de confirmar;
  animação que resume a resolução sem atrasar quem já entendeu (acelerar/pular).
- Feedback de erro sem punição (ação recusada explicada); som e movimento nos pontos
  de virada, não em cada clique.

## Riscos habituais

- Estado mutado fora do reducer/executor de ações; ação recusada que consome turno;
  vitória disparada duas vezes.
- Opção dominante e IA trivial; turnos longos sem decisão.
- Rede: autoridade, identidade do jogador, ações fora de ordem, reconexão no meio do
  turno, informação oculta vazando ao cliente.

## Orçamentos e medições típicas

- Tempo de resolução de turno da IA; tamanho do estado serializado; latência de
  sincronização por ação; duração média de turno humano observada.

## QA e playtest específicos

- Testes de invariantes por ação (nunca duplica recurso, recusa não consome turno);
  replays por seed; salvar/recarregar em cada fase; duas sessões reais quando online.
- Playtest: a pessoa entende por que perdeu? Prevê o resultado antes de confirmar?
  Há decisões que ela nunca considera?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md) e [rede](../../recipes/network.md)
(boardgame.io: ações recusadas, identidade), [ciclo de vida](../../recipes/lifecycle.md) (seed).
