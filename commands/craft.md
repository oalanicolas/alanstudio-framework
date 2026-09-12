# Craft

Construir uma mudança de jogo de ponta a ponta com o acabamento pretendido: shape
com brief confirmado, fatia jogável que atravessa regra, apresentação e conteúdo,
feel e áudio do verbo, prova em movimento, registro e prompt de continuidade. É o
comando padrão para "crie", "mude", "adicione", "faça funcionar".

Antes de escrever código, três coisas precisam existir: o `context` do projeto
carregado, a escala identificada e uma direção confirmada para esta tarefa (vinda de
[`shape`](shape.md) ou dada pelo usuário). Contexto do projeto não é brief da tarefa. Se o craft recusa que contexto do projeto seja brief da tarefa, a área `gdd` do `scan` nomeia o brief que o craft já recusa. Contexto no disco não é o brief. Sem chave `brief`.

## Escala

- `jam`: brief curto ou uma seção de `game-design.md`; um ciclo jogável com feel do
  verbo e comparação em movimento fecham a sessão. Não gere a pasta de templates.
- `product`: brief + GDD/MDA, PRD/TDD do recorte; a fatia mira `slice` na barra.
- `aa`: os mesmos artefatos, com feel, áudio, luz, animação, pacing e receita de
  conteúdo como **requisitos do recorte**, não polimento depois.

O piso do verbo — decisão, feel sincronizado no impacto, áudio da consequência,
pacing — não é negociável em nenhuma escala ([ambição](../references/ambition.md)).

## Avaliar

1. `context <projeto> --focus create` (ou o foco que a mudança pede: `mechanics`,
   `feel`, `audio`, `content`…). Leia AGENTS aplicáveis, `foundation.read_first`, a
   receita e os pacotes em `read_next`. Se `foundation.audit.required`, rode
   [`teach`](teach.md) primeiro e retome aqui.
2. Projeto sem destino no disco e engine web: [`init`](init.md) com um starter é
   REUSE; escrever loop, save e entrada do zero é CREATE e exige lacuna escrita.
3. Direção confirmada. Se o pedido e o brief já fixam fantasia, verbo, plataforma e
   prova sem ambiguidade real, o shape pode ser **compacto** (3–5 linhas: o que se
   constrói, o verbo, a prova, "confirme ou corrija"). Se há ambiguidade material,
   rode [`shape`](shape.md) inteiro. **Pare e espere a confirmação.** Shape confirmado
   é sinal verde para construir; não é licença para pular feel e áudio.

Portões que não se comprimem: (1) brief confirmado; (2) referência visual ou sonora
aprovada quando a mudança é de direção — `--event direction-approved` e base
sincronizada no mesmo turno ([roteiro](../references/project-audit.md#aprovação-de-direção-materializar-e-continuar));
(3) apresentação da fatia com prova. Uma confirmação não autoriza publicar nem delegar.

## Executar

1. **REUSE → ADAPT → CREATE** no jogo, no acervo e nas fontes do foco
   ([processo §2](../references/process.md)). Som: `sfx search` antes de baixar.
   Registre necessidade → candidatos/consumidores → decisão → limite → prova.
2. **Arquitetura proporcional** se a mudança toca contratos, estado/tempo, saves,
   render ou integrações: [receita](../recipes/architecture.md) (`--focus architecture`).
3. **Fatia jogável**: perceber → decidir → agir → consequência → reinício, no caminho
   real do jogador. [Criar](../recipes/create.md) e [mecânicas](../recipes/mechanics.md).
   Título e cores novos não demonstram experiência nova.
4. **Feel e áudio desse verbo**, no mesmo recorte: [feel](../recipes/feel.md) e
   [áudio](../recipes/audio.md). Flash, hitstop, shake, partícula e som no **mesmo
   quadro** do contato. Arte provisória é aceitável com direção declarada; verbo mudo
   ou sem peso não é.
5. Em passes deliberados, como uma definição de pronto: estrutura da regra; estados
   (pausa, perda, reinício, saída); apresentação; feel/áudio; entrada em cada
   dispositivo alvo; conteúdo real, sem placeholder que fica.

## Verificar

- Validadores do projeto e o cenário afetado por `verify --script … --output PASTA_NOVA`
  (ou `--command`). Quando os testes exercitarem pause, reset, seed, observe, act,
  advance, capture ou dispose, anexe `--proves`; sai como `claimed`, nunca verificado.
- **Jogue o recorte** com as ferramentas do harness (navegador, captura, execução).
  Compare antes/depois em condições equivalentes e **em movimento**. Leia a captura
  de volta; uma captura que você não leu não conta.
- Critique o resultado contra o brief e contra as recusas do `SKILL.md`; corrija o
  material e reinspecione. Não invente defeito para parecer iteração: "primeira
  passagem limpa" é resposta válida quando é verdade.
- Não conta como prova: build verde para diversão, screenshot para feel, typecheck
  para reinício, avaliação do agente para aprovação do usuário.
  `experience_status` fica `not_assessed` até observação em movimento.

## Nunca

- Pular o shape porque o pedido "parecia claro" e descobrir a ambiguidade no código.
- Entregar scaffold, título ou HUD novo como fatia. Slice demonstra experiência
  **e** repeatability; PoC responde uma pergunta; scaffold demonstra estrutura.
- Acrescentar runtime comum, hierarquia de agentes, ECS ou IA por quadro para
  absorver um contrato.
- Chamar o recorte de AAA ou "quase AAA" sem `finish` observado.
- Publicar, delegar ou contatar pessoas por conta de uma confirmação de avanço.

## Entregar

Mostre a fatia no estado principal e nos estados-chave (perda, reinício, pausa);
diga o que foi observado em movimento, o que foi corrigido após inspeção, o que foi
herdado/adaptado/criado, e o que ficou de fora. Faça a
[revisão de entrega](../references/delivery.md) no registro existente, atualize o
canônico (Devlog/plano) e cumpra `continuity.before_close` e
`documentation.before_close`. Extraia [aprendizado transferível](../references/learning.md)
para o framework quando houver. Termine com **uma** próxima ação e o prompt de
continuidade pronto ([roteiro](../references/gauntlet.md)); depois, pergunte o que
funciona e o que não funciona. Sequência natural: [`critique`](critique.md) ou
[`polish`](polish.md).
