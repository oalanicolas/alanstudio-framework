---
tipo: processo
resumo: "Como copiar este vault, abrir no Obsidian e provar que o cérebro funciona: check, índice, busca e grafo. O exemplo Hexa Drop/Oficina é inventado."
temas:
  - processo
status: vigente
data: 2026-09-19
---
# Como replicar

Esta pasta **é** o vault. Não mora dentro de `docs/` de outro repositório. Copie-a,
abra-a no Obsidian e os comandos passam sem o laboratório de origem.

O exemplo ([[Hexa Drop]], [[Oficina]], [[Peça que encaixa]]) é **inventado**. Serve
para exercitar o contrato. Troque-o pelos seus jogos. Não copie IP de terceiros
para o vault.

## Copiar

```sh
cp -R assets/cerebro ~/MeuCerebroDeJogos
# ou, a partir deste diretório:
cp -R . ~/MeuCerebroDeJogos
```

A cópia não precisa do `alanstudio-framework`. Python 3.10+ e Obsidian 1.9+ (Bases)
bastam. Sem Obsidian, o `cerebro.py` continua a validar.

## Abrir

1. Obsidian → *Open folder as vault* → a pasta copiada.
2. Cmd/Ctrl+P → *Reload app without saving* se as cores do Graph não baterem com a
   [[Legenda do grafo]].
3. Porta: [[00 Comece Aqui]].

## Provar

Na raiz da cópia:

```sh
python3 _sistema/cerebro.py check     # saída 0, sem ERROS
python3 _sistema/cerebro.py indice    # regenera Índice.md
python3 _sistema/cerebro.py buscar --jogo oficina
python3 genealogia-jogos/_kit/exportar_grafo.py --check
```

`check` sem erros é o critério de réplica. Avisos (órfãs, resumo longo) não falham.
`--nivel erro` mostra só o que quebra agora; `--json` devolve código, arquivo e linha.

A cópia já vem com `.claude/settings.json`: num harness com hooks, cada edição de nota
dispara `_sistema/hook_pos_edicao.py`, que devolve ao agente os problemas **daquele**
arquivo. Sem harness, nada muda — o arquivo é inerte e o `check` continua manual.
Se copiar de novo a cópia, os mesmos comandos passam: o kit não depende de caminhos
absolutos nem do hub privado.

Depois do `check` verde, a densidade vem de [[Como crescer]] — não de copiar
`docs/` do laboratório de origem.

## Primeiro uso real

1. Apague ou substitua os nós de exemplo em `genealogia-jogos/nos/` e as notas em
   `estudos/`, `padroes/`, `evidencias/`, `aprendizados/` que citam Hexa Drop/Oficina.
2. Crie o seu jogo com o modelo [[_sistema/modelos/grafo/Jogo nosso|Jogo nosso]]
   (tag `nosso`, `projeto:` com a pasta do código).
3. Estudo novo: modelo [[_sistema/modelos/Estudo|Estudo]].
4. `python3 _sistema/cerebro.py check` e `indice`.
5. Aresta nova: `python3 genealogia-jogos/_kit/exportar_grafo.py`.

Contrato: [[Processo]]. Agentes: [[AGENTS]]. Crescimento: [[Como crescer]].
