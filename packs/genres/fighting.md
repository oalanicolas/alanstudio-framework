# Gênero — Luta (2D, 3D, platform fighter)

Aplicabilidade: `--genre fighting`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: ler e punir. Decisões: espaçamento (neutral), quando atacar/defender/
  agarrar, gerenciar recursos (meter, stamina), escolha de opção em situação
  vantajosa/desvantajosa (okizeme, pressão).
- Modelo: 2D tradicional (frame data, cancels, combos), 3D (sidestep, tracking),
  platform fighter (movimento livre, knockback por dano). Registre e defina o
  público: casual, competitivo, ambos.

## Feel que importa

- Determinismo em frames: startup/active/recovery inteiros, hitstop, hitstun,
  blockstun; input buffer e leniência de comandos (motion inputs) documentados.
- Feedback: hit spark por força, screen shake por golpe pesado, som em camadas
  (impacto + voz), câmera que enquadra ambos sem cortar.
- Zero variação por FPS: simulação a 60 Hz fixos; render pode interpolar.

## Riscos habituais

- Balanceamento: opções dominantes, infinitos, loops de pressão sem resposta;
  personagens sem identidade de gameplay.
- Netcode: delay-based em vez de rollback; rollback exige simulação determinística,
  serialização de estado leve e arte que aguenta rewind visual.
- Onboarding inexistente: comandos e frame data invisíveis para novatos; treino sem
  dados; hitboxes que não batem com a arte.

## Orçamentos e medições típicas

- Latência input → primeiro frame visível (alvo < 4 frames incluindo display);
  quadro p99 sempre abaixo de 16,67 ms; tamanho do estado serializado e tempo de
  rollback por frame previsto; frame data por golpe em tabela versionada.

## QA e playtest específicos

- Replay determinístico: gravar inputs e rejogar batendo estado bit a bit; testes de
  hitbox por frame; input buffer em todos os comandos; pausa/foco durante combo.
- Playtest: novato faz um golpe especial em 5 minutos? Experiente sente que perdeu
  por leitura, não por sistema? Espectador entende quem está ganhando?

## Receitas e fontes

[feel](../../recipes/feel.md), [mecânicas](../../recipes/mechanics.md) (passo fixo,
determinismo), [rede](../../recipes/network.md) (rollback), [produção](../../recipes/production.md).
Ver [multiplayer competitivo](multiplayer-competitive.md) para ranked e temporada.
