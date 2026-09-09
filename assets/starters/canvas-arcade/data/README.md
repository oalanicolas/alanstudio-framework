# Mesas de conteúdo

Uma mesa nova entra pelo mesmo carregador. O custo conhecido do próximo
item de chuva é **o comando** — o jogo já consome qualquer mesa com a
forma de `spawn`. `copy.fantasy` alimenta o aviso do primeiro ciclo.
`palettes` alimenta o desenho: trocar um token não exige abrir
`render.js`. O look `dusk` mora nessa mesa; `?look=` / `settings.look`
o consomem. `dusk` na chuva é outra mesa (`dusk.json`) e outro
consumidor (`?spawn=`). Nasça o próximo look com o comando; mesas
genéricas ainda pedem consumidor.

```sh
npm run table -- <nome> --from spawn
npm run table -- <nome> --from dusk --as denser
npm run session -- --spawn <nome>
npm run look -- <nome> --from dusk --as warmer
npm run sfx -- --from dash --as brighter
```

`--from` copia um perfil de chuva que já existe (`spawn` ou `dusk`).
`--as denser|calmer|brief` desloca os knobs sem pedir o schema de
cabeça: a chuva nova não é um clone. Sem `--from`, o comando escreve
`{ "schema": 1 }` e `loadTable("<nome>")` resolve; o jogo não muda até
alguém ligar a regra ou a apresentação.

`npm run look -- <nome> --from dusk --as warmer` copia um look que o
jogo já pinta. `--from` é obrigatório; `contrast` não é look.
`--as warmer|cooler|night` desloca os tokens. Sem `--as` a cópia é
idêntica até alguém editar. Intenção não é look aprovado.

A partida lê `?spawn=<nome>` ou `settings.spawnProfile`. `dusk` já é o
segundo perfil: prática mais curta, chuva mais densa. Intenção nomeada
não é chuva melhor nem alguém de fora no piso.

`npm run sfx -- --from dash --as brighter|darker|tighter` reescreve
um papel que o mixer já toca. `--as` precisa de `--from`. Sem `--from`
o banco inteiro nasce de novo. Intenção não é mix ouvido.

Campo obrigatório se declara com `requireFields("spawn", [...])`. Mesa
desconhecida ou campo ausente falha com o nome do que faltou, não com
`undefined` no meio do tick. Nome que não é chuva cai no padrão na hora
de jogar; `loadSpawn` recusa.

## Knobs da chuva

| Campo | O que decide |
| --- | --- |
| `intervalTicks` / `minIntervalTicks` | Folga entre quedas, do começo ao teto |
| `rampTicks` | Em quantos ticks a chuva chega no teto |
| `hazardChanceStart` / `hazardChanceEnd` | Quanto da chuva é estilhaço |
| `fallSpeedMin` / `fallSpeedMax` | Quão rápido o item atravessa o campo |
| `practiceTicks` | Primeiros ticks só com orbe |
| `recoveryTicks` / `recoveryIntervalScale` | Folga depois de guardar |

Duas chuvas mais o texto do HUD não são volume. `enough` no harness
continua falso. Alguém de fora ainda não produziu no piso.
