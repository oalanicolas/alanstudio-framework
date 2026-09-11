# Audit

Checagem técnica sistemática, sem corrigir: o que é mensurável ou conferível no
harness e no repositório — ambiente, base documental, forma das declarações de
barra e gates, validadores, capacidades alegadas, proveniência. Documenta para
outros comandos resolverem. É código e forma; a experiência é [`critique`](critique.md).

## Escala

Igual em todas: a forma se confere do mesmo jeito. O que muda é o que se cobra:
`jam` não precisa de plano de produção nem de tabela com dez dimensões; cobrar isso
de um conto é ruído. `product`/`aa` cobram plano, gates declarados e proveniência
completa antes de qualquer marco.

## Avaliar

Rode, na ordem, e leia inteiro:

1. `doctor --root <lab>`: ferramentas, integridade do framework, starters,
   atalhos da skill, repositório, acervo. Itens `missing` bloqueiam; `optional` não.
2. `scan <projeto>`: nove áreas com candidato, rascunho, histórico ou não localizado;
   `agent_context`; cobertura e limites da varredura.
3. `bar <projeto>` e `gate <projeto>` ([barra](../references/production-bar.md),
   [gates](../references/gates.md)): `problems` com arquivo, linha e motivo —
   dimensão fora das dez, degrau fora dos cinco, alvo que não é o seguinte, `met`
   sem evidência, dispensa do que não se dispensa, linhas em conflito.
4. `context <projeto> --focus lifecycle`: `capabilities.mentioned` (token em
   arquivo, não capacidade), `scripts` declarados, `metadata_issues`, `git.dirty_paths`.
5. `verify <projeto> --script <validador> --output PASTA_NOVA` nos validadores
   reais; leia os logs, não só o status. Um validador que não existe é achado.
6. Proveniência: licenças, créditos, origem de cada asset embarcado
   ([release](../recipes/release.md)); licença desconhecida é P0 para entregar.
7. [Arquitetura](../references/project-audit.md): entrypoint → estado → consumidores
   percorridos de fato quando o pedido inclui o código, não só a forma.

## Executar

Relatório por severidade, cada achado com localizador:

- **Resumo:** bloqueios do `doctor`, áreas não localizadas, problemas de forma,
  validadores ausentes ou vermelhos, capacidades alegadas sem teste, licenças
  desconhecidas — contados por P0–P3.
- **Achados:** `[P?] nome` · onde (arquivo, linha) · categoria (ambiente, base,
  barra/gate, validação, capacidade, proveniência, arquitetura) · impacto ·
  recomendação · comando sugerido (`teach`, `document`, `harden`, `release`,
  `produce`, `next`).
- **Padrões sistêmicos:** o que se repete (tabela otimista sem condição em três
  documentos; `met` sem lastro em todos os gates) é problema de processo, não de linha.
- **O que está bem:** práticas a manter.

## Verificar

O relatório aponta só o que o harness leu ou executou, com o recibo. `held_by_declaration`
não é `passed`; `claimed` não é verificado; tabela bem formada e otimista sai
intacta e é dito que saiu. Nada aqui atribui degrau, concede gate ou promove marco.

## Nunca

- Corrigir durante a auditoria; ela documenta, outros comandos agem.
- Relatar problema sem impacto ou sem localizador.
- Contar `candidate_found` como suficiência, atualidade ou aprovação.
- Inflar P3 até o relatório virar ruído; o que importa cabe em uma página.
- Auditar o workspace inteiro por um pedido sobre um jogo.

## Entregar

O relatório, a lista ordenada de comandos que resolve cada achado, e a nota de que
rodar `audit` de novo depois das correções mostra o que mudou. Se houve achado
na base documental, [`teach`](teach.md) vem primeiro.
