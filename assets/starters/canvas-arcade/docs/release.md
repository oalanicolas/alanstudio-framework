# Como entregar o artefato — Canvas Arcade

Runbook vigente. Existe um passo de export e um modo de servir o
resultado. Isso não afirma que outra máquina já executou o `dist/`.
`shipped` no harness continua falso.

## Exportar

```sh
npm run build
```

A árvore jogável sai em `dist/`. Sem testes, sem orçamento, sem o
art-bible. `CREDITS.md`, `public/sfx` e `VERSION.json` entram no
artefato. `VERSION.json` nomeia a versão e o HEAD; não prova outra
máquina nem reprodução bit a bit.

## Servir o artefato

```sh
cd dist
node tools/serve.mjs
```

Node 20 ou mais novo. Não rode `npm install`: o artefato não tem
dependências. Módulos ES não carregam por `file://`. Servir essa pasta
é o que a torna jogável. O serve anuncia localhost e, se a máquina
tiver outro endereço IPv4, a URL da rede — um endereço alcançável
não é outra máquina tendo corrido o `dist/`. A prova de `playable`
nesta dimensão é outra pessoa seguindo estes dois blocos numa
máquina que não é a de desenvolvimento.

## O que falta para o degrau seguinte

Outra pessoa seguir os dois blocos acima numa máquina que não é a de
desenvolvimento. `VERSION.json`, árvore completa, HEAD atual, `npm run size`
e o teste que serve o `dist/` não substituem essa prova. `shipped` e
`elsewhere` continuam falsos. `ship.incomplete` nomeia VERSION sem jogo;
`ship.stale` nomeia artefato de outro commit.

`npm run size` relata os bytes de `dist/` sem teto. Identidade e
tamanho no disco não são outra máquina.
