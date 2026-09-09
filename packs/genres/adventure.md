# Gênero — Aventura gráfica (point-and-click, escape room, hidden object)

Aplicabilidade: `--genre adventure`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal. Para ficção por texto e
visual novel, ver [narrativa](narrative.md).

## Verbo central e decisões

- Verbo: investigar e combinar. Decisões: onde olhar, o que pegar, o que usar com
  o quê, com quem falar e sobre o que; ordem de resolução em puzzles abertos.
- Modelo: clássico (inventário, verbos, diálogo), escape room (um espaço denso),
  hidden object/casual, aventura moderna com cenas e QTE. Registre a lógica dos
  puzzles: dedutiva (pistas no mundo) vs associativa (lógica de cartoon) e o tom.

## Feel que importa

- Hotspots claros (highlight opcional, cursor que muda, tecla para revelar) sem
  pixel hunting; caminhar rápido (duplo clique para pular travessia); diálogo com
  histórico e pulo por linha.
- Feedback para tentativas erradas que ensina ("isso não vai funcionar porque…"),
  não uma frase genérica; inventário sempre visível ou a um toque.

## Riscos habituais

- Puzzle "leia a mente do designer": solução sem pista; combinações exaustivas
  como estratégia dominante; dead ends (estado sem solução, item perdido) sem
  aviso; backtracking longo.
- Máquina de estados de flags espalhada em scripts: ordem inesperada quebra
  diálogos; saves em estado intermediário de cutscene; localização que quebra
  trocadilhos-chave.

## Orçamentos e medições típicas

- Tempo por puzzle em playtest (mediana e cauda); taxa de uso de dica; contagem de
  tentativas erradas antes da solução; tempo de troca de cena; tamanho por cena
  (fundos em alta resolução).

## QA e playtest específicos

- Grafo de estados (puzzle dependency chart) verificado: toda solução alcançável,
  sem dead end; walkthrough automatizado por script de ações; tentativa de cada
  item em cada hotspot sem crash; save/load em cada estado de flag.
- Playtest: a pessoa verbaliza a hipótese antes de tentar? Quando trava, sabe onde
  procurar? Ri nas respostas de erro?

## Receitas e fontes

[conteúdo](../../recipes/content.md) (diálogo, flags, saves, localização),
[mecânicas](../../recipes/mechanics.md) (grafo de dependência), [feel](../../recipes/feel.md),
[produção](../../recipes/production.md). Vizinhos: [narrativa](narrative.md), [puzzle](puzzle.md), [horror](horror.md).
