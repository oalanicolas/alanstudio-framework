---
tipo: processo
resumo: "Como o cérebro funciona: o ciclo capturar → classificar → conectar → destilar → aplicar → revisar, o contrato de metadados, onde nasce cada tipo de nota e os comandos de manutenção."
temas:
  - processo
status: vigente
---
# Processo

O cérebro existe para três coisas:

1. **Refinar os jogos.** Uma IA que vai mexer num jogo acha, em um comando, o que
   o estúdio já aprendeu que serve a ele.
2. **Achar a informação.** Abrir o Obsidian e chegar em dois cliques ao estudo, à
   decisão ou à prova.
3. **Ver os padrões.** O que se repete entre estudos e jogos sobe para [[Padrões]],
   para o grafo ou para uma regra canônica, em vez de ficar enterrado num dossiê.

O resto deste arquivo é o como. Réplica: [[Como replicar]].

## Estrutura

Como no grafo de genealogia: **a pasta diz o tipo, o nome diz o que é.** Não existe
pasta por estudo nem arquivo chamado `README`, `ESTUDO` ou `LEIA-ME`.

| Pasta | `tipo` | Nome do arquivo |
|---|---|---|
| `estudos/` | estudo | `Estudo <Referência>` na porta; `<Referência> — <aspecto>` em cada parte |
| `pesquisas/` | pesquisa | `<Ferramenta ou método> — <o que avalia>` |
| `aprendizados/` | aprendizado | o tema |
| `planos/` | plano | `<Jogo ou produto> — <o que planeja>` |
| `identidade/` | identidade | a peça de direção visual |
| `operacao/` | operacao | o assunto |
| `aulas/` | aula | `Aula NNNN — <tese>` ou `Assunto — <parte>` |
| `registros/` | registro | `<Assunto> — <parecer, resultado, relato>` |
| `evidencias/` | evidencia | `<Referência> — <o que a ficha mostra>` |
| `padroes/` | padrao | o princípio em uma frase |
| `genealogia-jogos/nos/<tipo>/` | jogo, ludema, pessoa, estudio, mito, obra | o nome da entidade |
| `genealogia-jogos/visoes/` | visao | o recorte |
| `_anexos/<origem>/` | nenhum | JSON, scripts, imagens; fora da busca e do Graph |
| `_entrada/` | captura | livre; sai na revisão semanal |
| raiz | hub, processo | portas: Comece Aqui, Índice, Padrões, Processo, AGENTS |

Regras de nome, conferidas pelo `check`:

- **Único no vault.** O wikilink é sempre `[[Nome]]`, sem caminho.
- **Diz o que é sem abrir.** `Assunto — aspecto`, com travessão, em português. Sem
  `:` `/` `#` `|` `[` `]`.
- **O `# título` é o nome do arquivo.** Contexto extra vai no `resumo`.
- **Parte aponta para a porta** com `parte_de: "[[Estudo X]]"`; a porta lista as partes.
- **Anexo não é nota.** Arquivo que não é Markdown vai para `_anexos/<origem>/`.

## O ciclo

```
capturar → classificar → conectar → destilar → aplicar → revisar
```

### Capturar

- Ideia, link, trecho, print: nota nova no Obsidian. Cai em `_entrada/` com o modelo
  [[_sistema/modelos/Captura|Captura]].
- Estudo pedido: `estudos/Estudo <Referência>.md` a partir do modelo
  [[_sistema/modelos/Estudo|Estudo]]. Cada parte vira
  `estudos/<Referência> — <aspecto>.md`; fichas vão para `evidencias/`; dados, para
  `_anexos/<referência>/`.
- Arquivo pesado: fora do Git. No vault ficam o link, o hash e como recuperar.
- Material privado: só as conclusões. Sem contato pessoal nem trecho sobre terceiros.

### Classificar

Toda nota fora do grafo tem este frontmatter.

```yaml
tipo: estudo
resumo: "Uma ou duas frases: o que tem aqui e para que serve."
jogos:
  - "[[Oficina]]"
temas:
  - combate
status: vigente
data: 2026-09-19
referencias:
  - "[[Hexa Drop]]"
parte_de: "[[Estudo Hexa Drop]]"
substituido_por: "[[…]]"
canonico: references/performance.md
```

`jogos` responde "serve a qual jogo nosso?"; `referencias` responde "estuda qual
jogo de fora?". As duas alimentam a tabela *No cérebro* no nó do jogo. Vocabulários
fechados: `_sistema/cerebro.py`. Tipos das propriedades: `.obsidian/types.json`.

| `tipo` | Quando |
|---|---|
| `estudo` | dossiê sobre referência externa: jogo, plataforma, mercado, pessoa |
| `pesquisa` | avaliação de método, ferramenta ou tecnologia para o nosso fluxo |
| `aprendizado` | lições de casos nossos, com prova |
| `plano` | PRD, plano de execução, visão de produto, desenho de jogo em estudo |
| `identidade` | bíblia, design system, banco de referências de arte |
| `operacao` | workspace, acervo, publicação, analytics, catálogo |
| `aula` | material de ensino |
| `registro` | parecer, revisão, relato, story, experimento concluído |
| `evidencia` | ficha, inventário, fonte primária organizada |
| `padrao` | princípio que se repete; leva `familia` (design, metodo, armadilha) e `forca` (confirmado, candidato) |
| `hub` · `visao` · `processo` | navegação, recorte do grafo, método |
| `captura` | entrada crua em `_entrada/` |

| `status` | Significa para quem lê |
|---|---|
| `vigente` | pode usar como referência atual |
| `em-andamento` | trabalho aberto; conferir a data |
| `rascunho` | proposta não aprovada |
| `historico` | registro de um momento: vale como prova, não como orientação |
| `superado` | substituído; seguir `substituido_por` |

`temas`: `design`, `combate`, `progressao`, `economia`, `level-design`, `narrativa`,
`mitologia`, `arte`, `animacao`, `audio`, `feel`, `performance`, `engenharia`,
`multiplayer`, `ia`, `processo`, `publicacao`, `ugc`, `juridico`, `video`, `ensino`.
Tema novo entra primeiro em `TEMAS` no `cerebro.py` e nesta lista.

`jogos` aceita só nós com a tag `nosso`. Jogo nosso novo: modelo
[[_sistema/modelos/grafo/Jogo nosso|Jogo nosso]] (`projeto:`, tabela *No cérebro*).

### Conectar

- A nota aponta para o **nó do jogo** (`jogos:`) e, se for parte, para a mãe (`parte_de:`).
- Influência entre jogos é aresta na tabela *Recebeu de* do nó, com fonte e confiança
  A–D ([[Genealogia]]). Link no texto não substitui aresta.
- Toda afirmação importante leva o rótulo da origem ([[Rotular cada afirmação pela origem]]).

### Destilar

No fim de cada estudo:

1. Já apareceu em outra fonte? Vira ou reforça uma nota em `padroes/`.
2. Mecânica que dois jogos carregam? Ludema no grafo.
3. Método que serve a outros jogos? A regra vai para o canônico (harness, receita);
   a nota guarda o caso e ganha `canonico:`.

**Invariante não é padrão observado.** No estudo e no ludema, separe o contrato — sem
ele o mecanismo deixa de ser aquilo — da regularidade vista nas peças, cada uma com o
`n` ao lado. `n=1` e `n=2` são hipótese: não se cobra um jogo nosso por elas. Cristalizar
a regularidade de dois exemplos é o erro que depois reprova toda peça nova por não
encaixar. O `check` avisa quando um ludema não tem a seção *Invariante*, e o grafo avisa
quando só um jogo o carrega.

**Toda regra tem fronteira.** Nota em `padroes/` diz onde **deixa de valer** — o caso em
que segui-la piora o jogo. Em `armadilha`, diz também a instância proibida, na forma em
que apareceu. Sem fronteira, o `check` avisa: regra sem limite vira dogma e volta como
veto três semanas depois.

**Erro que se repete e veto viram registro.** Duas vezes o mesmo erro: padrão `armadilha`
com o caso, a instância e a fronteira. Proposta recusada: uma linha em `registros/` com
dono, data e motivo — para a ideia recusada não voltar como novidade.

### Aplicar

- Antes de mexer num jogo: `python3 _sistema/cerebro.py buscar --jogo <pasta>`.
- O que o jogo decide copiar, adaptar ou recusar fica na seção *Tradução para o
  nosso jogo* do estudo e no documento do jogo. O estudo **não é cânone** do jogo.

### Revisar

Uma vez por semana:

1. Esvaziar `_entrada/` ([[Entrada]]).
2. `python3 _sistema/cerebro.py check`
3. `python3 _sistema/cerebro.py indice`
4. Se houve aresta nova: `python3 genealogia-jogos/_kit/exportar_grafo.py`
5. [[Padrões#Candidatos]]: algum ganhou segunda fonte?

O `check` também diz o que **parou de andar**, no nível `info`: `CANDIDATO_PARADO` (padrão com
uma fonte só passou do prazo), `STATUS_PARADO` (um mesmo status em quase todo nó — o ritual não
acontece), `ESTUDO_SEM_FICHA` (síntese sem nenhuma ficha em `evidencias/`) e `LINK_PARTIDO`
(wikilink aberto numa linha e fechado noutra). Os prazos ficam em `_sistema/cerebro_config.json`.


## Bases: listas vivas

**Lista que dá para derivar de propriedades é uma Base, não uma lista escrita à mão.**
A lista à mão envelhece. Texto curado (ordem de leitura, tese de uma visão) continua
em prosa, ao lado da Base.

| Onde | O que a Base mostra | Filtro |
|---|---|---|
| [[00 Comece Aqui]] | galeria dos nossos jogos | `file.hasTag("nosso")` |
| cada nó de jogo, *No cérebro* | tudo do cérebro sobre aquele jogo | `jogos.contains(this)` ou `referencias.contains(this)` |
| cada porta de estudo, *Todas as partes* | as partes do estudo | `parte_de == this` |
| cada ludema, *Quem carrega* | jogos e padrões ligados | `file.hasLink(this)` / `ludemas.contains(this)` |
| [[Padrões]] | confirmados e candidatos | `file.inFolder("padroes")` |
| [[Estudos de referência]] | portas de estudo | `file.inFolder("estudos")` sem `parte_de` |
| [[Catálogo.base\|Catálogo]] | todas as notas | vault inteiro |
| [[genealogia-jogos/Atlas.base\|Atlas]] | nós do grafo, nossos, sem linhagem | `genealogia-jogos/nos/` |

Bases não aparecem para agentes que leem Markdown cru. Para eles: [[Índice]] e
`cerebro.py buscar`.

## Onde nasce cada coisa

| Coisa nova | Onde | Modelo |
|---|---|---|
| Estudo de referência | `estudos/Estudo <Referência>.md` + partes | [[_sistema/modelos/Estudo\|Estudo]] |
| Pesquisa de referência pedida para um jogo | `estudos/` com `jogos:`, **nunca** `games/<pasta>/docs/research/` | [[_sistema/modelos/Estudo\|Estudo]] |
| Jogo, pessoa, estúdio, mito, obra | `genealogia-jogos/nos/<tipo>/` | `_sistema/modelos/grafo/` |
| Mecânica de 2+ jogos | `genealogia-jogos/nos/ludemas/` | [[_sistema/modelos/grafo/Ludema\|Ludema]] |
| Recorte do grafo com 5+ nós | `genealogia-jogos/visoes/` | skill `build-moc` |
| Aprendizado de caso nosso | `aprendizados/` | [[_sistema/modelos/Nota\|Nota]] |
| Pesquisa de ferramenta ou método | `pesquisas/`; runs em `_anexos/<pesquisa>/runs/` | [[_sistema/modelos/Nota\|Nota]] |
| Plano, PRD, desenho ainda sem pasta | `planos/` | [[_sistema/modelos/Nota\|Nota]] |
| Parecer, resultado, relato | `registros/` | [[_sistema/modelos/Nota\|Nota]] |
| Ficha, inventário, fonte | `evidencias/` | [[_sistema/modelos/Nota\|Nota]] |
| Identidade visual | `identidade/` | [[_sistema/modelos/Nota\|Nota]] |
| Aula | `aulas/` | [[_sistema/modelos/Nota\|Nota]] |
| Operação do estúdio | `operacao/` | [[_sistema/modelos/Nota\|Nota]] |
| Padrão | `padroes/` | [[_sistema/modelos/Padrão\|Padrão]] |
| Doc de produção de um jogo | **fora daqui**: `games/<pasta>/docs/` | |
| Método reutilizável de *fazer* o jogo | **fora daqui**: harness / `canonico:` | |

Crescer até um vault denso: [[Como crescer]].

## Regras que evitam estrago

- **Não mover com `mv`.** Use `cerebro.py mover` (ou `migrar` em lote). Recibos
  históricos não se reescrevem: `cerebro.py onde` traduz o caminho antigo.
- **Nada pesado no Git.** Vídeo, render e captura ficam fora; no vault, o link e o hash.
- **Não é cânone.** Estudo informa, o documento do jogo decide. Padrão sugere, o jogo testa.
- **Nada de hipótese promovida sem prova.** `inspirou` exige A/B. Sem citação: `linhagem`
  ou `parece`. Ver [[Clonar o que se vê]].
- **Jogo órfão é válido.** Um jogo nosso sem aresta (como [[Folha em Branco]]) não
  ganha influência inventada só para o Graph ficar bonito.

## Comandos

```sh
python3 _sistema/cerebro.py check
python3 _sistema/cerebro.py check --nivel erro        # só o que quebra agora
python3 _sistema/cerebro.py check --json              # itens com código, arquivo e linha
python3 _sistema/cerebro.py indice
python3 _sistema/cerebro.py buscar --jogo oficina
python3 _sistema/cerebro.py mover ORIGEM DESTINO --titulo
python3 _sistema/cerebro.py cores
python3 genealogia-jogos/_kit/exportar_grafo.py
```

Não mover com `mv`. `mover` reescreve os wikilinks.
