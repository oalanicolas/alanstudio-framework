# Gênero — Furtividade (stealth, infiltração, social stealth)

Aplicabilidade: `--genre stealth`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: passar sem ser visto. Decisões: rota, tempo (esperar padrão), ferramenta
  (distração, neutralizar, esconder corpo), quando abortar e recuar.
- Modelo: puro (detecção = falha), tolerante (combate como plano B), social (se
  misturar), imersivo (sistemas combináveis). Registre o que acontece ao ser visto.

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Regras de percepção legíveis: cones de visão visualizáveis (ou aprendidos com
  consistência), estados de alerta com feedback (ícone, som, voz), luz e sombra que
  significam algo, ruído por superfície e velocidade.
- Movimento silencioso com controle fino (agachar, encostar, inclinar); esconderijos
  com entrada/saída rápidas; a espera precisa ser interessante (observar padrões).

## Riscos habituais

- IA onisciente ou cega: detecção sem regra, memória infinita/zero, guardas que
  "sentem" atrás; patrulhas sem janela; alerta global permanente sem retorno.
- Punição sem checkpoint (repetir 10 minutos); quicksave que substitui design;
  distração que resolve tudo; combate como plano B tão bom que a furtividade some.

## Orçamentos e medições típicas

- Custo de percepção (raycasts por guarda por tick) com N guardas; latência entre
  entrar no cone e feedback; taxa de detecções "injustas" relatadas em playtest;
  tempo médio por trecho e uso de cada ferramenta.

## QA e playtest específicos

- Testes de percepção com cenários (fora do cone, atrás de vidro, no escuro, correndo
  em cascalho); estados de alerta e decaimento; corpos escondidos vs vistos; pausa
  e save durante alerta.
- Playtest: a pessoa prevê a detecção antes de acontecer? Entende por que foi vista?
  Tenta rotas diferentes ao repetir?

## Receitas e fontes

[mecânicas](../../recipes/mechanics.md) (IA, estados), [visual](../../recipes/visual.md)
(luz, câmera), [feel](../../recipes/feel.md), [produção](../../recipes/production.md).
Vizinhos: [horror](horror.md), [action-adventure](action-adventure.md), [shooter](shooter.md).
