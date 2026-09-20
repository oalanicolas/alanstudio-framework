---
tipo: hub
resumo: "Porta dos padrões: o que se repete em duas ou mais fontes, em design, método e armadilhas. Uma nota por padrão em padroes/."
temas:
  - design
  - processo
status: vigente
---
# Padrões

O que o cérebro já viu **mais de uma vez**. Cada padrão é uma nota em `padroes/`,
com família, força (`confirmado` com duas fontes independentes, `candidato` com
uma), os jogos em que age, as evidências e os ludemas. No Graph, os padrões
aparecem em branco ([[Legenda do grafo]]).

Três destinos, sem duplicar:

- **Mecânica que viaja entre jogos** vira ludema no grafo ([[Genealogia]]). O padrão só linka.
- **Método transferível** vira regra canônica; o padrão guarda o caso e `canonico:`.
- **Princípio de design ou de trabalho** que não é nenhum dos dois é um padrão.

Padrão novo: modelo [[_sistema/modelos/Padrão|Padrão]], no passo *Destilar* do
[[Processo]]. Candidato que ganha a segunda fonte muda `forca` para `confirmado`.

Todo padrão declara a **fronteira**: onde a regra deixa de valer. O `check` avisa quando
falta (`SEM_FRONTEIRA`). Em `armadilha`, declare também a instância proibida na forma em
que ela apareceu, e o veto que a originou, se houve.

Neste kit: [[O tabuleiro pune o encaixe tardio]] (design, confirmado) ·
[[O timer não substitui o espaço]] (candidato) · [[Rotular cada afirmação pela origem]]
(método) · [[Clonar o que se vê]] (armadilha).

Regra de método que chegou **sem prova neste vault** não é padrão: fica em
[[Métodos herdados]] e só desce para `padroes/` quando a sua segunda fonte aparecer.

```base
filters:
  and:
    - file.inFolder("padroes")
    - forca == "confirmado"
properties:
  file.name:
    displayName: Padrão
  resumo:
    displayName: O que diz
  jogos:
    displayName: Nossos jogos
  ludemas:
    displayName: Ludemas
views:
  - type: table
    name: Confirmados
    groupBy:
      property: note.familia
      direction: ASC
    order:
      - file.name
      - resumo
      - jogos
      - ludemas
```

## Candidatos

```base
filters:
  and:
    - file.inFolder("padroes")
    - forca == "candidato"
properties:
  file.name:
    displayName: Candidato
  resumo:
    displayName: O que diz
  evidencias:
    displayName: Única fonte até agora
views:
  - type: table
    name: Candidatos
    order:
      - file.name
      - evidencias
      - jogos
```

Famílias: `design`, `metodo`, `armadilha`. Agentes:
`python3 _sistema/cerebro.py buscar --tipo padrao`.
