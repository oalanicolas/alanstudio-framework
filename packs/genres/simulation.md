# Gênero — Simulação e gestão (fábrica, automação, tycoon, city builder, colônia)

Aplicabilidade: `--genre simulation`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: construir sistemas que funcionam sem você. Decisão: onde investir, o que
  automatizar, que gargalo resolver. Satisfação vem de ver o sistema fluir e escalar.
- Economia: fontes, transformações, sumidouros e taxas; toda cadeia tem gargalo
  legível. Registre unidades e o que é determinístico.

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Feedback de fluxo: itens visíveis em esteiras/tubos, indicadores de gargalo, som de
  atividade proporcional; construção com snap, preview e desfazer.
- Câmera livre com limites; zoom com nível de detalhe coerente; hora do dia e clima
  como ritmo.

## Riscos habituais

- Simulação dependente do FPS ou de ordem de atualização (perda/duplicação de itens):
  passo fixo, ordem determinística, tick lógico separado do render.
- Explosão de custo com escala (milhares de entidades): dados orientados, chunks,
  simulação em nível de detalhe.
- Save enorme e migração entre versões; pausa que não congela tudo (timers, sons).
- Gargalo invisível: jogador não sabe por que a produção parou.

## Orçamentos e medições típicas

- Tempo do tick lógico por N entidades (curva de escala); quadro p99 em base grande;
  tamanho e tempo de save/load; memória por entidade; paridade 30/60/144 FPS.

## QA e playtest específicos

- Linha temporal mínima (fonte → máquina → esteira → armazém) sem perda/duplicação,
  com bloqueio, pausa/save/recarga preservando estado; soak de horas.
- Playtest: a pessoa identifica o gargalo sozinha? Planeja antes de construir? Sente
  progresso ao automatizar?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md), [ciclo de vida](../../recipes/lifecycle.md)
(relógio controlado, seed), [arquitetura](../../recipes/architecture.md),
[produção](../../recipes/production.md). Exemplo de continuidade com fábrica 2D em
[processo](../../references/process.md#continuidade-e-retomada).
