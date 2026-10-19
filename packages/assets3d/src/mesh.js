// Malhas glTF → GLB com EXT_meshopt_compression, sem simplificar e sem descartar dados.
// Só NORMAL, TANGENT e TEXCOORD_n (e POSITION, se positionError > 0) da malha base recebem filtro com perda, e a precisão de cada
// accessor é a menor que respeita o limite de erro medido; o resto (índices, cores, pesos, morph targets,
// animação) vai sem perda. A verificação decodifica o resultado e compara com o original.
import { MeshoptEncoder } from "../vendor/meshoptimizer/meshopt_encoder.js";
import { MeshoptDecoder } from "../vendor/meshoptimizer/meshopt_decoder.mjs";
import { accessorBytes, accessorNumbers, elementBytes, geometryStats, TYPE_SIZE, viewBytes, writeGlb } from "./gltf.js";

await MeshoptEncoder.ready;
await MeshoptDecoder.ready;

export const MESH_DEFAULTS = {
  // fração da diagonal da caixa do accessor; 0 = posições exatas. Arredondar posição move a caixa de cada peça em frações de
  // milímetro, invisível na malha, mas o consumidor que decide por limite (corte de teto, colisão, classificação por altura)
  // pode trocar de lado numa peça que está exatamente no limite. Por isso o padrão é exato; arredondar é escolha explícita.
  positionError: 0,
  uvTexels: 0.1, // erro máximo de UV, em texels de uma textura de lado textureSize
  textureSize: 4096,
  normalDegrees: 0.1, // erro angular máximo de NORMAL e TANGENT
};

const pad4 = (n) => Math.ceil(n / 4) * 4;

function usos(json) {
  const papel = new Map(); // accessor → Set de usos
  const marcar = (i, u) => {
    if (typeof i !== "number") return;
    if (!papel.has(i)) papel.set(i, new Set());
    papel.get(i).add(u);
  };
  for (const m of json.meshes ?? []) {
    for (const p of m.primitives ?? []) {
      marcar(p.indices, (p.mode ?? 4) === 4 ? "TRIANGLES" : "INDICES");
      for (const [k, i] of Object.entries(p.attributes ?? {})) marcar(i, k);
      for (const t of p.targets ?? []) for (const i of Object.values(t)) marcar(i, "MORPH");
    }
  }
  for (const s of json.skins ?? []) marcar(s.inverseBindMatrices, "IBM");
  for (const a of json.animations ?? []) for (const s of a.samplers ?? []) {
    marcar(s.input, "ANIM");
    marcar(s.output, "ANIM");
  }
  return papel;
}

/** Motivo para não tocar no arquivo, ou null. */
export function unsupportedReason(json) {
  const ext = new Set([...(json.extensionsUsed ?? []), ...(json.extensionsRequired ?? [])]);
  if (ext.has("EXT_meshopt_compression") || ext.has("KHR_meshopt_compression")) return "já está comprimido com meshopt";
  if (ext.has("KHR_draco_mesh_compression")) return "usa Draco: converta a partir da fonte sem compressão";
  // bufferView citada fora de accessors e imagens (extensão desconhecida): não dá para reempacotar com segurança
  const fora = [];
  const andar = (o, caminho) => {
    if (!o || typeof o !== "object") return;
    for (const [k, v] of Object.entries(o)) {
      if (k === "bufferView" && !/^(accessors|images)\[\d+\](\.sparse\.(indices|values))?$/.test(caminho)) fora.push(caminho);
      else if (v && typeof v === "object") andar(v, Array.isArray(o) ? `${caminho}[${k}]` : caminho ? `${caminho}.${k}` : k);
    }
  };
  for (const [k, v] of Object.entries(json)) if (v && typeof v === "object") andar(v, k);
  return fora.length ? `bufferView usada fora de accessors e imagens (${fora[0]})` : null;
}

function filtrar(tipo, f32, count, bits) {
  if (tipo === "POSITION") return { data: MeshoptEncoder.encodeFilterExp(f32, count, 12, bits, "SharedComponent"), stride: 12, filter: "EXPONENTIAL" };
  if (tipo === "TEXCOORD") return { data: MeshoptEncoder.encodeFilterExp(f32, count, 8, bits, "Separate"), stride: 8, filter: "EXPONENTIAL" };
  // NORMAL (preenchido para 4 floats) e TANGENT: octaédrico em int16 normalizado
  return { data: MeshoptEncoder.encodeFilterOct(f32, count, 8, bits), stride: 8, filter: "OCTAHEDRAL" };
}

function desfiltrar(enc, count) {
  const comp = MeshoptEncoder.encodeGltfBuffer(enc.data, count, enc.stride, "ATTRIBUTES");
  const out = new Uint8Array(count * enc.stride);
  MeshoptDecoder.decodeGltfBuffer(out, count, enc.stride, comp, "ATTRIBUTES", enc.filter);
  return Buffer.from(out.buffer);
}

function erroMaximo(tipo, original, dec, count) {
  let max = 0;
  if (tipo === "POSITION" || tipo === "TEXCOORD") {
    const n = tipo === "POSITION" ? 3 : 2;
    const stride = n * 4;
    for (let i = 0; i < count; i++) {
      for (let c = 0; c < n; c++) max = Math.max(max, Math.abs(dec.readFloatLE(i * stride + c * 4) - original[i * n + c]));
    }
    return max;
  }
  const comps = tipo === "NORMAL" ? 3 : 4;
  for (let i = 0; i < count; i++) {
    const o = [0, 1, 2].map((c) => original[i * comps + c]);
    const d = [0, 1, 2].map((c) => Math.max(dec.readInt16LE(i * 8 + c * 2) / 32767, -1));
    const no = Math.hypot(...o) || 1;
    const nd = Math.hypot(...d) || 1;
    const dot = Math.min(1, Math.max(-1, (o[0] * d[0] + o[1] * d[1] + o[2] * d[2]) / (no * nd)));
    max = Math.max(max, (Math.acos(dot) * 180) / Math.PI);
    if (comps === 4 && Math.sign(dec.readInt16LE(i * 8 + 6)) !== Math.sign(original[i * 4 + 3])) return Infinity;
  }
  return max;
}

function diagonal(numeros, n, count) {
  const min = Array(n).fill(Infinity);
  const max = Array(n).fill(-Infinity);
  for (let i = 0; i < count; i++) {
    for (let c = 0; c < n; c++) {
      min[c] = Math.min(min[c], numeros[i * n + c]);
      max[c] = Math.max(max[c], numeros[i * n + c]);
    }
  }
  return Math.hypot(...max.map((v, c) => v - min[c])) || 1;
}

/** Menor número de bits que respeita o limite; null quando nem o máximo serve. */
function escolherBits(tipo, original, count, limite) {
  const [lo, hi] = tipo === "NORMAL" || tipo === "TANGENT" ? [8, 16] : [8, 24];
  const fonte = new Float32Array(tipo === "NORMAL" ? count * 4 : original.length);
  if (tipo === "NORMAL") for (let i = 0; i < count; i++) fonte.set([original[i * 3], original[i * 3 + 1], original[i * 3 + 2], 0], i * 4);
  else fonte.set(original);
  const passa = (bits) => {
    const enc = filtrar(tipo, fonte, count, bits);
    return erroMaximo(tipo, original, desfiltrar(enc, count), count) <= limite ? enc : null;
  };
  if (!passa(hi)) return null;
  let a = lo;
  let b = hi;
  while (a < b) {
    const m = (a + b) >> 1;
    if (passa(m)) b = m;
    else a = m + 1;
  }
  return { bits: a, ...passa(a) };
}

/**
 * Comprime um glTF lido por readGltf. Retorna { glb, accessors: [{index, uso, bits, erro}], skipped }.
 * opts: MESH_DEFAULTS sobrescritos; imageUri(uri) reescreve a URI de imagens externas (GLB gravado noutra pasta).
 */
export function compressMesh(gltf, opts = {}) {
  const o = { ...MESH_DEFAULTS, ...opts };
  const motivo = unsupportedReason(gltf.json);
  if (motivo) return { skipped: motivo };
  const json = structuredClone(gltf.json);
  const uso = usos(json);
  const partes = [];
  let binLen = 0;
  let rawLen = 0;
  let quantizou = false;
  const views = [];
  const put = (bytes) => {
    const pad = pad4(binLen) - binLen;
    if (pad) partes.push(Buffer.alloc(pad));
    binLen += pad;
    const at = binLen;
    partes.push(Buffer.from(bytes.buffer, bytes.byteOffset, bytes.byteLength));
    binLen += bytes.byteLength;
    return at;
  };
  const relatorio = [];

  // imagens embutidas: copiadas sem mudança
  for (const img of json.images ?? []) {
    if (img.bufferView === undefined) continue;
    const bytes = viewBytes(gltf, img.bufferView);
    views.push({ buffer: 0, byteOffset: put(bytes), byteLength: bytes.length });
    img.bufferView = views.length - 1;
  }

  json.accessors.forEach((a, i) => {
    if (a.bufferView === undefined && !a.sparse) return;
    const usosA = [...(uso.get(i) ?? [])];
    const semantico = usosA.length === 1 ? usosA[0] : null;
    let dados = accessorBytes(gltf, i);
    delete a.sparse; // fica denso, com os mesmos valores
    delete a.byteOffset;
    let stride = elementBytes(a);
    let filter = "NONE";
    let mode = "ATTRIBUTES";
    let info = { index: i, uso: usosA.join("+") || "sem uso", bits: null, erro: 0 };

    const tipo = semantico === "POSITION" ? "POSITION" : semantico === "NORMAL" ? "NORMAL" : semantico === "TANGENT" ? "TANGENT" : /^TEXCOORD_\d+$/.test(semantico ?? "") ? "TEXCOORD" : null;
    if (tipo && a.componentType === 5126 && !a.normalized) {
      const numeros = accessorNumbers(gltf, i);
      const n = TYPE_SIZE[a.type];
      const limite = tipo === "POSITION" ? o.positionError * diagonal(numeros, n, a.count) : tipo === "TEXCOORD" ? o.uvTexels / o.textureSize : o.normalDegrees;
      const escolha = escolherBits(tipo, Float32Array.from(numeros), a.count, limite);
      if (escolha) {
        const dec = desfiltrar(escolha, a.count);
        info = { ...info, bits: escolha.bits, erro: erroMaximo(tipo, numeros, dec, a.count), limite, unidade: tipo === "NORMAL" || tipo === "TANGENT" ? "graus" : "unidades" };
        dados = Buffer.from(escolha.data.buffer, escolha.data.byteOffset, escolha.data.byteLength);
        stride = escolha.stride;
        filter = escolha.filter;
        if (filter === "OCTAHEDRAL") {
          a.componentType = 5122;
          a.normalized = true;
          delete a.min;
          delete a.max;
          quantizou = true;
        } else if (a.min || tipo === "POSITION") {
          // os limites do accessor acompanham os valores arredondados
          a.min = Array(n).fill(Infinity);
          a.max = Array(n).fill(-Infinity);
          for (let k = 0; k < a.count * n; k++) {
            const v = dec.readFloatLE(k * 4);
            a.min[k % n] = Math.min(a.min[k % n], v);
            a.max[k % n] = Math.max(a.max[k % n], v);
          }
        }
      } else {
        info.bits = "sem perda";
      }
    }
    if (semantico === "TRIANGLES" && a.count % 3 === 0) mode = "TRIANGLES";
    else if (semantico === "TRIANGLES" || semantico === "INDICES") mode = "INDICES";

    const cabe = mode === "ATTRIBUTES" ? stride % 4 === 0 && stride <= 256 : stride === 2 || stride === 4;
    if (!cabe || a.count === 0) {
      views.push({ buffer: 0, byteOffset: put(dados), byteLength: dados.length, ...(stride !== elementBytes(a) ? { byteStride: stride } : {}) });
    } else {
      const comp = MeshoptEncoder.encodeGltfBuffer(new Uint8Array(dados.buffer, dados.byteOffset, dados.byteLength), a.count, stride, mode);
      const at = put(comp);
      views.push({
        buffer: 1,
        byteOffset: rawLen,
        byteLength: a.count * stride,
        ...(mode === "ATTRIBUTES" && stride !== elementBytes(a) ? { byteStride: stride } : {}),
        extensions: { EXT_meshopt_compression: { buffer: 0, byteOffset: at, byteLength: comp.byteLength, byteStride: stride, count: a.count, mode, ...(filter !== "NONE" ? { filter } : {}) } },
      });
      rawLen += pad4(a.count * stride);
    }
    a.bufferView = views.length - 1;
    relatorio.push(info);
  });

  if (o.imageUri) for (const img of json.images ?? []) if (img.uri && !img.uri.startsWith("data:")) img.uri = o.imageUri(img.uri);
  json.bufferViews = views;
  json.buffers = [{ byteLength: pad4(binLen) }, { byteLength: rawLen, extensions: { EXT_meshopt_compression: { fallback: true } } }];
  const usadas = new Set([...(json.extensionsUsed ?? []), "EXT_meshopt_compression"]);
  const exigidas = new Set([...(json.extensionsRequired ?? []), "EXT_meshopt_compression"]);
  if (quantizou) {
    usadas.add("KHR_mesh_quantization");
    exigidas.add("KHR_mesh_quantization");
  }
  json.extensionsUsed = [...usadas];
  json.extensionsRequired = [...exigidas];
  return { glb: writeGlb(json, Buffer.concat(partes, binLen)), accessors: relatorio };
}

/** Lê as views de um GLB com EXT_meshopt_compression, decodificadas. */
export function meshoptViewDecoder(gltf) {
  const cache = new Map();
  return (vi) => {
    if (cache.has(vi)) return cache.get(vi);
    const v = gltf.json.bufferViews[vi];
    const m = v.extensions?.EXT_meshopt_compression;
    let out;
    if (!m) out = viewBytes(gltf, vi);
    else {
      const src = gltf.buffers[m.buffer].subarray(m.byteOffset ?? 0, (m.byteOffset ?? 0) + m.byteLength);
      const alvo = new Uint8Array(m.count * m.byteStride);
      MeshoptDecoder.decodeGltfBuffer(alvo, m.count, m.byteStride, src, m.mode, m.filter ?? "NONE");
      out = Buffer.from(alvo.buffer);
    }
    cache.set(vi, out);
    return out;
  };
}

function mesmosTriangulos(a, b) {
  if (a.length !== b.length) return false;
  for (let t = 0; t < a.length; t += 3) {
    const x = [a[t], a[t + 1], a[t + 2]];
    const y = [b[t], b[t + 1], b[t + 2]];
    const igual = [0, 1, 2].some((r) => x[0] === y[r] && x[1] === y[(r + 1) % 3] && x[2] === y[(r + 2) % 3]);
    if (!igual) return false;
  }
  return true;
}

/**
 * Confere o GLB comprimido contra o original, accessor por accessor.
 * Retorna { ok, original: {triangles, vertices}, novo: {...}, falhas: [...] }.
 */
export function verifyMesh(original, novo, opts = {}) {
  const o = { ...MESH_DEFAULTS, ...opts };
  const falhas = [];
  const g0 = geometryStats(original);
  const g1 = geometryStats(novo);
  if (g0.triangles !== g1.triangles || g0.vertices !== g1.vertices) falhas.push(`geometria mudou: ${g0.triangles}/${g0.vertices} → ${g1.triangles}/${g1.vertices}`);
  if (original.json.accessors.length !== novo.json.accessors.length) falhas.push("número de accessors mudou");
  const dec = meshoptViewDecoder(novo);
  const uso = usos(original.json);
  original.json.accessors.forEach((a, i) => {
    const b = novo.json.accessors[i];
    if (!b) return;
    if (a.count !== b.count || a.type !== b.type) return falhas.push(`accessor ${i}: contagem ou tipo mudou`);
    const sem = [...(uso.get(i) ?? [])];
    const s = sem.length === 1 ? sem[0] : "";
    const va = accessorNumbers(original, i);
    const vb = accessorNumbers(novo, i, dec);
    if (s === "TRIANGLES" && a.count % 3 === 0) {
      if (!mesmosTriangulos(va, vb)) falhas.push(`accessor ${i}: triângulos diferentes`);
      return;
    }
    const n = TYPE_SIZE[a.type];
    if (s === "NORMAL" || s === "TANGENT") {
      let max = 0;
      for (let k = 0; k < a.count; k++) {
        const p = [0, 1, 2].map((c) => va[k * n + c]);
        const q = [0, 1, 2].map((c) => vb[k * n + c]);
        const dot = (p[0] * q[0] + p[1] * q[1] + p[2] * q[2]) / ((Math.hypot(...p) || 1) * (Math.hypot(...q) || 1));
        max = Math.max(max, (Math.acos(Math.min(1, Math.max(-1, dot))) * 180) / Math.PI);
        if (n === 4 && Math.sign(va[k * 4 + 3]) !== Math.sign(vb[k * 4 + 3])) return falhas.push(`accessor ${i}: sinal da tangente mudou`);
      }
      if (max > o.normalDegrees + 1e-9) falhas.push(`accessor ${i} (${s}): ${max.toFixed(4)}° > ${o.normalDegrees}°`);
      return;
    }
    let max = 0;
    for (let k = 0; k < va.length; k++) max = Math.max(max, Math.abs(va[k] - vb[k]));
    let limite = 0;
    if (s === "POSITION") limite = o.positionError * diagonal(va, n, a.count);
    else if (/^TEXCOORD_\d+$/.test(s)) limite = o.uvTexels / o.textureSize;
    if (max > limite * (1 + 1e-9)) falhas.push(`accessor ${i} (${s || "sem uso"}): erro ${max.toExponential(3)} > ${limite.toExponential(3)}`);
  });
  return { ok: falhas.length === 0, original: g0, novo: g1, falhas };
}
