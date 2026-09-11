# Optimize

Estabilidade sob orçamento no pior momento: distribuição de tempo de quadro pelo
pior percentil, cena de pior caso, carregamento frio, custo por ciclo de vida,
comparação em condições equivalentes. A qualidade visual aprovada é o piso;
otimizar é achar uma implementação mais eficiente do **mesmo** resultado. Receita:
[performance](../recipes/performance.md).

## Escala

`jam`: roda na máquina alvo declarada sem travar (`playable`). `product`:
orçamento de quadro declarado e a cena representativa cabendo nele, medida
(`slice`). `aa`: pior percentil, engasgos de carregamento, coleta e primeiro shader
tratados, tempo até jogar com teto (`shippable`).

## Avaliar

1. `context <projeto> --focus performance`. Leia o orçamento declarado (dispositivo,
   resolução, cena, tempo de quadro alvo, teto do pior percentil, tempo até jogar);
   sem orçamento não existe "rápido o suficiente" — declare antes de medir.
2. Sintoma percebido: engasgo, atraso de entrada, tempo de carga, consumo crescente.
   Cada um tem causa e correção diferentes: custo contínuo, engasgo pontual, vazamento.
3. Ferramenta de medição do pacote da plataforma; no starter, `npm run budget` mede
   a simulação por percentil e diz o que não cobre.
4. Pergunte só o que o orçamento não fixa: o dispositivo alvo real e o que a direção
   considera não negociável.

## Executar

Localize o gargalo no caminho real antes de mudar código (profiler, captura de
quadro, draw calls, alocação por quadro). Uma variável por vez. Implementação mais
eficiente do mesmo resultado: LOD, culling correto, batching, streaming, atlas,
pooling, cache de shader, menos alocação, trabalho não refeito por quadro. Cortar
sombras, efeitos ou animação é decisão de direção registrada como desvio aprovado,
nunca solução automática. Montar → desmontar → montar para vazamento
([ciclo de vida](../recipes/lifecycle.md)).

## Verificar

Distribuição de tempo de quadro (não FPS médio) na cena de pior caso, antes e
depois, mesmas condições; primeiro carregamento em ambiente frio; comparação visual
em movimento confirmando que o acabamento sobreviveu; consumo após um ciclo de
montar e descartar. `record --kind budget` com métrica, valor, unidade, plataforma,
ferramenta. Editor não é build exportado. Degraus: `performance` na
[barra](../references/production-bar.md).

## Nunca

- Medir média; o jogador sente o pior quadro.
- Rebaixar arte aprovada e chamar de otimização.
- Otimizar sem orçamento declarado ou sem localizar o gargalo.
- Mudar duas coisas e atribuir a melhora a uma.
- Medir com máquina quente de desenvolvimento e declarar para a máquina fria do jogador.

## Entregar

O gargalo, a hipótese, o custo antes e depois com condições, as tentativas
descartadas (inclusive as óbvias que não mudaram nada), e a comparação visual.
Sequência: [`harden`](harden.md) para o resto da confiança; [`polish`](polish.md).
