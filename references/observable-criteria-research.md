# Critérios observáveis: o que a literatura sustenta

Pesquisa de fontes externas feita em 9 de setembro de 2026. Este arquivo **não é
uma escada de acabamento nem um conjunto de gates** — é o levantamento que
precisa existir antes de qualquer um dos dois ganhar número. Se a pesquisa recusa ser um conjunto de gates, o `sources` do `craft` nomeia o conjunto que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `conjunto`. A
[barra](production-bar.md) diz explicitamente que seus limiares em `performance`
e `audio_mix` são pontos de partida a confirmar. Este documento é a tentativa de
descobrir quais números *podem* ser confirmados contra uma fonte, e quais não
podem ser citados de jeito nenhum.

A distinção que organiza tudo aqui:

- **Critério observável** — alguém confere olhando o jogo ou medindo, e duas
  pessoas competentes chegam ao mesmo veredito. *"A fonte do HUD tem no mínimo
  26 px na resolução alvo."*
- **Opinião disfarçada de critério** — parece regra, decide por gosto. *"A arte
  está consistente."*
- **Número folclórico** — tem casas decimais e nenhuma medição atrás. É o mais
  perigoso dos três, porque passa por observável. Se a pesquisa recusa que o número folclórico seja critério observável, o item do craft nomeia o folclore que a pesquisa já recusa. Folclore no disco não é o critério. Sem chave `folclore`. Se a pesquisa recusa que três métricas com o mesmo nome sejam um critério, o item do craft nomeia as métricas que a pesquisa já recusa. Nome no disco não é a métrica. Sem chave `métricas`.

## Como ler as fontes deste arquivo

Cada fonte vem com autor, tipo, data e **limite** — o que ela sustenta e onde
para de sustentar. As categorias de tipo:

| Tipo | O que significa |
| --- | --- |
| **Primária** | O experimento, o código, a norma, a documentação do próprio fornecedor |
| **Secundária** | Alguém relatando ou sintetizando o que a primária diz |
| **Prática declarada** | Profissional reconhecido descrevendo o que faz, sem medição |

Onde li só o resumo, o preview ou uma citação de terceiro, está dito. Onde a
fonte primária está atrás de paywall e não a li, está dito. Números que não
consegui rastrear até a origem estão na seção final e **não devem ser citados**.

---

## 1. Game feel e latência de entrada

### 1.1 A cadeia dos 100 ms — de onde ela realmente vem

O número mais repetido do assunto tem uma origem rastreável, e ela não é sobre
jogos.

**Miller, R. B. (1968). "Response time in man-computer conversational
transactions."** AFIPS Fall Joint Computer Conference, vol. 33, pp. 267–277.
[dl.acm.org/doi/10.1145/1476589.1476628](https://dl.acm.org/doi/10.1145/1476589.1476628)
· Primária · 1968.

O artigo abre atacando exatamente o hábito de citar um número único. Miller diz
que a controvérsia sobre tempo de resposta é insolúvel por causa de duas questões
semânticas, e a primeira é *"Response time to what?"* — propósitos e ações
humanas diferentes têm tempos aceitáveis diferentes. Ele então dá uma tabela por
tipo de tarefa. Os itens relevantes:

- Feedback visual de tecla pressionada: *"the delay between depressing the key
  and the visual feedback should be no more than 0.1 to 0.2 seconds"*.
- Ativação de controle (o clique da tecla, a mudança de força do interruptor):
  *"Time delay: No more than 0.1 second."*

**Limite.** É 1968, terminais de texto, caneta óptica, digitação. Miller ainda
adverte, no mesmo parágrafo, que 0,1–0,2 s pode ser *lento demais* para
datilógrafos hábeis, que olham a tela e não o teclado, e lembra que o órgão de
tubos mecânico tinha atraso estimado de 0,1 a 0,2 s — parte da habilidade do
organista era se adaptar a ele. **A fonte original do "100 ms" já contém a
contradição do "100 ms" como constante.** Nada nela mediu controle de avatar.

**Nielsen, J. "Response Time Limits: The 3 Important Limits."** Nielsen Norman
Group.
[nngroup.com/articles/response-times-3-important-limits](https://www.nngroup.com/articles/response-times-3-important-limits/)
· Secundária · publicado em 1993, do livro *Usability Engineering* do mesmo ano.

Os três limites — 0,1 s (instantâneo), 1,0 s (fluxo de pensamento preservado),
10 s (atenção mantida). O próprio Nielsen apresenta como síntese: *"The basic
advice regarding response times has been about the same for thirty years [Miller
1968; Card et al. 1991]."*

**Limite.** É síntese de HCI para interfaces de diálogo, declaradamente derivada
de Miller. Não é medição em jogo. E o que ela afirma é o inverso do que se cita:
*abaixo* de 0,1 s a resposta parece instantânea. Ela **não diz** que jogadores
percebem latência acima de 100 ms.

### 1.2 Swink, *Game Feel* — o que consigo e o que não consigo verificar

**Swink, S. (2008). *Game Feel: A Game Designer's Guide to Virtual Sensation*.**
Morgan Kaufmann / CRC. Preview do editor:
[api.pageplace.de/preview/DT0400.9781482267334_A36189297](https://api.pageplace.de/preview/DT0400.9781482267334_A36189297/preview-9781482267334_A36189297.pdf)
· Primária como arcabouço autoral · 2008.

O preview que li confirma o *projeto* do livro: Swink diz que vai explorar *"the
physiological thresholds that cause game feel to be sustained or break down"* e
que pretende dar *"measures for frame rate, response time and other conditions
necessary for game feel to occur"*. O propósito declarado é converter "floaty" e
"tight" em coisa mensurável.

**O que não consegui verificar.** Os números específicos que circulam atribuídos
a este livro — 50 ms parece instantâneo, acima de 100 ms o atraso é perceptível
mas ignorável, 200 ms parece arrastado, ciclo perceptual humano de 50–200 ms,
fusão de movimento a 10 fps — **não estão no trecho do preview a que tive
acesso**. Eu os vi em duas fontes secundárias: uma resposta no
[gamedev.stackexchange](https://gamedev.stackexchange.com/questions/203106/what-does-continuity-of-response-mean-in-the-book-game-feel)
que cita o livro, e a resenha de
[Liz England](https://lizengland.com/blog/review-game-feel-by-steve-swink/)
(desenvolvedora reconhecida, resenha de primeira mão do livro), que confirma
apenas a definição geral: resposta dentro de um ciclo de correção *"of under 100
milliseconds"*.

**Limite.** Cite Swink para a definição de resposta em tempo real (~100 ms) e
para o projeto de medir feel. Não cite o degrau 50/100/200 como se fosse
verificado — marque como *atribuído a Swink, não conferido no original*. Ainda
que estivesse lá: é síntese de psicologia de HCI (a linhagem do Model Human
Processor de Card, Moran e Newell), não experimento com jogadores.

### 1.3 O que foi de fato medido com jogadores

**Jörg, S., Normoyle, A., Safonova, A. (2012). "How responsiveness affects
players' perception in digital games."** ACM Symposium on Applied Perception
(SAP '12). [doi.org/10.1145/2338676.2338683](https://doi.org/10.1145/2338676.2338683)
· Primária, experimental · agosto de 2012. Li o texto completo.

Plataformer feito em Unity com personagem capturada por motion capture, 18
participantes, **atraso de controle de 150 ms** aplicado como 10 frames a ~70 fps
— e os participantes **não sabiam** que o atraso existia nem tiveram comparação
lado a lado. Resultados, com o que confirmou e o que não confirmou:

- Controlar ficou significativamente mais difícil na condição com atraso.
- Frustração aumentou (efeito principal significativo na satisfação com o próprio
  desempenho, p<0,05; mais confirmação por observação e comentários).
- Desempenho caiu em várias métricas: 106 s no tutorial contra 68 s, 2,3 pontos
  de vida a mais perdidos.
- **Diversão: não confirmado.** O efeito não atingiu significância; os autores
  dizem que as tendências apontam na direção prevista mas a amostra era pequena.
- **Percepção do personagem e do jogo: não confirmado.**

A conclusão prática mais útil do artigo é sobre playtest, não sobre latência:
*"when playtesters complain of either bad controls or an unrealistic and
unsympathetic character, the true cause may actually be poor responsiveness in
the controls."*

**Limite.** Um jogo custom, n=18, um único nível de atraso, atraso com jitter
porque foi implementado em frames. Não estabelece limiar. Estabelece que 150 ms
degrada desempenho e frustra mesmo sem ser percebido conscientemente.

**Claypool, M. e Claypool, K. (2006). "Latency and player actions in online
games."** Communications of the ACM 49(11).
[doi.org/10.1145/1167838.1167860](https://doi.org/10.1145/1167838.1167860). PDF
do modelo em
[web.cs.wpi.edu/~claypool/papers/precision-deadline/final.pdf](http://web.cs.wpi.edu/~claypool/papers/precision-deadline/final.pdf)
· Primária · 2006, estendido em 2010.

**Este é o achado mais importante do tópico 1**, e não é um número: é o modelo
**precisão × prazo** (*precision–deadline*). A sensibilidade à latência não é
propriedade do jogo, é propriedade da *ação*. Duas variáveis: o prazo em que a
ação precisa acontecer e a precisão exigida para ela dar certo. Quanto mais perto
da origem, pior a latência dói. Atirar de sniper em primeira pessoa: precisão
alta, prazo apertado. Correr em terceira pessoa: precisão baixa, prazo médio.
Ações num jogo de perspectiva onipresente (estratégia, simulação): prazos frouxos.

**Limite.** É modelo classificatório, não fórmula. Não devolve milissegundos.
Devolve a pergunta certa: *qual ação, com que precisão, em que prazo* — que é
exatamente o que uma checklist observável precisa perguntar antes de exigir um
número.

**Liu, S., Claypool, M., Kuwahara, A., Scovell, J., Sherman, J. (2021). "Lower is
Better? The Effects of Local Latencies on Competitive First-Person Shooter Game
Players."** CHI '21.
[doi.org/10.1145/3411764.3445245](https://doi.org/10.1145/3411764.3445245) ·
Primária, experimental · maio de 2021. Li o texto completo.

43 jogadores experientes de CS:GO, latências **locais** abaixo de 125 ms
(laptops instrumentados levados às casas dos participantes por causa da
pandemia). Resultado quantificado: **cada 10 ms de redução de latência rende
+0,8% de acurácia e +1,2 ponto de score** — cerca de uma morte extra por partida
— e ~5% de melhora nas notas subjetivas de frustração, irritação e
responsividade. E o detalhe que o artigo faz questão de registrar: os
participantes disseram que muitas vezes **não conseguiam notar** a diferença
entre as rodadas.

**Limite.** Um jogo, jogadores competitivos, latência local e não de rede, faixa
abaixo de 125 ms. Não generaliza para outros gêneros. Mas destrói a ideia de que
existe um limiar de percepção abaixo do qual latência deixa de importar: aqui o
desempenho continuou melhorando numa faixa em que os jogadores não percebiam
diferença.

**Números de terceiros que aparecem citados nesses artigos** (não li os
originais — trate como referência para conferir, não como fato): Dick et al.
(2005) — jogadores dizem em survey que ~120 ms é o máximo tolerável, mas o estudo
deles achou 150 ms aceitável em dois FPS e um jogo de corrida, e em
Counter-Strike **atrasos de 500 ms foram avaliados como "aceitáveis", com a
melhor pontuação média justamente na maior latência**; Armitage et al. — ~150–180
ms em Quake 3; Pantel e Wolf — ~100 ms já afeta corrida; Fritsch et al. —
EverQuest 2 tolera centenas de ms; Hoßfeld et al. — jogadores de Minecraft
insensíveis a até 1 s; Mania et al. (2004) — observadores treinados detectam ~15
ms de latência de head tracking em ambiente virtual.

**A faixa vai de 15 ms a 1 segundo.** Qualquer número único de "latência
perceptível" está escolhendo um ponto dessa faixa e escondendo o resto.

### 1.4 Medições fim a fim: quanto latency os jogos publicados realmente têm

**Nigel "noodalls" Woodall — Input Lag Testing Results.**
[sites.google.com/view/noodallsinputlagtestingresults](https://sites.google.com/view/noodallsinputlagtestingresults/home)
· Primária, autopublicada · década de testes, atualizada continuamente.

Método documentado: Arduino (atualmente um Arduino Giga com touchscreen) controla
o disparo dos inputs e, quando necessário, lê o retorno; análise por vídeo. Ele
escolheu Arduino em parte porque *"being a known brand, it would mean if anybody
wants to follow my testing they can do so"* — reprodutibilidade declarada como
critério de escolha. E abre o site com a ressalva: *"there is no perfect method
for input lag testing."*

Resultados publicados (via EventHubs, que reporta os tweets dele — **secundária**
para os números, primária para o método):

- Street Fighter 6, junho de 2023: PS5 ~57,40 ms; Xbox Series X ~58,30 ms; Series
  S ~55,65 ms; PC ~58,93 ms; PS4 ~70,32 ms; PS4 Pro ~71,93 ms — com "Input Delay
  Reduction" ligado.
  [eventhubs.com/news/2023/jun/05/input-lag-tests-sf6-platforms](https://www.eventhubs.com/news/2023/jun/05/input-lag-tests-sf6-platforms/)
- Fatal Fury: City of the Wolves (beta), fevereiro de 2025: PS5 Pro 69,9 ms; PS4
  slim 49,72 ms; versão PS4 rodando em PS5 30,7 ms; Xbox Series X/S 58,39 ms;
  Steam Deck 63,17 ms (VSync off) / 65,83 ms (VSync on).
  [eventhubs.com/news/2025/feb/20/fatal-fury-input-lag](https://www.eventhubs.com/news/2025/feb/20/fatal-fury-input-lag/)

**Limite.** É a cadeia inteira — controle + console + jogo + captura — em builds e
configurações específicas. Não é revisado por pares e os dados brutos não estão
num repositório citável. Os números chegam por site de notícias citando posts.

**O que isso sustenta, e é muito.** Jogos de luta AAA, o gênero que mais se
importa com latência, entregam **30 a 72 ms fim a fim**. Um alvo de "abaixo de 50
ms" não é impossível, mas está abaixo do que a maioria dos jogos de console
publicados alcança. Isso é calibração honesta: mede-se contra o que existe, não
contra um ideal de blog.

**Método replicável.** Gravar com câmera de alta taxa (240 fps ou mais), apertar
um botão visível, contar frames até a primeira resposta na tela, multiplicar pela
duração do frame. Descrito em
[gamejuice.co.uk/articles/controls-responsiveness-100ms-rule](https://gamejuice.co.uk/articles/controls-responsiveness-100ms-rule)
— **blog sem fontes**, cuja parte teórica está na seção 6; mas o método em si é
conferível por construção e é o mesmo que noodalls usa em versão pobre.

### 1.5 Janelas de perdão: os únicos números realmente auditáveis do tópico

Aqui a evidência é de outra natureza. Não é estudo, é **código publicado**.

**Celeste — `Source/Player/Player.cs`, repositório de Noel Berry.**
[github.com/NoelFB/Celeste/blob/master/Source/Player/Player.cs](https://github.com/NoelFB/Celeste/blob/master/Source/Player/Player.cs)
· Primária (o código que rodou) · fonte publicada pelo desenvolvedor.

Constantes que existem, com nome, no jogo publicado (60 fps, canvas 320×180):

| Constante | Valor | O que é |
| --- | --- | --- |
| `JumpGraceTime` | `0.1f` | coyote time — 100 ms |
| `VarJumpTime` | `.2f` | janela de pulo de altura variável |
| `CeilingVarJumpGrace` | `.05f` | perdão ao bater a cabeça |
| `WallSpeedRetentionTime` | `.06f` | retenção de velocidade ao sair da parede |
| `UpwardCornerCorrection` | `4` | px de correção de quina no pulo |
| `DashCornerCorrection` | `4` | px de correção de quina no dash |
| `WallJumpCheckDist` | `3` | px de distância para wall jump |
| `DashTime` / `DashCooldown` / `DashRefillCooldown` | `.15f` / `.2f` / `.1f` | |
| `Gravity` / `MaxFall` / `MaxRun` / `JumpSpeed` | `900` / `160` / `90` / `-105` | |

**Matt Thorson, thread de 12 de março de 2020** (espelho:
[threadreaderapp.com/thread/1238338574220546049](https://threadreaderapp.com/thread/1238338574220546049.html))
· Primária, declaração do desenvolvedor.

Lista dez mecanismos de perdão: coyote time, jump buffering, gravidade pela
metade no ápice do pulo, correção de quina no pulo e no dash, subida em
plataformas semissólidas, armazenamento de momento de plataforma móvel, wall jump
a 2 px da parede, super wall jump a *"I think it's 5 pixels"*, e devolução de
stamina em wall jump. Ele abre a thread dizendo *"I don't think we invented any of
these"* e hesita no número dos 5 px. **A hesitação faz parte da citação.**

**Uma discrepância que não resolvi.** A wiki da comunidade
([celeste.ink/wiki/Tech](https://celeste.ink/wiki/Tech), secundária) diz "5
coyote frames" e "buffer de 5 frames". O código diz `JumpGraceTime = 0.1f`, que a
60 fps são 6 frames. Ou a wiki conta de outro jeito (talvez sem contar o frame em
que se deixa o chão), ou os números divergem. **Cite `0.1 s`, que está no
código.** O buffer de input do Celeste vive em `VirtualButton`, cujo `bufferTime`
não consegui confirmar para o botão de pulo na fonte original.

**Limite grande.** Um jogo, 320×180, 60 fps, plataformer de precisão. Esses
valores **não são um padrão**. Copiá-los para um jogo com outra escala ou outra
taxa é cargo cult.

**Onde está o critério observável.** Não é "coyote time deve ser 0,1 s". É:
*existe uma constante nomeada para cada janela de perdão, seu valor está num só
lugar, e está declarado em segundos ou em frames com a taxa dita*. Isso um agente
confere lendo o código. "O pulo está bom" ninguém confere.

### 1.6 As palestras canônicas de juice não têm número — e tudo bem

**Jonasson, M. e Purho, P. (2012). "Juice it or lose it."** · Primária, palestra.
**Nijman, J. W. / Vlambeer (2013). "The art of screenshake."** · Primária,
palestra.

São listas de técnicas — cor, tweening, squash and stretch, partículas,
screenshake, hit stop, camera kick, recuo, permanência. **Nenhuma das duas
oferece limiar, duração ou magnitude.** Isso não é defeito delas; é o que elas
são.

**Pichlmair, M. e Johansen, M. "Designing Game Feel: A Survey."**
[arxiv.org/pdf/2011.09201](https://arxiv.org/pdf/2011.09201) · Secundária
acadêmica, catálogo · preprint de 2020, depois em IEEE Transactions on Games.

Cataloga as técnicas e cita nominalmente Nijman e Jonasson & Purho. Enquadra juice
como *amplificação* — *"providing excessive amounts of feedback in relation to
user input"* — e diz que *"juice requires exact timing"* sem dizer qual timing.

**Limite.** Taxonomia, não critério. Serve para nomear o que se está fazendo.
Não serve para aprovar nada. Se alguém apresentar um número atribuído a essas
palestras, o número foi inventado depois.

---

## 2. Consistência de direção de arte, de forma checável

### 2.1 Pixel art: o que tem critério de verdade

**Pedro Medeiros (saint11), "My Thoughts on Style Consistency."**
[saint11.art/blog/consistency](https://saint11.art/blog/consistency/) · Prática
declarada, de um artista de pixel art do Celeste · sem data no post. Li o texto
completo.

É a melhor fonte que encontrei, e é honesta sobre o que é: opinião informada por
produção, não estudo. O que ela oferece de conferível:

- **Escolher uma resolução de canvas e ficar nela.** No Celeste foi 320×180,
  escolhido porque ×6 dá exatamente 1920×1080, a resolução do Switch. *"This is
  important because when you rescale pixel art to non-integer resolutions you can
  get a jagged image."*
- **Desenhar num canvas na resolução nativa e escalar o canvas, não os sprites.**
  Ele diz explicitamente que jogos de pixel art *"in most cases, shouldn't scale
  their sprites to draw them on the screen."*
- **Escala inteira com nearest neighbor não perde nada.** *"Never use any
  smoothing algorithms for scaling pixel art, unless you know exactly what you are
  doing."*
- **Se precisar escalar sprites**: mesmo fator inteiro para todos; encaixar
  posição em `position * gameScale`; nunca desenhar nada menor que 1 px na tela.
- **Quando a tela não é múltiplo inteiro**, ele lista quatro saídas — recortar a
  câmera, escalar para cima e depois para baixo, letterbox, ou assumir os
  serrilhados — e **não diz qual é a certa**. A decisão é do projeto.
- **Cor:** paleta limitada é *uma* forma de consistência, não a única. E o achado
  contraintuitivo: em jogos sem paleta limitada, *"the most common color
  inconsistency (…) is that some sprites don't use colors that they could be
  using."* O defeito é subuso de cor existente, não excesso de cores.
- **Quarentena de estilos.** No Celeste havia três "mundos" declarados — Game
  (pixel art), UI (alta resolução), Map (3D) — e *"styles never leak from one
  world to another"*. O coração de cristal foi desenhado três vezes. Em Earthblade
  ele redesenhou um ícone flutuante em alta resolução ao perceber que, em pixel
  art, ele seria um objeto diegético dentro do mundo.
- Soluções nomeadas para dois problemas específicos: *layer sliding* (camadas
  deslizando em resolução de tela mas estabilizando em coordenada inteira ao
  parar) e *camera jitter* (canvas com área de sangria e offset
  `gameScale * ((float2)camera.position - (int2)camera.position - BLEED_SIZE / 2)`).

**Limite.** Nenhum número de tamanho de paleta. Nenhuma medição. A tese final é
*"intent is key"* — quebrar a regra deliberadamente é permitido. É ensaio de
profissional, não literatura com evidência.

### 2.2 A ferramenta impõe uma parte do critério

**Aseprite — conceito de Sprite.**
[aseprite-aseprite.mintlify.app/concepts/sprites](https://aseprite-aseprite.mintlify.app/concepts/sprites)
· Documentação da ferramenta · sem data.

Cada sprite tem dimensão fixa, um color mode e um `pixelRatio` (`Size{1,1}` por
padrão; `Size{3,2}` para emular pixels não quadrados de sistemas retrô). Um
documento = uma grade de pixels.

A confirmação de que **densidade mista não acontece por acidente**: no fórum
oficial, à pergunta direta sobre camadas com tamanhos de pixel diferentes no mesmo
canvas, a resposta é *"No, it is not possible"*, com a ressalva de que Tile Layers
no 1.3 aproximam o efeito quando os "pixels" maiores são múltiplos inteiros dos
menores.
[community.aseprite.org/t/.../15195](https://community.aseprite.org/t/is-it-possible-to-have-layers-of-different-pixel-size-in-the-same-canvas/15195)
· Secundária, resposta de usuário do fórum, agosto de 2022.

**Limite.** A documentação estabelece que a densidade mista é uma decisão
*entre arquivos*, tomada no motor — logo, auditável no motor. Não estabelece que
ela seja errada.

### 2.3 Restrições de hardware: onde limite de paleta é fato, não gosto

Se o alvo é um sistema real, o número existe e é verificável.

**NESdev Wiki — PPU palettes.**
[nesdev.org/wiki/PPU_palettes](https://www.nesdev.org/wiki/PPU_palettes) ·
Secundária (wiki comunitária de engenharia reversa, tratada como autoritativa pela
cena de homebrew).

64 saídas de cor possíveis. Fundo e sprites têm **4 paletas de 4 cores cada**. A
entrada 0 de cada paleta é transparente. *"A single element on the screen can only
use a single palette"* — para o fundo, normalmente uma região de 16×16 px; para
sprites, um objeto de 8×8 ou 8×16.

**Pan Docs — Graphics e Palettes (Game Boy).**
[gbdev.io/pandocs/Palettes.html](https://gbdev.io/pandocs/Palettes.html) ·
Secundária, mesma natureza.

Tiles 8×8, 2 bits por pixel. O Game Boy monocromático tem **uma** paleta de fundo
e **duas** de objeto, 4 tons cada, com o índice 0 transparente para objetos. O
Color tem 8 e 8, em RGB555.

**Limite.** Esses números valem **se e somente se** o projeto declarar esse alvo.
Não são uma regra geral de pixel art. Um jogo em Canvas a 320×180 não herda o
limite de 4 cores por tile do NES.

### 2.4 Arte não-pixel: escala, pivot, unidade

Aqui a pesquisa voltou quase vazia, e é importante dizer isso em vez de preencher.

**Unity — Sprite texture Import Settings.**
[docs.unity3d.com/Manual/texture-type-sprite.html](https://docs.unity3d.com/Manual/texture-type-sprite.html)
· Primária, documentação do fornecedor.

Documenta **Pixels Per Unit**: *"The number of pixels of width/height in the
Sprite image that correspond to one distance unit in world space."* Isso é
definição, e é conferível: um projeto tem um PPU declarado e cada asset tem o seu.

**O que a Unity não documenta.** A convenção "1 unidade = 1 metro" é
universalmente repetida, mas **não a encontrei em documentação da Unity nesta
passagem** — ela aparece em respostas de fórum e do StackExchange, onde é
apresentada corretamente como convenção: *"units in Unity are arbitrary (…) the
most common interpretation is that 1 unit means 1 meter, but that's just the most
commonly agreed upon value."* O argumento físico (a simulação se comporta melhor
perto da escala de 1 metro, e o padrão de 100 PPU existe para que a física não
mova objetos centenas de unidades por frame) também vem de fórum, não de doc.

**Não encontrei nenhuma fonte citável com números para convenção de pivot,
unidade de medida ou consistência de escala em arte não-pixel.** Não a encontrei
e não vou inventá-la. A busca desta passagem foi centrada em pixel art e não
esgotou a documentação de motores.

### 2.5 O que dá para transformar em critério observável mesmo assim

Nenhuma autoridade externa é necessária para checar **conformidade com o que o
projeto declarou**. Esses critérios são auto-suficientes:

| Critério | Como se confere |
| --- | --- |
| A resolução de canvas está declarada | Está escrita num arquivo do projeto |
| A escala tela÷canvas é inteira, ou o projeto declara qual das quatro saídas do saint11 escolheu | Aritmética + leitura |
| Todos os assets de um mesmo "mundo" declarado usam o mesmo fator inteiro | Script que compara metadados |
| Cada cor RGBA usada consta da paleta declarada | Script que varre os arquivos |
| O PPU do projeto está declarado e cada asset importado bate com ele | Leitura dos import settings |
| Existe uma lista de "mundos" de estilo e nenhum asset aparece em dois | Inspeção |

Note o que mudou: o critério não é *"poucas cores"* (opinião), é *"bate com a
paleta declarada"* (conferível). Não é *"escala consistente"*, é *"mesmo fator
inteiro dentro do mundo declarado"*. O projeto fornece o número; a checklist
confere a conformidade.

---

## 3. Orçamento de performance com números

### 3.1 A aritmética, e quem a estabelece como prática

**Unity — "Best practices for profiling game performance."**
[unity.com/how-to/best-practices-for-profiling-game-performance](https://unity.com/how-to/best-practices-for-profiling-game-performance)
· Primária, documentação do fornecedor.

A parte que é aritmética e a parte que é prática, separadas pela própria Unity:

- *"as a developer, it's generally recommended to use frame time in milliseconds
  instead"* de fps. 30 fps → menos de 33,33 ms; 60 fps → 16,66 ms.
- E então a regra de produção, que **não** é aritmética: *"A general tip to
  combat device thermal issues over extended play times is to leave a frame idle
  time of around 35%."* Isso dá ~22 ms de orçamento para alvo de 30 fps e 10,83 ms
  para 60 fps em mobile. A Unity acrescenta que 60 fps em mobile *"is difficult to
  achieve on many mobile devices and would drain the battery twice as fast"*, e
  que por isso muitos jogos mobile miram 30.

**Limite.** Os 35% são dados como *"a general tip"*, sem medição citada. É
recomendação de fornecedor, não resultado. É mobile.

**Google — "Get started with game development in Unity", Android game
development.**
[developer.android.com/games/engines/unity/start-in-unity](https://developer.android.com/games/engines/unity/start-in-unity)
· Primária, documentação da plataforma.

*"To prevent overheating on Android devices, target frame time values of under 21
milliseconds on average"*, com 33 ms como o teto duro; 10 ms para 60 Hz e 5 ms
para 120 Hz se você quiser essas taxas. E o comportamento que torna o orçamento
não-linear: com VSync forçado, se você não alcança 60 fps é jogado para 30; se não
alcança 30, para 15.

**Limite.** Android. Os 21 ms aparecem sem experimento citado.

**Epic — Unreal Engine, profiling.**
[docs.unrealengine.com/4.27/en-US/TestingAndOptimization/PerformanceAndProfiling/ProfilingStereoRendering](https://docs.unrealengine.com/4.27/en-US/TestingAndOptimization/PerformanceAndProfiling/ProfilingStereoRendering/)
· Primária, documentação do fornecedor.

`stat unit` devolve Frame, Game, Draw, GPU em ms, mais Draws e Primitives. A
triagem documentada é qualitativa e útil: se Frame ≈ Game, o gargalo é a thread de
jogo; se Frame ≈ Draw, é a thread de renderização; se Draw está alto, *"draw call
count may need to be reduced."* A página de estéreo dá o único número orçamentário
que achei em doc da Epic: o compositor pode levar até 1 ms, *"which means there is
one less millisecond per frame for an application to use"*, e o alvo deve ser
*"lower than 1 second divided by the number of frames (minus 1 for the
compositor), to account for occasional hitches."*

**Limite.** Página de VR. A Epic documenta a ferramenta e a triagem, **não** um
orçamento em ms por subsistema.

### 3.2 Draw calls: o ponto mais fraco de todo este documento

**Nenhum fornecedor de motor publica um orçamento numérico de draw calls.** Isso
foi o que a pesquisa devolveu, e é um resultado.

Os números que circulam vêm de dois lugares:

- [gamedeveloper.com — "Unity CPU Optimization: Is Your Game… Draw Call
  Bound?"](https://www.gamedeveloper.com/programming/unity-cpu-optimization-is-your-game-draw-call-bound-):
  menos de 200 draw calls em mobile, menos de 2000 em desktop, custo de renderização
  na main thread abaixo de 5 ms ou 1/3 do orçamento. O autor **rotula os próprios
  números** de *"guesstimates"* e fecha com *"these numbers have served me well."*
  Prática declarada, honestamente etiquetada como tal.
- Blog de agência repetindo "abaixo de 150 draw calls, abaixo de 80 SetPass calls,
  abaixo de 2× de overdraw" sem citar nada. Ver seção 6.

**O que é defensável.** A Unity documenta que o Rendering Profiler mostra batches
e SetPass calls por frame e que o Frame Debugger mostra quais batches a render
thread emite; a Epic documenta `stat scenerendering` e `stat gpu`. Logo o critério
observável é **"o número está registrado por cena e por build, e não regride"** —
não "está abaixo de N". A ferramenta existe; a constante não.

### 3.3 Percentis: quem defende medir p95/p99, e por quê

Esta parte tem origem clara e é o achado mais forte do tópico 3.

**Scott Wasson, The Tech Report, "Inside the second: A new look at game
benchmarking", 8 de setembro de 2011.** Republicado em
[techreport.com/review/inside-the-second-gaming-performance-with-todays-cpus](https://techreport.com/review/inside-the-second-gaming-performance-with-todays-cpus/)
· Primária (metodologia original do autor) · setembro de 2011.

O raciocínio, nas palavras dele: *"FPS averages summarize performance over a
relatively long span of time. It's quite possible to have lots of slowdowns and
performance hiccups during the period in question and still end up with an average
frame rate that seems quite good. In other words, the FPS averages we (and
everyone else) had been dishing out to readers for years weren't very helpful—and
were potentially misleading."* A solução foi tomada de empréstimo: *"a new
approach, borrowed from the world of server benchmarking, that focuses on the
actual problem at hand: frame latencies."* Daí o **99º percentil de frame time**.

E ele documenta o próprio limite do instrumento — o que é raro o bastante para
merecer citação: Fraps e FCAT *"are both accurate for what they measure; they just
measure different points in the frame production process"*, e por isso ele filtra
o Fraps com média móvel de três frames, para dar conta da fila de submissão de
três frames do Direct3D.
[techreport.com/blog/is-fcat-more-accurate-than-fraps-for-frame-time-measurements](https://techreport.com/blog/is-fcat-more-accurate-than-fraps-for-frame-time-measurements/)

**Limite.** É jornalismo de hardware para PC, não estudo revisado por pares, e é
sobre bancada de teste, não telemetria de jogadores. Mas é a origem rastreável da
prática inteira.

**Google — Android, "Frame Rate".**
[developer.android.com/games/optimize/refreshrate](https://developer.android.com/games/optimize/refreshrate)
· Primária, documentação da plataforma.

Uma plataforma dizendo para medir percentil, com nome de ferramenta:

- **P90 FPS** — *"consistent baseline"*. Os 10% de frames mais lentos ficam
  abaixo. *"If your P90 frame rate is high and close to your average, the game is
  running consistently well for the vast majority of the session."*
- **P99 FPS** — *"stutter indicator"*. Isola o 1% mais lento. *"This metric is
  essential for catching micro-stutters, asset-loading delays, and sudden
  asset-heavy rendering spikes that cause visible hitches."*
- Como medir: `dumpsys surfaceflinger timestats`, histograma `presentToPresent`.

**Limite.** Android. Mas é a citação mais forte que existe para a *prática*: um
fornecedor de plataforma prescrevendo percentil, explicando o que cada um detecta
e apontando a ferramenta.

**Um cuidado de definição que é ele próprio um critério.**
[damagelabs.com — "Inside the second: where things stand today"](https://www.damagelabs.com/p/inside-the-second-where-things-stand)
· Secundária, jornalismo especializado na linhagem do Wasson.

Documenta que **três métricas diferentes atendem pelo nome "1% low"**: o 99º
percentil de frame time convertido em FPS (que *exclui* o 1% pior), a média do 1%
de frames mais lentos (que *foca* no 1% pior), e outras. São coisas distintas e
dão números distintos. **"1% low" sem definição declarada não é critério.** Isso é
conferível por construção, sem precisar confiar na fonte. Se a pesquisa recusa que três métricas com o mesmo nome sejam um critério, o item do craft nomeia as métricas que a pesquisa já recusa. Nome no disco não é a métrica. Sem chave `métricas`.

Um alerta metodológico correlato — calcular percentis sobre os frames brutos
agrupados, não sobre médias de execuções, e não suavizar antes de calcular — vem
de [gamelandmag.com](https://www.gamelandmag.com/repeatable-frame-time-benchmarking-for-accurate-1-and-01-lows/),
**blog sem fonte primária**. É coerente com o método do Wasson, mas trate como
hipótese a conferir, não como regra citável.

### 3.4 Memória de textura

**Não encontrei orçamento de memória de textura publicado por fornecedor.** Os
números que circulam (250–400 MB de textura em mobile, 1–4 GB de VRAM em desktop)
vêm de blog de agência sem fonte — seção 6. Esta passagem de pesquisa não
investigou a fundo os limites de memória documentados por plataforma (jetsam no
iOS, heap por app no Android), que seriam o lugar certo para procurar.

---

## 4. Legibilidade de interface, com critério mensurável

### 4.1 WCAG: o que ela diz, e por que caminho ela chega (ou não) num jogo

**W3C — Web Content Accessibility Guidelines (WCAG) 2.2, Success Criterion 1.4.3
Contrast (Minimum), Nível AA.**
[w3.org/TR/WCAG22](https://www.w3.org/TR/WCAG22/Overview.html) · Primária,
normativa · Recomendação W3C.

Texto normativo: razão de contraste de pelo menos **4,5:1**, com três exceções —
texto de grande escala, que exige **3:1**; texto incidental (componente de
interface inativo, decoração pura, invisível, ou *"part of a picture that contains
significant other visual content"*); e logotipos, que não têm requisito nenhum.

"Grande escala" é definido normativamente **em pontos**: 18 pt, ou 14 pt em
negrito. O documento *Understanding* (informativo, não normativo) converte:
*"The ratio between sizes in points and CSS pixels is 1pt = 1.333px, therefore
14pt and 18pt are equivalent to approximately 18.5px and 24px."*
[w3.org/WAI/WCAG22/Understanding/contrast-minimum.html](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

Vale registrar de onde o W3C tirou o corte de tamanho: das diretrizes de letra
grande da American Printing House for the Blind e da Library of Congress, citadas
no Understanding. E o próprio W3C hedge: *"'18 point' and 'bold' can both have
different meanings in different fonts."*

**O limite de escopo, que é o ponto central deste tópico.** WCAG é para **conteúdo
web**. O caminho pelo qual seus números alcançam software não-web é:

WCAG → **WCAG2ICT** (W3C Working Group Note) → **EN 301 549**, cláusula 11
"Non-web software" → Diretivas (UE) 2016/2102 (sites e apps do setor público) e
(UE) 2019/882 (European Accessibility Act).

**ETSI — EN 301 549 V4.1.1, "Accessibility requirements for ICT products and
services."**
[etsi.org/deliver/etsi_en/301500_301599/301549/04.01.01_60/en_301549v040101p.pdf](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/04.01.01_60/en_301549v040101p.pdf)
· Primária, norma harmonizada.

E aqui está o detalhe mais interessante que a pesquisa devolveu: a própria norma
**cita jogos como exceção**. No critério de reflow (11.1.4.10), a nota diz que
exemplos de conteúdo que exigem layout bidimensional são *"images, maps, diagrams,
video, games, presentations, data tables"*. Ou seja: quando a norma que importa a
WCAG para software encontra jogos, ela abre exceção. Isso é evidência documental
de que a transposição não é automática.

**Limite honesto.** Verifiquei que a EN 301 549 existe, incorpora critérios da
WCAG para software não-web na cláusula 11 e sustenta aquelas duas Diretivas. **Não
li os Anexos ZA/ZB nem determinei se um jogo comercial específico está no escopo
do EAA.** Isso é questão jurídica e não estou respondendo a ela. As páginas de
userway, audioeye e vispero que apareceram na busca são marketing de fornecedores
de acessibilidade — usei só como orientação; o que sustenta o parágrafo é o PDF da
ETSI e a adoção canadense da norma.

### 4.2 Os números que jogos de fato usam

**Microsoft — Xbox Accessibility Guideline 101: Text display.**
[learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/101](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/101)
· Primária, documentação do fornecedor de plataforma.

Tamanho **mínimo padrão no lançamento do jogo**:

| Contexto | Mínimo |
| --- | --- |
| Console | 26 px @1080p · 52 px @4K |
| PC / VR | 18 px @1080p · 36 px @4K |
| Mobile / Game Streaming | 18 px @100 DPI · 36 px @200 DPI · 72 px @400 DPI, escalando linearmente |

Mais: o jogador deve poder **redimensionar até 200%** dos mínimos *"without the
loss of content, functionality, or meaning"*; texto que ultrapassa a tela precisa
de forma de leitura; não se pode exigir rolagem nas duas direções ao mesmo tempo
(numa direção está ok); e reduzir abaixo do mínimo é permitido a critério do
jogador.

**Microsoft — Xbox Accessibility Guideline 102: Contrast.**
[learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/102](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/102)
· Primária. Li a página inteira.

**Esta é a melhor fonte que existe para "WCAG traduzida para jogos"**, porque faz
a tradução explicitamente e redefine o termo que não sobrevive à transposição:

| Elemento | Razão |
| --- | --- |
| Texto/elemento de tamanho padrão | 4,5:1 |
| Texto/elemento de grande escala | 3:1 |
| Texto de elemento inativo | 3:1 |
| Placeholder / campo de entrada | 4,5:1 (3:1 se grande escala) |
| Modo de alto contraste | 7:1 para **todos** os elementos |

E "grande escala" deixa de ser 18 pt e vira px por plataforma: **console 52 px
@1080p; PC/VR 36 px @1080p; mobile 36 px @100 DPI**.

Duas regras que são especificamente de jogo e especificamente conferíveis:

- *"When text is displayed over a non-solid color background, the text contrast
  ratio should be measured between the text and the **lowest contrasting area** of
  the background."* Resolve o problema que a web não tem: o fundo se mexe.
- *"Images shouldn't contain text except for Logotypes"* — porque texto dentro de
  imagem não pode ser reajustado para atingir contraste nem lido por narrador.

Mantém as isenções da WCAG (logotipo, decoração pura). Nomeia ferramentas de
medição: Accessibility Insights for Windows, Colour Contrast Analyser.

**Microsoft — XAG 104: legendas.**
[learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104)
· Primária.

Legendas devem atender ao mínimo da XAG 101, mas *"developers are encouraged to
offer larger minimum default sizes for caption and subtitle text to facilitate ease
of rapid reading"* — porque ficam pouco tempo na tela. Escalável a ≥200%. Evitar
linhas com mais de **40 caracteres**. No máximo **2 linhas** na tela (3 em casos
excepcionais). Quebras de linha manuais, em pontos editorialmente sensatos.
Caixa mista. Ao menos uma opção sans serif. Fundo sólido configurável pelo
jogador, com **opacidade ajustável de 0 a 100**.

**Limite comum às três.** São *guidelines* publicadas. **Não verifiquei se alguma
delas é requisito de certificação do Xbox** — os requisitos de certificação estão
sob NDA e não tenho acesso. Não escreva "a Microsoft exige". Escreva "a Microsoft
publica, na XAG 10x".

**Game Accessibility Guidelines — "Use an easily readable default font size."**
[gameaccessibilityguidelines.com/use-an-easily-readable-default-font-size](https://gameaccessibilityguidelines.com/use-an-easily-readable-default-font-size/)
· Secundária, consórcio de indústria.

A origem do "28 px", declarada pela própria página: *"Amazon TV have 10-foot-UI
guidelines that include text size recommendations, of 28px minimum when viewed on a
1080p screen."* E o raciocínio, que é honesto: isso *"tallies for what would be
expected for someone with 20/20 vision while using the Snellen Chart"*, e
justamente por isso *"because it does not take any degree of vision impairment into
account, use 28px as a minimum rather than a target, aim to exceed it wherever
possible."*

**Limite.** É derivação de uma diretriz de TV, não resultado de pesquisa em jogos.
As citações ilustrativas na página são comentários do Reddit — anedota, apresentada
como anedota.

**Amazon — Design and User Experience Guidelines (Fire TV).**
[developer.amazon.com/docs/fire-tv/design-and-user-experience-guidelines.html](https://developer.amazon.com/docs/fire-tv/design-and-user-experience-guidelines.html)
· Primária, a origem do 28 px.

*"Because television screens must be read from across the room, use larger type
sizes for body text (at least 14sp, which is approximately 19px on 720p, 28px on
1080p)."*

**A divergência que precisa ser citada junto.** Microsoft diz 26 px @1080p em
console. Amazon diz 28 px @1080p em TV. Mesma ordem de grandeza, dois fornecedores,
**nenhum dos dois publica o experimento**. A forma honesta de citar é a faixa e a
procedência, não um número escolhido.

**Amazon — Test Criteria for Amazon Appstore Apps.**
[developer.amazon.com/docs/app-testing/test-criteria.html](https://developer.amazon.com/docs/app-testing/test-criteria.html)
· Primária.

Este é o gênero exato de artefato que uma checklist observável quer imitar — teste
e resultado esperado, escritos como teste:

> **Test:** Identify all areas of the app's core functionality that require text
> entry, as well as observing in-app text from approximately 10 feet away.
> **Expected Results:** UI components (menus, buttons, images) must be large enough
> and spaced far enough apart to be read from approximately 10 feet away.

E o de safe area: *"Apps should occupy 90% of the screen to be fully compatible (…)
but apps can still pass as long as they fill 80% of the screen and are centered."*

### 4.3 Safe areas de TV: o padrão existe, e o número que todo mundo usa está velho

**SMPTE ST 2046-1 (2009).** Não li a norma (paywall). Li o explicador da NAB,
["Television Safe Areas Redefined"](https://nab.org/xert/scitech/pdfs/tv031510.pdf)
· Secundária, mas de associação de radiodifusores · março de 2010.

- **Safe Action Area = 93% da largura × 93% da altura** da Production Aperture,
  concêntrica.
- **Safe Title Area = 90% × 90%.**
- Histórico: SMPTE RP 8 (1961) definiu Safe Title como 80%×80%; RP 13 (1963)
  definiu Safe Action como 90%×90%; fundidas em 1978; substituídas em 2009 por causa
  dos displays de matriz fixa. SMPTE RP 2046-2 trata de 16:9 exibido em 4:3 e define
  só 90%/90%.

**Consequência.** **90/80 é a prática de 1961–63, retirada.** Quem usa 90/80 hoje
está citando norma superada.

**EBU R95 — 16:9 Safe Areas.** Li via cópia no Scribd do PDF da EBU
([scribd.com/document/383445980](https://www.scribd.com/document/383445980/EBU-Technical-Recommendation-R95-2000-pdf))
· Primária em conteúdo, **cópia não oficial** — confira em tech.ebu.ch antes de
citar normativamente.

Margem de action safe de 3,5% em todas as bordas; graphics safe de 5% vertical e
10% horizontal. **E, o mais valioso, a premissa empírica declarada:** *"the safe
areas have been specified on the premise that the overscan on modern domestic
television receiver displays will normally be in the range 3.5 ± 1% of overall
picture width or height, but on any one picture edge, the over-scan will not exceed
4%."*

Isso é o oposto de folclore: a norma diz de qual medição o número saiu.

**Convergência útil.** SMPTE title safe (90%) e a regra da Amazon Fire TV (nada nos
5% externos de qualquer borda; texto e item focado inteiramente nos 90% internos)
dão o mesmo retângulo. **Limite:** só vale para saída em TV. Um build de Steam não
herda isso.

### 4.4 Legendas: os padrões que existem, e o que eles escolhem não dizer

**BBC Subtitle Guidelines.**
[bbc.co.uk/accessibility/forproducts/guides/subtitles](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/)
· Primária, emissora.

O achado mais transponível para jogos: o tamanho é **relativo à altura do vídeo**,
não em pixels.

- Autoria: altura de linha entre **7% e 8% da altura ativa do vídeo** para 16:9,
  4:3 e 1:1. Entre **3,9% e 4,5%** para 9:16.
- Apresentação: multiplicador de **0,6 a 0,8** na maioria das telas; **×1** em
  celulares pequenos; tabela por dispositivo (TVs de 32"–42" → ×0,67, faixa ×0,5–1).
- E a regra de fallback, que é boa engenharia: quando o processador não consegue
  determinar o tamanho físico da tela, *"it should use the unmodified authored size
  to mitigate the risk of illegibly small text (i.e. default to a multiplier of 1)."*
  Na dúvida, erra para o lado grande.

O raciocínio está declarado: a altura física do vídeo na tela é o determinante,
mas na prática o processador raramente a conhece.

**Limite.** É para entrega broadcast em EBU-TT-D e pressupõe um player que escala.
Um jogo precisa implementar a escala ele mesmo.

**Netflix — Timed Text Style Guide: General Requirements.**
[partnerhelp.netflixstudios.com/hc/en-us/articles/215758617](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements)
· Primária, especificação de fornecedor.

*"Only use percentage values. Do not use pixel values."* `tts:fontSize` definido
como 100%. Tamanho *"relative to video resolution and ability to fit 42 characters
across the screen"*. Centralizado, topo ou base, evitando sobrepor texto na
imagem.

**Convergência que vale registrar:** Netflix diz 42 caracteres por linha, Microsoft
diz evitar mais de 40. Duas fontes independentes, mesma ordem. **Limite:** é spec de
entrega para fornecedores de legenda, não estudo de legibilidade, e não diz nada
sobre contraste.

**FCC — 47 CFR § 79.1(j)(2) e § 79.103.**
[law.cornell.edu/cfr/text/47/79.1](https://www.law.cornell.edu/cfr/text/47/79.1) ·
[law.cornell.edu/cfr/text/47/79.103](https://www.law.cornell.edu/cfr/text/47/79.103)
· Primária, regulação federal dos EUA.

O regulador **se recusa a dar um tamanho**, e isso é instrutivo. Os padrões de
qualidade em § 79.1(j)(2) são precisão, sincronia, completude e posicionamento; no
item de posicionamento a exigência de tamanho é qualitativa: *"Caption font shall be
sized appropriately for legibility."* Mais: as legendas *"shall not block other
important visual content on the screen, including (…) character faces, featured
text (…) and other information that is essential to understanding a program's
content"*, e não podem se sobrepor entre si nem sair da borda da tela.

Onde a FCC **dá** número, é sobre **ajustabilidade**, não sobre valor: § 79.103(a)(4)
exige que aparelhos permitam ao usuário variar o tamanho *"from 50% of the default
character size to 200% of the default character size"*. Também: 8 fontes do CEA-708,
paleta de ao menos 8 cores de fundo, e opacidade de fundo opaca/semitransparente/
transparente.

**A lição de método.** Um regulador com poder de multar, olhando um problema de
legibilidade por décadas, decidiu que o critério defensável é **a faixa de
configuração** (50%–200%), não o tamanho absoluto. Isso bate exatamente com o "até
200%" da XAG 101. Duas autoridades independentes chegando ao mesmo formato de
critério é evidência de que **o formato certo é a faixa de ajuste, não o valor**.

---

## 5. Playtest com metodologia

### 5.1 Os "5 usuários": o que o artigo original realmente conclui

Este é o achado que mais muda a prática, e é uma correção de leitura.

**Nielsen, J. e Landauer, T. K. (1993). "A mathematical model of the finding of
usability problems."** INTERCHI '93, pp. 206–213.
[doi.org/10.1145/169059.169166](https://doi.org/10.1145/169059.169166) ·
**Primária** · abril de 1993. Li o texto completo.

O modelo: descoberta de problemas de usabilidade como processo de Poisson, ajustado
a 11 estudos / 13 conjuntos de dados. Problemas encontrados por *i* avaliadores =
`N(1 - (1-λ)^i)`.

**A conclusão do próprio artigo não é "cinco".** No abstract:

> *"For a 'medium' example, we estimate that **16 evaluations** would be worth
> their cost, with maximum benefit/cost ratio at **four**."*

E na discussão os autores registram explicitamente a tensão: *"These optimum
numbers of evaluators/test users are much larger than obtained for our earlier
'discount usability engineering' recommendation of using about five heuristic
evaluators"* — e justificam o número menor por **design iterativo** (não vale
avaliar até o fim uma versão que vai mudar), não por cobertura. Com um custo fixo de
$20.000 por estudo, o pico de benefício/custo vai para 6,7 usuários de teste e 7,9
avaliadores heurísticos.

**Onde nasce o "cinco".** Em **Nielsen, J., "Why You Only Need to Test with 5
Users", NN/g, 19 de março de 2000** — artigo de divulgação do mesmo autor, sete anos
depois. Secundária. É ali que o número virou regra. A MeasuringU chama o gráfico
desse artigo de *"parabola of optimism"*.
[measuringu.com/five-history](https://measuringu.com/five-history/) · Secundária,
história do número.

**Os 85% vêm de λ ≈ 0,31** — a probabilidade média de um usuário encontrar um dado
problema, ajustada sobre aqueles 13 conjuntos de dados de 1993: suítes de escritório,
sistema bancário, interfaces de caractere. **Nenhum jogo.**

### 5.2 As críticas, e o que cada uma mediu

**Spool, J. e Schroeder, W. (2001). "Testing web sites: Five users is nowhere near
enough."** CHI '01 Extended Abstracts.
[PDF](http://englishtamucc.pbworks.com/w/file/fetch/140271369/Spoolschroeder_5usersnotenough.pdf)
· Primária · 2001. Li o PDF.

Quatro sites de e-commerce, tarefas abertas (usuários navegando livremente por até
quatro sites atrás de CDs específicos). λ medido: **nenhum acima de 0,16**, contra
o 0,31 que Nielsen ajustou. Consequência: após cinco usuários tinham ~35% dos
problemas. E o detalhe que dói: problemas graves que **impediam a compra pretendida**
apareceram pela primeira vez nos testes **13 e 15**. *"Is halfway through 'early?'"*

Eles não jogam a fórmula fora: *"the formula given in [3] can still be usefully
applied, but more work needs to be done in determining an appropriate value of L."*
**A crítica é ao valor de λ, não ao modelo.**

**Faulkner, L. (2003). "Beyond the five-user assumption: Benefits of increased sample
sizes in usability testing."** Behavior Research Methods, Instruments & Computers
35(3), 379–383. · **Não li o original** — conheço via MeasuringU e resumos
secundários.

60 usuários, 100 reamostragens aleatórias por tamanho de amostra. Amostras de cinco:
média de 85%, **mas variação de 55% a 99%**. Amostras de dez: média de 95%, piso de
82%.

**A leitura correta.** Os 85% de Nielsen não estão errados como média. Estão errados
como *promessa*. O que você obtém depende de **quais** cinco pessoas você recrutou, e
o pior caso plausível é pouco mais da metade dos problemas.

**Perfetti e Landesman (2001):** após 18 usuários ainda descobriam problemas sérios,
com menos da metade de ~600 problemas estimados encontrados. · Secundária apenas.

**Bevan, Barnum, Cockton, Nielsen, Spool, Wixon (2003).** Painel na CHI 2003: *"The
'magic number 5': is it enough for web testing?"* Que o campo tenha feito um painel
com o próprio Nielsen na mesa já diz que o número é contestado dentro da disciplina.

**O que isso significa para um framework de jogos.** "Cinco playtesters" não é
critério. Ninguém publicou λ para playtest de jogo. O critério defensável é
processual: **medir a própria curva** — quantos problemas *novos* cada testador
adicional traz — e parar quando testadores novos param de trazer problemas novos.

### 5.3 RITE: o método que tem regra de parada

**Medlock, M. C., Wixon, D., Terrano, M., Romero, R. L., Fulton, B. (2002). "Using
the RITE method to improve products: a definition and a case study."** Usability
Professionals Association.
[PDF](https://www.jpattonassociates.com/wp-content/uploads/2015/04/rite_method.pdf)
· **Primária** · 2002. Li o PDF. Autores da Microsoft Games Studios e da Ensemble
Studios.

Rapid Iterative Testing and Evaluation. A diferença em relação ao teste tradicional é
uma só: **muda-se o build assim que um problema é identificado e a solução está
clara** — às vezes depois de um único participante — e o build alterado é testado com
os participantes seguintes.

Estudo de caso: tutorial de Age of Empires II. 16 participantes (5 mulheres, 11
homens, 25–44 anos, sem experiência com RTS mas interessados). Fonte primária de
dados: observação do testador.

**A parte que vira critério é a etapa de verificação.** Segundo a MeasuringU
([measuringu.com/rite-method](https://measuringu.com/rite-method/), secundária), após
iterar por dez participantes, os **seis seguintes não exigiram nenhuma mudança**.
"N sessões consecutivas sem mudança necessária" é uma regra de parada observável — e
é o operacional exato de "parar quando a repetição para".

**Limites documentados** (MeasuringU, secundária): o RITE **não define quando parar
se você não vê problemas**; no estudo de caso da Citrix (Shirey et al.) o método
exigiu grande compromisso de tempo e envolvimento profundo do time de produto, e eles
rodaram só seis participantes. Estruturalmente, o RITE mistura pesquisa e design —
*"in some ways it represents a design method"* — então ele não te dá uma medição
limpa do design original.

**Uma advertência de fonte.** A página da Grokipedia sobre RITE apareceu na busca e
traz afirmações numéricas (por exemplo, "até 80% dos problemas corrigidos e
verificados") que **não consegui rastrear**. Grokipedia é enciclopédia gerada por
LLM. Não a use como evidência.

### 5.4 Valve: hipótese e experimento como formato

**Valve — deck de slides do Steam Dev Days.**
[media.steampowered.com/apps/steamdevdays/slides/data.pdf](http://media.steampowered.com/apps/steamdevdays/slides/data.pdf)
· Primária, artefato da própria empresa.

O enquadramento, textual: *"Game designs are hypotheses. Playtests are experiments.
Evaluate designs based off playtest results. Repeat."*

E a distinção metodológica que o deck faz explicitamente:

- **Observacional** — retrospectivo ou prospectivo; *"correlational not causal"*.
- **Experimento** — condição de controle e condição experimental; controlar variáveis
  de confusão; medir a variável de interesse.

Metodologias listadas: tradicionais (observação direta, relatos verbais, Q&As) e
técnicas (coleta de estatísticas, experimentos de design, surveys, medição
fisiológica).

Os exemplos trabalhados seguem uma cadeia fixa, e **é a cadeia que é o artefato
checável**. Para Left 4 Dead: problema explícito (jogadores deixando companheiros
morrerem) → evidência (surveys, Q&As, altas taxas de morte) → hipótese teórica (falta
de consciência da localização do companheiro) → medição (surveys, Q&As, taxas de
morte) → iteração (dar melhores pistas visuais de localização). Para Dota 2: reduzir
comunicação negativa, com banimentos de comunicação como hipótese e taxas de report,
ban e reincidência como medição.

**Critério observável derivado disso:** para cada achado de playtest, o registro
consegue nomear *o problema, a evidência, a hipótese e a medição*? Se não consegue,
é impressão, não achado.

**Mike Ambinder, via Steve Bromley**, 1 de setembro de 2011.
[stevebromley.com/blog/2011/09/01/valves-philosophy-with-user-research-in-games](https://www.stevebromley.com/blog/2011/09/01/valves-philosophy-with-user-research-in-games-habe-newell-and-mike-ambinder/)
· Secundária, mas citação direta por e-mail.

O antídoto contra a lenda de que a Valve testa tudo com biometria: *"Our most common
form of playtesting is direct observation followed by a brief survey and then Q&As.
We don't use biofeedback too much in our standard playtests."* E: *"We start
playtesting as early as we can—as soon as we have something playable. We'll start
with internal folks and then bring in external folks soon after."*

A palestra de biofeedback do Ambinder na GDC 2011 é primária mas é palestra, sem
dataset publicado — não cite números dela.

**Não encontrei metodologia de playtest publicada por Riot ou Blizzard** nesta
passagem de pesquisa.

### 5.5 Contar repetição em vez de reagir a cada comentário

**Procurei e não encontrei fonte que estabeleça isso como regra com limiar.** Não
existe, que eu tenha achado, um "aja quando três pessoas relatarem".

O que a literatura **sustenta indiretamente**, e é bastante:

- O modelo de Nielsen & Landauer é literalmente sobre contar **problemas distintos**
  em função do número de avaliadores. A unidade de análise é o problema, descoberto
  repetidamente — não o comentário.
- O resultado de variância da Faulkner (55%–99% para cinco usuários) é um argumento
  direto contra dar peso a um testador individual, e a favor de contar recorrência
  entre testadores.
- A etapa de verificação do RITE operacionaliza "parar quando a repetição para".
- A distinção correlacional × causal do deck da Valve é a mesma ideia em outra roupa:
  um comentário é observação, não causa demonstrada.

**Mas o limiar numérico não tem fonte.** Se este framework adotar um, ele precisa ser
declarado como decisão editorial deste estúdio — como a [barra de
acabamento](production-bar.md) já faz com a própria escada — e não como achado.

---

## 6. Números que circulam sem fonte primária

O que **não** pode ser citado como fato estabelecido, e o que dizer no lugar.

### 6.1 Latência e game feel

**"Jogadores percebem latência acima de 100 ms."**
Rastreia até Miller (1968), sobre feedback de tecla e caneta óptica em terminais de
1968, via a síntese de Nielsen para interfaces de diálogo. Nenhuma medição em jogo
estabelece isso. A literatura de jogos contradiz nos dois sentidos: ~15 ms detectáveis
por observadores treinados em head tracking (Mania et al.), jogadores de Minecraft
insensíveis a ~1 s (Hoßfeld et al.), e jogadores de CS:GO melhorando de desempenho
numa faixa em que dizem não perceber diferença (Liu et al. 2021).
**Diga em vez disso:** a sensibilidade depende da precisão e do prazo da ação
(Claypool & Claypool), e o intervalo publicado vai de 15 ms a 1 s.

**"Abaixo de 50 ms parece instantâneo, acima de 100 ms perceptível, 200 ms
arrastado."**
Atribuído a Swink, *Game Feel*. **Não verifiquei no original**; o preview do editor
não contém esses valores. Circula via uma resposta de StackExchange e blogs.
**Diga em vez disso:** "atribuído a Swink, não conferido no original" — ou confira o
livro.

**"A regra dos 100 ms é resultado de pesquisa sobre propriocepção."**
Afirmado por gamejuice.co.uk sem citar ninguém: *"Research on human perception places
the threshold at approximately 100 milliseconds."* A ideia subjacente é o processador
perceptual do Model Human Processor (Card, Moran e Newell, 1983), um modelo de 1983.
Não é medição em jogo, não é sobre propriocepção. Se a pesquisa recusa que a pendência seja medição em jogo, o `pending` do `craft` nomeia a medição que a pesquisa já recusa. Pesquisa no disco não é ofício observado. Sem chave `medição`.

**"Celeste tem 5 frames de coyote time."**
O código publicado diz `JumpGraceTime = 0.1f` — 6 frames a 60 fps. Os "5 frames"
vêm da wiki da comunidade. Não resolvi a divergência.
**Diga em vez disso:** `0.1 s`, citando `Source/Player/Player.cs`.

**Qualquer número atribuído a "Juice it or lose it" ou "The art of screenshake".**
Nenhuma das duas palestras dá limiar, duração ou magnitude. São listas de técnicas.

### 6.2 Arte

**"Nunca use mais de N cores em pixel art."**
Não encontrei nenhum estudo, guia sério ou norma que estabeleça um teto de paleta
para pixel art em geral. O saint11, a fonte mais próxima de autoridade, diz
explicitamente que paleta limitada é *uma* forma de consistência entre outras — e
aponta que o defeito mais comum é o contrário: sprites que **não reusam** cores que
já existem no projeto.
Paletas de hardware (4 cores por sub-paleta no NES, 4 tons no Game Boy) são reais e
citáveis, mas **só valem se o projeto declarar esse alvo**.

**"1 unidade Unity = 1 metro."**
Convenção real e útil, **mas não a achei em documentação da Unity**. As fontes são
fórum e StackExchange, que a apresentam corretamente como convenção: *"units in Unity
are arbitrary."* A Unity documenta o Pixels Per Unit; a interpretação métrica é do
ecossistema.

**Convenções numéricas de pivot e escala para arte não-pixel.**
Não encontrei nenhuma. Esta passagem de pesquisa não esgotou a documentação de
motores, mas também não vou inventar o que não achei.

### 6.3 Performance

**"Menos de 200 draw calls em mobile, menos de 2000 em desktop."**
O autor no gamedeveloper.com **rotula os próprios números** como *"guesstimates"* e
*"these numbers have served me well"*. É experiência declarada, e ele foi honesto.
Quem repete sem a etiqueta é que produz folclore.

**"Menos de 150 draw calls, menos de 80 SetPass calls, menos de 2× de overdraw."**
Blog de agência (game-ace.com), sem fonte. **Nenhum fornecedor de motor publica
orçamento numérico de draw calls.**

**"p50 < 14 ms, p95 < 18 ms, p99 < 25 ms para 60 fps" (e 28/36/50 ms para 30 fps).**
bugnet.io, blog sem fonte. O próprio artigo diz *"These are not universal
constants"*, mas não mostra derivação nem dados. Igualmente sem fonte, do mesmo
domínio: "uma regressão de p99 maior que 5 ms deve disparar alerta; uma de p50 maior
que 2 ms merece investigação".

**"250–400 MB de textura em mobile, 1–4 GB de VRAM em desktop."**
Blog de agência, sem fonte.

**"1% low."**
Três métricas diferentes usam esse nome. Sem definição declarada, não é critério.
**Diga em vez disso:** "99º percentil de frame time" ou "média do 1% de frames mais
lentos", explicitamente.

**Os 35% de idle da Unity e os 21 ms da Google** são recomendações de fornecedor sem
experimento citado. São citáveis **como recomendação do fornecedor** — que é bem
diferente de citá-las como resultado.

### 6.4 Interface

**"28 px é o mínimo de fonte em jogos."**
Origem: 14sp da Amazon Fire TV para apps de TV, convertido para 28 px em 1080p, e
repassado pelas Game Accessibility Guidelines. É número de 10-foot UI, não pesquisa em
jogos, e a Microsoft publica 26 px para console.
**Diga em vez disso:** a faixa 26–28 px @1080p para console/TV, com as duas
procedências e o aviso de que nenhuma das duas publicou o experimento.

**"WCAG exige 4,5:1 em jogos."**
WCAG é para conteúdo web. A ponte é WCAG2ICT → EN 301 549 cláusula 11 → Diretivas da
UE — e a própria EN 301 549 **lista jogos** entre o conteúdo que exige layout
bidimensional, abrindo exceção no critério de reflow.
**Diga em vez disso:** "a Microsoft adota, na XAG 102, os limiares 4,5:1 / 3:1 / 7:1
da WCAG, redefinindo 'texto grande' em px por plataforma."

**"Title safe é 90/80."**
É SMPTE RP 8 (1961) e RP 13 (1963), substituídas pela ST 2046-1 em 2009. O vigente é
**93% action / 90% title**.

**Alvos de contraste de 7:1 para texto e 10:1 para elementos pequenos de UI em TV.**
Aparecem em um blog de design (alicia.design) sem fonte. Note que 7:1 é o nível AAA
da WCAG e é o que a Microsoft reserva para **modo de alto contraste**, não para o
padrão.

### 6.5 Playtest

**"Cinco usuários encontram 85% dos problemas."**
O artigo-fonte conclui que **16 avaliações valem seu custo, com pico de
benefício/custo em 4**. Os 85% saem de λ=0,31, ajustado sobre 13 conjuntos de dados
não-jogos de 1993. Spool e Schroeder mediram λ ≤ 0,16 em e-commerce (≈35% após cinco
usuários; problemas graves aparecendo nos testes 13 e 15). Faulkner mediu a faixa real
de cinco usuários em 55%–99%.
**Ninguém publicou λ para playtest de jogo.** Os 85% não têm nenhuma validade para
jogos.

**"Reaja quando três (ou N) pessoas relatarem o mesmo problema."**
Não encontrei fonte alguma com limiar. A prática de contar recorrência é defensável
como síntese; o número é invenção.

**"A Valve testa com biometria."**
Ambinder, por escrito: biofeedback *"not too much in our standard playtests"*. O
padrão da casa é observação direta, survey curto e Q&A.

**"O RITE corrige e verifica até 80% dos problemas."**
Vi essa afirmação na Grokipedia (enciclopédia gerada por LLM) e não consegui
rastreá-la até o capítulo de *Cost-Justifying Usability* que ela cita.

### 6.6 Uma advertência sobre as próprias buscas

Boa parte do que a busca devolveu para esses temas é marketing de conteúdo ou texto
gerado por LLM: bugnet.io, kindatechnical.com, ilovesprites.com, pixnote.net,
game-ace.com, filemender.com, gamelandmag.com, altftool.com, testparty.ai,
closedcaptioncreator.com, recap-innovations.com, e a Grokipedia. Essas páginas são
fluentes, citam números com casas decimais e **não citam fontes**. Foram usadas aqui
só como ponteiro para as fontes reais; nenhuma afirmação deste documento se apoia
nelas.

O padrão a reconhecer: **quanto mais precisa a formulação e mais ausente a
procedência, maior a suspeita.** Fonte séria hedge. A EBU diz de qual medição de
overscan tirou os 3,5%. O Wasson explica por que filtra o Fraps com média de três
frames. Miller abre perguntando "response time to what?". O Thorson escreve "I think
it's 5 pixels". A Unity chama os 35% de "a general tip". O blog que diz
"p99 < 25 ms" não hedge nada.

---

## 7. O que dá para virar checklist agora

Resumo do que sobreviveu à triagem, separado pelo tipo de autoridade que sustenta.

**Números com norma ou regulação atrás:**

| Critério | Valor | Fonte |
| --- | --- | --- |
| Safe title area (saída em TV) | 90% × 90% | SMPTE ST 2046-1 |
| Safe action area (saída em TV) | 93% × 93% | SMPTE ST 2046-1 |
| Overscan presumido | 3,5% ± 1%, máx. 4% por borda | EBU R95 |
| Faixa de ajuste de tamanho de legenda | 50% a 200% do padrão | 47 CFR § 79.103(a)(4) |
| Contraste de texto (web) | 4,5:1 / 3:1 grande escala | WCAG 2.2 SC 1.4.3 |

**Números publicados por fornecedor de plataforma (guideline, não certificação
verificada):**

| Critério | Valor | Fonte |
| --- | --- | --- |
| Fonte mínima padrão, console | 26 px @1080p / 52 px @4K | Xbox XAG 101 |
| Fonte mínima padrão, PC/VR | 18 px @1080p / 36 px @4K | Xbox XAG 101 |
| Escalabilidade de texto | até 200% sem perda de conteúdo | Xbox XAG 101 |
| Contraste em jogo | 4,5:1 / 3:1 / 7:1 (alto contraste) | Xbox XAG 102 |
| "Texto grande" em console | 52 px @1080p | Xbox XAG 102 |
| Contraste sobre fundo variável | medir contra a área de **menor** contraste | Xbox XAG 102 |
| Linha de legenda | ≤ 40 caracteres, ≤ 2 linhas | Xbox XAG 104 |
| Linha de legenda | 42 caracteres na largura da tela | Netflix TTSG |
| Altura de linha de legenda | 7–8% da altura ativa do vídeo | BBC |
| Texto em TV | ≥ 14sp (~28 px @1080p) | Amazon Fire TV |
| Ocupação de tela em TV | 90% (80% ainda passa) | Amazon Appstore |
| Orçamento de frame | 33,33 ms @30 fps · 16,66 ms @60 fps | Unity |
| Orçamento com folga térmica mobile | ~22 ms @30 fps · ~10,83 ms @60 fps | Unity |
| Frame time médio em Android | < 21 ms | Google |
| Percentis a medir | P90 (baseline), P99 (stutter) | Google |

**Critérios que não precisam de autoridade externa** — conformidade com o que o
próprio projeto declarou, que é o formato mais robusto porque não depende de nenhum
número ser verdadeiro em geral:

- A resolução de canvas está declarada, e a escala tela÷canvas é inteira ou o projeto
  declara qual fallback escolheu.
- Cada cor usada consta da paleta declarada.
- Todo asset de um mesmo "mundo" de estilo usa o mesmo fator inteiro, e nenhum asset
  aparece em dois mundos.
- Cada janela de perdão tem constante nomeada, em um só lugar, com unidade declarada.
- Draw calls e frame time por cena estão registrados por build e comparados com o
  build anterior.
- Percentil está declarado por definição (99º percentil de frame time, ou média do 1%
  pior) e não pelo apelido.
- Cada achado de playtest registra problema, evidência, hipótese e medição.
- O playtest tem regra de parada declarada — N sessões consecutivas sem mudança
  necessária — em vez de número fixo de participantes.

**O que não tem critério e não deve fingir ter:** tamanho de paleta em geral,
orçamento de draw calls, orçamento de memória de textura, convenção de pivot e escala
em arte não-pixel, limiar de latência universal, número de playtesters, e limiar de
repetição de feedback.
