# Document

Escrever o design system do jogo a partir do que **existe no código**, para que o
próximo personagem, tela, efeito ou som nasça pertencendo ao jogo: tokens com
consumidor real, famílias do mundo, feel do verbo, mix, UI/acesso, receita de item
novo e proveniência. Gera ou atualiza o Art Bible; não aprova arte.

Contrato do estúdio: [design system do jogo](../references/game-design-system.md).
Template: [art-bible](../assets/templates/art-bible.md).

## Escala

`jam`: as seções do design system cabem no `game-design.md` ou no README; arquivo
separado é opcional. `product`: Art Bible próprio, com tokens rastreados até o
consumidor. `aa`: a **receita de conteúdo novo** (repeatability) é obrigatória e
testada produzindo um item; sem ela a slice não fecha.

## Avaliar

1. `context <projeto> --focus visual`. Leia o brief (fantasia, tom, referências
   aprovadas e seu alcance) e o candidato de `art_direction` no `scan`.
2. Dois modos, decididos pela varredura: **scan** quando há arte, código e
   consumidores para extrair; **semente** quando o projeto ainda não tem sistema
   visual (produz um esqueleto marcado como semente, a refazer quando houver código).
   Não troque de modo em silêncio; diga qual está usando.
3. Extraia o que se extrai: paleta usada de fato (não o arquivo de paleta sem
   import), escalas e pivots, tempos de animação, tokens de câmera, buses e ducking
   do mixer, famílias que se repetem, HUD e menus, sinais de acesso existentes.
   Localize o **consumidor** de cada token; paleta sem uso não descreve o sistema.
4. Pergunte só o que não se extrai, numa rodada estruturada: metáfora que nomeia
   o sistema, o que a direção rejeita, caráter dos materiais e da luz, feel em uma
   frase, um exemplo que cabe e um que quebra.
5. Art Bible existente: mostre-o e pergunte se refresca, sobrescreve ou funde.

## Executar

Preencha as nove seções do contrato: autoridade (referências, quem aprovou, o que a
aprovação não cobre, o que não pode degradar); tokens com caminho do consumidor;
componentes do mundo e como um item novo nasce; feel/feedback ligado ao verbo do
GDD ([feel](../recipes/feel.md)); áudio/mix com papéis e interrupção
([áudio](../recipes/audio.md)); UI/HUD/acesso ou a decisão de não ter; fazer/não
fazer com exemplos concretos; proveniência; verificação (cenário de comparação em
movimento, mesmas condições). Direção, câmera e mundo: [visual](../recipes/visual.md).

Regras nomeadas são mais fortes que listas: "A regra do impacto no quadro: flash,
hitstop e som disparam no mesmo quadro do contato, ou não disparam." Voz de
direção de arte, com valor exato entre parênteses ("aterrissagem: 4 quadros de
squash (67 ms)").

## Verificar

Produza **um item novo pela receita** e compare em movimento com o hero asset, no
engine, não no DCC. Se o item nasceu sem improvisar o piso, o sistema existe. Se o
implementador precisou perguntar, a seção que faltou é a lacuna. Rode `context` de
novo para a sessão usar o documento fresco.

## Nunca

- Documentar tokens sem consumidor ou componentes que não existem no jogo.
- Duplicar o GDD: ele diz o que o jogador faz; aqui diz como se parece, soa, pesa e
  se multiplica.
- Exigir Storybook, tokens CSS ou biblioteca web de um jogo que não os tem.
- Aprovar direção por inspeção de arquivos; a aprovação é evento da conversa
  (`--event direction-approved`).
- Sobrescrever um Art Bible sem perguntar.

## Entregar

O documento no canônico, as escolhas não óbvias (nomes descritivos, regras nomeadas,
o que o sistema recusa), e o item novo produzido como prova. Ofereça refinar
seções. Sequência natural: [`content`](content.md) para produzir pela receita, ou
[`visual`](visual.md) para uma direção que ainda não fechou.
