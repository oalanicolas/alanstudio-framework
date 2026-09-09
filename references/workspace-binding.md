# Um harness, vários workspaces

O checkout `alanstudio-framework` é a única fonte do código, recipes, packages,
checklists, templates e testes comuns. O workspace guarda suas regras, jogos,
acervos, ferramentas próprias e provas. Atualizar o checkout central atualiza
imediatamente os arquivos compartilhados usados pelos workspaces ligados a ele.

## Ligação

`framework/core` no workspace é um link para o checkout central. O encaminhador
[game.py](../assets/workspace/game.py) fica em `framework/scripts/game.py` e define
a raiz do laboratório antes de executar o código central. Não contém regras de jogo,
scanner, templates ou validadores próprios. O comando existente continua funcionando:

```sh
python3 framework/scripts/game.py context games/meu-jogo --focus feel
```

O encaminhador usa `GAMES_WORKSPACE_ROOT` somente no processo atual. `--root` explícito
continua disponível. Comandos propostos pelo harness preservam a raiz para poderem
ser executados de outro diretório. Se o checkout estiver ausente, a entrada explica
qual ligação está quebrada; não baixa nem cria outra cópia automaticamente.

Links para `SKILL.md`, `references`, `recipes`, `packs`, `assets` e `examples` podem
preservar os caminhos antigos do workspace. São aliases para os mesmos arquivos.
O destino de `framework/core` é o único endereço da implementação compartilhada.

## Personalização

- `AGENTS.md` e documentos dos jogos: direção, restrições e convenções locais.
- `framework/config.json`: referências adicionais ao contexto, relativas à raiz
  do workspace. O exemplo abaixo não altera o framework compartilhado.
- `framework/evidence/`: recibos e observações locais, vinculados ao código testado.
- Ferramentas locais de catálogo, módulos ou publicação continuam com seus donos.

```json
{
  "version": 1,
  "context_files": ["docs/workflow-criacao-jogos-com-ia.md"]
}
```

`context.workspace` informa os arquivos encontrados e os ausentes. Referência não
localizada permanece uma lacuna; seu conteúdo não é inventado. Caminhos de
personalização precisam permanecer dentro do workspace.

O manifesto opcional `workspace.json` pode declarar módulos com `id` e `path`.
Uma pasta ainda não baixada é relatada como `not_downloaded`; não é preenchida pelo
starter. O helper de download continua no workspace, em `framework/scripts/workspace.py`.

Não copie o núcleo para personalizar um laboratório. Mudanças reutilizáveis pertencem
ao checkout central; exemplos, escolhas e provas específicas pertencem ao workspace.
