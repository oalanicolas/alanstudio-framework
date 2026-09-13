# Alan Studios Framework · 0.10

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

O framework pode ser usado por vários workspaces com uma única implementação.
Cada laboratório mantém um link `framework/core` para este checkout e um
encaminhador curto em `framework/scripts/game.py`. Regras e evidências locais
ficam no laboratório; recipes, packages, templates e testes compartilhados ficam
aqui. [Ligação e personalização](references/workspace-binding.md). Se a ligação recusa preencher pasta não baixada com o starter, o `context` nomeia a preenchida que a ligação já recusa. Módulo no disco não é o jogo. Sem chave `preenchida`. Se a ligação recusa inventar o conteúdo da referência ausente, o `context` nomeia o inventado que a ligação já recusa. Lacuna no disco não é a regra. Sem chave `inventado`.

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
passo de empacotar. `signals` nomeia os mesmos flags que o `next` usa
para o primeiro ciclo, o ofício, o feel sem recibo, o achado sem forma,
o convite, a origem sem recibo e as lacunas de dimensão — sem propor e
sem ranquear. Se o package declara os scripts, o `discover` nomeia os scripts que o package já declara. Lista no disco não é passo executado. Sem chave `scripts`. Se o roteiro recusa que o documento comprove qualidade, o `discover` nomeia a qualidade que o roteiro já recusa. Conta no disco não é acabamento. Sem chave `qualidade`. Se a guia recusa que gerar o documento seja autorizar, o item do review nomeia o autorizar que a guia já recusa. Documento no disco não é a autorização. Sem chave `autorizar`. Se o README recusa que listagem de caminho e tipo apague o estado, o `discover` nomeia a listagem que o README já recusa. Caminho no disco não é o jogo. Sem chave `listagem`. Sinal
verdadeiro não é partida jogada. Se o README recusa que sinal verdadeiro seja partida jogada, o `signals` do review nomeia a partida que o README já recusa. Sinal no disco não é alguém de fora. Sem chave `partida`. Lista de arquivo sem recibo não é
licença. Lista de chave ausente não é alcance observado. Se o README recusa que a lista de chave ausente seja alcance observado, o item do discover nomeia o alcance que o README já recusa. Lista no disco não é o alcance. Sem chave `alcance`. É essa diferença que
uma listagem de caminho e tipo apagava — três jogos em estados incomparáveis saíam
iguais. `--plain` volta ao caminho e tipo, sem ler documento nenhum.

A ordem é a do disco e não muda: **o harness não classifica os jogos por
urgência**, porque nada aqui observa qual importa mais. Se o README recusa que o recorte classifique por urgência, o `truncated` do `review` nomeia a urgência que o README já recusa. Recorte no disco não é o inventário. Sem chave `urgência`. Ele conta e lê; escolher
continua sendo trabalho de quem olha. Um projeto ilegível aparece com o motivo, em
vez de derrubar a revisão ou desaparecer da lista.

## Começar um jogo novo

Com starter (REUSE de infraestrutura já testada):

```sh
python3 scripts/game.py start --idea "atravessar estilhaços para guardar a corrente"
python3 scripts/game.py start /caminho/do/laboratorio/meu-jogo --starter canvas-arcade --idea "atravessar estilhaços para guardar a corrente"
```

Sem caminho, `--idea` nomeia e cria a pasta (ao lado do framework se o start corre de dentro desta árvore; no diretório atual se corre de fora). Se a receita recusa que nomear a pasta grave a frase, o `named` do `start` nomeia a frase que a receita já recusa. Slug no disco não é o documento. Sem chave `frase`. `guide --idea` continua só no comando, não no disco. O JSON devolve `open` (o comando de agora, igual a `play`), `then.note` (o próximo comando do harness **depois** de uma partida), os mesmos `steps` do `guide` com o passo 1 feito e, se o starter declara, `cycle` (verbo, porta, teclas, cluster de uma mão, toque, controle e as queries de look, chuva, par, seed, relógio e convite). Se o projeto — ou o starter, antes do destino existir — declara as ferramentas, `then` também nomeia `pair`, `look`, `table` e `sfx`. Se o `tools/new-pair.*` nasce look e chuva, o `start` nomeia o par que o pair já nasce. Ferramenta no disco não é alguém de fora. Sem chave `pair` no recibo. Se a receita recusa que nove arquivos vazios aumentem a qualidade, o `start` nomeia os vazios que a receita já recusa. Arquivo no disco não é a fatia. Sem chave `vazios`. Se a receita recusa que título e cores novos sejam experiência, o then do start nomeia a experiência que a receita já recusa. Nome no disco não é o ciclo jogado. Sem chave `experiência`. Se a receita recusa que o start execute e observe, o `created` do `start` nomeia o executa que a receita já recusa. Pasta no disco não é a partida. Sem chave `executa`. Se declara `session`, `then` a aponta e o prompt a nomeia (`Sessão:`). Não executa e não observa. Se o disco tem last-run com seed, `then` aponta a seed e o convite; nomear o endereço não observa. O `note` do mapa sugere o autor do git ou do ambiente; não é quem jogou. Nomear o ofício não pinta. Depois de um recibo de observação, o prompt aponta esses três em vez de repetir só o primeiro ciclo. Não executa o jogo. `--idea` entra na abertura se houver `data/copy.json`. O `start` não planta os rascunhos; `--docs` os cria. O `init` continua plantando. A frase na tela não muda o verbo. `runtime` lê o `node` do PATH se o play pede npm ou node; sem 20+ o prompt avisa. Nomear não serve. Depois do `init`, `?look=dusk` ou `?look=calm` troca a paleta (campo e a página), `?spawn=dusk` ou `?spawn=calm` troca a chuva, `?mood=calm` ou `?mood=dusk` troca o par e `?invite=1` some a tabela — as quatro sem recomeçar o projeto. `?seed=<n>` abre essa partida e ignora o hold. `?speed=0.75` dilata o relógio da partida; 1 e fora da faixa somem. A página nomeia o par no select. Look ou chuva explícitos vencem o mood no próprio eixo. Trocar a chuva do par recomeça a partida; trocar só o look não. Ferramenta no disco não é alguém de fora nem mix ouvido.

`guide` (também sem subcomando: `python3 scripts/game.py`) mapeia os três passos — start → jogar → `note` — sem executar nenhum. `open` é o comando de agora (o start se o destino ainda não existe, o play se já existe); `prompt` o nomeia para colar e também sai em stderr — o JSON fica no stdout. Se o starter declara o verbo e as teclas, o prompt as nomeia — inclusive a porta — antes do destino existir. Se o manifesto declara o relógio, o `guide` nomeia o relógio que o manifesto já declara. Frase no disco não é partida observada. Sem chave `speed`. Se o roteiro recusa que o mural seja onboarding, o `guide` nomeia o onboarding que o roteiro já recusa. Texto no disco não é a primeira ação. Sem chave `onboarding`. Se a receita recusa que o screenshot comprove feel, o `guide` nomeia o screenshot que a receita já recusa. Recibo no disco não é peso percebido. Sem chave `screenshot`. Se o processo recusa que o comando abra o jogo, o `guide` nomeia a abertura que o processo já recusa. Nome no disco não é partida. Sem chave `abertura`. Se a receita recusa que passos textuais sejam uma garantia de execução, o `guide` nomeia os passos que a receita já recusa. Texto no disco não é a partida. Sem chave `passos`. Se a receita recusa que mostrar a estrutura seja a slice, o then do `guide` nomeia a estrutura que a receita já recusa. Mapa no disco não é a fatia. Sem chave `estrutura`. Se a receita recusa que estar em run prove estar livre, o ciclo nomeia o livre que a receita já recusa. Estado no disco não é a janela. Sem chave `livre`. Se a receita recusa que o tap seja o avanço, o ciclo nomeia o tap que a receita já recusa. Polegar no disco não é o dash. Sem chave `tap`. Se a receita recusa que o segurar seja o avanço, o ciclo nomeia o segurar que a receita já recusa. Segurar no disco não é o dash. Sem chave `segurar`. Se a receita recusa que o toque sem corrente decida o orbe, o ciclo nomeia o orbe que a receita já recusa. Toque no disco não é a escolha. Sem chave `orbe`. Se a receita recusa que a ordem do array decida a aposta, o ciclo nomeia a ordem que a receita já recusa. Ordem no disco não é a escolha. Sem chave `ordem`. Se a receita recusa que o hitstop no fim alongue o relógio, o ciclo nomeia o alonga que a receita já recusa. Hitstop no disco não é o limite. Sem chave `alonga`. Se a receita recusa que o cooldown metralhe, o ciclo nomeia o metralha que a receita já recusa. Cooldown no disco não é a rajada. Sem chave `metralha`. Se a receita recusa que o segurar na porta dispare o ofício, o ciclo nomeia o ofício que a receita já recusa. Porta no disco não é o ofício. Sem chave `ofício`. Se a receita recusa que o corpo siga o hold escondido, o ciclo nomeia o segue que a receita já recusa. Aba no disco não é o corpo. Sem chave `segue`. Se a receita recusa que Space e R disparem no quadro seguinte, o ciclo nomeia o seguinte que a receita já recusa. Foco no disco não é o verbo. Sem chave `seguinte`. Se a receita recusa que escrever dispare o verbo, o ciclo nomeia o escrever que a receita já recusa. Recado no disco não é o verbo. Sem chave `escrever`. Se a receita recusa que o buffer preserve a intenção, o ciclo nomeia a intenção que a receita já recusa. Buffer no disco não é a intenção. Sem chave `intenção`. Se a receita recusa que a nova direção no primeiro tick legal vire o verbo, o ciclo nomeia o tick que a receita já recusa. Tick no disco não é o verbo. Sem chave `tick`. Se a receita recusa que o lock seja o descanso, o ciclo nomeia o lock que a receita já recusa. Lock no disco não é o descanso. Sem chave `lock`. Se a receita recusa que três efeitos no impacto compensem input que ignora o botão, o ciclo nomeia os efeitos que a receita já recusa. Efeitos no disco não são o input. Sem chave `efeitos`. Sem destino, a frase nomeia a pasta no comando do start (ao lado do framework se você está dentro desta árvore; no diretório atual se está fora). Não grava a frase nem cria a pasta. Sem destino, se o diretório atual é um jogo fora deste repositório, o mapa usa esse caminho. Diretório atual não é o ciclo jogado. Se a receita recusa que o diretório atual seja o ciclo jogado, o `here` do `guide` nomeia o aqui que a receita já recusa. Pasta no disco não é a partida. Sem chave `aqui`. Na raiz deste repositório, sem `--idea` e sem caminho, o mapa recusa — o mesmo `sem destino` do `start`. A recusa nomeia o `start --idea` que este README já imprime. Nomear não cria. Não devolve mais `start '<destino>'`. De uma subpasta (o starter) ou de um jogo, o comando sem argumentos continua o mapa. O convite a começar na raiz leva a frase:

```sh
python3 scripts/game.py --idea "atravessar estilhaços para guardar a corrente"
python3 scripts/game.py guide /caminho/do/laboratorio/meu-jogo --idea "atravessar estilhaços para guardar a corrente"
```

Perdeu o JSON do `start`? `play` (também `open`) aponta de novo o comando que abre o jogo, sem executar. Sem caminho, o único jogo do laboratório basta; dois pedem o caminho.

```sh
python3 scripts/game.py play
python3 scripts/game.py play /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py open /caminho/do/laboratorio/meu-jogo
```

`play` e `open` são o mesmo verbo. Se o play pede npm, o `package.json` tem dependências e `node_modules` falta, `then.install` nomeia `npm install`. Sem dependências a chave some. Nomear não instala. Se o serve recusa produção, o `play` nomeia a produção que o serve já recusa. Serve no disco não é publicação. Sem chave `produção`. Se a receita recusa que verbo mudo ou sem peso seja, o `play` nomeia o verbo que a receita já recusa. Abrir no disco não é o verbo. Sem chave `verbo`. Se a receita recusa que o arco prometa o dash, o `play` nomeia o arco que a receita já recusa. Arco no disco não é o dash. Sem chave `arco`. `url` nomeia a superfície pedida (`http://localhost:8080/` quando o script é `serve` e não há `PORT`). Nomear não serve. Se o serve tenta abrir o navegador, o prompt nomeia a tentativa. Sem o marcador, pede Abrir. Nomear não abre. Com tela, o avanço abre a porta. Depois de uma partida, a página grava o recibo se você escrever; o próximo comando do harness continua `note`. o recibo escrito não observa. Se a receita recusa que o recibo escrito observe, o `noted` do `play` nomeia o escrito que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `escrito`. O prompt nomeia o `playtest` que o `AGENTS.md` já cita. Só lê. Sem os quatro não é achado. Sem `then.playtest`. Nomear o leitor não observa. Se a receita recusa que nomear o leitor observe, o `observations` do `playtest` nomeia o recibo que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `recibo`. `note`, `next`, `feel` e `playtest` sem caminho usam o mesmo resolvedor. Se o disco tem last-run com seed, `then.seed` aponta `/?seed=<n>` e, se o candidato nomeou a chuva ou o look, junta a mesa e a paleta. `then.invite` aponta o convite com os mesmos eixos. Nomear o endereço não observa. Se a receita recusa que aceitar o parâmetro prove que ele afeta o RNG, o then do `play` nomeia o RNG que a receita já recusa. Endereço no disco não é a simulação. Sem chave `RNG`. Se a receita recusa que oferecer o recibo seja observação, o then do `play` nomeia a observação que a receita já recusa. Recibo no disco não é a sessão. Sem chave `observação`. Vestir a query não grava. A chuva da query não retoma o hold. Na porta e no fim a região viva nomeia a mesa e o look que a chuva já veste — spawn e normal somem. Na porta o telefone vê Jogar: toque sem ter apertado. Depois do tap a porta não chama o avanço de cima. `executed` fica `false`. `runtime` lê o `node` do PATH se o play pede npm ou node; sem 20+ o prompt avisa. `usable` é só o binário. Se a receita recusa que o usable seja mais que o binário, o `usable` do `runtime` nomeia o binário que a receita já recusa. Node no PATH não é o dispositivo. Sem chave `binário`. `session` aponta a partida simulada se o manifesto a declara; o prompt a nomeia. Não executa e não observa. Nomear não serve. Não cria pasta e não serve. Achar o único jogo do laboratório também não executa e não sente. A frase de agora sai em stderr; encanar o stdout continua o recibo.

`guide` não cria o projeto. Se o README recusa que o guide crie o projeto, o `exists` do `guide` nomeia o projeto que o README já recusa. Destino no disco não é criação do mapa. Sem chave `projeto`. `next` sai do caminho feliz: só entra em `then.lost`, quando o ciclo já correu e você não sabe o que falta. Com destino existente, preenche o comando que abre o jogo e o `kind` do passo de jogar. `executed` fica `false`. Sem `start`, o caminho em dois passos continua valendo:

```sh
python3 scripts/game.py init /caminho/do/laboratorio/meu-jogo --starter canvas-arcade --idea "atravessar estilhaços para guardar a corrente"
python3 scripts/game.py next /caminho/do/laboratorio/meu-jogo --focus feel
```

`doctor` observa Python, Node, git, ffmpeg, presença dos arquivos do framework (receitas,
templates, referências e pacotes), raiz, projetos reconhecidos, estudos, acervo
sonoro, starters disponíveis e os atalhos de skill do host — vigente, desatualizado
ou ausente, comparando conteúdo.
Sem jogo reconhecido e com starter, `then.guide` aponta o mapa ideia→ciclo com `--idea`. Se o README imprime o exemplo, o `doctor` nomeia o exemplo que o README já imprime. Frase no then não é pasta criada. Sem chave `exemplo`. Se a ambição recusa que o harness seja motor, o `doctor` nomeia o motor que a ambição já recusa. Convite no then não é runtime. Sem chave `motor`. Se a skill recusa que AAA seja tier de publisher, o `doctor` nomeia o publisher que a skill já recusa. Atalho no disco não é orçamento. Sem chave `publisher`. Se o mapa recusa que a ausência seja evidência negativa, o `doctor` nomeia a ausência que o mapa já recusa. Lista no disco não é laboratório. Sem chave `ausência`. Se a receita recusa que o mapa crie a pasta, o `empty` do `doctor` nomeia a pasta que a receita já recusa. Lista no disco não é projeto criado. Sem chave `pasta`. não comprova que um projeto funciona. Se a receita recusa que a lista bloqueante comprove que um projeto funciona, o `blocking` do `doctor` nomeia o funciona que a receita já recusa. Checagem no disco não é o jogo. Sem chave `funciona`. Sem frase a raiz recusa.
Se o package pede Node, o `doctor` nomeia o engines que o package já declara. Pedido no disco não é binário no PATH. Sem chave `engines`. Nomear não instala. Se o manifesto declara as trocas, o `doctor` nomeia as substituições que o manifesto já declara. Manifesto no disco não é projeto criado. Sem chave `substitutions`.
Não cria e não executa. Sem starter, o aviso nomeia `start --idea`, não `init`.
Symlink apontando para o `SKILL.md` deste repositório conta como vigente: é o
atalho que não tem como ficar para trás. Não escreve nada; sinaliza bloqueio pelo
código de saída, e a correção que ele sugere roda como está — inclusive criando a
pasta do atalho.

`init` copia um starter, troca pelo nome do projeto os valores que o
`starter.json` dele declara e cria em `docs/` os rascunhos que ainda faltam —
brief, gdd, mda, tdd, devlog e qa — além de `AGENTS.md` na raiz. rascunho plantado não é GDD. Se a receita recusa que o rascunho plantado seja GDD, o `documents` do `init` nomeia o GDD que a receita já recusa. Rascunho no disco não é o documento. Sem chave `gdd`. Se o package declara o módulo, o `init` nomeia o módulo que o package já declara. Tipo no disco não é runtime instalado. Sem chave `type`. Se o processo recusa que se copie runtime de referência só para absorver um contrato, o `init` nomeia as referências que o processo já recusa. Runtime no disco não é o contrato. Sem chave `referências`. Se a receita recusa que o scaffold ou a cópia que inicia seja mais que ponto de partida, o then do `init` nomeia o scaffold que a receita já recusa. Cópia no disco não é a slice. Sem chave `scaffold`. O MDA
nomeia a porta; brief e GDD já falavam e o cenário do MDA começava no
campo. Nomear a abertura não observa. Documento
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
que `init` aponta é o que serve o jogo. `open`, `url` e `prompt` nomeiam
a mesma superfície do `start` — o `prompt` também sai em stderr. Nomear
não serve. `verify` roda os validadores do starter onde houver Node. Se o roteiro recusa aprovar a criatividade, o `verify` nomeia a criatividade que o roteiro já recusa. Recibo verde não é aprovação. Sem chave `criatividade`. Se a ambição recusa que o recibo comprove diversão, o `verify` nomeia a diversão que a ambição já recusa. Log no disco não é experiência. Sem chave `diversão`. Se a entrega recusa que o hash comprove o significado, o comando do verify nomeia o significado que a entrega já recusa. Hash no disco não é o critério. Sem chave `significado`. Se a receita recusa que teste unitário de serialização prove conectividade real, o `verify` nomeia a conectividade que a receita já recusa. Recibo verde não é sessão real. Sem chave `conectividade`.

`next` deriva **uma** proposta do estado no disco e ordena por dependência: módulo não baixado → sem
destino → sem entrypoint → área não localizada → ciclo jogável ainda sem partida
→ segundo ciclo de par, look, chuva e voz
→ papéis de áudio vazios → feel ainda sem observação → convite para quem nunca viu o jogo → achado sem forma →
acessibilidade sem opção
→ save sem versão → orçamento ausente → direção de arte ausente → conteúdo
ainda no código → empacotar ainda sem passo → artefato incompleto → artefato de outro HEAD → árvore pronta para servir → rascunho → documento sem versão
vigente → continuidade → sem instruções para o agente → validadores → origens sem
recibo → gate → ofício → barra. Se o processo pede uma ação recomendada, o `next` nomeia a ação que o processo já pede. Proposta no disco não é autorização. Sem chave `ação`. Se o roteiro recusa que o comando crie o jogo, o `next` nomeia a criação que o roteiro já recusa. Proposta no disco não é pasta criada. Sem chave `criação`. Se o next recusa que fonte encontrada seja tarefa validada, o `next` nomeia a validada que o next já recusa. Fonte no disco não é a tarefa. Sem chave `validada`. Se o processo recusa fabricar tarefa para cumprir o formato, o `next` nomeia a fabricação que o processo já recusa. Lista no disco não é backlog. Sem chave `fabricação`. Se o processo recusa que comando registrado com falha ou uma proposta rejeitada conclua a etapa, a alternativa do `next` nomeia a etapa que o processo já recusa. Proposta no disco não é a etapa. Sem chave `etapa`. Se a receita recusa que nome de comando prove a conclusão, o `signals` do next nomeia a conclusão que a receita já recusa. Sinal no disco não é o término. Sem chave `conclusão`. Se o fluxo recusa que melhorar o jogo seja uma rodada executável, o `next` nomeia a rodada que o fluxo já recusa. Pedido no disco não é o recorte. Sem chave `rodada`. Depois de um `init` fresco — nove áreas com
candidato, seis ainda rascunho (o art-bible do starter já vem vigente), e um script que abre o jogo — a primeira proposta
é jogar o ciclo, não preencher os templates. Depois de um `start` — sem os seis rascunhos — a primeira proposta continua jogar o ciclo: jogo que abre não espera área localizada. Depois do recibo, se o projeto
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
nove áreas. `context` entrega o recorte de leitura e a checagem documental. Se o processo recusa que o hash seja leitura, o `git` nomeia a leitura que o processo já recusa. Identidade no disco não é inspeção. Sem chave `leitura`. Se o processo recusa que estados salvos estejam atualizados, o `git` nomeia os desatualizados que o processo já recusa. Snapshot no disco não é o estado. Sem chave `desatualizados`. Itens
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

## Comandos da skill

A skill roteia por intenção, no modelo da skill `impeccable` de frontend: uma
preparação obrigatória (contexto e escala), leis e recusas que valem em todo
trabalho, e vinte e três sub-comandos em seis categorias, cada um com uma
referência própria em [`commands/`](commands/README.md) que a skill carrega antes
de agir. `$game-dev` sem argumento mostra o menu; `$game-dev critique <jogo>` carrega
`commands/critique.md` e segue o fluxo dele; texto livre cai no comando mais
próximo pela situação.

| Categoria | Comandos |
| --- | --- |
| Construir | `craft`, `shape`, `teach`, `document`, `init` |
| Avaliar | `critique`, `audit`, `playtest` |
| Refinar | `polish`, `feel`, `audio`, `harden`, `onboard`, `distill` |
| Ampliar | `juice`, `visual`, `content` |
| Corrigir | `adapt`, `optimize`, `clarify` |
| Produzir | `next`, `produce`, `release` |

O catálogo é [`commands/commands.json`](commands/commands.json): categoria,
descrição, dica de argumentos, focos e leituras canônicas de cada comando. Três
comandos do harness o servem:

```sh
python3 scripts/game.py commands --root /caminho/do/laboratorio
python3 scripts/game.py pin critique --root /caminho/do/laboratorio
python3 scripts/game.py unpin critique --root /caminho/do/laboratorio
```

`commands` imprime o catálogo em JSON, com o caminho de cada referência e se ela
existe. `pin` cria um atalho próprio do host (`/critique` passa a invocar
`$game-dev critique`) em cada diretório de skills onde a `game-dev` já está
instalada; o arquivo leva um marcador, e uma skill sua com o mesmo nome nunca é
sobrescrita. `pin` não copia a skill. Se o README recusa que o pin copie a skill, o `created` do `pin` nomeia a cópia que o README já recusa. Atalho no disco não é a skill. Sem chave `cópia`. Se o processo recusa que a neutralidade de interface prove substitutibilidade, o `created` do `pin` nomeia a substitutibilidade que o processo já recusa. Neutralidade no disco não é a skill. Sem chave `substitutibilidade`. Se o README recusa sobrescrever skill sua com o mesmo nome, o `pin` nomeia a própria que o README já recusa. Atalho no disco não é a skill. Sem chave `própria`. `unpin` remove só o que tem o marcador. Se o README recusa que o unpin remova o que não tem o marcador, o `skipped` do `pin` nomeia o marcador que o README já recusa. Skill no disco não é o atalho. Sem chave `marcador`. `doctor` ganhou a checagem
`commands`: catálogo, arquivo de referência e linha na tabela do `SKILL.md`
precisam concordar, senão o menu manda o agente ler um arquivo que não existe. Se o menu recusa invocar sem carregar a referência, o `commands` nomeia o genérico que o menu já recusa. Linha no disco não é a skill. Sem chave `genérico`. arquivo presente não é a referência carregada. Se o menu recusa que o arquivo presente seja a referência carregada, o `reference_present` do `commands` nomeia a carregada que o menu já recusa. Arquivo no disco não é a skill. Sem chave `carregada`.

Uma referência de comando é um orquestrador fino, não uma receita nova: diz qual
`context` rodar, qual receita ler, onde parar para o usuário, o que prova conclusão
e o que não fazer ([contrato](commands/README.md)). Se o README recusa que a referência de comando seja uma receita nova, o `created` do `pin` nomeia o orquestrador que o README já recusa. Atalho no disco não é a receita. Sem chave `orquestrador`. As receitas continuam sendo
selecionadas por `--focus`; o comando acrescenta o fluxo.

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

A **escala** de ambição (`jam`, `product`, `aa`) é o "register" da skill: governa
quantidade de artefatos e de conteúdo, nunca o piso do verbo. Se a receita recusa que o piso do verbo seja opcional, o `scale` nomeia o opcional que a receita já recusa. Escala no disco não é o piso. Sem chave `opcional`. `context` a devolve
em `scale`: `--scale` declarado na conversa vence; sem ele, um campo `Escala:` num
documento do projeto só **sugere**, com arquivo e linha; sem nenhum dos dois, o
campo vem nulo e a skill infere uma vez e pede para gravar no brief. "AAA" escrito
num brief é lido como `aa`, porque é o único sentido que este harness aceita para
a palavra. O comando lê o campo; não classifica o jogo.

O contexto entrega caminhos para leitura, registros já existentes, catálogos de
estudo (se um irmão `Games-Frameworks` existir, ou `GAMES_FRAMEWORKS_ROOT`),
menções locais de pause/reset/seed, `foundation` (nove áreas documentais),
`production_bar` (as dimensões de acabamento pertinentes ao foco), `finish` (perfil
do checklist de piso) e o acervo `shared/sfx` da raiz informada. Não executa o jogo. Se o mapa recusa que o catálogo ouça o starter, o `context` nomeia a escuta que o mapa já recusa. Acervo no disco não é mix ouvida. Sem chave `ouve`. Se o mapa recusa que tocar nessa página seja mix ouvida, o `sfx` do `studio_assets` nomeia o tocar que o mapa já recusa. Página no disco não é o mix. Sem chave `tocar`. Se o mapa recusa que um workspace herde silenciosamente as preferências de outro, o `policy` do `studio_assets` nomeia a herança que o mapa já recusa. Política no disco não é o outro laboratório. Sem chave `herança`. Se o mapa recusa que o catálogo no disco seja o presente, o `exists` do `studio_assets` nomeia o presente que o mapa já recusa. Arquivo no disco não é mix. Sem chave `presente`. Se a guia recusa preencher o checklist, o `context` nomeia o checklist que a guia já recusa preencher. Guia no disco não é observação. Sem chave `checklist`. Se a ambição recusa que o checklist completo seja nota AAA, o `finish` nomeia o grau que a ambição já recusa. Guia no disco não é observação. Sem chave `grau`.
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
gênero — como convenções a confirmar no projeto, não como capacidade certificada. Se o pacote recusa que teste unitário prove o navegador, o `context` nomeia o navegador que o pacote já recusa provar. Pacote no disco não é comportamento no aparelho. Sem chave `navegador`. Se o índice recusa que o pacote certifique capacidade, o `context` nomeia a capacidade que o índice já recusa. Pacote no disco não é comportamento. Sem chave `capacidade`. Se o pacote recusa que métricas RAF comprovem os quadros, a plataforma nomeia os quadros que o pacote já recusa. Callback no disco não é quadro apresentado. Sem chave `quadros`. Se o mapa recusa que o pacote seja extração, o `context` nomeia a extração que o mapa já recusa. Convenção no disco não é repositório executado. Sem chave `extração`. Se o mapa recusa que a menção seja mecânica obrigatória, o `genre_mentions[n]` nomeia a mecânica que o mapa já recusa. Campo no disco não é regra do jogo. Sem chave `mecânica`. Se a receita recusa que o nome seja API, o `context` nomeia a API que a receita já recusa. Vocabulário no disco não é runtime. Sem chave `api`. Se o roteiro recusa que menções locais sejam rastreamento de comportamento, a menção nomeia o rastreamento que o roteiro já recusa. Menção no disco não é o gesto. Sem chave `rastreamento`. Se a barra recusa que o determinismo seja capacidade, o `capabilities` desconhecido nomeia o determinismo que a barra já recusa. Lista no disco não é ciclo demonstrado. Sem chave `determinismo`.
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
as dez tiverem linha, porque dimensão não declarada não é dimensão alta. Se a barra recusa que dimensão não declarada seja dimensão alta, o `undeclared` do `bar` nomeia a alta que a barra já recusa. Linha no disco não é acabamento. Sem chave `alta`. Se a barra recusa que a declaração seja um selo, o `sources` do `bar` nomeia o selo que a barra já recusa. Linha no disco não é acabamento. Sem chave `selo`. Se a barra recusa que o piso seja uma nota, o `floor` do `bar` nomeia a nota que a barra já recusa. Linha no disco não é acabamento. Sem chave `nota`. Se a barra recusa que a tabela otimista seja observação, o `at_floor` do `bar` nomeia a otimista que a barra já recusa. Linha no disco não é acabamento. Sem chave `otimista`. Se o mapa recusa que o checklist seja um score, o `bar` nomeia o score que o mapa já recusa. Mapa no disco não é acabamento. Sem chave `score`. Se a prosa declara o mínimo, o `bar` nomeia o mínimo que a barra já declara. Degrau no disco não é acabamento observado. Sem chave `mínimo`. Se a barra recusa que o degrau seja prazo, o `bar` nomeia os prazos que a barra já recusa. Linha no disco não é calendário. Sem chave `prazos`. Se a barra recusa que o nome seja uma das dez, o `bar` nomeia a dimensão que a barra já recusa. Linha no disco não é acabamento. Sem chave `dimensão`. Se a barra recusa que duas linhas discordantes se resolvam por precedência, o `conflicts[n]` do `bar` nomeia a precedência que a barra já recusa. Linha no disco não é acabamento. Sem chave `precedência`.

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

O projeto declara uma linha por critério, em `README.md` ou num `qa.md`,
`devlog.md`, `release.md` ou `prd.md` em qualquer subpasta de documentação
(o Rabisco Boom guarda o seu em `docs/planning/`; `sources` na saída diz o que foi lido).
Se a tabela declara o gate, o `gate` nomeia o gate que a tabela já declara. Linha no disco não é passagem concedida. Sem chave `gate`. Se o roteiro recusa que o silêncio seja aprovação, o `gate` nomeia o silêncio que o roteiro já recusa. Linha vazia no disco não é passagem. Sem chave `silêncio`. Se o roteiro recusa que a lista de entrega seja um gate, o `sources` do `gate` nomeia a lista que o roteiro já recusa. Linha no disco não é passagem. Sem chave `lista`. Se o roteiro recusa que a declaração seja passed, o `held_by_declaration` do `gate` nomeia o passou que o roteiro já recusa. Tabela no disco não é passagem. Sem chave `passou`. Se o roteiro recusa que must_meet seja dispensável, o `gate` nomeia a dispensa que o roteiro já recusa. Linha no disco não é passagem. Sem chave `dispensa`. Se o roteiro recusa que fora de escopo seja dispensa, o `gate` nomeia o escopo que o roteiro já recusa. Linha no disco não é passagem. Sem chave `escopo`. Se a guia recusa que código que compila prove a hipótese, o `gate` nomeia a hipótese que a guia já recusa. Linha no disco não é o experimento. Sem chave `hipótese`. Se o fluxo recusa que um teste local concluído seja lançamento, o `gate` nomeia o lançamento que o fluxo já recusa. Linha no disco não é outra máquina. Sem chave `lançamento`. Se a receita recusa que a slice sem repeatability esteja pronta para ampliar, o `gate` scale nomeia a repeatability que a receita já recusa. Linha no disco não é o próximo trecho. Sem chave `repeatability`. Se o roteiro recusa que abandonar seja falha do gate, o `gate` nomeia o abandono que o roteiro já recusa. Roteiro no disco não é passagem. Sem chave `abandono`:

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
cumprir, não que alguém conferiu. Se o roteiro recusa que a declaração seja passed, o `held_by_declaration` do `gate` nomeia o passou que o roteiro já recusa. Tabela no disco não é passagem. Sem chave `passou`. **Nenhum comando concede passagem** (`granted`
é sempre `false`), e uma tabela bem formada e otimista sai daí intacta, como sai
da barra.

## Origens

`deliver.licensing` é um dos quatro critérios que a prosa não deixa dispensar, e
até aqui o harness só lia a linha da tabela. Uma frase otimista fechava o gate.
`origins` percorre o disco:

```sh
python3 scripts/game.py origins /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py origins /caminho/do/laboratorio/meu-jogo --declare textures/hero.png --origin "foto própria" --author "Ana" --license CC0-1.0
```

Lista arquivos de mídia embarcados (som, imagem, fonte, vídeo, modelo) e cruza
com recibos: `sources.json`, `licenses.json`, `CREDITS` e sidecar
`.credits.txt`. JSON sem origem, autor e licença não declara. Sidecar sem
os três rótulos também não. Se o sidecar declara `Consumidor:`, o `origins` nomeia o consumidor que o sidecar já declara. Consumidor no disco não é licença válida. Sem chave `consumer`. Se o roteiro recusa que o sidecar sem rótulos declare, o `origins` nomeia os rótulos que o roteiro já recusa. Recibo no disco não é licença. Sem chave `rótulos`. Se o roteiro recusa que o recibo presente seja licença válida, o `receipts` do `origins` nomeia a válida que o roteiro já recusa. Arquivo no disco não é a concessão. Sem chave `válida`. Se a guia recusa que o embarcado sem recibo seja licença conhecida, o `undeclared` do `origins` nomeia a desconhecida que a guia já recusa. Arquivo no disco não é a concessão. Sem chave `desconhecida`. Se o molde recusa que o crédito seja licença válida, o `form` do `origins` nomeia o crédito que o molde já recusa. Arquivo no disco não é a concessão. Sem chave `crédito`. Se o roteiro recusa que o JSON sem os três campos declare, o `fields` do `origins` nomeia os três que o roteiro já recusa. Recibo no disco não é a concessão. Sem chave `três`. Se o roteiro recusa que nomear devolva o arquivo, o `missing` do `origins` nomeia o devolve que o roteiro já recusa. Recibo no disco não é a concessão. Sem chave `devolve`. Se o roteiro recusa que a varredura incompleta seja a concessão, o `truncated` do `origins` nomeia a varredura que o roteiro já recusa. Recorte no disco não é a concessão. Sem chave `varredura`. Se a receita recusa que o conteúdo baixado receba uma licença nova pelo simples reuso, o `embedded` do `origins` nomeia a nova que a receita já recusa. Arquivo no disco não é a concessão. Sem chave `nova`.
Nomeia a mídia que o recibo lista e o disco
perdeu. Nomear não devolve o arquivo. Entra em
`textures/`, `fonts/`, `models/` e `videos/` — pastas
que o `scan` de documentos ignora de propósito. Nomeia `form` e `fields`
(origem, autor, licença). `--declare` escreve o sidecar. Sem `then`.
Se a receita recusa que o recibo comprove a consistência do gerador, o `fields` do `origins --declare` nomeia a consistência que a receita já recusa. Recibo no disco não é o asset. Sem chave `consistência`.
**Não valida a licença.** Não
consulta titular, não interpreta texto jurídico e não distingue licença válida
de inválida. O que falta é recibo de origem; o que o recibo afirma continua
sendo alegação de quem escreveu. Recibo no disco não é licença válida.

`granted` e `validated` são sempre `false`. Se o projeto declara
`deliver.licensing` como `met` e o disco ainda tem arquivo sem recibo, a saída
marca `contradicts_licensing`. `next` aponta `--declare` — ou tirar o
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
este jogo, o que ninguém verificou. Se a tabela declara saída de escopo, o `craft` nomeia a saída de escopo que a tabela já declara. Linha no disco não é ofício observado. Sem chave `out_of_scope`. Se a pesquisa recusa ser escada de acabamento, o `craft` nomeia a escada que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `escada`. Se a pesquisa recusa que o número folclórico seja critério observável, o item do craft nomeia o folclore que a pesquisa já recusa. Folclore no disco não é o critério. Sem chave `folclore`. Se a pesquisa recusa que três métricas com o mesmo nome sejam um critério, o item do craft nomeia as métricas que a pesquisa já recusa. Nome no disco não é a métrica. Sem chave `métricas`. Se a pesquisa recusa que as palestras dêem limiar, o item do craft nomeia o limiar que a pesquisa já recusa. Palestra no disco não é o critério. Sem chave `limiar`. Se a pesquisa recusa que esses valores sejam um padrão, o item do craft nomeia o padrão que a pesquisa já recusa. Valor no disco não é o padrão. Sem chave `padrão`. Se a pesquisa recusa que o pulo bom seja critério, o item do craft nomeia o pulo que a pesquisa já recusa. Frase no disco não é o critério. Sem chave `pulo`. Se a pesquisa recusa que o que não tem critério finja ter, o item do craft nomeia o fingir que a pesquisa já recusa. Lista no disco não é o critério. Sem chave `fingir`. Se a pesquisa recusa que números sem origem sejam citados, o item do craft nomeia os citados que a pesquisa já recusa. Número no disco não é a fonte. Sem chave `citados`. Se a pesquisa recusa que o artigo meça controle de avatar, o item do craft nomeia o avatar que a pesquisa já recusa. Artigo no disco não é o avatar. Sem chave `avatar`. Se a pesquisa recusa que o modelo seja fórmula, o item do craft nomeia a fórmula que a pesquisa já recusa. Classificação no disco não é a fórmula. Sem chave `fórmula`. Se a pesquisa recusa que a constante apague a contradição, o item do craft nomeia a contradição que a pesquisa já recusa. Fonte no disco não é a contradição. Sem chave `contradição`. Se a pesquisa recusa ser um conjunto de gates, o `sources` do `craft` nomeia o conjunto que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `conjunto`. Se a pesquisa recusa que a pendência seja medição em jogo, o `pending` do `craft` nomeia a medição que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `medição`. Se a pesquisa recusa que o número sem definição seja critério, o `craft` nomeia a definição que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `definição`. Se o mapa recusa que o número com casa decimal e sem origem seja mais preciso, o `craft` nomeia o preciso que o mapa já recusa. Mapa no disco não é ofício observado. Sem chave `preciso`. Se o craft recusa que shape confirmado seja licença para pular feel e áudio, o `craft` nomeia o pular que o craft já recusa. Confirmação no disco não é o ofício. Sem chave `pular`. Se o craft recusa que uma confirmação autorize delegar, o `craft` nomeia o delegar que o craft já recusa. Confirmação no disco não é delegar. Sem chave `delegar`. `observed` e `granted` são sempre `false`.
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
entidades; evento, telegraph e o gerador da chuva também reusam. Também tem `npm run budget` para o orçamento das cenas `title.attract` e `playing.run` (mostra da porta e partida + draw num
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
sem esperar um segundo pedido**. Se o roteiro recusa que o scanner comece a auditoria, o `required` do `audit` nomeia o começo que o roteiro já recusa. JSON no disco não é o levantamento. Sem chave `começo`. Restrição explícita na conversa continua valendo.
Exceção: ciclo fresco que já abre (`audit.deferred`) — o `next` pede jogar
primeiro; o `context` não manda preencher template. Lacuna de rascunho depois do start não é auditoria neste turno. Se o roteiro recusa que a lacuna de rascunho seja auditoria neste turno, o `deferred` do `audit` nomeia a auditoria que o roteiro já recusa. Sinal no disco não é o levantamento. Sem chave `auditoria`. `--event direction-approved`
e `--stage audit` continuam pedindo a base. O scanner não executa a auditoria
(`audit.executed: false`). Se o roteiro recusa que executed falso seja uma instrução para parar, o `audit` nomeia o parar que o roteiro já recusa. Roteiro no disco não é espera. Sem chave `parar`. Se o README aponta o serve, o `scan` nomeia o serve que o README já aponta. Página no disco não é partida jogada. Sem chave `serve`. Se o roteiro recusa que a pasta references seja descartada, o `scan` nomeia a descartada que o roteiro já recusa. Roteiro no disco não é inventário. Sem chave `descartada`. Se o sistema recusa que o scanner certifique tokens, o `scan` nomeia os tokens que o sistema já recusa. Documento no disco não é aprovação artística. Sem chave `tokens`. Se o visual recusa que salvar a imagem seja o trabalho, a área `art_direction` do `scan` nomeia a imagem que o visual já recusa. Imagem no disco não é a aprovação. Sem chave `imagem`. Se o roteiro recusa que o recibo presente seja licença válida, o `scan` nomeia a licença que o roteiro já recusa. Área no disco não é concessão. Sem chave `licença`. Se o release recusa que localização atribua autoria, a área `provenance` do `scan` nomeia a localização que o release já recusa. Localização no disco não é o titular. Sem chave `localização`. Se o roteiro recusa prescrever quantas pessoas, o `scan` nomeia as pessoas que o roteiro já recusa. Área no disco não é censo. Sem chave `pessoas`. Se a guia recusa que o checklist seja uma décima área, a área `qa` do `scan` nomeia a décima que a guia já recusa. Área no disco não é o inventário. Sem chave `décima`. Se a receita recusa que telemetria seja padrão silencioso, o `scan` nomeia a telemetria que a receita já recusa. Área no disco não é consentimento. Sem chave `telemetria`. Se o processo recusa que servidor aberto conclua inicialização documental, a área `runbook` do `scan` nomeia a inicialização que o processo já recusa. Servidor no disco não é o documento. Sem chave `inicialização`. Se a receita recusa promover histórico a regra vigente, o `scan` nomeia o histórico que a receita já recusa. Área no disco não é decisão atual. Sem chave `histórico`. Se o mapa recusa que alegar eficácia comprovada seja evidência, a área `decisions` do `scan` nomeia a eficácia que o mapa já recusa. Mapa no disco não é o ensaio. Sem chave `eficácia`. Se a guia recusa que divertido isoladamente baste, o `scan` nomeia o divertido que a guia já recusa. Área no disco não é o verbo. Sem chave `divertido`. Se o craft recusa que contexto do projeto seja brief da tarefa, a área `gdd` do `scan` nomeia o brief que o craft já recusa. Contexto no disco não é o brief. Sem chave `brief`. Se a guia recusa pontuação universal de diversão, o `scan` nomeia a pontuação que a guia já recusa. Área no disco não é experiência. Sem chave `pontuação`. Se a guia recusa que a ferramenta de raciocínio seja documento obrigatório, a área `mda` do `scan` nomeia o obrigatório que a guia já recusa. Ferramenta no disco não é a obrigação. Sem chave `obrigatório`. Se a guia recusa inventar público observado, o `scan` nomeia o público que a guia já recusa. Área no disco não é audiência. Sem chave `público`. Se o shape recusa que documento preenchido seja PoC executada, a área `vision` do `scan` nomeia a executada que o shape já recusa. Documento no disco não é o experimento. Sem chave `executada`. Se a ambição recusa AAA como adjetivo de marketing, o `scan` nomeia o marketing que a ambição já recusa. Campo no disco não é campanha. Sem chave `marketing`. Se o roteiro recusa que reconstruir documentos comprove intenções, o `scan` nomeia as intenções que o roteiro já recusa. Candidato no disco não é autoria. Sem chave `intenções`. Se o roteiro pede documentar sem consentimento, o `context` nomeia o audit que o roteiro já pede. Roteiro no disco não é base escrita. Sem chave `audit`. Se o roteiro recusa que a checagem seja daemon, o `audit` nomeia o daemon que o roteiro já recusa. Roteiro no disco não é interceptação. Sem chave `daemon`. Se o roteiro recusa que o local não percorrido seja inexistente, o `scan` nomeia a inexistência que o roteiro já recusa. Contagem no disco não é inventário. Sem chave `inexistente`. Se o teach recusa que cobertura lexical seja a prova, o `coverage` nomeia o lexical que o teach já recusa. Varredura no disco não é o rastro. Sem chave `lexical`. Se o roteiro recusa que o recorte de estudo tome a prioridade, o `limits` da coverage nomeia a prioridade que o roteiro já recusa. Limite no disco não é a base. Sem chave `prioridade`. Se o mapa recusa que a cobertura desigual seja acidente, o `issues[n]` da coverage nomeia o acidente que o mapa já recusa. Recorte no disco não é falha. Sem chave `acidente`. Se o roteiro recusa que a lista cortada seja a cobertura, o `issues_truncated` da coverage nomeia a falta que o roteiro já recusa. Recorte no disco não é o inventário. Sem chave `falta`. Se a guia recusa que preencher linhas certifique o jogo, o `non_current_documents[n]` nomeia as linhas que a guia já recusa. Documento no disco não é o jogo. Sem chave `linhas`. Se o processo recusa que a etapa certifique o progresso, o `context` nomeia o progresso que o processo já recusa. Contexto no disco não é degrau. Sem chave `progresso`. Se o roteiro recusa que o evento seja inferido do nome de um arquivo, o `context` nomeia o inferido que o roteiro já recusa. Arquivo no disco não é a conversa. Sem chave `inferido`.

Eventos de conversa, interpretados pelo agente — o comando não concede aprovação:

```sh
python3 scripts/game.py context /caminho/do/jogo --focus visual --event direction-approved --root /caminho/do/laboratorio
python3 scripts/game.py context /caminho/do/jogo --focus mechanics --event resume --root /caminho/do/laboratorio
```

`direction-approved` sincroniza a base mínima no mesmo turno. `resume` localiza
fontes de continuidade; o agente resolve o próximo passo. O harness deixa
`next_step: null` e `executed: false`. Se o processo nega que documento pronto seja PoC, o `context` nomeia a PoC que o processo já nega. Fonte no disco não é jogo implementado. Sem chave `process`. Se o processo recusa que sources_found comprove a fila, o `sources[n]` do continuity nomeia a fila que o processo já recusa. Fonte no disco não é backlog. Sem chave `fila`. Se o next recusa que fonte em rascunho seja passo, o `sources[n]` do continuity nomeia o passo que o next já recusa. Rascunho no disco não é o passo. Sem chave `passo`.

Fonte encontrada não é tarefa validada — e fonte em rascunho não é nem passo. Num
projeto recém-criado, as fontes que `scan` lista são os campos de template
("Próxima ação: [...]"), todas com `status: "draft"`; `next` não propõe retomar
nenhuma delas, porque não há nada escrito para retomar. Ele volta a propor quando
alguma fonte deixa de ser rascunho.

## Processo

`context --event initialize` prepara uma análise profunda e documental quando esse
for o pedido ou a convenção do workspace. O evento não cria um jogo nem executa a
auditoria. [Inicialização](references/project-audit.md#inicializar-o-projeto). Se o roteiro recusa que o aviso seja uma pergunta, o `context` nomeia a pergunta que o roteiro já recusa. Aviso no disco não é espera. Sem chave `pergunta`. Se o roteiro recusa que o resultado seja inferido pelo scanner, o `context` nomeia o scanner que o roteiro já recusa. Sinal no disco não é o resultado. Sem chave `scanner`.
`delivery_review` orienta a conferência do pedido, artefato, prova e continuidade. Se a entrega recusa que templates preenchidos comprovem regras, o `context` nomeia as regras que a entrega já recusa. Critério no disco não é a entrega. Sem chave `regras`.
O comando `python3 scripts/game.py gauntlet <projeto> --objective "recorte definido"` prepara um prompt de
continuidade; duração é opcional e preparação não inicia execução. Se o gauntlet recusa que o arquivo de prompts seja a fonte de status, o `context` nomeia a receita que o gauntlet já recusa. Prompt no disco não é o estado. Sem chave `receita`. Se o processo recusa que arquivos encontrados comprovem prontidão, o `prompt` do continuity nomeia a prontidão que o processo já recusa. Arquivo no disco não é o recorte. Sem chave `prontidão`. Se o roteiro recusa que uma lista de PoCs baste, o `prompt` do continuity nomeia os pocs que o roteiro já recusa. Lista no disco não é o prompt. Sem chave `pocs`. Se o gauntlet recusa que horas nulas sejam prazo infinito, o contrato do `gauntlet` nomeia o infinito que o gauntlet já recusa. Contrato no disco não é o orçamento. Sem chave `infinito`. Se o gauntlet recusa que papéis simulados comprovem independência, o contrato do `gauntlet` nomeia a independência que o gauntlet já recusa. Papel no disco não é crítico isolado. Sem chave `independência`.
[Continuidade](references/gauntlet.md) · [Revisão de entrega](references/delivery.md).

[Pré-produção](references/preproduction.md): Game Brief → GDD/MDA ↔ protótipo/PoC
e playtest → PRD/TDD → vertical slice → produção/MVP → QA → release. Orientação de
dependências, não esteira rígida. Um jogo pequeno pode reunir essas decisões em
um documento.

Dez templates do ciclo: brief, mda, gdd, poc, prd, tdd, vertical-slice, mvp, qa,
release. Quatro complementos: `art-bible`, `devlog`, `audit`, `aaa` (checklist de piso;
o `context` expõe `finish` — núcleo / produto / promessa / mercado; slice, QA, create,
feel e audio carregam a guia; `template aaa` não certifica). Três de consolidação e
produção: `game-design` (documento único), `production-plan`, `milestone`.
O complemento `agents` gera a memória persistente em `AGENTS.md` a partir do disco: o comando que abre, o `note`, o `playtest` e o que ainda não foi plantado. Sem rascunhos do ciclo, não lista GDD. O `playtest` só lê. Sem os quatro não é achado. Nomear o leitor não observa. O `start` já escreve o mesmo arquivo; `template agents` e o `next` em `agent_context.not_located` não voltam ao molde que fingia brief. Se a memória recusa o adjetivo, o `scan` nomeia o AAA que a memória já recusa. Memória no disco não é acabamento. Sem chave `agents`.

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
concede autorização de publicação. Se o molde recusa publicar, o `template` nomeia a publicação que o molde já recusa. Molde no disco não é autorização. Sem chave `publicar`. Se a guia recusa que o MVP prove a hipótese de valor, o `template` nomeia o valor que a guia já recusa. Molde no disco não é validação. Sem chave `valor`. Se a guia recusa que placeholders certifiquem o acabamento, o `template` nomeia o acabamento que a guia já recusa. Molde no disco não é a fatia. Sem chave `acabamento`. Se a guia recusa que o checklist seja um ciclo paralelo, o `template` nomeia o paralelo que a guia já recusa. Guia no disco não é o molde. Sem chave `paralelo`.

**REUSE → ADAPT → CREATE.** CREATE só entra com lacuna explícita.
O [contrato JSON](assets/work.example.json) formaliza uma decisão nova;
`check-plan` valida a forma, não o mérito. Se o processo recusa garantir o mérito, o `check-plan` nomeia o mérito que o processo já recusa. Forma no disco não é adequação. Sem chave `mérito`. Se o processo recusa que três nomes parecidos bastem, o `check-plan` nomeia os nomes que o processo já recusa. Nome no disco não é a camada. Sem chave `nomes`. Se o processo recusa que o contrato válido garanta obediência, o `contract_valid` do `check-plan` nomeia a obediência que o processo já recusa. Forma no disco não é o processo. Sem chave `obediência`. Se a guia recusa que a checagem seja validador semântico, o `metadata_issues[n]` nomeia o semântico que a guia já recusa. Parse no disco não é o jogo. Sem chave `semântico`. O arquivo de exemplo é um formulário em
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
receita de arquitetura. Se a receita recusa que o harness infira dependências, o `scan` nomeia as dependências que a receita já recusa. Receita no disco não é decisão. Sem chave `dependências`. Se a receita recusa que exemplares locais comprovem comportamento multiplayer, o `scan` nomeia o multiplayer que a receita já recusa. Receita no disco não é sessão real. Sem chave `multiplayer`. Se a receita recusa que a estimativa implícita seja discutível, a área `architecture` do `scan` nomeia a estimativa que a receita já recusa. Receita no disco não é decisão. Sem chave `estimativa`. Se a receita recusa que contexto carregado prove a arquitetura compreendida, o candidato da arquitetura nomeia a compreendida que a receita já recusa. Candidato no disco não é a decisão. Sem chave `compreendida`. `--focus feel` e `--focus audio` carregam acabamento do verbo;
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
barramento de música; no `over` ela solta com fade. `roles` lê a declaração — inclusive o `duckMs` que a tabela já lista — e cruza com
arquivos em `public/sfx` (e equivalentes). Sem duck a chave some. Nomear não é mix ouvida. Se o `tools/mix.*` soma as vozes, o `roles` nomeia a soma. Soma no disco não é mix ouvida. Sem chave `mix`. Se o `tools/design-sfx.*` desloca a voz, o `roles` nomeia a voz que o sfx já desloca. Arquivo no disco não é mix ouvida. Sem chave `sfx`. Se o `tools/wav.*` lê o PCM, o `roles` nomeia o PCM que o wav já lê. Bytes no disco não são mix ouvida. Sem chave `wav`. Se a receita recusa que o heap JavaScript sozinho meça PCM ou VRAM, o `roles` nomeia o heap que a receita já recusa. Contador no disco não é o mix. Sem chave `heap`. Se a receita recusa que o arquivo ausente seja silêncio deliberado, o `empty` do `roles` nomeia o ausente que a receita já recusa. Lista no disco não é mix. Sem chave `ausente`. Se a receita recusa que o catálogo completo entre, o `catalog_exists` do `roles` nomeia o entra que a receita já recusa. Acervo no disco não é mix. Sem chave `entra`. Se a receita recusa que desconectar, liberar e fechar comprovem coleta imediata, o `sources` do `roles` nomeia a imediata que a receita já recusa. Sinal no disco não é o sistema. Sem chave `imediata`. Se a receita recusa que áudio AAA seja quantidade de arquivos, o `roles` nomeia a quantidade que a receita já recusa. Lista no disco não é mix. Sem chave `quantidade`. Se a receita recusa que o número no panner seja mix, o papel do x do campo nomeia o panner que a receita já recusa. Número no disco não é mix. Sem chave `panner`. Se a receita recusa que retomar, fila e paralelo sejam mix, o `roles` nomeia o retomar que a receita já recusa. Pedido no disco não é mix. Sem chave `retomar`. Papel vazio continua lacuna:

```sh
python3 scripts/game.py roles /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py roles /caminho/do/laboratorio/meu-jogo --fill
python3 scripts/game.py roles /caminho/do/laboratorio/meu-jogo --fill --apply --root /caminho/do/laboratorio
```

`heard` e `approved` são sempre `false`: arquivo presente não é mixagem ouvida.
`next` propõe `audio.roles` quando um papel está vazio. Se o processo recusa o reuso automático, o `roles --fill` nomeia o reuso que o processo já recusa. Arquivo no disco não é licença. Sem chave `reuso`. `roles --fill` sugere
um id do acervo ou a ficha do stem do starter; `--apply` copia o id do
acervo ou o stem do starter para `public/sfx/<papel>` com recibo —
e recoloca o WAV se o recibo já está e origem e licença casam.
`--apply` não é mix ouvido. Se a receita recusa que o apply seja mix ouvido, o `applied` do `roles --fill` nomeia o aplica que a receita já recusa. Cópia no disco não é mix. Sem chave `aplica`.
`sfx copy` continua o caminho explícito. Copiar não é ouvir.
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

Sem esse acervo, `sfx search` não inventa id: o catálogo vem vazio e a
busca nomeia o stem do starter que casa com o termo. Se o `tools/design-sfx.*` desloca a voz, o `sfx search` nomeia o deslocamento que o sfx já oferece. Arquivo no disco não é mix ouvida. Sem chave `sfx`. Se a receita recusa que o acervo compartilhado seja o primeiro ciclo, o `local` do `sfx search` nomeia o adapt que a receita já recusa. Stem no disco não é mix. Sem chave `adapt`. Se a barra recusa que triagem documental/técnica seja aprovação artística, o `matches` do `sfx search` nomeia a triagem que a barra já recusa. Ficha no disco não é mix. Sem chave `triagem`. `sfx info`
lê a chave e nomeia o stem que o recibo lista e o disco perdeu.
`sfx copy` e `sfx export` levam bytes e créditos
desse stem. Se o sidecar declara licença, o `sfx copy` nomeia os créditos que o copy já leva. Créditos no disco não são mix ouvida. Sem chave `sidecar`. Se a receita recusa que importar e exportar seja ouvir, o `sfx copy` do acervo nomeia o ouvir que a receita já recusa. Cópia no disco não é mix. Sem chave `ouvir`. Se a receita recusa que o arquivo importado esteja sendo consumido, o `record` do `sfx copy` do acervo nomeia o consumido que a receita já recusa. Recibo no disco não é mix. Sem chave `consumido`. `sfx export` nomeia o stem que o recibo lista
e o disco perdeu — exportar não inventa bytes. Se a receita recusa que o export invente bytes, o `sfx export` do stem nomeia a invenção que a receita já recusa. Cópia no disco não é mix. Sem chave `invenção`.
`sfx verify` nomeia os stems sem cruzar o que não
existe e nomeia o stem que o recibo lista e o disco perdeu. Se o check cruza a integridade, o `sfx verify` nomeia a integridade que o check já cruza. Hash no disco não é mix ouvida. Sem chave `sha256`. Se a receita recusa que o ok do catálogo seja ouvido, o `ok` do `sfx verify` nomeia o ouvido que a receita já recusa. Cruzou no disco não é o jogo. Sem chave `ouvido`. Se a receita recusa que variante ausente seja lacuna, o `sfx verify` vazio nomeia a lacuna que a receita já recusa. Lista no disco não é mix. Sem chave `lacuna`. Se a receita recusa que nomear o 404 seja mix, o `missing` do `sfx verify` nomeia o 404 que a receita já recusa. Lista no disco não é mix. Sem chave `404`.
`sfx summary` lista todos. Se a receita recusa que o acervo vazio seja mix ouvido, o `empty` do `sfx summary` nomeia o acervo que a receita já recusa. Lista no disco não é mix. Sem chave `acervo`. Se a receita recusa que o catálogo vazio seja a busca, o `empty` do `sfx search` nomeia a busca que a receita já recusa. Lista no disco não é mix. Sem chave `busca`. Se o `tools/peak.*` relata o pico do arquivo, o `sfx summary` nomeia o pico que o peak já relata. Relato no disco não é mix ouvida. Sem chave `peak`. Se a receita recusa que a categoria do catálogo seja a camada que o jogo mistura, o `categories[n]` do `sfx summary` nomeia a camada que a receita já recusa. Lista no disco não é mix. Sem chave `camada`. Se a receita recusa que medir alocação com canais em zero seja ouvir, o `quality_bar` do `sfx summary` nomeia a alocação que a receita já recusa. Barra no disco não é mix ouvida. Sem chave `alocação`. Se a receita recusa que o tamanho comprimido meça áudio decodificado, o `local` do `sfx summary` nomeia o comprimido que a receita já recusa. Bytes no disco não são mix. Sem chave `comprimido`. `sfx serve` recusa — não
há o que ouvir no acervo.
Com sons, `sfx serve` abre a página de escuta; se `shared/sfx/ui`
faltar, o harness gera a lista. Tocar nessa página não é mix
ouvida no jogo. Arquivo no disco não é mix ouvido. Crescer o
acervo é arquivo local com recibo:

```sh
python3 scripts/game.py sfx import /caminho/do.wav --metadata /caminho/meta.json --root /caminho/do/laboratorio
python3 scripts/game.py sfx seed --root /caminho/do/laboratorio
python3 scripts/game.py sfx info passo-madeira-01 --root /caminho/do/laboratorio
python3 scripts/game.py sfx export passo-madeira-01 --to /caminho/do/jogo/public/audio --root /caminho/do/laboratorio
```

Se a receita recusa improvisar licença, o `sfx import` nomeia a improvisação que a receita já recusa. Importar no disco não é licença. Sem chave `improvisar`.
`sfx import` exige ffmpeg e um JSON com id, título, categoria, estilo,
tags, processamento e fontes (licença CC0 ou CC-BY). `sfx seed` lê
`shared/sfx/selection.json` com `local_path` já no disco. Sem seleção,
o seed recusa. Se a receita recusa que avaliação do agente seja aprovação do usuário, o `sfx seed` nomeia a aprovação que a receita já recusa. Seed no disco não é mix. Sem chave `aprovação`. `sfx summary` (também sem subcomando) lê o acervo, os atalhos
e os stems do starter em `public/sfx` — arquivo no disco não é mix ouvido.
`sfx verify` cruza bytes e fichas do acervo; sem acervo nomeia os
stems do starter e não cruza. Se o check cruza a integridade, o `sfx verify` nomeia a integridade que o check já cruza. Hash no disco não é mix ouvida. Sem chave `sha256`. Se a receita recusa que o ok do catálogo seja ouvido, o `ok` do `sfx verify` nomeia o ouvido que a receita já recusa. Cruzou no disco não é o jogo. Sem chave `ouvido`. Nomeia o stem que o recibo lista e
o disco perdeu. Nomeia o som que o catálogo lista e o disco
perdeu — não despeja errno. Não ouve. `sfx info` lê a ficha
do acervo ou a chave do stem do starter. O recibo que lista um
stem e o disco perdeu não é id desconhecido. Se o inspect já mediu
o pico, o `sfx info` nomeia o pico que o inspect já mede. Pico no
recibo não é mix ouvida. Se a receita recusa que teste técnico de decode aprove o mix, o `sfx info` do acervo nomeia o decode que a receita já recusa. Ficha no disco não é mix ouvida. Sem chave `decode`. Se a receita recusa que arquivo sem papel seja áudio do jogo, o `sfx info` do stem nomeia o lixo que a receita já recusa. Arquivo no disco não é mix. Sem chave `lixo`. Arquivo no disco não é
mix ouvido. `sfx export` de um id do acervo copia
bytes, `manifest.json` e `CREDITS.txt` para uma pasta fora do acervo. Se o export recusa processamento, o `sfx export` nomeia o processamento que o export já recusa. Bytes no disco não são mix ouvida. Sem chave `processamento`. Se a receita recusa que remontar bytes por hash reduza a memória após decodificar, o `sfx export` do acervo nomeia a memória que a receita já recusa. Hash no disco não é o buffer. Sem chave `memória`.
De uma chave do starter, copia o WAV, o `.credits.txt` e anexa
`sources.json`. O recibo que lista um stem e o disco perdeu
não é id desconhecido; exportar não inventa bytes.
Copiar não é mix ouvido.
Importar e exportar não é mix ouvido. O primeiro ciclo já tem voz
no starter (`public/sfx/<papel>.wav`). `shared/sfx` é ADAPT, não
pré-requisito. Piso: gravação licenciada ou design contemporâneo.
8-bit, chiptune, jsfxr e Kenney arcade não são o padrão. Este
repositório **não inclui** o acervo `shared/sfx` do laboratório.

## Feel

O starter nomeia perdão, graça, hitstop, buffer de guardar, punch de
câmera, rumble e o peso do passo no `CONFIG`. As janelas da chuva (prática, folga, fecho) moram
na mesa. O coil do dash marca o rumo no corpo. Se o laço declara
`attractMove`, o `feel` nomeia o corpo que a porta já desloca.
Pose no disco não é peso percebido. Sem chave `attract`.
Se o laço declara `lookAhead`, o `feel` nomeia a inclinação que o lookAhead já marca.
Lean no disco não é peso percebido. Sem chave `lookAhead`.
Se o `tools/probe.*` exercita as janelas de perdão, o `feel` nomeia o perdão que o probe já exercita.
Conta no disco não é peso percebido. Sem chave `probe`.
Se o laço senta a guarda, o `feel` nomeia o sit que a guarda já senta. Pose no disco não é peso percebido. Sem chave `bank`.
Se o laço emite o término, o `feel` nomeia o land que o dash já emite. Pose no disco não é peso percebido. Sem chave `land`.
Se a receita recusa que o autor sugerido seja quem jogou, o `feel` nomeia o autor que a receita já recusa. Recibo no disco não é sessão. Sem chave `autor`. Se a receita recusa que o texto no DOM seja direção observada, o item da observação nomeia o dom que a receita já recusa. Texto no DOM não é a direção. Sem chave `dom`. Se a receita recusa que o texto no DOM seja sessão, o item da observação nomeia a sessão que a receita já recusa. Texto no DOM não é a sessão. Sem chave `sessão`. Se a receita recusa que o harness jogue com o modo ativo, o item da observação nomeia o ativo que a receita já recusa. Recibo no disco não é o modo. Sem chave `ativo`. Se a receita recusa que o número na faixa seja sessão observada, o item da observação nomeia a contagem que a receita já recusa. Contagem no disco não é a sessão. Sem chave `contagem`. Se a receita recusa que Esc e P existam no polegar, o item da observação nomeia o polegar que a receita já recusa. Tecla no disco não é o polegar. Sem chave `polegar`. Se a receita recusa que a porta e o fim chamem o avanço de cima, o item da observação nomeia o avanço que a receita já recusa. Tap no disco não é o avanço. Sem chave `avanço`. Se a receita recusa que o Espaço avance enquanto a pessoa escolhe, o item da observação nomeia o espaço que a receita já recusa. Tecla no disco não é a escolha. Sem chave `espaço`. Se a receita recusa que o botão focado avance, o item da observação nomeia a casca que a receita já recusa. Casca no disco não é o verbo. Sem chave `casca`. Se a receita recusa que o acesso seja camada final, o item da observação nomeia o final que a receita já recusa. Acesso no disco não é o recorte. Sem chave `final`. Se a receita recusa que tratar depois evite o retrabalho, o item da observação nomeia o retrabalho que a receita já recusa. Conteúdo no disco não é o acesso. Sem chave `retrabalho`. Se a receita recusa que tratar no GDD evite a escolha, o item da observação nomeia a escolha que a receita já recusa. GDD no disco não é a escolha. Sem chave `escolha`.
Se a receita recusa que o valor seja constante universal, o `feel` nomeia o universal que a receita já recusa. Número no disco não é lei. Sem chave `universais`.
Se a receita recusa que velocidade não nula prove a posição, o item da constante nomeia a posição que a receita já recusa. Número no disco não é a pose. Sem chave `posição`.
Se a receita recusa que esses testes demonstrem qualidade artística, o then do `feel` nomeia a artística que a receita já recusa. Número no disco não é direção. Sem chave `artística`. Se a receita recusa que captura no disco seja sessão observada, o `sources` do `feel` nomeia a captura que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `captura`. Se a receita recusa que o soltar no disco seja sessão observada, o `observations` do `feel` nomeia o soltar que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `soltar`. Se a receita recusa que animar demais substitua a regra, o `observations` do `feel` nomeia o animar que a receita já recusa. Animar no disco não é a regra. Sem chave `animar`. Se a receita recusa que a recovery invisível ou infinita seja o retorno, o `observations` do `feel` nomeia o justo que a receita já recusa. Recovery no disco não é o controle. Sem chave `justo`. Se a receita recusa que P e aba escondida comam a aposta, o `observations` do `feel` nomeia a aposta que a receita já recusa. Pausa no disco não é o fim. Sem chave `aposta`. Se a receita recusa que a queda longe coma o verbo em curso, o `observations` do `feel` nomeia a queda que a receita já recusa. Queda no disco não é o ofício. Sem chave `queda`. Se a receita recusa que o segundo estilhaço empilhe impacto, o `observations` do `feel` nomeia o empilha que a receita já recusa. Estilhaço no disco não é a pilha. Sem chave `empilha`. Se a receita recusa que dois orbes inflam a corrente, o `observations` do `feel` nomeia a corrente que a receita já recusa. Orbe no disco não é a corrente. Sem chave `corrente`. Se a receita recusa que coleta, queda e erro compartilhem squash, o `observations` do `feel` nomeia o squash que a receita já recusa. Medida no disco não é o squash. Sem chave `squash`. Se a receita recusa que a coleta acenda o campo, o `observations` do `feel` nomeia o acende que a receita já recusa. Coleta no disco não é o erro. Sem chave `acende`. Se a receita recusa que a recuperação seja a tinta da prática, o `observations` do `feel` nomeia a tinta que a receita já recusa. Silhueta no disco não é a prática. Sem chave `tinta`. Se a receita recusa que esconder o gesto encerre o gesto, o `observations` do `feel` nomeia o gesto que a receita já recusa. Esconder no disco não é o gesto. Sem chave `gesto`. Se a receita recusa que a silhueta parada seja lida, o `observations` do `feel` nomeia a silhueta que a receita já recusa. Pose no disco não é a silhueta. Sem chave `silhueta`.
Constante nomeada não é peso percebido. Se o README recusa que a constante nomeada seja peso percebido, o `constants` do `feel` nomeia o peso que o README já recusa. Número no disco não é o verbo. Sem chave `peso`. Se a receita recusa que o coil seja janela de hit, o `constants` do `feel` nomeia a janela que a receita já recusa. Coil no disco não é a janela. Sem chave `janela`. Se a receita recusa que achar o jogo seja ter sentido, o `unobserved` do `feel` nomeia o sentido que a receita já recusa. Arquivo no disco não é o verbo. Sem chave `sentido`. Se a receita recusa que a guarda seja janela de hit, o `unobserved` do `feel` nomeia a guarda que a receita já recusa. Guarda no disco não é a janela. Sem chave `guarda`. Se a receita recusa que um tween genérico sem dono seja feel reutilizável, o `feel` nomeia o tween que a receita já recusa. Receita no disco não é peso percebido. Sem chave `tween`. Se a receita recusa que guardar no hitstop seja engolido, o `feel` nomeia o engolido que a receita já recusa. Hitstop no disco não é o perdão. Sem chave `engolido`. Se a receita recusa que corrigir a regra substitua o feel, o `feel` nomeia a regra que a receita já recusa. Regra no disco não é o feel. Sem chave `regra`. Se a receita recusa que pose e arquivo no disco sejam peso percebido, o `feel` nomeia a pose que a receita já recusa. Arquivo no disco não é o peso. Sem chave `pose`. Se a receita recusa que o aperto no disco seja peso percebido, o `feel` nomeia o percebido que a receita já recusa. Aperto no disco não é o percebido. Sem chave `percebido`. Se a receita recusa que o pedido decaia no travel, o `feel` nomeia o pedido que a receita já recusa. Pedido no disco não é o land. Sem chave `pedido`. Se a receita recusa que o freeze queime o perdão, o `feel` nomeia o freeze que a receita já recusa. Freeze no disco não é o perdão. Sem chave `freeze`. Se a receita recusa que o sit inflame a aposta, o `feel` nomeia o inflama que a receita já recusa. Sit no disco não é a aposta. Sem chave `inflama`. Se a receita recusa que sentar e pontuar no mesmo impacto matem, o `feel` nomeia o mata que a receita já recusa. Impacto no disco não é a morte. Sem chave `mata`. Se a receita recusa que o relógio coma a guarda que já sentou, o `feel` nomeia o come que a receita já recusa. Relógio no disco não é a guarda. Sem chave `come`. Se a receita recusa que o impacto de coleta pareça golpe mortal, o `feel` nomeia o mortal que a receita já recusa. Coleta no disco não é o golpe. Sem chave `mortal`. Se a receita recusa que o atraso registre um peso, o `feel` nomeia o atraso que a receita já recusa. Atraso no disco não é o peso. Sem chave `atraso`. Se a receita recusa que o feedback gostoso compense a regra injusta, o `feel` nomeia o gostoso que a receita já recusa. Feedback no disco não é a regra. Sem chave `gostoso`. Se a receita recusa que o tempo pareça quebrado, o `feel` nomeia o quebrado que a receita já recusa. Hitstop no disco não é o tempo. Sem chave `quebrado`. Se a receita recusa que a câmera combata o jogador, o `feel` nomeia a câmera que a receita já recusa. Look no disco não é a câmera. Sem chave `câmera`. `feel` lê as
constantes — inclusive o pulso e o passo — essas janelas e o rumo, procura um `record.json` de observação no projeto e nomeia
`then.play` e `then.note` sem executar. Com last-run, nomeia `then.seed`
e `then.invite` — o mesmo endereço que `play` / `guide`. Sem comando de
abrir, a chave some. Sem last-run, seed e invite somem. Não tem
`prompt`. `felt` é sempre falso:

```sh
python3 scripts/game.py feel
python3 scripts/game.py feel /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py note --author "NOME" --note "o que o verbo sentiu"
python3 scripts/game.py note /caminho/do/laboratorio/meu-jogo --author "NOME" --note "o que o verbo sentiu"
# o mapa preenche --author com git ou o ambiente; NOME só se os dois faltarem
```

Sem caminho, o único jogo do laboratório basta; dois pedem o caminho.
`next` e `playtest` usam o mesmo resolvedor. Achar o jogo não é ter
sentido nem assistir.

`note` grava o recibo de observação em `docs/playtest/<utc>/` com cenário e
papel por omissão. `--from-run` anexa `docs/playtest/last-run.json` (resumo
e, se houver, a curva) como candidato de medição e não fecha o achado.
Nomeia `finding` (os quatro no recibo), `form` e `needed`. Sem `then`.
recibo com os quatro não é achado. Se a receita recusa que o recibo com os quatro seja achado, o `finding` do `note` nomeia o achado que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `achado`. Recibo sem os quatro não é achado. Se a receita recusa que o recibo sem os quatro seja achado, o `fields` do `record --kind observation` nomeia a impressão que a receita já recusa. Recibo no disco não é playtest. Sem chave `impressão`. Os quatro no disco não observam. Se o disco tem last-run e o comando veio sem --from-run, o note nomeia o last-run que o disco já guarda. Sem o arquivo a frase some. Nomear não anexa.
Não joga. `felt` é sempre
`false`. `next` propõe `feel.unobserved` quando há constante e não há
recibo; o comando que ele aponta é o mesmo `note` que `then.note` —
com `--from-run` se last-run existir. O harness não atribui peso.

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
uiScale, preset de uma mão (o ciclo nomeia IJKL + P/O quando o starter declara `hand`), assistência, velocidade da partida, tinta estável, região viva e pulso no aparelho. Na porta e no fim o canvas nomeia a lacuna do som que o painel já mostra. Se a casca declara `:focus-visible`, o `access` nomeia o foco que a receita já pede. Outline no disco não é sessão com o teclado. Sem chave `focus`. Se o `tools/contrast.*` amostra o stub, o `access` nomeia o contraste. Stub no disco não é sessão com o modo ativo. Sem chave `contrast`. Se a receita recusa que tamanho CSS igual garanta pixels, o `access` nomeia os pixels que a receita já recusa. Tamanho no disco não é o buffer. Sem chave `pixels`. Se a receita recusa que se declare cobertura não observada, o `missing` do `access` nomeia a cobertura que a receita já recusa. Lista no disco não é sessão. Sem chave `cobertura`. Se a receita recusa que a chave no fonte seja sessão, o `declared` do `access` nomeia a fonte que a receita já recusa. Chave no disco não é o modo ativo. Sem chave `fonte`. Se a receita recusa que a verificação automática substitua uma sessão, o `access` nomeia a automática que a receita já recusa. Checagem no disco não é o modo ativo. Sem chave `automática`. Se o live anuncia o perigo à frente, o `access` nomeia o perigo que o live já anuncia. Texto no DOM não é sessão. Sem chave `threat`. Se o disco declara `paintCommands`, o `access` nomeia as teclas que a tabela já lista. Tabela no disco não é sessão. Sem chave `commands`. Se a porta lê a legenda que o mixer ainda guarda, o `access` nomeia a legenda que a porta já lê. Texto no disco não é sessão. Sem chave `caption`. Se a receita recusa que o número na legenda seja mix, a opção `captions` do `access` nomeia o número que a receita já recusa. Número no disco não é mix. Sem chave `número`. Se a receita recusa que a legenda prove o jogo completável sem áudio, a opção `captions` do `access` nomeia o mudo que a receita já recusa. Texto no disco não é a partida muda. Sem chave `mudo`. Se a receita recusa que o pulso seja sessão no controle, a opção `haptics` do `access` nomeia o controle que a receita já recusa. Pulso no disco não é sessão. Sem chave `controle`. Se a receita recusa que o botão seja sessão, a opção `remap` do `access` nomeia o botão que a receita já recusa. Botão no disco não é sessão. Sem chave `botão`. Se a receita recusa que o movimento reduzido apague a causa, a opção `reduced_motion` do `access` nomeia a causa que a receita já recusa. Causa no disco não é sessão. Sem chave `causa`. Se a receita recusa que o fundo neutro seja o pior caso, a opção `high_contrast` do `access` nomeia o neutro que a receita já recusa. Neutro no disco não é sessão. Sem chave `neutro`. Se a receita recusa que o estado dependa só da cor, a opção `colorblind` do `access` nomeia o ícone que a receita já recusa. Ícone no disco não é sessão. Sem chave `ícone`. Se a receita recusa que completar o jogo peça as duas mãos, a opção `one_hand` do `access` nomeia a mão que a receita já recusa. Mão no disco não é sessão. Sem chave `mão`. Se a receita recusa que a assistência esconda conteúdo, a opção `assist` do `access` nomeia o oculto que a receita já recusa. Oculto no disco não é sessão. Sem chave `oculto`. Se a receita recusa que a precisão fique sem alternativa, a opção `game_speed` do `access` nomeia a precisão que a receita já recusa. Precisão no disco não é sessão. Sem chave `precisão`. Se a receita recusa que a escala substitua a tipografia, a opção `ui_scale` do `access` nomeia a tipografia que a receita já recusa. Tipografia no disco não é sessão. Sem chave `tipografia`. Se a receita recusa que o overlay substitua o leitor, a opção `live` do `access` nomeia o leitor que a receita já recusa. Overlay no disco não é sessão. Sem chave `leitor`. Se a pesquisa recusa que acessibilidade seja gate de certificação, o `access` nomeia a certificação que a pesquisa já recusa. Opção no disco não é certificação. Sem chave `certificação`. Se a receita recusa que opção sem consumidor seja opção, o `access` nomeia a opção que a receita já recusa. Chave no disco não é alcance. Sem chave `opção`. `verified` é sempre `false`. Trocar no stub não é sessão observada. `save` procura
armazenamento, PROGRESS_SCHEMA/migrate e se o disco nomeia sessão volátil
(`persistLine`, `title_volatile`, `title_unsaved`) ou preferências
ilegíveis (`settings_recovered`, `settings.broken`); relata `warned`. Se o
canvas pinta `settingsLine`, o `save` nomeia a recuperação. A pausa não.
Texto no disco não é aba fechada. Sem chave `recovery`. Se o disco
escuta `beforeunload`, o `save` nomeia o fechamento que o disco já grava.
Gancho no disco não é aba fechada. Sem chave `beforeunload`. Se o disco verifica a gravação, o `save` nomeia a gravação que o storage já verifica. Escrita no disco não é aba fechada. Sem chave `storage`. Se a receita recusa que o estágio seja atomicidade, o `save` nomeia a atomicidade que a receita já recusa. Estágio no disco não é substituição. Sem chave `atomicidade`. Se a receita recusa que um único número una a versão do conteúdo e a do save, o `save` nomeia os contratos que a receita já recusa. Schema no disco não é a história. Sem chave `contratos`. Se a receita recusa que o hold sem o número invente ensino feito, o `save` nomeia o ensino que a receita já recusa. Hold no disco não é o ensino. Sem chave `ensino`. Se a receita recusa que o teste de dado inválido prove a interrupção abrupta, o `save` nomeia a interrupção que a receita já recusa. Teste no disco não é a interrupção. Sem chave `interrupção`. Se a receita recusa que o derivado seja o save, o `save` nomeia o derivado que a receita já recusa. Derivado no disco não é o progresso. Sem chave `derivado`. Se a receita recusa que isto seja aba fechada observada, o `save` nomeia a observada que a receita já recusa. Save no disco não é a aba observada. Sem chave `observada`. Se a receita recusa que o flush grave esses eixos, o `save` nomeia os eixos que a receita já recusa. Flush no disco não é o save. Sem chave `eixos`. Se a receita recusa que a outra aba vista o progresso em curso, o `save` nomeia o curso que a receita já recusa. Preferência no disco não é o curso. Sem chave `curso`. Se a receita recusa que o dado transformado volte por reversão, o `save` nomeia a reversão que a receita já recusa. Código no disco não é o save. Sem chave `reversão`. Se a receita recusa que a interrupção no meio deixe um save pela metade, o `save` nomeia a metade que a receita já recusa. Meio no disco não é o save. Sem chave `metade`. Se a receita recusa que dado inválido seja exceção, o `save` nomeia a exceção que a receita já recusa. Dado no disco não é a exceção. Sem chave `exceção`. Se a receita recusa que o estágio seja transação, o `save` nomeia a transação que a receita já recusa. Alvo no disco não é a transação. Sem chave `transação`. Se a receita recusa que o ajuste de estrutura seja a migração, o `save` nomeia o ajuste que a receita já recusa. Formato no disco não é o ajuste. Sem chave `ajuste`. Se a receita recusa que o efêmero seja o save, o `save` nomeia o efêmero que a receita já recusa. Partida no disco não é o efêmero. Sem chave `efêmero`. Se a receita recusa que apagar o save real faça um teste passar, o `used` do `save` nomeia o original que a receita já recusa. Teste no disco não é o save. Sem chave `original`. Se a receita recusa que o índice ou o nome de arquivo preserve o save, o `used` do `save` nomeia o índice que a receita já recusa. Índice no disco não é a entidade. Sem chave `índice`. Se a receita recusa que o harness confirme a escrita, o `used` do `save` nomeia a escrita que a receita já recusa. Uso no disco não é a escrita. Sem chave `escrita`. Se a receita recusa que listar o fonte prove a cadeia inteira, o `sources` do `save` nomeia a cadeia que a receita já recusa. Arquivo no disco não é a migração. Sem chave `cadeia`. Se a receita recusa que o aviso volátil seja aba fechada, o `warnings` do `save` nomeia o volátil que a receita já recusa. Arquivo no disco não é a aba. Sem chave `volátil`. Se a receita recusa que o nomear seja trusted, o `warned` do `save` nomeia a confiança que a receita já recusa. Arquivo no disco não é a aba. Sem chave `confiança`. Se a receita recusa que query no disco seja aba fechada, o `warned` do `save` nomeia a query que a receita já recusa. Endereço no disco não é a aba. Sem chave `query`. Se a receita recusa que o harness abra o save, o `used` do `save` nomeia o abre que a receita já recusa. Texto no disco não é a aba. Sem chave `abre`. Se a receita recusa que ouvir seja aba fechada, o `used` do `save` nomeia a audição que a receita já recusa. Ouvir no disco não é a aba. Sem chave `audição`. Se a receita recusa que o número no disco seja aba fechada, o `used` do `save` nomeia a aba que a receita já recusa. Número no disco não é a aba. Sem chave `aba`. Se a receita recusa que uma versão sem migração preserve o progresso, o `versioned` do `save` nomeia a versão que a receita já recusa. Schema no disco não é a atualização. Sem chave `versão`. Se a receita recusa que o armazenamento sem versão seja o formato, o `unversioned` do `save` nomeia o formato que a receita já recusa. Disco sem schema não é o contrato. Sem chave `formato`. Nomear
não é aba fechada. `trusted` é sempre `false`.
`budget` procura script `budget`/`bench`, `tools/budget.*` ou
`record --kind budget`. Se o tool declara `title.attract`, o
`budget` nomeia a porta que a receita já cronometra. Stub no
disco não é dispositivo. Sem chave `door`. Se o `tools/size.*`
declara sem teto, o `budget` nomeia os bytes que o size já relata.
Bytes no disco não são o quadro medido. Sem chave `size`. Se o
`tools/budget.*` relata o pior percentil, o `budget` nomeia o percentil que a receita já pede. Se a receita recusa que um jogo estável a 30 seja instável, o `budget` nomeia o estável que a receita já recusa. Média no disco não é o quadro. Sem chave `estável`. Se a receita recusa que menos chamadas de desenho garantam menos trabalho total, o `budget` nomeia as chamadas que a receita já recusa. Chamadas no disco não são o trabalho. Sem chave `chamadas`. Se a receita recusa que o aquecimento, o cache e o perfil deixem o resultado intacto, o `budget` nomeia o perfil que a receita já recusa. Perfil no disco não é a medição. Sem chave `perfil`.
Relato no disco não é dispositivo. Sem chave `percentile`.
Se a receita recusa que custos de build, compilação aquecida e serialização sejam FPS, o `files` do `budget` nomeia o fps que a receita já recusa. Custo no disco não é o quadro. Sem chave `fps`. Se a receita recusa que uma melhoria visual seja otimização, o `receipts` do `budget` nomeia a otimização que a receita já recusa. Recibo no disco não é os dois lados. Sem chave `otimização`. Se a receita recusa que a ferramenta de medição deixe o resultado intacto, o `scripts` do `budget` nomeia o resultado que a receita já recusa. Script no disco não é o quadro limpo. Sem chave `resultado`. Se a receita recusa que o harness execute a medição, o `declared` do `budget` nomeia a medida que a receita já recusa. Script no disco não é o quadro. Sem chave `medida`. Se a receita recusa que sem orçamento exista rápido o suficiente, o `expected` do `budget` nomeia o suficiente que a receita já recusa. Pacote no disco não é o quadro. Sem chave `suficiente`. Se a receita recusa que o pacote sem orçamento seja o dispositivo, o `unbudgeted` do `budget` nomeia o dispositivo que a receita já recusa. Manifesto no disco não é o quadro medido. Sem chave `dispositivo`.
`measured` é sempre `false`. O starter declara
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

`art` procura `const PALETTES`, tokens.json, `data/palettes.json`, `docs/art-bible.md` vigente
e mesas de chuva (`intervalTicks` e `fallSpeed` em `data/`, `tables/` ou `content/`).
Se o `tools/new-look.*` nasce o look, o `art` nomeia o look que o disco já nasce.
Ferramenta no disco não é comparação em movimento. Sem chave `look`.
Se o look recusa contraste, o `art` nomeia o contraste que o look já recusa. Alcance no disco não é comparação em movimento. Sem chave `contrast`.
Se o canvas declara `drawTelegraph`, o `art` nomeia o trilho que o telegraph já marca.
Marca no disco não é comparação em movimento. Sem chave `telegraph`.
Se o canvas declara `drawVignette`, o `art` nomeia a vinheta que o recorte já marca.
Recorte no disco não é comparação em movimento. Sem chave `vignette`.
Se o sistema recusa que a paleta compartilhada seja o contrato, o `art` nomeia a paleta que o sistema já recusa. Lista no disco não é contrato. Sem chave `paleta`. Se a receita recusa que importação sem erro comprove aparência equivalente, o `art` nomeia a aparência que a receita já recusa. Importar no disco não é o renderer. Sem chave `aparência`. Se a receita recusa que uma correção local valide o enquadramento, o `art` nomeia o enquadramento que a receita já recusa. Correção no disco não é o conjunto. Sem chave `enquadramento`. Se a receita recusa que câmera próxima e geometria numericamente correta provem leitura, o `art` nomeia a geometria que a receita já recusa. Número no disco não é a silhueta. Sem chave `geometria`. Se a receita recusa que o lean seja punch, o `art` nomeia o punch que a receita já recusa. Lean no disco não é o punch. Sem chave `punch`. Se a receita recusa que a qualidade visual aprovada seja moeda de troca por número, o `manifests` do `art` nomeia a moeda que a receita já recusa. Manifesto no disco não é comparação. Sem chave `moeda`. Se a receita recusa que paleta no código ou em palettes.json seja direção consistente, o `sources` do `art` nomeia a direção que a receita já recusa. Arquivo no disco não é comparação. Sem chave `direção`. Se a receita recusa que o rascunho do init conte, o `bible` do `art` nomeia o rascunho que a receita já recusa. Arquivo no disco não é comparação. Sem chave `rascunho`. Se a receita recusa que o art-bible com marcador de rascunho seja comparação, o `bible_draft` do `art` nomeia o esboço que a receita já recusa. Arquivo no disco não é o quadro. Sem chave `esboço`.
Se a receita recusa que a mesa seja volume, o `art` nomeia o volume que a receita já recusa. Lista no disco não é comparação. Sem chave `volume`. Se a receita recusa que a mesa no disco seja comparação em movimento, o `rains` do `art` nomeia o movimento que a receita já recusa. Mesa no disco não é o quadro. Sem chave `movimento`. Se a receita recusa que isso seja direção consistente, o `bible_current` do `art` nomeia o vigente que a receita já recusa. Arquivo no disco não é comparação. Sem chave `vigente`.
`consistent` é sempre `false`. Mesa no disco não é volume. Rascunho do `init` não conta. `content`
procura dado em `data/`, `levels/` (e equivalentes) ou `.ldtk`/`.tmx`/`.ink`.
`palettes.json` e `tokens.json` não contam — o `art` lê esses manifestos.
Se o disco declara `listMoods`, o `content` nomeia o par. Nome no
disco não é volume. Sem chave `moods`. Se a receita recusa que dusk e calm sejam volume, o `content` nomeia a chuva que a receita já recusa. Chuva no disco não é volume. Sem chave `chuva`.
Se o `tools/new-table.*` nasce a mesa, o `content` nomeia a mesa que o disco já nasce.
Ferramenta no disco não é volume. Sem chave `table`.
Se o disco declara `migrateTable`, o `content` nomeia a migração que as mesas já compartilham.
Arquivo no disco não é volume. Sem chave `migrate`.
Se a receita recusa que mais módulos provem a composição, o `content` nomeia a composição que a receita já recusa. Arquivo no disco não é o mundo. Sem chave `composição`. Se a receita recusa que a variação de material substitua detalhe funcional de forma, o `content` nomeia o material que a receita já recusa. Material no disco não é a forma. Sem chave `material`. Se a receita recusa que o alerta autorize apagar pixels, quantizar cores ou redimensionar, o `content` nomeia o alerta que a receita já recusa. Alerta no disco não é a correção. Sem chave `alerta`. Se a receita recusa que mais resolução mude as dimensões no mundo, o `content` nomeia a resolução que a receita já recusa. Resolução no disco não é a escala. Sem chave `resolução`. Se a receita recusa que o limite de hospedagem exija reduzir quadros, o `content` nomeia a hospedagem que a receita já recusa. Limite no disco não é o corte. Sem chave `hospedagem`. Se a receita recusa que o refinamento estático exija regenerar bancos, o `content` nomeia os bancos que a receita já recusa. Refino no disco não é o banco. Sem chave `bancos`. Se a receita recusa que uma tarefa omitida equivalha a falha, o `content` nomeia a omitida que a receita já recusa. Omissão no disco não é a falha. Sem chave `omitida`. Se a receita recusa que o fornecedor seja obrigatório, o `content` nomeia o fornecedor que a receita já recusa. Menção no disco não é a integração. Sem chave `fornecedor`. Se a receita recusa que a página HTML ocupe o lugar do recurso, o `content` nomeia o html que a receita já recusa. Página no disco não é o recurso. Sem chave `html`. Se a receita recusa que o histórico de HMR isole o vazamento, o `content` nomeia o vazamento que a receita já recusa. Histórico no disco não é o vazamento. Sem chave `vazamento`. Se a receita recusa que a solução seja só do filtro, o `content` nomeia o filtro que a receita já recusa. Filtro no disco não é a emenda. Sem chave `filtro`. Se a receita recusa que o alpha reduzido preserve a opacidade, o `content` nomeia a opacidade que a receita já recusa. Alpha no disco não é a opacidade. Sem chave `opacidade`. Se a receita recusa que escalar o módulo preserve as ferragens, o `content` nomeia as ferragens que a receita já recusa. Módulo no disco não é a ferragem. Sem chave `ferragens`. Se a receita recusa que o tamanho codificado meça custo decodificado ou GPU, o `content` nomeia o codificado que a receita já recusa. Arquivo no disco não é o quadro. Sem chave `codificado`. Se a receita recusa que o arquivo de dados seja volume, o `files` do `content` nomeia os dados que a receita já recusa. Arquivo no disco não é volume. Sem chave `dados`. Se a receita recusa que o baixado seja o consumido, o `external` do `content` nomeia o baixado que a receita já recusa. Arquivo no disco não é o recurso integrado. Sem chave `baixado`. Se a receita recusa que o conteúdo no código escale, o `inline` do `content` nomeia o código que a receita já recusa. Código no disco não é volume. Sem chave `código`.
`enough` é sempre `false`. `ship` procura script `build`/`export`/`package`/
`release`, `docs/release.md` vigente ou CI. Se `dist/VERSION.json`
existe, relata nome e versão. Se `dist/` de um jogo web existe, relata
se a árvore jogável está completa e se o HEAD do artefato é o HEAD
atual. Nomeia a árvore que perdeu o `src/` que o projeto já tem. Se o
`tools/size.*` declara sem teto, o `ship` nomeia o tamanho. Bytes no
disco não são outra máquina. Sem chave `size`. Se o `tools/serve.*`
nomeia a árvore exportada, o `ship` nomeia o banner que o serve já imprime.
Banner no disco não é outra máquina. Sem chave `serve`. Se o
`tools/export.*` declara o empacote, o `ship` nomeia o passo que o export já declara.
Empacotar no disco não é outra máquina. Sem chave `export`. Se o
`tools/export.*` recusa `file://`, o `ship` nomeia o file:// que o export já recusa. Recusar no disco não é outra máquina. Sem chave `file`. Se a receita recusa que a identidade seja outra máquina, o `tree` do ship nomeia a identidade que a receita já recusa. Árvore no disco não é entrega. Sem chave `identidade`. Se a receita recusa que abrir o menu ou obter um ZIP comprove portabilidade, o `tree` do ship nomeia a portabilidade que a receita já recusa. ZIP no disco não é o destino. Sem chave `portabilidade`. Se a receita recusa que o teste no editor demonstre o jogo exportado, o `artifact` do ship nomeia o editor que a receita já recusa. Manifesto no disco não é o jogo exportado. Sem chave `editor`. Se a receita recusa que uma pasta de build existente corresponda à fonte atual, o `artifact` do ship nomeia a atual que a receita já recusa. Manifesto no disco não é o HEAD. Sem chave `atual`. Se a receita recusa que o JSON legível seja outra máquina, o `readable` do artifact do `ship` nomeia o legível que a receita já recusa. Manifesto no disco não é outra máquina. Sem chave `legível`. Se a receita recusa que link não listado comprove controle de acesso, o `ship` nomeia o acesso que a receita já recusa. Link no disco não é outra máquina. Sem chave `acesso`. Se a receita recusa que o tamanho sem teto seja o orçamento de entrega, o `ship` nomeia o teto que a receita já recusa. Relato no disco não é a plataforma alvo. Sem chave `teto`. Se a receita recusa que a CI seja a primeira execução, o `ci` do `ship` nomeia a primeira que a receita já recusa. Fluxo no disco não é instalação limpa. Sem chave `primeira`. Se a receita recusa que emulação e redimensionar uma janela substituam a plataforma real, o `scripts` do `ship` nomeia a emulação que a receita já recusa. Script no disco não é o dispositivo. Sem chave `emulação`. Se a receita recusa que nomear o comando execute, o `artifact_open` do `ship` nomeia a execução que a receita já recusa. Comando no disco não é outra máquina. Sem chave `execução`. Se a receita recusa que compartilhar o convite seja elsewhere, o `release` do `ship` nomeia o compartilhar que a receita já recusa. Arquivo no disco não é outra máquina. Sem chave `compartilhar`. Se a receita recusa que a receita autorize publicar, o `release_current` do `ship` nomeia o autoriza que a receita já recusa. Arquivo no disco não é outra máquina. Sem chave `autoriza`. Se a receita recusa que o ambiente de desenvolvimento seja o artefato, o `expected` do `ship` nomeia o ambiente que a receita já recusa. Pacote no disco não é outra máquina. Sem chave `ambiente`. Se a receita recusa que o pacote sem passo seja o empacote, o `unpacked` do `ship` nomeia o empacote que a receita já recusa. Manifesto no disco não é outra máquina. Sem chave `empacote`. Nomear
não devolve o jogo. `shipped` e `elsewhere` são sempre `false`. Árvore
incompleta recebe `ship.incomplete`; artefato de outro commit recebe
`ship.stale`. Se a receita recusa que o HEAD diferente seja outra máquina, o `stale` do `ship` nomeia o velho que a receita já recusa. Arquivo no disco não é outra máquina. Sem chave `velho`. Se a receita recusa que a árvore sem os quatro seja jogável, o `incomplete` do `ship` nomeia o jogável que a receita já recusa. Arquivo no disco não é outra máquina. Sem chave `jogável`.
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

Observação sem os quatro campos é impressão. Se a receita recusa que o recibo sem os quatro seja achado, o `fields` do `record --kind observation` nomeia a impressão que a receita já recusa. Recibo no disco não é playtest. Sem chave `impressão`. `playtest` lê se o disco tem
problema, evidência, hipótese e medição — num documento ou no próprio
recibo:

```sh
python3 scripts/game.py playtest /caminho/do/laboratorio/meu-jogo
python3 scripts/game.py playtest /caminho/do/laboratorio/meu-jogo --invite
```

`observed` e `outsider` são sempre `false`. `--invite` escreve
`docs/playtest/invite.md` e aponta `href` (`/?invite=1` ou, com seed
no disco, `/?invite=1&seed=<n>`, com chuva nomeada
`&spawn=<mesa>`, com look nomeado `&look=<paleta>`, e com
relógio nomeado e ≠ 1 `&speed=<relógio>`), onde a tabela de
comandos some; depois do fim a página do maker aponta o convite
desta partida se a seed ficou no recibo — copiar o endereço não
grava — e, no convite, mostra seed, pontos, eixos, a curva que o last-run já traçou e se o candidato foi simulado (`nearest-orb` vira `simulada`; `played` some; a faixa não leva a conta nem o relógio) e oferece
os quatro nomes para copiar ou gravar. Se o serve prende o bind, o convite nomeia o bind que o serve já prende. Bind no disco não é alguém de fora. Sem chave `HOST`. Se a receita recusa que o endereço seja duas sessões, o convite nomeia as sessões que a receita já recusa. Convite no disco não é alguém de fora. Sem chave `sessões`. Se a receita recusa que o convite seja preferência, o `invite` do `playtest` nomeia a preferência que a receita já recusa. Convite no disco não é a sessão. Sem chave `preferência`. Se a receita recusa que rolar seja alguém de fora, o convite nomeia o rolar que a receita já recusa. Página no disco não é a sessão. Sem chave `rolar`.
Simulada não é alguém de fora. Depois do fim a página
rola até o painel. Rolar não é alguém de fora. Se a receita recusa que rolar seja alguém de fora, o convite nomeia o rolar que a receita já recusa. Página no disco não é a sessão. Sem chave `rolar`. Número na faixa não
preenche os quatro. Se a receita recusa que o número na faixa preencha os quatro, o `candidate_tally` nomeia o quatro que a receita já recusa. Conta no disco não é achado. Sem chave `quatro`. O achado copiado e gravado leva a faixa
do last-run. Sem tally nem relógio. Markdown no disco não é
alguém de fora. Copiar não grava. O Copiar nomeia o
destino. Gravar já virava Achado no disco; o botão calava.
Nomear não é alguém de fora. Sem a área de
transferência, o Copiar baixa o markdown. Baixar não grava.
Gravado vira
`docs/playtest/<utc>-achado.md` se os quatro tiverem texto.
Se last-run existir, o serve anexa
`docs/playtest/<utc>-achado.run.json`. `playtest` relata esses
anexos em `finding_attachments`. Anexo não é sessão observada. Se a receita recusa que o gravado seja alguém de fora, o `finding_attachments` do `playtest` nomeia o gravado que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `gravado`. Se a receita recusa que nomear o endereço observe, o `created` do `invite` nomeia o endereço que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `endereço`.
Página no disco, texto na área de transferência, markdown
baixado e markdown preenchido não são alguém de fora e não sobem `pacing`.
Esqueleto vazio não é achado. `next` propõe `playtest.invite`
depois do recibo de quem fez (e depois do segundo ciclo, se houver).
`next` propõe `playtest.unstructured` quando há recibo de observação
(ou um `docs/qa.md` vigente) e o achado ainda não tem forma. A
proposta aponta a página (`finding_href` / `finding_open`,
`/?invite=1#finding` ou a url do serve com o convite) e
`note --field`. O comando nomeia o endereço; o serve nu não
abre o painel. Sem o convite o âncora some. `playtest` só lê.
Nomeia `finding_open` (a url do serve com o convite, ou o mesmo
endereço sem serve), `form` (o esqueleto dos quatro nomes) e
`fields`. Sem `then`. Esqueleto no disco
não é achado. Se a receita recusa que o esqueleto no disco seja achado, o `findings` do `playtest` nomeia o esqueleto que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `esqueleto`. Se a receita recusa que os quatro no disco sejam playtest observado, o `structured` do `playtest` nomeia o observado que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `observado`. Se o arquivo `docs/qa.md`
existir, o recibo o nomeia em `qa`. Escrever não é sessão
observada. Se
`docs/playtest/last-run.json` existir, `playtest` o relata
como `candidate` e, se nomear a seed, como `candidate_seed`.
Se nomear a chuva, como `candidate_spawn`. Se a receita recusa que a chuva da outra mesa retome o hold, o `candidate_spawn` nomeia a retoma que a receita já recusa. Mesa no disco não é a sessão. Sem chave `retoma`. Se nomear o look,
como `candidate_look`. Se a receita recusa que o contrast seja look de arte, o `candidate_look` do `playtest` nomeia a arte que a receita já recusa. Paleta no disco não é a sessão. Sem chave `arte`. `?seed=<n>` abre essa partida e ignora
o hold; se o candidato nomeou a chuva ou o look, junta a mesa
e a paleta. O convite usa os mesmos eixos. O `next` aponta
`note --from-run`. A partida no serve grava esse arquivo;
`npm run session` grava a simulação.
Se o `tools/session.*` grava a simulação, o `playtest` nomeia a simulação.
Traço no disco não é alguém de fora. Sem chave `session`.
Se o `tools/serve.*` grava o recado, o `playtest` nomeia o recado que o serve já grava. Texto no disco não é alguém de fora. Sem chave `note`.
Nenhum dos dois é sessão observada. Se a receita recusa que a origem no last-run seja sessão observada, o `candidate_policy` nomeia a origem que a receita já recusa. Texto no disco não é alguém de fora. Sem chave `origem`. Se a receita recusa que simular no relógio cheio observe, o `candidate_speed` nomeia o cheio que a receita já recusa. Número no disco não é alguém de fora. Sem chave `cheio`. Se a receita recusa que o número no disco seja causa, o `candidate_seed` nomeia a atribuição que a receita já recusa. Número no disco não é a sessão. Sem chave `atribuição`. Se a receita recusa que o last-run seja Continuar, o `candidate` do `playtest` nomeia o Continuar que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `continuar`. Se a receita recusa que a simulação seja alguém de fora, o `qa` do `playtest` nomeia a simulada que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `simulada`. Se a receita recusa que o harness assista à sessão, o `qa_current` do `playtest` nomeia o assiste que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `assiste`. Se o molde recusa que a regra de parada seja número de participantes, o `form` do `playtest` nomeia os participantes que o molde já recusa. Arquivo no disco não é a sessão. Sem chave `participantes`. Se o molde recusa que os quatro no disco observem, o `fields` do `playtest` nomeia os campos que o molde já recusa. Arquivo no disco não é a sessão. Sem chave `campos`. Se a receita recusa que o contrast seja look de arte, o `candidate_look` do `playtest` nomeia a arte que a receita já recusa. Paleta no disco não é a sessão. Sem chave `arte`. Se a pesquisa recusa que cinco playtesters sejam critério, o `candidate_tally` nomeia o cinco que a pesquisa já recusa. Conta no disco não é sessão observada. Sem chave `cinco`. Se a receita recusa que o número na faixa preencha os quatro, o `candidate_tally` nomeia o quatro que a receita já recusa. Conta no disco não é achado. Sem chave `quatro`. Se a receita recusa que o aperto seja curva observada, o `candidate_curve` nomeia o aperto que a receita já recusa. Número no disco não é sessão. Sem chave `aperto`. Se a receita recusa que o fecho seja faixa no HUD, o `candidate_curve` nomeia o fecho que a receita já recusa. Fecho no disco não é a faixa. Sem chave `fecho`. Se o candidato
tiver curva, o `note` a anexa. Número no disco não é causa. A tabela de
ofício que *descreve* o formato não conta como
achado. O harness não assiste à sessão e não conta jogadores.

Sem esse acervo, o catálogo vem vazio. A origem e a licença continuam obrigatórias.
Estilos, fornecedores excluídos e piso técnico são [configuração do workspace](references/workspace-binding.md#áudio),
preservando a direção sonora de cada jogo.
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
capacidade, e `claimed` continua não sendo `verified`. Se o processo recusa que claimed seja verified, o `verify` nomeia a verificação que o processo já recusa. Alegação no disco não é cobertura. Sem chave `verified`. Se a receita recusa que o registro declarado prove suporte real, o `capabilities[n]` do `verify` nomeia o suporte que a receita já recusa. Registro no disco não é o consumidor. Sem chave `suporte`.

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
mede e não aprova. Se o roteiro recusa medir os critérios, o `record` nomeia a medição que o roteiro já recusa. Recibo no disco não é observação. Sem chave `mede`. Se a receita recusa que o ganho no caso rejeitado seja ganho equivalente no solver ativo, o `record` nomeia o solver que a receita já recusa. Ganho rejeitado no disco não é o solver. Sem chave `solver`. Se a receita recusa que cenas dinâmicas virem estáticas porque a matriz local ficou igual, o `record` nomeia a matriz que a receita já recusa. Matriz no disco não é a cena. Sem chave `matriz`. Se a receita recusa que o editor seja build exportado, o `record` nomeia o alvo que a receita já recusa. Editor no disco não é o build. Sem chave `alvo`. Se a receita recusa que várias variáveis atribuam a causa, o `record` nomeia a variável que a receita já recusa. Variável no disco não é a causa. Sem chave `variável`. Se a receita recusa que reduzir acabamento para um número seja otimizar, o `record` nomeia o rebaixar que a receita já recusa. Corte no disco não é o mesmo resultado. Sem chave `rebaixar`. Se a receita recusa que a adaptação herde o resultado, o `record` nomeia a contraprova que a receita já recusa. Adaptação no disco não é a contraprova. Sem chave `contraprova`. Se a receita recusa que o subpasso repita eventos de borda, o `record` nomeia o subpasso que a receita já recusa. Subpasso no disco não é o quadro. Sem chave `subpasso`. Se a receita recusa que e orçar só o campo cubra o primeiro quadro, o `record` nomeia o primeiro que a receita já recusa. Campo no disco não é a porta. Sem chave `primeiro`. Se a receita recusa que o FPS médio esconda o problema que importa, o `record` nomeia o médio que a receita já recusa. Média no disco não é o problema. Sem chave `médio`. Se a receita recusa que a falha de gravação apague o registro anterior, o `record` nomeia o registro que a receita já recusa. Falha no disco não é o registro. Sem chave `registro`. Se a receita recusa que a fixture cubra a abertura, o `record` nomeia a fixture que a receita já recusa. Fixture no disco não é o efeito. Sem chave `fixture`. Se a receita recusa que as medidas diferentes sejam a grandeza, o `record` nomeia a grandeza que a receita já recusa. Leitura no disco não é a grandeza. Sem chave `grandeza`. Se a receita recusa que ganho na média demonstre redução de engasgos, o `fields` do `record --kind budget` nomeia os engasgos que a receita já recusa. Número no disco não é o quadro estável. Sem chave `engasgos`. Se a receita recusa que a máquina de desenvolvimento quente seja a máquina do jogador fria, o `fields` do `record --kind budget` nomeia a quente que a receita já recusa. Plataforma no disco não é a máquina fria. Sem chave `quente`. Se a receita recusa que o recibo feche o marco, o `fields` do `record --kind milestone` nomeia o marco que a receita já recusa. Recibo no disco não é a passagem. Sem chave `marco`. Se a receita recusa que o recibo sem os quatro seja achado, o `fields` do `record --kind observation` nomeia a impressão que a receita já recusa. Recibo no disco não é playtest. Sem chave `impressão`. Se o roteiro recusa que o screenshot isolado comprove animação, o `record` nomeia a animação que o roteiro já recusa. Anexo no disco não é controle. Sem chave `animação`. Se a receita recusa que bytes menores provem fidelidade, o `record` nomeia a fidelidade que a receita já recusa. Anexo no disco não é a trajetória. Sem chave `fidelidade`. Se o roteiro recusa que o HEAD substitua o julgamento, o `version` nomeia o julgamento que o roteiro já recusa. Identidade no disco não é avaliação. Sem chave `julgamento`. `role=agent` é avaliação do agente, não aprovação do usuário.

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
interesse a alguém — acabamento é condição necessária, não suficiente. Se a barra recusa promover o degrau, o `context` nomeia a promoção que a barra já recusa. Guia no disco não é acabamento. Sem chave `promove`. Se a receita recusa que AAA seja orçamento ou tamanho de equipe, o `production_bar` nomeia a equipe que a receita já recusa. Receita no disco não é acabamento. Sem chave `equipe`. Se a barra recusa que o degrau sem condição seja observação, o `dimensions[n]` do `production_bar` nomeia a opinião que a barra já recusa. Linha no disco não é acabamento. Sem chave `opinião`. Se o onboard recusa que tempo de sessão seja interesse, o `dimensions[pacing]` do `production_bar` nomeia o interesse que o onboard já recusa. Relógio no disco não é o interesse. Sem chave `interesse`.

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
