# Gênero — Corrida (arcade, kart, simulação)

Aplicabilidade: `--genre racing`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: pilotar no limite. Decisão: traçado, frenagem, ultrapassagem, uso de
  drift/boost/itens, risco vs consistência por volta.
- Modelo: arcade (aderência generosa, drift assistido), kart (itens, catch-up),
  simulação (pneus, peso, telemetria). Registre qual e o que não pode mudar.

## Feel que importa

- Sensação de velocidade: FOV dinâmico, motion blur controlado, partículas laterais,
  som de motor por RPM e Doppler, vibração por superfície.
- Câmera: antecipação de curva, estabilidade em colisão, altura/distância por
  velocidade, sem oclusão do apex.
- Resposta do volante/analógico: zona morta, curva, contra-esterço em drift.

## Riscos habituais

- Física dependente do FPS (passo fixo obrigatório para paridade 30/60/144).
- IA que segue linha perfeita ou "rubber band" perceptível; colisões injustas.
- Pista sem landmarks: o jogador não antecipa a curva; largada e reset na pista.
- Ghost/replay e determinismo: replay diverge da corrida real.

## Orçamentos e medições típicas

- Quadro p99 com todos os carros e VFX na largada; tempo de carga de pista; streaming
  de cenário; latência input → reação do carro; paridade de tempos de volta por FPS.

## QA e playtest específicos

- Simulação headless de voltas com seed; colisão em muro/carro em várias velocidades;
  reset na pista; pausa em pleno drift; comparação em movimento da câmera.
- Playtest: a pessoa prevê a curva? Melhora o tempo por volta com prática? Sente
  velocidade sem perder controle?

## Receitas e fontes

[visual](../../recipes/visual.md) (câmera, culling, GLTF), [feel](../../recipes/feel.md),
[ciclo de vida](../../recipes/lifecycle.md), [mecânicas](../../recipes/mechanics.md).
Ponto de partida no laboratório: Brasa-Pista ([criar](../../recipes/create.md)).
