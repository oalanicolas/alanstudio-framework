# Exemplo compacto — da trilha jogável ao capítulo acabado

**Exemplo de aplicação da receita de produção, não plano aprovado para um jogo.**
Continua [a trilha de João e Maria](era-uma-vez-preproduction.md) depois que a PoC
mostrou que a pessoa marca a trilha e usa as marcas para voltar. Todos os números
abaixo são hipóteses ilustrativas; nenhum foi medido para este documento.

## Alvo de acabamento

Plataforma: navegador desktop e tablet, 60 Hz, mouse e toque. Referência de
acabamento: contos ilustrados em movimento — silhuetas legíveis, luz que muda com a
hora do conto, som só nas interações. Lentes obrigatórias: design, arte, áudio, feel,
UX/acesso, técnica, QA. Localização: português primeiro; inglês adiado com motivo
(texto ainda muda a cada playtest). Não pode degradar: a ilustração aprovada da
floresta e a leitura das marcas a distância.

## Orçamentos (hipóteses até a primeira medição)

| Orçamento | Meta | Como medir | Estado |
| --- | --- | --- | --- |
| Tempo de quadro p99 | 16 ms no tablet de referência | DevTools performance, travessia completa | hipótese |
| Carregamento inicial | 3 s em 4G | Lighthouse e cronômetro no dispositivo | hipótese |
| Latência toque → marca aparece | 2 quadros | captura 240 fps do tablet | hipótese |

Primeira medição vira recibo:

```sh
python3 scripts/game.py record /lab/era-uma-vez --kind budget --author "Alan" \
  --note "Travessia completa, tablet de referência, build 3f2c1" \
  --field metric=frame_p99 --field value=14.2 --field unit=ms \
  --field platform=tablet-ref --field tool=devtools --output /lab/evidence/era-budget-01
```

O recibo guarda HEAD e status do git; o plano passa a citar a pasta, e o estado da
linha muda de `hipótese` para `medido`.

## Marcos deste capítulo

- **First playable:** ida, marcas, noite, volta; placeholders. Prova: `verify --script test`
  verde + observação de uma pessoa completando a volta sem instrução. Estado: atingido
  na PoC (recibo de observação `obs-01`, role=human).
- **Vertical slice:** a mesma travessia com a ilustração aprovada, som das marcas e
  transição de luz. Prova: comparação em movimento com a referência e receita para o
  próximo trecho (a casa de doces) custeada. Estado: pendente.
- **Alpha:** três trechos com todas as mecânicas do capítulo (marcar, voltar, migalhas
  consumidas, casa). Conteúdo pode faltar arte final. Estado: pendente.
- **Beta:** capítulo completo, orçamentos medidos dentro da meta, acesso (contraste,
  alvos de toque, movimento reduzido) implementado, playtest externo com 3 pessoas.
  Estado: pendente.
- **Gold:** zero bloqueadores triados, save/recarga e reinstalação verificados,
  créditos completos. Estado: pendente.

## Revisão de marco, quando chegar a hora

`context /lab/era-uma-vez --focus production --stage milestone` carrega a receita e o
template. A revisão lê cada critério contra o recibo correspondente (`verify` para
técnica, `record --kind observation` para experiência, `record --kind budget` para
orçamentos). A passagem é registrada por pessoa:

```sh
python3 scripts/game.py record /lab/era-uma-vez --kind milestone --author "Alan" \
  --note "Vertical slice: critérios com evidência em evidence/vs-*; desvio aceito: som da migalha provisório" \
  --field milestone=vertical-slice --field decision=declared --field declared_by=Alan --field role=human \
  --output /lab/evidence/era-vs-gate
```

Um recibo com `role=agent` registra a avaliação do agente e não substitui essa decisão.

## Riscos

| ID | Risco | Sinal | Mitigação |
| --- | --- | --- | --- |
| RISK-01 | marcas ilegíveis no tablet à noite | pessoa procura a marca por mais de 3 s | PoC de contraste noturno antes da vertical slice |
| RISK-02 | transição de luz estoura o quadro | p99 acima de 16 ms na travessia | medir antes de adicionar partículas; alternativa: gradiente pré-computado |

## Continuidade

- **Onde estamos:** first playable atingido; vertical slice pendente.
- **Próximo passo:** TASK-VS-01 — aplicar a ilustração aprovada à travessia e medir o p99.
- **Por que agora:** RISK-02 pode invalidar a direção de luz antes de haver mais conteúdo.
- **Pronto quando:** comparação em movimento aprovada por Alan e recibo de orçamento dentro da meta.
- **Retomar por:** este plano, `record.json` em `evidence/`, e o design system do jogo.

Este exemplo cabe em um documento porque o capítulo é pequeno. Um jogo com mais
sistemas separa plano, revisões de marco e registro de riscos; o harness localiza o
plano como fonte de continuidade e nada mais.
