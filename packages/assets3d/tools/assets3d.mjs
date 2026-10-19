#!/usr/bin/env node
// Otimização de ativos 3D sem perda visível.
//   assets3d textures <origem> [--saida DIR] [--perfil sem-perda-visivel|lado-a-lado] [--regras regras.json] [--regua regua.json] [--jobs N] [--relatorio texturas.json] [--forcar]
//   assets3d meshes   <origem> [--saida DIR] [--posicao 1e-5] [--uv-texels 0.1] [--textura 4096] [--normal-graus 0.1] [--relatorio malhas.json] [--forcar]
//   assets3d verify   <origem> [--saida DIR] [--perfil ...] [--regras ...] [--regua ...] [--relatorio verificacao.json]
//   assets3d report   <json...> --saida pagina.html [--titulo "..."] [--medicoes medicoes.json]
// Sem --saida, o resultado fica ao lado do original (mesmo nome, extensão .avif ou .glb). Os originais nunca são alterados.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from "node:fs";
import { cpus } from "node:os";
import { dirname, join, relative, resolve, sep } from "node:path";
import { toolVersions } from "../src/avif.js";
import { readGltf } from "../src/gltf.js";
import { compressMesh, MESH_DEFAULTS, verifyMesh } from "../src/mesh.js";
import { renderReport } from "../src/report.js";
import { roleFor } from "../src/roles.js";
import { resolveRuler } from "../src/ruler.js";
import { convertTexture, verifyTexture } from "../src/textures.js";

const VERSAO = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8")).version;

function argumentos(argv) {
  const pos = [];
  const op = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const k = a.slice(2);
      const v = argv[i + 1];
      if (v === undefined || v.startsWith("--")) op[k] = true;
      else {
        op[k] = v;
        i++;
      }
    } else pos.push(a);
  }
  return { pos, op };
}

const lerJson = (p) => (p ? JSON.parse(readFileSync(p, "utf8")) : undefined);
const hash = (x) => createHash("sha256").update(typeof x === "string" ? x : JSON.stringify(x)).digest("hex").slice(0, 16);
const mb = (b) => (b / 1e6).toFixed(2);

function andar(dir, filtro, out = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".") || e.name === "node_modules") continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) andar(p, filtro, out);
    else if (filtro(e.name)) out.push(p);
  }
  return out.sort();
}

function destino(origem, saida, arquivo, ext) {
  const rel = relative(origem, arquivo).replace(/\.[^.]+$/, ext);
  return join(saida ?? origem, rel);
}

async function emLote(itens, jobs, fn, rotulo) {
  const fila = [...itens.entries()];
  let feitos = 0;
  const t0 = Date.now();
  const res = new Array(itens.length);
  await Promise.all(
    Array.from({ length: Math.max(1, jobs) }, async () => {
      while (fila.length) {
        const [i, item] = fila.shift();
        res[i] = await fn(item);
        feitos++;
        if (feitos % 25 === 0 || feitos === itens.length) process.stderr.write(`${rotulo}: ${feitos}/${itens.length} em ${Math.round((Date.now() - t0) / 1000)} s\n`);
      }
    }),
  );
  return res;
}

function lerCache(p) {
  try {
    return JSON.parse(readFileSync(p, "utf8"));
  } catch {
    return {};
  }
}

async function texturas({ pos, op }) {
  const origem = resolve(pos[0] ?? ".");
  const saida = op.saida ? resolve(op.saida) : null;
  const ferramentas = await toolVersions();
  if (!ferramentas) throw new Error("faltam avifenc e avifdec (libavif) no PATH");
  const regua = resolveRuler(lerJson(op.regua) ?? {}, { hasSsimulacra2: Boolean(ferramentas.ssimulacra2) && !op["sem-ssimulacra2"], profile: op.perfil ?? undefined });
  const regras = lerJson(op.regras) ?? [];
  const pngs = andar(origem, (n) => /\.png$/i.test(n));
  const cacheArq = join(saida ?? origem, ".assets3d-texturas.json");
  const cache = op.forcar ? {} : lerCache(cacheArq);
  const chaveRegua = hash([regua, ferramentas.avifenc, VERSAO]);
  const jobs = Number(op.jobs) || Math.max(1, Math.floor(cpus().length / 2));
  const resultados = await emLote(
    pngs,
    jobs,
    async (png) => {
      const rel = relative(origem, png);
      const papel = roleFor(rel, regras);
      const avif = destino(origem, saida, png, ".avif");
      const sha = createHash("sha256").update(readFileSync(png)).digest("hex");
      const c = cache[rel];
      if (c && c.sha === sha && c.chave === chaveRegua && c.registro.role === papel.role && (c.registro.decision === "original" || existsSync(avif))) {
        return { arquivo: rel, guessed: papel.guessed, ...c.registro, cache: true };
      }
      mkdirSync(dirname(avif), { recursive: true });
      let registro;
      try {
        registro = await convertTexture(png, avif, papel.role, { ruler: regua, ssimulacra2: !op["sem-ssimulacra2"] });
      } catch (e) {
        registro = { role: papel.role, decision: "original", reason: `erro: ${e.message}`, pngBytes: statSync(png).size };
      }
      if (registro.decision === "original") rmSync(avif, { force: true });
      cache[rel] = { sha, chave: chaveRegua, registro };
      return { arquivo: rel, guessed: papel.guessed, ...registro };
    },
    "texturas",
  );
  mkdirSync(dirname(cacheArq), { recursive: true });
  writeFileSync(cacheArq, JSON.stringify(cache));
  const rel = { tipo: "texturas", versao: VERSAO, data: new Date().toISOString(), ferramentas, regua, total: resultados.length, resultados };
  if (op.relatorio) writeFileSync(op.relatorio, JSON.stringify(rel, null, 1));
  const conv = resultados.filter((r) => r.decision === "avif");
  const antes = resultados.reduce((s, r) => s + (r.pngBytes ?? 0), 0);
  const depois = resultados.reduce((s, r) => s + (r.decision === "avif" ? r.avifBytes : r.pngBytes ?? 0), 0);
  console.log(`texturas: ${resultados.length} de ${pngs.length} processadas · ${conv.length} em AVIF · ${resultados.length - conv.length} mantidas no original · ${mb(antes)} → ${mb(depois)} MB`);
  return rel;
}

async function malhas({ pos, op }) {
  const origem = resolve(pos[0] ?? ".");
  const saida = op.saida ? resolve(op.saida) : null;
  const opcoes = {
    positionError: Number(op.posicao ?? MESH_DEFAULTS.positionError),
    uvTexels: Number(op["uv-texels"] ?? MESH_DEFAULTS.uvTexels),
    textureSize: Number(op.textura ?? MESH_DEFAULTS.textureSize),
    normalDegrees: Number(op["normal-graus"] ?? MESH_DEFAULTS.normalDegrees),
  };
  const arquivos = andar(origem, (n) => /\.gltf$/i.test(n) || (/\.glb$/i.test(n) && saida && saida !== origem));
  const cacheArq = join(saida ?? origem, ".assets3d-malhas.json");
  const cache = op.forcar ? {} : lerCache(cacheArq);
  const chave = hash([opcoes, VERSAO]);
  const resultados = [];
  for (const arq of arquivos) {
    const rel = relative(origem, arq);
    const glb = destino(origem, saida, arq, ".glb");
    if (resolve(glb) === resolve(arq)) continue;
    let g;
    try {
      g = readGltf(arq);
    } catch (e) {
      resultados.push({ arquivo: rel, decision: "original", reason: `não abriu: ${e.message}` });
      continue;
    }
    const externos = (g.json.buffers ?? []).filter((b) => b.uri && !b.uri.startsWith("data:")).map((b) => join(g.baseDir, decodeURIComponent(b.uri)));
    const bytesAntes = statSync(arq).size + externos.reduce((s, p) => s + statSync(p).size, 0);
    const sha = hash([readFileSync(arq).toString("base64"), ...externos.map((p) => createHash("sha256").update(readFileSync(p)).digest("hex"))]);
    const c = cache[rel];
    if (c && c.sha === sha && c.chave === chave && (c.registro.decision === "original" || existsSync(glb))) {
      resultados.push({ arquivo: rel, ...c.registro, cache: true });
      continue;
    }
    const imageUri = (uri) => relative(dirname(glb), join(g.baseDir, decodeURIComponent(uri))).split(sep).map(encodeURIComponent).join("/");
    const r = compressMesh(g, { ...opcoes, imageUri });
    let registro;
    if (r.skipped) registro = { decision: "original", reason: r.skipped, bytesAntes };
    else {
      mkdirSync(dirname(glb), { recursive: true });
      // imagens externas continuam onde estão: a URI passa a ser relativa ao GLB
      const json = JSON.parse(r.glb.subarray(20, 20 + r.glb.readUInt32LE(12)).toString("utf8"));
      writeFileSync(glb, r.glb);
      const v = verifyMesh(g, readGltf(glb), opcoes);
      if (!v.ok) {
        rmSync(glb, { force: true });
        registro = { decision: "original", reason: `verificação falhou: ${v.falhas[0]}`, bytesAntes };
      } else {
        const lossy = r.accessors.filter((a) => typeof a.bits === "number");
        registro = {
          decision: "glb",
          bytesAntes,
          bytesDepois: r.glb.length,
          triangles: v.novo.triangles,
          vertices: v.novo.vertices,
          imagensExternas: (json.images ?? []).filter((i) => i.uri && !i.uri.startsWith("data:")).length,
          precisao: lossy.map((a) => ({ uso: a.uso, bits: a.bits, erro: a.erro, limite: a.limite, unidade: a.unidade })),
        };
      }
    }
    cache[rel] = { sha, chave, registro };
    resultados.push({ arquivo: rel, ...registro });
  }
  mkdirSync(dirname(cacheArq), { recursive: true });
  writeFileSync(cacheArq, JSON.stringify(cache));
  const rel = { tipo: "malhas", versao: VERSAO, data: new Date().toISOString(), opcoes, total: resultados.length, resultados };
  if (op.relatorio) writeFileSync(op.relatorio, JSON.stringify(rel, null, 1));
  const conv = resultados.filter((r) => r.decision === "glb");
  console.log(`malhas: ${resultados.length} de ${arquivos.length} processadas · ${conv.length} em GLB · ${resultados.length - conv.length} mantidas · ${mb(conv.reduce((s, r) => s + r.bytesAntes, 0))} → ${mb(conv.reduce((s, r) => s + r.bytesDepois, 0))} MB nas convertidas`);
  return rel;
}

async function verificar({ pos, op }) {
  const origem = resolve(pos[0] ?? ".");
  const saida = op.saida ? resolve(op.saida) : null;
  const ferramentas = await toolVersions();
  const regua = resolveRuler(lerJson(op.regua) ?? {}, { hasSsimulacra2: Boolean(ferramentas?.ssimulacra2) && !op["sem-ssimulacra2"], profile: op.perfil ?? undefined });
  const regras = lerJson(op.regras) ?? [];
  const pares = andar(origem, (n) => /\.png$/i.test(n)).map((png) => ({ png, avif: destino(origem, saida, png, ".avif") })).filter((p) => existsSync(p.avif));
  const jobs = Number(op.jobs) || Math.max(1, Math.floor(cpus().length / 2));
  const tex = ferramentas
    ? await emLote(pares, jobs, async ({ png, avif }) => {
        const rel = relative(origem, png);
        const papel = roleFor(rel, regras).role;
        const r = await verifyTexture(png, avif, papel, { ruler: regua, ssimulacra2: !op["sem-ssimulacra2"] });
        return { arquivo: rel, role: papel, ...r };
      }, "verificação de texturas")
    : [];
  const mal = [];
  for (const arq of andar(origem, (n) => /\.gltf$/i.test(n))) {
    const glb = destino(origem, saida, arq, ".glb");
    if (!existsSync(glb)) continue;
    const v = verifyMesh(readGltf(arq), readGltf(glb), {
      positionError: Number(op.posicao ?? MESH_DEFAULTS.positionError),
      uvTexels: Number(op["uv-texels"] ?? MESH_DEFAULTS.uvTexels),
      textureSize: Number(op.textura ?? MESH_DEFAULTS.textureSize),
      normalDegrees: Number(op["normal-graus"] ?? MESH_DEFAULTS.normalDegrees),
    });
    mal.push({ arquivo: relative(origem, arq), pass: v.ok, failed: v.falhas, original: v.original, novo: v.novo });
  }
  const falhas = [...tex, ...mal].filter((r) => !r.pass);
  const rel = { tipo: "verificacao", versao: VERSAO, data: new Date().toISOString(), regua, texturas: tex, malhas: mal, falhas: falhas.length };
  if (op.relatorio) writeFileSync(op.relatorio, JSON.stringify(rel, null, 1));
  console.log(`verificação: texturas ${tex.filter((r) => r.pass).length} de ${tex.length} na régua · malhas ${mal.filter((r) => r.pass).length} de ${mal.length} iguais na geometria e dentro do erro`);
  for (const f of falhas.slice(0, 20)) console.log(`  falhou: ${f.arquivo} — ${f.failed.join("; ")}`);
  if (!ferramentas && pares.length) console.log("  texturas não verificadas: faltam avifenc e avifdec");
  if (falhas.length) process.exitCode = 1;
  return rel;
}

function relatorio({ pos, op }) {
  if (!op.saida) throw new Error("report precisa de --saida pagina.html");
  const fontes = pos.map((p) => ({ arquivo: p, ...lerJson(p) }));
  const html = renderReport({ titulo: op.titulo, fontes, medicoes: lerJson(op.medicoes) });
  writeFileSync(op.saida, html);
  console.log(`relatório: ${op.saida}`);
}

const comandos = { textures: texturas, meshes: malhas, verify: verificar, report: relatorio };
const { pos, op } = argumentos(process.argv.slice(2));
const cmd = comandos[pos[0]];
if (!cmd || op.help || op.ajuda) {
  console.log(readFileSync(new URL(import.meta.url), "utf8").split("\n").slice(1, 7).map((l) => l.replace(/^\/\/ ?/, "")).join("\n"));
  process.exit(cmd ? 0 : 2);
}
try {
  await cmd({ pos: pos.slice(1), op });
} catch (e) {
  console.error(`assets3d: ${e.message}`);
  process.exit(2);
}
