---
tipo: processo
resumo: "Do vault-semente a um cérebro da densidade do estúdio: a ordem, o que cada peça faz e o critério de pronto. Sem copiar o conteúdo de docs/."
temas:
  - processo
status: vigente
data: 2026-09-19
---
# Como crescer

Este kit não traz os estudos do laboratório. Traz o **contrato** com que esse
laboratório foi montado. Seguir esta ordem chega a um vault da mesma *forma*
(portas, grafo com evidência, padrões, bases, busca por jogo). Não chega ao
mesmo *conteúdo* — e não deve.

Réplica vazia: [[Como replicar]]. Contrato: [[Processo]].

## O que “como o de hoje” significa

Um cérebro denso tem, no mínimo:

| Peça | Para que serve | Neste kit, o exemplo |
|---|---|---|
| Porta [[00 Comece Aqui]] + [[Índice]] | dois cliques até a nota | já estão |
| Um jogo `nosso` com `projeto:` e *No cérebro* | a IA acha tudo que serve a ele | [[Oficina]] |
| Um segundo jogo nosso, mesmo órfão | o Graph não inventa linhagem | [[Folha em Branco]] |
| Estudo com porta, partes, [O]/[T]/[I], recusas | referência sem virar cânone | [[Estudo Hexa Drop]] |
| Evidência A antes da aresta `inspirou` | fala do autor, não feeling | [[Hexa Drop — postmortem]] |
| Ludema com 2+ jogos | mecânica que viaja | [[Peça que encaixa]] |
| Padrão confirmado (duas fontes) e um candidato | destilar | [[O tabuleiro pune o encaixe tardio]] · [[O timer não substitui o espaço]] |
| `inspirou` A, `linhagem` C, `parece` D, `fonte` | as setas não se misturam | [[Oficina]], [[Cai-Cai]], [[O Anel]] |
| Mito e obra | fonte cultural, não só jogo | [[O Anel]] · [[Anel e Centro]] |
| Visão com 5+ nós | recorte, não índice | [[Máquina de queda]] |
| Canvas | pôster que o Graph não argumenta | [[Mapa de queda]] |
| Bases | listas que não envelhecem | Catálogo, Atlas, *No cérebro* |
| Pesquisa, plano, aula, identidade, operação, registro, captura | o resto dos tipos | pastas com uma nota cada |
| Método pronto antes do primeiro estudo | não reinventar o que já foi validado | [[Métodos herdados]] |
| `buscar --jogo` + `check` semanal | o cérebro serve à IA e não apodrece | `cerebro.py` |

O laboratório real acrescenta dezenas de estudos e anexos. Isso é *acervo*, não
*framework*. O framework está aqui.

## Ordem (não pule)

1. **Abrir o vault** e passar no `check` ([[Como replicar]]).
2. **O seu primeiro jogo nosso.** Copie o modelo *Jogo nosso*. Preencha `projeto:`,
   tag `nosso`, *No cérebro*. Pode ficar órfão. Não invente aresta.
3. **Uma referência com estudo.** Porta `Estudo <Nome>`, uma parte, uma ficha em
   `evidencias/`. Rótulos [O]/[T]/[I]. Recusas de IP. Tradução em tabela, não em
   parágrafo solto.
4. **Aresta só com evidência.** `inspirou` exige A/B na [[Biblioteca de fontes]]
   *antes* da linha. Sem fala do autor: `linhagem` ou `parece`.
5. **Destilar.** Segunda fonte → padrão `confirmado`. Dois jogos com o mesmo
   contrato → ludema. Método que serve a outro jogo → `canonico:` no harness.
   Regra herdada que ganhou o seu caso sai de [[Métodos herdados]] e vira nota em
   `padroes/`.
6. **Cinco nós no mesmo recorte** → visão em `visoes/`. O Graph sozinho não é
   argumento; o canvas é o pôster ([[Mapa de queda]]).
7. **Mito/obra** só quando a fonte é cultural (texto, figura), não para “enfeitar”.
8. **Segundo jogo nosso.** Pode ser [[Folha em Branco]]: zero arestas, aparece no
   Atlas em *Jogos sem linhagem*.
9. **Os outros tipos**, quando existirem: pesquisa de ferramenta, plano, aula,
   identidade, operação, registro. Não crie a pasta vazia à mão — a nota cria a pasta.
10. **Ritual semanal.** `_entrada/` vazia, `check`, `indice`, export do grafo,
    candidatos em [[Padrões]].

Pronto quando `buscar --jogo <pasta>` devolve estudo, padrão e evidência para cada
jogo com trabalho, o Atlas distingue nossos / referências / sem linhagem, e o
`check` não tem ERROS.

## O que não copiar do laboratório de origem

- Estudos de cliente instalado, dumps, prints, GLB, Lua.
- Planos de produto, identidade de marca, operação, analytics.
- Material privado (conversa, mentoria).
- IP de terceiros. O exemplo Hexa Drop é inventado precisamente por isso.

## Ligação com o harness

O cérebro *guarda*. O harness *faz*. Quando um método atravessa jogos, a regra vai
para o canônico (`canonico:`) e a nota daqui fica com o caso. Não duplique a
receita no vault.
