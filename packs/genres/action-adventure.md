# Gênero — Ação-aventura (Zelda-like, mundo aberto, soulslike, hack and slash)

Aplicabilidade: `--genre action-adventure`. Orientação de gênero para direcionar
perguntas, riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: explorar e enfrentar. Decisões: para onde ir, quando lutar ou evitar, qual
  ferramenta/habilidade usar, quando investir em progressão.
- Espectro: combate (soulslike: stamina, janelas, punição), traversal (grapple,
  escalada), quebra-cabeças ambientais (Zelda), sistemas emergentes (mundo aberto).
  Registre o eixo dominante; o resto o serve.

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Combate: cancel windows, hitstop, recuo por peso da arma, i-frames legíveis,
  lock-on que não rouba câmera, feedback de bloqueio/parry distinto.
- Câmera: terceira pessoa com colisão, reposicionamento suave em espaços apertados,
  enquadramento em lock-on, sem clipping em parede.
- Traversal: aderência em bordas, "coyote" em saltos, transições sem travar animação.

## Riscos habituais

- Mundo grande e vazio: densidade de conteúdo por km² sem propósito; marcadores
  substituem curiosidade. Câmera em corredores. Dificuldade por HP inflado em vez de
  padrões novos.
- Progressão que trivializa (stat check) ou muralhas sem sinalização; saves em
  estado inconsistente (quest flags, itens duplicados).
- Streaming: pop-in, hitches ao cruzar células, físicas dormindo/acordando.

## Orçamentos e medições típicas

- Quadro p99 em combate com N inimigos + VFX; hitches de streaming (> 33 ms) por
  minuto de travessia; latência input → início de ataque; memória por célula do
  mundo; tempo de carga de save; taxa de morte por encontro em playtest.

## QA e playtest específicos

- Testes de flags de quest (ordem fora da esperada), soft locks (preso em geometria,
  item chave perdido), save/load em cada etapa de boss, combate com passo fixo e
  FPS variados.
- Playtest: a pessoa acha o caminho sem marcador? Morre e entende por quê? Prefere
  explorar ao invés de seguir o objetivo?

## Receitas e fontes

[feel](../../recipes/feel.md), [visual](../../recipes/visual.md) (câmera, culling,
streaming), [mecânicas](../../recipes/mechanics.md), [conteúdo](../../recipes/content.md)
(saves), [produção](../../recipes/production.md). Combina com [rpg](rpg.md) e
[platformer](platformer.md) conforme o eixo dominante.
