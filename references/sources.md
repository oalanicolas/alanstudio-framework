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
O harness adapta o **piso** e recusa o **tier** como objetivo.

## Áudio (catálogo)

O acervo `shared/sfx` é do laboratório, não deste repositório. O harness expõe
`sfx search` / `sfx copy` quando essa pasta existir na raiz de `--root`.
A receita de áudio orienta mix e interrupção; o catálogo só localiza arquivos.

## Playground

Os jogos públicos da Alan Studios ficam em [games.alanicolas.com](https://games.alanicolas.com/).
Cada um usa a própria engine. Este harness não reivindica tê-los produzido.
