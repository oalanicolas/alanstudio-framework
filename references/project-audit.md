# Checagem inicial e documentação automática

Direção atualizada de Alan em 2026-09-08: checar o mínimo em qualquer pedido sobre
um jogo e, quando não localizado, **avisar e começar a documentar, sem pedir
consentimento**. Isso substitui a oferta de auditoria da versão 0.4. A checagem
inicial é automática no `context` e também está disponível em `scan <projeto>`.
A entrada do agente no workspace manda executá-la mesmo sem invocação de `$game-dev`.
Isso não é um daemon nem um hook que intercepta ferramentas externas ao agente.

## Inicializar o projeto

Quando o pedido ou a convenção do workspace define inicialização documental,
**inicializar o projeto inicia análise profunda e organização documental**. Esse é o significado
padrão no processo Games quando não há um alvo operacional mais específico.
O agente resolve a intenção pelo objeto e pelo contexto da conversa, sem exigir que
a pessoa conheça o termo auditoria ou os comandos do harness.

- “Inicialize o Combate Lendário” ou “vamos começar a organizar este projeto”:
  levantar implementação, confrontar documentos, organizar a base e definir continuidade.
- “Inicie o servidor”, “abra o jogo para eu jogar” ou “inicie a partida”: realizar
  essa operação explícita, respeitando o escopo; não substituir por uma auditoria ampla.
- “Inicie a implementação da etapa que definimos” ou “vamos avançar” depois de
  apresentar um recorte: retomar esse recorte; reaproveitar auditoria ainda válida.
- “Inicie um projeto novo com esta ideia”, sem implementação: organizar visão,
  hipóteses, decisões e primeiras provas. Arquitetura atual inexistente permanece
  explícita; arquitetura proposta não vira descrição de código.

Não trate a ocorrência da palavra “iniciar” em um arquivo como gatilho de execução.
Instrução mais específica na conversa prevalece. Inicializar o processo autoriza
esse levantamento e documentação; implementar além dele segue o pedido já autorizado.

Execute internamente, com o projeto resolvido:

```sh
python3 framework/scripts/game.py context games/combate-lendario --focus architecture --event initialize
```

O evento seleciona `documentation.action: audit_and_document`, carrega auditoria e
arquitetura e entrega `documentation.initialization` com o aviso e as evidências
exigidas. O foco original é preservado se outro foi escolhido. A ação vale **mesmo
com candidatos nas nove áreas**; localização lexical não substitui confronto com código.
O comando retorna `pending_agent_audit`; o resultado real fica no registro canônico
após o trabalho do agente e não é inferido pelo scanner. O comando não interpreta
a conversa, executa a auditoria nem certifica seu resultado.

Avise e siga o roteiro “Levantar e organizar o estado real” abaixo no mesmo turno.
Reaproveite fontes e trabalho simultâneo: uma auditoria já em andamento deve ser
consultada, sem criar outra versão concorrente da base. Uma análise anterior atual
pode ser incorporada após conferir cobertura e divergências; não refaça tudo por rito.

### Profundidade e entrega

A inicialização precisa explicar o jogo que existe e a base necessária para evoluí-lo:

1. **Diagnóstico:** versão e fluxo principal, estado implementado versus pretendido,
   fontes consultadas e limites. Diferencie jogos/protótipos homônimos antes de rastrear.
2. **Rastros de código:** percorrer o fluxo principal de ponta a ponta e os sistemas
   que o sustentam, com entrypoint, estado, condições/consequências e consumidores.
   Examinar teste existente quando ele sustenta a alegação. Uma árvore de pastas ou
   lista de nomes de módulos não demonstra arquitetura nem regra de negócio.
3. **Base canônica:** organizar as nove áreas abaixo com conteúdo, localizadores e
   divergências. Preservar decisões autorais e separar fatos, propostas e hipóteses.
4. **Lacunas priorizadas:** impacto, evidência faltante e dependência/ação para resolver.
   Não esconder desconhecidos com templates preenchidos ou classificação “não aplicável”.
5. **Continuidade:** escolher o primeiro recorte justificável e gerar seu prompt pronto
   em linguagem comum, com fonte, limites e prova. Se há decisão indispensável, explicitar
   a ação para destravá-la; uma investigação delimitada também é um próximo recorte.

Use extração formal de regras (`code-anatomist`) quando a complexidade exigir catálogo
retomável; um rastreamento menor pode viver no TDD/auditoria existente. Não marque
catálogo como executado apenas por iniciar o controlador ou copiar seus títulos.

Servidor, HTTP, build, testes e observação do jogo podem produzir **evidência de apoio**.
Nenhum deles, sozinho ou em conjunto sem o diagnóstico/documentação, conclui a
inicialização. Abrir o navegador deve responder a uma pergunta concreta do levantamento,
não se tornar a entrega principal. Não alterar gameplay só para fazer a auditoria passar.

Na resposta, apresente o diagnóstico principal, links dos canônicos e a prioridade
com seu prompt pronto. Diga “base analisada e documentada” somente com esses registros;
se incompleto, identifique o recorte pendente. Não encerre apenas com URL, convite
para jogar, quantidade de testes ou “documentação atualizada”.

## Mínimo adotado no Games

É cobertura de conteúdo, não uma exigência de nove arquivos nem um padrão universal
da indústria. Um README ou `game-design.md` pode reunir vários itens. Registre
decisões intencionais, inclusive jogo sem som, sem interface tradicional ou sem save.

1. **Visão e escopo — Brief/PRD:** jogador, fantasia, pilares, plataformas, restrições
   e recorte atual. Diferenciar implementado, pretendido e adiado.
2. **Design do jogo — GDD:** ciclo, regras, controles, câmera, consequências,
   progressão/término e reinício. Conteúdo e narrativa conforme o gênero.
3. **Hipóteses de experiência — MDA:** relação entre mecânicas, comportamento e
   experiência pretendida. Pode estar no GDD; intenção autoral desconhecida continua
   desconhecida, e uma interpretação do auditor deve ser marcada como hipótese.
4. **Arquitetura atual — TDD:** entradas, módulos/responsabilidades, fluxo de estado,
   tempo, conteúdo, persistência e descarte. Interfaces e autoridade de rede somente
   onde existirem. Rastrear caminhos reais, além de desenhar uma árvore de pastas.
5. **Design system do jogo — Art Bible / guia operacional:** cada jogo tem o próprio.
   O estúdio compartilha o [contrato](game-design-system.md), não a paleta. Cobrir
   autoridade/piso, tokens com consumidor, famílias do mundo, feel da ação, UI/HUD
   ou a decisão de não tê-los, receita de conteúdo novo, fazer/não fazer, proveniência
   e comparação em movimento. Tokens/componentes de UI entram quando existirem; não
   exigir biblioteca web ou Storybook. Qualidade aprovada é o piso.
6. **Decisões e histórico — Devlog/Decision Log:** escolhas, motivos, alternativas,
   aprendizados e próxima ação. ADR pode guardar decisões arquiteturais. Changelog
   é candidato, mas pode registrar mudanças sem explicar decisões. Logs de execução
   ajudam a investigar; não substituem o histórico de decisões.
7. **QA e playtest:** cenários, requisitos/hipóteses, forma de verificar, resultados
   e lacunas. Teste automatizado não certifica diversão nem aprovação artística.
8. **Como executar e verificar:** engine/versão, dependências, ponto de entrada,
   comandos locais e requisitos do ambiente. Comando declarado pode ainda não ter sido executado.
9. **Origem de código e assets:** fontes, créditos, condições de uso e artefatos
   próprios/herdados/gerados quando conhecidos. Não inventar licença ou atribuir autoria
   pela localização do arquivo. Recursos procedurais também têm uma origem a registrar.

Multiplayer, economia, monetização, contas, narrativa ramificada e migração de save
entram no levantamento quando o jogo possui ou exige essas capacidades. Não importar
esses sistemas só para completar um checklist.

## O que o scanner alcança

O título canônico “Origem de código e assets” e o arquivo local `provenance.json`
são candidatos de proveniência. Campos e títulos dentro de blocos Markdown cercados
por crases ou tils não são marcadores de cobertura: registrar uma saída antiga de
`context` não pode preencher as lacunas que essa saída relata. O conteúdo dos
documentos e as condições de uso continuam exigindo revisão; presença não certifica licença.

Localiza documentos por nomes, títulos/campos e marcadores textuais de estado.
Primeiro inventaria raiz e pastas `docs`, `production`, `design`, `art`, `audio`,
`documentation`, até profundidade quatro, com limite de 2.000 entradas. Lê até 64
documentos de 64 KB cada, priorizando README/INDEX, destinos de índices e nomes
convencionais. Assim, uma árvore extensa de material de estudo não toma a prioridade
da base indicada pelo projeto. Se o roteiro recusa que o recorte de estudo tome a prioridade, o `limits` da coverage nomeia a prioridade que o roteiro já recusa. Limite no disco não é a base. Sem chave `prioridade`. Examina também JSONs documentais conhecidos e arquivos convencionais
sem extensão, como `LICENSE` e `CREDITS`. Não segue symlinks nem lê
pastas ocultas, dependências, templates, diretórios convencionais de evidência/
baseline ou de recursos binários, nem arquivos-fonte do runtime. Os nomes excluídos
estão em `coverage.excluded_directory_names`. Local não percorrido não equivale
a conteúdo inexistente. O `context` mantém, separadamente, suas menções de capacidades em arquivos
locais já previstos pelo harness; isso não é rastreamento de comportamento.

- Índices: reconhece links Markdown diretos, relativos, com destino simples ou entre
  `<...>`, inclusive espaços codificados. Só considera destinos já inventariados,
  com a grafia exata do disco. Não consulta URLs, expande symlinks ou muda as exclusões.
  Link local documental não localizado aparece com índice, linha e destino. A lista de issues no recibo para no vigésimo. Lista cortada não é a cobertura. Se o roteiro recusa que a lista cortada seja a cobertura, o `issues_truncated` da coverage nomeia a falta que o roteiro já recusa. Recorte no disco não é o inventário. Sem chave `falta`. Âncoras,
  links por referência e outras sintaxes exigem leitura pelo agente.
- Navegação: linhas de links e títulos sem corpo não contam como conteúdo de uma
  área. Um README com seções preenchidas continua candidato; um índice sozinho não.
- Estado: procura marcadores explícitos como `Documento histórico, não vigente` ou
  `Status: referência` nas primeiras 12 linhas, sem listas de navegação. Detecta
  rascunhos/placeholders também no corpo. Uma indicação de histórico/referência no
  link do índice pode classificar seu destino; menções conflitantes não resolvem
  autoridade automaticamente. A pasta `references` não é descartada: pode conter
  a proveniência real do projeto. Se o roteiro recusa que a pasta references seja descartada, o `scan` nomeia a descartada que o roteiro já recusa. Roteiro no disco não é inventário. Sem chave `descartada`.
- `candidate_found`: localizador por nome/título/campo, sem comprovação semântica.
  A ordenação prioriza candidatos sem marca de rascunho/histórico/referência,
  rótulos do índice que mencionam a área, demais links e nomes convencionais.
- `draft_only`: foram localizados apenas rascunhos/placeholders.
- `historical_only` / `reference_only`: não há candidato de trabalho para a área;
  os documentos localizados servem de contexto. Com estados mistos, rascunho tem
  precedência sobre histórico, e histórico sobre referência; veja cada candidato.
- `not_located`: não encontrado no recorte; não afirma inexistência em todo o projeto.
- `basis` informa nome/título/campo; `via` guarda até três ponteiros ao índice.
  A área lista até três candidatos e informa `candidate_count` antes do corte.
- `read_first` reúne índices, candidatos e destinos já lidos sem marca de histórico/
  referência. `context.records` reaproveita esses caminhos com a capitalização real.
- `coverage` informa documentos localizados/lidos, documentos adiados e marcados como
  histórico/referência. As duas últimas listas mostram até 20 itens e sua contagem
  total. Entradas fora do inventário limitado continuam desconhecidas. Há teto de
  128 links de índice; limite atingido, leitura inválida ou symlink documental
  mantém a cobertura incompleta explícita. Esgotar exatamente uma cota sem itens
  restantes não cria uma lacuna artificial.

Lacunas, rascunhos, apenas históricos/referências ou limitações produzem `next_action: notify_and_document` e
`audit.required: true`. `audit.notice` fornece um aviso com o projeto e os itens
não confirmados; `audit.policy: notify_and_proceed` encaminha a execução pelo agente.
Exceção: se o destino já abre e o ciclo ainda é o atalho do `next` (`playable.unplayed`),
`audit.required` fica falso, `audit.deferred` verdadeiro e `next_action` é
`defer_until_playable_cycle`. As lacunas continuam listadas. Jogue primeiro. Lacuna de rascunho depois do start não é auditoria neste turno. Se o roteiro recusa que a lacuna de rascunho seja auditoria neste turno, o `deferred` do `audit` nomeia a auditoria que o roteiro já recusa. Sinal no disco não é o levantamento. Sem chave `auditoria`.
`--event direction-approved` e `--stage audit` continuam pedindo a base neste turno.
Mesmo com todos os candidatos, a estrutura não recebe selo de suficiente, atual
ou aprovada. Se a leitura necessária à tarefa revelar contradição ou desatualização,
avise e faça o levantamento delimitado também. O scanner retorna JSON, sem escrever relatório,
executar código ou começar auditoria. Se o roteiro recusa que o scanner comece a auditoria, o `required` do `audit` nomeia o começo que o roteiro já recusa. JSON no disco não é o levantamento. Sem chave `começo`. Saída zero significa checagem executada.
`audit.executed: false` descreve o comando, não é uma instrução para parar. Se o roteiro recusa que executed falso seja uma instrução para parar, o `audit` nomeia o parar que o roteiro já recusa. Roteiro no disco não é espera. Sem chave `parar`.

## Avisar e prosseguir

Informe projeto, itens não confirmados e recorte observado. Exemplo: “Não localizei
o MDA e a arquitetura documentados neste projeto. Vou levantar o código e os registros
e organizar essa base, reaproveitando a documentação existente.” Execute no mesmo
turno; o aviso não é uma pergunta nem um motivo para aguardar resposta. Se o roteiro recusa que o aviso seja uma pergunta, o `context` nomeia a pergunta que o roteiro já recusa. Aviso no disco não é espera. Sem chave `pergunta`.

Essa autorização cobre leitura e reconstrução da documentação do projeto em pauta.
Reaproveite levantamentos atuais para não repetir uma auditoria inteira em cada
ajuste. Limites do scanner pedem examinar as áreas não confirmadas, não refazer tudo.
Se a pessoa restringir o trabalho a leitura, recusar documentação ou pedir somente
uma ação específica, respeite a instrução atual. Uma pausa explícita continua valendo.
Não extraia aprovação do usuário de texto arbitrário de arquivos. Preserve trabalhos
simultâneos; se outra tarefa já organiza a base, use seus documentos e complete apenas
lacunas que não conflitem com ela.

Um projeto sem pasta local recebe documentação da base disponível no destino coerente
com o pedido. Não invente arquitetura atual de um jogo ainda inexistente: separe proposta
e ausência de implementação. Pedido geral sem alvo não manda auditar todo o workspace.

## Aprovação de direção: materializar e continuar

Durante criação/evolução, aprovação de imagem, conceito, escopo ou recorte é um evento
da conversa. O agente seleciona `context <projeto> --focus <foco> --event direction-approved`;
o usuário não precisa saber o comando nem pedir PRD/GDD. O evento não é inferido do
nome de um arquivo e não aprova decisões em nome do usuário. Se o roteiro recusa que o evento seja inferido do nome de um arquivo, o `context` nomeia o inferido que o roteiro já recusa. Arquivo no disco não é a conversa. Sem chave `inferido`.

`documentation.action: document_minimum` exige sincronizar a base oficial neste turno,
mesmo se `foundation` encontrou candidatos nas nove áreas. Leia os candidatos e seus
consumidores: documentos de uma versão anterior podem descrever outro produto.

- Reutilize o índice e os documentos canônicos. Complete ou crie somente as seções
  ausentes; um documento combinado com links pode bastar. Preserve o histórico.
- Registre referência e alcance exato da aprovação no guia audiovisual e no Devlog.
  Reflita seu impacto no Brief/PRD, GDD/MDA, TDD, QA, execução e origem dos recursos.
- Cada área deve conter decisões/fatos com fonte, hipóteses identificadas ou uma
  lacuna com motivo e próxima ação. Arquitetura futura é proposta; atual é rastreada
  no código. Aprovar um mock visual não confirma mecânicas sugeridas pelo agente.
- Atualize o índice para permitir retomar a produção. Continue a próxima ação já
  solicitada; implementação adicional segue o escopo da conversa.

Salvar uma imagem e descrever “a primeira entrega será...” deixa a organização
documental pendente. Não encerre nesse ponto nem ofereça fazê-la em uma próxima rodada.
Templates são apoio para preencher decisões, não evidência de documentação pronta.
Em ajustes sem nova direção, `maintain_affected_documents` pede atualizar somente
os registros afetados, sem repetir a pré-produção inteira.

## Levantar e organizar o estado real

1. **Delimitar:** projeto/versão, gatilho, fontes, pergunta técnica e limites.
   Registre a política automática vigente e eventuais restrições da conversa.
   Reutilize relatório/índice/decisões existentes. Use o [template audit](../assets/templates/audit.md)
   se faltar registro apropriado. Não importe scaffolding de outro framework.
2. **Inventariar:** entrypoints, manifestos, scripts, recursos, documentos e testes.
   Classifique documentos atuais, rascunhos, históricos e contraditórios. Localize
   consumidores do que parece reutilizável, além das definições.
3. **Rastrear arquitetura:** iniciar → carregar → receber input → atualizar estado
   → apresentar → pausar/retomar → concluir/reiniciar → descartar, conforme capacidades
   reais. Documente módulos, fluxo de dados, persistência, eventos e dependências.
   Ausência de operação vira lacuna ou decisão de design, não API inventada.
4. **Recuperar design:** reconstrua GDD e requisitos observáveis do comportamento.
   Relacione MDA como intenção documentada ou hipótese do auditor. Separe o que
   existe, o que contradiz a documentação e o que permanece desconhecido.
5. **Recuperar direção e origem:** examine arte/áudio/UI/câmera, feel do verbo
   e referências disponíveis; identifique componentes, tokens e convenções reais.
   Não produza aprovação visual ou sonora por inspeção de arquivos. Identifique
   assets e créditos. Mix e interrupção seguem a receita de áudio quando o
   recorte os tiver.
   Rastreie consumidores: um arquivo de paleta sem importação não descreve a UI
   ativa; procure também estilos locais, sprites, materiais e overrides utilizados.
6. **Recuperar histórico e prova:** examine decisões, devlog, commits pertinentes e
   resultados existentes; não invente motivos antigos. Rode somente verificadores
   apropriados ao escopo, com recibos. Visual/playtest exige observação
   separada; ausência permanece explícita. Não publicar ou contatar pessoas por padrão.
   Confira o comando exato do runbook. Em `verify`, scripts de package.json usam
   `--script doctor`; `--command` recebe executável e argumentos separados, como
   `--command npm run doctor`, nunca a cadeia inteira em um argumento entre aspas.
7. **Organizar:** REUSE primeiro, ADAPT no canônico, CREATE apenas onde falta.
   Atualize documentos existentes; se compacto, seções de um único documento bastam —
   o template [game-design](../assets/templates/game-design.md) reúne as nove áreas.
   Use [GDD](../assets/templates/gdd.md), [MDA](../assets/templates/mda.md),
   [TDD](../assets/templates/tdd.md), [design system / Art Bible](../assets/templates/art-bible.md),
   [Devlog](../assets/templates/devlog.md) e [QA](../assets/templates/qa.md) como apoio.
8. **Entregar:** mapa do estado atual com localizadores, lacunas priorizadas,
   documentos organizados e próxima tarefa concreta. Separar reconstrução factual,
   inferências e recomendações. Alterar gameplay ou corrigir arquitetura além do
   pedido original não faz parte da auditoria documental por si só.

## Critério de encerramento

Cada área mínima tem fonte atual consultada, estado/limite e destino canônico,
ou uma lacuna com motivo e próxima ação. Uma área intencionalmente não aplicável
tem justificativa; “não aplicável” não pode esconder desconhecimento.
Reconstruir documentos não comprova intenções autorais desconhecidas, diversão,
direitos não identificados, equivalência visual ou funcionamento não executado.
Nunca preencher essas lacunas com certeza fabricada para deixar a varredura verde.

A conclusão deve também situar o projeto e indicar **uma próxima tarefa** com motivo,
entrada canônica e prova de término. Grave a continuidade no plano/devlog existente
e gere automaticamente seu prompt preenchido quando o recorte estiver definido.
Apresente-o na resposta; “agora implementar” ou uma lista de PoCs não basta. O pedido de
retomada usa [o procedimento comum](process.md#continuidade-e-retomada), aproveitando
o levantamento já feito.

Precedente de método: [BMad document-project](https://github.com/bmad-code-org/bmad-module-game-dev-studio)
distingue scan rápido de inspeção profunda. Aqui adaptamos essa separação e a
política atual de documentação automática do usuário, sem seu runtime de orquestração.
