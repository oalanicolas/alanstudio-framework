# Init

Começar um jogo novo a partir de um starter do acervo, como REUSE de
infraestrutura já testada: loop de passo fixo, RNG semeado, hash de estado,
entrada abstraída e remapeável, mixer com barramentos, save versionado com
migração, renderizador com alto contraste e redução de movimento. Cria rascunhos
declarados em `docs/` e `AGENTS.md`. Não instala dependências, não toca no starter
de origem e recusa destino ocupado.

## Escala

Igual em todas: avalie o starter quando o destino não existe e a plataforma é
compatível. `init` conserva a opção de gerar rascunhos; `--no-docs` a dispensa.
No fluxo de criação, prefira o `start` existente quando não houver necessidade
dos rascunhos. O agente mantém `game-design.md` ou os canônicos pertinentes à
escala com decisões reais; o criador não preenche templates para começar.

## Avaliar

1. `doctor --root <lab>`: lista os starters, confere os manifestos e o ambiente
   (Node 20+ para o `canvas-arcade`). Manifesto fora de sincronia bloqueia antes de
   copiar.
2. Escolha por adequação ao verbo: leia o [README do starter](../assets/starters/canvas-arcade/README.md),
   o que ele já exercita em testes headless (`npm test`) e em que degrau declara cada
   dimensão. Um starter que não serve ao verbo é ADAPT caro, não REUSE.
3. Sem starter adequado, em qualquer engine: `template game-design` e siga
   [`craft`](craft.md); escrever laço e save do zero é CREATE e pede a lacuna escrita.
4. Reuse destino, título e plataforma já definidos. Resolva caminhos pela convenção
   do workspace e peça só a escolha material que faltar. Destino ocupado é recusa,
   não autorização para apagar ou sobrescrever.

## Executar

```sh
python3 scripts/game.py init <lab>/<jogo> --starter canvas-arcade [--title "Nome"] [--no-docs]
```

Para começar uma criação sem rascunhos, `start` reutiliza a mesma infraestrutura:

```sh
python3 scripts/game.py start <lab>/<jogo> --starter canvas-arcade --idea "Ideia do jogo"
```

`--idea` altera a abertura, não as regras. A adaptação à ideia pertence a
[`craft`](craft.md); copiar o starter não entrega o jogo descrito.

Em seguida `context <jogo> --focus create`: o `scan` localiza o conteúdo criado,
incluindo rascunhos quando solicitados; `verify --script test` roda os validadores herdados. O que o starter
declara sobre si (README, `starter.json`) vale para o starter; o jogo derivado
começa em `prototype` até demonstrar o contrário ([criar](../recipes/create.md)).

## Verificar

`init` devolve o que copiou e substituiu; `verify` verde prova o starter, não o
jogo. A prova do comando é o projeto abrir e servir (`npm run serve`) na máquina de
quem criou, com o `AGENTS.md` e os rascunhos solicitados no lugar.

## Nunca

- Inventar starter inexistente ou copiar um projeto do acervo à mão.
- Sobrescrever destino ocupado ou "limpar" a pasta para caber.
- Chamar os rascunhos de decisão documentada.
- Instalar dependências ou publicar por conta do `init`.

## Entregar

Caminho do projeto e o que foi herdado. Se o pedido era apenas copiar a base,
declare esse resultado e o trabalho que ainda falta. Se incluía criar o jogo,
continue em [`craft`](craft.md) com o brief vigente, adapte a ação à ideia e
verifique o acesso. `next <jogo> --focus create` é insumo para a próxima ação.
