# Craft

Construir uma mudança de jogo de ponta a ponta com o acabamento pretendido: direção
resolvida, fatia jogável que atravessa regra, apresentação e conteúdo, feel e áudio
do verbo, acesso verificado, prova em movimento e continuidade. É o
comando padrão para "crie", "mude", "adicione", "faça funcionar".

Antes de escrever código, três coisas precisam existir: o `context` do projeto
carregado, a escala identificada e uma direção confirmada para esta tarefa (vinda de
[`shape`](shape.md) ou dada pelo usuário). Contexto do projeto não é brief da tarefa.

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
   receita e os pacotes em `read_next`. Em jogo existente com `foundation.audit.required`,
   rode [`teach`](teach.md) primeiro e retome aqui. Destino ainda inexistente segue
   para o preparo abaixo; não audite como jogo construído uma pasta por criar.
2. Projeto sem destino no disco: avalie o starter por adequação, como em
   [`init`](init.md). Use `start <destino> --starter <nome> --idea "..."` quando
   adequado para começar sem a pasta de rascunhos. O comando fornece infraestrutura;
   o agente adapta regras e apresentação à experiência pedida. Criar loop, save e
   entrada exige lacuna de reuso explícita. Preserve a plataforma escolhida.
3. Resolva a direção. Se pedido e decisões aceitas já definem o recorte, registre um
   brief compacto e execute; não repita a confirmação. Se faltar uma escolha que
   muda materialmente a experiência, use a descoberta de [`shape`](shape.md) e peça
   apenas essa decisão. Uma frase vaga não autoriza inventar uma direção completa.

Portões que não se comprimem: (1) direção resolvida com autorização para o recorte;
(2) referência visual ou sonora aprovada quando a mudança é de direção —
`--event direction-approved` e base
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
   Para jogo-modelo, universo ou estilo indicado, execute a
   [adaptação de referências](../references/reference-adaptation.md): cena principal
   comparada às fontes antes de expandir conteúdo. Título e cores não bastam.
4. **Feel e áudio desse verbo**, no mesmo recorte: [feel](../recipes/feel.md) e
   [áudio](../recipes/audio.md). Flash, hitstop, shake, partícula e som no **mesmo
   quadro** do contato. Arte provisória serve à investigação de regras; uma entrega
   com estilo visual pedido precisa demonstrar esse estilo na cena jogável. Verbo
   mudo ou sem peso não cumpre o recorte.
5. Em passes deliberados, como uma definição de pronto: estrutura da regra; estados
   (pausa, perda, reinício, saída); apresentação; feel/áudio; entrada em cada
   dispositivo alvo; conteúdo real, sem placeholder que fica.

## Verificar

- Validadores do projeto e o cenário afetado por `verify --script … --output PASTA_NOVA`
  (ou `--command`). Quando os testes exercitarem pause, reset, seed, observe, act,
  advance, capture ou dispose, anexe `--proves`; sai como `claimed`, nunca verificado.
- **Jogue o recorte** com as ferramentas do harness (navegador, captura, execução).
  Execute o preparo autorizado, verifique a página ou aplicação acessível e exercite
  a ação repetida, suas transições até a consequência e o reinício. Um primeiro
  ponto ou captura não verifica movimento contínuo, fim de poder ou variedade
  prometida. Receber um comando de `play`/`open` ainda não cumpre essa entrega.
  Compare antes/depois em condições equivalentes e **em movimento**. Leia a captura
  de volta; uma captura que você não leu não conta.
- Critique o resultado contra o brief e contra as recusas do
  [piso de execução](../references/craft-floor.md); corrija o
  material e reinspecione. Não invente defeito para parecer iteração: "primeira
  passagem limpa" é resposta válida quando é verdade.
- Não conta como prova: build verde para diversão, screenshot para feel, typecheck
  para reinício, avaliação do agente para aprovação do usuário.
  `experience_status` fica `not_assessed` até observação em movimento.

## Nunca

- Pular a leitura da intenção e das decisões porque o pedido "parecia claro".
- Entregar scaffold, título ou HUD novo como fatia. Slice demonstra experiência
  **e** repeatability; PoC responde uma pergunta; scaffold demonstra estrutura.
- Acrescentar runtime comum, hierarquia de agentes, ECS ou IA por quadro para
  absorver um contrato.
- Chamar o recorte de AAA ou "quase AAA" sem `finish` observado.
- Publicar, delegar ou contatar pessoas por conta de uma confirmação de avanço.

## Entregar

Apresente acesso ao jogo, o controle necessário no dispositivo usado e uma tarefa
curta para experimentar, sem antecipar a resposta esperada. Não repasse JSON,
queries de diagnóstico ou formulário de QA como instrução ao criador.
Mostre a fatia no estado principal e nos estados-chave (perda, reinício, pausa);
diga o que foi observado em movimento, o que foi corrigido após inspeção, o que foi
herdado/adaptado/criado, e o que ficou de fora. Faça a
[revisão de entrega](../references/delivery.md) no registro existente, atualize o
canônico (Devlog/plano) e cumpra `continuity.before_close` e
`documentation.before_close`. Extraia [aprendizado transferível](../references/learning.md)
para o framework quando houver. Termine com **uma** próxima ação e o prompt de
continuidade pronto ([roteiro](../references/gauntlet.md)). Convide um relato livre
do trecho experimentado, conforme a [condução do criador](../references/creative-workflow.md#conduzir-quem-está-criando).
A reação orienta a próxima melhoria; [`critique`](critique.md) e [`polish`](polish.md)
entram quando pertinentes.
