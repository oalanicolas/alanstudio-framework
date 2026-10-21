# Loading

Reduzir o trabalho e os bytes necessários para apresentar o jogo e começar a jogar,
mantendo conteúdo, apresentação, som, controles e comportamento aprovados. Use para
port, página pesada, boot, banda, cache ou primeiros minutos. A receita canônica é
[carregamento](../recipes/loading.md); o agente executa o processo até a entrega.

## Escala

`jam`: uma entrada e uma cena representativa; `product`: entrada, sessão curta,
continuação, cache e recuperação; `aa`: também pior rota, saves/idiomas, aparelhos
alvo e entrega pública quando autorizada. A escala muda cobertura, nunca qualidade.

## Avaliar

1. Reutilize o `context <projeto> --focus performance` vigente; obtenha-o se ainda
   não foi lido. `loading <projeto>` no CLI aponta leituras e ferramentas declaradas;
   não mede nem altera o jogo. Confirme a engine real e seus consumidores.
2. Fixe versão, entrypoint, cenário, marcos, dispositivo e referência aprovada.
   Confira pesquisas e decisões técnicas existentes antes de escolher formato ou
   pipeline. Parâmetro de outro projeto não é default deste.
3. Leia [performance](../recipes/performance.md) para comparação, ruído e domínios
   de memória. Observe antes de atribuir o custo a rede, decode, montagem ou GPU.
4. Reuse decisões e autorização. Pergunte apenas por uma escolha material que não
   possa ser inferida; uma dependência inacessível permanece lacuna explícita.

## Executar

Siga as fases da receita [loading.md](../recipes/loading.md), nesta ordem:

1. Registrar a referência e medir cada marco frio/quente com o conteúdo aprovado.
2. Traçar pedidos/leitura real; encontrar o trabalho evitável e a previsão inicial.
3. Aplicar a menor mudança compatível com a engine: entrada por clique, metadados,
   demanda, concorrência, transporte, cache ou posse. Não parar só no diagnóstico
   quando a implementação faz parte do pedido.
4. Repetir a medição e as contraprovas do consumidor. Em GLB/textura, reutilizar o
   [assets3d](../packages/assets3d/README.md), sem duplicar conversor. Em I/O nativo,
   adaptar pending/ready/sync/cancel/teardown, preservando seus contratos.
5. Concluir reinício, descarte e recuperação conforme [lifecycle](../recipes/lifecycle.md).
   Registrar resultados nos documentos e recibos do jogo, sem copiar o caso para o
   núcleo público. Publicar somente com autorização vigente.

## Verificar

Conferir bytes/tempo por marco e condição, conteúdo posterior acessível, amostras
sonoras e eventos preservados, montagem e cancelamento, cache e versão recebida.
Nativo sem perdas restaura N de N unidades por tamanho/hash; transformação de
representação também precisa provar estrutura e resultado renderizado/sonoro.
Comparar em movimento, mesma pose/estado e resolução de uso/cheia. Para performance,
três pares intercalados e ruído conforme performance.md; aparelho emulado não é físico.

Registrar por `record --kind budget` e anexar os resultados locais identificados.
Uma tabela menor, HTTP200, arquivo convertido, checklist ou resultado médio isolado
não encerra a função. Regressão de qualidade recupera o acabamento antes de continuar.

## Nunca

- Cortar resolução, detalhe, distância, sombra, efeito, animação, som, idioma ou
  conteúdo para passar o orçamento; ativar perfil leve automático.
- Confundir montar com baixar, cache RAM com persistência, bytes com FPS ou AVIF
  com compressão da textura na GPU.
- Transformar previsão em whitelist, baixar o resto por cronômetro, devolver
  zeros como dados ou escrever por callback em ponteiro nativo antigo.
- Herdar ganho, configuração ou aprovação de outro jogo ou de outra engine.
- Marcar a otimização aplicada apenas porque o CLI encontrou uma ferramenta.

## Entregar

Jogo acessível na versão comparada; antes/depois por marco com unidade e condições;
mudanças e técnica por consumidor; prova de qualidade/conteúdo/ciclo de vida;
limitações e pendências reais. Atualizar o registro canônico do jogo e encerrar o
recorte. Se houver próximo gargalo comprovado, encaminhar a [optimize](optimize.md)
ou [harden](harden.md); não inventar nova rodada quando o pedido foi concluído.
