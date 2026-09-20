---
tipo: padrao
familia: design
forca: candidato
resumo: "Acelerar o relógio não substitui apertar o tabuleiro. Só uma fonte neste kit."
jogos:
  - "[[Oficina]]"
ludemas:
  - "[[Peça que encaixa]]"
evidencias:
  - "[[Hexa Drop — postmortem]]"
temas:
  - design
status: vigente
data: 2026-09-19
---
# O timer não substitui o espaço

Hipótese: a punição tem de morar no espaço que resta, não num timer mais rápido.
Neste kit só o postmortem de [[Hexa Drop]] afirma isso. Segunda fonte independente
promove a `forca: confirmado` — até lá, candidato. Ver o confirmado vizinho
[[O tabuleiro pune o encaixe tardio]].

- Verificar: uma sessão em que o timer mata a peça *antes* do tabuleiro apertar
  invalida o padrão.
- Fronteira: enquanto é candidato (`n=1`), não se cobra uma peça nova por ele. Se o
  segundo caso mostrar o contrário, o padrão morre em vez de virar exceção.
- Porta: [[Padrões#Candidatos]].
