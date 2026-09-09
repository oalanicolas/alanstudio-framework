# Game design — {{PROJECT}}

Projeto: {{PROJECT_PATH}}
Status: rascunho. Autor/revisão: [preencher]. Direção do usuário e fonte anterior: [localizar; adaptar se já existir].
Documento único para um jogo pequeno: reúne brief, GDD, MDA, requisitos, decisões
técnicas, design system, devlog, QA, execução e origem. Preenchido, cobre as nove
áreas mínimas; separe um documento por área só quando o ritmo de atualização divergir.
Substitua cada `[preencher]`; uma área intencionalmente não aplicável recebe o motivo.

## Visão e escopo

- Fantasia em uma frase: [quem o jogador é e o que realiza].
- Experiência pretendida: [sensação e o momento que a expressa].
- Jogador, plataforma e entradas: [perfil, dispositivo, teclado/toque/gamepad, restrições].
- Pilares: [compromisso concreto → escolha favorecida → o que o violaria].
- Recorte atual: [implementado / pretendido / adiado, com motivo].
- Hipótese mais arriscada e experimento inicial: [o que pode invalidar a experiência; como descobrir].

## Game design e mecânicas

- Ciclo principal: [informação → alternativas → ação → consequência → próxima decisão].
- GDD-M01: [estado inicial e ação → alternativas e custo → novo estado e feedback → recusas].
- Controles, câmera e legibilidade: [verbo central por dispositivo, resposta, enquadramento, cancelamento].
- Ritmo e progressão: [primeira aprendizagem, prática, combinação de riscos, recuperação].
- Término e reinício: [vitória/derrota/conclusão; o que persiste e o que zera].
- Conteúdo, espaço e narrativa: [rotas, landmarks, entidades, história; conforme o gênero].

## Hipóteses de experiência (MDA)

- MDA-001: [mecânica → dinâmica esperada → experiência pretendida].
- Alternativa plausível e efeito indesejado: [outra explicação; tensão virar frustração, opção dominante].
- Observação que apoia / contradiz: [situação concreta antes do playtest; resultado: não executado].

## Requisitos e aceite

- FR-001 (origem GDD-M01): [sob condição X, o jogador consegue Y, produzindo Z].
- AC-001: dado [estado], quando [ação], então [resultado observável].
- NFR-001: [acesso, confiabilidade, controle ou orçamento de performance com condição e método de medição].
- Essenciais e adiados: [IDs e motivo; exigências explícitas do usuário preservadas].

## Arquitetura e decisões técnicas (TDD)

- Engine/versão e ponto de entrada: [caminhos reais].
- Fluxo: iniciar → carregar → input → atualizar estado → apresentar → pausar → terminar/reiniciar → descartar: [módulos por etapa; ausência é lacuna, não API inventada].
- Estado, tempo e persistência: [dono do relógio, RNG/seed se existir, saves e versões].
- TDD-D01: [problema → alternativas REUSE/ADAPT/CREATE → escolha → contrato → contraprova → reversibilidade].
- Mapa de reuso: [necessidade → candidato → consumidor → adequação].

## Design system do jogo (Art Bible)

- Autoridade e piso: [referência aprovada, origem, quem aprovou, o que não pode degradar].
- Tokens com consumidor: [papel → valor → caminho real ou “ainda não existe”].
- Componentes do mundo e receita de item novo: [famílias recorrentes; passos para o próximo].
- Feel da ação central: [hitstop, câmera, squash, partículas, som, silêncio; ligar ao verbo].
- UI/HUD/acesso: [ou a decisão explícita de não ter interface tradicional].
- Fazer / não fazer: [um exemplo que cabe e um que quebra a direção].

## Decisões e histórico (Devlog)

- DEC-001: [data, direção recebida ou problema, candidatos lidos, decisão e motivo, alternativas rejeitadas, verificação].
- Hipóteses descartadas e custos observados: [para não repetir tentativas].

## QA e playtest

- QA-001 (AC-001): [condição, ações, esperado, comando real; resultado: não executado].
- PLAY-001: [hipótese MDA, perfil do jogador, sinais a observar; observação: não coletada].
- Comparação em movimento: [referência e condições equivalentes].
- Aprovação: [autor e origem; avaliação do agente não é aprovação do usuário].

## Como executar e verificar

- Dependências e instalação: [engine, versão, gerenciador, comandos].
- Executar: [comando ou ponto de entrada].
- Validar: [testes/lint/build e ordem; comando declarado não comprova execução].

## Origem de código e assets (proveniência)

- Código: [próprio / herdado de qual projeto / gerado; condições de uso].
- Arte, áudio, fontes, dados: [origem, crédito, licença conhecida; não atribuir licença desconhecida].

## Continuidade

- Onde estamos: [etapa real e última entrega com evidência].
- Próximo passo: [verbo, alvo e saída; ID quando houver].
- Por que agora / pronto quando: [dependência ou risco; evidência que encerra].
- Retomar por: [seção deste documento, arquivo/símbolo e consumidores a ler].
