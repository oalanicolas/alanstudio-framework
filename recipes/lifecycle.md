# Ciclo de vida, tempo e observação

Entrada: transição ou estado que precisa ser criado, reproduzido ou encerrado.

Antes de abstrair, localize os caminhos reais de início, atualização, render,
eventos, áudio, pausa, término, reinício e descarte. Declare o que é controlável e
o que permanece desconhecido. Os nomes `pause`, `reset`, `observe`, `act`, `advance`, `capture`
e `dispose` são vocabulário de inspeção; não uma API implementada pelo harness.
`context --focus lifecycle` lista catálogos do foco e menções nesses arquivos,
sem promover token a capacidade verificada.

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

Referências de estudo: Phaser `RE-PHASER-005..010`, Excalibur `RE-EXCAL-004/007`, Godot
`RE-DODGE-002/003/010` e PettingZoo `RE-PZ-002/005/007` fornecem precedentes
distintos, incluindo callbacks que sobrevivem e seed ignorada. [Fontes](../references/sources.md).
