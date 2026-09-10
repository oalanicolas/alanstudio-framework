# Alcance — o que este recorte atende

Declaração vigente. Opção no código não é sessão observada.
`verified` no harness continua falso.

## O que o recorte atende

- Contraste alto (`highContrast`) com paleta própria; se o sistema pede more no meio da sessão, o recorte liga — desligar o sistema não apaga a caixa
- Tinta estável (`colorblind`): look que já separa orbe quente e estilhaço frio (ou o contrário) permanece; o par azul/laranja do padrão é o fallback quando as duas tintas ainda compartilham o eixo. O campo do look permanece. Alto contraste vence. Chave no disco não é sessão observada
- Redução de movimento (`reducedMotion`): tremor e piscada viram forma estática; na porta a mostra trava no canvas, no toque e no aviso vivo — os três leem a mesma chuva parada; se o sistema pede reduce no meio da sessão, o recorte liga — desligar o sistema não apaga a caixa. Isso não é sessão observada
- Legendas para toda informação sonora (`captions`); a faixa vence a cortina da pausa e do fim no stub; coleta e guarda nomeiam a corrente que o tom já sobe; o erro nomeia a corrente que `lost` derrubou e cala a aposta quando era zero; o pulso do fecho refresca a linha que já está lá — dez "últimos segundos" não comem o verbo — isso não é sessão observada
- Remapeamento de ações (`bindings`); a página expõe as seis ações do teclado e a tabela `#commands` nomeia as teclas vigentes — toque e controle ficam no sufixo e não entram no remap; a escuta come a tecla que escolhe o verbo; o botão focado não dispara o verbo; persistir no stub não é sessão observada
- Escala da interface (`uiScale`); o overlay do fim e da pausa também cresce; a casca da página (tabela, painel, convite) também — isso não é sessão observada
- Knobs da casca (select, faixa, caixa) vestem o look e têm foco visível; as faixas nomeiam o percentual vigente (velocidade, escala, mix) — token no disco não é sessão observada
- Preset de uma mão no cluster direito (`oneHand`, IJKL + P/O); desligar devolve o remap que a pessoa já tinha; save antigo sem o conjunto guardado não inventa remap; o aviso, o overlay e o `cycle.hand` nomeiam essas teclas; no stub o cluster coleta, guarda, pausa e reinicia — isso não é sessão observada
- Toque: arrastar move, faixa de cima avança, faixa de baixo guarda; o toque que sai do campo ainda solta; esconder a aba solta o hold do teclado e do toque; perder o foco da janela solta o ofício pendente; o `cycle.touch` nomeia o mapa; o stub percorre as três intenções; o aviso do primeiro ciclo nomeia o arraste junto do teclado e do controle e, depois do primeiro toque, o mapa da superfície vira passo — isso não é sessão no aparelho
- Controle: analógico/dpad move, A avança, X guarda, Start pausa, Select reinicia; o `cycle.pad` nomeia o mapa; o stub percorre o verbo e os comandos; o aviso do primeiro ciclo nomeia o analógico e o X junto do teclado e do toque e, depois do primeiro eixo, o mapa da superfície vira passo; overlay e HUD confirmam o mapa quando o controle falou por último; se o pad some no meio da sessão, o relógio senta e o hold fica no disco — na porta só descarrega; teclado e toque não sentam porque um pad na gaveta desconectou — isso não é sessão no aparelho
- Assistência que não esconde orbe nem pontuação (`assist`): na partida e na mostra da porta, alcance maior e chuva mais lenta. A graça extra fica no campo. Isso não é sessão observada
- Velocidade da partida (`gameSpeed`): o relógio da partida anda mais devagar; a mostra da porta e o fim ficam no relógio cheio. A cama segue o relógio da sessão só na partida — o fecho sobe em cima dele; coleta e guarda guardam o tom da aposta. A assistência continua sendo alcance e queda, não este knob. `advance()` headless não dilata. Isso não é sessão observada
- Região viva (`#live`): fase, pausa, perigo, última legenda, o aviso do primeiro ciclo que o canvas já pinta e, no fim e na porta, o placar e o recorde que o canvas já mostra; no fim, a corrente que caiu se o overlay a nomeia; na porta o toque da mostra (`a mostra toca` / `a mostra raspa`) sem fingir coleta; no fim e na porta a recuperação das preferências que o painel já mostra também nasce no canvas. No fim o aviso do ciclo some. Texto no DOM não é sessão observada
- Pulso no aparelho (`haptics`): dash, land, collect, bank, hit, over e o fecho pulsam com peso distinto; queda, raspo e voz da mostra não; `reducedMotion` e pausa cancelam; sem knob separado. Stub não é sessão no controle

## O que o recorte não atende

- Contraste medido no dispositivo e em movimento — `npm run contrast` amostra pixels do stub após `draw()` e relata o par sem limiar; o aparelho alvo não foi observado
- Jogo completável com uma só mão, observado
- Sessão com cada modo ativo, observada
- Sessão com o pulso no controle, observada — o pad que some senta o relógio no disco; `reducedMotion` cancela no disco; o aparelho não foi observado
- Leitura em escala de cinza no dispositivo alvo, observada — `npm run contrast` relata pixels que só o orbe ou só o estilhaço pintam com a mesma tinta no stub; o aparelho não foi observado

Esta página não sobe o degrau. Ela impede de fingir que o recorte é completo.
