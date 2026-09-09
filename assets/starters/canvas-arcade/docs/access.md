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
- Assistência que não esconde orbe nem pontuação (`assist`)

## O que o recorte não atende

- Contraste medido no dispositivo e em movimento — `npm run contrast` amostra pixels do stub após `draw()` e relata o par sem limiar; o aparelho alvo não foi observado
- Jogo completável com uma só mão, observado
- Sessão com cada modo ativo, observada
- Leitura em escala de cinza no dispositivo alvo, observada — `npm run contrast` relata pixels que só o orbe ou só o estilhaço pintam com a mesma tinta no stub; o aparelho não foi observado

Esta página não sobe o degrau. Ela impede de fingir que o recorte é completo.
