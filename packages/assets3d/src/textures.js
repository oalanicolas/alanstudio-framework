// Texturas PNG → AVIF com a qualidade escolhida textura por textura: a menor que passa a régua do papel.
// O que não passa, ou não fica menor que o PNG, continua no original. Nada de resolução cortada.
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, renameSync, rmSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { decodeAvif, encodeAvif, ssimulacra2 } from "./avif.js";
import { decodePng, encodePng, extractChannel, readPngHeader, to8bit } from "./png.js";
import { normalAngle, psnr } from "./metrics.js";
import { MASK_CHANNEL } from "./roles.js";
import { DEFAULT_RULER } from "./ruler.js";

/** Remove o alfa (para as métricas perceptuais, que medem só a cor). */
function semAlfa(img) {
  if (img.channels !== 4 && img.channels !== 2) return img;
  const cor = img.channels - 1;
  const n = img.width * img.height;
  const out = new Uint8Array(n * cor);
  for (let i = 0; i < n; i++) for (let c = 0; c < cor; c++) out[i * cor + c] = img.data[i * img.channels + c];
  return { ...img, channels: cor, data: out };
}

/**
 * Mede a versão decodificada contra a original pela régua do papel.
 * Retorna { pass, metrics, failed: [motivos] }.
 */
export async function measure(role, original, decoded, ruler, { tmpDir, refPng = null } = {}) {
  const r = ruler[role];
  const m = {};
  const falhas = [];
  const exigir = (nome, valor, limite, maior = true) => {
    if (limite === null || limite === undefined) return;
    if (maior ? valor < limite : valor > limite) falhas.push(`${nome} ${Number(valor).toFixed(2)} ${maior ? "<" : ">"} ${limite}`);
  };
  if (role === "mask") {
    const p = psnr(original, decoded, { channels: [[Math.min(MASK_CHANNEL, original.channels - 1), 0]] });
    Object.assign(m, { psnr: p.psnr, worstBlock: p.worstBlock });
    exigir("PSNR", p.psnr, r.psnr);
    exigir("PSNR do pior bloco", p.worstBlock, r.worstBlock);
    return { pass: !falhas.length, metrics: m, failed: falhas };
  }
  if (role === "normal") {
    const a = normalAngle(original, decoded, { z: r.z ?? "stored" });
    Object.assign(m, { meanDeg: a.mean, p99Deg: a.p99, worstBlockMeanDeg: a.worstBlockMean });
    exigir("ângulo médio", a.mean, r.meanDeg, false);
    exigir("ângulo p99", a.p99, r.p99Deg, false);
    exigir("ângulo médio do pior bloco", a.worstBlockMean, r.worstBlockMeanDeg, false);
  } else {
    const rgb = [0, 1, 2].filter((c) => c < Math.min(original.channels, decoded.channels) && !(original.channels === 2 && c === 1));
    const p = psnr(original, decoded, { channels: rgb });
    Object.assign(m, { psnr: p.psnr, worstBlock: p.worstBlock });
    exigir("PSNR", p.psnr, r.psnr);
    exigir("PSNR do pior bloco", p.worstBlock, r.worstBlock);
    if (r.ssimulacra2 != null && refPng) {
      const teste = join(tmpDir, `s2-${process.pid}-${Math.random().toString(36).slice(2)}.png`);
      writeFileSync(teste, encodePng(semAlfa(decoded)));
      try {
        m.ssimulacra2 = await ssimulacra2(refPng, teste);
      } finally {
        rmSync(teste, { force: true });
      }
      exigir("SSIMULACRA 2", m.ssimulacra2, r.ssimulacra2);
    }
  }
  if ((original.channels === 4 || original.channels === 2) && r.alphaPsnr != null) {
    const ca = original.channels - 1;
    if (decoded.channels !== original.channels) falhas.push("o alfa sumiu");
    else {
      const p = psnr(original, decoded, { channels: [[ca, ca]] });
      Object.assign(m, { alphaPsnr: p.psnr, alphaWorstBlock: p.worstBlock });
      exigir("PSNR do alfa", p.psnr, r.alphaPsnr);
      exigir("PSNR do pior bloco do alfa", p.worstBlock, r.alphaWorstBlock);
    }
  }
  return { pass: !falhas.length, metrics: m, failed: falhas };
}

export function sha256(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

/**
 * Converte uma textura. role: papel (roles.js). Retorna o registro:
 * { decision: "avif" | "original", reason, q, pngBytes, avifBytes, width, height, metrics, tries }.
 * Grava o AVIF em outAvif só quando a decisão é "avif".
 */
export async function convertTexture(pngPath, outAvif, role, opts = {}) {
  const ruler = opts.ruler ?? DEFAULT_RULER;
  const qMin = opts.qMin ?? 40;
  const speed = opts.speed ?? 6;
  const pngBytes = readFileSync(pngPath);
  const head = readPngHeader(pngBytes);
  const original = to8bit(decodePng(pngBytes));
  const tmp = mkdtempSync(join(opts.tmpDir ?? tmpdir(), "assets3d-"));
  const reg = { role, width: head.width, height: head.height, pngBytes: pngBytes.length, tries: [] };
  try {
    // entrada do codificador: máscara vira PNG de 1 canal; o resto vai como está
    let entrada = pngPath;
    if (role === "mask") {
      entrada = join(tmp, "canal.png");
      writeFileSync(entrada, encodePng(extractChannel(original, Math.min(MASK_CHANNEL, original.channels - 1))));
    }
    let refPng = null;
    if (ruler[role]?.ssimulacra2 != null && opts.ssimulacra2 !== false) {
      refPng = join(tmp, "ref.png");
      writeFileSync(refPng, encodePng(semAlfa(original)));
    }
    const hasAlpha = head.hasAlpha && role !== "mask";
    const tentativas = new Map();
    const testar = async (q) => {
      if (tentativas.has(q)) return tentativas.get(q);
      const arq = join(tmp, `q${q}.avif`);
      await encodeAvif(entrada, arq, role, q, { speed, hasAlpha });
      const dec = await decodeAvif(arq, tmp);
      if (dec.width !== original.width || dec.height !== original.height) throw new Error("o AVIF mudou a resolução");
      const r = await measure(role, original, dec, ruler, { tmpDir: tmp, refPng });
      const t = { q, bytes: statSync(arq).size, file: arq, ...r };
      tentativas.set(q, t);
      reg.tries.push({ q, bytes: t.bytes, pass: t.pass, metrics: t.metrics });
      return t;
    };
    // busca binária do menor q que passa (a régua é monótona em q na prática; a verificação final confirma)
    let escolhido = null;
    const topo = await testar(99);
    if (topo.pass) {
      let a = qMin;
      let b = 99;
      escolhido = topo;
      while (a < b) {
        const meio = (a + b) >> 1;
        const t = await testar(meio);
        if (t.pass) {
          escolhido = t;
          b = meio;
        } else a = meio + 1;
      }
      if (escolhido.q !== a) escolhido = await testar(a);
    } else {
      const sem = await testar(100);
      if (sem.pass) escolhido = sem;
    }
    if (!escolhido) return { ...reg, decision: "original", reason: "nenhuma qualidade passou a régua" };
    if (escolhido.bytes >= pngBytes.length) {
      return { ...reg, decision: "original", reason: `o AVIF que passa (q ${escolhido.q}) não fica menor que o PNG`, q: escolhido.q, metrics: escolhido.metrics };
    }
    renameSync(escolhido.file, outAvif);
    return { ...reg, decision: "avif", q: escolhido.q, avifBytes: escolhido.bytes, metrics: escolhido.metrics };
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

/** Verifica um AVIF já gerado contra o PNG original, pela régua. */
export async function verifyTexture(pngPath, avifPath, role, opts = {}) {
  const ruler = opts.ruler ?? DEFAULT_RULER;
  const original = to8bit(decodePng(readFileSync(pngPath)));
  const tmp = mkdtempSync(join(opts.tmpDir ?? tmpdir(), "assets3d-v-"));
  try {
    const dec = await decodeAvif(avifPath, tmp);
    if (dec.width !== original.width || dec.height !== original.height) {
      return { pass: false, failed: [`resolução ${dec.width}×${dec.height} ≠ ${original.width}×${original.height}`], metrics: {} };
    }
    let refPng = null;
    if (ruler[role]?.ssimulacra2 != null && opts.ssimulacra2 !== false) {
      refPng = join(tmp, "ref.png");
      writeFileSync(refPng, encodePng(semAlfa(original)));
    }
    return await measure(role, original, dec, ruler, { tmpDir: tmp, refPng });
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}
