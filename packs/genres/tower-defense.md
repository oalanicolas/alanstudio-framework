# Gênero — Tower defense (fixo, livre, híbrido com ação)

Aplicabilidade: `--genre tower-defense`. Orientação de gênero para direcionar
perguntas, riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: preparar para a onda. Decisões: onde e o que construir, quando melhorar vs
  expandir, quando vender, como moldar o caminho (maze), como gastar entre ondas.
- Modelo: caminho fixo (posições de torre), construção livre (o jogador cria o
  labirinto), híbrido (herói controlável ou ação em tempo real). Registre e defina o
  tempo entre ondas (pausa, acelerar, iniciar cedo por bônus).

## Feel que importa

- Colocação: preview com alcance, snap, validação instantânea de caminho bloqueado;
  som e animação de construção; venda com feedback.
- Ondas legíveis: preview da próxima onda, contagem, inimigos com silhueta por tipo
  (voador, blindado, rápido); projéteis que acertam visualmente (homing ou
  antecipação).
- Acelerar tempo (2×/3×) sem quebrar física ou som.

## Riscos habituais

- Uma torre dominante (DPS/custo); ondas que só escalam HP; pathfinding com labirinto
  livre (recalcular sem travar; inimigos presos ao bloquear); vazamento de dano por
  projétil perdido.
- Sem informação: alcance real, prioridade de alvo, DPS não visíveis; ondas finais
  decididas pela economia das primeiras (sem recuperação).

## Orçamentos e medições típicas

- Quadro p99 na onda final com máximo de inimigos + projéteis + torres em velocidade
  3×; tempo de recálculo de caminho ao construir; balanceamento por simulação: taxa
  de vitória por estratégia simples/ótima por mapa.
- Interface: fração da altura de anel, poderes, herói, recursos e chamada da onda em
  celular estreito, celular largo e tablet 4:3, contra a faixa de *Interface móvel*.

## Interface móvel: tamanhos validados (paisagem)

Medido em quatro tower defense de trilho publicados para celular, de três estúdios (n = 3), pelo
layout do pacote (templates, XML, atlas) e por capturas de aparelho. Unidade: **fração da altura da
tela**, que é o que o polegar e o olho percebem; pixels CSS não se comparam entre aparelhos.

| Elemento | Faixa observada | Como aparece |
| --- | --- | --- |
| Anel de construção | 28–38% | opções de 10–14% cada, preço na própria opção; título e descrição fora do anel no celular |
| Poderes / magias | 13–17% | canto inferior, longe do herói |
| Retrato do herói | 11–14% | canto inferior oposto |
| Recursos (vida, ouro, onda) | 5–12% | um bloco no topo, número legível de relance |
| Pausa / velocidade | 7,5–11% | canto superior |
| Chamada da onda | 7–12% | ícone na entrada do caminho, com contagem até a próxima onda e bônus por antecipar |
| Texto de interface | ≈3–3,5% no celular | rótulos curtos; descrição em painel, não no campo |

**Aplicar** em TD de trilho para celular e tablet em paisagem. **Verificar:** medir a caixa real de cada
elemento no navegador nas resoluções-alvo (celular estreito, celular largo, tablet 4:3), dividir pela
altura e comparar com a faixa; olhar o campo com o anel aberto e com uma onda em andamento.

- **O anel não passa de ~40% da altura no celular.** Acima disso ele cobre metade do campo e o jogador
  constrói às cegas (caso observado: 59%, com opções de 22%). Diminuir o desenho e manter o alvo de toque.
- **No tablet, a proporção acompanha a altura; não os pixels.** Interface que só ganha alvos maiores em px
  encolhe na tela (caso observado: recursos a 4,6% e texto a 2% da altura). Uma referência reduz a escala
  do HUD a ≈0,85 em telas 4:3; as demais mantêm a fração do celular.
- **A onda é chamada na entrada do caminho**, em dois toques (inspecionar, confirmar), com a contagem e o
  bônus no próprio ícone. Uma barra de onda no rodapé duplica a função e ocupa o centro inferior, onde o
  caminho costuma passar; no celular, retirar. Em tablet há espaço para manter.
- **Toque continua ≥ 44 pt.** Quando a faixa pede um desenho menor, ampliar a área de toque, não o desenho.

**Invalida:** TD de construção livre (sem anel), jogos em retrato, câmera com zoom ou rolagem do campo
(a fração da tela deixa de ser estável) e produtos pensados primeiro para tablet. **Limites:** capturas
medidas com erro de ±1 ponto; quadros de atlas incluem margem e sombra; sem medição em aparelho físico das
referências; a escala do campo (torres, atores, estrada) não entrou na regra.

## QA e playtest específicos

- Simulação headless de ondas com builds fixas (a "build óbvia" deve perder em
  algum ponto e a "build boa" deve vencer); validação de caminho em labirintos;
  determinismo em 1×/3×; pausa entre ondas.
- Playtest: a pessoa lê o alcance antes de construir? Reage à onda preview? Repete
  o mapa com outra estratégia?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md) (economia, passo fixo), [feel](../../recipes/feel.md),
[visual](../../recipes/visual.md) (legibilidade), [produção](../../recipes/production.md),
[web](../platforms/web.md#aprendizados-de-interface-de-jogo-no-celular) (jogo, não página).
Vizinhos: [strategy](strategy.md), [idle](idle.md) (TD incremental).
