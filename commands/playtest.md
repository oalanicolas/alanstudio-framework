# Playtest

Observar pessoas jogando o recorte, com método: cenário, hipótese, regra de parada
declarada antes de começar, achado com evidência e medição, arquétipos como lente,
e recibo com `role=human`. É o único comando que produz observação humana; o que o
agente observa sozinho é [`critique`](critique.md).

Protocolo: [qualidade](../references/quality.md). Arquétipos: [personas](../references/personas.md).
Registro: [template de QA](../assets/templates/qa.md).

## Escala

`jam`: uma pessoa que nunca viu o jogo, uma sessão curta, três perguntas. `product`:
rodadas com regra de parada e a distinção entre tempo de sessão e interesse.
`aa`: as promessas do brief (narrativa, voz, rede) entram no roteiro; o gate
`evaluate` pede método de observação definido.

## Avaliar

1. `context <projeto> --focus mechanics --stage qa`. Leia a hipótese de experiência
   (MDA/GDD), o cenário e a versão exata que será jogada; um build diferente do
   registrado invalida a comparação.
2. Escreva antes da sessão: **cenário e hipótese** (o jogador faz X, esperamos W),
   **condições** (versão, dispositivo, entrada, seed ou variação declarada),
   **referência** (sessão anterior equivalente, se houver), **regra de parada**
   (ex.: N sessões consecutivas sem mudança necessária) — o framework não prescreve
   quantas pessoas, e um método sem regra de parada não está definido.
3. Escolha dois ou três arquétipos para orientar quem convidar e o que observar.
4. Autorização: contato com pessoas, gravação e uso de dados exigem consentimento
   e decisão explícita do usuário; o comando não convida ninguém.

## Executar

Durante: não explique o jogo; anote hesitação, erro repetido, abandono, estratégia,
surpresa, vontade de repetir; o que a pessoa disse e o que ela fez, separados.
Grave em movimento quando autorizado.

Depois, cada **achado** nomeia problema, evidência (momento na gravação, fala,
ação), hipótese de causa e medição (quantas vezes, em quantas sessões). O que não
nomeia os quatro é impressão, e entra como impressão. Ligue cada achado à dimensão
da [barra](../references/production-bar.md) que ele toca: perdeu-se → `legibility`;
não sentiu o impacto → `feel`; não entendeu por que perdeu → `pacing`; perdeu
progresso → `state_trust`.

## Verificar

`record <projeto> --kind observation --author <quem observou> --field role=human
--field scenario=<cenário> --note <achado principal> --attach <gravação> --output
<pasta-nova>`. O recibo guarda HEAD, autor, fato e anexos por SHA-256; não valida
nem aprova. A regra de parada decide se há próxima rodada; contagem de sessões não.

## Nunca

- Registrar teste com pessoa quando houve só simulação ou avaliação do agente
  (critério `human_vs_agent`, não dispensável).
- Confundir tempo de sessão com diversão, ou vitória do próprio agente com equilíbrio.
- Convidar, contatar ou publicar por conta do comando.
- Corrigir durante a sessão para "ver se melhora"; uma variável por vez, depois.
- Inventar regra de parada depois de ver o resultado.

## Entregar

Achados por severidade, ligados às dimensões, com os recibos; a decisão que eles
pedem (manter, ajustar, reformular, investigar); e o comando que ataca o achado
principal. Playtest que contradiz a hipótese devolve ao GDD/MDA — isso é o processo
funcionando.
