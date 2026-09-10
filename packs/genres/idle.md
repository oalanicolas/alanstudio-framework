# Gênero — Idle e incremental (clicker, idle, prestige)

Aplicabilidade: `--genre idle`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: otimizar crescimento. Decisões: o que comprar agora (retorno por custo),
  quando resetar (prestige), quando ficar ativo vs deixar rodar, quais
  multiplicadores destravar.
- Modelo: clicker ativo, idle puro (progresso offline), híbrido com minijogo ou
  camadas (Antimatter Dimensions). Registre a curva de números (linear, exponencial,
  notação) e o horizonte (dias, meses).

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Números subindo com satisfação: formatação legível (1.2M, notação científica
  opcional), animação de compra, som por marco; "a próxima compra" sempre visível
  com tempo estimado.
- Retorno offline claro: "enquanto você esteve fora, ganhou X" em tela dedicada.
- UI rápida: comprar 1/10/100/máx; nenhum clique inútil.

## Riscos habituais

- Muro de tempo sem decisão nova (só esperar); prestige que não muda o jogo;
  precisão numérica (float64 estoura ~1e308; usar big number ou log) e overflow
  em saves; progresso offline explorável por relógio do sistema.
- Consumo de bateria/CPU em segundo plano; monetização predatória; sem fim ou
  fim sem cerimônia.

## Orçamentos e medições típicas

- Tempo por camada/prestige em simulação (curva alvo vs real); CPU em idle (deve
  tender a zero fora de foco); tamanho e frequência do save; retenção D1/D7 se houver
  telemetria consentida.

## QA e playtest específicos

- Simulação headless da economia com estratégia gulosa e ótima (tempo até cada marco);
  cálculo offline com relógio adiantado/atrasado; precisão em números extremos;
  save/load em cada camada.
- Playtest: a pessoa sabe o que comprar sem calculadora? Volta depois de 8 horas?
  O prestige parece perda ou ganho?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md) (economia, números), [conteúdo](../../recipes/content.md)
(saves, offline), [ciclo de vida](../../recipes/lifecycle.md) (foco, segundo plano),
[produção](../../recipes/production.md). Vizinhos: [simulação](simulation.md), [casual](casual.md).
