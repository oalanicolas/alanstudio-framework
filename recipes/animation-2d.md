# Personagens 2D: montagem, animação e revisão

Aplicar à produção ou correção de personagens animados com recortes, sprites ou
malhas 2D. A técnica base é **cutout animation**; quando as partes seguem uma
hierarquia de juntas, há **skeletal animation/rigging 2D**. PNGs, articulações
procedurais e trocas de desenho podem formar uma solução híbrida. A revisão de
poses e movimento pertence à animação técnica e ao QA visual.

Complementa [conteúdo](content.md) e [feel](feel.md). Referência e qualidade
aprovadas do projeto governam o resultado. Não exige migrar de engine, adquirir
editor ou substituir um rig que funciona.

## Resolver o consumidor antes da arte

Identifique renderer, câmera, resolução de apresentação, escala no mundo, elenco
afetado, estados, timing lógico e referência aprovada. Abra o jogo e veja a ação
antes de editar. Diferencie galeria de poses, treino e partida real; uma não prova
as outras. Registre o recorte no QA/brief existente.

Prefira recursos da engine ou pipeline instalado. Spine e Godot documentam
soluções neste domínio; isso não prova qual ferramenta uma referência comercial
usa. Adotar editor/runtime requer verificar compatibilidade, exportação, licença
e integração com a versão do projeto. Não instale para descobrir.

Classifique pelo comportamento:

- **Recorte rígido:** cabeça, armadura, escudo, arma, coroa. PNG segue um encaixe;
  não dobra junto com pele ou tecido.
- **Junta articulada:** recortes sobrepostos, malha existente ou geometria do
  renderer. Escolha pela aparência na rotação extrema.
- **Superfície flexível:** capa, cauda, tecido, gélée. Deformação ou pesos de malha
  quando o rig sustentar isso; aplicar ao componente flexível.
- **Troca de desenho:** boca, mão, giro, perspectiva ou oclusão que o recorte não
  representa. Use quadros coerentes ou attachments exclusivos.
- **Efeito dependente do estado:** corda, rastro, projétil e contato seguem o
  relógio lógico. Não duplique um elemento já pintado no PNG.

Fonte incompleta ou errada pede reparo da fonte. Alongar ossos, acrescentar glow
ou esconder o membro não restaura anatomia. Não gere quadros independentes sem
um processo que mantenha identidade, proporção, arma e pivô.

## Montagem e calibração

Reproduza primeiro a pose de referência com o personagem equipado. Inspecione
alfa, partes já pintadas, margens para sobreposição, chão embutido e contaminação
por peças vizinhas. Registre fonte, recorte e consumidor no manifesto existente.
Um atlas limpo pode continuar montado incorretamente.

Use pontos **anatômicos e funcionais**: pescoço, ombro, cotovelo, punho, quadril,
joelho, tornozelo, sola, empunhadura e boca da arma. Centro/borda do retângulo não
são substitutos: a ponta da trança não é o pescoço. Transforme o ponto junto com
origem do recorte, escala, orientação e matriz do pai; não calibre só na resolução
original. Registre os dados onde o renderer realmente os consome.

Projétil que se solta da arma guarda o ponto de emissão no disparo. Feixe que
permanece conectado resolve o encaixe na pose apresentada em cada quadro,
incluindo inclinação, espelhamento e transformação de construção/upgrade.
Guarde também a origem de fallback caso o emissor desapareça. Valide o encaixe
contra o ponto realmente desenhado, não apenas repetindo a fórmula do helper;
confira separadamente que dano, alvos e cadência não mudaram.

Separe parentesco de **ordem de desenho**. Um braço herda movimento do torso mas
pode ficar atrás; antebraço e arma podem passar à frente. Inspecione preparo,
contato, recuperação e orientações suportadas. Peças mutuamente exclusivas ocupam
um slot lógico: não desenhe duas faces para simular uma transição. Interpole a
transformação e troque a imagem no instante certo.

Valide uma montagem por anatomia antes de multiplicar variantes: bípede,
quadrúpede, múltiplas pernas e corpo flexível, conforme o elenco. Compartilhe rig
só entre proporções e funções compatíveis. Evoluções usam encaixes calibrados;
não alongue o mesmo boneco para simular outra anatomia.

## Construção do movimento

Defina poses-chave e instante de contato antes dos intervalos. Preparação, contato,
recuperação e retorno precisam de silhuetas compreensíveis. Use curvas e arcos
intencionais; interpolação suave não torna uma pose correta. Preserve o timing
e as regras do jogo ao refinar o gesto.

**FK** controla rotações da hierarquia, útil para gestos livres. **IK** resolve
juntas para um alvo, útil para mão na empunhadura e pé no apoio. Configure lado
de flexão, comprimentos e alcance; não ative alongamento involuntário para alcançar
um alvo impossível. Teste perto da extensão completa e ao espelhar o personagem.
Pesos de malha e troca de skins resolvem problemas diferentes.

Na caminhada, distinga apoio e balanço. O pé apoiado acompanha o chão no espaço do
mundo; isso envolve deslocamento do corpo e fase do ciclo. Na prévia parada o pé
pode andar para trás: caminhar no lugar não prova ausência de deslizamento na
partida. Confira sola, elevação, joelho e direção. Quadrúpedes e aranhas precisam
de coordenação própria entre apoios.

Arma rígida segue a mão; mão de apoio segue seu encaixe quando necessário.
Projétil/item solto nasce na transformação correta no evento lógico de soltura.
Capa/cauda podem atrasar o corpo, mas equipamento não deve escorregar. Pausa,
morte, hitstop e reinício governam também os movimentos secundários. Mudar de
estado encerra ou mistura o gesto conforme seu contrato, sem deixá-lo escondido.

Na integração, use as **cadências reais** de todos os níveis e variantes. Um ciclo
isolado pode ser contínuo e ainda saltar quando a recuperação ocupa a preparação
do golpe seguinte. Ajuste as janelas visuais dentro do intervalo disponível,
preservando o instante lógico de contato. Tripulantes que alternam disparos têm
relógios individuais; confira também o primeiro disparo e a troca de alvo.

Congelamento retém a pose amostrada, não substitui caminhada ou ataque por repouso.
A saída mistura para o estado atual sem alongar os membros; salve os dados
necessários à continuidade. Parada assenta os pés; recuo inverte a progressão do
apoio em relação à orientação. Escala e largura do rig entram na compensação do
deslocamento. Confira isso no renderer final, inclusive quadrúpedes.

Em grupos, revise aquisição de alvo, duelo plantado, passagem de terceiros e
liberação da vaga após derrota. Afastamento radial sozinho pode trocar de lado
ao cruzar um obstáculo. Se houver deslocamento apenas visual, ele deve manter
continuidade, preservar coordenadas lógicas e alimentar sombras, barras, sockets
e impactos coerentes. Uma captura sem sobreposição não prova a sequência inteira.

Quando vários aliados convergem, confira se todos perseguem o mesmo adversário
até o primeiro contato e depois trocam de alvo. Reserve oponentes durante a
aproximação quando o combate pedir duelos; preserve exceções intencionais, como
chefes atacados por vários aliados. Amortecimento exponencial sem limite ainda
pode produzir um salto grande ao trocar a formação: meça deslocamento por quadro
e inversões de orientação com alvo estável. Corrija a causa na seleção e limite
a velocidade da correção visual. Repita as medições de combate, pois escolher
outro alvo pode mudar resultados mesmo sem alterar dano ou cadência.

## Revisão autônoma em duas passagens

Faça as revisões no turno do trabalho autorizado, sem esperar o usuário encontrar
defeitos. Não significa agendamento, revisão infinita ou aceite humano. Numa
correção localizada, recorte a cobertura ao que mudou e seus consumidores.

**Montagem e contato.** Observe os personagens afetados em repouso, preparo,
contato, recuperação e extremos da caminhada. Pause/avance quando necessário.
Procure juntas abertas, peças duplicadas, pés inclinados, pivôs errados, membros
invertidos, arma atravessando a cabeça, deformação indevida e clipping. Compare
com a versão aprovada nas mesmas condições. Uma prancha cobre o elenco, mas não
substitui a cena real nem o movimento.

Corrija a causa material: imagem, calibração, solver, ordem de desenho, relógio ou
layout. Escolha uma causa por comparação; não cubra o problema com VFX.

**Movimento e leitura.** Execute ciclos completos no runtime em velocidade normal;
reduza a velocidade depois para diagnosticar. Confira entrada/saída da ação, loop,
pausa/retomada, reinício, variante e direção. Observe no tamanho final — 64/128 px
são exemplos mobile, não escala universal — e nos fundos relevantes. Verifique
contato com chão/alvo, papel, enquadramento e um trecho aprovado que compartilha
o código. Olhe também o início e o fim do movimento, não só seu quadro bonito.

Não declare uma ação testada apenas porque clicou: confirme o estado resultante
e espere o carregamento real. Capturas devem corresponder à revisão atual; use
identificadores distintos para não confundir arquivos ou builds antigos.

Outra falha pede correção e repetição do cenário afetado. Não repita a matriz
inteira sem mudança ou dúvida nova. Encerre quando as correções estiverem
verificadas e não houver defeito material conhecido no recorte. Limitação sem
solução fica explícita, sem afirmar acabamento concluído.

## Prova e limites

Testes úteis verificam comprimentos/alcance, continuidade, amostragem estável em
pausa, apoio no mundo, exclusividade de attachments e integridade do atlas. Não
avaliam graça, silhueta ou anatomia artística. Rode o validador do projeto e
confira o build que a pessoa abrirá.

Amostre fronteiras entre estados e fases, não só alguns instantes do ciclo.
Inclua recuperação → preparação com cooldown curto, parada em fases diferentes,
avanço/recuo, pausa/congelamento e restauração. Verifique a composição final do
alfa: fade aplicado no ator e novamente no consumidor pode apagar a queda antes
do assentamento, mesmo quando cada função isolada passa nos testes.

Registre no QA existente: personagem/cenário; fase, escala e fundo; defeito;
causa e arquivo; correção; prova no runtime; regressão conferida; limites e quem
avaliou. Binários de evidência seguem o destino do workspace. Separe validado por
teste, inspecionado pelo agente e aprovado pelo criador.

## Fontes e condições de aplicação

- [Godot — Cutout animation](https://docs.godotengine.org/en/stable/tutorials/animation/cutout_animation.html):
  recortes, pivôs e combinação com quadros. Em 24/09/2026 a página avisa que não
  foi atualizada para 4.7; não assuma APIs atuais de IK a partir dela.
- [Spine — IK](https://esotericsoftware.com/spine-ik-constraints): alvos, flexão e
  extensão. Confira recursos da edição em uso.
- [Spine — Slots](https://esotericsoftware.com/spine-slots) e
  [Skins](https://esotericsoftware.com/spine-skins): ordem de desenho, exclusividade
  e variantes. Conceitos adaptáveis; não obrigam usar o runtime do produto.
- [Spine — Weights](https://esotericsoftware.com/spine-weights): deformação por pesos.
- [Adobe — Principles of animation](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html):
  poses, antecipação, arcos e movimento secundário. Intensidade depende do estilo.

Caso de aplicação: Bastiões de Eldoria, revisão de 24/09/2026 registrada no
`game-design.md` e em `arena/roster-render.js` do projeto. Pescoços, faces exclusivas,
camadas e apoios foram inspecionados em HTML. O elenco novo ainda depende de aceite
artístico. A prova sustenta diagnóstico de montagem, não certifica outros rigs,
engines ou ferramentas automaticamente.

A aplicação da skill encontrou também cauda e outras oscilações que continuavam
após a queda. Corrigir o peso do movimento secundário e conferir o renderer entre
dois instantes antes do fade evitou tratar uma pose estática correta como ciclo
correto. O teste diferencia repouso vivo de corpo caído; a revisão visual verifica
o assentamento e a passagem entre eles.
