# Plataforma — Web (Canvas, WebGL/WebGPU, JavaScript/TypeScript)

Aplicabilidade: `kind: package.json` ou `static-web`. Convenções da plataforma para
orientar leitura e verificação; confirme cada uma no código do projeto. Não substitui
AGENTS, `package.json` nem a documentação oficial dos navegadores e bibliotecas.

## Executar e verificar

- Comandos reais estão em `scripts` do `package.json`; `context.scripts` os lista e
  `verify --script <nome>` os executa com o gerenciador declarado/lockfile.
- Testes de lógica: `node --test`, Vitest ou Jest, conforme o projeto. Testes no
  navegador (input, render, áudio): Playwright ou equivalente; teste unitário não prova
  comportamento no navegador.
- Site estático sem `package.json`: servidor local (`python3 -m http.server`) e
  inspeção manual; registre por `--command`.

## Ciclo de vida e estado

- Loop: `requestAnimationFrame` com delta e passo fixo para simulação, quando o jogo
  precisar de determinismo. Verifique quem possui o relógio.
- Pausa: `visibilitychange`/Page Visibility, `blur`/`focus`; `AudioContext` entra em
  `suspended` e precisa de gesto do usuário para retomar. Aba em segundo plano reduz
  rAF a zero ou poucos Hz.
- Perda de contexto: `webglcontextlost`/`webglcontextrestored`; recursos de GPU devem
  ser recriáveis. Descarte: remover listeners, cancelar rAF, `dispose()` de geometrias,
  materiais e texturas (three.js/Babylon), fechar `AudioContext`.
- Entrada: Pointer Events unificam mouse/toque/caneta; Gamepad API por polling.

## Conteúdo e pipeline

- Assets por `fetch`/`import` com bundler (Vite, esbuild); atlas de sprites, GLTF/GLB
  para 3D (nomes de nós podem mudar na exportação — confira após carregar), áudio
  decodificado por `decodeAudioData`, fontes por `FontFace`.
- Tamanho importa: compressão (Draco/Meshopt/KTX2), lazy loading por cena, cache.

## Performance e orçamentos

- Ferramentas: DevTools Performance (tempo de quadro, long tasks), Memory (heap ao
  longo do tempo), Lighthouse (carregamento), `performance.now()` em pontos de prova,
  `renderer.info` em three.js (draw calls, triângulos).
- Orçamentos típicos a medir: quadro p99 no dispositivo mais fraco alvo, heap após
  N minutos (vazamento), tempo até interativo em rede móvel, tamanho transferido.
- Otimizações que preservam arte: batching/instancing, atlas, culling, LOD, pooling de
  objetos para evitar GC, `OffscreenCanvas`/workers para trabalho pesado.

## Build, plataformas e distribuição

- Build de produção pelo bundler; PWA para instalação; toque e viewport em mobile;
  política de autoplay de áudio; cross-origin para assets externos.
- Lojas web (itch.io, Poki, Newgrounds) e wrappers (Electron, Tauri, Capacitor) têm
  requisitos próprios — consulte a fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `package.json` e `index.html`; `verify --script` cobre os
  scripts declarados; `context.capabilities` procura menções em `game.mjs`,
  `game.test.mjs`, `src/engine/core/loop.js` e `headless/env_server.ts`.
- Não abre navegador, não mede quadro nem heap; registre medições com
  `record --kind budget` e observações com `record --kind observation`.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [visual](../../recipes/visual.md),
[feel](../../recipes/feel.md), [produção](../../recipes/production.md).
