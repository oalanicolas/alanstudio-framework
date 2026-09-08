# Conteúdo, assets e progresso

Entrada: nível, história, entidade ou recurso visual/sonoro a adicionar ou substituir.

Leia o formato atual, sua carga em runtime e os consumidores. Procure definição ou
slot substituível antes de duplicar lógica. Preserve identidade, escala, pivot,
colisões, animações e referências ao trocar arte. Registre origem e condições de
uso; conteúdo baixado não recebe uma licença nova pelo simples reuso.

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

Referências de estudo: Ink `RE-INK-004/007/009` e LDtk `RE-LDTK-005/006/010`.
[Fontes](../references/sources.md).
