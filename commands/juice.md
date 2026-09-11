# Juice

Amplificar o sinal da consequência quando o timing já está certo: flash, hitstop,
shake, partícula, stinger e câmera trabalhando juntos no mesmo quadro do contato,
sem esconder a ação nem o próximo obstáculo. Feel é a cadeia inteira
([`feel`](feel.md)); juice é a apresentação do impacto dentro dela.

Receitas: [feel](../recipes/feel.md) (cadeia e sincronia), [visual](../recipes/visual.md)
(câmera, efeitos, comparação em movimento).

## Escala

`jam`: um sinal claro por ação central, sincronizado. `product`: cada ação com
sinal próprio de partida, contato e término (`slice`). `aa`: a ação reconhecível
num clipe de três segundos sem HUD (`flagship` em `feel`) é o alvo declarado, não
o pressuposto.

## Avaliar

1. `context <projeto> --focus feel`. Se a latência, o buffer ou a recuperação
   ainda estão errados, volte a [`feel`](feel.md): juice sobre timing errado vira
   ruído. Confirme que a regra e a apresentação já existem.
2. Nomeie a **sensação** em palavras físicas (curto e seco, pesado e lento) e o
   **ponto** do contato no quadro.
3. Inventário do que o jogo já tem: partículas, shake, flash, hitstop, stingers,
   tokens de tempo e câmera no design system. REUSE antes de criar sistema de VFX.
4. Movimento reduzido: cada efeito precisa de um sinal estático equivalente que
   preserve a causa ([acessibilidade](../recipes/accessibility.md)).

## Executar

Um elo por vez: hitstop (quadros, constante nomeada) → flash/squash → partícula →
câmera → stinger. Todos disparam no mesmo quadro do contato. Compare em movimento a
cada elo; se o próximo obstáculo ou a alternativa ficou escondida, o elo regrediu.
Variação contra fadiga (não a mesma partícula toda vez). Nada de bounce em UI que o
jogo não tem; a linguagem de movimento vem do design system.

## Verificar

Lado a lado em movimento, mesmas condições; a ação repetida por um minuto sem
objetivo; a cena com movimento reduzido ativo mantendo a leitura da causa.
`record --kind observation --field role=agent` com a captura. Screenshot não prova.

## Nunca

- Juice antes do timing: partícula não conserta latência.
- Efeitos disparando em quadros diferentes.
- Esconder a consequência ou o próximo perigo atrás do efeito.
- Copiar o checklist de juice do gênero sem o sinal próprio do verbo.
- Remover o sinal de causa ao reduzir movimento.

## Entregar

Os elos adicionados com suas constantes, a comparação em movimento, o comportamento
com movimento reduzido, o degrau observado em `feel`. Sequência: [`audio`](audio.md)
se o stinger ainda não fecha; [`polish`](polish.md).
