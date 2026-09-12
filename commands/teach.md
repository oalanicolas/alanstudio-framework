# Teach

Dar ao projeto a base que todos os outros comandos leem: análise profunda do que
existe, nove áreas mínimas com fato ou lacuna, instruções persistentes do agente
(`AGENTS.md`) e escala declarada no brief. É o análogo de "criar PRODUCT.md":
sem essa base, tudo que a IA produz é genérico e ignora o projeto.

Roda sozinho quando `context` devolve `foundation.audit.required` — avise com
`audit.notice` e comece, sem pedir segundo consentimento
([direção do usuário](../references/project-audit.md)). Também atende a "inicialize o
projeto" sem alvo operacional. Restrição explícita na conversa continua valendo.

## Escala

`jam`: um `game-design.md` cobre as nove áreas; AGENTS curto. `product`/`aa`:
documentos separados por ritmo de atualização (brief, GDD/MDA, PRD/TDD, art-bible,
devlog, QA, runbook, origem) e um plano de produção como fonte única de marcos.
A escala é a primeira coisa que este comando escreve no brief quando falta: o
`context` devolve `scale.name: null` e pede exatamente isso.

## Avaliar

1. `context <projeto> --focus architecture --event initialize`. Leia `scan`:
   áreas `not_located`, `draft_only`, `historical_only`; `agent_context`;
   `continuity.sources`; `git.recent` (histórico, não prova).
2. Explore antes de perguntar: entrypoints, manifestos, scripts, testes, assets,
   índices, documentos atuais versus históricos, consumidores do que parece
   reutilizável. Forme uma hipótese de escala e de gênero pelo que existe.
3. Entrevista, não confirmação: com base vazia ou pedido de uma frase, faça uma
   rodada de duas ou três perguntas (escala, jogador/verbo, referência e
   anti-referência, acesso) antes de propor a base. Pergunte só o que o código e
   os documentos não respondem. Não pergunte paleta nem fonte aqui.
4. Base já existente: nunca sobrescreva em silêncio. Pergunte qual documento
   refrescar e preserve o histórico.

## Executar

Siga [levantar e organizar o estado real](../references/project-audit.md) (oito
passos): delimitar, inventariar, rastrear a arquitetura pelo fluxo real (iniciar →
carregar → input → estado → apresentar → pausar → concluir → descartar), recuperar
design e direção do comportamento observado, recuperar histórico e prova, organizar
(REUSE no índice, ADAPT no canônico, CREATE só onde falta), entregar.

- Jogo pequeno: [`game-design`](../assets/templates/game-design.md), preenchido.
- Instruções do agente: [`agents`](../assets/templates/agents.md) → `AGENTS.md`
  na raiz, curto e verdadeiro: como rodar, validadores, cenário real, convenções que
  o código não explica, zonas de risco, política de assets gerados por IA.
- Escala no brief, em campo lido pelo harness: `Escala: jam | produto | AA / Triple-I`.
- Design system do jogo ausente: ofereça [`document`](document.md); não invente
  tokens por inspeção de nomes de arquivo.

## Verificar

Cada área tem fonte atual consultada, estado/limite e destino canônico, ou lacuna
com motivo e próxima ação. `scan` no mesmo turno reconhece a cobertura, mas
cobertura lexical não é a prova. Se o teach recusa que cobertura lexical seja a prova, o `coverage` nomeia o lexical que o teach já recusa. Varredura no disco não é o rastro. Sem chave `lexical`. A prova é o rastro de código com entrypoint,
estado e consumidores. Servidor aberto, testes verdes e documentos encontrados **não
encerram** este comando (`documentation.initialization.not_sufficient`).

Depois de escrever, rode `context` de novo para que a sessão use a base fresca.

## Nunca

- Preencher lacuna com certeza fabricada para deixar a varredura verde.
- Inventar arquitetura atual de um jogo ainda inexistente; proposta é proposta.
- Gerar nove templates vazios e chamar de base documental.
- Produzir aprovação visual ou sonora por inspeção de arquivos.
- Reiniciar a auditoria por rito quando uma análise atual já cobre o que se pede.

## Entregar

Mapa do estado atual com localizadores, lacunas priorizadas, documentos organizados,
os três a cinco princípios que vão guiar o trabalho (extraídos do que o projeto já
decide), e **uma** próxima tarefa com motivo, entrada canônica e prova, com o
prompt pronto ([roteiro](../references/gauntlet.md)). Se `teach` foi acionado como
bloqueio de outro comando, retome esse comando agora com a base nova.
