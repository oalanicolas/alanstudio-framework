> Registro histórico da linha do PR #3 antes da integração. Para o estado combinado, veja [HANDOFF.md](HANDOFF.md).

# Handoff — branch `cursor/framework-0-9-facil-e-aaa-1083`

Quem continua daqui não precisa da conversa. Este arquivo diz o que a branch
entrega, o que ela recusou afirmar, e o que ainda está aberto. A conversa
serviu para chegar aqui; a autoridade é o disco.

- Branch: `cursor/framework-0-9-facil-e-aaa-1083` (32 commits à frente de `main`)
- Base: `main` (framework 0.8)
- PR: https://github.com/oalanicolas/alanstudio-framework/pull/3 — **ainda em draft**
- HEAD no momento deste texto: o commit que adiciona este arquivo, acima de `fc2e48a`
- Testes no momento deste texto: `python3 -m unittest discover -s tests` → 154 OK;
  `cd assets/starters/canvas-arcade && npm test` → 83/83

O objetivo que abriu o trabalho: revisar o harness, reduzir atrito, nomear o
que separa protótipo de acabamento AAA, implementar com testes, e não prometer
o que o harness não verifica. Quatro pedidos do usuário mudaram a ordem:

1. Revisar e melhorar o framework para criar jogos com IA com qualidade AAA.
2. *“Dentro do local que ele vai ser usado normalmente já tem jogos por isso
   ele revisa o que tem.”*
3. *“Estude materiais como esses para podermos criarmos mais gates, workflows,
   checklists”* — com um vídeo de YouTube.
4. Este handoff.

## O que a 0.9 entrega de fato

Quatro lacunas entre a promessa de 0.8 e o que o harness fazia. Cada uma tem
comando e teste.

### Chegar — o laboratório já tem jogos

`discover` deixou de devolver só caminho e tipo. Sem `--plain` ele **revisa**:
áreas mínimas com candidato, rascunhos, documento sem versão vigente, passo
registrado para retomar, piso de acabamento declarado, dimensões sem linha e
validadores. A ordem é a do disco. **O harness não classifica os jogos por
urgência** — nada nele observa qual importa mais, e inventar “mais carente”
seria prioridade sem evidência. `doctor` nomeia os projetos que contou.

### Começar — três comandos

- `doctor` observa ambiente, integridade do `SKILL.md` (conteúdo, inclusive
  symlink vigente) e atalhos da skill. Não escreve. Num `--root` inexistente
  sugere `mkdir -p` com o caminho que falta, inclusive se o pai também falta.
- `init` copia um starter, substitui o que o `starter.json` declara e gera
  sete rascunhos, cobrindo sete das nove áreas mínimas (README e CREDITS do
  starter cobrem as outras duas). Não instala dependências, não toca no
  starter de origem, recusa destino ocupado.
- `next` deriva **uma** proposta do estado no disco e não executa
  (`executed` é sempre `false`).

Ordenação do `next`, e um teste extrai os ramos do fonte e exige cada um no
README: sem destino → sem entrypoint → área não localizada → rascunho →
documento sem versão vigente → continuidade → validadores → linha de gate
malformada → pergunta de valor → critério pendente → linha de degrau
malformada → dimensão sem linha → duas linhas em conflito → subir a dimensão
mais baixa.

### Acabar — a barra que o projeto declara

[references/production-bar.md](references/production-bar.md): cinco degraus
(protótipo, jogável, fatia, publicável, carro-chefe) em dez dimensões. O
degrau percebido é o **mínimo**, não a média. `bar` lê a tabela que o
projeto escreveu. Confere **forma** (dimensão, degrau, alvo imediatamente
seguinte) e relata em `problems`. **Nunca atribui um degrau.** Tabela bem
formada e otimista sai intacta.

Nenhum dos cinquenta critérios da barra cita dígito — teste
`test_no_tier_criterion_smuggles_a_threshold_into_the_bar`. Isso é decisão,
não esquecimento: o levantamento de critérios observáveis mostrou que os
limiares mais repetidos ou estão desatualizados, ou não vêm de jogo, ou não
têm fonte.

### Recusar — dez gates

[references/gates.md](references/gates.md). Cada gate formaliza uma linha
`**Pronto para…**` de [references/preproduction.md](references/preproduction.md).
Nome do que se pede (`design`, `build`, `scale`, `deliver`), não do marco da
indústria — não existe definição canônica desses marcos.

Estados: `met`, `unmet`, `waived`, `out_of_scope`. Quatro critérios da prosa
não se dispensam: `design.reference_origin`, `implement.user_requirements`,
`conclude.human_vs_agent`, `deliver.licensing`. Três são `must_meet` e também
não se dispensam: `close.decision`, `implement.worth_building`,
`scale.worth_scaling`. `granted` é sempre `false`. O campo é
`held_by_declaration`, não `passed`.

`out_of_scope` não é dispensa: um jogo sem save não “dispensa” migração de
save. Sem estado próprio, a conta de dispensas inflava.

### Starter `canvas-arcade`

Loop de passo fixo, RNG semeado, hash de estado, abstração de entrada,
mixagem com legendas, save versionado com gravação **verificada** (não
atômica — `localStorage` não tem rename), alto contraste e redução de
movimento. Abre no lugar, sem `{{TOKEN}}`. HUD com placa **e borda**: a
placa cobria sem se ver (campo e placa quase a mesma cor; em alto contraste,
idênticas). A lição está no README do starter: teste de cobertura
geométrica não é teste de percepção. `legibility` permanece `playable`.

### Receitas e ciclo

Seis receitas novas: `feel`, `performance`, `accessibility`, `audio`,
`persistence`, `release`. Template e etapa `release`.

## Honestidade epistêmica — não reabrir

Onde o repositório dizia mais do que sustentava, ele passou a dizer menos.
Não “consertar” estas frases de volta:

| Dizia | Passou a dizer |
| --- | --- |
| prova as oito capacidades | **exercita**, e `capture` só na guarda de ausência de tela |
| escrita atômica no save | **gravação verificada** |
| `verify` comprova | `verify` **registra** |
| `verify --proves` verifica | grava `claimed`, nunca `verified` |

Padrão de teste desta branch: quando prosa e código discordam, o teste exige
os dois juntos. Não “corrigir a frase e seguir”. Exemplos: todo subcomando
no README; todo ramo do `next` nomeado em português no README; nenhum par de
exemplos compartilha `--output`; todo gate aponta para a prosa de origem;
âncoras internas pelo slug do GitHub.

## Duas pesquisas, e o que delas entrou

Arquivos longos, para consultar, não para reler inteiros:

- [references/gates-research.md](references/gates-research.md) — marcos,
  stage-gate, certificação, acessibilidade como checklist, DoD.
- [references/observable-criteria-research.md](references/observable-criteria-research.md)
  — feel/latência, arte, performance, UI, playtest.

O que **entrou no código ou no processo**:

- Vocabulário de Cooper: `readiness` × `must_meet`. *Should-meet* **não**
  foi implementado — scorecard ordena projetos, e um gate a mais sem função
  é burocracia no sentido do próprio Cooper.
- `out_of_scope` (forma dos XAGs / TRC “Applicable”).
- Regra de parada de playtest (RITE): N sessões consecutivas sem mudança
  necessária, no [roteiro](references/quality.md) e no
  [template de QA](assets/templates/qa.md). Cadeia
  problema / evidência / hipótese / medição (Valve). Sem os quatro, é
  impressão.
- Mapa de três colunas na barra: norma (SMPTE, FCC, WCAG) × guideline de
  fornecedor × número sem fonte.

O que **não** entrou, e não deve entrar sem fonte nova e calibração:

- Qualquer limiar (16 ms, 100 ms, 4,5:1, 93%, “cinco usuários”, orçamento
  de draw call).
- A afirmação de que gates melhoram o jogo. Nenhuma das duas pesquisas
  achou avaliação empírica para jogos. Disciplina explícita é o que se
  sustenta; eficácia comprovada, não. Isso está escrito em `gates.md`.

Três correções de leitura que o próximo agente **não deve desfazer**:

1. Nielsen & Landauer (1993) estimam 16 avaliações, pico em 4; os 85% vêm
   de λ≈0,31 sobre treze conjuntos **sem jogo**. Faulkner: cinco usuários
   acham 55%–99%. Ninguém publicou λ para playtest de jogo.
2. “100 ms” é Miller (1968), tecla de terminal; o próprio parágrafo se
   contradiz. Em jogos a faixa publicada vai de ~15 ms a 1 s.
3. Title safe 90/80 é 1961–63; SMPTE ST 2046-1 (2009) é 93% action / 90%
   title.

Heurística de triagem que sobrou: fonte séria diz de onde tirou o número.
A EBU declara a medição de overscan dos 3,5%; a Unity chama o 35% de
“a general tip”. Número com casa decimal e sem origem é menos honesto, não
mais preciso. O levantamento nomeia domínios de marketing e de texto
gerado por modelo — não citar.

## O que ainda está aberto

Ordenado pelo que mais fecha a lacuna entre promessa e entrega. O objetivo
original **não** está concluído.

### 1. `deliver.licensing` é não-dispensável e ninguém observa o disco

Este era o próximo trabalho quando o pedido de handoff chegou. O harness
recusa dispensar “nenhum recurso embarcado tem licença desconhecida” e
**não percorre o projeto**. `scan` já ignora `textures`, `fonts`, `models`,
`videos`. `sfx copy` escreve `sources.json` e `.credits.txt` no destino, e
para por aí. Um projeto que declara `met` nesse critério com uma frase
otimista passa na forma. Fechar isso é o ganho mais concreto que resta no
harness: um comando (ou um ramo de `gate` / `doctor`) que liste arquivos
embarcados sem recibo de origem, sem inventar que a licença é válida —
só que está **declarada**. Não conceder passagem.

`scripts/audio.py` e `scripts/sfx_catalog.py` quase não foram tocados nesta
branch. Qualquer trabalho de proveniência deveria começar por eles e pelo
que `scan` exclui, não por mais prosa em `gates.md`.

### 2. Checklists observáveis por gate ainda não existem

A pesquisa de craft deixou uma lista do que dá para checar **sem** número
externo ( paleta declarada, constante de perdão num só lugar, percentil
definido pela definição, delta contra o build anterior, regra de parada ).
Nada disso virou critério de gate nem proposta do `next`. Não transformar
isso em limiar importado.

### 3. Duas lacunas de Cooper que `gates.md` já nomeia e não fecha

- Entregáveis fixados na **saída** do gate anterior, para este projeto, em
  vez de só o menu fixo por etapa.
- A coluna de evidência não distingue “log de comando” de “alguém olhou”
  — o asterisco dos XRs da Microsoft.

### 4. Caminho ideia → jogo jogável ainda tem atrito de laboratório

`init` + starter cobrem o projeto novo. O laboratório real tem
`shared/sfx` e jogos vizinhos; o harness os descobre, mas o primeiro
`next` depois do `init` ainda manda documentar áreas (política do
estúdio) antes de jogar o que acabou de nascer. Vale perguntar se
“rascunho gerado pelo `init`” deveria continuar empatado com “área sem
candidato” ou se o próximo passo honesto de um projeto de dez segundos é
`npm test` / `serve`. Houve um conserto parecido: continuidade fantasma
a partir do texto do template. O mesmo modo de falha pode estar no
`areas.draft_only`.

### 5. A barra não foi calibrada

Nenhum degrau foi confrontado com uma amostra de jogos publicados. Sem
isso, “AAA” continua sendo vocabulário de acabamento em escopo reduzido,
não aferição. Calibrar é trabalho de evidência, não de mais critério.

### 6. O starter não é o jogo do laboratório

Os 83 testes provam o `canvas-arcade`, não um derivado. Feel, arte em
escala, conteúdo, mixagem em sessão real e aprovação de pessoa **não**
foram observados fora do starter. `experience_status` permanece
`not_assessed`.

### 7. O PR continua draft

Não marcar ready sem revisão humana. O corpo do PR descreve as quatro
lacunas, as duas pesquisas e os testes que amarram doc e código.

## Como verificar depois de puxar

```sh
python3 -m unittest discover -s tests
cd assets/starters/canvas-arcade && npm test && npm run budget
python3 scripts/game.py doctor --root /caminho/do/laboratorio
python3 scripts/game.py discover --root /caminho/do/laboratorio
python3 scripts/game.py next /caminho/de/um/jogo --focus create
```

`--root` vale antes ou depois do subcomando. Caminho com espaço tem de
continuar citado com `shlex.quote` em **todo** comando que o harness
sugere — já quebrou uma vez.

Não use `vertical-slice` como `--focus`; os focos do CLI são os de
`FOCI` (`create`, `feel`, `release`, …). A etapa `vertical-slice` existe
em `STAGES` e no `context --stage`.

## Branches laterais

Duas branches de pesquisa foram absorvidas aqui e podem ser ignoradas:

- `cursor/pesquisa-gates-marcos-producao-064d` — parou em `ec95360`
- `cursor/observable-criteria-research-6f33` — parou em `5069959`

O conteúdo útil delas está neste histórico (`a3e9add`, `c98f704` e
seguintes). Não rebaseá-las sobre esta.

## Arquivos novos que importam

| Arquivo | Por quê |
| --- | --- |
| `scripts/game.py` | `doctor`, `init`, `next`, `bar`, `gate`, `review` |
| `tests/test_game.py` |  o contrato; leia um teste antes de mudar o comportamento que ele nomeia |
| `references/gates.md` | recusa, tipos, estados, limites |
| `references/production-bar.md` | escada e a seção “conferir sem importar número” |
| `references/gates-research.md` | fontes; §8 é o confronto com o desenho |
| `references/observable-criteria-research.md` | fontes; §6 é o que **não** citar; §7 é o que daria checklist |
| `references/sources.md` | mapa: o que é interno, o que veio depois, a ordem |
| `assets/starters/canvas-arcade/` | o único REUSE executável |
| `SKILL.md` / `README.md` / `adoption.md` | o que o agente e a pessoa vêem primeiro |

## Princípio para o próximo passo

Tratar a causa, não o sintoma. Se a tentação for “mais um gate” ou “mais
um número na barra”, a resposta provavelmente já está na §6 de
`observable-criteria-research.md` ou na §8.2 de `gates-research.md`. O
buraco que mais dói hoje é o item 1: um critério que o framework chama
de inegociável e que ninguém lê no disco.
