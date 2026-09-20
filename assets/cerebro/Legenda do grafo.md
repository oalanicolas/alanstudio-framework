---
tipo: hub
resumo: "Legenda de cores do Graph view: a cor de cada nó diz o que ele é. Gerada por cerebro.py cores."
status: vigente
---
# Legenda do grafo

> Gerada por `python3 _sistema/cerebro.py cores`, que também grava as cores no Graph.
> Para mudar uma cor, edite `CORES` no `cerebro.py` e rode de novo. Contrato: [[Processo]].


## Jogos

| | Nós | Quantos | O que é |
|---|---|---|---|
| <span style="color:#FF3B30;font-size:1.6em">●</span> | **Nossos jogos** | 2 | jogo do estúdio, com pasta em games/, demos/ ou apps/ |
| <span style="color:#FF9500;font-size:1.6em">●</span> | **Jogos de referência** | 2 | jogo de outro estúdio que estudamos ou que influenciou |
| <span style="color:#FFD60A;font-size:1.6em">●</span> | **Ludemas** | 1 | mecânica que viaja entre dois ou mais jogos |

## Cultura e autoria

| | Nós | Quantos | O que é |
|---|---|---|---|
| <span style="color:#A2845E;font-size:1.6em">●</span> | **Estúdios** | 2 | quem desenvolveu |
| <span style="color:#FF8FAB;font-size:1.6em">●</span> | **Pessoas** | 1 | autor, diretor, compositor |
| <span style="color:#BF5AF2;font-size:1.6em">●</span> | **Mitos** | 1 | figura mítica entre o texto-fonte e o jogo |
| <span style="color:#D7B3FF;font-size:1.6em">●</span> | **Obras** | 1 | livro, poema, filme que serviu de fonte |

## Conhecimento

| | Nós | Quantos | O que é |
|---|---|---|---|
| <span style="color:#0A84FF;font-size:1.6em">●</span> | **Estudos** | 3 | dossiê sobre referência externa |
| <span style="color:#64D2FF;font-size:1.6em">●</span> | **Pesquisas** | 1 | método, ferramenta ou tecnologia avaliada |
| <span style="color:#30D158;font-size:1.6em">●</span> | **Aprendizados** | 1 | lição de caso nosso, com prova |
| <span style="color:#B5E48C;font-size:1.6em">●</span> | **Planos** | 1 | PRD, plano, desenho de jogo em estudo |
| <span style="color:#2EC4B6;font-size:1.6em">●</span> | **Visões do grafo** | 3 | recorte curado do grafo |

## Estúdio

| | Nós | Quantos | O que é |
|---|---|---|---|
| <span style="color:#E040FB;font-size:1.6em">●</span> | **Identidade** | 1 | design system, bíblia e referências visuais |
| <span style="color:#FFB4A2;font-size:1.6em">●</span> | **Aulas** | 2 | material de ensino |
| <span style="color:#A3B18A;font-size:1.6em">●</span> | **Operação** | 1 | workspace, acervo, publicação, analytics |

## Prova

| | Nós | Quantos | O que é |
|---|---|---|---|
| <span style="color:#C7C7CC;font-size:1.6em">●</span> | **Registros** | 1 | parecer, resultado, relato, story |
| <span style="color:#636366;font-size:1.6em">●</span> | **Evidências** | 2 | ficha, inventário, fonte organizada |

## Padrões e portas

| | Nós | Quantos | O que é |
|---|---|---|---|
| <span style="color:#FFFFFF;font-size:1.6em">●</span> | **Padrões** | 4 | o que se repete em duas ou mais fontes |
| <span style="color:#5E5CE6;font-size:1.6em">●</span> | **Portas do cérebro** | 11 | Comece Aqui, Padrões, Processo, Genealogia, Legenda |

## Como ler

- **Tamanho** do nó: quantas ligações ele tem. Hubs do grafo ficam grandes.
- **Seta**: direção da ligação. Na genealogia, vai de quem influenciou para quem recebeu.
- Nós em cinza sem cor de grupo: nota sem tipo reconhecido (hoje: 1).
- O Graph esconde o [[Índice]], o `AGENTS` e a `_entrada/`, que linkam tudo e virariam um centro falso.

## Filtros prontos

Cole no campo de busca do Graph view:

| Para ver | Filtro |
|---|---|
| só a genealogia (jogos, ludemas, cultura) | `path:"genealogia-jogos/"` |
| só o conhecimento, sem as fichas de evidência | `-path:"genealogia-jogos/" -path:"evidencias/" -path:"registros/"` |
| o que existe sobre um jogo nosso | abra o nó do jogo e use o *grafo local* (Ctrl/Cmd+P → Open local graph) |
| sem mitos e obras | `-path:"genealogia-jogos/nos/mitos/" -path:"genealogia-jogos/nos/obras/"` |
| só o que é nosso | `tag:#nosso OR path:"planos/" OR path:"aprendizados/" OR path:"identidade/"` |

Depois de mudar as cores com o Obsidian aberto: Cmd/Ctrl+P → *Reload app without saving*. Sem isso, o Obsidian regrava o `graph.json` com o que tem na memória.
