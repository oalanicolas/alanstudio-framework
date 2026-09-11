# Gênero — RPG (ação, por turnos, JRPG, CRPG)

Aplicabilidade: `--genre rpg`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: crescer e escolher quem ser. Decisão: build, equipamento, aliados, rota,
  diálogo. Progressão precisa abrir opções e leitura, não só aumentar números.
- Sistemas: atributos, combate (ação ou turno), inventário, quests, diálogo, mundo.
  Cada um tem dono de estado e fonte de dados; registre o mapa.

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Combate: acerto legível (hitstop, número, som por tipo de dano), telegraph de
  inimigos, cancelamento e buffer; por turnos, ver [turno](turn-based.md).
- Recompensa: som e animação de level up/loot proporcionais à raridade; UI que
  responde (barras com easing, comparação de equipamento).
- Mundo: landmarks, música por região, transições sem corte quando possível.

## Riscos habituais

- Dados em código (stats, tabelas) sem fonte externa; balanceamento sem simulação.
- Save: estado enorme, quests em meio de fase, migração entre versões; softlock por
  quest em estado inconsistente.
- Escala de conteúdo: centenas de itens/inimigos sem receita de produção e validação.
- Opção dominante de build; dificuldade que só escala números.

## Orçamentos e medições típicas

- Tempo de carga de área; quadro p99 em cidade cheia; tamanho de save; tempo de
  simulação de N combates para balancear; memória de assets por região.

## QA e playtest específicos

- Simulação em massa de combates por seed para distribuição de resultados; testes de
  cada quest em ordem alternativa e com save/recarga; inventário nos limites.
- Playtest: a pessoa entende por que ganhou/perdeu? Muda de build por decisão? Sabe
  para onde ir sem marcador?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md), [conteúdo](../../recipes/content.md)
(saves, narrativa), [arquitetura](../../recipes/architecture.md), [produção](../../recipes/production.md).
