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
| Primeira vez ou raiz em dúvida | `doctor --root <lab>`; corrija itens `missing`. Ele nomeia os projetos e lista os starters |
| Laboratório com jogos (o caso normal) | `discover --root <lab>` lê cada jogo e devolve o que os distingue; a ordem é a do disco — **não trate a primeira linha como prioridade** |
| Jogo novo | Destino inexistente e engine web: `start <novo> --starter <starter> --idea "<fantasia>"` cria o projeto, põe a frase na tela do primeiro ciclo e devolve `play` + `then.note` sem executar. Se o starter declara o verbo e as teclas, o prompt as nomeia — inclusive o cluster de uma mão, o toque, o controle e as queries de look e chuva, se houver. Se o projeto declara as ferramentas, `then` nomeia look, chuva e voz; depois de um recibo, o prompt as aponta. A frase não muda o verbo. `guide [<novo>] --idea "<fantasia>"` (também sem subcomando) mapeia start → jogar → note. Sem destino, se o diretório atual é um jogo fora do framework, o mapa usa esse caminho. `next` só se o ciclo já correu e você não sabe o que falta. Sem `start`: `init` e depois o comando em `play`. Jogo pequeno em qualquer engine: `template game-design --project <novo> --output <novo>/docs/game-design.md` e `--stage game-design`. Não gere nove templates |
| Em dúvida sobre o próximo passo | `next <projeto> --focus <foco>` deriva uma proposta do estado no disco; `executed` fica `false` e a escolha é sua |
| O verbo funciona mas não convence | `feel <projeto>`; se `unobserved`, `note <projeto> --author … --note "o que o verbo sentiu"`. Depois `roles` e `context --focus audio` |
| Paleta, conteúdo no código ou jogo só na máquina de quem construiu | `art` / `content` / `ship` <projeto>; `consistent`/`enough`/`shipped` ficam `false` |
| Observou uma partida e só tem uma nota | `playtest <projeto>`; se `unstructured`, escreva problema, evidência, hipótese e medição. Depois do recibo, `playtest --invite` escreve a página para quem nunca viu o jogo — não é alguém de fora |
| “Está AAA?” ou slice pronta | `context <projeto> --stage vertical-slice` e leia `finish`; só então `template aaa` |
| Mudança em jogo existente | `context <projeto> --focus <foco>`; com gênero definido, `--genre <g>` |
| “continue” / “vamos avançar” | `context <projeto> --focus <foco> --event resume` e leia `continuity.sources`, preservando o foco da tarefa |
| Usuário aprovou uma referência | `context <projeto> --focus <foco> --event direction-approved` e sincronize a base no mesmo turno |
| Recorte já demonstra a experiência | `context <projeto> --focus production --stage production-plan` |
| Revisar um marco (alpha, beta, gold) | `context <projeto> --focus production --stage milestone`; `bar <projeto>` diz o piso declarado e `gate <projeto>` o que ainda não pode passar |
| Registrar observação, orçamento medido ou decisão de marco | `record <projeto> --kind observation\|budget\|milestone --author ... --note ... --field k=v --output <pasta-nova>` |

Focos: `create`, `mechanics`, `lifecycle`, `content`, `visual`, `audio`, `feel`,
`network`, `architecture`, `performance`, `accessibility`, `persistence`, `release`,
`production`. Etapas: `brief`, `mda`, `gdd`, `poc`, `prd`, `tdd`, `vertical-slice`,
`mvp`, `qa`, `release`, `art-bible`, `devlog`, `audit`, `aaa`, `game-design`,
`production-plan`, `milestone`, `agents` (instruções persistentes). Gêneros (`--genre`): `narrative`, `adventure`,
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
   com `--genre`; pacotes são convenções a confirmar no código, não capacidades.
   `capabilities.mentioned` aponta
   arquivo local; não prova pause, reset, seed nem determinismo. Confira `basis`,
   `via` e os limites. `context` já executa `scan`: se `foundation.audit.required`
   for verdadeiro, avise as lacunas com `audit.notice` e comece o levantamento conforme
   [auditoria de projeto](references/project-audit.md), sem pedir um segundo
   consentimento; respeite restrição explícita na conversa atual. Sem projeto
   identificável, não invente um alvo. Em retomada, fonte encontrada não é tarefa
   validada: siga [continuidade e retomada](references/process.md#continuidade-e-retomada).
2. **Intenção e prontidão.** Defina fantasia, verbo central, plataforma, cenário,
   restrições, a maior incerteza e a prova de conclusão; assuma o resto com registro e
   pergunte só o que impede de jogar. A escala (jam/conto, produto, AA / Triple-I)
   vive no brief e muda a quantidade de documentos, não o piso do verbo
   ([ambição](references/ambition.md)). Leia [processo](references/process.md) e
   [qualidade](references/quality.md). Para criação ou pré-produção, siga
   [o ciclo criativo](references/preproduction.md): Game Brief, MDA/GDD, PoC, PRD/TDD,
   vertical slice, MVP, QA/playtest e release. `--stage <etapa>` carrega só o template
   pertinente; `template <etapa> --project <projeto>` imprime um rascunho. Reaproveite
   documentos existentes; um jogo pequeno reúne tudo em `game-design`. O design system
   do jogo (`art-bible`) é conteúdo mínimo; o arquivo separado é opcional se outro
   canônico cobrir. Contrato: [design system do jogo](references/game-design-system.md).
   Direção aprovada: `--event direction-approved` e base mínima sincronizada no mesmo
   turno, mesmo com nove candidatos encontrados.
3. **REUSE → ADAPT → CREATE.** Busque no jogo, no acervo e nas fontes pertinentes.
   `doctor` lista os starters disponíveis; começar por um deles é REUSE, escrever um
   loop do zero é CREATE. Se o laboratório tiver `shared/sfx` com sons, use
   `sfx search` antes de baixar. Sem acervo, o starter já fala em
   `public/sfx`; `sfx serve` recusa catálogo vazio. Crescer o acervo é
   `sfx import ARQUIVO --metadata JSON` (ffmpeg); `sfx seed` lê
   `selection.json` local. `sfx info ID` lê a ficha; `sfx export ID
   --to PASTA` copia bytes e créditos. Importar e exportar não é
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
   certifica e `N/A` exige motivo. Não publique nem delegue sem autorização aplicável.
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
   e diz o piso, `next` propõe subir a dimensão pelo nome. Nenhum comando atribui
   degrau; ao declarar um, declare dispositivo, versão, cena e quem observou.
   **A barra descreve, o gate recusa.** [Os dez gates](references/gates.md) formalizam
   as linhas “Pronto para…” do ciclo: ao pedir a próxima permissão, declare uma linha
   por critério com `met`/`unmet`/`waived`/`out_of_scope` e o que sustenta o estado; `gate <projeto>`
   lê. Critério sem linha é pendente. As três saídas são passar, cortar escopo e
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
   recibo de origem. Não valida licença. Arquivo sem recibo conta como licença
   desconhecida, e `next` propõe declarar a origem antes de seguir.
   **`craft <projeto>`** lê checklists de ofício (paleta, perdão, percentil,
   regra de parada) — conformidade com o que o projeto declarou, sem limiar
   importado. `observed` é sempre falso. Só levanta o gate que o projeto pediu.
   Depois de um `init` fresco, `next` propõe **abrir o ciclo** antes de
   substituir os rascunhos: o starter já é um jogo que abre, ensina o
   primeiro ciclo no campo — mover, avançar, coletar, guardar e o mapa
   da superfície que falou — e traz art-bible vigente. O `init` não o
   reescreve.
   **`guide [<projeto>]`** devolve os três passos ideia→ciclo (start,
   jogar, note) sem executar nenhum. Sem subcomando, o harness é o
   próprio `guide`. Destino existente preenche o comando que abre o
   jogo e o `kind` do passo de jogar; se o starter declara o verbo, o
   passo 2 o nomeia; `then` nomeia look, chuva e voz quando o projeto
   as declara; `executed` fica `false`. `next` fica em `then.lost`.
   **`start <projeto>`** cria se o destino estiver livre e devolve
   `play` + `then.note`. Se o starter declara o verbo e as teclas, o
   prompt as nomeia — inclusive o cluster de uma mão, o toque, o
   controle e as queries de look e chuva, se o starter as declara. Se o
   projeto declara `look`/`table`/`sfx`, `then` as nomeia; depois de um
   recibo, o prompt aponta o segundo ciclo. Não executa o jogo. `--idea` entra no brief
   e, se houver `data/copy.json`, na tela do primeiro ciclo. O brief
   continua rascunho. A frase na tela não muda o verbo.
   **`roles <projeto>`** lê os papéis de áudio que o código declara e os
   arquivos que os preenchem. `--fill` sugere o acervo; `--apply` copia
   com o nome do papel. Crescer o acervo é `sfx import` / `sfx seed`
   (ffmpeg); `sfx info` lê a ficha e `sfx export` copia bytes e
   créditos. Importar e exportar não é ouvir. `heard` é sempre falso. Papel vazio
   entra no `next` como `audio.roles` — o verbo mudo não espera os
   rascunhos.
   **`feel <projeto>`** lê constantes de perdão/hitstop/câmera no `CONFIG` e o
   recibo de observação no disco. `felt` é sempre falso. Sem recibo, `next`
   propõe `feel.unobserved` e aponta `note`.
   **`note <projeto>`** grava o recibo curto (cenário e papel por omissão)
   em `docs/playtest/<utc>/`. `--from-run` anexa `docs/playtest/last-run.json`
   (resumo e, se houver, a curva) como candidato de medição e não fecha o
   achado. Não joga e não sente.
   **`access` / `save` / `budget`** leem opção de alcance (incluindo
   uiScale e preset de uma mão), versão de save e artefato de orçamento.
   `verified`/`trusted`/`measured` são sempre falsos.
   Falta no disco entra no `next` antes dos rascunhos.
   **`art` / `content` / `ship`** leem paleta ou art-bible vigente, conteúdo
   fora do código e passo de empacotar. Se `dist/VERSION.json` existe,
   `ship` relata nome e versão. `consistent`/`enough`/`shipped` são
   sempre falsos. Sem declaração, o `next` nomeia `art.missing`,
   `content.inline` e `ship.unpacked` antes dos rascunhos.
   **`playtest <projeto>`** lê se o achado tem problema, evidência, hipótese
   e medição. `observed` e `outsider` são sempre falsos. `--invite` escreve
   a página para quem nunca viu o jogo; `next` a aponta depois do recibo
   de quem fez. Recibo sem forma entra no `next` como `playtest.unstructured`.

Fontes detalhadas sob demanda: [mapa dos estudos](references/sources.md).
Comandos, limites e adoção: [README](README.md).
