# Performance: estabilidade sob orçamento

Entrada: cena, dispositivo alvo e o sintoma percebido — engasgo, atraso de entrada,
tempo de carga ou consumo crescente.

A qualidade visual aprovada é o piso. Otimizar é encontrar uma implementação mais
eficiente do **mesmo** resultado; reduzir sombras, resolução, animação ou efeitos
para atingir um número é rebaixar o jogo, não otimizá-lo. Se a única saída for
cortar acabamento, isso é uma decisão de escopo e precisa ser registrada como tal.

Com tela, a porta também anda: a mostra da mesa vigente cai todo
tick. Orçar só o campo esconde o primeiro quadro. Sem tela o
headless já joga.

Meça o que o jogador sente. FPS médio esconde exatamente o problema que importa:
use a distribuição do tempo de quadro e o pior percentil. Um jogo a 60 quadros com
um engasgo de 200 ms por minuto é lido como instável; um jogo estável a 30 não é.

Declare o orçamento antes de otimizar: dispositivo, resolução, cena representativa,
tempo de quadro alvo, teto do pior percentil e tempo até jogar. Sem orçamento não
existe “rápido o suficiente”, e cada medição vira opinião.

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
sem isso não é possível atribuir causa. Registre o custo observado, a hipótese, o
resultado e as tentativas descartadas — inclusive as que pareciam óbvias e não
mudaram nada.

Confirme onde a prova vale. Editor não é build exportado; máquina de desenvolvimento
quente não é máquina do jogador fria. Aquecimento, cache e ferramentas de perfil
alteram o próprio resultado que estão medindo.

`budget <projeto>` lê se existe script `budget`/`bench`, `tools/budget.*` ou
`record --kind budget`. Se o tool declara `title.attract`, o `budget`
nomeia a porta que a receita já cronometra. Stub no disco não é
dispositivo. Sem chave `door`. `measured` é sempre falso: o harness não executa a
medição.

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
  iguais; renderização por software e HMR concorrente mudam o ensaio.
- Compare câmera, semente, relógio, vento, física e estado de aquecimento equivalentes.
  Preserve amostras brutas e configuração. Uma captura diferente pode revelar uma
  abertura ou um efeito que a fixture geométrica não cobre.
- Nomeie a grandeza medida: simulação isolada, duração de callback, intervalo de RAF,
  CPU, GPU, carregamento e tempo de captura/exportação são medidas diferentes.
  Leituras GPU, escrita de PNG e tempo simulado alteram a própria execução.
- Confirme que o medidor não criou um segundo loop de desenho sobre o RAF do jogo.
  Fixe resolução interna e qualidade entre condições; um governador adaptativo ou
  teto de vsync pode esconder a diferença. Alterne a ordem das variantes, registre
  aquecimento e deriva térmica e inclua um controle sem alteração. Ganhos que mudam
  de sinal entre ordens ou ficam dentro do ruído não justificam promover a variante.
- Para engasgos de shader, conte programas e primeira compilação durante carregamento,
  primeiro uso de cada efeito e reinício. Aqueça as variantes reais de material e
  iluminação antes da ação; retenha recursos compartilhados enquanto tiverem dono.
  Não descarte e recrie todos os programas a cada partida, nem retenha recursos sem
  limite para evitar recompilação. Confira três partidas e o descarte final, além
  da equivalência visual em movimento. Caso: sessões S09/S14 do piloto Beacon/Jev
  do laboratório em 22/09/2026; os números locais não são metas universais.
- **Tempo até jogar:** separe pedidos, bytes e decodificação antes de escolher a técnica.
  - *Como medir:* com cache frio, repita o carregamento variando uma coisa por vez
    (concorrência, formato, rede emulada). Meça também na produção real: a emulação de rede
    cobra latência por pedido e não reproduz HTTP/2.
  - *Junto do tempo:* conte a regressão que ele pode esconder. Um início mais rápido que toca
    a ação sem som é pior, não melhor.
  - *Cache:* depois de um deploy, confira que quem já tem cache recebe a versão nova.
  - *Caso Distrito Rabisco (23/09/2026):* com FLAC, a espera ficou limitada por idas e voltas
    (4 → 16 downloads: 1,79 → 0,57 s em produção). Regras em
    [áudio](audio.md#aprendizados-de-carregamento-formato-e-entrega) e no
    [pack Web](../packs/platforms/web.md#build-plataformas-e-distribuição).
- No navegador, quando execuções separadas variam mais que a diferença procurada, abra
  referência, variante e uma segunda cópia da referência (A/B/A′) no mesmo processo e
  alterne rajadas curtas na mesma cena, com o loop do jogo parado durante a rajada. Use
  o timer de GPU do WebGL quando existir e conclua só por razões entre variantes: com
  várias abas, o valor absoluto não é o tempo de quadro. Antes de afirmar "sem diferença",
  prove a sensibilidade com uma alteração de custo conhecido; se ela não aparecer, o
  método não decide. Caso: Só Sobra Um, 22/09/2026, onde builds idênticos variaram até 25%
  entre execuções separadas.
- Ao cronometrar desenhos no navegador em sequência, sincronize a GPU antes e depois de
  cada um, por exemplo com a leitura de 1 pixel. Sem isso, o timer pode somar trabalho que
  ainda estava na fila do desenho anterior e inventar custo. Com GPU disputada, meça as
  variantes intercaladas no mesmo instante da simulação e conclua pela mediana da razão por
  instante, com intervalo. Custo que não muda quando a área desenhada cai a uma fração é
  sinal de artefato do método, não de preenchimento. Caso: Só Sobra Um, 22/09/2026 — efeito
  medido em +30% a +47% sem sincronizar e em 0% a +2,4% sincronizado, com a contraprova do
  AO (−20% a −28%) visível nos dois métodos.
- Separe bytes transferidos, buffers decodificados, heap, recursos GPU e memória total.
  Contador de objetos ou heap JavaScript sozinho não mede PCM nem VRAM. Remover
  referências e desconectar áudio não demonstram coleta imediata pelo sistema.
- Tempo antes e depois exige repetição: três ou mais rodadas intercaladas de cada
  versão na mesma cena e um controle da mesma versão contra si mesma, que mede o
  ruído. Ganho menor que a variação entre rodadas iguais não é ganho. Confirme pelo
  estado da página que cada rodada chegou à cena pretendida antes de usar o número,
  e tire antes e depois de execuções rotuladas, nunca de capturas avulsas. Para o
  que acontece durante um evento — perda de contexto, aba oculta, pausa —, leia o
  estado do jogo antes, durante e depois (relógio, placar, tela visível), em vez de
  deduzir por uma captura final ([origem](../references/sources.md#acervo-externo-swipe)).
- Faça contraprovas que deveriam falhar: trocar a variante, zerar o dado suspeito,
  desativar o diagnóstico ou comparar reconstrução completa com atualização parcial.
  Uma ferramenta de medição também pode desenhar na cena e falsificar seu resultado.
- Ganho na média não demonstra redução de engasgos. Custos de build, compilação
  aquecida e serialização não são FPS. Uma melhoria visual pode aumentar o custo;
  registre ambos sem chamar a correção artística de otimização.

## Eliminar trabalho preservando o contrato

- Rejeite candidatos impossíveis antes de cálculos caros, usando limites conservadores.
  Em física, considere pesos extrapolados, projeções anteriores e mudança de massa.
  Mantenha ordem e precisão aritmética quando a paridade exigir e compare também o estado privado
  de recuperação. Um grande ganho no caso rejeitado não é ganho equivalente no solver ativo.
- Atualize derivadas caras quando seus dados mudarem. Um checksum calculado por quadro
  pode pertencer ao evento de criação/alteração do mundo. Valide que o resultado e seus
  consumidores continuam iguais, inclusive nas bordas entre regiões.
- Cache precisa declarar invalidação por movimento, deformação em shader, ancestrais,
  criação e remoção. Cenas dinâmicas não viram estáticas porque a matriz local ficou igual.
- Agrupamento excessivo pode anular o culling. Compare grupos espaciais, instâncias e
  custo por passagem; menos chamadas de desenho não garantem menos trabalho total.
- Não asse dentro de um mapa grande um termo que muda em jogo, como a oclusão alterada
  por destruição: aplique-o no shader a partir da própria textura pequena, reproduzindo a
  mistura e o espaço de cor originais, e compare a imagem. A atualização passa a reenviar
  só o mapa pequeno.
- Texturas procedurais geradas por laços de pixel no JavaScript podem ir para a GPU. Crie
  um único contexto de bake por sessão (criar um por uso custa e o navegador limita o
  total), compare pixel a pixel com a versão de CPU e mantenha a CPU como alternativa
  quando a extensão necessária faltar. Números do caso Só Sobra Um: 608 → 57 ms num mapa
  de 2816², sem prometer o mesmo ganho em outro hardware.
- Copiar um mapa grande ou compor estático/dinâmico pode custar mais que redesenhar
  o conteúdo visível. Conte transferências, sincronização e submissões efetivas.
- Subdividir apenas a integração de movimento pode reduzir dependência da taxa de
  quadros. Não repetir eventos de borda, decisões de IA nem relógios de rede por subpasso.
  Meça o aumento de consultas físicas em taxas baixas.
- Ao limitar atualizações visuais por distância ou visibilidade, mantenha relógios
  de gameplay fora desse corte: equipar, recarregar, cooldowns e efeitos que alteram
  a simulação devem avançar mesmo sem pose desenhada. Compare o mesmo agente perto,
  longe e fora da câmera; confirme inventário, munição e ações concluídas, além de
  observar uma partida inteira. Um combate que só progride ao aproximar a câmera
  invalida a otimização. A prova funcional não autoriza reduzir detalhe de animação.
- Grave trajetórias na precisão necessária e meça erro de posição/orientação antes
  de reduzir frequência. Escolha armazenamento e retenção conforme o contrato; uma
  falha de gravação deve preservar o registro anterior. Bytes menores não provam fidelidade.
- Pague a primeira compilação antes do jogo. Compile os materiais e variantes que só
  aparecem depois — efeito raro, inimigo novo, transparência, construção — atrás da
  tela de carga, com os objetos visíveis e o culling desligado durante o aquecimento.
  Trocar um material de opaco para transparente em runtime cria outro programa;
  prefira estados já aquecidos. Prova estrutural: a contagem de programas não cresce
  numa sessão que percorre esses primeiros usos.
- Sombra e render sob demanda para o que está parado: mapa de sombra sem atualização
  automática, marcado como sujo quando luz, câmera além de um limiar ou caster
  animado mudam; render suspenso em menu, pausa e modo foto quando nada muda.
  Atualizar a meia taxa é corte, não otimização. Uma marcação incondicional em outro
  ponto do laço anula o ganho. Prova: captura idêntica à versão por quadro, em movimento.
- Carregamento cooperativo: montagem de cena, decodificação e upload em etapas que
  cedem o thread principal a cada quadro ou orçamento declarado, nomeadas na tela de
  carga. Um `Promise.all` seguido de construção síncrona longa congela a página.
  Prova: nenhuma tarefa longa acima de 50 ms depois do primeiro quadro.
- Destruição proporcional à região: terreno ou cenário destrutível envia à GPU só o
  retângulo ou chunk alterado. Reenviar o recurso inteiro põe o custo no quadro do
  impacto, o mais visível do turno. Prova: bytes enviados por explosão no mapa máximo.
- O que não muda é desenhado uma vez. Em Canvas 2D, fundo e palco estáticos vivem em
  camada própria; HUD em DOM escreve só quando o valor muda — `innerHTML` do HUD
  inteiro por quadro gera layout e lixo. Prova: captura idêntica e contagem de
  operações de desenho ou mutações por quadro com o jogo parado.

## Adaptadores automáticos de qualidade

Grande parte da web 3D adapta a qualidade sozinha: no acervo externo estudado em
setembro de 2026, 20 de 58 clientes e snapshots web cortavam resolução, AO, sombra,
LOD, partículas ou efeitos por tempo de quadro, e outros escolhiam o perfil pelo
dispositivo ao iniciar. Para este framework isso é degradação. Separe três casos:

- **Por tempo de quadro, em runtime:** nunca como ação. O mecanismo — janela,
  histerese, cooldown, percentil — serve de diagnóstico: registra cena e gargalo e,
  no máximo, recomenda uma opção ao jogador. Se reduzir um efeito não melhora o
  percentil, o gargalo está em outro lugar; isso é informação, não permissão.
- **Por dispositivo, ao iniciar:** aceitável só quando o perfil escolhido é a
  qualidade aprovada para aquela classe de dispositivo, fica visível ao jogador e
  pode ser trocado. Toque, núcleos ou memória que levam a um perfil abaixo da
  qualidade aprovada são degradação automática.
- **Fallback técnico:** sem o backend exigido (WebGPU, WebGL2), o jogo roda no
  disponível e diz isso. Exigir um backend sem fallback exclui jogadores e é decisão
  de escopo registrada, não ajuste de qualidade.

Verificar: o padrão das preferências é a qualidade aprovada, não `auto`; nenhum
callback de tempo de quadro altera DPR, escala de render, sombras, efeitos, LOD ou
contagem de instâncias; a cena pesada roda e o estado de qualidade termina igual sem
entrada do jogador. Qualidade escolhida pelo jogador, com efeito documentado, não é
degradação.

## Orçamento que falha

Orçamento em README, comentário ou HUD não protege nada, e um contador que nenhum
caminho incrementa também não. Cada linha de orçamento vira uma verificação que
falha no build ou no teste. Em máquina compartilhada, tempo de quadro é evidência do
relatório — percentis antes e depois —, não gate. Os gates são invariantes
estruturais da mesma cena: o mapa baixa uma vez; programas estáveis após o
aquecimento; texturas e geometrias não crescem depois de reiniciar a partida N
vezes; chamadas de desenho não passam da referência; bytes até o primeiro quadro
jogável dentro do declarado. Limiar em milissegundos só vira gate em hardware
dedicado e declarado. Estourar um orçamento abre investigação, nunca corte da
qualidade aprovada. [Origem e limites](../references/sources.md#acervo-externo-swipe).

Os detalhes de carregador, sombras e migração ficam nos packages de
[web](../packs/platforms/web.md) e [Unity](../packs/platforms/unity.md).
Uma adaptação em outra versão precisa repetir a contraprova, não herdar o resultado.
