# Next

Uma próxima ação derivada do estado no disco, ordenada por dependência, com as
alternativas descartadas — e o agente resolvendo o passo, confirmando com a
conversa e entregando o prompt de continuidade pronto. O harness propõe; nunca
executa (`executed: false`).

## Escala

Igual em todas: a ordem é a das dependências. O que muda é o que existe para ler:
em `jam` a barra pode ter três linhas e nenhum gate declarado; cobrar dez
dimensões de um conto é ruído, e `next` não cobra o que o projeto não declarou.

## Avaliar

1. `next <projeto> --focus <foco>`. A proposta segue esta ordem: módulo não baixado →
   sem destino → sem entrypoint → área não localizada → rascunho → documento sem
   versão vigente → continuidade → sem instruções para o agente → validadores →
   gate (linha malformada, pergunta de valor, critério pendente) → barra (linha
   malformada, dimensão sem linha, conflito, subir a mais baixa).
2. Confronte com a conversa e o código: fonte encontrada não é tarefa validada. Se o next recusa que fonte encontrada seja tarefa validada, o `next` nomeia a validada que o next já recusa. Fonte no disco não é a tarefa. Sem chave `validada`.
   fonte em rascunho não é passo. Se o next recusa que fonte em rascunho seja passo, o `sources[n]` do continuity nomeia o passo que o next já recusa. Rascunho no disco não é o passo. Sem chave `passo`. Um comando registrado com falha não conclui etapa.
   Em "continue"/"vamos avançar", use `context --event resume` e leia
   `continuity.sources` ([processo](../references/process.md#continuidade-e-retomada)).
3. Se a proposta é uma **pergunta de valor** (`must_meet`), ela vem antes de mais
   trabalho: pergunte ao usuário se isto ainda vale o que custa. Se é subir a
   dimensão mais baixa, a proposta cita o critério escrito e a linha de onde veio.
4. Quando falta uma decisão que só o usuário pode tomar, peça-a em linguagem comum;
   não gere implementação presumida.

## Executar

Escolha **uma** ação recomendada, priorizando dependências e a incerteza que pode
invalidar o recorte; o backlog continua no plano. Se a ação já está autorizada,
registre e execute no mesmo turno; preparar o prompt não cria pausa de aprovação.
Gere o prompt de continuidade conforme o [roteiro](../references/gauntlet.md):
projeto, ação, fonte canônica, limites, prova; sem variáveis, sem jargão, sem pedir
horas. `gauntlet <projeto> --objective "..."` prepara o pacote; prepará-lo não
inicia execução.

## Verificar

A ação tem verbo, alvo e saída concreta; "pronto quando" é observável; a fonte para
retomar existe. `next_step: null` no JSON significa que **o agente ainda deve
resolver e comunicar o passo**, nunca encerrar com esse valor cru.

## Nunca

- Transferir a priorização do backlog ao usuário na resposta final.
- Retomar um rascunho de template como se fosse continuidade.
- Autorizar silenciosamente um backlog inteiro, publicação ou contato externo por
  causa de um "vamos avançar".
- Inventar tarefa quando o objetivo terminou, ou pedir horas para gerar o prompt.
- Declarar bloqueio por permissão já concedida.

## Entregar

Onde estamos, a próxima ação com motivo e prova, e o prompt pronto para copiar.
Se o objetivo inteiro terminou, diga isso. O comando que executa a ação é o que
ela nomeia (`craft`, `feel`, `harden`…).
