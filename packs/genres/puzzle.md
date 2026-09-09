# Gênero — Puzzle (lógica, física, match, quebra-cabeça espacial)

Aplicabilidade: `--genre puzzle`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: perceber, hipotetizar, testar. A regra deve ser aprendida por experimentação,
  não por texto; cada nível introduz uma ideia ou combina duas já dominadas.
- Curva: sequência de níveis como currículo; solução única ou aberta — registre qual e
  o que conta como "resolvido".

## Feel que importa

- Desfazer/refazer instantâneos e ilimitados quando o gênero permite; reinício sem
  custo; resposta imediata a cada movimento; "aha" sublinhado por som/luz, não por
  texto.
- Legibilidade: estado inteiro visível ou memória explícita; forma além da cor.

## Riscos habituais

- Nível resolvível por força bruta ou por atalho não previsto (solver ajuda a detectar).
- Regra ambígua descoberta tarde; feedback de "por que não posso" ausente.
- Dificuldade em degrau; ausência de pistas progressivas quando o jogador trava.

## Orçamentos e medições típicas

- Tempo de resposta por movimento; tempo de carga por nível; taxa de reinício e de
  uso de desfazer por nível (observada, não presumida).

## QA e playtest específicos

- Solver automático para confirmar solução mínima e ausência de soluções indesejadas;
  undo/redo em todas as ações; salvar no meio do nível.
- Playtest: onde a pessoa trava e o que tenta? Ela formula a regra em voz alta? Pula
  níveis? Registre hesitação e ordem de tentativas.

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md), [conteúdo](../../recipes/content.md) (níveis),
[qualidade](../../references/quality.md).
