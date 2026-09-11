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
     tempo), teste de slop de jogo (`SKILL.md`), dois ou três arquétipos.
   - **B — evidência técnica:** `verify` nos validadores existentes, recibos e
     `record` anteriores, `gate` e `bar` (forma das declarações), captura do pior
     quadro se houver ferramenta. B é evidência de defeito; nunca prova de acerto.
   Termine A antes de ler B; B ancora o julgamento.
3. Cada achado é **achado, não impressão**: problema, evidência, hipótese, medição.
   O que não nomeia os quatro entra como impressão.

## Executar

Sintetize as duas avaliações num relatório único, tecido, não concatenado:

- **Leitura da barra:** tabela com uma linha por dimensão pertinente — degrau
  observado, condição (dispositivo, versão, cena, quem), o que sustenta, e a
  distância para a declaração do projeto. **O piso** nomeado em uma frase.
- **Veredito de slop:** o jogo parece feito por IA à primeira vista? Onde
  (placeholder que ficou, juice genérico fora do quadro, tutorial em mural,
  título novo sobre verbo velho). Direto, sem suavizar.
- **O que funciona** (dois ou três pontos concretos).
- **Achados prioritários** (três a cinco), cada um com severidade: P0 impede jogar
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

O relatório inteiro na conversa (não um resumo com link), a linha de tendência
quando houver recibo anterior, o caminho do recibo. Depois, pergunte com base nos
achados — não genericamente: qual área atacar primeiro (duas ou três opções), se
um tom percebido foi intencional, quanto escopo (P0–P1 só, ou tudo). Com as
respostas, uma lista ordenada de comandos, terminando em [`polish`](polish.md).
