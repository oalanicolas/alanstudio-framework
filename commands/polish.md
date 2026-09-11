# Polish

Passagem final que separa "funciona" de "acabado": encontrar a dimensão mais baixa
da barra e subi-la um degrau, corrigindo por causa, sem tocar no que já está alto.
Exige fatia funcionalmente completa. Polir scaffold é decoração sobre protótipo.

## Escala

`jam`: polir é fechar feel e áudio do verbo e a leitura do primeiro minuto; nada
mais. `product`: subir o piso das dimensões pertinentes à fatia até `slice`.
`aa`: além do piso, a receita de conteúdo precisa sobreviver ao polimento — um item
polido à mão que ignora o pipeline é regressão, não acabamento.

## Avaliar

1. **Completo?** O ciclo existe no caminho real (perceber → decidir → agir →
   consequência → reinício), com estados definidos. Se não, volte a [`craft`](craft.md).
2. `bar <projeto>`: o que o projeto declara, qual dimensão é o piso, e `problems`.
   Sem tabela, a primeira tarefa é declará-la (`next` propõe exatamente isso).
   `context --focus <foco>` traz `production_bar` com as dimensões pertinentes.
3. Leitura própria: jogue o recorte e confira a declaração dimensão por dimensão —
   [barra de acabamento](../references/production-bar.md). Uma tabela otimista é
   afirmação de quem escreveu; a discordância vira achado.
4. Recibo anterior de [`critique`](critique.md) para o mesmo recorte: os P0/P1 de lá
   entram na lista; não são a lista.
5. Alinhamento ao design system: cada desvio é **token ausente**, **implementação
   avulsa** (existia consumidor canônico e não foi usado) ou **desalinhamento de
   conceito** (o item não pertence ao jogo). A correção muda conforme a causa.
6. Triagem: **funcional** (trai, bloqueia, confunde) antes de **cosmético**.

## Executar

Suba a dimensão mais baixa pelo critério do degrau seguinte, escrito na tabela,
citando a linha. Sistematicamente, só nas dimensões pertinentes:

- `feel` → [feel](../recipes/feel.md): sinal de partida, contato e término no mesmo
  quadro; perdão de entrada intencional e medido.
- `audio_mix` → [áudio](../recipes/audio.md): prioridade, ducking, variação, silêncio.
- `legibility` → [`clarify`](clarify.md). `pacing` → [`onboard`](onboard.md).
- `state_trust`, `performance`, `release` → [`harden`](harden.md), [`optimize`](optimize.md).
- `art_direction`, `content_scale` → [`visual`](visual.md), [`content`](content.md).
- `accessibility` → [`adapt`](adapt.md).

Uma variável por vez quando precisar atribuir causa. Preserve a melhor versão
demonstrada; regressão posterior não vira nova referência
([qualidade](../references/quality.md)).

## Verificar

Comparação antes/depois em condições equivalentes e em movimento; validadores do
projeto por `verify`; a tabela de degraus atualizada com condição e autor. Detector
e QA automáticos são evidência de defeito, nunca prova de acabamento. Se subiu um
degrau, diga qual e o que sustenta; se não subiu, diga o que faltou.

## Nunca

- Polir antes de o ciclo existir, ou polir a dimensão mais visível em vez da mais baixa.
- Fazer média: arte alta não compensa feel baixo.
- Cortar arte aprovada para "ganhar FPS" durante o polimento.
- Perfeccionar um canto e deixar outro áspero: o nível de acabamento é consistente.
- Criar componente ou padrão avulso quando o design system tem equivalente.
- Introduzir regressão no que já funcionava.

## Entregar

A dimensão que subiu, a evidência, a tabela atualizada, o que continua sendo o
piso e por quê. Uma próxima ação com prompt pronto. Depois de polir, [`critique`](critique.md)
mostra a diferença no mesmo recorte.
