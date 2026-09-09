# Plataforma — Ren'Py

Aplicabilidade: `kind: renpy` (`game/options.rpy`). Convenções da plataforma para
orientar leitura e verificação; confirme a versão pelo launcher/SDK e `config.version`.
Não substitui AGENTS nem a documentação oficial.

## Executar e verificar

- Rodar: `<sdk>/renpy.sh <projeto>`; lint: `renpy.sh <projeto> lint`; compilar sem
  jogar: `renpy.sh <projeto> compile`. Build/distribuição por `renpy.sh launcher
  distribute <projeto>`.
- Testes: `lint` pega labels/jumps quebrados e variáveis; testes de fluxo por
  `renpy.sh <projeto> --auto` não são padrão — scripts Python puros em `game/` podem
  ser testados fora. Use `verify --command <sdk>/renpy.sh <projeto> lint`.

## Ciclo de vida e estado

- Script por labels; `start` → `jump`/`call`/`return`; menus e escolhas; `init` blocos
  para definições. Rollback percorre o histórico de instruções.
- Estado: variáveis definidas por `default` entram no save e no rollback; `define` não.
  Persistente entre jogos via `persistent.`. Mudar estrutura de dados quebra saves sem
  migração (`renpy.register_persistent`/versão em `config.save_directory`).
- Pausa/foco: engine trata; `config.rollback_enabled`, `renpy.pause`; áudio por canais.
- Reinício: `renpy.full_restart()`; `persistent` sobrevive — fonte de estado
  sobrevivente intencional.

## Conteúdo e pipeline

- Imagens por `image` e atributos (layered images), `screen` language para UI,
  transforms/ATL para movimento, áudio em canais, tradução por `renpy.sh <projeto>
  translate <idioma>` gerando `tl/<idioma>/`. Fontes com cobertura por idioma.

## Performance e orçamentos

- Ferramentas: `Shift+G` (renderer), `config.profile`, `renpy.sh <projeto> --profile`.
  Orçamentos: tempo de troca de cena, memória de imagens (cache), tamanho da
  distribuição por idioma/voz.
- Preservando arte: `image cache`, WebP, `predict`, evitar transforms por quadro em
  telas grandes.

## Build, plataformas e distribuição

- Desktop, web (`renpy.sh web`), Android/iOS via RAPT/Renios. Requisitos de loja e
  classificação etária na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `game/options.rpy`; `verify` só por `--command`; `record`
  guarda observações e medições. Não lê `.rpy`.

Núcleo: [conteúdo](../../recipes/content.md) (histórico, saves), [produção](../../recipes/production.md).
Gênero típico: [narrativa](../genres/narrative.md).
