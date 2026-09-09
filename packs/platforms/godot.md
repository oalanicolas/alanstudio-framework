# Plataforma — Godot

Aplicabilidade: `kind: godot` (`project.godot`). Convenções da plataforma para
orientar leitura e verificação; confirme a versão (`config/features` em
`project.godot`) e o que o projeto realmente faz. Não substitui AGENTS nem a
documentação oficial.

## Executar e verificar

- Rodar: `godot --path <proj>`; headless: `godot --headless --path <proj>`.
  Importar assets sem abrir o editor: `godot --headless --import`.
- Testes: GUT ou gdUnit4 (addons); por convenção, `godot --headless -s addons/gut/gut_cmdln.gd`
  ou o runner do gdUnit4. Script solto: `godot --headless -s script.gd`.
- Exportar: `godot --headless --export-release <preset> <saida>` com templates
  instalados. Não há CLI padronizada no harness: use `verify --command godot ...`.

## Ciclo de vida e estado

- Nós: `_enter_tree` → `_ready` → `_process(delta)` / `_physics_process(delta)` →
  `_exit_tree`. `_input`/`_unhandled_input` para entrada; `Input` para polling.
- Pausa: `get_tree().paused = true` e `process_mode` por nó (Inherit/Pausable/
  WhenPaused/Always). `Engine.time_scale` para câmera lenta. Foco:
  `NOTIFICATION_APPLICATION_FOCUS_OUT/IN`, `NOTIFICATION_WM_CLOSE_REQUEST`.
- Cenas: `change_scene_to_file`/`change_scene_to_packed`; autoloads (singletons)
  persistem — fonte comum de estado sobrevivente ao reinício.
- Descarte: `queue_free` vs `free`; sinais conectados a nós liberados; `Tween`/
  `Timer` órfãos; `AudioStreamPlayer` em autoload.

## Conteúdo e pipeline

- `.tscn`/`.tres` em texto (diff legível); `.import` e cache em `.godot/`;
  `ResourceLoader.load_threaded_request` para carga assíncrona; `preload` vs `load`.
- Renderizadores: Forward+, Mobile, Compatibility — definem recursos de luz e
  pós-processamento. Escolha é decisão de direção e alvo, registrada no TDD.

## Performance e orçamentos

- Ferramentas: Profiler e Visual Profiler do editor, Monitors (`Performance.get_monitor`),
  `--debug-collisions`, `RenderingServer` stats. Meça no export do alvo.
- Orçamentos típicos: quadro em `_process` e `_physics_process`, objetos/draw calls,
  memória de texturas, contagem de nós, tempo de carga de cena.
- Preservando arte: MultiMesh/instancing, occlusion culling (4.x), LOD/visibility
  ranges, `VisibleOnScreenNotifier`, atlas, compressão de texturas por plataforma.

## Build, plataformas e certificação

- Presets em `export_presets.cfg`; templates por versão; Android/iOS exigem SDKs;
  web usa threads/SharedArrayBuffer conforme configuração. Consoles via parceiros
  oficiais. Requisitos de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `project.godot`; `verify` só por `--command`; `record` guarda
  medições e observações. O harness não lê cenas nem infere autoloads.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[arquitetura](../../recipes/architecture.md), [produção](../../recipes/production.md).
