# Shape

Definir a mudança antes de qualquer código: fantasia, verbo central, escala,
plataforma e entrada, cenário, maior incerteza e prova de conclusão. Produz o
**brief da rodada**. Quando solicitado como planejamento, encerra com o brief e as
decisões ainda abertas; não escreve código nem gera pasta de templates. O preparo
interno de uma construção autorizada segue [`craft`](craft.md).

## Escala

`jam`: o brief cabe em cinco linhas ou numa seção de `game-design.md`. `product`:
brief + hipóteses MDA e recorte do GDD, com IDs estáveis. `aa`: o brief declara as
promessas (cinematográfica, rede, idioma) pelas quais o jogo será julgado, porque
o contrato com o jogador acompanha o que o recorte promete. Em qualquer escala a
[escada](../references/ambition.md) é a mesma: fantasia e verbo → ciclo → feel →
áudio → receita → slice → produção.

## Avaliar

Consulte pedido, decisões aceitas e verdade do projeto antes de perguntar. Para
uma lacuna material, use uma pergunta situada ou até três relacionadas, com a
ferramenta estruturada do host quando houver. Outra rodada só se restar uma escolha
que mude o trabalho. Assuma o que é rotineiro com registro; explique o efeito na
partida, sem pedir termos de design. Uma decisão já dada não exige reconfirmação.
Use os itens abaixo para raciocinar, não para entrevistar sobre tudo:

- **Experiência:** o jogador faz X, decide entre Y e Z, percebe W, para sentir S.
  Quem é o jogador, em que contexto, com que entrada.
- **Conteúdo e faixas:** o que existe em 0, no típico e no máximo (uma sala, dez,
  cem); estados de borda (primeira partida, perda, retomada, save antigo).
- **Direção:** referência aprovada com origem e alcance, ou ausência explícita.
  Anti-referências: o que isto **não** é. Uma frase de cena física para a
  direção audiovisual: onde, com que luz, com que som ao redor, em que humor.
- **Escala e prova:** `jam`/`product`/`aa` e o que precisa ser observável ao
  terminar: cenário, dispositivo, comparação em movimento.
- **Maior incerteza:** a que pode invalidar o recorte; ela define a primeira fatia
  ou uma PoC ([pré-produção](../references/preproduction.md)).
- **Restrições:** engine e versão, orçamento de quadro, dispositivos, licenças,
  o que não pode degradar.

Consulte o [workflow de criação](../references/creative-workflow.md) para o loop
e o [pacote de gênero](../packs/README.md) quando o gênero estiver declarado.

## Executar

Escreva o brief no canônico que existe (brief, `game-design.md` ou seção do GDD),
com o [template](../assets/templates/brief.md) como pergunta, não como forma. Forma
compacta (3–5 itens) quando o pedido é claro; forma completa quando há várias telas,
sistemas ou partes interessadas:

1. Resumo da experiência (duas frases). 2. Verbo central e decisão característica.
3. Direção: referência, anti-referências, cena. 4. Escala e artefatos que ela pede.
5. Estados: primeira partida, perda, pausa, retomada, término. 6. Interação: entrada
por dispositivo, feedback esperado por ação. 7. Conteúdo: famílias e faixas.
8. Leituras recomendadas (receitas e pacotes). 9. Maior incerteza e prova.
10. Perguntas abertas — só as sem padrão razoável; onde escreveria "recomendo X",
decida X.

Apresente o brief, distinguindo decisão aceita, proposta e dúvida. Se ainda faltar
uma escolha material, peça essa escolha. Quando o pedido é apenas `shape` ou
planejamento, **encerre sem código**, inclusive com o brief já confirmado. Quando
a conversa também autoriza construir e as decisões estão resolvidas, retome
`craft` no mesmo turno; o brief não cria uma nova pausa de aprovação.

## Verificar

O brief está pronto quando alguém consegue descrever uma partida curta, o que se
pretende sentir e o que precisa ser aprendido primeiro; a referência tem origem e
autoridade declaradas, ou a ausência é explícita (gate `design`,
[gates](../references/gates.md)). Documento preenchido não é PoC executada.

## Nunca

- Sintetizar um brief completo a partir de uma frase e pedir confirmação em bloco.
- Perguntar o que o brief, o AGENTS ou o código já respondem.
- Pedir paleta, fonte ou nome de asset aqui: isso é [`document`](document.md).
- Transformar aprovação de uma imagem em aprovação de mecânicas que ninguém jogou.
- Prometer no brief o que a escala não vai observar na slice.

## Entregar

O brief no canônico, seu estado de decisão e a próxima ação com o que ela permitirá
experimentar. Recomende uma construção ou uma prova da maior incerteza em linguagem
comum. [`craft`](craft.md) executa o recorte; a pessoa não precisa invocá-lo para
continuar uma construção já autorizada.
