---
tipo: processo
resumo: "Instruções para agentes de IA que consultam ou escrevem no cérebro: ordem de leitura, autoridade, onde gravar, metadados e comandos."
temas:
  - processo
  - ia
status: vigente
---
# AGENTS

Esta pasta é um vault Obsidian: estudos de referência, aprendizados com prova,
genealogia dos jogos e padrões. Código e documentos de cada jogo ficam no projeto
do jogo. Métodos reutilizáveis de *fazer* o jogo podem viver num harness à parte.
Contrato: [[Processo]]. Réplica: [[Como replicar]].

## Consultar para refinar um jogo

1. `python3 _sistema/cerebro.py buscar --jogo <pasta>`. Sem terminal: a seção do
   jogo em [[Índice]].
2. Leia o **nó do jogo** em `genealogia-jogos/nos/jogos/<Nome>.md`: tabela
   *Recebeu de*, ludemas e visão.
3. Leia os padrões que agem no jogo (a busca por jogo já lista `padroes/`). Porta:
   [[Padrões]].
4. Abra só as notas cujo resumo responde à tarefa. Notas grandes: `grep -n '^## '`.

Não leia `_anexos/` nem `genealogia-jogos/_kit/dados/` sem motivo. As notas linkam
o anexo quando ele importa.

Todo nome é único: `[[Nome]]` basta.

## Autoridade

| Pergunta | Quem decide |
|---|---|
| O que o jogo é e faz | documentos do jogo (`games/<pasta>/docs/`) |
| O que uma referência externa faz | o estudo (`estudos/`), com rótulo de evidência |
| Como fazer (método, performance, conteúdo) | regra canônica (`canonico:`) ou o harness |
| Regras deste cérebro | [[Processo]] e este arquivo |
| Método sem prova local ainda | [[Métodos herdados]], como regra herdada — não como padrão |

Estudo **não é cânone** do jogo e não autoriza copiar IP. `status: historico` é
prova de um momento. `status: superado` aponta o substituto. Rótulos [O]/[T]/[I]
e A–D: [[Rotular cada afirmação pela origem]]. Features visíveis não são o jogo:
[[Clonar o que se vê]]. Crescimento: [[Como crescer]].

## Escrever

- Onde e com qual modelo: tabela *Onde nasce cada coisa* em [[Processo]].
- Frontmatter: `tipo`, `resumo`, `status`; `data`, `jogos`, `referencias`, `temas`
  quando couber; `parte_de` nas partes.
- Nome do arquivo = o que a nota é, único, igual ao `# título`.
- Influência: aresta no nó (skills em `genealogia-jogos/.agents/skills/`).
- Material privado: só conclusões.

Ao terminar:

```sh
python3 _sistema/cerebro.py check
python3 _sistema/cerebro.py indice
python3 genealogia-jogos/_kit/exportar_grafo.py   # só se mexeu em nós ou arestas
```

Num harness com hooks, `_sistema/hook_pos_edicao.py` já devolve, depois de cada edição,
os problemas **daquele** arquivo (`.claude/settings.json` o liga no `PostToolUse`).
Resolva os que a sua edição causou antes de encerrar; não invente conteúdo para calar um
aviso. Para ler o diagnóstico em máquina: `check --json` (código, arquivo, linha) e
`check --nivel erro`.

## Não fazer

- Mover com `mv`. Use `cerebro.py mover`.
- Gravar documento que só serve a um jogo aqui. O lugar é o projeto do jogo.
- Promover hipótese a fato, `parece` a `inspirou` ou conversa a decisão.
- Criar tema, tipo ou tag fora do contrato sem atualizar [[Processo]] e o `cerebro.py`.
