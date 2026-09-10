# Gênero — Multiplayer competitivo (MOBA, hero shooter, battle royale, arena)

Aplicabilidade: `--genre multiplayer-competitive`. Orientação de gênero para
direcionar perguntas, riscos e provas; o GDD do jogo decide. Não é regra universal.
Combine com o gênero do verbo (shooter, fighting, racing): este pacote cobre o que é
específico de competição online.

## Verbo central e decisões

- Verbo: vencer outras pessoas. Decisões: composição/pick, posicionamento,
  cooperação em equipe, gestão de recurso por partida (ouro, ultimates, loot),
  quando engajar.
- Modelo: MOBA (lanes, objetivos, 5×5), hero shooter (papéis, habilidades), battle
  royale (zona, loot, últimos vivos), arena (rodadas curtas). Registre tamanho de
  time, duração e o que torna cada partida diferente.

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Netcode como feel: predição no cliente, reconciliação, compensação de lag para
  acerto, interpolação de remotos; tudo isso precisa ser testado com latência e perda
  simuladas, não em LAN.
- Legibilidade: silhuetas e cores por papel, VFX que informam sem esconder, som
  posicional confiável (passos, habilidades) — som é informação competitiva.
- Comunicação: ping, roda de voz, texto; mudo e reporte acessíveis.

## Riscos habituais

- Autoridade no cliente (trapaça trivial); matchmaking sem população (filas longas)
  ou sem paridade de habilidade; balanceamento por dados sem contexto.
- Meta estagnada, snowball sem contrajogo, tempo morto (respawn, espera de partida);
  toxicidade sem ferramentas; servidores: custo por partida, regiões, tick rate.
- Live service sem plano: temporadas, economia de cosméticos, backlog de bugs.

## Orçamentos e medições típicas

- Tick rate do servidor e custo de CPU por partida; latência p50/p95 por região;
  KB/s por cliente; tempo em fila; duração de partida; win rate por
  personagem/arma por faixa de habilidade; taxa de desistência.

## QA e playtest específicos

- Bots headless preenchendo partida completa no servidor; testes com latência
  100–250 ms e perda 2–5 %; reconexão no meio; exploits de autoridade (velocidade,
  dano); testes de carga em servidor.
- Playtest: a pessoa culpa a rede ou a si mesma? Entende o papel do herói em uma
  partida? Quer jogar "só mais uma"?

## Receitas e fontes

[rede](../../recipes/network.md), [feel](../../recipes/feel.md), [mecânicas](../../recipes/mechanics.md),
[produção](../../recipes/production.md) (live). Verbo em [shooter](shooter.md),
[fighting](fighting.md), [racing](racing.md), [strategy](strategy.md).
