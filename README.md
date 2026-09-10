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
dimensões ainda não têm linha, quais validadores existem, quantos papéis de
áudio estão declarados e vazios, se o feel tem constante e recibo de
observação, se o achado de playtest tem forma, se alcance, save e orçamento
estão declarados no código, se a
direção de arte aparece no disco, se o conteúdo saiu do código e se existe
passo de empacotar. É essa diferença que
uma listagem de caminho e tipo apagava — três jogos em estados incomparáveis saíam
iguais. `--plain` volta ao caminho e tipo, sem ler documento nenhum.

A ordem é a do disco e não muda: **o harness não classifica os jogos por
urgência**, porque nada aqui observa qual importa mais. Ele conta e lê; escolher
continua sendo trabalho de quem olha. Um projeto ilegível aparece com o motivo, em
vez de derrubar a revisão ou desaparecer da lista.

## Começar um jogo novo

Com starter (REUSE de infraestrutura já testada):

```sh
python3 scripts/game.py start --idea "atravessar estilhaços para guardar a corrente"
python3 scripts/game.py start /caminho/do/laboratorio/meu-jogo --starter canvas-arcade --idea "atravessar estilhaços para guardar a corrente"
```

Sem caminho, `--idea` nomeia e cria a pasta (ao lado do framework se o start corre de dentro desta árvore; no diretório atual se corre de fora). `guide --idea` continua só no comando, não no disco. O JSON devolve `play` (o comando que **abre** o jogo), `then.note` (o próximo comando do harness **depois** de uma partida) e, se o starter declara, `cycle` (verbo, teclas, cluster de uma mão, toque, controle e as queries de look, chuva, par e convite). Se o projeto — ou o starter, antes do destino existir — declara as ferramentas, `then` também nomeia `pair`, `look`, `table` e `sfx`. Se declara `session`, `then` a aponta. O `note` do mapa sugere o autor do git ou do ambiente; não é quem jogou. Nomear o ofício não pinta. Depois de um recibo de observação, o prompt aponta esses três em vez de repetir só o primeiro ciclo. Não executa o jogo. `--idea` entra no brief e, se houver `data/copy.json`, na abertura e no aviso do primeiro ciclo. O brief continua rascunho. A frase na tela não muda o verbo. Depois do `init`, `?look=dusk` ou `?look=calm` troca a paleta (campo e a página), `?spawn=dusk` ou `?spawn=calm` troca a chuva, `?mood=calm` ou `?mood=dusk` troca o par e `?invite=1` some a tabela — as quatro sem recomeçar o projeto. A página nomeia o par no select. Look ou chuva explícitos vencem o mood no próprio eixo. Trocar a chuva do par recomeça a partida; trocar só o look não. Ferramenta no disco não é alguém de fora nem mix ouvido.

`guide` (também sem subcomando: `python3 scripts/game.py`) mapeia os três passos — start → jogar → `note` — sem executar nenhum. `open` é o comando de agora (o start se o destino ainda não existe, o play se já existe); `prompt` o nomeia para colar. Sem destino, a frase nomeia a pasta no comando do start (ao lado do framework se você está dentro desta árvore; no diretório atual se está fora). Não grava a frase nem cria a pasta. Sem destino, se o diretório atual é um jogo fora deste repositório, o mapa usa esse caminho. Dentro do framework o comando sem argumentos continua o convite a começar:

```sh
python3 scripts/game.py --idea "atravessar estilhaços para guardar a corrente"
python3 scripts/game.py guide /caminho/do/laboratorio/meu-jogo --idea "atravessar estilhaços para guardar a corrente"
```

`guide` não cria o projeto. `next` sai do caminho feliz: só entra em `then.lost`, quando o ciclo já correu e você não sabe o que falta. Com destino existente, preenche o comando que abre o jogo e o `kind` do passo de jogar. `executed` fica `false`. Sem `start`, o caminho em dois passos continua valendo:

```sh
python3 scripts/game.py init /caminho/do/laboratorio/meu-jogo --starter canvas-arcade --idea "atravessar estilhaços para guardar a corrente"
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
`starter.json` dele declara e cria em `docs/` os rascunhos que ainda faltam —
brief, gdd, mda, tdd, devlog e qa — além de `AGENTS.md` na raiz. Documento
vigente que o starter já trouxe (o art-bible do `canvas-arcade`) não é
reescrito: o `template` recusaria o destino e a decisão vigente sumiria.
Os seis rascunhos mais o art-bible cobrem sete das nove áreas mínimas que
`scan` cobra; as outras duas, origem e execução, ficam com o README e o
CREDITS do starter, então depois do `init` as nove têm candidato. Com
`--no-docs`, o art-bible permanece e os rascunhos não são criados; README,
CREDITS e art-bible cobrem três áreas. `--idea` escreve a frase da fantasia
no brief e em `data/copy.json`; o brief continua rascunho e a frase na tela
não muda o verbo. Os demais templates do ciclo entram depois, com `template`, quando a
etapa chegar. Não instala dependências, não toca no starter de origem e recusa
destino ocupado. `scan` reconhece o resultado no mesmo turno; o primeiro comando
que `init` aponta é o que serve o jogo, e `verify` roda os validadores do starter
onde houver Node.

`next` deriva **uma** proposta do estado no disco e ordena por dependência: sem
destino → sem entrypoint → área não localizada → ciclo jogável ainda sem partida
→ segundo ciclo de par, look, chuva e voz
→ papéis de áudio vazios → feel ainda sem observação → convite para quem nunca viu o jogo → achado sem forma →
acessibilidade sem opção
→ save sem versão → orçamento ausente → direção de arte ausente → conteúdo
ainda no código → empacotar ainda sem passo → rascunho → documento sem versão
vigente → continuidade → sem instruções para o agente → validadores → origens sem
recibo → gate → ofício → barra. Depois de um `init` fresco — nove áreas com
candidato, seis ainda rascunho (o art-bible do starter já vem vigente), e um script que abre o jogo — a primeira proposta
é jogar o ciclo, não preencher os templates. Depois do recibo, se o projeto
declara `pair`/`look`/`table`/`sfx` e ainda não nasceu look, chuva ou voz deslocada,
o `next` aponta o segundo ciclo de par, look, chuva e voz — ferramenta no disco
não é alguém de fora. O verbo mudo vem em seguida: papéis
declarados sem arquivo. Depois, se o código nomeia perdão e hitstop e ninguém
registrou uma observação no projeto, o `next` pede esse recibo — constante
nomeada não é peso percebido. Depois do recibo, se o achado não nomeia
problema, evidência, hipótese e medição, o `next` pede a forma — nota de
partida não é métrica. Sem opção de alcance no código, sem versão de
save ou sem artefato de orçamento, esses ramos vêm antes dos rascunhos. Sem
paleta ou art-bible vigente, com conteúdo só no código, ou com manifesto e
nenhum passo de empacotar, esses ramos também vêm antes dos rascunhos. O gate tem três ramos: linha
de gate malformada, pergunta de valor e critério pendente — nessa ordem, porque
terminar o que talvez não devesse existir é o desperdício que um gate existe para
interromper. O ofício tem dois: linha de ofício malformada e checklist pendente.
A barra tem quatro, na ordem: linha de
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
| `deliver` | `save_migration` | `out_of_scope` | jogo sem save — Alan, 2026-09-05 |
```

**As três saídas de um gate são passar, cortar escopo e abandonar.** A terceira é
a que costuma faltar: abandonar não é falha do gate, é uma das respostas dele — o
ciclo já dizia isso na etapa `poc`, e aqui vale para todas. Um processo que só
admite “passou” e “ainda não” empurra escopo morto para frente até ele custar
caro demais para matar. As três correspondem a Go / Recycle / Kill do método
stage-gate, e a correspondência foi encontrada depois, não copiada antes
([levantamento](references/gates-research.md)).

**Um critério pergunta uma de duas coisas, e a diferença muda quem responde.**
`readiness` pergunta se o trabalho está feito, e falhar devolve para a etapa
anterior. `must_meet` pergunta se isto ainda vale o que custa, e falhar mata o
escopo — não se resolve trabalhando mais. Três critérios são desse tipo
(`close.decision`, `implement.worth_building`, `scale.worth_scaling`) e `next`
pergunta o valor antes de pedir mais trabalho no mesmo gate.

Dispensa é estado de primeira classe, porque produção real dispensa requisito com
assinatura — mas exige motivo escrito, senão é o critério apagado da lista.
**Quatro critérios não são dispensáveis**, e não por escolha do harness: a prosa
da etapa não deixa terceira opção (licença desconhecida bloqueia a entrega;
prioridade não remove exigência explícita do usuário; teste com pessoa não se
registra onde houve só simulação; origem de referência é declarada ou a ausência
é explícita). Os três `must_meet` também recusam dispensa, por outro motivo: um
“No” num must-meet decide sozinho, sem compensação.

**`out_of_scope` não é dispensa.** Dispensar é deixar de cumprir o que incide, e
um jogo sem save não “dispensa” a migração de save. Contar os dois juntos
inflaria a conta de dispensas justamente onde ela deveria doer, então o estado é
separado, exige motivo escrito igual, e é recusado nos sete critérios que sempre
incidem.

Critério sem linha conta como **pendente**, nunca como cumprido: silêncio não é
aprovação. `met` sem nada escrito ao lado é recusado. Duas linhas discordantes
mantêm o estado mais fraco e o conflito fica listado. `next` propõe resolver o
critério pendente do primeiro gate **declarado** — um gate que o projeto não
mencionou não está sendo pedido.

O campo se chama `held_by_declaration`, não `passed`: ele diz que o projeto afirma
cumprir, não que alguém conferiu. **Nenhum comando concede passagem** (`granted`
é sempre `false`), e uma tabela bem formada e otimista sai daí intacta, como sai
da barra.

## Origens

`deliver.licensing` é um dos quatro critérios que a prosa não deixa dispensar, e
até aqui o harness só lia a linha da tabela. Uma frase otimista fechava o gate.
`origins` percorre o disco:

```sh
python3 scripts/game.py origins /caminho/do/laboratorio/meu-jogo
```

Lista arquivos de mídia embarcados (som, imagem, fonte, vídeo, modelo) e cruza
com recibos: `sources.json`, `licenses.json`, `CREDITS` e sidecar
`.credits.txt`. Entra em `textures/`, `fonts/`, `models/` e `videos/` — pastas
que o `scan` de documentos ignora de propósito. **Não valida a licença.** Não
consulta titular, não interpreta texto jurídico e não distingue licença válida
de inválida. O que falta é recibo de origem; o que o recibo afirma continua
sendo alegação de quem escreveu.

`granted` e `validated` são sempre `false`. Se o projeto declara
`deliver.licensing` como `met` e o disco ainda tem arquivo sem recibo, a saída
marca `contradicts_licensing`. `next` propõe declarar a origem — ou tirar o
arquivo do embarque — antes de seguir o restante do gate.

## Ofício

Os gates perguntam se o trabalho está feito e se ainda vale o que custa. Isso
não cobre paleta, janela de perdão, definição de percentil nem regra de parada
de playtest. Esses checklists vêm do [levantamento de critérios
observáveis](references/observable-criteria-research.md) §7 — o único conjunto
que a pesquisa chamou de “não precisa de autoridade externa”: conformidade com
o que o **próprio projeto** declarou.

```sh
python3 scripts/game.py craft /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py craft /caminho/do/laboratorio/meu-jogo --gate scale
```

```markdown
| Check | Estado | Evidência |
| --- | --- | --- |
| `palette` | `met` | paleta em docs/art-bible.md; cores de src/game/render.js listadas lá — Ana |
| `playtest_stop` | `unmet` | regra de parada ainda não escrita |
```

**Nenhum checklist cita dígito.** Um limiar aqui seria o harness afirmando, para
este jogo, o que ninguém verificou. `observed` e `granted` são sempre `false`.
`next` só levanta um checklist do gate que o projeto **declarou** — o mesmo
silêncio dos gates: quem não pediu a permissão não recebe a lista.

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
existe em headless. A chuva compacta o array vivo e reusa um poço de
entidades; evento, telegraph e o gerador da chuva também reusam. Também tem `npm run budget` para o orçamento da cena `playing.run` (simulação e draw num
canvas stub) — relata o reuso, sem teto — e `npm run size` para os bytes de `dist/`. O
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
O complemento `agents` gera as instruções persistentes em `AGENTS.md`.

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

Quatorze receitas: [criar](recipes/create.md), [mecânicas](recipes/mechanics.md),
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

## Áudio

O starter declara os papéis do verbo, o orbe perdido, o fecho, a prática, a guarda e a cama (`const SOUNDS`) e já traz
design original em `public/sfx/<papel>.wav`. A cama entra em loop no
barramento de música. `roles` lê a declaração e cruza com
arquivos em `public/sfx` (e equivalentes). Papel vazio continua lacuna:

```sh
python3 scripts/game.py roles /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py roles /caminho/do/laboratorio/meu-jogo --fill
python3 scripts/game.py roles /caminho/do/laboratorio/meu-jogo --fill --apply --root /caminho/do/laboratorio
```

`heard` e `approved` são sempre `false`: arquivo presente não é mixagem ouvida.
`next` propõe `audio.roles` quando um papel está vazio. `roles --fill` sugere
um candidato do acervo; `--apply` copia para `public/sfx/<papel>` com recibo.
O starter carrega esse arquivo no mixer. `npm run mix` soma cama e vozes
de uma partida simulada com a mesma taxa da corrente; isso também não é
mix ouvida. Primeiro resultado da
busca não é mixagem. Silêncio deliberado é o papel fora da declaração, não
o slot sem arquivo.

Se o laboratório tiver `shared/sfx` **com sons** na raiz passada em `--root`:

```sh
python3 scripts/game.py sfx search passos --root /caminho/do/laboratorio
python3 scripts/game.py sfx copy ID --to /caminho/do/jogo/public/sfx --root /caminho/do/laboratorio
```

Sem esse acervo, `sfx search` devolve vazio e `sfx serve` recusa — não
há o que ouvir. Crescer o acervo é arquivo local com recibo:

```sh
python3 scripts/game.py sfx import /caminho/do.wav --metadata /caminho/meta.json --root /caminho/do/laboratorio
python3 scripts/game.py sfx seed --root /caminho/do/laboratorio
python3 scripts/game.py sfx info passo-madeira-01 --root /caminho/do/laboratorio
python3 scripts/game.py sfx export passo-madeira-01 --to /caminho/do/jogo/public/audio --root /caminho/do/laboratorio
```

`sfx import` exige ffmpeg e um JSON com id, título, categoria, estilo,
tags, processamento e fontes (licença CC0 ou CC-BY). `sfx seed` lê
`shared/sfx/selection.json` com `local_path` já no disco. Sem seleção,
o seed recusa. `sfx summary` (também sem subcomando) lê o acervo e os atalhos.
`sfx verify` cruza bytes e fichas; não ouve. `sfx info` lê a ficha
no disco. `sfx export` copia
bytes, `manifest.json` e `CREDITS.txt` para uma pasta fora do acervo.
Importar e exportar não é mix ouvido. O primeiro ciclo já tem voz
no starter (`public/sfx/<papel>.wav`). `shared/sfx` é ADAPT, não
pré-requisito. Piso: gravação licenciada ou design contemporâneo.
8-bit, chiptune, jsfxr e Kenney arcade não são o padrão. Este
repositório **não inclui** o acervo `shared/sfx` do laboratório.

## Feel

O starter nomeia perdão, graça, hitstop, buffer de guardar e punch de
câmera no `CONFIG`. Constante nomeada não é peso percebido. `feel` lê as
constantes e procura um `record.json` de observação no projeto:

```sh
python3 scripts/game.py feel /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py note /caminho/do/laboratorio/meu-jogo --author "NOME" --note "o que o verbo sentiu"
# o mapa preenche --author com git ou o ambiente; NOME só se os dois faltarem
```

`note` grava o recibo de observação em `docs/playtest/<utc>/` com cenário e
papel por omissão. `--from-run` anexa `docs/playtest/last-run.json` (resumo
e, se houver, a curva) como candidato de medição e não fecha o achado.
Não joga. `felt` é sempre
`false`. `next` propõe `feel.unobserved` quando há constante e não há
recibo; o comando que ele aponta é o `note`. O harness não atribui peso.

## Alcance, save e orçamento

Três leituras do disco, no mesmo formato honesto: o que o código declara, não
o que alguém observou.

```sh
python3 scripts/game.py access /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py save /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py budget /caminho/do/laboratorio/meu-jogo
```

`access` procura highContrast, reducedMotion, captions, remapeamento
(a página do starter lista as seis ações do teclado; toque e controle não entram),
uiScale, preset de uma mão (o ciclo nomeia IJKL + P/O quando o starter declara `hand`) e assistência. `verified` é sempre `false`. Trocar no stub não é sessão observada. `save` procura
armazenamento e PROGRESS_SCHEMA/migrate; `trusted` é sempre `false`.
`budget` procura script `budget`/`bench`, `tools/budget.*` ou
`record --kind budget`; `measured` é sempre `false`. O starter declara
os três; um canvas sem opção de alcance recebe `access.missing` antes da
barra.

## Arte, conteúdo e empacotar

Três dimensões que separam protótipo de produto, no mesmo formato: o que o
disco declara, não o que alguém aprovou.

```sh
python3 scripts/game.py art /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py content /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py ship /caminho/do/laboratorio/meu-jogo
```

`art` procura `const PALETTES`, tokens.json, `data/palettes.json` e `docs/art-bible.md` vigente.
`consistent` é sempre `false`. Rascunho do `init` não conta. `content`
procura dado em `data/`, `levels/` (e equivalentes) ou `.ldtk`/`.tmx`/`.ink`.
`enough` é sempre `false`. `ship` procura script `build`/`export`/`package`/
`release`, `docs/release.md` vigente ou CI. Se `dist/VERSION.json`
existe, relata nome e versão. `shipped` é sempre `false`.
HTML estático sem manifesto já é o artefato; manifesto sem passo de
empacotar recebe `ship.unpacked`. O starter declara paleta em
`data/palettes.json`, escolhe o look por `?look=` / `settings.look`
(`dusk` já é o segundo; `contrast` é alcance, não look), nasce o
próximo com `look --from` / `--as`, extrai a chuva
para `data/spawn.json` e `data/dusk.json`, escolhe o perfil por `?spawn=`,
nasce a próxima com `table --from` / `--as` e `session --spawn`, e
empacota com `npm run build` — look no disco, ferramenta que desloca knobs
ou tokens e um export na máquina de quem construiu não são direção
consistente, escala nem entrega.

## Playtest

Observação sem os quatro campos é impressão. `playtest` lê se o disco tem
problema, evidência, hipótese e medição — num documento ou no próprio
recibo:

```sh
python3 scripts/game.py playtest /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py playtest /caminho/do/laboratorio/meu-jogo --invite
```

`observed` e `outsider` são sempre `false`. `--invite` escreve
`docs/playtest/invite.md` e aponta `/?invite=1`, onde a tabela de
comandos some; página no disco não é alguém de fora e não sobe
`pacing`. `next` propõe `playtest.invite`
depois do recibo de quem fez (e depois do segundo ciclo, se houver).
`next` propõe `playtest.unstructured` quando há recibo de observação
(ou um `docs/qa.md` vigente) e o achado ainda não tem forma. Se
`docs/playtest/last-run.json` existir, `playtest` o relata
como `candidate` e o `next` aponta `note --from-run`. Se o candidato
tiver curva, o `note` a anexa. Número no disco não é causa. A tabela de
ofício que *descreve* o formato não conta como
achado. O harness não assiste à sessão e não conta jogadores.

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
cd assets/starters/canvas-arcade && npm test && npm run budget && npm run size
```

Histórico 0.1–0.9: [adoção](adoption.md).
