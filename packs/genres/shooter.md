# Gênero — Shooter (FPS, TPS, twin-stick, shmup)

Aplicabilidade: `--genre shooter`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: mirar, atirar, posicionar-se. Decisão: alvo, arma, cobertura, recarga,
  avanço vs recuo. Cada arma precisa de um papel legível (alcance, cadência, custo).
- Encontros: composição de inimigos com funções distintas; arenas com leitura clara de
  cobertura, flanco e rota de fuga.

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Hitmarker/hit feedback em som, VFX e animação do alvo; recuo e recuperação da arma;
  muzzle flash e tracers proporcionais; câmera com kick e recuperação; hitstop curto
  em impactos fortes.
- Mira: curva de sensibilidade, aim assist explícito no gamepad, FOV configurável,
  latência input → tiro medida.
- Som: camadas por distância, oclusão, prioridade de vozes; silêncio antes do boss.

## Riscos habituais

- Hitscan vs projétil sem decisão consciente; colisão de projétil com delta variável.
- IA que só corre para o jogador; ausência de "telegraph" antes de dano alto.
- Rede: autoridade do servidor para dano, reconciliação e compensação de lag; cliente
  nunca decide o acerto. Duas sessões reais para validar.
- Legibilidade em movimento: inimigos, aliados e perigos sem contraste.

## Orçamentos e medições típicas

- Latência input → tiro (quadros); quadro p99 em arena cheia com VFX; contagem de
  projéteis/partículas ativas; tráfego por jogador e tick do servidor quando online.

## QA e playtest específicos

- Cenários: dano em movimento, recarga interrompida, tiro através de geometria fina,
  pausa durante projétil, morte simultânea, reconexão no meio da partida.
- Playtest: a pessoa entende de onde levou dano? Troca de arma por decisão ou por
  acidente? Observe uso de cobertura e leitura de telegraphs.

## Receitas e fontes

[feel](../../recipes/feel.md), [rede](../../recipes/network.md),
[visual](../../recipes/visual.md), [mecânicas](../../recipes/mechanics.md).
Ponto de partida no laboratório: Distrito Rabisco ([criar](../../recipes/create.md)).
