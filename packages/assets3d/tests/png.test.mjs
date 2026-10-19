import test from "node:test";
import assert from "node:assert/strict";
import { deflateSync } from "node:zlib";
import { decodePng, encodePng, extractChannel, readPngHeader, to8bit } from "../src/png.js";
import { colorTexture } from "./_support.mjs";

test("codifica e decodifica PNG de 1 a 4 canais sem mudar um pixel", () => {
  for (const ch of [1, 2, 3, 4]) {
    const img = colorTexture(37, 4);
    const data = new Uint8Array(37 * 37 * ch);
    for (let i = 0; i < 37 * 37; i++) for (let c = 0; c < ch; c++) data[i * ch + c] = img.data[i * 4 + c];
    const png = encodePng({ width: 37, height: 37, channels: ch, data });
    const back = decodePng(png);
    assert.equal(back.channels, ch);
    assert.deepEqual(Buffer.from(back.data), Buffer.from(data));
    assert.equal(readPngHeader(png).hasAlpha, ch === 2 || ch === 4);
  }
});

test("lê PNG de 16 bits e de paleta com transparência", () => {
  const assinatura = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  const chunk = (tipo, dados) => {
    const len = Buffer.alloc(4);
    len.writeUInt32BE(dados.length);
    return Buffer.concat([len, Buffer.from(tipo, "latin1"), dados, Buffer.alloc(4)]);
  };
  const ihdr = (bits, tipo) => {
    const h = Buffer.alloc(13);
    h.writeUInt32BE(2, 0);
    h.writeUInt32BE(1, 4);
    h[8] = bits;
    h[9] = tipo;
    return h;
  };
  // 16 bits, cinza, 2×1: 0 e 65535
  const raw16 = Buffer.from([0, 0x00, 0x00, 0xff, 0xff]);
  const p16 = Buffer.concat([assinatura, chunk("IHDR", ihdr(16, 0)), chunk("IDAT", deflateSync(raw16)), chunk("IEND", Buffer.alloc(0))]);
  const d16 = decodePng(p16);
  assert.equal(d16.bitDepth, 16);
  assert.deepEqual(Array.from(to8bit(d16).data), [0, 255]);
  // paleta de 8 bits com tRNS
  const rawP = Buffer.from([0, 0, 1]);
  const pP = Buffer.concat([assinatura, chunk("IHDR", ihdr(8, 3)), chunk("PLTE", Buffer.from([255, 0, 0, 0, 0, 255])), chunk("tRNS", Buffer.from([10])), chunk("IDAT", deflateSync(rawP)), chunk("IEND", Buffer.alloc(0))]);
  const dP = decodePng(pP);
  assert.equal(dP.channels, 4);
  assert.deepEqual(Array.from(dP.data), [255, 0, 0, 10, 0, 0, 255, 255]);
});

test("separa um canal e recusa o que não é PNG", () => {
  const img = colorTexture(8, 3);
  const g = extractChannel(img, 1);
  assert.equal(g.channels, 1);
  assert.equal(g.data[5], img.data[5 * 3 + 1]);
  assert.throws(() => readPngHeader(Buffer.from("não sou png, só texto comprido o bastante para o teste")), /não é PNG/);
});
