# Plataforma — C/C++ com CMake (SDL2/SDL3, raylib, SFML, bgfx, motor próprio)

Aplicabilidade: `kind: cpp` (`CMakeLists.txt`). Convenções da plataforma para orientar
leitura e verificação; confirme bibliotecas em `find_package`/`FetchContent` e o alvo
executável. Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- Configurar/compilar: `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build`.
  Presets em `CMakePresets.json` quando existirem (`cmake --preset <nome>`).
- Testes: CTest (`ctest --test-dir build`) com Catch2, doctest ou GoogleTest. Lógica de
  jogo separada da janela é testável sem GPU. Sanitizers (`-fsanitize=address,undefined`)
  em debug pegam uso após liberação e overflow.
- Use `verify --command cmake --build build` e `verify --command ctest --test-dir build`.

## Ciclo de vida e estado

- Loop explícito: eventos (`SDL_PollEvent`, `glfwPollEvents`) → atualizar (passo fixo
  com acumulador) → render → present/swap. Quem possui o relógio é decisão do projeto.
- Pausa e foco: `SDL_EVENT_WINDOW_FOCUS_LOST`/`MINIMIZED`, `glfwSetWindowFocusCallback`;
  áudio por `SDL_PauseAudioDevice`/miniaudio/OpenAL. Limite o `dt` na volta do foco.
- Reinício: reconstruir o estado do jogo; estáticos e singletons persistem — fonte
  comum de estado sobrevivente. Descarte: texturas, buffers, contextos, threads,
  ordem de destruição (`SDL_Quit` por último).

## Conteúdo e pipeline

- Assets em pasta própria copiados no build (`file(COPY)`/`configure_file`) ou
  embutidos; carregadores (stb_image, cgltf, tinygltf, dr_wav); pipeline offline para
  atlas, compressão (KTX2/Basis) e shaders (glslang/shaderc/SPIRV-Cross).

## Performance e orçamentos

- Ferramentas: Tracy, perf/VTune/Instruments, RenderDoc/Nsight/PIX para GPU, valgrind
  massif para memória. Orçamentos: quadro por sistema, alocações por quadro (evitar
  `new` no loop), draw calls, memória de GPU, tempo de carga.
- Preservando arte: batching, instancing, culling, LOD, pooling, SoA/ECS quando o
  volume exigir, threads para carga e áudio.

## Build, plataformas e distribuição

- Toolchains por alvo (MSVC/clang/gcc, Emscripten para web, NDK/Xcode para mobile,
  SDKs de console via parceiro). Empacotamento e requisitos de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `CMakeLists.txt` e ignora `build`, `cmake-build-*`; `verify` só
  por `--command`; `record` guarda medições (Tracy, RenderDoc) e observações.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [arquitetura](../../recipes/architecture.md),
[visual](../../recipes/visual.md), [produção](../../recipes/production.md).
