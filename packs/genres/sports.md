# Gênero — Esportes (simulação, arcade, extremos)

Aplicabilidade: `--genre sports`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: executar sob regras conhecidas. Decisões: posicionamento, timing do passe/
  chute/tackle, gestão de time e substituições, risco em manobras (extremos).
- Modelo: simulação (regras completas, física de bola, IA tática), arcade (poucos
  botões, exagero, power-ups), extremos (skate/snow: tricks, fluxo, pontuação).
  Registre qual e se há licença ou regras fictícias.

## Feel que importa

- Física de bola/objeto crível e consistente: quique, spin, peso; contato atleta-bola
  legível. Animação: blending por contexto sem travar controle; IK de pés.
- Câmera: broadcast (lateral, com zoom por ação) ou ação; nunca perde a bola.
- Feedback de acerto de timing (chute perfeito, trick land) por som/animação; replays.

## Riscos habituais

- IA de companheiros que não se posiciona; adversário lendo input (trapaça); regras
  incompletas (impedimento, faltas) quebrando partidas; física que "cola" a bola.
- Modos sem fim (temporada) sem economia de tempo; multiplayer sem paridade de
  input; licenças e nomes reais sem direito.

## Orçamentos e medições típicas

- Quadro p99 com todos os atletas + torcida + replay; latência input → ação;
  determinismo de física por FPS; tempo por partida; taxa de eventos raros (gol,
  penalidade) por partida em simulação headless.

## QA e playtest específicos

- Simulação IA×IA headless com seed para regras e distribuição de resultados; testes
  de regra por cenário (impedimento, fora, fim de tempo); replay reprodutível.
- Playtest: fã do esporte reconhece as regras? Novato marca ponto em 2 minutos?
  Comemoração/replay dá vontade de repetir?

## Receitas e fontes

[feel](../../recipes/feel.md), [mecânicas](../../recipes/mechanics.md), [visual](../../recipes/visual.md)
(câmera, animação), [rede](../../recipes/network.md), [produção](../../recipes/production.md).
Extremos compartilham com [platformer](platformer.md) (traversal, fluxo).
