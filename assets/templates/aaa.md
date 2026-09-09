# Checklist de piso de acabamento — {{PROJECT}}

Projeto: {{PROJECT_PATH}}
Status: rascunho. Preencher este arquivo **não** certifica AAA de publisher,
não mede diversão e não autoriza publicar. “AAA” = piso da fatia observada.
Contrato: `framework/references/ambition.md` e
`framework/references/aaa-checklist.md`.

- Escala: [jam/conto · produto · AA / Triple-I].
- Recorte observado: [slice / capítulo / verbo; o que está fora].
- Promessas do recorte: [cinemática, HUD, save, rede, localização, acesso…].
- Referência aprovada: [localizador, quem aprovou, o que não cobre].
- Observador / data / versão / dispositivo / entrada: [preencher].
- Legenda: `não executado` · `observado` · `inconclusivo` · `N/A` (motivo).

Não some linhas. Screenshot isolada não fecha feel, animação, câmera, mix
nem pacing. N/A exige motivo. Vermelho material bloqueia o adjetivo.

## 0. Contrato — CHK-0

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-0.1 | Escala e recorte estão explícitos; o adjetivo “AAA” não foi usado sem as barras | Brief/slice; busca pelo adjetivo no recorte | não executado | |
| CHK-0.2 | Direção aprovada tem alcance; o que ela não cobre está escrito | Art Bible / conversa; mock ≠ mecânica | não executado | |
| CHK-0.3 | Scaffold, PoC e slice não estão confundidos | Nome do build vs. comportamento | não executado | |
| CHK-0.4 | Itens não prometidos estão `N/A` com motivo; nada foi inventado para “completar AAA” | Rede, live ops, localização, mocap… | não executado | |

## 1. Verbo e decisão — CHK-1

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-1.1 | Há um verbo central nomeado e jogável | GDD + uma partida curta | não executado | |
| CHK-1.2 | A escolha muda estado, rota, recurso ou expectativa | Alternativa A vs. B no mesmo cenário | não executado | |
| CHK-1.3 | O risco é legível **antes** da punição | Informação disponível no momento da ação | não executado | |
| CHK-1.4 | Recusa é distinta de sucesso (estado e feedback) | Recurso insuficiente, alvo inválido, após término | não executado | |
| CHK-1.5 | Não há opção sempre dominante no recorte, ou isso é decisão explícita | Duas alternativas sob o mesmo cenário | não executado | |
| CHK-1.6 | Término e reinício do ciclo estão definidos e jogáveis | Vitória, derrota, saída, repeat | não executado | |

## 2. Primeiro minuto — CHK-2

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-2.1 | A primeira ação ensina o verbo sem mural que bloqueia o jogo | Cold start, instrução neutra | não executado | |
| CHK-2.2 | Input, frame e câmera do primeiro minuto não denunciam atraso nem stutter | Observação em movimento no boot | não executado | |
| CHK-2.3 | A fantasia é reconhecível antes do brief | O que a pessoa faz e vê nos primeiros 60s | não executado | |

## 3. Controle e câmera — CHK-3

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-3.1 | O verbo responde no dispositivo alvo (teclado / toque / gamepad) | Mesma ação em cada entrada prometida | não executado | |
| CHK-3.2 | Buffer, deadzone, cancelamento e perda de foco foram exercitados | Alt-tab, gesto abortado, reconexão | não executado | |
| CHK-3.3 | Câmera antecipa curva/ameaça sem ocluir o jogador nem enjoar | Percurso real, não still | não executado | |
| CHK-3.4 | Look-ahead, aterrissagem e punch confirmam a ação e devolvem o controle | Trecho do verbo central | não executado | |
| CHK-3.5 | Escala e transição de câmera preservam leitura de ameaça e landmark | Zoom, corte, indoor/outdoor se existirem | não executado | |

## 4. Feel sincronizado — CHK-4

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-4.1 | Intenção: oportunidade e ameaça são legíveis antes do input | Frame anterior à ação | não executado | |
| CHK-4.2 | Antecipação (pose/frames) promete o golpe/pulo/disparo | Comparar com e sem wind-up | não executado | |
| CHK-4.3 | Corpo muda silhueta o bastante (squash, recuo, IK, veículo, cursor) | Em movimento | não executado | |
| CHK-4.4 | Impacto tem peso proporcional (hitstop, flash, partícula, rumble) | Coleta ≠ golpe mortal | não executado | |
| CHK-4.5 | Flash, hit-pause, shake, partícula e áudio disparam no **mesmo frame** do contato | Gravação quadro a quadro ou observação atenta | não executado | |
| CHK-4.6 | Recuperação devolve o controle num tempo justo | Encadear a próxima ação | não executado | |
| CHK-4.7 | Juice não esconde a consequência nem atrasa o próximo input além do ritmo | Silhueta e timing | não executado | |
| CHK-4.8 | Feel sobrevive a pause, unfocus e restart (sem hitstop/rumble fantasma) | Montar → pausar → retomar; reset | não executado | |

## 5. Áudio e mix — CHK-5

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-5.1 | A ação central se ouve; recusa soa distinta do sucesso | Com som; comparar os dois | não executado | |
| CHK-5.2 | One-shot de impacto no mesmo frame do hit visual | Sync com CHK-4.5 | não executado | |
| CHK-5.3 | Camadas (ação, mundo, música, UI, silêncio) têm prioridade; ducking existe | Stinger vs. verbo vs. música | não executado | |
| CHK-5.4 | Pause, morte, restart, troca de cena e unfocus não deixam voz fantasma | Montar → desmontar → montar | não executado | |
| CHK-5.5 | O jogo permanece legível no mute, se o recorte exigir acesso ou ruído | Mesmo trecho com mute | não executado | |
| CHK-5.6 | Piso de gravação licenciada ou direção contemporânea explícita; 8-bit/jsfxr/Kenney não são o padrão | Proveniência do asset | não executado | |
| CHK-5.7 | Música informa estado (ou a ausência é decisão registrada) | Entrar/sair de combate, menu, morte | não executado | |
| CHK-5.8 | `shared/sfx` foi buscado antes de baixar, se o laboratório o tiver | Recibo de `sfx search` | não executado | |

## 6. Pacing e performance — CHK-6

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-6.1 | Latência de input é aceitável no dispositivo alvo | Ação repetida; percepção + medição se existir | não executado | |
| CHK-6.2 | Spikes de frametime no trecho real foram procurados; stutter não é “normal” | Percurso carregado, não menu vazio | não executado | |
| CHK-6.3 | O piso visual/sonoro aprovado não foi cortado para “ganhar FPS” | Antes/depois; hipótese de eficiência | não executado | |
| CHK-6.4 | Ambiente da prova está declarado (editor vs. build/export, resolução, plataforma) | Runbook do recorte | não executado | |

## 7. Mundo, luz, animação, consistência — CHK-7

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-7.1 | Silhueta, material e luz são legíveis **em movimento** | Percurso; não a melhor still | não executado | |
| CHK-7.2 | Landmark e ameaça distinguem-se sem a cor como único sinal | Formas, movimento, áudio | não executado | |
| CHK-7.3 | Animação tem antecipação e follow-through no verbo; não está “floaty” | Comparar com referência | não executado | |
| CHK-7.4 | Família coerente com o asset-herói **no engine**, mesma luz/câmera | Hero comparison in-engine | não executado | |
| CHK-7.5 | Asset lindo no DCC e errado no jogo foi procurado (integração) | Import real, shader, escala, pivot | não executado | |
| CHK-7.6 | Um exemplo de “cabe neste jogo” e um de “quebra a direção” existem | Art Bible | não executado | |

## 8. UI, HUD e acesso — CHK-8

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-8.1 | HUD/menus existem e são do jogo, **ou** a ausência é decisão explícita | Art Bible / GDD | não executado | |
| CHK-8.2 | Contraste e forma além da cor permitem ler estado crítico | Daltonismo, UI em movimento | não executado | |
| CHK-8.3 | Foco, alvos de toque e movimento reduzido quando o recorte os exige | Dispositivo prometido | não executado | |
| CHK-8.4 | UI não grita sobre o mundo; não tapa a silhueta da consequência | Mix + layout | não executado | |
| CHK-8.5 | Navegação de menu sobrevive a pause, erro e volta ao jogo | Ida e volta | não executado | |

## 9. Narrativa e cinemática — CHK-9

`N/A` se o recorte não promete história, voz ou cutscene. Se o marketing
promete imersão cinematográfica, estes itens tornam-se aplicáveis.

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-9.1 | História/escolha tem consequência jogável, não só texto | Caminho alternativo | não executado | |
| CHK-9.2 | Voz, lip-sync e tom são consistentes (estilização ok; costura entre equipes não) | Cena representativa | não executado | |
| CHK-9.3 | Corte/câmera de cena não rouba o verbo nem contradiz o feel | Transição jogo ↔ cena | não executado | |
| CHK-9.4 | Save/histórico narrativo restaura o que o GDD promete | Load no meio da escolha | não executado | |

## 10. Receita de conteúdo e produção — CHK-10

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-10.1 | Existe receita para o próximo item da família (inimigo, sala, efeito) | Art Bible / GDD | não executado | |
| CHK-10.2 | A slice usou o **pipeline real**, não um atalho irrepetível | Ferramenta, import, naming | não executado | |
| CHK-10.3 | Custo observado do próximo trecho está registrado | Tempo/esforço medido, não chute | não executado | |
| CHK-10.4 | Repeatability: outro trecho nasce sem heroísmo | Quatro eixos: valor, técnica, produção, clareza | não executado | |
| CHK-10.5 | Tokens têm consumidor real; arquivo órfão não conta | Path do uso | não executado | |

## 11. Ciclo de vida e confiança — CHK-11

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-11.1 | Iniciar, jogar, pausar, perder, ganhar, reiniciar e sair têm consequência definida | Cada transição uma vez | não executado | |
| CHK-11.2 | Score, timer, entidade, som, input e progresso sobrevivem ou zeram como o GDD diz | Pause/reset/load | não executado | |
| CHK-11.3 | Save (se prometido) não corrompe; migração/dado inválido está tratado | Load, save velho, arquivo lixo | não executado | |
| CHK-11.4 | Descarte: montar → desmontar → montar sem listener/áudio/GPU duplicado | Dois boots seguidos | não executado | |
| CHK-11.5 | Erro (falha de load, input, rede se houver) fala a verdade ao jogador | Caminho de falha real | não executado | |

## 12. Rede — CHK-12

`N/A` se o recorte é local / um jogador sem estado compartilhado.

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-12.1 | Quem aceita a ação e quem decide o estado está explícito | Duas sessões reais | não executado | |
| CHK-12.2 | Ação recusada no autoritativo, não só na UI | Cliente desonesto ou replay | não executado | |
| CHK-12.3 | Entrada, saída, desconexão e reconexão foram exercitadas | Duas sessões | não executado | |
| CHK-12.4 | Mensagem duplicada, atrasada ou fora de ordem não quebra o recorte | Quando o protocolo permite | não executado | |

## 13. Localização — CHK-13

`N/A` se o recorte não promete outro idioma. Promessa de público amplo
torna o item aplicável.

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-13.1 | Textos do recorte não estão hardcoded sem gancho de locale | UI + diálogo do trecho | não executado | |
| CHK-13.2 | Overflow, fonte e leitura funcionam no idioma alvo (ou a lacuna está explícita) | Idioma mais longo se houver | não executado | |

## 14. QA, playtest e evidência — CHK-14

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-14.1 | Casos técnicos do recorte têm comando real e recibo (`verify` ou equivalente) | Logs; inspect antes de rodar | não executado | |
| CHK-14.2 | Playtest (pessoa) e avaliação do agente estão separados | Relato literal vs. interpretação | não executado | |
| CHK-14.3 | Comparação antes/depois em condições equivalentes, em movimento | Versão, resolução, entrada, trecho | não executado | |
| CHK-14.4 | `experience_status` permanece `not_assessed` até haver observação em movimento | Recibo de verify | não executado | |

## 15. Origem e direitos — CHK-15

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-15.1 | Código e assets do recorte têm origem, crédito e condição de uso | CREDITS / proveniência | não executado | |
| CHK-15.2 | Nada recebeu licença inventada pela pasta em que está | Arquivo baixado / gerado | não executado | |

## 16. Tier de mercado (contexto, não piso) — CHK-16

Todos começam `N/A` salvo se o projeto **for** desse tier. Não usar para
reprovar um conto ou um AA / Triple-I.

| ID | Item | Como observar | Estado | Evidência / lacuna |
| --- | --- | --- | --- | --- |
| CHK-16.1 | Publisher, orçamento e headcount reais (se existirem) | Fato, não meta | N/A | Não é condição do piso. |
| CHK-16.2 | Live ops / temporada / microtransação | Só se o produto as tiver | N/A | Não inventar. |
| CHK-16.3 | Certificação de console / XR / BVT | Só se houver submissão | N/A | Não é selo de acabamento. |
| CHK-16.4 | Marketing blockbuster, celebridade, AAAA | Só como contexto | N/A | Buzzword; sem definição. |

## Resumo do recorte

- Aplicáveis observados: [IDs].
- Aplicáveis inconclusivos: [IDs].
- Aplicáveis não executados: [IDs].
- N/A com motivo: [IDs].
- **O que ainda impede chamar isto de piso de acabamento:** [IDs materiais].
- Próxima ação (uma): [verbo, alvo, prova].
- Aprovação do usuário: [somente se concedida; senão, avaliação do agente].
