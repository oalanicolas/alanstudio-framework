# Criar uma experiência

Entrada: fantasia, público/entrada, verbo central, direção artística e cenário curto.
Se algo foi omitido, assuma a opção coerente com o acervo e registre; só interrompa
por decisão indispensável. O destino de um jogo novo deve ser novo; continuação usa
o projeto atual.

Siga [o ciclo de pré-produção](../references/preproduction.md) para escolher o
próximo artefato e revisar sua prontidão. Brief e GDD definem a experiência; MDA
explicita a hipótese; PoC a investiga; PRD/TDD delimitam requisitos e implementação;
vertical slice e MVP têm objetivos distintos; QA e playtest alimentam o design.
Carregue o template da etapa com `context <projeto> --stage <etapa>` e adapte o
documento canônico. Não gere todos os arquivos antes de começar a experimentar.
Uma direção aprovada exige sincronizar a base oficial no mesmo turno, conforme
[o roteiro](../references/project-audit.md#aprovação-de-direção-materializar-e-continuar).
Cubra as nove áreas com conteúdo ou lacunas explícitas, em documentos proporcionais
ao projeto, e prossiga com o recorte solicitado. O usuário não precisa pedir essa base.

1. Consulte o [playground](https://games.alanicolas.com/) e identifique uma família
   compatível. Procure código, contratos e conteúdo reutilizável no jogo escolhido.
   Som: se o laboratório tiver `shared/sfx`, use `sfx search` antes de qualquer
   download. Explique REUSE, ADAPT ou CREATE antes de produzir novos sistemas.
2. Construa um ciclo jogável com uma decisão característica da proposta. Defina
   entrada, objetivo percebido, consequência, término e repetição. Título e cores
   novos não demonstram uma experiência nova.
3. Faça a primeira fatia atravessar controles, estado, apresentação e conteúdo.
   Valide essa integração antes de multiplicar fases, itens ou personagens.
4. Compare com a intenção e com a referência visual. Preserve funcionalidades
   explicitamente pedidas e registre o que foi herdado versus produzido.

Pontos de partida a **examinar**, não bases aprovadas automaticamente:

- FPS em papel: Distrito Rabisco / Jogo Rabisco. Já tem briefing, bootstrap e marcos.
  O bootstrap recusa divergência do manifesto de origem.
- Contos Canvas: Era Uma Vez, no [playground](https://games.alanicolas.com/).
- Corrida: Brasa-Pista, no playground.
- Unity: protótipo local com verificações próprias; presença em `prototypes/` não
  declara publicação.

BMad inspira leitura por etapa e retomada (`RE-GDS-002`, `RE-GDS-022`); seus passos
textuais não são uma garantia de execução. [Fonte](../references/sources.md).

Concluir exige conteúdo distintivo, cenário real e QA. Scaffold ou cópia que inicia
continua sendo ponto de partida. Esta receita não copia nem publica projetos por si.
