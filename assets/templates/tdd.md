# TDD — {{PROJECT}}

Projeto: {{PROJECT_PATH}}
Status: rascunho. Autor/revisão: [preencher]. Requisitos do recorte: [IDs/fontes].
TDD aqui é Technical Design Document, documento de decisões técnicas.

## Recorte e profundidade

- Cenário do jogador → requisito/aceite → consequência observável: [fontes].
- Alcance, incerteza e reversibilidade: [efeito concreto nos consumidores/jogador].
- Profundidade escolhida: [decisão local / análise entre sistemas / PoC primeiro; motivo].
- Atual observado / direção aprovada / proposta / desconhecido: [separar].
- Decisões vigentes aplicáveis: [fonte/estado; divergências com código ou direção atual].

## Estado atual e mapa de reuso

- Fonte/versão e comandos atuais: [paths, manifestos e validator lidos].
- Necessidade → candidato → consumidor → adequação: [preencher ou referenciar registro canônico].
- REUSE/ADAPT/CREATE: [decisão por responsabilidade, motivo e lacuna].
- Limite do diff: [arquivos/módulos afetados e consumidores a preservar].
- Contexto da tarefa: [entrada/símbolo → fonte a alterar → consumidor; por que importa].
- Exemplares, dependências e testes: [padrão útil, relação e limite da inspeção].

## Impacto do recorte

- Responsabilidade afetada → quem lê/escreve → contrato/invariante → regressão possível.
- [Examinar tempo/estado, saves/versões, conteúdo, apresentação/recursos e rede pertinentes.]
- Fora do recorte / cobertura ainda desconhecida: [motivo e investigação necessária].

## Decisão — TDD-D01

- Requisitos cobertos: [FR/NFR/AC].
- Problema observado: [por que a decisão é necessária].
- Alternativa menor examinada: [resultado e limite].
- Outras alternativas relevantes: [REUSE/ADAPT/CREATE; manter o atual quando viável].
- Escolha e responsabilidade: [onde implementar e o que permanece no jogo].
- Contrato: [entrada, saída, estado, invariantes e recusa relevante].
- Consequências: [acoplamento, manutenção, recursos e limitações].
- Prova: [teste/experimento e cenário de integração].
- Contraprova / gatilho de revisão: [resultado que invalida a escolha e ação correspondente].
- Reversibilidade: [como desfazer a mudança; recuperar dados pode exigir mais que reverter código].

## Estado, tempo e recursos

[Ciclo de vida, controle do tempo/RNG quando existente, persistência/versionamento,
carregamento de conteúdo, eventos, GPU, som e descarte pertinentes. Não declarar
reset/seed/observe/act/advance/capture/dispose disponíveis sem evidência.]

## Integrações e limites

[Interfaces existentes, autoridade de ações e identidade quando houver rede,
formatos de assets/dados e compatibilidade. Origem/licença e custos de recursos.
Preserve a qualidade aprovada; investigue eficiência sem empobrecer o resultado.]

## Fatias de implementação

- TASK-01: [resultado jogável], requisitos [IDs], entrada [fontes], saída [mudança].
- Dependência: [decisão/recurso necessário antes de começar].
- Consome artefato: [quando houver; caminho/versão disponível, distinto da mera ordem].
- Retomar por: [arquivo/símbolo e exemplar; primeiro consumidor a integrar].
- Aceite/prova: [caso, comando do projeto e observação correspondente].
- Ambiente da prova: [editor/build/export, plataforma e configuração; limites].
- Risco sem prova: [PoC delimitada; não tratar hipótese como capacidade].

## Revisão e retomada

- Cobertura do recorte: [requisitos sem decisão ou sem teste].
- Prontidão: [fontes/consumidores lidos, contratos suficientes e riscos delimitados?].
- Provas disponíveis: [comportamento demonstrável por requisito; ausência vira PoC/observabilidade].
- Revisado por / evidência / data: [preencher após revisão].
- Próxima tarefa e resultado esperado: [preencher].
- Por que agora / pronto quando: [dependência ou risco prioritário e evidência que encerra].
- Impacto de mudança futura: [quais requisitos, consumidores e evidências reexaminar].
