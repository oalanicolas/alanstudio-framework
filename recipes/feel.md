# Feel da ação

Entrada: verbo central, referência de sensação (aprovada ou proposta) e a
diferença percebida entre intenção e resposta atual.

Depois da partida, o achado precisa de forma. `playtest <projeto>` lê se o
disco tem problema, evidência, hipótese e medição. Recibo sem os quatro é
impressão — `next` propõe `playtest.unstructured`. `playtest --invite`
escreve a página e aponta `/?invite=1`, onde a tabela some; `next` a
aponta depois do recibo de quem fez. O serve anuncia a URL da rede
se a máquina tiver outro endereço IPv4. Esconder a tabela e anunciar
a rede não são alguém de fora. `observed` e `outsider` são sempre
falsos: o harness não assiste à sessão. O starter grava um candidato com
`npm run session` em `docs/playtest/last-run.json`. Se o projeto (ou o
starter) declara `session`, `then` a aponta. `note --from-run` anexa o
resumo e, se houver, a curva — o mapa já põe `--from-run` quando o
arquivo existe. Número no disco não é causa nem sessão observada. O
autor sugerido no comando não é quem jogou.

Feel é o intervalo entre o input e a certeza de que o mundo respondeu.
Swink: controle em tempo real, espaço simulado, polish. Jam e piso de
acabamento se separam aqui com mais frequência do que na escolha da engine.
Sem feel, o ciclo pode estar correto e o jogo parecer vazio. Sem sincronia,
o juice vira ruído.

Leia o verbo no GDD, os tokens de tempo/câmera/áudio no
[design system](../references/game-design-system.md) e o
[piso](../references/quality.md). `context --focus feel` seleciona esta
receita. `feel <projeto>` lê as constantes nomeadas no `CONFIG` e o
recibo de observação no disco; `felt` é sempre falso. `note <projeto>`
grava o recibo curto depois da partida. O usuário não
precisa pedir “ative o juice”.

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
4. **Resposta de corpo** — squash, stretch, deslocamento, IK, arma, veículo
   ou cursor. A silhueta muda o bastante para ser lida em movimento.
5. **Impacto** — hitstop, freeze frames, flash, partículas, rumble, stinger.
   Duração proporcional à importância; impacto de coleta não pode parecer
   golpe mortal, e o contrário também. Visual, áudio e pause de hit disparam
   no **mesmo frame** do contato. Alguns milissegundos de atraso fazem o
   cérebro registrar dois eventos, não um peso.
6. **Câmera** — punch, lookahead, aterrissagem, oclusão, recuperação. A
   câmera confirma a ação sem enjoar nem esconder o próximo risco.
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
Observe também pause, perda de foco, reinício e troca de entrada: um
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
guardar, graça após dano, alcance de coleta maior que o desenho — cada valor com o
motivo ao lado. Guardar no hitstop não é engolido; um toque sem corrente não decide
o próximo orbe. Cada verbo desloca a câmera numa direção própria e achata o corpo
numa medida própria: coleta, dash, aterrissagem, guardar e o erro não compartilham
squash. O dash aterrissa: o corpo senta, a câmera confirma para baixo
e o rastro cai — distintos da partida. A ameaça que
ainda não chegou marca o trilho (`approaching`); a recuperação do dash muda a
silhueta; o erro acende o campo, a coleta não. O controle pulsa no
impacto com duração e magnitude por verbo; pausa e descarte cancelam.
Cada verbo deixa um rastro próprio no campo; com menos movimento o
rastro vira marca. A corrente mora no corpo em pips; o HUD continua
com a conta. A faixa do dash enche o tempo de recuperação e
cooldown e veste o look — rótulo sozinho era o mesmo quadro.
O fecho da partida contorna o campo e pulsa o controle a cada
segundo; não é faixa no HUD. Com menos movimento vira traço.
A prática e a guarda falam no mixer quando a janela acaba;
o orbe que cai fala e acende o campo, sem pulsar o controle.
Arquivo no disco não é peso percebido. A coleta leva o orbe ao slot; o erro espalha os pips;
na guarda eles voam para o placar; no fim a aposta não guardada
cai e o overlay nomeia o que caiu — a queda vence a cortina, que
reusa a placa do look. As legendas nascem depois da cortina. O
raspo risca o campo. Nenhum some. A conta no estado
sobrevive ao fim — a órbita não.
A entrada continua separada da
regra em `src/core/input.js`. Perdão de entrada é decisão de design explícita com
valor registrado; sem registro, esses valores viram folclore e regridem na
próxima alteração. `felt` continua falso. Degraus e critérios da dimensão `feel`:
[barra de acabamento](../references/production-bar.md#feel--resposta-da-ação-central).
