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
mãos de alguém, e teste **a cadeia inteira**, não apenas o último salto.

Trate dado inválido como caso normal, não como exceção: arquivo truncado, campo
ausente, valor fora de faixa, save de uma versão futura, armazenamento cheio ou
negado. A política precisa preservar o que ainda é aproveitável e falhar de forma
legível para o jogador. **Não apague save real para fazer um teste passar**; ao
migrar, preserve o original até a nova gravação estar confirmada.

Grave em escrita atômica — arquivo temporário e substituição — para que uma
interrupção no meio não deixe um save pela metade. Defina os momentos de gravação
automática e verifique o que acontece na interrupção abrupta: aba fechada, processo
encerrado, bateria, perda de foco, suspensão do dispositivo.

Identidade estável é o que permite migrar. Se entidades, níveis ou itens são
referenciados por índice ou por nome de arquivo, qualquer reordenação corrompe
saves antigos silenciosamente. Versão do conteúdo e versão do save são contratos
distintos; não os una em um número por conveniência.

Implementação concreta: o starter `canvas-arcade` versiona o save em
`src/core/save.js`, com migração e recuperação de dado inválido, e escreve de forma
atômica em `src/core/storage.js`. `tests/save.test.mjs` exercita migração, dado
corrompido e preferência fora de faixa.

Prova: cadeia de migração desde a versão mais antiga em uso, carregamento de cada
forma de dado inválido, interrupção forçada durante a gravação, progresso real
preservado após atualização, e preferências sobrevivendo à remoção da partida.
Degraus: [barra de acabamento](../references/production-bar.md#state_trust--confiança-no-estado).
Transições, pausa e descarte continuam em [lifecycle](lifecycle.md); formato de
conteúdo em [content](content.md).
