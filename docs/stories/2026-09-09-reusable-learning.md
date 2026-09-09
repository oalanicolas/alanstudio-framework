# Conhecimento reutilizável no núcleo, escolhas no laboratório

Status: Ready for Review — implementação e validação concluídas.

A ligação thin eliminava cópias do runtime, mas workflow, métodos técnicos e
ferramentas genéricas ainda ficavam no laboratório. No sentido inverso, o núcleo
impunha preferências de áudio de um criador a todos os workspaces.

- [x] Centralizar o workflow de criação, mantendo o caminho local como link.
- [x] Incorporar as lições de performance, web, Unity, conteúdo e áudio nos canônicos existentes.
- [x] Mover módulos/extração e seus testes para o núcleo; parâmetros e identidades vêm do workspace.
- [x] Incorporar as correções de publicação do laboratório em `a719829` sem perder suas regressões.
- [x] Preservar links e modos na extração; não copiar o destino do checkout compartilhado.
- [x] Configurar escolhas sonoras no laboratório, mantendo o núcleo sem restrição de estética ou autor.
- [x] Exercitar dois workspaces com políticas diferentes e a mesma implementação.
- [x] Definir a extração de novos aprendizados e eliminar instruções comuns duplicadas do laboratório.
- [x] Conferir provas históricas, contextos reais e testes finais nos dois repositórios.

O harness permanece independente da implementação dos jogos. Métodos ganham
condições, contraprovas e limites; números locais não viram promessa de ganho.
As APIs de áudio recebem a política explicitamente, enquanto os comandos usam a
configuração da raiz selecionada. Procedência e integridade continuam obrigatórias.

Validação: 226 testes do núcleo passaram. Pelo encaminhador do laboratório, 226
passaram e cinco testes do acervo opcional foram pulados por sua ausência; essa
suíte inclui a do núcleo. Era Uma Vez passou seus 62 testes na revisão `b085293`.
Contextos de três jogos preservaram comandos e fontes de continuidade; 399 arquivos
de evidência anteriores e o corpo do histórico de performance foram preservados.
Não houve novo playtest nem avaliação artística. Os comandos npm da regra geral
não se aplicam ao harness Python, que não tem package.json na raiz.

A publicação usa a branch `codex/thin-workspace-binding` nos dois repositórios.
O recibo final, os hashes do runtime testado e os logs ficam no laboratório em
`framework/evidence/2026-09-09/reusable-learning/`.

Canônicos: [aprendizados](../../references/learning.md),
[ligação e configuração](../../references/workspace-binding.md),
[workflow](../../references/creative-workflow.md).

Arquivos: `scripts/{workspace,split_workspace,game,audio,sfx_catalog}.py`,
`assets/workspace/game.py`, `tests/{test_workspace,test_workspace_binding,test_audio}.py`,
`recipes/{create,performance,content,audio,feel,production}.md`,
`packs/platforms/{web,unity,pico8}.md`,
`references/{learning,creative-workflow,workspace-binding,process,quality,game-design-system,sources}.md`,
`README.md`, `SKILL.md` e esta story.

No laboratório: `AGENTS.md`, configuração/entrada/aliases em `framework/`, teste
específico do acervo, link do workflow, referência aos canônicos no registro de
performance e provas em `framework/evidence/2026-09-09/reusable-learning/`.
Jogos, decisões e alterações anteriores do laboratório permanecem com seus donos.
