# Visual

Direção de arte e mundo: silhueta, material, luz e animação legíveis em movimento;
câmera que antecipa e não oclui; item novo que nasce pertencendo ao jogo;
referência aprovada sincronizada na base no mesmo turno. Use para arte, HUD, câmera
e mundo. Receita: [visual](../recipes/visual.md); contrato:
[design system do jogo](../references/game-design-system.md).

## Escala

`jam`: placeholders identificáveis como placeholders, escala e pivot consistentes,
direção declarada mesmo com arte provisória. `product`: design system com tokens
que têm consumidor, famílias e receita (`slice`). `aa`: um implementador que não
participou da direção produz o próximo item dentro do piso, e a comparação em
movimento confirma.

## Avaliar

1. `context <projeto> --focus visual`. Leia a referência aprovada, seu alcance
   exato e o que a aprovação não cobre; o Art Bible; os consumidores reais de
   tokens (paleta sem import não descreve a UI ativa).
2. Cena física em uma frase: onde o jogador está, com que luz, em que humor, no
   dispositivo alvo. Se a frase não força escolhas de contraste, escala e paleta,
   ela ainda é vaga.
3. **Teste de reflexo:** se alguém adivinha a paleta e o estilo pelo gênero
   ("horror → dessaturado escuro", "casual → pastel arredondado"), é o primeiro
   reflexo. Se adivinha pela categoria mais a anti-referência ("plataforma que não
   é pixel art → low-poly flat"), é o segundo. Reformule até nenhum dos dois ser óbvio.
4. Aprovação é evento da conversa: quando o usuário aprovar imagem, conceito ou
   recorte, `--event direction-approved` e a base sincronizada **neste turno**
   ([roteiro](../references/project-audit.md#aprovação-de-direção-materializar-e-continuar)).
   Salvar a imagem não é o trabalho. Se o visual recusa que salvar a imagem seja o trabalho, a área `art_direction` do `scan` nomeia a imagem que o visual já recusa. Imagem no disco não é a aprovação. Sem chave `imagem`.
5. Pergunte só o que a referência não diz: o que não pode degradar; anti-referências
   nomeadas; o hero asset que serve de régua.

## Executar

REUSE em materiais, modelos, efeitos, tokens e métodos coerentes com a direção;
ADAPT nos consumidores antes de variantes paralelas. Silhueta e forma antes de cor
e texto; landmarks para orientação; ameaças e caminhos legíveis em movimento.
Câmera: antecipação de curvas e ameaças, oclusão do jogador, estabilidade, escala,
transição. Compare em movimento com o hero asset **no engine**, não no DCC. Feel e
mix têm receitas próprias; partícula e loop de fundo não os substituem.

## Verificar

Captura em movimento nas mesmas condições (versão, resolução, dispositivo, trecho,
luz); teste em escala de cinza para legibilidade; o item novo comparado ao hero. A
qualidade aprovada é o piso: nada se corta para número. Degraus: `art_direction` e
`legibility` na [barra](../references/production-bar.md).

## Nunca

- Aprovar direção por inspeção de arquivos ou por hipótese do agente.
- Rebaixar arte aprovada para "ganhar FPS"; isso é [`optimize`](optimize.md)
  procurando implementação melhor.
- Título, paleta e HUD novos como prova de experiência nova.
- Placeholder que fica sem ser declarado como placeholder.
- Paleta de reflexo do gênero sem uma frase de cena que a justifique.

## Entregar

A direção declarada e seu alcance, a comparação em movimento, os tokens com
consumidor, e o documento sincronizado. Sequência: [`document`](document.md) para
fixar o sistema; [`content`](content.md) para produzir pela receita;
[`clarify`](clarify.md) se a leitura em movimento falhou.
