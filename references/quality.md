# O que torna a experiência boa

Este é um roteiro de concepção e observação. Não é uma fórmula de nota nem um teste
automático de diversão. Selecione critérios que correspondam ao jogo e ao pedido.

Esta página pergunta **o que observar**. A
[barra de acabamento](production-bar.md) pergunta **quão longe isso foi levado**:
os mesmos temas aparecem lá organizados em cinco degraus por dimensão de ofício,
com a prova que sustenta cada degrau. Use as duas juntas — aqui para decidir o que
importa neste jogo, lá para saber se o que importa está em protótipo ou acabado.
E lembre da regra que mais muda a ordem do trabalho: **o degrau percebido é o
mínimo entre as dimensões, não a média.**

## Verbo, decisão e consequência

O jogador consegue agir, entender as alternativas e perceber por que algo aconteceu?
Uma escolha precisa mudar seu estado, rota, recursos ou expectativa. Verifique se há
uma opção sempre dominante e se o risco é legível antes de punir. Uma travessia,
uma curva e uma escolha narrativa podem cumprir esse contrato de maneiras distintas.

## Controle e feedback

Entrada, movimento e câmera sustentam o verbo central. Observe resposta, continuidade,
orientação, precisão e recuperação de erro. Movimento bom com mouse pode falhar no
toque; cancelar um gesto, perder foco e reconectar um controle são cenários próprios.
Som, animação, luz, efeitos e interface devem tornar causa e consequência perceptíveis
sem esconder a ação. Efeito novo sai de `shared/sfx` no laboratório, se existir; o
piso é gravação licenciada, não 8-bit, chiptune, jsfxr nem Kenney arcade. Verifique
também silêncio, contraste e formas além da cor quando forem necessários para
interpretar o estado.

## Ritmo, aprendizado e domínio

O primeiro ciclo ensina a ação? Há oportunidade de praticar antes de combinar riscos?
Alterne intensidade e recuperação conforme a intenção. Progressão precisa abrir
decisões ou domínio, não apenas aumentar números. Meça comportamentos observados
(hesitação, erro repetido, abandono, estratégia), sem confundir tempo de sessão com
diversão. Um playtest curto bem observado vale mais que uma nota inventada.

## Feel da ação

A ação central precisa de peso, timing e recuperação. Antecipação, impacto
(hitstop, squash, partículas, rumble, stinger) e câmera confirmam o verbo.
Flash, hit-pause, shake, partícula e áudio disparam no **mesmo frame** do
contato; dessincronia vira dois eventos. Juice que esconde a consequência é
regressão. Ajuste um elo por vez e compare em movimento. Screenshot não
comprova feel. Receita: [feel](../recipes/feel.md).

## Mix e silêncio

O jogador ouve causa e efeito. Camadas (ação, ambiente, música, UI) têm
prioridade; pause/reinício não deixam voz fantasma. Silêncio é design, não
arquivo ausente. Piso: gravação licenciada ou direção contemporânea explícita
— 8-bit, chiptune, jsfxr e Kenney arcade não são o padrão. Receita:
[áudio](../recipes/audio.md).

## Mundo, luz e animação

Escala, câmera, silhuetas, materiais, iluminação e animação formam uma direção
coerente. Landmarks ajudam orientação; ameaças e caminhos precisam ser
legíveis em movimento. Antecipação e follow-through da animação pertencem ao
verbo, não só à “beleza”. A versão visual aprovada é o piso. Não diminua
detalhes, sombras, reflexos, animação ou efeitos para atingir FPS. Investigue
implementações mais eficientes e registre custo quando a expansão visual
exigir mais recursos. O
[design system do jogo](game-design-system.md) é o contrato operacional dessa
direção: tokens, famílias, feel e receita de conteúdo novo, não só o moodboard.

## Primeiro minuto e acesso

A primeira ação ensina o verbo. Mural de texto que bloqueia o jogo não é
onboarding. Contraste, forma além da cor, foco, alvos de toque e movimento
reduzido entram quando o recorte os exige — não como anexo depois do “polimento”.

O primeiro minuto também denuncia **latência e pacing**. Spike de frametime
quebra suavidade e desempenho percebido com mais força do que baixar um
preset de textura. Observe input, frame e câmera no trecho real antes de
discutir fidelidade gráfica. Não corte o piso aprovado para “ganhar FPS”.

## Estado e confiança

Iniciar, jogar, pausar, perder, ganhar, reiniciar e sair precisam ter consequências
definidas. Teste o que sobrevive a cada transição: score, timers, entidades, som,
inputs, progresso e conexões. Jogo narrativo precisa respeitar histórico e save;
multiplayer precisa explicitar quem pode agir e quem decide o resultado.

## Acabamento e estabilidade

O que separa um recorte que funciona de um jogo no acabamento pretendido é
observável por disciplina, na plataforma alvo, em movimento e ao longo do tempo:

- **Feel:** latência entrada → resposta medida; a ação central é legível sem ajuda.
  Ver [feel](../recipes/feel.md).
- **Orçamentos:** tempo de quadro (p50/p99), memória, carregamento e tamanho medidos
  com ferramenta, cena e data; desvio só com aprovação registrada.
- **Estabilidade:** soak, reinício repetido, saves inválidos e antigos, perda de foco,
  desconexão e atualização sobre instalação existente, no build exportado.
- **Acesso e localização:** contraste, forma além da cor, foco, toque, movimento
  reduzido, remapeamento, legendas; textos fora do código e fontes com cobertura, ou a
  decisão explícita de um idioma. Consulte as diretrizes da plataforma na fonte oficial.
- **Consistência de conteúdo:** o último asset produzido pertence ao mesmo jogo que o
  primeiro; a receita do design system foi seguida e validada.
- **Proveniência completa:** créditos e licenças de tudo que embarca no build.

Esses critérios entram no [plano de produção](../assets/templates/production-plan.md)
e são revisados por marco ([produção](../recipes/production.md)). O harness não os
mede; pessoa e agente medem, registram e declaram a passagem com a prova ligada.

## Piso da escala, não nota

Jam, produto e AA / Triple-I compartilham o piso do verbo e diferem na
quantidade de conteúdo e de artefatos. “AAA” neste texto é piso de
acabamento, não tier de publisher. Não chame o recorte de AAA — nem de
“quase AAA” — se a vertical slice não demonstra as barras (feel sincronizado,
mix, pacing, mundo, repeatability). Contrato: [ambição](ambition.md).
Scaffold demonstra estrutura; slice demonstra experiência e que outro trecho
nasce sem heroísmo. Confundi-los é declarar vitória cedo demais.

## Protocolo de observação

Para cada critério afetado registre no local de QA existente:

- **Cenário e hipótese:** ação do jogador e mudança esperada.
- **Condições:** versão, dispositivo, resolução, entrada, câmera/rota e seed quando
  seu efeito tiver sido demonstrado. Sem seed verificável, declare a variação.
- **Referência:** captura ou execução anterior equivalente e quem a aprovou; se
  ainda não existe aprovação, registre isso.
- **Evidência técnica:** comando, caso, resultado e limite do que ele cobre.
- **Experiência:** vídeo ou observação em movimento, comportamento percebido,
  problemas e julgamento/autor. Screenshot isolada não comprova animação nem controle.
- **Conclusão:** critério atendido, regressão ou pendência. Não declare aprovação
  do usuário quando só houve avaliação do agente.

E, por rodada de playtest, duas coisas que não são sobre um critério e sim sobre a
observação inteira:

- **Achado, não impressão.** Cada achado nomeia o problema, a evidência, a
  hipótese e a medição. O que não consegue nomear os quatro é impressão, e entra
  como impressão. A cadeia é o formato que a Valve usa nos próprios exemplos
  publicados de Left 4 Dead e Dota 2.
- **Regra de parada declarada, e não número de participantes.** Escreva antes de
  começar o que encerra a rodada — por exemplo, N sessões consecutivas sem
  mudança necessária. Um método de observação sem regra de parada não está
  definido, e é isso que o critério `observation` do gate
  [`evaluate`](gates.md) pede.

**Este framework não prescreve quantas pessoas.** O “cinco usuários” que circula
como regra vem de um artigo cuja conclusão é outra: Nielsen e Landauer estimaram
que 16 avaliações valeriam o custo, com pico de benefício/custo em 4, e o 85%
saiu de um parâmetro ajustado sobre treze conjuntos de dados que não continham
jogo nenhum. Faulkner mediu, empiricamente, cinco usuários achando entre 55% e
99% dos problemas — a faixa é grande o bastante para que o número sozinho não
signifique nada. Ninguém publicou o parâmetro para playtest de jogo. A
procedência está em
[observable-criteria-research.md](observable-criteria-research.md), §5.1 e §5.2;
a regra de parada vem do RITE, §5.3.

Para ligar a observação à versão do jogo, grave-a com
`record --kind observation --field role=human|agent --attach <vídeo>`; o recibo guarda
HEAD, autor, fato e anexos por SHA-256, e não substitui o julgamento registrado acima.

Instrumento: [checklist de piso](aaa-checklist.md). O `context` diz o perfil
em `finish` (núcleo / produto / promessa). `--stage aaa` só imprime o
rascunho inteiro. Não some itens para uma nota.

Origens: o [playground](https://games.alanicolas.com/), os recortes em
[sources.md](sources.md) e a direção de qualidade deste repositório. Os estudos
são referências históricas; suas medições não foram repetidas só por entrarem
neste roteiro.
