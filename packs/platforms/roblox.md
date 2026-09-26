# Plataforma — Roblox (Rojo, Luau)

Aplicabilidade: `kind: roblox` (`default.project.json` do Rojo). Convenções da
plataforma para orientar leitura e verificação; places `.rbxl` binários sem Rojo não
são reconhecidos. Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- `rojo build -o build.rbxl` e `rojo serve` para sincronizar com o Studio; ferramentas
  por `aftman`/`rokit` (`rojo`, `selene`, `stylua`, `wally`).
- Testes: TestEZ/Jest-Lua rodando no Studio ou por `run-in-roblox`; `selene` (lint) e
  `luau-analyze`/`luau-lsp` (tipos) rodam sem Studio. Use `verify --command selene src`
  e `verify --command rojo build -o /tmp/build.rbxl`.

## Ciclo de vida e estado

- Cliente/servidor obrigatórios: `ServerScriptService` (autoridade), `StarterPlayerScripts`
  (cliente), `ReplicatedStorage` (compartilhado). `RemoteEvent`/`RemoteFunction` com
  validação no servidor — o cliente é adversário.
- Loop: `RunService.Heartbeat`/`RenderStepped`/`Stepped`; `task.wait`; `Players.PlayerAdded/Removing`.
  `DataStoreService` para persistência (limites de taxa, `UpdateAsync`, retries).
- Reinício: `TeleportService` ou reset de personagem; estado em `ModuleScript` persiste
  no servidor — fonte comum de estado sobrevivente. Descarte: `Connection:Disconnect`,
  `Instance:Destroy`, `Janitor`/`Trove` para agrupar.

## Conteúdo e pipeline

- Assets por `rbxassetid://` (upload via Studio/Open Cloud), `Tarmac` para sync de
  imagens, `wally` para pacotes, Luau com `--!strict`. Streaming (`StreamingEnabled`)
  muda quando instâncias existem no cliente.

## Performance e orçamentos

- Ferramentas: MicroProfiler, Developer Console, `Stats` (Data Send/Receive, memory),
  Script Profiler. Orçamentos: KB/s por jogador, instâncias por região, memória no
  cliente mobile, tempo de `DataStore`.
- Preservando arte: LOD por `StreamingEnabled`, `Debris`, batching de partes, evitar
  `while true do wait()`, mesh LOD automático.

## Build, plataformas e distribuição

- Publicação via Studio ou Open Cloud API; Game Settings (idade, dispositivos, servidores
  privados); monetização e moderação seguem as políticas da plataforma na fonte oficial.

## Porte de jogo de outra engine

Fatos de documentação verificados em 24/09/2026; o traço sem shader continua hipótese.

- Nenhuma engine exporta para o Roblox: experiências rodam só Luau no Studio
  ([Luau](https://create.roblox.com/docs/luau)). Levar um jogo existente é fazer versão
  nativa em projeto separado; atravessam design, balanceamento, arte-fonte e áudio com
  licença que permita o upload.
- Importação: `.fbx`, `.obj` e `.gltf` com PBR, rig, skin e animação
  ([3D Importer](https://create.roblox.com/docs/art/modeling/3d-importer)); malha até
  20.000 triângulos e 4 ossos por vértice
  ([especificações](https://create.roblox.com/docs/art/modeling/specifications));
  textura até 4096×4096.
- Render: sem shader próprio; o pós se limita a Bloom, Blur, ColorCorrection,
  DepthOfField, SunRays e ColorGrading
  ([pós](https://create.roblox.com/docs/environment/post-processing-effects)). Estilo que
  dependa de shader (traço, hachura, contorno) vai assado na textura (`SurfaceAppearance`),
  com contorno por `Highlight` (até 255 simultâneos no cliente). `EditableImage` pinta em
  tempo real até 1024×1024, exibe uma atualização por quadro e, publicado, exige criador
  verificado 13+ e por identidade. Compare em movimento com a versão aprovada; a versão
  Roblox recebe aprovação visual própria e não redefine o piso do jogo original.
- Agentes: o Studio tem MCP embutido que lê e edita scripts, roda Luau, faz playtest, lê
  a saída, captura a tela e insere assets ([Studio MCP](https://create.roblox.com/docs/studio/mcp));
  o `Roblox/studio-rust-mcp-server` foi descontinuado em abril de 2026. Rojo 7.7 mantém
  o código em arquivos e no Git.
- Caso de origem: série Rabisco do laboratório (24/09/2026), com a variante Roblox do
  Rabisco Fight como primeiro projeto. Invalida: Roblox passar a aceitar shader próprio
  ou código de outra origem.

## O que o harness faz aqui

- `discover` reconhece `default.project.json`; `verify` só por `--command`; `record`
  guarda MicroProfiler e observações. Não abre o Studio.

Núcleo: [rede](../../recipes/network.md) (autoridade), [ciclo de vida](../../recipes/lifecycle.md),
[produção](../../recipes/production.md). Gênero comum: [multiplayer competitivo](../genres/multiplayer-competitive.md).
