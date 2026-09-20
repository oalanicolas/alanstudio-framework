# Criar a partir de jogos, universos e imagens

Use quando o pedido cita um jogo como modelo, uma IDV existente ou uma referência
visual. O agente faz a tradução abaixo; o criador não precisa conhecer game design.
Registre no brief ou `game-design.md` existente, sem novo formulário ou aprovação
quando o usuário já escolheu as referências.

## 1. Transforme as referências em uma cena verificável

Separe os papéis: **jogo de referência → decisões e consequências**;
**universo → personagens e linguagem**; **imagens → tratamento visual**.
Uma referência não anula a outra. Observe a fonte pertinente: jogabilidade,
arte do universo e as imagens indicadas. Listar arquivos ou ler nomes e cores não
equivale a ver imagens. Se a fonte estiver inacessível, explicite essa lacuna.

Escolha 2–3 imagens representativas quando houver um painel. Anote seus caminhos
e três características visíveis que devem aparecer na cena: por exemplo, volumes
desenhados à mão, hachura que constrói sombra e vegetação com silhuetas variadas.
Copiar a paleta e desenhar retângulos não atende essas características. Referência
de estudo orienta produção original; reutilização de assets exige direitos.

Escreva uma frase sobre a primeira situação jogável e três provas concretas:

- **Ação:** que decisão do jogo de referência o jogador executará e repetirá?
- **Identidade:** quais características das fontes serão reconhecíveis na cena?
- **Fechamento:** como esse recorte chega a uma consequência e permite continuar
  ou recomeçar?

Reduza quantidade de mapas, inimigos e sistemas até caber uma fatia terminada.
Preserve a decisão característica do gênero e o acabamento pedido. Informe esse
recorte em linguagem comum e prossiga com a autorização existente.

## 2. Construa primeiro a cena que carrega a promessa

Execute nesta ordem, antes de implementar o restante do jogo:

1. **Abra as imagens com a ferramenta de imagem**, incluindo arte do universo.
   Registre quais realmente viu; ler metadados não cumpre essa ação.
2. **Escolha o caminho de produção:** reutilizar assets adequados do acervo;
   adaptar uma cena existente com direitos; ou produzir arte original com a
   ferramenta de geração/edição de imagem disponível. Use a referência visual
   como entrada quando a ferramenta permitir. Confira a arte produzida.
3. **Monte a primeira cena real** com essa arte, personagem e ação central. Para
   uma pequena cena 2D, um cenário ilustrado e sprites próprios podem bastar;
   alinhe desenho, colisão e interação. Não crie um motor de conteúdo para isso.
4. **Capture e compare** antes de expandir as regras e o conteúdo.

Quando o pedido exige ilustração, textura ou um personagem reconhecível, não use
um conjunto de círculos/retângulos em Canvas, SVG ou CSS como atalho para a arte
final. Esses recursos servem a regras, HUD e depuração; seu uso como linguagem
visual depende da referência realmente escolhida. Se não conseguir produzir a
arte necessária, a entrega está parcial, não “concluída com arte fora do escopo”.

Abra essa cena no runtime e compare a captura com as imagens escolhidas, no
tamanho em que se joga. Confira silhueta, composição, material, detalhe e leitura
da ação. Corrija o desvio material antes de multiplicar mapas, criaturas ou menus.
Essa comparação é revisão do agente contra a direção recebida; não invente aceite
humano nem peça uma nova aprovação rotineira.

Ao adaptar um starter, siga o entrypoint até os módulos realmente consumidos.
Mantenha apenas promessas demonstráveis nos controles, documentação e entrega.
Arquivos antigos de input, áudio, save ou testes não provam integração com o jogo
novo. Áudio da ação não sai do recorte por decisão unilateral de implementação.
Verifique a URL real de fontes, imagens e sons no servidor usado para jogar.
Em jogo web estático local, execute a ajuda sem dependências do núcleo:

```sh
python3 scripts/check_web_delivery.py /caminho/do/jogo http://127.0.0.1:PORTA/
```

Ela compara o HTML servido ao arquivo do projeto e percorre recursos literais do
entrypoint (CSS, módulos, imagens, fontes e áudio), sem ler módulos órfãos. Registre
a saída no QA existente. Servidores que transformam HTML e caminhos dinâmicos
exigem conferência equivalente no navegador; não altere o jogo para passar nesta
checagem. Sucesso HTTP não comprova reprodução, arte ou jogabilidade.

## 3. Teste a promessa inteira, não apenas o primeiro efeito

Derive o roteiro das regras implementadas. Exemplos para escolher apenas o
pertinente ao pedido:

| Recorte | Prova que distingue jogo funcionando de aparência de sucesso |
| --- | --- |
| Labirinto e perseguição | Começar pelo controle anunciado; atravessar várias células e virar; ver inimigos perseguirem; coletar em posições distintas; perder e recomeçar; completar a condição de vitória. |
| Poder temporário | Ativar, usar, esperar terminar e reencontrar o perigo; se inimigo capturado retorna, observar sua volta e a retomada da perseguição. |
| Exploração e captura | Sair do início, encontrar criaturas diferentes, executar ação e resposta adversária, capturar, consultar coleção e continuar; conferir que todo conteúdo anunciado é alcançável. |
| Menus durante ação | Abrir e fechar pausa/coleção durante uma consequência pendente; retornar sem apagar turno, duplicar prêmio ou travar a ação. |

Faça a sequência principal no runtime pelo input público, com passagem real de
tempo. Testes de regras complementam com trajetos e transições inteiras; não basta
pontuar no spawn, acionar um estado ou comparar duas execuções do mesmo código.
Teste que procura nomes de funções/strings nos arquivos só verifica texto; não o
apresente como teste de movimento, batalha, captura ou do ciclo jogável.
Diagnóstico com teleporte, estado fabricado ou relógio controlado deve ser marcado
como tal e não comprova que o jogador chega ao cenário.

Compare a imagem final com as fontes e confira assets carregados, além dos testes
funcionais. Console vazio não prova ausência de 404 nem qualidade visual. Mantenha
o registro curto: cenário → esperado → observado → prova/limite. Corrija falhas
necessárias à promessa antes de apresentar como pronto; siga [entrega](delivery.md).

Origem: mecanismo de referência e comparação da Impeccable, aplicado aos casos
de adaptação de jogos registrados na [adoção](../adoption.md).
