# Alcance — o que este recorte atende

Declaração vigente. Opção no código não é sessão observada.
`verified` no harness continua falso.

## O que o recorte atende

- Contraste alto (`highContrast`) com paleta própria
- Tinta estável (`colorblind`): look que já separa orbe quente e estilhaço frio (ou o contrário) permanece; o par azul/laranja do padrão é o fallback quando as duas tintas ainda compartilham o eixo. O campo do look permanece. Alto contraste vence. Chave no disco não é sessão observada
- Redução de movimento (`reducedMotion`): tremor e piscada viram forma estática; na porta a mostra trava no canvas, no toque e no aviso vivo — os três leem a mesma chuva parada. Isso não é sessão observada
- Legendas para toda informação sonora (`captions`); a faixa vence a cortina da pausa e do fim no stub; coleta e guarda nomeiam a corrente que o tom já sobe; o erro nomeia a corrente que `lost` derrubou e cala a aposta quando era zero — isso não é sessão observada
- Remapeamento de ações (`bindings`); a página expõe as seis ações do teclado e a tabela `#commands` nomeia as teclas vigentes — toque e controle ficam no sufixo e não entram no remap; a escuta come a tecla que escolhe o verbo; o botão focado não dispara o verbo; persistir no stub não é sessão observada
- Escala da interface (`uiScale`); o overlay do fim e da pausa também cresce; a casca da página (tabela, painel, convite) também — isso não é sessão observada
- Knobs da casca (select, faixa, caixa) vestem o look e têm foco visível; as faixas nomeiam o percentual vigente (velocidade, escala, mix) — token no disco não é sessão observada
- Preset de uma mão no cluster direito (`oneHand`, IJKL + P/O); desligar devolve o remap que a pessoa já tinha; save antigo sem o conjunto guardado não inventa remap; o aviso, o overlay e o `cycle.hand` nomeiam essas teclas; no stub o cluster coleta, guarda, pausa e reinicia — isso não é sessão observada
- Toque: arrastar move, faixa de cima avança, faixa de baixo guarda; o toque que sai do campo ainda solta; o `cycle.touch` nomeia o mapa; o stub percorre as três intenções; o aviso do primeiro ciclo nomeia o arraste junto do teclado e do controle e, depois do primeiro toque, o mapa da superfície vira passo — isso não é sessão no aparelho
- Controle: analógico/dpad move, A avança, X guarda, Start pausa, Select reinicia; o `cycle.pad` nomeia o mapa; o stub percorre o verbo e os comandos; o aviso do primeiro ciclo nomeia o analógico e o X junto do teclado e do toque e, depois do primeiro eixo, o mapa da superfície vira passo; overlay e HUD confirmam o mapa quando o controle falou por último — isso não é sessão no aparelho
- Assistência que não esconde orbe nem pontuação (`assist`): na partida e na mostra da porta, alcance maior e chuva mais lenta. A graça extra fica no campo. Isso não é sessão observada
- Velocidade da partida (`gameSpeed`): o relógio da partida anda mais devagar; a mostra da porta e o fim ficam no relógio cheio. A assistência continua sendo alcance e queda, não este knob. `advance()` headless não dilata. Isso não é sessão observada
- Região viva (`#live`): fase, pausa, perigo, última legenda, o aviso do primeiro ciclo que o canvas já pinta e, no fim e na porta, o placar e o recorde que o canvas já mostra; no fim, a corrente que caiu se o overlay a nomeia; na porta o toque da mostra (`a mostra toca` / `a mostra raspa`) sem fingir coleta. No fim o aviso do ciclo some. Texto no DOM não é sessão observada

## O que o recorte não atende

- Contraste medido no dispositivo e em movimento — `npm run contrast` amostra pixels do stub após `draw()` e relata o par sem limiar; o aparelho alvo não foi observado
- Jogo completável com uma só mão, observado
- Sessão com cada modo ativo, observada
- Leitura em escala de cinza no dispositivo alvo, observada — `npm run contrast` relata pixels que só o orbe ou só o estilhaço pintam com a mesma tinta no stub; o aparelho não foi observado

Esta página não sobe o degrau. Ela impede de fingir que o recorte é completo.
