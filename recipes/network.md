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

Preserve o motivo de término separado do estado de fim da partida. Vitória,
derrota, encerramento administrativo e troca de mapa podem compartilhar o fluxo,
mas não a interpretação do resultado. Transporte o motivo aos consumidores de UI,
placar e analytics; no COOP, encerrar pelo anfitrião não significa perder para a
máquina. Prove os motivos aplicáveis em cada modo, com anfitrião e convidado; uma
prova PVP não cobre automaticamente a cópia e o resultado do COOP. Caso e prova:
sessão S17, `qa/verify-coop-end.mjs` do Distrito Rabisco e piloto de memória do
laboratório, 22/09/2026. Modos sem vitória ou derrota mantêm sua própria semântica.

Separe presença atual de resultado concluído. Depois de encerrar uma rodada,
congele participantes, classificação, tempos e conteúdo que compõem o placar por
identificador da rodada. Sair ou reconectar muda presença e liderança, sem reescrever
quem disputou ou venceu. Uma revanche abre uma nova rodada com a lista vigente.
Prove resultado → saída de participante → recarga do anfitrião → revanche.

Caso observado e testes: `games/desnhe-um-cavalo/docs/qa.md` no laboratório,
11/09/2026. A inspeção com duas abas encontrou remoção do rival após recarga; os
testes de sessão cobrem também eventos atrasados. Não presume teste humano.

Em salas com papéis, filtre ações no host antes de encaminhá-las a outro par:
remover o corpo visual do espectador não impede dano, itens ou eventos forjados.
Separe capacidade de combate, capacidade de observação e identidade de jogador.

Ao transferir o host, não confunda ID do jogador com endereço de sinalização.
Prepare o sucessor, confirme recebimento, congele o estado e só então libere o
endereço; reconexões usam tickets vinculados aos pares e prazo de falha explícito.
Preserve relógios, resultados e autoridade sobre simulação, incluindo projéteis e
inventário. Segredos de admissão passam somente ao sucessor por canal privado;
nunca em roster ou convite. Declare se cobre saída explícita ou falha abrupta,
e se o histórico persistido acompanha a transferência. Prove uma segunda sucessão.

Caso e provas: `games/distrito-rabisco/production/evidence/m9-sala-vagas-20260922/`
no laboratório. Três clientes verificaram código/IDs estáveis, sucessão para
espectador, senha e bloqueios preservados, FFA e COOP. Transporte em memória e
WebRTC com sinalização real são provas distintas; uma máquina não comprova TURN
forçado nem redes físicas diferentes.

Para agentes que jogam, defina observação, ações permitidas, retorno de erro e término
de acordo com o jogo. Reutilize o ambiente existente antes de criar um servidor.
Separe contrato testado de capacidade presumida; nem toda interface sequencial
suporta execução paralela.

Em modos por equipe, separe identidade pessoal, vaga e time; a atribuição vem do
anfitrião, nunca de campos declarados no pacote de dano. Filtre origem e destino
antes do relay e novamente no receptor. Guarde pontos coletivos fora da lista de
presença: desconectar o autor não pode retirar um abate. Prove entrada tardia e
sucessão com pontos já marcados. Reinício de rodada deve limpar limites temporais
e deduplicação vinculados à rodada anterior; exercite uma revanche imediata,
pois aguardar a intermissão inteira pode esconder estado herdado indevidamente.
Caso e prova: `games/distrito-rabisco/production/evidence/m10-equipes-20260922/`.

Referências no laboratório: testes de rede do Distrito Rabisco e estudos em `swipe/`.
boardgame.io `RE-BGIO-005/009` e PettingZoo `RE-PZ-004/005/010`
([fontes](../references/sources.md)). O estudo externo não demonstra a segurança
ou o comportamento de rede do jogo em edição.
