# Origem de código e assets — Canvas Arcade

Registro de proveniência. Origem desconhecida permanece desconhecida: não
atribuir licença ou autoria pela localização de um arquivo.

## Código

| Parte | Origem | Condição de uso |
| --- | --- | --- |
| `src/`, `tools/`, `tests/`, `index.html` | Starter `canvas-arcade` do Alan Studios Framework, adaptado neste projeto | Mesma licença do framework de origem |
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

Nenhum arquivo embarcado. Os seis papéis sonoros estão declarados e vazios em
`src/game/audio.js`. O piso do estúdio é gravação licenciada ou design
contemporâneo — 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão.

Ao copiar do acervo compartilhado, `sfx copy` grava `sources.json` e um arquivo
de créditos ao lado do som; mantenha os dois e referencie-os nesta seção.
Reuso não concede licença nova.

## Tipografia

`system-ui` e a pilha de fontes do sistema operacional. Nenhuma fonte embarcada.
Ao embarcar uma, verifique se a licença cobre distribuição no formato pretendido.

## Pendências de proveniência

- Nenhuma no estado inicial. Toda adição de asset abre uma linha aqui até que
  origem e condição de uso estejam confirmadas.
