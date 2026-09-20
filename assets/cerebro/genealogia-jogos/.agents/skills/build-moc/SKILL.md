---
name: build-moc
description: Create or update a visoes/ map in genealogia-jogos when a cluster of nodes needs a door. Use when five or more notes share a theme, a hub is needed, or 00 Comece Aqui should expose a new area. Does not add folder hierarchy.
---

# Criar uma visão

Porta de entrada, não índice de tudo. Neste vault o mapa é uma nota em `visoes/`, no modelo das existentes ([[Máquina de queda]], [[Estudos de referência]], [[Biblioteca de fontes]]).

## Quando

Pelo menos cinco nós relacionados e uma pergunta de navegação. Com menos, acrescente uma seção numa visão já existente.

## Como

1. Uma frase: para que este recorte existe.
2. 5–15 nós que realmente pertencem.
3. Agrupe por relação (combate, mito, processo), não por pasta.
4. Uma linha de contexto por grupo.
5. Lacunas e perguntas abertas.
6. Link em [[Genealogia]] (e em [[00 Comece Aqui]] só se virar entrada principal do vault).

```markdown
---
tags:
  - visao
---
# Visão · [tema]

Uma frase.

## Nós

- [[Nó]]: papel no recorte.

## Ludemas

- [[Ludema]]

## Lacunas

- O que ainda não tem aresta A/B.
```

Não replique o dossiê das notas. Não crie subpasta. Não liste nó cujo papel você não explica. Depois: `python3 _kit/exportar_grafo.py --check` se houver arestas novas.
