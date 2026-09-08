# Rede, autoridade e ações

Entrada: ação, participantes, estado compartilhado e comportamento esperado na falha.

Leia o protocolo existente e quem o consome. Identifique quem aceita a ação, valida
identidade/turno/recursos e decide o estado. Verifique o caminho com e sem identidade;
uma validação opcional de jogador não comprova autenticação. UI bloqueada não
equivale a recusa no executor autoritativo.

Preserve namespaces, isolamento de sala e estado local/persistente. Use duas sessões
reais para validar conexão, entrada, saída, reinício e reconexão. Examine mensagens
duplicadas, atrasadas, fora de ordem e após término quando o protocolo permitir esses
eventos. Teste unitário de serialização não prova conectividade real.

Para agentes que jogam, defina observação, ações permitidas, retorno de erro e término
de acordo com o jogo. Reutilize o ambiente existente antes de criar um servidor.
Separe contrato testado de capacidade presumida; nem toda interface sequencial
suporta execução paralela.

Referências de estudo: boardgame.io `RE-BGIO-005/009` e PettingZoo `RE-PZ-004/005/010`.
O estudo externo não demonstra a segurança ou o comportamento de rede do jogo
em edição. [Fontes](../references/sources.md).
