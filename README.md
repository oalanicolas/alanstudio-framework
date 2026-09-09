# Alan Studios Framework · 0.8

Harness thin para criar e evoluir games com IA. Compartilha conceitos, processo,
seleção de contexto e evidência. Cada jogo continua usando sua engine, suas regras,
seus assets e seus validadores.

Não é um motor. Não publica sozinho. Não mede diversão.

Executor para macOS/Linux, Python 3.10+; biblioteca padrão, sem instalação de
dependências. Testes do harness usam também Node/npm quando exercitam
`package.json`.

Playground: [games.alanicolas.com/framework](https://games.alanicolas.com/framework)

## Começar

No Codex ou no Claude, invoque **`$game-dev`** com o projeto e a mudança desejada.

```
$game-dev crie um conto jogável em Canvas a partir do acervo existente
$game-dev desenvolva o Game Brief e o GDD desta ideia, usando MDA
```

A fonte é [SKILL.md](SKILL.md). Copie-a para o atalho do host
(`.agents/skills/game-dev/SKILL.md` ou `.claude/skills/game-dev/SKILL.md`).

Na raiz deste repositório:

```sh
python3 scripts/game.py discover --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus create --root /caminho/do/laboratorio
python3 scripts/game.py scan /caminho/do/jogo --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus architecture --stage tdd --root /caminho/do/laboratorio
```

O contexto entrega caminhos para leitura, registros já existentes, catálogos de
estudo (se um irmão `Games-Frameworks` existir, ou `GAMES_FRAMEWORKS_ROOT`),
menções locais de pause/reset/seed e `foundation` (nove áreas documentais).
Não executa o jogo. `mentioned` não é `verified`. `candidate_found` não prova
suficiência, atualidade nem aprovação.

Descoberta percorre até três níveis, reconhece `package.json`, HTML, Godot e
Unity e para na raiz de cada projeto. `shared/` não entra como jogo.

## Checagem e continuidade

Todo `context` já corre `scan`. Também existe sozinho:

```sh
python3 scripts/game.py scan /caminho/do/jogo --root /caminho/do/laboratorio
```

Nove áreas: Brief/PRD; GDD; MDA; arquitetura/TDD; design system / Art Bible;
Devlog; QA/playtest; como executar; origem de código e assets. Um documento
pode cobrir várias. O scanner só lê nomes, títulos e campos; não segue symlink
nem escreve arquivo.

Se faltar base, `foundation.audit.required` pede ao agente **avisar e documentar
sem esperar um segundo pedido**. Restrição explícita na conversa continua valendo.
O scanner não executa a auditoria (`audit.executed: false`).

Eventos de conversa, interpretados pelo agente — o comando não concede aprovação:

```sh
python3 scripts/game.py context /caminho/do/jogo --focus visual --event direction-approved --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus mechanics --event resume --root /caminho/do/laboratorio
```

`direction-approved` sincroniza a base mínima no mesmo turno. `resume` localiza
fontes de continuidade; o agente resolve o próximo passo. O harness deixa
`next_step: null` e `executed: false`.

## Processo

[Pré-produção](references/preproduction.md): Game Brief → GDD/MDA ↔ protótipo/PoC
e playtest → PRD/TDD → vertical slice → produção/MVP → QA. Orientação de
dependências, não esteira rígida. Um jogo pequeno pode reunir essas decisões em
um documento.

Nove templates do ciclo: brief, mda, gdd, poc, prd, tdd, vertical-slice, mvp, qa.
Três complementos: `art-bible`, `devlog`, `audit`.

```sh
python3 scripts/game.py context /caminho/do/jogo --focus content --stage gdd --root /caminho/do/laboratorio
python3 scripts/game.py template brief --project meu-jogo
python3 scripts/game.py template art-bible --project meu-jogo --output /tmp/meu-jogo-art.md
```

Sem `--output`, `template` só imprime. Com ele, cria um rascunho novo e recusa
sobrescrita, inclusive de symlinks. Gerar `template audit` não executa auditoria.

**REUSE → ADAPT → CREATE.** CREATE só entra com lacuna explícita.
O [contrato JSON](assets/work.example.json) formaliza uma decisão nova;
`check-plan` valida a forma, não o mérito.

```sh
python3 scripts/game.py check-plan caminho/do/trabalho.json --root /caminho/do/laboratorio
```

Receitas: [criar](recipes/create.md), [mecânicas](recipes/mechanics.md),
[ciclo de vida](recipes/lifecycle.md), [conteúdo](recipes/content.md),
[visual](recipes/visual.md), [rede](recipes/network.md),
[arquitetura](recipes/architecture.md). `--focus architecture` ou `--stage tdd`
carrega a receita de arquitetura. A skill aplica quando a mudança afeta
contratos ou responsabilidades; o CLI só seleciona referências.

## Áudio (opcional)

Se o laboratório tiver `shared/sfx` na raiz passada em `--root`:

```sh
python3 scripts/game.py sfx search passos --root /caminho/do/laboratorio
python3 scripts/game.py sfx copy ID --to /caminho/do/jogo/public/sfx --root /caminho/do/laboratorio
```

Sem esse acervo, o catálogo vem vazio. Piso: gravação licenciada ou design
contemporâneo. 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão.
Este repositório **não inclui** os arquivos de som.

## Verificar

Inspecione os scripts retornados por `context`. Escolha os validadores e a ordem
do próprio jogo.

```sh
python3 scripts/game.py verify /caminho/do/jogo --script test --output /tmp/jogo-qa-01 --root /caminho/do/laboratorio
python3 scripts/game.py verify /caminho/do/jogo --output /tmp/jogo-qa-01 --root /caminho/do/laboratorio --command python3 tools/verify.py
```

`--command` vai por último. Não há shell implícito. Cada execução cria uma pasta
inédita. Destino existente é recusado. Build verde não prova arte, reinício, rede
nem que o jogo é divertido. `experience_status` continua `not_assessed`.

## Três camadas

- **IA:** interpreta a intenção, consulta fontes e propõe a mudança. Não depende
  de um fornecedor.
- **Harness:** recorta o contexto, varre a base, valida a forma do contrato e
  corre os comandos escolhidos com recibo.
- **Memória:** brief, decisões, estudos e evidência ficam nos locais canônicos
  de cada jogo.

## O que este repositório não é

Não há engine comum, API universal de ações, avaliação automática de diversão
ou publicação automática. Os jogos do [playground](https://games.alanicolas.com/)
continuam com a própria engine; este harness não reivindica tê-los produzido.

Os oito frameworks externos foram estudados em recortes; seus testes não foram
executados. Os conceitos são adaptações desses estudos, não garantias universais.
Mapa: [sources.md](references/sources.md).

Recibos brutos de execução e o acervo sonoro ficam no laboratório.

## Testes

```sh
python3 -m unittest discover -s tests -v
```

Histórico 0.1–0.8: [adoção](adoption.md).
