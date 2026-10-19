import test from "node:test";
import assert from "node:assert/strict";
import { writeFileSync } from "node:fs";
import { join } from "node:path";
import { accessorNumbers, readGltf, viewBytes } from "../src/gltf.js";
import { compressMesh, meshoptViewDecoder, verifyMesh } from "../src/mesh.js";
import { gridGltf, tempDir } from "./_support.mjs";

function preparar(t) {
  const dir = tempDir(t);
  const { json, triangles, vertices } = gridGltf();
  const arq = join(dir, "grade.gltf");
  writeFileSync(arq, JSON.stringify(json));
  return { dir, arq, triangles, vertices };
}

test("comprime sem perder triângulos, atributos, morph target nem imagem embutida", (t) => {
  const { dir, arq, triangles, vertices } = preparar(t);
  const original = readGltf(arq);
  const r = compressMesh(original);
  assert.ok(!r.skipped, r.skipped);
  const glb = join(dir, "grade.glb");
  writeFileSync(glb, r.glb);
  const novo = readGltf(glb);
  const v = verifyMesh(original, novo);
  assert.equal(v.ok, true, v.falhas.join("; "));
  assert.deepEqual(v.novo, { triangles, vertices });
  assert.equal(novo.json.accessors.length, original.json.accessors.length);
  const dec = meshoptViewDecoder(novo);
  // cor de vértice e morph target saem idênticos (sem perda); UVs ficam dentro do limite (verifyMesh acima)
  for (const i of [5, 7]) assert.deepEqual(Array.from(accessorNumbers(novo, i, dec)), Array.from(accessorNumbers(original, i)));
  // a imagem embutida continua byte a byte
  assert.deepEqual(viewBytes(novo, novo.json.images[0].bufferView), viewBytes(original, original.json.images[0].bufferView));
  assert.ok(novo.json.extensionsRequired.includes("EXT_meshopt_compression"));
  assert.ok(r.glb.length < 0.8 * Buffer.byteLength(JSON.stringify(original.json)), "o GLB tem de ficar menor que o glTF em base64");
});

test("a precisão escolhida respeita o limite, inclusive UV repetido até 40", (t) => {
  const { arq } = preparar(t);
  const r = compressMesh(readGltf(arq), { uvTexels: 0.1, textureSize: 4096 });
  const uv = r.accessors.find((a) => a.uso === "TEXCOORD_0");
  assert.ok(typeof uv.bits === "number" && uv.erro <= 0.1 / 4096, JSON.stringify(uv));
  const pos = r.accessors.find((a) => a.uso === "POSITION");
  assert.ok(pos.erro <= pos.limite, JSON.stringify(pos));
  const nor = r.accessors.find((a) => a.uso === "NORMAL");
  assert.ok(nor.erro <= 0.1, JSON.stringify(nor));
});

test("a verificação acusa um vértice fora do limite", (t) => {
  const { dir, arq } = preparar(t);
  const original = readGltf(arq);
  const r = compressMesh(original, { positionError: 1e-3 });
  const glb = join(dir, "grade.glb");
  writeFileSync(glb, r.glb);
  const v = verifyMesh(original, readGltf(glb), { positionError: 1e-9 });
  assert.equal(v.ok, false);
  assert.match(v.falhas.join(" "), /POSITION/);
});

test("recusa o que não dá para reempacotar com segurança", (t) => {
  const { arq } = preparar(t);
  const g = readGltf(arq);
  g.json.extensionsUsed = ["KHR_draco_mesh_compression"];
  assert.match(compressMesh(g).skipped, /Draco/);
  const h = readGltf(arq);
  h.json.extensionsUsed = ["EXT_meshopt_compression"];
  assert.match(compressMesh(h).skipped, /já está comprimido/);
});
