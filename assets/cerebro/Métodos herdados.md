---
tipo: processo
resumo: "Nove regras de método e de armadilha validadas em outro laboratório e sem prova neste vault: o que cada uma diz, como se cumpre e o que exige para virar padrão em padroes/."
temas:
  - processo
status: vigente
data: 2026-09-19
---
# Métodos herdados

Estas regras não nasceram aqui. Vêm de um laboratório que rodou dezenas de estudos e
pareceres, e chegam **sem a prova**: as fontes que as confirmaram ficaram lá, junto com
o IP e o material privado que não se copia ([[Como crescer]]).

Por isso não são padrões. Padrão deste vault tem família, força e evidência local — duas
fontes independentes para `confirmado`, uma para `candidato` ([[Padrões]]). Regra herdada
é orientação de trabalho com a origem declarada, como pede
[[Rotular cada afirmação pela origem]]. Vale desde o primeiro dia; vira padrão quando o
seu caso aparecer.

Duas chegaram com caso dentro do exemplo do kit e por isso já são notas em `padroes/`:
[[Rotular cada afirmação pela origem]] e [[Clonar o que se vê]]. As nove abaixo, não.

## Estudar uma referência

| Regra | O que diz | Como se cumpre |
|---|---|---|
| Ler o disco antes da wiki | A fonte primária manda: cliente instalado, script, manual, notas de versão. Wiki e vídeo vêm depois. | Declarar no estudo o que **não** foi feito (sem playtest, sem partida medida). |
| Todo estudo tem o mesmo esqueleto | Versão do objeto, método e limites, legenda de evidência, resposta curta, o que governa e o que não governa, tradução para o nosso jogo, lacunas, próxima ação, fontes. | É o modelo [[_sistema/modelos/Estudo\|Estudo]]. Com as três negações: não é cânone, não autoriza IP, não abre jogo novo. |
| Copiar a regra, não o IP | O estudo traduz o verbo do jogo. Nome, arte, voz, gag e UI de marca ficam com o dono. | Seção de recusas no estudo — e o jogo não usa nada dela. Ver [[Clonar o que se vê]]. |

## Decidir e destilar

| Regra | O que diz | Como se cumpre |
|---|---|---|
| Pareceres independentes, depois consolidação | Dois leitores (ou dois modelos) leem sem ver um ao outro; um terceiro confere o que diverge. | Cada parecer é um `registro`; a consolidação é outro registro, e cita os dois. |
| A regra sobe; o caso fica | Método que serve a outro jogo vai para o harness. O cérebro guarda caso, prova e link. | `canonico:` na nota, receita no harness, nenhuma cópia da receita aqui. |
| Base antes de expansão | Provar um trecho pequeno com acabamento final antes de crescer. | Cenário reproduzível e seed antes de mais sistema. |
| Qualidade aprovada é o piso | Otimizar é tirar trabalho que não aparece na tela. Corte visual não é otimização. | Comparar antes e depois em movimento; registrar o que foi descartado por mudar o visual. |

## Armadilhas

| Regra | O que diz | Antídoto |
|---|---|---|
| Hipótese vira fato no caminho | Um `parece` repetido três vezes vira `inspirou`. Um requisito dito numa conversa vira decisão. | `inspirou` exige confiança A ou B ([[Genealogia]]); `status` e rótulo de evidência em toda nota. |
| O contador de FPS esconde o tranco | Média boa e jogo travando: o defeito está no p99, na primeira aparição de cada objeto ou em quadro repetido. | Medir p99 e o primeiro surgimento; aquecer programas e objetos no preparo. |

## Promover a padrão

1. A segunda fonte independente aparece no seu vault (estudo, evidência, aprendizado).
2. Nota em `padroes/` pelo modelo [[_sistema/modelos/Padrão|Padrão]], com `familia`
   (`metodo` ou `armadilha`), `forca: confirmado`, `evidencias` nas **suas** notas e a
   **fronteira** — onde a regra deixa de valer. O `check` cobra a fronteira.
3. Uma fonte só: `forca: candidato`. Nenhuma: a regra continua aqui.
4. Apague a linha desta tabela. A regra passou a ter casa e prova.
5. `python3 _sistema/cerebro.py check` e `python3 _sistema/cerebro.py indice`.

Com um harness ligado, *A regra sobe; o caso fica* e *Qualidade aprovada é o piso* viram
regra canônica lá, e aqui fica o caso. Ordem de crescimento: [[Como crescer]]. Contrato:
[[Processo]].
