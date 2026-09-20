# Gênero — Shooter (FPS, TPS, twin-stick, shmup)

Aplicabilidade: `--genre shooter`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

> **Curadoria** — revisado em 2026-09-14.
> **Contempla:** FPS, TPS, twin-stick e shmup, em qualquer plataforma. É
> vocabulário de design, não API: nada aqui depende de versão de engine.
> **Decisões antes de escrever código (REUSE → ADAPT → CREATE):** o papel de cada
> arma e a composição dos encontros são do GDD. Reaproveite o que o projeto já
> tem antes de propor sistema novo — a abertura do jogo, por exemplo, é decisão
> do jogo e do starter, não do gênero.
> **Verificar:** escolha uma arma e prove o papel dela num recorte jogável —
> alcance, cadência e custo distinguíveis de outra arma na mesma arena. O
> esperado é uma diferença que o jogador percebe sem ler número na tela.
> **Limites:** o harness não mede latência de input → tiro, não ouve o mix e não
> observa a curva de dificuldade. Essas provas são de sessão, por
> `record --kind observation`.
> **Exemplo rastreável:** `games/distrito-rabisco` é um FPS de ondas
> (`production/game-design.md:349`), com combate de armas e katana.

## Verbo central e decisões

- Verbo: mirar, atirar, posicionar-se. Decisão: alvo, arma, cobertura, recarga,
  avanço vs recuo. Cada arma precisa de um papel legível (alcance, cadência, custo).
- Encontros: composição de inimigos com funções distintas; arenas com leitura clara de
  cobertura, flanco e rota de fuga.

## Feel que importa

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
