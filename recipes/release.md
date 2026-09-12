# Release: do repositório até o jogador

Entrada: a versão que se pretende entregar, a plataforma alvo e quem vai jogar.

**Autorização primeiro.** Nada nesta receita autoriza publicar, criar conta em
loja, subir artefato, contatar pessoas ou anunciar. Publicação exige autorização
explícita do usuário para aquela entrega. Preparar um artefato verificável é
trabalho técnico; distribuí-lo é decisão dele.

O ciclo criativo do framework terminava em QA, e essa lacuna produz um padrão
conhecido: um jogo que funciona na máquina de quem construiu e falha em qualquer
outra. Release é a etapa que converte “funciona aqui” em “funciona para alguém”.

O starter `canvas-arcade` grava `dist/VERSION.json` no export: versão e
HEAD. `ship` relata esse arquivo quando ele existe, e se a pasta `dist/`
de um jogo web tem index, serve, package e VERSION. Árvore sem esses
quatro é `incomplete`. HEAD do artefato diferente do checkout é
`stale`. Identidade do artefato não é outra máquina. `elsewhere` é
sempre falso. O serve anuncia a URL da rede se a
máquina tiver outro endereço IPv4; um endereço alcançável não é outra
máquina. Na árvore exportada o banner nomeia o artefato. Se o `tools/serve.*` nomeia a árvore exportada, o `ship` nomeia o banner que o serve já imprime. Banner no disco não é outra máquina. Sem chave `serve`. `npm run size`
relata os bytes de `dist/` sem teto. Se o `tools/size.*` declara sem
teto, o `ship` nomeia o tamanho. Bytes no disco não são outra
máquina. Sem chave `size`. Se a receita recusa que o tamanho sem teto seja o orçamento de entrega, o `ship` nomeia o teto que a receita já recusa. Relato no disco não é a plataforma alvo. Sem chave `teto`. `shipped` é sempre falso.

Com tela, a primeira superfície do artefato também é a porta. O serve
de desenvolvimento apontar `/?invite=1&seed=&spawn=` não é o `dist/`
em outra máquina. Compartilhar o convite não é `elsewhere`.

Verifique o artefato, não o ambiente de desenvolvimento. Editor, servidor de
desenvolvimento e build de depuração têm caminhos, permissões, recursos e tempos
diferentes do export. Um teste no editor não demonstra o jogo exportado.

O que precisa estar resolvido antes de chamar uma versão entregável:

- **Build reproduzível:** a partir de um clone limpo e de uma versão declarada,
  outra pessoa produz o mesmo artefato seguindo o runbook. Dependência
  não fixada, recurso local não versionado e passo manual não documentado
  são as três causas usuais de build que só funciona em uma máquina.
- **Orçamento de entrega:** tamanho do artefato e tempo até jogar têm teto
  declarado e medido na plataforma alvo, em rede e máquina realistas. Se a receita recusa que o tamanho sem teto seja o orçamento de entrega, o `ship` nomeia o teto que a receita já recusa. Relato no disco não é a plataforma alvo. Sem chave `teto`.
- **Plataforma real:** execução em dispositivo que não é o de desenvolvimento,
  com a entrada, a resolução e o sistema pretendidos. Emulação e redimensionar
  uma janela não substituem isso. Se a receita recusa que emulação e redimensionar uma janela substituam a plataforma real, o `scripts` do `ship` nomeia a emulação que a receita já recusa. Script no disco não é o dispositivo. Sem chave `emulação`.
- **Primeira execução:** instalação limpa, sem save, sem cache, sem permissão
  concedida. É o único caminho que todo jogador percorre e o menos testado. Se a receita recusa que a CI seja a primeira execução, o `ci` do `ship` nomeia a primeira que a receita já recusa. Fluxo no disco não é instalação limpa. Sem chave `primeira`.
- **Proveniência do que embarca:** cada asset, fonte, som, biblioteca e recurso
  gerado com origem, crédito e condição de uso compatíveis com a distribuição
  pretendida. Licença desconhecida bloqueia a entrega, não recebe uma suposição.
- **Registro de falha:** quando o jogo quebra no dispositivo de alguém, existe
  como saber. Coleta de erro precisa de decisão explícita sobre o que é enviado e
  do consentimento aplicável; telemetria não é padrão silencioso. Se a receita recusa que telemetria seja padrão silencioso, o `scan` nomeia a telemetria que a receita já recusa. Área no disco não é consentimento. Sem chave `telemetria`.
- **Reversão:** como voltar à versão anterior e o que acontece com saves criados
  pela versão nova. Reverter código não recupera dado já transformado; veja
  [persistence](persistence.md).
- **Acabamento mínimo:** as dimensões pertinentes da
  [barra](../references/production-bar.md) declaradas no degrau observado, com
  condição e autor. Uma dimensão abaixo do pretendido é lacuna registrada, não
  surpresa depois da entrega.

Quando exportar envolver adaptação para outro host, identifique separadamente fonte,
build, transformação/adaptador e artefato distribuído. Confira o conteúdo real do pacote:
uma pasta de build existente não prova que corresponde à fonte atual, nem que só ela
será enviada. Se a receita recusa que uma pasta de build existente corresponda à fonte atual, o `artifact` do ship nomeia a atual que a receita já recusa. Manifesto no disco não é o HEAD. Sem chave `atual`. Prévia, upload de versão e publicação têm efeitos e públicos distintos;
link não listado não comprova controle de acesso. Se a receita recusa que link não listado comprove controle de acesso, o `ship` nomeia o acesso que a receita já recusa. Link no disco não é outra máquina. Sem chave `acesso`.

Mapeie os serviços usados pelo jogo para o destino: início/fim de carregamento e
partida, pausa/áudio, identidade, save e rede quando presentes. Consulte a versão atual
do SDK do destino; evento de foco não tem necessariamente a semântica de pausa do jogo.
Registre disponível, adaptado, ausente ou não verificado por serviço. Teste o artefato
transformado, inclusive recuperação e falha do serviço; abrir o menu ou obter um ZIP
não comprova portabilidade. Se a receita recusa que abrir o menu ou obter um ZIP comprove portabilidade, o `tree` do ship nomeia a portabilidade que a receita já recusa. ZIP no disco não é o destino. Sem chave `portabilidade`. Preserve a fonte autoral e confira suas invariantes após
exportar. [Origem e limites](../references/sources.md#autoria-ugc-pública).

Registre a versão entregue, o conteúdo dela, o que ficou de fora e as lacunas
conhecidas. Uma entrega sem essa nota impede diagnosticar o primeiro relato de
problema, porque ninguém sabe o que estava dentro dela.

Implementação concreta a adaptar: o starter `canvas-arcade` não tem dependências
e serve por `tools/serve.mjs`. `npm run build` copia a árvore jogável para
`dist/` (index, src, data, serve). Isso torna o clone limpo trivial de
reproduzir e declara o passo de empacotar — não prova que outra máquina
já executou o artefato. Se o `tools/export.*` declara o empacote, o `ship` nomeia o passo que o export já declara.
Empacotar no disco não é outra máquina. Sem chave `export`. Se o `tools/export.*` recusa `file://`, o `ship` nomeia o file:// que o export já recusa. Recusar no disco não é outra máquina. Sem chave `file`. Se a receita recusa que a identidade seja outra máquina, o `tree` do ship nomeia a identidade que a receita já recusa. Árvore no disco não é entrega. Sem chave `identidade`. Se a receita recusa que abrir o menu ou obter um ZIP comprove portabilidade, o `tree` do ship nomeia a portabilidade que a receita já recusa. ZIP no disco não é o destino. Sem chave `portabilidade`. Se a receita recusa que o teste no editor demonstre o jogo exportado, o `artifact` do ship nomeia o editor que a receita já recusa. Manifesto no disco não é o jogo exportado. Sem chave `editor`. Se a receita recusa que uma pasta de build existente corresponda à fonte atual, o `artifact` do ship nomeia a atual que a receita já recusa. Manifesto no disco não é o HEAD. Sem chave `atual`. Se a receita recusa que link não listado comprove controle de acesso, o `ship` nomeia o acesso que a receita já recusa. Link no disco não é outra máquina. Sem chave `acesso`. Se a receita recusa que o tamanho sem teto seja o orçamento de entrega, o `ship` nomeia o teto que a receita já recusa. Relato no disco não é a plataforma alvo. Sem chave `teto`. O harness lê o passo com `ship <projeto>`.
`shipped` é sempre falso. Sem o passo, `next` propõe `ship.unpacked`.
Árvore incompleta é `ship.incomplete`; artefato de outro commit é
`ship.stale`. Nomeia a árvore que perdeu o `src/` que o projeto já
tem. Nomear não devolve o jogo. Árvore completa no HEAD atual ganha `artifact_open`
— o comando que serve `dist/`. Nomear não executa. HTML estático
sem manifesto já é o artefato e não dispara esses ramos.

Prova: build a partir de clone limpo, execução do artefato exportado em máquina
que não é a de desenvolvimento, primeira execução sem estado anterior, medição de
tamanho e tempo de carga, e a lista de proveniência do que foi embarcado. `verify`
registra esses comandos com recibo; recibo verde não aprova a entrega nem
substitui a autorização do usuário. Degraus:
[barra de acabamento](../references/production-bar.md#release--confiança-operacional).
Template da etapa: [release](../assets/templates/release.md). Se o molde recusa publicar, o `template` nomeia a publicação que o molde já recusa. Molde no disco não é autorização. Sem chave `publicar`.
