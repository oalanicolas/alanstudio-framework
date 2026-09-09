# Pacotes de plataforma e gênero

O núcleo do framework (processo, qualidade, receitas, templates) é agnóstico. Um
pacote só entra no `context` quando há evidência para ele:

- **Plataforma** (`packs/platforms/<nome>.md`): selecionado automaticamente pelo
  marcador que `identify` encontra no projeto. Marcadores próprios de engine vêm
  antes dos manifestos de ecossistema (RPG Maker MZ também tem `package.json`):

  | Marcador | Pacote | Marcador | Pacote |
  |---|---|---|---|
  | `ProjectSettings/ProjectVersion.txt` | `unity` | `*.p8` | `pico8` |
  | `project.godot` | `godot` | `Project.xml`, `*.hxml` | `haxe` |
  | `*.uproject` | `unreal` | `pubspec.yaml` | `flutter` |
  | `game.project` | `defold` | `*.sln`, `*.csproj` | `dotnet` |
  | `*.yyp` | `gamemaker` | `package.json`, `index.html` | `web` |
  | `*.c3proj` | `construct` | `Cargo.toml` | `cargo` |
  | `*.rmmzproject`, `*.rpgproject` | `rpgmaker` | `CMakeLists.txt` | `cpp` |
  | `game/options.rpy` | `renpy` | `pyproject.toml` | `python` |
  | `default.project.json` | `roblox` | `main.lua` | `lua` |

- **Gênero** (`packs/genres/<nome>.md`): selecionado por `--genre` declarado na
  conversa. Um campo `Gênero:` em documento do projeto gera apenas `suggested`; o
  agente confirma e passa a flag. Jogo híbrido escolhe o gênero do verbo central e
  lê o segundo pacote por conta própria (cada pacote aponta os vizinhos).

  | Verbo | Gêneros |
  |---|---|
  | Ler e escolher | `narrative`, `adventure` |
  | Mover e enfrentar | `platformer`, `action-adventure`, `shooter`, `fighting`, `stealth`, `horror` |
  | Pilotar e executar | `racing`, `sports`, `rhythm` |
  | Planejar | `turn-based`, `deckbuilder`, `strategy`, `tower-defense`, `puzzle` |
  | Construir e gerir | `simulation`, `survival-crafting`, `rpg`, `roguelike`, `idle` |
  | Competir e repetir | `multiplayer-competitive`, `casual` |

Os pacotes entram em `read_next` logo após a receita do foco: **receita → plataforma
→ gênero**. `context.packs` explica a base de cada seleção e o que não foi selecionado.

## O que um pacote é

Convenções para orientar leitura, perguntas e verificação. Cada comando, callback ou
orçamento citado é convenção da plataforma ou do gênero **a confirmar no projeto e na
documentação oficial da versão em uso**. Um pacote nunca substitui AGENTS, o GDD, o
TDD nem o que o código realmente faz; não certifica capacidade nem aprova nada.

## Contrato para um pacote de plataforma

1. Aplicabilidade (`kind` e marcador) e aviso de convenção.
2. Executar e verificar: CLI real, runner de testes, como o `verify` alcança (script
   declarado ou `--command`).
3. Ciclo de vida e estado: ordem de callbacks, pausa/foco, cenas, estado que
   sobrevive ao reinício, descarte.
4. Conteúdo e pipeline: formatos, importação, carga dinâmica, pipeline de render.
5. Performance e orçamentos: ferramentas de medição, orçamentos típicos, otimizações
   que preservam arte.
6. Build, plataformas e certificação: alvos, exportação, onde ficam os requisitos.
7. O que o harness faz e não faz ali.
8. Receitas do núcleo pertinentes.

## Contrato para um pacote de gênero

1. Aplicabilidade (`--genre`) e aviso de orientação.
2. Verbo central e decisões.
3. Feel que importa.
4. Riscos habituais.
5. Orçamentos e medições típicas.
6. QA e playtest específicos.
7. Receitas e fontes.

## Adicionar um pacote

Plataforma: acrescente o marcador em `ENGINE_MARKERS`, o mapeamento em
`PLATFORM_PACKS` e o arquivo; o teste de cobertura exige que todo `kind` tenha pacote.
Gênero: acrescente em `GENRES`, palavras-chave em `GENRE_KEYWORDS` e o arquivo.
`doctor` verifica a integridade dos pacotes. Origem e limites: [fontes](../references/sources.md#pacotes-09).
