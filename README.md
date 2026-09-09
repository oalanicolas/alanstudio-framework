# Alan Studios Framework · 0.9

Harness thin para criar, evoluir e produzir games com IA. Compartilha conceitos,
processo, seleção de contexto, marcos de produção e evidência. Cada jogo continua
usando sua engine, suas regras, seus assets e seus validadores.

Não é um motor. Não publica sozinho. Não mede diversão. Não promove marcos.

Executor para macOS/Linux, Python 3.10+; biblioteca padrão, sem instalação de
dependências. Testes do harness usam também Node/npm quando exercitam
`package.json`.

Playground: [games.alanicolas.com/framework](https://games.alanicolas.com/framework)

## Começar em três comandos

```sh
python3 scripts/game.py doctor --root /caminho/do/laboratorio
python3 scripts/game.py template game-design --project /caminho/do/laboratorio/meu-jogo --output /caminho/do/laboratorio/meu-jogo/docs/game-design.md
python3 scripts/game.py context /caminho/do/laboratorio/meu-jogo --focus create --stage game-design --root /caminho/do/laboratorio
```

`doctor` confere Python, integridade dos arquivos do framework, raiz, projetos
reconhecidos, estudos, acervo sonoro e git; itens `absent` são opcionais. O template
`game-design` é um documento único que, preenchido, cobre as nove áreas mínimas de um
jogo pequeno. `context` entrega o recorte de leitura e a checagem documental.
`--root` pode vir antes ou depois do subcomando.

No Codex ou no Claude, invoque **`$game-dev`** com o projeto e a mudança desejada:

```
$game-dev crie um conto jogável em Canvas a partir do acervo existente
$game-dev desenvolva o Game Brief e o GDD desta ideia, usando MDA
$game-dev monte o plano de produção e diga em que marco estamos
```

A fonte é [SKILL.md](SKILL.md). Copie-a para o atalho do host
(`.agents/skills/game-dev/SKILL.md` ou `.claude/skills/game-dev/SKILL.md`).

## Contexto por foco

```sh
python3 scripts/game.py discover --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus create --root /caminho/do/laboratorio
python3 scripts/game.py scan /caminho/do/jogo --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus architecture --stage tdd --root /caminho/do/laboratorio
```

Focos: `create`, `mechanics`, `lifecycle`, `content`, `visual`, `feel`, `network`,
`architecture`, `production`. O contexto entrega caminhos para leitura, registros já
existentes, catálogos de estudo (se um irmão `Games-Frameworks` existir, ou
`GAMES_FRAMEWORKS_ROOT`), menções locais de pause/reset/seed, `foundation` (nove
áreas documentais) e o acervo `shared/sfx` da raiz informada. Não executa o jogo.
`mentioned` não é `verified`. `candidate_found` não prova suficiência, atualidade
nem aprovação.

Descoberta percorre até três níveis, reconhece `package.json`, Unity, Godot, Unreal
(`.uproject`), Defold, GameMaker (`.yyp`), Cargo, Python (`pyproject.toml`), Love2D
(`main.lua`) e HTML, e para na raiz de cada projeto. `shared/` e pastas de build das
engines não entram como jogo.

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
Três complementos: `art-bible`, `devlog`, `audit`. Três de consolidação e produção:
`game-design` (documento único), `production-plan`, `milestone`.

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
[visual](recipes/visual.md), [feel](recipes/feel.md), [rede](recipes/network.md),
[arquitetura](recipes/architecture.md), [produção](recipes/production.md).
`--focus architecture` ou `--stage tdd` carrega a receita de arquitetura;
`--focus production`, `--stage production-plan` ou `--stage milestone` carregam a
de produção. A skill aplica quando a mudança pede; o CLI só seleciona referências.

## Produção e acabamento

[Produção](recipes/production.md) trata marcos como gates de evidência — first
playable → vertical slice → alpha → beta → gold → live — com lentes de disciplina
(design, arte, animação, áudio, feel, UX/acesso, técnica, conteúdo, localização, QA,
plataforma), orçamentos medidos na plataforma alvo, pipeline de conteúdo e
estabilidade. “AAA” aqui é padrão de acabamento observável, não orçamento.

```sh
python3 scripts/game.py context /caminho/do/jogo --focus production --stage production-plan --root /caminho/do/laboratorio
python3 scripts/game.py template milestone --project meu-jogo --output /tmp/meu-jogo-alpha.md
```

O plano de produção entra em `continuity.sources` quando existe. Nenhum comando mede
orçamento, executa soak, promove marco ou certifica requisito de plataforma; a
passagem é declarada por pessoa com a prova ligada.

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
- **Memória:** brief, decisões, plano de produção, estudos e evidência ficam nos
  locais canônicos de cada jogo.

## O que este repositório não é

Não há engine comum, API universal de ações, avaliação automática de diversão,
medição automática de performance ou publicação automática. Os jogos do
[playground](https://games.alanicolas.com/) continuam com a própria engine; este
harness não reivindica tê-los produzido.

Os oito frameworks externos foram estudados em recortes; seus testes não foram
executados. Os conceitos são adaptações desses estudos, não garantias universais.
Mapa: [sources.md](references/sources.md).

Recibos brutos de execução e o acervo sonoro ficam no laboratório.

## Testes

```sh
python3 -m unittest discover -s tests -v
```

Histórico 0.1–0.9: [adoção](adoption.md).
