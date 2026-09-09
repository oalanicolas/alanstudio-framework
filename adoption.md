# Adoção — Alan Studios Framework

Histórico das versões 0.1–0.9. Recibos brutos de execução e o acervo sonoro
ficam no laboratório; aqui permanece o que a versão afirma e o que ela não afirma.

## 0.9 — Começar e acabar

Quatro lacunas entre o que o framework prometia e o que entregava.

**Recusar.** A barra descreve onde o jogo está e nada dizia o que não pode
passar. Os dez [gates](references/gates.md) formalizam as linhas “Pronto para…”
que já estavam no ciclo criativo — 38 critérios extraídos da prosa, não
inventados, com um teste exigindo que cada gate continue apontando para a linha
de origem. O projeto declara `met`/`unmet`/`waived`/`out_of_scope` por critério
com o que sustenta o estado, e `gate` lê. Critério sem linha é pendente: silêncio
não é aprovação. As três saídas são passar, cortar escopo e **abandonar** — a
terceira o ciclo já tinha na etapa `poc`, e passou a valer nas dez. Dispensa exige
motivo escrito; quatro critérios não se dispensam, porque a prosa da etapa não
deixa terceira opção. `granted` é sempre falso.

Depois, um [levantamento de fontes](references/gates-research.md) mostrou duas
coisas que faltavam. Os dez gates perguntavam só “o trabalho está feito?”, e a
pergunta de valor — “isto ainda vale o que custa?” — existia apenas como a saída
`abandonar`, dependendo de alguém levantá-la: agora três critérios a fazem, e
`next` a coloca antes de pedir mais trabalho no mesmo gate. E um critério que
nunca incidiu só podia virar dispensa, inflando a conta que existe para doer:
`out_of_scope` é estado separado, com motivo escrito e recusado onde o critério
sempre incide.

**Chegar.** O laboratório onde este harness roda normalmente já tem jogos, e o
primeiro movimento nele é revisar o que existe. `discover` devolvia caminho e
tipo, o que faz jogos em estados incomparáveis saírem iguais; agora ele lê cada
projeto e devolve áreas mínimas com candidato, rascunhos, passo registrado para
retomar, piso de acabamento declarado e validadores — com `--plain` para a
listagem crua. A ordem é a do disco, e o harness não classifica os jogos por
urgência, porque nada nele observa qual importa mais. `doctor` passou a nomear os
projetos que contou, em vez de só contá-los.

**Começar.** Até 0.8 o harness sabia ler um jogo existente e não sabia criar um.
`doctor` observa ambiente, integridade e os atalhos de skill do host — vigente,
desatualizado, ausente, comparados por conteúdo, com symlink para o `SKILL.md`
vigente contando como vigente — sem escrever nada. `init` monta um projeto a partir
de um starter do acervo, troca os valores que o `starter.json` dele declara e gera
como rascunho declarado sete documentos, que cobrem sete das nove áreas mínimas
(as outras duas ficam com o README e o CREDITS do starter); não instala
dependências e não toca no starter de origem. Um starter carrega valores reais em
vez de marcadores porque ele é referência executável: serve e abre antes de
qualquer `init`.
`next` deriva uma proposta ordenada do estado no disco. `--root` passa a ser
aceito antes e depois do subcomando, como a documentação já afirmava.

**Acabar.** A [barra de acabamento](references/production-bar.md) nomeia cinco
degraus em dez dimensões de ofício, com a observação que sustenta cada degrau, e
chega em todo `context` pelo campo `production_bar`. `bar <projeto>` lê a tabela
de degraus que o projeto declara nos próprios documentos e devolve o piso, as
dimensões que estão nele e — só quando as dez tiverem linha — o degrau percebido;
com isso `next` propõe subir a dimensão mais baixa pelo nome, citando o critério
escrito e a linha de onde veio. O harness confere a forma da declaração — e
relata em `problems` dimensão fora das dez, degrau fora dos cinco e alvo que não
é o seguinte — nunca o jogo: tabela bem formada e otimista sai de lá intacta.
Seis receitas novas — feel,
performance, acessibilidade, áudio, persistência, release — e a etapa `release`
fecham o ciclo. O starter `canvas-arcade` existe para que o passo REUSE tenha um
candidato real: loop de passo fixo, RNG semeado, save versionado com migração,
mixer com legendas e um contrato de ciclo de vida exercitado por testes headless,
em vez de apenas mencionado.

**Alegação com recibo.** `context` lê arquivos e por isso só sabe dizer
`mentioned` sobre as oito capacidades conhecidas. `verify --proves <capacidade>`
**não** as promove a verificadas — o harness não sabe se um comando exercita
pause. O que ele acrescenta é uma alegação com autor, data, argv e log: `claimed`
com recibo verde, `unsupported` quando a execução falha. A afirmação deixa de sumir
na prosa e passa a ser contestável. Nenhum arquivo do repositório seleciona
capacidade.

A escada quase não cita número, e isso era decisão sem justificativa escrita. Um
[levantamento](references/observable-criteria-research.md) foi buscar os limiares
que se poderia importar e achou o oposto do esperado: o safe title que todo mundo
usa foi substituído em 2009, o “100 ms” de latência vem de um artigo de 1968 sobre
teclas de terminal que já se contradiz no próprio parágrafo, e o “cinco usuários”
de playtest sai de um artigo que conclui dezesseis. Nenhum limiar entrou; o que
entrou foi um mapa de onde existe norma, onde existe página de fornecedor e onde
não existe fonte — e uma regra de parada de playtest, que substitui a pergunta
“quantas pessoas?” por “o que encerra a rodada?”. Um teste novo mantém os
cinquenta critérios da barra livres de dígito.

O que 0.9 **não** afirma: nenhum comando atribui um degrau da barra, e a escada não
foi calibrada contra uma amostra de jogos publicados — é linguagem para observar,
não aferição. `init` cria rascunho, e rascunho não é decisão documentada. `next`
propõe e nunca executa. Os testes do starter provam o starter, não um jogo derivado
dele. AAA continua descrevendo orçamento e equipe; o que este repositório persegue
é acabamento por dimensão em escopo reduzido.

## 0.8 — Arquitetura proporcional

Receita [architecture](recipes/architecture.md). `--focus architecture` e
`--stage tdd` selecionam essa receita. A skill aplica análise proporcional
quando a mudança afeta contratos, responsabilidades ou sistemas. O CLI não
infere dependências nem aprova decisões.

## 0.7 — Continuidade e retomada

`--event resume` localiza fontes de continuidade. A entrega deve situar o
avanço e uma próxima ação, motivo e prova. O harness deixa `next_step: null`;
o agente resolve o passo.

## 0.6 — Aprovação de direção

`--event direction-approved` sincroniza a base mínima no mesmo turno, mesmo
com todos os candidatos encontrados. Salvar a imagem e listar entregas não
basta.

## 0.5 — Documentar o mínimo sem segundo pedido

Se a checagem deixar lacunas, o agente avisa e documenta. Restrição explícita
na conversa continua valendo. O scanner permanece somente leitura.

## 0.4 — Scan e foundation

`context` sempre inclui `scan`. Nove áreas, candidatos, lacunas e limites.
`candidate_found` não certifica suficiência. Templates complementares:
Art Bible, Devlog, Auditoria.

## 0.3 — Contexto por foco com estudos e menções locais

`context` lista catálogos do foco quando o irmão de estudos existe, e registra
menções de pause, reset, seed e demais capacidades em um conjunto fechado de
arquivos locais. Nenhuma menção vira `verified`.

## 0.2 — Pré-produção e ciclo criativo

Nove templates sob demanda. `context --stage` e `template` selecionam um
artefato. Nenhuma etapa é aprovada pelo comando.

## 0.1 — Entrega inicial

Descobrir projetos, recortar contexto, validar a forma do contrato de reuso e
executar comandos escolhidos com recibo.

## Limites que continuam valendo

Build verde não comprova diversão, arte, reinício, rede, direitos de assets nem
aprovação humana. Troca de modelo com qualidade equivalente continua hipótese a
testar. Os oito frameworks externos foram estudados em recortes; seus testes
não foram executados neste repositório. Este extrato não inclui evidência JSON
nem a biblioteca `shared/sfx`.
