---
name: game-dev
description: Criar, evoluir, depurar e verificar jogos com IA, partindo do acervo existente.
---

# Game Dev

Use este processo em qualquer engine. O objetivo é uma experiência jogável com
evidência, preservando a direção do usuário e a qualidade visual aprovada.

1. Resolva o projeto e a tarefa. Execute `python3 scripts/game.py context
   <projeto> --focus <foco> --root <laboratorio>` a partir deste repositório
   (ou o caminho absoluto do script). Focos: `create`, `mechanics`, `lifecycle`,
   `content`, `visual`, `network`. Leia os AGENTS aplicáveis, os registros
   atuais, os catálogos em `studies` e somente as referências indicadas.
   `capabilities.mentioned` aponta arquivo local; não prova pause, reset, seed
   nem determinismo.
2. Defina sensação pretendida, verbo central, cenário, restrições e prova de
   conclusão. Leia [processo](references/process.md) e
   [qualidade](references/quality.md). Para criação ou pré-produção, siga
   [o ciclo criativo](references/preproduction.md): Game Brief, MDA/GDD, PoC,
   PRD/TDD, vertical slice, MVP e QA/playtest. Use `context <projeto> --stage
   <etapa>` para carregar só o template pertinente; `template <etapa> --project
   <projeto>` imprime um rascunho. Reaproveite documentos existentes; um jogo
   pequeno pode reunir essas decisões em um documento.
3. **REUSE → ADAPT → CREATE.** Busque no jogo, no acervo e nas fontes
   pertinentes; leia candidatos e consumidores. CREATE exige lacuna explícita.
   Para trabalho novo sem registro, use [o contrato](assets/work.example.json);
   `check-plan` valida sua estrutura, não o mérito da escolha.
4. Ligue intenção/GDD → requisitos/aceite → decisões técnicas → tarefas →
   evidência. Implemente uma fatia jogável. Use os comandos e ferramentas do
   projeto; não acrescente um runtime comum, uma hierarquia de agentes ou IA
   por quadro. Carregue outra receita apenas quando surgir uma necessidade
   concreta.
5. Verifique com os validadores existentes e com o cenário real. `verify`
   registra comandos explícitos e logs. Build verde não comprova diversão,
   arte, reinício, rede, direitos de assets nem aprovação humana. Capacidade
   desconhecida permanece desconhecida até ser demonstrada.
6. Compare antes/depois em condições equivalentes e em movimento quando houver
   efeito visual. Corrija regressões, registre decisões e hipóteses descartadas,
   reporte lacunas e deixe o próximo passo reproduzível. Não promova scaffold a
   jogo concluído. Não publique nem delegue sem autorização aplicável.

Fontes detalhadas sob demanda: [mapa dos estudos](references/sources.md).
Comandos, limites e adoção: [README](README.md).
