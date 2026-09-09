# Ciclo criativo e produção de games

Use ao conceber um jogo, definir uma expansão ou revisar sua direção. A unidade
de trabalho continua sendo uma mudança jogável e verificável. Estes artefatos
organizam decisões; a existência de documentos não comprova qualidade do jogo.

Em qualquer pedido sobre um jogo, comece pelo `context`: a checagem `foundation`
é automática, mesmo em ajustes localizados. Ao encontrar lacunas, avise e inicie a
[documentação automática](project-audit.md), sem pedir consentimento. A reconstrução
de um jogo existente segue aquele roteiro; não exige
reiniciar seu ciclo criativo nem preencher documentos sem evidência. O design system do jogo (Art Bible) e o
Devlog complementam este ciclo quando o conteúdo ainda não tem registro canônico.
Todo jogo identificável precisa da instância; o arquivo separado é opcional se outro
canônico cobrir as seções. O contrato do estúdio está no
[design system do jogo](game-design-system.md).
Direção aprovada durante criação/evolução exige sincronizar a base no mesmo turno,
mesmo quando arquivos antigos cobrem nominalmente as nove áreas. Use o evento
`direction-approved` no `context`; registro de imagem isolado não encerra esse passo.

## Escolher a profundidade

**Ajuste localizado:** atualize decisão, requisito e caso de QA no registro existente.
Não reinicie a pré-produção. **Jogo pequeno:** um `game-design.md` pode reunir brief,
GDD, requisitos, decisões técnicas e experimentos. Use os templates como perguntas,
sem duplicar a mesma informação em nove arquivos. **Projeto com sistemas/equipe
maiores:** separe os documentos que têm responsabilidade e ritmo de atualização
distintos. Linke suas fontes canônicas, mantendo IDs estáveis.

Ao iniciar, resolva o pedido, artefatos atuais e referência aprovada. Extraia o que
já foi decidido; identifique hipóteses e lacunas. Pergunte somente por decisão
indispensável que não possa ser inferida; registre suposições rotineiras e continue
o trabalho autorizado. Não invente aprovação, público observado ou resultado de teste.

## Fluxo com retorno

**Game Brief → GDD + MDA ↔ protótipo/PoC + playtest → PRD/TDD → vertical slice →
produção/MVP → QA e aprendizado → release.**

Essa é uma orientação de dependências, não uma esteira rígida. Requisitos conhecidos
podem ser escritos antes do protótipo. Uma PoC técnica pode anteceder o GDD. QA
começa na concepção. Um playtest que contradiz a hipótese devolve o trabalho ao
GDD/MDA; PRD, TDD e tarefas afetadas precisam acompanhar a mudança. O MVP pode
coincidir com a vertical slice em um jogo muito pequeno, se cumprir ambos os objetivos.

REUSE → ADAPT → CREATE vale para documentos, mecânicas, ferramentas, código e assets.
Leia candidatos e consumidores, adapte o canônico e explique lacunas antes de criar.
Para um jogo que ainda não existe no disco, o candidato de reuso é um starter do
acervo: `init <destino> --starter <starter>` monta o projeto e cria estes
documentos como rascunho declarado, para serem substituídos por decisão — não para
serem entregues como se fossem uma.

Cada etapa pretende um degrau da [barra de acabamento](production-bar.md): PoC
responde uma pergunta em degrau de protótipo, o MVP entrega um ciclo jogável, a
vertical slice existe justamente para demonstrar o degrau `slice` em um recorte
pequeno, e o release pretende `shippable`. Declarar a etapa não concede o degrau;
`context --stage` apenas informa qual é a pretensão.

## Etapas, significado e prontidão

Cada linha **Pronto para…** abaixo é o critério de saída da etapa, e é dela que
os [gates](gates.md) são extraídos: um gate por linha, com os critérios
enumerados. Isso muda o que a frase faz — ela deixa de ser só orientação de
leitura e passa a ser recusável, com `gate <projeto>` lendo o que o projeto
declara cumprir. Nenhum comando concede passagem, e as três saídas de um gate são
passar, cortar escopo e abandonar. A terceira já aparece explícita na etapa `poc`
e vale para todas.

### `brief` — Game Brief

Visão curta: jogador, fantasia, sensação, pilares, verbo central, plataformas,
referências e fronteira do primeiro jogo. Entrada: pedido e acervo. Saída: uma
proposta compreensível, com diferenciação e maior incerteza identificada.

**Pronto para desenhar/experimentar:** é possível descrever uma partida curta, o
que se pretende sentir e o que precisa ser aprendido primeiro. A referência visual
tem origem e autoridade declaradas; ausências são explícitas.
[Template](../assets/templates/brief.md).

### `mda` — Mechanics, Dynamics, Aesthetics

Ferramenta de raciocínio, não documento obrigatório separado. **Mecânicas:** regras
e ações. **Dinâmicas:** comportamentos produzidos pela interação ao longo do tempo.
**Experiência estética:** resposta emocional pretendida, incluindo desafio,
descoberta, fantasia, expressão ou convivência; vai além do visual.

Entrada: sensação e pilares. Saída: hipóteses ligando regra → comportamento →
experiência, alternativas e observação capaz de contradizê-las. Pode começar pela
experiência desejada e trabalhar de volta às regras. **Pronto para testar:** existe
uma situação que distingue a hipótese de sua alternativa. Não há pontuação universal
de diversão. [Template](../assets/templates/mda.md), [artigo original](https://www.cs.northwestern.edu/~hunicke/MDA.pdf).

### `gdd` — Game Design Document

Design da experiência: ciclo principal, decisões, controles, câmera, regras,
progressão, ritmo, conteúdo, espaço, narrativa e direção audiovisual pertinentes
ao jogo. Entrada: brief, hipóteses MDA e observações existentes. Saída: recorte
jogável definido, com consequências e situações de teste.

**Pronto para prototipar:** o implementador consegue explicar o que o jogador faz,
quais alternativas tem, o que acontece e como termina/reinicia. Pilares precisam
resolver escolhas concretas; “imersivo” ou “divertido” isoladamente não basta.
[Template](../assets/templates/gdd.md).

### `poc` — Proof of Concept

Experimento para reduzir uma incerteza criativa ou técnica. Entrada: pergunta
delimitada. Saída: comportamento observado, condições, evidência e decisão de
continuar, ajustar ou abandonar a hipótese. Protótipo pode ser descartável; código
de experimento só entra na produção após revisão de adequação e consumidores.

**Pronto para encerrar:** o resultado distingue a hipótese, ou explica por que o
experimento foi inconclusivo. Código que compila não prova hipótese criativa.
Defina antes o limite de esforço proporcional à tarefa. [Template](../assets/templates/poc.md).

### `prd` — Product Requirements Document

Propósito, público, escopo e comportamento exigido do produto. Conecta a experiência
do GDD a requisitos funcionais (**FR**) e de qualidade (**NFR**), com critérios de
aceite (**AC**). Entrada: direção de design e restrições conhecidas. Saída: requisitos
priorizados, observáveis e ligados aos cenários do jogador.

**Pronto para implementar o recorte:** cada requisito necessário tem condição,
resultado esperado e método de verificação; dependências e lacunas que podem mudar
o escopo estão resolvidas ou delimitam um experimento. Prioridade não permite
remover exigências explícitas do usuário. [Template](../assets/templates/prd.md).

### `tdd` — Technical Design Document

Decisões de implementação. Aqui TDD significa documento técnico; desenvolvimento
orientado por testes também usa essa sigla em outros contextos. Entrada: requisitos,
fontes atuais e mapa de reuso. Saída: arquitetura suficiente para a mudança,
contratos, estado, integração, recursos e plano de verificação.

**Pronto para construir:** caminhos canônicos e consumidores foram lidos, as
decisões cobrem os requisitos do recorte e riscos sem prova viraram PoCs explícitas.
Não imponha uma engine ou API universal. Decisão relevante pode usar um **ADR**,
registro de decisão arquitetural, se o projeto já adota esse formato.
`context --stage tdd` inclui a [receita de arquitetura](../recipes/architecture.md):
contexto por tarefa, análise de consumidores, alternativas, reversibilidade,
contraprova e passagem para a primeira fatia. A profundidade acompanha o alcance e
a incerteza; alteração pequena não precisa de um novo documento.
[Template](../assets/templates/tdd.md).

### `vertical-slice` — Vertical slice

Trecho pequeno com gameplay, conteúdo, arte, áudio e tecnologia integrados no
acabamento pretendido. Demonstra a experiência e a capacidade de produzir mais
conteúdo nesse padrão. Entrada: recorte e decisões de design/implementação.

**Pronto para ampliar:** cenário jogável e repetível, integrações verificadas,
comparação em movimento e regressões resolvidas. Cobertura parcial e avaliação do
agente permanecem distintas de aprovação do usuário. Placeholders podem servir a
uma PoC; não certificam o acabamento da vertical slice.
[Template](../assets/templates/vertical-slice.md).

### `mvp` — Minimum Viable Product

Menor versão capaz de validar valor com os jogadores pretendidos. Define a fronteira
de uma entrega, enquanto a vertical slice demonstra profundidade e acabamento de
um recorte. Entrada: hipótese de valor, escopo e evidência já obtida.

**Pronto para avaliar a entrega:** ciclo completo, requisitos essenciais atendidos,
acesso ao jogo e método de observação definidos. Reduza a quantidade de conteúdo
quando adequado; preserve a qualidade aprovada e o que o usuário exigiu. Entregar
um MVP não prova que sua hipótese de valor foi validada.
[Template](../assets/templates/mvp.md).

### `qa` — Quality Assurance e playtest

QA acompanha requisitos e riscos; playtest observa compreensão, decisões, controle
e experiência de jogar. Podem compartilhar um relatório, com resultados separados.
Entrada: cenário, hipótese/requisito, versão e referência. Saída: evidências técnicas,
observações, problemas, interpretação e decisão de próxima iteração.

**Pronto para concluir o escopo:** os critérios aplicáveis têm evidência correspondente,
falhas relevantes foram resolvidas/retestadas e lacunas estão explícitas. Não há
contato automático com participantes nem publicação implícita. Não registre teste
com pessoa quando houve somente simulação ou avaliação do agente.
[Template](../assets/templates/qa.md), [protocolo de qualidade](quality.md).

### `release` — Entrega

Fecha o ciclo: o caminho repetível entre o repositório e o jogador. Entrada:
versão pretendida, plataforma alvo e evidência acumulada. Saída: build reproduzível
a partir de clone limpo, orçamento de tamanho e de tempo até jogar, verificação do
**artefato exportado** — não do editor nem do servidor de desenvolvimento —,
proveniência de tudo que embarca, procedimento de reversão e lacunas declaradas na
nota da versão.

**Pronto para entregar:** outra pessoa constrói a partir do runbook, o artefato roda
em máquina que não é a de desenvolvimento, save migra da versão anterior e nenhum
recurso embarcado tem licença desconhecida. Licença desconhecida bloqueia a entrega;
localização de um arquivo não atribui autoria. O template registra o degrau observado
por dimensão; **nenhum comando concede autorização de publicação**, e gerar o
documento não é autorizar.
[Template](../assets/templates/release.md), [receita](../recipes/release.md).

## Revisão, rastreabilidade e retomada

Antes de passar à próxima decisão, revise intenção, coerência entre documentos,
alternativas de reuso, escopo, riscos e evidência. Use os critérios acima no trabalho
do agente. Registre no documento: **rascunho → revisado para o próximo passo**,
autor da revisão, base consultada, lacunas restantes e ação seguinte. Experimentos
têm resultados **não executado / observado / inconclusivo**. Nenhum comando promove
esses estados automaticamente. A aprovação do usuário só existe quando ele a deu.

Para vários requisitos, use uma trilha como **GDD-M01 → FR-001/AC-001 → TDD-D01 →
TASK-01 → QA-001 → evidência**. Uma linha com links basta; não crie um banco de dados.
Em tarefa única, referências textuais podem bastar. Não renumere IDs usados só por
mudar a ordem dos documentos. Requisito sem origem pede esclarecimento ou hipótese;
requisito sem verificação deixa a conclusão pendente.

Tarefas de produção devem ser fatias jogáveis com entrada, saída, dependências,
critério de aceite e prova. Após mudança, atualize primeiro a decisão canônica e
marque a evidência afetada como desatualizada. Retome pelo último resultado, falha e
próxima ação, sem descartar decisões já aceitas. Preserve hipóteses rejeitadas e custos
observados para evitar repetir tentativas improdutivas.

Ao concluir a entrega, selecione uma próxima ação, explique por que vem primeiro e
o que comprova seu término; registre-a na fonte atual. “Continue” retoma esse ponto
após conferir o estado real. Siga [continuidade e retomada](process.md#continuidade-e-retomada),
sem apresentar todas as PoCs como se fossem uma única tarefa nem recomeçar o ciclo.

## Ferramentas e limites reais

`context <projeto> --stage gdd` adiciona guia e template GDD aos caminhos selecionados.
`template gdd --project <projeto>` imprime o rascunho; `--output <arquivo-novo>` o
salva recusando destino existente. A escolha e leitura do documento canônico são
responsabilidade do agente. O comando não preenche design, revisa mérito ou cria um jogo.

`check-plan` continua validando o registro de reuso; não é validador semântico de
PRD/GDD. `verify` executa comandos técnicos explícitos; não aprova criatividade.
As revisões desta página dependem de execução e julgamento do agente/pessoa, com
limites declarados. Exemplo completo sem criar documentos paralelos:
[estudo aplicado a Era Uma Vez](../examples/era-uma-vez-preproduction.md).

Referências usadas e limites de adaptação: [fontes](sources.md#pré-produção-e-checagem).
