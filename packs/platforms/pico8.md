# Plataforma — PICO-8 (e fantasy consoles afins: TIC-80, Picotron)

Aplicabilidade: `kind: pico8` (`*.p8`). Convenções da plataforma para orientar leitura
e verificação; limites são parte do design (128×128, 16 cores, 8192 tokens, 4 canais).
Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- `pico8 -run jogo.p8`; headless: `pico8 -x script.p8` executa e sai (útil para testes
  em Lua com `assert` e `printh`). Exportar: `export jogo.html`/`.bin` dentro do
  console. Ferramentas externas: `shrinko8`/`p8tool` para tokens e build de múltiplos
  arquivos (`#include`).
- Use `verify --command pico8 -x tests.p8`.

## Ciclo de vida e estado

- `_init` → `_update` (30 fps) ou `_update60` (60 fps) → `_draw`. Sem pausa nativa além
  do menu do sistema (P); pausa de jogo é estado próprio. Foco: o console pausa sozinho.
- Reinício: `run()` reinicia o cartucho; `cartdata`/`dset`/`dget` persistem (64 valores)
  — fonte de estado sobrevivente intencional. Descarte: irrelevante — reinício limpa
  tudo, exceto `cartdata`.

## Conteúdo e pipeline

- Sprites (256 de 8×8), mapa (128×32/64), SFX (64) e música (64 padrões) no editor do
  console; tudo no `.p8` em texto. Dados extras em strings/`peek`/`poke`; `#include`
  para dividir código. Paleta secreta via `poke(0x5f2e,1)`/`pal` com cuidado.

## Performance e orçamentos

- Ferramentas: `stat(1)` (CPU do quadro em fração), `stat(0)` (memória Lua), `Ctrl+P`
  (monitor). Orçamentos: CPU < 1.0 no pior quadro, tokens (8192), caracteres (65535),
  memória Lua (2 MB).
- Preservando arte: `spr`/`sspr` em lote, `map` em vez de sprites soltos, evitar tabelas
  criadas por quadro, `flr` por `\` e `%`; a arte é o limite — não há LOD.

## Build, plataformas e distribuição

- HTML (Lexaloffle BBS, itch.io), binários desktop, Raspberry Pi. Cartuchos são
  públicos por natureza (código legível); licença própria dos assets ainda se aplica.

## O que o harness faz aqui

- `discover` reconhece `*.p8`; `verify` só por `--command`; `record` guarda `stat(1)`
  e observações.

Núcleo: [mecânicas](../../recipes/mechanics.md), [feel](../../recipes/feel.md),
[produção](../../recipes/production.md). O piso sonoro "sem 8-bit por padrão" não se
aplica a um fantasy console: aqui o chiptune é a plataforma; registre a decisão.
