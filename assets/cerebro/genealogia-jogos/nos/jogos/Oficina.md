---
tipo: jogo
ano: 2026
studio:
genero:
  - puzzle
hub: false
status: semente
projeto: games/oficina
estagio: semente
categoria: puzzle
tags:
  - tipo/jogo
  - nosso
entradas: 3
saidas: 0
melhor_confianca: A
pendentes: 1
---
# Oficina

> Jogo **nosso** de exemplo deste kit: encaixar peças no caderno. Substitua pelo seu jogo.

## Recebeu de

| De | Relação | O que passou | Evidência | Confiança |
|---|---|---|---|---|
| [[Hexa Drop]] | inspirou | anel que some no lugar da linha | [[Hexa Drop — postmortem]] | A |
| [[Peça que encaixa]] | carrega | peça cai, encaixa ou pune | [[Oficina — o anel que chegou tarde]] | A |
| [[Cai-Cai]] | parece | crítico aponta queda-e-some | [[Cai-Cai — recensão]] | D |

## Notas

- Pasta: `games/oficina` (não existe neste kit; o campo `projeto:` alimenta `buscar --jogo oficina`).
- A aresta `inspirou` A usa o postmortem de exemplo. Num vault real, a evidência é fala pública do autor.

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
