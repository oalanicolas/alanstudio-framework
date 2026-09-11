# Content

Fazer o segundo trecho custar menos que o primeiro: receita e pipeline para que o
próximo nível, inimigo, item, tela ou som nasça dentro do piso, com custo
cronometrado, identidade estável, validação e falha legível para dado inválido. Use
quando produzir mais parece heroísmo. Receita: [conteúdo](../recipes/content.md);
contrato: [design system do jogo](../references/game-design-system.md).

## Escala

`jam`: conteúdo separado da regra, como dado (`playable`). `product`: receita e
ferramenta para nascer um item novo, custo do próximo conhecido (`slice`). `aa`: a
slice prova **repeatability** — outro trecho nasce no mesmo padrão, pela receita,
sem intervenção excepcional — antes de multiplicar.

## Avaliar

1. `context <projeto> --focus content`. Leia o formato atual, a carga em runtime, os
   consumidores e a receita por família no Art Bible (se falta, [`document`](document.md)).
2. Que família está sendo produzida (personagem, nível, efeito, tela, som) e qual foi
   o custo real do último item dessa família? Sem cronômetro, é chute.
3. Pipeline: fonte → importação → validação → runtime. Onde cada validação roda,
   convenções de nome, escala/pivot, compressão, LODs. Geração ou importação
   assíncrona: pronto no serviço, baixado, validado e consumido são estados diferentes.
4. Narrativa: como escolhas dependem do histórico, quando efeitos se aplicam, o que
   um save restaura; versão da história e do save são contratos distintos.
5. Pergunte só o que a receita não fixa: a quantidade pretendida e o que não pode
   variar entre itens.

## Executar

Produza **um item pela receita**, cronometrando. Preserve identidade, escala, pivot,
colisões, animações e referências ao trocar arte; use o caminho e o nome que o
serviço retornou; valide integridade antes de promover arquivo temporário; preserve
master e versão anterior. Som novo passa por `sfx search` e traz proveniência.
Conteúdo inválido de propósito: o jogo falha de forma legível, sem quebrar. Adapte
as ferramentas da engine antes de criar pipeline próprio.

## Verificar

O item novo carregado no cenário real, consumido pelo consumidor certo, comparado em
movimento ao hero; o custo cronometrado registrado; o dado inválido carregado de
propósito. Arquivo gerado não prova consumo. Degraus: `content_scale` na
[barra](../references/production-bar.md). Proveniência de tudo que entrou.

## Nunca

- Produzir dez itens à mão e chamar de pipeline.
- Trocar o formato inteiro para absorver a validação de outro editor.
- Presumir nome ou caminho quando o serviço versiona ou renomeia.
- Apagar pixels, quantizar ou redimensionar porque um verificador alertou.
- Copiar arquivo do acervo sem origem e condição de uso.

## Entregar

A receita seguida, o item, o custo, a validação e o que a receita ainda não cobre.
Sequência: [`produce`](produce.md) quando a receita sustenta multiplicar;
[`document`](document.md) se a receita precisou ser inventada no caminho.
