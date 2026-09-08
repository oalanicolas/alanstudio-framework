# Alan Studios Framework · 0.3

Harness thin para criar e evoluir games com IA. Compartilha conceitos, processo,
seleção de contexto e evidência. Cada jogo continua usando sua engine, suas regras,
seus assets e seus validadores.

Não é um motor. Não publica sozinho. Não mede diversão.

Executor para macOS/Linux, Python 3.10+; biblioteca padrão, sem instalação de
dependências. Testes do harness usam também Node/npm quando exercitam
`package.json`.

Playground: [games.alanicolas.com](https://games.alanicolas.com/framework)

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
python3 scripts/game.py context /caminho/do/jogo --focus lifecycle --root /caminho/do/laboratorio
```

O contexto entrega caminhos para leitura, registros já existentes, catálogos de
estudo (se um diretório irmão `Games-Frameworks` existir, ou
`GAMES_FRAMEWORKS_ROOT`) e menções locais de pause/reset/seed em arquivos de
inspeção. Não executa nada, não lê o acervo inteiro para dentro do prompt e não
declara capacidade comprovada a partir de um token ou do nome da engine.
`mentioned` não é `verified`.

Descoberta percorre até três níveis, reconhece `package.json`, HTML, Godot e
Unity e para na raiz de cada projeto.

## Processo

[Pré-produção](references/preproduction.md): Game Brief → GDD/MDA ↔ protótipo/PoC
e playtest → PRD/TDD → vertical slice → produção/MVP → QA. Orientação de
dependências, não esteira rígida. Um jogo pequeno pode reunir essas decisões em
um documento. Os nove templates existem; o harness carrega só a etapa pedida.

```sh
python3 scripts/game.py context /caminho/do/jogo --focus content --stage gdd
python3 scripts/game.py template brief --project meu-jogo
python3 scripts/game.py template prd --project meu-jogo --output /tmp/meu-jogo-prd.md
```

Etapas: `brief`, `mda`, `gdd`, `poc`, `prd`, `tdd`, `vertical-slice`, `mvp`, `qa`.
Sem `--output`, `template` só imprime. Com ele, cria um rascunho novo e recusa
sobrescrita, inclusive de symlinks.

**REUSE → ADAPT → CREATE.** CREATE só entra com lacuna explícita.
O [contrato JSON](assets/work.example.json) formaliza uma decisão nova;
`check-plan` valida a forma, não o mérito.

```sh
python3 scripts/game.py check-plan caminho/do/trabalho.json --root /caminho/do/laboratorio
```

Receitas por foco: [criar](recipes/create.md), [mecânicas](recipes/mechanics.md),
[ciclo de vida](recipes/lifecycle.md), [conteúdo](recipes/content.md),
[visual](recipes/visual.md), [rede](recipes/network.md).

## Verificar

Inspecione os scripts retornados por `context`. Escolha os validadores e a ordem
do próprio jogo.

```sh
python3 scripts/game.py verify /caminho/do/jogo --script test --output /tmp/jogo-qa-01
python3 scripts/game.py verify /caminho/do/jogo --output /tmp/jogo-qa-01 --command python3 tools/verify.py
```

`--command` vai por último, com o executável e os argumentos. Não há shell
implícito. Cada execução cria uma pasta inédita com logs, hashes, código de
saída e HEAD/status Git. Destino existente é recusado. Build verde não prova
arte, reinício, rede nem que o jogo é divertido. `experience_status` continua
`not_assessed` mesmo com testes verdes.

## Três camadas

- **IA:** interpreta a intenção, consulta fontes e propõe a mudança. Não depende
  de um fornecedor.
- **Harness:** recorta o contexto, valida a forma do contrato e corre os
  comandos escolhidos com recibo.
- **Memória:** brief, decisões, estudos e evidência ficam nos locais canônicos
  de cada jogo.

## O que este repositório não é

Não há engine comum, API universal de ações, avaliação automática de diversão
ou publicação automática. Os jogos do [playground](https://games.alanicolas.com/)
continuam com a própria engine; este harness não reivindica tê-los produzido.

Os oito frameworks externos foram estudados em recortes; seus testes não foram
executados. Os conceitos são adaptações desses estudos, não garantias universais.
Mapa: [sources.md](references/sources.md).

## Testes

```sh
python3 -m unittest discover -s tests -v
```

Histórico das versões 0.1–0.3: [adoção](adoption.md).
