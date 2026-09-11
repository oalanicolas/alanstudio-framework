# Gênero — Sobrevivência e crafting (sandbox, colônia, base building)

Aplicabilidade: `--genre survival-crafting`. Orientação de gênero para direcionar
perguntas, riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: transformar o mundo para durar. Decisões: onde acampar, o que coletar agora
  vs depois, o que construir, quanto arriscar em expedições, gestão de necessidades
  (fome, temperatura, sanidade).
- Modelo: sandbox voxel/tile (mundo editável), colônia (gestão indireta de agentes),
  survival puro (recursos e ameaças). Registre a curva: quando a sobrevivência deixa
  de ameaçar e o que toma seu lugar (construção, exploração, sociedade).

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Coleta e construção com resposta imediata (som por material, partícula, snap de
  peça); inventário rápido (arrastar, empilhar, filtros); crafting com receitas
  legíveis e "posso fazer agora" visível.
- Ciclo dia/noite e clima que mudam decisão, não só cor; ameaças anunciadas.

## Riscos habituais

- Grind sem propósito (tempo de coleta sem decisão); necessidades que interrompem
  o que é divertido; economia sem ralo (recursos infinitos) ou muro de receitas.
- Mundo persistente: saves grandes e lentos, corrupção, migração de versão; física
  de construções (colapso) explorável; geração procedural sem garantia de recursos
  essenciais.
- Multiplayer: griefing, autoridade de inventário no cliente.

## Orçamentos e medições típicas

- Tempo de save/load por tamanho de mundo; memória por chunk carregado; quadro p99 em
  base grande (contagem de entidades/luzes); taxa de recurso por hora em simulação;
  tempo até primeiro abrigo em playtest.

## QA e playtest específicos

- Simulação headless de economia (fontes/ralos por hora); geração com seeds e
  verificação de recursos essenciais alcançáveis; save/load com base máxima;
  migração de save entre versões.
- Playtest: a pessoa sabe o que fazer na primeira noite? Constrói algo próprio nas
  primeiras 2 horas? Volta para "só mais uma coisa"?

## Receitas e fontes

[conteúdo](../../recipes/content.md) (saves, procedural), [mecânicas](../../recipes/mechanics.md)
(economia), [arquitetura](../../recipes/architecture.md), [produção](../../recipes/production.md).
Combina com [simulação](simulation.md) (colônia) e [roguelike](roguelike.md) (permadeath).
