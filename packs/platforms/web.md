# Plataforma — Web (Canvas, WebGL/WebGPU, JavaScript/TypeScript)

Aplicabilidade: `kind: package.json` ou `static-web`. Convenções da plataforma para
orientar leitura e verificação; confirme cada uma no código do projeto. Não substitui
AGENTS, `package.json` nem a documentação oficial dos navegadores e bibliotecas.

> **Curadoria** — revisado em 2026-09-14.
> **Contempla:** a stack web corrente — Node ≥ 22 (`node --test`,
> `WebSocket` global), Vite 6.x, three.js 0.17x. Versões anteriores mudam APIs de
> cor e de renderer no three; confirme no `package.json` do projeto antes de
> aplicar qualquer item de renderização.
> **Verificar:** `npm test` do projeto deve passar, e a captura headless do
> projeto deve produzir um quadro com a cena carregada — não um
> screenshot em branco. Um teste unitário verde não prova comportamento no
> navegador.
> **Limites:** o harness não abre navegador, não mede quadro nem heap. Medições
> entram por `record --kind budget`, observações por `record --kind observation`.
> Requisitos de loja (itch.io, Poki) e wrappers ficam na fonte oficial.
> **Exemplo rastreável:** os aprendizados de renderização abaixo vêm de casos com
> arquivo e data; registre o seu por `record`, com o arquivo da prova.

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
  traço em desktop, celular e corrida cheia.

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
- Áudio no navegador — o contrato geral (gate antes do verbo, zero sons mudos, entrega sem
  perda) está na [receita de áudio](../../recipes/audio.md#aprendizados-de-carregamento-formato-e-entrega).
  Específico da Web:
  - **Memória:** `decodeAudioData` decodifica fora da thread principal e guarda float32 na taxa
    do contexto. A memória não depende do formato baixado; música longa vai por elemento de mídia.
  - **FLAC com reserva:** entregue WAV como FLAC com o WAV como reserva por arquivo. `canPlayType`
    descreve o `<audio>`, não o `decodeAudioData`: o Safari 15 anunciou WebM Opus que a Web Audio
    recusava e silenciou jogos Construct. howler.js e Phaser não trocam de formato quando a
    decodificação falha; o carregador do jogo precisa fazer isso.
  - **Concorrência:** sobre HTTP/2, dezenas de arquivos pequenos esperam mais por idas e voltas
    do que por bytes. Meça a concorrência do carregador em produção antes de juntar arquivos
    em sprite.
  - **Prova:** compare os bytes do FLAC com os do WAV e confira amostras idênticas em Safari, Chrome
    e Firefox. Na concorrência, meça em produção: subir o número de downloads simultâneos ajuda até um
    ponto e piora depois. O valor ótimo é local.
  - **Hipótese com prova pendente:** no iOS, a sessão `ambient` padrão silencia Web Audio com a
    chave de silêncio, e elemento de mídia pode seguir outra regra. `navigator.audioSession`
    (Safari 16.4+) escolhe a categoria. Teste no aparelho.
- Confira os arquivos publicados antes de cada release; é uma fraqueza comum,
  inclusive em projetos com loop e renderização bem resolvidos:
  - GLB acima de ~1 MB com meshopt ou Draco e quantização; o script de bake declarar
    a extensão não prova que o arquivo publicado a tem. Em bibliotecas de animação,
    meça também o chunk JSON, que pode dominar o arquivo e escapa do meshopt.
  - Textura com resolução de arquivo igual à usada: baixar 4096² para reduzir no
    decode, fazer chroma key ou downscale em runtime, ou repetir a mesma imagem em
    vários GLB (compare hashes) é trabalho que cabia no pipeline.
  - KTX2/Basis com codec por classe — sem perda ou UASTC para normais, ETC1S para
    cor somente depois de comparação visual. Compressão que muda a imagem é corte.
  - Música comprimida e tocada por streaming (`<audio>` ligado ao grafo) ou decodificada
    sob demanda; decodificar toda a trilha no boot custa dezenas de MB de PCM. Um
    formato por navegador; a mesma música sob duas chaves baixa e decodifica duas vezes.
  - Nada publicado sem consumidor no caminho padrão (variantes legadas, GLB vazios,
    mocks de referência), nenhum WASM em base64 dentro do bundle, nenhuma URL absoluta
    de produção nos loaders, e a mídia do loader depois dos bytes críticos.
  - Meça bytes transferidos e decodificados até o primeiro quadro jogável; o resto da
    sessão entra por manifesto com prioridade e concorrência limitada.

### Primeiro minuto como pacote

Vale para jogo para celular (inclusive o web empacotado em Capacitor/Electron) e para web de
carga longa.

- **Quando aplicar.** A primeira carga completa passa do tempo que a pessoa espera parada.
  Se o jogo inteiro cabe na primeira carga, não há o que cobrir: leve tudo no pacote e use o
  tutorial só como ensino.
- **Como.**
  - **Declare em dado o pacote do primeiro minuto:** a cena ou arena da primeira partida, o kit
    base do personagem inicial, a UI, os sons do verbo e a voz do tutorial. Uma constante numa
    tabela de dados que nomeia o local da primeira partida é o que permite garantir que o
    conteúdo esteja no pacote.
  - **O resto vai para um manifesto em segundo plano**, na ordem provável do jogador: outras
    arenas, skins, voz por personagem, música longa, eventos.
  - **O tutorial roda sem esperar o manifesto,** local e contra bots se for multiplayer.
  - **O fim do tutorial cai em conteúdo já baixado,** ou num pedido honesto com o tamanho
    ("<tamanho> para continuar", depois do onboarding).
  - **Depois do primeiro minuto, catálogo grande vem sob demanda:** cada arena, skin ou item
    baixa quando é aberto, e o próximo destino provável entra em pré-carga.
  - **Evite a tela de espera bloqueante.** Uma cena própria que pede mais de um gigabyte, sem
    nada jogável no pacote, é o padrão a evitar. Se a espera for inevitável, mostre tamanho e
    progresso e ofereça algo jogável que já esteja no pacote, como um modo de treino no mesmo
    diálogo do download.
- **A maquinaria comum em jogos de carga longa.** Ponha estas peças no carregador antes de ter
  muito conteúdo:
  - **Adiar só acréscimo.** O adiado nunca é a peça da primeira partida. Adie
    apenas a alta resolução, as vozes extras e as músicas alternativas, e deixe a base de cada
    textura no pacote. Vale com o piso visual: o que aparece no primeiro minuto já tem o
    acabamento aprovado, e trocar por alta resolução depois só é aceitável para conteúdo que
    ainda não apareceu.
  - **Manifesto com hash e núcleo marcado.** Hash por arquivo e versão no manifesto. O bootstrap
    fica marcado para que verificação e reparo nunca o apaguem.
  - **Camadas com versão própria.** Dados, código e modos versionam separados do app. Arquivo
    grande estável ganha diff; o resto é checado por hash e baixado de novo. Dado novo tem
    mensagem própria ("dado atualizado, reiniciando"), distinta de "atualize o app".
  - **Fila com prioridade e nova tentativa.** Três níveis, obrigatório, importante e opcional,
    com teto de tentativas e espera crescente. Retomada
    ligada à reconexão.
  - **Avisos antes de gastar.** Tamanho sempre. Rede celular e espaço onde a plataforma permite:
    no navegador, `navigator.storage.estimate()` para espaço; no empacotado, o aviso nativo.
  - **Em multiplayer, a sala confere o conteúdo de cada jogador** antes de começar, com o
    estado de download do mapa por jogador.
  - **Padrões locais primeiro.** A config remota começa pelos valores embarcados e sincroniza
    sem bloquear. Não condicione a partida offline a uma chamada que pode falhar: capture o
    erro, registre e siga com os padrões locais.
  - **A barra mostra o progresso do carregador,** não uma animação independente. A espera pode
    ensinar: dicas filtradas pelo nível da conta.
- **O que verificar.**
  - **Carga fria com rede limitada** (perfil de celular do DevTools): tempo até o primeiro input
    e bytes até o primeiro quadro jogável.
  - **Manifesto bloqueado:** o tutorial precisa terminar inteiro sem nenhum arquivo dele.
  - **Fim do tutorial:** não pode bater em arquivo ausente.
  - **Veterano:** com save, pula o tutorial e recebe a espera com progresso.
  - **Rede derrubada no meio:** o download retoma e o jogo abre offline com os padrões locais.
  - **Reparo:** apagar um arquivo do manifesto faz ele voltar, e o bootstrap nunca some.
- **O que invalida.**
  - **Alongar ou travar o tutorial para esconder a carga.** O primeiro minuto precisa ser bom
    como ensino, e o download só aproveita o tempo dele.
  - **Rebaixar o acabamento para caber no pacote.** Levar uma versão `_low` do conteúdo no
    pacote seria corte do piso aprovado. Adie o conteúdo em vez de degradá-lo.
- **Limites.**
  - Nenhum tempo de carga foi medido para esta seção.
  - Retenção não foi medida; "feito para reter" é inferência.

## Performance e orçamentos

- Ferramentas: DevTools Performance (tempo de quadro, long tasks), Memory (heap ao
  longo do tempo), Lighthouse (carregamento), `performance.now()` em pontos de prova,
  `renderer.info` em three.js (draw calls, triângulos).
- Orçamentos típicos a medir: quadro p99 no dispositivo mais fraco alvo, heap após
  N minutos (vazamento), tempo até interativo em rede móvel, tamanho transferido.
- Otimizações que preservam arte: batching/instancing, atlas, culling, LOD, pooling de
  objetos para evitar GC, `OffscreenCanvas`/workers para trabalho pesado.
- Densidade de pixels é qualidade: o teto de DPR ou o orçamento de pixels
  (`min(devicePixelRatio, teto, sqrt(orçamento / (largura × altura)))`, recalculado no
  resize) entra na aprovação visual e não muda em runtime sem escolha do jogador.
  Em Canvas 2D, o backing store é o tamanho CSS × DPR; resolução lógica fixa
  ampliada por CSS perde nitidez, salvo pixel art declarada com escala inteira.
  Compare o drawing buffer real em três tamanhos de janela.

## Build, plataformas e distribuição

- Build de produção pelo bundler; PWA para instalação; toque e viewport em mobile;
  política de autoplay de áudio; cross-origin para assets externos.
- Quando o jogo conserva HTML/CSS legado ou carrega recursos por URLs montadas em
  runtime, teste o diretório emitido em um servidor estático separado do dev server.
  Confirme a ordem efetiva de estilos, dimensões do palco/controles e uma ação real;
  sucesso no Vite não prova o artefato de distribuição. Inclua no empacotamento os
  sons, manifestos e bibliotecas chamados dinamicamente; confira disponibilidade,
  decodificação e integridade dos arquivos, sem trocar qualidade por tamanho.
  “HTML único” só é autônomo se suas dependências também forem incorporadas.
  Exemplos do que aparece: CSS hoisted sobreposto pelo legado e áudio/PeerJS ausentes no
  dist. Isso não invalida bundlers nem certifica arte ou áudio.
- Cache de assets:
  - **Imutável só com versão:** `immutable` com `max-age` longo só é seguro em URL que muda
    quando o conteúdo muda (hash no nome ou `?v=` com o hash). Manifestos e índices sem versão
    são servidos com `no-cache` e ETag.
  - **Clientes antigos:** um manifesto que um deploy anterior serviu como imutável fica preso no
    navegador; mudar o cabeçalho não o alcança. Peça com `fetch(url, { cache: 'no-cache' })` para
    forçar a consulta condicional.
  - **404:** uma regra de cabeçalho por caminho também vale para 404; uma URL errada fica em
    cache pelo mesmo prazo.
  - **Prova:** uma visita com a cópia antiga guardada recebe a versão nova. Um pedido comum
    pode devolver a cópia velha sem consultar o servidor, e `no-cache` traz a nova; confira nos
    navegadores-alvo.
  - **Pasta inteira imutável:** uma regra por pasta (`/(audio|sfx|music)/(.*)`) pega também os
    manifestos e as mídias de nome fixo que ela guarda. Sem versão na URL, a pasta leva `max-age`
    curto sem `immutable` (um dia, por exemplo); o script de deploy do framework serve
    `.json`, `.md`, `.txt` e `.webmanifest` com `no-cache` em qualquer pasta. Sem isso,
    manifestos de nome fixo podem sair imutáveis por um ano.
  - **Limite:** o cabeçalho do host só se confirma num deploy de prévia.
- Configuração pública do build (`import.meta.env.VITE_*`, flags do `vite.config`):
  - **Falha muda:** o Vite compila sem erro com a variável ausente e o recurso some do ar
    sem aviso. Um build num checkout limpo ou noutra hospedagem não tem os `.env*` nem o
    painel do host anterior.
  - **Declarar:** `deploy.env` no `workspace.json`: `{"NOME": null}` vem da máquina (ambiente
    ou `.env*` do módulo, nunca do Git); `{"NOME": "valor"}` é fixo e versionado, só para o
    que é público; `""` desliga de propósito. O `gameops deploy` bloqueia variável ausente e
    `VITE_` lida pelo código sem declaração; o script de deploy estático, também no atalho
    `npm run deploy`, recusa o build que não contém cada `VITE_` com valor.
  - **Prova:** testes e conferência por hash passam com a variável ausente; só a leitura do
    bundle servido mostra `env={}`. Leia o bundle publicado depois de trocar de hospedagem.
- Lojas web (itch.io, Poki, Newgrounds) e wrappers (Electron, Tauri, Capacitor) têm
  requisitos próprios — consulte a fonte oficial.
- Empacotar o mesmo jogo para desktop, Steam e lojas móveis (fatos de 24/09/2026; o
  desempenho no aparelho é hipótese até a prova):
  - **Steam por Electron:** Steamworks só por binding comunitário (`steamworks.js`, MIT,
    última release no npm 0.4.0, de 2024) — risco de manutenção; mantenha o módulo nativo
    no processo principal via IPC, com `sandbox` e `contextIsolation` no renderer. No Steam
    Deck, sem depot Linux o jogo roda a versão Windows por Proton; o Electron nativo depende
    do Steam Linux Runtime (ValveSoftware/steam-runtime #579, 2023).
  - **Lojas móveis por Capacitor:** o WKWebView tem WebGPU ligado por padrão a partir do
    iOS 26 (flags do Safari não valem para WebView); no Android WebView o WebGPU não tem
    marco registrado, então WebGL 2 é o caminho. App Store 2.5.2: conteúdo dentro do
    pacote, sem baixar código que mude funcionalidade; 4.2: mais que site reempacotado.
  - **Verificar:** imagem e p95 de quadro do pacote no aparelho e no Deck, em movimento e
    pareados com o navegador. Se não sustentar o acabamento aprovado, a saída é outra
    engine, não cortar arte. Contraprova: o Vampire Survivors relatou em 2022 falhas de
    renderização do Electron em parte do hardware e migrou de engine por desempenho e
    consoles; stack web não chega a console.
  - Plataformas UGC fechadas não recebem exportação web: ver [Roblox](roblox.md#porte-de-jogo-de-outra-engine)
    e [UEFN](unreal.md#uefn-ilhas-do-fortnite).

## Telemetria de produto

Regras que valem para qualquer jogo web medido (auditoria de tag e de camadas de eventos).
Hipótese de valor, não promessa de ganho.

- **Uma tag, cópias idênticas.** Se cada jogo leva a própria cópia, um teste compara todas
  ignorando só a identidade (`game_id`, `game_name`). Deriva entre cópias foi o defeito mais comum.
- **Limpar a URL sem perder campanha.** Tirar query e fragmento (código de sala, token, retorno de
  login) mas manter `utm_*` e ids de clique; senão toda campanha vira acesso direto.
- **Volta de login não é origem.** Referência de provedor OAuth (`accounts.google.com`, Supabase,
  Apple) sai vazia com `ignore_referrer`; senão o login aparece como canal.
- **Só domínio próprio mede.** Lista de hosts permitidos na tag; cópia publicada por terceiros com o
  mesmo ID suja a propriedade. `?analytics_debug=1` libera QA em qualquer host.
- **Telas virtuais desligam a visita automática.** Jogo que emite uma `page_view` por tela marca a
  tag (`data-screens="virtual"`); sem isso cada entrada conta duas vezes.
- **Lista fechada nasce do registro do jogo.** Valores permitidos (personagem, mapa, modo) vêm do
  mesmo módulo que o jogo usa; lista copiada envelhece e descarta o conteúdo novo em silêncio.
- **Medir o convite.** Jogo com sala por link mede copiar o link e chegar por ele; esse boca a boca
  aparece como acesso direto e fica invisível sem evento.
- **Verificar na propriedade.** Dimensão personalizada registrada com o parâmetro exato (conferir o
  nome salvo), retenção de eventos acima do padrão de 2 meses e rolagem automática desligada em
  página de jogo (dispara sozinha e vira ruído de engajamento).

## O que o harness faz aqui

- `discover` reconhece `package.json` e `index.html`; `verify --script` cobre os
  scripts declarados; `context.capabilities` procura menções em `game.mjs`,
  `game.test.mjs`, `src/engine/core/loop.js` e `headless/env_server.ts`.
- Não abre navegador, não mede quadro nem heap; registre medições com
  `record --kind budget` e observações com `record --kind observation`.
- Captura de WebGL sem navegador aberto: em Mac
  com GPU, `chrome --headless=new --use-angle=metal --remote-debugging-port=0` renderiza o
  pipeline completo (SwiftShader em VM não conclui). `--screenshot` sai antes da cena
  carregar e `--virtual-time-budget` nunca termina com `requestAnimationFrame`; conecte pelo
  DevTools Protocol (`WebSocket` nativo do Node ≥ 22), espere um status da própria página
  informar quadros e só então `Page.captureScreenshot`.

Núcleo: [ciclo de vida](../../recipes/lifecycle.md), [visual](../../recipes/visual.md),
[feel](../../recipes/feel.md), [produção](../../recipes/production.md).

## Aprendizados de renderização e medição

Extraídos de casos WebGL/WebGPU; confirmar no carregador e no backend instalado.

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
- Em filetes, frisos e réguas com poucos centímetros de espessura, o chanfro de uma caixa
  arredondada não aparece na câmera de jogo e custa dezenas de vezes os triângulos de uma
  caixa reta (300 × 12 com `RoundedBoxGeometry` de 2 segmentos). Troque só as peças finas.
  Prove comparando a diferença de pixels com o ruído de duas capturas iguais e olhando um
  recorte ampliado lado a lado. A regra não vale para peças grandes ou vistas de perto,
  onde o chanfro pega luz.
- Geometria gerada por grade (marching cubes/tetrahedra, SDF) também precisa seguir o erro
  na tela da escala em que vai aparecer. Uma grade fixa fina fez as mãos somarem a maior parte
  dos triângulos de cada personagem numa câmera de cima, onde elas ocupam poucos pixels.
  Gere por escala, mantendo a malha fina onde ela é vista de perto (menu, retrato). Prove
  com pose e câmera fixas, comparando com o ruído de capturas iguais.
- Um servidor de desenvolvimento compartilhado com outra sessão recarrega a página e disputa
  a GPU. Meça cópias isoladas (o commit base e o base com os arquivos alterados), cada uma
  na sua porta, em rodadas alternadas, e compare só pares da mesma rodada. O ruído entre
  rodadas pode ser maior que o efeito medido.
- Renderer de traço por pós-processo (contorno e hachura lidos de um buffer de dados,
  como um renderer de tinta): todo material próprio escreve o mesmo contrato do
  buffer (tom, caneta, normal). Sombreamento amplo vai como tom que o pós converte em
  hachura; modos de tinta chapada leem como mancha. Linha procedural fina usa um modo
  contínuo (aguada) para não serrilhar. Verifique ampliando a captura em movimento.
- Nesse renderer em câmera ortográfica, a densidade da hachura depende da altura
  visível: atualize o parâmetro a cada mudança de zoom, não só no redimensionamento.
- Miniatura ou retrato gerado pelo mesmo renderer: renderize no tamanho de exibição
  (× DPR). Traço medido em pixels afina quando a imagem é reduzida depois.
- Efeitos num buffer sem transparência somem por escala ou por estágios de tom; a
  opacidade não participa.
- Ao passar de câmera lateral para perspectiva 2.5D com terreno extrudado, o plano dos
  personagens precisa ir para cima do bloco (atrás da borda da frente). Mantido à frente da
  fachada, como na vista lateral, o personagem parece flutuar diante do prédio. Uma sombra
  de contato no chão ancora o pé. Confira de perto, parado e no salto.
- Numa elipse deitada vista de ~10° acima, a altura na tela é só ~0,2 da profundidade
  real. Aumente a profundidade para a sombra aparecer.
- Nomes reservados do GLSL (`patch`, `sample`, `input`, `output`, `filter`) quebram a
  compilação sem erro de JavaScript. Leia o log do programa no console do navegador.
- Planejador de IA que simula num clone do mundo real: desligue os cálculos que só servem
  à verificação (hash de 2 MiB do terreno por explosão, por exemplo). Meça o CPU por
  plano antes e depois de desligar.
- Configuração de elenco ou slots copiada com `[...lista]` compartilha os objetos
  internos. Uma partida que reescreve um campo contamina a partida seguinte. Copie cada
  slot (`map((slot) => ({ ...slot }))`) e teste duas criações seguidas.

Persistência, pausa e descarte dos buffers de animação/áudio seguem as receitas de
[conteúdo](../../recipes/content.md), [áudio](../../recipes/audio.md) e
[performance](../../recipes/performance.md).

## Aprendizados de páginas interativas

Valem para landings, hubs e páginas com canvas, camadas e 2.5D; confirmar no navegador de destino.

- **Layout decidido cedo.** Um modo que muda a altura da página (palco fixo, caderno 3D, galeria
  horizontal) precisa ser aplicado no carregamento, e não quando o código da seção chega. Senão,
  âncoras e links do menu caem no lugar errado. Verifique clicando em cada link antes de qualquer rolagem.
- **`loading="lazy"` não basta em pilhas.** Elementos empilhados num palco fixo ficam todos
  "perto" da tela e baixam juntos. Oculte os distantes (`display: none`) até a seção se aproximar.
  `background-image` em pseudo-elemento carrega assim que o CSS se aplica: libere por classe.
  Meça o que baixa na abertura, e não só o total.
- **Troca de conteúdo exige nome novo.** Com cache longo (ex.: `max-age=86400`), republicar um
  asset com o mesmo nome deixa quem já visitou com a versão antiga. Versione o nome ou o parâmetro.
- **Isolar cada componente.** Um construtor que lança erro não pode derrubar os vizinhos:
  inicialize cada miniatura isoladamente e registre a falha.
- **Máscara corta sombra.** `mask` ou `clip-path` no mesmo elemento da `box-shadow` a recorta.
  Ponha a sombra num pseudo-elemento fora da máscara.
- **Pilhas de fonte manuscrita não terminam em `cursive`.** No macOS o genérico vira Apple
  Chancery enquanto a fonte carrega. Termine em `system-ui, sans-serif` e use `font-display: block`
  nas fontes pré-carregadas da tela de entrada.
- **Desenho de caneta determinístico.** Tremor de traço com semente fixa por objeto não "ferve"
  entre quadros. Formas geométricas (asas, caixas, triângulos) não passam pelo suavizador de
  traço, que arredonda quinas e muda a silhueta.
- **2.5D sem deformar texto.** Mover `perspective-origin` com o ponteiro, e não girar a página,
  preserva a nitidez do texto e o alinhamento de um canvas de desenho. `pathLength` com
  `vector-effect: non-scaling-stroke` não anima o tracejado; revele por `clip-path`.
- **Stop-motion.** Poucos quadros por segundo (8 a 12) e deslocamento em degraus. Tremor
  aleatório contínuo por quadro lê como inseto ou nervosismo.
- **Desenho do público que ganha vida precisa de limite de forma.** Converter o traço no contorno
  convexo arredondado, com alongamento limitado, impede reproduzir formas obscenas sem bloquear o
  gesto. Teste com casos positivos e negativos. Filtro de forma não é moderação completa: texto,
  imagens enviadas e contexto social exigem outras camadas.
- **Heurísticas de gesto** (reconhecer ∞, laço, risco) só entram depois de testar formas que devem
  e que não devem disparar.

Limites: observado em Chromium de desktop e em emulação de celular; sem aparelho físico
nem rede móvel real. Os números de peso são exemplos e não se transferem.

## Aprendizados de interface de jogo no celular

Valem para jogo web em paisagem no celular e no tablet, inclusive empacotado. O sintoma comum é a
interface parecer uma página: fonte do sistema, texto selecionável, dica de mouse, rolagem, aviso legal.

- **Tipografia própria, embutida.** Arquivos `woff2` locais com `preload` e `font-display: block`, para
  não piscar e funcionar sem rede. Família de título nos botões, números e placas; família de leitura nas
  descrições. O `font` do canvas não aceita `var(--x)`: escreva o nome real da família ali, ou o texto cai
  na fonte padrão sem erro. Texto claro sobre peça escura leva contorno; texto escuro sobre dourado, relevo.
- **Comportamento de aplicativo.** `user-select: none` e `-webkit-touch-callout: none` no jogo;
  `contextmenu` e `dragstart` cancelados; nada de `title` (vira dica de mouse), use `aria-label`; contorno
  de foco só depois de uma tecla (classe ligada no `keydown` e desligada no `pointerdown`).
- **Telas cabem por desenho.** Sem rolagem nativa, o que não cabe vira grade com ficha de detalhe, abas ou
  cartas lado a lado. Um paginador genérico que fatia pela altura corta cartas ao meio; quando paginar,
  quebre na borda de itens inteiros, oculte o item parcial e aceite o gesto de deslizar.
- **Nada fixo que não seja jogo.** Um convite de instalação permanente custou 13% da altura em paisagem;
  ofereça-o na abertura e nas configurações. O prompt nativo só depois de um toque.
- **Sem cópia de página.** Sobrancelhas acima de títulos, slogans, avisos como "salvo localmente" e setas
  de link saem; entram progresso real, placas e o triângulo de jogar. Créditos num painel próprio.
- **Resposta de jogo.** Uma transição curta ao trocar de tela, janela que surge com pequeno salto, botão que
  afunda ao toque, som de clique quando o som está ligado; `prefers-reduced-motion` remove os movimentos.
  Carregamento com progresso real e dicas de jogo no lugar de slogan.

**Verificar** em cada tamanho-alvo: varredura de estouro (`scrollWidth > clientWidth` em botões e títulos;
família de título larga quebra rótulos que cabiam); matriz sem rolagem em nenhum contêiner, alvo ≥ 44 px e
alcance pelo ponto central (`elementFromPoint`). Testes que dependem de uma classe de layout quebram quando a
tela é refeita: mantenha um gancho estável ou teste pelo controle público. Um harness de lógica sem
`cancelAnimationFrame` ou `setInterval` quebra com chamadas novas; guarde-as ou use `setTimeout` em cadeia.

Limites: observado em Chromium com toque emulado e GPU real, em celular e tablet emulados; sem Safari nem
aparelho físico. Percentuais são do caso e não se transferem como meta.
