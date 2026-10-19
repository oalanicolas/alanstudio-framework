// Leitura e escrita de glTF 2.0 (.gltf com buffers externos ou data:, e .glb) e acesso a accessors.
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

export const TYPE_SIZE = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT2: 4, MAT3: 9, MAT4: 16 };
export const COMPONENT_BYTES = { 5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4 };
const GLB_MAGIC = 0x46546c67;
const CHUNK_JSON = 0x4e4f534a;
const CHUNK_BIN = 0x004e4942;

export const elementBytes = (a) => TYPE_SIZE[a.type] * COMPONENT_BYTES[a.componentType];

function lerBuffer(uri, base) {
  if (uri.startsWith("data:")) return Buffer.from(uri.slice(uri.indexOf(",") + 1), "base64");
  return readFileSync(resolve(base, decodeURIComponent(uri)));
}

/** Lê .gltf ou .glb: { json, buffers: Buffer[], baseDir }. */
export function readGltf(file) {
  const raw = readFileSync(file);
  const baseDir = dirname(file);
  let json;
  let bin = null;
  if (raw.readUInt32LE(0) === GLB_MAGIC) {
    let off = 12;
    while (off < raw.length) {
      const len = raw.readUInt32LE(off);
      const type = raw.readUInt32LE(off + 4);
      const data = raw.subarray(off + 8, off + 8 + len);
      if (type === CHUNK_JSON) json = JSON.parse(data.toString("utf8"));
      else if (type === CHUNK_BIN) bin = data;
      off += 8 + len;
    }
  } else {
    json = JSON.parse(raw.toString("utf8"));
  }
  const buffers = (json.buffers ?? []).map((b, i) => {
    if (b.uri !== undefined) return lerBuffer(b.uri, baseDir);
    if (i === 0 && bin) return bin;
    if (b.extensions?.EXT_meshopt_compression?.fallback) return null;
    throw new Error(`buffer ${i} sem dados`);
  });
  return { json, buffers, baseDir };
}

/** Bytes de uma bufferView. */
export function viewBytes(gltf, viewIndex) {
  const v = gltf.json.bufferViews[viewIndex];
  const buf = gltf.buffers[v.buffer];
  if (!buf) throw new Error(`bufferView ${viewIndex} aponta para um buffer sem dados`);
  return buf.subarray(v.byteOffset ?? 0, (v.byteOffset ?? 0) + v.byteLength);
}

/**
 * Lê um accessor como bytes compactos (sem stride), aplicando sparse.
 * Para arquivos com EXT_meshopt_compression, passe decodeView (index da view → bytes decodificados).
 */
export function accessorBytes(gltf, index, decodeView = null) {
  const a = gltf.json.accessors[index];
  const eb = elementBytes(a);
  const out = Buffer.alloc(a.count * eb);
  if (a.bufferView !== undefined) {
    const v = gltf.json.bufferViews[a.bufferView];
    const src = decodeView ? decodeView(a.bufferView) : viewBytes(gltf, a.bufferView);
    const stride = v.byteStride ?? eb;
    const base = a.byteOffset ?? 0;
    for (let i = 0; i < a.count; i++) src.copy(out, i * eb, base + i * stride, base + i * stride + eb);
  }
  if (a.sparse) {
    const s = a.sparse;
    const idxView = decodeView ? decodeView(s.indices.bufferView) : viewBytes(gltf, s.indices.bufferView);
    const valView = decodeView ? decodeView(s.values.bufferView) : viewBytes(gltf, s.values.bufferView);
    const ib = COMPONENT_BYTES[s.indices.componentType];
    for (let k = 0; k < s.count; k++) {
      const o = (s.indices.byteOffset ?? 0) + k * ib;
      const i = ib === 1 ? idxView[o] : ib === 2 ? idxView.readUInt16LE(o) : idxView.readUInt32LE(o);
      valView.copy(out, i * eb, (s.values.byteOffset ?? 0) + k * eb, (s.values.byteOffset ?? 0) + (k + 1) * eb);
    }
  }
  return out;
}

/** Lê um accessor como números (Float64 por componente, normalizado quando o accessor pede). */
export function accessorNumbers(gltf, index, decodeView = null) {
  const a = gltf.json.accessors[index];
  const bytes = accessorBytes(gltf, index, decodeView);
  const n = a.count * TYPE_SIZE[a.type];
  const out = new Float64Array(n);
  const cb = COMPONENT_BYTES[a.componentType];
  const ler = {
    5120: (o) => bytes.readInt8(o),
    5121: (o) => bytes.readUInt8(o),
    5122: (o) => bytes.readInt16LE(o),
    5123: (o) => bytes.readUInt16LE(o),
    5125: (o) => bytes.readUInt32LE(o),
    5126: (o) => bytes.readFloatLE(o),
  }[a.componentType];
  const norm = a.normalized ? { 5120: (v) => Math.max(v / 127, -1), 5121: (v) => v / 255, 5122: (v) => Math.max(v / 32767, -1), 5123: (v) => v / 65535 }[a.componentType] : null;
  for (let i = 0; i < n; i++) {
    const v = ler(i * cb);
    out[i] = norm ? norm(v) : v;
  }
  return out;
}

/** Escreve um GLB (JSON + um chunk BIN). */
export function writeGlb(json, bin) {
  const jb = Buffer.from(JSON.stringify(json), "utf8");
  const jChunk = Buffer.concat([jb, Buffer.alloc((4 - (jb.length % 4)) % 4, 0x20)]);
  const bChunk = Buffer.concat([bin, Buffer.alloc((4 - (bin.length % 4)) % 4, 0)]);
  const total = 12 + 8 + jChunk.length + (bChunk.length ? 8 + bChunk.length : 0);
  const head = Buffer.alloc(12);
  head.writeUInt32LE(GLB_MAGIC, 0);
  head.writeUInt32LE(2, 4);
  head.writeUInt32LE(total, 8);
  const jh = Buffer.alloc(8);
  jh.writeUInt32LE(jChunk.length, 0);
  jh.writeUInt32LE(CHUNK_JSON, 4);
  const partes = [head, jh, jChunk];
  if (bChunk.length) {
    const bh = Buffer.alloc(8);
    bh.writeUInt32LE(bChunk.length, 0);
    bh.writeUInt32LE(CHUNK_BIN, 4);
    partes.push(bh, bChunk);
  }
  return Buffer.concat(partes);
}

/** Triângulos e vértices desenhados, somando primitivas (modo 4 = triângulos; 5 e 6 = faixa e leque). */
export function geometryStats(gltf) {
  let triangles = 0;
  let vertices = 0;
  for (const m of gltf.json.meshes ?? []) {
    for (const p of m.primitives ?? []) {
      const nv = gltf.json.accessors[p.attributes.POSITION]?.count ?? 0;
      const ni = p.indices !== undefined ? gltf.json.accessors[p.indices].count : nv;
      vertices += nv;
      const mode = p.mode ?? 4;
      if (mode === 4) triangles += Math.floor(ni / 3);
      else if (mode === 5 || mode === 6) triangles += Math.max(0, ni - 2);
    }
  }
  return { triangles, vertices };
}
