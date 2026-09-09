# Checklist de piso de acabamento — {{PROJECT}}

Projeto: {{PROJECT_PATH}}
Status: rascunho. Preencher **não** certifica AAA de publisher, não mede
diversão e não autoriza publicar. “AAA” = piso da fatia observada.
Contrato: `framework/references/ambition.md` e
`framework/references/aaa-checklist.md`.

- Escala: [jam/conto · produto · AA / Triple-I] → perfil do `finish`.
- Recorte: [slice / capítulo / verbo; o que está fora].
- Promessas: [cinemática, HUD, save, rede, locale, haptic, 30/60/120…].
- Referência aprovada: [localizador, quem, o que não cobre].
- Observador / data / versão / dispositivo / entrada: [preencher].
- Origem: ID canônico (GDD-M01, FR-001, foco feel…) ou “recorte”.

Jam: só **núcleo**; resto `N/A` com a escala. Não abra este arquivo na
primeira sessão. Produto/AA: núcleo + produto + promessas do brief, na slice.
Mercado nunca reprova jam. Não some linhas. Still não fecha feel/mix/pacing.

Legenda: `não executado` · `observado` · `inconclusivo` · `N/A` (motivo).

## Núcleo — qualquer escala após um ciclo jogável

### 0. Contrato — CHK-0 · núcleo

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-0.1 | Escala e recorte explícitos; “AAA” não usado sem as barras | Brief/slice; busca do adjetivo | brief | não executado | |
| CHK-0.2 | Direção aprovada tem alcance; o que não cobre está escrito | Art Bible / conversa; mock ≠ mecânica | art-bible | não executado | |
| CHK-0.3 | Scaffold, PoC e slice não estão confundidos | Nome do build vs. comportamento | slice | não executado | |
| CHK-0.4 | Fora do perfil está `N/A` com motivo; nada inventado para “completar AAA” | Rede, live ops, locale, mocap | finish | não executado | |

### 1. Verbo e decisão — CHK-1 · núcleo

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-1.1 | Verbo central nomeado e jogável | GDD + uma partida curta | GDD-M | não executado | |
| CHK-1.2 | A escolha muda estado, rota, recurso ou expectativa | Alternativa A vs. B no mesmo cenário | GDD-M / MDA | não executado | |
| CHK-1.3 | O risco é legível **antes** da punição | Informação no momento da ação | GDD-M | não executado | |
| CHK-1.4 | Recusa distinta de sucesso (estado e feedback) | Recurso, alvo inválido, após término | GDD-M / mechanics | não executado | |
| CHK-1.5 | Sem opção sempre dominante, ou isso é decisão explícita | Duas alternativas | MDA | não executado | |
| CHK-1.6 | Término e reinício do ciclo definidos e jogáveis | Vitória, derrota, saída, repeat | GDD / lifecycle | não executado | |

### 2. Primeiro minuto — CHK-2 · núcleo

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-2.1 | A primeira ação ensina o verbo sem mural que bloqueia | Cold start, instrução neutra | GDD | não executado | |
| CHK-2.2 | Input, frame e câmera do boot sem atraso nem stutter | Movimento nos primeiros segundos | feel / pacing | não executado | |
| CHK-2.3 | A fantasia é reconhecível antes do brief | O que a pessoa faz e vê ~60s | brief | não executado | |

### 4. Feel sincronizado — CHK-4 · núcleo · `--focus feel`

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-4.1 | Intenção: oportunidade e ameaça legíveis antes do input | Frame anterior à ação | feel | não executado | |
| CHK-4.2 | Antecipação (pose/frames) promete o golpe/pulo/disparo | Com vs. sem wind-up | feel | não executado | |
| CHK-4.3 | Corpo muda silhueta o bastante | Squash, recuo, IK, veículo, cursor | feel | não executado | |
| CHK-4.4 | Impacto com peso proporcional | Coleta ≠ golpe mortal | feel | não executado | |
| CHK-4.5 | Flash, hit-pause, shake, partícula e áudio no **mesmo frame** do contato | Gravação ou observação atenta | feel + audio | não executado | |
| CHK-4.6 | Recuperação devolve o controle num tempo justo | Encadear a próxima ação | feel | não executado | |
| CHK-4.7 | Juice não esconde a consequência nem atrasa o próximo input | Silhueta e timing | feel | não executado | |
| CHK-4.8 | Feel sobrevive a pause, unfocus e restart | Sem hitstop/rumble fantasma | lifecycle | não executado | |
| CHK-4.9 | Cancelamento ou overlap não deixa o feel preso | Abortar gesto; duas ações seguidas | feel / input | não executado | |

### 5. Áudio e mix — CHK-5 · núcleo · `--focus audio`

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-5.1 | Ação central se ouve; recusa soa distinta | Com som; os dois casos | audio | não executado | |
| CHK-5.2 | One-shot de impacto no mesmo frame do hit visual | Sync com CHK-4.5 | audio | não executado | |
| CHK-5.3 | Camadas com prioridade; ducking existe | Stinger vs. verbo vs. música | audio | não executado | |
| CHK-5.4 | Pause, morte, restart, cena e unfocus sem voz fantasma | Montar → desmontar → montar | lifecycle | não executado | |
| CHK-5.5 | Legível no mute se o recorte exigir acesso ou ruído | Mesmo trecho mutado | audio / acesso | não executado | |
| CHK-5.6 | Piso de gravação licenciada ou direção contemporânea explícita | Sem 8-bit/jsfxr/Kenney como padrão | proveniência | não executado | |
| CHK-5.7 | Música informa estado, ou a ausência é decisão | Combate, menu, morte | audio | não executado | |
| CHK-5.8 | `sfx search` antes de baixar, se `shared/sfx` existir | Recibo | audio | não executado | |
| CHK-5.9 | Espacialização só se o jogo já tem espaço; sem HRTF de checklist | 2D/3D real | audio | não executado | |

### 6. Pacing e performance — CHK-6 · núcleo

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-6.1 | Latência de input aceitável no dispositivo alvo | Ação repetida; medição se existir | feel | não executado | |
| CHK-6.2 | Spikes de frametime procurados no trecho **carregado** | Não o menu vazio | visual / TDD | não executado | |
| CHK-6.3 | Piso aprovado não foi cortado para “ganhar FPS” | Antes/depois; hipótese de eficiência | quality | não executado | |
| CHK-6.4 | Ambiente da prova declarado | Editor vs. export, resolução, plataforma | runbook | não executado | |
| CHK-6.5 | Se o recorte declara 30/60/120, o feel é equivalente | Mesma ação nas taxas prometidas | TDD / NFR | não executado | |

### 11. Ciclo de vida e confiança — CHK-11 · núcleo · `--focus lifecycle`

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-11.1 | Iniciar, jogar, pausar, perder, ganhar, reiniciar e sair definidos | Cada transição | lifecycle | não executado | |
| CHK-11.2 | Score, timer, entidade, som, input e progresso batem com o GDD | Pause/reset/load | lifecycle | não executado | |
| CHK-11.3 | Save (se prometido) não corrompe; dado inválido tratado | Load, save velho, arquivo lixo | content | não executado | |
| CHK-11.4 | Montar → desmontar → montar sem listener/áudio/GPU duplicado | Dois boots | lifecycle | não executado | |
| CHK-11.5 | Erro (load, input, rede se houver) fala a verdade | Caminho de falha real | TDD | não executado | |
| CHK-11.6 | Seed/determinismo só como `observado` se o parâmetro **afeta** o recorte | Repeat + compare; mentioned ≠ verified | lifecycle | não executado | |

## Produto — escala produto ou AA / Triple-I

`N/A` com a escala num jam, salvo se o brief prometeu câmera, mundo ou HUD.

### 3. Controle e câmera — CHK-3 · produto

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-3.1 | O verbo responde em cada entrada prometida | Teclado / toque / gamepad | GDD | não executado | |
| CHK-3.2 | Buffer, deadzone, cancelamento e perda de foco exercitados | Alt-tab, gesto abortado | feel | não executado | |
| CHK-3.3 | Câmera antecipa ameaça sem ocluir nem enjoar | Percurso real | visual | não executado | |
| CHK-3.4 | Look-ahead, aterrissagem e punch confirmam e devolvem o controle | Verbo central | feel | não executado | |
| CHK-3.5 | Escala e transição preservam landmark e ameaça | Zoom, corte, indoor/outdoor | visual | não executado | |
| CHK-3.6 | Rumble/haptic é elo do feel ou decisão explícita de não ter | Impacto vs. UI | feel | não executado | |

### 7. Mundo, luz, animação — CHK-7 · produto · `--focus visual`

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-7.1 | Silhueta, material e luz legíveis **em movimento** | Percurso, não still | visual | não executado | |
| CHK-7.2 | Landmark e ameaça sem a cor como único sinal | Forma, movimento, áudio | visual / acesso | não executado | |
| CHK-7.3 | Animação com antecipação e follow-through; não “floaty” | Referência em movimento | visual / feel | não executado | |
| CHK-7.4 | Família coerente com o herói **no engine**, mesma luz/câmera | Hero comparison | art-bible | não executado | |
| CHK-7.5 | Asset lindo no DCC e errado no jogo foi procurado | Shader, escala, pivot | content | não executado | |
| CHK-7.6 | Um “cabe neste jogo” e um “quebra a direção” | Art Bible | art-bible | não executado | |
| CHK-7.7 | Luz serve à leitura; mood não apaga ameaça nem landmark | Trecho escuro/claro | visual | não executado | |

### 8. UI, HUD e acesso — CHK-8 · produto

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-8.1 | HUD/menus do jogo, **ou** decisão explícita de não ter | Art Bible / GDD | art-bible | não executado | |
| CHK-8.2 | Contraste e forma além da cor no estado crítico | Daltonismo, UI em movimento | acesso | não executado | |
| CHK-8.3 | Foco, alvos de toque e movimento reduzido se o recorte os exige | Dispositivo prometido | acesso | não executado | |
| CHK-8.4 | UI não grita sobre o mundo nem tapa a consequência | Mix + layout | audio / visual | não executado | |
| CHK-8.5 | Menu sobrevive a pause, erro e volta ao jogo | Ida e volta | lifecycle | não executado | |
| CHK-8.6 | Fotossensibilidade: flashes do feel não viram strobe contínuo | CHK-4.5 sob movimento reduzido | acesso / feel | não executado | |

### 10. Receita e produção — CHK-10 · produto

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-10.1 | Receita do próximo item da família | Art Bible / GDD | art-bible | não executado | |
| CHK-10.2 | A slice usou o **pipeline real**, não atalho irrepetível | Ferramenta, import, naming | TDD | não executado | |
| CHK-10.3 | Custo observado do próximo trecho | Medido, não chute | slice | não executado | |
| CHK-10.4 | Repeatability: outro trecho sem heroísmo | Valor, técnica, produção, clareza | slice | não executado | |
| CHK-10.5 | Tokens com consumidor real | Path do uso | art-bible | não executado | |
| CHK-10.6 | Gate de import (nome, escala, pivot) antes de multiplicar | Um asset novo pela receita | content | não executado | |

### 14. QA e evidência — CHK-14 · produto · `--stage qa`

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-14.1 | Casos técnicos com comando real e recibo | `verify`; inspect antes | qa | não executado | |
| CHK-14.2 | Playtest de pessoa ≠ avaliação do agente | Relato literal vs. interpretação | qa | não executado | |
| CHK-14.3 | Antes/depois em condições equivalentes, em movimento | Versão, resolução, entrada, trecho | quality | não executado | |
| CHK-14.4 | `experience_status` = `not_assessed` até haver movimento | Recibo de verify | verify | não executado | |

### 15. Origem e direitos — CHK-15 · produto

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-15.1 | Código e assets do recorte com origem, crédito e uso | CREDITS | provenance | não executado | |
| CHK-15.2 | Nenhuma licença inventada pela pasta | Baixado / gerado | provenance | não executado | |

## Promessa — só se o brief prometeu

### 9. Narrativa e cinemática — CHK-9 · promessa

`N/A` sem história, voz ou cutscene. Marketing cinematográfico torna aplicável.

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-9.1 | Escolha com consequência jogável, não só texto | Caminho alternativo | GDD / content | não executado | |
| CHK-9.2 | Voz, lip-sync e tom consistentes | Cena representativa | art-bible | não executado | |
| CHK-9.3 | Corte de cena não rouba o verbo nem o feel | Transição jogo ↔ cena | feel | não executado | |
| CHK-9.4 | Save/histórico restaura o que o GDD promete | Load no meio da escolha | content | não executado | |

### 12. Rede — CHK-12 · promessa · `--focus network`

`N/A` se for local, sem estado compartilhado.

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-12.1 | Quem aceita a ação e quem decide o estado | Duas sessões reais | network | não executado | |
| CHK-12.2 | Recusa no autoritativo, não só na UI | Cliente desonesto ou replay | network | não executado | |
| CHK-12.3 | Entrada, saída, desconexão e reconexão | Duas sessões | network | não executado | |
| CHK-12.4 | Duplicata, atraso ou fora de ordem não quebra o recorte | Se o protocolo permite | network | não executado | |

### 13. Localização — CHK-13 · promessa

`N/A` sem outro idioma. Público amplo declarado torna aplicável.

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-13.1 | Textos do recorte com gancho de locale | UI + diálogo | content | não executado | |
| CHK-13.2 | Overflow e leitura no idioma alvo, ou lacuna explícita | Idioma mais longo | content | não executado | |

## Mercado — contexto, nunca piso

### 16. Tier de publisher — CHK-16 · mercado

Começa `N/A`. Não reprova conto nem AA / Triple-I.

| ID | Item | Observar | Origem | Estado | Evidência |
| --- | --- | --- | --- | --- | --- |
| CHK-16.1 | Publisher, orçamento e headcount **reais** | Fato, não meta | — | N/A | Não é condição do piso. |
| CHK-16.2 | Live ops / temporada / microtransação | Só se o produto as tiver | — | N/A | Não inventar. |
| CHK-16.3 | Certificação de console / XR / BVT | Só se houver submissão | — | N/A | Não é selo de acabamento. |
| CHK-16.4 | Marketing blockbuster, celebridade, AAAA | Só contexto | — | N/A | Buzzword; sem definição. |

## Resumo do recorte

- Perfil usado: [núcleo · núcleo+produto · +promessas].
- Núcleo observado / inconclusivo / não executado: [IDs].
- Produto e promessa: [IDs ou N/A].
- **O que ainda impede o adjetivo no perfil em vigor:** [IDs materiais].
- Próxima ação (uma): [verbo, alvo, prova].
- Aprovação do usuário: [somente se concedida].
