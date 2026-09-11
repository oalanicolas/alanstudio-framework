---
name: game-dev
description: Criar, evoluir, depurar, produzir e verificar jogos com IA, partindo do acervo existente, até o acabamento pretendido.
---

# Game Dev

Use este processo em qualquer engine. O objetivo é uma experiência jogável no
**acabamento pretendido**, com evidência, preservando a direção do usuário e a
qualidade aprovada — fácil de começar, difícil de rebaixar. “AAA” neste framework é
piso de acabamento observável (verbo, feel sincronizado, áudio, pacing, mundo, receita
repetível), não tier de publisher, orçamento nem adjetivo de trailer; o alvo honesto
com IA é AA / Triple-I nesse piso. Todos os comandos abaixo são
`python3 scripts/game.py ...` a partir deste repositório (ou pelo caminho absoluto do
script), com `--root <laboratorio>` antes ou depois do subcomando.

## Caminho rápido

| Situação | Faça |
| --- | --- |
| Primeira vez ou raiz em dúvida | `doctor --root <lab>`; corrija itens `missing`. Ele nomeia os projetos e lista os starters. Se o package pede Node, o `doctor` nomeia o engines que o package já declara. Pedido no disco não é binário no PATH. Sem chave `engines`. Nomear não instala. Se o manifesto declara as trocas, o `doctor` nomeia as substituições que o manifesto já declara. Manifesto no disco não é projeto criado. Sem chave `substitutions`. Sem jogo e com starter, `then.guide` aponta o mapa ideia→ciclo com `--idea` — não cria e não executa. Na raiz do framework, `guide` sem `--idea` recusa com o mesmo `sem destino` do `start` — não devolve `start '<destino>'`. A recusa nomeia o `start --idea` que o README já imprime; nomear não cria |
| Laboratório com jogos (o caso normal) | `discover --root <lab>` lê cada jogo e devolve o que os distingue, inclusive os sinais que o `next` usa (primeiro ciclo, ofício, feel sem recibo, achado sem forma, convite, origem sem recibo e lacunas de dimensão); a ordem é a do disco — **não trate a primeira linha como prioridade**. Se o package declara os scripts, o `discover` nomeia os scripts que o package já declara. Lista no disco não é passo executado. Sem chave `scripts`. Sinal verdadeiro não é partida jogada. Lista de arquivo sem recibo não é licença. Lista de chave ausente não é alcance observado |
| Perdeu o comando que abre | `play` (ou `open`) aponta o serve e a superfície (`url`, padrão `http://localhost:8080/`) sem executar. Sem caminho, o único jogo do laboratório basta; dois pedem o caminho. Se o serve recusa produção, o `play` nomeia a produção que o serve já recusa. Serve no disco não é publicação. Sem chave `produção`. Com tela, o avanço abre a porta. Depois da partida a página grava o recibo se você escrever; `note` sem caminho usa o mesmo jogo. `then.note` continua. `executed` fica falso. `runtime` lê o Node do PATH. Nomear o endereço não serve. Não cria |
| Jogo novo | Destino inexistente e engine web: `start --idea "<fantasia>"` (ou `start <novo> --starter <starter> --idea "<fantasia>"`) cria o projeto — sem caminho, a frase nomeia a pasta, ao lado do framework se o start corre de dentro desta árvore —, põe a frase na abertura e no aviso do primeiro ciclo, escreve `AGENTS.md` com o comando que abre, o `note` e o `playtest` (não é GDD; não lista rascunhos que não plantou; o `playtest` só lê; sem os quatro não é achado; nomear o leitor não observa), o prompt nomeia o `playtest` que o `AGENTS.md` já cita (só lê; sem os quatro não é achado; sem `then.playtest`; nomear o leitor não observa), não planta os rascunhos do ciclo (`--docs` os cria) e devolve `open` (= `play`), `url` e `then.note` sem executar. Se o play pede npm, o `package.json` tem dependências e `node_modules` falta, `then.install` nomeia `npm install`. Sem dependências a chave some. Nomear não instala. `open` é o comando de agora; `url` é a superfície pedida; `steps` é o mesmo mapa de três passos do `guide`, com o passo 1 feito. Se o starter declara o verbo e as teclas, o prompt as nomeia — `Fantasia:` à parte de `Verbo:` quando `--idea` ou `copy.json` têm frase; a frase não muda o verbo — inclusive a porta, o cluster de uma mão, o toque, o controle e as queries de look, chuva, par, seed, relógio e convite, se houver. Se o projeto — ou o starter, antes do destino existir — declara as ferramentas, `then` nomeia par, look, chuva e voz; depois de um recibo, o prompt as aponta. Se o disco tem last-run com seed, `then` aponta a partida (número, chuva e look quando o candidato os nomeia) e o convite; nomear o endereço não observa. Vestir a query não grava. A chuva da query não retoma o hold. Na porta e no fim a região viva nomeia a mesa e o look que a chuva já veste — spawn e normal somem. Na porta o telefone vê Jogar: toque sem ter apertado. Depois do tap a porta não chama o avanço de cima. Nomear o ofício não pinta. A frase não muda o verbo. `guide [<novo>] --idea "<fantasia>"` (também sem subcomando: `python3 scripts/game.py --idea "<fantasia>"`) mapeia start → jogar → note. `open` é o comando de agora; `prompt` o nomeia. Sem destino, a frase nomeia a pasta no comando do start — ao lado do framework se o mapa corre de dentro desta árvore; no diretório atual se corre de fora. Não grava a frase nem cria a pasta. Sem destino, se o diretório atual é um jogo fora do framework, o mapa usa esse caminho. `next` só se o ciclo já correu e você não sabe o que falta. Sem `start`: `init` e depois o comando em `play`. Se o package declara o módulo, o `init` nomeia o módulo que o package já declara. Tipo no disco não é runtime instalado. Sem chave `type`. Jogo pequeno em qualquer engine: `template game-design --project <novo> --output <novo>/docs/game-design.md` e `--stage game-design`. Não gere nove templates |
| Em dúvida sobre o próximo passo | `next --focus <foco>` deriva uma proposta do estado no disco; sem caminho, o único jogo do laboratório basta. `executed` fica `false` e a escolha é sua. Se o processo pede uma ação recomendada, o `next` nomeia a ação que o processo já pede. Proposta no disco não é autorização. Sem chave `ação`. |
| O verbo funciona mas não convence | `feel`; se `unobserved`, `note --author … --note "o que o verbo sentiu"`. Sem caminho, o único jogo do laboratório basta. Lê rumble, o peso do passo, as janelas da chuva e o rumo que o coil do dash marca; nomear não é `felt`. Depois `roles` e `context --focus audio` |
| Paleta, conteúdo no código ou jogo só na máquina de quem construiu | `art` / `content` / `ship` <projeto>; `consistent`/`enough`/`shipped` ficam `false` |
| Observou uma partida e só tem uma nota | `playtest`; se `unstructured`, escreva problema, evidência, hipótese e medição. Sem caminho, o único jogo do laboratório basta. Depois do recibo, `playtest --invite` escreve a página e aponta `href` (`/?invite=1` ou, com seed no disco, `/?invite=1&seed=<n>`, com chuva nomeada `&spawn=<mesa>`, com look nomeado `&look=<paleta>`, e com relógio nomeado e ≠ 1 `&speed=<relógio>`), onde a tabela some; depois do fim a página do maker aponta o convite desta partida se a seed ficou no recibo — copiar o endereço não grava; a página também mostra seed, pontos, eixos, a curva que o last-run já traçou e se o candidato foi simulado (`nearest-orb` vira `simulada`; `played` some; a faixa não leva a conta nem o relógio) e oferece os quatro nomes para copiar ou gravar — o achado copiado e gravado leva essa faixa; sem tally nem relógio; markdown no disco não é alguém de fora; depois do fim ela rola até o painel; rolar não é alguém de fora; número na faixa não preenche os quatro; copiar não grava; sem a área de transferência o Copiar baixa o markdown; baixar não grava; gravar anexa o candidato se houver last-run; gravado não é alguém de fora |
| “Está AAA?” ou slice pronta | `context <projeto> --stage vertical-slice` e leia `finish`; só então `template aaa` |
| Mudança em jogo existente | `context <projeto> --focus <foco>`; com gênero definido, `--genre <g>` |
| “continue” / “vamos avançar” | `context <projeto> --focus <foco> --event resume` e leia `continuity.sources`, preservando o foco da tarefa |
| Usuário aprovou uma referência | `context <projeto> --focus <foco> --event direction-approved` e sincronize a base no mesmo turno |
| Recorte já demonstra a experiência | `context <projeto> --focus production --stage production-plan` |
| Revisar um marco (alpha, beta, gold) | `context <projeto> --focus production --stage milestone`; `bar <projeto>` diz o piso declarado e `gate <projeto>` o que ainda não pode passar |
| Registrar observação, orçamento medido ou decisão de marco | `record <projeto> --kind observation\|budget\|milestone --author ... --note ... --field k=v --output <pasta-nova>`. Se o roteiro recusa medir os critérios, o `record` nomeia a medição que o roteiro já recusa. Recibo no disco não é observação. Sem chave `mede`. |

Focos: `create`, `mechanics`, `lifecycle`, `content`, `visual`, `audio`, `feel`,
`network`, `architecture`, `performance`, `accessibility`, `persistence`, `release`,
`production`. Etapas: `brief`, `mda`, `gdd`, `poc`, `prd`, `tdd`, `vertical-slice`,
`mvp`, `qa`, `release`, `art-bible`, `devlog`, `audit`, `aaa`, `game-design`,
`production-plan`, `milestone`, `agents` (memória persistente gerada do disco: o comando que abre e o que não foi plantado; sem rascunhos não lista GDD). Gêneros (`--genre`): `narrative`, `adventure`,
`platformer`, `action-adventure`, `shooter`, `fighting`, `stealth`, `horror`, `racing`,
`sports`, `rhythm`, `turn-based`, `deckbuilder`, `strategy`, `tower-defense`, `puzzle`,
`simulation`, `survival-crafting`, `rpg`, `roguelike`, `multiplayer-competitive`, `idle`,
`casual` — a lista vigente está em `context.packs.genre.available`.

## Passos

1. **Contexto.** Resolva projeto e tarefa; execute `context <projeto> --focus <foco>`.
   Leia os AGENTS aplicáveis, `foundation.read_first`/`records`, os catálogos em
   `studies` e somente as referências em `read_next`. O núcleo é agnóstico;
   `read_next` inclui o [pacote de plataforma](packs/README.md) quando a engine foi
   identificada e o de gênero quando você passou `--genre`. Se `packs.genre.suggested`
   trouxer um gênero lido de documento, confirme com a conversa e repita o `context`
   com `--genre`; pacotes são convenções a confirmar no código, não capacidades. Se o pacote recusa que teste unitário prove o navegador, o `context` nomeia o navegador que o pacote já recusa provar. Pacote no disco não é comportamento no aparelho. Sem chave `navegador`.
   `capabilities.mentioned` aponta
   arquivo local; não prova pause, reset, seed nem determinismo. Confira `basis`,
   `via` e os limites. `context` já executa `scan`: se `foundation.audit.required`
   for verdadeiro, avise as lacunas com `audit.notice` e comece o levantamento conforme
   [auditoria de projeto](references/project-audit.md), sem pedir um segundo
   consentimento; respeite restrição explícita na conversa atual. Se
   `foundation.audit.deferred` for verdadeiro, o destino já abre — jogue
   primeiro; lacuna de rascunho depois do `start` não é auditoria neste
   turno. Se o README aponta o serve, o `scan` nomeia o serve que o README já aponta. Página no disco não é partida jogada. Sem chave `serve`. Se o roteiro pede documentar sem consentimento, o `context` nomeia o audit que o roteiro já pede. Roteiro no disco não é base escrita. Sem chave `audit`. `--event direction-approved` e `--stage audit` continuam
   pedindo a base. Sem projeto
   identificável, não invente um alvo. Em retomada, fonte encontrada não é tarefa
   validada: siga [continuidade e retomada](references/process.md#continuidade-e-retomada). Se o processo nega que documento pronto seja PoC, o `context` nomeia a PoC que o processo já nega. Fonte no disco não é jogo implementado. Sem chave `process`. Se a memória recusa o adjetivo, o `scan` nomeia o AAA que a memória já recusa. Memória no disco não é acabamento. Sem chave `agents`.
2. **Intenção e prontidão.** Defina fantasia, verbo central, plataforma, cenário,
   restrições, a maior incerteza e a prova de conclusão; assuma o resto com registro e
   pergunte só o que impede de jogar. A escala (jam/conto, produto, AA / Triple-I)
   vive no brief e muda a quantidade de documentos, não o piso do verbo
   ([ambição](references/ambition.md)). Leia [processo](references/process.md)
   — com tela, a primeira superfície é a porta; `play` aponta sem executar —
   e [qualidade](references/quality.md). Para criação ou pré-produção, siga
   [o ciclo criativo](references/preproduction.md): Game Brief, MDA/GDD, PoC, PRD/TDD,
   vertical slice, MVP, QA/playtest e release. `--stage <etapa>` carrega só o template
   pertinente; `template <etapa> --project <projeto>` imprime um rascunho. Se o molde recusa publicar, o `template` nomeia a publicação que o molde já recusa. Molde no disco não é autorização. Sem chave `publicar`.
   Reaproveite
   documentos existentes; um jogo pequeno reúne tudo em `game-design`. O design system
   do jogo (`art-bible`) é conteúdo mínimo; o arquivo separado é opcional se outro
   canônico cobrir. Contrato: [design system do jogo](references/game-design-system.md).
   Direção aprovada: `--event direction-approved` e base mínima sincronizada no mesmo
   turno, mesmo com nove candidatos encontrados.
3. **REUSE → ADAPT → CREATE.** Busque no jogo, no acervo e nas fontes pertinentes.
   `doctor` lista os starters disponíveis; começar por um deles é REUSE, escrever um
   loop do zero é CREATE. Se o laboratório tiver `shared/sfx` com sons, use
   `sfx search` antes de baixar. Sem acervo, o starter já fala em
   `public/sfx`; `sfx search` nomeia o stem que casa com o termo. Se o `tools/design-sfx.*` desloca a voz, o `sfx search` nomeia o deslocamento que o sfx já oferece. Arquivo no disco não é mix ouvida. Sem chave `sfx`.
   `sfx info` lê a chave e nomeia o stem que o recibo lista e o
   disco perdeu, `roles --fill` nomeia o mesmo stem,
   `sfx verify` nomeia os stems sem cruzar
   o que não existe e nomeia o stem que o recibo lista e o
   disco perdeu. Se o check cruza a integridade, o `sfx verify` nomeia a integridade que o check já cruza. Hash no disco não é mix ouvida. Sem chave `sha256`. `sfx summary` lista todos. Se o `tools/peak.*` relata o pico do arquivo, o `sfx summary` nomeia o pico que o peak já relata. Relato no disco não é mix ouvida. Sem chave `peak`. `sfx serve`
   recusa catálogo vazio.
   Com sons no acervo, `sfx serve` abre a página de escuta — se
   `shared/sfx/ui` faltar, o harness gera a lista e nomeia o som
   que o catálogo lista e o disco perdeu. `sfx verify`
   nomeia o som que o catálogo lista e o disco perdeu —
   não despeja errno. Tocar nessa
   página não é mix ouvida no jogo. Arquivo no disco não é mix ouvido. Crescer o acervo é
   `sfx import ARQUIVO --metadata JSON` (ffmpeg); `sfx seed` lê
   `selection.json` local. `sfx info ID` lê a ficha do acervo ou a
   chave do stem do starter — o recibo que lista um stem e o
   disco perdeu não é id desconhecido; se o inspect já mediu o pico, o `sfx info` nomeia o pico que o inspect já mede.
   Pico no recibo não é mix ouvida. `sfx export ID
   --to PASTA` copia bytes e créditos do acervo ou do stem —
   o recibo que lista um stem e o disco perdeu não é id
   desconhecido; exportar não inventa bytes. Se o export recusa processamento, o `sfx export` nomeia o processamento que o export já recusa. Bytes no disco não são mix ouvida. Sem chave `processamento`.
   `sfx copy` leva o stem do starter. Importar e exportar não é
   ouvir. Sem 8-bit,
   chiptune, jsfxr ou Kenney arcade como padrão. Leia candidatos e consumidores.
   CREATE exige lacuna explícita. Para trabalho novo sem registro, use
   [o contrato](assets/work.example.json); `check-plan` valida a estrutura, não o mérito.
4. **Arquitetura e fatia jogável.** Ligue intenção/GDD → requisitos/aceite → decisões
   técnicas → tarefas → evidência. Se a mudança afetar responsabilidades, contratos,
   estado/tempo, saves, renderização ou integrações, aplique
   [arquitetura](recipes/architecture.md) (`--focus architecture` ou `--stage tdd`).
   Implemente uma fatia jogável que atravesse regra, apresentação e conteúdo: perceber
   → decidir → agir → consequência → reinício. Em seguida o feel e o áudio **desse**
   verbo (`--focus feel`, `--focus audio`); título e cores novos não demonstram
   experiência nova. Não acrescente um runtime comum, uma hierarquia de agentes ou IA
   por quadro.
5. **Verificar.** Use os validadores existentes e o cenário real. `verify` registra
   comandos explícitos e logs (scripts de `package.json` ou alvos Cargo; outras engines
   por `--command`). Build verde não comprova diversão, arte, reinício, rede, direitos
   de assets nem aprovação humana. O que uma pessoa observou em movimento, uma medição
   de orçamento ou uma decisão de marco entra por `record`, com `role=human` ou
   `role=agent`; avaliação do agente não é aprovação do usuário. Capacidade
   desconhecida permanece desconhecida até ser demonstrada: `context` só sabe dizer
   `mentioned` sobre as oito capacidades conhecidas (pause, reset, seed, observe, act,
   advance, capture, dispose), porque lê arquivos sem executá-los. Quando os testes do
   projeto de fato exercitarem alguma delas, anexe a alegação ao recibo com
   `verify --proves <capacidade>`: sai como `claimed`, com autor, argv e log, nunca
   como verificada; declare só o que os comandos cobrirem. `experience_status`
   continua `not_assessed` até haver observação em movimento.
6. **Comparar, registrar, continuar.** Compare antes/depois em condições equivalentes
   e em movimento quando houver efeito visual. Corrija regressões, registre decisões e
   hipóteses descartadas, cumpra `continuity.before_close` e
   `documentation.before_close`. Não promova scaffold a slice nem slice a jogo
   concluído. Não chame o recorte de AAA — nem de “quase AAA” — se o perfil em
   `finish` (núcleo; produto se a escala pedir; promessas só se o brief as tiver) não
   foi observado; na slice ou em “está AAA?”, leia `finish` e
   [o guia](references/aaa-checklist.md) e grave no canônico — completar linhas não
   certifica e `N/A` exige motivo. Se a guia recusa preencher o checklist, o `context` nomeia o checklist que a guia já recusa preencher. Guia no disco não é observação. Sem chave `checklist`. Não publique nem delegue sem autorização aplicável.
7. **Produzir até o acabamento, pela dimensão mais baixa.** Quando o recorte já
   demonstrou a experiência, siga [produção](recipes/production.md): plano de produção
   com marcos com critérios de evidência (first playable → vertical slice → alpha → beta →
   gold → live), lentes de disciplina, orçamentos medidos na plataforma alvo, pipeline
   de conteúdo e estabilidade. Aplique [feel](recipes/feel.md) ao verbo central. Os
   marcos são o calendário; `context` devolve `production_bar` com as dimensões
   pertinentes ao foco, e o degrau percebido de um jogo é o **mínimo** entre elas, não
   a média — antes de melhorar o que já está alto, procure o que está baixo
   ([barra de acabamento](references/production-bar.md)). Declare em tabela, uma linha
   por dimensão, com degrau atual, seguinte e o critério que falta; `bar <projeto>` lê
   e diz o piso, `next` propõe subir a dimensão pelo nome. Se a prosa declara o mínimo, o `bar` nomeia o mínimo que a barra já declara. Degrau no disco não é acabamento observado. Sem chave `mínimo`. Se a barra recusa promover o degrau, o `context` nomeia a promoção que a barra já recusa. Guia no disco não é acabamento. Sem chave `promove`. Nenhum comando atribui
   degrau; ao declarar um, declare dispositivo, versão, cena e quem observou.
   **A barra descreve, o gate recusa.** [Os dez gates](references/gates.md) formalizam
   as linhas “Pronto para…” do ciclo: ao pedir a próxima permissão, declare uma linha
   por critério com `met`/`unmet`/`waived`/`out_of_scope` e o que sustenta o estado; `gate <projeto>`
   lê. Se a tabela declara o gate, o `gate` nomeia o gate que a tabela já declara. Linha no disco não é passagem concedida. Sem chave `gate`. Critério sem linha é pendente. As três saídas são passar, cortar escopo e
   abandonar — proponha a terceira quando for a honesta. Dispensa exige motivo; quatro
   critérios de `readiness` não se dispensam. `out_of_scope` é o critério que nunca
   incidiu: exige motivo e não entra na conta das dispensas. Três critérios são
   `must_meet` — perguntam se ainda vale o que custa, não se o trabalho está feito;
   pendência neles não se resolve trabalhando mais. Esses três também não se dispensam,
   e os sete recusam saída de escopo. `granted` é sempre falso. Nenhum comando promove marco,
   mede orçamento ou certifica acabamento; a passagem é declarada por pessoa com a
   prova ligada (`record --kind milestone`, recibos de `verify`, `observation` e
   `budget`). Exemplo: [da trilha ao capítulo acabado](examples/era-uma-vez-production.md).
   **`origins <projeto>` lê o disco**, não a tabela: lista mídia embarcada sem
   recibo de origem. Nomeia a mídia que o recibo lista e o disco perdeu.
   Nomear não devolve o arquivo. Nomeia `form` e `fields`. `--declare` escreve
   o sidecar `.credits.txt`. Sem `then`. Não valida licença. Recibo no disco
   não é licença válida. JSON sem origem, autor e licença não declara.
   Sidecar sem os três rótulos também não.
   Se o sidecar declara `Consumidor:`, o `origins` nomeia o consumidor que o sidecar já declara. Consumidor no disco não é licença válida. Sem chave `consumer`.
   Arquivo sem recibo conta como licença
   desconhecida, e `next` aponta `--declare` antes de seguir.
   **`craft <projeto>`** lê checklists de ofício (paleta, perdão, percentil,
   regra de parada) — conformidade com o que o projeto declarou, sem limiar
   importado. Se a tabela declara saída de escopo, o `craft` nomeia a saída de escopo que a tabela já declara. Linha no disco não é ofício observado. Sem chave `out_of_scope`. `observed` é sempre falso. Só levanta o gate que o projeto pediu.
   Depois de um `init` fresco ou de um `start` sem rascunhos, `next` propõe
   **abrir o ciclo** antes de documentar o que falta: o starter já é um jogo que abre. Com tela,
   o avanço abre a porta; no campo o aviso ensina mover, avançar,
   coletar, guardar e o mapa da superfície que falou. No fecho, corrente
   viva pede guardar de novo; pad e toque não voltam. Art-bible vigente.
   O `init` não o reescreve.
   **`guide [<projeto>]`** devolve os três passos ideia→ciclo (start,
   jogar, note) sem executar nenhum. Sem subcomando, o harness é o
   próprio `guide`; `--idea` no mapa (com ou sem o verbo `guide`) só
   entra no comando do start. Sem destino, a frase nomeia a pasta —
   ao lado do framework se o mapa corre de dentro desta árvore.
   Destino existente preenche o comando que abre o jogo e o `kind`
   do passo de jogar. `open` é o comando de agora; `prompt` o nomeia
   e também sai em stderr — o JSON fica no stdout.
   Se o starter declara o verbo, o prompt e o passo 2 o
   nomeiam — `Fantasia:` à parte de `Verbo:` quando há `--idea` ou
   `copy.json`; a frase não muda o verbo — e a porta, se o manifesto a declara; se o manifesto declara o relógio, o `guide` nomeia o relógio que o manifesto já declara. Frase no disco não é partida observada. Sem chave `speed`. `then` nomeia par, look, chuva e voz quando o projeto — ou o
   starter, se o destino ainda não existe — as declara; se declara
   `session`, `then` a aponta e o prompt a nomeia; se o disco tem last-run com seed,
   `then` aponta a partida (número, chuva e look quando o candidato os nomeia) e o convite; nomear o endereço não observa; se o serve tenta abrir o navegador, o prompt nomeia a tentativa; sem o marcador, pede Abrir; nomear não abre; `executed` fica `false`. `runtime` lê o `node` do PATH se o play pede npm ou node. O autor do
   `note` é sugestão do git ou do ambiente, não quem jogou. Nomear o
   ofício não pinta. `next` fica em `then.lost`.
   **`start [<projeto>]`** cria se o destino estiver livre e devolve
   `open` (= `play`) + `then.note` e os mesmos `steps` do `guide`, com
   o passo 1 feito. Se o `tools/new-pair.*` nasce look e chuva, o `start` nomeia o par que o pair já nasce. Ferramenta no disco não é alguém de fora. Sem chave `pair` no recibo. Sem caminho, `--idea` nomeia e cria a pasta —
   ao lado do framework se o start corre de dentro desta árvore.
   `guide --idea` continua só no comando, não no disco. Se o starter declara o verbo e as teclas, o
   prompt as nomeia — inclusive a porta, o cluster de uma mão, o toque, o
   controle e as queries de look, chuva, par, seed, relógio e convite, se o starter as declara. Se o
   projeto declara `pair`/`look`/`table`/`sfx`, `then` as nomeia; se o disco
   tem last-run com seed, `then` aponta a partida e o convite; depois de um
   recibo, o prompt aponta o segundo ciclo. O `prompt` também sai em
   stderr; o JSON fica no stdout. Não executa o jogo. `--idea` entra na
   abertura se houver `data/copy.json`. O `start` não planta os rascunhos;
   `--docs` os cria. O `init` continua plantando e agora devolve o mesmo
   `open`, `url` e `prompt` do ciclo — não executa. A frase na tela não muda o verbo.
   `runtime` lê o `node` do PATH se o play pede npm ou node; sem 20+ o prompt
   avisa. `session` aponta a partida simulada se o manifesto a declara; o
   prompt a nomeia. Não executa e não observa. Nomear não serve.
   Se o serve tenta abrir o navegador, o prompt nomeia a tentativa.
   Sem o marcador, pede Abrir. Nomear não abre.
   **`play [<projeto>]`** (também `open`) aponta o comando que abre o
   jogo. Não executa, não cria e não serve. Sem caminho, usa o
   diretório atual se ele for um jogo fora desta árvore; se o
   laboratório tem um único jogo, esse basta; dois pedem o caminho.
   `open` é o play. Com tela, o avanço abre a porta. Depois de uma
   partida, a página grava o recibo se você escrever; o próximo
   comando do harness continua `note`. O prompt nomeia o `playtest`
   que o `AGENTS.md` já cita. Só lê. Sem os quatro não é achado.
   Sem `then.playtest`. Nomear o leitor não observa. `note`, `next`, `feel` e
   `playtest` sem caminho usam o mesmo resolvedor. Se o disco tem
   last-run com seed, `then` aponta a partida (número, chuva e look
   quando o candidato os nomeia) e o convite; nomear o endereço não
   observa. `executed` fica `false`. `runtime` lê o `node` do PATH se o
   play pede npm ou node; sem 20+ o prompt avisa. `session` aponta a
   partida simulada se o manifesto a declara; o prompt a nomeia. Não
   executa e não observa. Nomear não serve.
   Se o serve tenta abrir o navegador, o prompt nomeia a tentativa.
   Sem o marcador, pede Abrir. Nomear não abre.
   O `prompt` também sai em stderr;
   o JSON fica no stdout.
   **`roles <projeto>`** lê os papéis de áudio que o código declara, o
   `duckMs` que a tabela já lista, e os arquivos que os preenchem.
   Sem duck a chave some. Nomear não é mix ouvida. Se o
   `tools/mix.*` soma as vozes, o `roles` nomeia a soma. Soma no
   disco não é mix ouvida. Sem chave `mix`. Se o `tools/design-sfx.*`
   desloca a voz, o `roles` nomeia a voz que o sfx já desloca.
   Arquivo no disco não é mix ouvida. Sem chave `sfx`. Se o `tools/wav.*` lê o PCM, o `roles` nomeia o PCM que o wav já lê. Bytes no disco não são mix ouvida. Sem chave `wav`. `--fill` sugere o acervo ou a ficha
   do stem do starter; `--apply` copia o id do acervo ou o stem
   do starter com créditos — e recoloca o WAV se o recibo já está
   e origem e licença casam. `sfx copy` continua o caminho explícito. Se o sidecar declara licença, o `sfx copy` nomeia os créditos que o copy já leva. Créditos no disco não são mix ouvida. Sem chave `sidecar`. Crescer o acervo é `sfx import` / `sfx seed`
   (ffmpeg); `sfx info` lê a ficha do acervo ou a chave do stem
   do starter — o recibo que lista um stem e o disco perdeu não
   é id desconhecido; se o inspect já mediu o pico, o `sfx info` nomeia o pico que o inspect já mede.
   Pico no recibo não é mix ouvida.    `sfx verify` nomeia os stems sem cruzar o que não
   existe e nomeia o stem que o recibo lista e o disco perdeu. Se o check cruza a integridade, o `sfx verify` nomeia a integridade que o check já cruza. Hash no disco não é mix ouvida. Sem chave `sha256`.
   `sfx verify` nomeia o som que o catálogo lista e o disco
   perdeu — não despeja errno;
   `sfx export` copia bytes e
   créditos e nomeia o stem que o recibo lista e o disco perdeu —
   exportar não inventa bytes. Se o export recusa processamento, o `sfx export` nomeia o processamento que o export já recusa. Bytes no disco não são mix ouvida. Sem chave `processamento`. Importar e exportar não é ouvir. `heard` é sempre falso. Papel vazio
   entra no `next` como `audio.roles` — o verbo mudo não espera os
   rascunhos.
   **`feel [<projeto>]`** lê constantes de perdão/hitstop/câmera no `CONFIG`,
   o peso do passo (`player.speed`, o avanço),
   as janelas da chuva (`practiceTicks`, `recoveryTicks`, o fecho) — o
   campo já as marca; o comando calava o passo — e o rumo que o
   coil do dash marca no corpo. Se o laço declara `attractMove`, o
   `feel` nomeia o corpo que a porta já desloca. Pose no disco
   não é peso percebido. Sem chave `attract`. Se o laço declara
   `lookAhead`, o `feel` nomeia a inclinação que o lookAhead já marca.
   Lean no disco não é peso percebido. Sem chave `lookAhead`. Se o `tools/probe.*`
   exercita as janelas de perdão, o `feel` nomeia o perdão que o probe já exercita.
   Conta no disco não é peso percebido. Sem chave `probe`. Se o laço senta a guarda, o `feel` nomeia o sit que a guarda já senta. Pose no disco não é peso percebido. Sem chave `bank`. Se o laço emite o término, o `feel` nomeia o land que o dash já emite. Pose no disco não é peso percebido. Sem chave `land`. Traço no disco não é peso percebido. Lê o
   recibo de observação no disco. Nomeia `then.play` e `then.note` sem
   executar. Com last-run, nomeia `then.seed` e `then.invite` — o mesmo
   endereço que `play` / `guide`. Sem comando de abrir, `then.play` some.
   Sem last-run, seed e invite somem. Não tem `prompt`. `felt` é sempre
   falso. Sem recibo, `next` propõe `feel.unobserved` e aponta o mesmo
   `note` que `then.note` — com `--from-run` se last-run existir. Sem
   caminho, o único jogo do laboratório basta.
   **`note [<projeto>]`** grava o recibo curto (cenário e papel por omissão)
   em `docs/playtest/<utc>/`. Sem caminho, o único jogo do laboratório
   basta; dois pedem o caminho. O comando do mapa sugere `--author` a partir
   do git ou do ambiente; não é quem jogou. `--from-run` anexa `docs/playtest/last-run.json`
   (resumo e, se houver, a curva) como candidato de medição e não fecha o
   achado. Nomeia `finding` (os quatro no recibo), `form` e `needed`.
   Sem `then`. Recibo sem os quatro não é achado. Os quatro no disco
   não observam. Se o disco tem last-run e o comando veio sem --from-run, o note nomeia o last-run que o disco já guarda. Sem o arquivo a frase some. Nomear não anexa. Não joga e não sente. Achar o único jogo não é ter sentido.
   **`access` / `save` / `budget`** leem opção de alcance (incluindo
   uiScale, remapeamento das seis ações do teclado na página — a escuta
   come a tecla que escolhe o verbo e o botão focado não dispara o
   ofício —, faixas que nomeiam o percentual vigente, pedido do sistema
   no meio da sessão (desligar o SO não apaga a caixa), preset de
   uma mão (desligar devolve o remap; save antigo não inventa tecla), assistência, velocidade da partida, tinta estável, região viva e pulso no aparelho), versão de save e artefato
   de orçamento. `save` relata `warned` se o disco nomeia sessão volátil
   (`persistLine`, `title_volatile`, `title_unsaved`) ou preferências
   ilegíveis (`settings_recovered`, `settings.broken`). Se o canvas
   pinta `settingsLine`, o `save` nomeia a recuperação. A pausa não.
   Texto no disco não é aba fechada. Sem chave `recovery`. Se o disco
   escuta `beforeunload`, o `save` nomeia o fechamento que o disco já grava.
   Gancho no disco não é aba fechada. Sem chave `beforeunload`. Se o disco verifica a gravação, o `save` nomeia a gravação que o storage já verifica. Escrita no disco não é aba fechada. Sem chave `storage`. A receita
   de persistência e alcance ensina o canvas da porta e do fim; a
   pausa não.    Na porta e no fim o canvas nomeia a lacuna do som
   que o painel já mostra. Se a casca declara `:focus-visible`,
   o `access` nomeia o foco que a receita já pede. Outline no
   disco não é sessão com o teclado. Se o `tools/contrast.*`
   amostra o stub, o `access` nomeia o contraste. Stub no
   disco não é sessão com o modo ativo. Sem chave `contrast`.
   Se o live anuncia o perigo à frente, o `access` nomeia o perigo que o live já anuncia.
   Texto no DOM não é sessão. Sem chave `threat`.
   Se o disco declara `paintCommands`, o `access` nomeia as teclas que a tabela já lista.
   Tabela no disco não é sessão. Sem chave `commands`.
   Se a porta lê a legenda que o mixer ainda guarda, o `access` nomeia a legenda que a porta já lê. Texto no disco não é sessão. Sem chave `caption`.
   Texto no disco não é mix ouvido.
   Nomear não é
   `trusted`. Trocar no stub não é sessão observada.
   Se o `tools/budget.*` declara `title.attract`, o `budget`
   nomeia a porta que a receita já cronometra. Stub no disco
   não é dispositivo. Sem chave `door`. Se o `tools/size.*`
   declara sem teto, o `budget` nomeia os bytes que o size já relata.
   Bytes no disco não são o quadro medido. Sem chave `size`. Se o `tools/budget.*` relata o pior percentil, o `budget` nomeia o percentil que a receita já pede.
   Relato no disco não é dispositivo. Sem chave `percentile`.
   `verified`/`trusted`/`measured` são sempre falsos.
   Falta no disco entra no `next` antes dos rascunhos.
   **`art` / `content` / `ship`** leem paleta ou art-bible vigente, mesas
   de chuva (`intervalTicks` e `fallSpeed` em data/tables/content), conteúdo
   fora do código (`palettes.json` e `tokens.json` não extraem) e passo de empacotar. Se o
   `tools/new-look.*` nasce o look, o `art` nomeia o look que o disco já nasce.
   Ferramenta no disco não é comparação em movimento. Sem chave `look`. Se o look recusa contraste, o `art` nomeia o contraste que o look já recusa. Alcance no disco não é comparação em movimento. Sem chave `contrast`. Se o canvas declara `drawTelegraph`, o `art` nomeia o trilho que o telegraph já marca.
   Marca no disco não é comparação em movimento. Sem chave `telegraph`. Se o canvas declara `drawVignette`, o `art` nomeia a vinheta que o recorte já marca. Recorte no disco não é comparação em movimento. Sem chave `vignette`. Se o disco declara `listMoods`, o `content` nomeia o par. Nome no disco não é volume. Sem chave `moods`. Se o `tools/new-table.*` nasce a mesa, o `content` nomeia a mesa que o disco já nasce. Ferramenta no disco não é volume. Sem chave `table`. Se o disco declara `migrateTable`, o `content` nomeia a migração que as mesas já compartilham. Arquivo no disco não é volume. Sem chave `migrate`. Se `dist/VERSION.json` existe,
   `ship` relata nome e versão. Se `dist/` de um jogo web existe, relata
   árvore e HEAD. `consistent`/`enough`/`shipped`/`elsewhere` são
   sempre falsos. Sem declaração, o `next` nomeia `art.missing`,
   `content.inline` e `ship.unpacked` antes dos rascunhos. Árvore
   incompleta é `ship.incomplete`; artefato de outro commit é `ship.stale`.
   Nomeia a árvore que perdeu o `src/` que o projeto já tem. Se o
   `tools/size.*` declara sem teto, o `ship` nomeia o tamanho. Bytes
   no disco não são outra máquina. Sem chave `size`. Se o
   `tools/serve.*` nomeia a árvore exportada, o `ship` nomeia o banner que o serve já imprime.
   Banner no disco não é outra máquina. Sem chave `serve`. Se o `tools/export.*` declara o empacote, o `ship` nomeia o passo que o export já declara.
   Empacotar no disco não é outra máquina. Sem chave `export`. Se o `tools/export.*` recusa `file://`, o `ship` nomeia o file:// que o export já recusa. Recusar no disco não é outra máquina. Sem chave `file`. Nomear não
   devolve o jogo. Árvore completa no HEAD atual ganha `artifact_open` e o
   `next` nomeia `ship.artifact_open`. Nomear não executa. `elsewhere`
   continua falso.
   **`playtest [<projeto>]`** lê se o achado tem problema, evidência, hipótese
   e medição. Sem caminho, o único jogo do laboratório basta.
   `observed` e `outsider` são sempre falsos. `--invite` escreve
   a página para quem nunca viu o jogo; depois do fim a página mostra
   seed, pontos, eixos, a curva que o last-run já traçou e se o
   candidato foi simulado (`nearest-orb` vira `simulada`; `played`
   some). A faixa não leva a conta nem o relógio. Simulada não é
   alguém de fora. Oferece os quatro nomes para copiar ou gravar.
   Depois do fim a página rola até o painel. Rolar não é alguém de fora.
   Número na faixa não preenche os quatro. O achado copiado e
   gravado leva a faixa do last-run (seed, pontos, eixos e se
   foi simulado). Sem tally nem relógio. Markdown no disco não
   é alguém de fora. Copiar não grava. O
   Copiar nomeia o destino. Gravar já virava Achado no disco;
   o botão calava. Nomear não é alguém de fora. Sem a
   área de transferência, o Copiar baixa o markdown. Gravar anexa
   o candidato se last-run existir. Gravado não é alguém de fora.
   `next` aponta o convite depois do recibo de quem fez. O serve anuncia
   localhost e, se a máquina tiver outro endereço IPv4, a URL da rede —
   compartilhar essa URL não é alguém de fora. Se o serve prende o bind, o convite nomeia o bind que o serve já prende. Bind no disco não é alguém de fora. Sem chave `HOST`.
   A partida no serve grava
   o candidato em `docs/playtest/last-run.json`; a simulação também.
   Se o `tools/session.*` grava a simulação, o `playtest` nomeia a simulação.
   Traço no disco não é alguém de fora. Sem chave `session`.
   Se o `tools/serve.*` grava o recado, o `playtest` nomeia o recado que o serve já grava. Texto no disco não é alguém de fora. Sem chave `note`.
   Se o candidato nomeia a seed, `playtest` relata `candidate_seed`
   e `?seed=` abre essa partida, ignorando o hold. Se nomeia a
   chuva, relata `candidate_spawn`; se nomeia o look, relata
   `candidate_look`; se nomeia a curva, relata `candidate_curve`;
   se nomeia a origem, relata `candidate_policy` (`played` ou
   `nearest-orb`); se nomeia a conta, relata `candidate_tally`
   (pontos, coletas, quedas, erros e guardas). A simulação não
   sobrescreve `played` sem `--force`.
   O convite junta mesa e paleta. Nenhum dos
   dois é sessão observada.    Recibo sem forma entra no
   `next` como `playtest.unstructured`: a proposta aponta a
   página (`/?invite=1#finding` ou a url do serve com o
   convite) e `note --field`. O comando nomeia o endereço;
   o serve nu não abre o painel. Sem o
   convite o âncora some. `playtest` só lê.
   Nomeia `finding_open` (a url do serve com o convite, ou o
   mesmo endereço sem serve), `form` (esqueleto dos quatro) e
   `fields`. Sem `then`. Esqueleto no disco não é achado.

Fontes detalhadas sob demanda: [mapa dos estudos](references/sources.md).
Comandos, limites e adoção: [README](README.md).
