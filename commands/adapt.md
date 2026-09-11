# Adapt

Levar o jogo a outro dispositivo, entrada ou público sem trair o verbo: toque,
gamepad, teclado, remapeamento, uma mão, contraste no pior caso da cena, forma além
da cor, movimento reduzido com sinal de causa preservado, legendas para o que só
existe no som, alvos de toque, escala de texto. Acesso é decisão de design, não
camada final. Receita: [acessibilidade](../recipes/accessibility.md); convenções do
alvo: [pacotes de plataforma](../packs/README.md).

## Escala

`jam`: entrada primária funciona e nenhum estado depende só de cor (`playable`).
`product`: remapeamento, redução de movimento, legendas, alvos de toque (`slice`).
`aa`: contraste verificado, escala de interface, assistência que não esconde
conteúdo e uma declaração honesta do que ainda não atende (`shippable`).

## Avaliar

1. `context <projeto> --focus accessibility`. Leia o pacote da plataforma (entrada,
   resoluções, requisitos de loja na fonte oficial) e os requisitos de qualidade
   do PRD. Barreira concreta primeiro: entrada, visão, audição, movimento, leitura,
   tempo de reação.
2. Jogue como [Sam e Léo](../references/personas.md): mudo, uma mão, movimento
   reduzido, celular mediano com o polegar.
3. Inventário do que existe: tokens de contraste, mixer com legendas, abstração de
   entrada remapeável (o starter `canvas-arcade` traz as três). REUSE antes de sistema
   paralelo.
4. Pergunte só o que o brief não diz: o público prometido e o dispositivo alvo real.

## Executar

Por barreira: entrada (remapear tudo, inclusive menus; alternativa a segurar e
apertar repetido; deadzone ajustável); visão (forma, ícone ou posição acompanham a
cor; contraste medido na cena cheia; foco visível); audição (legenda ou indicador
para toda informação sonora, inclusive ameaça fora da tela; nome de quem fala);
movimento (tremor, paralaxe e flashes desligáveis, com o sinal de causa migrando
para estático); tempo (pausa em qualquer momento seguro; assistência que não
esconde conteúdo); toque (alvos com tamanho, ação principal no alcance do polegar,
estado preservado na interrupção). Movimento bom com mouse pode falhar no toque:
cancelar gesto, perder foco e reconectar controle são cenários próprios.

## Verificar

Sessão com cada modo ativo: mudo, movimento reduzido, uma mão quando aplicável;
verificação de contraste; jogo completável em cada dispositivo alvo com a entrada
real, não emulada. Degraus: `accessibility` na [barra](../references/production-bar.md).
Diretrizes de plataforma citadas pela fonte oficial e versão; guideline de fornecedor
não é certificação.

## Nunca

- Adicionar acesso como anexo depois do conteúdo pronto sem registrar o retrabalho.
- Remover o feedback de causa ao reduzir movimento.
- Esconder conteúdo atrás de "modo fácil".
- Testar toque redimensionando a janela do desktop.
- Inventar requisito de loja ou console; consulte a fonte oficial.

## Entregar

As barreiras tratadas, as sessões por modo, a declaração do que o jogo ainda não
atende, e a tabela atualizada. Sequência: [`clarify`](clarify.md) se a leitura falhou
sem áudio; [`polish`](polish.md).
