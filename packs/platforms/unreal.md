# Plataforma — Unreal Engine

Aplicabilidade: `kind: unreal` (`*.uproject`). Convenções da plataforma para orientar
leitura e verificação; confirme versão (`EngineAssociation` no `.uproject`), módulos e
plugins habilitados. Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- Compilar: `Build.bat`/`Build.sh` do engine ou UAT. Por convenção, cook/stage/pak:
  `RunUAT BuildCookRun -project=<uproject> -platform=<Win64|...> -clientconfig=Development -cook -stage -pak -build`.
- Testes: Automation Framework (`UnrealEditor-Cmd <uproject> -ExecCmds="Automation RunTests <Filtro>; Quit" -unattended -nullrhi -log`),
  Functional Tests em mapas, Gauntlet para builds e dispositivos.
- Não há CLI padronizada no harness: use `verify --command <UnrealEditor-Cmd|RunUAT> ...`.

## Ciclo de vida e estado

- Framework: `GameInstance` (persiste entre mapas) → `GameMode`/`GameState`
  (autoridade, regras) → `PlayerController`/`PlayerState` → `Pawn`/`Character`.
  `BeginPlay`/`EndPlay`/`Tick`; `PrimaryActorTick` e grupos de tick definem ordem.
- Pausa: `UGameplayStatics::SetGamePaused`; `SetTickableWhenPaused` para UI/câmera;
  `CustomTimeDilation`/`SetGlobalTimeDilation` para slow-motion. Foco/suspensão do
  app por `FCoreDelegates::ApplicationWillDeactivateDelegate` e correlatos.
- Mundos: level streaming, World Partition, `UGameplayStatics::OpenLevel`; objetos em
  `GameInstance` e subsistemas persistem — fonte de estado sobrevivente.
- Descarte: `Destroy`, timers (`FTimerManager`) e delegates desvinculados, GC por
  `UPROPERTY`; referências cruas a `UObject` não impedem coleta.
- Rede: replicação por propriedade, RPCs (Server/Client/Multicast), autoridade no
  servidor (`HasAuthority`). Cliente não decide resultado.

## Conteúdo e pipeline

- `Content/` com `.uasset`/`.umap` binários (diff só por ferramenta); Data Assets e
  Data Tables para dados; Blueprints e C++ no mesmo projeto. Nanite/Lumen/Virtual
  Shadow Maps mudam orçamento e alvo — decisão de direção registrada no TDD.
- Import de FBX/glTF/USD com escala (cm), materiais por instância, LODs automáticos ou
  Nanite; áudio por MetaSounds ou Wwise/FMOD.

## Performance e orçamentos

- Ferramentas: Unreal Insights, `stat unit`, `stat gpu`, `stat scenerendering`,
  `stat memory`, GPU Visualizer (`ProfileGPU`), Scalability groups.
- Orçamentos típicos: Game/Draw/GPU thread por quadro, draw calls, memória de
  texturas/streaming pool, tempo de carga e hitch por streaming, tráfego por conexão.
- Preservando arte: Nanite/LOD, HLOD, culling por distância, instancing (ISM/HISM),
  streaming de texturas, Scalability por alvo com aprovação da direção.

## Build, plataformas e certificação

- Cook por plataforma, pak/iostore, Project Settings por alvo, DDC compartilhado.
  Consoles exigem SDKs e acesso de parceiro; requisitos de loja/console (TRC/XR,
  classificação, privacidade) na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `*.uproject` e ignora `Binaries`, `Intermediate`, `Saved`,
  `DerivedDataCache`. `verify` só por `--command`; `record` guarda Insights/stat e
  observações. O harness não abre o editor nem lê `.uasset`.

Núcleo: [rede](../../recipes/network.md), [arquitetura](../../recipes/architecture.md),
[visual](../../recipes/visual.md), [produção](../../recipes/production.md).
