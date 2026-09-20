# Gênero — Plataforma (2D/3D, metroidvania, precisão)

Aplicabilidade: `--genre platformer`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: mover e pular com precisão; decidir rota, timing e risco. O nível é o
  argumento; cada sala ensina ou combina uma habilidade.
- Progressão: habilidades que abrem leitura nova do espaço (metroidvania) ou desafio
  crescente com a mesma gramática (precisão). Registre qual.

## Feel que importa

- Coyote time, jump buffer, altura variável por tempo de botão, aceleração/fricção
  assimétricas, cantos perdoados (ledge forgiveness), curva de gravidade na descida.
- Câmera: lookahead na direção do movimento, zonas mortas, limites de sala, sem
  esconder o chão de destino.
- Animação: antecipação curta no pulo, squash na aterrissagem, poeira, som por
  material do piso.

## Riscos habituais

- Colisão inconsistente com delta variável (túnel, agarrar em quinas): passo fixo ou
  varredura.
- Inputs perdidos por ordem de leitura; controle que muda com FPS.
- Dificuldade sem prática: combinar riscos antes de ensinar cada um.
- Checkpoint distante demais do desafio; morte que custa tempo em vez de aprendizado.

## Orçamentos e medições típicas

- Latência input → primeiro quadro de pulo (meta comum: 1–2 quadros); tempo de
  respawn; quadro p99 com partículas e paralaxe; memória de tiles por nível.

## QA e playtest específicos

- Testes de invariantes de colisão com seed/replay de inputs; salto em quinas, tetos
  baixos, plataformas móveis e one-way; pausa no meio do pulo.
- Playtest: onde a pessoa morre repetidamente sem mudar de estratégia? Ela lê o
  caminho seguro antes de pular? Registre tentativas por sala.

## Receitas e fontes

[feel](../../recipes/feel.md), [mecânicas](../../recipes/mechanics.md),
[ciclo de vida](../../recipes/lifecycle.md), [conteúdo](../../recipes/content.md) (LDtk: níveis).
