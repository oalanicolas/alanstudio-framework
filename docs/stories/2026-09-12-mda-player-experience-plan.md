# Evolução do framework: guiar uma pessoa da ideia ao jogo

Data: 2026-09-12. Revisão 6: auditoria de Rabisco Red/Pac-Rabisco e adaptação por
referências, com Impeccable como referência principal de aplicação e uso. Estado:
**versão 0.10.4 implementada; compatibilidade técnica verificada; dois replays com
Luna como desenvolvedor reprovados no pedido; robustez e validação humana pendentes**.
Base inspecionada: núcleo `09408361d2bacfac83dd4fc04b572dc7c2de0c7a`, incluindo os
arquivos presentes no checkout. A alteração preexistente em `recipes/release.md`
não foi modificada; a alteração paralela em `recipes/visual.md` também foi preservada.
A revisão 3 não tinha ensaio independente. A revisão 4 acrescenta execução por um
desenvolvedor separado, interação de Luna e leitura de retomada por outro agente;
não houve playtest humano ou experimento de eficácia.

**Direção da mudança:** priorizar a capacidade do agente de conduzir a pessoa
até uma pequena experiência coerente com sua ideia, abrir o jogo, orientar o que
experimentar e transformar sua reação na próxima melhoria. A primeira proposta
colocava ficha de experimento e métodos de playtest cedo demais para esse público.
Esses recursos continuam úteis quando existe uma pergunta que precisa deles.

O critério de utilidade imediata é: **a pessoa consegue escolher, jogar, dizer o
que achou e continuar sem aprender os comandos ou a terminologia do framework?**
Uma jornada melhor ainda precisa ser demonstrada com pessoas; os testes abaixo
comprovam comportamentos das ferramentas e conflitos das instruções.

O [registro da leitura no laboratório](../../../games-workspace/docs/pesquisas/MDA%20%E2%80%94%20evolu%C3%A7%C3%A3o%20do%20framework%20de%20games.md)
identifica o corpus, o texto fornecido por Alan e os limites da pesquisa disponível.
Este documento é o destino central da proposta transferível; não é uma nova receita
ativa nem substitui os documentos canônicos abaixo.

## Revisão 6 — primeiro replay reprovado e auxílio executável

Luna leu o guia 0.10.3, mas confirmou que não abriu imagens, comparou a cena apenas
ao final e testou somente presença de strings. A entrega excluiu áudio e apresentou
um mapa de formas simples. O [resultado preservado](../../../games-workspace/docs/_anexos/mda-framework/evidence/2026-09-12-luna-build-failures/replay-1/RESULT.md)
reprova a hipótese de que explicitar critérios em texto bastaria nesta execução.

A 0.10.4 torna explícitas operações de produção de arte e inclui
`scripts/check_web_delivery.py`: checagem de HTML servido e recursos literais
para web estática local. Não é detector artístico nem teste de jogabilidade.
O novo `tests/test_web_delivery.py` passou em nove casos de HTTP real, incluindo
recursos ausentes, servidor errado, HTML devolvido no lugar de áudio, imports,
módulos órfãos e um falso positivo de `canvas.toDataURL` encontrado e corrigido
na aplicação ao Red. O checker final identifica exatamente os três recursos 404
do Red e os seis sons 404 do Pac. O primeiro replay passa no checker e continua
reprovado artisticamente: limite demonstrado, não apenas declarado.

Arquivos adicionais à revisão 5: script, testes e ajustes na rota de adaptação.
A acessibilidade pertinente foi conservada no piso; “entrada” não a substitui.
O [candidato 2](../../../games-workspace/docs/_anexos/mda-framework/evidence/2026-09-12-luna-build-failures/framework-candidate-2/manifest.json)
identifica os arquivos antes do segundo replay com outro Luna, sem o diagnóstico.
Critérios e adaptações do segundo teste foram registrados antes da execução.

O [segundo resultado](../../../games-workspace/docs/_anexos/mda-framework/evidence/2026-09-12-luna-build-failures/replay-2/RESULT.md)
também reprovou: abriu dois pins e rodou a ajuda HTTP, mas fez captura direta sem
batalha, manteve formas simples e áudio ausente. Declarou a falha do navegador
e os testes herdados incompatíveis. O revisor conseguiu abrir sua cena depois;
não corrigiu código nem fez um resgate atribuído ao Luna. As duas execuções são
evidência de limites e de adoção parcial, não de eficácia geral ou ganho causal.

**Próxima prova prioritária:** uma base pequena e testada de exploração → encontro
→ batalha → captura, com arte real fiel às fontes, aplicada pelo Luna e revisada
contra o pedido. Não começar por outra engine, um catálogo de gêneros ou mais
questionários. O estudo humano de condução continua pendente, mas não substitui
resolver essa lacuna de produção. Esta revisão conclui a auditoria e os dois
replays; não declara que o framework já garante boas entregas.

## Revisão 5 — entregas reais atribuídas ao Luna

Alan rejeitou Rabisco Red e Pac-Rabisco, criados a partir de pedidos com gênero e
IDV definidos. Os históricos concluídos, consumidores reais, testes e navegador
mostram falhas necessárias ao recorte: movimento bloqueado e poder sem término no
Pac; variedade de encontros impossível e interrupção de batalha pelo Dex no Red;
URLs de assets 404; arte do Red distante do painel indicado. Não foi preciso exigir
o conteúdo integral de Pokémon para demonstrar a falha.

O [caso completo no laboratório](../../../games-workspace/docs/_anexos/mda-framework/evidence/2026-09-12-luna-build-failures/REPORT.md)
preserva pedidos, mensagens/ações observáveis, fontes com hashes, reproduções e
capturas. Originais não foram alterados. Diagnóstico com estado fabricado está
separado de interação pública. O campo de modelo não veio no histórico consultado;
Alan é a fonte da atribuição histórica a Luna.

Correção de interpretação do piloto anterior: Luna era o criador simulado;
outro agente construía. Aquele caso não valida o desempenho de Luna implementando.
O [novo protocolo](../../../games-workspace/docs/_anexos/mda-framework/evidence/2026-09-12-luna-build-failures/REPLAY-PROTOCOL.md)
define antes da execução um replay isolado com `gpt-5.6-luna`, sem o gabarito da
auditoria, e compara o resultado aos critérios do pedido.

- [x] Auditar os dois jogos e as entregas concluídas sem corrigir os originais.
- [x] Confrontar imagens do painel indicado, assets do universo e a cena do Red.
- [x] Inserir uma rota condicional: traduzir referências → comparar a cena → testar
  o ciclo inteiro; nenhuma entrevista extra, novo schema ou engine.
- [x] Remover a ambiguidade de arte provisória na entrega de estilo ilustrado.
- [x] Conferir compatibilidade: 16 testes de comandos e 514 do launcher do
  laboratório passaram; 82 links iniciais válidos; entrada com 118 linhas.
- [x] Concluir e avaliar o primeiro replay com Luna implementando, sem resgate oculto:
  reprovado, conforme a revisão 6 acima.

Arquivos centrais desta revisão: `SKILL.md`, `commands/craft.md`,
`references/{new-work,reference-adaptation,craft-floor,delivery}.md`, `adoption.md`
e esta story. O novo guia é carregado quando há referência, não em toda mudança.
Sem alteração de código do harness, starter, dependências ou testes de frases.
As mudanças preexistentes em `recipes/release.md` e `recipes/visual.md` continuam
preservadas. Não se afirma que mais instruções garantam uma boa execução; o replay
precisa demonstrar quais omissões diminuíram e quais persistem.

## Implementação autorizada — 0.10.2

Pedido de Alan: continuar avançando, tendo a skill Impeccable como referência
máxima de aplicação e uso. A versão local consultada foi `4.3.1`, em
`/Users/oalanicolas/.agents/skills/impeccable`; `context` foi executado no núcleo.
Esta tarefa modifica o processo existente, sem criar uma superfície de frontend.
Os fluxos de entrevista visual, geração de comps e revisão de UI não se aplicam
a esta manutenção documental.

Uma correção à revisão 2: o menu completo tem lugar na invocação vazia da skill,
como na Impeccable. O problema é usá-lo para um pedido concreto em linguagem comum.
Da mesma forma, `shape` explicitamente solicitado continua entregando planejamento;
o preparo interno de uma criação já autorizada não acrescenta confirmação repetida.
Essa adaptação respeita a autorização da conversa e não é uma reprodução literal
das paradas de Impeccable.

Aceites definidos antes da edição, conferidos por revisão própria das instruções
e testes técnicos. Marcação concluída não equivale a uma jornada humana executada:

- [x] Separar invocação vazia, dúvida de workflow, pedido concreto e planejamento explícito.
- [x] Reutilizar decisões e autorização; resolver escolhas materiais em linguagem comum.
- [x] Usar `start` quando adequado e exigir adaptação da ação à ideia antes de entregar o jogo.
- [x] Exigir verificação de acesso, ação e reinício e algo curto para experimentar.
- [x] Aceitar reação livre, conservar autoria e distinguir relato de diagnóstico.
- [x] Recomendar continuação pelo objetivo e evidência, sem obedecer cegamente a `next`.
- [x] Manter os documentos pelo agente e preservar qualidade e aprovação humanas.
- [x] Conferir catálogo, referências, regressões aplicáveis e limites da validação.

Arquivos alterados: `SKILL.md`, `README.md`, `commands/README.md`,
`commands/commands.json`, `commands/{shape,craft,init,critique,next,playtest}.md`,
`references/{routing,new-work,creative-workflow,delivery,process,sources}.md`,
`adoption.md` e esta story. Evidências e registro do caso permanecem no laboratório.
Runtime, schemas de recibos, jogos e starter não fazem parte desta implementação.

Validação: 525 testes do núcleo e 5 adicionais do catálogo de áudio do laboratório
passaram. A execução inicial restrita falhou ao abrir portas locais; o teste mínimo
retornou `EPERM`, e a repetição com rede local permitida passou sem mudar código ou
testes. `doctor` confirmou catálogo, manifesto do starter e atalhos vigentes.
A entrada da skill tem 116 linhas. Foram conferidos os links novos e alterados.
O núcleo Python não tem scripts próprios de lint/typecheck npm.

O [registro de verificação no laboratório](../../../games-workspace/docs/_anexos/mda-framework/evidence/2026-09-12-guided-creation/README.md)
preserva logs, hashes e a revisão de nove percursos por leitura. Naquela etapa não
houve revisão independente ou validação de UX com participante. O texto de diagnóstico na interface do
starter permanece fora deste patch; ajuste-a pela fricção observada no piloto.

Continuidade proposta na revisão 3, preservada como histórico: testar a condução
com uma pessoa sem experiência, em um projeto e
recorte definidos para o piloto. Pronto quando houver registro de ideia, decisões,
acesso ao jogo, reação e primeira melhoria, com os obstáculos e limites explícitos.
Prompt para retomar: “Continue a validação da condução 0.10.2 seguindo esta story.
Defina o projeto e o recorte do piloto, acompanhe uma pessoa iniciante da ideia à
primeira melhoria e preserve pedido, ações e resultado reais. Corrija a primeira
fricção material demonstrada nas referências existentes; não simule aprovação
humana nem acrescente infraestrutura sem necessidade observada.”

O restante deste documento conserva o diagnóstico e o repertório da pesquisa.
Seções sobre questionários e modelos aprofundados continuam propostas condicionais.

## O diagnóstico pragmático da base anterior

### Resultado posterior: ensaio de criação e primeira melhoria

Após a implementação acima, Alan pediu simulação completa, autorizando Luna no
papel de criador leigo. O [relatório do piloto](../../../games-workspace/docs/_anexos/mda-framework/evidence/2026-09-12-luna-pilot/REPORT.md)
preserva protocolo anterior à entrega, mensagens sem reescrita, versões, ações
e critérios. O teste usou instruções 0.10.2 e um protótipo local; não uma conversa
inteiramente inventada pelo autor da análise.

- Luna escolheu um jogo de desviar de meteoros e respondeu uma escolha sobre
  controle direto ou inércia. Não escolheu engine, comandos ou campos de documento.
- O desenvolvedor entregou a ação pedida, acesso, controles e um convite a duas
  tentativas. Luna abriu no Chrome, iniciou, enviou setas, perdeu e reiniciou.
- O relato foi positivo e comparou os dois tempos. A V2 tornou essa diferença
  visível no resultado, preservando controle, dificuldade, render, áudio e assets.
  O comentário sobre aprender as setas não virou diagnóstico de defeito.
- Na repetição, a interface mostrou 5,2 s, depois 11,3 s e diferença de 6,1 s;
  o recorde de 23,1 s permaneceu. O ganho percebido no relato continua simulado.
- Uma leitura de retomada sem histórico encontrou V2 concluída e a pendência de
  receber o relato, conforme o canônico naquele momento; não inventou uma V3.

O ensaio encontrou uma limitação importante para interpretar a prova: as setas
foram enviadas como toques discretos. Isso não comprova conforto com controle
sustentado. A experiência do instrumento e a do jogador precisam permanecer
distintas. As capturas da Luna ficaram no histórico das ferramentas, sem arquivos
exportados; as provas visuais preservadas no protótipo são do desenvolvedor.

**Extração pequena, posterior ao congelamento da V2:** o
[protocolo de qualidade](../../references/quality.md#protocolo-de-observação)
agora explicita a separação entre preferência, defeito, hipótese e limite da
automação, além de correção/repetição quando há causa sustentada. A
[condução do criador](../../references/creative-workflow.md#conduzir-quem-está-criando)
aponta essa referência e reconhece que uma reação positiva também pode orientar
uma melhoria. É esclarecimento nas instruções existentes, sem comando, schema,
formulário, questionário obrigatório ou nova arquitetura.

Esses complementos preservam o número 0.10.2 da skill; hashes antes/depois
identificam a revisão documental. Seis regressões dos consumidores existentes
de qualidade e autoria passaram após a edição. Os 525 testes do núcleo e cinco
adicionais do laboratório citados acima pertencem à verificação anterior; não
foram repetidos integralmente para este complemento documental. O protótipo passou
oito testes na V1 e onze na V2, além das verificações de entrega registradas.

A simulação demonstra viabilidade deste percurso e fornece exemplos úteis de
condução. Não estima ganho de produtividade ou diversão, nem substitui observar
uma pessoa iniciante. O próximo teste humano, se realizado, deve usar o mesmo
percurso de ideia, ação, reação e melhoria; o ensaio atual não autoriza recrutamento.

### Diagnóstico que motivou a 0.10.2

Já temos o ciclo conceitual, ferramentas de execução, starter, receitas,
documentação compacta, captura de notas e continuidade. A lacuna principal está
na ligação entre esses recursos e a conversa com o criador. Acrescentar uma
camada nova de formulários ou um assistente com etapas fixas não resolve essa ligação.

Examinei a entrada da skill, seus comandos, consumidores em `game.py` e o starter.
Depois executei `guide → start → next → note → next → playtest` numa fixture.
O [registro do teste](../../../games-workspace/docs/_anexos/mda-framework/evidence/2026-09-12-beginner-journey/README.md)
preserva entradas, saídas, hashes e limites. A nota era sintética e identificada
como avaliação do agente; nenhuma pessoa foi usada ou simulada como participante.

| O que havia na base inspecionada | Evidência | Consequência prática e mudança proposta |
| --- | --- | --- |
| Entrada encaminha ausência de subcomando para catálogo de 23 comandos | `SKILL.md`, `references/routing.md` | Separar pedido natural de invocação vazia; nesta última, manter navegação e catálogo como na Impeccable |
| Confirmação obrigatória mesmo com direção clara | `commands/craft.md`, §Avaliar; `commands/shape.md`, §Executar | Reutilizar decisões e autorizações existentes; perguntar apenas pela escolha material que falta |
| Ideia de horta vira texto sobre o arcade de orbes | `01-guide` e `02-start`; regras idênticas ao starter | O agente verifica adequação e adapta a ação central antes de apresentar a criação como o jogo pedido |
| `start` permite começar sem seis rascunhos | `02-start`, `03-next-before-note` | Consumir esse recurso; atualizar memória com decisões reais conforme o trabalho avança |
| Depois de uma nota sobre controle, `next` propõe par/look/chuva/voz | `05-next-after-note`, prioridade `cycle.craft` | O agente prioriza pelo pedido e pelo problema; a sugestão determinística é insumo |
| Nota livre é aceita, mas a classificação de achado exige quatro campos | `04-note`, `06-playtest` | A pessoa relata em suas palavras; o agente conserva o relato e investiga o que falta |
| Critique exige relatório integral e escolha de área pelo usuário | `commands/critique.md`, §Entregar | Mostrar diagnóstico principal, mudança recomendada e prova; detalhes ficam acessíveis no registro |

O JSON extenso é apropriado como interface entre ferramentas e agente. O problema
surge ao repassá-lo à pessoa como instrução de trabalho. No teste, o prompt inicial
tinha 294 palavras, combinando comandos, controles de vários dispositivos, queries,
simulação e recibos. Não precisamos criar outra API para o agente resumir isso em
uma ação adequada ao momento e ao dispositivo.

O teste de horta não demonstra defeito no algoritmo de um gerador de jogos:
`start` copia uma base e introduz a frase; a documentação reconhece esse limite.
Ele demonstra uma responsabilidade que a skill precisa cumprir: **reuso de
infraestrutura não encerra a adaptação à experiência pedida**. Na base inspecionada
há um starter (`canvas-arcade`); não presumir que ele é adequado a qualquer ideia,
nem construir antecipadamente um catálogo de engines para resolver isso.

## A experiência que o framework deveria oferecer

O criador precisa fazer poucas coisas: expressar uma intenção, decidir escolhas
que afetam seu jogo, experimentar e reagir. O agente assume tradução técnica,
implementação, validação disponível, organização das evidências e recomendação.

| Momento | O que a pessoa vê/faz | O que o agente resolve |
| --- | --- | --- |
| Ideia | Descreve o jogo, uma referência ou o que gostaria de sentir | Consulta contexto, propõe uma situação jogável e escolhe a preparação técnica adequada |
| Escolha relevante | Decide entre experiências concretas quando a intenção ainda está aberta | Expõe consequência e recomenda uma; não pede para escolher engine, escala ou método sem necessidade |
| Primeira entrega | Abre uma partida e recebe o controle necessário para aquela ação | Implementa o recorte, serve/abre quando o host permite e verifica a superfície acessível |
| Experimentação | Recebe uma tarefa curta: algo para tentar e algo para reparar | Escolhe uma incerteza; testa previamente falhas técnicas que conseguir verificar |
| Reação | Conta o que aconteceu e o que sentiu, com liberdade para outras observações | Registra fala, separa interpretação, reproduz quando possível e não inventa causa |
| Continuação | Entende a melhoria recomendada e sua razão | Executa o autorizado ou resolve a decisão material pendente; mantém memória e direção |

Isso vale também para quem já tem jogo. Uma reclamação sobre o pulo entra na
correção daquele pulo. A pessoa não precisa voltar à concepção nem passar por uma
entrevista de identidade. “Continue” retoma o recorte vigente e as decisões aceitas.

Se o ambiente não abre o jogo, o agente investiga e resolve o preparo necessário
dentro da autorização vigente. A ausência de erro num comando não é abertura
verificada. Na fixture desta análise, `npm run serve` saiu sem anunciar escuta;
não houve verificação de página. Essa tentativa foi registrada como inconclusiva,
sem afirmar defeito geral do starter. Uma entrega real ao criador ainda teria de
resolver o acesso ou identificar precisamente o bloqueio.

## Como usar os estudos sem ensinar siglas antes de jogar

| Contribuição do estudo | Trabalho interno do agente | Orientação em linguagem comum |
| --- | --- | --- |
| MDA: partir da experiência e prever consequências | Relacionar regras, apresentação, comportamento e sensação | “Você escolhe para quem entregar a colheita, e a reação do vizinho mostra que sua escolha importou.” |
| Playcentric: aprender com o jogo em uso | Construir um momento completo que responda à dúvida atual | “Vamos experimentar uma colheita e uma entrega para sentir como é cuidar desse lugar.” |
| GameFlow/PLAY: inspecionar obstáculos previsíveis | Conferir compreensão, controle, consequência e ritmo pertinentes | “Antes de você jogar, vou conferir se dá para entender o que fazer e recomeçar.” |
| RITE: corrigir problemas claros e retestar | Observar, formular causa, mudar quando há suporte e comparar novamente | “O retorno da ação ficou pouco visível. Vou ajustar esse sinal e repetir a situação.” |
| Medição de experiência | Escolher instrumento apenas quando necessário e usar a forma adequada | Só introduzir pesquisa estruturada quando explicar qual decisão ela ajudará a tomar |

As frases são exemplos propostos, não resultados observados. Nenhuma delas obriga
a incluir desafios, competição ou cronômetro. O modelo precisa servir à fantasia
do jogo; uma experiência tranquila pode valorizar descoberta e vínculo.

Aprendizado pode acontecer dentro da escolha: “um tempo limite cria pressão;
para o clima tranquilo que você pediu, proponho começar sem cronômetro”. A pessoa
entende uma relação de design enquanto decide algo concreto. Glossários, cursos
e explicações extensas entram quando forem pedidos ou necessários à decisão.

## Exemplo de condução, do pedido à próxima melhoria

Exemplo inteiramente proposto; o teste do harness não produziu esta horta.

**Pedido:** “Quero um jogo tranquilo em que cuido de uma horta e entrego a colheita
aos vizinhos.”

**Condução inicial:** “Vou começar com um canteiro e uma entrega: você planta,
rega, colhe e escolhe um vizinho. A reação dele deve dar a sensação de cuidar de
um lugar e das pessoas. Vou preparar uma versão para experimentar no navegador.”
O navegador é uma escolha técnica possível neste contexto, não uma obrigação
universal. Se plataforma ou direção já estiverem definidas, elas prevalecem.
Uma dúvida que realmente mude a experiência pode ser resolvida antes de construir.

**Primeira entrega:** depois de implementar e verificar o acesso, o agente apresenta
o jogo e orienta: “Use o mouse para cuidar do canteiro e faça uma entrega. Repare se
você entende quando pode colher e se a reação do vizinho faz diferença para você.”
O recorte tem a arte, o som e a resposta necessários a essa sensação. Menor
quantidade de conteúdo não reduz a qualidade aprovada.

**Reação:** “Parece uma tarefa. Não fiquei com vontade de continuar.”

**Interpretação e ação:** conservar a fala. A IA pode investigar se há repetição
sem surpresa, pouca resposta do mundo ou outra causa. Se a observação sustentar
falta de consequência, recomendar uma mudança concreta: uma reação distinta do
vizinho à entrega. Se só houver o relato, fazer uma pergunta situada ou observar
o trecho antes de tratar essa causa como demonstrada. Não responder com um menu
de loja, pets, ranking, multiplayer e dezenas de novos recursos.

**Memória da rodada, mantida pelo agente:** queríamos cuidado e vínculo; entregamos
um canteiro; o criador relatou sensação de tarefa; a causa ainda é hipótese; a
próxima comparação examina a reação do vizinho. Usar o documento atual e ligar a
versão quando houver comparação. Esse registro permite retomar sem reentrevistar.

## O menor investimento que recomendo

**Primeira rodada, aplicada nas instruções 0.10.2: alinhar a entrada à primeira partida.** Foi ajustada a orientação
existente em `SKILL.md`, `references/routing.md`, `references/new-work.md`,
`commands/shape.md` e `commands/craft.md`. Prioridades: uma ação em linguagem
comum, confirmação apenas onde falta decisão material, uso coerente de `start`
quando adequado, fidelidade à ideia e entrega acessível com algo específico para
experimentar. Não criar novo comando, modo iniciante, perfil persistente ou wizard.

**Segunda rodada, aplicada nas instruções 0.10.2: ligar reação à continuação.** Foram ajustadas as orientações de `commands/critique.md`,
`commands/next.md` e da seção de continuidade existente para o agente recomendar a
próxima mudança a partir do relato e do objetivo. Se a interface do starter fizer
parte do caminho escolhido, trocar “o que o verbo sentiu” por uma pergunta situada
e separar detalhes de diagnóstico da ação principal. Não redesenhar o jogo nem
esconder controles de acesso para simplificar a orientação.

**Documentação é trabalho do agente.** Aproveitar `game-design.md` ou o canônico
existente. Atualizar decisão, implementação, reação e próximo passo; preencher
somente o que a rodada torna conhecido. Não acrescentar uma ficha paralela, nem
fazer a pessoa preencher as nove áreas. Os requisitos documentais aplicáveis ao
projeto continuam sendo atendidos pelo agente, proporcionalmente ao trabalho.

**Métodos mais pesados entram por necessidade observada.** Questionários quando
há uma pergunta relevante e participantes adequados; telemetria quando observação
ou dados existentes não respondem; experimento controlado quando a decisão exige
atribuição causal. Um ajuste de legibilidade não precisa atravessar essas etapas.

As confirmações de nova direção e ações consequenciais continuam respeitando
o pedido e as autorizações. Autonomia deve tirar o trabalho técnico da pessoa,
preservando suas decisões criativas.

## O que já existe e deve ser aproveitado

| Necessidade | Evidência no núcleo | Melhoria necessária |
| --- | --- | --- |
| Partir da experiência e iterar | [Workflow criativo](../../references/creative-workflow.md), passos 1–4 | Explicitar qual pergunta exige qual prova; preservar o ciclo de quatro passos |
| Hipótese falsificável | [Template MDA](../../assets/templates/mda.md): alternativa, efeito indesejado, apoio e contraprova | Dar conteúdo verificável à dinâmica e ligar a hipótese à sessão e à decisão |
| Observar pessoas | [Playtest](../../commands/playtest.md) e [QA](../../assets/templates/qa.md) | Distinguir descoberta, RITE, mensuração e comparação causal |
| Diagnóstico antes do teste humano | [Qualidade](../../references/quality.md) e [critique](../../commands/critique.md) | Incorporar seletivamente lacunas de GameFlow/PLAY, evitando duplicar checklists |
| Regra de parada e correção/reteste | [Pesquisa de critérios](../../references/observable-criteria-research.md), §5.3 | A referência ao RITE existe; falta operacionalizar sua triagem e os limites de comparação |
| Proveniência de evidências | [record e note](../../scripts/game.py), funções `record` e `note_observation` | Reusar campos e anexos antes de criar novos comandos ou schemas |
| Qualidade artística | [Design system](../../references/game-design-system.md) e workflow | Manter aprovação artística separada da medição de experiência |

Na busca por nomes em `references`, `commands`, `assets/templates`, `recipes`,
`scripts` e `tests`, não foram encontrados PXI, miniPXI, PENS, BANGS, GUESS,
GameFlow ou Playcentric. Isso indica ausência de adoção explícita desses métodos,
não ausência de todas as práticas que eles descrevem.

O código de `playtest_reading` procura estrutura de achados e registros; não
observa participantes nem atribui causa. Essa fronteira é correta e deve permanecer.

## O que os estudos acrescentam

**MDA oferece mais que três rótulos.** O paper e a palestra NWU trabalham com
modelos de experiência, condições de fracasso, distribuições de probabilidade,
recursos e feedback. Conceber parte da experiência desejada para as dinâmicas e
regras; observar percorre a relação inversa. Os oito tipos de diversão formam um
vocabulário aberto. O próprio paper inclui competição nos exemplos e não apresenta
uma fórmula universal de diversão. Fontes: [paper](https://users.cs.northwestern.edu/~hunicke/MDA.pdf),
[palestra NWU](http://algorithmancy.8kindsoffun.com/MDAnwu.ppt) e
[material local do workshop](../../../games-workspace/docs/_anexos/mda-framework/runs/mda-framework-20260912-e0/raw/leblanc-gdc2004-handout/derived/leblanc-gdc2004-OrientationHandout.txt).

**Arte, áudio, interface e narrativa participam da causa.** Lantz identifica a
ambiguidade de “mechanics” e “aesthetics”; a exposição pública de DDE organiza
design em blueprint, mecânicas e interface. A adaptação útil é nomear todas as
variáveis de design controláveis na hipótese. O framework já faz isso no workflow;
o template MDA pode tornar a cobertura explícita. Não é preciso renomear todo o
processo para DDE. Fontes locais: [Lantz, 2015](../../../games-workspace/docs/_anexos/mda-framework/runs/mda-framework-20260912-e0/raw/lantz-2015-mda/derived/lantz-mda-critique.txt)
e [Walk, 2017](../../../games-workspace/docs/_anexos/mda-framework/runs/mda-framework-20260912-e0/raw/walk-2017-from-mda-to-dde/derived/gamedeveloper-walk-mda-to-dde.txt).

**Processo, heurística e questionário cumprem funções diferentes.** O ciclo
Playcentric converge com o nosso workflow. PLAY oferece inspeção complementar;
isso não autoriza transformar todas as suas recomendações em exigências para
qualquer gênero. Por exemplo, perda de recursos conquistados pode ser parte da
experiência pretendida. Fontes: [Fullerton, excerto autoral](https://www.gamedeveloper.com/design/book-excerpt-game-design-workshop)
e [Desurvire e Wiberg, PLAY](https://userbehavioristics.squarespace.com/s/DesigningBetterGames-09HCI-Desurvire.pdf).

**PXI é um candidato para mensuração, sem nota geral de qualidade.** A validação
independente com 1.518 respostas favoreceu a escala, com dificuldades em imersão
e apoio ao modelo de fatores por construto. Na proposta, resultados permanecem
por dimensão; não viram média de “qualidade do jogo” ou certificação de acabamento.
[Validação independente, CHI 2024](https://edoc.unibas.ch/entities/publication/5c0c6e43-575c-4248-af2c-889e5db1859c).

**miniPXI exige uma ressalva adicional ao texto fornecido.** O estudo de
teste–reteste de 2024 encontrou resultados mistos em 100 participantes e quatro
jogos. Recomenda cautela ao acompanhar dimensões complexas, especialmente domínio
e imersão, usando apenas um item. Os grupos pequenos e a mudança real da experiência
ao longo do tempo limitam a conclusão. Portanto, miniPXI pode ajudar na leitura
exploratória, mas não será o termômetro automático de melhoria entre versões.
[Haider et al., versão pública de 2024](https://arxiv.org/html/2407.19516v1).

**A integridade do instrumento muda o que podemos afirmar.** O guia PXI avisa que
recortar construtos, reescrever itens ou mudar a escala cria uma variante e perde
a comparabilidade com o benchmark. “miniPXI challenge + autonomy + mastery” não
deve ser apresentado automaticamente como o instrumento validado completo.
Registrar versão, idioma e adaptação. Não foi confirmada nesta leitura uma versão
validada em português para nosso público; isso permanece lacuna, não prova de
inexistência. [Guia oficial PXI](https://playerexperienceinventory.org/docs).

**BANGS acrescenta satisfação e frustração de necessidades separadamente.** É útil
quando a pergunta envolve autonomia, competência ou vínculos sociais. Seu estudo
aponta limitações, incluindo menor confiabilidade da subescala de frustração de
autonomia. Não somar satisfação e frustração num saldo único.
[Artigo BANGS](https://doi.org/10.1016/j.ijhcs.2024.103289) e
[guia dos autores](https://nickballou.com/docs/bangs/userguide/).

**RITE tem evidência de correção de usabilidade, com alcance delimitado.** No caso
de Age of Empires II, 30 de 31 problemas receberam correção: os 97% são a proporção
de problemas que receberam uma mudança. A verificação subsequente fornece outra
evidência; o percentual isolado não demonstra aumento de diversão ou superioridade
causal do método. O artigo permite mudanças entre participantes, priorizando causa
e solução claras, e pede mais dados quando a causa ou o próprio teste são suspeitos.
[Medlock et al., paper original](https://www.jpattonassociates.com/wp-content/uploads/2015/04/rite_method.pdf).

Não adotar o ranking de quinze métodos como hierarquia científica. A validação de
uma medida não prova que usá-la melhora decisões de design. A convergência de
relato, questionário e comportamento também não garante causalidade: pode haver
expectativa induzida, aprendizado ou uma causa compartilhada.

## Ordem de adoção e locais de mudança

### Análise complementar solicitada em 12/09

Foi lido integralmente o [relatório comparativo fornecido por Alan](../../../games-workspace/docs/pesquisas/Frameworks%20de%20game%20design%20%E2%80%94%20compara%C3%A7%C3%A3o%20da%20evid%C3%AAncia.md),
incluindo as passagens adicionais sobre replicação, tipologias, telemetria e FPS web.
É uma síntese de pesquisa fornecida, não uma validação independente de todas as
fontes citadas. O paper original do RITE e o teste–reteste do miniPXI foram
conferidos novamente para as decisões abaixo. O relatório ficou fora do contexto
dos agentes do piloto para não induzir suas respostas.

| Recomendação do relatório | Decisão para o nosso framework |
| --- | --- |
| Separar concepção, processo, inspeção e mensuração (§§1, 17, 32) | Adotar a distinção no raciocínio do agente; o criador continua descrevendo uma ideia e experimentando o jogo |
| Design Evidence Loop em dez etapas (§20) | Usar como repertório; conservar o ciclo de quatro passos e os consumidores existentes, sem dez passagens obrigatórias |
| Corrigir com causa e solução claras, depois retestar (§§14, 33) | Tornar a triagem prática: falha demonstrada pede correção; causa ambígua pede investigação; preferência pede escolha de design identificada como tal |
| miniPXI de três dimensões por feature (§23) | Não tornar padrão; selecionar instrumento pela decisão, preservar sua identidade e explicitar adaptação e limites |
| Telemetria como prioridade de entrada e evidência “mais causal” (§35) | Instrumentar somente a dúvida que o jogo real apresenta; registros observacionais não isolam causa, e abandono não explica sozinho seu motivo |
| Stack “superior” e ausência de nível G tratada como estabelecida (§§1, 29) | Tratar como proposta e limite do corpus consultado; a pesquisa apresentada não demonstra superioridade causal desse conjunto nem uma ausência universal de estudos |
| Fichas por feature, quantidades e metas ilustrativas (§§22, 23, 33, 35) | Manter memória no canônico atual; não exigir novos formulários, seis jogadores, cem respostas ou uma taxa de vitória universal para criar ou melhorar |

Os 97% do caso RITE descrevem problemas que receberam correção, não o ganho de
diversão. O estudo de miniPXI encontrou confiabilidade variável entre construtos
e jogos. Essas duas fontes sustentam uso criterioso, não o empilhamento automático
de métodos. A análise anterior nesta story já contém as referências primárias e
seus limites; o relatório novo reforça a seleção pela pergunta, sem alterar o
critério de utilidade imediata para o criador.

O ensaio de criação executou o percurso e identificou limites concretos de
verificação. Ações de navegador de um modelo podem demonstrar acesso e
interação; relatos de uma persona simulada não validam compreensão, gosto ou
diversão de iniciantes humanos.

### Sequência de adoção

As duas primeiras linhas foram incorporadas às instruções em 0.10.2; a mudança de
copy do starter continua condicionada à observação do seu uso. A condução ainda
precisa de validação com iniciante. As demais linhas são repertório para necessidades
posteriores, não um backlog obrigatório antes de jogar.

| Prioridade | Mudança | Consumidor canônico | Aceite da implementação futura |
| --- | --- | --- | --- |
| Primeiro | Conduzir da ideia à primeira partida | `SKILL.md`, `references/routing.md`, `references/new-work.md`, `commands/shape.md`, `commands/craft.md` | Uma recomendação compreensível; decisões aceitas reutilizadas; ação do jogo corresponde à ideia; acesso verificado e orientação curta |
| Em seguida | Transformar reação em continuidade | `commands/critique.md`, `commands/next.md` e continuidade existente; copy do starter se usado | Relato livre preservado; interpretação identificada; próxima mudança explica como responde ao relato e à intenção |
| Quando a dúvida exigir | Aprofundar hipótese e modelo de dinâmica | `assets/templates/mda.md`, `references/preproduction.md`, workflow existente | Modelo ajuda a escolher ou descartar uma mudança; detalhes do starter não viram exigência para todos os jogos |
| Quando a observação exigir | Distinguir descoberta, correção/reteste e comparação controlada | `commands/playtest.md`, `references/quality.md`, `assets/templates/qa.md` | Método condiz com a decisão; versões alteradas entre sessões não viram comparação controlada |
| Quando a medição justificar | Orientar seleção e uso de instrumentos | Seção na referência de qualidade, ligada pelo playtest; separar arquivo apenas se o conteúdo justificar | Forma, idioma, adaptação e limites explícitos; questionário responde a uma pergunta concreta |
| Quando surgir lacuna de inspeção | Incorporar heurísticas pertinentes | `references/quality.md`, com origem em `references/sources.md` | Cada critério tem motivo de aplicação; tensão ou perda intencional não viram defeito universal |
| Após repetição demonstrada | Automatizar trabalho mecânico | `scripts/game.py` e testes, no consumidor específico | Tempo ou erro recorrente reduzido; registros antigos legíveis; automação não declara experiência aprovada |

No template MDA atual, a experiência começa obrigatoriamente na “porta” e a dinâmica
“depois do avanço”. Esses detalhes de um starter devem virar exemplo contextual.
A hipótese pode tratar de negociação entre jogadores, de uma cena narrativa ou de
um momento posterior da partida. Remover a prescrição universal preserva a revisão
da primeira experiência quando ela for o objeto do teste.

## Registro de investigação, quando necessário

Na rodada cotidiana, a memória concisa do exemplo de horta basta para orientar a
continuação: intenção, mudança, reação e próximo passo, com hipótese identificada.
Os itens abaixo são perguntas de trabalho do agente para uma investigação mais
substancial. Selecionar o que a decisão exige e registrar no MDA/GDD/QA existente;
não criar outra ficha, nem exigir que o criador preencha oito campos para prosseguir.

1. **Intenção:** quem joga, em qual situação, e o que deve perceber e sentir.
2. **Modelo:** qual mudança de design deve gerar qual dinâmica, por quais razões.
3. **Alternativa e risco:** outra causa plausível; consequência indesejada e piso a preservar.
4. **Prova:** comportamento observável, experiência a investigar e critério que mudará a decisão.
5. **Método:** descoberta, RITE ou comparação; cenário, exposição, participantes e parada.
6. **Identidade:** hipótese → versão da condição → sessão → observação/medida → decisão.
7. **Resultado:** previsto, observado, relatado e interpretado em campos distinguíveis.
8. **Decisão:** manter, ajustar, reformular ou investigar; evidência pendente e próximo recorte.

Para variáveis numéricas, declarar unidade, denominador e janela temporal. “72%
esquivaram tarde” precisa informar 72% de quais jogadores ou tentativas, em qual
versão, depois de quanto treino. Tentativas da mesma pessoa não são participantes
independentes. Em multiplayer, considerar também o agrupamento por partida/equipe.

O registro deve conservar resultados que sustentam a hipótese e descobertas
inesperadas, além de defeitos. O formato atual “problema, evidência, hipótese,
medição” continua útil para problemas; não inventar um problema para registrar
uma experiência bem-sucedida ou inconclusiva.

## Escolher o método pela decisão

| Pergunta | Método proposto | Limite da conclusão |
| --- | --- | --- |
| O jogador entende o verbo e consegue agir? | Observação e perguntas abertas; inspeção prévia do trecho | Descobre obstáculos nas condições observadas |
| A causa e uma correção pequena estão claras? | RITE: registrar sessão, alterar, identificar novo build, retestar | Aprende e verifica correções; não estima efeito causal entre grupos equivalentes |
| A experiência pretendida apareceu? | Observação + relato; PXI quando a mensuração justificar o esforço | Medição subjetiva depende de contexto, versão e instrumento |
| Queremos uma leitura breve e exploratória? | miniPXI completo quando adequado | Evitar concluir melhoria pequena a partir de um item isolado |
| Escolhas parecem livres? O desafio produz competência ou frustração? | BANGS; PENS quando houver razão de comparabilidade e versão apropriada | Construto motivacional não explica sozinho o comportamento nem a retenção |
| Queremos avaliar satisfação ampla? | Considerar GUESS-18, sem empilhar com todos os anteriores | Não substitui diagnóstico específico; [fonte de validação](https://research.google/pubs/validation-of-the-guess-18-a-short-version-of-the-game-user-experience-satisfaction-scale-guess/) |
| A mudança causou uma melhora? | Comparação controlada, alocação adequada, desfecho e análise definidos antes | Depende de amostra, desenho e integridade das condições |

RITE não exige alterar durante a sessão. Preservar a sessão registrada e trocar
o build antes da seguinte. Causa ambígua pede investigação; ajuda do moderador
ou defeito no roteiro pede revisão do teste. No método controlado, definir a
alocação e tratar ordem/treino quando a mesma pessoa jogar ambas as variantes.
Uma descoberta que exija mudança encerra aquela comparação ou inicia novo estudo.

A regra “N sessões sem mudança necessária” é uma opção para descoberta/verificação.
Para teste quantitativo, definir amostra por efeito relevante, variabilidade e
desenho; usar plano de análise e parada apropriados. Não converter seis pessoas,
cem respostas ou ausência de diferença significativa em garantia de conclusão.

## Modelos de dinâmica que merecem entrar no repertório

O ganho específico do corpus MDA é ensinar o agente a prever e explicar, além de
preencher “mecânica → dinâmica → sensação”. Usar o modelo pertinente à hipótese:

| Modelo | Pergunta que resolve | Contraprova ou limite |
| --- | --- | --- |
| Feedback de vantagem | Vencer facilita vencer de novo? Existe recuperação efetiva? | Jogadores mudam estratégia; aproximação de pontuação não prova disputa interessante |
| Estoque e fluxo de recursos | A escassez altera decisões? O recurso acaba e a partida termina? | Premissas de consumo/reposição podem falhar no uso real |
| Probabilidade e variabilidade | Uma recompensa tem média aceitável, mas sequências frustrantes? | Distribuição matemática não mede justiça percebida |
| Informação e coordenação | O que cada pessoa sabe e precisa comunicar para cooperar? | Dependência pode gerar espera, exclusão ou uma pessoa comandando todas |
| Incerteza e resolução | Há tensão com progresso perceptível até o desfecho? | Duração, dificuldade e tensão emocional não são equivalentes |

Os três primeiros e o modelo de drama aparecem nos materiais dos autores; a
aplicação de informação/coordenação aqui é síntese para o nosso processo.
Simulações verificam consequências das regras sob suas premissas; pessoas verificam
se essas consequências sustentam a experiência. Para balanceamento mais amplo,
modelos, telemetria e estratificação por habilidade continuam necessários.

Narrativa e aprendizado podem pedir outras lentes: DDE para explicitar superfícies
de design, DPE para separar objetivos de aprendizado e experiência. Aprendizado
exige prova própria; satisfação com um jogo educacional não demonstra aprendizagem.
[DPE de Winn, corpus local](../../../games-workspace/docs/_anexos/mda-framework/runs/mda-framework-20260912-e0/raw/winn-dpe-chapter/derived/winn-dpe.txt).

## Exemplo: antecipação de um ataque

Exemplo hipotético, sem execução ou associação a um jogo do catálogo.

Intenção: tensão e domínio crescente ao reconhecer um ataque. Variável candidata:
duração da antecipação visual. Dinâmica esperada: reconhecimento seguido de
esquiva deliberada. Risco: o ataque deixar de exigir aprendizado ou perder impacto.

Se muitas esquivas começam tarde, ainda há causas concorrentes: sinal pouco
visível, regra mal compreendida, decisão tardia, atraso de input, animação ou janela
de invulnerabilidade. Primeiro observar a sequência e medir seus eventos reais;
não assumir que aumentar a janela resolve a causa.

Uma comparação posterior pode variar só a duração da antecipação, preservando
arte, áudio, câmera, dano e comportamento do ataque. Relacionar sinais de
reconhecimento, momento do input, execução, resultado e evolução entre tentativas
com o relato de desafio e domínio. Qualquer instrumento escolhido mantém sua
forma identificada. Aumento de sucesso sem domínio percebido pode pedir nova
hipótese. Melhoria medida não autoriza degradar o acabamento aprovado.

## Harness fino e validação da adoção

O primeiro piloto deve testar **a condução de uma pessoa desde uma ideia simples
até uma primeira melhoria**, incluindo acesso ao jogo e continuidade. Uma execução
do agente verifica se as instruções são executáveis; uma pessoa sem experiência
permite observar onde a orientação ainda exige conhecimento que ela não tem. Uma
coisa não substitui a outra. A revisão inicial só executou ferramentas isoladas;
a revisão 4 acrescentou o piloto simulado registrado acima.

Selecionar o projeto na execução, respeitando autorização e direção existentes.
O piloto simulado ficou isolado em `prototypes/meteor-dodge-pilot`, sem varrer ou
alterar jogos do catálogo. Se houver convite a participantes humanos, resolver
autorização para contato e dados antes do recrutamento.

Aceites observáveis do piloto:

- A pessoa descreve uma ideia sem precisar escolher comando ou conhecer game design.
- O agente explica uma situação jogável concreta e implementa a ação correspondente;
  trocar o título de um starter não encerra essa etapa.
- O acesso é verificado e a instrução permite começar, agir e recomeçar no dispositivo usado.
- A pessoa recebe algo curto para experimentar e pode comentar livremente; o agente
  não preenche como observação humana o que só verificou por código ou simulação.
- A próxima recomendação responde ao relato e à intenção, incluindo investigação
  quando a causa é incerta; uma sugestão genérica do CLI não decide a prioridade.
- Ao retomar, o agente conserva decisões e trabalho existentes sem repetir a entrevista.
- Escopo pequeno preserva o piso audiovisual; apreciação artística humana continua explícita.

Registrar tempo de preparação até acesso verificado, bloqueios encontrados,
decisões técnicas desnecessárias transferidas à pessoa e se a reação levou a uma
mudança pertinente. Usar notas e recibos existentes, sem construir analytics.
Não prometer um tempo universal até um jogo satisfatório: o escopo e o ambiente
mudam o esforço. Um piloto mostra viabilidade e atritos, não superioridade causal
do framework nem compreensão garantida para todos os iniciantes.

Na revisão das instruções, conferir casos concretos: ideia vaga, direção já aceita,
jogo existente com um problema específico, impossibilidade de abrir o jogo,
reação ambígua e retomada. Preservar testes de regressão existentes e rodar os
pertinentes aos arquivos alterados. Novos testes devem verificar comportamento
necessário, sem apenas exigir frases nos documentos. Os seletores que hoje dependem
de frases exatas merecem atenção nos consumidores afetados, não uma reescrita geral.

Quando um projeto realmente precisar de investigação mais estruturada, `record`
já aceita campos e anexos. Ligar evidência ao build/configuração efetivamente jogados:
HEAD sozinho não identifica alterações não commitadas ou assets. Separar observação,
relato, interpretação, simulação e mensuração; identificar instrumentos adaptados
e não chamar de A/B uma sequência com mudanças entre sessões. Telemetria ou novos
schemas só entram se o uso mostrar uma lacuna que os registros atuais não resolvem.

**Próximo recorte humano, ainda pendente após o piloto simulado:** percorrer a jornada com uma pessoa
sem experiência, desde uma ideia até uma primeira melhoria, usando as instruções
atualizadas. Preservar o pedido, ações e resultado reais; corrigir a primeira
fricção material demonstrada no consumidor existente. Não começar pela ficha de
experimento ou pelo questionário. Nenhum gate novo ou eficácia do processo foi
declarado nesta entrega.
