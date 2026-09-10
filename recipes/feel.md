# Feel da ação

Entrada: verbo central, referência de sensação (aprovada ou proposta) e a
diferença percebida entre intenção e resposta atual.

Com tela, a primeira superfície é a porta. O campo começa depois do
avanço. A mostra da porta marca o trilho no mesmo alcance do campo.
O toque que sai do campo ainda solta — a captura leva o up.
Captura no disco não é sessão observada. Esconder a aba solta o
hold — o keyup some e o corpo não segue. Perder o foco da janela
solta o ofício pendente — Space e R não disparam no quadro
seguinte. Na pausa o toque retoma — Esc e P não existem no
polegar; o tap não é o avanço. Na porta o telefone vê
Jogar: toque sem ter apertado; o aviso continua teclado
até o gesto. Soltar no disco não é
sessão observada. Depois do fim, um avanço novo volta à porta; R também. Depois da partida, o achado precisa de forma. `playtest <projeto>` lê se o
disco tem problema, evidência, hipótese e medição. Recibo sem os quatro é
impressão — `next` propõe `playtest.unstructured` e aponta a página
(`#finding`) e `note --field`. `playtest` só lê. Nomeia `form` e
`fields`. Sem `then`. Esqueleto no disco não é achado. O `note`
nomeia `finding` e `needed` no próprio recibo. Recibo sem os
quatro não é achado. `playtest --invite`
escreve a página e aponta `href` (`/?invite=1` ou, com seed no disco,
`/?invite=1&seed=<n>`, com chuva nomeada `&spawn=<mesa>`, com look nomeado `&look=<paleta>`, e com relógio nomeado e ≠ 1 `&speed=<relógio>`), onde a tabela some; depois do
fim a página oferece os quatro nomes para copiar ou gravar e
mostra seed, pontos, eixos e a curva que o last-run já traçou.
Depois do fim a página
rola até o painel e foca o campo. Escrever não dispara o
verbo — Espaço e R ficam no recado. Rolar não é alguém de fora. Número na faixa não
preenche os quatro. Copiar não grava. Sem a área de
transferência, o Copiar baixa o markdown. Gravar anexa o candidato
se last-run existir. Gravado
não é alguém de fora. Nomear o endereço não observa. Depois do
fim, a página aponta o convite desta partida se a seed ficou no
recibo. Copiar o endereço não grava. `next` aponta o convite
depois do recibo de quem fez. O serve anuncia a URL da rede
se a máquina tiver outro endereço IPv4. Esconder a tabela, anunciar
a rede, mostrar os números, copiar o achado e gravar os quatro nomes não são alguém de fora. `observed` e `outsider` são sempre
falsos: o harness não assiste à sessão. A partida no serve grava o
mesmo candidato em `docs/playtest/last-run.json` com `policy: played`.
`npm run session` grava a simulação (`nearest-orb`) e não
sobrescreve `played` sem `--force`. `session --look` e
`session --speed` nomeiam o que o convite já lê. Simular
no relógio cheio não observa.
`playtest` relata
`candidate_policy`. Nenhum dos dois é sessão observada. Se o
projeto (ou o starter) declara `session`, `then` a aponta. `note --from-run`
anexa o resumo e, se houver, a curva — o mapa já põe `--from-run`
quando o arquivo existe. Depois do fim, a página grava o mesmo
recibo de `note` se você escrever — `felt` continua falso. Número
no disco não é causa. O autor sugerido no comando não é quem jogou.

Feel é o intervalo entre o input e a certeza de que o mundo respondeu.
Swink: controle em tempo real, espaço simulado, polish. Jam e piso de
acabamento se separam aqui com mais frequência do que na escolha da engine.
Sem feel, o ciclo pode estar correto e o jogo parecer vazio. Sem sincronia,
o juice vira ruído.

Leia o verbo no GDD, os tokens de tempo/câmera/áudio no
[design system](../references/game-design-system.md) e o
[piso](../references/quality.md). `context --focus feel` seleciona esta
receita. `feel` lê as constantes nomeadas no `CONFIG` e o
recibo de observação no disco; nomeia `then.play` e `then.note`
sem executar. Sem comando de abrir, a chave some. Não tem
`prompt`. `felt` é sempre falso. `note`
grava o recibo curto depois da partida. Sem caminho, o único
jogo do laboratório basta; dois pedem o caminho. Achar o jogo
não é ter sentido. O usuário não precisa pedir “ative o juice”.

## 1. Isolar o verbo

Descreva **uma** ação: o que o jogador faz, o que o estado muda, o que os
olhos e os ouvidos deveriam confirmar. Se várias ações competem, comece
pela que o brief chama de central.

Separe:

- **Regra** — a ação é legal, o estado muda, a recusa existe.
- **Apresentação** — a mudança é perceptível.
- **Feel** — a percepção tem peso, timing e recuperação.

Corrigir a regra não substitui o feel. Animar demais não substitui a regra.
Se a ação ainda não existe, volte a [criar](create.md) ou a
[mecânicas](mechanics.md); esta receita assume um ciclo jogável.

## 2. Cadeia perceptível

Siga a ação da intenção ao descanso. Examine só os elos que o recorte tem
(ou deveria ter). Nomes abaixo são vocabulário de inspeção, não uma API.

1. **Intenção** — o jogador sabe que pode agir? Ameaça e oportunidade são
   legíveis antes do input.
2. **Input** — latência, deadzone, buffer, cancelamento, perda de foco,
   toque versus gamepad versus mouse. O mesmo verbo pode falhar numa entrada
   e funcionar em outra.
3. **Antecipação** — frames ou pose que prometem o golpe/pulo/disparo antes
   do impacto. Sem ela, a ação chega “de graça” ou atrasada demais.
   No starter o avanço senta (`squashCoil`) dois ticks antes de alongar;
   esses ticks já atravessam o estilhaço — o coil não é janela de hit.
   O término emite `land` (squash, câmera, puff, rumble e voz).
   Esse quadro também atravessa o estilhaço; a recuperação depois
   do land continua vulnerável.
   Guardar uma corrente que já existe senta os mesmos dois ticks antes
   de converter (`squashBankCoil` senta; o coil do avanço estreita);
   esses ticks já atravessam o estilhaço — o arco da
   guarda não é janela de hit. Pedido de guarda com corrente já
   existente espera o coil e o land do avanço: os dois arcos no mesmo tick
   comiam o disparo; o sit no travel comia a pose e convertia no ar.
   O pedido não decai durante o coil nem o travel. O quadro que converte também atravessa:
   sentar e pontuar no mesmo impacto não mata. Coleta e guarda no mesmo
   quadro continuam na hora — o contato já foi a antecipação. Orbe
   que cai no arco da guarda espera: o sit não inflama a aposta
   que você já pediu; depois do commit o orbe entra. O relógio
   não come a guarda que já sentou: o sit converte antes do
   `over`.    O hitstop no fim não alonga o relógio: o limite
   encerra mesmo durante o congelamento. A queda
   longe não come o verbo em curso: marca o chão
   e não senta o avanço, o coil nem o sit da guarda.
   Parado, a queda ainda senta. Dois
   orbes no mesmo quadro não inflam a corrente: o segundo espera o
   próximo tick. Orbe e estilhaço no mesmo quadro: o estilhaço letal
   resolve; o orbe espera. Ordem do array não decide a aposta. A graça
   após dano também vale no mesmo quadro: o segundo estilhaço raspa,
   não empilha impacto. Pose e
   arquivo no disco não são peso percebido.
4. **Resposta de corpo** — squash, stretch, deslocamento, IK, arma, veículo
   ou cursor. A silhueta muda o bastante para ser lida em movimento.
5. **Impacto** — hitstop, freeze frames, flash, partículas, rumble, stinger.
   Duração proporcional à importância; impacto de coleta não pode parecer
   golpe mortal, e o contrário também. Visual, áudio e pause de hit disparam
   no **mesmo frame** do contato. Alguns milissegundos de atraso fazem o
   cérebro registrar dois eventos, não um peso.
6. **Câmera** — punch, lookahead, aterrissagem, oclusão, recuperação. A
   câmera confirma a ação sem enjoar nem esconder o próximo risco.
   No starter o trilho já marca a ameaça; a câmera inclina para o
   mesmo aviso (`lookAheadX`), menor que o punch do dash. Lean no
   disco não é peso percebido.
7. **Áudio** — ataque, corpo, impacto, cauda e silêncio. Sem camada que
   marque o verbo, o feel fica visual-only; use [áudio](audio.md).
8. **Recuperação** — o jogador volta ao controle num tempo justo. Recovery
   invisível ou infinito quebra confiança.

Registre o elo fraco antes de adicionar mais partículas. Três efeitos no
impacto não compensam input que ignora o botão.

## 3. REUSE → ADAPT → CREATE

Procure o feel já existente no jogo: hitstop, easing, impulse de câmera,
envelope de som, rumble. Leia o **consumidor** (o golpe, o pulo, o clique),
não só o utilitário. Um tween genérico sem dono não é feel reutilizável.

- **REUSE:** o envelope atual atende com outros parâmetros.
- **ADAPT:** estenda o canônico (mesmo hitstop, outra curva) e preserve quem
  já o consome.
- **CREATE:** nenhuma cadeia existente cobre o verbo sem acoplamento
  estranho. Explicite a lacuna; crie só o elo que falta.

Não importe um “juice pack” universal. Feel copiado de outro jogo sem ADAPT
e proveniência dilui a instância. 8-bit, bounce cartoon ou screen-shake
contínuo não são o padrão; o padrão é a referência aprovada deste jogo.

## 4. Ajustar uma variável por vez

Feel é causal. Altere duração, escala ou intensidade de **um** elo e
compare nas mesmas condições: versão, resolução, entrada, trecho, seed
quando demonstrada. Valores iniciais do acervo são ponto de partida, não
constantes universais.

Evite:

- Juice que atrasa o próximo input além do que o ritmo pede.
- Câmera que combate o jogador ou esconde a ameaça.
- Hitstop em toda interação até o tempo parecer quebrado.
- Partículas que tapam a silhueta da consequência.
- Compensar regra injusta com feedback “gostoso”.

A qualidade aprovada é o piso. Não corte feel para ganhar FPS; investigue
implementação mais barata que preserve a percepção (menos overdraw, mesmo
punch). Antes de negociar fidelidade gráfica, observe latência de input e
spikes de frametime no mesmo trecho: stutter quebra o feel com mais força
do que um preset mais baixo.

## 5. Provar em movimento

Screenshot não comprova feel. Compare o antes/depois no percurso real.
Observe também pause, perda de foco, o controle que some, reinício e troca de entrada: um
hitstop que sobrevive à pausa ou um rumble que não morre no descarte é
regressão de [ciclo de vida](lifecycle.md).

No QA, um caso de feel declara: ação, elo sob teste, duração/escala
esperada, condição equivalente e julgamento (agente ou pessoa, sem
confundir). Sem referência aprovada, registre que o piso ainda é proposta.

Fontes de método: [qualidade](../references/quality.md),
[ambição](../references/ambition.md), Art Bible do jogo, Swink / *Juice it
or lose it* no [mapa](../references/sources.md#aaa-tier-e-piso-09). Estudos
de câmera/tempo no laboratório, quando existirem, são precedentes — não um
kit de juice obrigatório.

## Limites

O harness não mede latência nem captura quadros; use as ferramentas da engine ou do
[pacote de plataforma](../packs/README.md) e registre o comando ou procedimento. A
medição entra por `record --kind budget` (latência, p99 do quadro com efeitos ativos)
e a observação em movimento por `record --kind observation`, ligadas ao HEAD do jogo.
Os valores certos pertencem a cada jogo e só existem depois de medidos e observados;
o feel do verbo central é lente de marco em [produção](production.md).

## Implementação de referência e degraus

Antes de escrever a sua cadeia, leia uma concreta: o starter `canvas-arcade` reúne o
perdão de entrada em `CONFIG`, em `src/game/rules.js` — buffer de dash, buffer de
guardar, graça após dano — inclusive no mesmo quadro —, alcance de coleta maior que o desenho — cada valor com o
motivo ao lado. Guardar no hitstop não é engolido; o freeze também
não queima o perdão do avanço nem o da guarda. Um toque sem corrente não decide
o próximo orbe. Cada verbo desloca a câmera numa direção própria e achata o corpo
numa medida própria: coleta, queda, dash, raspo, aterrissagem, guardar e o erro não compartilham
squash. O dash aterrissa: o corpo senta, a câmera confirma para baixo,
o rastro cai e o mixer fala `land` — distintos da partida. O avanço
é o aperto, não o segurar: teclado, toque e A leem a borda. Segurar
na porta não dispara o ofício; no campo o cooldown não metralha. A
guarda continua nível. Na porta o tap abre inclusive na faixa da
guarda — o polegar no primeiro gesto não cala a abertura. No campo
a faixa inferior continua guardando. Aperto no disco não é peso
percebido. A porta
fecha o mesmo arco no tick que abre, sem contar o ofício. O hold
leva o relógio da mostra: retomar no campo não devolve a frase
nem o mover que a porta já deu. Hold antigo sem o número não
inventa ensino feito. Número no disco não é aba fechada.
A guarda
que já tem corrente senta os mesmos dois ticks e também atravessa
o estilhaço. Corrente já existente espera o land do avanço —
o sit não come a pose do dash; o pedido não decai no travel.
Arquivo no
disco não é peso percebido. A ameaça que
ainda não chegou marca o trilho (`approaching`) — na porta a mostra
usa o mesmo aviso; a live já nomeava o perigo e o trilho calava.
A câmera inclina para o mesmo aviso (`lookAheadX`), menor que o
punch do dash. Lean no disco não é peso percebido. A recuperação do dash muda a
silhueta; o erro acende o campo, a coleta não. O controle pulsa no
impacto com duração e magnitude por verbo; pausa e descarte cancelam.
Cada verbo deixa um rastro próprio no campo; com menos movimento o
rastro vira marca. A corrente mora no corpo em pips; o HUD continua
com a conta. A faixa do dash enche o tempo de recuperação e
cooldown e veste o look — rótulo sozinho era o mesmo quadro.
O fecho da partida contorna o campo e pulsa o controle a cada
segundo; não é faixa no HUD. Com menos movimento vira traço.
A prática e a guarda falam no mixer quando a janela acaba;
o orbe que cai fala, acende o campo, marca o lugar, desloca
a câmera para baixo e senta o corpo quando o verbo está parado;
no avanço, no coil e no sit da guarda a queda marca o chão e
não senta o compromisso. Sem pulsar o controle. Arquivo no disco não é peso percebido. A coleta leva o orbe ao slot; o erro espalha os pips;
na guarda eles voam para o placar; no fim a aposta não guardada
cai, o corpo senta (`squashOver`), o quadro senta (tremor, flash e
punch do último verbo não atravessam o overlay); na pausa o quadro
senta do mesmo jeito — o corpo fica na pose congelada — e o overlay nomeia o que caiu; no fim a cortina do over vence a pausa — P e aba escondida não comem a aposta — a queda vence a cortina, que
reusa a placa do look. As legendas nascem depois da cortina. O
raspo risca o campo, estreita o corpo, empurra a câmera na
direção e acende menos que a queda. Sem hitstop. Sem pulso no
controle. Nenhum some. A conta no estado
sobrevive ao fim — a órbita não.
A entrada continua separada da
regra em `src/core/input.js`. Perdão de entrada é decisão de design explícita com
valor registrado; sem registro, esses valores viram folclore e regridem na
próxima alteração. `felt` continua falso. Degraus e critérios da dimensão `feel`:
[barra de acabamento](../references/production-bar.md#feel--resposta-da-ação-central).
