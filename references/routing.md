# Navegação contextual

Use esta rota quando `$game-dev` chegar sem um subcomando explícito. Navegar é
recomendar; não é autorização para criar projeto, reescrever direção, instalar
dependências, publicar ou promover marco.

## Leitura única de sinais

1. Se a raiz ou o binding ainda não foi confirmado nesta sessão, rode
   `python3 scripts/game.py doctor --root <laboratório>` uma vez.
2. Sem projeto identificável, rode `discover --root <laboratório>`. A ordem é a do
   disco, não uma prioridade. Se não houver jogo, recomende `init`; não o execute.
3. Com um projeto definido, rode `context <projeto> --focus <foco>` e leia o JSON
   inteiro. Para escolher continuidade, use `next <projeto> --focus <foco>` apenas
   quando o pedido realmente for “o que vem agora?”.
4. Não repita detector, `doctor`, `discover` ou `context` se a saída vigente já está
   na conversa.

## Como apresentar a navegação

Comece com duas ou três recomendações específicas, em ordem de dependência. Para
cada uma, diga em uma frase qual sinal a motivou e o que ela produz. Depois mostre o
menu completo agrupado: Construir, Avaliar, Refinar, Ampliar, Corrigir e Produzir.

Não despeje o catálogo antes de raciocinar sobre o estado. Não esconda o restante do
menu depois das recomendações. Se falta projeto ou uma decisão que mudaria o jogo,
nomeie a lacuna em vez de inventar prioridade.

## Mapa de intenção

| Situação observada ou pedida | Rota principal | Continuação comum |
| --- | --- | --- |
| Criar, mudar, adicionar, “faça funcionar” | `craft` | começa por `shape` |
| Jogo novo sem destino no disco | `init` | `craft` |
| Inicializar base ou reconstruir documentação | `teach` | comando original |
| Extrair o design system existente | `document` | `visual` ou `content` |
| Referência visual aprovada | `visual` com evento `direction-approved` | `document` |
| Verbo funciona, mas não convence | `feel` | `audio`, depois `juice` |
| “Está pronta?”, “está AAA?”, “o que falta?” | `critique` | `polish` |
| Revisão técnica sem correção | `audit` | comando apontado pelo achado |
| Jogador não entende ou trava no início | `clarify` ou `onboard` | `playtest` |
| Perda de progresso, pausa ou interrupção frágil | `harden` | `audit` |
| Outro dispositivo, público, sem som ou uma mão | `adapt` | `playtest` |
| Engasgo, aquecimento ou carregamento ruim | `optimize` | confirmar qualidade visual |
| Escopo grande e irregular | `distill` | `shape` |
| Novo trecho, inimigo ou item custa heroísmo | `content` | `produce` |
| Alpha, beta, gold ou plano de produção | `produce` | `release` |
| “Continue”, “vamos avançar” | `next` com evento `resume` | comando proposto |

## Limites da rota

Sinal no disco não é comportamento observado; recibo não é aprovação; teste não é
playtest; documentação não é implementação; URL não é publicação. Quando houver
ambiguidade, consulte [manual operacional](operations.md) e mantenha explícita a
diferença entre `claimed`, `observed` e `verified`.
