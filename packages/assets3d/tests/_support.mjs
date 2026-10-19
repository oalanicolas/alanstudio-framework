// Fixtures sintéticas: texturas e malhas geradas em código, sem binários no repositório.
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

export function tempDir(t) {
  const d = mkdtempSync(join(tmpdir(), "assets3d-test-"));
  t.after(() => rmSync(d, { recursive: true, force: true }));
  return d;
}

export function hasLibavif() {
  try {
    execFileSync("avifenc", ["--version"], { stdio: "ignore" });
    execFileSync("avifdec", ["--version"], { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

// gerador determinístico
export function rng(seed = 1) {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 2 ** 32;
  };
}

/** Textura de cor com detalhe fino (ruído) sobre gradiente: o tipo que perde granulado com q baixo. */
export function colorTexture(size = 256, channels = 3, seed = 7) {
  const r = rng(seed);
  const data = new Uint8Array(size * size * channels);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const o = (y * size + x) * channels;
      const n = (r() - 0.5) * 60;
      data[o] = Math.max(0, Math.min(255, 90 + x * 0.4 + n));
      data[o + 1] = Math.max(0, Math.min(255, 70 + y * 0.3 + n * 0.8));
      data[o + 2] = Math.max(0, Math.min(255, 50 + n * 0.6));
      if (channels === 4) data[o + 3] = (x >> 4) % 2 ? 255 : 128;
    }
  }
  return { width: size, height: size, channels, bitDepth: 8, data };
}

/** Normal map tangente de calombos suaves com microrrelevo. */
export function normalTexture(size = 256, seed = 3) {
  const r = rng(seed);
  const data = new Uint8Array(size * size * 3);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const nx = 0.35 * Math.sin(x / 9) + (r() - 0.5) * 0.08;
      const ny = 0.35 * Math.cos(y / 11) + (r() - 0.5) * 0.08;
      const nz = Math.sqrt(Math.max(0, 1 - nx * nx - ny * ny));
      const o = (y * size + x) * 3;
      data[o] = Math.round((nx * 0.5 + 0.5) * 255);
      data[o + 1] = Math.round((ny * 0.5 + 0.5) * 255);
      data[o + 2] = Math.round((nz * 0.5 + 0.5) * 255);
    }
  }
  return { width: size, height: size, channels: 3, bitDepth: 8, data };
}

const f32 = (arr) => Buffer.from(new Float32Array(arr).buffer);
const u16 = (arr) => Buffer.from(new Uint16Array(arr).buffer);
const u8 = (arr) => Buffer.from(new Uint8Array(arr));

/**
 * glTF de uma grade n×n com POSITION (longe da origem), NORMAL, TANGENT, TEXCOORD_0 repetido (UV até 40),
 * TEXCOORD_1, COLOR_0 em bytes, índices, um morph target e uma imagem embutida por bufferView.
 */
export function gridGltf(n = 24) {
  const pos = [];
  const nor = [];
  const tan = [];
  const uv0 = [];
  const uv1 = [];
  const cor = [];
  const morph = [];
  for (let j = 0; j <= n; j++) {
    for (let i = 0; i <= n; i++) {
      const h = 0.3 * Math.sin(i / 3) * Math.cos(j / 4);
      pos.push(1000 + i * 0.25, 50 + h, -300 + j * 0.25);
      const dx = (0.3 / 3) * Math.cos(i / 3) * Math.cos(j / 4);
      const dz = (-0.3 / 4) * Math.sin(i / 3) * Math.sin(j / 4);
      const l = Math.hypot(-dx * 4, 1, -dz * 4);
      nor.push(-dx * 4 / l, 1 / l, -dz * 4 / l);
      tan.push(1, 0, 0, j % 2 ? 1 : -1);
      uv0.push((i / n) * 40, (j / n) * 40);
      uv1.push(i / n, j / n);
      cor.push((i * 10) % 256, (j * 10) % 256, 128, 255);
      morph.push(0, 0.01 * i, 0);
    }
  }
  const idx = [];
  for (let j = 0; j < n; j++) {
    for (let i = 0; i < n; i++) {
      const a = j * (n + 1) + i;
      idx.push(a, a + n + 1, a + 1, a + 1, a + n + 1, a + n + 2);
    }
  }
  const imagem = u8([0x89, 0x50, 0x4e, 0x47, 1, 2, 3, 4, 5, 6, 7, 8]);
  const partes = [f32(pos), f32(nor), f32(tan), f32(uv0), f32(uv1), u8(cor), u16(idx), f32(morph), imagem];
  const views = [];
  let off = 0;
  const blocos = [];
  for (const p of partes) {
    const pad = (4 - (off % 4)) % 4;
    if (pad) blocos.push(Buffer.alloc(pad));
    off += pad;
    views.push({ buffer: 0, byteOffset: off, byteLength: p.length });
    blocos.push(p);
    off += p.length;
  }
  const bin = Buffer.concat(blocos);
  const v = (n + 1) * (n + 1);
  const mm = (arr, k) => {
    const min = Array(k).fill(Infinity);
    const max = Array(k).fill(-Infinity);
    for (let i = 0; i < arr.length; i++) {
      min[i % k] = Math.min(min[i % k], arr[i]);
      max[i % k] = Math.max(max[i % k], arr[i]);
    }
    return { min, max };
  };
  const json = {
    asset: { version: "2.0" },
    buffers: [{ byteLength: bin.length, uri: `data:application/octet-stream;base64,${bin.toString("base64")}` }],
    bufferViews: views,
    accessors: [
      { bufferView: 0, componentType: 5126, count: v, type: "VEC3", ...mm(pos, 3) },
      { bufferView: 1, componentType: 5126, count: v, type: "VEC3" },
      { bufferView: 2, componentType: 5126, count: v, type: "VEC4" },
      { bufferView: 3, componentType: 5126, count: v, type: "VEC2" },
      { bufferView: 4, componentType: 5126, count: v, type: "VEC2" },
      { bufferView: 5, componentType: 5121, normalized: true, count: v, type: "VEC4" },
      { bufferView: 6, componentType: 5123, count: idx.length, type: "SCALAR" },
      { bufferView: 7, componentType: 5126, count: v, type: "VEC3", ...mm(morph, 3) },
    ],
    images: [{ bufferView: 8, mimeType: "image/png" }],
    meshes: [{ primitives: [{ attributes: { POSITION: 0, NORMAL: 1, TANGENT: 2, TEXCOORD_0: 3, TEXCOORD_1: 4, COLOR_0: 5 }, indices: 6, targets: [{ POSITION: 7 }] }] }],
    nodes: [{ mesh: 0 }],
    scenes: [{ nodes: [0] }],
  };
  return { json, triangles: idx.length / 3, vertices: v };
}
