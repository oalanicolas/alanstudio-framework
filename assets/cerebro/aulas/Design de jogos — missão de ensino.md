---
tipo: aula
resumo: "Missão do material de ensino deste kit: o aluno escreve uma hipótese que uma observação pode contrariar."
temas:
  - ensino
  - design
status: vigente
data: 2026-09-19
---
# Design de jogos — missão de ensino

Ensinar o método que o cérebro usa: rótulo de origem, estudo que não é cânone,
tradução em tabela. Exemplo: [[Aula 0001 — o anel não é a linha]].

## Success looks like

- O aluno separa [O], [T] e [I] em voz alta.
- Sai com uma ficha cuja hipótese uma partida pode falsificar.
- Não atribui ao objeto o que o objeto não disse.

## Todas as partes

```base
filters:
  and:
    - parte_de == this
properties:
  file.name:
    displayName: Parte
views:
  - type: table
    name: Aulas
    order:
      - file.name
      - resumo
```
