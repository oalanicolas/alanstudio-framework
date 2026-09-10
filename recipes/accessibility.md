# Acessibilidade e alcance

Entrada: a barreira concreta que impede alguém de jogar — entrada, visão, audição,
movimento, leitura ou tempo de reação.

Com tela, a primeira superfície é a porta. O aviso do primeiro ciclo
mora no canvas — fantasia e mover na porta, o resto no campo — e a
região viva nomeia a mesma linha. Sem isto quem não vê a tela só
tinha a tabela, e o convite some `#commands`. Overlay, HUD da abertura, a
legenda e a casca da página também seguem `uiScale`. Os knobs da casca
vestem o look e têm foco visível. O canvas continua no
desenho. A porta lê a legenda que o mixer ainda guarda.
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
  o jogo permanece completável com o áudio desligado. No starter a coleta e a
  guarda sobem de tom com a corrente; a legenda nomeia essa aposta. Número
  na faixa não é sessão observada.
- **Movimento:** redução de movimento desligando tremor de câmera, paralaxe
  agressiva, flashes e transições longas — sem remover o feedback de causa, que
  precisa migrar para um sinal estático equivalente. No starter o pulso do
  aparelho também some com `reducedMotion` e com a pausa. O controle que some
  senta o relógio se a sessão falou no pad. Pulso no disco
  não é sessão no controle.
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
assistência, velocidade da partida, tinta estável, região viva e
pulso no aparelho). `verified` é sempre falso: chave no fonte não é sessão
com o modo ativo. O starter `canvas-arcade` expõe `assist`, `gameSpeed` e o remapeamento
das seis ações do teclado na página; a tabela `#commands`
nomeia as teclas vigentes e mantém toque e controle no
sufixo. Declara em
`docs/access.md` o que o recorte não atende. O aviso do primeiro ciclo
nomeia teclado (ou o remapeamento vigente), toque e controle juntos.
Estilhaço no trilho pede o dash; toque e controle ganham passo depois
do movimento. Overlay e HUD confirmam o aparelho que falou por último.
Na pausa o toque retoma — Esc e P não existem no polegar.
O overlay e a casca da página seguem `uiScale` e as legendas vencem a cortina no stub. Estilhaço no
x do corpo, no alcance do telegraph, vira `perigo à frente` na região viva
junto da última legenda. Na porta o canvas também marca a mostra no
trilho — o mesmo aviso do campo. Texto no DOM não é sessão. A pausa entra como `pausado` só quando o
overlay diz Pausado — no fim a cortina do over vence; na porta a
placa nem nasce. Com a cortina no campo, nomeia o placar e o
recorde que o overlay agora mostra. Jogando sem pausa o número
não entra. No fim a região viva nomeia o placar, o recorde e a
corrente que caiu se o overlay a nomeia; na porta, a última
pontuação e o recorde se o save os tem. Na porta e no fim a
região viva também nomeia o aviso da sessão se o canvas o
mostra. Preferências ilegíveis: o painel avisa; a região viva
nomeia a mesma recuperação na porta e no fim; o canvas da
porta e do fim pinta a mesma linha. A pausa não.
Nomear não é aba fechada. O overlay do canvas não chega ao leitor. Texto no
DOM não é sessão. O harness não joga com o modo ativo.

Não declare cobertura que não observou. Verificação automática de contraste é útil
e não substitui uma sessão com o modo ativo. Uma lacuna registrada com motivo vale
mais que uma lista de recursos não testados.

Implementação concreta: o starter `canvas-arcade` guarda remapeamento, redução de
movimento e velocidade da partida em `src/core/settings.js`. A escuta do remap
come a tecla que escolhe o verbo — Espaço não avança enquanto a pessoa
escolhe. O botão focado também é casca: Espaço ativa o controle
e não avança. Botão no disco não é sessão. `gameSpeed` dilata o
acumulador em `src/core/loop.js` só na partida; a porta e o fim ficam no
relógio cheio. A cama segue o relógio da sessão; coleta e guarda
guardam o tom da aposta. `advance()` headless não passa por ele. `assist` cede queda e
alcance também na mostra da porta; a graça extra fica no campo. `reducedMotion`
na porta trava canvas, toque e aviso vivo na mesma chuva parada. `colorblind`
não esmaga a chuva do look que já separa quente e frio; o par do
padrão é o fallback quando as duas tintas ainda compartilham o eixo.
Herda a preferência do sistema, preenche
`{pause}`, `{reset}` e `{bank}` em `copy.json` com as teclas vivas, desenha formas
distintas além da cor em `src/game/render.js` e mantém legenda equivalente para
toda informação sonora em `src/game/audio.js` — coleta e guarda nomeiam a
corrente que o tom já sobe. A região viva nomeia o aviso do primeiro
ciclo que o canvas já pinta; no fim a linha some. Texto no DOM
não é sessão observada. `npm run contrast` amostra
pixels do stub depois do `draw()` além dos pares hex e, em cinza, conta
o que só o orbe ou só o estilhaço pinta — relata, não aprova,
e não substitui o dispositivo.

Prova: uma sessão completa com cada modo ativado, o jogo terminado sem áudio,
verificação de contraste na cena de pior caso, remapeamento aplicado e
persistido entre execuções, e a declaração explícita do que o jogo ainda não
atende. Degraus:
[barra de acabamento](../references/production-bar.md#accessibility--alcance).
Legibilidade em movimento continua em [visual](visual.md) e [feel](feel.md).
