# Gênero — Ritmo (rhythm action, música, dança)

Aplicabilidade: `--genre rhythm`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: acertar o tempo. Decisões: leitura antecipada, priorizar precisão vs
  combo, escolha de dificuldade/modificadores, ritmo do corpo (dança, VR).
- Modelo: notas em faixa (lane), ação sincronizada ao beat (combate no ritmo),
  call-and-response, dança por sensor. Registre e defina o piso de latência.

## Feel que importa

- Sincronia audiovisual absoluta: relógio do jogo derivado do áudio (posição de
  reprodução), não do frame; calibração de latência de áudio e de input separadas,
  com teste guiado.
- Janelas de acerto por camada (perfect/great/good) com feedback visual+sonoro
  imediato; hit sound opcional; movimento das notas com velocidade constante.
- Falha graciosa: errar não deve interromper a música.

## Riscos habituais

- Drift entre áudio e notas ao longo da música (relógio errado, resample, pausa);
  latência do Bluetooth/TV sem calibração; tela com input lag.
- Charts (mapas de notas) fora do beat, densidade sem curva; detecção de beat
  automática sem revisão humana; licença de música.

## Orçamentos e medições típicas

- Deriva áudio↔jogo ao fim da música (alvo < 1 ms); latência input → julgamento
  (medida com câmera 240 fps ou loopback); quadro p99 constante (jitter destrói
  leitura); distribuição de acertos por janela em playtest.

## QA e playtest específicos

- Teste automatizado de chart: notas no grid do BPM (com tolerância), densidade por
  seção; reprodução com inputs perfeitos gravados; pausa/retomada sem deriva; troca de
  dispositivo de áudio.
- Playtest: a pessoa acerta com os olhos fechados no refrão? Calibração é entendida?
  Sente que errou por culpa própria?

## Receitas e fontes

[feel](../../recipes/feel.md) (latência, tempo), [mecânicas](../../recipes/mechanics.md)
(relógio), [conteúdo](../../recipes/content.md) (áudio, charts), [produção](../../recipes/production.md).
