# Plataforma — Python (Pygame, Arcade, Pyglet, Ren'Py, Godot-Python)

Aplicabilidade: `kind: python` (`pyproject.toml`). Convenções da plataforma para
orientar leitura e verificação; confirme a biblioteca pelas dependências e o ponto de
entrada em `[project.scripts]` ou `__main__`. Não substitui AGENTS nem a documentação
oficial.

## Executar e verificar

- Rodar: `python -m <pacote>` ou o script declarado. Testes: `python -m pytest` se
  configurado em `pyproject.toml`; `python -m unittest`. Lógica de jogo separada do
  loop de janela é testável sem display (`SDL_VIDEODRIVER=dummy` no Pygame).
- Não há alvo padronizado no harness: use `verify --command python3 -m pytest`.

## Ciclo de vida e estado

- Loop explícito: `while running` → eventos (`pygame.event.get`) → atualizar → desenhar
  → `clock.tick(fps)`. Delta real vs passo fixo é decisão do projeto.
- Pausa: variável de estado ou máquina de estados; `ACTIVEEVENT`/`WINDOWFOCUSLOST`
  para foco; `pygame.mixer.pause`. Arcade: `on_update`, `Window.set_update_rate`,
  views para telas.
- Reinício: recriar objetos ou reinicializar estado; globais de módulo persistem —
  fonte comum de estado sobrevivente.
- Descarte: `pygame.quit`, fechar mixer, threads/`asyncio` pendentes.

## Conteúdo e pipeline

- Imagens por `pygame.image.load(...).convert_alpha()` (conversão evita custo por
  quadro); sprite sheets manuais; áudio OGG/WAV; fontes por `pygame.font`. Ren'Py tem
  pipeline próprio de script/tradução.

## Performance e orçamentos

- Ferramentas: `cProfile`/`py-spy`, `clock.get_fps`, `tracemalloc`. Orçamentos: tempo
  por quadro, blits por quadro, memória de superfícies.
- Preservando arte: dirty rects, superfícies pré-convertidas, `Group.draw`, evitar
  criação de objetos no loop, Pyglet/Arcade (OpenGL) quando o volume de sprites exigir.

## Build, plataformas e distribuição

- PyInstaller/Nuitka para executáveis; `pygbag` para web (asyncio); Ren'Py exporta
  para desktop/mobile/web. Requisitos de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `pyproject.toml` e ignora `__pycache__`; `verify` só por
  `--command`; `record` guarda medições e observações.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[produção](../../recipes/production.md).
