# Arquétipos de jogador para observar

Uma revisão feita por um único olhar — o do agente que construiu — deixa passar o
que outros jogadores tropeçam primeiro. Cinco arquétipos, cada um expondo uma classe
diferente de falha. Escolha dois ou três por sessão, conforme o recorte, e relate
**o que quebrou para aquele jogador**, com o elemento exato, não a descrição do arquétipo.

Não são pessoas de verdade e não substituem playtest humano: são lentes para o
agente e para quem prepara a sessão. O que um arquétipo "acha" entra como
avaliação do agente (`role=agent`), nunca como observação de pessoa.

## 1. Quem nunca viu o jogo: "Nina"

Abre o jogo sem instrução, sem contexto, sem ler nada que bloqueie a tela.

Perguntas: a primeira ação é descoberta em segundos, pelo próprio jogo? Sabe o que
a ameaça é antes de ser punida? Entende por que perdeu? Sabe como recomeçar?

Bandeiras: mural de texto antes de jogar; primeiro erro sem causa legível; controles
que só o README explica; reinício que exige menu; ícone sem significado aprendível.

## 2. Quem domina o gênero: "Rafa"

Já jogou os melhores do gênero e mede este pelos mesmos reflexos.

Perguntas: a entrada responde no quadro em que ele espera? Buffer, coyote time e
cancelamento existem onde o gênero os pressupõe? Consegue pular tudo que não é jogo?
A ação central aguenta um minuto de repetição sem objetivo?

Bandeiras: latência ou deadzone fora do costume do gênero; tutorial impossível de
pular; animação que trava a próxima entrada; feel de placeholder num verbo central.

## 3. Quem joga sem som, com uma mão, ou com movimento reduzido: "Sam"

Precisa que estado, ameaça e alternativa cheguem por mais de um canal.

Perguntas: o jogo é completável mudo? Algum estado depende só de cor? Todos os
comandos remapeiam, inclusive os de menu? Reduzir movimento remove o tremor sem
remover o sinal de causa? Há pausa em qualquer momento seguro?

Bandeiras: aviso de perigo só em áudio; vermelho/verde sem forma; segurar e apertar
repetido sem alternativa; contraste que some na cena cheia; texto pequeno com
informação crítica.

## 4. Quem tenta quebrar: "Bia"

Pausa no meio do impacto, fecha a aba, volta, carrega save antigo, aperta tudo ao
mesmo tempo.

Perguntas: pausar, perder, reiniciar e sair têm consequência definida? Montar →
desmontar → montar deixa recurso vivo? Save inválido falha de forma legível sem
apagar progresso? Perda de foco e volta preservam o estado?

Bandeiras: som fantasma depois de reiniciar; timer que corre em pausa; progresso
perdido ao trocar de aba; dado inválido que corrompe em silêncio; ação aceita
depois do término.

## 5. Quem joga no dispositivo ruim, distraído: "Léo"

Celular mediano, uma mão, interrupções, rede lenta, primeira execução fria.

Perguntas: o primeiro carregamento tem teto e o respeita? O pior quadro da cena
representativa cabe no orçamento? Alvos de toque têm tamanho? O jogo sobrevive a
uma interrupção e volta onde estava?

Bandeiras: engasgo de primeiro shader no primeiro salto; ação principal fora do
alcance do polegar; alvo pequeno junto de outro; estado perdido na interrupção;
tempo até jogar sem medida.

## Seleção por recorte

| Recorte | Arquétipos | Por quê |
| --- | --- | --- |
| Primeiro minuto, onboarding | Nina, Léo | compreensão e interrupção |
| Feel e juice do verbo | Rafa, Sam | timing e canal alternativo |
| Confiança de estado, save, release | Bia, Léo | transições e máquina alheia |
| Acesso e adaptação | Sam, Léo | canais, entrada, toque |
| Slice ou "está no piso?" | Nina, Rafa, Bia | os três olhares que a barra pede |

## Arquétipo do projeto

Se o brief nomeia um público específico, derive um sexto arquétipo dele: perfil em
duas linhas, três comportamentos, três bandeiras. Só com dado real do brief; sem
brief, use os cinco. Ligue os achados à [barra de acabamento](production-bar.md)
pela dimensão que cada bandeira toca, e ao [protocolo de observação](quality.md)
quando forem levados a uma sessão com gente.
