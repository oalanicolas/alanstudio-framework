# O que torna a experiência boa

Este é um roteiro de concepção e observação. Não é uma fórmula de nota nem um teste
automático de diversão. Selecione critérios que correspondam ao jogo e ao pedido.

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

## Mundo e direção visual

Escala, câmera, silhuetas, materiais, iluminação e áudio formam uma direção coerente.
Landmarks ajudam orientação; ameaças e caminhos precisam ser legíveis em movimento.
A versão visual aprovada é o piso. Não diminua detalhes, sombras, reflexos, animação
ou efeitos para atingir FPS. Investigue implementações mais eficientes e registre
custo quando a expansão visual exigir mais recursos. O
[design system do jogo](game-design-system.md) é o contrato operacional dessa
direção: tokens, famílias, feel e receita de conteúdo novo, não só o moodboard.

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

Origens: o [playground](https://games.alanicolas.com/), os recortes em
[sources.md](sources.md) e a direção de qualidade deste repositório. Os estudos
são referências históricas; suas medições não foram repetidas só por entrarem
neste roteiro.
