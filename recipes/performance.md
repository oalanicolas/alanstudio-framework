# Performance: estabilidade sob orçamento

Entrada: cena, dispositivo alvo e o sintoma percebido — engasgo, atraso de entrada,
tempo de carga ou consumo crescente.

A qualidade visual aprovada é o piso. Otimizar é encontrar uma implementação mais
eficiente do **mesmo** resultado; reduzir sombras, resolução, animação ou efeitos
para atingir um número é rebaixar o jogo, não otimizá-lo. Se a receita recusa que reduzir acabamento para um número seja otimizar, o `record` nomeia o rebaixar que a receita já recusa. Corte no disco não é o mesmo resultado. Sem chave `rebaixar`. Se a única saída for
cortar acabamento, isso é uma decisão de escopo e precisa ser registrada como tal.

Com tela, a porta também anda: a mostra da mesa vigente cai todo
tick. Orçar só o campo esconde o primeiro quadro. Se a receita recusa que orçar só o campo cubra o primeiro quadro, o `record` nomeia o primeiro que a receita já recusa. Campo no disco não é a porta. Sem chave `primeiro`. Sem tela o
headless já joga.

Meça o que o jogador sente. FPS médio esconde exatamente o problema que importa. Se a receita recusa que o FPS médio esconda o problema que importa, o `record` nomeia o médio que a receita já recusa. Média no disco não é o problema. Sem chave `médio`.
use a distribuição do tempo de quadro e o pior percentil. Um jogo a 60 quadros com
um engasgo de 200 ms por minuto é lido como instável; um jogo estável a 30 não é. Se a receita recusa que um jogo estável a 30 seja instável, o `budget` nomeia o estável que a receita já recusa. Média no disco não é o quadro. Sem chave `estável`.

Declare o orçamento antes de otimizar: dispositivo, resolução, cena representativa,
tempo de quadro alvo, teto do pior percentil e tempo até jogar. Sem orçamento não
existe “rápido o suficiente”, e cada medição vira opinião. Se a receita recusa que sem orçamento exista rápido o suficiente, o `expected` do `budget` nomeia o suficiente que a receita já recusa. Pacote no disco não é o quadro. Sem chave `suficiente`. Pacote sem orçamento não é o dispositivo. Se a receita recusa que o pacote sem orçamento seja o dispositivo, o `unbudgeted` do `budget` nomeia o dispositivo que a receita já recusa. Manifesto no disco não é o quadro medido. Sem chave `dispositivo`.

Localize o gargalo no caminho real antes de alterar código. Distinga custo por
quadro de evento pontual, porque as causas e as correções são diferentes:

- **Custo contínuo:** quantidade de objetos atualizados, trabalho por objeto,
  chamadas de desenho, custo de preenchimento, física, colisão, consultas
  repetidas e trabalho refeito por quadro sem necessidade.
- **Engasgo pontual:** alocação e coleta de lixo, primeira compilação de shader,
  carregamento e decodificação de recurso, criação de textura, mudança de cena,
  layout ou reflow, e o primeiro uso de qualquer caminho que ainda não aqueceu.
- **Vazamento:** listeners, timers, loops, texturas e conexões que sobrevivem ao
  descarte. Execute montar → desmontar → montar e compare o consumo; ciclo de vida
  tem receita própria em [lifecycle](lifecycle.md).

Compare alternativas em condições equivalentes e altere **uma** variável por vez;
sem isso não é possível atribuir causa. Se a receita recusa que várias variáveis atribuam a causa, o `record` nomeia a variável que a receita já recusa. Variável no disco não é a causa. Sem chave `variável`. Registre o custo observado, a hipótese, o
resultado e as tentativas descartadas — inclusive as que pareciam óbvias e não
mudaram nada.

Confirme onde a prova vale. Editor não é build exportado; máquina de desenvolvimento
quente não é máquina do jogador fria. Se a receita recusa que o editor seja build exportado, o `record` nomeia o alvo que a receita já recusa. Editor no disco não é o build. Sem chave `alvo`. Se a receita recusa que várias variáveis atribuam a causa, o `record` nomeia a variável que a receita já recusa. Variável no disco não é a causa. Sem chave `variável`. Se a receita recusa que reduzir acabamento para um número seja otimizar, o `record` nomeia o rebaixar que a receita já recusa. Corte no disco não é o mesmo resultado. Sem chave `rebaixar`. Se a receita recusa que a adaptação herde o resultado, o `record` nomeia a contraprova que a receita já recusa. Adaptação no disco não é a contraprova. Sem chave `contraprova`. Se a receita recusa que o subpasso repita eventos de borda, o `record` nomeia o subpasso que a receita já recusa. Subpasso no disco não é o quadro. Sem chave `subpasso`. Se a receita recusa que orçar só o campo cubra o primeiro quadro, o `record` nomeia o primeiro que a receita já recusa. Campo no disco não é a porta. Sem chave `primeiro`. Se a receita recusa que o FPS médio esconda o problema que importa, o `record` nomeia o médio que a receita já recusa. Média no disco não é o problema. Sem chave `médio`. Se a receita recusa que a falha de gravação apague o registro anterior, o `record` nomeia o registro que a receita já recusa. Falha no disco não é o registro. Sem chave `registro`. Se a receita recusa que a fixture cubra a abertura, o `record` nomeia a fixture que a receita já recusa. Fixture no disco não é o efeito. Sem chave `fixture`. Se a receita recusa que as medidas diferentes sejam a grandeza, o `record` nomeia a grandeza que a receita já recusa. Leitura no disco não é a grandeza. Sem chave `grandeza`. Se a receita recusa que a máquina de desenvolvimento quente seja a máquina do jogador fria, o `fields` do `record --kind budget` nomeia a quente que a receita já recusa. Plataforma no disco não é a máquina fria. Sem chave `quente`. Aquecimento, cache e ferramentas de perfil
alteram o próprio resultado que estão medindo. Se a receita recusa que o aquecimento, o cache e o perfil deixem o resultado intacto, o `budget` nomeia o perfil que a receita já recusa. Perfil no disco não é a medição. Sem chave `perfil`.

`budget <projeto>` lê se existe script `budget`/`bench`, `tools/budget.*` ou
`record --kind budget`. Se o tool declara `title.attract`, o `budget`
nomeia a porta que a receita já cronometra. Stub no disco não é
dispositivo. Sem chave `door`. `measured` é sempre falso: o harness não executa a
medição. Se a receita recusa que o harness execute a medição, o `declared` do `budget` nomeia a medida que a receita já recusa. Script no disco não é o quadro. Sem chave `medida`.

Implementação concreta: `tools/budget.mjs` do starter `canvas-arcade` mede a
simulação e o `draw` num canvas stub, por percentil, não por média. Se o `tools/budget.*` relata o pior percentil, o `budget` nomeia o percentil que a receita já pede.
Relato no disco não é dispositivo. Sem chave `percentile`. A ferramenta declara
no próprio resultado que não cobre compositor, áudio, carregamento nem o
dispositivo alvo. A chuva compacta o array vivo e reusa um poço de
entidades; o evento volta ao poço no passo seguinte, o telegraph
reusa um buffer e o gerador da chuva reusa o mesmo objeto — o
orçamento declara as cenas `title.attract` e `playing.run` e relata esse reuso, sem teto
e sem aprovação. Orçar só o campo escondia o primeiro quadro.
O laço de passo fixo em `src/core/loop.js` é o que torna
a medição da simulação comparável entre execuções. `npm run size` relata
os bytes de `dist/` sem teto. Se o `tools/size.*` declara sem teto, o
`budget` nomeia os bytes que o size já relata. Bytes no disco não são
o quadro medido. Sem chave `size`.

Prova: distribuição de tempo de quadro na cena de pior caso, primeiro carregamento
em ambiente frio, comparação visual em movimento confirmando que o acabamento
sobreviveu, e o consumo após um ciclo completo de montar e descartar. Degraus:
[barra de acabamento](../references/production-bar.md#performance--estabilidade-não-média).
Direção visual e câmera continuam em [visual](visual.md).

## Comparações que permitem concluir alguma coisa

Aprendizados de aplicações reais, com [origem e limites](../references/sources.md#aprendizados-de-aplicações):

- Identifique o build servido, backend gráfico, dispositivo, visibilidade da página,
  dimensões do buffer, DPR e escala interna. Tamanho CSS igual não garante pixels
  iguais; renderização por software e HMR concorrente mudam o ensaio. Se a receita recusa que tamanho CSS igual garanta pixels, o `access` nomeia os pixels que a receita já recusa. Tamanho no disco não é o buffer. Sem chave `pixels`.
- Compare câmera, semente, relógio, vento, física e estado de aquecimento equivalentes.
  Preserve amostras brutas e configuração. Uma captura diferente pode revelar uma
  abertura ou um efeito que a fixture geométrica não cobre. Se a receita recusa que a fixture cubra a abertura, o `record` nomeia a fixture que a receita já recusa. Fixture no disco não é o efeito. Sem chave `fixture`.
- Nomeie a grandeza medida: simulação isolada, duração de callback, intervalo de RAF,
  CPU, GPU, carregamento e tempo de captura/exportação são medidas diferentes. Se a receita recusa que as medidas diferentes sejam a grandeza, o `record` nomeia a grandeza que a receita já recusa. Leitura no disco não é a grandeza. Sem chave `grandeza`.
  Leituras GPU, escrita de PNG e tempo simulado alteram a própria execução.
- Separe bytes transferidos, buffers decodificados, heap, recursos GPU e memória total.
  Contador de objetos ou heap JavaScript sozinho não mede PCM nem VRAM. Se a receita recusa que o heap JavaScript sozinho meça PCM ou VRAM, o `roles` nomeia o heap que a receita já recusa. Contador no disco não é o mix. Sem chave `heap`. Remover
  referências e desconectar áudio não demonstram coleta imediata pelo sistema. Se a receita recusa que desconectar, liberar e fechar comprovem coleta imediata, o `sources` do `roles` nomeia a imediata que a receita já recusa. Sinal no disco não é o sistema. Sem chave `imediata`.
- Faça contraprovas que deveriam falhar: trocar a variante, zerar o dado suspeito,
  desativar o diagnóstico ou comparar reconstrução completa com atualização parcial.
  Uma ferramenta de medição também pode desenhar na cena e falsificar seu resultado. Se a receita recusa que a ferramenta de medição deixe o resultado intacto, o `scripts` do `budget` nomeia o resultado que a receita já recusa. Script no disco não é o quadro limpo. Sem chave `resultado`.
- Ganho na média não demonstra redução de engasgos. Se a receita recusa que ganho na média demonstre redução de engasgos, o `fields` do `record --kind budget` nomeia os engasgos que a receita já recusa. Número no disco não é o quadro estável. Sem chave `engasgos`. Custos de build, compilação
  aquecida e serialização não são FPS. Se a receita recusa que custos de build, compilação aquecida e serialização sejam FPS, o `files` do `budget` nomeia o fps que a receita já recusa. Custo no disco não é o quadro. Sem chave `fps`. Uma melhoria visual pode aumentar o custo;
  registre ambos sem chamar a correção artística de otimização. Se a receita recusa que uma melhoria visual seja otimização, o `receipts` do `budget` nomeia a otimização que a receita já recusa. Recibo no disco não é os dois lados. Sem chave `otimização`.

## Eliminar trabalho preservando o contrato

- Rejeite candidatos impossíveis antes de cálculos caros, usando limites conservadores.
  Em física, considere pesos extrapolados, projeções anteriores e mudança de massa.
  Mantenha ordem e precisão aritmética quando a paridade exigir e compare também o estado privado
  de recuperação. Um grande ganho no caso rejeitado não é ganho equivalente no solver ativo. Se a receita recusa que o ganho no caso rejeitado seja ganho equivalente no solver ativo, o `record` nomeia o solver que a receita já recusa. Ganho rejeitado no disco não é o solver. Sem chave `solver`.
- Atualize derivadas caras quando seus dados mudarem. Um checksum calculado por quadro
  pode pertencer ao evento de criação/alteração do mundo. Valide que o resultado e seus
  consumidores continuam iguais, inclusive nas bordas entre regiões.
- Cache precisa declarar invalidação por movimento, deformação em shader, ancestrais,
  criação e remoção. Cenas dinâmicas não viram estáticas porque a matriz local ficou igual. Se a receita recusa que cenas dinâmicas virem estáticas porque a matriz local ficou igual, o `record` nomeia a matriz que a receita já recusa. Matriz no disco não é a cena. Sem chave `matriz`.
- Agrupamento excessivo pode anular o culling. Compare grupos espaciais, instâncias e
  custo por passagem; menos chamadas de desenho não garantem menos trabalho total. Se a receita recusa que menos chamadas de desenho garantam menos trabalho total, o `budget` nomeia as chamadas que a receita já recusa. Chamadas no disco não são o trabalho. Sem chave `chamadas`. Se a receita recusa que o aquecimento, o cache e o perfil deixem o resultado intacto, o `budget` nomeia o perfil que a receita já recusa. Perfil no disco não é a medição. Sem chave `perfil`.
- Copiar um mapa grande ou compor estático/dinâmico pode custar mais que redesenhar
  o conteúdo visível. Conte transferências, sincronização e submissões efetivas.
- Subdividir apenas a integração de movimento pode reduzir dependência da taxa de
  quadros. Não repetir eventos de borda, decisões de IA nem relógios de rede por subpasso.
  Se a receita recusa que o subpasso repita eventos de borda, o `record` nomeia o subpasso que a receita já recusa. Subpasso no disco não é o quadro. Sem chave `subpasso`.
  Meça o aumento de consultas físicas em taxas baixas.
- Grave trajetórias na precisão necessária e meça erro de posição/orientação antes
  de reduzir frequência. Escolha armazenamento e retenção conforme o contrato; uma
  falha de gravação deve preservar o registro anterior. Se a receita recusa que a falha de gravação apague o registro anterior, o `record` nomeia o registro que a receita já recusa. Falha no disco não é o registro. Sem chave `registro`. Bytes menores não provam fidelidade. Se a receita recusa que bytes menores provem fidelidade, o `record` nomeia a fidelidade que a receita já recusa. Anexo no disco não é a trajetória. Sem chave `fidelidade`.

Os detalhes de carregador, sombras e migração ficam nos packages de
[web](../packs/platforms/web.md) e [Unity](../packs/platforms/unity.md).
Uma adaptação em outra versão precisa repetir a contraprova, não herdar o resultado. Se a receita recusa que a adaptação herde o resultado, o `record` nomeia a contraprova que a receita já recusa. Adaptação no disco não é a contraprova. Sem chave `contraprova`.
