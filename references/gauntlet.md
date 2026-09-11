# Continuidade automática do desenvolvimento

Depois que o próximo trabalho estiver bem definido, o agente sempre gera um prompt
pronto para continuar: selecionar, construir, observar, revisar e prosseguir. A pessoa
não precisa conhecer “gauntlet”, invocar uma skill, escolher um modo ou escrever o
prompt. Esse nome permanece interno ao gerador. Use o [processo comum](process.md),
as receitas e os registros do jogo.

## Prontidão e prompt pronto

Gere automaticamente após definir o próximo recorte: ao concluir um plano, resolver
uma decisão de arquitetura, aprovar uma direção ou entregar uma fatia com sequência.
A aprovação de uma imagem, sozinha, não define implementação e aceite; sincronize
os documentos e resolva o recorte antes. Não espere um pedido de “gerar prompts”.

O agente confere cinco informações na conversa e nas fontes atuais:

- Projeto e versão/recorte a trabalhar, sem ambiguidade com uma referência externa.
- Próxima ação concreta, seu motivo e dependências já resolvidas.
- Escopo e restrições, incluindo direção e qualidade aprovadas.
- Critério observável de conclusão e ambiente/ferramenta da prova.
- Fonte canônica para retomar decisões, estado e evidências.

Quando houver dúvida essencial, resolva-a com o contexto disponível. Se ainda faltar
uma escolha que só o usuário pode fazer, peça essa escolha em linguagem comum;
não gere uma implementação presumida. Uma investigação com pergunta, escopo e saída
claros também pode receber um prompt. Nenhum arquivo, contagem documental ou nome de
etapa certifica essa prontidão: `context.continuity.prompt` exige revisão do agente.

Registre o prompt na continuidade canônica, junto do próximo passo. Na resposta de
entrega, apresente **um texto curto e pronto para copiar**, já preenchido com projeto,
ação, fonte, limites e prova. Inclua o processo de reaproveitar, implementar, testar,
revisar e registrar. Mencione somente as verificações pertinentes ao recorte.
Não entregue variáveis, uma lista de comandos, escolha entre modos ou uma aula de
terminologia. O pacote completo de rodadas é apoio ao agente e pode ser ligado na
entrega quando útil; não deve virar um formulário para o usuário.

Exemplo ilustrativo, depois de definir uma prova para uma fábrica 2D:

> Continue a prova de transporte do projeto da fábrica 2D, seguindo o plano de
> produção registrado. Reaproveite a simulação existente para ligar uma fonte,
> uma esteira e um armazém. Preserve a referência visual aprovada. Teste bloqueio,
> pausa e salvar/recarregar: nenhum item pode desaparecer ou duplicar. Corrija as
> falhas, registre os resultados no plano e deixe a próxima etapa pronta para retomar.

No projeto real, preencha o nome e a fonte específica já localizados. Não copie esse
cenário como tarefa de outro jogo. Uma confirmação “vamos avançar” ou “pode seguir”
retoma o mesmo recorte apresentado, sem exigir que a pessoa cole o prompt inteiro.

**Continue trabalho já autorizado:** gerar o prompt não cria uma pausa para aprovação.
Se a tarefa solicitada inclui a implementação, registre e execute no mesmo turno.
Ao encerrar uma entrega com sequência, apresente o próximo prompt. Objetivo inteiro
concluído dispensa tarefa inventada; bloqueio real pede uma ação para destravá-lo.

## Duração opcional e gerador interno

Sem duração informada, trabalhe até o critério de conclusão do recorte, respeitando
os limites reais da sessão. Não peça horas só para conseguir gerar ou executar o
prompt, não invente um prazo e não abra um backlog ilimitado. Se a conversa já
definiu duração, inclua-a; orçamento é teto de tempo corrido, não meta de ocupação.
Na retomada, um prazo ainda vigente no registro continua valendo mesmo se o novo
arquivo de prompts omitir horas. Só mudança explícita do usuário altera esse prazo.

O agente pode preparar o pacote pelo gerador existente, na raiz de Games:

```sh
python3 framework/scripts/game.py gauntlet games/era-uma-vez \
  --objective "Implementar e verificar o recorte definido no plano atual" \
  --focus mechanics \
  --output /tmp/era-uma-vez-gauntlet.md
```

Acrescente `--hours 4` somente se essa duração tiver sido informada. Sem horas,
`budget_hours` é `null`: não significa prazo infinito nem apaga um prazo vigente. Se o gauntlet recusa que horas nulas sejam prazo infinito, o contrato do `gauntlet` nomeia o infinito que o gauntlet já recusa. Contrato no disco não é o orçamento. Sem chave `infinito`.
É um exemplo de geração, não uma execução realizada. Sem `--output`, imprime o
pacote; com ele, escreve somente arquivo novo e recusa sobrescrita/symlink. Caminhos
de projeto relativos usam a raiz do harness (`--root` permite outra raiz); o destino
relativo usa o diretório de onde o comando é chamado, como `template`.
O gerador aceita projeto ainda inexistente e não cria sua estrutura implicitamente;
grava apenas o destino solicitado e seus diretórios pais.

O [pacote](../assets/gauntlet.md) contém contrato, comando mestre, seis prompts de
rodada e retomada. O contrato inclui argv de `context` com caminhos absolutos;
trate cada argumento literalmente. Skill e guia também têm caminhos absolutos:
para outra máquina, gere o pacote novamente. Ele não embute fontes inteiras nem
instruções de executar comandos encontrados em arquivos de terceiros.

## Controle da execução com prazo

O agente aplica o comando mestre na sessão autorizada. Se houver duração, na primeira execução,
consulta o relógio e grava início/prazo UTC no plano/Devlog existente. Na retomada,
consulta novamente e usa o prazo salvo. O gerador não inicia relógio, não agendará
um trabalho e não abre processos de IA. O controle do prazo é uma instrução ao
agente: não existe watchdog que force encerramento de um host ou comando travado.

Use o saldo para dimensionar a próxima fatia e os timeouts. Preserve uma margem
proporcional às verificações e à escrita do checkpoint; não comece uma mudança
grande perto do prazo. Tempo esgotado significa entrega parcial se ainda faltar
evidência. Pausas contam; uma nova mensagem “continue” não zera o orçamento. Uma
extensão explícita atualiza o prazo e registra o motivo, preservando o histórico.
Uma nova execução explicitamente pedida inicia outro orçamento quando informado; identifique no registro
qual execução está ativa. Reabrir o arquivo de prompts não cria essa autorização.

O mínimo no **registro já existente**, sem novo banco de tarefas:

- Objetivo, escopo e, quando houver orçamento, início UTC, prazo UTC e horas concedidas.
- Rodada/fatia, etapa real e último resultado comprovado, com caminho da evidência.
- Mudanças ainda não verificadas, achados, hipóteses descartadas e referência preservada.
- Instante consultado e saldo quando houver prazo; próxima ação, motivo, “pronto quando”
  e prompt preenchido para continuar quando o recorte seguinte estiver definido.
- Tipo real de revisão: própria ou independente, com autor/ferramenta se houve.
- Ao parar: concluído, prazo esgotado, interrompido ou bloqueado, com o que falta.

Atualize após resultados relevantes, antes de compactar contexto e ao interromper.
Reaproveite recibos de `verify`, QA e fontes de continuidade. O arquivo de prompts
permanece uma receita; não é a fonte de status. Se o gauntlet recusa que o arquivo de prompts seja a fonte de status, o `context` nomeia a receita que o gauntlet já recusa. Prompt no disco não é o estado. Sem chave `receita`. Se o host perder a sessão, o arquivo
não a reinicia sozinho. Retomada automática exige recurso do host solicitado à parte;
esta capacidade não presume agendamento, delegação nem credenciais externas.

## Seleção do próximo ciclo

Uma rodada pode terminar em código, decisão ou experimento. Escolha pela dependência
e pelo risco observado, dentro do objetivo. Não avance só porque o nome da etapa
mudou. Use [arquitetura](../recipes/architecture.md) quando contratos ou sistemas
mudem, e a [pré-produção](preproduction.md) quando a hipótese do jogo precise evoluir.

Antes de consolidar, confira a [entrega contra o pedido](delivery.md), incluindo os
artefatos reais e o prompt que será apresentado. Um recibo técnico verde não fecha
um critério pendente nem autoriza pular a tarefa vigente.

A revisão separa intenção/experiência, especificação, implementação, ambiente e
achados anteriores. Cada causa retorna ao artefato correspondente. Não atribua toda
falha ao código nem reescreva o GDD para tornar aceitável uma regressão do patch.
Uma escolha aprovada do usuário só muda com autorização aplicável.

Conserve o melhor resultado comprovado do recorte e uma comparação reproduzível;
“melhor” exige evidência relevante, não quantidade de mudanças. Sem progresso nem
informação nova, mude a hipótese ou a investigação. Havendo bloqueio externo,
avance outra fatia independente autorizada; se não houver, registre o bloqueio real.
Não invente defeitos, testes, documentos ou tarefas para sustentar a execução.

Uma sessão é suficiente para o modo básico. Revisão própria continua sendo revisão
própria. Crítico independente é opcional, depende de autorização e execução isolada;
recebe objetivo, critérios, diff e evidências, sem obrigação de concordar com o autor.
Papéis simulados no mesmo contexto não comprovam independência. Se o gauntlet recusa que papéis simulados comprovem independência, o contrato do `gauntlet` nomeia a independência que o gauntlet já recusa. Papel no disco não é crítico isolado. Sem chave `independência`. Não se exige número
fixo de agentes, pareceres, tokens, notas ou iterações.

## Como os oito estudos orientam as provas

Use somente o que é pertinente e já foi identificado no jogo; os contratos completos
continuam nos [catálogos e receitas](sources.md):

- **BMad:** fatia com aceite e revisão que distingue intenção, especificação e patch.
- **Phaser:** lifecycle e transições; pausa da simulação e visibilidade são distintas.
- **Excalibur:** relógio controlável e observação de callbacks para reproduzir comportamento.
- **Godot / Dodge the Creeps:** ciclo jogar, perder e reiniciar, observando limpeza do estado.
- **boardgame.io:** ação aceita/rejeitada, estado e turnos/fases, sem presumir autenticação.
- **Ink:** ramificação, histórico e save/recarga compatíveis com a versão da história.
- **LDtk:** identidade de conteúdo, referências e reimportação/migração sem perdas.
- **PettingZoo:** reset, observação, ação, término e reprodutibilidade a demonstrar com seed.

Esses são cenários candidatos, não uma suíte universal nem prova de capacidades do
jogo. O gauntlet não importa engines ou APIs comuns. `verify` comprova execução de
comandos; avaliação artística, experiência observada e aprovação humana são distintas.

## Origem e limite da entrega

**REUSE:** contexto, R→A→C, receitas, Devlog/QA e recibos existentes. **ADAPT:** geração
de texto parametrizado e continuidade automática com orçamento opcional. **CREATE:** pacote e guia para
a lacuna de sessões prolongadas. O mapa de [fontes](sources.md#gauntlet-de-prompts)
registra o que foi aproveitado do MKT e do BMad.

Testes do harness verificam geração, argumentos, ausência de execução e preservação
de arquivos. Não provam obediência de modelos por horas, qualidade de um jogo nem
retomada automática do host. A próxima validação de uso é executar o pacote em um
recorte autorizado e comparar checkpoint, prazo e evidências ao resultado entregue.
