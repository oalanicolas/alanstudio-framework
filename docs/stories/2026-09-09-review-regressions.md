# Corrigir as cinco falhas da revisão pós-merge

Status: Ready for Review.
Origem: revisão da `main` em `bee41e6` e pedido de correção das cinco falhas.

## Critérios de aceite

- [x] O servidor recusa links para arquivos e diretórios externos, preservando links internos.
- [x] URLs malformadas recebem HTTP 400 sem encerrar o servidor.
- [x] O jogo abre com save ou preferências corrompidos quando não há espaço para uma cópia.
- [x] Gravações posteriores preservam o original até que o backup seja confirmado.
- [x] Títulos com aspas, quebras de linha e marcação geram JSON válido e texto HTML seguro.
- [x] O CLI recusa destinos que sejam symlinks, existentes ou pendurados, sem criar arquivos no alvo.
- [x] As suítes completas do framework e do starter passam: 181 testes Python e 89 do starter.
- [x] O orçamento de simulação do starter passa: 20 execuções, 72.000 passos.

## Validação

Regressões exercitadas pelo CLI, pelo servidor HTTP e pelo adaptador de armazenamento
usado pelo jogo. A substituição dos arquivos é preparada antes de criar o projeto.
Também há cobertura para JSON inválido no starter e backup que falha silenciosamente.

O repositório usa unittest do Python e os testes nativos do Node. O starter oferece
`test` e `budget`; não há scripts de lint, typecheck ou build configurados.

## Arquivos

- `scripts/game.py`
- `tests/test_game.py`
- `assets/starters/canvas-arcade/tools/serve.mjs`
- `assets/starters/canvas-arcade/src/core/storage.js`
- `assets/starters/canvas-arcade/src/core/save.js`
- `assets/starters/canvas-arcade/tests/serve.test.mjs`
- `assets/starters/canvas-arcade/tests/save.test.mjs`
- `docs/stories/2026-09-09-review-regressions.md`
