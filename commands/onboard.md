# Onboard

Fazer o primeiro minuto ensinar o verbo sem mural de texto: a primeira ação é
descoberta pelo próprio jogo, há prática antes de combinação de riscos, o primeiro
erro tem causa legível, e latência e stutter são observados nesse trecho real. Use
quando quem nunca viu o jogo trava, abandona ou não entende por que perdeu.

## Escala

`jam`: o primeiro ciclo ensina a ação sem texto obrigatório (`playable`).
`product`: prática antes de combinação, intensidade alternando com recuperação
conforme a intenção declarada (`slice`). `aa`: a curva observada com pessoas que
nunca viram o jogo; abandono e erro repetido investigados, não só contados.

## Avaliar

1. `context <projeto> --focus mechanics` (ou `content` para a ordem das situações).
   Leia a hipótese de pacing no GDD/MDA e a promessa do brief sobre público.
2. Jogue o primeiro minuto como [Nina](../references/personas.md): sem ler nada,
   sem contexto. Anote o segundo em que a primeira ação fica clara, o primeiro
   erro e se a causa era legível **antes** da punição.
3. O primeiro minuto denuncia latência, float e stutter mais do que qualquer
   preset gráfico: observe input, quadro e câmera nesse trecho
   ([qualidade](../references/quality.md)).
4. Pergunte só o que o GDD não diz: qual é a única coisa que o jogador precisa
   aprender para chegar ao momento em que o jogo se prova.

## Executar

Mostre, não conte: a primeira situação pede a ação central e recompensa; a segunda
introduz uma variação; a combinação de riscos vem depois da prática. Texto
contextual, no ponto de uso, dispensável por quem já sabe. Estados vazios e
primeira execução são onboarding: o que vai aparecer aqui, por que importa, como
começar. Tutorial que bloqueia o jogo não é onboarding; pulável sempre. Não crie
"modo tutorial" desligado do jogo real. Regras e recusa: [mecânicas](../recipes/mechanics.md).

## Verificar

Uma pessoa que nunca viu o jogo joga sem narração e entende o que aconteceu
(`playable`); comportamentos observados — hesitação, erro repetido, abandono — em
[`playtest`](playtest.md), com regra de parada. Tempo de sessão não é interesse.
Degraus: dimensão `pacing` na [barra](../references/production-bar.md).

## Nunca

- Mural de texto, sequência de telas ou tutorial obrigatório antes de jogar.
- Explicar o que o jogo poderia ensinar por situação.
- Mostrar a mesma dica de novo depois de dispensada.
- Medir onboarding por conclusão do tutorial em vez de por chegada ao momento que
  prova o jogo.

## Entregar

A sequência das primeiras situações e o que cada uma ensina, a observação do
primeiro minuto (latência, leitura, erro), e o que mudou. Sequência: [`clarify`](clarify.md)
se o problema é leitura do estado; [`feel`](feel.md) se é resposta.
