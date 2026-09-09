# Gênero — Casual (hypercasual, party, minigames, arcade mobile)

Aplicabilidade: `--genre casual`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: uma ação, entendida em segundos. Decisões: timing (um toque), escolha
  binária, encadear para pontuação; em party, interação social entre jogadores.
- Modelo: hypercasual (um mecanismo, sessões < 2 min, alta repetição), party
  (local, controles simples, humor), arcade mobile (endless runner, high score),
  puzzle casual (ver [puzzle](puzzle.md)). Registre a sessão-alvo e o contexto de uso
  (ônibus, sofá com amigos).

## Feel que importa

- Primeiro toque ensina tudo: sem tutorial em texto; feedback exagerado (squash,
  partículas, som "juicy"); falha rápida e reinício instantâneo (< 1 s).
- Toque: alvos ≥ 44 pt, tolerância de gesto, sem exigir precisão que o dedo não dá;
  uma mão. Party: cada jogador se acha na tela (cor, ícone, posição).

## Riscos habituais

- Mecanismo esgotado em 5 minutos sem variação (novos obstáculos, ritmo,
  "meta" de coleção); dificuldade por sorte; anúncio interrompendo o ritmo;
  sessão que não termina em ponto natural.
- Tamanho do app e tempo de carga acima do que o contexto tolera; consumo de bateria;
  party: um jogador dominante ou eliminado cedo sem o que fazer.

## Orçamentos e medições típicas

- Tempo até jogar (abrir → primeiro input); duração de sessão e de tentativa;
  tempo de reinício; quadro p99 em aparelho de entrada; tamanho do binário; taxa de
  retorno em 24 h se houver telemetria consentida.

## QA e playtest específicos

- Bot de input aleatório e "perfeito" para curva de dificuldade; toque em bordas e
  gestos ambíguos; rotação/interrupção (chamada, notificação) e retomada; party
  com número mínimo e máximo de jogadores.
- Playtest: pessoa que não joga entende sem explicação? Ri ou xinga (bom sinal) ao
  falhar? Passa o celular para outra pessoa mostrar?

## Receitas e fontes

[feel](../../recipes/feel.md), [ciclo de vida](../../recipes/lifecycle.md) (interrupções),
[mecânicas](../../recipes/mechanics.md), [produção](../../recipes/production.md).
Plataformas comuns: [web](../platforms/web.md), [flutter](../platforms/flutter.md),
[construct](../platforms/construct.md).
