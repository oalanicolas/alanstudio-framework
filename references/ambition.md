# Ambição, facilidade e piso de acabamento

Este framework não é um motor AAA e não fabrica um jogo grande sozinho. Ele é o
contrato que torna a criação com IA **fácil de começar** e **difícil de
rebaixar**: um pedido vira um ciclo jogável; um recorte ambicioso não chama
scaffold de vertical slice.

Há **dois sentidos** de AAA. Misturá-los é o modo mais comum de um agente
usar o adjetivo no vazio.

1. **Tier de mercado.** Rótulo financeiro, sem órgão certificador. Nasceu no
   varejo dos anos 1990, copiado da nota AAA de crédito: publisher médio/grande,
   orçamento e marketing acima do resto. Em 2023–26 o piso citado gira em
   centenas de milhões, equipes de centenas, ciclos de vários anos. Esse tier
   é perfil de risco. Não promete diversão, originalidade nem ausência de bug.
2. **Piso de acabamento.** O que o jogador chama de “qualidade AAA”: cada
   sistema tratado como cidadão de primeira classe; primeiro minuto competente
   (input, frame, câmera); feel e áudio no mesmo frame do impacto; mundo
   legível em movimento; consistência de família; transições sem costura;
   confiança (save, UI, erro). Um conto Canvas pode cumprir esse piso. Um
   open world de orçamento AAA que abre sem peso na ação não cumpre.

Neste repositório, “AAA” **só** significa o segundo sentido, e só depois da
vertical slice demonstrar as barras da escala escolhida. Não chame o recorte
de AAA, “quase AAA” ou AAAA por trailer, engine, ray tracing ou quantidade
de conteúdo. AAAA não tem definição acordada; é buzzword.

O alvo honesto para criação com IA é **AA / Triple-I com piso de acabamento**:
escopo focado, receita repetível, mesmo critério de fatia. *Hellblade*,
*A Plague Tale* e *Clair Obscur: Expedition 33* são precedentes de mercado
desse território — não *GTA* nem live service de publisher. Fontes e limites:
[mapa](sources.md#aaa-tier-e-piso-09).

## O que nos propomos a fazer

- **Interpretar um pedido** e chegar a uma fatia jogável sem exigir que a
  pessoa conheça o harness, preencha nove templates ou escolha uma hierarquia
  de agentes.
- **Preservar a direção** do usuário e a referência aprovada. Hipótese do
  agente não vira decisão; screenshot isolada não vira aprovação.
- **Reusar antes de inventar.** CREATE só entra com lacuna explícita.
- **Provar o que afirma.** Build verde não comprova diversão, arte, reinício,
  rede, direitos, feel nem pacing. Experiência sem observação em movimento
  permanece `not_assessed`.
- **Escalar a profundidade ao risco.** Jogo pequeno reúne decisões num
  documento. Projeto com sistemas distintos separa artefatos. A qualidade do
  verbo não é opcional em nenhum dos dois.

O harness recorta contexto, varre a base e corre comandos com recibo. A IA
lê, decide e implementa. A memória fica no jogo. Nenhum dos três mede
diversão, publica sozinho ou promove o jogo ao tier de mercado AAA.

## Fácil sem ser raso

Fácil é **um caminho curto até a primeira decisão jogável**, não a ausência
de critério. Na primeira sessão de um jogo novo:

1. Resolva fantasia, verbo, plataforma e a maior incerteza. Assuma o resto
   com registro; pergunte só o que impede de jogar.
2. Escreva ou adapte um brief curto (ou a seção equivalente). Não gere a
   pasta inteira de templates.
3. Construa um ciclo: perceber → decidir → agir → consequência → reinício.
4. Faça essa ação **parecer e soar** a intenção — feel e áudio do verbo no
   mesmo instante do impacto, mesmo com arte provisória, desde que a direção
   esteja declarada.
5. Compare em movimento com a referência. Sinta também latência e estabilidade
   de frame nesse trecho. Registre o próximo passo único.

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
| **AA / Triple-I (piso de acabamento)** | Fantasia focada que precisa nascer de novo sem diluir | Os mesmos, com feel, áudio, luz, animação, pacing e receita de conteúdo como requisitos do recorte — não “polimento depois” | A slice prova **repeatability**: outro trecho nasce no mesmo padrão, com custo e receita compreendidos |

O nome interno antigo “AAA-shaped” significa esta terceira linha: piso de
acabamento em escopo focado. **Não** significa orçamento de publisher, equipe
de centenas, live ops nem marketing de blockbuster. Reduza quantidade de
conteúdo; não reduza o piso aprovado.

Quem se vende com promessa cinematográfica será julgado por animação, voz,
face e direção de cena — mesmo que o verbo seja o ponto forte. O contrato
com o jogador acompanha o que o recorte promete, não o adjetivo no brief.

Se a escala mudar, atualize o brief e as fronteiras. Não retroaja aprovação
visual de um mock para mecânicas que ninguém jogou.

## Escada até o acabamento

Orientação de dependências, não esteira rígida. Pule um degrau só com motivo
registrado (ex.: PoC técnica antes do GDD).

1. **Fantasia e verbo** — quem o jogador é, o que faz, o que sente.
2. **Ciclo jogável** — uma decisão característica com término e repetição.
3. **Feel do verbo** — a ação tem peso, resposta e recuperação, sincronizados.
   Receita: [feel](../recipes/feel.md).
4. **Áudio da consequência** — causa e efeito no mesmo instante; silêncio é
   design. Receita: [áudio](../recipes/audio.md).
5. **Receita de conteúdo** — o próximo inimigo, sala ou efeito nasce sem
   improvisar o piso. Contrato: [design system](game-design-system.md).
6. **Vertical slice no piso** — gameplay, arte, áudio, pacing e tecnologia no
   acabamento pretendido, em movimento, **e** o pipeline que produz o próximo
   trecho sem heroísmo.
7. **Produção sem diluir** — multiplicar conteúdo pela receita; qualquer
   atalho que quebre o piso é regressão, não velocidade.

PoC investiga incerteza. Scaffold demonstra estrutura. Slice demonstra
experiência **e** repeatability. Confundi-los é o modo mais comum de um
agente declarar vitória cedo demais. A slice trava o piso → tempo por asset
→ esforço → o que é possível ampliar. Sem essa trava, o plano de produção
é chute.

## Barras operacionais (não nota)

Selecione as que o recorte afeta. Não some arte + correção + diversão.
Nenhuma destas barras é “ser AAA de publisher”.

- **Verbo:** a escolha muda estado, rota ou expectativa; o risco é legível
  antes da punição.
- **Controle:** entrada, câmera e recuperação sustentam o verbo em cada
  dispositivo alvo.
- **Feel:** antecipação, impacto, câmera, partículas, rumble e silêncio
  tornam a ação inequívoca. Flash, hit-pause, shake, partícula e áudio
  disparam no **mesmo frame** do contato; dessincronia vira dois eventos,
  não um impacto. Juice que esconde o verbo é regressão.
- **Mix:** camadas (ação, ambiente, música, UI) com ducking e interrupção;
  pause/reinício não deixam voz fantasma.
- **Pacing:** latência de input e estabilidade de frame no trecho real.
  Spike de frametime quebra suavidade e desempenho percebido com mais força
  do que baixar um preset de textura. Não corte o piso aprovado para “ganhar
  FPS”; investigue implementação mais barata que preserve a percepção.
- **Mundo:** silhueta, material, luz e animação legíveis em movimento;
  landmark e ameaça distinguíveis sem a melhor screenshot; família coerente
  com o asset-herói, **no engine**, não só no DCC.
- **Primeiro minuto:** com tela, a primeira superfície é a porta; a primeira
  ação ensina o verbo sem mural de texto; tutorial que bloqueia o jogo não é
  onboarding. O primeiro minuto também denuncia float, atraso e stutter.
- **Acesso:** contraste, forma além da cor, foco, toque, movimento reduzido
  quando o recorte os exige — e quando a promessa de público os exige.
- **Confiança:** iniciar, pausar, perder, ganhar, reiniciar e sair têm
  consequências definidas. Save, UI e erro não traem o jogador.
- **Produção / repeatability:** um item novo da família segue a receita sem
  intervenção excepcional; proveniência e consumidor são rastreados; custo
  observado do próximo trecho é conhecido.

O [protocolo](quality.md) registra cenário, condições, referência, evidência
técnica e observação em movimento. O instrumento único é o
[checklist de piso](aaa-checklist.md). O `context` escolhe o perfil em
`finish`; `--stage aaa` só materializa o rascunho inteiro.
Sem essa comparação, declare a lacuna. Não rebatize uma versão degradada
como novo piso. Completar o checklist não é nota AAA.

## O que este repositório continua recusando

Não há engine comum, API universal de ações, avaliação automática de
diversão, publicação automática nem hierarquia de agentes. Troca de modelo
com qualidade equivalente continua hipótese. Os estudos externos foram
lidos em recortes; seus testes não foram executados aqui. A literatura de
tier AAA não foi reproduzida neste harness: orçamentos e headcounts citados
são contexto, não meta.

O playground da Alan Studios é acervo de famílias e precedentes, não prova
de que este harness produziu aqueles jogos e não base aprovada para copiar
paleta ou feel.

## Continuidade

- **Onde estamos:** 0.9 abriu caminho curto, feel, áudio e o contrato de
  ambição. A pesquisa de 2026-09-09 separou tier de mercado e piso de
  acabamento e tornou pacing, sincronia e repeatability explícitos.
- **Próximo passo:** ao criar ou elevar um jogo, usar este guia com
  `--focus create` (início), `--focus feel` ou `--focus audio` (acabamento),
  sem gerar documentos que o recorte não precisa e sem chamar o build de AAA.
- **Por que agora:** sem a distinção, o agente documenta demais, polida de
  menos, ou usa “AAA” como adjetivo de marketing.
- **Pronto quando:** a escala está no brief (jam / produto / AA–Triple-I),
  o ciclo existe, o próximo passo da escada está nomeado com prova, e o
  [checklist](aaa-checklist.md) do recorte tem estado ou N/A em cada item
  aplicável.
- **Retomar por:** este guia, [criar](../recipes/create.md),
  [qualidade](quality.md) e a continuidade do próprio jogo.
