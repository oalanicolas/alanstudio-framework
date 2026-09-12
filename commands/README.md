# Sub-comandos da skill

A skill `game-dev` roteia por **intenção**: `$game-dev craft`, `$game-dev critique`,
`$game-dev feel`. Cada comando tem uma referência aqui, carregada depois da
[preparação](../SKILL.md) (contexto e escala) e antes de qualquer ação. O modelo é a
skill `impeccable`: menu por categoria, uma referência por comando, atalhos fixáveis,
e a regra de que invocar sem carregar a referência produz trabalho genérico. Se o menu recusa invocar sem carregar a referência, o `commands` nomeia o genérico que o menu já recusa. Linha no disco não é a skill. Sem chave `genérico`. arquivo presente não é a referência carregada. Se o menu recusa que o arquivo presente seja a referência carregada, o `reference_present` do `commands` nomeia a carregada que o menu já recusa. Arquivo no disco não é a skill. Sem chave `carregada`.

[`commands.json`](commands.json) é o catálogo: categoria, descrição, dica de
argumentos, focos do `context` e leituras canônicas. Ele alimenta `game.py commands`
(menu em JSON), `pin`/`unpin` (atalhos no host) e a checagem `commands` do `doctor`,
que exige catálogo, arquivo e linha na tabela do `SKILL.md` em acordo. `pin` não copia a skill. Se o README recusa que o pin copie a skill, o `created` do `pin` nomeia a cópia que o README já recusa. Atalho no disco não é a skill. Sem chave `cópia`. Se o README recusa sobrescrever skill sua com o mesmo nome, o `pin` nomeia a própria que o README já recusa. Atalho no disco não é a skill. Sem chave `própria`.

## Contrato de uma referência

Uma referência é um **orquestrador fino**: diz qual `context` rodar, qual receita ler,
onde parar para o usuário, o que prova conclusão e o que não fazer. Ela não repete a
receita; aponta o canônico. Seções obrigatórias, nesta ordem (o teste confere):

1. Uma frase de abertura: o que o comando faz e quando usá-lo.
2. `## Escala` — o que muda entre `jam`, `product` e `aa`. O piso do verbo nunca muda.
3. `## Avaliar` — o que ler e rodar antes de decidir; as perguntas que param a
   execução (`STOP` e pergunta estruturada) e as que se assumem com registro.
4. `## Executar` — passos, apontando receitas, templates e comandos do harness.
5. `## Verificar` — a prova que encerra o comando e o que **não** conta como prova.
6. `## Nunca` — recusas específicas do comando, além das do `SKILL.md`.
7. `## Entregar` — o que apresentar, o registro canônico a atualizar e o comando
   seguinte natural (a maioria passa por `polish` ou `next`).

Uma referência que precisa de mais seções pode acrescentá-las entre `Avaliar` e
`Executar` (`## Planejar` é a mais comum). Nenhuma referência concede degrau, marco,
gate, aprovação artística ou publicação: quem faz isso é pessoa com prova ligada.

## Adicionar um comando

1. Entrada em `commands.json` com categoria existente, `foci` válidos e `reads`
   apontando arquivos reais.
2. `commands/<nome>.md` com as seções acima.
3. Linha na tabela **Comandos** do `SKILL.md`, ligando `commands/<nome>.md`.
4. `python3 scripts/game.py doctor --root <lab>` verde na checagem `commands` e
   `python3 -m unittest tests.test_commands`.

Comando que só repete uma receita não merece existir: a receita já é selecionada por
`--focus`. Um comando existe quando há um **fluxo** (ordem, paradas, prova, entrega)
que a receita sozinha não dá.
