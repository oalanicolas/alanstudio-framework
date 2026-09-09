# Alan Studios Framework · 0.9

Harness thin para criar e evoluir games com IA. Compartilha conceitos, processo,
seleção de contexto e evidência. Cada jogo continua usando sua engine, suas regras,
seus assets e seus validadores.

Não é um motor. Não publica sozinho. Não mede diversão.

Executor para macOS/Linux, Python 3.10+; biblioteca padrão, sem instalação de
dependências. Testes do harness usam também Node/npm quando exercitam
`package.json`.

Playground: [games.alanicolas.com/framework](https://games.alanicolas.com/framework)

## Começar em três comandos

```sh
python3 scripts/game.py doctor --root /caminho/do/laboratorio
python3 scripts/game.py init /caminho/do/laboratorio/meu-jogo --starter canvas-arcade
python3 scripts/game.py next /caminho/do/laboratorio/meu-jogo --focus feel
```

`doctor` observa Python, integridade do framework, raiz, starters disponíveis e os
atalhos de skill do host — vigente, desatualizado ou ausente. Não escreve nada;
sinaliza bloqueio pelo código de saída.

`init` copia um starter, troca pelo nome do projeto os valores que o
`starter.json` dele declara e cria em `docs/` os sete documentos que cobrem as
áreas mínimas — brief, gdd, mda, tdd, art-bible, devlog e qa — como **rascunho
declarado**. Os demais templates do ciclo entram depois, com `template`, quando a
etapa chegar. Não instala dependências, não toca no starter de origem e recusa
destino ocupado. `scan` reconhece o resultado no mesmo turno, e `verify` roda os
validadores do starter onde houver Node.

`next` deriva **uma** proposta do estado no disco e ordena por dependência: sem
destino → sem entrypoint → área não localizada → rascunho → documento sem versão
vigente → continuidade → validadores → dimensão mais baixa da barra. Devolve
também as alternativas descartadas. `executed` permanece `false`: o harness propõe,
quem decide é o agente ou você.

No Codex ou no Claude, invoque **`$game-dev`** com o projeto e a mudança desejada.

```
$game-dev crie um conto jogável em Canvas a partir do acervo existente
$game-dev desenvolva o Game Brief e o GDD desta ideia, usando MDA
```

A fonte é [SKILL.md](SKILL.md). Copie-a para o atalho do host
(`.agents/skills/game-dev/SKILL.md` ou `.claude/skills/game-dev/SKILL.md`);
`doctor` avisa quando a cópia ficou para trás.

## Contexto

```sh
python3 scripts/game.py discover --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus create --root /caminho/do/laboratorio
python3 scripts/game.py scan /caminho/do/jogo --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus architecture --stage tdd --root /caminho/do/laboratorio
```

`--root` é aceito antes ou depois do subcomando.

O contexto entrega caminhos para leitura, registros já existentes, catálogos de
estudo (se um irmão `Games-Frameworks` existir, ou `GAMES_FRAMEWORKS_ROOT`),
menções locais de pause/reset/seed, `foundation` (nove áreas documentais) e
`production_bar` (as dimensões de acabamento pertinentes ao foco).
Não executa o jogo. `mentioned` não é `verified`. `candidate_found` não prova
suficiência, atualidade nem aprovação.

Descoberta percorre até três níveis, reconhece `package.json`, HTML, Godot e
Unity e para na raiz de cada projeto. `shared/` não entra como jogo.

## Barra de acabamento

O que separa um protótipo de um jogo tratado como produto não é orçamento: é
acabamento por dimensão de ofício. [A escada](references/production-bar.md) tem
cinco degraus — protótipo, jogável, fatia, publicável, carro-chefe — em dez
dimensões: feel, legibilidade, direção de arte, mixagem, ritmo, confiança de
estado, performance, acessibilidade, escala de conteúdo e release.

**O degrau percebido é o mínimo entre as dimensões, não a média.** Esse é o modo
de falha típico de um estúdio assistido por IA: texto, quantidade de conteúdo e
variação visual sobem sozinhos, enquanto feel, mixagem, estabilidade de quadro e
confiança de estado ficam para trás e definem a leitura final.

`context` seleciona as dimensões pertinentes; **nenhum comando atribui um degrau**.
Cada critério é observável, mas a observação é trabalho humano ou do agente, com
condição e autor declarados.

O que o projeto **declara** é outra coisa, e essa o harness lê:

```sh
python3 scripts/game.py bar /caminho/do/laboratorio/meu-jogo
```

`bar` procura, nos documentos do projeto — README, qa, devlog, gdd, art-bible —
uma tabela com uma linha por dimensão: degrau atual, degrau seguinte e o critério
que falta. É o formato que o [README do
starter](assets/starters/canvas-arcade/README.md) já usa. O comando devolve o
piso, quais dimensões estão nele e o degrau percebido — este último **só** quando
as dez tiverem linha, porque dimensão não declarada não é dimensão alta.

Ele confere a forma da declaração, não o jogo: dimensão conhecida, degrau
existente, alvo no degrau imediatamente seguinte. **Uma tabela otimista sai daí
intacta.** O ganho não é aferição, é que a dimensão mais baixa passa a ter nome —
e `next` propõe subir exatamente ela, citando o critério escrito no documento e a
linha de onde veio, em vez de listar as dez.

## Starters

`assets/starters/` guarda projetos de referência completos para o passo REUSE.
Hoje há um:

**`canvas-arcade`** — jogo em Canvas 2D com loop de passo fixo, RNG semeado,
hash de estado, abstração de entrada (teclado, ponteiro, gamepad, remapeável),
mixer com barramentos/ducking/limite de vozes/legendas, save versionado com
migração e escrita atômica, e renderizador com alto contraste e redução de
movimento. Expõe `pause`, `reset`, `seed`, `observe`, `act`, `advance`, `capture`
e `dispose` — e **prova cada uma** em testes headless (`npm test`), além de
`npm run budget` para o orçamento de simulação. O README do starter declara em
que degrau cada dimensão está, incluindo as que ainda não subiram.

Um starter é referência **executável**: `cd assets/starters/canvas-arcade && npm
run serve` abre o jogo antes de qualquer `init`. É por isso que os arquivos
carregam valores reais em vez de `{{TOKEN}}` — um token no `<title>` apareceria na
aba do navegador — e por isso que cada starter tem um `starter.json` dizendo quais
valores `init` troca e em quais arquivos. O escopo por arquivo é o que impede uma
troca de nome de alcançar um import ou um caminho relativo que só se parece com o
nome. Manifesto fora de sincronia com os arquivos é bloqueio em `doctor` e recusa
em `init`, antes de qualquer cópia.

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
e playtest → PRD/TDD → vertical slice → produção/MVP → QA → release. Orientação de
dependências, não esteira rígida. Um jogo pequeno pode reunir essas decisões em
um documento.

Dez templates do ciclo: brief, mda, gdd, poc, prd, tdd, vertical-slice, mvp, qa,
release. Três complementos: `art-bible`, `devlog`, `audit`.

```sh
python3 scripts/game.py context /caminho/do/jogo --focus content --stage gdd --root /caminho/do/laboratorio
python3 scripts/game.py template brief --project meu-jogo
python3 scripts/game.py template art-bible --project meu-jogo --output /tmp/meu-jogo-art.md
```

Sem `--output`, `template` só imprime. Com ele, cria um rascunho novo e recusa
sobrescrita, inclusive de symlinks. Gerar `template audit` não executa auditoria.
Gerar `template release` não concede autorização de publicação.

**REUSE → ADAPT → CREATE.** CREATE só entra com lacuna explícita.
O [contrato JSON](assets/work.example.json) formaliza uma decisão nova;
`check-plan` valida a forma, não o mérito.

```sh
python3 scripts/game.py check-plan caminho/do/trabalho.json --root /caminho/do/laboratorio
```

Treze receitas: [criar](recipes/create.md), [mecânicas](recipes/mechanics.md),
[ciclo de vida](recipes/lifecycle.md), [conteúdo](recipes/content.md),
[visual](recipes/visual.md), [rede](recipes/network.md),
[arquitetura](recipes/architecture.md), [feel](recipes/feel.md),
[performance](recipes/performance.md), [acessibilidade](recipes/accessibility.md),
[áudio](recipes/audio.md), [persistência](recipes/persistence.md) e
[release](recipes/release.md). `--focus architecture` ou `--stage tdd` carrega a
receita de arquitetura. A skill aplica quando a mudança afeta contratos ou
responsabilidades; o CLI só seleciona referências.

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

`context` só sabe dizer `mentioned` sobre as oito capacidades conhecidas — pause,
reset, seed, observe, act, advance, capture, dispose — porque lê arquivos sem
executá-los. `--proves` **não** promove nenhuma delas a verificada; o harness não
tem como saber se um comando exercita pause.

```sh
python3 scripts/game.py verify /caminho/do/jogo --script test --output /tmp/jogo-qa-02 --proves pause --proves reset --proves seed
```

O que ele acrescenta é uma alegação com autor, data, argv e log: `claimed` quando
os comandos passaram, `unsupported` quando falharam. Em vez de sumir na prosa, a
afirmação fica anexada a um recibo e pode ser contestada por quem ler. A declaração
é de **quem executa**, nunca do repositório: nenhum arquivo do projeto seleciona
capacidade, e `claimed` continua não sendo `verified`.

## Três camadas

- **IA:** interpreta a intenção, consulta fontes e propõe a mudança. Não depende
  de um fornecedor.
- **Harness:** recorta o contexto, varre a base, valida a forma do contrato,
  monta projetos a partir de starters e corre os comandos escolhidos com recibo.
- **Memória:** brief, decisões, estudos e evidência ficam nos locais canônicos
  de cada jogo.

## O que este repositório não é

Não há engine comum, API universal de ações, avaliação automática de diversão
ou publicação automática. Os jogos do [playground](https://games.alanicolas.com/)
continuam com a própria engine; este harness não reivindica tê-los produzido.

A barra de acabamento descreve o que observar; ela não observa. Nenhum comando
promove um jogo a um degrau, e cumprir todos os critérios não garante que o jogo
interesse a alguém — acabamento é condição necessária, não suficiente.

Os oito frameworks externos foram estudados em recortes; seus testes não foram
executados. Os conceitos são adaptações desses estudos, não garantias universais.
Mapa: [sources.md](references/sources.md).

Recibos brutos de execução e o acervo sonoro ficam no laboratório.

## Testes

```sh
python3 -m unittest discover -s tests -v
cd assets/starters/canvas-arcade && npm test && npm run budget
```

Histórico 0.1–0.9: [adoção](adoption.md).
