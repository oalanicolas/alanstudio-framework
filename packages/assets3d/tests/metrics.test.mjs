import test from "node:test";
import assert from "node:assert/strict";
import { normalAngle, psnr } from "../src/metrics.js";
import { colorTexture, normalTexture } from "./_support.mjs";

test("PSNR de imagens idênticas é 120 dB e segue 10·log10(1/MSE)", () => {
  const a = colorTexture(64);
  assert.equal(psnr(a, a).psnr, 120);
  const b = { ...a, data: Uint8Array.from(a.data, (v) => Math.min(255, v + 1)) };
  const r = psnr(a, b);
  // quase todo pixel erra 1/255: ~48,1 dB
  assert.ok(r.psnr > 47.9 && r.psnr < 48.2, `psnr ${r.psnr}`);
});

test("o pior bloco acusa um estrago local que a média esconde", () => {
  const a = colorTexture(256);
  const b = { ...a, data: Uint8Array.from(a.data) };
  for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) for (let c = 0; c < 3; c++) b.data[(y * 256 + x) * 3 + c] = 0;
  const r = psnr(a, b, { block: 64 });
  assert.ok(r.psnr - r.worstBlock > 10, `global ${r.psnr} × pior bloco ${r.worstBlock}`);
});

test("erro angular de normal map: zero quando igual, e o ângulo da rotação quando gira", () => {
  const a = normalTexture(64);
  assert.ok(normalAngle(a, a).mean < 1e-4); // só arredondamento de ponto flutuante
  // inclina tudo para um normal fixo diferente
  const plano = (nx) => {
    const nz = Math.sqrt(1 - nx * nx);
    const data = new Uint8Array(64 * 64 * 3);
    for (let i = 0; i < 64 * 64; i++) data.set([Math.round((nx * 0.5 + 0.5) * 255), 128, Math.round((nz * 0.5 + 0.5) * 255)], i * 3);
    return { width: 64, height: 64, channels: 3, bitDepth: 8, data };
  };
  const r = normalAngle(plano(0), plano(Math.sin((10 * Math.PI) / 180)));
  assert.ok(Math.abs(r.mean - 10) < 0.6, `ângulo ${r.mean}`);
  assert.throws(() => psnr(colorTexture(8), colorTexture(16)), /resoluções diferentes/);
});
