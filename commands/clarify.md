# Clarify

Legibilidade do estado: o jogador sempre sabe onde está, o que o ameaça e o que
pode fazer — em movimento, na resolução e no dispositivo alvo, por silhueta e forma
antes de cor e texto. Cobre também o texto do jogo (instruções, HUD, mensagens de
erro e de fim). Use quando o jogador não entende o que aconteceu.

## Escala

`jam`: estado, ameaça e alternativa identificáveis com o jogo parado (`playable`).
`product`: identificáveis em movimento, por forma (`slice`). `aa`: legíveis em cena
cheia, com o pior contraste suportado, sem áudio e sem ler texto; a interface
desaparece (`shippable`/`flagship`).

## Avaliar

1. `context <projeto> --focus visual` (ou `accessibility`). Leia os tokens de
   silhueta, cor e HUD no design system e a promessa de leitura do GDD.
2. Três testes baratos: captura em movimento da cena mais cheia; a mesma cena em
   **escala de cinza**; uma sessão **muda**. O que sumiu em cada um é o achado.
3. Jogue como [Nina](../references/personas.md): o primeiro erro tinha causa
   legível antes da punição? A alternativa era visível?
4. Texto: cada mensagem diz o que aconteceu e o que fazer, na língua do jogador,
   sem jargão de engine; a mesma coisa tem o mesmo nome em todo lugar.
5. Pergunte só o que a direção não fixa: o que precisa ler em um relance versus o
   que pode exigir atenção.

## Executar

Hierarquia por forma, tamanho e movimento antes de cor e rótulo; ameaça com
silhueta própria; caminho e landmark distinguíveis sem a melhor screenshot; HUD que
mostra só o que decide a próxima ação. Copy: verbo e consequência ("Sem energia:
volte à base"), não código nem "algo deu errado"; recusa distinta de sucesso também
no texto e no som. Receitas: [visual](../recipes/visual.md),
[acessibilidade](../recipes/accessibility.md).

## Verificar

Os três testes repetidos depois da mudança, em movimento, nas mesmas condições;
uma pessoa que não conhece o jogo nomeia estado, ameaça e alternativa olhando a
cena. Degraus: `legibility` na [barra](../references/production-bar.md).

## Nunca

- Resolver leitura com mais texto ou mais HUD.
- Depender de cor sozinha, ou de áudio sozinho.
- Mensagem que nomeia o erro sem dizer o que fazer.
- Testar só na melhor screenshot, parada.
- Usar nomes diferentes para a mesma coisa em telas diferentes.

## Entregar

O que sumia em cada teste e o que mudou, capturas antes/depois em movimento, o
glossário do jogo se houve renome. Sequência: [`onboard`](onboard.md) se o problema
é o primeiro minuto; [`visual`](visual.md) se é a direção.
