# Direção visual, câmera e performance

Entrada: referência aprovada, diferença percebida e percurso/câmera de comparação.

Com tela, a primeira superfície é a porta. Halo, vinheta e a chuva
da abertura são o primeiro quadro; a mostra lê a mesa vigente —
dusk cai mais denso e com mais estilhaço, calm mais folgado e
com menos risco — sem comer a seed. A ameaça
da mostra marca o trilho com o mesmo telegraph do campo; a live já
nomeava o perigo. Se o canvas declara `drawTelegraph`, o `art` nomeia o trilho que o telegraph já marca.
Marca no disco não é comparação em movimento. Sem chave `telegraph`. Se o canvas declara `drawVignette`, o `art` nomeia a vinheta que o recorte já marca. Recorte no disco não é comparação em movimento. Sem chave `vignette`. Se o sistema recusa que a paleta compartilhada seja o contrato, o `art` nomeia a paleta que o sistema já recusa. Lista no disco não é contrato. Sem chave `paleta`. O campo
começa depois do avanço.
Comparar só o meio da partida esconde a imagem que o jogador vê ao
abrir. Sem tela o headless já joga.

O harness lê paleta e art-bible vigentes com `art <projeto>`. Paleta no
código ou em `data/palettes.json` não é direção consistente — `consistent` é sempre falso. Rascunho
do `init` não conta. Sem declaração, `next` propõe `art.missing`.
`art` também nomeia as mesas de chuva que o disco já tem
(`intervalTicks`, `fallSpeed` e `hazardChance` em `data/`, `tables/` ou `content/`).
Mesa no disco não é volume nem comparação em movimento. Se a receita recusa que a mesa seja volume, o `art` nomeia o volume que a receita já recusa. Lista no disco não é comparação. Sem chave `volume`. Paleta sem
chuva continua direção declarada; chuva sem paleta não declara.
No starter, `look --from` / `--as` nasce um look que o jogo já pinta —
campo, cortina, a casca da página e os knobs (select, faixa, foco).
Se o `tools/new-look.*` nasce o look, o `art` nomeia o look que o disco já nasce.
Ferramenta no disco não é comparação em movimento. Sem chave `look`. Se o look recusa contraste, o `art` nomeia o contraste que o look já recusa. Alcance no disco não é comparação em movimento. Sem chave `contrast`. `pair --from` nasce look e chuva
no mesmo nome e `?mood=` aplica. `dusk` e `calm` já são o segundo
e o terceiro look; `calm` não é o `cooler` aplicado em `normal`.
`dusk` pinta orbe âmbar e estilhaço índigo; o campo continua
quente. `--as warmer` / `--as cooler` deslocam campo e orbe;
o estilhaço e o perigo permanecem — o fecho e o impacto
não herdam o eixo do orbe. A receita do art-bible nomeia
essas tintas e as janelas do campo (prática no orbe, folga
na corrente, fecho no perigo). A recuperação do dash veste
o apoio, não o orbe — a regra já diz vulnerável. Token no disco não é
comparação em movimento. No starter, halo e
vinheta dão volume ao recorte geométrico; com menos movimento
somem. Isso não é direção consistente.
depois de um `note`, `start` e `next` apontam esses comandos.
Ferramenta no disco não é alguém de fora nem comparação em movimento.

Leia [a qualidade](../references/quality.md) e os aprendizados de performance
do laboratório, quando existirem.
Reutilize materiais, modelos, efeitos, tokens e métodos coerentes com essa direção;
adapte seus consumidores antes de criar variantes paralelas. A instância canônica
é o design system do jogo (Art Bible); o contrato do estúdio está no
[design system do jogo](../references/game-design-system.md). Se o sistema recusa que o scanner certifique tokens, o `scan` nomeia os tokens que o sistema já recusa. Documento no disco não é aprovação artística. Sem chave `tokens`.

Quando o usuário aprovar uma referência durante criação/evolução, use `context
<projeto> --focus visual --event direction-approved` e sincronize a base documental
conforme [o roteiro](../references/project-audit.md#aprovação-de-direção-materializar-e-continuar).
Salvar a imagem e anunciar o que será construído deixa esse trabalho pendente.
Registre o alcance da aprovação; requisitos ou arquitetura ainda propostos mantêm esse estado.

Capture o antes em condições equivalentes: versão, resolução, dispositivo, entrada,
iluminação e trecho em movimento. Localize o gargalo pelo caminho real antes de
otimizar. Medição serve para escolher uma implementação melhor preservando arte e
jogabilidade. Não corte sombras, reflexos, transparência, textura, detalhes ou
animação como solução automática de FPS.

Trabalho dedicado a orçamento de quadro, pior percentil, engasgo de carregamento e
custo por ciclo de vida tem receita própria: [performance](performance.md), por
`--focus performance`. Aqui o piso é o inverso — a qualidade visual aprovada não é
moeda de troca por número.

Na câmera, observe antecipação de curvas/ameaças, oclusão do jogador, estabilidade,
escala e transição. No starter a câmera inclina para o que o trilho
já marca; não é punch. Lean no disco não é comparação em movimento. No mundo, compare silhueta, materiais, luz, sombras, efeitos e
coerência em movimento, não apenas a melhor screenshot. Feel da ação e mix da
consequência têm receitas próprias: [feel](feel.md), [áudio](audio.md). Não trate
partículas ou um loop de fundo como substituto desses focos.

Casos já documentados: nomes podem mudar após o carregamento do GLTF; culling deve
ser testado em todas as aberturas visíveis; animação em shader invalida suposições
de sombras estáticas. Reproduza a cena em vez de inferir a correção por nomes crus.

Ao modelar a partir de pranchas, preserve os originais e registre a variante usada.
Vistas geradas podem repetir acessórios ou divergir em perspectiva; construa um
volume coerente sem tratar a inconsistência como exigência geométrica. Confira
frente, perfis e costas após cada mudança estrutural. Curvas com espessura precisam
de terminais fechados quando representam tecido; hachuras devem permanecer na
superfície efetiva, inclusive em domos parciais. Compare o asset isolado e o elenco
na luz final: uma correção local não valida o enquadramento e a iluminação do conjunto.
No glTF, confira também UVs, pixels embutidos e espaço de cor de baseColor/normal;
importação sem erro não comprova aparência equivalente entre renderers.

Para tinta desenhada sobre volumes, calibre a espessura aparente por família no
export, com uma vista isolada da referência e o modelo à mesma altura. Expansão
de hull, raio de curva e espessura física não admitem um multiplicador comum.
Marcas de superfície devem aderir à malha avaliada também em perfil; faixas finas
projetadas são uma opção quando curvas cilíndricas parecem fios. Faixas largas
precisam de subdivisão transversal: projetar somente as bordas deixa o miolo do
quad atravessar a superfície curva, aparecendo como dois riscos vazados. Confira
também o interior dos triângulos e a oclusão por peças vizinhas em vários ângulos.
Verifique cor da
tinta, luz do papel e gerenciamento de cor separadamente. Antes de polir pigmento,
confira silhueta, profundidade, proporções e projeção da câmera: comprimir só o
corpo amplia a cabeça na comparação normalizada. Interrompa detalhe quando a
forma externa ainda divergir da direção vigente.

Ao reaproveitar um renderer com outra projeção de câmera, confira também o pós-processamento:
um passe de silhueta por profundidade inversa pressupõe perspectiva; ortográfica
pede profundidade linear e densidade de hachura pela escala da vista. Verifique
silhuetas e superfícies em tamanho de jogo antes de atribuir a diferença à arte.

Se um contorno por segunda diferença de profundidade criar manchas em planos
inclinados só em certas resoluções, confira o filtro e os endereços de amostragem.
Com `NearestFilter`, um raio fracionário somado ao deslocamento de tinta pode
selecionar o texel central de um lado e o vizinho do outro: o plano vira falsa
borda. Para esse detector, uma vizinhança simétrica em texels inteiros evita a
assimetria sem suavizar IDs/profundidade nem remover detalhes da cena. Valide no
shader real: plano inclinado sem falsos contornos, degrau ainda desenhado e tintas
preservadas, com mais de um raio/resolução. Tire a pauta e outras marcas legítimas
da região de medição; não relaxe o limiar para absorvê-las. Depois compare o jogo
em movimento. Caso e prova: Rabisco Boom, `art/validation/2026-09-11-gameplay-hardening/`
no laboratório, 11/09/2026.

Efeitos que precisam sobreviver a pausa, replay ou snapshots devem guardar a decisão
visual no estado e reconstruir pose/partículas pela idade do evento e seed cosmética.
Teste recebimento sem o evento inicial, reinício e reaproveitamento do pool; compare
objetos visíveis, pois transformações antigas de partículas inativas não representam
diferença renderizada. Mantenha o movimento cosmético fora da posição de colisão.

Registre efeito visual, custo e hipóteses descartadas. Teste técnico não aprova arte.
Sem comparação suficiente, declare a lacuna; não redefina uma versão degradada como
novo piso. Não marque aprovação do usuário a partir da opinião da IA.

Fontes históricas no laboratório: estudos de FPS, corrida e demos visuais.
Excalibur `RE-EXCAL-020/021` descreve infraestrutura de teste visual, não um critério
universal de qualidade artística ([fonte](https://github.com/excaliburjs/Excalibur)).

Ao acrescentar uma câmera de visão geral a um jogo com tinta que se atenua pela distância,
confira a escala espacial pressuposta no shader. Afastar a câmera para caber o mapa inteiro
pode apagar pigmento e contornos sem qualquer mudança de geometria. Uma escala explícita de
distância artística por câmera permite manter a leitura da prévia e restaurar exatamente o
valor original nas câmeras jogáveis. Preserve resolução, materiais e sombra; compare entrada,
troca de mapa e retorno à partida. Caso: Corrida Rabisco, QA “Home com mapas — 2026-09-11”.

Em renderizadores que codificam identificadores, sombra e normais num buffer intermediário,
alpha RGBA convencional não representa transparência válida. Componha o material transparente
na passagem de cor final, consultando a profundidade opaca e preservando antialiasing e
oclusão. Confira objetos na frente e atrás, vistas internas, descarte e reconstrução da cena.
O formato do buffer deve orientar a integração; não tornar o vidro opaco nem remover sua malha
para mascarar o problema. Caso e prova: Distrito Rabisco,
`production/evidence/arena-identity-20260912/`, 12/9/2026.

Em telas de seleção com rolagem interna, confira a altura dos cartões e de seus
filhos, além do overflow da página. Uma linha `minmax(0, 1fr)` dentro de uma tela
limitada ao viewport pode comprimir os cartões enquanto retratos e controles
continuam pintando por fora. Deixe o conteúdo definir a altura nas composições
estreitas e confira topo, rodapé e início da partida pelo caminho real. Caso:
Rabisco Boom, `art/validation/2026-09-13-polish/confirmation/` no laboratório.

Em partidas que continuam durante notificações, avisos de início, perigo e
mudança de fase precisam ocupar espaço reservado fora da arena e dos controles.
`pointer-events: none` não resolve a oclusão visual. Compare os retângulos de
canvas, aviso, HUD e direcional antes/depois da mensagem; a arena não deve mudar
de enquadramento nem receber texto sobre uma rota de fuga. Inclua mensagens
longas, celulares em retrato/paisagem e estados de derrota. Caso: Rabisco Boom,
`art/validation/2026-09-12-gameplay-design/checks/`, após relato de morte por banner.

Ao integrar um canvas 3D a uma página contínua, elimine somente o fundo duplicado,
preservando material e profundidade dos objetos. O alpha deve sobreviver ao
passe de cor, antialiasing e composição final; num canvas premultiplicado, RGB
não nulo em pixels de alpha zero pode produzir uma placa branca. Verifique os
pixels vazios e as bordas suavizadas, além da imagem composta. Este ajuste não
pode tornar transparentes personagens cujo corpo aprovado é opaco. Caso: Rabisco
Boom, `src/view/three/renderer.js` e capturas `2026-09-12-gameplay-design/shipped/`.

Ao compor um lobby com backplate e avatar 3D numa camada própria de câmera,
trate a máscara de visibilidade e a exposição como estado de apresentação.
Restaure-as em todas as saídas, inclusive editores de equipamento abertos pelos
ajustes, não apenas em Jogar. Exercite troca de visual, gesto, editor, retorno
e início de partida; um botão que funciona com a cena invisível não passa.
Backplate deve preservar proporção e deixar o personagem/contato 3D reais.
Caso e prova: MineNite, `docs/qa/fortnite-presentation.json`, 20/09/2026.

Quando o polimento troca a representação de um personagem (instâncias por
volumes modelados, por exemplo), confira os consumidores do tipo da malha:
sombra, culling, primeira pessoa, espelhos e pontos de arma/mão. Renderizar bem
em pose neutra não basta. Retratos de seleção podem vir do mesmo rig/material,
desde que a câmera caiba também nos acessórios mais altos e a geração restaure
o estado do renderer sem consumir o RNG da simulação. Caso: MineNite,
`tests/hero-presentation.mjs` e `docs/qa/hero-polish.json`, 20/09/2026.

Antes de trocar a linguagem de um efeito, confira o que carrega a identidade dele. Num jogo
em que o tiro é luz (clarão que ilumina o chão, bloom, brilho na cor do kit), uma forma
recortada por cima some no círculo da própria luz: a luz leva o chão acima de 1 em HDR e o
tone mapping transforma a forma em branco. Isole a causa desenhando o sprite fora do
círculo, erguido e sem teste de profundidade. Não resolva contendo a luz e ocluindo o fundo
com formas opacas: o efeito muda de linguagem (vira desenho animado) e deixa de combinar
com o resto do jogo. Melhore dentro da luz e compare em movimento com o dono da direção
antes de trocar o padrão. Quando o dono disser que "antes era melhor", compare a versão
antiga rodando lado a lado (um worktree do commit anterior) em vez de adivinhar pelo código.
Caso: Só Sobra Um, 22/09/2026 — clarão, rastro e estrela recortados, e silhuetas com
contorno de tinta sobre projéteis que antes eram luz, ambos recusados; os tiros voltaram
aos feixes de luz do começo (devlog "Tiros de luz do começo do jogo").

Em câmera alta (top-down, isométrica íngreme), julgue o personagem primeiro pela silhueta
preta na câmera real da partida. Vista de cima, a cabeça ou o chapéu cobre a maior parte
do corpo. A identidade vem do que sai desse círculo (luvas, ferramenta, carga, arma) e de
dois ou três blocos grandes de cor. Botões, cintos e bolsos somem nesse tamanho. Um
acessório atrás da cabeça ou do mesmo lado de outra massa também some: confira na
silhueta. Peças de cabeça precisam respeitar a troca de visuais (chapéus alternativos),
e peças novas nas costas precisam conviver com capas. Prove em partida, andando, e nos
visuais alternativos. Caso: Só Sobra Um, 22/09/2026 (Galo de Briga como referência; Slick,
Rebita e Fuse).
