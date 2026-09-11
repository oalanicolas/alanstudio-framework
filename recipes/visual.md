# Direção visual, câmera e performance

Entrada: referência aprovada, diferença percebida e percurso/câmera de comparação.

Leia [a qualidade](../references/quality.md) e os aprendizados de performance
do laboratório, quando existirem.
Reutilize materiais, modelos, efeitos, tokens e métodos coerentes com essa direção;
adapte seus consumidores antes de criar variantes paralelas. A instância canônica
é o design system do jogo (Art Bible); o contrato do estúdio está no
[design system do jogo](../references/game-design-system.md).

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
escala e transição. No mundo, compare silhueta, materiais, luz, sombras, efeitos e
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
