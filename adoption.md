# Adoção — Alan Studios Framework

Histórico das versões 0.1–0.9. Recibos brutos de execução e o acervo sonoro
ficam no laboratório; aqui permanece o que a versão afirma e o que ela não afirma.

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
