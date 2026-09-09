# Plataforma — Unity

Aplicabilidade: `kind: unity` (`ProjectSettings/ProjectVersion.txt`). Convenções da
plataforma para orientar leitura e verificação; confirme cada uma no projeto e na
versão do editor declarada. Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- Versão do editor: `ProjectSettings/ProjectVersion.txt`; pacotes: `Packages/manifest.json`.
- Testes: Unity Test Framework (EditMode/PlayMode). Linha de comando, por convenção:
  `<Unity> -batchmode -nographics -quit -projectPath <proj> -runTests -testPlatform EditMode -testResults <xml>`.
  PlayMode em batch pode exigir `-testPlatform PlayMode` e não cobre GPU real.
- Métodos estáticos por `-executeMethod Namespace.Classe.Metodo`; logs por `-logFile`.
- Não há CLI padronizada no harness: use `verify --command <caminho-do-Unity> ...`.

## Ciclo de vida e estado

- Ordem: `Awake` → `OnEnable` → `Start` → `FixedUpdate` (física, passo fixo) →
  `Update` → `LateUpdate` → render → `OnDisable` → `OnDestroy`. Câmera que segue
  alvo físico vai em `LateUpdate` ou usa interpolação do Rigidbody.
- Pausa: `Time.timeScale = 0` para a simulação; `Time.unscaledDeltaTime` para UI.
  `OnApplicationPause`/`OnApplicationFocus` no mobile/desktop. Áudio: `AudioListener.pause`.
- Cenas: `SceneManager.LoadSceneAsync`, aditivas, `DontDestroyOnLoad` — fonte comum
  de estado sobrevivente ao reinício. Estáticos e singletons persistem entre cenas.
- Descarte: `Destroy` vs `DestroyImmediate`, `Addressables.Release`, eventos C#
  desassinados, `Resources.UnloadUnusedAssets`.

## Conteúdo e pipeline

- `Assets/` com `.meta` (GUIDs — não apague); import settings por asset (compressão,
  mipmaps, sprite atlas); Addressables ou Resources para carga dinâmica; prefabs e
  variantes; ScriptableObjects para dados.
- Pipeline de render: Built-in, URP ou HDRP definem shaders, luz e pós-processamento
  disponíveis. Sombras, reflexos e volumetria são decisões de direção, não de FPS.

## Performance e orçamentos

- Ferramentas: Profiler (CPU/GPU/Memory/Rendering), Frame Debugger, Memory Profiler
  (pacote), Profile Analyzer, `Stats` no Game view (só indicativo). Meça no build do
  dispositivo alvo com `Development Build` + `Autoconnect Profiler`.
- Orçamentos típicos: quadro por thread (main/render), alocações por quadro
  (GC.Alloc), draw calls/SetPass, memória de texturas, tempo de carga de cena.
- Preservando arte: SRP Batcher, GPU instancing, static/dynamic batching, LOD Groups,
  occlusion culling, texture streaming, Addressables por cena, pooling.

## Build, plataformas e certificação

- Player Settings por alvo; IL2CPP para consoles/mobile; `BuildPipeline.BuildPlayer`
  em `-executeMethod`; Cloud Build ou CI com licença. Requisitos de loja/console
  (TRC/XR, classificação, privacidade) na fonte oficial da plataforma.

## O que o harness faz aqui

- `discover` reconhece o projeto e ignora `Library`, `Temp`, `Logs`, `UserSettings`.
- `verify` só por `--command`; `record` guarda medições do Profiler e observações.
  O harness não abre o editor nem interpreta `.meta`, cenas ou prefabs.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[arquitetura](../../recipes/architecture.md), [produção](../../recipes/production.md).
