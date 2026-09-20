---
tipo: jogo
ano: 
studio: 
genero: []
hub: false
status: semente
projeto: games/<pasta>
estagio: semente
categoria:
tags:
  - tipo/jogo
  - nosso
---
# {{title}}

> O jogo em uma frase: verbo, sessão, onde roda.

## Recebeu de

| De | Relação | O que passou | Evidência | Confiança |
|---|---|---|---|---|

## Notas

- Pasta: `games/<pasta>`.

## No cérebro

Notas do vault sobre este jogo (`jogos` ou `referencias`). IA: `python3 _sistema/cerebro.py buscar --jogo "<pasta>"`.

```base
filters:
  or:
    - jogos.contains(this)
    - referencias.contains(this)
properties:
  file.name:
    displayName: Nota
  resumo:
    displayName: O que tem
  data:
    displayName: Data
views:
  - type: table
    name: Notas sobre este jogo
    groupBy:
      property: note.tipo
      direction: ASC
    order:
      - file.name
      - resumo
      - status
      - data
    sort:
      - property: data
        direction: DESC
```
