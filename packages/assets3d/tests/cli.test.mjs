import test from "node:test";
import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { encodePng } from "../src/png.js";
import { colorTexture, gridGltf, hasLibavif, normalTexture, tempDir } from "./_support.mjs";

const CLI = fileURLToPath(new URL("../tools/assets3d.mjs", import.meta.url));
const node = (args) => execFileSync(process.execPath, [CLI, ...args], { encoding: "utf8" });

test("ponta a ponta: texturas, malhas, verificação N de N, relatório e cache", { skip: !hasLibavif() && "faltam avifenc/avifdec (libavif)" }, (t) => {
  const dir = tempDir(t);
  const src = join(dir, "ativos");
  const out = join(dir, "leve");
  mkdirSync(join(src, "pedra"), { recursive: true });
  writeFileSync(join(src, "pedra", "muro_BC.png"), encodePng(colorTexture(128)));
  writeFileSync(join(src, "pedra", "muro_N.png"), encodePng(normalTexture(128)));
  writeFileSync(join(src, "pedra", "muro.gltf"), JSON.stringify(gridGltf(12).json));
  const tex = join(dir, "texturas.json");
  const mal = join(dir, "malhas.json");
  const ver = join(dir, "verificacao.json");
  const html = join(dir, "relatorio.html");
  node(["textures", src, "--saida", out, "--sem-ssimulacra2", "--relatorio", tex]);
  node(["meshes", src, "--saida", out, "--relatorio", mal]);
  const saida = node(["verify", src, "--saida", out, "--sem-ssimulacra2", "--relatorio", ver]);
  assert.match(saida, /malhas 1 de 1/);
  const v = JSON.parse(readFileSync(ver, "utf8"));
  assert.equal(v.falhas, 0);
  assert.ok(existsSync(join(out, "pedra", "muro.glb")));
  node(["report", tex, mal, ver, "--saida", html, "--titulo", "Teste"]);
  const pagina = readFileSync(html, "utf8");
  for (const trecho of ["Verificação N de N", "Texturas", "Malhas", "Como ler a régua"]) assert.ok(pagina.includes(trecho), trecho);
  // segunda execução: tudo do cache
  const t2 = JSON.parse((node(["textures", src, "--saida", out, "--sem-ssimulacra2", "--relatorio", tex]), readFileSync(tex, "utf8")));
  assert.ok(t2.resultados.every((r) => r.cache));
  // original intacto
  assert.ok(existsSync(join(src, "pedra", "muro_BC.png")));
});

test("comando desconhecido sai com código 2", () => {
  const r = spawnSync(process.execPath, [CLI, "nada"], { encoding: "utf8" });
  assert.equal(r.status, 2);
});
