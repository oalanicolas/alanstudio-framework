# Design system — Canvas Arcade

Primitivas por decisão, não placeholder. Orbe e estilhaço se separam por
**forma** (círculo com anel versus losango), não só por cor. O stub
distingue as duas silhuetas com a mesma tinta; o dispositivo alvo
não foi observado. Paletas canônicas em
`data/palettes.json` (`normal`, `contrast`, `dusk` e `calm`); o desenho consome
`PALETTES` via `src/game/tables.js`. `look` escolhe `normal`, `dusk` ou `calm`;
`contrast` continua sendo o modo de alcance.

## Tokens

| Papel | Valor | Consumidor |
| --- | --- | --- |
| campo | `#171b26` / `#000000` | `data/palettes.json` → `PALETTES.*.field` |
| jogador | `#f2f4f8` / `#ffffff` | `PALETTES.*.player` |
| orbe | `#4ea8ff` / `#00d2ff` | `PALETTES.*.orb` |
| estilhaço | `#ff8a3d` / `#ff6a00` | `PALETTES.*.shard` |
| corrente | `#ffd166` / `#ffe600` | `PALETTES.*.chain` |
| placa | preenchimento + borda | `PALETTES.*.plate` e `plateEdge` — em `contrast`, campo e placa são pretos; quem separa é a borda branca |

Escala: 1 unidade = 1 pixel lógico em `FIELD` 320×180. Pivot do jogador no
centro da faixa (`PLAYER_Y`). Sem asset de mundo: a linguagem é geométrica
e cabe neste recorte.

## Receita de um primitivo novo

1. Escolha **forma**, não só cor — o par orbe/estilhaço é o piso.
2. Acrescente o token em `data/palettes.json` (`normal`, `contrast` e
   cada look de arte). Trocar só a cor não exige abrir `render.js`.
   Um look novo entra na mesa e o jogo o consome por `?look=` /
   `settings.look` — `dusk` e `calm` já são o segundo e o terceiro.
   Nasça o próximo com
   `npm run look -- <nome> --from dusk|calm --as warmer|cooler|night`.
   Para look e chuva no mesmo nome, `npm run pair -- <nome> --from dusk|calm`.
   Intenção não é look aprovado nem alguém de fora no piso.
3. Se o item for forma nova, desenhe o consumidor em `src/game/render.js`.
4. Registre a linha nesta tabela e a origem em `CREDITS.md`.
5. Se o item for chuva, nasça com `npm run table -- <nome> --from spawn`
   (ou `--from dusk` / `--from calm`) e, se a chuva não for um clone, `--as denser|calmer|brief`.
   O par (`npm run pair`) já nasce a chuva junto do look.
   Confira com `npm run session -- --spawn <nome>`. Outro dado:
   `npm run table -- <nome>` e ligue o consumidor.
6. Se o item for voz, nasça com `npm run sfx -- --from dash --as brighter|darker|tighter`.
   `--as` precisa de `--from`. Intenção não é mix ouvido.

Isto é a receita, não a prova de que alguém de fora a cumpriu.

## O que isto não afirma

Consistência em movimento ainda não foi observada. Moodboard não substitui
esta página. `consistent` no harness permanece falso.
