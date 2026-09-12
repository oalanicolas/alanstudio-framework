# Produção e acabamento

Entrada: um recorte que já demonstrou a experiência (PoC ou vertical slice) e precisa
virar um jogo completo no acabamento pretendido; ou um jogo em produção que precisa
saber em que marco está e o que falta. `context --focus production` seleciona esta
receita; `--stage production-plan` e `--stage milestone` também a incluem.

Saída: plano de produção com marcos, orçamentos, pipeline de conteúdo e riscos no
documento canônico do jogo, e revisões de marco com evidência ligada. O harness
localiza o plano como fonte de continuidade; não mede orçamentos, não promove marcos
nem certifica acabamento. Se a barra recusa promover o degrau, o `context` nomeia a promoção que a barra já recusa. Guia no disco não é acabamento. Sem chave `promove`. Se a barra recusa que o degrau sem condição seja observação, o `dimensions[n]` do `production_bar` nomeia a opinião que a barra já recusa. Linha no disco não é acabamento. Sem chave `opinião`. Se o onboard recusa que tempo de sessão seja interesse, o `dimensions[pacing]` do `production_bar` nomeia o interesse que o onboard já recusa. Relógio no disco não é o interesse. Sem chave `interesse`.

“AAA” aqui não é orçamento nem tamanho de equipe. Se a receita recusa que AAA seja orçamento ou tamanho de equipe, o `production_bar` nomeia a equipe que a receita já recusa. Receita no disco não é acabamento. Sem chave `equipe`. É um **padrão de acabamento
observável**: cada disciplina atinge o piso definido no plano, medido na plataforma
alvo, em movimento, e o jogo permanece estável sob uso prolongado. Um jogo pequeno
pode alcançá-lo num recorte pequeno; um jogo grande falha nele com muito conteúdo
desigual. A pré-produção prova que a experiência vale; a produção prova que ela
sobrevive à escala, ao tempo e à plataforma.

No starter, com tela, a primeira superfície do recorte é a porta.
Convite, last-run e recibo no disco não fecham marco nem certificam
acabamento. Se a receita recusa que o recibo feche o marco, o `fields` do `record --kind milestone` nomeia o marco que a receita já recusa. Recibo no disco não é a passagem. Sem chave `marco`.

## 0. Três instrumentos, três perguntas

Este framework usa três vocabulários que não se substituem, e esta receita liga os três:

- **Marcos** (esta receita) respondem *em que ponto da produção estamos* — first
  playable → vertical slice → alpha → beta → gold → live. São o calendário do
  projeto, com critérios de evidência definidos antes.
- **A [barra de acabamento](../references/production-bar.md)** responde *quão longe
  cada dimensão de ofício foi levada* — dez dimensões, cinco degraus, e o degrau
  percebido é o mínimo entre elas. `bar <projeto>` lê a declaração; `next` propõe subir
  a dimensão mais baixa. Se a prosa declara o mínimo, o `bar` nomeia o mínimo que a barra já declara. Degrau no disco não é acabamento observado. Sem chave `mínimo`. Se a barra recusa que o degrau seja prazo, o `bar` nomeia os prazos que a barra já recusa. Linha no disco não é calendário. Sem chave `prazos`. Se a barra recusa que o nome seja uma das dez, o `bar` nomeia a dimensão que a barra já recusa. Linha no disco não é acabamento. Sem chave `dimensão`. Se a barra recusa que dimensão não declarada seja dimensão alta, o `undeclared` do `bar` nomeia a alta que a barra já recusa. Linha no disco não é acabamento. Sem chave `alta`. Se a barra recusa que a declaração seja um selo, o `sources` do `bar` nomeia o selo que a barra já recusa. Linha no disco não é acabamento. Sem chave `selo`. Se a barra recusa que o piso seja uma nota, o `floor` do `bar` nomeia a nota que a barra já recusa. Linha no disco não é acabamento. Sem chave `nota`. Se a barra recusa que a tabela otimista seja observação, o `at_floor` do `bar` nomeia a otimista que a barra já recusa. Linha no disco não é acabamento. Sem chave `otimista`. Se o mapa recusa que o checklist seja um score, o `bar` nomeia o score que o mapa já recusa. Mapa no disco não é acabamento. Sem chave `score`. Se a barra recusa que duas linhas discordantes se resolvam por precedência, o `conflicts[n]` do `bar` nomeia a precedência que a barra já recusa. Linha no disco não é acabamento. Sem chave `precedência`.
- **Os [gates](../references/gates.md)** respondem *o que ainda não pode passar* — dez
  recusas por etapa do ciclo, com critérios `met`/`unmet`/`waived`. `gate <projeto>` lê.
  Se a tabela declara o gate, o `gate` nomeia o gate que a tabela já declara. Linha no disco não é passagem concedida. Sem chave `gate`. Se o roteiro recusa que o silêncio seja aprovação, o `gate` nomeia o silêncio que o roteiro já recusa. Linha vazia no disco não é passagem. Sem chave `silêncio`. Se o roteiro recusa que a lista de entrega seja um gate, o `sources` do `gate` nomeia a lista que o roteiro já recusa. Linha no disco não é passagem. Sem chave `lista`. Se o roteiro recusa que a declaração seja passed, o `held_by_declaration` do `gate` nomeia o passou que o roteiro já recusa. Tabela no disco não é passagem. Sem chave `passou`. Se o roteiro recusa que must_meet seja dispensável, o `gate` nomeia a dispensa que o roteiro já recusa. Linha no disco não é passagem. Sem chave `dispensa`. Se o roteiro recusa que fora de escopo seja dispensa, o `gate` nomeia o escopo que o roteiro já recusa. Linha no disco não é passagem. Sem chave `escopo`. Se a guia recusa que código que compila prove a hipótese, o `gate` nomeia a hipótese que a guia já recusa. Linha no disco não é o experimento. Sem chave `hipótese`. Se o fluxo recusa que um teste local concluído seja lançamento, o `gate` nomeia o lançamento que o fluxo já recusa. Linha no disco não é outra máquina. Sem chave `lançamento`. Se a receita recusa que a slice sem repeatability esteja pronta para ampliar, o `gate` scale nomeia a repeatability que a receita já recusa. Linha no disco não é o próximo trecho. Sem chave `repeatability`. Se o roteiro recusa que abandonar seja falha do gate, o `gate` nomeia o abandono que o roteiro já recusa. Roteiro no disco não é passagem. Sem chave `abandono`.
  Se a tabela declara saída de escopo, o `craft` nomeia a saída de escopo que a tabela já declara. Linha no disco não é ofício observado. Sem chave `out_of_scope`. Se a pesquisa recusa ser escada de acabamento, o `craft` nomeia a escada que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `escada`. Se a pesquisa recusa que o número folclórico seja critério observável, o item do craft nomeia o folclore que a pesquisa já recusa. Folclore no disco não é o critério. Sem chave `folclore`. Se a pesquisa recusa que três métricas com o mesmo nome sejam um critério, o item do craft nomeia as métricas que a pesquisa já recusa. Nome no disco não é a métrica. Sem chave `métricas`. Se a pesquisa recusa que as palestras dêem limiar, o item do craft nomeia o limiar que a pesquisa já recusa. Palestra no disco não é o critério. Sem chave `limiar`. Se a pesquisa recusa que esses valores sejam um padrão, o item do craft nomeia o padrão que a pesquisa já recusa. Valor no disco não é o padrão. Sem chave `padrão`. Se a pesquisa recusa que o pulo bom seja critério, o item do craft nomeia o pulo que a pesquisa já recusa. Frase no disco não é o critério. Sem chave `pulo`. Se a pesquisa recusa ser um conjunto de gates, o `sources` do `craft` nomeia o conjunto que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `conjunto`. Se a pesquisa recusa que a pendência seja medição em jogo, o `pending` do `craft` nomeia a medição que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `medição`. Se a pesquisa recusa que o número sem definição seja critério, o `craft` nomeia a definição que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `definição`. Se o mapa recusa que o número com casa decimal e sem origem seja mais preciso, o `craft` nomeia o preciso que o mapa já recusa. Mapa no disco não é ofício observado. Sem chave `preciso`. Se o craft recusa que shape confirmado seja licença para pular feel e áudio, o `craft` nomeia o pular que o craft já recusa. Confirmação no disco não é o ofício. Sem chave `pular`. Se o craft recusa que uma confirmação autorize delegar, o `craft` nomeia o delegar que o craft já recusa. Confirmação no disco não é delegar. Sem chave `delegar`.

Correspondência usual, a confirmar em cada jogo: first playable fecha o gate `prototype`
e pede a barra em `playable`; vertical slice fecha `scale` e pede `slice` em todas as
dimensões do recorte; alpha e beta atravessam `evaluate` e `conclude`; gold fecha
`deliver` e pede `shippable`. Um marco declarado com uma dimensão ainda em `prototype`
é a contradição que a barra existe para expor.

## 1. Marcos com critérios de evidência

Cada marco tem critérios observáveis definidos **antes** e é declarado por pessoa com
a prova ligada. Datas organizam trabalho; não substituem critérios.

| Marco | O que precisa ser verdade | O que ainda não prova |
| --- | --- | --- |
| First playable | ciclo central de ponta a ponta, com placeholders; verbo, decisão, consequência e reinício funcionam | diversão, arte, escala |
| Vertical slice | trecho representativo no acabamento pretendido; receita para produzir o próximo trecho compreendida e custeada | que o restante do conteúdo terá a mesma qualidade |
| Alpha | todos os sistemas do recorte presentes (feature complete); conteúdo pode ser parcial; nenhum bloqueador sem plano | orçamentos estáveis, localização |
| Beta | todo o conteúdo do recorte (content complete); orçamentos dentro da meta ou desvio aprovado; localização e acesso implementados; playtest externo observado | zero defeitos |
| Gold / RC | zero bloqueadores; soak, reinstalação, atualização e save verificados; checklist da plataforma revisado na fonte oficial; créditos e licenças completos | sucesso comercial, recepção |
| Live | telemetria mínima, canal de relato, plano de hotfix e de conteúdo, quando houver operação | nada além do que for medido |

Um marco só regride por decisão registrada. “Quase alpha” não existe: ou os critérios
têm prova, ou o marco continua pendente com a lista do que falta. Use o
[template de marco](../assets/templates/milestone.md) para a revisão e o
[plano de produção](../assets/templates/production-plan.md) para manter o estado.

## 2. Lentes de disciplina

O agente é um só; as disciplinas continuam existindo. Aplique cada lente como uma
pergunta sobre o recorte, sem criar hierarquia de agentes nem cerimônia. Uma lente
não aplicável ao jogo registra o motivo.

- **Design:** verbo, decisão, consequência e ritmo se sustentam em toda a extensão do
  conteúdo? Onde a curva de aprendizado quebra? Há opção dominante?
- **Arte e animação:** silhueta, materiais, luz e leitura em movimento seguem o design
  system do jogo? Animação sustenta o verbo (antecipação, impacto, recuperação)?
- **Áudio:** mixagem por camadas, prioridade de sons, silêncio intencional, música
  reagindo ao estado; direção sonora do projeto e proveniência respeitadas.
- **Feel:** latência entrada → resposta, hitstop, câmera, partículas, haptics; ver a
  [receita de feel](feel.md).
- **UX/UI e acesso:** contraste, forma além da cor, foco e navegação por controle,
  alvos de toque, movimento reduzido, remapeamento, legendas, tamanho de texto.
  Consulte diretrizes de acessibilidade da plataforma na fonte oficial.
- **Técnica:** orçamentos medidos, estabilidade, saves, reinício, descarte, tempo
  determinístico onde exigido, build reproduzível.
- **Conteúdo e pipeline:** o próximo asset nasce pela receita, passa por validação
  automática e chega ao runtime sem ajuste manual não documentado.
- **Localização:** textos fora do código, fontes com cobertura, pseudo-localização,
  layout elástico; ou a decisão explícita de um idioma.
- **QA:** matriz plataforma × entrada × cenário; regressão automatizada onde couber;
  soak; observação humana separada de execução técnica.
- **Plataforma e legal:** requisitos de loja/console, classificação etária, privacidade,
  créditos e licenças. Consulte a fonte oficial; não invente requisito nem certifique.

## 3. Orçamentos medidos

Orçamento é um contrato entre disciplinas: tempo de quadro (p50 e p99), memória de
pico, carregamento, tamanho do build, latência de entrada, tráfego de rede quando
houver. Cada valor tem plataforma, cena, ferramenta e data. Número sem medição é
hipótese; a meta é definida pelo alvo do jogo, não por convenção universal.

A qualidade visual aprovada é o piso. Quando um orçamento estoura, primeiro localize o
gargalo no caminho real (profiler, captura de quadro, contagem de draw calls, alocação
por quadro) e busque a implementação mais eficiente: LOD, culling correto, batching,
streaming, atlas, pooling, cache de shaders, redução de alocação. Cortar sombras,
efeitos ou animação é decisão de direção, registrada como desvio aprovado, nunca
solução automática. Compare antes/depois em condições equivalentes e em movimento.

## 4. Pipeline de conteúdo

Produzir muito conteúdo com qualidade constante exige um caminho repetível:
**fonte → importação → validação → runtime.** Registre ferramentas, formatos,
convenções de nome, escala/pivot, LODs, compressão e onde cada validação roda.
Uma receita por família (personagem, nível, efeito, tela, som) diz como o próximo item
nasce dentro do piso. Validação automática pega nome, tamanho, referência quebrada e
orçamento por asset; pessoa e IA julgam se pertence ao jogo. Adapte as ferramentas da
engine antes de criar pipeline próprio.

## 5. Estabilidade

Soak (horas de jogo, memória ao longo do tempo), reinício repetido (montar → desmontar
→ montar), saves com dados inválidos e versões antigas, perda de foco, desconexão,
atualização sobre instalação existente. Capture crash e logs com reprodução mínima.
Teste no build exportado da plataforma alvo, não só no editor. Cada falha entra na
triagem com impacto no jogador e dono; “zero bloqueadores” só após triagem registrada.

## 6. Ritmo de produção

Trabalhe em fatias jogáveis que atravessam regra, apresentação e conteúdo, ordenadas
por dependência e pelo risco que pode invalidar o recorte. Mantenha o plano de
produção como fonte única de estado: marco atual, orçamentos, riscos e continuidade.
Atualize-o a cada entrega; não crie planos paralelos. Ao fechar uma fatia, siga
[continuidade e retomada](../references/process.md#continuidade-e-retomada).

## 7. Evidência ligada

Cada critério de marco aponta para um recibo em pasta inédita, ligado ao HEAD do
projeto: `verify` para comandos técnicos; se o roteiro recusa aprovar a criatividade, o `verify` nomeia a criatividade que o roteiro já recusa. Recibo verde não é aprovação. Sem chave `criatividade`. Se a ambição recusa que o recibo comprove diversão, o `verify` nomeia a diversão que a ambição já recusa. Log no disco não é experiência. Sem chave `diversão`. Se a entrega recusa que o hash comprove o significado, o comando do verify nomeia o significado que a entrega já recusa. Hash no disco não é o critério. Sem chave `significado`. Se a receita recusa que teste unitário de serialização prove conectividade real, o `verify` nomeia a conectividade que a receita já recusa. Recibo verde não é sessão real. Sem chave `conectividade`. Se a receita recusa que o registro declarado prove suporte real, o `capabilities[n]` do `verify` nomeia o suporte que a receita já recusa. Registro no disco não é o consumidor. Sem chave `suporte`. `record --kind observation` para o que uma
pessoa (ou o agente, com `role=agent`) viu em movimento; `record --kind budget` para
cada medição de orçamento com plataforma e ferramenta; `record --kind milestone` para
a decisão de passagem, com quem declarou. O recibo guarda o fato declarado; não o
valida. Se a receita recusa que o recibo feche o marco, o `fields` do `record --kind milestone` nomeia o marco que a receita já recusa. Recibo no disco não é a passagem. Sem chave `marco`. Exemplo completo: [da trilha ao capítulo acabado](../examples/era-uma-vez-production.md).

## Limites

O harness localiza o plano de produção e o inclui em `continuity.sources`; a leitura
dos marcos, a medição dos orçamentos e a declaração de passagem são do agente e da
pessoa. `record` escreve o que lhe foi declarado e recusa sobrescrita; nenhum comando
mede desempenho, executa soak ou certifica requisitos de plataforma. Se o roteiro recusa medir os critérios, o `record` nomeia a medição que o roteiro já recusa. Recibo no disco não é observação. Sem chave `mede`. Se a receita recusa que o ganho no caso rejeitado seja ganho equivalente no solver ativo, o `record` nomeia o solver que a receita já recusa. Ganho rejeitado no disco não é o solver. Sem chave `solver`. Se a receita recusa que cenas dinâmicas virem estáticas porque a matriz local ficou igual, o `record` nomeia a matriz que a receita já recusa. Matriz no disco não é a cena. Sem chave `matriz`. Se a receita recusa que o editor seja build exportado, o `record` nomeia o alvo que a receita já recusa. Editor no disco não é o build. Sem chave `alvo`. Se a receita recusa que várias variáveis atribuam a causa, o `record` nomeia a variável que a receita já recusa. Variável no disco não é a causa. Sem chave `variável`. Se a receita recusa que reduzir acabamento para um número seja otimizar, o `record` nomeia o rebaixar que a receita já recusa. Corte no disco não é o mesmo resultado. Sem chave `rebaixar`. Se a receita recusa que a adaptação herde o resultado, o `record` nomeia a contraprova que a receita já recusa. Adaptação no disco não é a contraprova. Sem chave `contraprova`. Se a receita recusa que o subpasso repita eventos de borda, o `record` nomeia o subpasso que a receita já recusa. Subpasso no disco não é o quadro. Sem chave `subpasso`. Se a receita recusa que ganho na média demonstre redução de engasgos, o `fields` do `record --kind budget` nomeia os engasgos que a receita já recusa. Número no disco não é o quadro estável. Sem chave `engasgos`. Se a receita recusa que a máquina de desenvolvimento quente seja a máquina do jogador fria, o `fields` do `record --kind budget` nomeia a quente que a receita já recusa. Plataforma no disco não é a máquina fria. Sem chave `quente`. Se o roteiro recusa que o screenshot isolado comprove animação, o `record` nomeia a animação que o roteiro já recusa. Anexo no disco não é controle. Sem chave `animação`. Se a receita recusa que bytes menores provem fidelidade, o `record` nomeia a fidelidade que a receita já recusa. Anexo no disco não é a trajetória. Sem chave `fidelidade`. Se o roteiro recusa que o HEAD substitua o julgamento, o `version` nomeia o julgamento que o roteiro já recusa. Identidade no disco não é avaliação. Sem chave `julgamento`. Os termos first playable, alpha, beta e gold seguem o uso corrente da
indústria; cada estúdio e plataforma define detalhes próprios, e o plano do jogo
registra a definição adotada. Ver [fontes](../references/sources.md#produção-09).
