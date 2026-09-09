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

## Aprendizados de migração e fidelidade

Derivados de migrações observadas em HDRP no laboratório em setembro de 2026.
São pontos de investigação para a versão instalada, não promessa de equivalência
entre engines. [Origem e limites](../../references/sources.md#aprendizados-de-aplicações).

- Confira configuração serializada, cena reaberta e player. Componentes vivos no
  Editor não comprovam que subassets, referências de lightmap ou materiais foram
  persistidos. Teste perda de vínculo e reconstrução a partir da fonte canônica.
- Variantes e keywords precisam existir no build, inclusive nas contraprovas.
  Referências serializadas e o procedimento de atualização do pipeline devem ser
  verificados antes de atribuir transparência quebrada à arte. Limpar keywords
  indiscriminadamente também pode mudar o resultado.
- Na paridade de render, confronte tonemapping, exposição, orientação HDR, luz ambiente
  difusa, reflexos, resolução efetiva de sombras e filtragem. Alterar albedo para
  esconder uma fonte de iluminação duplicada mascara a causa.
- Valide o receptor final, não só a textura intermediária: pontos, normais, faces do
  material e regiões influenciadas. Um buffer com energia positiva pode não produzir
  a sombra esperada na imagem. Compare seleção de faces e amostragem equivalentes.
- Reflexo planar exige plano, orientação, influência, resolução e mip corretos.
  Intensidade maior não corrige projeção errada. Preserve valores HDR ao reorientar.
- Malhas deformadas na CPU precisam fornecer história por vértice quando o pipeline
  temporal a utiliza. Teste movimento, repouso e várias atualizações no mesmo quadro.
  Vetores de câmera não substituem deformação local; registre custo de arrays e envio.
- Isole shaders/passagens de diagnóstico do desenho normal e confirme a leitura de
  pixels no espaço correto. Zero na entrada deve produzir a contraprova prevista.
- Ao migrar física, preserve escala, unidades, gravidade por domínio, regras de
  repouso e condições iniciais efetivas. Compare trajetórias e ciclo completo de contato;
  posições parecidas em um instante não provam a mesma recuperação.
- Para assets gerados muito grandes, investigue serialização binária por asset antes
  de mudar a configuração global. Compare hashes dos buffers, bounds e identidade
  das referências após salvar, reimportar e reaplicar. Tempo de desserialização não
  é custo de GPU; preserve a prova de que o conteúdo permaneceu idêntico.

As verificações acima complementam os testes do jogo e as comparações em movimento.
Sucesso numérico não substitui correspondência visual nem aprovação artística.
