# Mesas de conteúdo

Uma mesa nova entra pelo mesmo carregador. O custo conhecido do próximo
item de chuva é **o comando** — o jogo já consome qualquer mesa com a
forma de `spawn`. `copy.fantasy` alimenta o aviso do primeiro ciclo.
Mesas genéricas ainda pedem consumidor.

```sh
npm run table -- <nome> --from spawn
```

Isso copia `data/spawn.json` e registra o nome. A partida lê
`?spawn=<nome>` ou `settings.spawnProfile`. Sem `--from`, o comando
escreve `{ "schema": 1 }` e `loadTable("<nome>")` resolve; o jogo não
muda até alguém ligar a regra ou a apresentação.

`dusk` já é o segundo perfil: prática mais curta, chuva mais densa.
Campo obrigatório se declara com `requireFields("spawn", [...])`. Mesa
desconhecida ou campo ausente falha com o nome do que faltou, não com
`undefined` no meio do tick. Nome que não é chuva cai no padrão na hora
de jogar; `loadSpawn` recusa.

Duas chuvas mais o texto do HUD não são volume. `enough` no harness
continua falso. Alguém de fora ainda não produziu no piso.
