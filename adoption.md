# Adoção — Alan Studios Framework

Histórico das versões 0.1–0.9. Recibos brutos de execução e o acervo sonoro
ficam no laboratório; aqui permanece o que a versão afirma e o que ela não afirma.

## 0.9.36 — A próxima chuva nasce distinta e se deixa traçar

`npm run table -- --from spawn` só clonava a chuva padrão. Agora copia
qualquer perfil jogável, `--as denser|calmer|brief` desloca os knobs
e `session --spawn` traça essa chuva. A forma do save não muda.
`content_scale` permanece `shippable`: ferramenta que nasce mesa não
é alguém de fora no piso. `enough` continua falso. Só `release` fica
no piso.

O que 0.9.36 não afirma: ninguém de fora produziu, a intenção nomeada
não é chuva melhor e o harness não assistiu à sessão.

## 0.9.35 — A sessão traça a curva pelos eventos

`npm run session` só gravava totais de fim de partida. Agora percorre
os eventos e relata first_*_tick, never_banked, never_hit e as
sequências mais longas de hit e missed. `note --from-run` anexa a
curva quando ela existe. Número na simulação não é abandono observado.
`pacing` permanece `slice`: ninguém de fora jogou. `observed` e `felt`
continuam falsos. Só `release` fica no piso.

O que 0.9.35 não afirma: o harness não assistiu, não investigou causa
e não importou limiar de erro como selo.

## 0.9.34 — A ideia chega na tela do primeiro ciclo

`--idea` só escrevia no brief: a partida continuava o mesmo jogo
mudo. A frase entra em `data/copy.json` e o coach a mostra antes do
movimento. Sem brief (`--no-docs`) a superfície ainda recebe a
frase. O brief continua rascunho. A frase na tela não muda o verbo.
`executed` permanece falso. Só `release` fica no piso.

O que 0.9.34 não afirma: o harness não abriu o jogo e a fantasia não
foi jogada nem avaliada.

## 0.9.33 — Contraste em cena no stub, sem limiar

`npm run contrast` deixava de ver o que o token hex não cobre: placa
composta sobre o campo, flash sobre o orbe, preenchimento da placa
que some no alto contraste. Agora amostra pixels depois do `draw()`
numa cena montada. `fillText` é retângulo da cor, não glifo.
`verified` continua falso. Acessibilidade permanece `slice`: stub não
é dispositivo nem sessão com o modo ativo. Só `release` fica no piso.

O que 0.9.33 não afirma: o harness não leu o jogo em movimento no
aparelho e não importou razão de contraste como selo.

## 0.9.32 — Evento e telegraph sem array novo

O passo seguinte ao poço da chuva ainda alocava `{ type }` por verbo e
um `filter` por quadro no aviso do trilho. O evento volta ao poço no
passo seguinte, sem campo do verbo anterior; o telegraph reusa um
buffer. `createRng` no spawn ainda aloca. `performance` permanece
`playable`. Só `release` fica no piso.

O que 0.9.32 não afirma: o harness não mediu quadro no aparelho e
reuso não é estabilidade no dispositivo.

## 0.9.31 — Poço da chuva, sem quadro medido

Cada tick deixava um array novo de sobreviventes e um objeto novo no
spawn. A chuva compacta o mesmo array e reusa o poço; mortos não
ficam no estado. `npm run budget` relata o reuso. `performance`
permanece `playable`: poço no processo não é compositor nem
dispositivo. Evento e telegraph ainda alocam. Só `release` fica no
piso.

O que 0.9.31 não afirma: o harness não mediu quadro no aparelho, não
comparou com o build anterior e não importou unidade de quadro como selo.

## 0.9.30 — Candidato de medição no disco

`npm run session` corre uma partida simulada e grava
`docs/playtest/last-run.json`. `note --from-run` anexa o resumo. O
achado continua sem os quatro campos; `observed` continua falso.
Número no disco não é causa nem sessão observada. Só `release` fica
no piso.

O que 0.9.30 não afirma: ninguém jogou, o harness não assistiu e a
métrica não fecha o playtest.

## 0.9.29 — Antecipação no trilho e recuperação visível

A cadeia do feel ganhava contato e câmera e chegava “de graça” no
impacto. A ameaça que ainda não chegou marca o trilho; a recuperação do
dash muda a silhueta; o erro acende o campo, a coleta não. Redução de
movimento troca o flash por contorno. `feel` permanece `playable`:
elo no código não é peso percebido. `felt` continua falso. Só `release`
fica no piso.

O que 0.9.29 não afirma: o harness não jogou, não sentiu o punch e
ninguém identificou o jogo por um clipe de três segundos.

## 0.9.28 — O primeiro ciclo não pede `next`

`start` devolve `play`, `then.note` e um `prompt` colável. `guide`
mapeia três passos: start → jogar → note. `next` sai do caminho feliz
e fica em `then.lost`, para quando o ciclo já correu. O harness
continua sem abrir o jogo. `executed` permanece falso. Só `release`
fica no piso.

O que 0.9.28 não afirma: ninguém jogou, o verbo não foi sentido e o
projeto não deixou de ser protótipo.

## 0.9.27 — Segunda chuva com o mesmo consumidor

`dusk` é um perfil de spawn distinto (prática mais curta, intervalo
menor). A partida lê `state.spawn`, não só `CONFIG.spawn`.
`?spawn=dusk` e `settings.spawnProfile` escolhem a mesa; trocar o perfil
recomeça a partida. `npm run table -- <nome> --from spawn` copia a forma
que o jogo já consome. Mesa genérica continua sem consumidor.
`content_scale` permanece `shippable`: duas chuvas não são volume e
ninguém de fora produziu no piso. `enough` continua falso. Só `release`
fica no piso.

O que 0.9.27 não afirma: o harness não carregou a mesa no dispositivo,
não cronometrou um autor de fora e não conta itens.

## 0.9.26 — Folga no palco de ganho

A soma da 0.9.25 passou de 1.0 porque o palco usava o teto do arquivo
em overlap. O starter baixa o padrão dos barramentos, aplica folga no
master e um compressor no destino. `npm run mix` usa o mesmo palco.
`heard` continua falso. `audio_mix` permanece `slice`: folga no código
não é faixa ouvida no dispositivo. Só `release` fica no piso.

O que 0.9.26 não afirma: o harness não ouviu, não aprovou loudness e
não importou unidade como selo.

## 0.9.25 — Mix somado na partida e HUD em sequência

`npm run mix` soma as vozes de uma partida simulada com barramento,
ducking e limite. Relata o pico da soma, não do arquivo. `heard`
continua falso. `audio_mix` permanece `slice`: soma headless não é
dispositivo nem loudness percebido. A suíte desenha uma sequência de
quadros e confere placa e ordem; `legibility` permanece `playable`:
stub não é o dispositivo alvo. Só `release` fica no piso.

O que 0.9.25 não afirma: o harness não ouviu o mix e não leu o jogo
em movimento no aparelho.

## 0.9.24 — Buffer da decisão e câmera por verbo

O pedido de guardar feito no hitstop da coleta dispara quando o mundo
volta a andar. Guardar no mesmo quadro da coleta decide a corrente
nova; um toque sem corrente não decide o próximo orbe. Cada verbo
empurra a câmera numa direção própria (dash, coleta, guarda, dano).
`feel` permanece `playable`: câmera e buffer no código não são peso
percebido. `npm run probe` conta as duas janelas. `felt` continua
falso. Só `release` fica no piso.

O que 0.9.24 não afirma: o harness não jogou, não sentiu o punch e
ninguém identificou o jogo por um clipe de três segundos.

## 0.9.23 — Desenho no stub, identidade lida e cluster de uma mão

`npm run budget` cronometra o `draw` num canvas stub além da
simulação. `performance` permanece `playable`: stub não é compositor
nem dispositivo. `ship` relata `dist/VERSION.json` quando o arquivo
existe; `shipped` continua falso. `npm run size` relata bytes de
`dist/` sem teto. O starter oferece `oneHand` no cluster direito
(IJKL + P/O); `access` passa a ver o preset. Acessibilidade permanece
`slice`: sessão com uma mão não foi observada. Só `release` fica no
piso.

O que 0.9.23 não afirma: o harness não mediu quadro no dispositivo,
não jogou com uma mão e ninguém correu o artefato fora daqui.

## 0.9.22 — Artefato com identidade e save na interrupção

O export grava `dist/VERSION.json` (versão e HEAD). `shipped` continua
falso. Esconder a página ou `pagehide` descarrega progresso e
preferência. `state_trust` permanece `slice`: aba fechada de verdade
não foi observada. `docs/access.md` declara o que o recorte não
atende; `uiScale` entra na leitura de `access`. `verified` continua
falso. Só `release` fica no piso.

O que 0.9.22 não afirma: outra máquina não jogou o artefato e o
harness não fechou a aba.

## 0.9.21 — Prática antes do risco, pico sem limiar e o harness sem subcomando

A chuva começa só com orbes (`practiceTicks`) e guardar alonga o
intervalo (`recoveryTicks`). `pacing` sobe a `slice`. A curva com
quem nunca viu o jogo continua pendente. `npm run peak` relata o pico
de cada WAV sem LUFS nem aprovação; `npm run probe` conta o buffer
declarado sem chamar isso de peso. `python3 scripts/game.py` sem
subcomando é o `guide` de quatro passos. `heard` e `felt` continuam
falsos. Só `release` fica no piso.

O que 0.9.21 não afirma: o harness não jogou a curva, não ouviu o
pico e não mediu quadro no dispositivo.

## 0.9.20 — Recibo curto, contrato da família e receita de arte

`note` grava a observação depois da primeira partida sem a linha longa
do `record`. `felt` e `observed` continuam falsos. Toda mesa do starter
passa pelo mesmo `migrateTable`; `npm run table` já nasce com schema.
`content_scale` sobe a `shippable`. O art-bible ganha a receita do
próximo primitivo; `art_direction` sobe a `slice`. `consistent` e
`enough` continuam falsos. Dash e guardar passam a ter squash e tremor
próprios — sinal no código, não peso medido. `feel` permanece
`playable`. Só `release` fica no piso.

O que 0.9.20 não afirma: o harness não jogou, não aprovou a direção em
movimento e ninguém de fora produziu no piso.

## 0.9.19 — Variação no mix, schema da mesa e o mapa ideia→ciclo

Cada papel ganha `public/sfx/<papel>-b.wav`: o mixer alterna as
variantes. `audio_mix` sobe a `slice`. `heard` continua falso — rodízio
não é loudness medido. `data/spawn.json` declara `schema` e migra o
formato antigo; schema futuro falha com o número. `content_scale`
permanece `slice`: uma mesa migrada não é a família inteira. `guide`
devolve start → jogar → next sem executar. Só `release` permanece no
piso.

O que 0.9.19 não afirma: o harness não ouviu a variação, não carregou
schema inválido em sessão e não correu os três passos.

## 0.9.18 — Runbook vigente, medição de sessão e contraste sem limiar

`docs/release.md` já nasce vigente: como exportar e servir o `dist/`.
`shipped` continua falso. A partida encerrada guarda `lastRun` no
progresso — forma para o campo de medição de um achado, não playtest
observado. `npm run contrast` relata luminância relativa dos pares hex
sem importar 4,5:1 e sem aprovar.

O que 0.9.18 não afirma: outra máquina não jogou o artefato, o harness
não assistiu à sessão e o contraste em movimento não foi observado.

## 0.9.17 — Design sonoro original nos seis papéis

O starter embarca `public/sfx/<papel>.wav` gerado por
`tools/design-sfx.py`: seno e ruído filtrado, CC0-1.0, recibo ao lado.
`audio_mix` sobe a `playable`. Um arquivo por papel ainda não é
variação; `heard` continua falso. Só `release` permanece no piso.

O que 0.9.17 não afirma: o harness não ouviu, não aprovou a mixagem e
não substituiu o acervo do laboratório.

## 0.9.16 — Assistência que não esconde conteúdo

O starter ganha a opção `assist`: alcance de coleta maior, chuva mais
lenta e graça mais longa. Os mesmos orbes, a mesma pontuação. `verified`
continua falso — o harness não jogou com o modo ativo. Contraste ainda
não foi medido; acessibilidade segue em `slice`.

O que 0.9.16 não afirma: o harness não mediu contraste e não observou
uma sessão com assistência ligada.

## 0.9.15 — Receita e ferramenta para a próxima mesa

O starter nasce uma mesa com `npm run table -- <nome>`: JSON novo e
registro no mesmo `loadTable`. Campo obrigatório ausente falha com o
nome da mesa e do campo. `content_scale` sobe a `slice`. `enough`
continua falso — receita não é volume, e não há migração de formato.

O que 0.9.15 não afirma: o harness não carregou a mesa nova nem mediu
o custo de um item produzido por alguém de fora.

## 0.9.14 — Primeiro ciclo no jogo e art-bible vigente

O starter ensina mover, coletar e guardar no próprio campo; o aviso some
depois da primeira guarda. `pacing` sobe a `playable`. `docs/art-bible.md`
já vem escrito (primitivas por decisão) e o `init` não o sobrescreve.
`art_direction` sobe a `playable`. `consistent` e observação de sessão
continuam pendentes. Duas dimensões seguem em `prototype`: mix e release.

O que 0.9.14 não afirma: o harness não jogou o ciclo e não aprovou a
direção em movimento.

## 0.9.13 — Mixer consome o arquivo e o acervo preenche o papel

O starter carrega `public/sfx/<papel>` no mixer: copiar um .wav sem
consumidor deixava `roles` verde e o jogo mudo. `roles --fill` busca o
papel no acervo (`audio.py` / `sfx_catalog`); `--apply` copia com o
nome do papel e o recibo. `heard` continua falso. Duas mesas
(`data/spawn.json`, `data/copy.json`) passam pelo mesmo `loadTable` —
uma família ainda não é escala.

O que 0.9.13 não afirma: o harness não ouve, não escolhe o som certo e
não autoriza improvisar arquivo quando o acervo está vazio.

## 0.9.12 — Conteúdo fora do código, export e achado de playtest

O starter extrai a chuva para `data/spawn.json` e passa a ter `npm run
build` (`tools/export.mjs` → `dist/`). `content` e `ship` deixam de
apontar essas duas lacunas no `init` fresco: o dado existe, o passo
existe. Uma mesa não é escala; copiar a árvore não é outra máquina
tendo jogado. `playtest` lê o formato problema/evidência/hipótese/medição.
`observed` é sempre `false`. `next` propõe `playtest.unstructured` quando
há observação (ou qa.md vigente) sem os quatro campos. A linha da tabela
de ofício que descreve o formato não conta.

O que 0.9.12 não afirma: o harness não carrega o JSON no jogo, não
executa o export e não assiste ao playtest.

## 0.9.11 — Arte, conteúdo e empacotar no disco

Três dimensões AAA que a barra já nomeava e o harness não lia: `art`
(`const PALETTES`, tokens.json, art-bible vigente), `content` (data/levels
ou .ldtk/.tmx/.ink) e `ship` (script build/export, docs/release.md vigente
ou CI). `consistent`/`enough`/`shipped` são sempre `false`. `next` propõe
`art.missing`, `content.inline` e `ship.unpacked` depois do orçamento e
antes dos rascunhos. O starter declara paleta; conteúdo ainda mora no
código e não há passo de export — um `init` fresco ganha essas duas
tarefas nas alternativas, não na primeira proposta.

O que 0.9.11 não afirma: o harness não compara silhueta, não conta itens
e não executa o export. HTML sem manifesto não dispara `ship.unpacked`.

## 0.9.10 — Alcance, save e orçamento no disco

Três dimensões AAA que o starter já implementa e o harness não lia:
`access` (highContrast, reducedMotion, captions, remap), `save` (uso de
armazenamento × PROGRESS_SCHEMA/migrate) e `budget` (script ou
tools/budget.*). `verified`/`trusted`/`measured` são sempre `false`. `next`
propõe `access.missing`, `save.unversioned` e `performance.unbudgeted`
quando o disco não declara. O starter declara os três, então um `init`
fresco não ganha três tarefas novas — um canvas sem opção de alcance, sim.

O que 0.9.10 não afirma: o harness não mede contraste, não abre o save e
não roda o orçamento.

## 0.9.9 — Feel declarado e observação no disco

O starter nomeia perdão, graça e hitstop no `CONFIG`; o harness só via a
tabela de ofício. `feel` lê as constantes e procura `record.json` com
`kind=observation` no projeto. `felt` é sempre `false`. `next` propõe
`feel.unobserved` depois dos papéis de áudio e antes dos rascunhos:
constante nomeada não é peso percebido. `discover` conta constantes e
recibos por jogo.

O que 0.9.9 não afirma: o harness não joga, não mede latência e não
atribui degrau. Recibo otimista sai intacto.

## 0.9.8 — Papéis de áudio no disco

O starter declara seis papéis do verbo e os deixa vazios; o harness não lia
isso. `roles` cruza `const SOUNDS` (e `sounds.json`) com arquivos em
`public/sfx`. `heard` e `approved` são sempre `false`. `next` propõe
`audio.roles` depois do primeiro ciclo e antes dos rascunhos: verbo mudo não
espera sete templates. `discover` conta papéis e vazios por jogo. Sem
`shared/sfx`, o catálogo continua vazio — isso não autoriza improvisar
licença nem sintetizar beep.

O que 0.9.8 não afirma: arquivo presente não é mixagem, não é feel e não é
som ouvido. Copiar do acervo ainda passa por `sfx copy` com recibo; `origins`
continua sem validar licença.

## 0.9.7 — Disco, ofício e primeiro ciclo

Três lacunas entre a promessa (ideia→jogo jogável, acabamento observável) e o
que o harness de fato fazia:

- **`origins`** percorre mídia embarcada e cruza com recibos. Não valida
  licença. `granted` e `validated` são sempre `false`. Se `deliver.licensing`
  está `met` e o disco tem arquivo sem recibo, a saída marca
  `contradicts_licensing`.
- **`craft`** lê os nove checklists da §7 — paleta, perdão, percentil, regra de
  parada — como conformidade com a declaração do projeto. Nenhum rótulo tem
  dígito. `observed` é sempre `false`. Só entra no `next` se o projeto declarou
  o gate correspondente.
- **`start`** e `playable.unplayed`: depois de um `init` fresco o `next` propõe
  abrir o ciclo, não preencher sete templates. `--idea` escreve a fantasia no
  brief; o brief continua rascunho. `executed` permanece `false`.

O que 0.9.7 não afirma: nenhum comando observa o jogo, mede contraste, concede
passagem de gate ou transforma recibo em licença válida. Feel, arte e conteúdo
em sessão real continuam `not_assessed` até haver observação em movimento.

## 0.9.6 — Memória do agente entre sessões (parcial)

Handoff: [HANDOFF.md](HANDOFF.md). `instruction_files` localiza AGENTS.md e equivalentes
(CLAUDE, GEMINI, .cursorrules, .cursor/rules, copilot-instructions, windsurfrules).
`context` expõe `instructions` e `git` (HEAD, branch, sujeira, recentes — sem provar
nada). `scan` reporta `agent_context`; `next` propõe `template agents` quando falta;
`init` gera `AGENTS.md` na raiz. Frentes 2–5 do plano de remediação com IA ainda não
começaram nesta branch.

## 0.9.5 — Integração das três linhas 0.9

Três linhas paralelas de 0.9 foram unificadas neste repositório: facilidade e piso de
acabamento (0.9–0.9.3), começar e acabar (starter, `init`, `next`, `bar`, `gate`,
`discover` revisado, `verify --proves`) e produção por marcos, pacotes e recibos
(0.9.4). Uma só seleção de leituras une `audio`, `aaa`, `finish`, `production-bar`,
pacotes e `production`; `doctor` confere também referências e pacotes e nomeia os
projetos; `verify --script` aceita alvos Cargo; `record` e `--genre` entram no CLI
com `init`, `next`, `bar` e `gate`. Catorze focos, dezessete etapas, dez referências.
Onde as linhas discordavam — a receita de feel existia em três versões — ficou a
mais completa, com o que as outras traziam de único (starter como implementação de
referência, ligação com `record`).

## 0.9.4 — Produção por marcos, pacotes e recibos

Revisão do que o framework se propõe (criar jogos com IA com evidência, até a
qualidade aprovada) contra o que entregava até 0.9.3, integrada às linhas paralelas
de facilidade e piso de acabamento. Lacunas encontradas:

- **Os comandos documentados não rodavam.** Todo exemplo do README e da skill passava
  `--root` depois do subcomando; o argparse só aceitava antes. Corrigido: `--root` em
  qualquer posição (a linha paralela chegou à mesma correção).
- **`context` ignorava `--root` para o acervo sonoro** e consultava o diretório atual.
  Corrigido.
- **Não havia autodiagnóstico.** `doctor` confere Python, presença dos arquivos do
  framework (receitas, templates, referências, pacotes), raiz, projetos, estudos, sfx e
  git; a linha paralela somou ferramentas, starters e atalhos da skill.
- **A pré-produção recomendava um `game-design.md` único para jogos pequenos, mas não
  havia template.** O template `game-design` reúne as nove áreas e, preenchido, é
  reconhecido pelo scan como cobertura completa (teste garante).
- **A descoberta só via package.json, Unity, Godot e HTML.** Agora reconhece Unreal,
  Defold, GameMaker, Cargo, Python e Love2D, e ignora pastas de build das engines.
- **O processo terminava no MVP.** Não havia marcos de produção, orçamentos, pipeline
  de conteúdo, estabilidade, acessibilidade ou localização. A receita `production`
  define marcos como gates de evidência (first playable → vertical slice → alpha →
  beta → gold → live), lentes de disciplina e orçamentos medidos; os templates
  `production-plan` e `milestone` mantêm o estado; `quality.md` ganhou a barra de
  acabamento.
- **Feel e áudio** vieram da linha 0.9–0.9.3 (abaixo); a receita de feel ganhou a ligação
  com `record` e com as lentes de marco.
- **A skill era um bloco denso.** Reorganizada em caminho rápido e sete passos, sem
  remover regras.
- **Só havia recibo para comandos técnicos.** A receita de produção exige orçamento
  medido e passagem declarada por pessoa, mas nada ligava essas provas à versão do
  jogo. `record` grava observação (`role=human|agent`), medição de orçamento e
  decisão de marco em pasta inédita, com HEAD do git e anexos por SHA-256. Ele guarda
  o que foi declarado; não valida nem aprova.
- **`verify --script` só conhecia npm.** Projetos Cargo ganham `check`, `build` e
  `test`; Unity, Godot e Unreal seguem por `--command`, sem inventar CLI.
- **O núcleo era agnóstico, mas a calibração real era web/2D.** Em vez de
  especializar o núcleo, a 0.9 adiciona [pacotes](packs/README.md): dezoito de
  plataforma (web, Unity, Godot, Unreal, Defold, GameMaker, Construct, RPG Maker,
  Ren'Py, Roblox, PICO-8, Haxe, Flutter, .NET, C++/CMake, Cargo, Python, Lua),
  selecionados automaticamente pelo marcador que `identify` encontra, e vinte e três
  de gênero (da narrativa ao multiplayer competitivo, passando por luta, esportes,
  ritmo, horror, estratégia, deckbuilding, idle e casual), por `--genre`. Entram em
  `read_next` depois da receita; um campo `Gênero:` em documento só sugere. A ordem
  dos marcadores passou a dar precedência a engines que carregam manifestos genéricos
  (RPG Maker MZ com `package.json`, Unity/Godot com `.csproj`). Pacotes são convenções
  a confirmar, não capacidades certificadas.
- **Faltava exemplo de produção.** [Da trilha ao capítulo acabado](examples/era-uma-vez-production.md)
  mostra plano, orçamentos como hipóteses, marcos e recibos num jogo pequeno.

O que 0.9 não afirma: “AAA” é padrão de acabamento observável, não orçamento nem
equipe; nenhum comando mede performance, executa soak, promove marco, certifica
requisito de plataforma ou aprova arte. Os termos de marco seguem uso corrente da
indústria; cada jogo registra a definição adotada.

## 0.9.3 — Checklist adaptado ao harness

O checklist deixa de ser só `--stage aaa`. `context` expõe `finish`
(núcleo / produto / promessa / mercado e a ação). Slice, QA, `create`,
`feel` e `audio` carregam a [guia](references/aaa-checklist.md); o
template inteiro só na etapa `aaa`. Scanner trata o documento como
candidato de QA — continua havendo nove áreas. Primeira sessão não gera
o arquivo.

## 0.9.2 — Checklist de piso de acabamento

Etapa `aaa`: [guia](references/aaa-checklist.md) e
[template](assets/templates/aaa.md). 16 grupos (CHK-0 a CHK-16), estados
`não executado` / `observado` / `inconclusivo` / `N/A`. Completar linhas não
certifica publisher. Tier de mercado fica na seção 16 como contexto. Jam
pode marcar o resto `N/A` com a escala.

## 0.9.1 — Tier de mercado ≠ piso de acabamento

Pesquisa de 2026-09-09 dobrada em [ambição](references/ambition.md) e
[sources](references/sources.md#aaa-tier-e-piso-09). AAA de publisher é
rótulo financeiro (sem certificação). O harness usa “AAA” só como piso da
slice. Escala de produto ambicioso passa a **AA / Triple-I**. Barras novas:
sincronia no frame do impacto, pacing/latência, repeatability da slice.
Nenhum orçamento citado vira meta.

## 0.9 — Facilidade e piso AAA operacional

Caminho curto na skill e em [criar](recipes/create.md): primeira sessão chega a
um ciclo jogável sem gerar nove templates. Focos [feel](recipes/feel.md) e
[áudio](recipes/audio.md). Contrato [ambição](references/ambition.md): AAA é
acabamento demonstrado na slice, não motor nem nota. Escala jam / produto /
AAA-shaped muda quantidade, não o piso do verbo. O harness continua thin:
não mede diversão, não publica, não escolhe engine.

## 0.9 — Começar e acabar (linha paralela)

Quatro lacunas entre o que o framework prometia e o que entregava.

**Recusar.** A barra descreve onde o jogo está e nada dizia o que não pode
passar. Os dez [gates](references/gates.md) formalizam as linhas “Pronto para…”
que já estavam no ciclo criativo — 38 critérios extraídos da prosa, não
inventados, com um teste exigindo que cada gate continue apontando para a linha
de origem. O projeto declara `met`/`unmet`/`waived`/`out_of_scope` por critério
com o que sustenta o estado, e `gate` lê. Critério sem linha é pendente: silêncio
não é aprovação. As três saídas são passar, cortar escopo e **abandonar** — a
terceira o ciclo já tinha na etapa `poc`, e passou a valer nas dez. Dispensa exige
motivo escrito; quatro critérios não se dispensam, porque a prosa da etapa não
deixa terceira opção. `granted` é sempre falso.

Depois, um [levantamento de fontes](references/gates-research.md) mostrou duas
coisas que faltavam. Os dez gates perguntavam só “o trabalho está feito?”, e a
pergunta de valor — “isto ainda vale o que custa?” — existia apenas como a saída
`abandonar`, dependendo de alguém levantá-la: agora três critérios a fazem, e
`next` a coloca antes de pedir mais trabalho no mesmo gate. E um critério que
nunca incidiu só podia virar dispensa, inflando a conta que existe para doer:
`out_of_scope` é estado separado, com motivo escrito e recusado onde o critério
sempre incide.

**Chegar.** O laboratório onde este harness roda normalmente já tem jogos, e o
primeiro movimento nele é revisar o que existe. `discover` devolvia caminho e
tipo, o que faz jogos em estados incomparáveis saírem iguais; agora ele lê cada
projeto e devolve áreas mínimas com candidato, rascunhos, passo registrado para
retomar, piso de acabamento declarado e validadores — com `--plain` para a
listagem crua. A ordem é a do disco, e o harness não classifica os jogos por
urgência, porque nada nele observa qual importa mais. `doctor` passou a nomear os
projetos que contou, em vez de só contá-los.

**Começar.** Até 0.8 o harness sabia ler um jogo existente e não sabia criar um.
`doctor` observa ambiente, presença dos arquivos e os atalhos de skill do host — vigente,
desatualizado, ausente, comparados por conteúdo, com symlink para o `SKILL.md`
vigente contando como vigente — sem escrever nada. `init` monta um projeto a partir
de um starter do acervo, troca os valores que o `starter.json` dele declara e gera
como rascunho declarado sete documentos, que cobrem sete das nove áreas mínimas
(as outras duas ficam com o README e o CREDITS do starter); não instala
dependências e não toca no starter de origem. Um starter carrega valores reais em
vez de marcadores porque ele é referência executável: serve e abre antes de
qualquer `init`.
`next` deriva uma proposta ordenada do estado no disco. `--root` passa a ser
aceito antes e depois do subcomando, como a documentação já afirmava.

**Acabar.** A [barra de acabamento](references/production-bar.md) nomeia cinco
degraus em dez dimensões de ofício, com a observação que sustenta cada degrau, e
chega em todo `context` pelo campo `production_bar`. `bar <projeto>` lê a tabela
de degraus que o projeto declara nos próprios documentos e devolve o piso, as
dimensões que estão nele e — só quando as dez tiverem linha — o degrau percebido;
com isso `next` propõe subir a dimensão mais baixa pelo nome, citando o critério
escrito e a linha de onde veio. O harness confere a forma da declaração — e
relata em `problems` dimensão fora das dez, degrau fora dos cinco e alvo que não
é o seguinte — nunca o jogo: tabela bem formada e otimista sai de lá intacta.
Seis receitas novas — feel,
performance, acessibilidade, áudio, persistência, release — e a etapa `release`
fecham o ciclo. O starter `canvas-arcade` existe para que o passo REUSE tenha um
candidato real: loop de passo fixo, RNG semeado, save versionado com migração,
mixer com legendas e um contrato de ciclo de vida exercitado por testes headless,
em vez de apenas mencionado.

**Alegação com recibo.** `context` lê arquivos e por isso só sabe dizer
`mentioned` sobre as oito capacidades conhecidas. `verify --proves <capacidade>`
**não** as promove a verificadas — o harness não sabe se um comando exercita
pause. O que ele acrescenta é uma alegação com autor, data, argv e log: `claimed`
com recibo verde, `unsupported` quando a execução falha. A afirmação deixa de sumir
na prosa e passa a ser contestável. Nenhum arquivo do repositório seleciona
capacidade.

A escada quase não cita número, e isso era decisão sem justificativa escrita. Um
[levantamento](references/observable-criteria-research.md) foi buscar os limiares
que se poderia importar e achou o oposto do esperado: o safe title que todo mundo
usa foi substituído em 2009, o “100 ms” de latência vem de um artigo de 1968 sobre
teclas de terminal que já se contradiz no próprio parágrafo, e o “cinco usuários”
de playtest sai de um artigo que conclui dezesseis. Nenhum limiar entrou; o que
entrou foi um mapa de onde existe norma, onde existe página de fornecedor e onde
não existe fonte — e uma regra de parada de playtest, que substitui a pergunta
“quantas pessoas?” por “o que encerra a rodada?”. Um teste novo mantém os
cinquenta critérios da barra livres de dígito.

**Origem no disco.** `deliver.licensing` recusava dispensa e só lia a linha da
tabela. `origins` percorre o projeto, lista mídia embarcada e cruza com recibos;
`next` propõe declarar o que falta. Recibo não é licença válida, e os dois
campos que poderiam mentir sobre isso (`granted`, `validated`) são sempre
falsos.

O que 0.9 **não** afirma: nenhum comando atribui um degrau da barra, e a escada não
foi calibrada contra uma amostra de jogos publicados — é linguagem para observar,
não aferição. `init` cria rascunho, e rascunho não é decisão documentada. `next`
propõe e nunca executa. Os testes do starter provam o starter, não um jogo derivado
dele. AAA continua descrevendo orçamento e equipe; o que este repositório persegue
é acabamento por dimensão em escopo reduzido.

## 0.8 — Arquitetura proporcional

Receita [architecture](recipes/architecture.md). `--focus architecture` e
`--stage tdd` selecionam essa receita. A skill aplica análise proporcional
quando a mudança afeta contratos, responsabilidades ou sistemas. O CLI não
infere dependências nem aprova decisões.

## 0.7 — Continuidade e retomada

`--event resume` localiza fontes de continuidade. A entrega deve situar o
avanço e uma próxima ação, motivo e prova. O harness deixa `next_step: null`;
o agente resolve o passo.

## 0.6 — Aprovação de direção

`--event direction-approved` sincroniza a base mínima no mesmo turno, mesmo
com todos os candidatos encontrados. Salvar a imagem e listar entregas não
basta.

## 0.5 — Documentar o mínimo sem segundo pedido

Se a checagem deixar lacunas, o agente avisa e documenta. Restrição explícita
na conversa continua valendo. O scanner permanece somente leitura.

## 0.4 — Scan e foundation

`context` sempre inclui `scan`. Nove áreas, candidatos, lacunas e limites.
`candidate_found` não certifica suficiência. Templates complementares:
Art Bible, Devlog, Auditoria.

## 0.3 — Contexto por foco com estudos e menções locais

`context` lista catálogos do foco quando o irmão de estudos existe, e registra
menções de pause, reset, seed e demais capacidades em um conjunto fechado de
arquivos locais. Nenhuma menção vira `verified`.

## 0.2 — Pré-produção e ciclo criativo

Nove templates sob demanda. `context --stage` e `template` selecionam um
artefato. Nenhuma etapa é aprovada pelo comando.

## 0.1 — Entrega inicial

Descobrir projetos, recortar contexto, validar a forma do contrato de reuso e
executar comandos escolhidos com recibo.

## Limites que continuam valendo

Build verde não comprova diversão, arte, reinício, rede, direitos de assets nem
aprovação humana. Troca de modelo com qualidade equivalente continua hipótese a
testar. Os oito frameworks externos foram estudados em recortes; seus testes
não foram executados neste repositório. Este extrato não inclui evidência JSON
nem a biblioteca `shared/sfx`.
