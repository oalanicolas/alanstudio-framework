# Gates de produção

A [barra de acabamento](production-bar.md) descreve **onde o jogo está**. Um gate
diz **o que ainda não pode passar**. São mecanismos diferentes e não se
substituem: a barra é uma leitura, o gate é uma recusa.

Os dez gates deste arquivo não foram inventados aqui. Cada um formaliza uma linha
que já existia em prosa no [ciclo criativo](preproduction.md) — uma frase
`**Pronto para…**` por etapa, com o critério de saída dela. O que faltava era
alguém ler essas linhas e alguém recusar avanço enquanto elas não fossem
cumpridas. Era a mesma situação da barra antes do comando `bar`: vocabulário
escrito, nada que o lesse.

## O que um gate é

Um gate é a permissão que você está pedindo, não a etapa que acabou. Ele tem
nome do que vem depois:

| Gate | Pede | Critério de saída vem de |
| --- | --- | --- |
| `design` | desenhar e experimentar | `brief` — Pronto para desenhar/experimentar |
| `test` | testar a hipótese | `mda` — Pronto para testar |
| `prototype` | prototipar | `gdd` — Pronto para prototipar |
| `close` | encerrar o experimento | `poc` — Pronto para encerrar |
| `implement` | implementar o recorte | `prd` — Pronto para implementar o recorte |
| `build` | construir | `tdd` — Pronto para construir |
| `scale` | ampliar a produção | `vertical-slice` — Pronto para ampliar |
| `evaluate` | avaliar a entrega | `mvp` — Pronto para avaliar a entrega |
| `conclude` | concluir o escopo | `qa` — Pronto para concluir o escopo |
| `deliver` | entregar | `release` — Pronto para entregar |

A ordem é a do ciclo, não alfabética, porque um gate guarda a permissão seguinte
e a sequência é o que dá sentido a “o próximo”. O ciclo tem retorno: reprovar em
`scale` devolve para `build`, e isso é uso normal, não fracasso do processo.

## As três saídas

Um gate com critério pendente tem três respostas legítimas, e a terceira é a que
costuma faltar nos processos:

1. **Passar** — os critérios têm o que os sustenta.
2. **Cortar escopo** — o critério não é alcançável no recorte atual, então o
   recorte diminui até que seja.
3. **Abandonar** — o critério não vale o que custa, e o trabalho para aqui.

Abandonar **não é falha do gate**: é uma das respostas dele. O ciclo já dizia
isso em um lugar — a etapa `poc` fecha com “decisão de continuar, ajustar ou
abandonar a hipótese”. O que este arquivo faz é generalizar: se abandonar é
resposta legítima ao fim de um experimento, também é ao fim de uma fatia que não
sustentou o acabamento pretendido. Um processo que só admite “passou” e “ainda
não” empurra escopo morto para frente até que ele custe caro demais para matar.

A saída escolhida é registrada no devlog, com autor. Nenhum comando escolhe por
você.

## Dispensa, e os quatro critérios sem terceira opção

Produção real dispensa requisito com assinatura, e um processo que finge o
contrário só produz declaração falsa. Então `waived` é um estado de primeira
classe — mas ele exige **motivo escrito**. Dispensa sem motivo é o critério
apagado da lista, que é justamente o que um gate existe para impedir.

Quatro critérios não são dispensáveis, e não por escolha do harness: a prosa da
etapa não deixa terceira opção.

| Gate · critério | O que a etapa diz |
| --- | --- |
| `deliver` · `licensing` | “Licença desconhecida bloqueia a entrega” |
| `implement` · `user_requirements` | “Prioridade não permite remover exigências explícitas do usuário” |
| `conclude` · `human_vs_agent` | “Não registre teste com pessoa quando houve somente simulação ou avaliação do agente” |
| `design` · `reference_origin` | “Origem e autoridade declaradas; ausências são explícitas” — declarar a ausência já é a saída |

Tentar dispensar um desses sai como problema de forma, e o critério volta a
contar como pendente.

## Como declarar, para o harness ler

Uma tabela em `README.md`, `docs/qa.md`, `docs/devlog.md`, `docs/release.md` ou
`docs/prd.md`. Uma linha por critério:

```markdown
| Gate | Critério | Estado | Evidência |
| --- | --- | --- | --- |
| `deliver` | `runbook` | `met` | Ana construiu do zero em 2026-09-02, log em /tmp/qa-07 |
| `deliver` | `foreign_machine` | `unmet` | só rodou na máquina de dev |
| `deliver` | `save_migration` | `waived` | sem versão anterior publicada — Alan, 2026-09-05 |
```

Estados: `met`, `unmet`, `waived`. A última coluna é o que sustenta o estado —
quem observou, quando, e onde está o recibo. `met` sem nada escrito ao lado é
recusado, pelo mesmo motivo que a dispensa sem motivo: um estado sem lastro é
uma linha que só serve para fechar a tabela.

`gate <projeto>` devolve os dez, ou `--gate <nome>` devolve um. Critério sem
linha conta como **pendente**, nunca como cumprido: silêncio não é aprovação.
Duas linhas discordantes sobre o mesmo critério não se resolvem por precedência —
o estado mais fraco vale e o conflito fica listado.

`next` propõe resolver o critério pendente do primeiro gate **declarado** que
tenha algum. Um gate que o projeto não mencionou não está sendo pedido, e listar
os dez num projeto que declarou um transformaria a recusa em ruído.

## Limites

O harness confere a **forma** da declaração e relata em `problems`: gate
desconhecido, critério que não pertence ao gate, estado fora dos três, dispensa
do que não se dispensa, `met` ou `waived` sem nada escrito, e linhas
discordantes. Ele não observa o jogo, não executa nada e **não concede
passagem**.

O campo se chama `held_by_declaration`, não `passed`, de propósito: ele diz que o
projeto afirma cumprir todos os critérios, não que alguém conferiu. Uma tabela
bem formada e otimista sai daqui intacta, como sai da barra. Quem confere é
pessoa ou agente, com autor declarado, e `verify` serve para anexar o recibo do
que for comando.

Um gate cumprido não diz que o jogo é bom. Ele diz que uma condição de avanço
específica tem lastro declarado. Acabamento é a barra; diversão não é nem uma
coisa nem outra, e nada neste repositório mede isso.
