# Rede, autoridade e ações

Entrada: ação, participantes, estado compartilhado e comportamento esperado na falha.

No starter, a rede que existe é o serve anunciando a LAN e, depois
do fim, a página apontando `/?invite=1&seed=<n>` — e `&spawn=<mesa>`
e `&look=<paleta>` se o last-run nomeou a chuva ou o look — para
enviar essa partida. Compartilhar o endereço não é alguém de fora
nem duas sessões reais. Com tela, a primeira superfície continua a
porta.

Leia o protocolo existente e quem o consome. Identifique quem aceita a ação, valida
identidade/turno/recursos e decide o estado. Verifique o caminho com e sem identidade;
uma validação opcional de jogador não comprova autenticação. UI bloqueada não
equivale a recusa no executor autoritativo.

Preserve namespaces, isolamento de sala e estado local/persistente. Use duas sessões
reais para validar conexão, entrada, saída, reinício e reconexão. Examine mensagens
duplicadas, atrasadas, fora de ordem e após término quando o protocolo permitir esses
eventos. Teste unitário de serialização não prova conectividade real.

Ao sair ou trocar de sala, invalide a conexão anterior antes de fechá-la. Listeners
de `state` e `close` precisam pertencer à conexão corrente: um snapshot em voo não
pode reabrir a sala abandonada, nem o fechamento antigo apagar a promessa de uma
conexão nova. Entrada explícita também cancela retomada automática pendente. Prove
sair → entrar, retomada interrompida e entrega tardia do socket antigo.

Separe presença atual de resultado concluído. Depois de encerrar uma rodada,
congele participantes, classificação, tempos e conteúdo que compõem o placar por
identificador da rodada. Sair ou reconectar muda presença e liderança, sem reescrever
quem disputou ou venceu. Uma revanche abre uma nova rodada com a lista vigente.
Prove resultado → saída de participante → recarga do anfitrião → revanche.

Caso observado e testes: `games/desnhe-um-cavalo/docs/qa.md` no laboratório,
11/09/2026. A inspeção com duas abas encontrou remoção do rival após recarga; os
testes de sessão cobrem também eventos atrasados. Não presume teste humano.

Para agentes que jogam, defina observação, ações permitidas, retorno de erro e término
de acordo com o jogo. Reutilize o ambiente existente antes de criar um servidor.
Separe contrato testado de capacidade presumida; nem toda interface sequencial
suporta execução paralela.

Referências no laboratório: testes de rede do Distrito Rabisco e estudos em `swipe/`.
boardgame.io `RE-BGIO-005/009` e PettingZoo `RE-PZ-004/005/010`
([fontes](../references/sources.md)). O estudo externo não demonstra a segurança
ou o comportamento de rede do jogo em edição.
