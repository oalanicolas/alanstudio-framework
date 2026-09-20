# Gênero — Roguelike / roguelite (runs, permadeath, geração procedural)

Aplicabilidade: `--genre roguelike`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: adaptar-se ao que a run oferece. Decisão: risco vs recompensa por sala,
  sinergias de build, quando parar. Meta-progressão (roguelite) abre opções, não
  compra a vitória.
- Geração: seed determina mapa, drops e encontros; regras de geração garantem
  solvabilidade e ritmo. Registre o que é seedado e o que não é.

## Feel que importa

- Morte rápida e reinício imediato (segundos); leitura do build em uma tela; recompensa
  com peso (som, luz, pausa curta) proporcional à raridade.
- Combate/ação com feel do subgênero (ver [shooter](shooter.md), [plataforma](platformer.md)).

## Riscos habituais

- Seed que não reproduz a run (RNG compartilhado com VFX/UI, ordem de inicialização).
- Geração que produz salas impossíveis ou triviais; sinergias que quebram a economia.
- Meta-progressão que torna as primeiras horas ruins por design.
- Save no meio da run: o que é permitido e como impedir exploit de save/load.

## Orçamentos e medições típicas

- Tempo de geração de mapa; tempo de morte → nova run; distribuição de duração de run
  e de vitórias por seed simulada; quadro p99 com muitos projéteis/inimigos.

## QA e playtest específicos

- Replay de run por seed com comparação de estado; geração em massa com validação
  (conectividade, itens obrigatórios, dificuldade); save/load na run.
- Playtest: a pessoa culpa a sorte ou a decisão? Quer "só mais uma"? Reconhece
  sinergias sem tutorial?

## Receitas e fontes

[ciclo de vida](../../recipes/lifecycle.md) (seed, reinício), [mecânicas](../../recipes/mechanics.md),
[conteúdo](../../recipes/content.md), [feel](../../recipes/feel.md).
