# Plataforma — Haxe (HaxeFlixel, OpenFL, Heaps, Kha)

Aplicabilidade: `kind: haxe` (`Project.xml` para OpenFL/Lime/Flixel ou `*.hxml` para
Heaps/Kha/puro). Convenções da plataforma para orientar leitura e verificação;
confirme o framework em `haxelib`/`Project.xml`. Não substitui AGENTS nem a
documentação oficial.

## Executar e verificar

- OpenFL/Flixel: `lime test <alvo>` (html5, windows, mac, linux, android, ios, hl),
  `lime build <alvo>`. Heaps: `haxe build.hxml` gerando JS/HL/C++, rodar com `hl` ou
  navegador. Kha: `khamake`/`node Kha/make <alvo>`.
- Testes: `utest`, `munit`, `buddy` via hxml de teste; lógica sem display é testável
  no alvo `interp`/`eval` (`haxe --run`). Use `verify --command haxe test.hxml`.

## Ciclo de vida e estado

- Flixel: `FlxGame` → `FlxState` (`create`/`update(elapsed)`/`destroy`), `FlxG.switchState`,
  `FlxG.timeScale`, `FlxG.autoPause` para foco. Heaps: `hxd.App` (`init`/`update(dt)`),
  `hxd.Window` eventos de foco. OpenFL: `Event.ENTER_FRAME`, `Event.ACTIVATE/DEACTIVATE`.
- Reinício: novo `FlxState`/reset de `hxd.App`; estáticos (`FlxG.save`, singletons)
  persistem — fonte comum de estado sobrevivente. Descarte: `destroy()` em Flixel,
  `remove()` em Heaps, listeners e `Tween`s.

## Conteúdo e pipeline

- OpenFL `<assets path=.../>` em `Project.xml` com embed por alvo; Flixel atlases
  (`FlxAtlasFrames`), Tiled/LDtk (`flixel-addons`, `ldtk-haxe-api`); Heaps `hxd.Res`
  com PAK e `res/` tipado; shaders HXSL (Heaps) / GLSL (OpenFL).

## Performance e orçamentos

- Ferramentas: `FlxG.debugger`, `hxd.Perf`, profiler do navegador (html5), HashLink
  profiler. Orçamentos: quadro por alvo (html5 é o mais fraco), draw calls, memória de
  texturas, tempo de carga de assets.
- Preservando arte: atlases, `FlxSpriteGroup`/`FlxTypedGroup` pooling, `h2d.SpriteBatch`,
  `TileGroup`, culling por câmera.

## Build, plataformas e distribuição

- Alvos nativos via hxcpp/HashLink, web via JS/WebGL, mobile via Lime; consoles via
  parceiros (Kha/Heaps). Requisitos de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `Project.xml`/`*.hxml` e ignora `export`, `bin`; `verify` só por
  `--command`; `record` guarda medições e observações.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md),
[produção](../../recipes/production.md).
