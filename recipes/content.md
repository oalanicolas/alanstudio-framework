# Conteúdo, assets e progresso

Entrada: nível, história, entidade ou recurso visual/sonoro a adicionar ou substituir.

O harness lê se o conteúdo saiu do código com `content <projeto>` (`data/`,
`levels/`, `.ldtk`/`.tmx`/`.ink`). Paleta e token (`palettes.json`,
`tokens.json`) não extraem conteúdo — o `art` lê esses manifestos.
Arquivo de dados não é volume
suficiente — `enough` é sempre falso. Sem arquivo, `next` propõe
`content.inline`. O starter `canvas-arcade` carrega `data/spawn.json` e `data/copy.json`
pelo mesmo `migrateTable`. Formato antigo vira schema 1; schema futuro
falha com o número; campo obrigatório falha com o nome da mesa.
`npm run table -- <nome>` já nasce com schema. `--from spawn`, `--from dusk` ou `--from calm` copia a forma que o
starter já consome (`?spawn=` / `settings.spawnProfile`).
Se o `tools/new-table.*` nasce a mesa, o `content` nomeia a mesa que o disco já nasce.
Ferramenta no disco não é volume. Sem chave `table`.
Se o disco declara `migrateTable`, o `content` nomeia a migração que as mesas já compartilham. Arquivo no disco não é volume. Sem chave `migrate`.
`--as denser|calmer|brief` desloca os knobs e deixa a chuva distinta.
`brief` encurta prática e rampa; a folga da guarda permanece —
encolher a abertura não come o verbo.
Spawn 3 acrescenta `closeIntervalScale`; ausente fica `1` e o fecho
só pisca. Spawn 4 acrescenta `closeHazardScale`; ausente fica `1` e
o fecho não muda a mistura. Aperto no disco não é curva observada.
`npm run pair -- <nome> --from dusk|calm` nasce look e chuva no mesmo
nome; `listMoods` inclui e `?mood=` aplica. `npm run session -- --spawn <nome>` traça essa chuva. Com tela, a
porta também chove essa mesa — cadência, queda e risco, sem o RNG da
partida. Trocar `?spawn=` / `?mood=` troca a mostra. Mesa no disco
não é volume. O `art` nomeia essas mesas. Se o disco declara
`listMoods`, o `content` nomeia o par. Nome no disco não é
volume. Sem chave `moods`. Depois de um
`note`, `start` e `next` apontam `pair --from`, `look --from` e `table --from`. `dusk` e `calm` são
a segunda e a terceira chuva, não volume — `enough` é sempre
falso. Alguém de fora ainda não produziu no piso.

Leia o formato atual, sua carga em runtime e os consumidores. Procure definição ou
slot substituível antes de duplicar lógica. Preserve identidade, escala, pivot,
colisões, animações e referências ao trocar arte. Som novo: consulte
`shared/sfx` no laboratório (`sfx search`) só se o acervo tiver sons; sem
ele, o starter já fala em `public/sfx` e a busca nomeia o stem que
casa com o termo. Copie o arquivo e a
proveniência. Mix, interrupção e silêncio seguem [áudio](audio.md), não apenas
a cópia do arquivo. Registre origem e condições de uso; conteúdo baixado não
recebe uma licença nova pelo simples reuso. Se o sidecar declara `Consumidor:`, o `origins` nomeia o consumidor que o sidecar já declara. Consumidor no disco não é licença válida. Sem chave `consumer`. Se o roteiro recusa que o sidecar sem rótulos declare, o `origins` nomeia os rótulos que o roteiro já recusa. Recibo no disco não é licença. Sem chave `rótulos`.

Geração externa (Magnific e similares) distingue capacidades documentadas de
integração comprovada. Não torna o fornecedor obrigatório.

Quando a geração ou importação for assíncrona, registre no manifesto/recibo já usado:
pedido e referência autoral, tarefa do fornecedor, estado remoto, arquivo local e
hash, derivação e consumidor integrado. **Pronto no serviço, baixado, validado e
consumido são estados diferentes.** Uma tarefa omitida numa consulta não equivale a
falha; siga o contrato de consulta e limite de tentativas do fornecedor.

Use a identidade e o caminho efetivamente retornados. Não presuma nomes quando o
serviço versiona ou renomeia assets. No download, validar resposta e integridade
antes de promover o arquivo temporário evita que uma transferência parcial ou uma
página HTML ocupe o lugar do recurso válido. Preserve master e versão anterior.

Verificadores de sprites/texturas localizam candidatos a defeito; correções que
apagam pixels, quantizam cores ou redimensionam não são consequência automática de
um alerta. Confira recorte, alpha, sequência e aparência no jogo conforme sua política
artística. Prova: falha preserva o recurso anterior; sucesso chega ao consumidor certo,
com origem/licença e acabamento conferidos. Este procedimento não comprova consistência
do gerador. Se a receita recusa que o recibo comprove a consistência do gerador, o `fields` do `origins --declare` nomeia a consistência que a receita já recusa. Recibo no disco não é o asset. Sem chave `consistência`. [Origem e limites](../references/sources.md#autoria-ugc-pública).

Para níveis, examine identidade estável, referências a entidades, arquivos externos,
spawn e rotas legíveis. Teste carregamento ausente/incompatível e retorno a um nível
já visitado. Não troque o formato inteiro para absorver uma validação de outro editor.

Para narrativa, confirme como escolhas disponíveis dependem do histórico, quando
efeitos são aplicados e qual estado uma escolha restaura. Teste caminhos alternativos,
fim sem opções e retorno após save. Versão da história compilada e versão do save
são contratos distintos; não use um único número por conveniência se já são separados.

Para saves, identifique estado efêmero versus persistente, compatibilidade, migração
e comportamento de dados inválidos. A política de recuperação deve preservar o
progresso conforme o requisito; não apague saves reais para fazer o teste passar.

Prova: recurso correto carregado no cenário real, comportamento preservado, caminho
alternativo e referência visual quando afetada. Arquivo gerado ou importado não
comprova que está sendo consumido. Se a receita recusa que o arquivo importado esteja sendo consumido, o `record` do `sfx copy` do acervo nomeia o consumido que a receita já recusa. Recibo no disco não é mix. Sem chave `consumido`.

## Aprendizados de produção e transporte de assets

[Origem dos casos](../references/sources.md#aprendizados-de-aplicações). Aplicar
conforme o contrato do consumidor e repetir a prova no projeto de destino.

- Separe resolução do master, pixels por metro e escala física. Mais resolução não
  exige mudar dimensões no mundo. Meça a superfície e a geometria avaliadas, não
  apenas origem ou bounds; projeção, portas, pivôs e conexões precisam continuar iguais.
- Textura repetível exige bordas e iluminação compatíveis. Ruído não periódico,
  faces laterais e gradientes próprios de cada tile podem produzir emendas mesmo
  em alta resolução. A solução depende da composição, não só do filtro.
- Escalar um módulo inteiro pode deformar ferragens e sombras. Repetições montadas
  antes do render e faixas disjuntas são alternativas quando preservam oclusão e
  densidade. Escolha cortes pela silhueta projetada na câmera real, inclusive fora da grade.
- Misturar imagens com alpha reduzido pode mudar opacidade. Compare composição
  pré-multiplicada, orientação e estado térmico nas implementações de destino.
- Em cenas de geração, limitar objetos vivos ao necessário evita trabalho alheio à
  exportação. Preserve o arquivo autoral e diferencie tempo de preparação, render e IO.
- Para limites de arquivo, considere dividir transporte mantendo os payloads originais
  e conferir a remontagem por hash. Limite de hospedagem não exige reduzir quadros,
  resolução ou duração. Tamanho codificado não mede custo decodificado ou GPU.
- Animação de máquinas e efeitos deve seguir o relógio e o trabalho da simulação:
  pausa, bloqueio, save e retomada precisam escolher a mesma pose. Um animador autônomo
  de imagem pode quebrar esse contrato. Teste também o caminho de compatibilidade.
- Reutilize canvas/texturas e feche imagens/decodificadores quando apropriado. Meça
  montagem, aquecimento e descarte repetidos; histórico de HMR não isola vazamento.
- Preserve assets não afetados e suas referências. Um refinamento estático não exige
  regenerar bancos animados intactos. Compare manifestos e inventário distribuído
  separadamente antes de afirmar aumento ou redução de download.
- Variação de material não substitui detalhe funcional de forma, e distribuir mais
  módulos não prova composição natural. Se a receita recusa que mais módulos provem a composição, o `content` nomeia a composição que a receita já recusa. Arquivo no disco não é o mundo. Sem chave `composição`. Observe repetição, escala e leitura no jogo;
  uma mudança artística não deve ser anunciada como otimização técnica.

Referências: Era Uma Vez no playground, troca de assets em protótipo Unity, Ink `RE-INK-004/007/009`
e LDtk `RE-LDTK-005/006/010` ([fontes](../references/sources.md)).
