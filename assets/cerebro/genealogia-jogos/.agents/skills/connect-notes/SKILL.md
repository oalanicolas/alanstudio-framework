---
name: connect-notes
description: Add typed evidence edges among genealogia-jogos notes. Use when the Graph is sparse, a node is isolated, Recebeu de is empty, or the user asks to connect games, ludemas, or sources without decorative wiki-links.
---

# Conectar notas

O Graph representa influência que dá para explicar. Quantidade de `[[links]]` no prosa não substitui a tabela **Recebeu de**.

## 1. Teste da frase

Antes de ligar: “Esta nota se conecta àquela porque…”. Sem frase específica, não crie.

Prioridade:

1. Mesmo jogo / estúdio / ludema.
2. `carrega` / `origem` (ludema ↔ jogo).
3. Evidência que apoia ou contradiz ([[Biblioteca de fontes]]).
4. Sequência ou linhagem.
5. Visão (`visoes/`) que já recorta o cluster.

## 2. Onde escrever

- Influência: linha na tabela Recebeu de da nota **destino** (ver `genealogia-grafo`).
- Navegação: `[[Nome]]` no prosa só se ajudar a ler.
- Não crie nota vazia para satisfazer um link.
- Não use tag no lugar da aresta.

Duas a cinco arestas por nota, se o conteúdo aguentar. Menos é válido.

## 3. Fechar

```sh
python3 genealogia-jogos/_kit/exportar_grafo.py
```

Informe notas revistas, arestas novas, links quebrados corrigidos, e o que ficou isolado por falta de evidência.
