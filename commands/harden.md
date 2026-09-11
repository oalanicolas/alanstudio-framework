# Harden

Tornar o jogo confiável no pior momento: pausar, perder, reiniciar, sair; save
inválido, antigo e de versão futura; interrupção abrupta (aba fechada, bateria,
perda de foco); cena de pior caso; primeira execução fria; artefato exportado em
máquina alheia. Use antes de chamar qualquer coisa de publicável.

Receitas: [ciclo de vida](../recipes/lifecycle.md), [persistência](../recipes/persistence.md),
[performance](../recipes/performance.md), [release](../recipes/release.md).

## Escala

`jam`: pausar, perder, reiniciar e sair com consequência definida; montar →
desmontar → montar sem sobrevivente (`playable`). `product`: save versionado com
migração e dado inválido recuperado sem apagar progresso (`slice`/`shippable`).
`aa`: interrupção abrupta, determinismo declarado demonstrado, soak, build exportado.

## Avaliar

1. `context <projeto> --focus lifecycle` (e `persistence`, `performance`,
   `release` conforme o sintoma). `capabilities.mentioned` diz onde pause, reset,
   seed, observe, act, advance, capture e dispose são **mencionados**; não prova nada.
2. Localize os caminhos reais de início, atualização, render, pausa, término,
   reinício e descarte. Teste o contrato **pela ligação**, não pela API: a tecla de
   despausar não pode ser lida por um caminho que a pausa desliga.
3. Separe estado efêmero, progresso e preferência; versão do save e do conteúdo
   são contratos distintos. Liste as versões de save que já estiveram nas mãos de
   alguém: a migração cobre a cadeia inteira.
4. Declare orçamento antes de medir: dispositivo, cena representativa, tempo de
   quadro alvo, pior percentil, tempo até jogar.
5. Arquétipos [Bia e Léo](../references/personas.md): o que cada um quebra primeiro.

## Executar

Por risco, não por lista universal — o pacote de plataforma diz o que a engine
faz em pausa/foco/cena:

- **Transições:** ciclo completo iniciar → jogar → pausar → perder → reiniciar →
  sair, checando o que sobrevive (score, timers, entidades, som, inputs, conexões).
- **Save:** versionado desde a primeira gravação; migração escrita junto da mudança;
  dado inválido, truncado, futuro, armazenamento cheio ou negado tratados como caso
  normal; original preservado até a nova gravação confirmar. Nunca apagar save real
  para um teste passar.
- **Interrupção:** perda de foco, aba fechada, bateria, desconexão; volta onde estava.
- **Pior caso:** cena densa, primeiro shader, primeiro carregamento frio, coleta de
  lixo; engasgo pontual tem causa diferente de custo contínuo.
- **Artefato:** build exportado, não editor; clone limpo; máquina que não é a de
  desenvolvimento.

## Verificar

`verify` com os testes de transição, migração e determinismo; `--proves` para o que
os testes exercitam de fato (`claimed`, nunca verificado). Distribuição de tempo de
quadro pelo pior percentil (`record --kind budget` com métrica, valor, unidade,
plataforma, ferramenta). Interrupção forçada observada em movimento. Degraus:
`state_trust`, `performance`, `release` na [barra](../references/production-bar.md).

## Nunca

- Declarar capacidade pelo nome da engine ou pelo token no arquivo.
- Medir FPS médio; o jogador sente o pior quadro.
- Cortar sombras, efeitos ou animação como solução automática de orçamento.
- Testar só no editor ou só na máquina de desenvolvimento.
- Impor todos os cenários a todos os gêneros; um jogo sem save não "dispensa" migração,
  ela é `out_of_scope` com motivo.

## Entregar

O que sobrevive a cada transição, as versões de save cobertas, o pior quadro medido
com condição, o que falhou e foi corrigido, e o que continua desconhecido. Recibos
ligados ao HEAD. Sequência: [`release`](release.md) quando o gate `deliver` for o
pedido; [`optimize`](optimize.md) se o orçamento estourou.
