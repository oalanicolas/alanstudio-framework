# Mecânicas e decisões

Entrada: ação, estado inicial, alternativa e consequência que precisam mudar.

Leia regra, configuração e consumidor existentes. Separe o requisito de experiência
da primeira solução imaginada. Tente configurar o sistema atual, depois estendê-lo;
crie uma capacidade somente quando a lacuna estiver demonstrada.

Descreva a regra como **estado + ação permitida → novo estado + feedback**. Inclua
recusa e ausência de efeito: recurso insuficiente, alvo inválido, jogador inativo,
ação depois do término. Não presuma que um erro lança exceção ou retorna o mesmo
estado em todas as bibliotecas; confirme a implementação local.

Teste invariantes nos limites: recursos não duplicam, ações recusadas não consomem
turno indevidamente, vitória/derrota não dispara duas vezes. Separe esse teste da
pergunta criativa: a decisão é compreensível e vale a pena?

Para ajuste de dificuldade ou economia, registre situação inicial, comportamento
observado e variável alterada. Compare alternativas sob o mesmo cenário. Não deduza
equilíbrio da ausência de exceções ou de uma partida vencida pela própria IA.

Referências de estudo: boardgame.io `RE-BGIO-003`, `RE-BGIO-006`, `RE-BGIO-011`.
As regras externas descrevem aquele fluxo; não obrigam outros gêneros a usar turnos.
[Fontes](../references/sources.md).
