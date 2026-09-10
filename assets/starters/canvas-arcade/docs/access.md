# Alcance — o que este recorte atende

Declaração vigente. Opção no código não é sessão observada.
`verified` no harness continua falso.

## O que o recorte atende

- Contraste alto (`highContrast`) com paleta própria
- Redução de movimento (`reducedMotion`): tremor e piscada viram forma estática
- Legendas para toda informação sonora (`captions`); a faixa vence a cortina da pausa e do fim no stub — isso não é sessão observada
- Remapeamento de ações (`bindings`); a página expõe as seis ações do teclado e a tabela `#commands` nomeia as teclas vigentes — toque e controle ficam no sufixo e não entram no remap; persistir no stub não é sessão observada
- Escala da interface (`uiScale`); o overlay do fim e da pausa também cresce — isso não é sessão observada
- Preset de uma mão no cluster direito (`oneHand`, IJKL + P/O); o aviso, o overlay e o `cycle.hand` nomeiam essas teclas; no stub o cluster coleta, guarda, pausa e reinicia — isso não é sessão observada
- Toque: arrastar move, faixa de cima avança, faixa de baixo guarda; o `cycle.touch` nomeia o mapa; o stub percorre as três intenções; o aviso do primeiro ciclo nomeia o arraste junto do teclado e do controle e, depois do primeiro toque, o mapa da superfície vira passo — isso não é sessão no aparelho
- Controle: analógico/dpad move, A avança, X guarda, Start pausa, Select reinicia; o `cycle.pad` nomeia o mapa; o stub percorre o verbo e os comandos; o aviso do primeiro ciclo nomeia o analógico e o X junto do teclado e do toque e, depois do primeiro eixo, o mapa da superfície vira passo; overlay e HUD confirmam o mapa quando o controle falou por último — isso não é sessão no aparelho
- Assistência que não esconde orbe nem pontuação (`assist`)
- Velocidade da partida (`gameSpeed`): o relógio anda mais devagar; a assistência continua sendo alcance e queda, não este knob. `advance()` headless não dilata. Isso não é sessão observada

## O que o recorte não atende

- Contraste medido no dispositivo e em movimento — `npm run contrast` amostra pixels do stub após `draw()` e relata o par sem limiar; o aparelho alvo não foi observado
- Jogo completável com uma só mão, observado
- Sessão com cada modo ativo, observada
- Leitura em escala de cinza no dispositivo alvo, observada — `npm run contrast` relata pixels que só o orbe ou só o estilhaço pintam com a mesma tinta no stub; o aparelho não foi observado

Esta página não sobe o degrau. Ela impede de fingir que o recorte é completo.
