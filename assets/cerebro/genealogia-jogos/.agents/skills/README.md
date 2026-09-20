# Skills deste vault

Cinco skills de agente para este cérebro. Derivadas de um pacote genérico de PKM e
reescritas para o grafo de evidência: aqui a unidade é o **nó com aresta tipada**, não
a pasta de anotações. O vault é a raiz de `genealogia-jogos/` (onde ficam `Processo.md`
e `_sistema/`).

| Skill | Para que serve |
| --- | --- |
| `genealogia-grafo` | Nó novo ou defeituoso: modelo, tabela *Recebeu de*, `exportar_grafo.py`. |
| `capture-source` | Fonte entra com procedência e confiança A–D na [[Biblioteca de fontes]]. |
| `connect-notes` | Aresta tipada que passa no teste da frase. Sem link decorativo. |
| `build-moc` | Visão em `visoes/` quando cinco nós pedem uma porta. |
| `review-vault` | Saúde do vault e do Graph sem alterar arquivo. |

## O que não virou skill (e por quê)

A regra vale para qualquer skill que você queira acrescentar:

- **Caminho de outro cofre no código.** Skill que aponta para pasta de sincronização
  ou vault de origem quebra na primeira cópia.
- **Estrutura concorrente.** Hierarquia de pastas, MOC ou taxonomia paralela disputam
  com o contrato do [[Processo]]. Uma estrutura só.
- **O que o `cerebro.py` já faz.** Curadoria, contagem e índice são comando, não
  instrução em prosa: `check`, `indice`, `buscar`.
- **Extração genérica de arquivo.** `capture-source` já cobre artigo, manual e vídeo
  com procedência; despejar `.txt` no vault não.
- **Skill de outro domínio** (apresentação, planilha, design). Este pacote é o cérebro
  de jogos.

## Depois de mexer

```sh
python3 _sistema/cerebro.py check                  # valida também os wikilinks destas skills
python3 genealogia-jogos/_kit/exportar_grafo.py    # só se criou nó ou aresta
```

Toda nota citada aqui existe neste vault: o `check` falha se uma skill apontar para
nota que só existe no laboratório de origem.
