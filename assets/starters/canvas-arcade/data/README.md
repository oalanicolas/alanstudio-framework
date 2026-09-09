# Mesas de conteúdo

Uma mesa nova entra pelo mesmo carregador. O custo conhecido do próximo
item é **o comando mais o consumidor** — não republicar o verbo.

```sh
npm run table -- <nome>
```

O comando cria `data/<nome>.json` e registra o nome em
`src/game/tables.js`. `loadTable("<nome>")` passa a resolver. Sem
consumidor a mesa existe e o jogo não muda: isso é o custo fixo
(segundos). Ligar a regra ou a apresentação é o custo variável — minutos
se o campo já existe, uma sessão se for verbo novo.

Campo obrigatório se declara com `requireFields("spawn", [...])`. Mesa
desconhecida ou campo ausente falha com o nome do que faltou, não com
`undefined` no meio do tick.

Duas mesas (chuva e texto) mais a receita não são volume. `enough` no
harness continua falso. Não há migração de formato: mudar a forma de
`spawn.json` é decisão, não versão.
