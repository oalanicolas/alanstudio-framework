# Gates e marcos de produção: levantamento de fontes

Pesquisa feita em 9 de setembro de 2026 para embasar o desenho de um mecanismo de
gate — um ponto que **recusa** avanço até critérios serem cumpridos. Este
documento não é a especificação do gate; é o levantamento do que existe fora
deste repositório, com a procedência e o limite de cada fonte.

**Como ler os limites.** Para cada fonte estão declarados: URL, quem publicou, se
é primária (o próprio autor/organização que define a coisa) ou secundária (alguém
relatando), data quando disponível, e o **limite** — o que aquela fonte sustenta e
o que ela não sustenta. Um limite não é uma ressalva decorativa: várias das fontes
mais citadas na internet sobre este assunto sustentam muito menos do que aparentam.

A conclusão mais importante do levantamento vem primeiro, porque muda o desenho:
**só um dos cinco tópicos tem gates com critérios públicos, versionados e
verificáveis** — certificação de plataforma, e mesmo aí apenas Xbox, Steam e Apple.
Marcos de produção de jogos **não têm definição canônica**; quem afirmar que têm
está inventando. Ver [§1](#1-marcos-de-produção-de-jogos) e
[§6](#6-o-que-não-encontrei-fonte-confiável).

---

## 1. Marcos de produção de jogos

### 1.1 Não existe autoridade normativa

Procurei e **não encontrei** norma, padrão ou definição publicada por corpo de
padronização (ISO, IEEE), por associação da indústria (IGDA) ou por publisher em
documento público que defina First Playable, Vertical Slice, Alpha, Beta, Content
Lock ou Gold Master. O que existe é: livros de produção, posts de praticantes,
wikis de estúdio e **contratos privados de publishing**. Nenhum deles obriga
ninguém além de quem assinou.

Isso não é uma lacuna da minha busca que outra busca resolveria. É a estrutura do
assunto: os termos circulam como vocabulário profissional, não como especificação.
Qualquer gate que este framework construir sobre esses nomes está construindo
sobre convenção local, e é honesto dizer isso ao usuário em vez de citar uma
"definição da indústria" que não existe.

### 1.2 O desacordo é real e específico

Encontrei **pelo menos três mapeamentos incompatíveis** entre os nomes dos marcos
e o conteúdo que eles supostamente exigem. Não é imprecisão de blog: as fontes
discordam sobre o fato central.

**Desacordo A — Alpha significa "feature complete" ou "40–50% dos assets finais"?**

Rami Ismail (desenvolvedor, ex-Vlambeer, autor de material de produção
independente) põe o equivalente entre parênteses, como se fosse definitório:

> "Alpha (Feature Complete) - ensuring all features are functional
> Beta (Content Complete) - ensuring all content is implemented"

— [ltpf.ramiismail.com/prototypes-and-vertical-slice](https://ltpf.ramiismail.com/prototypes-and-vertical-slice/).
Fonte primária para a prática do autor; praticante reconhecido escrevendo em site
próprio, sem citação a norma. **Limite:** é a definição de um profissional, não um
padrão; o próprio texto não reivindica autoridade externa.

Heather Maxwell Chandler, em *The Game Production Handbook* — o livro-texto mais
usado de produção de jogos — define Alpha de forma **incompatível** com isso:

> "Alpha: At this milestone, key gameplay functionality is implemented, assets are
> 40–50% final (the rest are placeholders), the game runs on the correct hardware
> platform in debug mode, and there is enough working to provide the team with a
> feel for the game. Features might undergo major adjustments at this point, based
> on play-testing results and other feedback. Alpha occurs 8 to 10 months before
> code release."

— citado em [goodreads.com/work/quotes/22237702](https://www.goodreads.com/work/quotes/22237702-the-game-production-handbook).
**Limite grave:** li esta definição através de uma página de citações do
Goodreads, **não no livro**. A atribuição de autoria e obra é consistente, mas não
verifiquei a página, a edição nem o contexto. Antes de usar como âncora, confirmar
no livro. Registrado assim porque o conteúdo importa: "features podem sofrer
ajustes maiores neste ponto" é o **oposto** de feature lock, e "40–50% dos assets"
contradiz frontalmente a leitura de que Alpha é sobre features estarem completas.

**Desacordo B — Beta é "content complete" ou vem depois de content complete?**

Um modelo de cronograma de milestones reproduzido num guia jurídico de contratos
de publishing trata **Content Lock e Beta como marcos distintos, a três meses de
distância**:

| Marco (do modelo de contrato) | Descrição | Data |
|---|---|---|
| Feature Complete/Feature Lock (Alpha) | "All features are proven and fully functional (bugs notwithstanding). The build is ready for full feature testing through QA." | 7/30/2023 |
| Content Lock (Beta) | "The game's content is now in the build and the game can be played from beginning to end without major blockers or crashes." | 10/30/2023 |
| Beta | "The Game has all content integrated at shippable quality and all features are fully playable." | 1/30/2024 |

— [deviantlegal.com/guide/game-developers-guide-publishing-agreements/milestone-schedules-advance-payments](https://deviantlegal.com/guide/game-developers-guide-publishing-agreements/milestone-schedules-advance-payments/),
Deviant Legal (escritório de advocacia especializado em games), sem data de
publicação visível. **Fonte secundária** sobre a prática da indústria, mas
**primária** quanto ao que um advogado do setor apresenta como modelo utilizável.
**Limite:** é um exemplo ilustrativo num guia comercial, não um contrato executado
nem uma amostra de contratos. Não sustenta "a indústria faz assim". Sustenta o
ponto mais forte para o meu propósito: num instrumento onde a definição tem
consequência financeira, "Content Lock" e "Beta" **precisaram** ser separados, e a
qualidade ("shippable quality") entrou só no segundo.

Note também que este mesmo modelo distingue "Vertical Slice" de "Vertical Chunk /
Final Spec (mid-project review)" — um quarto termo que não aparece em nenhuma das
outras fontes.

**Desacordo C — "Content Complete" e "Beta" como níveis de acabamento diferentes**

O wiki GameDev Pensieve separa os dois por **qualidade final**, não por presença de
conteúdo:

> Content Complete: "All content is in the game but all of it is not final quality."
> Beta: "All content is final and only the bugs remain."

E define Vertical Slice como "a small section of the game done at Beta level
quality" — isto é, o vertical slice é definido **em função de** Beta, criando uma
dependência circular com qualquer definição de Beta.

— [gamedevpensieve.com/production/build](https://www.gamedevpensieve.com/production/build).
Wiki pessoal de um desenvolvedor, sem autoria destacada, sem data, sem citações.
**Limite:** reflete a prática de um estúdio/indivíduo. Vale como evidência de que
a variação existe, **não** como definição.

### 1.3 Onde as fontes concordam

Duas coisas apareceram consistentemente e podem ser afirmadas com mais segurança:

- **A ordem relativa.** Prototype → First Playable → Vertical Slice → Alpha → Beta
  → Release Candidate → Gold Master aparece na mesma ordem em fontes independentes.
  A ordem é mais estável que o conteúdo de cada nome.
- **First Playable = o loop central jogável, com arte provisória.** Ismail,
  GameDev Pensieve e o modelo de contrato descrevem a mesma coisa
  ("prove out a first look at the basic core gameplay loop"; "the first version of
  the game where one can play anything and feel that it is indeed a game").

E um ponto de vocabulário que vale para o desenho do gate: Ismail argumenta
explicitamente que o Vertical Slice é mal compreendido, e que ele **não** é um
protótipo de design:

> "The Vertical Slice is often misunderstood as an advanced prototype... But the
> Vertical Slice is not a design prototype, but a production prototype... The
> Vertical Slice, instead of proving out that the game works, proves that you can
> create that game."

Ou seja: o critério de saída do vertical slice é sobre **pipeline e capacidade de
produção**, não sobre o jogo ser bom. Se este framework tiver um gate de vertical
slice, essa distinção decide o que ele deve recusar.

### 1.4 Freeze: aqui há fonte melhor, e ela não é de jogos

Ao contrário de "content lock", a terminologia de *freeze* tem definição estável e
antiga na cultura de engenharia de software em geral.

O **Jargon File** (Eric S. Raymond, ed.; compilação histórica da cultura hacker)
distingue os três graus:

> "A feature freeze, for example, locks out modifications intended to introduce
> new features but still allows bugfixes and completion of existing features; a
> code freeze connotes no more changes at all. At Sun Microsystems and elsewhere,
> one may also hear references to code slush — that is, an almost-but-not-quite
> frozen state."

— [catb.org/~esr/jargon/html/F/freeze.html](http://catb.org/~esr/jargon/html/F/freeze.html).
Primária quanto ao uso documentado do termo na comunidade; é um léxico curado, não
uma norma. **Limite:** descreve uso corrente, não prescreve.

Um exemplo concreto de projeto real, com regra operacional em vez de definição
abstrata — o FAQ da lista do kernel Linux:

> "A code freeze is more restrictive than a feature freeze; it means only severe
> bug fixes are accepted."

— [lkml.iu.edu/0008.1/0425.html](https://lkml.iu.edu/0008.1/0425.html), agosto de
2000. Primária para o projeto Linux. **Limite:** é um projeto, não a indústria; e a
mensagem seguinte no mesmo thread mostra desenvolvedores discutindo que a fronteira
"bugfix vs. feature" é ela mesma disputada caso a caso.

O verbete [Freeze (software engineering)](https://en.wikipedia.org/wiki/Freeze_(software_engineering))
da Wikipédia sintetiza os tipos e é útil como mapa. **Limite:** enciclopédia,
terciária; usar para orientação, não para citar.

**Não encontrei fonte primária** para "Content Lock" como termo de engenharia — ele
parece ser específico de contratos de jogos, e as fontes que o usam são as de §1.2,
que discordam entre si.

### 1.5 Uma fonte que descartei, e por quê

[zebonastic.substack.com/p/every-stage-of-game-development-explained](https://zebonastic.substack.com/p/every-stage-of-game-development-explained)
aparece bem posicionada em busca e parece autoritativa. **Não a usei.** Sinais de
que é texto gerado por IA sem verificação: o corpo é estruturado em rubricas
"WHAT WE KNOW / WHAT WE THINK / WHAT WE DON'T KNOW"; apresenta números de grande
efeito sem nenhuma citação ("budgets exceeding $300 million", "upward of a thousand
contributors"); e atribui conclusões a "developer interviews, postmortems, and
production-methodology literature" em bloco, sem nomear um único deles.

Ironicamente, a própria página faz a observação correta de que "there is no central
authority that audits or enforces these definitions". Concordar com uma conclusão
não é razão para citar uma fonte que não mostra como chegou nela.

Mesmo tratamento para o [post no LinkedIn de Willem Delventhal](https://www.linkedin.com/posts/ifyouwillem_gamedevelopment-gamingindustry-gamedev-activity-7366454773182595074-P-uT)
("6 major milestones"): é opinião de praticante em rede social, sem fonte. Registra
que a variação de contagem existe; não define nada.

---

## 2. Stage-Gate como método formal

Este é o tópico com a **melhor procedência** do levantamento, e o mais diretamente
aproveitável para o desenho — inclusive nas críticas.

### 2.1 Anatomia formal de um gate

Robert G. Cooper é o autor do método. A formulação canônica em três componentes
aparece de forma estável em textos dele ao longo de décadas:

> "1. A set of required deliverables: what the project team must bring to the gate
> decision point. These deliverables are visible, and based on a standard menu for
> each gate, and are decided at the output of the previous gate... Deliverables are
> both hard (such as a 'field-tested prototype' or 'set of CAD design drawings')
> and soft (such as a 'full business case' or 'launch plan').
> 2. Go/Kill Criteria: the project is judged against these to make the Go/Kill and
> prioritization decisions.
> 3. Defined outputs: for example, a decision (Go, Kill, Hold or Recycle), an
> approved action plan for the next stage, the resources committed to execute the
> next stage, and the agreed-to deliverables for the next gate."

— "The Latest View on Stage-Gate",
[bobcooper.ca/images/files/articles/2/2-2-The-Latest-View-on-Stage-Gate.pdf](http://www.bobcooper.ca/images/files/articles/2/2-2-The-Latest-View-on-Stage-Gate.pdf).
**Primária**, auto-hospedada pelo autor (PDF de artigo publicado). Também em Cooper,
"The Stage-Gate Idea to Launch System", *Wiley International Encyclopedia of
Marketing* (2010), [doi 10.1002/9781444316568.wiem05014](https://onlinelibrary.wiley.com/doi/full/10.1002/9781444316568.wiem05014)
— **primária e revisada editorialmente**, a melhor citação formal do conjunto.

### 2.2 Os três tipos de critério — e o que isso corrige no desenho

Este é o achado mais útil de toda a pesquisa. Cooper **não** tem dois tipos de
critério (must-meet / should-meet); tem **três**, e o terceiro é o que a maioria
das discussões esquece:

> "**Readiness check:** These are Yes/No questions that check whether the key tasks
> have been completed, and that the deliverables are in place for that gate. A 'No'
> signals a recycle to the previous stage because the project is not ready to move on.
>
> **Must meet:** These are Yes/No or 'knockout' questions that include the minimum
> business criteria that a project must meet to move forward. A single consensus
> 'No' signals a Kill decision. Example: 'Does this project align with our business
> strategy?' If No, then Kill.
>
> **Should meet:** These are highly desirable project characteristics that are used
> to distinguish between superb projects and the minimally acceptable ones. These
> are typically in a scorecard format, and include strategic, competitive advantage
> and financial criteria, and are used for both Go/Kill and prioritization decisions."

— mesma fonte primária acima; formulação idêntica na entrada Wiley (2010).

As consequências são precisas e vale registrá-las porque um gate mal desenhado
colapsa as três em uma:

- **Readiness ≠ must-meet.** Falhar readiness é *recycle* (volta para o estágio
  anterior, o trabalho continua). Falhar must-meet é *kill* (o projeto morre). São
  respostas diferentes para perguntas diferentes: "o trabalho está feito?" versus
  "isto ainda vale a pena?". Um gate que só checa readiness não é um gate
  Stage-Gate — é uma checklist de entrega.
- **Must-meet são pass/fail e binários, e um único "No" mata.** Não há média, não
  há pontuação, não há compensação por outro critério estar ótimo.
- **Should-meet são pontuados e comparativos**, existem para ordenar projetos entre
  si, não para autorizar um. Transformar um should-meet em bloqueio é um erro de
  categoria; transformar um must-meet em pontuação é o erro inverso.
- **O gate compromete recursos, não só aprova.** Cooper insiste que gates são
  prospectivos: "Gates are not mere status reviews and project approval meetings;
  they are where resource commitments are made!" E, sobre a saída Go: "This avoids
  'approval without resources'" — [Stage-Gate®: The "Official" 2026 Version](https://community.pdma.org/blogs/robert-cooper/2026/02/03/stage-gate-the-official-2026-version),
  PDMA (Product Development and Management Association), 3 fev 2026. Primária,
  publicada em comunidade profissional.
- **Deliverables são definidos na saída do gate anterior.** A expectativa é fixada
  antes de o trabalho começar, não negociada na hora da avaliação.

**Limite sobre a versão comercial:** [stage-gate.com](https://www.stage-gate.com/blog/the-stage-gate-model-an-overview/)
publica texto quase idêntico ao de Cooper, mas Stage-Gate® é marca registrada e a
Stage-Gate International é empresa de consultoria e treinamento. É fonte primária
do método **e** material de vendedor. Para citar, prefira Cooper direto ou a
entrada Wiley.

### 2.3 As críticas documentadas

Aqui há uma assimetria epistêmica que preciso declarar: **a lista de críticas mais
completa que encontrei foi escrita pelo próprio autor do método**, resumindo
críticos, e em seguida discordando parcialmente deles. Isso é evidência boa de que
as críticas existem e são levadas a sério, e evidência fraca sobre se elas
procedem.

> "In this context, Stage-Gate has attracted a number of criticisms: It is accused
> of being too linear, too rigid, and too planned to handle more innovative or
> dynamic projects. It's not adaptive enough and does not encourage experimentation.
> It's not context-based—one size should not fit all. Its gates are too structured
> or too financially based, and the system is too controlling and bureaucratic,
> loaded with paperwork, checklists, and too much non value-added work (Becker 2006;
> Lenfle and Loch 2010). Some authors have taken issue with these criticisms,
> arguing that most are due to faulty implementation (Becker 2006), while some
> deficiencies have been corrected in more recent evolutions of Stage-Gate
> (Cooper 2011). But issues do remain..."

— Cooper, "What's Next After Stage-Gate?",
[bobcooper.ca/images/files/articles/2/9-Whats-Next-After-Stage-Gate.pdf](http://bobcooper.ca/images/files/articles/2/9-Whats-Next-After-Stage-Gate.pdf).
Primária quanto à posição de Cooper. **Limite:** **não li** Becker (2006) nem Lenfle
& Loch (2010) no original. As críticas estão citadas de segunda mão, através de quem
está respondendo a elas. Para tratar como literatura crítica, ler os originais.

Uma definição de Cooper que é diretamente útil como critério de projeto:

> "The definition of bureaucracy is 'work that adds no value'."

— mesma fonte. Serve como teste para qualquer critério que este framework
adicionar a um gate: se cumpri-lo não muda nada observável no jogo nem na decisão,
é burocracia pela própria definição do autor do método.

Cooper diz o mesmo mais cruamente em entrevista:

> "a process designed with the best intentions often ends up thwarting innovation
> because it's so cumbersome, so bureaucratic, so painful to get through. And some
> people have told me privately, in their companies, because the process is so rigid
> and old-fashioned that it's stopping innovation."

— [Dr Robert Cooper on Innovation and the Future of Stage-Gate](https://www.youtube.com/watch?v=VCWM4ZI_iHo),
YouTube. Primária (o autor falando). **Limite:** vídeo promocional de consultoria;
a evidência dos "some people" é anedótica e explicitamente privada.

A resposta de Cooper é o "Triple A" (Adaptive & flexible, Agile, Accelerated) e o
híbrido Agile-Stage-Gate: Stage-Gate define os estágios, gates e deliverables
maiores; dentro dos estágios de desenvolvimento, o trabalho corre em sprints. A
referência acadêmica é Cooper, R.G. & Sommer, A.F. (2016), "The Agile–Stage-Gate
Hybrid Model: A Promising New Approach and a New Research Opportunity", *Journal of
Product Innovation Management* 33(5): 513–526. **Limite decisivo para nós:** o
artigo é sobre **produtos físicos** (o caso ilustrativo é a LEGO, sobre produção de
brinquedos, não de jogos digitais), e os próprios autores registram que "much
research is needed" e que "little empirical evidence supports this".

### 2.4 Stage-Gate aplicado a jogos: a literatura é rala

Procurei especificamente por avaliação de stage-gate em desenvolvimento de jogos.

O que existe de revisado por pares e relevante é indireto — Politowski et al., "Are
the Old Days Gone? A Survey on Actual Software Engineering Processes in Video Game
Industry", [arXiv:2009.02448](https://ar5iv.labs.arxiv.org/html/2009.02448). Estudo
acadêmico baseado em postmortems. Achado pertinente:

> "significant facts were found on publishers and milestones. Once a company
> (including indie) made a deal with a publisher, normally a set of milestones are
> predefined, and when a portion of the game must be presented. These milestones are
> usually underestimated"

e a conclusão geral de que "iterative process is actually mainstream in video game
industry and agile practices adoption is increasing". **Limite:** é survey de
postmortems publicados (amostra autosselecionada — quem escreve postmortem não é
quem fracassou em silêncio), e **não** é um estudo sobre stage-gate; não avalia
gates, avalia processos declarados.

Encontrei também uma monografia finlandesa de revisão de literatura sobre
Stage-Gate em desenvolvimento de jogos ([theseus.fi](http://theseus.fi/handle/10024/907423)
e resumo em [exa.ai](https://exa.ai/library/publication/wl00ksq0b1t)), cuja
conclusão é que o híbrido Agile-Stage-Gate "is a good example of such hybrid model
in which game developers should keep an eye on". **Limite forte:** trabalho de
conclusão de curso, revisão de literatura sem dados próprios, em finlandês, sem
revisão por pares. Não sustenta afirmação sobre a indústria.

**Conclusão honesta do tópico:** não encontrei estudo empírico revisado por pares
que avalie stage-gate aplicado a jogos. A transferência do método para jogos é
plausível e praticada (os milestones contratuais de §1.2 são gates de facto), mas
**não é uma prática validada na literatura**, e o framework não deve alegar que é.

---

## 3. Certificação de plataforma

Este é o único lugar onde existe gate real, público, versionado e citável. A
diferença entre as plataformas é enorme, e não na direção que a reputação sugere.

### 3.1 Xbox — integralmente público, e o melhor material disponível

A Microsoft publica os **Xbox Requirements (XRs) completos** no Microsoft Learn, sem
NDA, com número de versão e data. É a fonte primária mais forte do levantamento
inteiro.

- Console: [Xbox Requirements for Xbox Console Games](https://learn.microsoft.com/en-us/gaming/gdk/docs/store/policies/console/certification-requirements?view=gdk-2604)
  — "Version 16.3 - 07/01/2026". Contei **40 XRs** nesta página.
- Casos de teste: [console-certification-requirements-and-tests](https://learn.microsoft.com/en-us/gaming/gdk/docs/store/policies/console/console-certification-requirements-and-tests?view=gdk-2510)
- PC/mobile: [live-policies-pc](https://learn.microsoft.com/en-us/xbox/gdk/docs/store/policies/pc/live-policies-pc?view=gdk-2604)
- Processo: [certification-guide](https://learn.microsoft.com/en-us/gaming/game-publishing/concepts/certification/certification-guide)

Três propriedades de desenho que a Microsoft implementa e que são diretamente
transferíveis:

**A consequência é binária e declarada.**

> "Failure to comply with XRs will result in your title being denied the ability to
> publish to the Microsoft store. Titles which are already published might be
> removed if they do not maintain compliance with XRs."

**O subconjunto testado é marcado explicitamente.** "XRs that are tested in
Certification are identified with an asterisk (*)." Isto é, o documento separa
*requisito* de *requisito verificado* — exatamente a distinção entre alegação e
evidência. Nem todo XR é testado; a Microsoft diz qual é qual.

**O gate tem duas fases com ordem obrigatória.** BVTs (Build Verification Tests)
primeiro; só "Once a product has passed BVTs, it is scheduled for Xbox Requirement
(XR) testing". E a saída é um relatório Pass/Fail com itens nomeados: "If a Fail
report is issued, the title is not allowed to release to the public and the CFRs in
the report must be fixed before resub[mission]".

Exemplos concretos de requisito público e observável:

> **XR-001: Title Stability *** — cita a política de loja 10.4.2: "Products must
> start up promptly, continue to run, and remain responsive to user input. Products
> must shut down gracefully and not close unexpectedly."

> **XR-003: Title Quality for Submission *** — "Titles must be fully functional and
> testable when submitted for certification. This includes all client code,
> submission artifacts, and downloadable content. Titles must be packaged cleanly
> with no failures using the current version of Submission Validator. Submission
> Validator logs must be included with the submission."
>
> E, sob "Title integrity": "Titles must be free from severe issues such as crashes,
> freezes, unplayable frame rates, bugs causing major progression hindrances, or
> graphical corruption."

Note que XR-003 exige **o log da ferramenta junto com a entrega** — o gate não
aceita a afirmação de que passou, exige o artefato. E que "fully functional and
testable" é um critério de *testabilidade*, anterior a qualquer critério de
qualidade: o gate recusa builds que impedem a própria avaliação.

**Os dados de falha, publicados pela própria Microsoft.** A página
[Top failing test cases for console](https://learn.microsoft.com/en-us/gaming/gdk/docs/store/policies/console/console-topfailingtestcases)
("Version 2.0 - 4/01/2024") publica a distribuição:

| Requisito | Caso de teste | Distribuição |
|---|---|---|
| XR-001 Title Stability | 001-01 Title Stability | 38% |
| XR-003 Title Integrity | 003-02 Title Integrity | 14% |
| XR-045 Xbox Network and Account Privileges | 045-01 Respect User Privileges | 11% |
| XR-064 Joinable Game Sessions | 064-02 Joining from Same Game | 8% |
| XR-055 Achievements and Gamerscore | 055-01 Achievements | 7% |
| XR-124 Game Invitations | 124-01 Game Invitations | 6% |

**Limite importante:** a Microsoft **não publica** tamanho de amostra, janela
temporal nem metodologia. "38%" é uma distribuição entre falhas, não uma taxa de
falha — não diz que 38% dos jogos falham, diz que 38% das falhas foram dessa causa.
Não repetir esse número como se fosse taxa de reprovação.

O que ele sustenta bem: **as falhas concentram-se em estabilidade e completude
básicas** (38% + 14% = 52% em "não trava" e "é testável de ponta a ponta"), não em
requisitos exóticos de plataforma. Para desenhar um gate, isso é orientação forte
sobre onde pôr peso.

### 3.2 Steam — público, e mais frouxo do que se supõe

Valve documenta o processo publicamente em
[partner.steamgames.com/doc/store/review_process](https://partner.steamgames.com/doc/store/review_process)
e [.../releasing](https://partner.steamgames.com/doc/store/releasing). Primária.

Estrutura: **duas checklists com dependência sequencial** — store presence e build,
e "you'll need to submit your store page for review before you can submit your build
for review". Prazo publicado: "typically takes 3-5 business days", com recomendação
de 7 dias úteis. É o único prazo de certificação que encontrei publicado pelo
próprio detentor de plataforma.

Critérios concretos e verificáveis:

> - "Your product will need to start up properly. This means that your product must
>   successfully launch in all supported operating systems listed on the store page."
> - "All supported features listed on the store page will need to be implemented in
>   the current build. If you intend to add a feature in the future, you'll need to
>   remove the selected feature in the Basic Info tab until it is implemented and
>   released."
> - "Your product must use Steam Wallet for any in-game transactions."

O segundo é elegante e vale copiar como padrão: o critério não é "o jogo tem
features X, Y, Z", é **coerência entre o que foi prometido e o que existe**. A
promessa é a variável de ajuste; se a feature não existe, remova a promessa. Um
gate assim nunca é arbitrário, porque o alvo é declarado pelo próprio time.

E um contraste explícito com a cultura de code freeze:

> "Upload a mostly final build [to] default branch (The build should include all the
> features described on your store page, but doesn't have to be absolutely final. You
> can continue updating your build during and after the review process)."
>
> "You can continue to make updates and changes to your build after review and
> approval, but you should be submitting a near-final build for review."

Valve **não** exige congelamento. O gate dela é sobre coerência e inicialização, não
sobre imutabilidade.

### 3.3 Apple — público, com um número sem metodologia

As [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
são públicas e primárias. A diretriz relevante:

> **2.1 App Completeness** — "(a) Submissions to App Review, including apps you make
> available for pre-order, should be final versions with all necessary metadata and
> fully functional URLs included; placeholder text, empty websites, and other
> temporary content should be scrubbed before submission. Make sure your app has been
> tested on-device for bugs and stability before you submit it, and include demo
> account info (and turn on your back-end service!) if your app includes a login...
> We will reject incomplete app bundles and binaries that crash or exhibit obvious
> technical problems."

E, na mesma seção, uma regra que é o oposto exato de um marco "beta":

> "Demos, betas, and trial versions of your app don't belong on the App Store – use
> TestFlight instead."

A página [App Review](https://developer.apple.com/distribute/app-review/) da Apple
afirma:

> "On average, over 40% of unresolved issues are related to guideline 2.1: App
> Completeness, which covers crashes, placeholder content, incomplete information,
> and more."

**Limite:** a Apple não publica metodologia, período nem definição de "unresolved
issues". Convergente com o dado da Microsoft (completude e estabilidade dominam as
reprovações), mas é afirmação institucional não auditável. Citar como afirmação da
Apple, não como fato medido.

### 3.4 PlayStation — nada público de utilidade atual

A **TRC (Technical Requirements Checklist)** está atrás de NDA em
partner.playstation.com. **Não encontrei nenhum texto público e atual da TRC.**
Tudo que circula sobre "categorias da TRC" e requisitos específicos vem de blogs de
terceiros sem acesso citável, e alguns são demonstravelmente inventados (§3.6).

Existe um artefato histórico: um PDF da *Technical Requirements Checklist for
PlayStation Software* da era PS1 está espelhado em
[psx.arthus.net/sdk/Psy-Q/DOCS/TECHNOTE/mtrc13.pdf](https://psx.arthus.net/sdk/Psy-Q/DOCS/TECHNOTE/mtrc13.pdf).
**Não recomendo usá-lo, por três razões independentes**, e registro que ele existe
só para que ninguém "descubra" depois e pense que achou ouro:

1. O documento se declara confidencial na primeira página ("The content of this book
   is Confidential Information of Sony Computer Entertainment"). Não houve
   publicação autorizada; é vazamento.
2. É dos anos 1990. Não descreve a TRC de PS5 de forma alguma.
3. Ele próprio diz "The information ... is subject to change without notice" e
   instrui a confirmar a versão vigente com o representante Sony.

O único valor legítimo dele é histórico, e um detalhe estrutural que se alinha com
Cooper: a checklist usava seções condicionais — determina-se primeiro se a seção é
"Applicable" ao título, e então "must meet all requirements" dela. Escopo antes de
critério. Mas isso está melhor documentado em fontes que posso citar.

### 3.5 Nintendo — processo público, critérios sob NDA

A página [The Process](https://developer.nintendo.com/the-process) do Nintendo
Developer Portal é primária e confirma que o gate existe, sem revelar critérios:

> "Before you can publish your product, you'll need to submit it to Nintendo for
> reviewing. This process is necessary to ensure that the game can be safely played
> and conforms to Nintendo production standards."

E o acesso ao resto é explicitamente condicionado a NDA: "accept the Non-Disclosure
Agreement and Terms of Service to gain access to platform SDKs".

Existe um "Nintendo Switch Publishing Guide v1.0" (autoria Nintendo) espelhado num
servidor de terceiros ([crimeoclockgame.fr/...](https://crimeoclockgame.fr/ftp.justforgames.com/_spec/NINTENDO_Switch_charte-guidelines/Nintendo%20Switch%20Publishing%20Guide%20v1.0.pdf))
que descreve o Lotcheck em nível de processo:

> "Your title needs to be tested for platform compatibility and guideline compliance
> before it can be released. This testing is performed by Nintendo's global Lotcheck
> teams at NOA, NOE and NCL. Platform compatibility ensures that your title will run
> without a problem on a retail console in a consumer environment, and guideline
> compliance ensures that basic standards are met when it is running on our platform.
> If your title fails testing, you will need to submit a revised version until it can
> pass for release."

**Limite:** conteúdo de autoria Nintendo, mas redistribuído em servidor de terceiros,
versão 1.0 sem data, sem garantia de autorização nem de atualidade. Trate como
indicativo do processo, não como requisito vigente. A distinção que ele faz é útil e
plausivelmente estável: Lotcheck verifica **compatibilidade de plataforma e
conformidade com guidelines**, não se o jogo é bom nem se está livre de bugs.

### 3.6 Uma fonte que verifiquei e concluí ser fabricada

[code-note-vr.vercel.app/console-development---certification](https://code-note-vr.vercel.app/console-development---certification)
aparece em busca com aparência técnica e oferece exatamente o que se procura:
requisitos numerados, em tabela, com IDs. Por exemplo, afirma que a Microsoft usa
"TCR (Technical Certification Requirements)" com itens como:

> "TCR-ACC001 | Accessibility | Game must support button remapping (or use system
> remapping)"
> "TCR-ACC002 | Accessibility | Game must support Narrator (screen reader) in menus"

**Verifiquei contra a documentação da Microsoft e isto não procede.** Busquei
"TCR" nas páginas oficiais de XR de console e de casos de teste: **zero
ocorrências**. A nomenclatura atual da Microsoft é XR ("TCR" é terminologia da era
Xbox 360). E, entre os 40 XRs da página de console, **nenhum é de acessibilidade** —
o que é consistente com §4.2, onde a Microsoft diz explicitamente que suas
guidelines de acessibilidade *não* são critério de conformidade. A mesma página
oferece IDs de Lotcheck no formato "LOT-00x-003" e a estimativa "expect 50–150+ test
cases", sem fonte.

Conclusão: IDs plausíveis e inexistentes, exatamente o modo de falha que este
framework precisa evitar. Registrado aqui como caso de teste: um requisito com ID
parece verificável e não é. **A verificação não é "a fonte parece técnica", é "o ID
existe no documento do detentor da plataforma".**

Mesma ressalva, em grau menor, para os prazos de certificação que circulam ("2–6
semanas", "Lotcheck 30 dias", "PlayStation 3–4 semanas"). Aparecem em
[gamedevproducer.com](https://gamedevproducer.com/posts/console-game-certification-process-for-producers/),
[productionalchemist.com](https://www.productionalchemist.com/p/production-101-15-understanding-publishing)
e vários outros, sempre sem primária. São blogs de produtores — plausíveis como
experiência relatada, inúteis como número. O único prazo publicado pelo próprio
detentor que encontrei é o da Valve (3–5 dias úteis).

---

## 4. Diretrizes de acessibilidade como checklist

### 4.1 Game Accessibility Guidelines — a estrutura mais próxima de um gate graduado

[gameaccessibilityguidelines.com](https://gameaccessibilityguidelines.com/) —
**primária**, no ar desde setembro de 2012.

**Procedência.** Não é um corpo de padronização. É "a collaborative effort between a
group of studios, specialists and academics". O projeto foi iniciado e coordenado
por Ian Hamilton, designer e consultor independente, que o descreve como "self-initiated
project" ([ian-hamilton.com/project/game-accessibility-guidelines](https://ian-hamilton.com/project/game-accessibility-guidelines/)).
Colaboradores listados incluem Barrie Ellis (OneSwitch), Gareth Ford-Williams (BBC),
Lynsey Graham (Blitz Games Studios), Dimitris Grammenos, Ed Lee, Jake Manion
(Aardman Digital) e Thomas Westin (Universidade de Estocolmo). Cobertura de imprensa
contemporânea ao lançamento em [Polygon, 18 set 2012](https://www.polygon.com/gaming/2012/9/18/3354546/game-accessibility-guidelines-project-aims-to-help-developers/)
(secundária, confirma data e autoria).

**Os três níveis**, textualmente do site:

- **Basic** — "Easy to implement, wide reaching and apply to almost all game mechanics."
- **Intermediate** — "Require some planning and effort but still just good general game design."
- **Advanced** — "Complex adaptations for profound impairments and specific niche mechanics."

O eixo dos níveis é **custo de implementação e amplitude de alcance**, não gravidade
da exclusão. Isso importa: "Basic" não significa "o mínimo ético", significa "o
barato que atinge muita gente".

**Contagem.** Contei as entradas da página [full-list](https://gameaccessibilityguidelines.com/full-list/)
programaticamente em 9 set 2026:

| Categoria | Basic | Intermediate | Advanced |
|---|---|---|---|
| Motor | 7 | 11 | 4 |
| Cognitive | 7 | 17 | 6 |
| Vision | 7 | 13 | 10 |
| Hearing | 4 | 11 | 3 |
| Speech | 1 | 4 | 2 |
| General | 5 | 8 | 3 |
| **Total** | **31** | **64** | **28** |

123 entradas. **Limite:** é minha contagem da página naquela data, não um número que
o site publique. O site não anuncia total, e as entradas **repetem-se entre
categorias**.

Essa repetição é o detalhe estrutural mais importante para desenho de gate, e é
fácil de errar: **o nível de um critério não é propriedade do critério, é
propriedade do par (categoria, critério)**. "Include an option to adjust the game
speed" é **Basic** em Motor e **Intermediate** em Cognitive. "Provide separate volume
controls or mutes for effects, speech and background / music" é **Basic** em Hearing
e **Intermediate** em Cognitive e Vision. Ou seja: a mesma feature é barata-e-ampla
para um público e custosa-ou-nichada para outro. Um gate que trate "nível" como
atributo único do item vai atribuir o nível errado a metade da lista.

**Exemplos de critérios observáveis** (bons candidatos a verificação):

- "Allow controls to be remapped / reconfigured" (Motor, Basic)
- "Ensure that all areas of the user interface can be accessed using the same input method as the gameplay" (Motor, Basic)
- "Ensure no essential information is conveyed by a fixed colour alone" (Vision, Basic)
- "Ensure subtitles/captions are or can be turned on before any sound is played" (Hearing, Intermediate)
- "Include a cool-down period (post acceptance delay) of 0.5 seconds between inputs" (Motor, Advanced)
- "Base speech recognition on hitting a volume threshold (eg. 50%) instead of words" (Speech, Advanced)
- "Include some people with impairments amongst play-testing participants" (General, Intermediate)

**Limite crítico para uso como gate:** a esmagadora maioria **não tem limiar
numérico**. "Provide high contrast between text/UI and background" (Vision, Basic)
não define razão de contraste — ao contrário do WCAG, que define 4.5:1. Dos 123
itens, encontrei número em pouquíssimos (0.5 s, 50%). Portanto:
verificação depende de julgamento humano declarado, não de medição automática, e um
gate que alegar "critério objetivo" sobre a maioria destes itens está mentindo.
Também não há mecanismo de conformidade, selo, nível de aderência declarável nem
auditoria — nada aqui é certificável.

### 4.2 Xbox Accessibility Guidelines — 23 guidelines, e a própria Microsoft diz que não é gate

**23 guidelines, numeradas 101–123.** Confirmado em duas páginas primárias da
Microsoft: o [version history](https://learn.microsoft.com/en-us/xbox/accessibility/xag-version-history),
que lista a "Version 1.0.0 Oct 19, 2019" com a tabela completa de 101 a 123, e o
[accessibility-overview](https://learn.microsoft.com/en-us/xbox/gdk/docs/gdk-dev/game-principles/accessibility/accessibility-overview?view=gdk-2604),
que enumera os 23 tópicos com link individual.

A lista: 101 Text display · 102 Contrast · 103 Additional channels for visual and
audio cues · 104 Subtitles and captions · 105 Audio customization · 106 Screen
narration · 107 Input · 108 Game difficulty options · 109 Object clarity · 110
Haptic feedback · 111 Audio description · 112 UI navigation · 113 UI focus handling ·
114 UI context · 115 Error messages and destructive actions · 116 Time limits · 117
Visual distractions · 118 Photosensitivity · 119 STT/TTS chat · 120 Communication
experiences · 121 Accessible feature documentation · 122 Accessible customer support ·
123 Advanced best practices.

**Estrutura interna de cada XAG** (nove seções, da página
[certification-mgats](https://learn.microsoft.com/en-us/gaming/game-publishing/concepts/certification/certification-mgats)):
Goal · Overview · Scoping questions · Background and foundational information ("101")
· Key areas to target · Implementation guidelines · Example content · Gaming personas
· Resources and tools.

Duas dessas seções são desenho de gate melhor que o de muitos gates:

- **Scoping questions** resolvem aplicabilidade **antes** de critério: "This section
  lists primary game elements and mechanics that are directly related to each XAG, and
  prompts developers to determine whether their title contains these elements." Um
  critério sobre legendas não se aplica a um jogo sem fala — e a estrutura pergunta
  isso primeiro, em vez de gerar um "N/A" depois. Mesma lógica das seções
  "Applicable" de §3.4 e do readiness check de Cooper.
- **Gaming personas** ligam cada critério a quem é excluído se ele falhar. O critério
  carrega o motivo, não só a regra.

**O limite mais importante do tópico inteiro, nas palavras da Microsoft:**

> "The XAGs are not intended to act as a checklist to validate any type of compliance
> or legal requirements. Rather, they seek to ensure that the user experience in a game
> is enjoyable and playable for everyone."

E o serviço de teste correspondente é **opcional e pago**:

> "Microsoft Game Accessibility Testing Service (MGATS) is an optional testing service
> for developers and publishers of Xbox and PC games."

com "You will also need to provide a Purchase Order to the sum of the requested
submission type" e SLA de "7 business days". Submissões dividem-se em Standard
(single player, sem comunicação) e Advanced (múltiplos modos e/ou comunicação
multiplayer).

**Portanto: acessibilidade não é gate de certificação no Xbox.** Os XRs de
certificação (§3.1, 40 itens) não incluem acessibilidade; as guidelines de
acessibilidade existem em documento separado que se declara não-conformidade; e o
teste é serviço opcional faturado. Qualquer material que afirme "o Xbox exige
remapeamento de botões para certificar" (como §3.6) está errado.

**Inconsistência menor nas fontes da Microsoft**, registrada por honestidade: a
página de version history datou a versão inicial em "Oct 19, 2019", enquanto a
narrativa da página MGATS diz que "the original XAGs were launched in January 2020".
Não sei qual é a data de lançamento público; provavelmente uma é criação interna e
outra é publicação, mas isso é minha conjectura, não algo que as páginas digam.

### 4.3 Relação com WCAG 2.2: mais fraca do que se costuma dizer

Esta é uma pergunta onde a resposta correta é largamente negativa, e é importante
não preencher com plausibilidade.

**WCAG 2.2 é norma para conteúdo web.** É W3C Recommendation. Jogos não são conteúdo
web, e não há caminho de conformidade WCAG para um jogo.

A ponte que o W3C oferece é o **WCAG2ICT** — [w3.org/TR/wcag2ict](https://www.w3.org/TR/wcag2ict/),
"Guidance on Applying WCAG 2 to Non-Web Information and Communications Technologies".
Primária. E ela se autolimita na primeira frase:

> "It provides informative guidance (guidance that is not normative and does not set
> requirements)."
>
> "This document is a Working Group Note (in contrast to WCAG 2.0, WCAG 2.1, and
> WCAG 2.2, which are W3C Recommendations)."

Jogos e consoles entram no WCAG2ICT sob a categoria **"closed functionality"** — ICT
que não permite conectar tecnologia assistiva arbitrária. Interessante para
procedência: eles foram **adicionados por comentário público**, no [issue 466 do
repositório w3c/wcag2ict](https://github.com/w3c/wcag2ict/issues/466), onde a
sugestão de incluir "Gaming platforms or consoles" foi aceita pela task force. Isto
é, a aplicabilidade a jogos é recente e foi retroencaixada.

E a consequência que o próprio W3C tira é o oposto de "aplique WCAG aos seus jogos":

> "ICT with closed functionality does not allow the use of some assistive technologies
> for some or all of the ICT's functions... **To the extent the ICT is closed,
> following the WCAG success criteria by themselves will not ensure that non-web
> software is accessible.**"

O documento traz um Apêndice A, "Success Criteria Problematic for Closed
Functionality", listando quais critérios não transferem. E o W3C não recomenda exigir
AAA como política: "it is not recommended that Level AAA conformance be required as a
general policy for non-web documents and non-web software."

**Não encontrei crosswalk oficial** entre as Game Accessibility Guidelines e o WCAG,
nem entre os XAGs e o WCAG. Nenhuma das duas reivindica mapeamento. Se o framework
quiser afirmar "este critério corresponde ao WCAG 2.2 SC 1.4.3", esse mapeamento
seria trabalho editorial deste repositório, e teria de ser declarado como tal.

### 4.4 CVAA: o único gate de acessibilidade juridicamente vinculante que encontrei

Nos EUA, e apenas para funções de comunicação.

Guia do FCC (primária, agência reguladora):
[fcc.gov/consumers/guides/accessibility-communications-video-games](https://www.fcc.gov/consumers/guides/accessibility-communications-video-games)

> "Video game companies must ensure that any advanced communications services they
> offer, such as voice or text chat, are accessible and usable by individuals with
> disabilities, **unless doing so is not achievable**."

E a delimitação, do próprio FCC:

> "The accessibility rules mentioned in this guide only apply to video games and
> associated services and platforms that provide advanced communications services that
> allow players to communicate with each other. **These rules do not cover
> non-communications aspects of video games.**"

**Cronologia:** a isenção da indústria de jogos expirou em 31 dez 2018; jogos lançados
a partir de 1 jan 2019, e jogos anteriores que recebam "substantial upgrades", estão
sujeitos. Reportado por [Game Developer](https://www.gamedeveloper.com/game-platforms/cvaa-accessibility-rules-come-into-effect-for-games-as-fcc-waiver-expires)
(secundária, imprensa setorial) e por análises jurídicas de escritórios
([Perkins Coie via JDSupra](https://www.jdsupra.com/legalnews/new-accessibility-requirements-in-33893/),
[Frankfurt Kurnit](https://fkks.com/news/video-games-with-advanced-communications-services-must-now-be-accessible-to-players-with-disabilities)) —
secundárias, mas de advogados escrevendo sobre a própria especialidade.

**A obrigação concreta e verificável é de registro, não de feature.** As instruções
de arquivamento do FCC ([RCCCI-Filing-Instructions-2025.pdf](https://www.fcc.gov/sites/default/files/RCCCI-Filing-Instructions-2025.pdf),
primária) exigem manter registros de:

> "information about the manufacturer's or provider's efforts to consult with
> individuals with disabilities; descriptions of the accessibility features of its
> products and services; and information about the compatibility of such products and
> services with peripheral devices or specialized customer premises equipment"

com certificação anual até 1º de abril.

Isso é um achado de desenho relevante: o gate legal mais real do conjunto **não exige
que a acessibilidade exista**, exige que o esforço e o raciocínio de "achievability"
estejam **documentados**. É um gate sobre procedência de decisão, não sobre estado do
produto — o que se alinha bem com o princípio deste framework.

**Limites:** jurisdição dos EUA; só features de comunicação; "not achievable" é uma
defesa disponível cujo teste eu não pesquisei; e não sou advogado — nada disto é
orientação jurídica.

---

## 5. Definition of Done e quality gates em engenharia de software

### 5.1 Definition of Done: a semântica de recusa está no texto primário

Scrum Guide 2020 (Ken Schwaber e Jeff Sutherland),
[scrumguides.org](https://scrumguides.org/scrum-guide.html) — primária.

> "The Definition of Done is a formal description of the state of the Increment when
> it meets the quality measures required for the product."
>
> "**If a Product Backlog item does not meet the Definition of Done, it cannot be
> released or even presented at the Sprint Review. Instead, it returns to the Product
> Backlog for future consideration.**"

Essa segunda frase é exatamente a mecânica pedida: recusa com destino definido. Não é
"marque como pendente", é "sai do incremento e volta ao backlog". Compare com o
*recycle* de Cooper (§2.2) — a mesma ideia, dois vocabulários.

Três regras estruturais adicionais, todas do texto primário:

- **Herança com piso, não substituição.** "If the Definition of Done for an increment
  is part of the standards of the organization, all Scrum Teams must follow it as a
  minimum." O time pode **adicionar**, não remover.
- **Uma DoD por produto, não por time.** "If there are multiple Scrum Teams working
  together on a product, they must mutually define and comply with the same Definition
  of Done."
- **É compromisso, não artefato.** A DoD é o "commitment" do Increment, par de Product
  Goal (Product Backlog) e Sprint Goal (Sprint Backlog).

**Limite decisivo, e é uma ausência deliberada:** o Scrum Guide **não fornece nenhum
critério**. Não há lista, não há exemplo, não há mínimo sugerido. A DoD é um
contêiner cujo conteúdo é do time. Portanto o Scrum Guide sustenta a **forma** do
gate (o que acontece quando falha, quem define, como herda) e **nada** sobre o
conteúdo. Qualquer "DoD padrão" que apareça em blog é invenção de terceiros, não
Scrum. Além disso, o Scrum Guide é documento de dois autores publicado por eles
mesmos — influente, mas não uma norma de corpo de padronização.

### 5.2 Quality gate como implementado por ferramenta

SonarQube é a implementação de referência, e a documentação é primária (embora de
fornecedor comercial):
[Introduction to quality gates](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates)

> "A quality gate consists of a set of conditions against which the code is measured
> during analysis. A condition is defined on either new code or overall code.
> Depending on the result, the code will pass or fail the quality gate."

O gate embutido "Sonar way" tem **quatro condições**:

> - No new issues are introduced
> - All new Security Hotspots are reviewed
> - New code test coverage is greater than or equal to 80.0%
> - Duplication in the new code is less than or equal to 3.0%

**O mecanismo anti-rigidez vale copiar.** As condições incidem sobre **código novo**,
não sobre o total ("Clean as You Code"), e a documentação **recomenda contra** medir
o total: "When your quality gate is focused on new code, we do not recommend adding
conditions for overall code." A justificativa: "you aren't worried about having to
meet those standards in old code and having to remediate someone else's code."

Isto resolve o modo de falha óbvio de um gate retroativo — um projeto com dívida
herdada nunca passa, então o gate é desligado. Ao medir só o delta, o gate é sempre
alcançável e nunca precisa ser suspenso. Para um framework que quer gates que
recusem de verdade, "sempre alcançável" é o que impede que a recusa seja
contornada.

**Limite:** documentação de produto comercial. **Não encontrei justificativa empírica
publicada** para 80.0% e 3.0%; são padrões de fornecedor. O próprio SonarSource não
apresenta estudo que os sustente.

### 5.3 Quality gate como métrica gamificada: as críticas, com atribuição correta

**Primeiro, corrigir uma atribuição que circula errada em quase todo blog do tema.**

A frase "When a measure becomes a target, it ceases to be a good measure" é
universalmente atribuída a Charles Goodhart. **Goodhart não escreveu isso.** A cadeia
real, que verifiquei no PDF do artigo original:

- **Goodhart (1975)**, sobre política monetária britânica, escreveu algo mais estreito:
  "Any observed statistical regularity will tend to collapse once pressure is placed
  upon it for control purposes."
- **Keith Hoskin (1996)**, "The 'awful idea of accountability'", generalizou.
- **Marilyn Strathern (1997)**, "'Improving ratings': audit in the British University
  system", *European Review* 5(3): 305–321, é onde a frase famosa aparece — e ela a
  atribui a Hoskin, não a Goodhart. Texto verificável em
  [gwern.net/doc/statistics/decision/1997-strathern.pdf](https://gwern.net/doc/statistics/decision/1997-strathern.pdf):

  > "When a measure becomes a target, it ceases to be a good measure. The more a 2.1
  > examination performance becomes an expectation, the poorer it becomes as a
  > discriminator of individual performances. Hoskin describes this as 'Goodhart's law',
  > after the latter's observation on instruments for monetary control..."

Corroborado independentemente por uma página acadêmica de Cambridge
([damtp.cam.ac.uk/user/mem2/papers/LHCE/goodhart.html](https://www.damtp.cam.ac.uk/user/mem2/papers/LHCE/goodhart.html)),
que também atribui a reformulação a Strathern "following Hoskin (1996)".

O contexto original de Strathern é **auditoria universitária** — avaliação
institucional produzindo distorção. É analogia forte para gates de processo, e é
melhor citá-la corretamente do que repetir a atribuição errada.

**Segundo, a fonte mais valiosa: a posição do Google, que é pró-gate *e* cética.**

"Code Coverage Best Practices", por Carlos Arguelles, Marko Ivanković e Adam Bender,
Google Testing Blog, 7 ago 2020 — primária, autores incluem o primeiro autor do paper
FSE 2019 de §5.4. (A página bloqueia acesso automatizado; li via
[snapshot do Internet Archive](https://web.archive.org/web/20260901105333/https://testing.googleblog.com/2020/08/code-coverage-best-practices.html).)

O texto **defende** usar gate — e no mesmo parágrafo diz como ele apodrece:

> "**We should gate deployments that do not meet our code coverage standards.** Teams
> should debate and decide which gating mechanism makes sense to them. You should
> however be careful that **it doesn't turn into being treated as a checkbox that is
> required to be filled, as it can backfire (pressure to 'hit the metric' almost never
> yields the desired outcome).** There are many mechanisms available: gate on coverage
> for all code vs gate on coverage to new code only; gate on a specific hard-coded code
> coverage number vs gate on delta from prior version..."

E, sobre mandatos numéricos:

> "There is no 'ideal code coverage number' that universally applies to all products...
> **We cannot mandate every single team should have x% code coverage**; this is a
> business decision best made by the owners of the product with domain-specific
> knowledge... **Be mindful that engineers may start treating your target like a
> checkbox and avoid increasing coverage beyond the target, even if doing so would be
> prudent.**"
>
> "Although there is no 'ideal code coverage number,' at Google we offer the general
> guidelines of 60% as 'acceptable', 75% as 'commendable' and 90% as 'exemplary.'
> However we like to stay away from broad top-down mandates and encourage every team to
> select the value that makes sense for their business needs."

Três afirmações adicionais que reorientam o desenho de critério:

> "More important than the percentage of lines covered is human judgment over the
> actual lines of code (and behaviors) that aren't being covered... **What's not covered
> is more meaningful than what is covered.**"

> "You must treat it with the understanding that it's a **lossy and indirect metric
> that compresses a lot of information into a single number** so it should not be your
> only source of truth."

> "**It is an open research question whether code coverage alone reduces defects**, but
> our experience shows that efforts in increasing code coverage can often lead to
> culture changes in engineering excellence."

Essa última é notável: a empresa que mais mede cobertura no mundo diz que o elo entre
cobertura e menos defeitos é **questão aberta de pesquisa**, e chama a própria
justificativa de "our experience". Esse é o registro de limite que o framework deveria
imitar.

### 5.4 Evidência revisada por pares

- Ivanković, Petrović, Just, Fraser, **"Code Coverage at Google"**, ESEC/FSE 2019, pp.
  955–963. [PDF](https://homes.cs.washington.edu/~rjust/publ/google_coverage_fse_2019.pdf).
  Empírico: cobertura de 1 bilhão de linhas/dia em 7 linguagens, 5 anos de dados
  históricos, 512 respostas de 3000 desenvolvedores pesquisados. Relevante: cobertura
  **não é obrigatória** no Google, e ainda assim a adoção cresceu (>90% dos projetos em
  Q1 2018, segundo o [Q&A na IEEE Spectrum](https://spectrum.ieee.org/qa-how-google-implements-code-coverage-at-massive-scale)) —
  isto é, adoção sem mandato. **Limite:** um único ambiente, sem grupo de controle;
  não testa se a cobertura reduz defeitos.
- Ivanković et al., **"Productive Coverage: Improving the Actionability of Code
  Coverage"**, ICSE 2024. [PDF](https://homes.cs.washington.edu/~rjust/publ/productive_coverage_icse_2024.pdf).
  Metodologicamente mais forte: **experimento de campo escondendo a informação de
  cobertura em 30 mil code reviews selecionados aleatoriamente**. Premissa explícita
  do artigo é que tratar todo código como igualmente importante "is not only in stark
  contrast to how developers actually use code coverage" — os autores propõem gerar
  alvos de teste a partir de (1) código similar bem testado e (2) código similar
  frequentemente executado em produção, em vez de razão uniforme.

Isto é, a linha de pesquisa mais séria sobre o assunto está migrando de **"limiar
sobre uma razão"** para **"o gate aponta o que especificamente falta"**. Para um
framework cujo princípio é registrar o limite de cada afirmação, apontar a lacuna
nomeada é mais compatível do que emitir um número agregado.

### 5.5 As críticas de blog: úteis como sintoma, não como evidência

[roamingpigs.com/field-manual/test-coverage-lie](https://roamingpigs.com/field-manual/test-coverage-lie/)
e [Rodrigo Borrego Bernabé no Medium](https://medium.com/@rodrigobb/dont-use-code-coverage-as-a-kpi-ea8925d79554)
argumentam contra cobertura como quality gate. O segundo cita nominalmente o "Sonar
Quality Gate" como o problema, e faz uma observação de incentivo que soa verdadeira:
"What love will tests receive if the developer is frustrated and sees how the PR
cannot be integrated in main because the modified file has only 70% code coverage?"

**Limite:** ambos são posts de opinião, sem dados próprios, sem revisão. Ambos citam
Goodhart com a atribuição errada de §5.3. Ambos afirmam que desenvolvedores "escrevem
testes lixo" para bater a meta **sem medir isso**. Registro que a crítica circula
amplamente — o que é em si um fato relevante sobre a cultura em que este framework vai
operar — mas para sustentar a crítica prefira Google §5.3, que diz coisa parecida com
autoridade e com ressalva própria.

---

## 6. O que NÃO encontrei fonte confiável

Lista explícita, para que nada aqui seja preenchido por plausibilidade depois.

**Definições de marcos**

1. **Nenhuma definição normativa de First Playable, Vertical Slice, Alpha, Beta,
   Content Lock, Feature Freeze, Code Freeze, Gold Master ou Release Candidate**
   publicada por corpo de padronização, associação da indústria ou publisher em
   documento público. Não é lacuna de busca; é a natureza do assunto. Todo material é
   livro, blog, wiki ou contrato privado.
2. **Nenhuma definição pública de milestone emitida por publisher.** Publishers
   definem milestones em contratos, que não são públicos. O modelo em §1.2 é de um
   escritório de advocacia, não de um publisher.
3. **Nenhuma fonte primária para "Content Lock"** como termo de engenharia de
   software. Existe em contratos de jogos, com significados conflitantes.
4. **Não verifiquei no livro** as definições de Chandler (§1.2). Li via página de
   citações do Goodreads. Confirmar antes de tratar como âncora.
5. **Nenhum dado sobre com que frequência estúdios cumprem as próprias definições.**
   A afirmação plausível de que "estúdios enviam features depois do feature complete"
   não tem, que eu tenha achado, medição — só relato anedótico e o achado de
   Politowski et al. de que milestones "are usually underestimated".

**Stage-Gate**

6. **Nenhum estudo empírico revisado por pares avaliando Stage-Gate aplicado a
   desenvolvimento de jogos.** Existe Cooper & Sommer sobre produtos físicos, um
   survey de processos em jogos que não trata de gates, e uma monografia de graduação.
   A transferência para jogos não está validada na literatura.
7. **Não li as fontes primárias das críticas** ao Stage-Gate (Becker 2006; Lenfle &
   Loch 2010). Só a paráfrase de Cooper, que discorda delas em parte.

**Certificação**

8. **Nenhum texto público e atual da TRC da PlayStation.** Só um PDF vazado da era PS1,
   marcado confidencial, que não uso e recomendo não usar.
9. **Nenhum checklist público do Lotcheck da Nintendo.** O processo é público; os
   critérios são NDA.
10. **Nenhum prazo de certificação publicado por Microsoft, Sony ou Nintendo.** Os
    números que circulam ("2–6 semanas", "Lotcheck 30 dias") não têm primária. Só a
    Valve publica prazo (3–5 dias úteis).
11. **Nenhuma taxa de reprovação em primeira submissão** para qualquer plataforma. O
    "38%" da Microsoft é distribuição *entre* falhas, não taxa de falha; e não vem com
    amostra, período nem metodologia. O "over 40%" da Apple também não.
12. **Os requisitos "TCR-ACC001/ACC002" de acessibilidade do Xbox não existem.**
    Verifiquei: zero ocorrências de "TCR" nas páginas de XR da Microsoft, e nenhum XR
    de acessibilidade entre os 40. Fabricação de terceiro (§3.6).

**Acessibilidade**

13. **Nenhum crosswalk oficial** entre Game Accessibility Guidelines e WCAG, nem entre
    XAGs e WCAG. Nenhuma das duas reivindica mapeamento. Qualquer correspondência seria
    trabalho editorial deste repositório.
14. **Nenhum limiar numérico** para a maioria dos 123 critérios das Game Accessibility
    Guidelines. "High contrast" não tem razão definida. Verificação é julgamento humano.
15. **Nenhum mecanismo de conformidade, selo, nível declarável ou auditoria** para as
    Game Accessibility Guidelines. Não é certificável, por desenho.
16. **Não sei a data real de lançamento dos XAGs.** As duas páginas da Microsoft dão
    datas diferentes (out 2019 na version history; jan 2020 na narrativa MGATS). Minha
    hipótese de "interno vs. público" é conjectura minha, não algo que as páginas digam.
17. **Não pesquisei** como o teste de "not achievable" do CVAA é aplicado na prática,
    nem houve caso de enforcement contra jogo que eu tenha verificado. Não sou advogado.

**Quality gates**

18. **Nenhuma justificativa empírica publicada** para os padrões 80.0% de cobertura e
    3.0% de duplicação do SonarQube. São padrões de fornecedor.
19. **Nenhum critério de conteúdo no Scrum Guide** para a Definition of Done — ausência
    deliberada. Qualquer "DoD padrão" atribuída a Scrum é invenção de terceiros.
20. **A relação entre cobertura de teste e redução de defeitos permanece questão
    aberta** — não pela minha falha em achar o estudo, mas porque o Google diz
    textualmente que é "an open research question".
21. **Nenhuma medição** sustentando a afirmação, comum em blogs, de que metas de
    cobertura fazem desenvolvedores escreverem "testes lixo". O mecanismo é plausível e
    o Google alerta contra ele ("treating your target like a checkbox"), mas não achei
    quantificação.

**Sobre gates em geral**

22. **Nenhuma avaliação empírica de que gates de produção melhorem a qualidade do jogo
    entregue.** Este é o vazio mais relevante para o desenho: a prática é difundida,
    contratualmente obrigatória e intuitivamente sensata, e eu não encontrei estudo que
    a valide para jogos. O framework pode adotar gates como disciplina explícita; não
    pode alegar que a evidência mostra que funcionam.

**Fontes que descartei ativamente**

- [zebonastic.substack.com](https://zebonastic.substack.com/p/every-stage-of-game-development-explained) —
  provavelmente gerado por IA; números grandes sem citação; atribuições em bloco.
- [code-note-vr.vercel.app](https://code-note-vr.vercel.app/console-development---certification) —
  IDs de requisito fabricados, verificados contra a documentação da Microsoft.
- [psx.arthus.net](https://psx.arthus.net/sdk/Psy-Q/DOCS/TECHNOTE/mtrc13.pdf) — TRC de
  PS1 vazada e marcada confidencial; obsoleta e de uso indevido.
- Post de LinkedIn sobre "6 major milestones" — opinião de praticante, sem fonte.

---

## 7. Achados diretamente aproveitáveis no desenho

Resumo do que a pesquisa sustenta, com a fonte de cada item, para não perder o
rastro quando isto virar código.

| Achado | Fonte | Força |
|---|---|---|
| Separar **readiness check** (falta trabalho → recycle) de **must-meet** (não vale mais → kill) de **should-meet** (pontuação, ordena, não bloqueia) | Cooper, primária | Forte |
| Deliverables do gate são fixados **na saída do gate anterior**, não negociados na avaliação | Cooper, primária | Forte |
| Um único "No" em must-meet decide; sem média, sem compensação | Cooper, primária | Forte |
| "Burocracia é trabalho que não agrega valor" — teste para cada critério novo | Cooper, primária | Forte |
| Falha em DoD tem **destino declarado**: sai do incremento e volta ao backlog | Scrum Guide 2020, primária | Forte |
| Padrão da organização é **piso**; o time adiciona, não remove | Scrum Guide 2020, primária | Forte |
| Marcar quais requisitos são **efetivamente testados** (o asterisco dos XRs), separando requisito de requisito verificado | Microsoft, primária | Forte |
| Exigir o **artefato de verificação** junto da entrega (logs do Submission Validator), não a alegação de que passou | Microsoft XR-003, primária | Forte |
| **Testabilidade antes de qualidade**: recusar o que impede a própria avaliação | Microsoft XR-003 + BVTs, primária | Forte |
| Critério como **coerência entre o prometido e o existente**, com a promessa ajustável | Valve, primária | Forte |
| **Escopo antes de critério** (scoping questions / seções "Applicable") | Microsoft XAGs, primária | Forte |
| Cada critério carrega **quem é excluído se falhar** (gaming personas) | Microsoft XAGs, primária | Média |
| Medir **delta, não acervo**, para que o gate seja sempre alcançável e não precise ser desligado | SonarQube, primária de fornecedor | Média |
| **O que falta é mais informativo que o agregado** — apontar a lacuna nomeada, não emitir razão | Google, primária | Forte |
| Gate numérico **apodrece em checkbox**; declarar isso ao lado do gate | Google, primária | Forte |
| Onde há gate legal, ele pode exigir **procedência da decisão documentada**, não estado do produto | FCC/CVAA, primária | Forte |
| Falhas reais concentram-se em **estabilidade e completude**, não em requisitos exóticos | Microsoft top-failing, primária com limite | Média |
| Nível/severidade pode ser propriedade do par **(categoria, critério)**, não do critério | Game Accessibility Guidelines, primária | Média |
| Vertical slice prova **capacidade de produção**, não qualidade de design | Ismail, primária de praticante | Fraca |
| Nomes de marcos **não têm definição canônica** — declarar convenção local | ausência verificada | Forte |

---

## 8. Confronto com os gates já implementados

Esta pesquisa foi feita depois que [gates.md](gates.md) já existia. Os dez gates de
lá derivam de procedência interna (as linhas `**Pronto para…**` de
[preproduction.md](preproduction.md)), e a estrutura de três saídas veio de uma
única fonte fraca, declarada como tal em [sources.md](sources.md): um vídeo de
praticante. Vale registrar o que a literatura externa faz com aquelas escolhas,
porque o resultado não é uniforme.

### 8.1 Convergência independente — a literatura sustenta o que já estava lá

Estes pontos foram decididos no repositório sem conhecer as fontes abaixo, e as
fontes os apoiam. Convergência independente é evidência melhor que citação
posterior, e é honesto dizer que a ordem foi essa.

- **Três saídas em vez de duas.** `passar` / `cortar escopo` / `abandonar` mapeia
  quase diretamente em Go / Recycle / Kill de Cooper (§2.2), que é literatura de
  gestão de produto com décadas de uso, não conselho de YouTube. A crítica de
  `gates.md` a processos que "só admitem 'passou' e 'ainda não'" tem apoio formal:
  em Cooper, *Kill* é uma das quatro saídas canônicas de todo gate. **A fonte fraca
  pode ser substituída pela forte.**
- **`waived` com motivo escrito, e quatro critérios sem terceira opção.** É a
  distinção must-meet / should-meet (§2.2). Os quatro não dispensáveis são
  knockouts: um "No" e não passa, sem compensação. O resto é negociável com
  assinatura. Cooper insiste na mesma assimetria.
- **`held_by_declaration` em vez de `passed`.** Corresponde ao asterisco dos XRs da
  Microsoft (§3.1), que separa *requisito* de *requisito efetivamente testado* em
  documento público. A escolha de nome do campo tem precedente numa plataforma real.
- **Coluna de evidência, e `met` sem lastro recusado.** É XR-003 (§3.1), que exige o
  log do Submission Validator **junto** com a entrega em vez da alegação de que
  passou. O padrão "o gate quer o artefato, não a afirmação" é prática de detentor
  de plataforma.
- **"Silêncio não é aprovação" / critério sem linha conta como pendente.** É o
  readiness check de Cooper: a ausência do deliverable é um "No", não um vazio.
- **Reprovar em `scale` devolve para `build`, e isso é uso normal.** É exatamente
  *recycle* ("A 'No' signals a recycle to the previous stage"), e Cooper também o
  trata como funcionamento, não como fracasso.
- **Retorno ao backlog com destino declarado.** O Scrum Guide (§5.1) faz o mesmo
  movimento: o item que não cumpre a DoD "returns to the Product Backlog", não fica
  num limbo.

### 8.2 O que a literatura oferece e os gates ainda não têm

Lacunas concretas, cada uma com a fonte que a sugere. São observações de pesquisa,
não recomendações que eu tenha implementado.

- **Escopo antes de critério.** Os XAGs resolvem aplicabilidade com *scoping
  questions* antes de cobrar qualquer coisa, e a TRC histórica marcava seções como
  "Applicable" (§3.4, §4.2). Hoje, em `gates.md`, um critério inaplicável só tem a
  saída de virar `waived` com motivo — o que registra como dispensa algo que nunca
  incidia. Um estado de "fora de escopo" é categoria diferente de dispensa, e
  confundir os dois infla a contagem de dispensas.
- **Deliverables fixados na saída do gate anterior.** Em Cooper isso é explícito e
  serve para que a expectativa não seja renegociada na hora da avaliação. Os gates
  atuais têm critérios fixos por etapa, o que é mais rígido num sentido e mais
  frouxo noutro: não há momento em que se combine o que este projeto específico vai
  precisar trazer.
- **Readiness e must-meet estão fundidos.** Cooper separa "o trabalho está feito?"
  (recycle) de "isto ainda vale a pena?" (kill). Os dez gates atuais são quase todos
  readiness; a pergunta de valor aparece só como a saída `abandonar`, que depende de
  alguém levantá-la. Nenhum critério a **faz**.
- **Distinguir o que é verificável do que é julgamento.** A pesquisa mostra que os
  dois convivem em qualquer checklist real: dos 123 critérios de acessibilidade,
  quase nenhum tem limiar numérico (§4.1), e a Microsoft marca com asterisco só o
  subconjunto testado. `gates.md` já recusa `met` sem lastro, mas não distingue
  "lastro é log de comando" de "lastro é alguém que olhou".
- **Medir delta, não acervo.** O motivo pelo qual o SonarQube incide sobre código
  novo (§5.2) é impedir que o gate se torne inalcançável e seja desligado. Vale
  perguntar se algum critério dos dez é retroativo o bastante para criar esse efeito.
- **O critério carrega quem é prejudicado se falhar.** As *gaming personas* dos XAGs
  atam cada guideline a quem é excluído. Critério com motivo embutido resiste melhor
  a virar checkbox.

### 8.3 O que a pesquisa recomenda **não** fazer

- **Não citar "a definição da indústria" de marco nenhum.** Não existe (§1.1, §6.1).
  Se um gate se chamar `scale` e for descrito como "vertical slice", a definição é
  deste repositório. A escolha de `gates.md` de nomear gates pela **permissão pedida**
  (`design`, `build`, `scale`) em vez de pelo nome do marco da indústria evita
  exatamente essa armadilha, e agora há razão documentada para isso.
- **Não adotar limiar numérico sem origem.** O 80% do SonarQube não tem justificativa
  publicada (§5.2, §6.18); o "80% pronto" do vídeo já foi recusado em `sources.md`
  pelo mesmo motivo. A recusa estava certa.
- **Não alegar que gates melhoram a qualidade do jogo.** Não encontrei evidência para
  jogos (§6.22). E o Google diz textualmente que mesmo o elo entre cobertura e
  defeitos é "an open research question" (§5.3). Disciplina explícita é a alegação
  defensável; eficácia comprovada não é.
- **Não deixar um gate numérico sem o aviso ao lado.** Quem mais mede no mundo avisa
  que a meta "apodrece em checkbox" no mesmo parágrafo em que defende usá-la (§5.3).
