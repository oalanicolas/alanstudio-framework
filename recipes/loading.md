# Carregamento: menos trabalho, mesmo jogo

Função: [loading](../commands/loading.md). Entrada: projeto, revisão, caminho do
jogador, sintoma e referência aprovada. Saída: mudança implementada, jogo acessível
e comparação por marco, com integridade, qualidade e limites explícitos.

O agente conduz o processo; o harness localiza contexto e ferramentas. A função
serve a engines diferentes por adaptar o consumidor de dados. Não há um codec,
chunk, cache, orçamento ou patch nativo universal.

## 1. Fixar o que precisa permanecer igual

Antes da primeira alteração, registre nos documentos/recibos existentes do jogo:

- revisão de engine, dados e build; entrypoint e consumidor ativo;
- apresentação aprovada: câmera, resolução/DPR, materiais, luz, transparência,
  animação, UI, áudio e estados que entram na comparação;
- controles, timing, eventos, progressão, save, idiomas e conteúdo acessível;
- cenário, dispositivo/backend, rede/cache e critérios de invalidação.

Conservar o mesmo jogo é o critério. Não trocar qualidade por bytes, memória, FPS
ou tempo do agente. Uma hipótese precisa citar produtor e consumidor; uma decisão
de formato/pipeline reutiliza ou atualiza a pesquisa técnica pertinente antes de
converter em escala. Estado aprovado não localizado permanece lacuna, não liberdade
para redesenhar. Originais e caminho de comparação ficam preservados.

## 2. Medir marcos distintos

Separar, conforme o fluxo real do jogo:

1. **Apresentação:** navegação até a página/porta pronta, antes de iniciar a engine.
2. **Menu da engine:** clique até entrada nativa utilizável.
3. **Primeiro controle:** jogador consegue executar a ação central com feedback.
4. **Sessão curta:** percurso declarado dos primeiros minutos, com recursos usados.
5. **Continuação:** mudança de área, save/idioma alternativo e conteúdo posterior.
6. **Revisita:** navegação normal e novo processo, com condição de cache registrada.

Uma experiência sem menu não precisa criar um para preencher o processo. Definir
o marco equivalente e registrar por que outro não se aplica. Usar a duração pedida;
se não houver uma, escolher um cenário conservador e identificá-lo como decisão,
sem tratar uma permanência parada como cobertura de todas as rotas.

Medir separadamente pedidos, corpos, transferência real, espera de rede, decode,
montagem, upload, tarefas longas, memória e intervalos de quadro. Incluir rede de
Workers; `encodedBodySize` não significa download novo. `transferSize` zero exige
considerar origem e exposição da medição. Cache frio, revisita e perfil privado não
são condições equivalentes. Capacidades/limites de cache e WASM não são RAM residente.
O [método de performance](performance.md) governa interleaving, ruído e afirmações de FPS.

## 3. Descobrir o conjunto necessário, não só os arquivos maiores

Traçar quem pede cada recurso e por quê: import estático, preload, `open/read/seek`,
consulta de duração/dimensão, banco monolítico, dependência de cena ou primeiro uso.
Relacionar cada pedido ao marco e ao sistema. Um arquivo pequeno de outra área pode
ser menos necessário que um grande do primeiro quadro.

Classificar cada técnica como aplicável, já presente, não aplicável ou ainda sem
prova, com localizador do consumidor. Não excluir conteúdo ausente para melhorar
a porcentagem. Um índice de metadados é diferente de um corpo baixado.

Priorizar por causa observada: evitar trabalho desnecessário → adiar o que pode
esperar → reduzir os bytes solicitados → tratar retenção e entrega. A ordem é uma
hipótese orientada pela medição; uma restrição nativa pode mudar a dependência.
Fazer uma mudança causal por vez, preservando o baseline.

## 4. Aplicar por família de consumidor

### Página e engine

- Manter o shell de apresentação separado da engine. Importar/iniciar após a ação
  real quando o fluxo já tem uma porta. Conferir imports indiretos, preload e
  construtores com efeito no topo; nenhum deve iniciar a engine escondido.
- Garantir início único, feedback da preparação e erro/recarga. Não criar duas
  instâncias por clique repetido, nem uma tela que continua baixando tudo em fundo.
- Comprimir imagens da UI preservando resolução, RGBA e transparência. Fontes:
  contornos, métricas, kerning e caracteres completos. Conteúdo visível ou idioma
  não é removido para cumprir orçamento. Conferir arquivo decodificado e composição.
- Downloads de preparação têm concorrência limitada, integridade pertinente e
  barreira antes do boot. Falha aborta/drena irmãos; não libera um boot parcial.
  Aproveitar buffers somente com contrato de posse conhecido.

### Arquivos, mundos e cenas

- Disponibilizar os caminhos/IDs completos com seus tamanhos e semântica, mantendo
  o corpo remoto até o uso quando a engine suporta. Montar não é transferir.
- Produzir previsão de preparação pelas leituras reais, ligada à revisão. A previsão
  não é whitelist: outro caminho, idioma ou save continua podendo pedir qualquer
  recurso. Não há timer para baixar o restante depois de alguns minutos.
- Metadados produzidos no pipeline podem evitar varreduras de boot: duração,
  dimensão, offset ou dependências. Gerar pelo produtor correto, validar N de N e
  vincular a hashes/versão. Não estimar valores para esconder o conteúdo frio.
- Particionar por unidade de uso, dependências e acesso aleatório. Reutilizar a
  lógica de mundo/LOD já aprovada; não reduzir alcance ou forçar LOD inferior.
- Em leituras dispersas, não antecipar intervalos enormes. Em leituras sequenciais,
  agrupar conforme observado. Medir bytes antecipados sem uso, latência e reutilização.
- Deduplicar operações em curso e recursos prontos; declarar teto de concorrência,
  retenção e invalidação. Contar backing buffers retidos, não só o tamanho da view.
  Descartar por dono/ciclo de vida, não apenas ao ultrapassar um número arbitrário.

### Contrato assíncrono e engine nativa

- Identificar os estados pendente/pronto/erro e todos os chamadores. Worker com
  `fetch` não torna um `read` síncrono assíncrono; esperar no thread principal ainda
  pode congelar o quadro. Preparar Worker/ponte antes do primeiro consumo bloqueante.
- Quando o consumidor permite pendência, enfileirar, consultar readiness e continuar
  no quadro seguinte. Copiar só bytes residentes, no ponto em que a engine permite.
- Preservar `Sync`/flush que antecede parser, reutilização de canais/buffers, EOF,
  erros e teardown. Remover imagens após liberar buffer pode exigir descarte sem I/O.
- Callback de rede preenche cache com dono; não escreve em ponteiro nativo guardado.
  No consumo, usar heap/view atual e marcar residência só depois da leitura integral.
  Cancelamento, resultado tardio e conclusão síncrona concorrente precisam de contraprova.
- Evitar espera ocupada cuja condição só avança após devolver controle ao navegador,
  inclusive áudio. Não mudar a frequência da simulação como otimização de download;
  cadência/render pertencem a [performance](performance.md) e exigem prova própria.

### Áudio

- Separar catálogo/metadados de PCM/arquivo. Adiar o corpo só funciona se o boot não
  abrir todo áudio para descobrir duração e se o gerenciador não ler o banco inteiro.
- Bancos com tabela de amostras podem precisar de adaptação do consumidor nativo:
  canal pendente conta como usado; evento mantém identidade/vida até os bytes;
  Stop/Reset/cancelamento impedem reprodução tardia. Não cachear silêncio/zeros.
- Aquecer o conjunto pequeno de sinais com prazo imediato e previsível. Conferir
  pausas, transições e descarte que podem cancelar sons ainda frios. Não aquecer
  todo banco por conveniência.
- Preservar PCM ou, se houver transformação, o acabamento sonoro aprovado, frequência,
  loops, duração, posição/mix e sincronização dos eventos. Fonte comprimida menor
  não prova PCM menor em RAM. Medir primeira reprodução fria, atraso de rede e replay.
- Consultar a receita de [áudio](audio.md); uma rede lenta pode atrasar o primeiro
  som frio. Não prometer ausência de atraso só porque os quadros continuam.

### Transporte, modelos e texturas

- Para arquivo grande de acesso aleatório, avaliar quadros comprimidos independentes
  e índice de offsets lógicos/comprimidos. Gzip único do arquivo inteiro não oferece
  essa mesma unidade de acesso. Medir benefício por família antes de converter tudo.
- Restaurar tamanho/hash de cada unidade antes de entregar dados nativos; conferir
  cobertura, limites, origem e versão do índice. Conservar offsets/semântica originais.
- Para JS/WASM/texto, variantes HTTP precisam de negociação, MIME, encoding e `Vary`
  coerentes. Arquivo `.br` no disco não prova que a hospedagem o entrega. Range deve
  usar offsets da representação efetivamente pedida; não aplicar offsets brutos a
  outro conteúdo codificado.
- Payload de render pode omitir metadados de extração/buffers órfãos demonstradamente
  não usados, mantendo a preservação original fora dele. Compartilhar accessors,
  preservar índices/topologia e atributos consumidos, skins, morphs e animações.
- GLB/texturas: reutilizar [assets3d](../packages/assets3d/README.md) e a régua por
  papel. Não fixar qualidade para todo acervo nem julgar dados lineares por cor.
  Conferir após decode, por regiões e no render; preservar originais e recuperação.
- Distinguir compressão exata de representação com quantização/perdas. A segunda
  só entra se preserva o acabamento aprovado sob os critérios e cenas do projeto.
  Menos bytes não concede aprovação; AVIF não comprova menos VRAM.
- Reutilizar templates, geometria e texturas por identidade. Clonar uma cena não
  prova instancing ou redução de draw calls. Manter a fonte necessária para restaurar
  contexto gráfico; fechar bitmap logo após upload pode impedir essa recuperação.

### Cache e entrega

- Conteúdo identificado por hash/versão imutável recebe URL própria e cache longo;
  HTML/índice mutável revalida. `no-cache` não é `no-store`; 304 não reenvia corpo,
  mas pode manter o custo de pedidos. Não prometer persistência após descarte do browser.
- Validar status, intervalos e comprimento de respostas; falhar visivelmente em
  dados truncados. Fallback original e tentativas limitadas têm orçamento combinado
  menor que o prazo do consumidor. Não repetir o mesmo erro indefinidamente.
- Conferir MIME e requisitos da ponte, incluindo isolamento de origem quando usa
  SAB. Verificar cabeçalhos e bytes na hospedagem real, não apenas no servidor local.
- Identificar versão servida e manter publicação/recuperação coerentes com o índice.
  Upload incremental economiza publicação, não é economia extra por jogador.
  Seguir [release](release.md); autorização de otimização não concede publicação.

## 5. Adaptar a engine, não copiar o patch de outro jogo

- **C/C++ e WASM:** trabalhar na fronteira FS/gerenciador de recursos e nos estados
  reais de consumo. Preload separado ou Worker não substitui um protocolo de demanda.
  Sem fonte/gancho adequado, registrar o limite do carregamento integral obrigatório.
- **Emulador/disco virtual:** usar setores/blocos por demanda somente quando o core
  aceita essa disponibilidade. Se exige ROM inteira, trocar extensão ou dividir o
  download fora do core não resolve a exigência. Qualquer snapshot requer prova própria.
- **Three.js/GLB:** separar índices, área/ator solicitado e corpos; reaproveitar
  assets3d, recursos compartilhados, recuperação e descarte. Preservar o render aprovado.
- **Unity Web:** aplicar a cenas/grupos/dependências e sistemas do projeto, como
  Addressables quando disponíveis. Conferir dependência compartilhada que arrasta
  conteúdo posterior para a abertura. Um `.data` monolítico já construído pode limitar
  o recorte; não prometer demanda fina sem reconstruir o consumidor.
- **Outra engine:** localizar os equivalentes antes de decidir. Engine identificada
  por manifesto no disco não prova backend, exportação ou estratégia de carregamento.

## 6. Prova e regra de encerramento

Cada mudança mantém uma linha rastreável no registro existente do jogo: problema,
produtor/consumidor com localizador, hipótese, mudança, versão comparada, custo e
condição, prova de qualidade, cobertura e limitação. O estado pode ser aplicado,
rejeitado, não aplicável ou pendente; não preencher lacuna com zero.

Contraprovas pertinentes ao que mudou:

- zero engine/dados antes do clique; início único e erro/recarregar;
- conteúdo fora da previsão, idioma/save/área posterior e primeiro recurso frio;
- N de N unidades exatas restauradas; malhas/atributos e textura/áudio decodificados;
- latência, falha transitória, truncamento, cancelamento e resposta tardia;
- flush/Sync/reutilização de buffer e teardown nas adaptações nativas;
- sons curtos/loops preservados, parar/resetar pendências e replay quente;
- montar → descartar → montar, perda/restauração de contexto e consumo limitado;
- cache frio/quente, versão nova para quem tinha cache e cabeçalhos públicos;
- comparação audiovisual e jogável em movimento, arte integral e aparelho declarado.

Executar os validadores do recorte e a verificação primária do projeto. Não elevar
o limiar depois de falha para declarar sucesso. Uma mudança de critério precisa de
justificativa e registro; qualidade inferior exige recuperar a referência primeiro.
Reutilizar prova apenas quando versões, entradas e escopo continuam correspondentes.

Entregar antes/depois por marco e unidade, sem somar percentuais de bases distintas.
Separar estimativa de corpo de fatura, acervo total de download inicial, melhoria de
banda de FPS, teste local de produção e emulação de aparelho físico. O acesso na versão
comparada precisa funcionar. Pedido concluído encerra; lacuna material fica explícita.

## Fontes primárias de contrato

As fontes descrevem APIs; não certificam ganho em um projeto. Conferir versão do
consumidor e compatibilidade antes de adaptar:

- [Emscripten: empacotamento e arquivos](https://emscripten.org/docs/porting/files/packaging_files.html).
- [Resource Timing: transferSize](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceResourceTiming/transferSize).
- [HTTP: cache e revalidação](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching).
- [Unity Web: publicação e cabeçalhos](https://docs.unity3d.com/6000.0/Documentation/Manual/webgl-deploying.html).
- [Addressables: conteúdo e dependências](https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/AddressableAssetsOverview.html).
