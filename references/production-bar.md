# Barra de acabamento

Este documento responde a uma pergunta que o framework não respondia: **o que
significa “pronto” e o que separa um protótipo de um jogo que as pessoas tratam
como produto acabado.**

Não é uma nota. Não é um selo. Nenhum comando promove um jogo a um degrau desta
escada; cada critério só vale quando alguém o observou nas condições declaradas.
A escada existe para tornar a conversa concreta: em vez de “falta polir”, dizer
qual dimensão está em qual degrau e qual observação a move para o próximo.

## Sobre a palavra AAA

No mercado, AAA descreve orçamento e equipe, não uma técnica. Um estúdio pequeno
não compra esse degrau. O que é alcançável — e o que o jogador realmente percebe —
é **acabamento por dimensão de ofício em um escopo reduzido**. Um jogo curto,
coerente e impecável é lido como produto; um jogo grande e irregular é lido como
protótipo, independentemente da quantidade de conteúdo.

**O degrau percebido de um jogo é o mínimo entre suas dimensões, não a média.**

Essa é a regra que mais importa aqui. Arte de carro-chefe com resposta de
protótipo é lida como protótipo: o jogador sente o atraso do controle antes de
admirar a iluminação. Um save que corrompe apaga a memória de qualquer acabamento
anterior. Áudio ausente rebaixa a leitura de uma cena bem construída. O trabalho
de subir a barra é quase sempre **encontrar a dimensão mais baixa**, não melhorar
a que já está mais alta.

Esse é o modo de falha típico de um estúdio assistido por IA: as dimensões que a
IA produz rápido — texto, quantidade de conteúdo, variação visual — sobem sozinhas,
enquanto feel, mixagem, estabilidade de frame e confiança de estado ficam para trás
e definem a leitura final.

## Os cinco degraus

| Degrau | Chave | Significado operacional |
| --- | --- | --- |
| Protótipo | `prototype` | Responde a **uma** pergunta. Descartável. Ninguém além de quem construiu precisa conseguir jogar. |
| Jogável | `playable` | Um ciclo completo. Outra pessoa joga sozinha, sem narração, e entende o que aconteceu. |
| Fatia | `slice` | Um recorte pequeno no acabamento pretendido, com gameplay, arte, áudio e tecnologia integrados. Demonstra que **mais** conteúdo desse padrão é produzível. |
| Publicável | `shippable` | Sobrevive a um estranho, a uma máquina ruim e a um dia ruim. Falha sem perder progresso. |
| Carro-chefe | `flagship` | O acabamento pelo qual o estúdio quer ser reconhecido. A dimensão deixa de ser adequada e passa a ser característica. |

Degraus não são prazos nem tamanhos de equipe. Um jogo pode parar
deliberadamente em `slice` e estar correto; o erro é chamá-lo de publicável.

## As dez dimensões

Cada dimensão tem uma pergunta, os degraus e a observação que comprova o degrau.
Selecione as dimensões pertinentes ao pedido; um jogo sem áudio registra a escolha
em vez de fingir o degrau.

### `feel` — resposta da ação central

**A ação principal é gostosa de repetir mesmo sem objetivo?**

- `prototype`: a ação acontece.
- `playable`: a entrada responde a cada quadro, o alcance da ação é previsível e
  errar não parece injustiça do sistema.
- `slice`: cada ação tem sinal próprio de partida, contato e término — animação,
  som, câmera e interrupção do tempo trabalham juntos. Perdão de entrada
  (buffer, coyote time, tolerância de alvo) é intencional e medido.
- `shippable`: a resposta é igual em todos os dispositivos de entrada suportados e
  em carga alta; nenhum quadro perdido converte a ação em falha do jogador.
- `flagship`: a ação é reconhecível fora do contexto — alguém identifica o jogo
  por um clipe de três segundos sem HUD.

Prova: vídeo em movimento, latência da entrada até o primeiro quadro de resposta e
repetição da ação por um minuto sem objetivo. Receita: [feel](../recipes/feel.md).

### `legibility` — legibilidade do estado

**O jogador sempre sabe onde está, o que o ameaça e o que pode fazer?**

- `prototype`: o estado é legível para quem conhece o código.
- `playable`: estado, ameaça e alternativa são identificáveis com o jogo parado.
- `slice`: são identificáveis **em movimento**, na resolução e no dispositivo alvo,
  por silhueta e forma antes de cor e texto.
- `shippable`: continuam legíveis em cena cheia, com o pior contraste suportado,
  sem áudio e sem leitura de texto.
- `flagship`: a leitura é imediata e a interface desaparece — o jogador não
  consulta o HUD para decidir.

Prova: captura em movimento, teste em escala de cinza, sessão com o som desligado.

### `art_direction` — coerência audiovisual

**Um item novo nasce pertencendo ao jogo?**

- `prototype`: placeholders identificáveis como placeholders.
- `playable`: escala, pivot e linguagem consistentes o suficiente para não confundir.
- `slice`: existe design system do jogo com tokens que têm consumidor real no
  código, famílias do mundo e receita de conteúdo novo.
- `shippable`: um implementador que não participou da direção produz o próximo
  item dentro do piso aprovado, e a comparação em movimento confirma isso.
- `flagship`: a direção é assinatura; desvios são escolha autoral, não acidente.

Prova: [design system do jogo](game-design-system.md) preenchido, com consumidores
rastreados, e um item novo produzido pela receita.

### `audio_mix` — mixagem, não arquivos

**O som informa, ou apenas existe?**

- `prototype`: silêncio, ou sons soltos de teste.
- `playable`: as ações centrais têm som licenciado e a origem está registrada.
- `slice`: existe mixagem — barramentos, prioridade, ducking sob eventos críticos,
  variação para evitar fadiga e silêncio usado como recurso.
- `shippable`: faixa dinâmica controlada, sem clipping nem picos que obriguem o
  jogador a baixar o volume; controles separados de música, efeito e voz; o jogo
  permanece jogável com áudio desligado.
- `flagship`: o áudio é adaptativo ao estado e reconhecível; identifica o jogo.

Prova: medição de pico/loudness, cena densa com evento crítico e sessão muda.
Receitas: [audio](../recipes/audio.md) e o acervo `sfx` do laboratório.

### `pacing` — ritmo e aprendizado

**O primeiro minuto ensina e o resto sustenta?**

- `prototype`: a mecânica é demonstrada por quem construiu.
- `playable`: o primeiro ciclo ensina a ação sem texto explicativo obrigatório.
- `slice`: há prática antes de combinação de riscos, e intensidade alterna com
  recuperação de acordo com a intenção declarada.
- `shippable`: a curva foi observada com pessoas que nunca viram o jogo; abandono e
  erro repetido foram investigados, não apenas contados.
- `flagship`: progressão abre decisões e domínio, não apenas números.

Prova: playtest com pessoa real, comportamentos observados, e a distinção explícita
entre tempo de sessão e interesse. Piso: [qualidade](quality.md).

### `state_trust` — confiança no estado

**O jogador pode confiar que o jogo não vai desperdiçar o tempo dele?**

- `prototype`: iniciar e jogar.
- `playable`: pausar, perder, reiniciar e sair têm consequência definida, e
  montar → desmontar → montar não deixa recurso sobrevivente.
- `slice`: save/carga preservam o progresso pertinente; a versão do save é um
  contrato explícito.
- `shippable`: save com versão migra, dado inválido é recuperado sem apagar
  progresso real, e interrupção abrupta — aba fechada, bateria, perda de foco —
  não corrompe. Determinismo declarado foi demonstrado, não presumido.
- `flagship`: o jogador nunca pensa no assunto.

Prova: ciclo de transições, migração entre versões de save, interrupção forçada.
Receitas: [lifecycle](../recipes/lifecycle.md) e [persistence](../recipes/persistence.md).

### `performance` — estabilidade, não média

**O jogo é estável no pior momento, não no melhor?**

- `prototype`: roda na máquina de quem construiu.
- `playable`: roda na máquina alvo declarada sem travar.
- `slice`: existe orçamento de quadro declarado e a cena representativa cabe nele,
  medida em condições equivalentes.
- `shippable`: a estabilidade é medida pelo pior percentil, não pela média; engasgos
  de carregamento, coleta de lixo e primeira execução de shader foram tratados;
  o tempo até jogar tem teto declarado.
- `flagship`: sobra orçamento para acabamento adicional sem regressão.

Prova: distribuição de tempo de quadro (não FPS médio), cena de pior caso, primeiro
carregamento em máquina fria. **A qualidade visual aprovada é o piso**: cortar arte
para atingir número não sobe este degrau. Receita: [performance](../recipes/performance.md).

### `accessibility` — alcance

**Quem consegue jogar?**

- `prototype`: quem construiu.
- `playable`: entrada primária funciona; nenhum estado depende exclusivamente de cor.
- `slice`: remapeamento de controles, redução de movimento, legendas para
  informação sonora e alvos de toque adequados.
- `shippable`: contraste verificado, escala de interface, opções de dificuldade ou
  assistência que não escondem conteúdo, e uma declaração honesta do que o jogo
  ainda não atende.
- `flagship`: acesso é decisão de design desde o GDD, não camada adicionada depois.

Prova: sessão com cada modo ativo, verificação de contraste, jogo completável
sem áudio e sem uma das mãos quando isso for aplicável.
Receita: [accessibility](../recipes/accessibility.md).

### `content_scale` — capacidade de produzir mais

**O segundo nível custa menos que o primeiro?**

- `prototype`: conteúdo embutido no código.
- `playable`: conteúdo é dado, separado da regra.
- `slice`: existe receita e ferramenta para nascer um item novo, e o custo do
  próximo é conhecido.
- `shippable`: conteúdo tem identidade estável, migração e validação; conteúdo
  ausente ou inválido falha de forma legível em vez de quebrar o jogo.
- `flagship`: a ferramenta de conteúdo é boa o suficiente para alguém de fora
  produzir dentro do piso.

Prova: produzir um item novo cronometrando o custo real e carregar conteúdo
inválido de propósito. Receita: [content](../recipes/content.md).

### `release` — confiança operacional

**Existe um caminho repetível entre o repositório e o jogador?**

- `prototype`: roda no editor ou no servidor de desenvolvimento.
- `playable`: existe build/export executável por outra pessoa a partir do runbook.
- `slice`: o build é reproduzível a partir de uma versão declarada, e o artefato
  exportado — não o editor — é o que se verifica.
- `shippable`: orçamento de tamanho e de tempo de carga, verificação em
  plataforma alvo real, registro de falha em produção, procedimento de reversão e
  proveniência de todos os recursos embarcados.
- `flagship`: publicar é rotina de baixo risco.

Prova: build limpo a partir de um clone, execução do artefato em máquina que não é
a de desenvolvimento. Receita: [release](../recipes/release.md).

## Como usar

1. `context` já devolve, em `production_bar`, as dimensões pertinentes ao foco e à
   etapa, com o degrau que aquela etapa pretende atingir. Não é um diagnóstico:
   é a seleção do que precisa ser observado neste trabalho.
2. Antes de subir uma dimensão que já está alta, procure a mais baixa entre as
   pertinentes. Registre o degrau observado e a evidência no QA ou no Devlog.
3. Ao declarar um degrau, declare também a condição: dispositivo, versão, cena e
   quem observou. Degrau sem condição é opinião.
4. Uma dimensão intencionalmente fora do jogo é registrada como decisão, com motivo.
   “Não aplicável” não pode esconder desconhecimento.

## Limites

Esta escada não mede diversão, não aprova arte e não substitui a aprovação do
usuário. Os critérios são observáveis, mas a observação é trabalho humano ou do
agente, com autor declarado. `verify` comprova comandos técnicos; nenhum comando
deste repositório atribui um degrau. Um jogo pode cumprir todos os critérios
mencionados aqui e ainda não interessar a ninguém — a escada trata de acabamento,
e acabamento é condição necessária, não suficiente.
