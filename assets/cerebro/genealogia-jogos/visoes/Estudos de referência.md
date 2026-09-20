---
tags:
  - visao
tipo: visao
resumo: "Porta de todos os estudos de referência: objeto, nosso jogo e pasta."
temas:
  - processo
status: vigente
---
# Visão · Estudos de referência

Todos os dossiês de referência. O grafo continua em `nos/`. A porta de cada estudo
é `estudos/Estudo <Referência>.md`; as partes são `estudos/<Referência> — <aspecto>.md`.

Neste kit: [[Estudo Hexa Drop]] · [[Estudo Cai-Cai]].

```base
filters:
  and:
    - file.inFolder("estudos")
    - parte_de.isEmpty()
properties:
  file.name:
    displayName: Estudo
  referencias:
    displayName: Objeto no grafo
  jogos:
    displayName: Nosso jogo
  data:
    displayName: Data
views:
  - type: table
    name: Estudos
    order:
      - file.name
      - referencias
      - jogos
      - data
```
