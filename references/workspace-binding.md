# Um harness, vários workspaces

O checkout `alanstudio-framework` é a única fonte do código, recipes, packages,
checklists, templates e testes comuns. O workspace guarda suas regras, jogos,
acervos, configuração e provas. Aprendizados e ferramentas reutilizáveis, inclusive
gestão de módulos, pertencem ao núcleo. Atualizar o checkout central atualiza
imediatamente os arquivos compartilhados usados pelos workspaces ligados a ele.

## Ligação

`framework/core` no workspace é um link para o checkout central. O encaminhador
[game.py](../assets/workspace/game.py) fica em `framework/scripts/game.py` e define
a raiz do laboratório antes de executar o script central de mesmo nome. Não contém regras de jogo,
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
- Identidades de repositórios, destinos de publicação, seleção de módulos e
  preferências artísticas continuam locais; a implementação reutilizável fica aqui.

```json
{
  "version": 1,
  "context_files": ["docs/preferencias-do-criador.md"]
}
```

`context.workspace` informa os arquivos encontrados e os ausentes. Referência não
localizada permanece uma lacuna; seu conteúdo não é inventado. Caminhos de
personalização precisam permanecer dentro do workspace.

AGENTS e os documentos de cada jogo continuam sendo localizados automaticamente.
`context_files` pode ser vazio. Use-o somente para referências locais adicionais;
workflow, checklist e aprendizado genérico entram no núcleo, não nessa configuração.

## Módulos

O manifesto opcional `workspace.json` declara módulos com `id` e `path`.
Uma pasta ainda não baixada é relatada como `not_downloaded`; não é preenchida pelo
starter. [workspace.py](../scripts/workspace.py) obtém os módulos selecionados,
incluindo seus pais, e preserva checkouts presentes. [split_workspace.py](../scripts/split_workspace.py)
prepara extrações em pasta nova, com recibo, sem publicar nem alterar o original.

URLs pertencem ao manifesto: `url` por módulo, ou `repository` com nome simples.
Nesse segundo caso, o prefixo vem de `repository_base_url` ou do diretório da URL
`repository` do hub. Nenhum usuário ou organização é fixado no código.

`module_overlays` em `framework/config.json` seleciona arquivos locais usados na
extração; o padrão contém apenas `workspace.json`. Os demais arquivos vêm do commit
de origem. Links preservam modo e destino, sem incorporar seus arquivos externos.
As regras de publicação e módulos escolhidos continuam em `workspace.json`.

Os caminhos locais `scripts/workspace.py`, `scripts/split_workspace.py`,
`scripts/audio.py` e `scripts/sfx_catalog.py` podem apontar para o mesmo encaminhador
`scripts/game.py`. Ele usa o nome da entrada para escolher o script central.
Os testes reutilizáveis também apontam para o núcleo.

## Áudio

Sem configuração, o núcleo aceita estilos e autores diferentes, mantendo validação
de procedência, licença suportada e integridade. Restrições de gosto são opcionais:

```json
{
  "version": 1,
  "context_files": [],
  "audio": {
    "allowed_styles": ["recorded"],
    "excluded_terms": [],
    "excluded_authors": [],
    "min_sample_rate": 44100,
    "min_bits_per_sample": 16
  }
}
```

Listas vazias não restringem estilo ou autoria. Termos e autores são comparados sem
diferença de caixa/acentos; o piso técnico é configurável. A política aparece em
`studio_assets.sfx.policy` e `sfx summary`, e é aplicada na importação, verificação e
exportação. O piso numérico é conferido na importação e verificação; a exportação
preserva bytes e confere estilo, origem e integridade. Um workspace não herda
silenciosamente as preferências de outro.
As APIs Python recebem `policy` explicitamente; os comandos carregam a configuração
da raiz selecionada. `audio.py --root <workspace>` também permite uma raiz explícita.

Não copie o núcleo para personalizar um laboratório. Mudanças reutilizáveis pertencem
ao checkout central; escolhas e provas específicas pertencem ao workspace.
A [extração de aprendizados](learning.md) faz parte do encerramento de uma rodada:
o caso continua local, e a regra transferível passa a servir aos demais jogos.
