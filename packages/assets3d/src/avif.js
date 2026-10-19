// Codificação e decodificação AVIF pela CLI da libavif (avifenc/avifdec).
import { execFile } from "node:child_process";
import { readFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { decodePng } from "./png.js";
import { ROLES } from "./roles.js";

const run = (cmd, args) =>
  new Promise((resolve, reject) =>
    execFile(cmd, args, { maxBuffer: 1 << 26 }, (err, out, errOut) => (err ? reject(new Error(`${cmd}: ${(errOut || err.message).trim()}`)) : resolve(String(out)))),
  );

/** Versões das ferramentas, ou null se faltar alguma obrigatória. */
export async function toolVersions() {
  const v = {};
  try {
    v.avifenc = (await run("avifenc", ["--version"])).split("\n")[0].trim();
    v.avifdec = (await run("avifdec", ["--version"])).split("\n")[0].trim();
  } catch {
    return null;
  }
  try {
    await run("ssimulacra2", []);
  } catch (e) {
    v.ssimulacra2 = /Usage/.test(e.message) ? "presente" : null;
  }
  return v;
}

/**
 * Argumentos do avifenc para um papel e uma qualidade (0..100; 100 = sem perda).
 * Cor e emissive: 4:4:4 sRGB. Normal e material: 4:4:4 com matriz identidade (RGB sem conversão).
 * Máscara: 4:0:0 (só luma), a partir de um PNG de 1 canal.
 */
export function encodeArgs(role, quality, { speed = 6, jobs = 2, hasAlpha = false } = {}) {
  const r = ROLES[role];
  const args = ["-j", String(jobs), "-s", String(speed), "--yuv", r.yuv];
  if (quality >= 100) args.push("--lossless");
  else args.push("-q", String(quality));
  if (r.space === "linear" && r.yuv === "444" && quality < 100) args.push("--cicp", "2/2/0");
  if (hasAlpha && quality < 100) args.push("--qalpha", String(quality));
  return args;
}

export async function encodeAvif(inputPng, outputAvif, role, quality, opts = {}) {
  await run("avifenc", [...encodeArgs(role, quality, opts), inputPng, outputAvif]);
}

/** Decodifica um AVIF como o navegador decodifica (8 bits) e devolve a imagem de png.js. */
export async function decodeAvif(file, tmpDir) {
  const out = join(tmpDir, `dec-${process.pid}-${Math.random().toString(36).slice(2)}.png`);
  await run("avifdec", ["-d", "8", file, out]);
  try {
    return decodePng(readFileSync(out));
  } finally {
    rmSync(out, { force: true });
  }
}

/** SSIMULACRA 2 entre dois PNG (precisa do binário ssimulacra2 da libjxl). */
export async function ssimulacra2(refPng, testPng) {
  return parseFloat(await run("ssimulacra2", [refPng, testPng]));
}
