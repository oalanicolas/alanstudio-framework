# Acessibilidade e alcance

Entrada: a barreira concreta que impede alguém de jogar — entrada, visão, audição,
movimento, leitura ou tempo de reação.

Com tela, a primeira superfície é a porta. O aviso do primeiro ciclo
mora no campo, depois do avanço. Overlay, HUD da abertura e a legenda
também seguem `uiScale`. A porta lê a legenda que o mixer ainda guarda.
Sem tela o headless já joga.

Acesso é decisão de design, não camada final. Tratado no GDD, custa uma escolha;
tratado depois do conteúdo pronto, custa retrabalho de arte, UI e regra. Registre
essas opções como requisitos de qualidade no PRD, com forma de verificar.

Examine as barreiras que o jogo realmente cria:

- **Entrada:** remapeamento de todos os comandos, inclusive os de menu; alternativa
  a pressionar e segurar e a apertar repetidamente; sensibilidade e zona morta
  ajustáveis; jogo completável com uma das mãos quando isso for viável no gênero.
- **Visão:** nenhum estado dependente exclusivamente de cor — forma, ícone,
  posição ou texto acompanham; contraste verificado no pior caso da cena, não em
  fundo neutro; escala de interface e de texto; foco visível na navegação.
- **Audição:** legenda ou indicador visual para toda informação que hoje só existe
  no som, incluindo aviso de ameaça fora da tela; nomes de quem fala em diálogo;
  o jogo permanece completável com o áudio desligado.
- **Movimento:** redução de movimento desligando tremor de câmera, paralaxe
  agressiva, flashes e transições longas — sem remover o feedback de causa, que
  precisa migrar para um sinal estático equivalente.
- **Tempo e reação:** dificuldade ou assistência que **não** escondem conteúdo,
  velocidade ajustável quando o gênero permite, pausa disponível em qualquer
  momento seguro, e nenhuma exigência de precisão que não tenha alternativa.
- **Leitura:** linguagem clara na primeira instrução, tipografia legível no
  dispositivo alvo, e nenhuma informação crítica apenas em texto pequeno.

Reaproveite o que existe antes de criar sistema paralelo: tokens do design system,
tabela de comandos, camada de legenda do diálogo, opções já presentes no menu.
Uma opção sem consumidor no código não é uma opção.

`access <projeto>` lê as opções que o código declara (highContrast,
reducedMotion, captions, remapeamento, uiScale, preset de uma mão,
assistência, velocidade da partida, tinta estável e região viva). `verified` é sempre falso: chave no fonte não é sessão
com o modo ativo. O starter `canvas-arcade` expõe `assist`, `gameSpeed` e o remapeamento
das seis ações do teclado na página; a tabela `#commands`
nomeia as teclas vigentes e mantém toque e controle no
sufixo. Declara em
`docs/access.md` o que o recorte não atende. O aviso do primeiro ciclo
nomeia teclado (ou o remapeamento vigente), toque e controle juntos.
Estilhaço no trilho pede o dash; toque e controle ganham passo depois
do movimento. Overlay e HUD confirmam o aparelho que falou por último;
o overlay segue `uiScale` e as legendas vencem a cortina no stub. Estilhaço no
x do corpo, no alcance do telegraph, vira `perigo à frente` na região viva
junto da última legenda. A pausa entra como `pausado` — o overlay do canvas
não chega ao leitor. Texto no DOM não é sessão. O harness não joga com o
modo ativo.

Não declare cobertura que não observou. Verificação automática de contraste é útil
e não substitui uma sessão com o modo ativo. Uma lacuna registrada com motivo vale
mais que uma lista de recursos não testados.

Implementação concreta: o starter `canvas-arcade` guarda remapeamento, redução de
movimento e velocidade da partida em `src/core/settings.js`. `gameSpeed` dilata o
acumulador em `src/core/loop.js`; `advance()` headless não passa por ele. Herda a preferência do sistema, preenche
`{pause}`, `{reset}` e `{bank}` em `copy.json` com as teclas vivas, desenha formas
distintas além da cor em `src/game/render.js` e mantém legenda equivalente para
toda informação sonora em `src/game/audio.js`. `npm run contrast` amostra
pixels do stub depois do `draw()` além dos pares hex e, em cinza, conta
o que só o orbe ou só o estilhaço pinta — relata, não aprova,
e não substitui o dispositivo.

Prova: uma sessão completa com cada modo ativado, o jogo terminado sem áudio,
verificação de contraste na cena de pior caso, remapeamento aplicado e
persistido entre execuções, e a declaração explícita do que o jogo ainda não
atende. Degraus:
[barra de acabamento](../references/production-bar.md#accessibility--alcance).
Legibilidade em movimento continua em [visual](visual.md) e [feel](feel.md).
