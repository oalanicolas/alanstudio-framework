# Adoção — Alan Studios Framework

Histórico das versões 0.1–0.9. Recibos brutos de execução e o acervo sonoro
ficam no laboratório; aqui permanece o que a versão afirma e o que ela não afirma.

## 0.9 — Começar e acabar

Duas lacunas entre o que o framework prometia e o que entregava.

**Começar.** Até 0.8 o harness sabia ler um jogo existente e não sabia criar um.
`doctor` observa ambiente, integridade e os atalhos de skill do host — vigente,
desatualizado, ausente — sem escrever nada. `init` monta um projeto a partir de um
starter do acervo, troca os valores que o `starter.json` dele declara e gera como
rascunho declarado os sete documentos que cobrem as áreas mínimas; não instala
dependências e não toca no starter de origem. Um starter carrega valores reais em
vez de marcadores porque ele é referência executável: serve e abre antes de
qualquer `init`.
`next` deriva uma proposta ordenada do estado no disco. `--root` passa a ser
aceito antes e depois do subcomando, como a documentação já afirmava.

**Acabar.** A [barra de acabamento](references/production-bar.md) nomeia cinco
degraus em dez dimensões de ofício, com a observação que sustenta cada degrau, e
chega em todo `context` pelo campo `production_bar`. Seis receitas novas — feel,
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
