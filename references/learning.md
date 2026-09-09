# Aprendizados que atravessam jogos

O framework guarda conhecimento e ferramentas que podem servir a outros jogos.
O workspace guarda escolhas do criador, configuração, estado de cada jogo e provas
das aplicações. Um histórico local pode repetir a descrição de um caso; a regra
reutilizável tem uma fonte canônica no framework.

## Extrair no momento da descoberta

Quando uma rodada produz um método, falha recorrente ou correção transferível:

1. Identifique a fonte e a condição que tornou o problema observável. Preserve a
   evidência original no jogo, com versão, cenário, resultado e limitações.
2. Separe a escolha autoral da relação técnica. Uma preferência por gravação não é
   um requisito universal de áudio; validar licença e interrupção é reutilizável.
3. Encontre o consumidor canônico do aprendizado: receita, package da plataforma,
   checklist ou ferramenta existente. Adapte esse conteúdo; não crie uma segunda
   implementação nem um arquivo por incidente quando há lugar adequado.
4. Escreva **quando aplicar, o que verificar, o que invalida a conclusão e os limites**.
   Números locais ilustram o caso; não viram promessa de ganho em outra máquina.
5. Ligue a prova local à regra extraída. Na retomada, consulte a versão central;
   registre novas exceções ou contraprovas no mesmo lugar.

Se o conhecimento for uma hipótese, registre como hipótese com sua prova pendente.
Não promover uma hipótese a técnica comprovada e não deixar uma descoberta utilizável
presa ao laboratório. A execução desta revisão cabe ao agente: o scanner localiza
documentos, mas não decide sozinho se uma afirmação é transferível ou verdadeira.

## Destino do conteúdo

| Conteúdo | Fonte canônica |
| --- | --- |
| Ciclo de criação e critérios de decisão | [Workflow](creative-workflow.md), [processo](process.md) |
| Diagnóstico, comparação e custo de uma técnica | [Performance](../recipes/performance.md) |
| Carregador, renderizador ou serialização de uma plataforma | Package de [web](../packs/platforms/web.md) ou [Unity](../packs/platforms/unity.md), conforme o caso |
| Exportação, animação, buffers e proveniência | [Conteúdo](../recipes/content.md), [áudio](../recipes/audio.md) |
| Gestão de módulos e extração de repositórios | [Ferramentas de workspace](workspace-binding.md#módulos) |
| Preferência artística, fornecedor excluído, endereço de publicação | AGENTS/configuração do workspace ou documento do jogo |
| Medição bruta, captura, decisão aplicada e histórico | Jogo ou laboratório que produziu a prova |

Código específico permanece com seus consumidores. Para compartilhar uma implementação,
confirme o contrato comum e separe parâmetros de identidade, caminhos e políticas.
Uma técnica reutilizável pode viver como orientação em um package sem transformar
o código de um jogo inteiro numa biblioteca. O harness continua fino.

## Aprendizados incorporados nesta extração

O ciclo de criação, métodos de medição, invalidação de sombras, preservação de
identidade de instâncias, paridade entre renderizadores, exportação/serialização,
cadência de animação e custo de áudio foram extraídos dos registros de aplicações
do laboratório de setembro de 2026. As receitas e os packages acima contêm as
condições generalizadas; resultados e tentativas descartadas permanecem nos registros
originais. A [origem](sources.md#aprendizados-de-aplicações) delimita essa evidência.
