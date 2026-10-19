import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { encodePng } from "../src/png.js";
import { resolveRuler } from "../src/ruler.js";
import { convertTexture, verifyTexture } from "../src/textures.js";
import { colorTexture, hasLibavif, normalTexture, tempDir } from "./_support.mjs";

const pular = !hasLibavif() && "faltam avifenc/avifdec (libavif)";
const regua = resolveRuler({}, { hasSsimulacra2: false }); // determinístico: cor por PSNR

test("cor: escolhe o menor q que passa, e a verificação confirma", { skip: pular }, async (t) => {
  const dir = tempDir(t);
  const png = join(dir, "pedra_BC.png");
  writeFileSync(png, encodePng(colorTexture(256)));
  const avif = join(dir, "pedra_BC.avif");
  const r = await convertTexture(png, avif, "color", { ruler: regua, tmpDir: dir });
  assert.equal(r.decision, "avif", r.reason);
  assert.ok(r.metrics.psnr >= regua.color.psnr && r.metrics.worstBlock >= regua.color.worstBlock);
  const abaixo = r.tries.filter((x) => x.q < r.q);
  assert.ok(abaixo.every((x) => !x.pass), "nenhum q menor passou");
  assert.equal((await verifyTexture(png, avif, "color", { ruler: regua, tmpDir: dir })).pass, true);
  assert.ok(statSync(avif).size < statSync(png).size);
});

test("normal map é medido por ângulo e alfa é medido à parte", { skip: pular }, async (t) => {
  const dir = tempDir(t);
  const nm = join(dir, "pedra_N.png");
  writeFileSync(nm, encodePng(normalTexture(256)));
  const rn = await convertTexture(nm, join(dir, "pedra_N.avif"), "normal", { ruler: regua, tmpDir: dir });
  assert.ok(rn.metrics.meanDeg <= regua.normal.meanDeg && rn.metrics.p99Deg <= regua.normal.p99Deg, JSON.stringify(rn.metrics));
  const fo = join(dir, "folha_BC.png");
  writeFileSync(fo, encodePng(colorTexture(256, 4)));
  const ra = await convertTexture(fo, join(dir, "folha_BC.avif"), "color", { ruler: regua, tmpDir: dir });
  assert.ok(ra.decision === "original" || ra.metrics.alphaPsnr >= regua.color.alphaPsnr, JSON.stringify(ra.metrics));
});

test("régua impossível mantém o original e não grava AVIF", { skip: pular }, async (t) => {
  const dir = tempDir(t);
  const png = join(dir, "x_BC.png");
  writeFileSync(png, encodePng(colorTexture(128)));
  const impossivel = resolveRuler({ color: { psnr: 200 } }, { hasSsimulacra2: false });
  const avif = join(dir, "x_BC.avif");
  const r = await convertTexture(png, avif, "color", { ruler: impossivel, tmpDir: dir });
  assert.equal(r.decision, "original");
  assert.equal(existsSync(avif), false);
});

test("a verificação acusa um AVIF que não corresponde ao original", { skip: pular }, async (t) => {
  const dir = tempDir(t);
  const a = join(dir, "a_BC.png");
  const b = join(dir, "b_BC.png");
  writeFileSync(a, encodePng(colorTexture(128, 3, 1)));
  writeFileSync(b, encodePng(colorTexture(128, 3, 2)));
  const avif = join(dir, "b_BC.avif");
  await convertTexture(b, avif, "color", { ruler: regua, tmpDir: dir });
  const v = await verifyTexture(a, avif, "color", { ruler: regua, tmpDir: dir });
  assert.equal(v.pass, false);
});
