# Alcance — o que este recorte atende

Declaração vigente. Opção no código não é sessão observada.
`verified` no harness continua falso.

## O que o recorte atende

- Contraste alto (`highContrast`) com paleta própria
- Redução de movimento (`reducedMotion`): tremor e piscada viram forma estática
- Legendas para toda informação sonora (`captions`)
- Remapeamento de ações (`bindings`)
- Escala da interface (`uiScale`)
- Preset de uma mão no cluster direito (`oneHand`, IJKL + P/O); o aviso e o overlay nomeiam essas teclas, não as do manifesto
- Assistência que não esconde orbe nem pontuação (`assist`)

## O que o recorte não atende

- Contraste medido no dispositivo e em movimento — `npm run contrast` amostra pixels do stub após `draw()` e relata o par sem limiar; o aparelho alvo não foi observado
- Jogo completável com uma só mão, observado
- Sessão com cada modo ativo, observada
- Leitura em escala de cinza no dispositivo alvo, observada

Esta página não sobe o degrau. Ela impede de fingir que o recorte é completo.
