---
name: genealogia-grafo
description: Add or repair a node in the games genealogy graph (genealogia-jogos: nos/, visoes/). Use when creating a jogo, ludema, estudio, pessoa, mito or obra note, adding a Recebeu de edge, running exportar_grafo.py, or promoting a long study into the graph.
---

# Genealogia · grafo

Grafo: `genealogia-jogos` (o vault é a raiz desta pasta). Fonte da verdade: `nos/<tipo>/`. Regras em [[Genealogia]]; contrato do vault em [[Processo]].

## 1. Escolher o tipo

| Tipo | Pasta | Quando |
| --- | --- | --- |
| jogo | `nos/jogos/` | produto jogável |
| ludema | `nos/ludemas/` | contrato que **dois ou mais jogos** carregam |
| estudio | `nos/estudios/` | quem desenvolveu (`studio: "[[Nome]]"`) |
| pessoa | `nos/pessoas/` | autoria |
| mito / obra | `nos/mitos/` / `nos/obras/` | fonte cultural |

Nome do arquivo = nome do nó, sem `:`. Copie `_sistema/modelos/grafo/<Tipo>.md`. Jogo nosso: `Jogo nosso.md` (tag `nosso`, `projeto:`, tabela *No cérebro*).

Estudo longo: `estudos/Estudo <Referência>.md` (modelo `_sistema/modelos/Estudo.md`), partes `estudos/<Referência> — <aspecto>.md`, + uma nota em `visoes/`. Não grave dossiê em `games/<projeto>/docs/`.

## 2. Aresta

Na nota de destino, tabela **Recebeu de**:

`| [[De]] | relação | o que atravessou | evidência (URL ou path) | A–D |`

Relações: `inspirou` (fala pública do time), `sequencia_de`, `sucessor_espiritual`, `linhagem`, `carrega` (ludema → jogo, na nota do **jogo**), `origem` (jogo → ludema, na nota do **ludema**), `fonte`, `autoria`, `parece`, `tom`.

`inspirou` exige confiança A ou B. Sem citação pública: `linhagem` ou `parece` em C/D.

Favorito declarado não vira aresta. Sem “o que atravessou”, não crie a linha.

## 3. Validar

```sh
python3 genealogia-jogos/_kit/exportar_grafo.py
```

`--check` só valida. O script grava `entradas`, `saidas`, `melhor_confianca`, `pendentes` — não edite esses quatro à mão.

## 4. Depois

- Ligar a visão relevante (`visoes/`).
- Fonte nova entra em [[Biblioteca de fontes]] antes da aresta.
- Informar: nó criado, arestas, avisos do script.
