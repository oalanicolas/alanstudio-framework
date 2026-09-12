# Release

Converter "funciona aqui" em "funciona para alguém": build limpo a partir de um
clone e de uma versão declarada, artefato exportado rodando em máquina que não é a
de desenvolvimento, primeira execução fria, orçamento de tamanho e tempo até jogar,
proveniência de tudo que embarca, registro de falha e reversão. Prepara e verifica;
**não publica** e não concede autorização. Receita: [release](../recipes/release.md).

## Escala

`jam`: build/export executável por outra pessoa a partir do runbook (`playable`).
`product`: build reproduzível de versão declarada; o artefato, não o editor, é o
que se verifica (`slice`). `aa`: orçamentos, plataforma real, registro de falha,
reversão e proveniência completa (`shippable`); publicar como rotina de baixo risco
é `flagship`.

## Avaliar

1. `context <projeto> --focus release --stage release`. `gate <projeto> --gate
   deliver` ([gates](../references/gates.md)): `licensing` não se dispensa — licença desconhecida bloqueia, não recebe
   suposição. `bar <projeto>`: dimensões abaixo de `shippable` são a lista do que
   a nota da versão precisa declarar como lacuna.
2. Leia o runbook e o pacote da plataforma (alvos, exportação, onde ficam os
   requisitos de loja/console na fonte oficial).
3. Inventário do que embarca: cada asset, fonte, som, biblioteca e recurso gerado,
   com origem, crédito e condição de uso compatíveis com a distribuição pretendida.
   Assets gerados por IA seguem a política do `AGENTS.md`.
4. **Autorização primeiro:** nada aqui autoriza publicar, criar conta, subir
   artefato, contatar pessoas ou anunciar. Pergunte só isso ao usuário quando a
   publicação fizer parte do pedido; não pergunte o que o runbook já responde.

## Executar

Clone limpo → build pelo runbook, por outra pessoa ou em ambiente que não é o de
desenvolvimento → artefato exportado no dispositivo alvo com a entrada, resolução e
sistema pretendidos → instalação limpa sem save, cache ou permissão → save da versão
anterior migrando ([persistência](../recipes/persistence.md)) → procedimento de
reversão escrito, com o que acontece aos saves novos → nota da versão com o que
não atende. Registro de falha exige decisão explícita sobre o que é enviado e
consentimento; telemetria não é padrão silencioso. Se a receita recusa que telemetria seja padrão silencioso, o `scan` nomeia a telemetria que a receita já recusa. Área no disco não é consentimento. Sem chave `telemetria`.

## Verificar

A tabela do gate `deliver` com uma linha por critério (`met`/`unmet`/`waived`/
`out_of_scope`) e o que sustenta cada estado: quem construiu, quando, onde está o
log. `verify` do build com recibo; `record --kind budget` para tamanho e tempo até
jogar; `record --kind milestone` para a decisão de entregar, por pessoa.
`held_by_declaration` não é `passed`; `granted` é sempre falso.

## Nunca

- Publicar, subir artefato ou anunciar sem autorização explícita para aquela entrega.
- Verificar o editor ou o servidor de desenvolvimento no lugar do artefato.
- Presumir licença de asset localizado; localização não atribui autoria. Se o release recusa que localização atribua autoria, a área `provenance` do `scan` nomeia a localização que o release já recusa. Localização no disco não é o titular. Sem chave `localização`.
- Dispensar `licensing`, ou marcar `met` sem nada escrito ao lado.
- Chamar de entregável o que só rodou na máquina de quem construiu.

## Entregar

O artefato, a versão, onde rodou e quem viu, a tabela do gate, a nota da versão com
lacunas, o procedimento de reversão e — separadamente — a pergunta de publicação,
se couber. Sequência: [`harden`](harden.md) se algum critério de confiança falhou.
