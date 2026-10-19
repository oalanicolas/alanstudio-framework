// PNG sem dependência: decodifica (tons de cinza, RGB, paleta, com alfa; 1 a 16 bits; sem entrelaçamento)
// e codifica 8 bits. Serve à medição: a imagem sai como amostras por canal, sem gerenciamento de cor.
import { deflateSync, inflateSync } from "node:zlib";

const ASSINATURA = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const CANAIS_POR_TIPO = { 0: 1, 2: 3, 3: 1, 4: 2, 6: 4 };

const CRC_TABELA = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();

function crc32(buffers) {
  let c = 0xffffffff;
  for (const b of buffers) for (let i = 0; i < b.length; i++) c = CRC_TABELA[(c ^ b[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function paeth(a, b, c) {
  const p = a + b - c;
  const pa = Math.abs(p - a);
  const pb = Math.abs(p - b);
  const pc = Math.abs(p - c);
  return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
}

/** Lê só o cabeçalho: { width, height, bitDepth, colorType, channels, hasAlpha }. */
export function readPngHeader(buffer) {
  const b = Buffer.from(buffer.buffer ?? buffer, buffer.byteOffset ?? 0, buffer.byteLength ?? buffer.length);
  if (b.length < 33 || !b.subarray(0, 8).equals(ASSINATURA) || b.toString("latin1", 12, 16) !== "IHDR") {
    throw new Error("não é PNG");
  }
  const colorType = b[25];
  return {
    width: b.readUInt32BE(16),
    height: b.readUInt32BE(20),
    bitDepth: b[24],
    colorType,
    channels: CANAIS_POR_TIPO[colorType],
    hasAlpha: colorType === 4 || colorType === 6,
  };
}

/**
 * Decodifica um PNG.
 * Retorna { width, height, channels, bitDepth (8|16), data } com data intercalada por canal
 * (Uint8Array em 8 bits ou menos, Uint16Array em 16). Paleta vira RGB ou RGBA (com tRNS).
 */
export function decodePng(buffer) {
  const b = Buffer.from(buffer.buffer ?? buffer, buffer.byteOffset ?? 0, buffer.byteLength ?? buffer.length);
  const h = readPngHeader(b);
  if (!h.channels) throw new Error(`PNG com tipo de cor ${h.colorType} não suportado`);
  let off = 8;
  let interlace = 0;
  let palette = null;
  let trns = null;
  const idat = [];
  while (off + 8 <= b.length) {
    const len = b.readUInt32BE(off);
    const type = b.toString("latin1", off + 4, off + 8);
    const data = b.subarray(off + 8, off + 8 + len);
    if (type === "IHDR") interlace = data[12];
    else if (type === "PLTE") palette = data;
    else if (type === "tRNS") trns = data;
    else if (type === "IDAT") idat.push(data);
    else if (type === "IEND") break;
    off += 12 + len;
  }
  if (interlace) throw new Error("PNG entrelaçado (Adam7) não suportado: regrave sem entrelaçamento");
  const raw = inflateSync(Buffer.concat(idat));
  const { width, height, bitDepth, colorType } = h;
  const ch = h.channels;
  const bitsPorPixel = ch * bitDepth;
  const stride = Math.ceil((width * bitsPorPixel) / 8);
  const bpp = Math.max(1, bitsPorPixel >> 3);
  const linhas = Buffer.alloc(stride * height);
  let anterior = Buffer.alloc(stride);
  for (let y = 0, p = 0; y < height; y++) {
    const filtro = raw[p++];
    const linha = linhas.subarray(y * stride, (y + 1) * stride);
    raw.copy(linha, 0, p, p + stride);
    p += stride;
    for (let x = 0; x < stride; x++) {
      const a = x >= bpp ? linha[x - bpp] : 0;
      const c = x >= bpp ? anterior[x - bpp] : 0;
      const up = anterior[x];
      if (filtro === 1) linha[x] = (linha[x] + a) & 0xff;
      else if (filtro === 2) linha[x] = (linha[x] + up) & 0xff;
      else if (filtro === 3) linha[x] = (linha[x] + ((a + up) >> 1)) & 0xff;
      else if (filtro === 4) linha[x] = (linha[x] + paeth(a, up, c)) & 0xff;
    }
    anterior = linha;
  }
  const n = width * height;
  if (colorType === 3) {
    if (!palette) throw new Error("PNG de paleta sem PLTE");
    const outCh = trns ? 4 : 3;
    const out = new Uint8Array(n * outCh);
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const bit = x * bitDepth;
        const byte = linhas[y * stride + (bit >> 3)];
        const idx = bitDepth === 8 ? byte : (byte >> (8 - bitDepth - (bit & 7))) & ((1 << bitDepth) - 1);
        const o = (y * width + x) * outCh;
        out[o] = palette[idx * 3];
        out[o + 1] = palette[idx * 3 + 1];
        out[o + 2] = palette[idx * 3 + 2];
        if (trns) out[o + 3] = idx < trns.length ? trns[idx] : 255;
      }
    }
    return { width, height, channels: outCh, bitDepth: 8, data: out };
  }
  if (bitDepth === 16) {
    const out = new Uint16Array(n * ch);
    for (let y = 0; y < height; y++) {
      for (let i = 0; i < width * ch; i++) out[y * width * ch + i] = linhas.readUInt16BE(y * stride + i * 2);
    }
    return { width, height, channels: ch, bitDepth: 16, data: out };
  }
  const out = new Uint8Array(n * ch);
  if (bitDepth === 8) {
    for (let y = 0; y < height; y++) linhas.copy(out, y * width * ch, y * stride, y * stride + width * ch);
  } else {
    // cinza de 1, 2 ou 4 bits: expande para 0..255
    const max = (1 << bitDepth) - 1;
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const bit = x * bitDepth;
        const v = (linhas[y * stride + (bit >> 3)] >> (8 - bitDepth - (bit & 7))) & max;
        out[y * width + x] = Math.round((v * 255) / max);
      }
    }
  }
  return { width, height, channels: ch, bitDepth: 8, data: out };
}

function chunk(type, data) {
  const t = Buffer.from(type, "latin1");
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32([t, data]));
  return Buffer.concat([len, t, data, crc]);
}

/** Codifica uma imagem de 8 bits (1 a 4 canais) em PNG. */
export function encodePng({ width, height, channels, data }) {
  const tipo = { 1: 0, 2: 4, 3: 2, 4: 6 }[channels];
  if (tipo === undefined) throw new Error(`não há PNG com ${channels} canais`);
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8;
  ihdr[9] = tipo;
  const stride = width * channels;
  const raw = Buffer.alloc((stride + 1) * height);
  for (let y = 0; y < height; y++) {
    // filtro Sub: barato e bem melhor que nenhum para texturas
    const o = y * (stride + 1);
    raw[o] = 1;
    for (let x = 0; x < stride; x++) {
      const v = data[y * stride + x];
      raw[o + 1 + x] = (v - (x >= channels ? data[y * stride + x - channels] : 0)) & 0xff;
    }
  }
  return Buffer.concat([ASSINATURA, chunk("IHDR", ihdr), chunk("IDAT", deflateSync(raw, { level: 6 })), chunk("IEND", Buffer.alloc(0))]);
}

/** Converte para 8 bits por canal (16 bits é arredondado). */
export function to8bit(img) {
  if (img.bitDepth === 8) return img;
  const out = new Uint8Array(img.data.length);
  for (let i = 0; i < out.length; i++) out[i] = Math.round(img.data[i] / 257);
  return { ...img, bitDepth: 8, data: out };
}

/** Separa um canal (0 = R/cinza, 1 = G, 2 = B, 3 = A) numa imagem de 1 canal. */
export function extractChannel(img, channel) {
  if (channel >= img.channels) throw new Error(`a imagem tem ${img.channels} canais; não há o canal ${channel}`);
  const n = img.width * img.height;
  const out = new (img.bitDepth === 16 ? Uint16Array : Uint8Array)(n);
  for (let i = 0; i < n; i++) out[i] = img.data[i * img.channels + channel];
  return { width: img.width, height: img.height, channels: 1, bitDepth: img.bitDepth, data: out };
}
