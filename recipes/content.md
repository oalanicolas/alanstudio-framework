# Conteúdo, assets e progresso

Entrada: nível, história, entidade ou recurso visual/sonoro a adicionar ou substituir.

O harness lê se o conteúdo saiu do código com `content <projeto>` (`data/`,
`levels/`, `.ldtk`/`.tmx`/`.ink`). Arquivo de dados não é volume
suficiente — `enough` é sempre falso. Sem arquivo, `next` propõe
`content.inline`. O starter `canvas-arcade` extrai a chuva para
`data/spawn.json`; uma mesa não é escala.

Leia o formato atual, sua carga em runtime e os consumidores. Procure definição ou
slot substituível antes de duplicar lógica. Preserve identidade, escala, pivot,
colisões, animações e referências ao trocar arte. Som novo: consulte
`shared/sfx` no laboratório (`sfx search`) antes de baixar; copie o arquivo e a
proveniência. Mix, interrupção e silêncio seguem [áudio](audio.md), não apenas
a cópia do arquivo. Registre origem e condições de uso; conteúdo baixado não
recebe uma licença nova pelo simples reuso.

Geração externa (Magnific e similares) distingue capacidades documentadas de
integração comprovada. Não torna o fornecedor obrigatório.

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
comprova que está sendo consumido.

Referências: Era Uma Vez no playground, troca de assets em protótipo Unity, Ink `RE-INK-004/007/009`
e LDtk `RE-LDTK-005/006/010` ([fontes](../references/sources.md)).
