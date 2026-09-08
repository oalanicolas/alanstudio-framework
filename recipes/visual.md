# Direção visual, câmera e performance

Entrada: referência aprovada, diferença percebida e percurso/câmera de comparação.

Leia a direção do usuário e os aprendizados de performance do próprio jogo.
Reutilize materiais, modelos, efeitos, tokens e métodos coerentes com essa direção;
adapte seus consumidores antes de criar variantes paralelas.

Capture o antes em condições equivalentes: versão, resolução, dispositivo, entrada,
iluminação e trecho em movimento. Localize o gargalo pelo caminho real antes de
otimizar. Medição serve para escolher uma implementação melhor preservando arte e
jogabilidade. Não corte sombras, reflexos, transparência, textura, detalhes ou
animação como solução automática de FPS.

Na câmera, observe antecipação de curvas/ameaças, oclusão do jogador, estabilidade,
escala e transição. No mundo, compare silhueta, materiais, luz, sombras, efeitos e
coerência em movimento, não apenas a melhor screenshot.

Casos já documentados: nomes podem mudar após o carregamento do GLTF; culling deve
ser testado em todas as aberturas visíveis; animação em shader invalida suposições
de sombras estáticas. Reproduza a cena em vez de inferir a correção por nomes crus.

Registre efeito visual, custo e hipóteses descartadas. Teste técnico não aprova arte.
Sem comparação suficiente, declare a lacuna; não redefina uma versão degradada como
novo piso. Não marque aprovação do usuário a partir da opinião da IA.

Excalibur `RE-EXCAL-020/021` descreve infraestrutura de teste visual, não um
critério universal de qualidade artística. [Fontes](../references/sources.md).
