---
name: review-vault
description: Audit the genealogia-jogos Obsidian vault for note counts, wiki-links, broken links, isolated notes, and graph export errors. Use for weekly Graph health, navigation diagnosis, or before adding nodes. Does not move or delete files unless the user asks to fix.
---

# Revisar o cofre

Medir sem alterar. Depois, o grafo (`exportar_grafo.py`), não métricas vazias.

## 1. Saúde do vault

O vault é a raiz desta pasta (onde estão `Processo.md` e `_sistema/`). A partir dela:

```sh
python3 _sistema/cerebro.py check
```

Valida metadados, wikilinks (inclusive `\|` em tabelas, `.base` e `.canvas`), links relativos,
nomes repetidos e notas sem link de entrada. Respeita as exclusões de `.obsidian/app.json` e
separa módulos não baixados de links realmente quebrados. Não escreve arquivos.

`scripts/vault_health.py` é a contagem antiga: conta links crus, sem essas regras. Serve só para
comparar números de conexão.

Ordem de leitura: links quebrados → notas sem link de entrada → hubs → Home e Canvas.

Uma nota com muitos links não é automaticamente valiosa. Não force conexões para “melhorar” o número.

## 2. Contrato do grafo

```sh
python3 genealogia-jogos/_kit/exportar_grafo.py --check
```

Avisos de `inspirou` sem fonte A/B e links quebrados na tabela Recebeu de entram no diagnóstico.

## 3. Entregar

- total de notas e wikilinks
- links quebrados
- isoladas / fracas
- hubs (e se batem com `hub: true`)
- avisos do export
- três melhorias, com benefício em português

Se o pedido for só revisão, não edite. Se for correção, só arquivos deste cofre; depois rode os dois comandos de novo.
