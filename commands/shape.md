# Shape

Definir a mudança antes de qualquer código: fantasia, verbo central, escala,
plataforma e entrada, cenário, maior incerteza e prova de conclusão. Produz o
**brief da rodada** e para para confirmação. Não escreve código e não gera pasta de
templates; a maior parte dos jogos gerados por IA falha por pensamento pulado, não
por código ruim.

## Escala

`jam`: o brief cabe em cinco linhas ou numa seção de `game-design.md`. `product`:
brief + hipóteses MDA e recorte do GDD, com IDs estáveis. `aa`: o brief declara as
promessas (cinematográfica, rede, idioma) pelas quais o jogo será julgado, porque
o contrato com o jogador acompanha o que o recorte promete. Em qualquer escala a
[escada](../references/ambition.md) é a mesma: fantasia e verbo → ciclo → feel →
áudio → receita → slice → produção.

## Avaliar

Entrevista curta, não formulário. Uma rodada de duas ou três perguntas, com a
ferramenta de pergunta estruturada do host quando houver; segunda rodada só se a
primeira deixou lacuna material. Assuma o que é rotineiro com registro; pergunte só
o que impede de jogar. **Afirme e confirme, não ofereça menu:** quando o brief e o
pedido tornam uma opção óbvia, nomeie-a e peça confirmação.

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

Apresente e **encerre a resposta**. A confirmação do usuário é o portão; não
continue para código na mesma resposta, mesmo que o brief pareça óbvio.

## Verificar

O brief está pronto quando alguém consegue descrever uma partida curta, o que se
pretende sentir e o que precisa ser aprendido primeiro; a referência tem origem e
autoridade declaradas, ou a ausência é explícita (gate `design`,
[gates](../references/gates.md)). Documento preenchido não é PoC executada. Se o shape recusa que documento preenchido seja PoC executada, a área `vision` do `scan` nomeia a executada que o shape já recusa. Documento no disco não é o experimento. Sem chave `executada`.

## Nunca

- Sintetizar um brief completo a partir de uma frase e pedir confirmação em bloco.
- Perguntar o que o brief, o AGENTS ou o código já respondem.
- Pedir paleta, fonte ou nome de asset aqui: isso é [`document`](document.md).
- Transformar aprovação de uma imagem em aprovação de mecânicas que ninguém jogou.
- Prometer no brief o que a escala não vai observar na slice.

## Entregar

O brief confirmado, gravado no canônico com a escala visível, e uma linha dizendo
qual comando o executa: [`craft`](craft.md) para construir agora, ou `--stage poc`
quando a maior incerteza pede um experimento antes.
