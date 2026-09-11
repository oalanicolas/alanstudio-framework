# Edição, mídia e entrega: extração do estudo Rezona/Crayon

Status: Ready for Review — extração e validação concluídas.

O estudo público revelou contratos de parâmetros, alterações de cena, geração
assíncrona e entrega em hosts distintos. O núcleo já orientava arquitetura,
proveniência e release; faltavam critérios explícitos para revisões obsoletas,
estados de integração do asset e identidade da transformação de exportação.

- [x] Inspecionar fontes públicas versionadas e separar código, declaração e observação.
- [x] Adaptar os canônicos existentes, sem runtime compartilhado novo.
- [x] Preservar piso artístico, fonte autoral e trabalho anterior.
- [x] Registrar condições de aplicação, contraprovas e limites.
- [x] Verificar links, diff e suíte existente do harness pelo laboratório.

Arquivos: `recipes/{architecture,content,release}.md`, `packs/platforms/web.md`,
`references/sources.md` e esta story. Evidências e relatório no laboratório conforme
[origem](../../references/sources.md#autoria-ugc-pública).

Não houve implementação de editor/SDK, geração, instalação de ferramenta concorrente
ou publicação. Critérios documentais não demonstram ganho de produtividade. Alterações
anteriores em `feel.md` e `mechanics.md` não pertencem a esta extração.

Validação: 231 testes descobertos, 226 passaram e cinco foram pulados por ausência
do acervo opcional. Foram conferidos 91 links locais/âncoras, sem falhas, e o diff
nos dois repositórios. Recibo e log no laboratório em
`framework/evidence/2026-09-09/rezona-crayon-learning/`. Os comandos npm da regra
geral não se aplicam à raiz deste harness Python. A suíte não mede a eficácia das
novas orientações nem a qualidade dos produtos estudados.
