# Mecânicas e decisões

Entrada: ação, estado inicial, alternativa e consequência que precisam mudar.

Com tela, a primeira regra é a porta. O campo — chuva, guarda,
recusa — começa depois do avanço. A mostra da porta marca o
trilho no mesmo alcance do campo; descrever só o meio da partida
esconde o verbo que abre o ciclo. Sem tela o headless já joga.

Leia regra, configuração e consumidor existentes. Separe o requisito de experiência
da primeira solução imaginada. Tente configurar o sistema atual, depois estendê-lo;
crie uma capacidade somente quando a lacuna estiver demonstrada.

Descreva a regra como **estado + ação permitida → novo estado + feedback**. Inclua
recusa e ausência de efeito: recurso insuficiente, alvo inválido, jogador inativo,
ação depois do término. Não presuma que um erro lança exceção ou retorna o mesmo
estado em todas as bibliotecas; confirme a implementação local.

Teste invariantes nos limites: recursos não duplicam, ações recusadas não consomem
turno indevidamente, vitória/derrota não dispara duas vezes. Separe esse teste da
pergunta criativa: a decisão é compreensível e vale a pena? A regra correta com
verbo sem peso ainda pede [feel](feel.md); recusa e sucesso precisam ser
distintos também no [áudio](audio.md).

Para ajuste de dificuldade ou economia, registre situação inicial, comportamento
observado e variável alterada. Compare alternativas sob o mesmo cenário. Não deduza
equilíbrio da ausência de exceções ou de uma partida vencida pela própria IA.

Ao adaptar IA de grade para movimento contínuo, compare o primeiro trecho da rota
com a posição real do corpo. Recomeçar cada busca como se o agente estivesse no
centro da célula pode acrescentar tempo fictício e fazê-lo abandonar uma fuga em
andamento. Também distinga entrada na célula de chegada ao centro: prever que um
perigo terá acabado na chegada não garante travessia segura da borda. Reproduza
ameaças próximas com posições fracionárias, em vários passos consecutivos; uma
rota válida somente no instante do plantio não comprova fuga executável.

Caso e contraprovas: Rabisco Boom, revisão de gameplay de 2026-09-09 no laboratório,
`tests/gameplay-v2.test.js` (fogo ativo na borda e replanejamento entre duas bombas).
A condição é técnica; não estabelece pesos universais de IA nem comprova diversão.

Referências: testes de Era Uma Vez e simulação de Brasa-Pista no laboratório;
boardgame.io `RE-BGIO-003`, `RE-BGIO-006`, `RE-BGIO-011`
([fonte](https://github.com/boardgameio/boardgame.io)).
As regras externas descrevem aquele fluxo; não obrigam outros gêneros a usar turnos.
