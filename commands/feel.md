# Feel

Dar peso, timing e recuperação à ação central: o intervalo entre o input e a
certeza de que o mundo respondeu. Use quando o verbo funciona mas não convence,
quando "falta juice" ou quando o jogador não sente o impacto. Receita canônica:
[feel](../recipes/feel.md); contrato: [design system do jogo](../references/game-design-system.md).

## Escala

O piso é o mesmo em todas: flash, hitstop, shake, partícula, câmera e som disparam
no **mesmo quadro** do contato; dessincronia vira dois eventos. `jam` fecha o feel
de um verbo. `product`/`aa` fecham o feel de cada ação central e registram os
tokens de tempo/câmera no design system, com consumidor.

## Avaliar

1. `context <projeto> --focus feel` (o pacote de gênero diz que feel importa no
   verbo: pule com `--genre`). Leia o verbo no GDD, os tokens de tempo/câmera/áudio e
   a referência de sensação aprovada, ou proponha uma e peça aprovação.
2. **Isole um verbo.** Separe regra (a ação é legal), apresentação (a mudança é
   perceptível) e feel (a percepção tem peso). Regra corrigida não substitui feel;
   animar demais não substitui regra. Sem ciclo jogável, volte a [`craft`](craft.md).
3. Percorra a **cadeia**: intenção → input (latência, buffer, cancelamento, perda de
   foco) → antecipação → corpo (squash, follow-through) → impacto → câmera → áudio →
   recuperação. Nomeie o elo que falha e a diferença percebida entre intenção e
   resposta atual, em movimento.
4. Pergunte só o que a referência não responde: a sensação alvo em palavras físicas
   ("pesado e curto", "elástico e longo"), e se o perdão de entrada é intencional.

## Executar

REUSE → ADAPT → CREATE em animação, som e câmera do próprio jogo e do acervo. Ajuste
**um elo por vez**, com constante nomeada, num lugar só, com unidade (`hitstopFrames
= 3`, não um número solto). Compare em movimento com a versão anterior nas mesmas
condições. Juice que esconde a consequência ou o próximo obstáculo é regressão, não
acabamento. O starter `canvas-arcade` é implementação de referência do laço de
passo fixo que torna a medição comparável.

## Verificar

Prova em movimento: vídeo ou execução lado a lado, latência da entrada até o
primeiro quadro de resposta, e a ação repetida por um minuto **sem objetivo** — se
cansa, o feel não fechou. `record --kind observation --field role=agent` com a
captura; observação de pessoa entra por [`playtest`](playtest.md). Screenshot não
prova feel. Degraus: [barra](../references/production-bar.md), dimensão `feel`.

## Nunca

- Ativar juice por checklist de gênero em vez de pelo sinal próprio do verbo.
- Disparar som, flash e câmera em quadros diferentes "porque cada sistema tem seu tempo".
- Ajustar dois elos ao mesmo tempo e atribuir a melhora a um deles.
- Tratar partículas ou loop de fundo como feel.
- Declarar `slice` em `feel` sem a cadeia inteira observada em movimento.

## Entregar

O elo ajustado, a constante e seu consumidor, a comparação em movimento, o degrau
observado com condição. Sequência: [`audio`](audio.md) para a consequência sonora
desse verbo, [`juice`](juice.md) para amplificar o sinal do impacto quando o timing
já está certo.
