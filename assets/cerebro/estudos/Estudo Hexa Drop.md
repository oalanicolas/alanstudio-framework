---
tipo: estudo
resumo: "Porta do estudo de exemplo: Hexa Drop (inventado) e o anel que some. Não é cânone nem autoriza copiar IP."
jogos:
  - "[[Oficina]]"
temas:
  - design
  - combate
status: vigente
data: 2026-09-19
referencias:
  - "[[Hexa Drop]]"
---
# Estudo Hexa Drop

Pesquisa de exemplo deste kit. Pedido: mostrar um estudo completo que passa no `check`.
Não é cânone de produto, não autoriza copiar IP e o objeto **não existe** — foi inventado
para a réplica. Substitua pelo seu estudo.

**Objeto:** Hexa Drop, 1991, Byteforge (fictício).
**Método:** leitura da ficha de exemplo [[Hexa Drop — postmortem]]. Sem playtest.
**Legenda:** **[O]** fala da designer na ficha · **[I]** inferência nossa.
**Partes:** [[Hexa Drop — o anel que some]].

## Resposta curta

A peça cai num tabuleiro hexagonal. Fechar o anel em volta do centro some as peças
desse anel e o tabuleiro pune quem deixa um buraco. [O] Um crítico de 1995 vê a
mesma queda noutro sítio ([[Estudo Cai-Cai]]). [T] [[Oficina]] adapta o contrato a
uma linha no caderno, não o hexágono. [I]

## O que isto governa e o que não governa

- Governa: o recorte de método (estudo → ludema → padrão → nosso jogo).
- Não governa: arte, nomes, fantasia. O objeto é inventado.

## O que o jogador faz

Encaixa a peça que cai. Fecha o anel ou acumula buracos até não haver espaço.

## Pontos cegos

Um clone que só copia “peça que cai” perde a punição do anel incompleto.

## Tradução para o nosso jogo

| Do objeto | Copiar · adaptar · recusar | Onde no nosso jogo | Evidência |
|---|---|---|---|
| Anel que some | adaptar | linha no caderno de [[Oficina]] | [[Oficina — o anel que chegou tarde]] |

## Recusas

IP, nomes, arte. Hexa Drop não é um jogo real.

## Lacunas

Não houve playtest. A ficha de evidência é inventada.

## Próxima ação

Substituir este estudo pelo primeiro jogo que você for estudar de verdade.

## Fontes

[[Hexa Drop — postmortem]] · [[Biblioteca de fontes]].

## Todas as partes

```base
filters:
  and:
    - parte_de == this
properties:
  file.name:
    displayName: Parte
  resumo:
    displayName: O que tem
  data:
    displayName: Data
views:
  - type: table
    name: Partes
    order:
      - file.name
      - resumo
      - status
      - data
```
