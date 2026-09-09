# Plataforma — Defold

Aplicabilidade: `kind: defold` (`game.project`). Convenções da plataforma para
orientar leitura e verificação; confirme versão e dependências em `game.project`.
Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- Build por linha de comando com Bob: `java -jar bob.jar --platform <plat> resolve build bundle --archive`
  (a versão do Bob deve coincidir com a do editor). Rodar pelo editor ou `dmengine`.
- Testes: não há runner nativo; bibliotecas como deftest/telescope ou testes headless
  em `dmengine_headless`. Use `verify --command java -jar bob.jar ...`.

## Ciclo de vida e estado

- Scripts: `init` → `update(dt)`/`fixed_update` → `on_message` → `on_input` → `final`.
  Coleções são carregadas por collection proxy (`load`/`enable`/`unload`) ou factory.
- Pausa: `set_time_step` via `@system:` ou `msg.post("@system:", "set_update_frequency")`;
  `window.set_listener` para foco/iconificação. Áudio via `sound.pause`.
- Reinício: recarregar a proxy da coleção; estado em módulos Lua persiste — fonte
  comum de estado sobrevivente.
- Descarte: `go.delete`, `unload` da proxy, `timer.cancel`, mensagens pendentes.

## Conteúdo e pipeline

- Atlases e tilesources; `.collection`/`.go`/`.script` em texto; Live Update para
  conteúdo remoto; extensões nativas via `ext.manifest`.

## Performance e orçamentos

- Ferramentas: profiler visual (`profiler.enable_ui`), web profiler, `sys.get_engine_info`.
  Orçamentos: draw calls, tamanho de atlas, memória Lua/GC, tempo de carga por coleção.
- Preservando arte: atlas por cena, `sprite.set_constant` em vez de materiais novos,
  culling manual, pooling por factory.

## Build, plataformas e distribuição

- HTML5, Android, iOS, desktop, Switch (via parceiro). Requisitos de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `game.project`; `verify` só por `--command`; `record` guarda
  medições e observações. Não interpreta coleções nem mensagens.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[produção](../../recipes/production.md).
