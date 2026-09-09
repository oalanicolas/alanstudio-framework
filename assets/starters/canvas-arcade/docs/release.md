# Como entregar o artefato — Canvas Arcade

Runbook vigente. Existe um passo de export e um modo de servir o
resultado. Isso não afirma que outra máquina já executou o `dist/`.
`shipped` no harness continua falso.

## Exportar

```sh
npm run build
```

A árvore jogável sai em `dist/`. Sem testes, sem orçamento, sem o
art-bible. `CREDITS.md` e `public/sfx` entram no artefato.

## Servir o artefato

```sh
cd dist
node tools/serve.mjs
```

Módulos ES não carregam por `file://`. Servir essa pasta é o que a
torna jogável. A prova de `playable` nesta dimensão é outra pessoa
seguindo estes dois blocos numa máquina que não é a de desenvolvimento.

## O que falta para o degrau seguinte

Build reproduzível a partir de uma versão declarada, e verificação no
artefato — não no servidor de desenvolvimento. Este arquivo não
substitui essa prova.
