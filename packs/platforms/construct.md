# Plataforma — Construct 3

Aplicabilidade: `kind: construct` (`*.c3proj` em projeto salvo como pasta). Convenções
da plataforma para orientar leitura e verificação; projetos `.c3p` (arquivo único) não
são reconhecidos — salve como pasta para versionar e diffar. Não substitui AGENTS nem
a documentação oficial.

## Executar e verificar

- Editor no navegador; preview por layout ou projeto; exportação por menu (HTML5,
  NW.js, Cordova, Xbox/Windows via wrappers). Há CLI de exportação limitada via
  automação do editor em versões recentes — confirme na documentação da versão.
- Testes: não há runner nativo. Lógica em JavaScript (scripts do projeto) pode ser
  testada fora do editor; eventos são testados por layouts de teste e `Browser.Log`.
- Use `verify --command` com o que o projeto adotar; sem CLI, registre observação
  com `record`.

## Ciclo de vida e estado

- Event sheets: `On start of layout` → eventos por tick (`Every tick`, condições) →
  `On end of layout`. `dt` por `dt` do sistema; `Set time scale` para pausa/slow-mo
  (0 pausa comportamentos baseados em tempo, não eventos).
- Foco: `On suspended`/`On resumed` (Browser); áudio precisa de gesto no navegador.
- Globais e objetos globais persistem entre layouts — fonte comum de estado
  sobrevivente ao reinício. `Restart layout` não reseta globais.
- Descarte: objetos destruídos ao trocar layout salvo os globais; timers e tweens
  pendentes; `Audio` em loop.

## Conteúdo e pipeline

- Sprites com animações por frame, tilemaps, famílias e containers, behaviors
  (Platform, 8 Direction, Physics), Timelines. Arquivos em JSON/texto na pasta —
  legíveis, mas gerados pelo editor; edite pelo editor.

## Performance e orçamentos

- Ferramentas: Debugger com profiler (CPU por evento/objeto, GPU), `Browser` stats,
  DevTools do navegador (é WebGL/WebGPU). Orçamentos: quadro no dispositivo mais
  fraco, contagem de objetos e colisões por tick, spritesheets/texturas em memória.
- Preservando arte: collision cells, `Every X seconds` em vez de every tick, famílias
  para reduzir eventos, spritesheet padding, WebGL effects com parcimônia.

## Build, plataformas e distribuição

- Exportações web (itch, Poki, Newgrounds), mobile via Cordova/Build Service, desktop
  via NW.js/WebView2. Requisitos de loja na fonte oficial.

## O que o harness faz aqui

- `discover` reconhece `*.c3proj`; `verify` só por `--command`; `record` guarda
  medições do debugger e observações. Não lê event sheets.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [feel](../../recipes/feel.md),
[produção](../../recipes/production.md). Ver também [web](web.md).
