---
name: game-dev
description: Criar, evoluir, depurar, produzir e verificar jogos com IA, partindo do acervo existente, até o acabamento pretendido.
---

# Game Dev

Use este processo em qualquer engine. O objetivo é uma experiência jogável com
evidência, preservando a direção do usuário e a qualidade visual aprovada. Todos os
comandos abaixo são `python3 scripts/game.py ...` a partir deste repositório (ou pelo
caminho absoluto do script), com `--root <laboratorio>` antes ou depois do subcomando.

## Caminho rápido

| Situação | Faça |
| --- | --- |
| Primeira vez ou raiz em dúvida | `doctor --root <lab>`; corrija itens `missing` |
| Jogo novo e pequeno | `template game-design --project <novo> --output <novo>/docs/game-design.md`, depois `context <novo> --focus create --stage game-design` |
| Mudança em jogo existente | `context <projeto> --focus <foco>`; com gênero definido, `--genre <g>` |
| “continue” / “vamos avançar” | `context <projeto> --event resume` e leia `continuity.sources` |
| Usuário aprovou uma referência | `context <projeto> --focus <foco> --event direction-approved` e sincronize a base no mesmo turno |
| Recorte já demonstra a experiência | `context <projeto> --focus production --stage production-plan` |
| Revisar um marco (alpha, beta, gold) | `context <projeto> --focus production --stage milestone` |
| Registrar observação, orçamento medido ou decisão de marco | `record <projeto> --kind observation\|budget\|milestone --author ... --note ... --field k=v --output <pasta-nova>` |

Focos: `create`, `mechanics`, `lifecycle`, `content`, `visual`, `feel`, `network`,
`architecture`, `production`. Etapas: `brief`, `mda`, `gdd`, `poc`, `prd`, `tdd`,
`vertical-slice`, `mvp`, `qa`, `art-bible`, `devlog`, `audit`, `game-design`,
`production-plan`, `milestone`. Gêneros (`--genre`): `narrative`, `platformer`,
`shooter`, `racing`, `turn-based`, `puzzle`, `simulation`, `rpg`, `roguelike`.

## Passos

1. **Contexto.** Resolva projeto e tarefa; execute `context <projeto> --focus <foco>`.
   Leia os AGENTS aplicáveis, `foundation.read_first`/`records`, os catálogos em
   `studies` e somente as referências em `read_next`. O núcleo é agnóstico;
   `read_next` inclui o [pacote de plataforma](packs/README.md) quando a engine foi
   identificada e o de gênero quando você passou `--genre`. Se `packs.genre.suggested`
   trouxer um gênero lido de documento, confirme com a conversa e repita o `context`
   com `--genre`; pacotes são convenções a confirmar no código, não capacidades.
   `capabilities.mentioned` aponta
   arquivo local; não prova pause, reset, seed nem determinismo. Confira `basis`,
   `via` e os limites. `context` já executa `scan`: se `foundation.audit.required`
   for verdadeiro, avise as lacunas com `audit.notice` e comece o levantamento conforme
   [auditoria de projeto](references/project-audit.md), sem pedir um segundo
   consentimento; respeite restrição explícita na conversa atual. Sem projeto
   identificável, não invente um alvo. Em retomada, fonte encontrada não é tarefa
   validada: siga [continuidade e retomada](references/process.md#continuidade-e-retomada).
2. **Intenção e prontidão.** Defina sensação pretendida, verbo central, cenário,
   restrições e prova de conclusão. Leia [processo](references/process.md) e
   [qualidade](references/quality.md). Para criação ou pré-produção, siga
   [o ciclo criativo](references/preproduction.md): Game Brief, MDA/GDD, PoC, PRD/TDD,
   vertical slice, MVP e QA/playtest. `--stage <etapa>` carrega só o template
   pertinente; `template <etapa> --project <projeto>` imprime um rascunho. Reaproveite
   documentos existentes; um jogo pequeno reúne tudo em `game-design`. O design system
   do jogo (`art-bible`) é conteúdo mínimo; o arquivo separado é opcional se outro
   canônico cobrir. Contrato: [design system do jogo](references/game-design-system.md).
   Direção aprovada: `--event direction-approved` e base mínima sincronizada no mesmo
   turno, mesmo com nove candidatos encontrados.
3. **REUSE → ADAPT → CREATE.** Busque no jogo, no acervo e nas fontes pertinentes. Se o
   laboratório tiver `shared/sfx`, use `sfx search` antes de baixar som. Sem 8-bit,
   chiptune, jsfxr ou Kenney arcade como padrão. Leia candidatos e consumidores.
   CREATE exige lacuna explícita. Para trabalho novo sem registro, use
   [o contrato](assets/work.example.json); `check-plan` valida a estrutura, não o mérito.
4. **Arquitetura e fatia jogável.** Ligue intenção/GDD → requisitos/aceite → decisões
   técnicas → tarefas → evidência. Se a mudança afetar responsabilidades, contratos,
   estado/tempo, saves, renderização ou integrações, aplique
   [arquitetura](recipes/architecture.md) (`--focus architecture` ou `--stage tdd`).
   Implemente uma fatia jogável que atravesse regra, apresentação e conteúdo. Não
   acrescente um runtime comum, uma hierarquia de agentes ou IA por quadro.
5. **Verificar.** Use os validadores existentes e o cenário real. `verify` registra
   comandos explícitos e logs (scripts de `package.json` ou alvos Cargo; outras engines
   por `--command`). Build verde não comprova diversão, arte, reinício, rede, direitos
   de assets nem aprovação humana. O que uma pessoa observou em movimento, uma medição
   de orçamento ou uma decisão de marco entra por `record`, com `role=human` ou
   `role=agent`; avaliação do agente não é aprovação do usuário. Capacidade
   desconhecida permanece desconhecida até ser demonstrada.
6. **Comparar, registrar, continuar.** Compare antes/depois em condições equivalentes
   e em movimento quando houver efeito visual. Corrija regressões, registre decisões e
   hipóteses descartadas, cumpra `continuity.before_close` e
   `documentation.before_close`. Não promova scaffold a jogo concluído. Não publique
   nem delegue sem autorização aplicável.
7. **Produzir até o acabamento.** Quando o recorte já demonstrou a experiência, siga
   [produção](recipes/production.md): plano de produção com marcos como gates de
   evidência (first playable → vertical slice → alpha → beta → gold → live), lentes de
   disciplina, orçamentos medidos na plataforma alvo, pipeline de conteúdo e
   estabilidade. Aplique [feel](recipes/feel.md) ao verbo central. Nenhum comando
   promove marco, mede orçamento ou certifica acabamento; a passagem é declarada por
   pessoa com a prova ligada (`record --kind milestone`, recibos de `verify`,
   `observation` e `budget`). Exemplo: [da trilha ao capítulo acabado](examples/era-uma-vez-production.md).

Fontes detalhadas sob demanda: [mapa dos estudos](references/sources.md).
Comandos, limites e adoção: [README](README.md).
