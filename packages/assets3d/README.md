# Pacote de ativos 3D

Deixa texturas e malhas menores **sem perda visível**: a qualidade de cada textura é a menor que
passa uma régua medida, as malhas mantêm cada triângulo e atributo, e tudo é conferido N de N
depois de decodificar. A receita diz quando usar e o que verificar:
[Ativos menores sem perda visível](../../recipes/performance.md#ativos-menores-sem-perda-visível).
Este arquivo cobre o pacote: comandos, régua, formato, testes e limites.

ES modules, **zero dependências npm**, Node ≥ 20. Dependências externas:
[libavif](https://github.com/AOMediaCodec/libavif) (`avifenc`, `avifdec`) para texturas e, para a
régua de cor, o `ssimulacra2` da [libjxl](https://github.com/libjxl/libjxl) (sem ele, a cor é medida
por PSNR com limites mais duros). O meshoptimizer vai vendorizado em `vendor/` (MIT).

## Comandos

```sh
node tools/assets3d.mjs textures <origem> [--saida DIR] [--perfil sem-perda-visivel|lado-a-lado] \
  [--regras regras.json] [--regua regua.json] [--jobs N] [--relatorio texturas.json] [--forcar]
node tools/assets3d.mjs meshes <origem> [--saida DIR] [--posicao 0] [--uv-texels 0.1] \
  [--textura 4096] [--normal-graus 0.1] [--relatorio malhas.json] [--forcar]
node tools/assets3d.mjs verify <origem> [--saida DIR] [--perfil ...] [--relatorio verificacao.json]
node tools/assets3d.mjs report texturas.json malhas.json verificacao.json --saida pagina.html \
  [--titulo "..."] [--medicoes medicoes.json]
```

- **textures**: cada `.png` vira `.avif` quando passa a régua e fica menor; senão fica no PNG, com o
  motivo no JSON. Busca binária do q (4 a 7 codificações por textura). Cache por hash do PNG, papel,
  régua e versão do codificador: a segunda execução só refaz o que mudou.
- **meshes**: cada `.gltf` vira `.glb` com `EXT_meshopt_compression`. Só `NORMAL`, `TANGENT` e
  `TEXCOORD_n` da malha base recebem filtro com perda, cada um com a menor precisão que respeita o
  limite; índices, cores, pesos, morph targets, animação e imagens embutidas vão sem perda. As posições
  ficam exatas por padrão: arredondá-las move a caixa de cada peça em frações de milímetro, e um jogo
  que decide por limite (corte de teto, colisão, altura) troca de lado a peça que está exatamente nele.
  `--posicao 1e-5` (fração da diagonal) arredonda, quando o consumidor não decide nada pela geometria.
  O resultado é decodificado e comparado com o original antes de ser aceito. Draco, arquivos já
  comprimidos e `bufferView` usada por extensão desconhecida são recusados com o motivo.
- **verify**: recalcula a régua para todo par original × convertido e sai com código 1 se algum falhar.
- **report**: página antes × agora gerada só dos JSON. `--medicoes` acrescenta números do jogo
  rodando: `{ "antes": {"downloadMB", "vramMB", "heapMB", "cargaS", "fps"}, "agora": {...}, "notas": "..." }`.

`--papeis papeis.json` dá o papel de cada arquivo a partir do manifesto do projeto
(`{"pasta/Wall_BC.png": "color"}`; papéis: `color`, `emissive`, `normal`, `material`, `mask`) e vence o
sufixo; use quando o runtime decide o formato por papel. `--lista arquivos.txt` (um caminho relativo por
linha) limita textures, meshes e verify aos arquivos que o jogo usa. O caminho é normalizado (`a/../b`); se o
arquivo no disco só difere na caixa (`x_NM.png` para a linha `x_nm.png`), ele entra e a saída leva a grafia da
lista, que é a que o jogo pede ao servidor. Linha sem arquivo aparece no resumo e em `semArquivo` no relatório, e
faz o verify falhar.

Sem `--saida`, o resultado fica ao lado do original. Os originais nunca são alterados: o projeto
escolhe no carregamento entre o `.avif`/`.glb` e o original, e deve manter um interruptor para jogar
com os originais e comparar.

## Papéis e régua

O papel vem do sufixo do nome (`_BC`, `_N`, `_ORM`, `_EM`, `_Mask`…; ver `src/roles.js`). Sem
casamento, a textura é tratada como cor, a régua mais exigente. `--regras` acrescenta padrões do
projeto, testados antes dos padrão: `[{"role": "material", "pattern": "_mrs$"}]`.

| Papel | Codificação | Perfil `sem-perda-visivel` (padrão) | Perfil `lado-a-lado` |
| --- | --- | --- | --- |
| Cor, luz própria | AVIF 4:4:4 sRGB | SSIMULACRA 2 ≥ 90; alfa PSNR ≥ 47 e pior bloco ≥ 44 | SSIMULACRA 2 ≥ 80 |
| Normal map | AVIF 4:4:4, matriz identidade | ângulo médio ≤ 0,5°, p99 ≤ 2°, pior bloco ≤ 1° | 0,8° / 3° / 1,5° |
| Material (MRA/ORM) | AVIF 4:4:4, matriz identidade | PSNR ≥ 47 e pior bloco ≥ 44 | 42 / 38 |
| Máscara de 1 canal | AVIF 4:0:0 do canal G | PSNR ≥ 47 e pior bloco ≥ 44 | 42 / 38 |

- Cor: na escala publicada do SSIMULACRA 2, 90 é "visually lossless" (ninguém nota num teste de
  alternância em 1:1) e 80 é imperceptível lado a lado
  ([README do ssimulacra2](https://github.com/cloudinary/ssimulacra2)). Sem o binário, a cor usa
  PSNR ≥ 50 e pior bloco ≥ 48 (perfil padrão), mais duros que o SSIMULACRA 2 equivalente.
- Mapas de dados não são vistos diretamente e não têm limiar publicado. Os limites foram
  calibrados num conjunto real de texturas de jogo para cair no mesmo patamar de qualidade do
  codificador que a cor em cada perfil. Confirme no render do seu projeto.
- **Pior bloco** é o PSNR (ou o ângulo médio) do bloco de 64 px com mais erro: a média esconde perda local.
- `--regua` ajusta qualquer limite por papel (`{"normal": {"z": "reconstruct"}}` mede a normal como
  um formato de dois canais reconstrói). Usar um perfil ou limite mais frouxo é decisão de quem aprova o
  acabamento; o relatório registra o perfil usado.

## O que a régua não mede

- A textura é medida em tamanho cheio, antes da compressão em bloco da GPU (BC7, ASTC), que é uma
  segunda perda. No jogo ela aparece menor e iluminada: a prova final é a captura no render.
- Normal map em formato de dois canais (BC5) reconstrói o Z: meça com `z: "reconstruct"`.
- Malhas: o limite de UV é em texels de uma textura de lado `--textura`; texturas maiores pedem o lado real.
- AVIF sem perda costuma ficar maior que o PNG: nesses casos o PNG fica.

## API

```js
import { convertTexture, verifyTexture, resolveRuler, roleFor, readGltf, compressMesh, verifyMesh, renderReport } from "./src/index.js";
const ruler = resolveRuler({}, { profile: "sem-perda-visivel", hasSsimulacra2: true });
const r = await convertTexture("Wall_BC.png", "Wall_BC.avif", roleFor("Wall_BC.png").role, { ruler });
const m = compressMesh(readGltf("Wall.gltf"));        // { glb, accessors } ou { skipped }
const v = verifyMesh(readGltf("Wall.gltf"), readGltf("Wall.glb"));
```

## Testes

```sh
cd packages/assets3d && node --test
```

Fixtures sintéticas geradas no teste (texturas com detalhe fino, normal map, alfa, grade glTF com cor
de vértice, segundo UV, morph target e imagem embutida). Os testes de textura e da CLI são pulados
sem a libavif.
