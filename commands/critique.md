# Critique

Revisar a experiência como diretor de jogo: observar o recorte **em movimento**,
nomear o degrau de cada dimensão pertinente da barra com condição e autor, encontrar
o piso, triar achados por severidade e persistir a leitura por recibo. Não há nota:
o degrau percebido é o mínimo entre as dimensões, e nada aqui certifica.

Referências: [barra de acabamento](../references/production-bar.md),
[protocolo de observação](../references/quality.md),
[checklist de piso](../references/aaa-checklist.md), [arquétipos](../references/personas.md).

## Escala

`jam`: observe o **núcleo** do `finish` (verbo, feel, áudio, estado) e marque o
resto como fora da escala com motivo. `product`: núcleo + produto (câmera, mundo,
HUD, receita, QA). `aa`: promessas declaradas no brief entram na revisão, na slice,
antes de multiplicar conteúdo.

## Avaliar

1. Resolva **um** alvo estável: o jogo inteiro é vago; o recorte é uma cena, um
   verbo, um fluxo (primeira partida, travessia, chefe). `context <projeto> --focus
   <foco>`: `production_bar` diz as dimensões pertinentes; `finish` diz o perfil;
   `bar <projeto>` diz o que o projeto **declara** e onde está o piso declarado.
2. Duas avaliações independentes, que não se contaminam:
   - **A — revisão de experiência:** jogue o recorte com as ferramentas disponíveis
     (navegador, captura, execução real). Para cada dimensão pertinente, o degrau
     observado e a observação que o sustenta. Cinco eixos além da barra: leitura
     do estado em movimento, jornada emocional (pico e fim; onde o jogador é
     traído), carga cognitiva (decisões com mais de quatro opções visíveis ao mesmo
     tempo), [teste de slop de jogo](../references/operations.md#o-teste-de-slop-para-jogos),
     dois ou três arquétipos.
   - **B — evidência técnica:** `verify` nos validadores existentes, recibos e
     `record` anteriores, `gate` e `bar` (forma das declarações), captura do pior
     quadro se houver ferramenta. B é evidência de defeito; nunca prova de acerto.
   Termine A antes de ler B; B ancora o julgamento.
3. Cada achado é **achado, não impressão**: problema, evidência, hipótese, medição.
   O que não nomeia os quatro entra como impressão ou relato, preservado com autoria.
   O agente investiga e estrutura o que puder sustentar; não exige esses campos de
   quem diz “está confuso” e não inventa medição para completar o registro.

## Executar

Sintetize as duas avaliações no registro existente. Use a extensão pertinente ao
recorte; não preencha linhas ou invente achados só para completar um relatório:

- **Leitura da barra:** tabela com uma linha por dimensão pertinente — degrau
  observado, condição (dispositivo, versão, cena, quem), o que sustenta, e a
  distância para a declaração do projeto. **O piso** nomeado em uma frase.
- **Veredito de slop:** o jogo parece feito por IA à primeira vista? Onde
  (placeholder que ficou, juice genérico fora do quadro, tutorial em mural,
  título novo sobre verbo velho). Direto, sem suavizar.
- **O que funciona** (dois ou três pontos concretos).
- **Achados prioritários** (até cinco quando houver), cada um com severidade: P0 impede jogar
  ou trai o jogador (save corrompe, ação sem resposta); P1 quebra o verbo ou a
  leitura; P2 incômodo com contorno; P3 acabamento. Para cada: o quê, por que
  importa ao jogador, correção concreta, **comando sugerido**
  (`feel`, `audio`, `juice`, `clarify`, `onboard`, `harden`, `optimize`,
  `adapt`, `visual`, `content`, `distill`, `polish`).
- **Bandeiras por arquétipo:** o elemento exato que quebrou para Nina, Rafa, Sam,
  Bia ou Léo.
- **Perguntas provocativas:** "e se a ação central fosse a única?", "isto precisa
  de HUD?".

## Verificar

Persista: `record <projeto> --kind observation --author <quem> --field role=agent
--field scenario=<recorte> --note <resumo> --attach <captura>` em pasta inédita; e,
se a leitura discorda da tabela de degraus declarada, proponha a linha corrigida no
documento (não a edite como se fosse observação humana). Compare com o `record`
anterior do mesmo recorte quando existir: é a tendência. Avaliação do agente é
`role=agent`; só [`playtest`](playtest.md) produz `role=human`.

## Nunca

- Somar dimensões numa nota, fazer média ou compensar feel fraco com arte forte.
- Declarar degrau sem condição e autor; degrau sem condição é opinião.
- Marcar "observado" com screenshot, typecheck ou opinião: feel, animação, câmera,
  mix e pacing exigem movimento.
- Deixar o detector técnico (testes, lint) provar que a experiência está boa.
- Inventar CHK-12/13/16 ou "quase AAA" com o núcleo em `não executado`.

## Entregar

Apresente o diagnóstico principal, o que funciona, a evidência e uma próxima ação
recomendada, explicando o efeito no jogo. Ligue o registro detalhado e a tendência
quando houver comparação válida; mostre o relatório completo se ele for pedido.
Pergunte apenas pela intenção ou escolha material que continuar ambígua, sem
transferir a priorização do backlog ao criador. Revisão isolada não autoriza
correção; se o pedido já inclui melhorar o recorte, execute o autorizado e verifique.
[`polish`](polish.md) entra quando houver uma fatia pronta para acabamento.
