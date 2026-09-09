# Game feel e feedback

Entrada: uma ação central que funciona, mas não convence; ou um verbo novo que precisa
nascer já com a resposta pretendida. `context --focus feel` seleciona esta receita e
o [design system do jogo](../references/game-design-system.md), onde o feel é registrado.

Feel é a diferença percebida entre “funciona” e “parece um jogo de verdade”. É a
soma de latência, animação, câmera, efeitos, som e haptics em torno de uma ação, e é
específico de cada jogo: o peso de um soulslike quebra um plataforma de precisão.
Comece pelo verbo do GDD e pela sensação pretendida, não por uma lista de efeitos.

## 1. Medir o que existe

Antes de ajustar, capture a ação em movimento (vídeo ou sequência de quadros) e meça:

- **Latência entrada → resposta visível:** quadros entre o input e a primeira mudança
  na tela; some fila de input, tick, render e apresentação. Meça no build alvo.
- **Janela de antecipação e recuperação:** quadros antes do efeito e depois dele; ações
  canceláveis e buffer de input, se o gênero pedir.
- **Leitura:** a ação é legível a distância, em movimento, com outros elementos na tela?

Registre valores, cena, plataforma e captura. Sem medição, o ajuste é opinião.

## 2. Camadas de resposta

Cada camada responde a uma pergunta do jogador; adicione só as que servem ao verbo.

- **Animação:** antecipação, squash/stretch, follow-through, poses-chave legíveis;
  transições que preservam o momento; blend com o input, não em substituição a ele.
- **Câmera:** shake proporcional e com decaimento, kick, zoom breve, lead/antecipação
  de curvas e ameaças; nunca esconder o jogador nem a ameaça.
- **Tempo:** hitstop/freeze frames, slow-motion curto, aceleração após confirmação.
  Verifique que pausa, reinício e som respeitam a manipulação de tempo.
- **Efeitos:** partículas, flashes, trilhas, decalques, distorção; priorizados pela
  informação que carregam (acerto, erro, perigo, recompensa), não pelo volume.
- **Som:** camadas por intensidade, variação de pitch/sample, prioridade de vozes,
  silêncio antes do impacto, stinger de resultado. Piso de gravação licenciada.
- **Haptics:** rumble com envelope e intensidade por evento, quando o dispositivo tiver.
- **Interface:** contadores que respondem, números de dano, indicadores com easing;
  sem cobrir a ação.

## 3. Ajustar com uma variável por vez

Mude um parâmetro, capture em condições equivalentes, compare lado a lado. Curvas de
easing e magnitudes vivem em dados/tokens do design system do jogo, com consumidor
real, para que o próximo verbo herde o vocabulário. Registre o que foi descartado e
por quê: feel excessivo cansa e esconde informação; feel ausente parece quebrado.

## 4. Provar

Prova técnica: latência medida, ausência de regressão em pausa/reinício, orçamento de
quadro preservado com os efeitos ativos. Prova de experiência: observação em movimento
por pessoa, com a pergunta “o que aconteceu e por quê?” respondida sem ajuda.
Screenshot isolada não prova feel. Avaliação do agente não é aprovação do usuário.

## Limites

O harness não mede latência nem captura quadros; use as ferramentas da engine e da
plataforma e registre o comando ou procedimento. Os princípios acima são vocabulário
consolidado de animação e game design ([fontes](../references/sources.md#produção-09));
os valores certos pertencem a cada jogo e só existem depois de medidos e observados.
