# Arquitetura orientada à experiência

Entrada: mudança que afeta responsabilidades, contratos, estado, tempo, saves,
conteúdo, renderização ou integrações. Use também ao escolher tecnologia ou preparar
um TDD. O agente identifica essa necessidade na tarefa; o usuário não precisa pedir
“ative o arquiteto”. `context --focus architecture` seleciona esta receita;
`--stage tdd` também a inclui, preservando o foco escolhido.

Saída: decisão suficiente para implementar e verificar **o recorte autorizado**,
registrada no TDD/decisions/plano já adotado. Um ADR separado só quando for a convenção
do projeto ou quando a decisão precisar de histórico próprio. A receita orienta o
agente; o harness não infere dependências, escolhe arquitetura nem aprova decisões. Se a receita recusa que o harness infira dependências, o `scan` nomeia as dependências que a receita já recusa. Receita no disco não é decisão. Sem chave `dependências`.

## 1. Dimensionar a análise

Comece pelo cenário: **ação do jogador → mudança de estado → consequência percebida**.
Com tela, a primeira ação deste starter é abrir a porta. `hold` é o
tick interrompido; Continuar é repetir a seed. `?seed=` e `?spawn=`
nomeiam a partida — não são estado observado.
Ligue-o ao GDD/MDA, ao aceite e à referência aprovada. Reconstrua lacunas com o
[roteiro de auditoria](../references/project-audit.md), avisando e documentando.
Separe comportamento atual observado, direção aprovada, proposta e desconhecido.

Descubra as decisões vigentes que governam o recorte e confira seus caminhos e estado
atual; não fixe uma lista de ADRs no prompt. A fonte canônica orienta a mudança.
Contradição entre documento, código e direção atual pede registrar e resolver a
divergência, sem promover histórico a regra vigente nem inventar aprovação. Uma nova
direção explícita do usuário pode revisar uma decisão anterior. Se a receita recusa promover histórico a regra vigente, o `scan` nomeia o histórico que a receita já recusa. Área no disco não é decisão atual. Sem chave `histórico`.

- **Alteração localizada, contrato preservado e resultado conhecido:** leitura do
  caminho/consumidor afetado, decisão curta e prova correspondente no registro atual.
- **Mudança atravessa sistemas, formato persistente ou responsabilidade compartilhada:**
  mapear impacto e alternativas; adaptar a seção pertinente do TDD antes da integração.
- **Incerteza pode invalidar a experiência, perder progresso ou exigir retrabalho amplo:**
  primeiro uma PoC com hipótese, contraprova e limite de esforço; resultado inconclusivo
  permanece inconclusivo. A decisão de produção depende dessa evidência.

Julgue alcance nos consumidores, novidade, reversibilidade e consequência para o
jogador. Um único risco crítico pode determinar a profundidade; contagem de arquivos,
média de scores e prazo fixo não substituem esse julgamento. Uma PoC exploratória
não precisa esperar uma arquitetura completa.

## 2. Montar contexto da mudança

Reaproveite o [mapa de reuso](../references/process.md#2-reuse--adapt--create). Leia
fontes e consumidores; anote caminho/símbolo e **por que cada um importa**:

- Entrada real e cenário de reprodução; versão/configuração pertinente.
- Fonte canônica a modificar e responsáveis pelo estado; chamadas que a consomem.
- Exemplares existentes, com o padrão útil e o limite de adaptação.
- Dependências, assets/formatos e testes afetados; comandos realmente disponíveis.
- Restrições e lacunas capazes de mudar a decisão, com a próxima investigação.

Use os catálogos, manifestos e registros que já existem para localizar candidatos.
Confirme suas capacidades no consumidor; registro declarado não prova suporte real. Se a receita recusa que o registro declarado prove suporte real, o `capabilities[n]` do `verify` nomeia o suporte que a receita já recusa. Registro no disco não é o consumidor. Sem chave `suporte`.

Use o registro atual, sem gerar cópias de todo o contexto do projeto. Busca por nome,
import ou marcador produz candidatos. Resolva aliases, conteúdo serializado, eventos,
cenas e carregamento dinâmico pertinentes antes de declarar a cobertura. Se parte não
foi lida, explicite-a; “contexto carregado” não significa “arquitetura compreendida”.

## 3. Rastrear impacto e contratos

Siga a mudança **da entrada até o efeito percebido e de volta aos consumidores**.
Para cada responsabilidade afetada, registre quem lê/escreve, contrato e regressão
possível. Examine apenas os eixos pertinentes:

- **Regra/estado/tempo:** invariantes, ordem das atualizações, pausa/reinício, RNG
  quando existente. Quem possui o relógio e qual estado a apresentação pode alterar?
- **Persistência/conteúdo:** identidade, versões, loading e saves atuais; o que acontece
  com progresso existente e se é possível recuperar o estado anterior após uma mudança.
- **Apresentação/recursos:** input, câmera, UI, áudio, feel do verbo, carregamento
  e descarte de GPU, timers/listeners. Contrato lógico correto ainda pode produzir
  regressão perceptível; feel e mix têm receitas próprias.
- **Rede/serviços, quando presentes:** autoridade, ações recusadas, desconexão e limites
  externos. Exemplares locais não comprovam comportamento multiplayer.

Confirme também o ambiente em que a prova vale: editor versus build/export, plataforma,
entrada e configuração alvo. Um teste no editor ou em mock não demonstra o jogo exportado.

Registre também o que ficou fora do recorte e por quê. Um grafo lexical vazio não
prova ausência de consumidores. Formatos e sistemas universais só entram após uma
lacuna demonstrada em consumidores reais. Prefira as fronteiras que o jogo já possui.

O erro tem duas direções, e a frase acima só cobre uma. Construir o sistema geral
cedo desperdiça o esforço; continuar improvisando depois que as cópias se
acumularam desperdiça mais, e de forma silenciosa. Nenhuma regra decide isso por
você — a decisão depende de quanto conteúdo o jogo vai ter, e no começo isso é
estimativa. O que dá para fazer é **declarar a estimativa em vez de a manter na
cabeça**: escreva no TDD a contagem a partir da qual o sistema passa a valer a
pena (“acima de N falas, um sistema de diálogo; abaixo, texto no lugar”), com a
data e quem estimou. Quando a contagem real cruzar a linha, a decisão já está
tomada e datada, em vez de ser adiada por inércia. Estimativa declarada e errada
é revisável; estimativa implícita não é nem discutível.

### Edição estruturada e convivência com código

Quando humano ou agente alteram parâmetros, objetos ou cenas, declare a identidade do
alvo e a revisão a que a operação se aplica. Tipo, unidade, faixa e relações entre
campos precisam de validação no consumidor; um slider ou schema descritivo não impede
uma chamada direta inválida. Reuse o formato e o executor atuais antes de criar outro.

Separe definição autoral, alterações aplicadas, versão em prévia e estado da partida.
Uma alteração rejeitada preserva a versão válida. Uma aceita declara o que muda e o
que permanece: alvo, objetos não selecionados, referências, saves e acabamento.
Se código regenerado mudar identidade, geometria ou schema, detectar incompatibilidade
é preferível a reaplicar silenciosamente uma alteração sobre outro alvo.

Prove uma edição válida, uma incompatível/obsoleta e a recuperação; confira o consumidor
e o cenário percebido. Recuperar a cena não implica recuperar contadores ou progresso.
Humano e agente podem compartilhar operações quando os contratos coincidirem; isso
não exige uma engine comum nem elimina uma saída para código. Ganho de produtividade
é hipótese até comparar pedidos inéditos, incluindo preparação, falhas e regressões.
Origem e limites: [autoria UGC pública](../references/sources.md#autoria-ugc-pública).

## 4. Decidir com alternativas e contraprova

No [TDD existente](../assets/templates/tdd.md), reúna: problema e requisito de origem,
alternativas examinadas, **REUSE → ADAPT → CREATE**, escolha, contrato e consequências.
Considere manter o estado atual quando isso for uma alternativa real. CREATE exige
lacuna explícita; comparar alternativas não exige criar implementações de todas elas.

Registre a condição que faria abandonar ou revisar a escolha e o custo de desfazê-la.
Para dados persistentes, distinguir reverter código de recuperar dados já transformados.
Uma revisão não aprova migração destrutiva ou publicação por si só.

Avalie dependências, licença, manutenção e recursos com base em fontes. Meça eficiência
em condições equivalentes preservando o acabamento: a qualidade visual aprovada é o
piso. Economia de recursos não compensa regressão visual ou de jogabilidade.

## 5. Preparar a primeira fatia e revisar

Cada tarefa necessária tem **ação + alvo + propósito**, fontes a alterar/reaproveitar,
dependência real, resultado observável e prova. Ordene pela dependência e pela maior
incerteza; uma fatia de jogo pode atravessar regra, apresentação e conteúdo. O tamanho
é o menor resultado demonstrável, sem limite universal de arquivos ou ordem web fixa.

Distinga **dependência de ordem/decisão** de **consumo de artefato**. Se a tarefa precisa
de código, asset ou dados produzidos antes, registre caminho/versão e confira sua
disponibilidade e adequação. Duas tarefas tocarem o mesmo arquivo é conflito de edição,
não prova de dependência lógica. Não invente dependências para preencher um plano.

Antes de implementar, confronte:

1. Cada requisito do recorte tem uma decisão ou uma PoC que resolve sua incerteza?
2. A pessoa/agente seguinte encontra o caminho real, o padrão e o consumidor afetado?
3. Contratos definem dono do estado, invariantes e comportamento de falha pertinente?
4. Há caso capaz de refutar a hipótese e detectar a regressão no consumidor real?
5. A primeira tarefa tem entrada disponível e prova adequada? Se faltar prova,
   obtenha observabilidade ou faça a PoC; typecheck/build isolados não fecham gameplay.

Revise criticamente com evidência; registre autor e limites, sem presumir revisão
independente. Respeite autorizações existentes e pergunte só por decisão indispensável
que continue ambígua. Aplique a [qualidade](../references/quality.md) conforme a mudança.

## 6. Atualizar e continuar

Ao implementar ou refutar uma hipótese, atualize as decisões/requisitos/QA afetados e
aponte quais evidências precisam ser refeitas. Preserve o histórico e os IDs; uma
mudança de prioridade não exige reauditar documentos ainda válidos.

Siga a [continuidade](../references/process.md#continuidade-e-retomada): onde estamos,
uma próxima ação, por que agora, pronto quando e retomar por. Confira resultado real,
inclusive falha, rejeição ou trabalho de outra sessão, antes de avançar. Nome de
comando, arquivo existente ou fase salva não comprovam conclusão nem aprovação.
Execute o que ainda pertence ao pedido; apresente o próximo passo do projeto quando
o escopo desta entrega terminar.

Origem: estudo interno do Architect AIOX (sete rastros, limites no laboratório).
Adaptação local do processo; runtime e hierarquia AIOX não são dependências.
