# Plataforma — Lua (LÖVE, Solar2D, PICO-8-like via Lua)

Aplicabilidade: `kind: lua` (`main.lua`). Convenções da plataforma para orientar
leitura e verificação; confirme o runtime (`conf.lua` para LÖVE, `build.settings`
para Solar2D). Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- LÖVE: `love <pasta>` ou `love .`; `conf.lua` define janela, módulos e versão.
  Testes: `busted` ou runner próprio com `lua`/`luajit` para lógica sem gráficos.
- Não há alvo padronizado no harness: use `verify --command love . --test` ou o
  runner adotado.

## Ciclo de vida e estado

- LÖVE: `love.load` → `love.update(dt)` → `love.draw`; callbacks `love.focus`,
  `love.visible`, `love.quit`, `love.resize`. `love.run` customizável para passo fixo.
- Pausa: estado do jogo (máquina de estados com hump/gamestate ou própria);
  `love.audio.pause`. Foco fora → `dt` grande na volta: limite o `dt`.
- Reinício: reconstruir tabelas de estado; globais persistem — fonte comum de estado
  sobrevivente. `love.event.quit("restart")` reinicia o processo.
- Descarte: `Source:stop`, `Canvas:release`, `Image:release`, timers de bibliotecas.

## Conteúdo e pipeline

- `love.graphics.newImage`, quads para atlas, `love.filesystem` com diretório de save
  separado, fontes TTF/BMFont, shaders GLSL. Solar2D: `display.newImageSheet`.

## Performance e orçamentos

- Ferramentas: `love.graphics.getStats` (draw calls, canvases, texturas), `love.timer`,
  `collectgarbage("count")`, `jit.on/off`. Orçamentos: quadro, draw calls, memória Lua.
- Preservando arte: `SpriteBatch`, atlas, `Canvas` para camadas estáticas, pooling.

## Build, plataformas e distribuição

- `.love` (zip) e executáveis fundidos por plataforma; `love.js` para web; Android/iOS
  com projetos oficiais. Solar2D exporta nativamente. Requisitos de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `main.lua`; `verify` só por `--command`; `record` guarda
  medições e observações.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[produção](../../recipes/production.md).
