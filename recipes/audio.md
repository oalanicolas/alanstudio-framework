# Áudio: mixagem, não pasta de arquivos

Entrada: a informação que o som precisa entregar e o que o jogador ouve hoje.

Uma pasta com arquivos corretos não é áudio de jogo. O que o jogador percebe é a
mistura: o que sobressai, o que recua, o que se repete até incomodar e o que o
silêncio destaca. Antes de baixar qualquer som novo, procure no acervo do
laboratório com `sfx search`; o piso é gravação licenciada ou design contemporâneo,
e 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão.

Defina o papel de cada som antes do arquivo: informar uma mudança de estado,
confirmar uma ação, avisar de uma ameaça fora da tela, marcar progresso ou compor
ambiente. Som sem papel é ruído que compete com o som que importa.

Examine a mistura, não os arquivos isolados:

- **Barramentos e controles:** música, efeito, voz e interface separados, com
  volume independente e persistido. Um controle único obriga o jogador a escolher
  entre ouvir a ameaça e suportar a música.
- **Prioridade e limite de vozes:** quando muitos eventos coincidem, quais somem.
  Sem isso, a cena densa vira massa e o aviso crítico desaparece exatamente quando
  é necessário.
- **Ducking:** o evento crítico abaixa o resto por um instante. É o que faz um som
  ser ouvido sem precisar ser mais alto.
- **Variação:** camadas, afinação e amostras alternadas para o som mais repetido.
  Fadiga auditiva aparece em minutos de jogo, não na primeira escuta.
- **Silêncio:** ausência é recurso de ritmo e de tensão. Trilha contínua achata a
  intensidade e apaga o contraste dos momentos altos.
- **Faixa dinâmica:** picos controlados, sem clipping e sem obrigar o jogador a
  baixar o volume do sistema. Meça; não confie na escuta em um fone só.
- **Coincidência com o feel:** contato sonoro e contato visual no mesmo instante.
  Alguns quadros de diferença são percebidos como imprecisão do controle.

Espacialização e áudio adaptativo entram quando o jogo os exige, com consumidores
reais. Não importe um middleware para completar uma lista.

Toda informação sonora precisa de equivalente visual — é requisito de
[acessibilidade](accessibility.md), não recurso extra. Proveniência de cada arquivo
é obrigatória: origem, crédito e condição de uso, registrados junto ao asset.
Reuso não concede licença nova.

Prova: cena densa com um evento crítico audível, medição de pico e volume
percebido, sessão longa verificando fadiga do som mais repetido, jogo completável
com o áudio desligado, e a proveniência de tudo que foi embarcado. Degraus:
[barra de acabamento](../references/production-bar.md#audio_mix--mixagem-não-arquivos).
