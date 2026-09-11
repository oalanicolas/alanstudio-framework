# Acessibilidade e alcance

Entrada: a barreira concreta que impede alguém de jogar — entrada, visão, audição,
movimento, leitura ou tempo de reação.

Com tela, a primeira superfície é a porta. O aviso do primeiro ciclo
mora no canvas — fantasia e mover na porta, o resto no campo, inclusive
a prática orbe-só enquanto o campo a marca — e a
região viva nomeia a mesma linha. Sem isto quem não vê a tela só
tinha a tabela, e o convite some `#commands`. Overlay, HUD da abertura, a
legenda e a casca da página também seguem `uiScale`. Os knobs da casca
vestem o look e têm foco visível. O canvas continua no
desenho. A porta lê a legenda que o mixer ainda guarda.
Na porta e no fim o canvas nomeia a lacuna do som que o
painel e o live já mostram. A pausa não. Texto no disco
não é mix ouvido.
Sem tela o headless já joga.

Acesso é decisão de design, não camada final. Tratado no GDD, custa uma escolha;
tratado depois do conteúdo pronto, custa retrabalho de arte, UI e regra. Registre
essas opções como requisitos de qualidade no PRD, com forma de verificar.

Examine as barreiras que o jogo realmente cria:

- **Entrada:** remapeamento de todos os comandos, inclusive os de menu; alternativa
  a pressionar e segurar e a apertar repetidamente; sensibilidade e zona morta
  ajustáveis; jogo completável com uma das mãos quando isso for viável no gênero. Mão no disco não é sessão. Se a receita recusa que completar o jogo peça as duas mãos, a opção `one_hand` do `access` nomeia a mão que a receita já recusa. Mão no disco não é sessão. Sem chave `mão`.
- **Visão:** nenhum estado dependente exclusivamente de cor — forma, ícone,
  posição ou texto acompanham. Ícone no disco não é sessão. Se a receita recusa que o estado dependa só da cor, a opção `colorblind` do `access` nomeia o ícone que a receita já recusa. Ícone no disco não é sessão. Sem chave `ícone`. Contraste verificado no pior caso da cena, não em
  fundo neutro. Neutro no disco não é sessão. Se a receita recusa que o fundo neutro seja o pior caso, a opção `high_contrast` do `access` nomeia o neutro que a receita já recusa. Neutro no disco não é sessão. Sem chave `neutro`. Escala de interface e de texto; foco visível na navegação.
- **Audição:** legenda ou indicador visual para toda informação que hoje só existe
  no som, incluindo aviso de ameaça fora da tela; nomes de quem fala em diálogo;
  o jogo permanece completável com o áudio desligado. No starter a coleta e a
  guarda sobem de tom com a corrente; a legenda nomeia essa aposta. Número
  na faixa não é sessão observada.
- **Movimento:** redução de movimento desligando tremor de câmera, paralaxe
  agressiva, flashes e transições longas — sem remover o feedback de causa, que
  precisa migrar para um sinal estático equivalente. Causa no disco não é sessão. Se a receita recusa que o movimento reduzido apague a causa, a opção `reduced_motion` do `access` nomeia a causa que a receita já recusa. Causa no disco não é sessão. Sem chave `causa`. No starter o pulso do
  aparelho também some com `reducedMotion` e com a pausa. O controle que some
  senta o relógio se a sessão falou no pad.   Pulso no disco
  não é sessão no controle. Se a receita recusa que o pulso seja sessão no controle, a opção `haptics` do `access` nomeia o controle que a receita já recusa. Pulso no disco não é sessão. Sem chave `controle`.
- **Tempo e reação:** dificuldade ou assistência que **não** escondem conteúdo,
  velocidade ajustável quando o gênero permite, pausa disponível em qualquer
  momento seguro, e nenhuma exigência de precisão que não tenha alternativa.
- **Leitura:** linguagem clara na primeira instrução, tipografia legível no
  dispositivo alvo, e nenhuma informação crítica apenas em texto pequeno.

Reaproveite o que existe antes de criar sistema paralelo: tokens do design system,
tabela de comandos, camada de legenda do diálogo, opções já presentes no menu.
Uma opção sem consumidor no código não é uma opção. Se a receita recusa que opção sem consumidor seja opção, o `access` nomeia a opção que a receita já recusa. Chave no disco não é alcance. Sem chave `opção`.

`access <projeto>` lê as opções que o código declara (highContrast,
reducedMotion, captions, remapeamento, uiScale, preset de uma mão,
assistência, velocidade da partida, tinta estável, região viva e
pulso no aparelho). Se a casca declara `:focus-visible`, o `access`
nomeia o foco que esta receita já pede. Outline no disco não é
sessão com o teclado. Sem chave `focus`. `verified` é sempre falso: chave no fonte não é sessão
com o modo ativo. O starter `canvas-arcade` expõe `assist`, `gameSpeed` e o remapeamento
das seis ações do teclado na página; a tabela `#commands`
nomeia as teclas vigentes e mantém toque e controle no
sufixo. Se o disco declara `paintCommands`, o `access` nomeia as teclas que a tabela já lista.
Tabela no disco não é sessão. Sem chave `commands`.
Se a porta lê a legenda que o mixer ainda guarda, o `access` nomeia a legenda que a porta já lê. Texto no disco não é sessão. Sem chave `caption`. Se a receita recusa que o número na legenda seja mix, a opção `captions` do `access` nomeia o número que a receita já recusa. Número no disco não é mix. Sem chave `número`. Se a receita recusa que o pulso seja sessão no controle, a opção `haptics` do `access` nomeia o controle que a receita já recusa. Pulso no disco não é sessão. Sem chave `controle`. Se a receita recusa que o botão seja sessão, a opção `remap` do `access` nomeia o botão que a receita já recusa. Botão no disco não é sessão. Sem chave `botão`. Se a receita recusa que o movimento reduzido apague a causa, a opção `reduced_motion` do `access` nomeia a causa que a receita já recusa. Causa no disco não é sessão. Sem chave `causa`. Se a receita recusa que o fundo neutro seja o pior caso, a opção `high_contrast` do `access` nomeia o neutro que a receita já recusa. Neutro no disco não é sessão. Sem chave `neutro`. Se a receita recusa que o estado dependa só da cor, a opção `colorblind` do `access` nomeia o ícone que a receita já recusa. Ícone no disco não é sessão. Sem chave `ícone`. Se a receita recusa que completar o jogo peça as duas mãos, a opção `one_hand` do `access` nomeia a mão que a receita já recusa. Mão no disco não é sessão. Sem chave `mão`. Se a pesquisa recusa que acessibilidade seja gate de certificação, o `access` nomeia a certificação que a pesquisa já recusa. Opção no disco não é certificação. Sem chave `certificação`. Se a receita recusa que opção sem consumidor seja opção, o `access` nomeia a opção que a receita já recusa. Chave no disco não é alcance. Sem chave `opção`.
Declara em
`docs/access.md` o que o recorte não atende. O aviso do primeiro ciclo
nomeia teclado (ou o remapeamento vigente), toque e controle juntos.
A prática orbe-só também ganha passo no campo enquanto o canvas a
marca; a porta não ensina.
Estilhaço no trilho pede o dash; toque e controle ganham passo depois
do movimento. Overlay e HUD confirmam o aparelho que falou por último.
Na pausa o toque retoma — Esc e P não existem no polegar.
No campo o telefone pausa no relógio; o resto da tela
continua o avanço. O relógio nomeia a pausa — sem o ||
o canto calava o verbo e o convite some a tabela. Na
porta o canto continua abrindo.
A placa da pausa nomeia reiniciar; R já saía e o overlay calava.
A região viva espelha continuar e reiniciar — o overlay do canvas
não chega ao leitor.
Na porta o telefone vê Jogar: toque sem ter apertado. Depois da
partida o baixo pede seed nova; o campo repete a última. A região
viva espelha jogar, repetir, seed nova e a abertura do fim — o
overlay do canvas não chega ao leitor. Na porta e no fim a região viva
nomeia a mesa e o look que a chuva já veste — spawn e
normal somem; contrast não é look de arte. Texto no DOM
não é direção observada. O aviso
do primeiro ciclo continua teclado até o gesto. Depois do
tap a porta e o fim não chamam o avanço de cima.
O overlay e a casca da página seguem `uiScale` e as legendas vencem a cortina no stub. Estilhaço no
x do corpo, no alcance do telegraph, vira `perigo à frente` na região viva
junto da última legenda. Se o live anuncia o perigo à frente, o `access` nomeia o perigo que o live já anuncia.
Texto no DOM não é sessão. Sem chave `threat`. Na porta o canvas também marca a mostra no
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
Lacuna de som: o painel avisa; a região viva nomeia a
mesma lacuna na porta e no fim. Catálogo completo não
entra. Nomear o 404 não é mix ouvido.
Nomear não é aba fechada. O overlay do canvas não chega ao leitor. Texto no
DOM não é sessão. O harness não joga com o modo ativo.

Não declare cobertura que não observou. Verificação automática de contraste é útil
e não substitui uma sessão com o modo ativo. Uma lacuna registrada com motivo vale
mais que uma lista de recursos não testados.

Implementação concreta: o starter `canvas-arcade` guarda remapeamento, redução de
movimento e velocidade da partida em `src/core/settings.js`. A escuta do remap
come a tecla que escolhe o verbo — Espaço não avança enquanto a pessoa
escolhe. O botão focado também é casca: Espaço ativa o controle
e não avança. Botão no disco não é sessão. Se a receita recusa que o botão seja sessão, a opção `remap` do `access` nomeia o botão que a receita já recusa. Botão no disco não é sessão. Sem chave `botão`. Se a receita recusa que o movimento reduzido apague a causa, a opção `reduced_motion` do `access` nomeia a causa que a receita já recusa. Causa no disco não é sessão. Sem chave `causa`. `gameSpeed` dilata o
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
e não substitui o dispositivo. Se o `tools/contrast.*` amostra o
stub, o `access` nomeia o contraste. Stub no disco não é
sessão com o modo ativo. Sem chave `contrast`.

Prova: uma sessão completa com cada modo ativado, o jogo terminado sem áudio,
verificação de contraste na cena de pior caso, remapeamento aplicado e
persistido entre execuções, e a declaração explícita do que o jogo ainda não
atende. Degraus:
[barra de acabamento](../references/production-bar.md#accessibility--alcance).
Legibilidade em movimento continua em [visual](visual.md) e [feel](feel.md).
