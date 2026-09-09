---
name: game-dev
description: Criar, evoluir, depurar e verificar jogos com IA, partindo do acervo existente.
---

# Game Dev

Use este processo em qualquer engine. O objetivo é uma experiência jogável com
evidência, preservando a direção do usuário e a qualidade visual aprovada.

0. **Sem destino no disco, comece pelo começo.** `python3 scripts/game.py doctor
   --root <laboratorio>` diz se o ambiente responde e se a skill está atualizada;
   `init <destino> --starter <starter>` monta um projeto completo a partir de um
   starter do acervo e gera os documentos como rascunho declarado. Em dúvida sobre
   o próximo passo, `next <projeto> --focus <foco>` deriva uma proposta do estado
   observável. Proposta não é execução: `executed` permanece `false` e a escolha
   continua sua.
1. Resolva o projeto e a tarefa. Execute `python3 scripts/game.py context
   <projeto> --focus <foco> --root <laboratorio>` a partir deste repositório
   (ou o caminho absoluto do script). Focos: `create`, `mechanics`, `lifecycle`,
   `content`, `visual`, `network`, `architecture`, `feel`, `performance`,
   `accessibility`, `audio`, `persistence`, `release`. Leia os AGENTS aplicáveis,
   os registros atuais, os catálogos em `studies` e somente as referências
   indicadas. `capabilities.mentioned` aponta arquivo local; não prova pause,
   reset, seed nem determinismo.
   Comece por `foundation.read_first`/`records`; confira `basis`, `via` e os limites.
   **Checagem automática:** `context` já executa `scan`. Se
   `foundation.audit.required` for verdadeiro, avise as lacunas com `audit.notice`
   e comece o levantamento conforme [auditoria de projeto](references/project-audit.md).
   Não peça um segundo consentimento para documentar o mínimo; respeite restrição
   explícita na conversa atual. Sem projeto identificável, não invente um alvo.
   Em “continue”/“vamos avançar”, use `--event resume` e leia `continuity.sources`.
   Fonte encontrada não é tarefa validada. Siga
   [continuidade e retomada](references/process.md#continuidade-e-retomada).
2. Defina sensação pretendida, verbo central, cenário, restrições e prova de
   conclusão. Leia [processo](references/process.md) e
   [qualidade](references/quality.md). Para criação ou pré-produção, siga
   [o ciclo criativo](references/preproduction.md): Game Brief, MDA/GDD, PoC,
   PRD/TDD, vertical slice, MVP, QA/playtest e release. Use `context <projeto>
   --stage <etapa>` para carregar só o template pertinente; `template <etapa>
   --project <projeto>` imprime um rascunho. Reaproveite documentos existentes;
   um jogo pequeno pode reunir essas decisões em um documento.
   O design system do jogo (template `art-bible`) é conteúdo mínimo; o arquivo
   separado é opcional se outro canônico cobrir. Contrato:
   [design system do jogo](references/game-design-system.md).
   **Direção aprovada:** use `--event direction-approved` e sincronize a base
   mínima no mesmo turno, mesmo com nove candidatos encontrados.
3. **Trabalhe pela dimensão mais baixa.** `context` devolve `production_bar` com
   as dimensões pertinentes ao foco e o degrau pretendido pela etapa. O degrau
   percebido de um jogo é o **mínimo** entre suas dimensões, não a média: resposta
   de protótipo anula arte de carro-chefe, e um save que corrompe apaga qualquer
   acabamento anterior. Antes de melhorar o que já está alto, procure o que está
   baixo. Escada, critérios observáveis e provas:
   [barra de acabamento](references/production-bar.md). Nenhum comando atribui um
   degrau; ao declarar um, declare também dispositivo, versão, cena e quem observou.
4. **REUSE → ADAPT → CREATE.** Busque no jogo, no acervo e nas fontes
   pertinentes. `doctor` lista os starters disponíveis; começar por um deles é
   REUSE, escrever um loop do zero é CREATE. Se o laboratório tiver `shared/sfx`,
   use `sfx search` antes de baixar som. Sem 8-bit, chiptune, jsfxr ou Kenney
   arcade como padrão. Leia candidatos e consumidores. CREATE exige lacuna
   explícita. Para trabalho novo sem registro, use
   [o contrato](assets/work.example.json); `check-plan` valida a estrutura, não o
   mérito da escolha.
5. Ligue intenção/GDD → requisitos/aceite → decisões técnicas → tarefas →
   evidência. Se a mudança afetar responsabilidades, contratos, estado/tempo,
   saves, renderização ou integrações, aplique
   [arquitetura](recipes/architecture.md). `--focus architecture` ou `--stage tdd`
   carrega a receita. Implemente uma fatia jogável. Não acrescente um runtime
   comum, uma hierarquia de agentes ou IA por quadro.
6. Verifique com os validadores existentes e com o cenário real. `verify`
   registra comandos explícitos e logs. Build verde não comprova diversão,
   arte, reinício, rede, direitos de assets nem aprovação humana. Capacidade
   desconhecida permanece desconhecida até ser demonstrada — e `context` só sabe
   dizer `mentioned`, porque lê arquivos sem executá-los. Quando os testes do
   projeto de fato exercitarem pause, reset, seed ou determinismo, declare no
   recibo com `verify --proves <capacidade>`. A declaração é sua, não do
   repositório; declare só o que os comandos cobrirem.
7. Compare antes/depois em condições equivalentes e em movimento quando houver
   efeito visual. Corrija regressões, registre decisões e hipóteses descartadas,
   cumpra `continuity.before_close` e `documentation.before_close`. Não promova
   scaffold a jogo concluído. Não publique nem delegue sem autorização aplicável.

Fontes detalhadas sob demanda: [mapa dos estudos](references/sources.md).
Comandos, limites e adoção: [README](README.md).
