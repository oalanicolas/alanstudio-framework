# Adoção — Alan Studios Framework

Histórico das versões 0.1–0.9. Recibos brutos de execução e o acervo sonoro
ficam no laboratório; aqui permanece o que a versão afirma e o que ela não afirma.

## 0.9 — Caminho fácil e produção até o acabamento

Revisão do que o framework se propõe (criar jogos com IA com evidência, até a
qualidade aprovada) contra o que entregava até 0.8. Lacunas encontradas:

- **Os comandos documentados não rodavam.** Todo exemplo do README e da skill passava
  `--root` depois do subcomando; o argparse só aceitava antes. Corrigido: `--root` em
  qualquer posição.
- **`context` ignorava `--root` para o acervo sonoro** e consultava o diretório atual.
  Corrigido.
- **Não havia autodiagnóstico.** `doctor` confere Python, integridade dos arquivos do
  framework, raiz, projetos, estudos, sfx e git, e indica o próximo comando.
- **A pré-produção recomendava um `game-design.md` único para jogos pequenos, mas não
  havia template.** O template `game-design` reúne as nove áreas e, preenchido, é
  reconhecido pelo scan como cobertura completa (teste garante).
- **A descoberta só via package.json, Unity, Godot e HTML.** Agora reconhece Unreal,
  Defold, GameMaker, Cargo, Python e Love2D, e ignora pastas de build das engines.
- **O processo terminava no MVP.** Não havia marcos de produção, orçamentos, pipeline
  de conteúdo, estabilidade, acessibilidade ou localização. A receita `production`
  define marcos como gates de evidência (first playable → vertical slice → alpha →
  beta → gold → live), lentes de disciplina e orçamentos medidos; os templates
  `production-plan` e `milestone` mantêm o estado; `quality.md` ganhou a barra de
  acabamento.
- **Feel não tinha receita.** `feel` trata latência, animação, câmera, tempo, efeitos,
  som e haptics como camadas medidas e observadas, registradas no design system do jogo.
- **A skill era um bloco denso.** Reorganizada em caminho rápido e sete passos, sem
  remover regras.
- **Só havia recibo para comandos técnicos.** A receita de produção exige orçamento
  medido e passagem declarada por pessoa, mas nada ligava essas provas à versão do
  jogo. `record` grava observação (`role=human|agent`), medição de orçamento e
  decisão de marco em pasta inédita, com HEAD do git e anexos por SHA-256. Ele guarda
  o que foi declarado; não valida nem aprova.
- **`verify --script` só conhecia npm.** Projetos Cargo ganham `check`, `build` e
  `test`; Unity, Godot e Unreal seguem por `--command`, sem inventar CLI.
- **O núcleo era agnóstico, mas a calibração real era web/2D.** Em vez de
  especializar o núcleo, a 0.9 adiciona [pacotes](packs/README.md): nove de plataforma
  (web, Unity, Godot, Unreal, Defold, GameMaker, Cargo, Python, Lua), selecionados
  automaticamente pelo marcador que `identify` encontra, e nove de gênero (narrativa,
  plataforma, shooter, corrida, turno, puzzle, simulação, RPG, roguelike), por
  `--genre`. Entram em `read_next` depois da receita; um campo `Gênero:` em documento
  só sugere. Pacotes são convenções a confirmar, não capacidades certificadas.
- **Faltava exemplo de produção.** [Da trilha ao capítulo acabado](examples/era-uma-vez-production.md)
  mostra plano, orçamentos como hipóteses, marcos e recibos num jogo pequeno.

O que 0.9 não afirma: “AAA” é padrão de acabamento observável, não orçamento nem
equipe; nenhum comando mede performance, executa soak, promove marco, certifica
requisito de plataforma ou aprova arte. Os termos de marco seguem uso corrente da
indústria; cada jogo registra a definição adotada.

## 0.8 — Arquitetura proporcional

Receita [architecture](recipes/architecture.md). `--focus architecture` e
`--stage tdd` selecionam essa receita. A skill aplica análise proporcional
quando a mudança afeta contratos, responsabilidades ou sistemas. O CLI não
infere dependências nem aprova decisões.

## 0.7 — Continuidade e retomada

`--event resume` localiza fontes de continuidade. A entrega deve situar o
avanço e uma próxima ação, motivo e prova. O harness deixa `next_step: null`;
o agente resolve o passo.

## 0.6 — Aprovação de direção

`--event direction-approved` sincroniza a base mínima no mesmo turno, mesmo
com todos os candidatos encontrados. Salvar a imagem e listar entregas não
basta.

## 0.5 — Documentar o mínimo sem segundo pedido

Se a checagem deixar lacunas, o agente avisa e documenta. Restrição explícita
na conversa continua valendo. O scanner permanece somente leitura.

## 0.4 — Scan e foundation

`context` sempre inclui `scan`. Nove áreas, candidatos, lacunas e limites.
`candidate_found` não certifica suficiência. Templates complementares:
Art Bible, Devlog, Auditoria.

## 0.3 — Contexto por foco com estudos e menções locais

`context` lista catálogos do foco quando o irmão de estudos existe, e registra
menções de pause, reset, seed e demais capacidades em um conjunto fechado de
arquivos locais. Nenhuma menção vira `verified`.

## 0.2 — Pré-produção e ciclo criativo

Nove templates sob demanda. `context --stage` e `template` selecionam um
artefato. Nenhuma etapa é aprovada pelo comando.

## 0.1 — Entrega inicial

Descobrir projetos, recortar contexto, validar a forma do contrato de reuso e
executar comandos escolhidos com recibo.

## Limites que continuam valendo

Build verde não comprova diversão, arte, reinício, rede, direitos de assets nem
aprovação humana. Troca de modelo com qualidade equivalente continua hipótese a
testar. Os oito frameworks externos foram estudados em recortes; seus testes
não foram executados neste repositório. Este extrato não inclui evidência JSON
nem a biblioteca `shared/sfx`.
