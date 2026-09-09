# Plataforma — RPG Maker (MZ, MV)

Aplicabilidade: `kind: rpgmaker` (`*.rmmzproject` ou `*.rpgproject`). Convenções da
plataforma para orientar leitura e verificação; MZ/MV são NW.js + JavaScript (Pixi.js);
versões antigas (VX Ace, Ruby) não são reconhecidas. Não substitui AGENTS nem a
documentação oficial.

## Executar e verificar

- Playtest pelo editor; o jogo é `index.html` + `js/` + `data/*.json` rodando em NW.js
  (`nw .` na pasta) ou navegador com servidor local. Deploy por menu (Windows, macOS,
  web, mobile).
- Testes: não há runner nativo. Plugins (`js/plugins/*.js`) são JavaScript testável
  fora do engine com mocks de `Game_*`/`Scene_*`; eventos são testados jogando.
- Use `verify --command` (ex.: `node --test` para plugins) e `record` para observação.

## Ciclo de vida e estado

- `SceneManager` (Boot → Title → Map/Battle/Menu), `Scene_Base.update`, `Game_*`
  objetos serializados no save (`$gameVariables`, `$gameSwitches`, `$gameParty`...).
- Pausa: cenas de menu pausam o mapa; foco por eventos de janela do NW.js; áudio via
  `AudioManager`. `Graphics.frameCount` e `Graphics.app.ticker` para tempo.
- Reinício: `SceneManager.goto(Scene_Title)`; `$data*` (banco) não muda, `$game*`
  reinicia por `DataManager.setupNewGame`. Plugins com estado em módulo persistem —
  fonte comum de estado sobrevivente.
- Saves: `DataManager.makeSaveContents` — mudar `Game_*` em plugin quebra saves antigos
  sem migração.

## Conteúdo e pipeline

- `data/*.json` (mapas, banco de dados, eventos), `img/` (tilesets, characters,
  faces, pictures em tamanhos fixos), `audio/` (BGM/BGS/ME/SE em OGG/M4A), plugins com
  parâmetros em `plugins.js`. Ordem de plugins importa.

## Performance e orçamentos

- Ferramentas: DevTools do NW.js (F8/F12), `Graphics.fps`, profiler do Chrome.
  Orçamentos: eventos paralelos por mapa, pictures grandes em memória, sprites em
  batalha, tempo de carga de mapa.
- Preservando arte: pré-carregar imagens, evitar eventos paralelos com `Wait 0`,
  atlas de tiles, filtros Pixi com parcimônia.

## Build, plataformas e distribuição

- Deployment do editor (exclui recursos não usados, criptografia opcional); web exige
  servidor; mobile via Cordova/wrappers. Requisitos de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece o projeto antes de `package.json` (o MZ tem um na raiz);
  `verify` só por `--command`; `record` guarda observações e medições.

Núcleo: [conteúdo](../../recipes/content.md) (saves, dados), [ciclo de vida](../../recipes/lifecycle.md),
[produção](../../recipes/production.md). Gênero típico: [rpg](../genres/rpg.md).
