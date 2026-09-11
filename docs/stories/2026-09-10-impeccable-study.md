# Estudo da skill impeccable e transposição da sua forma para o game-dev

Status: Ready for Review — estudo, transposição e validação concluídos.

Pedido: "estude profundamente a skill impeccable, quero que nosso framework de
games funcione que nem ela". A impeccable é uma skill de design de interfaces
de frontend (`~/.claude/skills/impeccable`: `SKILL.md`, 36 referências, ~19 mil
linhas com scripts). Este registro diz o que ela é, por que funciona, o que foi
transposto para o `game-dev` e o que ficou de fora com motivo.

- [x] Ler `SKILL.md`, as 36 referências e os scripts centrais (`load-context`,
  `pin`, `critique-storage`, registro do detector, `live.mjs`).
- [x] Separar **forma de operar** (transponível) de **conteúdo de UI** (não é
  domínio do harness).
- [x] Mapear cada mecanismo para o que o `game-dev` já tinha, adaptando o canônico
  em vez de criar uma segunda implementação.
- [x] Implementar: `SKILL.md` roteador, 23 referências de comando, catálogo,
  `commands`/`pin`/`unpin`, `scale` no `context`, checagem no `doctor`, testes.
- [x] Validar: suíte inteira verde, links internos, catálogo ↔ arquivos ↔ tabela.

## 1. Anatomia da impeccable

**Um roteador, não um manual.** O `SKILL.md` tem 180 linhas e faz cinco coisas:
(a) uma *preparação* obrigatória em três passos — carregar contexto por script,
identificar o *register* (brand ou product), carregar a referência do sub-comando,
com a frase "pular isto produz output genérico que ignora o projeto"; (b) *leis
compartilhadas* curtas, aplicáveis a qualquer tarefa (OKLCH, sem `#000`, escala
tipográfica ≥1,25, sem animar layout); (c) *recusas absolutas* em modo
reconheça-e-recuse (borda lateral colorida, texto em gradiente, glassmorphism,
hero-metric, grade de cards idênticos, modal como primeira ideia); (d) o *teste de
slop* em dois níveis de reflexo ("observabilidade → azul escuro" é o primeiro;
"não é SaaS-creme → editorial-tipográfico" é o segundo); (e) uma *tabela de 23
comandos* em seis categorias com três regras de roteamento: sem argumento → menu;
primeira palavra é comando → carregue a referência; senão → invocação livre com
preparação e leis.

**Contexto por arquivo, carregado por script.** `PRODUCT.md` (quem/por quê:
register, usuários, personalidade, anti-referências, princípios) e `DESIGN.md`
(como parece: tokens em YAML no formato Google Stitch, seis seções fixas).
`load-context.mjs` devolve JSON; a regra é consumir inteiro, não filtrar. Se
`PRODUCT.md` falta ou é placeholder, `teach` é acionado como *bloqueio* e o comando
original retoma depois. `document` gera `DESIGN.md` a partir do código (modo
scan) ou de cinco perguntas (modo semente), com um sidecar JSON para o que o
formato não cabe.

**Uma referência por comando, com a mesma forma.** Cada `reference/<cmd>.md`
começa com uma frase do que o comando faz, tem uma nota de register, e segue
Avaliar → Planejar → Implementar → Verificar → Nunca → entregar a `polish`. O
conteúdo de UI é denso, mas a estrutura é o que permite a um agente executar
qualquer comando com a mesma disciplina.

**Portões que não se comprimem.** `craft` declara explicitamente que "shape
confirmado não é sinal verde para codar" e enumera os portões (brief, perguntas
de direção, paleta, mock aprovado). `shape` é entrevista de duas ou três perguntas
por rodada, "afirme e confirme, não ofereça menu", e termina a resposta esperando
confirmação. O texto nomeia o modo de falha dominante ("comprimir os portões
porque o brief parecia completo") — a skill foi escrita contra o comportamento
observado do modelo, não contra um ideal.

**Avaliação com dois olhares e persistência.** `critique` exige a avaliação A
(revisão de design, pensando como diretor) *antes* da B (detector determinístico
+ evidência de navegador), porque B ancora o julgamento; sintetiza sem
concatenar; pontua as dez heurísticas de Nielsen 0–4; tria P0–P3; passa por
personas (cinco arquétipos com bandeiras específicas); persiste em
`.impeccable/critique/<slug>` e mostra a tendência das últimas cinco rodadas;
termina perguntando com base nos achados (nunca genericamente) e devolve uma
lista ordenada de comandos que termina em `polish`.

**Detector e live.** Um registro de ~30 anti-padrões com id, categoria (slop /
quality), descrição e a seção da skill que o justifica, com quatro motores
(regex, HTML estático, navegador, contraste visual). O modo `live` injeta um
painel no dev server, o usuário seleciona um elemento e a skill gera três
variantes com HMR, num protocolo de polling com journal durável.

**Atalhos.** `pin.mjs` cria `<harness>/skills/<cmd>/SKILL.md` que redireciona
para `/impeccable <cmd>`, só onde a impeccable está instalada, com um marcador
para nunca apagar skill do usuário; `command-metadata.json` fornece a descrição.

## 2. Por que funciona

1. **A preparação é um contrato, e ela nomeia a consequência de pulá-la.** Não é
   "recomendamos ler"; é "sem isto o resultado é genérico".
2. **Register muda o que se cobra, não o que se recusa.** Brand e product têm
   permissões e bans próprios, mas as leis e as recusas absolutas valem nos dois.
3. **Recusas em forma reconhecível.** Cada ban é um padrão que o modelo produz
   por reflexo, descrito no vocabulário em que ele o produziria.
4. **O comando é um fluxo, não um assunto.** `feel` de jogo já existia como
   receita; o que a impeccable acrescenta é a ordem, as paradas e a entrega.
5. **Portões explícitos contra o modo de falha observado.** O texto descreve o
   que o modelo faz de errado e proíbe pelo nome.
6. **Prova separada de julgamento.** Detector é "evidência de defeito, nunca prova
   de acerto"; screenshot não lida "não conta"; "não invente defeito para parecer
   iteração".
7. **A tabela é o menu e o índice de manutenção.** Catálogo, arquivo e pin
   concordam por construção.

## 3. Mapeamento para o game-dev

O `game-dev` já tinha o *harness* mais forte (contexto por foco, scan de nove
áreas, barra, gates, `verify`, `record`, `next`, starters, pacotes). O que faltava
era exatamente a camada que a impeccable tem de melhor: a **forma de operar** da
skill. A tabela diz o que virou o quê; o princípio foi adaptar o canônico
existente, não criar uma segunda implementação.

| impeccable | game-dev (antes) | game-dev (0.10) |
| --- | --- | --- |
| Preparação em três passos | Passo 1 "Contexto" dentro de sete passos | `## Preparação`: contexto → escala → referência do comando, não negociável |
| `load-context.mjs` → JSON | `context <projeto> --focus` | Mantido; regra de consumir inteiro e de quando recarregar |
| `PRODUCT.md` (register, usuários, princípios) | Brief / `game-design.md`, AGENTS.md | Idem; `teach` é o bloqueio que os produz |
| `DESIGN.md` + sidecar | Art Bible / design system do jogo | Idem; `document` gera a partir do código, modo scan ou semente |
| Register brand / product | Escala jam / produto / AA em [ambição](../../references/ambition.md), sem leitura pelo harness | `## 2. Escala`; `context.scale` (`--scale` vence; campo `Escala:` sugere; "AAA" → `aa`) |
| Leis compartilhadas | Espalhadas em processo/qualidade/ambição | `## Leis compartilhadas`: verbo, impacto no quadro, mínimo entre dimensões, REUSE, prova, direção, continuidade, memória, autoridade |
| Recusas absolutas | Espalhadas ("não chame de AAA", "não gere nove templates") | `## Recusas absolutas`: doze, em forma reconhecível |
| Teste de slop em dois níveis | Inexistente | `## O teste de slop para jogos`: reflexo de gênero e reflexo de anti-referência |
| Tabela de comandos + roteamento | Tabela "Caminho rápido" situação → CLI | 23 comandos em seis categorias; três regras; tabela situação → comando |
| `reference/<cmd>.md` (Avaliar/Planejar/Implementar/Verificar/Nunca) | Receitas por foco (assunto, não fluxo) | `commands/<cmd>.md` (Escala/Avaliar/Executar/Verificar/Nunca/Entregar), apontando as receitas |
| `craft` com portões nomeados | Sete passos no SKILL | `commands/craft.md`: brief confirmado, direção aprovada, apresentação com prova |
| `shape` entrevista curta, afirme-e-confirme | Passo 2 "Intenção e prontidão" | `commands/shape.md`: brief da rodada, compacto ou completo, termina esperando |
| `teach` como bloqueio | `--event initialize` e auditoria automática | `commands/teach.md`: mesma política, agora com a escala como primeiro campo |
| `critique` A antes de B, P0–P3, persistência, tendência | Protocolo de observação; `record` | `commands/critique.md`: leitura da barra por dimensão com condição e autor, dois olhares, achado com quatro partes, `record --kind observation`, tendência por recorte — sem nota |
| `personas.md` (Alex, Jordan, Sam, Riley, Casey) | Inexistente | [personas](../../references/personas.md): Nina, Rafa, Sam, Bia, Léo, com bandeiras e seleção por recorte |
| `audit` técnico sem corrigir | `doctor`, `scan`, `bar`, `gate` soltos | `commands/audit.md`: os quatro em ordem, com relatório por severidade |
| `polish` alinhado ao design system | Barra: subir a mais baixa | `commands/polish.md`: exige fatia completa; drift por causa (token ausente / avulso / conceito) |
| `command-metadata.json` | — | `commands/commands.json` |
| `pin.mjs` / `unpin` | `doctor` só conferia o atalho da skill | `game.py pin/unpin`, marcador, só onde a game-dev está instalada |
| Integridade catálogo ↔ arquivos | — | `doctor` checagem `commands`; `tests/test_commands.py` |

Comandos novos que não têm par direto na impeccable e nascem do domínio:
`playtest` (observação humana com regra de parada; a impeccable não tem gente
jogando), `juice` (sinal do impacto, separado de `feel` como `animate` é separado
de `delight`), `produce` e `release` (marcos, gates, artefato), `init` (starter).
Comandos da impeccable sem par: `bolder`/`quieter` (tom visual de superfície;
em jogo o análogo é direção de arte, coberto por `visual`), `colorize`/`typeset`/
`layout` (UI web), `extract` (design system: coberto por `document`), `overdrive`
(sem consumidor; o piso já é o alvo), `animate`/`delight` (viraram `feel`/`juice`).

## 4. O que não foi transposto, e por quê

- **Pontuação Nielsen 0–40.** A barra recusa somar dimensões: "o degrau percebido é
  o mínimo, não a média". Uma nota total esconderia exatamente o piso. `critique`
  entrega tabela por dimensão + piso nomeado + severidade por achado.
- **Detector determinístico.** Opera sobre CSS/DOM estático, com regras
  verificáveis sem executar nada. O análogo em jogo (juice fora do quadro,
  timer que corre em pausa, som fantasma) exige executar o jogo, que o harness não
  faz por contrato. Fica como hipótese: um detector de *declarações* (barra, gates,
  proveniência) já existe em `bar`/`gate`; um detector de *comportamento* pediria
  o starter como consumidor e um contrato de execução que hoje é do projeto.
- **Modo `live`.** Depende de HMR e de um painel injetado; o equivalente em jogo
  (variantes de feel em tempo real com hot reload) não tem consumidor no laboratório
  hoje. Hipótese registrada, não recomendação.
- **Geração de mocks/paleta por imagem.** Depende de geração de imagem no host.
  O `craft` de jogo tem o portão "direção aprovada" (`--event direction-approved`)
  como equivalente, sem gerar imagem.
- **Armazenamento próprio (`.impeccable/critique/`).** O harness já persiste
  evidência por `record`, ligado ao HEAD e com anexos por SHA-256; criar um segundo
  armazenamento contradiria a regra de fonte canônica única.
- **Conteúdo de UI** (OKLCH, tipografia, bans de CSS, Stitch): não é domínio deste
  harness; fica onde está.

## 5. Decisões de implementação

- O `SKILL.md` perdeu os sete passos como corpo principal; eles vivem em
  `commands/craft.md` e em [processo](../../references/process.md). Nenhuma regra
  foi removida; o teste que exige as oito capacidades no SKILL continua passando.
- Referências de comando são **orquestradores finos**: apontam receita, template e
  comando do harness; não repetem a receita. O teste exige que cada `reads` do
  catálogo apareça linkado no arquivo.
- A escala é lida pelo harness exatamente como o gênero: campo em documento só
  sugere; a conversa declara. "AAA" num brief é lido como `aa` porque é o único
  sentido aceito para a palavra aqui ([ambição](../../references/ambition.md)).
- `pin` grava o caminho absoluto do `SKILL.md` e da referência no atalho, porque a
  skill tem um checkout único (o `framework/core` do workspace aponta para ele).
- A checagem `commands` do `doctor` é obrigatória (`required: true`): um comando no
  menu sem arquivo manda o agente ler o que não existe.

## 6. Validação

`python3 -m unittest discover -s tests`: 243 testes, todos aprovados (226 anteriores,
16 novos em `tests/test_commands.py` e um em `tests/test_game.py` para a declaração
em subpasta). A suíte já confere links internos e
âncoras de todo o repositório, exemplos com `--output` únicos, capacidades citadas
no SKILL e README, e a ordem do `next` no README. `python3 scripts/game.py doctor`
reporta `commands: ok` com 23 sub-comandos. Não foi executado nenhum jogo; os
scripts da impeccable não foram executados; nada foi publicado.

Arquivos: `SKILL.md`, `README.md`, `adoption.md`, `commands/` (README, catálogo e 23
referências), `references/personas.md`, `references/sources.md`, `scripts/game.py`,
`tests/test_commands.py` e esta story.

## 7. Primeiro uso real: `critique` no Rabisco Boom

Executado no mesmo dia, no laboratório (`games/rabisco-boom`, build publicada d6ce8e1).
O fluxo do comando funcionou como escrito: avaliação A (jogar; aqui, simulação avançada
quadro a quadro porque a janela do navegador da extensão fica oculta) antes da B (95/95
testes por `verify`, `bar`, `gate`, QA do projeto); leitura da barra por dimensão com
condição e autor; achado com quatro partes; severidade; arquétipos; recibo por
`record --kind observation` com relatório, recibo técnico e capturas anexados. Piso lido:
`playable` em seis dimensões. Dois P1 que nenhum teste cobria: opção selecionada invisível
no saguão (especificidade CSS) e morte súbita esmagando o spawn do P1 no mesmo tick da
ativação. Relatório: `games-workspace/framework/evidence/2026-09-10/rabisco-boom-critique/`.

O uso real corrigiu o harness: `bar`/`gate` não liam `docs/planning/qa.md`. Corrigido em
`declaration_sources`, com teste, docs e entrada na adoção. É o caso previsto em
[aprendizados](../../references/learning.md): o caso fica no jogo, a regra vai ao núcleo.

## Continuidade

- **Onde estamos:** a skill opera como a impeccable e o `critique` foi exercitado num
  jogo real, com recibo, tabela de degraus lida por `bar` e a lacuna do harness que ele
  expôs já corrigida na fonte.
- **Próximo passo:** `$game-dev polish games/rabisco-boom` subindo a dimensão citada:
  os dois P1 (`clarify` do saguão em `style.css`; um compasso de aviso na morte súbita
  em `step.js`, com regressão em `step.test.js`), depois `playtest` com Alan para os
  bots e o áudio.
- **Por que agora:** são as duas coisas que traem o jogador que a leitura encontrou, e
  cada uma é uma mudança pequena com prova objetiva.
- **Pronto quando:** botão selecionado legível (cor ≠ fundo, conferido no DOM); a
  primeira célula da margem só esmaga um compasso depois do aviso tracejado (teste em
  `step.test.js`); tabela do QA atualizada com a nova observação.
- **Retomar por:** `framework/evidence/2026-09-10/rabisco-boom-critique/critique.md`,
  seção "Critique do verbo central" em `docs/planning/qa.md` do jogo, `commands/polish.md`.
