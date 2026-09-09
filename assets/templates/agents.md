# AGENTS — {{PROJECT}}

Projeto: {{PROJECT_PATH}}
Status: rascunho. Este arquivo é a memória persistente do agente neste jogo: o que ele
precisa saber antes de mudar qualquer coisa e o que não pode inferir da conversa.
Mantenha-o curto e verdadeiro; instrução desatualizada é pior que ausente.

## Executar e verificar

- Rodar o jogo: [comando exato, porta, dispositivo ou editor; onde abrir].
- Validadores: [comando de teste, lint, build; o que cada um cobre e o que não cobre].
- Cenário real de verificação: [trecho jogável a atravessar antes de declarar pronto].
- O que nunca rodar sem pedir: [publicar, apagar saves, comandos que tocam fora do projeto].

## Convenções que o código não explica

- Engine e versão: [nome e versão exata; pacote de plataforma do framework, se houver].
- Onde vive cada coisa: [regra / apresentação / conteúdo / saves — pastas e módulos canônicos].
- Contratos que não mudam sem decisão registrada: [loop, estado, formato de save, entrada, eventos].
- Padrões proibidos aqui: [ex.: IA por quadro, singleton novo, dependência nova sem lacuna explícita].

## Documentos canônicos

- Design: [docs/gdd.md ou game-design.md].
- Requisitos e arquitetura: [docs/prd.md, docs/tdd.md].
- Design system do jogo: [docs/art-bible.md].
- Decisões e continuidade: [docs/devlog.md — atualizar "Continuidade" antes de encerrar].
- QA e evidência: [docs/qa.md; pastas de `verify` e `record`].

## Como trabalhar neste jogo

- Um subsistema por iteração; especifique antes de gerar código não trivial.
- REUSE → ADAPT → CREATE: leia candidatos e consumidores antes de criar; CREATE exige lacuna escrita.
- Bug: reproduza no caminho real, isole a causa, corrija a causa, adicione a regressão. Não troque de modelo antes de entender.
- Entrega auditável: diga o que mudou, como verificar, o que ficou de fora. Conclusão da IA é alegação até a observação.
- Preserve a direção aprovada e as exigências explícitas do usuário; não "melhore" o que não foi pedido.

## Limites da IA neste projeto

- Zonas de risco onde a IA mais erra e a revisão humana é obrigatória: [rede/netcode, física, shaders, migração de save, performance — marcar as que existem aqui].
- API que a IA costuma inventar nesta engine/versão: [anotar quando acontecer].
- Assets gerados por IA: [política adotada: proibidos / permitidos com registro de origem e ferramenta / só provisórios].
