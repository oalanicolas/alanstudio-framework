# Release

Converter "funciona aqui" em "funciona para alguém": build limpo a partir de um
clone e de uma versão declarada, artefato exportado rodando em máquina que não é a
de desenvolvimento, primeira execução fria, orçamento de tamanho e tempo até jogar,
proveniência de tudo que embarca, registro de falha e reversão. Prepara e verifica;
prepara o artefato. Receita: [release](../recipes/release.md).

## Recuperação do envio

O upload TUS consulta o offset confirmado após uma falha de rede antes de reenviar
dados. A consulta também tenta novamente quando o DNS ou a conexão falha; ela não
presume que o último lote foi perdido. As tentativas são limitadas e, se esgotadas,
o deploy falha sem declarar publicação. Não há retomada entre processos encerrados.

## Crawlers em sites estáticos

Em `workspace.json`, `deploy.block_ai_bots: true` ativa regras para GPTBot,
ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot
e Perplexity-User. O atalho direto também lê essa declaração; o empacotador aceita
`--block-ai-bots` para uma publicação avulsa.

O pacote preserva as `.htaccess` incluídas no build, também em subpastas, e
antepõe o bloqueio a suas rotas e arquivos. Substitui os grupos desses agentes
no `robots.txt`, preservando regras
dos demais crawlers e sitemaps; o arquivo fica público. Nenhum arquivo do
build local é alterado. A conferência remota exige bloqueio em `/` e em um arquivo
amostrado para cada agente, além das diretivas públicas. Respostas 403 exigem
`Cache-Control: no-store` e `Vary: User-Agent`. HTTP 429 do provedor é
registrado como bloqueio observado; não prova que a regra na origem executou.
Após publicar, invalide caches do provedor e confira também arquivos que já tinham
sido servidos a navegadores.

Com essa opção, configurações incluídas com `RewriteEngine` diferente de `On` ou blocos
condicionais `<If>` são recusadas antes de montar o ZIP ou enviar. Elas podem
desligar o filtro ou sobrescrever seus cabeçalhos depois de `FilesMatch`;
o empacotador não reativa regras do aplicativo que foram desligadas. Configurações
excluídas pelo filtro do build não são lidas nem publicadas por esta camada.

Essa camada filtra identificações declaradas, não impede um cliente de usar o
User-Agent de um navegador. Login só protege o jogo quando o servidor valida a
sessão também nos arquivos e APIs. Uma pessoa autorizada ainda recebe os arquivos
necessários para jogar. Rate limiting, desafios validados no servidor e regras de
WAF exigem configuração do provedor; não são instalados por esta opção.

Fontes: [OpenAI](https://developers.openai.com/api/docs/bots),
[Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler),
[Perplexity](https://docs.perplexity.ai/docs/resources/perplexity-crawlers).

## Escala

`jam`: build/export executável por outra pessoa a partir do runbook (`playable`).
`product`: build reproduzível de versão declarada; o artefato, não o editor, é o
que se verifica (`slice`). `aa`: orçamentos, plataforma real, registro de falha,
reversão e proveniência completa (`shippable`); publicar como rotina de baixo risco
é `flagship`.

## Avaliar

1. `context <projeto> --focus release --stage release`. `gate <projeto> --gate
   deliver` ([gates](../references/gates.md)). `bar <projeto>`: dimensões abaixo de `shippable` são a lista do que
   a nota da versão precisa declarar como lacuna.
2. Leia o runbook e o pacote da plataforma (alvos, exportação, onde ficam os
   requisitos de loja/console na fonte oficial).
3. Inventário do que embarca: cada asset, fonte, som, biblioteca e recurso gerado,
   com origem, crédito e condição de uso compatíveis com a distribuição pretendida.
   Assets gerados por IA seguem a política do `AGENTS.md`.
4. **Contato:** não contatar pessoas nem criar conta em nome do usuário. Não
   pergunte o que o runbook já responde.

## Executar

Clone limpo → build pelo runbook, por outra pessoa ou em ambiente que não é o de
desenvolvimento → artefato exportado no dispositivo alvo com a entrada, resolução e
sistema pretendidos → instalação limpa sem save, cache ou permissão → save da versão
anterior migrando ([persistência](../recipes/persistence.md)) → procedimento de
reversão escrito, com o que acontece aos saves novos → nota da versão com o que
não atende. Registro de falha exige decisão explícita sobre o que é enviado e
consentimento; telemetria não é padrão silencioso.

## Verificar

A tabela do gate `deliver` com uma linha por critério (`met`/`unmet`/`waived`/
`out_of_scope`) e o que sustenta cada estado: quem construiu, quando, onde está o
log. `verify` do build com recibo; `record --kind budget` para tamanho e tempo até
jogar; `record --kind milestone` para a decisão de entregar, por pessoa.
`held_by_declaration` não é `passed`; `granted` é sempre falso.

## Nunca

- Verificar o editor ou o servidor de desenvolvimento no lugar do artefato.
- Marcar `met` sem nada escrito ao lado.
- Chamar de entregável o que só rodou na máquina de quem construiu.

## Entregar

O artefato, a versão, onde rodou e quem viu, a tabela do gate, a nota da versão com
lacunas, o procedimento de reversão e — separadamente — a pergunta de publicação,
se couber. Sequência: [`harden`](harden.md) se algum critério de confiança falhou.
