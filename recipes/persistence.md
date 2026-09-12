# Persistência: progresso e confiança

Entrada: o que precisa sobreviver a fechar o jogo e o que acontece quando o dado
salvo não corresponde mais ao código.

Um save é um contrato com o tempo do jogador. Ele é a única parte do jogo que uma
atualização pode destruir de forma irreversível: código volta por reversão, dado
transformado não. Trate a mudança de formato com o cuidado de uma migração de
banco, não de um ajuste de estrutura.

Separe as três categorias antes de escrever qualquer coisa no disco:

- **Efêmero:** existe só durante a partida e é reconstruído ao iniciar.
- **Persistente de progresso:** o que o jogador conquistou e não aceitaria perder.
- **Persistente de preferência:** volume, controles, acessibilidade, idioma. Vive
  separado do progresso, porque sobrevive a apagar a partida.

Derivado não se salva: salvar o que pode ser recalculado cria dois caminhos que
divergem e uma inconsistência impossível de reproduzir.

Versione o formato desde a primeira gravação e escreva a migração junto da mudança,
não depois. Uma versão sem migração transforma qualquer atualização em perda de
progresso. Mantenha a migração para trás por quantas versões o jogo já esteve nas
mãos de alguém, e teste **a cadeia inteira**, não apenas o último salto. Se a receita recusa que listar o fonte prove a cadeia inteira, o `sources` do `save` nomeia a cadeia que a receita já recusa. Arquivo no disco não é a migração. Sem chave `cadeia`.

Trate dado inválido como caso normal, não como exceção: arquivo truncado, campo
ausente, valor fora de faixa, save de uma versão futura, armazenamento cheio ou
negado. A política precisa preservar o que ainda é aproveitável e falhar de forma
legível para o jogador. A porta e o fim nomeiam sessão volátil e
gravação que não ficou. Preferências ilegíveis avisam no painel
(`settings_recovered`); o arquivo fica em `settings.broken`. A porta
e o fim no canvas pintam a mesma linha (`settingsLine`). A pausa
não. Se o canvas pinta `settingsLine`, o `save` nomeia a recuperação.
A pausa não. Texto no disco não é aba fechada. Sem chave `recovery`.
`persistLine` continua só sessão volátil e gravação recusada.
A região viva, na porta e no fim, nomeia a mesma linha do painel.
Jogando a chave some. Nomear não é aba fechada. `save` relata `warned` se o disco tem
`persistLine`, `title_volatile`, `title_unsaved`, `settings_recovered`
ou `settings.broken`. Nomear não é
aba fechada nem `trusted`.
**Não apague save real para fazer um teste passar**; ao
migrar, preserve o original até a nova gravação estar confirmada.

Grave em escrita atômica — arquivo temporário e substituição — para que uma
interrupção no meio não deixe um save pela metade. Defina os momentos de gravação
automática e verifique o que acontece na interrupção abrupta: aba fechada, processo
encerrado, bateria, perda de foco, suspensão do dispositivo.

Identidade estável é o que permite migrar. Se entidades, níveis ou itens são
referenciados por índice ou por nome de arquivo, qualquer reordenação corrompe
saves antigos silenciosamente. Versão do conteúdo e versão do save são contratos
distintos; não os una em um número por conveniência. Se a receita recusa que um único número una a versão do conteúdo e a do save, o `save` nomeia os contratos que a receita já recusa. Schema no disco não é a história. Sem chave `contratos`.

`save <projeto>` lê se o código usa armazenamento e se declara schema/migrate.
`trusted` é sempre falso: o harness não abre o save e não confirma escrita.

Implementação concreta, com o limite dito: o starter `canvas-arcade` versiona o
save em `src/core/save.js` (schema 3), com migração e recuperação de dado inválido.
`hold` guarda o tick interrompido — seed, `rngState`, chuva, ofício
e o relógio da porta (`attractTick`). Sem o relógio o campo
repetia a frase e o mover. `canResume` lê o hold; `canContinue`
continua sendo repetir a última seed.
`?seed=<n>` abre essa partida e ignora o hold — não é Continuar.
`?spawn=` abre essa chuva e ignora o hold da outra mesa.
`?look=` e `?speed=` vestem o hold que já está.
Pausa, `pagehide`, `beforeunload`, perda de foco e o controle que some gravam o hold. Se o disco escuta `beforeunload`, o `save` nomeia o fechamento que o disco já grava. Gancho no disco não é aba fechada. Sem chave `beforeunload`. Se o disco verifica a gravação, o `save` nomeia a gravação que o storage já verifica. Escrita no disco não é aba fechada. Sem chave `storage`. Terminar ou resetar limpa.
`?look=` / `?spawn=` / `?speed=` vestem a sessão. Fechar, esconder
ou `flush` não grava esses eixos — o convite é candidato, não
preferência. Escolher no painel grava. Query no disco não é
aba fechada nem `trusted`.
A outra aba veste as preferências desta página (`storage`); o progresso
em curso não. Ouvir não é aba fechada. Isto **não** é aba fechada observada e não sobe `state_trust`. Grava
de forma **verificada** em `src/core/storage.js` — escreve em chave de estágio,
relê, compara e só então grava na chave real. Isso **não** é a escrita atômica do
parágrafo acima: `localStorage` não tem substituição, então a gravação final é
uma escrita comum, com a mesma exposição a interrupção que uma escrita direta. O
estágio compra detecção de cota e de truncamento, não atomicidade. Se a receita recusa que o estágio seja atomicidade, o `save` nomeia a atomicidade que a receita já recusa. Estágio no disco não é substituição. Sem chave `atomicidade`. Para ter
atomicidade de verdade nesse alvo é preciso outro armazenamento — IndexedDB tem
transação. `tests/save.test.mjs` exercita migração, dado corrompido, preferência
fora de faixa e o aviso da recuperação; interrupção abrupta real, ninguém exercitou.

Prova: cadeia de migração desde a versão mais antiga em uso, carregamento de cada
forma de dado inválido, interrupção forçada durante a gravação, progresso real
preservado após atualização, e preferências sobrevivendo à remoção da partida.
Degraus: [barra de acabamento](../references/production-bar.md#state_trust--confiança-no-estado).
Transições, pausa e descarte continuam em [lifecycle](lifecycle.md); formato de
conteúdo em [content](content.md).
