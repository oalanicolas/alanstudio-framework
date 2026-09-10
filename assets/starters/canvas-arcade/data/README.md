# Mesas de conteúdo

Uma mesa nova entra pelo mesmo carregador. O custo conhecido do próximo
item de chuva é **o comando** — o jogo já consome qualquer mesa com a
forma de `spawn`. `copy.fantasy` alimenta a abertura e o aviso do
primeiro ciclo quando a porta ainda não deu a frase. `title_play`, `title_again` e `title_new` nomeiam a
porta. `title_volatile` e `title_unsaved` nomeiam sessão
que não grava e gravação que não ficou. `settings_recovered`
nomeia preferências ilegíveis no painel, no live e no canvas da
porta e do fim. Nomear não é save confiável. Repetir a última seed não é o tick interrompido.
`palettes` alimenta o desenho: trocar um token não exige abrir
`render.js`. Os looks `dusk` e `calm` moram nessa mesa; `?look=` /
`settings.look` os consomem. O look `dusk` pinta orbe âmbar e
estilhaço índigo; o campo continua quente. Hex no disco não é
comparação em movimento. `dusk` e `calm` na chuva são outras
mesas e outro consumidor (`?spawn=`). `?mood=` aplica o par quando o
nome é look e chuva; look ou chuva explícitos vencem no próprio
eixo. A página nomeia o mesmo par no select. A chuva `calm` é prática mais longa, menos risco, queda mais
lenta; não é o `calmer` aplicado em `spawn`. O look `calm` é sálvia
quieta; não é o `cooler` aplicado em `normal`. Nasça o próximo look
com o comando; mesas genéricas ainda pedem consumidor.

```sh
npm run pair -- <nome> --from dusk --look warmer --spawn denser
npm run table -- <nome> --from spawn
npm run table -- <nome> --from dusk --as denser
npm run table -- <nome> --from calm --as brief
npm run session -- --spawn <nome>
npm run look -- <nome> --from dusk --as warmer
npm run look -- <nome> --from calm --as cooler
npm run sfx -- --from dash --as brighter
```

`--from` copia um perfil de chuva que já existe (`spawn`, `dusk` ou `calm`).
`--as denser|calmer|brief` desloca os knobs sem pedir o schema de
cabeça: a chuva nova não é um clone. `brief` encurta prática e rampa;
a folga da guarda permanece. Sem `--from`, o comando escreve
`{ "schema": 1 }` e `loadTable("<nome>")` resolve; o jogo não muda até
alguém ligar a regra ou a apresentação.

`npm run look -- <nome> --from dusk|calm --as warmer` copia um look que o
jogo já pinta. `--from` é obrigatório; `contrast` não é look.
`--as warmer|cooler|night` desloca campo e orbe; o estilhaço
e o perigo permanecem. Sem `--as` a cópia é idêntica até alguém editar.
Intenção não é look aprovado.

A partida lê `?spawn=<nome>` ou `settings.spawnProfile`. `dusk` é o
perfil denso; `calm` é o inverso autoral. `?mood=<nome>` aplica look
e chuva do mesmo nome quando os dois existem. `npm run pair` nasce
os dois no mesmo nome. Intenção nomeada
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
| `hazardChanceStart` / `hazardChanceEnd` | Quanto da chuva é estilhaço; a porta lê o teto, sem RNG |
| `fallSpeedMin` / `fallSpeedMax` | Quão rápido o item atravessa o campo |
| `practiceTicks` | Primeiros ticks só com orbe; o campo marca a janela |
| `recoveryTicks` / `recoveryIntervalScale` | Folga depois de guardar; o campo marca a janela e o mixer fala na volta |
| `closeIntervalScale` | Aperto do intervalo nos últimos 10 s. `1` = o fecho não muda a chuva. Ausente vira `1`. |
| `closeHazardScale` | Aperto do risco nos últimos 10 s. `1` = o fecho não muda a mistura. Ausente vira `1`. |

Três chuvas mais o texto do HUD não são volume. `enough` no harness
continua falso. Alguém de fora ainda não produziu no piso.
