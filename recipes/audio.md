# Áudio da consequência

Entrada: ação ou transição que precisa ser ouvida, silenciada ou misturada,
e a referência sonora aprovada (ou a lacuna explícita).

Com tela, a primeira superfície é a porta. A cama para nela; o avanço
que abre dispara `dash` e fecha com `land` em `beginRun()`. Attract não consome a seed.
A porta também lê a legenda que o mixer ainda guarda — sem isto o fim
existia no áudio e sumia na abertura. Texto no disco não é mix ouvido.

Áudio AAA não é quantidade de arquivos. É mix: o jogador ouve a causa, o
efeito e o espaço, e o silêncio também informa. Um loop 8-bit no lugar de
uma gravação licenciada não cumpre o piso deste estúdio. jsfxr, chiptune
e Kenney arcade não são o padrão.

`context --focus audio` seleciona esta receita. `roles <projeto>` lê os
papéis que o código declara (`const SOUNDS` ou `sounds.json`) e os arquivos
em `public/sfx`. `roles --fill` sugere um id do acervo ou a ficha do
stem do starter que casa; `--apply` copia o id do acervo ou o stem
do starter com créditos — e recoloca o WAV se o recibo já está e
origem e licença casam. `sfx copy` do acervo faz o mesmo e
declara `heard` falso. `sfx copy` continua o caminho explícito.
O starter `canvas-arcade`
já traz design original (CC0) em `public/sfx/<papel>.wav` e carrega no
mixer. O pedido que chega antes do WAV — ou enquanto o contexto
ainda está suspenso — fica na fila e toca quando o buffer entra ou
o gesto retoma, sem segunda legenda. Os stems sobem juntos: collect
não espera dash terminar. Wav no lugar não pede ogg. O gesto
(tecla, toque ou controle) retoma o contexto suspenso. Retomar, fila e
paralelo não são mix ouvido.
Coleta e guarda sobem de tom com a corrente; o erro não herda o tom.
A legenda desses dois papéis nomeia a mesma aposta. Sem o número
o tom falava e a faixa calava. O erro emite `lost`; a faixa nomeia
a corrente que caiu e cala a aposta quando era zero. Não herda
`chain`. Número na legenda não é mix ouvido.
Coleta, queda, raspo, impacto, avanço, o término, a guarda e o fim levam o x do campo; o panner
marca o lugar. Número no panner não é mix ouvido. O término (`land`) é
voz própria, mais curta que o dash; sem o papel o aterrissar é mudo.
`sfx --from` / `--as` desloca a voz no papel que o mixer já toca;
depois de um `note`, `start` e `next` apontam esse comando.
Arquivo ausente é lacuna do verbo, não silêncio deliberado.
O loader marca o primário que esgota as extensões; o painel
nomeia os vazios mesmo quando outro papel já registrou.
A região viva espelha a lacuna na porta e no fim — o convite
some a tabela. Catálogo completo não entra. Relê quando o
fetch termina — pintar só no boot some o que chegou.
Variante ausente não é lacuna. Decode nulo tenta a próxima
extensão; wav ilegível não esconde o ogg nem o pedido.
Nomear o 404 não é mix ouvido.
`heard` é sempre falso. Sem `shared/sfx`, `--fill` nomeia o stem
do starter que casa, `--apply` o copia ou recoloca o WAV se o recibo já está, `sfx search` nomeia o mesmo stem,
`sfx info` lê a chave e nomeia o stem que o recibo lista e o
disco perdeu, `sfx verify` nomeia os stems sem cruzar o
que não existe, `sfx summary` lista todos os stems já no
`public/sfx` e `sfx serve`
recusa. Com sons no acervo, `sfx serve` abre a página de escuta —
se `shared/sfx/ui` faltar, o harness gera a lista e nomeia o
som que o catálogo lista e o disco perdeu. `sfx verify`
nomeia o som que o catálogo lista e o disco perdeu —
não despeja errno. Tocar nessa
página não é mix ouvida no jogo. Isso não
autoriza improvisar licença. Arquivo no disco não é mix ouvido. Crescer o acervo é `sfx import ARQUIVO
--metadata JSON` (ffmpeg) ou `sfx seed` com `selection.json` local.
`sfx info ID` lê a ficha do acervo ou a chave do stem do starter —
o recibo que lista um stem e o disco perdeu não é id desconhecido;
`sfx export ID --to PASTA` copia bytes e
créditos do acervo ou do stem do starter que `sfx info`
já nomeia — o recibo que lista um stem e o disco perdeu
não é id desconhecido; exportar não inventa bytes.
`sfx copy` leva o mesmo stem para a pasta do
jogo. `--apply` também leva o stem do starter. Importar e exportar não é ouvir. O acervo compartilhado é ADAPT, não o
primeiro ciclo.

## 1. Nomear a camada

Antes de importar, diga qual papel o som cumpre. Camadas típicas; use só
as que o jogo tem:

- **Ação / Foley** — passos, impactos, recusas, UI que é verbo.
- **Mundo** — ambiente, ocupação do espaço, clima, máquinas.
- **Música** — tensão, exploração, vitória; não papel de parede.
- **Stinger / one-shot** — marco (descoberta, morte, checkpoint).
- **Silêncio** — ausência deliberada após impacto, em menu, na morte.

Um arquivo sem papel e sem consumidor não é áudio do jogo; é lixo no disco.
Token de áudio no Art Bible precisa apontar o consumidor real (bus, evento,
cena), como qualquer outro token.

## 2. Seguir a ação até o mix

Para o verbo ou a transição em pauta:

1. **Disparo** — o que no estado dispara o som? Input, colisão, UI, timer,
   rede? Disparo duplicado (dois listeners, restart sem stop) é o defeito
   mais comum.
2. **Corpo** — ataque, sustain, release. One-shot sem cauda pode parecer
   clique; loop sem fade parece falha.
3. **Ducking** — música e ambiente cedem à ação importante? Stinger come
   a voz do verbo? Prioridade explícita evita volume máximo em tudo.
4. **Espaço** — 2D/3D, oclusão, distância. Só quando o jogo já tem (ou
   precisa de) espacialização; não adicione HRTF para cumprir checklist.
5. **Interrupção** — pause, aba, morte, restart, troca de cena, unfocus.
   Áudio que sobrevive é regressão de [ciclo de vida](lifecycle.md).
6. **Descarte** — montar → desmontar → montar. Voz fantasma ou bus
   duplicado indicam recurso sobrevivente.

Feel e áudio se confirmam: [feel](feel.md) descreve o impacto; esta receita
garante que ele se ouve e se cala na hora certa. O one-shot de impacto
dispara no **mesmo frame** do hit-pause e do flash. Som atrasado não “pesa”
o golpe — denuncia a costura. Som é o juice de maior retorno por esforço;
verbo mudo continua sendo o defeito mais barato de corrigir e o mais caro
de deixar.

## 3. REUSE → ADAPT → CREATE

Ordem:

1. Consumidor e evento já existentes no jogo.
2. `shared/sfx` no laboratório, se a pasta existir na raiz de `--root`.
3. Acervo do próprio projeto (com crédito e licença já registrados).
4. Download ou síntese **somente** com lacuna, licença compatível e
   registro de origem. Geração externa distingue preview de asset
   aprovado; não torna o fornecedor obrigatório.

Adapte pitch, volume e envelope no canônico antes de duplicar o arquivo.
Trocar um wav sem atualizar pivot rítmico, ducking ou interrupção é
regressão. Conteúdo baixado não ganha licença nova pelo reuso.

Piso: gravação licenciada ou design contemporâneo coerente com a Art
Bible. Se o jogo **escolhe** chip/lo-fi, isso é direção explícita, não o
padrão do estúdio — registre no design system.

## 4. Música como design

Música muda comportamento. Defina o que ela informa (perigo, progresso,
calma) e o que a corta (stinger, diálogo, morte). Teste transição: entrar
e sair de combate/menu/cutscene sem clique, sem camada dupla e sem
silêncio acidental de vários segundos, salvo se o silêncio for a direção.

Não use a faixa como prova de atmosfera se o verbo continua mudo. Em
recorte sem música, declare a escolha; não invente trilha para o scanner
ficar verde.

## 5. Provar com e sem

Compare nas mesmas condições, **com som e com mute**. O jogo ainda precisa
ser legível no silêncio quando o recorte exigir acesso ou ambiente ruidoso.
Verifique:

- Ação central audível contra o ambiente.
- Recusa audível e distinta do sucesso.
- Pause/reset sem cauda.
- Save/load ou troca de nível sem overlap.
- Volume relativo: UI não grita sobre o mundo; impacto não estoura.

Teste técnico de decode não aprova mix. Avaliação do agente não é
aprovação do usuário. Sem referência sonora, a lacuna permanece explícita.

Origem: piso de áudio do [README](../README.md),
[qualidade](../references/quality.md),
[ambição](../references/ambition.md) e catálogo `shared/sfx` do laboratório.
O acervo `shared/sfx` do laboratório não vive neste repositório. O
starter `canvas-arcade` inclui design original em `public/sfx`.

## Implementação de referência e degraus

`src/game/audio.js` do starter `canvas-arcade` traz barramentos, prioridade, ducking
só na cama (`music`), limite de vozes, rodízio de variantes e legenda.
O aviso crítico não some o próprio verbo. Os papéis do verbo e a
cama (`bed`, loop no barramento de música; o relógio da sessão dilata
a cama só na partida — o fecho sobe em cima dele), o fecho (`close`, tap e
legenda "últimos segundos"), a prática (`live` com `threat`,
"a ameaça começa" — a porta reusa a voz sem o tap e continua
"a chuva começa"),
a guarda (`stir`, "a folga acaba" — a chuva não some, só
afrouxa),
o orbe perdido (`missed`,
"orbe perdido") têm design original e variante
(`-b`) em `public/sfx`. No `over` a cama solta com fade; pause, title
e aba escondida continuam cortando a cama seco. No campo a pausa
também corta as vozes do verbo que ainda soavam. No fim e na
porta o `hush` não corre: a cortina já venceu e o stinger
precisa atravessar. Arquivo no disco não é mix ouvido. `npm run sfx -- --from dash --as brighter`
desloca a voz no papel que o mixer já toca; `--as` precisa de `--from`.
`npm run peak` relata o pico do
arquivo; `npm run mix` soma as vozes de uma partida simulada com o mesmo
palco, folga, ducking e taxa da corrente do mixer. Nenhum dos dois é mix ouvido. `heard` continua falso. Toda
informação sonora precisa de equivalente visual — requisito de
[acessibilidade](accessibility.md), não recurso extra. Degraus da dimensão `audio_mix`:
[barra de acabamento](../references/production-bar.md#audio_mix--mixagem-não-arquivos).
