# Init

Começar um jogo novo a partir de um starter do acervo, como REUSE de
infraestrutura já testada: loop de passo fixo, RNG semeado, hash de estado,
entrada abstraída e remapeável, mixer com barramentos, save versionado com
migração, renderizador com alto contraste e redução de movimento. Cria rascunhos
declarados em `docs/` e `AGENTS.md`. Não instala dependências, não toca no starter
de origem e recusa destino ocupado.

## Escala

Igual em todas: o starter é o candidato de reuso quando o destino não existe e a
engine é web. `jam` pode trocar os sete rascunhos por um `game-design.md` único
(`--no-docs` e depois `template game-design`). `product`/`aa` mantêm os rascunhos e
os substituem por decisão, não os entregam como se fossem uma.

## Avaliar

1. `doctor --root <lab>`: lista os starters, confere os manifestos e o ambiente
   (Node 20+ para o `canvas-arcade`). Manifesto fora de sincronia bloqueia antes de
   copiar.
2. Escolha por adequação ao verbo: leia o [README do starter](../assets/starters/canvas-arcade/README.md),
   o que ele já exercita em testes headless (`npm test`) e em que degrau declara cada
   dimensão. Um starter que não serve ao verbo é ADAPT caro, não REUSE.
3. Sem starter adequado, em qualquer engine: `template game-design` e siga
   [`craft`](craft.md); escrever laço e save do zero é CREATE e pede a lacuna escrita.
4. Confirme com o usuário o destino, o título e a engine; destino ocupado é recusa,
   não pergunta.

## Executar

```sh
python3 scripts/game.py init <lab>/<jogo> --starter canvas-arcade [--title "Nome"] [--no-docs]
```

Em seguida `context <jogo> --focus create`: o `scan` reconhece os rascunhos no
mesmo turno; `verify --script test` roda os validadores herdados. O que o starter
declara sobre si (README, `starter.json`) vale para o starter; o jogo derivado
começa em `prototype` até demonstrar o contrário ([criar](../recipes/create.md)).

## Verificar

`init` devolve o que copiou e substituiu; `verify` verde prova o starter, não o
jogo. A prova do comando é o projeto abrir e servir (`npm run serve`) na máquina de
quem criou, com os rascunhos e o `AGENTS.md` no lugar.

## Nunca

- Inventar starter inexistente ou copiar um projeto do acervo à mão.
- Sobrescrever destino ocupado ou "limpar" a pasta para caber.
- Chamar os rascunhos de decisão documentada.
- Instalar dependências ou publicar por conta do `init`.

## Entregar

Caminho do projeto, o que foi herdado, o comando de rodar e o próximo passo: o
brief da rodada em [`shape`](shape.md) ou direto [`craft`](craft.md) se o pedido já
o trouxe. `next <jogo> --focus create` propõe a primeira ação a partir do disco.
