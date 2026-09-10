# Origem de código e assets — Canvas Arcade

Registro de proveniência. Origem desconhecida permanece desconhecida: não
atribuir licença ou autoria pela localização de um arquivo.

## Código

| Parte | Origem | Condição de uso |
| --- | --- | --- |
| `src/`, `tools/`, `tests/`, `data/`, `index.html` | Starter `canvas-arcade` do Alan Studios Framework, adaptado neste projeto | Mesma licença do framework de origem |
| Dependências de terceiros | Nenhuma | — |

O gerador pseudoaleatório em `src/core/rng.js` implementa `mulberry32`, algoritmo
de domínio público amplamente publicado, e o embaralhamento de bits em
`src/core/hash.js` segue a mesma família de funções. Nenhum dos dois carrega
código de terceiros.

## Imagens e modelos

Nenhum. Toda a apresentação é desenhada em Canvas por `src/game/render.js`.
Ao adicionar arte, registre aqui origem, autor, crédito exigido, condição de
uso, versão e o consumidor no código.

## Áudio

| Parte | Origem | Condição de uso |
| --- | --- | --- |
| `public/sfx/dash.wav` / `dash-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/graze.wav` / `graze-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/collect.wav` / `collect-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/bank.wav` / `bank-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/hit.wav` / `hit-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/over.wav` / `over-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/close.wav` / `close-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/live.wav` / `live-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/stir.wav` / `stir-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |
| `public/sfx/bed.wav` / `bed-b.wav` | design original, `tools/design-sfx.py` | CC0-1.0 |

Recibo por arquivo em `public/sfx/<papel>.credits.txt` e lista em
`public/sfx/sources.json`. Sem samples de terceiros. O harness não
valida a licença — só vê o recibo.

Ao copiar do acervo compartilhado, `sfx copy` grava `sources.json` e um
arquivo de créditos ao lado do som; mantenha os dois e referencie-os
nesta seção. Reuso não concede licença nova.

## Tipografia

`system-ui` e a pilha de fontes do sistema operacional. Nenhuma fonte embarcada.
Ao embarcar uma, verifique se a licença cobre distribuição no formato pretendido.

## Pendências de proveniência

- Nenhuma no estado inicial. Toda adição de asset abre uma linha aqui até que
  origem e condição de uso estejam confirmadas.
