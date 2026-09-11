# Produção e acabamento

Entrada: um recorte que já demonstrou a experiência (PoC ou vertical slice) e precisa
virar um jogo completo no acabamento pretendido; ou um jogo em produção que precisa
saber em que marco está e o que falta. `context --focus production` seleciona esta
receita; `--stage production-plan` e `--stage milestone` também a incluem.

Saída: plano de produção com marcos, orçamentos, pipeline de conteúdo e riscos no
documento canônico do jogo, e revisões de marco com evidência ligada. O harness
localiza o plano como fonte de continuidade; não mede orçamentos, não promove marcos
nem certifica acabamento.

“AAA” aqui não é orçamento nem tamanho de equipe. É um **padrão de acabamento
observável**: cada disciplina atinge o piso definido no plano, medido na plataforma
alvo, em movimento, e o jogo permanece estável sob uso prolongado. Um jogo pequeno
pode alcançá-lo num recorte pequeno; um jogo grande falha nele com muito conteúdo
desigual. A pré-produção prova que a experiência vale; a produção prova que ela
sobrevive à escala, ao tempo e à plataforma.

No starter, com tela, a primeira superfície do recorte é a porta.
Convite, last-run e recibo no disco não fecham marco nem certificam
acabamento.

## 0. Três instrumentos, três perguntas

Este framework usa três vocabulários que não se substituem, e esta receita liga os três:

- **Marcos** (esta receita) respondem *em que ponto da produção estamos* — first
  playable → vertical slice → alpha → beta → gold → live. São o calendário do
  projeto, com critérios de evidência definidos antes.
- **A [barra de acabamento](../references/production-bar.md)** responde *quão longe
  cada dimensão de ofício foi levada* — dez dimensões, cinco degraus, e o degrau
  percebido é o mínimo entre elas. `bar <projeto>` lê a declaração; `next` propõe subir
  a dimensão mais baixa. Se a prosa declara o mínimo, o `bar` nomeia o mínimo que a barra já declara. Degrau no disco não é acabamento observado. Sem chave `mínimo`.
- **Os [gates](../references/gates.md)** respondem *o que ainda não pode passar* — dez
  recusas por etapa do ciclo, com critérios `met`/`unmet`/`waived`. `gate <projeto>` lê.

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
  reagindo ao estado; piso de gravação licenciada, não 8-bit por padrão.
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
projeto: `verify` para comandos técnicos; `record --kind observation` para o que uma
pessoa (ou o agente, com `role=agent`) viu em movimento; `record --kind budget` para
cada medição de orçamento com plataforma e ferramenta; `record --kind milestone` para
a decisão de passagem, com quem declarou. O recibo guarda o fato declarado; não o
valida. Exemplo completo: [da trilha ao capítulo acabado](../examples/era-uma-vez-production.md).

## Limites

O harness localiza o plano de produção e o inclui em `continuity.sources`; a leitura
dos marcos, a medição dos orçamentos e a declaração de passagem são do agente e da
pessoa. `record` escreve o que lhe foi declarado e recusa sobrescrita; nenhum comando
mede desempenho, executa soak ou certifica requisitos de plataforma. Os termos first playable, alpha, beta e gold seguem o uso corrente da
indústria; cada estúdio e plataforma define detalhes próprios, e o plano do jogo
registra a definição adotada. Ver [fontes](../references/sources.md#produção-09).
