---
name: game-dev
description: Criar, evoluir, depurar e verificar jogos com IA, partindo do acervo existente.
---

# Game Dev

Use em qualquer engine. O objetivo é uma experiência jogável no **acabamento
pretendido**, com evidência — fácil de começar, difícil de rebaixar. “AAA”
neste framework é só o piso da slice (verbo, feel sincronizado, áudio, pacing,
mundo, receita repetível). Não é tier de publisher, orçamento nem adjetivo
de trailer. O alvo honesto com IA é AA / Triple-I nesse piso.

Focos: `create`, `mechanics`, `lifecycle`, `content`, `visual`, `audio`,
`feel`, `network`, `architecture`.

## Primeira sessão (jogo novo ou recorte novo)

Não gere nove templates. Não peça o usuário para conhecer o harness.

1. Resolva fantasia, verbo, plataforma e a maior incerteza. Assuma o resto
   com registro; pergunte só o que impede de jogar.
2. Execute `python3 scripts/game.py context <projeto> --focus create
   --root <laboratorio>` a partir deste repositório (ou o caminho absoluto
   do script). Leia `read_next`, `foundation.read_first` e
   [ambição](references/ambition.md). Sem projeto identificável, não invente
   um alvo.
3. Adapte um brief curto ou a seção equivalente no canônico existente.
4. Construa um ciclo: perceber → decidir → agir → consequência → reinício.
   Em seguida o feel e o áudio **desse** verbo (`--focus feel`, `--focus audio`).
5. Compare em movimento. Diga uma próxima ação com prova. Título e cores
   novos não demonstram experiência nova.

Escala no brief: jam/conto, produto ou AA / Triple-I (piso de acabamento).
A escala muda quantidade de documentos, não o piso do verbo. Não chame o
build de AAA. Detalhe: [criar](recipes/create.md),
[ambição](references/ambition.md).

## Jogo existente e continuidade

Execute `context <projeto> --focus <foco>`. `context` já corre `scan`.
Comece por `foundation.read_first`/`records`; confira `basis`, `via` e os
limites. `capabilities.mentioned` aponta arquivo local; não prova pause,
reset, seed nem determinismo.

Se `foundation.audit.required` for verdadeiro, avise com `audit.notice` e
comece o levantamento em [auditoria](references/project-audit.md). Não peça
segundo consentimento para documentar o mínimo; restrição explícita na
conversa atual continua valendo.

Em “continue”/“vamos avançar”, use `--event resume` e leia
`continuity.sources`. Fonte encontrada não é tarefa validada. Siga
[continuidade](references/process.md#continuidade-e-retomada).

## Direção, reuso e implementação

Leia [processo](references/process.md) e [qualidade](references/quality.md).
Pré-produção: [ciclo criativo](references/preproduction.md).
`context --stage <etapa>` carrega o template; `template <etapa> --project
<projeto>` imprime um rascunho. Jogo pequeno pode reunir as decisões em um
documento. O design system (template `art-bible`) é conteúdo mínimo; arquivo
separado é opcional se outro canônico cobrir.
[Contrato](references/game-design-system.md).

**Direção aprovada:** `--event direction-approved` e sincronize a base
mínima no mesmo turno, mesmo com nove candidatos encontrados.

**REUSE → ADAPT → CREATE.** Busque no jogo, no acervo e nas fontes
pertinentes. Com `shared/sfx`, `sfx search` antes de baixar som. Sem 8-bit,
chiptune, jsfxr ou Kenney arcade como padrão. CREATE exige lacuna explícita.
Trabalho novo sem registro: [contrato](assets/work.example.json); `check-plan`
valida a estrutura, não o mérito.

Ligue intenção/GDD → requisitos/aceite → decisões técnicas → tarefas →
evidência. Mudança em contratos, estado/tempo, saves, renderização ou
integrações: [arquitetura](recipes/architecture.md)
(`--focus architecture` ou `--stage tdd`). Implemente uma fatia jogável.
Não acrescente runtime comum, hierarquia de agentes ou IA por quadro.

## Verificar e encerrar

Use os valores do próprio jogo e o cenário real. `verify` registra comandos
explícitos e logs. Build verde não comprova diversão, arte, feel, áudio,
reinício, rede, direitos nem aprovação humana. Capacidade desconhecida
permanece desconhecida até ser demonstrada. `experience_status` continua
`not_assessed` até haver observação em movimento.

Compare antes/depois em condições equivalentes. Corrija regressões,
registre decisões e hipóteses descartadas, cumpra `continuity.before_close`
e `documentation.before_close`. Não promova scaffold a slice nem slice a
jogo concluído. Não publique nem delegue sem autorização aplicável.

Não chame o recorte de AAA — nem de “quase AAA” — se a slice não demonstra
as barras da escala (incluindo pacing, sincronia do impacto e repeatability).
Checklist preenchível: `context --stage aaa` ou `template aaa`. Completar
linhas não certifica o jogo; N/A exige motivo.
[Ambição](references/ambition.md), [checklist](references/aaa-checklist.md).

Fontes detalhadas sob demanda: [mapa dos estudos](references/sources.md).
Comandos, limites e adoção: [README](README.md).
