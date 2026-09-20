---
tipo: ludema
ano: 
studio: 
genero: []
hub: false
status: semente
tags:
  - tipo/ludema
---
# {{title}}

> Unidade pequena de design que viaja entre jogos: um contrato com o jogador, não um tema.

Só nasce quando **dois ou mais jogos** o carregam.

## Recebeu de

| De | Relação | O que passou | Evidência | Confiança |
|---|---|---|---|---|

## Invariante

O contrato sem o qual deixa de ser este ludema. Uma ou duas linhas, no imperativo do
jogador. Aqui não entra número: é estrutural.

## Observado (n=)

Regularidade vista nos jogos que o carregam, cada linha com o `n` que a sustenta.
Com `n=1` ou `n=2` é hipótese, não regra: não cobre um jogo nosso por ela.

- … (`n=`)

## Notas

- Quem carrega: veja os backlinks (linhas `carrega` nas notas dos jogos).
- O que muda quando viaja: 

## Quem carrega

Lista viva: jogos cuja tabela *Recebeu de* aponta este ludema, e padrões que o citam.

```base
filters:
  or:
    - file.inFolder("genealogia-jogos/nos/jogos")
    - file.inFolder("padroes")
properties:
  file.name:
    displayName: Nó
views:
  - type: table
    name: Jogos que carregam
    filters:
      and:
        - file.inFolder("genealogia-jogos/nos/jogos")
        - file.hasLink(this.file)
    order:
      - file.name
      - ano
      - estagio
      - studio
  - type: table
    name: Padrões ligados
    filters:
      and:
        - file.inFolder("padroes")
        - ludemas.contains(this)
    order:
      - file.name
      - familia
      - resumo
```
