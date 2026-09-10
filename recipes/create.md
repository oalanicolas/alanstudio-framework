# Criar uma experiência

Entrada: fantasia, público/entrada, verbo central, direção artística e cenário curto.
Se algo foi omitido, assuma a opção coerente com o acervo e registre; só interrompa
por decisão indispensável. O destino de um jogo novo deve ser novo; continuação usa
o projeto atual.

O caminho curto está em [ambição](../references/ambition.md): um ciclo jogável
na primeira sessão, depois feel e áudio do verbo, depois receita de conteúdo.
`start` e `guide` mapeiam start → jogar → `note`. O [processo comum](../references/process.md)
também nomeia a porta nesse mapa. Os dois devolvem
`open` (o comando de agora) e `prompt` (a frase para colar; também
sai em stderr). Depois do
`start`, `open` é o play e `steps` é o mesmo mapa de três passos, com
o passo 1 feito. Sem destino, `--idea`
nomeia a pasta no comando do start e não grava a frase. Sem destino, se o
diretório atual é um jogo fora do framework, o `guide` usa esse caminho.
`then` nomeia par, look, chuva e voz se o projeto — ou o starter, antes do
destino existir — declara essas ferramentas. Se declara `session`,
`then` a aponta e o prompt a nomeia (`Sessão:`). Não executa e não observa. Se o disco tem last-run com seed, `then` aponta a
seed e o convite; nomear o endereço não observa. A partida no serve grava o candidato; a simulação
também. Depois do fim, a página grava o recibo se você escrever
e aponta o convite desta partida se a seed ficou no recibo. Copiar
o endereço não grava.
Depois do recibo, o mesmo `start` e o `next` apontam
o ofício. O autor do `note` é sugestão do git ou do ambiente, não
quem jogou. Nomear o ofício não pinta. `playtest --invite` aponta `href`
(`/?invite=1` ou, com seed no disco, `/?invite=1&seed=<n>`, com
chuva nomeada `&spawn=<mesa>`, com look nomeado `&look=<paleta>`,
e com relógio nomeado e ≠ 1 `&speed=<relógio>`), onde a
tabela some; depois do fim a página mostra seed, pontos, eixos e a
curva que o last-run já traçou e oferece os quatro nomes para copiar
ou gravar. Depois do fim a
página rola até o painel. Rolar não é alguém de fora. Número na faixa não
preenche os quatro. Copiar não grava. O Copiar nomeia o
destino. Gravar já virava Achado no disco; o botão calava.
Nomear não é alguém de fora. Sem a área de transferência,
o Copiar baixa o markdown. Gravar anexa o candidato se last-run
existir. Na árvore exportada o Gravar some; copie os quatro
nomes. Gravado não é alguém de fora. Não gere todos os templates antes de experimentar. Nove arquivos vazios não
aumentam a qualidade; uma fatia sem feel continua sendo protótipo.

Siga [o ciclo de pré-produção](../references/preproduction.md) para escolher o
próximo artefato e revisar sua prontidão. Brief e GDD definem a experiência; MDA
explicita a hipótese e, com tela, começa na porta; PoC a investiga; PRD/TDD delimitam requisitos e implementação;
MVP e PRD também nomeiam a abertura. Nomear a porta não observa.
vertical slice e MVP têm objetivos distintos; QA e playtest alimentam o design.
Carregue o template da etapa com `context <projeto> --stage <etapa>` e adapte o
documento canônico. Jogo pequeno: `template game-design --project <novo> --output <arquivo-novo.md>`
grava um documento único com as nove áreas; sem `--output`, só imprime o rascunho.
Preencha-o em vez de gerar nove arquivos. Não gere todos os arquivos
antes de começar a experimentar. Quando a fatia demonstrar a experiência, a
[receita de produção](production.md) leva do recorte ao acabamento por marcos.
Uma direção aprovada exige sincronizar a base oficial no mesmo turno, conforme
[o roteiro](../references/project-audit.md#aprovação-de-direção-materializar-e-continuar).
Cubra as nove áreas com conteúdo ou lacunas explícitas, em documentos proporcionais
ao projeto, e prossiga com o recorte solicitado. O usuário não precisa pedir essa base.

Declare a **escala** no brief: jam/conto, produto ou AA / Triple-I (piso de
acabamento). A escala governa quantidade de artefatos e de conteúdo. O piso
do verbo — decisão, feel sincronizado, áudio da consequência, pacing — não é
opcional em nenhuma delas. Não use “AAA” como adjetivo do build.

## Primeira sessão

1. Consulte o [playground](https://games.alanicolas.com/) e o acervo local.
   Identifique uma família compatível. Procure código, contratos e conteúdo
   reutilizável.    Sem destino no disco, o candidato local é um starter.
   `python3 scripts/game.py --idea "<fantasia>"` mapeia o start com a
   pasta nomeada pela frase (ao lado do framework se o mapa corre de
   dentro desta árvore) e não cria a pasta. `start --idea "<fantasia>"`
   (ou `start <destino> --starter <starter> --idea "<fantasia>"`) monta
   o projeto — sem caminho, a frase nomeia e cria a pasta —, põe a
   frase na abertura e no aviso do primeiro ciclo, escreve `AGENTS.md`
   com o comando que abre, o `note` e o `playtest` (não lista rascunhos que não plantou) e devolve o comando que abre o jogo.
   O `playtest` só lê. Sem os quatro não é achado. Nomear o leitor não observa.
   Sem memória no disco, `template agents` e o `next` geram o mesmo
   texto a partir do que existe — não o molde que listava GDD.
   Perdeu o JSON? `play` (ou `open`) aponta o serve de novo, sem executar.
   Se o manifesto declara `session`, o prompt também nomeia a partida
   simulada. Não executa e não observa.
   Sem caminho, o único jogo do laboratório basta; dois pedem o caminho.
   Com tela, o avanço abre a porta e, depois do fim, um avanço novo volta; sem tela o headless já joga.
   `?seed=<n>` abre essa partida e ignora o hold.
   `?spawn=` abre essa chuva e ignora o hold da outra mesa.
   A frase não muda o verbo.
   `init` faz a mesma cópia sem apontar o ciclo.
   O projeto nasce com laço de passo fixo, save versionado, entrada
   abstraída e testes que já rodam.
   Partir dele é REUSE; recomeçar essa infraestrutura é CREATE e pede lacuna
   explícita.    Som: se o laboratório tiver `shared/sfx` com sons, use `sfx search`
   antes de baixar. Sem acervo, o starter já fala em `public/sfx`;
   `sfx search` nomeia o stem que casa com o termo.
   Crescer o acervo é `sfx import` / `sfx seed` (ffmpeg); importar não
   é ouvir. Explique REUSE, ADAPT ou CREATE antes de produzir novos
   sistemas.
2. Construa um ciclo jogável com uma decisão característica. Defina entrada,
   objetivo percebido, consequência, término e repetição. Título e cores novos
   não demonstram uma experiência nova.
3. Faça essa fatia atravessar controles, estado, apresentação e conteúdo.
   Valide a integração antes de multiplicar fases, itens ou personagens.
4. Aplique o feel e o áudio **desse** verbo. Use `--focus feel` e
   `--focus audio`. Arte provisória é aceitável se a direção estiver
   declarada; verbo mudo ou sem peso não é.
5. Compare com a intenção e com a referência, em movimento. Preserve o que
   foi pedido. Registre herdado versus produzido e **uma** próxima ação.
   Não gere o template `aaa` nesta sessão. O `finish.action` permanece
   `defer_until_playable_cycle` até existir o ciclo.

## Da fatia à produção

A escada: fantasia → ciclo → feel → áudio → receita de conteúdo → vertical
slice no piso → produção sem diluir. PoC reduz incerteza; scaffold mostra
estrutura; slice mostra experiência no acabamento pretendido.

Em escala AA / Triple-I, feel, mix, luz, animação, pacing e a receita do
próximo item são requisitos do recorte, não “polimento depois”. Reduza
quantidade de conteúdo; não reduza o piso aprovado. Se a slice não demonstra
repeatability — outro trecho nasce no mesmo padrão, sem heroísmo — ainda
não está pronta para ampliar. Isso é piso de acabamento, não tier de
publisher.

Pontos de partida a **examinar**, não bases aprovadas automaticamente:

- FPS em papel: Distrito Rabisco / Jogo Rabisco. Já tem briefing, bootstrap e marcos.
  O bootstrap recusa divergência do manifesto de origem.
- Contos Canvas: Era Uma Vez, no [playground](https://games.alanicolas.com/).
- Corrida: Brasa-Pista, no playground.
- Unity: protótipo local com verificações próprias; presença em `prototypes/` não
  declara publicação.

Não copie paleta, feel ou mix de uma família sem ADAPT e proveniência. O
destino continua com instância própria no design system.

BMad inspira leitura por etapa e retomada (`RE-GDS-002`, `RE-GDS-022`); seus passos
textuais não são uma garantia de execução. [Fonte](../references/sources.md).

Concluir o pedido exige conteúdo distintivo, cenário real e QA. Scaffold ou
cópia que inicia continua sendo ponto de partida — um projeto recém-criado por
`init` é exatamente isso, com documentos em rascunho e a decisão característica
ainda por fazer. Esta receita não copia nem publica projetos por si. Não chame o
recorte de AAA se as barras da escala — feel sincronizado, mix, pacing,
repeatability — não foram demonstradas na slice.

Ao decidir onde investir depois do primeiro ciclo, use a
[barra de acabamento](../references/production-bar.md) e trabalhe pela dimensão mais
baixa: o degrau percebido é o mínimo entre elas, e um jogo curto e coerente é lido
como produto enquanto um grande e irregular é lido como protótipo. Quando a fatia
demonstrar a experiência, a [receita de produção](production.md) leva do recorte ao
acabamento por marcos.
