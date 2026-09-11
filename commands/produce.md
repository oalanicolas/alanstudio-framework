# Produce

Da fatia ao acabamento: plano de produção com marcos por evidência (first playable
→ vertical slice → alpha → beta → gold → live), lentes de disciplina, orçamentos
medidos na plataforma alvo, pipeline de conteúdo e estabilidade; barra e gates
lidos antes de ampliar. Use quando a slice já demonstrou a experiência e o
trabalho vira escala, acabamento e estabilidade. Receita: [produção](../recipes/production.md).

Três instrumentos, três perguntas: **marcos** (calendário), **barra** (onde está cada
dimensão), **gates** (o que ainda não pode passar).

## Escala

`jam`: não há plano de produção; a "produção" é fechar o ciclo e parar. `product`:
plano como fonte única de marco, orçamentos e riscos; MVP delimita a entrega.
`aa`: a slice trava o piso → tempo por asset → esforço → o que é possível ampliar;
sem essa trava o plano é chute. Promessas do brief entram como lentes obrigatórias.

## Avaliar

1. `context <projeto> --focus production --stage production-plan` (ou `--stage
   milestone` para revisar um marco). `bar <projeto>`: piso e dimensões nele.
   `gate <projeto> --gate scale`: `worth_scaling` é `must_meet` — pergunta se ampliar
   ainda vale o que custa antes de qualquer tarefa.
2. A slice demonstrou **repeatability**? Outro trecho nasceu pela receita com custo
   observado? Se não, [`content`](content.md) antes de produzir.
3. Orçamentos: tempo de quadro p50/p99, memória de pico, carregamento, tamanho,
   latência de entrada, rede — cada um com plataforma, cena, ferramenta e data.
   Número sem medição é hipótese.
4. Lentes: design, arte/animação, áudio, feel, UX/acesso, técnica, conteúdo,
   localização, QA, plataforma/legal. Uma lente não aplicável registra o motivo.
   Sem hierarquia de agentes: é o mesmo agente perguntando por lente.
5. Pergunte só a decisão indispensável: a fronteira do MVP e os marcos que o usuário
   quer declarar.

## Executar

Mantenha o [plano de produção](../assets/templates/production-plan.md) como fonte
única: marco atual, critérios de evidência por marco, orçamentos, riscos,
continuidade. Trabalhe em fatias jogáveis que atravessam regra, apresentação e
conteúdo, ordenadas por dependência e risco. A cada marco, a
[revisão](../assets/templates/milestone.md) lê a evidência por lente e registra
quem declarou a passagem. Estabilidade: soak, reinício repetido, saves antigos,
perda de foco, atualização sobre instalação, no build exportado.

## Verificar

Cada critério de marco aponta para um recibo em pasta inédita ligado ao HEAD:
`verify` para comandos, `record --kind observation` para o que alguém viu,
`record --kind budget` para medição, `record --kind milestone` para a decisão
(`declared`/`denied`/`deferred`, com `declared_by` e `role`). Nenhum comando mede
orçamento, executa soak, promove marco ou certifica plataforma
([gates](../references/gates.md), [barra](../references/production-bar.md)).

## Nunca

- Ampliar antes de a slice provar repeatability ou de responder `worth_scaling`.
- Criar plano paralelo ou regenerar toda a documentação a cada rodada.
- Tratar marco como número de tarefas fechadas em vez de evidência ligada.
- Compensar perda de acabamento com quantidade de conteúdo: qualquer atalho que
  quebre o piso é regressão, não velocidade.
- Chamar o build de AAA por orçamento, engine ou trailer.

## Entregar

Marco atual com evidência, orçamentos com condição, o piso da barra, o gate que
segura o próximo passo, e a próxima fatia com prompt pronto. Exemplo:
[da trilha ao capítulo acabado](../examples/era-uma-vez-production.md). Sequência:
[`release`](release.md) quando o gate `deliver` for o pedido.
