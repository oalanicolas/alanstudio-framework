# Plataforma — .NET (MonoGame, FNA, Stride, Raylib-cs)

Aplicabilidade: `kind: dotnet` (`*.sln` ou `*.csproj` na raiz, sem marcador Unity/Godot).
Convenções da plataforma para orientar leitura e verificação; confirme o framework
pelas referências do `.csproj`. Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- `dotnet build`, `dotnet run --project <csproj>`, `dotnet test` (xUnit/NUnit/MSTest)
  em projeto de testes separado; lógica de jogo sem `GraphicsDevice` é testável.
- MonoGame: conteúdo compilado pelo MGCB (`dotnet mgcb-editor`/`dotnet mgcb`), pipeline
  em `Content.mgcb`. FNA: assets crus. Stride: editor Game Studio + `dotnet build`.
- Use `verify --command dotnet build` e `verify --command dotnet test`.

## Ciclo de vida e estado

- MonoGame/FNA: `Initialize` → `LoadContent` → `Update(GameTime)` → `Draw(GameTime)`
  → `UnloadContent`. `IsFixedTimeStep`/`TargetElapsedTime` definem o passo;
  `Game.Activated`/`Deactivated` para foco; `IsActive` para pausar.
- Stride: componentes com `Start`/`Update`, `Game.UpdateTime`, cenas assíncronas.
- Reinício: recriar estado; estáticos persistem — fonte comum de estado sobrevivente.
  Descarte: `Dispose` de texturas/efeitos/`SoundEffectInstance`, `ContentManager.Unload`.

## Conteúdo e pipeline

- MGCB: importadores/processadores, `.xnb` por plataforma, compressão de texturas e
  áudio; fontes SpriteFont. FNA usa `Texture2D.FromStream`. Stride: assets no editor.

## Performance e orçamentos

- Ferramentas: dotnet-trace/dotnet-counters, Visual Studio Profiler, PerfView, RenderDoc
  para GPU. Orçamentos: alocações por quadro (GC gen0 pausas), `SpriteBatch` flushes,
  draw calls, memória de texturas, tempo de carga de conteúdo.
- Preservando arte: `SpriteBatch` com `SpriteSortMode.Deferred`/texture atlas, structs
  e pooling, `Span<T>`, instancing em 3D.

## Build, plataformas e distribuição

- `dotnet publish -r <rid> --self-contained`; AOT/trimming com cuidado (reflexão);
  consoles via parceiros (MonoGame/FNA têm caminhos oficiais). Requisitos na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `.sln`/`.csproj` e ignora `bin`, `obj`; `verify` só por
  `--command`; `record` guarda medições e observações.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[produção](../../recipes/production.md).
