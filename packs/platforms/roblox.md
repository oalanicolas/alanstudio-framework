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

## O que o harness faz aqui

- `discover` reconhece `default.project.json`; `verify` só por `--command`; `record`
  guarda MicroProfiler e observações. Não abre o Studio.

Núcleo: [rede](../../recipes/network.md) (autoridade), [ciclo de vida](../../recipes/lifecycle.md),
[produção](../../recipes/production.md). Gênero comum: [multiplayer competitivo](../genres/multiplayer-competitive.md).
