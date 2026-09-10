# Design system — Canvas Arcade

Primitivas por decisão, não placeholder. Orbe, estilhaço e jogador se
separam por **forma** (círculo com anel, losango, corpo que aponta),
não só por cor. A ponta segue o último avanço e fica com menos
movimento: é forma, não brilho. O halo do orbe e do estilhaço some
com redução; a vinheta também. O stub distingue as silhuetas com a
mesma tinta; o dispositivo alvo não foi observado. Paletas canônicas em
`data/palettes.json` (`normal`, `contrast`, `dusk` e `calm`); o desenho consome
`PALETTES` via `src/game/tables.js`. `look` escolhe `normal`, `dusk` ou `calm`;
`contrast` e a tinta estável (`colorblind`) são alcance, não look.
A tinta não esmaga chuva que já separa quente e frio; o par do padrão
é o fallback. A porta chove o risco da mesa vigente — dusk mais
estilhaço, calm menos — sem RNG. JSON no disco não é comparação em movimento.

## Tokens

| Papel | Valor | Consumidor |
| --- | --- | --- |
| fundo | `#10131a` / `#000000` | `PALETTES.*.background` — casca da página |
| campo | `#171b26` / `#000000` | `data/palettes.json` → `PALETTES.*.field` |
| jogador | `#f2f4f8` / `#ffffff` | `PALETTES.*.player` — o corpo em descanso; o coil do avanço, o coil da guarda e o avanço vestem a corrente; a recuperação veste o apoio, não o orbe |
| orbe | `#4ea8ff` / `#00d2ff` | `PALETTES.*.orb` — chuva e contorno da prática |
| estilhaço | `#ff8a3d` / `#ff6a00` | `PALETTES.*.shard` |
| corrente | `#ffd166` / `#ffe600` | `PALETTES.*.chain` — pips, rastro do avanço e contorno da folga |
| texto | `#e7ebf3` / `#ffffff` | `PALETTES.*.text` |
| apoio | `#8a93a6` / `#c9c9c9` | `PALETTES.*.muted` — HUD em descanso |
| perigo | `#ff5d5d` / `#ff2b2b` | `PALETTES.*.danger` — fecho, impacto e raspo |
| placa | preenchimento + borda | `PALETTES.*.plate` e `plateEdge` — em `contrast`, campo e placa são pretos; quem separa é a borda branca |

As janelas do campo não são faixa no HUD. Prática contorna na tinta
do orbe; a folga da guarda, na da corrente; o fecho, na do perigo.
Com menos movimento viram traço. `--as warmer|cooler|night` desloca
campo e orbe; estilhaço e perigo permanecem. Token no disco não é
comparação em movimento.

Escala: 1 unidade = 1 pixel lógico em `FIELD` 320×180. Pivot do jogador no
centro da faixa (`PLAYER_Y`). Sem asset de mundo: a linguagem é geométrica
e cabe neste recorte.

## Receita de um primitivo novo

1. Escolha **forma**, não só cor — o trio orbe/estilhaço/jogador é o piso.
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
