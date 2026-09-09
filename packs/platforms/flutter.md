# Plataforma — Flutter / Flame (Dart)

Aplicabilidade: `kind: flutter` (`pubspec.yaml`). Convenções da plataforma para
orientar leitura e verificação; confirme `flame` e `flutter` em `dependencies`.
Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- `flutter run -d <dispositivo>`, `flutter build <apk|ios|web|windows|macos|linux>`,
  `flutter test` (widget e unit), `flutter analyze`. Flame: `flame_test` para testes
  de componentes com `FlameGame` sem render.
- Use `verify --command flutter test` e `verify --command flutter analyze`.

## Ciclo de vida e estado

- Flame: `onLoad` → `update(dt)` → `render(canvas)` → `onRemove`; `Component` tree,
  `HasGameRef`, overlays Flutter para UI. `pauseEngine`/`resumeEngine`,
  `AppLifecycleState` via `WidgetsBindingObserver` para foco/segundo plano.
- Reinício: `removeAll` + `onLoad` ou recriar o `FlameGame`; estado em singletons
  Dart/providers persiste — fonte comum de estado sobrevivente. Descarte: `AudioPool`,
  `Sprite` caches (`Flame.images.clearCache`), timers e streams.

## Conteúdo e pipeline

- `assets/` declarados em `pubspec.yaml`; `Flame.images`/`Flame.audio` (flame_audio);
  sprite sheets/atlas (`SpriteSheet`, `TexturePacker`); Tiled (`flame_tiled`); Rive/
  Lottie para animação vetorial.

## Performance e orçamentos

- Ferramentas: DevTools (Performance overlay, raster/UI thread), `flutter run --profile`,
  Impeller vs Skia por plataforma. Orçamentos: UI e raster thread por quadro, jank,
  memória de imagens, tamanho do app.
- Preservando arte: `SpriteBatch`, atlas, `Picture` cache, evitar rebuild de widgets
  por quadro, `RepaintBoundary` em overlays.

## Build, plataformas e distribuição

- iOS/Android (lojas), web (CanvasKit/WASM), desktop. Assinatura, ícones, permissões
  e políticas de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `pubspec.yaml`; `verify` só por `--command`; `record` guarda
  medições e observações.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[produção](../../recipes/production.md). Gênero comum: [casual](../genres/casual.md).
