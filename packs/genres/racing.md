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
- Clipes reprodutíveis no navegador: com passo fixo e piloto de referência, substituir
  `performance.now` e `requestAnimationFrame` antes da página carregar (CDP
  `Page.addScriptToEvaluateOnNewDocument`) e avançar o relógio 1/fps por captura; a corrida
  gravada deve bater evento a evento com a bancada headless. Só funciona se a regra não ler
  tempo de parede nem `Math.random`.
- Teste de leitura com crítico de contexto limpo: quatro clipes de 10 s, perguntas sobre a
  próxima curva, quem está à frente e atrás, qual item acertou quem e de onde, e por que a
  posição mudou; comparar com o gabarito dos eventos gravados.

## Medir envolvimento, não só tempo de volta

Quando aplicar: pedido de "mais disputa", "o líder foge", "enjoa rápido" ou barra de outro
jogo (ex.: Mario Kart). O que verificar:

- **Pilotos de referência que só mandam entradas humanas** (um habilidoso: drift até o nível
  máximo, linha de risco, vácuo, arrancada; um seguro: sem drift, linha de recuperação).
  Mesma política de itens e armas nos dois, para a diferença medir pilotagem. Métricas por
  semente e pista: fração do tempo a até o alcance do vácuo de um rival, ultrapassagens em
  pista por volta (troca de ordem entre carros vivos e próximos, não respawn), troca na última
  volta, vitórias e último lugar de cada piloto, diferença de contra-relógio entre eles.
- **Recuperação por erro injetado com os objetos do próprio jogo** (mina/tinta na frente,
  vida baixa + mina para destruição, empurrão para o muro) contra a mesma corrida sem erro:
  posições perdidas, segundos perdidos, tempo até voltar a disputar.
- **Linhas:** cronometrar setores com a linha forçada e contar incidentes nela. Linha mais
  rápida com risco medido zero não é escolha.
- **Assimetrias escondidas antes de mexer em números:** procure limites que só os rivais têm
  (ex.: teto de velocidade de curva por prévia do traçado, cadência de armas). No Corrida
  Rabisco, a "cautela de curva" exclusiva da IA era a causa principal da fuga do jogador
  habilidoso; tirar a cautela de um único rival (o ás) levou o habilidoso de 36–39% para
  53–57% do tempo em disputa, com o seguro ainda vencendo 6–19%.
- Teste cada hipótese de reagrupamento isoladamente. Contraprovas do mesmo caso: zerar a ajuda
  de ritmo quase não mudou o pelotão; igualar a cadência de armas espalhou mais; invulnerabilidade
  após golpe protegeu o líder.

O que invalida: bots de referência que tocam no estado da corrida, sementes diferentes entre
antes e depois, ou clipes que não reproduzem a corrida medida. Limites: números de um jogo não
viram alvo de outro; disputa medida não é diversão — playtest humano decide.
Caso: `games/corrida-rabisco/docs/qa.md#barra-mario-kart--24092026` (laboratório Games).

## Câmera de perseguição: métrica que enxerga o que o jogador vê

Visão à frente medida só contra a geometria engana. Desconte os cartões **opacos do HUD**
(medidos no navegador), meça **subidas e cristas** à parte e siga uma volta inteira na
suavização real a 60 quadros por segundo separando **tranco** (mudança de velocidade na tela
de um quadro para o outro, típico de duas poses trocando) de **panorâmica** (varredura
contínua). Troca de pose (loop, anti-gravidade, túnel) se mistura por distância; mirar em
parte a pista 10–18 m à frente revela a curva antes do painel lateral, ao custo de o carro sair
mais do centro em curvas fortes — registre esse custo. Câmera mais baixa e centrada dá
"sensação de kart" mas pode esconder cristas; no caso Corrida ela foi reprovada por isso.

## Receitas e fontes

[visual](../../recipes/visual.md) (câmera, culling, GLTF), [feel](../../recipes/feel.md),
[ciclo de vida](../../recipes/lifecycle.md), [mecânicas](../../recipes/mechanics.md).
Ponto de partida no laboratório: Brasa-Pista ([criar](../../recipes/create.md)).
