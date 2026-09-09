# Alcance — o que este recorte atende

Declaração vigente. Opção no código não é sessão observada.
`verified` no harness continua falso.

## O que o recorte atende

- Contraste alto (`highContrast`) com paleta própria
- Redução de movimento (`reducedMotion`): tremor e piscada viram forma estática
- Legendas para toda informação sonora (`captions`)
- Remapeamento de ações (`bindings`)
- Escala da interface (`uiScale`)
- Preset de uma mão no cluster direito (`oneHand`, IJKL + P/O); o aviso, o overlay e o `cycle.hand` nomeiam essas teclas; no stub o cluster coleta, guarda, pausa e reinicia — isso não é sessão observada
- Toque: arrastar move, faixa de cima avança, faixa de baixo guarda; o `cycle.touch` nomeia o mapa; o stub percorre as três intenções; o aviso nomeia as faixas quando o toque falou por último — isso não é sessão no aparelho
- Controle: analógico/dpad move, A avança, X guarda, Start pausa, Select reinicia; o `cycle.pad` nomeia o mapa; o stub percorre o verbo e os comandos; o aviso e o overlay nomeiam esse mapa quando o controle falou por último — isso não é sessão no aparelho
- Assistência que não esconde orbe nem pontuação (`assist`)

## O que o recorte não atende

- Contraste medido no dispositivo e em movimento — `npm run contrast` amostra pixels do stub após `draw()` e relata o par sem limiar; o aparelho alvo não foi observado
- Jogo completável com uma só mão, observado
- Sessão com cada modo ativo, observada
- Leitura em escala de cinza no dispositivo alvo, observada — `npm run contrast` relata pixels que só o orbe ou só o estilhaço pintam com a mesma tinta no stub; o aparelho não foi observado

Esta página não sobe o degrau. Ela impede de fingir que o recorte é completo.
