# Criar uma experiência

Entrada: fantasia, público/entrada, verbo central, direção artística e cenário curto.
Se algo foi omitido, assuma a opção coerente com o acervo e registre; só interrompa
por decisão indispensável. O destino de um jogo novo deve ser novo; continuação usa
o projeto atual.

O caminho curto está em [ambição](../references/ambition.md): um ciclo jogável
na primeira sessão, depois feel e áudio do verbo, depois receita de conteúdo.
Não gere todos os templates antes de experimentar. Nove arquivos vazios não
aumentam a qualidade; uma fatia sem feel continua sendo protótipo.

Siga [o ciclo de pré-produção](../references/preproduction.md) para escolher o
próximo artefato e revisar sua prontidão. Brief e GDD definem a experiência; MDA
explicita a hipótese; PoC a investiga; PRD/TDD delimitam requisitos e implementação;
vertical slice e MVP têm objetivos distintos; QA e playtest alimentam o design.
Carregue o template da etapa com `context <projeto> --stage <etapa>` e adapte o
documento canônico. Uma direção aprovada exige sincronizar a base oficial no mesmo
turno, conforme
[o roteiro](../references/project-audit.md#aprovação-de-direção-materializar-e-continuar).
Cubra as nove áreas com conteúdo ou lacunas explícitas, em documentos proporcionais
ao projeto, e prossiga com o recorte solicitado. O usuário não precisa pedir essa base.

Declare a **escala** no brief: jam/conto, produto ou AAA-shaped. A escala governa
quantidade de artefatos e de conteúdo. O piso do verbo — decisão, feel, áudio da
consequência — não é opcional em nenhuma delas.

## Primeira sessão

1. Consulte o [playground](https://games.alanicolas.com/) e o acervo local.
   Identifique uma família compatível. Procure código, contratos e conteúdo
   reutilizável. Som: se o laboratório tiver `shared/sfx`, use `sfx search`
   antes de qualquer download. Explique REUSE, ADAPT ou CREATE antes de
   produzir novos sistemas.
2. Construa um ciclo jogável com uma decisão característica. Defina entrada,
   objetivo percebido, consequência, término e repetição. Título e cores novos
   não demonstram uma experiência nova.
3. Faça essa fatia atravessar controles, estado, apresentação e conteúdo.
   Valide a integração antes de multiplicar fases, itens ou personagens.
4. Aplique o feel e o áudio **desse** verbo. Use `--focus feel` e
   `--focus audio`. Arte provisória é aceitável se a direção estiver
   declarada; verbo mudo ou sem peso não é.
5. Compare com a intenção e com a referência, em movimento. Preserve o que
   foi pedido. Registre herdado versus produzido e **uma** próxima ação.

## Da fatia à produção

A escada: fantasia → ciclo → feel → áudio → receita de conteúdo → vertical
slice no piso → produção sem diluir. PoC reduz incerteza; scaffold mostra
estrutura; slice mostra experiência no acabamento pretendido.

Em escala AAA-shaped, feel, mix, luz, animação e a receita do próximo item
são requisitos do recorte, não “polimento depois”. Reduza quantidade de
conteúdo; não reduza o piso aprovado. Se a slice não demonstra que outro
trecho nasce no mesmo padrão, ainda não está pronta para ampliar.

Pontos de partida a **examinar**, não bases aprovadas automaticamente:

- FPS em papel: Distrito Rabisco / Jogo Rabisco. Já tem briefing, bootstrap e marcos.
  O bootstrap recusa divergência do manifesto de origem.
- Contos Canvas: Era Uma Vez, no [playground](https://games.alanicolas.com/).
- Corrida: Brasa-Pista, no playground.
- Unity: protótipo local com verificações próprias; presença em `prototypes/` não
  declara publicação.

Não copie paleta, feel ou mix de uma família sem ADAPT e proveniência. O
destino continua com instância própria no design system.

BMad inspira leitura por etapa e retomada (`RE-GDS-002`, `RE-GDS-022`); seus passos
textuais não são uma garantia de execução. [Fonte](../references/sources.md).

Concluir o pedido exige conteúdo distintivo, cenário real e QA. Scaffold ou
cópia que inicia continua sendo ponto de partida. Esta receita não copia nem
publica projetos por si. Não chame o recorte de AAA se as barras da escala
não foram demonstradas na slice.
