# Design system — Canvas Arcade

Primitivas por decisão, não placeholder. Orbe e estilhaço se separam por
**forma** (círculo com anel versus losango), não só por cor: o jogo
continua legível em escala de cinza. Paletas canônicas em
`src/game/render.js` (`PALETTES.normal` e `PALETTES.contrast`).

## Tokens

| Papel | Valor | Consumidor |
| --- | --- | --- |
| campo | `#171b26` / `#000000` | `PALETTES.*.field` |
| jogador | `#f2f4f8` / `#ffffff` | `PALETTES.*.player` |
| orbe | `#4ea8ff` / `#00d2ff` | `PALETTES.*.orb` |
| estilhaço | `#ff8a3d` / `#ff6a00` | `PALETTES.*.shard` |
| corrente | `#ffd166` / `#ffe600` | `PALETTES.*.chain` |
| placa | preenchimento + borda | `PALETTES.*.plate` e `plateEdge` |

Escala: 1 unidade = 1 pixel lógico em `FIELD` 320×180. Pivot do jogador no
centro da faixa (`PLAYER_Y`). Sem asset de mundo: a linguagem é geométrica
e cabe neste recorte.

## Receita de um primitivo novo

1. Escolha **forma**, não só cor — o par orbe/estilhaço é o piso.
2. Acrescente o token em `PALETTES.normal` e `PALETTES.contrast`.
3. Desenhe o consumidor em `src/game/render.js`.
4. Registre a linha nesta tabela e a origem em `CREDITS.md`.
5. Se o item for dado, nasça a mesa com `npm run table -- <nome>`.

Isto é a receita, não a prova de que alguém de fora a cumpriu.

## O que isto não afirma

Consistência em movimento ainda não foi observada. Moodboard não substitui
esta página. `consistent` no harness permanece falso.
