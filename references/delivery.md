# Conferir a entrega pelo pedido

Antes de declarar conclusão, releia o pedido vigente e confronte o aceite com os
artefatos produzidos e a resposta que pretende enviar. Uma execução tecnicamente
correta pode ter entregue outra coisa. Use o QA, plano ou Devlog existente; ajuste
pequeno cabe em poucas linhas, sem novo documento ou checklist apresentado ao usuário.

Para cada resultado necessário, registre **pedido → aceite observável → artefato
e localizador → prova e limite → atendido, não atendido ou desconhecido**. Não troque
o aceite depois da execução para acomodar o resultado. “Não aplicável” precisa de
motivo relacionado ao escopo, nunca apenas de evidência ausente.

- **Intenção:** a ação realizada responde ao objeto e ao contexto do pedido?
  “Inicialize o projeto” exige o diagnóstico da [auditoria](project-audit.md);
  “inicie o servidor” exige a operação; “vamos avançar” retoma o recorte vigente.
- **Artefato:** o conteúdo ou comportamento necessário existe e está ligado à fonte
  canônica? Leia o resultado e seus consumidores. Lista de arquivos, títulos e
  templates preenchidos não comprovam regras ou arquitetura corretas. Se a entrega recusa que templates preenchidos comprovem regras, o `context` nomeia as regras que a entrega já recusa. Critério no disco não é a entrega. Sem chave `regras`.
- **Prova:** o cenário exercita o resultado pedido? Localize fonte, trecho, teste,
  recibo ou observação. Teste do harness comprova seu mecanismo; execução do agente
  exige pedido, ações e resultado reais. Arte e experiência continuam separadas.
- **Continuidade:** o registro descreve o estado que acabou de ser comprovado?
  Se existe próximo recorte definido, o [prompt pronto](gauntlet.md) está no registro
  e na resposta, com projeto, ação, fonte, limites e prova? “Próximo: melhorar o jogo”
  não resolve o trabalho seguinte. Continue o que já estiver autorizado.

Não encerre com sucesso quando faltar um resultado necessário. Corrija a causa e
repita somente a verificação afetada: intenção errada volta ao pedido; especificação
ambígua volta à fonte da decisão; implementação falha volta ao código; evidência
insuficiente exige uma prova melhor. Bloqueio real deixa o resultado parcial explícito.
Não invente autorização, aprovação artística ou verificação ausente para fechar a lista.

Na resposta, priorize o resultado pedido, a evidência que o sustenta, a limitação
material e a continuidade. Não é preciso expor todo o registro de revisão.

## Quando melhorar o próprio framework

Uma falha recorrente de uso pede um caso comportamental, além dos testes do CLI.
Preserve o pedido real, a resposta e as ações observáveis; identifique versão e
lacunas do registro. Turno ainda em andamento não tem entrega final para aprovar.

Defina os critérios antes da execução. Em teste isolado, forneça ao agente apenas
skill, pedido realista e fontes necessárias; não forneça o gabarito nem a correção
esperada. Cópia reduzida deve declarar adaptações e recursos ausentes. Delegação
depende da autorização aplicável; revisão própria deve ser identificada como tal.

Guarde entrada, versão da skill, artefatos, comandos/resultados e resposta final.
Revise cada critério com localizadores, inclusive os que falharam ou permaneceram
desconhecidos. Hash ajuda a identificar o conteúdo; não comprova seu significado.
Reexecute o caso afetado após uma correção observada. Não transforme dois exemplos
aprovados em garantia de obediência universal ou de trabalho por horas.

Origem: revisão por aceite e por causa do [BMad e estudos](sources.md), disciplina
de evidência já adotada em [qualidade](quality.md), e casos de inicialização e
continuidade registrados na [adoção](../adoption.md).
