# Feel: resposta da ação central

Entrada: a ação que o jogador mais repete e a diferença entre o que ela deveria
provocar e o que provoca hoje.

Feel não é dificuldade nem quantidade de efeito. É a relação entre a intenção do
jogador e o que o sistema devolve. A pergunta de aceite é direta: **a ação é
gostosa de repetir mesmo sem objetivo?** Se a resposta exige explicar o contexto,
o problema está aqui.

Comece pela cadeia de latência real, não pela camada de efeitos: leitura da
entrada, quadro em que o estado muda, quadro em que o jogador percebe. Meça em
quadros, não em impressão. Buffer de entrada acumulado, polling em intervalo
diferente do passo de simulação, animação que precisa terminar antes de aceitar a
próxima ação e transição que engole o comando produzem “controle pesado” sem que
nenhum efeito visual esteja errado.

Descreva a ação em três momentos e verifique se cada um tem sinal próprio:

- **Antecipação:** o jogo avisa que a ação começou, antes do resultado.
- **Contato:** o instante do efeito. Interrupção breve do tempo (hitstop), som,
  deformação e deslocamento de câmera coincidem aqui, não em quadros dispersos.
- **Recuperação:** o retorno ao estado neutro e quando a próxima ação é aceita.

Perdão de entrada é decisão de design explícita, com valor registrado: buffer de
comando antes da janela, tolerância após sair da condição válida (coyote time),
assistência de alvo, tamanho efetivo de colisão diferente do desenho. Sem registro,
esses valores viram folclore e regridem na próxima alteração.

Antes de adicionar efeito, tente a solução menor: corrigir a ordem de atualização,
antecipar o feedback um quadro, encurtar a recuperação. Tremor de câmera não é
correção universal e precisa respeitar redução de movimento; efeito somado a uma
resposta lenta produz ruído, não peso.

Ligue cada sinal ao verbo do GDD e ao design system do jogo, na seção de feel. Um
sinal que não corresponde a mudança de estado ensina errado e prejudica a
[legibilidade](../references/production-bar.md).

Implementação concreta para ler antes de escrever a sua: o starter
`canvas-arcade` reúne o perdão de entrada em `CONFIG`, em `src/game/rules.js` —
buffer de dash, graça após dano, alcance de coleta maior que o desenho — cada
valor com o motivo ao lado, e separa entrada de regra em `src/core/input.js`.

Prova: clipe em movimento antes e depois nas mesmas condições, contagem de quadros
entre entrada e primeira resposta, repetição da ação por um minuto sem objetivo, e
o mesmo teste em cada dispositivo de entrada suportado. Teste automatizado confirma
a regra; feel exige observação. Degraus e critérios:
[barra de acabamento](../references/production-bar.md#feel--resposta-da-ação-central).
