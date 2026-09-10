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

Ao reaproveitar um renderer com outra projeção de câmera, confira também o pós-processamento:
um passe de silhueta por profundidade inversa pressupõe perspectiva; ortográfica
pede profundidade linear e densidade de hachura pela escala da vista. Verifique
silhuetas e superfícies em tamanho de jogo antes de atribuir a diferença à arte.

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
