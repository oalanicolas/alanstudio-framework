import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { createRasterCanvas } from "../tools/raster.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

test("o raster compõe a placa sobre o campo, não o token isolado", () => {
  const canvas = createRasterCanvas(8, 8);
  const context = canvas.getContext("2d");
  context.fillStyle = "#171b26";
  context.fillRect(0, 0, 8, 8);
  context.fillStyle = "rgba(7,9,13,0.86)";
  context.fillRect(0, 0, 8, 8);
  const pixel = canvas.sample(2, 2);
  assert.ok(pixel.r < 20 && pixel.g < 20);
  assert.notEqual(pixel.r, 23, "o campo cru não sobreviveu à composição");
});

test("o contraste relata pares hex sem importar limiar nem aprovar", async () => {
  const child = spawn(process.execPath, ["tools/contrast.mjs"], {
    cwd: ROOT,
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stdout = "";
  child.stdout.on("data", (chunk) => {
    stdout += chunk;
  });
  const [code] = await once(child, "exit");
  assert.equal(code, 0, stdout);
  const report = JSON.parse(stdout);
  assert.ok(report.pairs.normal && report.pairs.contrast);
  const text = report.pairs.normal.find((item) => item.foreground === "text");
  assert.ok(Number.isFinite(text.ratio));
  assert.ok(text.ratio > 1, "texto e campo não podem ser a mesma luminância");
  assert.ok(Array.isArray(report.scenes));
  const names = report.scenes.map((scene) => scene.name);
  assert.deepEqual(names, ["playing.normal", "playing.contrast", "playing.flash"]);
  const contrast = report.scenes.find((scene) => scene.name === "playing.contrast");
  const plate = contrast.pairs.find((item) => item.foreground === "plate" && item.background === "field");
  const edge = contrast.pairs.find((item) => item.foreground === "plate_edge" && item.background === "field");
  assert.ok(Number.isFinite(plate.ratio));
  assert.ok(Number.isFinite(edge.ratio));
  assert.notEqual(
    plate.ratio,
    edge.ratio,
    "preenchimento e borda da placa são pixels distintos na cena",
  );
  const flash = report.scenes.find((scene) => scene.name === "playing.flash");
  const tokenOrb = report.pairs.normal.find((item) => item.foreground === "orb").ratio;
  const flashOrb = flash.pairs.find((item) => item.foreground === "orb" && item.background === "field").ratio;
  assert.notEqual(flashOrb, tokenOrb, "o flash muda o par orbe/campo; o token hex não vê isso");
  assert.match(report.scope, /Sem limiar/);
  assert.match(report.scope, /cena montada/);
  assert.match(report.scope, /mesma tinta/);
  assert.equal(report.shapes.measured, false);
  assert.equal(report.shapes.same_ink, "#9a9a9a");
  assert.ok(report.shapes.orb_ink > 0);
  assert.ok(report.shapes.shard_ink > 0);
  assert.ok(report.shapes.only_orb > 0, "o círculo precisa pintar pixels que o losango não pinta");
  assert.ok(report.shapes.only_shard > 0, "o losango precisa pintar pixels que o círculo não pinta");
  assert.equal(report.shapes.masks_differ, true);
  assert.doesNotMatch(stdout, /4\.5\s*:\s*1|WCAG|aprovado|verified/);
});

test("a barra de accessibility não atribui medição no dispositivo ao contrast", async () => {
  const readme = await readFile(join(ROOT, "README.md"), "utf8");
  const row = readme.split("\n").find((line) => line.startsWith("| `accessibility`"));
  assert.ok(row, "a tabela precisa nomear accessibility");
  assert.match(row, /stub/);
  assert.match(row, /ainda não foi observado/);
  assert.doesNotMatch(row, /verificado por medição em cena no dispositivo/);
});
