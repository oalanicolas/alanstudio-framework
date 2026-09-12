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
- Na abertura, um prazo que inclui espera por `requestAnimationFrame` deve pausar
  enquanto a página está oculta, preservando o tempo restante. Não substituir a
  pintura final por um timer. Barreiras de imagens devem cobrir os elementos do
  jogo, sem incluir imagens de extensões ou ferramentas inseridas no documento.
  Provar retomada, timeout real em primeiro plano e descarte dos listeners.
- Perda de contexto: `webglcontextlost`/`webglcontextrestored`; recursos de GPU devem
  ser recriáveis. Descarte: remover listeners, cancelar rAF, `dispose()` de geometrias,
  materiais e texturas (three.js/Babylon), fechar `AudioContext`.
- Entrada: Pointer Events unificam mouse/toque/caneta; Gamepad API por polling.
- Desenho UGC: mantenha a proporção do espaço lógico entre editor, miniatura,
  personagem e exportação. CSS responsivo não pode esticar um bitmap com escalas X/Y
  diferentes; adapte o enquadramento ou preserve o aspect-ratio. Meça a proporção
  real do canvas da corrida ao redimensionar. No cenário de lotação máxima, reserve
  espaço para rótulos sem reduzir o personagem a um ícone ilegível. Compare o mesmo
  traço em desktop, celular e corrida cheia. Caso: `games/desnhe-um-cavalo/docs/qa.md`
  no laboratório, 11/09/2026.

### Jogo embutido e troca de versão

Quando uma prévia roda dentro de um host, confira permissões do iframe, origem e
contrato das mensagens na implementação real. Associe respostas à instância,
requisição e revisão correntes; uma resposta atrasada da prévia anterior não pode
editar ou salvar a nova. Valide remetente e payload no consumidor conforme o mecanismo
de isolamento adotado; não transplante um tratamento de origem para outro sandbox.

Distinga armazenamento do jogo, memória de contingência e persistência oferecida pelo
host. Um método chamado save pode apenas reter dados até recarregar. Prove recarga,
troca de versão e indisponibilidade do host nos percursos suportados. Reabrir a prévia
também exige conferir descarte de loops/listeners/recursos e retomada do áudio.

No smoke, escolha uma ação e um resultado próprios do jogo, além de carregamento e
erros. Temporizador andando, canvas alterado, texto com score e nomes de objetos são
sinais parciais; não comprovam interação correta, semântica de cena ou qualidade
artística. Registre versão, cenário, ação e limite da observação. Adaptar essas provas
não exige adotar o runtime do fornecedor. [Origem](../../references/sources.md#autoria-ugc-pública).

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
- Captura de WebGL sem navegador aberto (aprendizado Corrida Rabisco, 2026-09-11): em Mac
  com GPU, `chrome --headless=new --use-angle=metal --remote-debugging-port=0` renderiza o
  pipeline completo (SwiftShader em VM não conclui). `--screenshot` sai antes da cena
  carregar e `--virtual-time-budget` nunca termina com `requestAnimationFrame`; conecte pelo
  DevTools Protocol (`WebSocket` nativo do Node ≥ 22), espere um status da própria página
  informar quadros e só então `Page.captureScreenshot`. Referência:
  `games/corrida-rabisco/scripts/capture-bench.mjs`.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [visual](../../recipes/visual.md),
[feel](../../recipes/feel.md), [produção](../../recipes/production.md).

## Aprendizados de renderização e medição

Extraídos de casos WebGL/WebGPU de setembro de 2026; confirmar no carregador e no
backend instalado. [Origem](../../references/sources.md#aprendizados-de-aplicações).

- Inspecione os objetos após o carregamento. Nomes normalizados, adaptadores de canvas
  e formatos de textura podem diferir do arquivo exportado. Teste com o carregador
  real, contando aberturas e verificando pixels/alpha/energia das texturas resultantes.
- Em portais, cubra todas as aberturas, incluindo portas e frestas; confira a câmera
  refletida e planos oblíquos. A visibilidade da imagem não define quais objetos
  precisam projetar sombra. Cada passagem pode exigir sua própria lista visível.
- Ao compactar instâncias, preserve identidade, matriz, semente de animação e quantidade.
  Passagens que reescrevem listas precisam de buffers independentes; compartilhar
  vértices não implica compartilhar o buffer mutável de instâncias.
- Use margens de deformação coerentes com escala e domínio mundial. Vento em shader
  invalida sombras e bounds mesmo sem mudança da transformação do objeto.
- Ao separar estático/dinâmico, confirme a filtragem equivalente da profundidade.
  Combinar dois resultados filtrados não é automaticamente filtrar um único mapa
  composto. Meça cópias, preenchimento e submissões no backend real.
- Para arma em primeira pessoa, um buffer próprio pode evitar recorte por paredes,
  mas precisa compor profundidade e acabamento do jogo. Compare em espaço livre e
  perto da parede; contabilize textura, profundidade, desenho e redimensionamento.
- Confira DPR e projeção em shaders de partículas. Resolução nativa do renderer não
  basta se o tamanho do ponto ignora esses fatores. Teste distâncias, FOV e densidades.
- Clone de material não comprova independência do grafo de nós/uniforms. Rastreie
  compartilhamento e o construtor real do bundle antes de alterar um recurso herdado.
  Variar intensidade mantendo o conjunto de luzes estável é candidato a medir.
- Uma falha HTTP/cache antes da criação do renderer não demonstra falta de suporte
  gráfico. Isole cache do bundler e use build estável para comparar; registre o backend.
- Métricas RAF e de callback não comprovam quadros apresentados pela GPU. Compare
  também dimensões internas e escala da página; ferramentas e HMR podem alterar ambas.

Persistência, pausa e descarte dos buffers de animação/áudio seguem as receitas de
[conteúdo](../../recipes/content.md), [áudio](../../recipes/audio.md) e
[performance](../../recipes/performance.md).
