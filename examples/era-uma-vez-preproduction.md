# Exemplo compacto — a trilha de João e Maria

**Exemplo de aplicação do framework, não nova direção aprovada para um jogo.**
Mostra como conectar os nove conceitos em um único documento. Nenhuma mecânica
ou arte é alterada por este texto. A hipótese criativa permanece não testada.

## Game Brief

Pergunta de trabalho: o jogador compreende como marcar a trilha e usa essa
informação para decidir o retorno? A fantasia é ser Maria, agir com esperteza
e ajudar os irmãos a voltar. A experiência pretendida combina descoberta e
confiança na própria observação.

Pilares deste recorte: o verbo do conto vira controle; erro permite recuperação;
consequência aparece no cenário. Feel e áudio da marca (pedra que permanece,
migalha que some) fazem parte do ciclo, mesmo neste documento único. Escala:
conto / jam.

## GDD e MDA

**GDD-M01 — Marcar e interpretar a trilha.** O jogador segue, escolhe caminho,
deixa marcas e retorna à noite. A segunda saída introduz migalhas consumidas
pelos pássaros. Essa diferença é parte do conto e deve ser percebida como
consequência.

**MDA-001 — hipótese:** marcas persistentes e leitura das bifurcações permitem
que a pessoa formule e use uma estratégia, produzindo descoberta e confiança.
Alternativa: ela pode avançar por tentativa e erro sem perceber as marcas.

No playtest, observar antes de explicar: a pessoa deixa marcas, identifica o
significado e usa isso para decidir?

## PRD do recorte, como exemplo

- **FR-001 / AC-001:** após marcar com pedra e avançar o tempo, a marca continua
  visível no retorno.
- **FR-002 / AC-002:** migalha não sobrevive ao avanço equivalente.
- **NFR:** o recorte não introduz combate, cronômetro nem vida extra.

## TDD

Reusar o estado do conto e os testes que já distinguem pedra e migalha. CREATE
só entra se o registro atual não representar a marca.

## PoC, vertical slice, MVP, QA

PoC: uma travessia com as duas marcas. Vertical slice: o mesmo trecho no
acabamento pretendido. MVP: o capítulo jogável, não a coleção inteira. QA:
casos técnicos das marcas e observação da estratégia, em separado.

Este exemplo cabe em um documento. Projetos maiores separam as etapas; o
harness carrega só a pedida.
