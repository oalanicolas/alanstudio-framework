# Uma implementação compartilhada, personalização no laboratório

Status: implementação e validação concluídas. Publicação na branch `codex/thin-workspace-binding`.

A integração por cópia exigia manter o framework em dois repositórios. O pedido
é manter o harness thin em `alanstudio-framework/` e somente o necessário para
personalizar e operar o laboratório em `games-workspace/`.

- [x] Centralizar código, packages, checklists, templates e testes compartilhados.
- [x] Preservar os recursos úteis da linha do laboratório: inicialização,
  continuidade, revisão de entrega, scanner e correções do catálogo sonoro.
- [x] Substituir as cópias por `framework/core` e aliases para os mesmos arquivos.
- [x] Manter comandos existentes com encaminhador curto e contexto local por configuração.
- [x] Preservar módulos opcionais e impedir que uma pasta pendente seja recriada.
- [x] Validar execução fora da pasta do laboratório e raiz explícita nos comandos sugeridos.
- [x] Conferir testes, compatibilidade com jogos reais, provas históricas e índice Git.

Validação: 208 testes do núcleo passaram. Pelo laboratório, 219 passaram e cinco
do acervo sonoro opcional foram omitidos; essa suíte inclui os mesmos testes do
núcleo. Era Uma Vez manteve seus 62 testes aprovados. Contexto compatível em
Era Uma Vez, Fenda Arcana e Rabisco Boom. Os 383 arquivos de evidência anteriores,
as ferramentas próprias e o índice Git do laboratório permaneceram idênticos.
O diagnóstico confirmou a raiz local, o núcleo central e os atalhos vigentes.
Não existem lint, typecheck ou build na raiz deste harness Python. Não houve
alteração de gameplay nem avaliação artística nesta manutenção.

Contrato: [ligação com workspaces](../../references/workspace-binding.md).
O runtime e os recursos comuns têm uma única implementação. `workspace.py`,
`split_workspace.py`, AGENTS, documentos autorais e evidências permanecem locais.
O checkout central precisa estar acessível; mudanças nele passam a valer nos
workspaces ligados sem uma etapa de sincronização.

Arquivos: `scripts/game.py`, `scripts/audio.py`, `scripts/sfx_catalog.py`,
`assets/workspace/game.py`, `assets/gauntlet.md`, `SKILL.md`, `README.md`,
`references/{workspace-binding,delivery,gauntlet,process,project-audit,sources}.md`,
`tests/{test_game,test_audio,test_lab_integration,test_workspace_binding}.py` e esta story.
No laboratório: ligação/aliases em `framework/`, encaminhador, configuração,
README, AGENTS e registro da integração anterior. As provas ficam em
`games-workspace/framework/evidence/2026-09-09/thin-binding/`.
