# Gênero — Narrativa interativa (contos jogáveis, visual novel, aventura)

Aplicabilidade: `--genre narrative`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: escolher, explorar, interpretar. A decisão precisa mudar estado, rota, relação
  ou compreensão — não só o próximo texto. Escolha sem consequência perceptível é UI.
- Estrutura: linear com variações, ramificada com reconvergência, ou aberta por estado.
  Registre qual, e onde o jogador percebe que a história lembra dele.
- Ritmo: alternância entre leitura, ação e silêncio; o jogador controla o avanço.

## Feel que importa

- Transições de cena e de fala, tipografia legível em movimento, tempo de exibição
  ajustável, pular/rever sem punição, feedback sutil da escolha (som, luz, postura).
- Áudio: ambiente e stingers nos momentos de virada; silêncio como recurso.

## Riscos habituais

- Escolha ilusória (todas levam ao mesmo lugar sem reconhecer a diferença).
- Histórico e save fora de sincronia: escolhas disponíveis dependem do que já aconteceu;
  versão da história compilada e versão do save são contratos distintos.
- Volume de texto sem revisão e sem plano de localização; fontes sem cobertura.
- Fim sem opções ou sem retorno; softlock por estado inconsistente.

## Orçamentos e medições típicas

- Tempo entre input e próximo texto/cena; tempo de carga por capítulo; tamanho de
  áudio de voz por idioma; memória de imagens em cena longa.

## QA e playtest específicos

- Percorrer todos os ramos com estado salvo/recarregado em cada bifurcação; caminhos
  alternativos; fim sem opções; retorno a cena já visitada.
- Playtest: a pessoa percebe que a escolha importou? Recontou a história com as
  decisões dela? Observe releitura, hesitação e o que ela achou que causou o quê.

## Receitas e fontes

[conteúdo](../../recipes/content.md) (Ink: histórico, versões), [feel](../../recipes/feel.md),
[qualidade](../../references/quality.md). Exemplo: [Era Uma Vez](../../examples/era-uma-vez-preproduction.md).
