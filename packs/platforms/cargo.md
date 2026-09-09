# Plataforma — Rust / Cargo (Bevy, macroquad, ggez, Fyrox, wgpu)

Aplicabilidade: `kind: cargo` (`Cargo.toml`). Convenções da plataforma para orientar
leitura e verificação; confirme o motor pelas dependências em `Cargo.toml` e
features habilitadas. Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- `cargo check`, `cargo build`, `cargo test` estão em `context.scripts` e rodam por
  `verify --script`. `cargo run --release` para medir; debug é ordens de grandeza
  mais lento. `cargo clippy` e `cargo fmt --check` por `--command`.
- Testes de integração em `tests/`; em Bevy, `App` headless com `MinimalPlugins`
  para testar sistemas sem janela.

## Ciclo de vida e estado

- Bevy: ECS com schedules (`Startup`, `Update`, `FixedUpdate`), `States` para menu/
  jogo/pausa, `Time`/`Time<Fixed>`, `Res`/`ResMut` como estado global; `run_if` para
  pausar sistemas. Recursos persistem entre estados — fonte comum de estado sobrevivente.
- macroquad/ggez: loop explícito; `get_frame_time`, eventos de janela; pausa é regra
  do jogo, não da biblioteca.
- Descarte: `despawn_recursive`, `Assets::remove`, handles fortes vs fracos; áudio
  (`bevy_audio`/kira) e tarefas assíncronas pendentes.

## Conteúdo e pipeline

- `assets/` com `AssetServer` e loaders; hot reload em dev (`file_watcher`); glTF,
  atlases, RON/TOML para dados. Shaders WGSL. Embedding por `include_bytes!` para
  builds únicos.

## Performance e orçamentos

- Ferramentas: `tracy`/`puffin`, feature `bevy/trace`, `cargo flamegraph`, `perf`.
  Orçamentos: quadro por schedule, alocações (evitar em `Update`), draw calls
  (batching automático depende de material/mesh), memória de assets.
- Preservando arte: instancing, `Visibility` e culling por frustum, LOD manual,
  `Res<Msaa>` conforme alvo, texturas comprimidas (KTX2/Basis).

## Build, plataformas e distribuição

- Nativo por alvo (`--target`), Web via `wasm32-unknown-unknown` + `trunk`/`wasm-bindgen`
  (sem threads por padrão, áudio exige gesto), mobile via `cargo-apk`/`xcodebuild`.
  Perfil `release` com LTO e `opt-level` apropriado; `panic = "abort"` em web.

## O que o harness faz aqui

- `discover` reconhece `Cargo.toml` e ignora `target/`; `verify --script check|build|test`
  funciona sem configuração; `record` guarda medições e observações.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [arquitetura](../../recipes/architecture.md),
[produção](../../recipes/production.md).
