---
tipo: ludema
ano: 1991
studio:
genero:
  - puzzle
hub: false
status: semente
tags:
  - tipo/ludema
entradas: 1
saidas: 3
melhor_confianca: A
pendentes: 0
---
# Peça que encaixa

> Unidade pequena de design: a peça cai, encaixa ou pune. Não é um tema.

Só nasce quando **dois ou mais jogos** o carregam. Aqui: [[Hexa Drop]], [[Cai-Cai]]
e [[Oficina]].

## Recebeu de

| De | Relação | O que passou | Evidência | Confiança |
|---|---|---|---|---|
| [[Hexa Drop]] | origem | anel central some ao fechar | [[Hexa Drop — postmortem]] | A |

## Invariante

A peça entra num espaço finito e o espaço que sobra depois dela muda a jogada seguinte.
Sem isso é encaixe decorativo, não este ludema.

## Observado (n=)

- A punição aparece no espaço, não num relógio (`n=2`: [[Hexa Drop]], [[Oficina]]).
- A peça cai por gravidade (`n=2`: [[Hexa Drop]], [[Cai-Cai]]) — hipótese: [[Oficina]]
  a coloca com o cursor e continua carregando o ludema.

## Notas

- Quem carrega: backlinks `carrega` nas notas dos jogos.
- O que muda quando viaja: Hexa Drop pune com o anel; Oficina pune com a linha do caderno.

## Quem carrega

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
