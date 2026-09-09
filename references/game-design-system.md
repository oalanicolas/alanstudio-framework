# Design system do jogo

O equivalente a um design system de produto não é uma paleta compartilhada do
estúdio. É o contrato que permite produzir mais conteúdo do **mesmo** jogo sem
diluir a direção aprovada.

Em produto web, o sistema costuma ser: tokens, componentes, padrões, movimento,
acesso e governança. No jogo, as mesmas peças existem, mas o “componente” também
é do mundo e o “movimento” é o feel da ação.

| Design system de produto | Equivalente no jogo |
| --- | --- |
| Linguagem visual / marca | Fantasia, tom, silhueta, materiais, luz |
| Tokens | Papéis nomeados: cor, escala, tempo, câmera, tipografia, áudio |
| Componentes de UI | HUD, menus, painéis — se o jogo os tiver |
| Componentes de produto | Famílias que se repetem: inimigo, pickup, máquina, VFX, tile |
| Padrões | Receita para nascer um item novo sem quebrar o piso |
| Motion | Feel: hitstop, squash, câmera, rumble, stinger, silêncio |
| Acessibilidade | Contraste, forma além da cor, foco, toque, movimento reduzido |
| Governança | Quem aprovou o quê, alcance da aprovação, comparação em movimento |
| Storybook | Vertical slice + consumidores reais no código, não biblioteca obrigatória |

Art Bible, style guide e guia de UI são nomes da mesma área. Um moodboard ou uma
capa aprovada são o **piso**, não o sistema. O sistema existe quando um implementador
consegue criar o próximo personagem, tela ou efeito e saber se ainda pertence ao jogo.

## Duas camadas

**Estúdio:** este contrato, o [piso de qualidade](quality.md)
e o modo de aprovar/comparar. Não há paleta, tipografia ou feel únicos para todos
os jogos.

**Jogo:** a instância preenchida. Todo jogo identificável precisa da sua. Um jogo
pequeno pode reunir as seções no Art Bible, no `game-design.md` ou no README; a
ausência é lacuna. Família (Rabisco, por exemplo) autoriza ADAPT com proveniência
declarada; o destino continua tendo instância própria.

Não exigir Storybook, tokens CSS nem biblioteca web. Jogo sem HUD, sem som ou sem
juice registra a escolha. Arquivo de paleta sem consumidor não descreve o sistema
ativo; localize o uso real.

## Contrato mínimo da instância

1. **Autoridade:** referências com origem, quem aprovou, o que a aprovação não cobre
   e o que não pode degradar.
2. **Tokens:** papéis nomeados e, quando existirem, o caminho do consumidor.
3. **Componentes do mundo:** famílias recorrentes e como um item novo nasce.
4. **Feel / feedback:** sinal percebido da ação central; ligar ao verbo do GDD.
   Cadeia: intenção → input → antecipação → corpo → impacto → câmera → áudio
   → recuperação. Receita: [feel](../recipes/feel.md).
5. **Áudio / mix:** papéis (ação, mundo, música, stinger, silêncio), consumidor
   real e interrupção. Piso de gravação licenciada salvo direção explícita em
   contrário. Receita: [áudio](../recipes/audio.md).
6. **UI / HUD / acesso:** ou a decisão explícita de não ter interface tradicional.
7. **Fazer / não fazer:** um exemplo que cabe e um que quebra a direção.
8. **Proveniência:** origem, crédito e condição de uso dos recursos.
9. **Verificação:** cenário de comparação em movimento, nas mesmas condições.

GDD define o que o jogador faz. O design system define como isso se parece, soa,
pesa e se multiplica. MDA continua sendo hipótese de experiência, não paleta.
Áudio deixou de ser sub-item de feel: mix e silêncio têm consumidor próprio.

## Quando preencher

Na criação, na [aprovação de direção](project-audit.md#aprovação-de-direção-materializar-e-continuar)
e quando a área `art_direction` não estiver confirmada. O template é
[art-bible](../assets/templates/art-bible.md). O scanner localiza o documento; não
certifica tokens, consumidores nem aprovação artística.

## Continuidade

- **Onde estamos:** o contrato do estúdio existe; as instâncias continuam no documento
  canônico de cada jogo, com profundidade desigual.
- **Próximo passo:** ao trabalhar num jogo identificável, preencher ou recuperar a
  instância dele — tokens com consumidor, feel do verbo sincronizado no impacto,
  mix da consequência e uma receita de conteúdo novo (repeatability).
- **Por que agora:** sem isso, arte e UI novas improvisam e o piso aprovado não se
  reproduz.
- **Pronto quando:** as nove áreas acima têm fato, hipótese ou lacuna com próxima ação,
  e o próximo asset tem uma receita observável.
- **Retomar por:** este guia, o Art Bible do jogo e os consumidores rastreados no código.
