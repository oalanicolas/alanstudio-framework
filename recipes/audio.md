# Áudio da consequência

Entrada: ação ou transição que precisa ser ouvida, silenciada ou misturada,
e a referência sonora aprovada (ou a lacuna explícita).

Áudio AAA não é quantidade de arquivos. É mix: o jogador ouve a causa, o
efeito e o espaço, e o silêncio também informa. Um loop 8-bit no lugar de
uma gravação licenciada não cumpre o piso deste estúdio. jsfxr, chiptune
e Kenney arcade não são o padrão.

`context --focus audio` seleciona esta receita. `roles <projeto>` lê os
papéis que o código declara (`const SOUNDS` ou `sounds.json`) e os arquivos
em `public/sfx`. `roles --fill` sugere um candidato do acervo; `--apply`
copia para `public/sfx/<papel>` com recibo. O starter `canvas-arcade`
já traz design original (CC0) em `public/sfx/<papel>.wav` e carrega no
mixer. Arquivo ausente é lacuna do verbo, não silêncio deliberado;
`heard` é sempre falso. Sem `shared/sfx`, a sugestão de `--fill` vem
vazia — isso não autoriza improvisar licença.

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

`src/game/audio.js` do starter `canvas-arcade` traz barramentos, prioridade, ducking,
limite de vozes, rodízio de variantes e legenda. Os seis papéis têm design
original e variante (`-b`) em `public/sfx`. `npm run peak` relata o pico do
arquivo; `npm run mix` soma as vozes de uma partida simulada com o mesmo
palco, folga e ducking do mixer. Nenhum dos dois é mix ouvido. `heard` continua falso. Toda
informação sonora precisa de equivalente visual — requisito de
[acessibilidade](accessibility.md), não recurso extra. Degraus da dimensão `audio_mix`:
[barra de acabamento](../references/production-bar.md#audio_mix--mixagem-não-arquivos).
