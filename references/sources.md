# Mapa dos estudos utilizados

Consulta sob demanda. As fontes externas pertencem aos commits estudados em
8 de setembro de 2026. Confira a fonte atual antes de aplicar uma conclusão
histórica. Catálogos locais enriquecem a consulta quando existem; não são
dependência do executor Python.

Defina `GAMES_FRAMEWORKS_ROOT` ou mantenha um irmão `Games-Frameworks` ao lado
do laboratório de jogos. Ausência deixa `studies` vazio; isso não é evidência
negativa.

## Recortes estudados

57 rastros; 150 candidatos: 115 observados em fonte, 22 precisam de confirmação,
13 excluídos, zero promovidos a testados. Integridade dos catálogos foi
verificada no laboratório; testes dos frameworks externos não foram executados.
Cada regra herda o limite do recorte, não descreve necessariamente o framework
inteiro.

| Recorte | Commit | O que entrou no harness |
|---|---|---|
| [BMad Game Dev Studio](https://github.com/bmad-code-org/bmad-module-game-dev-studio) | `2486f5f5f3b8` | leitura por etapa e retomada em **create** |
| [Phaser](https://github.com/phaserjs/phaser) | `02d8931b626d` | pausa, visibilidade e operações em **lifecycle** |
| [Excalibur](https://github.com/excaliburjs/Excalibur) | `4a23dd1674b1` | tempo controlado e limite de prova em **lifecycle/visual** |
| [Godot Demo Projects](https://github.com/godotengine/godot-demo-projects) | `0db80ca5fd22` | reinício, colisão e timers em **lifecycle** |
| [boardgame.io](https://github.com/boardgameio/boardgame.io) | `5e9a2c94bde8` | ações recusadas e identidade em **mechanics/network** |
| [Ink](https://github.com/inkle/ink) | `35c63e52f1d3` | histórico e versões em **content** |
| [LDtk](https://github.com/deepnight/ldtk) | `6d69bd1d6be9` | IDs, migração e níveis externos em **content** |
| [PettingZoo](https://github.com/Farama-Foundation/PettingZoo) | `a865c24671b2` | observação, término e seed em **lifecycle/network** |

Nenhuma regra foi copiada como mecânica obrigatória para todos os gêneros.
`context --focus` lista os catálogos deste mapa que existirem no irmão.

**A cobertura não é uniforme, e isso não é acidente.** Só seis focos têm catálogo:
`create`, `mechanics`, `lifecycle`, `content`, `visual` e `network` — os que
correspondem aos recortes efetivamente estudados. Em `architecture`, `feel`,
`performance`, `accessibility`, `audio`, `persistence`, `release` e `production`, `studies` vem
vazio, porque não houve extração para eles. Vazio aqui significa **não estudado**,
não “nada relevante existe”. Preencher esses focos exigiria novos recortes com o
mesmo rigor; inventar citações para emparelhar a lista seria o oposto do que este
mapa existe para fazer.

## Critérios observáveis (pesquisa externa, 0.9)

O levantamento em
[observable-criteria-research.md](observable-criteria-research.md) é de outra
natureza e **não preenche os focos vazios acima**. Ele não é extração de código:
é busca por fontes publicadas — normas, documentação de fornecedor, artigos
revisados por pares, código-fonte de jogos publicados — que sustentem números
para game feel, consistência de arte, orçamento de performance, legibilidade de
interface e metodologia de playtest.

O resultado é assimétrico, e isso está dito lá dentro: safe area de TV, contraste
e tamanho de fonte têm norma ou documentação de plataforma atrás; orçamento de
draw calls, tamanho de paleta e limiar de latência universal não têm nada. A
seção final lista explicitamente os números que **não** podem ser citados como
fato estabelecido, com o motivo de cada um.

**Nenhum limiar de lá foi promovido** para a [barra](production-bar.md) nem para
os [gates](gates.md). Levantar a fonte e calibrar contra uma amostra de jogos são
passos diferentes, e só o primeiro foi dado — nenhum degrau passou a exigir 16 ms,
4,5:1 ou 93%.

Duas coisas que **não** são limiar entraram, e é justo dizer quais. A primeira é
um método: a regra de parada de playtest, do RITE (Medlock et al., 2002, fonte
primária), que substitui a pergunta “quantas pessoas?” por “o que encerra a
rodada?”. Ela entrou no [roteiro de observação](quality.md) e no template de QA.
A segunda é uma correção: o “cinco usuários” foi recusado por leitura do artigo
original, que conclui outra coisa, e a recusa está escrita onde alguém iria
procurar o número. Junto delas, a barra ganhou uma seção sobre o que se pode
conferir **sem** importar número — conformidade com o que o próprio projeto
declarou —, que é o formato de critério que não depende de nenhuma fonte externa
estar certa.

A heurística de triagem que sobrou do levantamento e vale para qualquer fonte
futura: **fonte séria declara de onde tirou o número.** A EBU diz de qual medição
de overscan saíram os 3,5%; a Unity chama o próprio 35% de “a general tip”. Um
número com casa decimal e sem origem não é mais preciso, é menos honesto — e o
levantamento nomeia os domínios em que isso apareceu.

## Pré-produção e checagem

Na versão 0.2, leitura adicional dos templates no mesmo commit BMad
`2486f5f5f3b8870baa6cee4615a870c0330f441c`. Não foi uma nova extração Code
Anatomist nem execução dos workflows BMad.

- Game Brief, GDD, PRD, arquitetura e playtest do módulo BMad, adaptados aos
  templates em [assets/templates](../assets/templates).
- [MDA, artigo original](https://www.cs.northwestern.edu/~hunicke/MDA.pdf).
- Distinção varredura × inspeção profunda, adaptada do fluxo document-project
  do BMad, no [roteiro de auditoria](project-audit.md).

Os templates foram redigidos em português. Não importam a hierarquia de agentes,
instalação, publicação ou cerimônias BMad.

## Arquitetura (0.8)

A receita [architecture](../recipes/architecture.md) adapta processo transversal
observado no Architect AIOX, sem copiar o runtime, o roteador de engines nem a
hierarquia de agentes. Estudo e hashes ficam no laboratório.

## Produção (0.9)

As receitas [production](../recipes/production.md) e [feel](../recipes/feel.md) e os
templates `production-plan`, `milestone` e `game-design` não vêm de uma nova extração
de repositório. Usam vocabulário corrente da indústria — marcos first playable, alpha,
beta e gold; orçamentos de quadro/memória/carregamento; lentes por disciplina;
princípios de animação e feedback — adaptados aos limites deste harness. Cada estúdio
e plataforma define os detalhes; o plano de cada jogo registra a definição adotada.
Requisitos de loja, console e acessibilidade devem ser consultados na fonte oficial
da plataforma; o framework não os reproduz nem certifica.

## Pacotes (0.9)

Os [pacotes de plataforma e gênero](../packs/README.md) reúnem convenções públicas das
engines (callbacks, CLIs, ferramentas de profiling, formatos) e vocabulário corrente de
design por gênero. Não são extração de repositório nem foram executados neste
repositório; comandos e nomes mudam entre versões. Cada pacote manda confirmar na
documentação oficial da versão em uso e no código do projeto. Fantasy consoles (PICO-8)
invertem o piso sonoro do framework de propósito: ali o chiptune é a plataforma, e o
pacote pede que a decisão fique registrada. Os pontos de partida do
laboratório citados nos pacotes de gênero (Era Uma Vez, Brasa-Pista, Distrito Rabisco)
seguem os limites já declarados em [criar](../recipes/create.md).


## Feel, áudio e ambição (0.9)

As receitas [feel](../recipes/feel.md) e [áudio](../recipes/audio.md) e o
contrato [ambição](ambition.md) sistematizam o piso de acabamento já implícito
em qualidade, Art Bible e no playground. Não extraem um kit universal de juice
nem um motor de mix. Não há recorte externo promovido a testado para esses
focos; `studies` permanece vazio até existir catálogo pertinente.

## AAA: tier e piso (0.9)

Leitura de 9 de setembro de 2026. Nenhum teste desses textos foi executado
neste repositório. Orçamentos e headcounts são contexto de mercado, não meta
do harness.

**Tier de mercado (o rótulo financeiro):**

- [AAA (video game industry)](https://en.wikipedia.org/wiki/AAA_(video_game_industry))
  — publisher médio/grande, orçamento e marketing; origem em nota de crédito;
  AA / Triple-I / AAAA como termos vizinhos sem certificação.
- [Bernevega & Gekker, *Games and Culture*](https://doi.org/10.1177/15554120211014151)
  — AAA como mercadoria de maior aposta, não como grau criativo.
- [Video Game Canon — What is a AAA game?](https://www.videogamecanon.com/adventurelog/what-is-a-aaa-game/)
  — história do empréstimo da nota de crédito.
- CMA do Reino Unido (2023), citada na Wikipedia: média ~US$ 200 mi para AAA
  greenlitados a 2024–25. Números de *Call of Duty* / *GTA V* são reportagem,
  não medição nossa.

**Piso de acabamento (o que o jogador percebe):**

- Steve Swink, *Game Feel* — controle em tempo real, espaço simulado, polish.
  [Verbete](https://en.wikipedia.org/wiki/Game_feel).
- Jonasson & Purho, [Juice it or lose it](https://www.youtube.com/watch?v=Fy0aCDmgnxg)
  (GDC) — som como juice de maior retorno; efeitos que não mudam a regra.
- Tokey et al., i3D 2026 — spike de frametime domina suavidade e pontuação
  num FPS; fidelidade gráfica muda a nota visual, pouco o desempenho.
  [Página](https://web.cs.wpi.edu/~claypool/papers/frame-stutter-graphics-i3d-26/).
- Vertical slice como trava de qualidade → tempo de asset → headcount: prática
  de pipeline (publisher gates). Repeatability: outro trecho sem heroísmo.

Blogs de estúdio/agência de 2025–26 (orçamento, AA vs AAA, consistência visual)
informaram o vocabulário contemporâneo; não foram promovidos a regra testada.
O harness adapta o **piso** e recusa o **tier** como objetivo. O instrumento
preenchível é o [checklist](aaa-checklist.md) (`--stage aaa`); não é um
score nem uma extração testada desses textos.

## Barra de acabamento (0.9)

A [escada](production-bar.md) **não** vem de uma fonte externa citável. Ela é uma
síntese redigida neste repositório a partir de três origens, e é honesto separá-las:

- **Critérios já presentes aqui**, reorganizados por dimensão e degrau: o roteiro
  de [qualidade](quality.md), o contrato do
  [design system do jogo](game-design-system.md) e as regras de ciclo de vida
  vindas dos recortes de Phaser, Excalibur, Godot Demo Projects e PettingZoo.
- **Vocabulário corrente da indústria** — protótipo, vertical slice, publicável —
  usado no sentido de dependência entre etapas, não como certificação.
- **Julgamento editorial deste estúdio** sobre o que o jogador percebe primeiro,
  em especial a regra do mínimo entre dimensões.

O formato de declaração que `bar` lê — tabela em Markdown, uma linha por dimensão
— também não vem de fora: ele foi extraído da tabela que o README do starter já
tinha escrita à mão, e o comando passou a ler o que já existia em vez de pedir um
arquivo novo. Nenhuma das dez dimensões ganhou limiar numérico nessa passagem: o
que o harness confere é a forma da linha, e a escada continua sem calibração
contra uma amostra de jogos publicados.

Nenhum degrau foi calibrado contra uma amostra de jogos publicados, e nenhuma
medição foi repetida para produzir esta escada. Os limites numéricos que aparecem
nas dimensões `performance` e `audio_mix` são pontos de partida a confirmar no
dispositivo alvo, não constantes verificadas. Trate a escada como linguagem
compartilhada para observar, não como aferição.

## Gates de produção (0.9)

Os dez gates de [gates.md](gates.md) têm procedência interna e verificável: cada
critério é extraído de uma linha `**Pronto para…**` que já estava escrita em
[preproduction.md](preproduction.md), uma por etapa. Nada ali foi inventado na
passagem, e um teste do harness exige que cada gate continue apontando para a
prosa de origem. A regra de quais critérios **não** são dispensáveis também não é
escolha do harness: são os quatro em que a prosa da etapa não deixa terceira
opção, com a frase citada na tabela do próprio `gates.md`.

O que **não** vem de dentro é a estrutura de três saídas — passar, cortar escopo,
abandonar. Ela vem de uma única fonte, e é preciso dizer o que essa fonte é:

| Fonte | O que é | O que sustenta |
| --- | --- | --- |
| [20 Game Dev Tips](https://youtu.be/fqb9MfRqK9I) | Vídeo de um desenvolvedor indie, patrocinado, dirigido a iniciantes, sem citação de estudo ou dado | Que praticantes tratam abandonar como decisão legítima, e que decidir cedo é melhor que decidir tarde |

Isso é **conselho de praticante**, não evidência. Sustenta “há quem defenda isso e
por quê”; não sustenta “isso funciona”. Peguei dela uma coisa só: a legitimação de
abandonar como saída de gate, que o ciclo já tinha na etapa `poc` (“continuar,
ajustar ou abandonar”) e que passou a valer nas dez. A generalização é julgamento
editorial deste estúdio, apoiada numa coerência interna, não na autoridade do
vídeo.

A segunda coisa que veio de lá é menor e está na [receita de
arquitetura](../recipes/architecture.md): o repositório já dizia para não
generalizar cedo e não dizia nada sobre o erro contrário, o de seguir improvisando
depois que as cópias se acumularam. O vídeo trata os dois lados e admite que a
escolha é um palpite. A adaptação — declarar a contagem-limite no TDD, com data e
autor, em vez de mantê-la na cabeça — é deste repositório, e segue a mesma lógica
que já vale para a barra e para os gates: transformar julgamento implícito em
declaração contestável. Nenhum número foi importado.

O que recusei da mesma fonte, para não dar a impressão de que absorvi o material
inteiro: o limiar de “80% pronto, então termine” é número sem origem, e não entrou
em critério nenhum. “Sua engine não importa” contradiz a receita de arquitetura
deste repositório e é simplificação para iniciante. Os conselhos sobre sorte,
dinheiro e tutoriais não são critério de avanço de nada. E cerca de metade do
vídeo descreve práticas que este framework já tinha — feel antes de conteúdo,
prototipar antes de decidir, documento de design, consistência de estilo, reusar
o que existe, definir público e sensação pretendida —, o que serve como
convergência independente, não como fonte nova.

### Levantamento externo posterior

Depois que os dez gates já estavam escritos, foi feito um levantamento da
literatura externa sobre gates e marcos de produção, registrado em
[gates-research.md](gates-research.md) com URL, autoria, natureza primária ou
secundária e limite de cada fonte. Ele **não** foi a origem dos gates; serve para
três coisas, e a terceira é a que mais importa.

Primeiro, **substituir a fonte fraca da tabela acima onde houver fonte forte**. A
estrutura de três saídas tem apoio formal em Robert G. Cooper (Go / Recycle / Kill,
do método Stage-Gate), em artigos do próprio autor e na *Wiley International
Encyclopedia of Marketing* — literatura de gestão de produto, não conselho de
praticante. O mesmo vale para `waived` e os quatro não dispensáveis, que reproduzem
a assimetria de Cooper entre critério que mata sozinho e critério negociável, e
para `held_by_declaration`, que corresponde
ao asterisco com que a Microsoft separa requisito de requisito testado nos Xbox
Requirements públicos. Essas escolhas foram feitas aqui sem conhecer as fontes;
convergência nessa ordem é evidência melhor que citação posterior, e a ordem está
declarada.

Segundo, **nomear lacunas**. Duas foram fechadas depois, e o que entrou por elas é
a única parte dos gates que não tem procedência interna. Cooper separa três tipos
de critério, e o segundo faltava aqui: `readiness` pergunta se o trabalho está
feito, `must_meet` pergunta se ainda vale o que custa, e a segunda pergunta
existia só como a saída `abandonar`, dependendo de alguém levantá-la. Dos três
critérios `must_meet` que passaram a existir, um — `close.decision` — já estava na
prosa do ciclo; os outros dois, `implement.worth_building` e `scale.worth_scaling`,
**vêm de Cooper e estão declarados como acréscimo** na tabela de `gates.md`. O
terceiro tipo de Cooper, *should-meet*, não foi implementado: scorecard existe para
ordenar projetos entre si, e um gate a mais sem função é o que ele mesmo chama de
burocracia. A outra lacuna era o estado `out_of_scope`, cuja forma vem dos XAGs
(perguntas de escopo antes do critério) e da TRC histórica (“Applicable”). As
lacunas que **continuam abertas** estão em `gates-research.md` §8.2 e repetidas nos
limites de `gates.md`: entregáveis fixados na saída do gate anterior, e a evidência
não distinguir log de comando de alguém que olhou.

Terceiro, e mais importante para o que este repositório pode afirmar: **o
levantamento confirma que não existe definição canônica dos marcos de produção de
jogos**. Não há norma de corpo de padronização, associação da indústria nem
publisher em documento público que defina First Playable, Vertical Slice, Alpha,
Beta, Content Lock ou Gold Master; e as fontes que existem — livro-texto, prosa de
praticante, modelo de contrato — **discordam entre si sobre o conteúdo**, não apenas
na ênfase. Alpha aparece como “feature complete” numa fonte e como “40–50% dos
assets finais, com features ainda sujeitas a ajustes maiores” noutra. Portanto a
decisão de nomear os gates pela permissão pedida (`design`, `build`, `scale`) em vez
de pelo nome do marco tem agora razão documentada, e o vocabulário de etapas
continua sendo convenção deste repositório, como a barra já declarava.

O levantamento também registra o que **não** tem fonte confiável, incluindo a
ausência de qualquer avaliação empírica de que gates de produção melhorem o jogo
entregue. Adotar gates como disciplina explícita é defensável; alegar eficácia
comprovada não é.

## Starter `canvas-arcade` (0.9)

Escrito neste repositório, sem dependências de terceiros. `mulberry32`, em
`src/core/rng.js`, é algoritmo de domínio público amplamente publicado; o
embaralhamento de bits em `src/core/hash.js` pertence à mesma família. O starter
não embarca imagem nem fonte. O som dos seis papéis é design original
em `public/sfx` (CC0-1.0, `tools/design-sfx.py`) — proveniência completa em
[CREDITS.md](../assets/starters/canvas-arcade/CREDITS.md).

Seus testes rodam neste repositório e exercitam o ciclo de vida, o determinismo e
a migração de save do próprio starter — com duas exceções ditas: `capture` só é
exercitada na guarda de ausência de tela, e nenhum teste interrompe a gravação no
meio. Nada disso alcança um jogo derivado depois que ele for adaptado.

## Áudio

O acervo `shared/sfx` é do laboratório, não deste repositório. O harness
expõe `sfx search` mesmo sem essa pasta: o catálogo vem vazio e a busca
nomeia o stem do starter que casa com o termo. `sfx copy` e
`sfx export` levam bytes e créditos desse stem, ou de um id do
acervo. Com sons, `sfx serve` abre a página de escuta; se `ui/`
faltar, o harness gera a lista. Tocar nessa página não é mix ouvida.
A receita de áudio orienta mix e interrupção; o catálogo só
localiza arquivos do acervo — não ouve o starter.

## Playground

Os jogos públicos da Alan Studios ficam em [games.alanicolas.com](https://games.alanicolas.com/).
Cada um usa a própria engine. Este harness não reivindica tê-los produzido.

## Gauntlet de prompts

Na 0.9, leitura adicional de fontes locais para o [modo prolongado](gauntlet.md),
sem executar workflows de terceiros nem ampliar as extrações Code Anatomist:

- MKT book-research-gauntlet (estudo local do laboratório)
  e manifesto (estudo local do laboratório):
  escopo declarado, fonte/localizador e lacuna explícita. Adaptados para objetivo e
  evidência do recorte; não copiamos corpus mínimo nem regras de produção editorial.
- Pesquisa local de gauntlet no MKT (estudo local do laboratório):
  insumo conceitual para rodadas, inspeção do artefato e preservação do melhor resultado.
  Suas alegações sobre modelos, custos e resultados externos não foram verificadas
  nesta entrega e não fundamentam garantias do Games.
- BMad quick-dev, revisão (estudo local do laboratório):
  distinguir intenção, especificação, patch, achado anterior e alegação descartada;
  preservar o que funciona antes de corrigir. Adaptamos também a causa “ambiente/prova”.
  Não importamos fan-out obrigatório, número fixo de iterações ou rollback automático.

Os oito estudos acima fornecem cenários candidatos conforme gênero/risco, não provas
de que um jogo já os suporta. O gerador é determinístico; seleção de fatias, controle
do prazo, avaliação e continuidade dependem da execução do agente. Testes do gerador
não demonstram uma sessão autônoma de várias horas.

## Pré-produção ampliada

Na versão 0.2, leitura adicional dos templates no mesmo commit BMad
`2486f5f5f3b8870baa6cee4615a870c0330f441c`. Esta leitura amplia o repertório de
processo; não foi uma nova extração Code Anatomist nem execução dos workflows BMad.

- Game Brief (estudo local do laboratório):
  visão, público, pilares, diferenciação, escopo e risco.
- GDD (estudo local do laboratório):
  ciclo, regras, controles, progressão, conteúdo e arte/áudio.
- PRD (estudo local do laboratório):
  seções proporcionais, requisitos com IDs, hipóteses, prioridades e escopo.
- Arquitetura (estudo local do laboratório):
  decisões, contratos e vínculo com implementação; adaptado como TDD do Games.
- Playtest (estudo local do laboratório):
  hipótese, participantes, observação e interpretação separadas.
- [MDA, artigo original](https://www.cs.northwestern.edu/~hunicke/MDA.pdf):
  mecânicas, dinâmicas e experiência estética. A ficha de hipótese/contraprova é
  aplicação nossa ao processo de trabalho, não uma garantia fornecida pelo artigo.
- [GDD na Unity](https://learn.unity.com/tutorial/664b276cedbc2a4d7b2e4f10?version=2022.3)
  e [PRD na Atlassian](https://www.atlassian.com/agile/product-management/requirements/):
  referências consultadas ao esclarecer os documentos ao usuário.

Os templates Games foram redigidos em português e adaptados aos executores locais.
Não importam a hierarquia de agentes, instalação, publicação ou cerimônias BMad.
PoC, vertical slice e MVP recebem critérios distintos no [ciclo criativo](preproduction.md);
profundidade e evidência acompanham a tarefa, sem nove arquivos obrigatórios.

## Aprendizados de aplicações

Extração dos registros do laboratório em setembro de 2026: workflow de criação
com IA e rodadas de Fenda Arcana, Bebê Geleia (web/HDRP), Rabisco, Brasa-Pista,
Satisfactory Blueprint, Megarealista, Guerra dos Rabiscos e Forja Lendária.
Os relatos incluem contraprovas e correções de interpretações anteriores.

- [Workflow](creative-workflow.md): intenção, materialização, QA e decisão num ciclo.
- [Performance](../recipes/performance.md): comparação causal, custo, invalidação e física.
- [Web](../packs/platforms/web.md): carregador, instâncias, passes e medição real.
- [Unity](../packs/platforms/unity.md): persistência, variantes, paridade e serialização.
- [Conteúdo](../recipes/content.md) e [áudio](../recipes/audio.md): contratos de assets,
  transporte íntegro, relógio da simulação e memória decodificada.
- [Gestão de módulos](workspace-binding.md#módulos): extração por commit, links,
  seleção por manifesto, preservação de trabalho e política de publicação.

As generalizações são pontos de aplicação condicionados ao contrato e à versão do
projeto. Não comprovam ganhos em outros jogos, não tornam fornecedores obrigatórios
e não substituem observar o consumidor final. Os números, arquivos brutos e
aprovações específicas ficam nos registros do jogo; o framework não depende de
acesso ao laboratório para usar as orientações. Revisão futura incorpora a
contraprova à fonte canônica conforme [o procedimento](learning.md).

## Autoria UGC pública

Estudo do laboratório de 09/09/2026: Rezona e Crayon. Inspeção estática de quatro
jogos públicos, frontend/iframe Crayon e pacote npm `rezona@0.2.0`; observações limitadas
de interface/partida. Não executamos o kit, geração paga, exportação, multiplayer ou
benchmark de autoria. Fontes públicas: [pacote versionado Rezona](https://registry.npmjs.org/rezona/-/rezona-0.2.0.tgz),
[Lab](https://rezona.ai/studio/game), [Crayon Arcade](https://app.usecrayon.ai/),
[ciclo do SDK CrazyGames](https://docs.crazygames.com/sdk/game/).

Foram adaptados critérios de [edição](../recipes/architecture.md#edição-estruturada-e-convivência-com-código),
[assets assíncronos](../recipes/content.md), [exportação](../recipes/release.md) e
[host/prévia web](../packs/platforms/web.md#jogo-embutido-e-troca-de-versão).
São procedimentos condicionais de engenharia, não implementação copiada ou prova de
vantagem econômica. Preservam contratos e escolhas artísticas do projeto. Heurísticas
de cena, limites universais e degradação automática não foram incorporados.

Hashes, amostras, observações e plano de contraprova ficam no laboratório em
`docs/estudo-profundo-rezona-crayon-framework.md` e
`docs/pesquisas/rezona-crayon-2026-09-09.json`. Os métodos acima são utilizáveis sem esses
arquivos e devem ser revistos quando o consumidor ou o contrato invalidar a hipótese.

## Skill impeccable (0.10)

Estudo de 10/09/2026 da skill `impeccable` (design e iteração de interfaces de
frontend, instalada em `~/.claude/skills/impeccable`): `SKILL.md`, 36 referências,
scripts (`load-context`, `pin`, `critique-storage`, detector de anti-padrões, modo
`live`). Lida integralmente; scripts não executados neste repositório.

O que foi adaptado é a **forma de operar**: preparação obrigatória (carregar
contexto → identificar register → carregar a referência do sub-comando), leis
compartilhadas separadas das recusas absolutas (match-and-refuse), teste de slop em
dois níveis de reflexo, tabela de comandos por categoria com regras de roteamento,
uma referência por comando com forma fixa (avaliar → planejar → executar →
verificar → nunca → entregar), catálogo em JSON, atalhos fixáveis com marcador,
critique com dois olhares independentes e severidade P0–P3, arquétipos de usuário
como lente. O register brand/product virou a escala jam/product/aa já existente em
[ambição](ambition.md); PRODUCT.md/DESIGN.md correspondem ao brief e ao design system
do jogo; `teach`/`document` correspondem à inicialização e ao Art Bible.

O que **não** foi adaptado, com motivo: pontuação Nielsen 0–40 (a barra recusa
somar dimensões: [production-bar](production-bar.md)); detector determinístico
(opera sobre CSS/DOM estático; o análogo em jogo exige executar o jogo, que o
harness não faz — hipótese registrada); modo `live` e geração de mocks (dependem
de HMR e de geração de imagem no host; sem consumidor no laboratório hoje);
`.impeccable/critique/` como armazenamento próprio (aqui a persistência é `record`,
ligado ao HEAD). Registro: [story](../docs/stories/2026-09-10-impeccable-study.md).
Conteúdo de design de UI (OKLCH, tipografia, bans de CSS) não foi transposto: não
é domínio deste harness.
