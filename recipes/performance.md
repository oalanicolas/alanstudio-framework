# Performance: estabilidade sob orçamento

Entrada: cena, dispositivo alvo e o sintoma percebido — engasgo, atraso de entrada,
tempo de carga ou consumo crescente.

A qualidade visual aprovada é o piso. Otimizar é encontrar uma implementação mais
eficiente do **mesmo** resultado; reduzir sombras, resolução, animação ou efeitos
para atingir um número é rebaixar o jogo, não otimizá-lo. Se a única saída for
cortar acabamento, isso é uma decisão de escopo e precisa ser registrada como tal.

Meça o que o jogador sente. FPS médio esconde exatamente o problema que importa:
use a distribuição do tempo de quadro e o pior percentil. Um jogo a 60 quadros com
um engasgo de 200 ms por minuto é lido como instável; um jogo estável a 30 não é.

Declare o orçamento antes de otimizar: dispositivo, resolução, cena representativa,
tempo de quadro alvo, teto do pior percentil e tempo até jogar. Sem orçamento não
existe “rápido o suficiente”, e cada medição vira opinião.

Localize o gargalo no caminho real antes de alterar código. Distinga custo por
quadro de evento pontual, porque as causas e as correções são diferentes:

- **Custo contínuo:** quantidade de objetos atualizados, trabalho por objeto,
  chamadas de desenho, custo de preenchimento, física, colisão, consultas
  repetidas e trabalho refeito por quadro sem necessidade.
- **Engasgo pontual:** alocação e coleta de lixo, primeira compilação de shader,
  carregamento e decodificação de recurso, criação de textura, mudança de cena,
  layout ou reflow, e o primeiro uso de qualquer caminho que ainda não aqueceu.
- **Vazamento:** listeners, timers, loops, texturas e conexões que sobrevivem ao
  descarte. Execute montar → desmontar → montar e compare o consumo; ciclo de vida
  tem receita própria em [lifecycle](lifecycle.md).

Compare alternativas em condições equivalentes e altere **uma** variável por vez;
sem isso não é possível atribuir causa. Registre o custo observado, a hipótese, o
resultado e as tentativas descartadas — inclusive as que pareciam óbvias e não
mudaram nada.

Confirme onde a prova vale. Editor não é build exportado; máquina de desenvolvimento
quente não é máquina do jogador fria. Aquecimento, cache e ferramentas de perfil
alteram o próprio resultado que estão medindo.

Implementação concreta: `tools/budget.mjs` do starter `canvas-arcade` mede a
simulação por percentil, não por média, e declara no próprio resultado que não
cobre render, áudio, carregamento nem o dispositivo alvo. O laço de passo fixo em
`src/core/loop.js` é o que torna essa medição comparável entre execuções.

Prova: distribuição de tempo de quadro na cena de pior caso, primeiro carregamento
em ambiente frio, comparação visual em movimento confirmando que o acabamento
sobreviveu, e o consumo após um ciclo completo de montar e descartar. Degraus:
[barra de acabamento](../references/production-bar.md#performance--estabilidade-não-média).
Direção visual e câmera continuam em [visual](visual.md).
