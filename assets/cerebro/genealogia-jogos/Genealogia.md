---
tags:
  - guia
tipo: hub
resumo: "Porta do grafo de genealogia: tipos de nó, relações, confiança A–D e como adicionar um nó ou uma aresta."
temas:
  - design
  - processo
status: vigente
---
# Genealogia

Um grafo dirigido com regra de evidência. **Uma nota por nó**, arestas tipadas com
"o que atravessou" e confiança. Sem citação pública, a seta é hipótese, não fato.

O vault é esta pasta inteira (porta: [[00 Comece Aqui]]). `genealogia-jogos/` guarda
o grafo. Plugins nativos: Graph, Canvas, Properties, Backlinks, Templates, Bases
(Obsidian 1.9+).

Jogos nossos têm a tag `nosso`, `projeto:` com a pasta do código e a tabela
*No cérebro*. Padrões: [[Padrões]]. Réplica: [[Como replicar]]. Crescer: [[Como crescer]].
Pôster: [[Mapa de queda]].

## Onde está cada coisa

- `nos/` · um arquivo por nó, em pastas por tipo. **Fonte da verdade.**
- `visoes/` · recortes: [[Estudos de referência]], [[Máquina de queda]], [[Biblioteca de fontes]].
- [[Mapa de queda]] · pôster curado do cluster de exemplo (o Graph explora; o canvas argumenta).
- Dossiês longos: `estudos/`, fora desta pasta.
- `Atlas.base` · tabela de todos os nós.
- `_kit/exportar_grafo.py` · valida, grava campos derivados e exporta CSV/DOT.
- `_sistema/modelos/grafo/` · um modelo por tipo, mais *Jogo nosso*.

## Seis tipos de nó

| Pasta | `tipo` | Neste kit |
|---|---|---|
| `nos/jogos` | jogo | [[Hexa Drop]], [[Cai-Cai]], [[Oficina]], [[Folha em Branco]] |
| `nos/ludemas` | ludema | [[Peça que encaixa]] — só nasce com **dois ou mais** jogos, com *Invariante* e *Observado (n=)* |
| `nos/pessoas` | pessoa | [[Lia Costa]] |
| `nos/estudios` | estudio | [[Byteforge]], [[Kite Works]] |
| `nos/mitos` | mito | [[O Anel]] — figura entre o texto-fonte e o jogo |
| `nos/obras` | filme, texto, livro, pintura, album | [[Anel e Centro]] |

## As setas que não podem se misturar

| Relação | Significa | Exige |
|---|---|---|
| `inspirou`, `tom`, `fonte`, `sucessor_espiritual` | o **time citou** | confiança A ou B |
| `linhagem` | desce da mesma árvore de gênero, sem citação | qualquer |
| `parece` | crítico ou jogador sente | qualquer |
| `origem` | jogo → ludema: onde o mecanismo foi formulado | na nota do ludema |
| `carrega` | ludema → jogo: o jogo adota o mecanismo | na nota do jogo |
| `sequencia_de`, `mesmo_studio`, `mesmo_ludem` | estrutura entre jogos | qualquer |
| `autoria`, `desenvolveu`, `integra` | pessoa → obra, estúdio → jogo, pessoa → estúdio | não contam como influência |

## Confiança

| | Fonte |
|---|---|
| **A** | entrevista, postmortem, post do próprio autor ou diretor |
| **B** | post oficial do estúdio, presskit, FAQ, art book, matéria que cita a entrevista |
| **C** | crítico, ensaio, análise interna |
| **D** | "todo mundo fala", veio de conversa, sem fonte |

Cada aresta guarda **o que atravessou**. Sem isso, não crie a linha. Favorito
declarado não é influência.

## Adicionar um nó

1. Nova nota na pasta do tipo, com o modelo certo. Nome do arquivo = nome do nó, sem `:`.
2. Preencha `tipo`, `ano`, `studio`, `genero`, `status` (`semente` até conferir as fontes).
3. Na tabela **Recebeu de**, uma linha por influência **que ele recebeu**.
4. As saídas não se escrevem: aparecem nos backlinks e no `arestas.csv`.
5. `python3 genealogia-jogos/_kit/exportar_grafo.py`.
