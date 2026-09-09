# Alan Studios Framework · 0.9

Harness thin para criar, evoluir e produzir games com IA. Compartilha conceitos,
processo, seleção de contexto, marcos de produção e evidência. Cada jogo continua
usando sua engine, suas regras, seus assets e seus validadores.

Fácil de começar: um pedido vira um ciclo jogável, sem nove templates vazios.
Difícil de rebaixar: feel, áudio, pacing e receita de conteúdo fazem parte do
recorte, não de um “polimento depois”. “AAA” aqui é só o piso de acabamento da
slice — não tier de publisher, orçamento nem adjetivo de trailer. O alvo
honesto com IA é AA / Triple-I nesse piso.

Não é um motor. Não publica sozinho. Não mede diversão. Não promove marcos.

Executor para macOS/Linux, Python 3.10+; biblioteca padrão, sem instalação de
dependências. Testes do harness usam também Node/npm quando exercitam
`package.json`.

Playground: [games.alanicolas.com/framework](https://games.alanicolas.com/framework)

## Chegar num laboratório que já tem jogos

Este é o caso normal: a raiz de trabalho não está vazia. O primeiro movimento é
revisar o que existe, não criar mais um.

```sh
python3 scripts/game.py doctor --root /caminho/do/laboratorio
python3 scripts/game.py discover --root /caminho/do/laboratorio
python3 scripts/game.py next /caminho/do/laboratorio/um-dos-jogos --focus feel
```

`discover` lê cada jogo da raiz e devolve o que os distingue: quantas das nove
áreas mínimas têm candidato, quantas estão em rascunho, se há um passo registrado
para retomar e onde, o piso de acabamento que o projeto declara e quantas
dimensões ainda não têm linha, e quais validadores existem. É essa diferença que
uma listagem de caminho e tipo apagava — três jogos em estados incomparáveis saíam
iguais. `--plain` volta ao caminho e tipo, sem ler documento nenhum.

A ordem é a do disco e não muda: **o harness não classifica os jogos por
urgência**, porque nada aqui observa qual importa mais. Ele conta e lê; escolher
continua sendo trabalho de quem olha. Um projeto ilegível aparece com o motivo, em
vez de derrubar a revisão ou desaparecer da lista.

## Começar um jogo novo

Com starter (REUSE de infraestrutura já testada):

```sh
python3 scripts/game.py doctor --root /caminho/do/laboratorio
python3 scripts/game.py init /caminho/do/laboratorio/meu-jogo --starter canvas-arcade
python3 scripts/game.py next /caminho/do/laboratorio/meu-jogo --focus feel
```

`doctor` observa Python, Node, git, ffmpeg, presença dos arquivos do framework (receitas,
templates, referências e pacotes), raiz, projetos reconhecidos, estudos, acervo
sonoro, starters disponíveis e os atalhos de skill do host — vigente, desatualizado
ou ausente, comparando conteúdo.
Symlink apontando para o `SKILL.md` deste repositório conta como vigente: é o
atalho que não tem como ficar para trás. Não escreve nada; sinaliza bloqueio pelo
código de saída, e a correção que ele sugere roda como está — inclusive criando a
pasta do atalho.

`init` copia um starter, troca pelo nome do projeto os valores que o
`starter.json` dele declara e cria em `docs/` sete documentos — brief, gdd, mda,
tdd, art-bible, devlog e qa — como **rascunho declarado**. Eles cobrem sete das
nove áreas mínimas que `scan` cobra; as outras duas, origem e execução, ficam com o
README e o CREDITS do starter, então depois do `init` as nove têm candidato. Com
`--no-docs`, sobram três. Os demais templates do ciclo entram depois, com `template`, quando a
etapa chegar. Não instala dependências, não toca no starter de origem e recusa
destino ocupado. `scan` reconhece o resultado no mesmo turno, e `verify` roda os
validadores do starter onde houver Node.

`next` deriva **uma** proposta do estado no disco e ordena por dependência: sem
destino → sem entrypoint → área não localizada → rascunho → documento sem versão
vigente → continuidade → sem instruções para o agente → validadores → gate → barra. O gate tem dois ramos: linha
de gate malformada e critério pendente. A barra tem quatro, na ordem: linha de
degrau malformada, dimensão sem linha, duas linhas em conflito e — só então —
subir a dimensão mais baixa. Num projeto sem tabela, portanto, a última proposta
é declarar os degraus, não subir um deles. Devolve
também as alternativas descartadas. `executed` permanece `false`: o harness propõe,
quem decide é o agente ou você.

Sem starter, em qualquer engine, um documento único de design cobre as nove áreas de
um jogo pequeno:

```sh
python3 scripts/game.py template game-design --project /caminho/do/laboratorio/meu-jogo --output /caminho/do/laboratorio/meu-jogo/docs/game-design.md
python3 scripts/game.py context /caminho/do/laboratorio/meu-jogo --focus create --stage game-design --root /caminho/do/laboratorio
```

O template `game-design`, preenchido, é reconhecido pelo `scan` como cobertura das
nove áreas. `context` entrega o recorte de leitura e a checagem documental. Itens
`optional` do `doctor` não bloqueiam. `--root` pode vir antes ou depois do subcomando.

No Codex ou no Claude, invoque **`$game-dev`** com o projeto e a mudança desejada:

```
$game-dev crie um conto jogável em Canvas a partir do acervo existente
$game-dev desenvolva o Game Brief e o GDD desta ideia, usando MDA
$game-dev monte o plano de produção e diga em que marco estamos
$game-dev o pulo ainda não tem peso; ajuste o feel e o áudio dessa ação
```

A fonte é [SKILL.md](SKILL.md). Copie-a para o atalho do host
(`.agents/skills/game-dev/SKILL.md` ou `.claude/skills/game-dev/SKILL.md`), ou
aponte um symlink para ela e nunca mais pense nisso; `doctor` avisa quando a cópia
ficou para trás.

## Contexto por foco

```sh
python3 scripts/game.py discover --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus create --root /caminho/do/laboratorio
python3 scripts/game.py scan /caminho/do/jogo --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus architecture --stage tdd --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus feel --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus audio --root /caminho/do/laboratorio
```

Focos: `create`, `mechanics`, `lifecycle`, `content`, `visual`, `audio`, `feel`,
`network`, `architecture`, `performance`, `accessibility`, `persistence`, `release`,
`production`. Jogo novo começa em `create`. Acabamento do verbo usa `feel` e `audio`;
contrato: [ambição](references/ambition.md). `--root` é aceito antes ou depois do
subcomando.

O contexto entrega caminhos para leitura, registros já existentes, catálogos de
estudo (se um irmão `Games-Frameworks` existir, ou `GAMES_FRAMEWORKS_ROOT`),
menções locais de pause/reset/seed, `foundation` (nove áreas documentais),
`production_bar` (as dimensões de acabamento pertinentes ao foco), `finish` (perfil
do checklist de piso) e o acervo `shared/sfx` da raiz informada. Não executa o jogo.
`mentioned` não é `verified`. `candidate_found` não prova suficiência, atualidade
nem aprovação.

Descoberta percorre até três níveis, reconhece Unity, Godot, Unreal (`.uproject`),
Defold, GameMaker (`.yyp`), Construct (`.c3proj`), RPG Maker (`.rmmzproject`/`.rpgproject`),
Ren'Py, Roblox/Rojo, PICO-8 (`.p8`), Haxe, Flutter (`pubspec.yaml`), .NET (`.sln`/`.csproj`),
`package.json`, Cargo, CMake, Python (`pyproject.toml`), Love2D (`main.lua`) e HTML, e
para na raiz de cada projeto. Marcadores próprios de engine vencem manifestos que ela
carrega junto (RPG Maker MZ tem `package.json`; Unity gera `.csproj`). `shared/` e
pastas de build das engines não entram como jogo.

## Pacotes de plataforma e gênero

O núcleo é agnóstico. Quando o projeto tem engine identificável, `context` acrescenta
o [pacote de plataforma](packs/README.md) correspondente logo após a receita; quando
o gênero é declarado, acrescenta o pacote de gênero:

```sh
python3 scripts/game.py context /caminho/do/jogo --focus feel --genre platformer --root /caminho/do/laboratorio
```

Plataformas (18): `web`, `unity`, `godot`, `unreal`, `defold`, `gamemaker`, `construct`,
`rpgmaker`, `renpy`, `roblox`, `pico8`, `haxe`, `flutter`, `dotnet`, `cpp`, `cargo`,
`python`, `lua`. Gêneros (23): `narrative`, `adventure`, `platformer`, `action-adventure`,
`shooter`, `fighting`, `stealth`, `horror`, `racing`, `sports`, `rhythm`, `turn-based`,
`deckbuilder`, `strategy`, `tower-defense`, `puzzle`, `simulation`, `survival-crafting`,
`rpg`, `roguelike`, `multiplayer-competitive`, `idle`, `casual`. Cada pacote traz comandos
reais de execução/teste, ciclo de vida, pipeline, ferramentas de medição e riscos do
gênero — como convenções a confirmar no projeto, não como capacidade certificada.
Um campo `Gênero:` em documento do projeto aparece em `packs.genre.suggested`; só
`--genre` carrega o pacote. `context.packs` explica cada seleção.

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

Ele confere a forma da declaração, não o jogo, e relata em `problems` o que
encontra com arquivo, linha e motivo: dimensão fora das dez (o caso típico é erro
de digitação), degrau fora dos cinco, alvo que não é o degrau imediatamente
seguinte, alvo ausente. **Uma tabela bem formada e otimista sai daí intacta**,
porque o degrau é afirmação de quem escreveu. O ganho não é aferição, é que a
dimensão mais baixa passa a ter nome — e `next` propõe subir exatamente ela,
citando o critério escrito no documento e a linha de onde veio, em vez de listar
as dez. Havendo linha malformada, ele propõe corrigi-la primeiro: ela é a causa da
dimensão que aparece como não declarada.

## Gates

A barra descreve **onde o jogo está**. Um gate diz **o que ainda não pode
passar**. [Os dez](references/gates.md) não foram inventados: cada um formaliza
uma linha `**Pronto para…**` que já existia em prosa no ciclo criativo, com o
critério de saída da etapa. Faltava alguém ler essas linhas e alguém recusar.

```sh
python3 scripts/game.py gate /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py gate /caminho/do/laboratorio/meu-jogo --gate deliver
```

Um gate tem nome do que você está pedindo, não da etapa que acabou: `design`,
`test`, `prototype`, `close`, `implement`, `build`, `scale`, `evaluate`,
`conclude`, `deliver`. A ordem é a do ciclo, e o ciclo tem retorno — reprovar em
`scale` devolve para `build`, o que é uso normal.

O projeto declara uma linha por critério, em `README.md`, `docs/qa.md`,
`docs/devlog.md`, `docs/release.md` ou `docs/prd.md`:

```markdown
| Gate | Critério | Estado | Evidência |
| --- | --- | --- | --- |
| `deliver` | `runbook` | `met` | Ana construiu do zero em 2026-09-02, log em /tmp/qa-07 |
| `deliver` | `foreign_machine` | `unmet` | só rodou na máquina de dev |
| `deliver` | `save_migration` | `waived` | sem versão anterior publicada — Alan, 2026-09-05 |
```

**As três saídas de um gate são passar, cortar escopo e abandonar.** A terceira é
a que costuma faltar: abandonar não é falha do gate, é uma das respostas dele — o
ciclo já dizia isso na etapa `poc`, e aqui vale para todas. Um processo que só
admite “passou” e “ainda não” empurra escopo morto para frente até ele custar
caro demais para matar.

Dispensa é estado de primeira classe, porque produção real dispensa requisito com
assinatura — mas exige motivo escrito, senão é o critério apagado da lista.
**Quatro critérios não são dispensáveis**, e não por escolha do harness: a prosa
da etapa não deixa terceira opção (licença desconhecida bloqueia a entrega;
prioridade não remove exigência explícita do usuário; teste com pessoa não se
registra onde houve só simulação; origem de referência é declarada ou a ausência
é explícita).

Critério sem linha conta como **pendente**, nunca como cumprido: silêncio não é
aprovação. `met` sem nada escrito ao lado é recusado. Duas linhas discordantes
mantêm o estado mais fraco e o conflito fica listado. `next` propõe resolver o
critério pendente do primeiro gate **declarado** — um gate que o projeto não
mencionou não está sendo pedido.

O campo se chama `held_by_declaration`, não `passed`: ele diz que o projeto afirma
cumprir, não que alguém conferiu. **Nenhum comando concede passagem** (`granted`
é sempre `false`), e uma tabela bem formada e otimista sai daí intacta, como sai
da barra.

## Starters

`assets/starters/` guarda projetos de referência completos para o passo REUSE.
Hoje há um:

**`canvas-arcade`** — jogo em Canvas 2D com loop de passo fixo, RNG semeado,
hash de estado, abstração de entrada (teclado, ponteiro, gamepad, remapeável),
mixer com barramentos/ducking/limite de vozes/legendas, save versionado com
migração e gravação verificada, e renderizador com alto contraste e redução de
movimento. Expõe `pause`, `reset`, `seed`, `observe`, `act`, `advance`, `capture`
e `dispose`, e **exercita** as oito em testes headless (`npm test`) — com uma
ressalva: `capture` só na guarda de ausência de tela, porque `toDataURL` não
existe em headless. Também tem `npm run budget` para o orçamento de simulação. O
README do starter declara em que degrau cada dimensão está, incluindo as que
ainda não subiram.

"Gravação verificada" é literal e menos do que atômica: escreve em chave de
estágio, relê, compara e grava na real. `localStorage` não tem substituição, então
a última escrita é comum. [A receita de persistência](recipes/persistence.md)
explica o que isso compra e o que não compra.

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

Fonte encontrada não é tarefa validada — e fonte em rascunho não é nem passo. Num
projeto recém-criado, as fontes que `scan` lista são os campos de template
("Próxima ação: [...]"), todas com `status: "draft"`; `next` não propõe retomar
nenhuma delas, porque não há nada escrito para retomar. Ele volta a propor quando
alguma fonte deixa de ser rascunho.

## Processo

[Pré-produção](references/preproduction.md): Game Brief → GDD/MDA ↔ protótipo/PoC
e playtest → PRD/TDD → vertical slice → produção/MVP → QA → release. Orientação de
dependências, não esteira rígida. Um jogo pequeno pode reunir essas decisões em
um documento.

Dez templates do ciclo: brief, mda, gdd, poc, prd, tdd, vertical-slice, mvp, qa,
release. Quatro complementos: `art-bible`, `devlog`, `audit`, `aaa` (checklist de piso;
o `context` expõe `finish` — núcleo / produto / promessa / mercado; slice, QA, create,
feel e audio carregam a guia; `template aaa` não certifica). Três de consolidação e
produção: `game-design` (documento único), `production-plan`, `milestone`.

```sh
python3 scripts/game.py context /caminho/do/jogo --focus content --stage gdd --root /caminho/do/laboratorio
python3 scripts/game.py template brief --project meu-jogo
python3 scripts/game.py template art-bible --project meu-jogo --output /tmp/meu-jogo-art.md
python3 scripts/game.py template aaa --project meu-jogo
python3 scripts/game.py context /caminho/do/jogo --stage aaa --root /caminho/do/laboratorio
```

Sem `--output`, `template` só imprime. Com ele, cria um rascunho novo e recusa
sobrescrita, inclusive de symlinks. Gerar `template audit` não executa auditoria. Gerar
`template aaa` não certifica acabamento nem publisher. Gerar `template release` não
concede autorização de publicação.

**REUSE → ADAPT → CREATE.** CREATE só entra com lacuna explícita.
O [contrato JSON](assets/work.example.json) formaliza uma decisão nova;
`check-plan` valida a forma, não o mérito. O arquivo de exemplo é um formulário em
branco, de propósito: rodá-lo no validador devolve os oito campos que faltam, que
é a lista do que preencher.

```sh
python3 scripts/game.py check-plan caminho/do/trabalho.json --root /caminho/do/laboratorio
```

Treze receitas: [criar](recipes/create.md), [mecânicas](recipes/mechanics.md),
[ciclo de vida](recipes/lifecycle.md), [conteúdo](recipes/content.md),
[visual](recipes/visual.md), [áudio](recipes/audio.md), [feel](recipes/feel.md),
[rede](recipes/network.md), [arquitetura](recipes/architecture.md),
[performance](recipes/performance.md), [acessibilidade](recipes/accessibility.md),
[persistência](recipes/persistence.md), [release](recipes/release.md) e
[produção](recipes/production.md). `--focus architecture` ou `--stage tdd` carrega a
receita de arquitetura; `--focus feel` e `--focus audio` carregam acabamento do verbo;
`--focus production`, `--stage production-plan` ou `--stage milestone` carregam a de
produção. A skill aplica quando a mudança pede; o CLI só seleciona referências.

## Produção e acabamento

[Produção](recipes/production.md) trata marcos como critérios de evidência — first
playable → vertical slice → alpha → beta → gold → live — com lentes de disciplina
(design, arte, animação, áudio, feel, UX/acesso, técnica, conteúdo, localização, QA,
plataforma), orçamentos medidos na plataforma alvo, pipeline de conteúdo e
estabilidade. Os marcos são o **calendário**; a [barra](#barra-de-acabamento) diz onde o
jogo está em cada dimensão e os [gates](#gates) o que ainda não pode passar. “AAA”
aqui é padrão de acabamento observável, não orçamento.

```sh
python3 scripts/game.py context /caminho/do/jogo --focus production --stage production-plan --root /caminho/do/laboratorio
python3 scripts/game.py template milestone --project meu-jogo --output /tmp/meu-jogo-alpha.md
```

O plano de produção entra em `continuity.sources` quando existe. Nenhum comando mede
orçamento, executa soak, promove marco ou certifica requisito de plataforma; a
passagem é declarada por pessoa com a prova ligada (`record --kind milestone`).
Exemplo: [da trilha ao capítulo acabado](examples/era-uma-vez-production.md).

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
python3 scripts/game.py verify /caminho/do/jogo --output /tmp/jogo-qa-02 --root /caminho/do/laboratorio --command python3 tools/verify.py
```

`--command` vai por último. Não há shell implícito. Cada execução cria uma pasta
inédita. Destino existente é recusado. Build verde não prova arte, feel, áudio, reinício, rede
nem que o jogo é divertido. `experience_status` continua `not_assessed`.

`--script` aceita scripts de `package.json` (npm/pnpm/yarn/bun conforme declaração
ou lockfile) e, em projetos com `Cargo.toml`, os alvos `check`, `build` e `test`.
Unity, Godot e Unreal não têm CLI padronizada; use `--command` com o executável real.

`context` só sabe dizer `mentioned` sobre as oito capacidades conhecidas — pause,
reset, seed, observe, act, advance, capture, dispose — porque lê arquivos sem
executá-los. `--proves` **não** promove nenhuma delas a verificada; o harness não
tem como saber se um comando exercita pause.

```sh
python3 scripts/game.py verify /caminho/do/jogo --script test --output /tmp/jogo-qa-03 --proves pause --proves reset --proves seed
```

O que ele acrescenta é uma alegação com autor, data, argv e log: `claimed` quando
os comandos passaram, `unsupported` quando falharam. Em vez de sumir na prosa, a
afirmação fica anexada a um recibo e pode ser contestada por quem ler. A declaração
é de **quem executa**, nunca do repositório: nenhum arquivo do projeto seleciona
capacidade, e `claimed` continua não sendo `verified`.

## Registrar evidência declarada

O que o `verify` não cobre — observação de pessoa em movimento, medição de orçamento,
decisão de marco — entra por `record`, em pasta inédita e ligado ao HEAD do projeto:

```sh
python3 scripts/game.py record /caminho/do/jogo --kind observation --author "Alan" --note "Completou a volta sem instrução." --field scenario=travessia --field role=human --attach /tmp/playtest.mp4 --output /tmp/jogo-obs-01 --root /caminho/do/laboratorio
python3 scripts/game.py record /caminho/do/jogo --kind budget --author "Alan" --note "Travessia completa" --field metric=frame_p99 --field value=14.2 --field unit=ms --field platform=tablet-ref --field tool=devtools --output /tmp/jogo-budget-01 --root /caminho/do/laboratorio
python3 scripts/game.py record /caminho/do/jogo --kind milestone --author "Alan" --note "Critérios com evidência ligada." --field milestone=alpha --field decision=declared --field declared_by=Alan --field role=human --output /tmp/jogo-alpha-gate --root /caminho/do/laboratorio
```

Campos obrigatórios por tipo: `observation` → `scenario`, `role` (`human`/`agent`);
`budget` → `metric`, `value` numérico, `unit`, `platform`, `tool`; `milestone` →
`milestone`, `decision` (`declared`/`denied`/`deferred`), `declared_by`, `role`. Anexos
entram por caminho e SHA-256. O recibo guarda o que foi declarado; não valida, não
mede e não aprova. `role=agent` é avaliação do agente, não aprovação do usuário.

## Três camadas

- **IA:** interpreta a intenção, consulta fontes e propõe a mudança. Não depende
  de um fornecedor.
- **Harness:** recorta o contexto, varre a base, valida a forma do contrato,
  monta projetos a partir de starters, corre os comandos escolhidos com recibo e
  registra evidência declarada.
- **Memória:** brief, decisões, plano de produção, estudos e evidência ficam nos
  locais canônicos de cada jogo.

## O que este repositório não é

Não há engine comum, API universal de ações, avaliação automática de diversão,
medição automática de performance ou publicação automática. “AAA” neste texto é piso
de acabamento observável, não tier de publisher, orçamento nem certificado de mercado;
o alvo honesto com IA é AA / Triple-I nesse piso. Os jogos do
[playground](https://games.alanicolas.com/) continuam com a própria engine; este
harness não reivindica tê-los produzido.

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
