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

## UEFN (ilhas do Fortnite)

Fatos verificados em 24/09/2026. Uma ilha não é um projeto Unreal completo.

- Lógica por dispositivos e Verse
  ([Verse no UEFN](https://dev.epicgames.com/documentation/fortnite/programming-with-verse-in-unreal-editor-for-fortnite));
  o editor de materiais não tem o nó Custom (HLSL) e não há Blueprints (fórum da Epic,
  fev/2025). C++ e Blueprints de um projeto UE5 não migram; a ilha é versão nativa.
- Assets: migração a partir de projetos UE 5.1+, com dependências; nem todo tipo é aceito
  e Static Mesh vai até 20 mil vértices
  ([migração](https://dev.epicgames.com/documentation/en-us/fortnite/migrating-assets-from-unreal-engine-to-unreal-editor-for-fortnite)).
  Material de pós num Post Process Volume é suportado, mas nem todo aparelho roda todo
  efeito ([pós](https://dev.epicgames.com/documentation/fortnite/intro-to-postprocessing-in-unreal-editor-for-fortnite));
  material pesado cai para versão simples em aparelho fraco. Teto de 100.000 unidades de
  memória por ilha, que precisa rodar em todas as plataformas do Fortnite
  ([memória](https://dev.epicgames.com/documentation/en-us/fortnite/memory-management-in-unreal-editor-for-fortnite)).
- Personagem: NPCs aceitam malha e animação importadas, com retarget ao esqueleto do
  Fortnite ([NPC Spawner](https://dev.epicgames.com/documentation/en-us/fortnite/using-the-npc-spawner-with-animations-in-unreal-editor-for-fortnite));
  o jogador usa o personagem do Fortnite, sem documentação para trocá-lo (pedidos de fórum
  em 2026). O elenco de um jogo trazido de fora entra como NPC, inimigo e cenário.
- Câmera fixa para visão de cima e lateral; spawners de veículo em Verse.
- UE6: a Epic anunciou em junho de 2026 unir UE5 e UEFN, com Verse e o mesmo projeto
  dentro e fora do Fortnite; Early Access previsto para o fim de 2027 (via imprensa; a
  página oficial recusou leitura automatizada). Nenhuma fonte cita alvo web. Até lá,
  projeto UE5 e ilha são entregas distintas.
- Caso de origem: série Rabisco do laboratório (24/09/2026). Invalida: UEFN aceitar
  personagem próprio do jogador ou a UE6 entregar o projeto único.

## O que o harness faz aqui

- `discover` reconhece `*.uproject` e ignora `Binaries`, `Intermediate`, `Saved`,
  `DerivedDataCache`. `verify` só por `--command`; `record` guarda Insights/stat e
  observações. O harness não abre o editor nem lê `.uasset`.

Núcleo: [rede](../../recipes/network.md), [arquitetura](../../recipes/architecture.md),
[visual](../../recipes/visual.md), [produção](../../recipes/production.md).
