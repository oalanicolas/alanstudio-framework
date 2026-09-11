# Gênero — Horror (survival horror, psicológico, terror em primeira pessoa)

Aplicabilidade: `--genre horror`. Orientação de gênero para direcionar perguntas,
riscos e provas; o GDD do jogo decide. Não é regra universal.

## Verbo central e decisões

- Verbo: persistir sob ameaça. Decisões: avançar ou recuar, gastar recurso escasso
  (munição, luz, save), confrontar ou esconder, quanto olhar para o que assusta.
- Modelo: survival (recursos, inventário, combate fraco), psicológico (percepção,
  narrativa não confiável), perseguição (stalker, hide and seek), jumpscare curto.
  Registre o motor do medo: antecipação, impotência, incerteza, nojo.

## Feel que importa

Com tela, a primeira superfície é a porta; o campo começa depois do avanço.

- Som acima de tudo: silêncio com propósito, camadas que sobem com proximidade, sons
  diegéticos ambíguos, mixagem que não cansa. Iluminação: escuro legível, fontes
  controláveis (lanterna com bateria), sombras que informam.
- Ritmo: tensão-alívio; o jogador precisa de espaços seguros para o medo voltar a
  funcionar. Câmera lenta e limitada é escolha; movimento pesado precisa ser
  intencional, não bug.

## Riscos habituais

- Jumpscare repetido perde efeito; inimigo visto de perto vira comédia; IA de stalker
  previsível ou injusta (teleporte sem regra). Escuro que vira ilegível em telas
  ruins; brilho sem opção.
- Acessibilidade: fotossensibilidade, ansiedade — avisos e opções (reduzir jumpscare,
  modo seguro) são parte do design, não concessão.

## Orçamentos e medições típicas

- Quadro p99 em escuridão com luzes dinâmicas e sombras; picos de áudio (LUFS) e
  faixa dinâmica; distância de detecção da IA; tempo entre eventos de tensão por
  sessão; taxa de abandono por trecho em playtest.

## QA e playtest específicos

- Testes de IA de perseguição (não fica presa, não teleporta sem regra); ilegibilidade
  do escuro em calibração mínima; pausa durante scripted scare; saves em pontos
  seguros apenas.
- Playtest: batimento/relato de tensão por trecho; a pessoa entende a regra do monstro
  após alguns encontros? Volta ao jogo no dia seguinte?

## Receitas e fontes

[feel](../../recipes/feel.md), [visual](../../recipes/visual.md) (luz, câmera),
[conteúdo](../../recipes/content.md) (áudio, saves), [produção](../../recipes/production.md).
Combina com [stealth](stealth.md), [adventure](adventure.md) e [narrativa](narrative.md).
