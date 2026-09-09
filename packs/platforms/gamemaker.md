# Plataforma — GameMaker

Aplicabilidade: `kind: gamemaker` (`*.yyp`). Convenções da plataforma para orientar
leitura e verificação; confirme versão do IDE/runtime e alvos de exportação.
Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- Compilação por linha de comando via Igor (ferramenta do IDE), por convenção:
  `Igor -- --project=<yyp> --user=<user> --runtime=<VM|YYC> --target=<alvo> Run|PackageZip`.
  Caminhos e licença variam por instalação.
- Testes: não há runner nativo; testes em rooms dedicadas ou scripts com asserções
  e `show_debug_message`. Use `verify --command` com o caminho do Igor.

## Ciclo de vida e estado

- Eventos: Create → Step (Begin/normal/End) → Draw (GUI separado) → Destroy/Clean Up.
  Rooms: Room Start/End; `room_goto`, `room_restart`, `game_restart`.
- Pausa: `instance_deactivate_all` + desenho congelado, ou variável global de pausa
  checada no Step; `game_set_speed`/delta_time para tempo. Foco: `os_is_paused`,
  eventos de sistema.
- Estado global (variáveis `global.`, instâncias persistentes, rooms persistentes)
  sobrevive a `room_restart` — fonte comum de estado sobrevivente.
- Descarte: `instance_destroy`, `surface_free`, `buffer_delete`, `audio_stop_all`,
  `ds_*_destroy`, `time_source_destroy`.

## Conteúdo e pipeline

- Sprites, tilesets, sequences, shaders GLSL ES/HLSL; texture pages e groups
  definem batching. Recursos em `.yy` JSON (diff legível).

## Performance e orçamentos

- Ferramentas: Debugger com profiler, `show_debug_overlay`, `fps_real`. Orçamentos:
  swaps de textura, draw calls (`gpu_get_*`), instâncias ativas, memória de superfícies.
- Preservando arte: texture groups por room, `vertex_buffer`, culling por câmera,
  YYC para CPU-bound.

## Build, plataformas e distribuição

- Alvos: Windows, macOS, Linux, HTML5, Android, iOS, consoles (licença). Requisitos
  de loja/console na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `*.yyp`; `verify` só por `--command`; `record` guarda medições
  e observações. Não lê `.yy` nem rooms.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[produção](../../recipes/production.md).
