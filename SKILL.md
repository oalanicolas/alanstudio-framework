---
name: game-dev
description: Criar, evoluir, avaliar, produzir e verificar jogos com IA, partindo do acervo existente, até o acabamento pretendido. Roteia por intenção (craft, shape, critique, polish, feel, audio, next…) sobre um harness thin que recorta contexto, lê declarações e registra evidência.
---

# Game Dev

Use este processo em qualquer engine. O objetivo é uma experiência jogável no
**acabamento pretendido**, com evidência, preservando a direção do usuário e a
qualidade aprovada — fácil de começar, difícil de rebaixar. “AAA” aqui é piso de
acabamento observável (verbo, feel sincronizado, áudio, pacing, mundo, receita
repetível), não tier de publisher; o alvo honesto com IA é AA / Triple-I nesse piso.

Todos os comandos do harness são `python3 scripts/game.py ...` a partir deste
repositório, com `--root <laboratorio>` antes ou depois do subcomando. Num
[workspace ligado](references/workspace-binding.md), a entrada local é
`python3 framework/scripts/game.py ...`; leia as personalizações em `context.workspace`. Se a ligação recusa preencher pasta não baixada com o starter, o `context` nomeia a preenchida que a ligação já recusa. Módulo no disco não é o jogo. Sem chave `preenchida`. Se a ligação recusa inventar o conteúdo da referência ausente, o `context` nomeia o inventado que a ligação já recusa. Lacuna no disco não é a regra. Sem chave `inventado`.

| Situação | Faça |
| --- | --- |
| Primeira vez ou raiz em dúvida | `doctor --root <lab>`; corrija itens `missing`. Ele nomeia os projetos e lista os starters. Se o package pede Node, o `doctor` nomeia o engines que o package já declara. Pedido no disco não é binário no PATH. Sem chave `engines`. Nomear não instala. Se o manifesto declara as trocas, o `doctor` nomeia as substituições que o manifesto já declara. Manifesto no disco não é projeto criado. Sem chave `substitutions`. Sem jogo e com starter, `then.guide` aponta o mapa ideia→ciclo com `--idea`. Se o README imprime o exemplo, o `doctor` nomeia o exemplo que o README já imprime. Frase no then não é pasta criada. Sem chave `exemplo`. Se a ambição recusa que o harness seja motor, o `doctor` nomeia o motor que a ambição já recusa. Convite no then não é runtime. Sem chave `motor`. Se a skill recusa que AAA seja tier de publisher, o `doctor` nomeia o publisher que a skill já recusa. Atalho no disco não é orçamento. Sem chave `publisher`. Se o mapa recusa que a ausência seja evidência negativa, o `doctor` nomeia a ausência que o mapa já recusa. Lista no disco não é laboratório. Sem chave `ausência`. Se a receita recusa que o mapa crie a pasta, o `empty` do `doctor` nomeia a pasta que a receita já recusa. Lista no disco não é projeto criado. Sem chave `pasta`. não comprova que um projeto funciona. Se a receita recusa que a lista bloqueante comprove que um projeto funciona, o `blocking` do `doctor` nomeia o funciona que a receita já recusa. Checagem no disco não é o jogo. Sem chave `funciona`. Não cria e não executa. Na raiz do framework, `guide` sem `--idea` recusa com o mesmo `sem destino` do `start` — não devolve `start '<destino>'`. A recusa nomeia o `start --idea` que o README já imprime; nomear não cria |
| Laboratório com jogos (o caso normal) | `discover --root <lab>` lê cada jogo e devolve o que os distingue, inclusive os sinais que o `next` usa (primeiro ciclo, ofício, feel sem recibo, achado sem forma, convite, origem sem recibo e lacunas de dimensão); a ordem é a do disco — **não trate a primeira linha como prioridade**. Se o package declara os scripts, o `discover` nomeia os scripts que o package já declara. Lista no disco não é passo executado. Sem chave `scripts`. Se o roteiro recusa que o documento comprove qualidade, o `discover` nomeia a qualidade que o roteiro já recusa. Conta no disco não é acabamento. Sem chave `qualidade`. Se a guia recusa que gerar o documento seja autorizar, o item do review nomeia o autorizar que a guia já recusa. Documento no disco não é a autorização. Sem chave `autorizar`. Se o README recusa que listagem de caminho e tipo apague o estado, o `discover` nomeia a listagem que o README já recusa. Caminho no disco não é o jogo. Sem chave `listagem`. Sinal verdadeiro não é partida jogada. Se o README recusa que sinal verdadeiro seja partida jogada, o `signals` do review nomeia a partida que o README já recusa. Sinal no disco não é alguém de fora. Sem chave `partida`. Se o README recusa que o recorte classifique por urgência, o `truncated` do `review` nomeia a urgência que o README já recusa. Recorte no disco não é o inventário. Sem chave `urgência`. Lista de arquivo sem recibo não é licença. Lista de chave ausente não é alcance observado |
| Perdeu o comando que abre | `play` (ou `open`) aponta o serve e a superfície (`url`, padrão `http://localhost:8080/`) sem executar. Sem caminho, o único jogo do laboratório basta; dois pedem o caminho. Se o serve recusa produção, o `play` nomeia a produção que o serve já recusa. Serve no disco não é publicação. Sem chave `produção`. Se a receita recusa que verbo mudo ou sem peso seja, o `play` nomeia o verbo que a receita já recusa. Abrir no disco não é o verbo. Sem chave `verbo`. Se a receita recusa que o arco prometa o dash, o `play` nomeia o arco que a receita já recusa. Arco no disco não é o dash. Sem chave `arco`. Se a receita recusa que aceitar o parâmetro prove que ele afeta o RNG, o then do `play` nomeia o RNG que a receita já recusa. Endereço no disco não é a simulação. Sem chave `RNG`. Se a receita recusa que oferecer o recibo seja observação, o then do `play` nomeia a observação que a receita já recusa. Recibo no disco não é a sessão. Sem chave `observação`. Sem seed a frase sai; com seed o then nomeia o RNG. Com tela, o avanço abre a porta. Depois da partida a página grava o recibo se você escrever; o recibo escrito não observa. Se a receita recusa que o recibo escrito observe, o `noted` do `play` nomeia o escrito que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `escrito`. `note` sem caminho usa o mesmo jogo. `then.note` continua. `executed` fica falso. `runtime` lê o Node do PATH. `usable` é só o binário. Se a receita recusa que o usable seja mais que o binário, o `usable` do `runtime` nomeia o binário que a receita já recusa. Node no PATH não é o dispositivo. Sem chave `binário`. Nomear o endereço não serve. Não cria |
| Jogo novo | Destino inexistente e engine web: `start --idea "<fantasia>"` (ou `start <novo> --starter <starter> --idea "<fantasia>"`) cria o projeto — sem caminho, a frase nomeia a pasta, ao lado do framework se o start corre de dentro desta árvore —, põe a frase na abertura e no aviso do primeiro ciclo, escreve `AGENTS.md` com o comando que abre, o `note` e o `playtest` (não é GDD; não lista rascunhos que não plantou; o `playtest` só lê; sem os quatro não é achado; nomear o leitor não observa), o prompt nomeia o `playtest` que o `AGENTS.md` já cita (só lê; sem os quatro não é achado; sem `then.playtest`; nomear o leitor não observa), não planta os rascunhos do ciclo (`--docs` os cria) e devolve `open` (= `play`), `url` e `then.note` sem executar. Se o play pede npm, o `package.json` tem dependências e `node_modules` falta, `then.install` nomeia `npm install`. Sem dependências a chave some. Nomear não instala. `open` é o comando de agora; `url` é a superfície pedida; `steps` é o mesmo mapa de três passos do `guide`, com o passo 1 feito. Se o starter declara o verbo e as teclas, o prompt as nomeia — `Fantasia:` à parte de `Verbo:` quando `--idea` ou `copy.json` têm frase; a frase não muda o verbo — inclusive a porta, o cluster de uma mão, o toque, o controle e as queries de look, chuva, par, seed, relógio e convite, se houver. Se o projeto — ou o starter, antes do destino existir — declara as ferramentas, `then` nomeia par, look, chuva e voz; depois de um recibo, o prompt as aponta. Se o disco tem last-run com seed, `then` aponta a partida (número, chuva e look quando o candidato os nomeia) e o convite; nomear o endereço não observa. Vestir a query não grava. A chuva da query não retoma o hold. Na porta e no fim a região viva nomeia a mesa e o look que a chuva já veste — spawn e normal somem. Na porta o telefone vê Jogar: toque sem ter apertado. Depois do tap a porta não chama o avanço de cima. Nomear o ofício não pinta. A frase não muda o verbo. `guide [<novo>] --idea "<fantasia>"` (também sem subcomando: `python3 scripts/game.py --idea "<fantasia>"`) mapeia start → jogar → note. `open` é o comando de agora; `prompt` o nomeia. Sem destino, a frase nomeia a pasta no comando do start — ao lado do framework se o mapa corre de dentro desta árvore; no diretório atual se corre de fora. Não grava a frase nem cria a pasta. Sem destino, se o diretório atual é um jogo fora do framework, o mapa usa esse caminho. `next` só se o ciclo já correu e você não sabe o que falta. Sem `start`: `init` e depois o comando em `play`. Se o package declara o módulo, o `init` nomeia o módulo que o package já declara. Tipo no disco não é runtime instalado. Sem chave `type`. Se o processo recusa que se copie runtime de referência só para absorver um contrato, o `init` nomeia as referências que o processo já recusa. Runtime no disco não é o contrato. Sem chave `referências`. Se a receita recusa que o scaffold ou a cópia que inicia seja mais que ponto de partida, o then do `init` nomeia o scaffold que a receita já recusa. Cópia no disco não é a slice. Sem chave `scaffold`. Jogo pequeno em qualquer engine: `template game-design --project <novo> --output <novo>/docs/game-design.md` e `--stage game-design`. Não gere nove templates |
| Em dúvida sobre o próximo passo | `next --focus <foco>` deriva uma proposta do estado no disco; sem caminho, o único jogo do laboratório basta. `executed` fica `false` e a escolha é sua. Se o processo pede uma ação recomendada, o `next` nomeia a ação que o processo já pede. Proposta no disco não é autorização. Sem chave `ação`. Se o roteiro recusa que o comando crie o jogo, o `next` nomeia a criação que o roteiro já recusa. Proposta no disco não é pasta criada. Sem chave `criação`. Se o next recusa que fonte encontrada seja tarefa validada, o `next` nomeia a validada que o next já recusa. Fonte no disco não é a tarefa. Sem chave `validada`. Se o processo recusa fabricar tarefa para cumprir o formato, o `next` nomeia a fabricação que o processo já recusa. Lista no disco não é backlog. Sem chave `fabricação`. Se o processo recusa que comando registrado com falha ou uma proposta rejeitada conclua a etapa, a alternativa do `next` nomeia a etapa que o processo já recusa. Proposta no disco não é a etapa. Sem chave `etapa`. Se a receita recusa que nome de comando prove a conclusão, o `signals` do next nomeia a conclusão que a receita já recusa. Sinal no disco não é o término. Sem chave `conclusão`. Se o fluxo recusa que melhorar o jogo seja uma rodada executável, o `next` nomeia a rodada que o fluxo já recusa. Pedido no disco não é o recorte. Sem chave `rodada`. |
| O verbo funciona mas não convence | `feel`; se `unobserved`, `note --author … --note "o que o verbo sentiu"`. Sem caminho, o único jogo do laboratório basta. Lê rumble, o peso do passo, as janelas da chuva e o rumo que o coil do dash marca; nomear não é `felt`. Depois `roles` e `context --focus audio` |
| Paleta, conteúdo no código ou jogo só na máquina de quem construiu | `art` / `content` / `ship` <projeto>; `consistent`/`enough`/`shipped` ficam `false` |
| Observou uma partida e só tem uma nota | `playtest`; se `unstructured`, escreva problema, evidência, hipótese e medição. Sem caminho, o único jogo do laboratório basta. Depois do recibo, `playtest --invite` escreve a página e aponta `href` (`/?invite=1` ou, com seed no disco, `/?invite=1&seed=<n>`, com chuva nomeada `&spawn=<mesa>`, com look nomeado `&look=<paleta>`, e com relógio nomeado e ≠ 1 `&speed=<relógio>`), onde a tabela some; depois do fim a página do maker aponta o convite desta partida se a seed ficou no recibo — copiar o endereço não grava; a página também mostra seed, pontos, eixos, a curva que o last-run já traçou e se o candidato foi simulado (`nearest-orb` vira `simulada`; `played` some; a faixa não leva a conta nem o relógio) e oferece os quatro nomes para copiar ou gravar — o achado copiado e gravado leva essa faixa; sem tally nem relógio; markdown no disco não é alguém de fora; depois do fim ela rola até o painel; rolar não é alguém de fora; número na faixa não preenche os quatro; copiar não grava; sem a área de transferência o Copiar baixa o markdown; baixar não grava; gravar anexa o candidato se houver last-run; gravado não é alguém de fora |
| “Está AAA?” ou slice pronta | `context <projeto> --stage vertical-slice` e leia `finish`; só então `template aaa` |
| Mudança em jogo existente | `context <projeto> --focus <foco>`; com gênero definido, `--genre <g>` |
| “continue” / “vamos avançar” | `context <projeto> --focus <foco> --event resume` e leia `continuity.sources`, preservando o foco da tarefa |
| Usuário aprovou uma referência | `context <projeto> --focus <foco> --event direction-approved` e sincronize a base no mesmo turno |
| Recorte já demonstra a experiência | `context <projeto> --focus production --stage production-plan` |
| Revisar um marco (alpha, beta, gold) | `context <projeto> --focus production --stage milestone`; `bar <projeto>` diz o piso declarado e `gate <projeto>` o que ainda não pode passar |
| Registrar observação, orçamento medido ou decisão de marco | `record <projeto> --kind observation\|budget\|milestone --author ... --note ... --field k=v --output <pasta-nova>`. Se o roteiro recusa medir os critérios, o `record` nomeia a medição que o roteiro já recusa. Recibo no disco não é observação. Sem chave `mede`. Se a receita recusa que o ganho no caso rejeitado seja ganho equivalente no solver ativo, o `record` nomeia o solver que a receita já recusa. Ganho rejeitado no disco não é o solver. Sem chave `solver`. Se a receita recusa que ganho na média demonstre redução de engasgos, o `fields` do `record --kind budget` nomeia os engasgos que a receita já recusa. Número no disco não é o quadro estável. Sem chave `engasgos`. Se a receita recusa que a máquina de desenvolvimento quente seja a máquina do jogador fria, o `fields` do `record --kind budget` nomeia a quente que a receita já recusa. Plataforma no disco não é a máquina fria. Sem chave `quente`. Se a receita recusa que o recibo feche o marco, o `fields` do `record --kind milestone` nomeia o marco que a receita já recusa. Recibo no disco não é a passagem. Sem chave `marco`. Se a receita recusa que o recibo sem os quatro seja achado, o `fields` do `record --kind observation` nomeia a impressão que a receita já recusa. Recibo no disco não é playtest. Sem chave `impressão`. Se o roteiro recusa que o screenshot isolado comprove animação, o `record` nomeia a animação que o roteiro já recusa. Anexo no disco não é controle. Sem chave `animação`. Se a receita recusa que bytes menores provem fidelidade, o `record` nomeia a fidelidade que a receita já recusa. Anexo no disco não é a trajetória. Sem chave `fidelidade`. Se o roteiro recusa que o HEAD substitua o julgamento, o `version` nomeia o julgamento que o roteiro já recusa. Identidade no disco não é avaliação. Sem chave `julgamento`. |

## Preparação

Antes de qualquer trabalho de design, código ou documento:

1. Carregar o contexto do projeto pelo harness.
2. Identificar a **escala** e ler o contrato dela.
3. **Se o usuário invocou um sub-comando** (`craft`, `critique`, `feel`…), carregar a
   referência dele em `commands/<comando>.md`. Não é negociável: `craft` sem
   `craft.md` pula o shape que o usuário espera; `critique` sem `critique.md` vira nota.

Pular a preparação produz trabalho genérico que ignora o projeto.

### 1. Contexto

```sh
python3 scripts/game.py context <projeto> --focus <foco> [--stage <etapa>] [--genre <g>] [--scale <s>] [--event <evento>]
```

Consuma o JSON inteiro. Leia os AGENTS aplicáveis (`instructions`),
`foundation.read_first`/`records`, os catálogos em `studies` e **somente** as
referências em `read_next` (receita → pacote de plataforma → pacote de gênero).
Não rode de novo se a saída já está nesta conversa; exceções: depois de `teach` ou
`document` (reescrevem a base), depois de `--event direction-approved`, e em
retomada (`--event resume`).

Focos: `create`, `mechanics`, `lifecycle`, `content`, `visual`, `audio`, `feel`,
`network`, `architecture`, `performance`, `accessibility`, `persistence`, `release`,
`production`. Etapas: `brief`, `mda`, `gdd`, `poc`, `prd`, `tdd`, `vertical-slice`,
`mvp`, `qa`, `release`, `art-bible`, `devlog`, `audit`, `aaa`, `game-design`,
`production-plan`, `milestone`, `agents` (memória persistente gerada do disco: o comando que abre e o que não foi plantado; sem rascunhos não lista GDD). Gêneros (`--genre`): `narrative`, `adventure`,
`platformer`, `action-adventure`, `shooter`, `fighting`, `stealth`, `horror`, `racing`,
`sports`, `rhythm`, `turn-based`, `deckbuilder`, `strategy`, `tower-defense`, `puzzle`,
`simulation`, `survival-crafting`, `rpg`, `roguelike`, `multiplayer-competitive`, `idle`,
`casual` — a lista vigente está em `context.packs.genre.available`; um campo
`Gênero:` em documento só sugere.

- **Sem projeto identificável:** `discover --root <lab>` lê cada jogo e devolve o que
  os distingue; a ordem é a do disco, **não** prioridade. Não invente um alvo.
  Primeira vez ou raiz em dúvida: `doctor --root <lab>`.
- **`foundation.audit.required` verdadeiro:** avise com `audit.notice` e rode
  [`teach`](commands/teach.md) sem pedir segundo consentimento; depois retome o
  comando original. Restrição explícita na conversa continua valendo.
- **“Inicie/inicialize o projeto”** sem alvo operacional é [`teach`](commands/teach.md)
  (`--event initialize`); “inicie o servidor/partida” é essa operação; “inicie a
  implementação” de etapa definida retoma o recorte. Se o roteiro recusa que o aviso seja uma pergunta, o `context` nomeia a pergunta que o roteiro já recusa. Aviso no disco não é espera. Sem chave `pergunta`. Se o roteiro recusa que o resultado seja inferido pelo scanner, o `context` nomeia o scanner que o roteiro já recusa. Sinal no disco não é o resultado. Sem chave `scanner`. O objeto e a conversa prevalecem.
- `capabilities.mentioned` aponta arquivo local; não prova pause, reset, seed,
  observe, act, advance, capture nem dispose. `context` lê arquivos sem executá-los.

1. **Contexto.** Resolva projeto e tarefa; execute `context <projeto> --focus <foco>`.
   Leia os AGENTS aplicáveis, `foundation.read_first`/`records`, os catálogos em
   `studies` e somente as referências em `read_next`. O núcleo é agnóstico;
   `read_next` inclui o [pacote de plataforma](packs/README.md) quando a engine foi
   identificada e o de gênero quando você passou `--genre`. Se `packs.genre.suggested`
   trouxer um gênero lido de documento, confirme com a conversa e repita o `context`
   com `--genre`; pacotes são convenções a confirmar no código, não capacidades. Se o pacote recusa que teste unitário prove o navegador, o `context` nomeia o navegador que o pacote já recusa provar. Pacote no disco não é comportamento no aparelho. Sem chave `navegador`. Se o índice recusa que o pacote certifique capacidade, o `context` nomeia a capacidade que o índice já recusa. Pacote no disco não é comportamento. Sem chave `capacidade`. Se o pacote recusa que métricas RAF comprovem os quadros, a plataforma nomeia os quadros que o pacote já recusa. Callback no disco não é quadro apresentado. Sem chave `quadros`. Se o mapa recusa que o pacote seja extração, o `context` nomeia a extração que o mapa já recusa. Convenção no disco não é repositório executado. Sem chave `extração`. Se o mapa recusa que a menção seja mecânica obrigatória, o `genre_mentions[n]` nomeia a mecânica que o mapa já recusa. Campo no disco não é regra do jogo. Sem chave `mecânica`. Se a receita recusa que o nome seja API, o `context` nomeia a API que a receita já recusa. Vocabulário no disco não é runtime. Sem chave `api`. Se o roteiro recusa que menções locais sejam rastreamento de comportamento, a menção nomeia o rastreamento que o roteiro já recusa. Menção no disco não é o gesto. Sem chave `rastreamento`. Se a barra recusa que o determinismo seja capacidade, o `capabilities` desconhecido nomeia o determinismo que a barra já recusa. Lista no disco não é ciclo demonstrado. Sem chave `determinismo`.
   `capabilities.mentioned` aponta
   arquivo local; não prova pause, reset, seed nem determinismo. Confira `basis`,
   `via` e os limites. Se o processo recusa que o hash seja leitura, o `git` nomeia a leitura que o processo já recusa. Identidade no disco não é inspeção. Sem chave `leitura`. Se o processo recusa que estados salvos estejam atualizados, o `git` nomeia os desatualizados que o processo já recusa. Snapshot no disco não é o estado. Sem chave `desatualizados`. `context` já executa `scan`: se `foundation.audit.required`
   for verdadeiro, avise as lacunas com `audit.notice` e comece o levantamento conforme
   [auditoria de projeto](references/project-audit.md), sem pedir um segundo
   consentimento; respeite restrição explícita na conversa atual. Se o roteiro recusa que o scanner comece a auditoria, o `required` do `audit` nomeia o começo que o roteiro já recusa. JSON no disco não é o levantamento. Sem chave `começo`. Se
   `foundation.audit.deferred` for verdadeiro, o destino já abre — jogue
   primeiro; lacuna de rascunho depois do `start` não é auditoria neste
   turno. Se o roteiro recusa que a lacuna de rascunho seja auditoria neste turno, o `deferred` do `audit` nomeia a auditoria que o roteiro já recusa. Sinal no disco não é o levantamento. Sem chave `auditoria`. Se o README aponta o serve, o `scan` nomeia o serve que o README já aponta. Página no disco não é partida jogada. Sem chave `serve`. Se o roteiro recusa que a pasta references seja descartada, o `scan` nomeia a descartada que o roteiro já recusa. Roteiro no disco não é inventário. Sem chave `descartada`. Se o roteiro pede documentar sem consentimento, o `context` nomeia o audit que o roteiro já pede. Roteiro no disco não é base escrita. Sem chave `audit`. Se o roteiro recusa que a checagem seja daemon, o `audit` nomeia o daemon que o roteiro já recusa. Roteiro no disco não é interceptação. Sem chave `daemon`. Se o roteiro recusa que executed falso seja uma instrução para parar, o `audit` nomeia o parar que o roteiro já recusa. Roteiro no disco não é espera. Sem chave `parar`. Se o roteiro recusa que o local não percorrido seja inexistente, o `scan` nomeia a inexistência que o roteiro já recusa. Contagem no disco não é inventário. Sem chave `inexistente`. Se o teach recusa que cobertura lexical seja a prova, o `coverage` nomeia o lexical que o teach já recusa. Varredura no disco não é o rastro. Sem chave `lexical`. Se o roteiro recusa que o recorte de estudo tome a prioridade, o `limits` da coverage nomeia a prioridade que o roteiro já recusa. Limite no disco não é a base. Sem chave `prioridade`. Se o mapa recusa que a cobertura desigual seja acidente, o `issues[n]` da coverage nomeia o acidente que o mapa já recusa. Recorte no disco não é falha. Sem chave `acidente`. Se o roteiro recusa que a lista cortada seja a cobertura, o `issues_truncated` da coverage nomeia a falta que o roteiro já recusa. Recorte no disco não é o inventário. Sem chave `falta`. Se a guia recusa que preencher linhas certifique o jogo, o `non_current_documents[n]` nomeia as linhas que a guia já recusa. Documento no disco não é o jogo. Sem chave `linhas`. Se o processo recusa que a etapa certifique o progresso, o `context` nomeia o progresso que o processo já recusa. Contexto no disco não é degrau. Sem chave `progresso`. Se o roteiro recusa que o evento seja inferido do nome de um arquivo, o `context` nomeia o inferido que o roteiro já recusa. Arquivo no disco não é a conversa. Sem chave `inferido`. `--event direction-approved` e `--stage audit` continuam
   pedindo a base. Sem projeto
   identificável, não invente um alvo. Em retomada, fonte encontrada não é tarefa
   validada: siga [continuidade e retomada](references/process.md#continuidade-e-retomada). Se o processo nega que documento pronto seja PoC, o `context` nomeia a PoC que o processo já nega. Fonte no disco não é jogo implementado. Sem chave `process`. Se o processo recusa que sources_found comprove a fila, o `sources[n]` do continuity nomeia a fila que o processo já recusa. Fonte no disco não é backlog. Sem chave `fila`. Se o next recusa que fonte em rascunho seja passo, o `sources[n]` do continuity nomeia o passo que o next já recusa. Rascunho no disco não é o passo. Sem chave `passo`. Se a memória recusa o adjetivo, o `scan` nomeia o AAA que a memória já recusa. Memória no disco não é acabamento. Sem chave `agents`.
2. **Intenção e prontidão.** Defina fantasia, verbo central, plataforma, cenário,
   restrições, a maior incerteza e a prova de conclusão; assuma o resto com registro e
   pergunte só o que impede de jogar. A escala (jam/conto, produto, AA / Triple-I)
   vive no brief e muda a quantidade de documentos, não o piso do verbo
   ([ambição](references/ambition.md)). Leia [processo](references/process.md)
   — com tela, a primeira superfície é a porta; `play` aponta sem executar —
   e [qualidade](references/quality.md). Para criação ou pré-produção, siga
   [o ciclo criativo](references/preproduction.md): Game Brief, MDA/GDD, PoC, PRD/TDD,
   vertical slice, MVP, QA/playtest e release. `--stage <etapa>` carrega só o template
   pertinente; `template <etapa> --project <projeto>` imprime um rascunho. Se o molde recusa publicar, o `template` nomeia a publicação que o molde já recusa. Molde no disco não é autorização. Sem chave `publicar`. Se a guia recusa que o MVP prove a hipótese de valor, o `template` nomeia o valor que a guia já recusa. Molde no disco não é validação. Sem chave `valor`. Se a guia recusa que placeholders certifiquem o acabamento, o `template` nomeia o acabamento que a guia já recusa. Molde no disco não é a fatia. Sem chave `acabamento`. Se a guia recusa que o checklist seja um ciclo paralelo, o `template` nomeia o paralelo que a guia já recusa. Guia no disco não é o molde. Sem chave `paralelo`.
   Reaproveite
   documentos existentes; um jogo pequeno reúne tudo em `game-design`. O design system
   do jogo (`art-bible`) é conteúdo mínimo; o arquivo separado é opcional se outro
   canônico cobrir. Contrato: [design system do jogo](references/game-design-system.md). Se o sistema recusa que o scanner certifique tokens, o `scan` nomeia os tokens que o sistema já recusa. Documento no disco não é aprovação artística. Sem chave `tokens`. Se o visual recusa que salvar a imagem seja o trabalho, a área `art_direction` do `scan` nomeia a imagem que o visual já recusa. Imagem no disco não é a aprovação. Sem chave `imagem`. Se o roteiro recusa que o recibo presente seja licença válida, o `scan` nomeia a licença que o roteiro já recusa. Área no disco não é concessão. Sem chave `licença`. Se o release recusa que localização atribua autoria, a área `provenance` do `scan` nomeia a localização que o release já recusa. Localização no disco não é o titular. Sem chave `localização`. Se o roteiro recusa prescrever quantas pessoas, o `scan` nomeia as pessoas que o roteiro já recusa. Área no disco não é censo. Sem chave `pessoas`. Se a guia recusa que o checklist seja uma décima área, a área `qa` do `scan` nomeia a décima que a guia já recusa. Área no disco não é o inventário. Sem chave `décima`. Se a receita recusa que telemetria seja padrão silencioso, o `scan` nomeia a telemetria que a receita já recusa. Área no disco não é consentimento. Sem chave `telemetria`. Se o processo recusa que servidor aberto conclua inicialização documental, a área `runbook` do `scan` nomeia a inicialização que o processo já recusa. Servidor no disco não é o documento. Sem chave `inicialização`. Se a receita recusa promover histórico a regra vigente, o `scan` nomeia o histórico que a receita já recusa. Área no disco não é decisão atual. Sem chave `histórico`. Se o mapa recusa que alegar eficácia comprovada seja evidência, a área `decisions` do `scan` nomeia a eficácia que o mapa já recusa. Mapa no disco não é o ensaio. Sem chave `eficácia`. Se a guia recusa que divertido isoladamente baste, o `scan` nomeia o divertido que a guia já recusa. Área no disco não é o verbo. Sem chave `divertido`. Se o craft recusa que contexto do projeto seja brief da tarefa, a área `gdd` do `scan` nomeia o brief que o craft já recusa. Contexto no disco não é o brief. Sem chave `brief`. Se a guia recusa pontuação universal de diversão, o `scan` nomeia a pontuação que a guia já recusa. Área no disco não é experiência. Sem chave `pontuação`. Se a guia recusa que a ferramenta de raciocínio seja documento obrigatório, a área `mda` do `scan` nomeia o obrigatório que a guia já recusa. Ferramenta no disco não é a obrigação. Sem chave `obrigatório`. Se a guia recusa inventar público observado, o `scan` nomeia o público que a guia já recusa. Área no disco não é audiência. Sem chave `público`. Se o shape recusa que documento preenchido seja PoC executada, a área `vision` do `scan` nomeia a executada que o shape já recusa. Documento no disco não é o experimento. Sem chave `executada`. Se a ambição recusa AAA como adjetivo de marketing, o `scan` nomeia o marketing que a ambição já recusa. Campo no disco não é campanha. Sem chave `marketing`. Se o roteiro recusa que reconstruir documentos comprove intenções, o `scan` nomeia as intenções que o roteiro já recusa. Candidato no disco não é autoria. Sem chave `intenções`.
   Direção aprovada: `--event direction-approved` e base mínima sincronizada no mesmo
   turno, mesmo com nove candidatos encontrados.
3. **REUSE → ADAPT → CREATE.** Busque no jogo, no acervo e nas fontes pertinentes.
   `doctor` lista os starters disponíveis; começar por um deles é REUSE, escrever um
   loop do zero é CREATE. Se o laboratório tiver `shared/sfx` com sons, use
   `sfx search` antes de baixar. Sem acervo, o starter já fala em
   `public/sfx`; `sfx search` nomeia o stem que casa com o termo. Se o `tools/design-sfx.*` desloca a voz, o `sfx search` nomeia o deslocamento que o sfx já oferece. Arquivo no disco não é mix ouvida. Sem chave `sfx`. Se a receita recusa que o acervo compartilhado seja o primeiro ciclo, o `local` do `sfx search` nomeia o adapt que a receita já recusa. Stem no disco não é mix. Sem chave `adapt`. Se a barra recusa que triagem documental/técnica seja aprovação artística, o `matches` do `sfx search` nomeia a triagem que a barra já recusa. Ficha no disco não é mix. Sem chave `triagem`.
   `sfx info` lê a chave e nomeia o stem que o recibo lista e o
   disco perdeu, `roles --fill` nomeia o mesmo stem. Se o processo recusa o reuso automático, o `roles --fill` nomeia o reuso que o processo já recusa. Arquivo no disco não é licença. Sem chave `reuso`. Se o mapa recusa que o catálogo ouça o starter, o `context` nomeia a escuta que o mapa já recusa. Acervo no disco não é mix ouvida. Sem chave `ouve`. Se o mapa recusa que tocar nessa página seja mix ouvida, o `sfx` do `studio_assets` nomeia o tocar que o mapa já recusa. Página no disco não é o mix. Sem chave `tocar`. Se o mapa recusa que um workspace herde silenciosamente as preferências de outro, o `policy` do `studio_assets` nomeia a herança que o mapa já recusa. Política no disco não é o outro laboratório. Sem chave `herança`. Se o mapa recusa que o catálogo no disco seja o presente, o `exists` do `studio_assets` nomeia o presente que o mapa já recusa. Arquivo no disco não é mix. Sem chave `presente`.
   `sfx verify` nomeia os stems sem cruzar
   o que não existe e nomeia o stem que o recibo lista e o
   disco perdeu. Se o check cruza a integridade, o `sfx verify` nomeia a integridade que o check já cruza. Hash no disco não é mix ouvida. Sem chave `sha256`. Se a receita recusa que o ok do catálogo seja ouvido, o `ok` do `sfx verify` nomeia o ouvido que a receita já recusa. Cruzou no disco não é o jogo. Sem chave `ouvido`. Se a receita recusa que variante ausente seja lacuna, o `sfx verify` vazio nomeia a lacuna que a receita já recusa. Lista no disco não é mix. Sem chave `lacuna`. Se a receita recusa que nomear o 404 seja mix, o `missing` do `sfx verify` nomeia o 404 que a receita já recusa. Lista no disco não é mix. Sem chave `404`. `sfx summary` lista todos. Se a receita recusa que o acervo vazio seja mix ouvido, o `empty` do `sfx summary` nomeia o acervo que a receita já recusa. Lista no disco não é mix. Sem chave `acervo`. Se a receita recusa que o catálogo vazio seja a busca, o `empty` do `sfx search` nomeia a busca que a receita já recusa. Lista no disco não é mix. Sem chave `busca`. Se o `tools/peak.*` relata o pico do arquivo, o `sfx summary` nomeia o pico que o peak já relata. Relato no disco não é mix ouvida. Sem chave `peak`. Se a receita recusa que a categoria do catálogo seja a camada que o jogo mistura, o `categories[n]` do `sfx summary` nomeia a camada que a receita já recusa. Lista no disco não é mix. Sem chave `camada`. Se a receita recusa que medir alocação com canais em zero seja ouvir, o `quality_bar` do `sfx summary` nomeia a alocação que a receita já recusa. Barra no disco não é mix ouvida. Sem chave `alocação`. Se a receita recusa que o tamanho comprimido meça áudio decodificado, o `local` do `sfx summary` nomeia o comprimido que a receita já recusa. Bytes no disco não são mix. Sem chave `comprimido`. `sfx serve`
   recusa catálogo vazio.
   Com sons no acervo, `sfx serve` abre a página de escuta — se
   `shared/sfx/ui` faltar, o harness gera a lista e nomeia o som
   que o catálogo lista e o disco perdeu. `sfx verify`
   nomeia o som que o catálogo lista e o disco perdeu —
   não despeja errno. Tocar nessa
   página não é mix ouvida no jogo. Arquivo no disco não é mix ouvido. Crescer o acervo é
   `sfx import ARQUIVO --metadata JSON` (ffmpeg); se a receita recusa improvisar licença, o `sfx import` nomeia a improvisação que a receita já recusa. Importar no disco não é licença.    Sem chave `improvisar`. `sfx seed` lê
   `selection.json` local. Se a receita recusa que avaliação do agente seja aprovação do usuário, o `sfx seed` nomeia a aprovação que a receita já recusa. Seed no disco não é mix. Sem chave `aprovação`. `sfx info ID` lê a ficha do acervo ou a
   chave do stem do starter — o recibo que lista um stem e o
   disco perdeu não é id desconhecido; se o inspect já mediu o pico, o `sfx info` nomeia o pico que o inspect já mede.
   Pico no recibo não é mix ouvida. Se a receita recusa que teste técnico de decode aprove o mix, o `sfx info` do acervo nomeia o decode que a receita já recusa. Ficha no disco não é mix ouvida. Sem chave `decode`. Se a receita recusa que arquivo sem papel seja áudio do jogo, o `sfx info` do stem nomeia o lixo que a receita já recusa. Arquivo no disco não é mix. Sem chave `lixo`. `sfx export ID
   --to PASTA` copia bytes e créditos do acervo ou do stem —
   o recibo que lista um stem e o disco perdeu não é id
   desconhecido; exportar não inventa bytes. Se a receita recusa que o export invente bytes, o `sfx export` do stem nomeia a invenção que a receita já recusa. Cópia no disco não é mix. Sem chave `invenção`. Se o export recusa processamento, o `sfx export` nomeia o processamento que o export já recusa. Bytes no disco não são mix ouvida. Sem chave `processamento`. Se a receita recusa que remontar bytes por hash reduza a memória após decodificar, o `sfx export` do acervo nomeia a memória que a receita já recusa. Hash no disco não é o buffer. Sem chave `memória`.
   `sfx copy` leva o stem do starter. Importar e exportar não é
   ouvir. Se a receita recusa que importar e exportar seja ouvir, o `sfx copy` do acervo nomeia o ouvir que a receita já recusa. Cópia no disco não é mix. Sem chave `ouvir`. Se a receita recusa que o arquivo importado esteja sendo consumido, o `record` do `sfx copy` do acervo nomeia o consumido que a receita já recusa. Recibo no disco não é mix. Sem chave `consumido`. Sem 8-bit,
   chiptune, jsfxr ou Kenney arcade como padrão. Leia candidatos e consumidores.
   CREATE exige lacuna explícita. Para trabalho novo sem registro, use
   [o contrato](assets/work.example.json); `check-plan` valida a estrutura, não o mérito. Se o processo recusa garantir o mérito, o `check-plan` nomeia o mérito que o processo já recusa. Forma no disco não é adequação. Sem chave `mérito`. Se o processo recusa que três nomes parecidos bastem, o `check-plan` nomeia os nomes que o processo já recusa. Nome no disco não é a camada. Sem chave `nomes`. Se o processo recusa que o contrato válido garanta obediência, o `contract_valid` do `check-plan` nomeia a obediência que o processo já recusa. Forma no disco não é o processo. Sem chave `obediência`. Se a guia recusa que a checagem seja validador semântico, o `metadata_issues[n]` nomeia o semântico que a guia já recusa. Parse no disco não é o jogo. Sem chave `semântico`.
4. **Arquitetura e fatia jogável.** Ligue intenção/GDD → requisitos/aceite → decisões
   técnicas → tarefas → evidência. Se a mudança afetar responsabilidades, contratos,
   estado/tempo, saves, renderização ou integrações, aplique
   [arquitetura](recipes/architecture.md) (`--focus architecture` ou `--stage tdd`). Se a receita recusa que o harness infira dependências, o `scan` nomeia as dependências que a receita já recusa. Receita no disco não é decisão. Sem chave `dependências`. Se a receita recusa que exemplares locais comprovem comportamento multiplayer, o `scan` nomeia o multiplayer que a receita já recusa. Receita no disco não é sessão real. Sem chave `multiplayer`. Se a receita recusa que a estimativa implícita seja discutível, a área `architecture` do `scan` nomeia a estimativa que a receita já recusa. Receita no disco não é decisão. Sem chave `estimativa`. Se a receita recusa que contexto carregado prove a arquitetura compreendida, o candidato da arquitetura nomeia a compreendida que a receita já recusa. Candidato no disco não é a decisão. Sem chave `compreendida`.
   Implemente uma fatia jogável que atravesse regra, apresentação e conteúdo: perceber
   → decidir → agir → consequência → reinício. Em seguida o feel e o áudio **desse**
   verbo (`--focus feel`, `--focus audio`); título e cores novos não demonstram
   experiência nova. Não acrescente um runtime comum, uma hierarquia de agentes ou IA
   por quadro.
5. **Verificar.** Use os validadores existentes e o cenário real. `verify` registra
   comandos explícitos e logs (scripts de `package.json` ou alvos Cargo; outras engines
   por `--command`). Build verde não comprova diversão, arte, reinício, rede, direitos
   de assets nem aprovação humana. Se o roteiro recusa aprovar a criatividade, o `verify` nomeia a criatividade que o roteiro já recusa. Recibo verde não é aprovação. Sem chave `criatividade`. Se a ambição recusa que o recibo comprove diversão, o `verify` nomeia a diversão que a ambição já recusa. Log no disco não é experiência. Sem chave `diversão`. Se a entrega recusa que o hash comprove o significado, o comando do verify nomeia o significado que a entrega já recusa. Hash no disco não é o critério. Sem chave `significado`. Se a receita recusa que teste unitário de serialização prove conectividade real, o `verify` nomeia a conectividade que a receita já recusa. Recibo verde não é sessão real. Sem chave `conectividade`. O que uma pessoa observou em movimento, uma medição
   de orçamento ou uma decisão de marco entra por `record`, com `role=human` ou
   `role=agent`; avaliação do agente não é aprovação do usuário. Capacidade
   desconhecida permanece desconhecida até ser demonstrada: `context` só sabe dizer
   `mentioned` sobre as oito capacidades conhecidas (pause, reset, seed, observe, act,
   advance, capture, dispose), porque lê arquivos sem executá-los. Quando os testes do
   projeto de fato exercitarem alguma delas, anexe a alegação ao recibo com
   `verify --proves <capacidade>`: sai como `claimed`, com autor, argv e log, nunca
   como verificada; declare só o que os comandos cobrirem. Se o processo recusa que claimed seja verified, o `verify` nomeia a verificação que o processo já recusa. Alegação no disco não é cobertura. Sem chave `verified`. Se a receita recusa que o registro declarado prove suporte real, o `capabilities[n]` do `verify` nomeia o suporte que a receita já recusa. Registro no disco não é o consumidor. Sem chave `suporte`. `experience_status`
   continua `not_assessed` até haver observação em movimento.
6. **Comparar, registrar, continuar.** Compare antes/depois em condições equivalentes
   e em movimento quando houver efeito visual. Corrija regressões, registre decisões e
   hipóteses descartadas, cumpra `continuity.before_close` e
   `documentation.before_close`. Não promova scaffold a slice nem slice a jogo
   concluído. Não chame o recorte de AAA — nem de “quase AAA” — se o perfil em
   `finish` (núcleo; produto se a escala pedir; promessas só se o brief as tiver) não
   foi observado; na slice ou em “está AAA?”, leia `finish` e
   [o guia](references/aaa-checklist.md) e grave no canônico — completar linhas não
   certifica e `N/A` exige motivo. Se a guia recusa preencher o checklist, o `context` nomeia o checklist que a guia já recusa preencher. Guia no disco não é observação. Sem chave `checklist`. Se a ambição recusa que o checklist completo seja nota AAA, o `finish` nomeia o grau que a ambição já recusa. Guia no disco não é observação. Sem chave `grau`. Não publique nem delegue sem autorização aplicável.
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
   e diz o piso, `next` propõe subir a dimensão pelo nome. Se a prosa declara o mínimo, o `bar` nomeia o mínimo que a barra já declara. Degrau no disco não é acabamento observado. Sem chave `mínimo`. Se a barra recusa que o degrau seja prazo, o `bar` nomeia os prazos que a barra já recusa. Linha no disco não é calendário. Sem chave `prazos`. Se a barra recusa que o nome seja uma das dez, o `bar` nomeia a dimensão que a barra já recusa. Linha no disco não é acabamento. Sem chave `dimensão`. Se a barra recusa que dimensão não declarada seja dimensão alta, o `undeclared` do `bar` nomeia a alta que a barra já recusa. Linha no disco não é acabamento. Sem chave `alta`. Se a barra recusa que a declaração seja um selo, o `sources` do `bar` nomeia o selo que a barra já recusa. Linha no disco não é acabamento. Sem chave `selo`. Se a barra recusa que o piso seja uma nota, o `floor` do `bar` nomeia a nota que a barra já recusa. Linha no disco não é acabamento. Sem chave `nota`. Se a barra recusa que a tabela otimista seja observação, o `at_floor` do `bar` nomeia a otimista que a barra já recusa. Linha no disco não é acabamento. Sem chave `otimista`. Se o mapa recusa que o checklist seja um score, o `bar` nomeia o score que o mapa já recusa. Mapa no disco não é acabamento. Sem chave `score`. Se a barra recusa que duas linhas discordantes se resolvam por precedência, o `conflicts[n]` do `bar` nomeia a precedência que a barra já recusa. Linha no disco não é acabamento. Sem chave `precedência`. Se a barra recusa promover o degrau, o `context` nomeia a promoção que a barra já recusa. Guia no disco não é acabamento. Sem chave `promove`. Se a receita recusa que AAA seja orçamento ou tamanho de equipe, o `production_bar` nomeia a equipe que a receita já recusa. Receita no disco não é acabamento. Sem chave `equipe`. Se a barra recusa que o degrau sem condição seja observação, o `dimensions[n]` do `production_bar` nomeia a opinião que a barra já recusa. Linha no disco não é acabamento. Sem chave `opinião`. Se o onboard recusa que tempo de sessão seja interesse, o `dimensions[pacing]` do `production_bar` nomeia o interesse que o onboard já recusa. Relógio no disco não é o interesse. Sem chave `interesse`. Nenhum comando atribui
   degrau; ao declarar um, declare dispositivo, versão, cena e quem observou.
   **A barra descreve, o gate recusa.** [Os dez gates](references/gates.md) formalizam
   as linhas “Pronto para…” do ciclo: ao pedir a próxima permissão, declare uma linha
   por critério com `met`/`unmet`/`waived`/`out_of_scope` e o que sustenta o estado; `gate <projeto>`
   lê. Se a tabela declara o gate, o `gate` nomeia o gate que a tabela já declara. Linha no disco não é passagem concedida. Sem chave `gate`. Se o roteiro recusa que o silêncio seja aprovação, o `gate` nomeia o silêncio que o roteiro já recusa. Linha vazia no disco não é passagem. Sem chave `silêncio`. Se o roteiro recusa que a lista de entrega seja um gate, o `sources` do `gate` nomeia a lista que o roteiro já recusa. Linha no disco não é passagem. Sem chave `lista`. Se o roteiro recusa que a declaração seja passed, o `held_by_declaration` do `gate` nomeia o passou que o roteiro já recusa. Tabela no disco não é passagem. Sem chave `passou`. Se o roteiro recusa que must_meet seja dispensável, o `gate` nomeia a dispensa que o roteiro já recusa. Linha no disco não é passagem. Sem chave `dispensa`. Se o roteiro recusa que fora de escopo seja dispensa, o `gate` nomeia o escopo que o roteiro já recusa. Linha no disco não é passagem. Sem chave `escopo`. Se a guia recusa que código que compila prove a hipótese, o `gate` nomeia a hipótese que a guia já recusa. Linha no disco não é o experimento. Sem chave `hipótese`. Se o fluxo recusa que um teste local concluído seja lançamento, o `gate` nomeia o lançamento que o fluxo já recusa. Linha no disco não é outra máquina. Sem chave `lançamento`. Se a receita recusa que a slice sem repeatability esteja pronta para ampliar, o `gate` scale nomeia a repeatability que a receita já recusa. Linha no disco não é o próximo trecho. Sem chave `repeatability`. Se o roteiro recusa que abandonar seja falha do gate, o `gate` nomeia o abandono que o roteiro já recusa. Roteiro no disco não é passagem. Sem chave `abandono`. Critério sem linha é pendente. As três saídas são passar, cortar escopo e
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
   Nomear não devolve o arquivo.    Nomeia `form` e `fields`. `--declare` escreve
   o sidecar `.credits.txt`. Sem `then`. Não valida licença. Recibo no disco
   não é licença válida. Se a receita recusa que o recibo comprove a consistência do gerador, o `fields` do `origins --declare` nomeia a consistência que a receita já recusa. Recibo no disco não é o asset. Sem chave `consistência`. JSON sem origem, autor e licença não declara.
   Sidecar sem os três rótulos também não.
   Se o sidecar declara `Consumidor:`, o `origins` nomeia o consumidor que o sidecar já declara. Consumidor no disco não é licença válida. Sem chave `consumer`. Se o roteiro recusa que o sidecar sem rótulos declare, o `origins` nomeia os rótulos que o roteiro já recusa. Recibo no disco não é licença. Sem chave `rótulos`. Se o roteiro recusa que o recibo presente seja licença válida, o `receipts` do `origins` nomeia a válida que o roteiro já recusa. Arquivo no disco não é a concessão. Sem chave `válida`. Se a guia recusa que o embarcado sem recibo seja licença conhecida, o `undeclared` do `origins` nomeia a desconhecida que a guia já recusa. Arquivo no disco não é a concessão. Sem chave `desconhecida`. Se o molde recusa que o crédito seja licença válida, o `form` do `origins` nomeia o crédito que o molde já recusa. Arquivo no disco não é a concessão. Sem chave `crédito`. Se o roteiro recusa que o JSON sem os três campos declare, o `fields` do `origins` nomeia os três que o roteiro já recusa. Recibo no disco não é a concessão. Sem chave `três`. Se o roteiro recusa que nomear devolva o arquivo, o `missing` do `origins` nomeia o devolve que o roteiro já recusa. Recibo no disco não é a concessão. Sem chave `devolve`. Se o roteiro recusa que a varredura incompleta seja a concessão, o `truncated` do `origins` nomeia a varredura que o roteiro já recusa. Recorte no disco não é a concessão. Sem chave `varredura`. Se a receita recusa que o conteúdo baixado receba uma licença nova pelo simples reuso, o `embedded` do `origins` nomeia a nova que a receita já recusa. Arquivo no disco não é a concessão. Sem chave `nova`.
   Arquivo sem recibo conta como licença
   desconhecida, e `next` aponta `--declare` antes de seguir.
   **`craft <projeto>`** lê checklists de ofício (paleta, perdão, percentil,
   regra de parada) — conformidade com o que o projeto declarou, sem limiar
   importado. Se a tabela declara saída de escopo, o `craft` nomeia a saída de escopo que a tabela já declara. Linha no disco não é ofício observado. Sem chave `out_of_scope`. Se a pesquisa recusa ser escada de acabamento, o `craft` nomeia a escada que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `escada`. Se a pesquisa recusa ser um conjunto de gates, o `sources` do `craft` nomeia o conjunto que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `conjunto`. Se a pesquisa recusa que a pendência seja medição em jogo, o `pending` do `craft` nomeia a medição que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `medição`. Se a pesquisa recusa que o número sem definição seja critério, o `craft` nomeia a definição que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `definição`. Se o mapa recusa que o número com casa decimal e sem origem seja mais preciso, o `craft` nomeia o preciso que o mapa já recusa. Mapa no disco não é ofício observado. Sem chave `preciso`. Se o craft recusa que shape confirmado seja licença para pular feel e áudio, o `craft` nomeia o pular que o craft já recusa. Confirmação no disco não é o ofício. Sem chave `pular`. Se o craft recusa que uma confirmação autorize delegar, o `craft` nomeia o delegar que o craft já recusa. Confirmação no disco não é delegar. Sem chave `delegar`. `observed` é sempre falso. Só levanta o gate que o projeto pediu.
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
   `copy.json`; a frase não muda o verbo — e a porta, se o manifesto a declara; se o manifesto declara o relógio, o `guide` nomeia o relógio que o manifesto já declara. Frase no disco não é partida observada. Sem chave `speed`. Se o roteiro recusa que o mural seja onboarding, o `guide` nomeia o onboarding que o roteiro já recusa. Texto no disco não é a primeira ação. Sem chave `onboarding`. Se a receita recusa que o screenshot comprove feel, o `guide` nomeia o screenshot que a receita já recusa. Recibo no disco não é peso percebido. Sem chave `screenshot`. Se o processo recusa que o comando abra o jogo, o `guide` nomeia a abertura que o processo já recusa. Nome no disco não é partida. Sem chave `abertura`. Se a receita recusa que passos textuais sejam uma garantia de execução, o `guide` nomeia os passos que a receita já recusa. Texto no disco não é a partida. Sem chave `passos`. Se a receita recusa que mostrar a estrutura seja a slice, o then do `guide` nomeia a estrutura que a receita já recusa. Mapa no disco não é a fatia. Sem chave `estrutura`. Se a receita recusa que estar em run prove estar livre, o ciclo nomeia o livre que a receita já recusa. Estado no disco não é a janela. Sem chave `livre`. Se a receita recusa que o tap seja o avanço, o ciclo nomeia o tap que a receita já recusa. Polegar no disco não é o dash. Sem chave `tap`. Se a receita recusa que o lock seja o descanso, o ciclo nomeia o lock que a receita já recusa. Lock no disco não é o descanso. Sem chave `lock`. `then` nomeia par, look, chuva e voz quando o projeto — ou o
   starter, se o destino ainda não existe — as declara; se declara
   `session`, `then` a aponta e o prompt a nomeia; se o disco tem last-run com seed,
   `then` aponta a partida (número, chuva e look quando o candidato os nomeia) e o convite; nomear o endereço não observa; se o serve tenta abrir o navegador, o prompt nomeia a tentativa; sem o marcador, pede Abrir; nomear não abre; `executed` fica `false`. `runtime` lê o `node` do PATH se o play pede npm ou node. O autor do
   `note` é sugestão do git ou do ambiente, não quem jogou. Nomear o
   ofício não pinta. `next` fica em `then.lost`.
   **`start [<projeto>]`** cria se o destino estiver livre e devolve
   `open` (= `play`) + `then.note` e os mesmos `steps` do `guide`, com
   o passo 1 feito. Se o `tools/new-pair.*` nasce look e chuva, o `start` nomeia o par que o pair já nasce. Ferramenta no disco não é alguém de fora. Sem chave `pair` no recibo. Se a receita recusa que nove arquivos vazios aumentem a qualidade, o `start` nomeia os vazios que a receita já recusa. Arquivo no disco não é a fatia. Sem chave `vazios`. Se a receita recusa que título e cores novos sejam experiência, o then do start nomeia a experiência que a receita já recusa. Nome no disco não é o ciclo jogado. Sem chave `experiência`. Se a receita recusa que o start execute e observe, o `created` do `start` nomeia o executa que a receita já recusa. Pasta no disco não é a partida. Sem chave `executa`.    Sem caminho, `--idea` nomeia e cria a pasta —
   ao lado do framework se o start corre de dentro desta árvore.
   Se a receita recusa que nomear a pasta grave a frase, o `named` do `start` nomeia a frase que a receita já recusa. Slug no disco não é o documento. Sem chave `frase`.
   `guide --idea` continua só no comando, não no disco. Se o README recusa que o guide crie o projeto, o `exists` do `guide` nomeia o projeto que o README já recusa. Destino no disco não é criação do mapa. Sem chave `projeto`. Se a receita recusa que o diretório atual seja o ciclo jogado, o `here` do `guide` nomeia o aqui que a receita já recusa. Pasta no disco não é a partida. Sem chave `aqui`. Se o starter declara o verbo e as teclas, o
   prompt as nomeia — inclusive a porta, o cluster de uma mão, o toque, o
   controle e as queries de look, chuva, par, seed, relógio e convite, se o starter as declara. Se o
   projeto declara `pair`/`look`/`table`/`sfx`, `then` as nomeia; se o disco
   tem last-run com seed, `then` aponta a partida e o convite; depois de um
   recibo, o prompt aponta o segundo ciclo. O `prompt` também sai em
   stderr; o JSON fica no stdout. Não executa o jogo. `--idea` entra na
   abertura se houver `data/copy.json`. O `start` não planta os rascunhos;
   `--docs` os cria. rascunho plantado não é GDD. Se a receita recusa que o rascunho plantado seja GDD, o `documents` do `init` nomeia o GDD que a receita já recusa. Rascunho no disco não é o documento. Sem chave `gdd`. O `init` continua plantando e agora devolve o mesmo
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
   Sem `then.playtest`. Nomear o leitor não observa. Se a receita recusa que nomear o leitor observe, o `observations` do `playtest` nomeia o recibo que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `recibo`. `note`, `next`, `feel` e
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
   Arquivo no disco não é mix ouvida. Sem chave `sfx`. Se o `tools/wav.*` lê o PCM, o `roles` nomeia o PCM que o wav já lê. Bytes no disco não são mix ouvida. Sem chave `wav`. Se a receita recusa que o heap JavaScript sozinho meça PCM ou VRAM, o `roles` nomeia o heap que a receita já recusa. Contador no disco não é o mix. Sem chave `heap`. Se a receita recusa que o arquivo ausente seja silêncio deliberado, o `empty` do `roles` nomeia o ausente que a receita já recusa. Lista no disco não é mix. Sem chave `ausente`. Se a receita recusa que o catálogo completo entre, o `catalog_exists` do `roles` nomeia o entra que a receita já recusa. Acervo no disco não é mix. Sem chave `entra`. Se a receita recusa que desconectar, liberar e fechar comprovem coleta imediata, o `sources` do `roles` nomeia a imediata que a receita já recusa. Sinal no disco não é o sistema. Sem chave `imediata`. Se a receita recusa que áudio AAA seja quantidade de arquivos, o `roles` nomeia a quantidade que a receita já recusa. Lista no disco não é mix. Sem chave `quantidade`. Se a receita recusa que o número no panner seja mix, o papel do x do campo nomeia o panner que a receita já recusa. Número no disco não é mix. Sem chave `panner`. Se a receita recusa que retomar, fila e paralelo sejam mix, o `roles` nomeia o retomar que a receita já recusa. Pedido no disco não é mix. Sem chave `retomar`. `--fill` sugere o acervo ou a ficha
   do stem do starter; `--apply` copia o id do acervo ou o stem
   do starter com créditos — e recoloca o WAV se o recibo já está
   e origem e licença casam. `--apply` não é mix ouvido. Se a receita recusa que o apply seja mix ouvido, o `applied` do `roles --fill` nomeia o aplica que a receita já recusa. Cópia no disco não é mix. Sem chave `aplica`. `sfx copy` continua o caminho explícito. Se o sidecar declara licença, o `sfx copy` nomeia os créditos que o copy já leva. Créditos no disco não são mix ouvida. Sem chave `sidecar`. Crescer o acervo é `sfx import` / `sfx seed`
   (ffmpeg); `sfx info` lê a ficha do acervo ou a chave do stem
   do starter — o recibo que lista um stem e o disco perdeu não
   é id desconhecido; se o inspect já mediu o pico, o `sfx info` nomeia o pico que o inspect já mede.
   Pico no recibo não é mix ouvida. Se a receita recusa que teste técnico de decode aprove o mix, o `sfx info` do acervo nomeia o decode que a receita já recusa. Ficha no disco não é mix ouvida. Sem chave `decode`.    `sfx verify` nomeia os stems sem cruzar o que não
   existe e nomeia o stem que o recibo lista e o disco perdeu. Se o check cruza a integridade, o `sfx verify` nomeia a integridade que o check já cruza. Hash no disco não é mix ouvida. Sem chave `sha256`. Se a receita recusa que o ok do catálogo seja ouvido, o `ok` do `sfx verify` nomeia o ouvido que a receita já recusa. Cruzou no disco não é o jogo. Sem chave `ouvido`. Se a receita recusa que nomear o 404 seja mix, o `missing` do `sfx verify` nomeia o 404 que a receita já recusa. Lista no disco não é mix. Sem chave `404`.
   `sfx verify` nomeia o som que o catálogo lista e o disco
   perdeu — não despeja errno;
   `sfx export` copia bytes e
   créditos e nomeia o stem que o recibo lista e o disco perdeu —
   exportar não inventa bytes. Se a receita recusa que o export invente bytes, o `sfx export` do stem nomeia a invenção que a receita já recusa. Cópia no disco não é mix. Sem chave `invenção`. Se o export recusa processamento, o `sfx export` nomeia o processamento que o export já recusa. Bytes no disco não são mix ouvida. Sem chave `processamento`. Se a receita recusa que remontar bytes por hash reduza a memória após decodificar, o `sfx export` do acervo nomeia a memória que a receita já recusa. Hash no disco não é o buffer. Sem chave `memória`. Importar e exportar não é ouvir. Se a receita recusa que importar e exportar seja ouvir, o `sfx copy` do acervo nomeia o ouvir que a receita já recusa. Cópia no disco não é mix. Sem chave `ouvir`. Se a receita recusa que o arquivo importado esteja sendo consumido, o `record` do `sfx copy` do acervo nomeia o consumido que a receita já recusa. Recibo no disco não é mix. Sem chave `consumido`. `heard` é sempre falso. Papel vazio
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
   Conta no disco não é peso percebido. Sem chave `probe`. Se o laço senta a guarda, o `feel` nomeia o sit que a guarda já senta. Pose no disco não é peso percebido. Sem chave `bank`. Se o laço emite o término, o `feel` nomeia o land que o dash já emite. Pose no disco não é peso percebido. Sem chave `land`. Se a receita recusa que o autor sugerido seja quem jogou, o `feel` nomeia o autor que a receita já recusa. Recibo no disco não é sessão. Sem chave `autor`. Se a receita recusa que o valor seja constante universal, o `feel` nomeia o universal que a receita já recusa. Número no disco não é lei. Sem chave `universais`. Se a receita recusa que velocidade não nula prove a posição, o item da constante nomeia a posição que a receita já recusa. Número no disco não é a pose. Sem chave `posição`. Se o README recusa que a constante nomeada seja peso percebido, o `constants` do `feel` nomeia o peso que o README já recusa. Número no disco não é o verbo. Sem chave `peso`. Se a receita recusa que o coil seja janela de hit, o `constants` do `feel` nomeia a janela que a receita já recusa. Coil no disco não é a janela. Sem chave `janela`. Se a receita recusa que achar o jogo seja ter sentido, o `unobserved` do `feel` nomeia o sentido que a receita já recusa. Arquivo no disco não é o verbo. Sem chave `sentido`. Se a receita recusa que a guarda seja janela de hit, o `unobserved` do `feel` nomeia a guarda que a receita já recusa. Guarda no disco não é a janela. Sem chave `guarda`. Se a receita recusa que um tween genérico sem dono seja feel reutilizável, o `feel` nomeia o tween que a receita já recusa. Receita no disco não é peso percebido. Sem chave `tween`. Se a receita recusa que guardar no hitstop seja engolido, o `feel` nomeia o engolido que a receita já recusa. Hitstop no disco não é o perdão. Sem chave `engolido`. Se a receita recusa que corrigir a regra substitua o feel, o `feel` nomeia a regra que a receita já recusa. Regra no disco não é o feel. Sem chave `regra`. Se a receita recusa que esses testes demonstrem qualidade artística, o then do `feel` nomeia a artística que a receita já recusa. Número no disco não é direção. Sem chave `artística`. Se a receita recusa que captura no disco seja sessão observada, o `sources` do `feel` nomeia a captura que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `captura`. Se a receita recusa que o soltar no disco seja sessão observada, o `observations` do `feel` nomeia o soltar que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `soltar`. Traço no disco não é peso percebido. Lê o
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
   Sem `then`. recibo com os quatro não é achado. Se a receita recusa que o recibo com os quatro seja achado, o `finding` do `note` nomeia o achado que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `achado`. Recibo sem os quatro não é achado. Se a receita recusa que o recibo sem os quatro seja achado, o `fields` do `record --kind observation` nomeia a impressão que a receita já recusa. Recibo no disco não é playtest. Sem chave `impressão`. Os quatro no disco
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
   Gancho no disco não é aba fechada. Sem chave `beforeunload`. Se o disco verifica a gravação, o `save` nomeia a gravação que o storage já verifica. Escrita no disco não é aba fechada. Sem chave `storage`. Se a receita recusa que o estágio seja atomicidade, o `save` nomeia a atomicidade que a receita já recusa. Estágio no disco não é substituição. Sem chave `atomicidade`. Se a receita recusa que um único número una a versão do conteúdo e a do save, o `save` nomeia os contratos que a receita já recusa. Schema no disco não é a história. Sem chave `contratos`. Se a receita recusa que o hold sem o número invente ensino feito, o `save` nomeia o ensino que a receita já recusa. Hold no disco não é o ensino. Sem chave `ensino`. Se a receita recusa que listar o fonte prove a cadeia inteira, o `sources` do `save` nomeia a cadeia que a receita já recusa. Arquivo no disco não é a migração. Sem chave `cadeia`. Se a receita recusa que o aviso volátil seja aba fechada, o `warnings` do `save` nomeia o volátil que a receita já recusa. Arquivo no disco não é a aba. Sem chave `volátil`. Se a receita recusa que o nomear seja trusted, o `warned` do `save` nomeia a confiança que a receita já recusa. Arquivo no disco não é a aba. Sem chave `confiança`. Se a receita recusa que query no disco seja aba fechada, o `warned` do `save` nomeia a query que a receita já recusa. Endereço no disco não é a aba. Sem chave `query`. Se a receita recusa que o harness abra o save, o `used` do `save` nomeia o abre que a receita já recusa. Texto no disco não é a aba. Sem chave `abre`. Se a receita recusa que ouvir seja aba fechada, o `used` do `save` nomeia a audição que a receita já recusa. Ouvir no disco não é a aba. Sem chave `audição`. Se a receita recusa que o número no disco seja aba fechada, o `used` do `save` nomeia a aba que a receita já recusa. Número no disco não é a aba. Sem chave `aba`. Se a receita recusa que uma versão sem migração preserve o progresso, o `versioned` do `save` nomeia a versão que a receita já recusa. Schema no disco não é a atualização. Sem chave `versão`. Se a receita recusa que o armazenamento sem versão seja o formato, o `unversioned` do `save` nomeia o formato que a receita já recusa. Disco sem schema não é o contrato. Sem chave `formato`. A receita
   de persistência e alcance ensina o canvas da porta e do fim; a
   pausa não.    Na porta e no fim o canvas nomeia a lacuna do som
   que o painel já mostra. Se a casca declara `:focus-visible`,
   o `access` nomeia o foco que a receita já pede. Outline no
   disco não é sessão com o teclado. Se o `tools/contrast.*`
   amostra o stub, o `access` nomeia o contraste. Stub no
   disco não é sessão com o modo ativo. Sem chave `contrast`. Se a receita recusa que tamanho CSS igual garanta pixels, o `access` nomeia os pixels que a receita já recusa. Tamanho no disco não é o buffer. Sem chave `pixels`. Se a receita recusa que se declare cobertura não observada, o `missing` do `access` nomeia a cobertura que a receita já recusa. Lista no disco não é sessão. Sem chave `cobertura`. Se a receita recusa que a chave no fonte seja sessão, o `declared` do `access` nomeia a fonte que a receita já recusa. Chave no disco não é o modo ativo. Sem chave `fonte`. Se a receita recusa que a verificação automática substitua uma sessão, o `access` nomeia a automática que a receita já recusa. Checagem no disco não é o modo ativo. Sem chave `automática`.
   Se o live anuncia o perigo à frente, o `access` nomeia o perigo que o live já anuncia.
   Texto no DOM não é sessão. Sem chave `threat`.
   Se o disco declara `paintCommands`, o `access` nomeia as teclas que a tabela já lista.
   Tabela no disco não é sessão. Sem chave `commands`.
   Se a porta lê a legenda que o mixer ainda guarda, o `access` nomeia a legenda que a porta já lê. Texto no disco não é sessão. Sem chave `caption`. Se a receita recusa que o número na legenda seja mix, a opção `captions` do `access` nomeia o número que a receita já recusa. Número no disco não é mix. Sem chave `número`. Se a receita recusa que a legenda prove o jogo completável sem áudio, a opção `captions` do `access` nomeia o mudo que a receita já recusa. Texto no disco não é a partida muda. Sem chave `mudo`. Se a receita recusa que o pulso seja sessão no controle, a opção `haptics` do `access` nomeia o controle que a receita já recusa. Pulso no disco não é sessão. Sem chave `controle`. Se a receita recusa que o botão seja sessão, a opção `remap` do `access` nomeia o botão que a receita já recusa. Botão no disco não é sessão. Sem chave `botão`. Se a receita recusa que o movimento reduzido apague a causa, a opção `reduced_motion` do `access` nomeia a causa que a receita já recusa. Causa no disco não é sessão. Sem chave `causa`. Se a receita recusa que o fundo neutro seja o pior caso, a opção `high_contrast` do `access` nomeia o neutro que a receita já recusa. Neutro no disco não é sessão. Sem chave `neutro`. Se a receita recusa que o estado dependa só da cor, a opção `colorblind` do `access` nomeia o ícone que a receita já recusa. Ícone no disco não é sessão. Sem chave `ícone`. Se a receita recusa que completar o jogo peça as duas mãos, a opção `one_hand` do `access` nomeia a mão que a receita já recusa. Mão no disco não é sessão. Sem chave `mão`. Se a receita recusa que a assistência esconda conteúdo, a opção `assist` do `access` nomeia o oculto que a receita já recusa. Oculto no disco não é sessão. Sem chave `oculto`. Se a receita recusa que a precisão fique sem alternativa, a opção `game_speed` do `access` nomeia a precisão que a receita já recusa. Precisão no disco não é sessão. Sem chave `precisão`. Se a receita recusa que a escala substitua a tipografia, a opção `ui_scale` do `access` nomeia a tipografia que a receita já recusa. Tipografia no disco não é sessão. Sem chave `tipografia`. Se a receita recusa que o overlay substitua o leitor, a opção `live` do `access` nomeia o leitor que a receita já recusa. Overlay no disco não é sessão. Sem chave `leitor`. Se a pesquisa recusa que acessibilidade seja gate de certificação, o `access` nomeia a certificação que a pesquisa já recusa. Opção no disco não é certificação. Sem chave `certificação`. Se a receita recusa que opção sem consumidor seja opção, o `access` nomeia a opção que a receita já recusa. Chave no disco não é alcance. Sem chave `opção`.
   Texto no disco não é mix ouvido.
   Nomear não é
   `trusted`. Trocar no stub não é sessão observada.
   Se o `tools/budget.*` declara `title.attract`, o `budget`
   nomeia a porta que a receita já cronometra. Stub no disco
   não é dispositivo. Sem chave `door`. Se o `tools/size.*`
   declara sem teto, o `budget` nomeia os bytes que o size já relata.
   Bytes no disco não são o quadro medido. Sem chave `size`. Se o `tools/budget.*` relata o pior percentil, o `budget` nomeia o percentil que a receita já pede. Se a receita recusa que um jogo estável a 30 seja instável, o `budget` nomeia o estável que a receita já recusa. Média no disco não é o quadro. Sem chave `estável`.
   Relato no disco não é dispositivo. Sem chave `percentile`.
   Se a receita recusa que custos de build, compilação aquecida e serialização sejam FPS, o `files` do `budget` nomeia o fps que a receita já recusa. Custo no disco não é o quadro. Sem chave `fps`. Se a receita recusa que uma melhoria visual seja otimização, o `receipts` do `budget` nomeia a otimização que a receita já recusa. Recibo no disco não é os dois lados. Sem chave `otimização`.    Se a receita recusa que a ferramenta de medição deixe o resultado intacto, o `scripts` do `budget` nomeia o resultado que a receita já recusa. Script no disco não é o quadro limpo. Sem chave `resultado`. Se a receita recusa que o harness execute a medição, o `declared` do `budget` nomeia a medida que a receita já recusa. Script no disco não é o quadro. Sem chave `medida`. Se a receita recusa que sem orçamento exista rápido o suficiente, o `expected` do `budget` nomeia o suficiente que a receita já recusa. Pacote no disco não é o quadro. Sem chave `suficiente`. Se a receita recusa que o pacote sem orçamento seja o dispositivo, o `unbudgeted` do `budget` nomeia o dispositivo que a receita já recusa. Manifesto no disco não é o quadro medido. Sem chave `dispositivo`.
   `verified`/`trusted`/`measured` são sempre falsos.
   Falta no disco entra no `next` antes dos rascunhos.
   **`art` / `content` / `ship`** leem paleta ou art-bible vigente, mesas
   de chuva (`intervalTicks` e `fallSpeed` em data/tables/content), conteúdo
   fora do código (`palettes.json` e `tokens.json` não extraem) e passo de empacotar. Se o
   `tools/new-look.*` nasce o look, o `art` nomeia o look que o disco já nasce.
   Ferramenta no disco não é comparação em movimento. Sem chave `look`. Se o look recusa contraste, o `art` nomeia o contraste que o look já recusa. Alcance no disco não é comparação em movimento. Sem chave `contrast`. Se o canvas declara `drawTelegraph`, o `art` nomeia o trilho que o telegraph já marca.
   Marca no disco não é comparação em movimento. Sem chave `telegraph`. Se o canvas declara `drawVignette`, o `art` nomeia a vinheta que o recorte já marca. Recorte no disco não é comparação em movimento. Sem chave `vignette`. Se o sistema recusa que a paleta compartilhada seja o contrato, o `art` nomeia a paleta que o sistema já recusa. Lista no disco não é contrato. Sem chave `paleta`. Se a receita recusa que importação sem erro comprove aparência equivalente, o `art` nomeia a aparência que a receita já recusa. Importar no disco não é o renderer. Sem chave `aparência`. Se a receita recusa que uma correção local valide o enquadramento, o `art` nomeia o enquadramento que a receita já recusa. Correção no disco não é o conjunto. Sem chave `enquadramento`. Se a receita recusa que câmera próxima e geometria numericamente correta provem leitura, o `art` nomeia a geometria que a receita já recusa. Número no disco não é a silhueta. Sem chave `geometria`. Se a receita recusa que o lean seja punch, o `art` nomeia o punch que a receita já recusa. Lean no disco não é o punch. Sem chave `punch`. Se a receita recusa que a qualidade visual aprovada seja moeda de troca por número, o `manifests` do `art` nomeia a moeda que a receita já recusa. Manifesto no disco não é comparação. Sem chave `moeda`. Se a receita recusa que paleta no código ou em palettes.json seja direção consistente, o `sources` do `art` nomeia a direção que a receita já recusa. Arquivo no disco não é comparação. Sem chave `direção`. Se a receita recusa que o rascunho do init conte, o `bible` do `art` nomeia o rascunho que a receita já recusa. Arquivo no disco não é comparação. Sem chave `rascunho`. Se a receita recusa que o art-bible com marcador de rascunho seja comparação, o `bible_draft` do `art` nomeia o esboço que a receita já recusa. Arquivo no disco não é o quadro. Sem chave `esboço`. Se a receita recusa que a mesa seja volume, o `art` nomeia o volume que a receita já recusa. Lista no disco não é comparação. Sem chave `volume`. Se a receita recusa que a mesa no disco seja comparação em movimento, o `rains` do `art` nomeia o movimento que a receita já recusa. Mesa no disco não é o quadro. Sem chave `movimento`. Se a receita recusa que isso seja direção consistente, o `bible_current` do `art` nomeia o vigente que a receita já recusa. Arquivo no disco não é comparação. Sem chave `vigente`. Se o disco declara `listMoods`, o `content` nomeia o par. Nome no disco não é volume. Sem chave `moods`. Se a receita recusa que dusk e calm sejam volume, o `content` nomeia a chuva que a receita já recusa. Chuva no disco não é volume. Sem chave `chuva`. Se o `tools/new-table.*` nasce a mesa, o `content` nomeia a mesa que o disco já nasce. Ferramenta no disco não é volume. Sem chave `table`. Se o disco declara `migrateTable`, o `content` nomeia a migração que as mesas já compartilham. Arquivo no disco não é volume. Sem chave `migrate`. Se a receita recusa que mais módulos provem a composição, o `content` nomeia a composição que a receita já recusa. Arquivo no disco não é o mundo. Sem chave `composição`. Se a receita recusa que a variação de material substitua detalhe funcional de forma, o `content` nomeia o material que a receita já recusa. Material no disco não é a forma. Sem chave `material`. Se a receita recusa que o tamanho codificado meça custo decodificado ou GPU, o `content` nomeia o codificado que a receita já recusa. Arquivo no disco não é o quadro. Sem chave `codificado`. Se a receita recusa que o arquivo de dados seja volume, o `files` do `content` nomeia os dados que a receita já recusa. Arquivo no disco não é volume. Sem chave `dados`. Se a receita recusa que o baixado seja o consumido, o `external` do `content` nomeia o baixado que a receita já recusa. Arquivo no disco não é o recurso integrado. Sem chave `baixado`. Se a receita recusa que o conteúdo no código escale, o `inline` do `content` nomeia o código que a receita já recusa. Código no disco não é volume. Sem chave `código`. Se `dist/VERSION.json` existe,
   `ship` relata nome e versão. Se `dist/` de um jogo web existe, relata
   árvore e HEAD. `consistent`/`enough`/`shipped`/`elsewhere` são
   sempre falsos. Sem declaração, o `next` nomeia `art.missing`,
   `content.inline` e `ship.unpacked` antes dos rascunhos. Árvore
   incompleta é `ship.incomplete`; artefato de outro commit é `ship.stale`.
   Se a receita recusa que o HEAD diferente seja outra máquina, o `stale` do `ship` nomeia o velho que a receita já recusa. Arquivo no disco não é outra máquina. Sem chave `velho`.
   Se a receita recusa que a árvore sem os quatro seja jogável, o `incomplete` do `ship` nomeia o jogável que a receita já recusa. Arquivo no disco não é outra máquina. Sem chave `jogável`.
   Nomeia a árvore que perdeu o `src/` que o projeto já tem. Se o
   `tools/size.*` declara sem teto, o `ship` nomeia o tamanho. Bytes
   no disco não são outra máquina. Sem chave `size`. Se o
   `tools/serve.*` nomeia a árvore exportada, o `ship` nomeia o banner que o serve já imprime.
   Banner no disco não é outra máquina. Sem chave `serve`. Se o `tools/export.*` declara o empacote, o `ship` nomeia o passo que o export já declara.
   Empacotar no disco não é outra máquina. Sem chave `export`. Se o `tools/export.*` recusa `file://`, o `ship` nomeia o file:// que o export já recusa. Recusar no disco não é outra máquina. Sem chave `file`. Se a receita recusa que a identidade seja outra máquina, o `tree` do ship nomeia a identidade que a receita já recusa. Árvore no disco não é entrega. Sem chave `identidade`. Se a receita recusa que abrir o menu ou obter um ZIP comprove portabilidade, o `tree` do ship nomeia a portabilidade que a receita já recusa. ZIP no disco não é o destino. Sem chave `portabilidade`. Se a receita recusa que o teste no editor demonstre o jogo exportado, o `artifact` do ship nomeia o editor que a receita já recusa. Manifesto no disco não é o jogo exportado. Sem chave `editor`. Se a receita recusa que uma pasta de build existente corresponda à fonte atual, o `artifact` do ship nomeia a atual que a receita já recusa. Manifesto no disco não é o HEAD. Sem chave `atual`. Se a receita recusa que o JSON legível seja outra máquina, o `readable` do artifact do `ship` nomeia o legível que a receita já recusa. Manifesto no disco não é outra máquina. Sem chave `legível`. Se a receita recusa que link não listado comprove controle de acesso, o `ship` nomeia o acesso que a receita já recusa. Link no disco não é outra máquina. Sem chave `acesso`. Se a receita recusa que o tamanho sem teto seja o orçamento de entrega, o `ship` nomeia o teto que a receita já recusa. Relato no disco não é a plataforma alvo. Sem chave `teto`. Se a receita recusa que a CI seja a primeira execução, o `ci` do `ship` nomeia a primeira que a receita já recusa. Fluxo no disco não é instalação limpa. Sem chave `primeira`. Se a receita recusa que emulação e redimensionar uma janela substituam a plataforma real, o `scripts` do `ship` nomeia a emulação que a receita já recusa. Script no disco não é o dispositivo. Sem chave `emulação`. Nomear não
   devolve o jogo. Árvore completa no HEAD atual ganha `artifact_open` e o
   `next` nomeia `ship.artifact_open`. Nomear não executa. Se a receita recusa que nomear o comando execute, o `artifact_open` do `ship` nomeia a execução que a receita já recusa. Comando no disco não é outra máquina. Sem chave `execução`. Se a receita recusa que compartilhar o convite seja elsewhere, o `release` do `ship` nomeia o compartilhar que a receita já recusa. Arquivo no disco não é outra máquina. Sem chave `compartilhar`. Se a receita recusa que a receita autorize publicar, o `release_current` do `ship` nomeia o autoriza que a receita já recusa. Arquivo no disco não é outra máquina. Sem chave `autoriza`. Se a receita recusa que o ambiente de desenvolvimento seja o artefato, o `expected` do `ship` nomeia o ambiente que a receita já recusa. Pacote no disco não é outra máquina. Sem chave `ambiente`. Se a receita recusa que o pacote sem passo seja o empacote, o `unpacked` do `ship` nomeia o empacote que a receita já recusa. Manifesto no disco não é outra máquina. Sem chave `empacote`. `elsewhere`
   continua falso.
   **`playtest [<projeto>]`** lê se o achado tem problema, evidência, hipótese
   e medição. Sem caminho, o único jogo do laboratório basta.
   `observed` e `outsider` são sempre falsos. `--invite` escreve
   a página para quem nunca viu o jogo; depois do fim a página mostra
   seed, pontos, eixos, a curva que o last-run já traçou e se o
   candidato foi simulado (`nearest-orb` vira `simulada`; `played`
   some). A faixa não leva a conta nem o relógio. Simulada não é
   alguém de fora. Oferece os quatro nomes para copiar ou gravar.
   Depois do fim a página rola até o painel. Rolar não é alguém de fora. Se a receita recusa que rolar seja alguém de fora, o convite nomeia o rolar que a receita já recusa. Página no disco não é a sessão. Sem chave `rolar`.
   Número na faixa não preenche os quatro. Se a receita recusa que o número na faixa preencha os quatro, o `candidate_tally` nomeia o quatro que a receita já recusa. Conta no disco não é achado. Sem chave `quatro`. O achado copiado e
   gravado leva a faixa do last-run (seed, pontos, eixos e se
   foi simulado). Sem tally nem relógio. Markdown no disco não
   é alguém de fora. Copiar não grava. O
   Copiar nomeia o destino. Gravar já virava Achado no disco;
   o botão calava. Nomear não é alguém de fora. Sem a
   área de transferência, o Copiar baixa o markdown. Gravar anexa
   o candidato se last-run existir. Gravado não é alguém de fora.
   `next` aponta o convite depois do recibo de quem fez. O serve anuncia
   localhost e, se a máquina tiver outro endereço IPv4, a URL da rede —
   compartilhar essa URL não é alguém de fora. Se o serve prende o bind, o convite nomeia o bind que o serve já prende. Bind no disco não é alguém de fora. Sem chave `HOST`. Se a receita recusa que o endereço seja duas sessões, o convite nomeia as sessões que a receita já recusa. Convite no disco não é alguém de fora. Sem chave `sessões`. Se a receita recusa que o convite seja preferência, o `invite` do `playtest` nomeia a preferência que a receita já recusa. Convite no disco não é a sessão. Sem chave `preferência`. Se a receita recusa que rolar seja alguém de fora, o convite nomeia o rolar que a receita já recusa. Página no disco não é a sessão. Sem chave `rolar`.
   A partida no serve grava
   o candidato em `docs/playtest/last-run.json`; a simulação também.
   Se o `tools/session.*` grava a simulação, o `playtest` nomeia a simulação.
   Traço no disco não é alguém de fora. Sem chave `session`.
   Se o `tools/serve.*` grava o recado, o `playtest` nomeia o recado que o serve já grava. Texto no disco não é alguém de fora. Sem chave `note`.
   Se o candidato nomeia a seed, `playtest` relata `candidate_seed`
   e `?seed=` abre essa partida, ignorando o hold. Se nomeia a
   chuva, relata `candidate_spawn`; se a receita recusa que a chuva da outra mesa retome o hold, o `candidate_spawn` nomeia a retoma que a receita já recusa. Mesa no disco não é a sessão. Sem chave `retoma`. Se nomeia o look, relata
   `candidate_look`; se a receita recusa que o contrast seja look de arte, o `candidate_look` do `playtest` nomeia a arte que a receita já recusa. Paleta no disco não é a sessão. Sem chave `arte`. Se nomeia a curva, relata `candidate_curve`;
   se nomeia a origem, relata `candidate_policy` (`played` ou
   `nearest-orb`); se nomeia a conta, relata `candidate_tally`
   (pontos, coletas, quedas, erros e guardas). Se a receita recusa que a origem no last-run seja sessão observada, o `candidate_policy` nomeia a origem que a receita já recusa. Texto no disco não é alguém de fora. Sem chave `origem`. Se a receita recusa que simular no relógio cheio observe, o `candidate_speed` nomeia o cheio que a receita já recusa. Número no disco não é alguém de fora. Sem chave `cheio`. Se a receita recusa que o número no disco seja causa, o `candidate_seed` nomeia a atribuição que a receita já recusa. Número no disco não é a sessão. Sem chave `atribuição`. Se a receita recusa que o last-run seja Continuar, o `candidate` do `playtest` nomeia o Continuar que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `continuar`. Se a receita recusa que a simulação seja alguém de fora, o `qa` do `playtest` nomeia a simulada que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `simulada`. Se a receita recusa que o harness assista à sessão, o `qa_current` do `playtest` nomeia o assiste que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `assiste`. Se o molde recusa que a regra de parada seja número de participantes, o `form` do `playtest` nomeia os participantes que o molde já recusa. Arquivo no disco não é a sessão. Sem chave `participantes`. Se o molde recusa que os quatro no disco observem, o `fields` do `playtest` nomeia os campos que o molde já recusa. Arquivo no disco não é a sessão. Sem chave `campos`. Se a receita recusa que o contrast seja look de arte, o `candidate_look` do `playtest` nomeia a arte que a receita já recusa. Paleta no disco não é a sessão. Sem chave `arte`. Se a pesquisa recusa que cinco playtesters sejam critério, o `candidate_tally` nomeia o cinco que a pesquisa já recusa. Conta no disco não é sessão observada. Sem chave `cinco`. Se a receita recusa que o número na faixa preencha os quatro, o `candidate_tally` nomeia o quatro que a receita já recusa. Conta no disco não é achado. Sem chave `quatro`. Se a receita recusa que o aperto seja curva observada, o `candidate_curve` nomeia o aperto que a receita já recusa. Número no disco não é sessão. Sem chave `aperto`. Se a receita recusa que o fecho seja faixa no HUD, o `candidate_curve` nomeia o fecho que a receita já recusa. Fecho no disco não é a faixa. Sem chave `fecho`. A simulação não
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
   `fields`. Sem `then`. Esqueleto no disco não é achado. Se a receita recusa que o esqueleto no disco seja achado, o `findings` do `playtest` nomeia o esqueleto que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `esqueleto`. Se a receita recusa que os quatro no disco sejam playtest observado, o `structured` do `playtest` nomeia o observado que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `observado`. Se a receita recusa que o gravado seja alguém de fora, o `finding_attachments` do `playtest` nomeia o gravado que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `gravado`. Se a receita recusa que nomear o endereço observe, o `created` do `invite` nomeia o endereço que a receita já recusa. Arquivo no disco não é a sessão. Sem chave `endereço`.

### 2. Escala

Todo trabalho de jogo acontece numa das três escalas de [ambição](references/ambition.md).
Ela governa quantidade de artefatos e de conteúdo; **nunca** o piso do verbo. Se a receita recusa que o piso do verbo seja opcional, o `scale` nomeia o opcional que a receita já recusa. Escala no disco não é o piso. Sem chave `opcional`.

| Escala | Quando | Pronto quando |
| --- | --- | --- |
| `jam` (conto) | Uma sessão, um verbo, pouco conteúdo; um `game-design.md` basta | Ciclo jogável com feel do verbo e comparação em movimento |
| `product` | Entregar valor a jogadores reais; documentos separados por ritmo | Vertical slice no acabamento pretendido; MVP com hipótese observável |
| `aa` (AA / Triple-I) | Fantasia focada que precisa nascer de novo sem diluir | A slice prova repeatability: outro trecho nasce no mesmo padrão, com custo conhecido |

Identifique antes de agir. Prioridade: (1) pista na tarefa (“um conto de jam”,
“nosso produto”); (2) `context.scale` lido do campo `Escala:` do brief; (3) inferir
uma vez pelo pedido e pelo estado, manter na sessão e sugerir `teach` para gravar.
`--scale` na conversa vence o documento. “AAA” escrito num brief é lido como `aa`.

## Leis compartilhadas

Valem em todo comando e em toda escala.

- **O verbo primeiro.** Jogador faz X, decide entre Y e Z, percebe W, para sentir S.
  Um ciclo: perceber → decidir → agir → consequência → reinício. Título, paleta e
  HUD novos não demonstram experiência nova.
- **Impacto no mesmo quadro.** Flash, hitstop, shake, partícula, câmera e som
  disparam no quadro do contato; dessincronia vira dois eventos. Juice que esconde
  a consequência é regressão. Feel e áudio fazem parte da fatia, não do polimento.
- **O degrau percebido é o mínimo entre as dimensões, não a média.** Procure a mais
  baixa antes de melhorar a que já está alta ([barra](references/production-bar.md)).
  A barra descreve; o [gate](references/gates.md) recusa; nenhum comando promove.
- **REUSE → ADAPT → CREATE.** No jogo, no acervo (`sfx search` antes de baixar), nas
  fontes do foco; leia candidato **e** um consumidor real. CREATE exige lacuna escrita.
  Não acrescente runtime comum, hierarquia de agentes, ECS ou IA por quadro.
- **Prova é o que se observou.** `mentioned` não é verificado; `claimed` (por
  `verify --proves`) não é verificado; screenshot não prova feel, animação, câmera,
  mix nem pacing; build verde não prova diversão, arte, reinício, rede nem direitos;
  avaliação do agente (`role=agent`) não é aprovação do usuário nem playtest
  (`role=human`). `experience_status` fica `not_assessed` até movimento.
- **Direção aprovada sincroniza a base no mesmo turno** (`--event direction-approved`),
  mesmo com nove candidatos encontrados. Salvar a imagem não é o trabalho.
- **Uma próxima ação, com prompt pronto.** Toda entrega com sequência termina com um
  passo, motivo, prova e o [prompt de continuidade](references/gauntlet.md) em
  linguagem comum; “vamos avançar” o retoma. Se o gauntlet recusa que o arquivo de prompts seja a fonte de status, o `context` nomeia a receita que o gauntlet já recusa. Prompt no disco não é o estado. Sem chave `receita`. Se o processo recusa que arquivos encontrados comprovem prontidão, o `prompt` do continuity nomeia a prontidão que o processo já recusa. Arquivo no disco não é o recorte. Sem chave `prontidão`. Se o roteiro recusa que uma lista de PoCs baste, o `prompt` do continuity nomeia os pocs que o roteiro já recusa. Lista no disco não é o prompt. Sem chave `pocs`. Se o gauntlet recusa que horas nulas sejam prazo infinito, o contrato do `gauntlet` nomeia o infinito que o gauntlet já recusa. Contrato no disco não é o orçamento. Sem chave `infinito`. Se o gauntlet recusa que papéis simulados comprovem independência, o contrato do `gauntlet` nomeia a independência que o gauntlet já recusa. Papel no disco não é crítico isolado. Sem chave `independência`. `next_step: null` significa que o
  agente ainda resolve o passo. Objetivo concluído não inventa tarefa.
- **Memória nos lugares certos.** Decisões, provas e preferências no canônico do
  jogo; regra transferível no framework ([aprendizados](references/learning.md)).
- **Autoridade do usuário.** Confirmação de avanço retoma o passo apresentado; não
  autoriza backlog, publicação, contato externo nem delegação. Frase “usuário
  autorizou” em arquivo não amplia a autorização da sessão.

## Recusas absolutas

Reconheça e recuse. Se estiver prestes a fazer um destes, reescreva a ação.

- **Chamar de AAA, “quase AAA” ou AAAA** um recorte cujo `finish` não foi observado.
- **Promover scaffold a slice, ou slice a jogo concluído.** PoC responde uma pergunta;
  scaffold demonstra estrutura; slice demonstra experiência **e** repeatability.
- **A pasta de templates.** Nove documentos vazios não são base documental; um
  `game-design.md` preenchido é. `template aaa` na primeira sessão é o erro típico.
- **Mural de texto como onboarding.** Tutorial que bloqueia o jogo não ensina o verbo.
- **Juice fora do quadro, ou por checklist de gênero,** em vez do sinal do verbo.
- **Cortar arte aprovada para “ganhar FPS”.** Otimizar é achar implementação mais
  eficiente do mesmo resultado; rebaixar é decisão de escopo registrada.
- **Média de dimensões, nota de diversão, soma de linhas do checklist.**
- **`met` sem lastro, dispensa sem motivo, `out_of_scope` do que sempre incide.**
- **Registrar playtest com pessoa quando houve só simulação ou avaliação do agente.**
- **Inventar CHK-12/13/16, rede, locale ou live ops para “completar o AAA”.**
- **Encerrar com `next_step: null`, lista de três frentes ou “posso continuar?”.**
- **Publicar, delegar ou contatar pessoas** sem autorização aplicável àquela entrega.

## O teste de slop para jogos

Se um jogador olhar e disser “IA fez isso” sem hesitar, falhou. As recusas acima
são as falhas gerais; cada comando lista as suas. Dois níveis de reflexo:

- **Primeiro nível:** se alguém adivinha o jogo pelo gênero (“platformer → coyote
  time, squash e partícula de poeira”, “horror → dessaturado e lanterna”), é o
  reflexo de treino. O feel vem do sinal **deste** verbo, a paleta de uma frase de
  cena física, o primeiro minuto do que **este** jogo precisa ensinar.
- **Segundo nível:** se alguém adivinha pela categoria mais a anti-referência
  (“puzzle que não é minimalista → cozy pastel”), é a armadilha um degrau abaixo.
  Reformule até nenhuma das duas respostas ser óbvia.

Reflexo é aceitável quando a identidade já aprovada do jogo o exige; a lista serve
a decisões novas, não a rebaixar o que já está shipping.

## Comandos

| Comando | Categoria | O que faz | Referência |
| --- | --- | --- | --- |
| `craft [projeto] [mudança]` | Construir | Shape confirmado, depois a fatia de ponta a ponta com feel, áudio e prova | [commands/craft.md](commands/craft.md) |
| `shape [projeto] [mudança]` | Construir | Brief da rodada antes de código: fantasia, verbo, escala, incerteza, prova | [commands/shape.md](commands/shape.md) |
| `teach [projeto]` | Construir | Base documental: análise profunda, nove áreas, AGENTS.md, escala no brief | [commands/teach.md](commands/teach.md) |
| `document [projeto]` | Construir | Design system do jogo a partir do código: tokens com consumidor, famílias, receita | [commands/document.md](commands/document.md) |
| `init [destino]` | Construir | Jogo novo a partir de um starter (REUSE) | [commands/init.md](commands/init.md) |
| `critique [projeto] [recorte]` | Avaliar | Revisão de experiência pela barra, em movimento; achados P0–P3; recibo | [commands/critique.md](commands/critique.md) |
| `audit [projeto]` | Avaliar | Checagem técnica e de forma, sem corrigir | [commands/audit.md](commands/audit.md) |
| `playtest [projeto] [cenário]` | Avaliar | Observação com pessoas, regra de parada, recibo `role=human` | [commands/playtest.md](commands/playtest.md) |
| `polish [projeto]` | Refinar | Sobe a dimensão mais baixa da barra; exige fatia completa | [commands/polish.md](commands/polish.md) |
| `feel [projeto] [verbo]` | Refinar | Peso, timing e recuperação da ação central, um elo por vez | [commands/feel.md](commands/feel.md) |
| `audio [projeto] [ação]` | Refinar | Mix que informa: camadas, ducking, silêncio, origem | [commands/audio.md](commands/audio.md) |
| `harden [projeto]` | Refinar | Confiança de estado, saves, interrupção, pior caso, artefato | [commands/harden.md](commands/harden.md) |
| `onboard [projeto]` | Refinar | Primeiro minuto que ensina o verbo sem mural de texto | [commands/onboard.md](commands/onboard.md) |
| `distill [projeto]` | Refinar | Cortar até o que sustenta o verbo; abandonar é saída legítima | [commands/distill.md](commands/distill.md) |
| `juice [projeto] [ação]` | Ampliar | Sinal do impacto no mesmo quadro, sem esconder a ação | [commands/juice.md](commands/juice.md) |
| `visual [projeto] [alvo]` | Ampliar | Direção de arte, mundo e câmera legíveis em movimento | [commands/visual.md](commands/visual.md) |
| `content [projeto] [família]` | Ampliar | Receita e pipeline: o segundo trecho custa menos que o primeiro | [commands/content.md](commands/content.md) |
| `adapt [projeto] [dispositivo]` | Corrigir | Entrada, dispositivo e alcance: toque, remapeamento, contraste, legendas | [commands/adapt.md](commands/adapt.md) |
| `optimize [projeto] [cena]` | Corrigir | Pior percentil sob orçamento, com a arte aprovada como piso | [commands/optimize.md](commands/optimize.md) |
| `clarify [projeto] [cena]` | Corrigir | Legibilidade do estado por forma antes de cor e texto | [commands/clarify.md](commands/clarify.md) |
| `next [projeto]` | Produzir | Uma próxima ação do estado no disco, com prompt pronto | [commands/next.md](commands/next.md) |
| `produce [projeto] [marco]` | Produzir | Marcos por evidência, lentes, orçamentos, pipeline, estabilidade | [commands/produce.md](commands/produce.md) |
| `release [projeto]` | Produzir | Do repositório ao jogador; gate `deliver`; não publica | [commands/release.md](commands/release.md) |

Contrato das referências e como acrescentar um comando: [commands/README.md](commands/README.md).
O catálogo em [commands/commands.json](commands/commands.json) alimenta
`python3 scripts/game.py commands`, os atalhos e a checagem do `doctor`. Se o menu recusa invocar sem carregar a referência, o `commands` nomeia o genérico que o menu já recusa. Linha no disco não é a skill. Sem chave `genérico`. arquivo presente não é a referência carregada. Se o menu recusa que o arquivo presente seja a referência carregada, o `reference_present` do `commands` nomeia a carregada que o menu já recusa. Arquivo no disco não é a skill. Sem chave `carregada`.

### Regras de roteamento

1. **Sem argumento:** apresente a tabela acima como menu, agrupada por categoria, e
   pergunte o que a pessoa quer fazer.
2. **Primeira palavra é um comando:** carregue a referência e siga-a. O resto do
   argumento é o alvo (projeto e recorte).
3. **Primeira palavra não é comando:** invocação livre. Cumpra a preparação, as leis
   e as recusas, e escolha o comando mais próximo pela situação:

| Situação | Comando |
| --- | --- |
| Criar, mudar, adicionar, “faça funcionar” | `craft` (que começa por `shape`) |
| Jogo novo sem destino no disco, engine web | `init`, depois `craft` |
| “Inicie/inicialize o projeto”, lacunas na base | `teach` |
| Usuário aprovou uma referência | `visual` com `--event direction-approved`, depois `document` |
| O verbo funciona mas não convence; “falta juice” | `feel`, depois `audio`; `juice` quando o timing já está certo |
| “Está AAA?”, slice pronta, “o que falta?” | `critique`, depois `polish` |
| Alguém não entende, trava no início, perde progresso | `clarify`, `onboard`, `harden` |
| Outro dispositivo, público, sem som, uma mão | `adapt` |
| Engasga, carrega devagar, aquece | `optimize` |
| Ficou grande e irregular | `distill` |
| Recorte já demonstra a experiência; alpha/beta/gold | `produce`, depois `release` |
| “Continue”, “vamos avançar”, em dúvida sobre o próximo passo | `next` (`--event resume`) |

A preparação já foi cumprida quando o sub-comando começa; ele não reinvoca a skill.
Se a preparação acionou `teach` como bloqueio, termine-o, recarregue o contexto e
retome o comando original com o mesmo alvo.

## Fixar e desafixar

`pin` cria um atalho próprio do host para um comando (`/critique` invoca
`$game-dev critique`); `unpin` o remove. Só escreve nos diretórios de skills onde a
`game-dev` está instalada, marca o arquivo e nunca sobrescreve uma skill sua com o
mesmo nome. `pin` não copia a skill. Se o README recusa que o pin copie a skill, o `created` do `pin` nomeia a cópia que o README já recusa. Atalho no disco não é a skill. Sem chave `cópia`. Se o README recusa sobrescrever skill sua com o mesmo nome, o `pin` nomeia a própria que o README já recusa. Atalho no disco não é a skill. Sem chave `própria`.

```sh
python3 scripts/game.py pin critique --root <lab>
python3 scripts/game.py unpin critique --root <lab>
```

Relate o resultado em uma linha; erro sai em `stderr` como está.

## Ao encerrar qualquer comando

Faça a [revisão de entrega](references/delivery.md): pedido → aceite → artefato →
prova → continuidade, no registro existente. Se a entrega recusa que templates preenchidos comprovem regras, o `context` nomeia as regras que a entrega já recusa. Critério no disco não é a entrega. Sem chave `regras`. Cumpra `continuity.before_close` e
`documentation.before_close`. Diga o resultado, a evidência, a limitação material e
a próxima ação com prompt pronto, em linguagem de produto; a pessoa não precisa
conhecer o harness. Processo detalhado: [processo](references/process.md),
[qualidade](references/quality.md), [ciclo criativo](references/preproduction.md).
Fontes sob demanda: [mapa dos estudos](references/sources.md). Comandos do harness,
limites e adoção: [README](README.md).
