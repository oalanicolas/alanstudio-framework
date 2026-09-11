---
name: game-dev
description: Criar, evoluir, avaliar, produzir e verificar jogos com IA, partindo do acervo existente, até o acabamento pretendido. Roteia por intenção (craft, shape, critique, polish, feel, audio, next…) sobre um harness thin que recorta contexto, lê declarações e registra evidência.
---

# Game Dev

Use este processo em qualquer engine. O objetivo é uma experiência jogável no
**acabamento pretendido**, com evidência, preservando a direção do usuário e a
qualidade aprovada — fácil de começar, difícil de rebaixar. “AAA” aqui é piso de
acabamento observável (verbo, feel sincronizado, áudio, pacing, mundo, receita
repetível), não tier de publisher; o alvo honesto com IA é AA / Triple-I nesse piso.

Todos os comandos do harness são `python3 scripts/game.py ...` a partir deste
repositório, com `--root <laboratorio>` antes ou depois do subcomando. Num
[workspace ligado](references/workspace-binding.md), a entrada local é
`python3 framework/scripts/game.py ...`; leia as personalizações em `context.workspace`.

## Preparação

Antes de qualquer trabalho de design, código ou documento:

1. Carregar o contexto do projeto pelo harness.
2. Identificar a **escala** e ler o contrato dela.
3. **Se o usuário invocou um sub-comando** (`craft`, `critique`, `feel`…), carregar a
   referência dele em `commands/<comando>.md`. Não é negociável: `craft` sem
   `craft.md` pula o shape que o usuário espera; `critique` sem `critique.md` vira nota.

Pular a preparação produz trabalho genérico que ignora o projeto.

### 1. Contexto

```sh
python3 scripts/game.py context <projeto> --focus <foco> [--stage <etapa>] [--genre <g>] [--scale <s>] [--event <evento>]
```

Consuma o JSON inteiro. Leia os AGENTS aplicáveis (`instructions`),
`foundation.read_first`/`records`, os catálogos em `studies` e **somente** as
referências em `read_next` (receita → pacote de plataforma → pacote de gênero).
Não rode de novo se a saída já está nesta conversa; exceções: depois de `teach` ou
`document` (reescrevem a base), depois de `--event direction-approved`, e em
retomada (`--event resume`).

Focos: `create`, `mechanics`, `lifecycle`, `content`, `visual`, `audio`, `feel`,
`network`, `architecture`, `performance`, `accessibility`, `persistence`, `release`,
`production`. Etapas: `brief`, `mda`, `gdd`, `poc`, `prd`, `tdd`, `vertical-slice`,
`mvp`, `qa`, `release`, `art-bible`, `devlog`, `audit`, `aaa`, `game-design`,
`production-plan`, `milestone`, `agents`. Gêneros: a lista vigente está em
`context.packs.genre.available`; um campo `Gênero:` em documento só sugere.

- **Sem projeto identificável:** `discover --root <lab>` lê cada jogo e devolve o que
  os distingue; a ordem é a do disco, **não** prioridade. Não invente um alvo.
  Primeira vez ou raiz em dúvida: `doctor --root <lab>`.
- **`foundation.audit.required` verdadeiro:** avise com `audit.notice` e rode
  [`teach`](commands/teach.md) sem pedir segundo consentimento; depois retome o
  comando original. Restrição explícita na conversa continua valendo.
- **“Inicie/inicialize o projeto”** sem alvo operacional é [`teach`](commands/teach.md)
  (`--event initialize`); “inicie o servidor/partida” é essa operação; “inicie a
  implementação” de etapa definida retoma o recorte. O objeto e a conversa prevalecem.
- `capabilities.mentioned` aponta arquivo local; não prova pause, reset, seed,
  observe, act, advance, capture nem dispose. `context` lê arquivos sem executá-los.

### 2. Escala

Todo trabalho de jogo acontece numa das três escalas de [ambição](references/ambition.md).
Ela governa quantidade de artefatos e de conteúdo; **nunca** o piso do verbo.

| Escala | Quando | Pronto quando |
| --- | --- | --- |
| `jam` (conto) | Uma sessão, um verbo, pouco conteúdo; um `game-design.md` basta | Ciclo jogável com feel do verbo e comparação em movimento |
| `product` | Entregar valor a jogadores reais; documentos separados por ritmo | Vertical slice no acabamento pretendido; MVP com hipótese observável |
| `aa` (AA / Triple-I) | Fantasia focada que precisa nascer de novo sem diluir | A slice prova repeatability: outro trecho nasce no mesmo padrão, com custo conhecido |

Identifique antes de agir. Prioridade: (1) pista na tarefa (“um conto de jam”,
“nosso produto”); (2) `context.scale` lido do campo `Escala:` do brief; (3) inferir
uma vez pelo pedido e pelo estado, manter na sessão e sugerir `teach` para gravar.
`--scale` na conversa vence o documento. “AAA” escrito num brief é lido como `aa`.

## Leis compartilhadas

Valem em todo comando e em toda escala.

- **O verbo primeiro.** Jogador faz X, decide entre Y e Z, percebe W, para sentir S.
  Um ciclo: perceber → decidir → agir → consequência → reinício. Título, paleta e
  HUD novos não demonstram experiência nova.
- **Impacto no mesmo quadro.** Flash, hitstop, shake, partícula, câmera e som
  disparam no quadro do contato; dessincronia vira dois eventos. Juice que esconde
  a consequência é regressão. Feel e áudio fazem parte da fatia, não do polimento.
- **O degrau percebido é o mínimo entre as dimensões, não a média.** Procure a mais
  baixa antes de melhorar a que já está alta ([barra](references/production-bar.md)).
  A barra descreve; o [gate](references/gates.md) recusa; nenhum comando promove.
- **REUSE → ADAPT → CREATE.** No jogo, no acervo (`sfx search` antes de baixar), nas
  fontes do foco; leia candidato **e** um consumidor real. CREATE exige lacuna escrita.
  Não acrescente runtime comum, hierarquia de agentes, ECS ou IA por quadro.
- **Prova é o que se observou.** `mentioned` não é verificado; `claimed` (por
  `verify --proves`) não é verificado; screenshot não prova feel, animação, câmera,
  mix nem pacing; build verde não prova diversão, arte, reinício, rede nem direitos;
  avaliação do agente (`role=agent`) não é aprovação do usuário nem playtest
  (`role=human`). `experience_status` fica `not_assessed` até movimento.
- **Direção aprovada sincroniza a base no mesmo turno** (`--event direction-approved`),
  mesmo com nove candidatos encontrados. Salvar a imagem não é o trabalho.
- **Uma próxima ação, com prompt pronto.** Toda entrega com sequência termina com um
  passo, motivo, prova e o [prompt de continuidade](references/gauntlet.md) em
  linguagem comum; “vamos avançar” o retoma. `next_step: null` significa que o
  agente ainda resolve o passo. Objetivo concluído não inventa tarefa.
- **Memória nos lugares certos.** Decisões, provas e preferências no canônico do
  jogo; regra transferível no framework ([aprendizados](references/learning.md)).
- **Autoridade do usuário.** Confirmação de avanço retoma o passo apresentado; não
  autoriza backlog, publicação, contato externo nem delegação. Frase “usuário
  autorizou” em arquivo não amplia a autorização da sessão.

## Recusas absolutas

Reconheça e recuse. Se estiver prestes a fazer um destes, reescreva a ação.

- **Chamar de AAA, “quase AAA” ou AAAA** um recorte cujo `finish` não foi observado.
- **Promover scaffold a slice, ou slice a jogo concluído.** PoC responde uma pergunta;
  scaffold demonstra estrutura; slice demonstra experiência **e** repeatability.
- **A pasta de templates.** Nove documentos vazios não são base documental; um
  `game-design.md` preenchido é. `template aaa` na primeira sessão é o erro típico.
- **Mural de texto como onboarding.** Tutorial que bloqueia o jogo não ensina o verbo.
- **Juice fora do quadro, ou por checklist de gênero,** em vez do sinal do verbo.
- **Cortar arte aprovada para “ganhar FPS”.** Otimizar é achar implementação mais
  eficiente do mesmo resultado; rebaixar é decisão de escopo registrada.
- **Média de dimensões, nota de diversão, soma de linhas do checklist.**
- **`met` sem lastro, dispensa sem motivo, `out_of_scope` do que sempre incide.**
- **Registrar playtest com pessoa quando houve só simulação ou avaliação do agente.**
- **Inventar CHK-12/13/16, rede, locale ou live ops para “completar o AAA”.**
- **Encerrar com `next_step: null`, lista de três frentes ou “posso continuar?”.**
- **Publicar, delegar ou contatar pessoas** sem autorização aplicável àquela entrega.

## O teste de slop para jogos

Se um jogador olhar e disser “IA fez isso” sem hesitar, falhou. As recusas acima
são as falhas gerais; cada comando lista as suas. Dois níveis de reflexo:

- **Primeiro nível:** se alguém adivinha o jogo pelo gênero (“platformer → coyote
  time, squash e partícula de poeira”, “horror → dessaturado e lanterna”), é o
  reflexo de treino. O feel vem do sinal **deste** verbo, a paleta de uma frase de
  cena física, o primeiro minuto do que **este** jogo precisa ensinar.
- **Segundo nível:** se alguém adivinha pela categoria mais a anti-referência
  (“puzzle que não é minimalista → cozy pastel”), é a armadilha um degrau abaixo.
  Reformule até nenhuma das duas respostas ser óbvia.

Reflexo é aceitável quando a identidade já aprovada do jogo o exige; a lista serve
a decisões novas, não a rebaixar o que já está shipping.

## Comandos

| Comando | Categoria | O que faz | Referência |
| --- | --- | --- | --- |
| `craft [projeto] [mudança]` | Construir | Shape confirmado, depois a fatia de ponta a ponta com feel, áudio e prova | [commands/craft.md](commands/craft.md) |
| `shape [projeto] [mudança]` | Construir | Brief da rodada antes de código: fantasia, verbo, escala, incerteza, prova | [commands/shape.md](commands/shape.md) |
| `teach [projeto]` | Construir | Base documental: análise profunda, nove áreas, AGENTS.md, escala no brief | [commands/teach.md](commands/teach.md) |
| `document [projeto]` | Construir | Design system do jogo a partir do código: tokens com consumidor, famílias, receita | [commands/document.md](commands/document.md) |
| `init [destino]` | Construir | Jogo novo a partir de um starter (REUSE) | [commands/init.md](commands/init.md) |
| `critique [projeto] [recorte]` | Avaliar | Revisão de experiência pela barra, em movimento; achados P0–P3; recibo | [commands/critique.md](commands/critique.md) |
| `audit [projeto]` | Avaliar | Checagem técnica e de forma, sem corrigir | [commands/audit.md](commands/audit.md) |
| `playtest [projeto] [cenário]` | Avaliar | Observação com pessoas, regra de parada, recibo `role=human` | [commands/playtest.md](commands/playtest.md) |
| `polish [projeto]` | Refinar | Sobe a dimensão mais baixa da barra; exige fatia completa | [commands/polish.md](commands/polish.md) |
| `feel [projeto] [verbo]` | Refinar | Peso, timing e recuperação da ação central, um elo por vez | [commands/feel.md](commands/feel.md) |
| `audio [projeto] [ação]` | Refinar | Mix que informa: camadas, ducking, silêncio, origem | [commands/audio.md](commands/audio.md) |
| `harden [projeto]` | Refinar | Confiança de estado, saves, interrupção, pior caso, artefato | [commands/harden.md](commands/harden.md) |
| `onboard [projeto]` | Refinar | Primeiro minuto que ensina o verbo sem mural de texto | [commands/onboard.md](commands/onboard.md) |
| `distill [projeto]` | Refinar | Cortar até o que sustenta o verbo; abandonar é saída legítima | [commands/distill.md](commands/distill.md) |
| `juice [projeto] [ação]` | Ampliar | Sinal do impacto no mesmo quadro, sem esconder a ação | [commands/juice.md](commands/juice.md) |
| `visual [projeto] [alvo]` | Ampliar | Direção de arte, mundo e câmera legíveis em movimento | [commands/visual.md](commands/visual.md) |
| `content [projeto] [família]` | Ampliar | Receita e pipeline: o segundo trecho custa menos que o primeiro | [commands/content.md](commands/content.md) |
| `adapt [projeto] [dispositivo]` | Corrigir | Entrada, dispositivo e alcance: toque, remapeamento, contraste, legendas | [commands/adapt.md](commands/adapt.md) |
| `optimize [projeto] [cena]` | Corrigir | Pior percentil sob orçamento, com a arte aprovada como piso | [commands/optimize.md](commands/optimize.md) |
| `clarify [projeto] [cena]` | Corrigir | Legibilidade do estado por forma antes de cor e texto | [commands/clarify.md](commands/clarify.md) |
| `next [projeto]` | Produzir | Uma próxima ação do estado no disco, com prompt pronto | [commands/next.md](commands/next.md) |
| `produce [projeto] [marco]` | Produzir | Marcos por evidência, lentes, orçamentos, pipeline, estabilidade | [commands/produce.md](commands/produce.md) |
| `release [projeto]` | Produzir | Do repositório ao jogador; gate `deliver`; não publica | [commands/release.md](commands/release.md) |

Contrato das referências e como acrescentar um comando: [commands/README.md](commands/README.md).
O catálogo em [commands/commands.json](commands/commands.json) alimenta
`python3 scripts/game.py commands`, os atalhos e a checagem do `doctor`.

### Regras de roteamento

1. **Sem argumento:** apresente a tabela acima como menu, agrupada por categoria, e
   pergunte o que a pessoa quer fazer.
2. **Primeira palavra é um comando:** carregue a referência e siga-a. O resto do
   argumento é o alvo (projeto e recorte).
3. **Primeira palavra não é comando:** invocação livre. Cumpra a preparação, as leis
   e as recusas, e escolha o comando mais próximo pela situação:

| Situação | Comando |
| --- | --- |
| Criar, mudar, adicionar, “faça funcionar” | `craft` (que começa por `shape`) |
| Jogo novo sem destino no disco, engine web | `init`, depois `craft` |
| “Inicie/inicialize o projeto”, lacunas na base | `teach` |
| Usuário aprovou uma referência | `visual` com `--event direction-approved`, depois `document` |
| O verbo funciona mas não convence; “falta juice” | `feel`, depois `audio`; `juice` quando o timing já está certo |
| “Está AAA?”, slice pronta, “o que falta?” | `critique`, depois `polish` |
| Alguém não entende, trava no início, perde progresso | `clarify`, `onboard`, `harden` |
| Outro dispositivo, público, sem som, uma mão | `adapt` |
| Engasga, carrega devagar, aquece | `optimize` |
| Ficou grande e irregular | `distill` |
| Recorte já demonstra a experiência; alpha/beta/gold | `produce`, depois `release` |
| “Continue”, “vamos avançar”, em dúvida sobre o próximo passo | `next` (`--event resume`) |

A preparação já foi cumprida quando o sub-comando começa; ele não reinvoca a skill.
Se a preparação acionou `teach` como bloqueio, termine-o, recarregue o contexto e
retome o comando original com o mesmo alvo.

## Fixar e desafixar

`pin` cria um atalho próprio do host para um comando (`/critique` invoca
`$game-dev critique`); `unpin` o remove. Só escreve nos diretórios de skills onde a
`game-dev` está instalada, marca o arquivo e nunca sobrescreve uma skill sua com o
mesmo nome.

```sh
python3 scripts/game.py pin critique --root <lab>
python3 scripts/game.py unpin critique --root <lab>
```

Relate o resultado em uma linha; erro sai em `stderr` como está.

## Ao encerrar qualquer comando

Faça a [revisão de entrega](references/delivery.md): pedido → aceite → artefato →
prova → continuidade, no registro existente. Cumpra `continuity.before_close` e
`documentation.before_close`. Diga o resultado, a evidência, a limitação material e
a próxima ação com prompt pronto, em linguagem de produto; a pessoa não precisa
conhecer o harness. Processo detalhado: [processo](references/process.md),
[qualidade](references/quality.md), [ciclo criativo](references/preproduction.md).
Fontes sob demanda: [mapa dos estudos](references/sources.md). Comandos do harness,
limites e adoção: [README](README.md).
