---
tipo: hub
resumo: "Porta do segundo cérebro de jogos: por jogo, por pergunta, padrões, genealogia e o kit replicável."
status: vigente
---
# 00 Comece Aqui

Aqui fica o que atravessou: de quem herdamos, o que medimos, o que aprendemos e o
que se repete. Código de cada jogo fica fora deste vault. Método reutilizável de
*fazer* o jogo pode viver num harness à parte; este cérebro *guarda* o que se
aprendeu. Como contribuir: [[Processo]]. Agentes: [[AGENTS]]. Como copiar:
[[Como replicar]]. Como chegar à densidade de um estúdio: [[Como crescer]].
Método que já vem pronto, sem prova local: [[Métodos herdados]].

As pastas seguem o tipo da nota: `estudos/`, `pesquisas/`, `aprendizados/`,
`planos/`, `identidade/`, `operacao/`, `aulas/`, `registros/`, `evidencias/` e o
grafo em `genealogia-jogos/`. Dados e imagens ficam em `_anexos/`.

## Quatro portas

| Porta | Quando usar |
|---|---|
| **Por jogo**: clique no jogo abaixo | Vou mexer num jogo. O nó mostra de quem ele herda e, na tabela *No cérebro*, tudo daqui que o cita. |
| **Por pergunta**: [[Índice]] | Quero tudo sobre combate, performance, economia, arte… |
| **Padrões**: [[Padrões]] | O que se repete entre estudos e jogos. |
| **Genealogia**: [[Genealogia]] | Quem inspirou quem, com evidência A–D. [[genealogia-jogos/Atlas.base\|Atlas]], [[Mapa de queda]]. |
| **Grafo colorido**: [[Legenda do grafo]] | Cada cor é um tipo de nó. |

Também: [[Catálogo.base|Catálogo]] e
`python3 _sistema/cerebro.py buscar --jogo <pasta>`.

## Nossos jogos

O cartão abaixo lista nós com a tag `nosso`. Neste kit há um jogo de exemplo,
[[Oficina]]. Substitua-o pelo seu.

```base
filters:
  and:
    - file.hasTag("nosso")
formulas:
  imagem: 'if(capa, capa, cor)'
properties:
  file.name:
    displayName: Jogo
  estagio:
    displayName: Estágio
  categoria:
    displayName: Categoria
  jogar:
    displayName: Jogar
views:
  - type: cards
    name: Nossos jogos
    image: formula.imagem
    imageFit: cover
    imageAspectRatio: 1
    cardSize: 180
    order:
      - file.name
      - estagio
      - categoria
      - jogar
    sort:
      - property: file.name
        direction: ASC
  - type: table
    name: Tabela
    order:
      - file.name
      - estagio
      - categoria
      - projeto
      - entradas
      - jogar
```

## Exemplo deste kit

Inventado, só para exercitar o contrato. Não é cânone de produto.

- Referências: [[Hexa Drop]] ([[Byteforge]], [[Lia Costa]]) · [[Cai-Cai]] ([[Kite Works]])
- Nossos jogos: [[Oficina]] · [[Folha em Branco]] (órfão de propósito)
- Ludema: [[Peça que encaixa]]
- Fonte cultural: [[Anel e Centro]] → [[O Anel]]
- Estudos: [[Estudo Hexa Drop]] · [[Estudo Cai-Cai]] · visão [[Máquina de queda]] · pôster [[Mapa de queda]]
- Padrões: [[O tabuleiro pune o encaixe tardio]] (confirmado) · [[O timer não substitui o espaço]] (candidato) · [[Rotular cada afirmação pela origem]] · [[Clonar o que se vê]]
- Fontes: [[Biblioteca de fontes]] · estudos: [[Estudos de referência]]
- Os outros tipos: [[Bases do Obsidian — listas que não envelhecem]] · [[Oficina — primeira noite]] · [[Design de jogos — missão de ensino]] · [[Oficina — três tintas]] · [[Acervo fora do Git]] · [[Oficina — parecer da semente]]

## Ritual curto

1. Capturou algo? Nota nova no Obsidian: cai em `_entrada/` ([[Entrada]]).
2. Terminou um estudo? Passo *Destilar* do [[Processo]]: padrão, ludema ou regra canônica.
3. Uma vez por semana: `cerebro.py check` e `cerebro.py indice`.
4. Quer um vault denso? [[Como crescer]].
