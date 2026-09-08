# Processo comum

O trabalho começa por uma tarefa e termina por seu resultado observado. A quantidade
de documentação acompanha o risco: um ajuste pequeno cabe no registro atual; uma
criação nova precisa de briefing e decisões retomáveis. Não há número obrigatório
de agentes, stories ou rodadas.

Para concepção e produção de um jogo novo, o [ciclo criativo](preproduction.md)
detalha Game Brief, MDA, GDD, PoC, PRD, TDD, vertical slice, MVP e QA/playtest,
com templates, critérios de prontidão e rastreabilidade. Em correções pequenas,
atualize somente a decisão e a evidência afetadas no registro existente.

## 1. Estado e intenção

Leia a direção atual do usuário, AGENTS, versão do jogo, brief, decisões e referência
aprovada. Diferencie original, variante e experimento. Uma hipótese do agente não
substitui uma decisão do usuário. Um caminho ou hash prova identidade, não leitura.

Descreva: **jogador faz X, decide entre Y e Z, percebe a consequência W, para sentir S**.
Registre plataforma/entrada, cenário, restrições e o que deve ser observável ao
terminar. Para correção, comece pelo sintoma reproduzido; para polimento, pela
referência e pela diferença percebida. Defina a prova de parada antes de ampliar o escopo.

## 2. REUSE → ADAPT → CREATE

Busque primeiro no próprio jogo; depois em jogos parecidos e nos estudos pertinentes.
Leia a implementação **e um consumidor real**. Registre comando/resultado da busca,
candidato e adequação. A busca é delimitada à necessidade, não uma auditoria de tudo.

- **REUSE:** atende à experiência por uso ou configuração já suportada.
- **ADAPT:** estender a fonte canônica preserva seus consumidores, qualidade e
  manutenção. Delimite a capacidade que falta e os testes de quem já a consome.
- **CREATE:** nenhuma alternativa atende sem acoplamento inadequado, regressão ou
  custo de adaptação injustificado. Explicite essa lacuna e crie somente o necessário.

Considere compatibilidade, licença/proveniência, dependências, substituição e custo
de manutenção. Um asset disponível no disco não é automaticamente reutilizável.
Não copie runtime de referência só para absorver um contrato. Antes de nova camada,
aponte a falha observada e tente a solução menor. Três consumidores com a mesma
responsabilidade justificam examinar uma extração; três nomes parecidos não bastam.

Registro mínimo: **necessidade → candidatos/consumidores → decisão e motivo → limite
da mudança → prova**. Pode viver em decisions.md ou story existente. O contrato
opcional e `check-plan` verificam forma e caminhos; não garantem mérito ou obediência.

## 3. Fatia jogável

Produza um ciclo curto com entrada, decisão, consequência e reinício, adequado ao
gênero. Resolva primeiro a incerteza que pode invalidar a experiência. Use valores
existentes como ponto de partida, não como constantes universais. Transforme uma
variável relevante por vez quando precisar atribuir causa a um resultado.

Preserve separação entre regra, apresentação e conteúdo **onde ela já existe**.
Não converta todos os jogos para um ECS, schema, relógio ou servidor comum. Ferramentas
compartilhadas recebem projeto/cenário por parâmetro; nomes de armas e carros pertencem
ao jogo. Scripts cuidam do exato; IA e pessoas avaliam intenção, legibilidade e gosto.

## 4. Diagnosticar e provar

Reproduza a falha no caminho real. Examine entrada, estado, ambiente, ferramentas e
causa antes de alterar sintomas ou trocar de modelo. Mocks servem a testes delimitados;
não substituem integração real nem observação do jogador.

Execute o validador do projeto e o cenário afetado. Para decisões relevantes, compare
alternativas nas mesmas condições e use revisão independente quando autorizada e
proporcional; registre divergências que mudem a escolha. Não faça média entre arte,
correção e diversão para compensar regressões.

## 5. Encerrar e aprender

Declare mudança, partes herdadas/adaptadas/criadas, comandos/resultados, observação
da experiência e lacunas. Conclusão da IA é uma alegação sustentada por evidência.
Registre tentativas descartadas, motivo das decisões e como reproduzir a comparação
no registro existente. Performance tem um local próprio no jogo em edição.

Se uma regra de processo falhar repetidamente, corrija fonte, contexto ou ferramenta
antes de adicionar instruções. Só automatize julgamento após observação e calibração.
Custos de tempo, ferramentas, assets, revisão e execução podem orientar escolhas
entre alternativas que preservam qualidade. Apoios específicos a um modelo precisam
ser reavaliados quando ele muda; neutralidade de interface não prova substitutibilidade.

## Origem e autoridade

Os 18 princípios traduzidos para este processo: reuso, estado canônico, falha antes de estrutura, repetição,
contratos portáteis, determinismo/julgamento, menor mudança, causa-raiz, entrada real,
honestidade do mecanismo, prova externa, criação/revisão/escolha, contexto sob demanda,
tarefa primeiro, processo antes de modelo, parada/aprendizado, contexto por parâmetro
e autoridade do usuário. São orientação aplicada por leitura e julgamento, exceto
os limites específicos documentados nos comandos do [harness](../README.md).
