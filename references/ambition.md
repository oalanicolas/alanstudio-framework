# Ambição, facilidade e piso AAA

Este framework não é um motor AAA e não fabrica um jogo grande sozinho. Ele é o
contrato que torna a criação com IA **fácil de começar** e **difícil de
rebaixar**: um pedido vira um ciclo jogável; um recorte ambicioso não chama
scaffold de vertical slice.

AAA, aqui, não é orçamento, equipe nem engine. É o **acabamento pretendido**
demonstrado num trecho pequeno: verbo legível, feel da ação, mix audível,
luz/materiais/animação coerentes, conteúdo que se multiplica sem diluir a
direção aprovada. Um conto Canvas pode cumprir esse piso; um open world que
abre sem feel não cumpre.

## O que nos propomos a fazer

- **Interpretar um pedido** e chegar a uma fatia jogável sem exigir que a
  pessoa conheça o harness, preencha nove templates ou escolha uma hierarquia
  de agentes.
- **Preservar a direção** do usuário e a referência aprovada. Hipótese do
  agente não vira decisão; screenshot isolada não vira aprovação.
- **Reusar antes de inventar.** CREATE só entra com lacuna explícita.
- **Provar o que afirma.** Build verde não comprova diversão, arte, reinício,
  rede, direitos nem feel. Experiência sem observação em movimento permanece
  `not_assessed`.
- **Escalar a profundidade ao risco.** Jogo pequeno reúne decisões num
  documento. Projeto com sistemas distintos separa artefatos. A qualidade do
  verbo não é opcional em nenhum dos dois.

O harness recorta contexto, varre a base e corre comandos com recibo. A IA
lê, decide e implementa. A memória fica no jogo. Nenhum dos três mede
diversão nem publica sozinho.

## Fácil sem ser raso

Fácil é **um caminho curto até a primeira decisão jogável**, não a ausência
de critério. Na primeira sessão de um jogo novo:

1. Resolva fantasia, verbo, plataforma e a maior incerteza. Assuma o resto
   com registro; pergunte só o que impede de jogar.
2. Escreva ou adapte um brief curto (ou a seção equivalente). Não gere a
   pasta inteira de templates.
3. Construa um ciclo: perceber → decidir → agir → consequência → reinício.
4. Faça essa ação **parecer e soar** a intenção — feel e áudio do verbo,
   mesmo com arte provisória, desde que a direção esteja declarada.
5. Compare em movimento com a referência. Registre o próximo passo único.

Nove documentos vazios atrasam o jogo e não aumentam a qualidade. Uma fatia
jogável sem feel também não: é protótipo, e deve ser nomeada como tal.

Use `context <projeto> --focus create`. Em “continue”, `--event resume`.
Quando a pessoa aprovar imagem, conceito ou recorte, `--event direction-approved`
e sincronize a base no mesmo turno. O usuário não precisa saber esses nomes.

## Escala de ambição

Escolha a escala no brief e mantenha-a visível. Ela governa quantidade de
artefatos e tamanho do recorte — **não** o piso do verbo.

| Escala | Quando | Artefatos | Pronto quando |
| --- | --- | --- | --- |
| **Jam / conto** | Uma sessão, um verbo, pouco conteúdo | Um `game-design.md` pode bastar | Ciclo jogável com feel do verbo e comparação em movimento |
| **Produto** | Entregar valor a jogadores reais | Brief + GDD/MDA, PRD/TDD do recorte, slice, MVP, QA | Vertical slice no acabamento pretendido; MVP com hipótese de valor observável |
| **AAA-shaped** | O recorte precisa sustentar produção longa sem diluir | Os mesmos, com feel, áudio, luz, animação e receita de conteúdo como requisitos do recorte — não “polimento depois” | A slice prova que **outro** trecho nasce no mesmo padrão, com custo e receita compreendidos |

“AAA-shaped” é uma decisão de qualidade e de produção, não uma promessa de
escala de mercado. Reduza quantidade de conteúdo; não reduza o piso aprovado.

Se a escala mudar, atualize o brief e as fronteiras. Não retroaja aprovação
visual de um mock para mecânicas que ninguém jogou.

## Escada até o acabamento

Orientação de dependências, não esteira rígida. Pule um degrau só com motivo
registrado (ex.: PoC técnica antes do GDD).

1. **Fantasia e verbo** — quem o jogador é, o que faz, o que sente.
2. **Ciclo jogável** — uma decisão característica com término e repetição.
3. **Feel do verbo** — a ação tem peso, resposta e recuperação. Receita:
   [feel](../recipes/feel.md).
4. **Áudio da consequência** — causa e efeito também se ouvem; silêncio é
   design. Receita: [áudio](../recipes/audio.md).
5. **Receita de conteúdo** — o próximo inimigo, sala ou efeito nasce sem
   improvisar o piso. Contrato: [design system](game-design-system.md).
6. **Vertical slice no piso** — gameplay, arte, áudio e tecnologia no
   acabamento pretendido, em movimento.
7. **Produção sem diluir** — multiplicar conteúdo pela receita; qualquer
   atalho que quebre o piso é regressão, não velocidade.

PoC investiga incerteza. Scaffold demonstra estrutura. Slice demonstra
experiência. Confundi-los é o modo mais comum de um agente declarar vitória
cedo demais.

## Barras operacionais (não nota)

Selecione as que o recorte afeta. Não some arte + correção + diversão.

- **Verbo:** a escolha muda estado, rota ou expectativa; o risco é legível
  antes da punição.
- **Controle:** entrada, câmera e recuperação sustentam o verbo em cada
  dispositivo alvo.
- **Feel:** antecipação, impacto, câmera, partículas, rumble e silêncio
  tornam a ação inequívoca. Juice que esconde o verbo é regressão.
- **Mix:** camadas (ação, ambiente, música, UI) com ducking e interrupção;
  pause/reinício não deixam voz fantasma.
- **Mundo:** silhueta, material, luz e animação legíveis em movimento;
  landmark e ameaça distinguíveis sem a melhor screenshot.
- **Primeiro minuto:** a primeira ação ensina o verbo sem mural de texto;
  tutorial que bloqueia o jogo não é onboarding.
- **Acesso:** contraste, forma além da cor, foco, toque, movimento reduzido
  quando o recorte os exige.
- **Confiança:** iniciar, pausar, perder, ganhar, reiniciar e sair têm
  consequências definidas.
- **Produção:** um item novo da família segue a receita; proveniência e
  consumidor são rastreados.

O [protocolo](quality.md) registra cenário, condições, referência, evidência
técnica e observação em movimento. Sem essa comparação, declare a lacuna.
Não rebatize uma versão degradada como novo piso. Não chame o recorte de
AAA — nem de “quase AAA” — se a slice não demonstra as barras que a escala
escolheu.

## O que este repositório continua recusando

Não há engine comum, API universal de ações, avaliação automática de
diversão, publicação automática nem hierarquia de agentes. Troca de modelo
com qualidade equivalente continua hipótese. Os estudos externos foram
lidos em recortes; seus testes não foram executados aqui.

O playground da Alan Studios é acervo de famílias e precedentes, não prova
de que este harness produziu aqueles jogos e não base aprovada para copiar
 paleta ou feel.

## Continuidade

- **Onde estamos:** o harness 0.8 cobria processo, scan e arquitetura
  proporcional. Faltavam o caminho curto da primeira sessão, o feel e o
  áudio como focos, e um contrato explícito de ambição.
- **Próximo passo:** ao criar ou elevar um jogo, usar este guia com
  `--focus create` (início), `--focus feel` ou `--focus audio` (acabamento),
  sem gerar documentos que o recorte não precisa.
- **Por que agora:** sem isso, o agente documenta demais e polida de menos,
  ou entrega protótipo como produto.
- **Pronto quando:** a escala está no brief, o ciclo existe, e o próximo
  passo da escada está nomeado com prova.
- **Retomar por:** este guia, [criar](../recipes/create.md),
  [qualidade](quality.md) e a continuidade do próprio jogo.
