# Checklist de piso de acabamento

Instrumento de observação da **fatia**, não certificado e não nota. Completar
linhas não torna o jogo AAA de publisher e não mede diversão. “AAA” aqui é o
[piso](ambition.md): verbo, feel sincronizado, mix, pacing, mundo, confiança
e repeatability.

O harness não preenche o checklist. Ele recorta **quais grupos valem**
(`finish` no `context`) e aponta esta guia. O agente observa o recorte
real e escreve no canônico do jogo — um documento combinado basta.

Template: [aaa](../assets/templates/aaa.md).
`context --stage aaa` imprime o rascunho inteiro. Slice, QA, `feel` e
`audio` já carregam **esta guia**; não geram arquivo novo.

## Como se adapta ao framework

O checklist não é um ciclo paralelo. Ele **observa** o que as outras
peças já decidem ou implementam.

| Peça do harness | O que o checklist faz |
| --- | --- |
| Brief / escala | Escolhe o perfil: jam = só **núcleo**; produto/AA soma **produto**; o que não foi prometido fica em **promessa** ou `N/A` |
| GDD / MDA | CHK-1 (verbo, escolha, recusa). Origem típica: GDD-M01 |
| `--focus feel` / `--focus audio` | CHK-4 e CHK-5; a guia entra no `read_next` |
| `--focus lifecycle` | CHK-11 (pause, reset, descarte) |
| `--focus visual` / Art Bible | CHK-7 e CHK-8; hero comparison no engine |
| `--focus content` | CHK-10 (receita, pipeline, custo) |
| `--focus network` | CHK-12 só se houver estado compartilhado |
| `--focus architecture` / TDD | Contratos que CHK-6 e CHK-11 precisam provar |
| `--stage vertical-slice` | Fecha o núcleo (+ produto, se a escala pedir) **antes** de ampliar |
| `--stage qa` | Evidência: CHK-14 liga IDs a casos e playtest |
| `verify` | Recibo técnico; `experience_status` continua `not_assessed` até movimento |
| Scan / nove áreas | Um arquivo de checklist é candidato de **QA**, não uma décima área |

Não invente rede, live ops, mocap ou locale para “completar o AAA”.
Isso já é regra da [auditoria](project-audit.md).

## Três perfis (não três notas)

O objeto `finish` do `context` lista os grupos. O agente não decora a tabela.

| Perfil | Grupos | Quando |
| --- | --- | --- |
| **Núcleo** | CHK-0, CHK-1, CHK-2, CHK-4, CHK-5, CHK-6, CHK-11 | Qualquer escala, assim que existir um ciclo jogável |
| **Produto** | CHK-3, CHK-7, CHK-8, CHK-10, CHK-14, CHK-15 | Escala produto ou AA / Triple-I; ou jam que prometeu câmera/mundo/HUD |
| **Promessa** | CHK-9, CHK-12, CHK-13 | Só se o recorte prometeu narrativa/voz, rede ou outro idioma |
| **Mercado** | CHK-16 | Contexto. **Nunca** reprova jam nem AA. Começa `N/A` |

Jam: observe o núcleo; marque produto/promessa/mercado como `N/A` com a
escala. Primeira sessão: **não** abra o template — construa o ciclo.
Produto/AA: núcleo + produto, e as promessas declaradas no brief, **na
slice**, antes de multiplicar conteúdo.

`finish.action` no JSON:

- `defer_until_playable_cycle` — ainda não há o que observar.
- `observe_core_on_slice` — feche o núcleo (e o perfil da escala) neste recorte.

## Estados

| Estado | Significa |
| --- | --- |
| `não executado` | Ainda não observado neste recorte. |
| `observado` | Evidência em movimento (ou comando, se o item for técnico) e um autor. |
| `inconclusivo` | Observou-se; a evidência não distingue a hipótese. |
| `N/A` | O recorte ou a escala declara que não se aplica; o motivo é obrigatório. |

Screenshot isolada não fecha feel, animação, câmera, mix nem pacing.
Com tela, a primeira superfície é a porta; o campo começa depois do avanço.
Avaliação do agente ≠ aprovação do usuário. Não some linhas. Um vermelho
**material do perfil em vigor** bloqueia o adjetivo; verde noutro eixo
não compensa.

## Falhas típicas do agente

- Gerar `template aaa` na primeira sessão e chamar o rascunho de progresso.
- Preencher 70 linhas de um jam em vez do núcleo.
- Marcar `observado` com still, typecheck ou opinião.
- Inventar CHK-12/13/16 para o scanner ficar verde.
- Usar “quase AAA” com núcleo em `não executado`.
- Tratar CHK-16 (orçamento, live ops, BVT) como piso de acabamento.
- Criar `aaa.md` paralelo quando a slice ou o QA já têm as linhas.

## O que o checklist não pede

Orçamento de US$ 100 mi, equipe de 200, marketing de blockbuster, live ops,
microtransação, ray tracing, celebridade na voz e AAAA **não** são piso.
Se o projeto for desse tier, CHK-16 registra o fato — nunca a condição
para o acabamento.

## Continuidade

- **Onde estamos:** o template existia como etapa solta; o agente só o via
  com `--stage aaa`.
- **Próximo passo:** na slice ou em “está AAA?”, observar o perfil que o
  `finish` indicar e gravar no canônico.
- **Por que agora:** sem perfil e sem carga na slice/QA, o checklist não
  pertence ao framework — é um anexo.
- **Pronto quando:** o núcleo do recorte tem estado ou `N/A`; o resumo
  nomeia o que ainda impede o adjetivo; a próxima ação é uma.
- **Retomar por:** `finish` no `context`, este guia, a slice e o QA do jogo.
