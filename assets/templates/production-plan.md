# Plano de produção — {{PROJECT}}

Projeto: {{PROJECT_PATH}}
Status: rascunho. Autor/revisão: [preencher]. Fontes: [brief/GDD, PRD, TDD, vertical slice].
Receita: `framework/recipes/production.md`. Marcos são gates de evidência, não datas.
Nenhum comando do harness promove um marco; a passagem é declarada por pessoa com a prova ligada.
Provas ficam em recibos de pasta inédita: `verify` (técnica), `record --kind observation|budget|milestone`.

## Alvo de acabamento

- Plataformas e entradas alvo: [dispositivo, resolução, taxa de quadros, controles].
- Referência de acabamento: [jogos/trechos que definem o piso pretendido; o que deles importa].
- Lentes obrigatórias neste jogo: [design, arte, animação, áudio, UX/UI, técnica, QA, acesso, localização; justificar ausências].
- O que não pode degradar: [qualidade aprovada e exigências explícitas do usuário].

## Orçamentos

Valores medidos no caminho real, na plataforma alvo. Número sem medição é hipótese.

| Orçamento | Plataforma | Meta | Medido | Como medir | Estado |
| --- | --- | --- | --- | --- | --- |
| Tempo de quadro (p50/p99) | [preencher] | [ms] | [ms ou lacuna] | [ferramenta e cena] | hipótese / medido / violado |
| Memória (pico) | [preencher] | [MB] | [preencher] | [preencher] | [preencher] |
| Carregamento inicial / entre cenas | [preencher] | [s] | [preencher] | [preencher] | [preencher] |
| Tamanho do build | [preencher] | [MB] | [preencher] | [preencher] | [preencher] |
| Latência entrada → resposta visível | [preencher] | [ms/quadros] | [preencher] | [preencher] | [preencher] |

## Marcos e gates

Para cada marco: critério observável, evidência ligada e quem declarou a passagem.

- **First playable:** ciclo central jogável de ponta a ponta com placeholders. Prova: [cenário, build, observação]. Estado: [pendente / atingido em (data, evidência)].
- **Vertical slice:** trecho representativo no acabamento pretendido; receita de conteúdo compreendida. Prova: [preencher]. Estado: [preencher].
- **Alpha (feature complete):** todos os sistemas do recorte presentes; conteúdo pode ser parcial; nenhum bloqueador conhecido sem plano. Prova: [preencher]. Estado: [preencher].
- **Beta (content complete):** todo o conteúdo do recorte; orçamentos dentro da meta ou desvio aprovado; localização e acesso implementados; playtest externo observado. Prova: [preencher]. Estado: [preencher].
- **Gold / release candidate:** zero bloqueadores; soak e reinstalação/atualização/save verificados; checklist da plataforma revisado; créditos e licenças completos. Prova: [preencher]. Estado: [preencher].
- **Live (se houver):** telemetria mínima, canal de relato, plano de hotfix e de conteúdo. Prova: [preencher]. Estado: [preencher].

## Pipeline de conteúdo

- Fonte → importação → validação → runtime: [ferramentas, formatos, convenções de nome, escala/pivot, LODs, compressão].
- Receita por família de asset: [passos para o próximo personagem/nível/efeito nascer dentro do piso].
- Validações automáticas: [scripts que checam nomes, tamanhos, referências quebradas; comando real].
- Localização: [idiomas, extração de textos, fontes, pseudo-localização; ou decisão explícita de não localizar].

## Riscos

| ID | Risco | Impacto no jogador | Sinal antecipado | Mitigação / PoC | Dono | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| RISK-01 | [preencher] | [preencher] | [preencher] | [preencher] | [preencher] | aberto / mitigado / aceito |

## Estabilidade e qualidade contínua

- Testes automáticos e ordem: [comandos reais; o que cobrem e o que não cobrem].
- Soak/estresse: [duração, cenário, memória ao longo do tempo; resultado ou lacuna].
- Saves e atualização: [migração, dados inválidos, reinstalação; não apagar saves reais].
- Relato de falhas: [captura de crash/logs, reprodução mínima, triagem].

## Continuidade

- Onde estamos: [marco real e última entrega com evidência].
- Próximo passo: [verbo, alvo e saída; ID existente quando houver].
- Por que agora / pronto quando: [dependência ou risco prioritário; evidência que encerra].
- Retomar por: [seção deste plano, arquivo/tarefa e consumidores a ler].
