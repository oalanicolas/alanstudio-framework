# Audio

Fazer o som informar: causa e efeito no mesmo instante, camadas com prioridade,
ducking sob evento crítico, variação contra fadiga, silêncio como recurso, origem e
licença registradas. Use quando a ação é muda, quando o mix é uma pasta de arquivos
ou quando pausar deixa voz fantasma. Receita: [áudio](../recipes/audio.md).

## Escala

`jam`: som licenciado nas ações centrais, com origem registrada (`playable`).
`product`: mixagem real — barramentos, prioridade, ducking, variação (`slice`).
`aa`: faixa dinâmica controlada, controles separados de música/efeito/voz, o jogo
jogável mudo, e áudio adaptativo ao estado quando prometido.

## Avaliar

1. `context <projeto> --focus audio`. Leia a direção sonora do projeto, a política
   local em `studio_assets.sfx.policy` (estilos permitidos, fornecedores excluídos,
   piso técnico) e os papéis de áudio no [design system do jogo](../references/game-design-system.md).
   O núcleo não escolhe o estilo.
2. **Nomeie a camada** de cada som: ação, mundo, música, UI, stinger, silêncio. Siga
   a ação até o mix: quem toca, com que prioridade, quem cede (ducking), quem
   interrompe em pausa e reinício.
3. Efeito novo: `sfx search <termo> --root <lab>` **antes** de baixar; `sfx copy`
   traz o arquivo com proveniência. Sem acervo, o catálogo vem vazio; origem e
   licença continuam obrigatórias.
4. Pergunte só o que a direção não diz: caráter do som da ação central em palavras
   físicas, e se música é design (reage ao estado) ou fundo.

## Executar

REUSE no acervo → ADAPT no mixer existente → CREATE só com lacuna escrita. Ligue o
som ao mesmo quadro do impacto que o [feel](../recipes/feel.md) definiu; um som
atrasado é um segundo evento. Trate pause/reinício: nenhuma voz sobrevive a um
reinício. Silêncio antes do impacto é ferramenta; use-o. O starter `canvas-arcade`
tem mixer com barramentos, ducking, limite de vozes e legendas como referência
executável.

## Verificar

**Prove com e sem:** a cena com áudio e a mesma cena muda; o jogo continua jogável
sem som (senão a informação só existe no áudio: [`adapt`](adapt.md)). Cena densa com
evento crítico: o crítico atravessa o mix? Medição de pico/loudness quando houver
ferramenta. Pausa e reinício repetidos: nada fantasma. Degraus: dimensão `audio_mix`
na [barra](../references/production-bar.md). Registre origem e licença de cada
arquivo novo no canônico.

## Nunca

- Baixar som antes de buscar no acervo, ou embarcar arquivo sem origem e licença.
- Escolher estilo pelo núcleo do framework; a direção sonora é do projeto.
- Tocar tudo no mesmo volume e chamar de mix.
- Deixar informação crítica só no áudio, sem legenda ou sinal visual.
- Considerar a pasta de arquivos como dimensão fechada.

## Entregar

Os sons por camada, o que cede a quê, a proveniência, a prova com e sem, e o degrau
observado. Sequência: [`feel`](feel.md) se o impacto ainda não pesa; [`adapt`](adapt.md)
para legendas e sinais visuais equivalentes.
