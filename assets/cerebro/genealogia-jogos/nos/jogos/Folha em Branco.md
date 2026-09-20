---
tipo: jogo
ano: 2026
studio:
genero:
  - narrative
hub: false
status: semente
projeto: games/folha-em-branco
estagio: semente
categoria: narrativa
tags:
  - tipo/jogo
  - nosso
entradas: 0
saidas: 0
melhor_confianca: -
pendentes: 0
---
# Folha em Branco

> Segundo jogo **nosso** deste kit, de propósito **órfão**: ainda sem linhagem.

## Recebeu de

Raiz neste vault: nada registrado. Não invente aresta para o Graph ficar bonito.

## Notas

- Pasta: `games/folha-em-branco`. Aparece no Atlas em *Jogos sem linhagem*.
- Quando houver evidência, a primeira aresta entra aqui. Até lá, zero.

## No cérebro

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
```
