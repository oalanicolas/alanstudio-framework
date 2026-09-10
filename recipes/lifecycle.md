# Ciclo de vida, tempo e observação

Entrada: transição ou estado que precisa ser criado, reproduzido ou encerrado.

Antes de abstrair, localize os caminhos reais de início, atualização, render,
eventos, áudio, pausa, término, reinício e descarte. Declare o que é controlável e
o que permanece desconhecido. Os oito nomes `pause`, `reset`, `seed`, `observe`,
`act`, `advance`, `capture` e `dispose` são vocabulário de inspeção; não uma API
implementada pelo harness. `context --focus lifecycle` lista catálogos do foco e
menções nesses arquivos, sem promover token a capacidade verificada. Quando um
teste do projeto exercitar um deles, `verify --proves <nome>` anexa a alegação ao
recibo, com autor, argv e log — `claimed`, nunca `verified`.

**Teste o contrato pela ligação, não só pela API.** Uma suíte que chama
`game.pause()` e `game.resume()` diretamente passa mesmo quando despausar pelo
teclado é impossível — foi o que aconteceu no starter `canvas-arcade`, onde a
leitura da tecla morava dentro da simulação, que não roda em pausa. O comando
para sair de um estado nunca pode ser lido por um caminho que aquele estado
desliga. Percorra a ligação real: evento de entrada → quadro → estado.

Com tela, o ciclo deste starter é abertura → partida → fim → abertura.
O avanço abre a porta e, depois do fim, um avanço *novo* volta a ela.
R no overlay também. Sem tela o headless já joga. A página oferece o
recibo no overlay e na porta se houver partida; isso não é observação.
Aba escondida pausa no campo e no fim. Na porta só descarrega — P já
é ignorado e a placa nem nasce. Na pausa o toque retoma; Espaço
continua só intenção. Na porta o telefone vê Jogar: toque
sem ter apertado; lastSource continua teclado. Perda de foco da janela grava o hold
e senta o mesmo relógio; na porta só descarrega. O controle que some
senta o mesmo relógio se a sessão falou no pad; teclado e toque não
sentam porque um pad na gaveta desconectou. Na porta só descarrega.
Hidden que pausa sem P para retomar
congela a mostra. A query de look, chuva e relógio veste a
sessão; `pagehide` e `flush` não a gravam. Escolher no painel
grava. `?spawn=` não retoma o hold de outra mesa; look e
relógio vestem o tick que já está. Stub não é aba fechada nem sessão no controle.

Examine separadamente:

- Pausa da simulação, render visível, input, áudio, callbacks e transições.
- Reinício de entidades, score, colisões, timers, RNG e progresso persistente.
- Descarte de listeners, loops, GPU, áudio e conexões. Execute montar → desmontar
  → montar; comportamento duplicado indica recurso sobrevivente.
- Tempo real versus relógio controlado. Verifique se avançar o relógio realmente
  move todos os sistemas relevantes, inclusive callbacks.
- Seed: repita estado inicial e sequência de ações, compare observações. Aceitar
  um parâmetro não prova que ele afeta RNG ou que toda a simulação é determinística.

Adapte o teste que já existe; crie um controle novo somente se o caso exigir e a
capacidade não estiver disponível. Observação de estado deve conter o necessário
à tarefa, sem transportar memória interna ilimitada para a IA a cada quadro.

Referências no laboratório: ciclo do Distrito Rabisco, verificador Unity de
protótipo e ambientes de estudo em `swipe/`. Ausência desses arquivos neste
repositório não invalida a receita.
Phaser `RE-PHASER-005..010`, Excalibur `RE-EXCAL-004/007`, Godot
`RE-DODGE-002/003/010` e PettingZoo `RE-PZ-002/005/007` fornecem precedentes
distintos, incluindo callbacks que sobrevivem e seed ignorada. [Fontes](../references/sources.md).
