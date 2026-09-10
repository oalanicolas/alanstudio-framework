// A ferramenta tem de nascer um look que o desenho já consome.
// Existir o script não prova isso — o teste corre o comando numa cópia.

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { cp, mkdtemp, readFile, rm } from "node:fs/promises";
import { once } from "node:events";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";

const STARTER = fileURLToPath(new URL("..", import.meta.url));

async function runLook(project, name, extra = []) {
  const child = spawn(process.execPath, ["tools/new-look.mjs", name, ...extra], {
    cwd: project,
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk) => {
    stdout += chunk;
  });
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });
  const [code] = await once(child, "exit");
  return { code, stdout, stderr };
}

test("o comando registra o look no mesmo consumidor", async () => {
  const base = await mkdtemp(join(tmpdir(), "starter-look-"));
  const project = join(base, "jogo");
  try {
    await cp(STARTER, project, { recursive: true, filter: (source) => !source.includes("/dist") });
    const missingFrom = await runLook(project, "dawn");
    assert.equal(missingFrom.code, 2);
    assert.match(missingFrom.stderr, /--from é obrigatório/);
    const created = await runLook(project, "dawn", ["--from", "dusk", "--as", "warmer"]);
    assert.equal(created.code, 0, created.stderr);
    assert.match(created.stdout, /\?look=dawn/);
    assert.match(created.stdout, /intenção warmer/);
    assert.doesNotMatch(created.stdout, /aprovado|verified|consistent/);
    const body = JSON.parse(await readFile(join(project, "data/palettes.json"), "utf8"));
    assert.ok(body.palettes.dawn);
    assert.notEqual(body.palettes.dawn.field, body.palettes.dusk.field);
    const { listLooks, resolveLookName, PALETTES } = await import(
      `${pathToFileURL(join(project, "src/game/tables.js")).href}?t=1`
    );
    assert.ok(listLooks().includes("dawn"));
    assert.equal(resolveLookName("dawn"), "dawn");
    assert.notEqual(PALETTES.dawn.field, PALETTES.dusk.field);
    assert.equal(PALETTES.normal.field, "#171b26");
    const again = await runLook(project, "dawn", ["--from", "dusk"]);
    assert.equal(again.code, 2);
    assert.match(again.stderr, /já existe look dawn/);
    const reserved = await runLook(project, "contrast", ["--from", "dusk"]);
    assert.equal(reserved.code, 2);
    const existing = await runLook(project, "normal", ["--from", "dusk"]);
    assert.equal(existing.code, 2);
    const calmReserved = await runLook(project, "calm", ["--from", "dusk"]);
    assert.equal(calmReserved.code, 2);
    assert.match(calmReserved.stderr, /já existe look calm/);
    const fromCalm = await runLook(project, "mist", ["--from", "calm"]);
    assert.equal(fromCalm.code, 0, fromCalm.stderr);
    const afterCalm = JSON.parse(await readFile(join(project, "data/palettes.json"), "utf8"));
    assert.equal(afterCalm.palettes.mist.field, afterCalm.palettes.calm.field);
    const invalid = await runLook(project, "Tempo-1", ["--from", "dusk"]);
    assert.equal(invalid.code, 2);
    const cloned = await runLook(project, "twin", ["--from", "dusk"]);
    assert.equal(cloned.code, 0, cloned.stderr);
    assert.match(cloned.stdout, /cópia de dusk/);
    const afterClone = JSON.parse(await readFile(join(project, "data/palettes.json"), "utf8"));
    assert.equal(afterClone.palettes.twin.field, afterClone.palettes.dusk.field);
    assert.ok(afterClone.palettes.dawn, "o look anterior permanece na mesa");
    const unknownAs = await runLook(project, "haze", ["--from", "dusk", "--as", "melhor"]);
    assert.equal(unknownAs.code, 2);
    assert.match(unknownAs.stderr, /intenção desconhecida/);
    const wrongFrom = await runLook(project, "words", ["--from", "contrast"]);
    assert.equal(wrongFrom.code, 2);
    assert.match(wrongFrom.stderr, /não é look de arte/);
    const inventada = await runLook(project, "words", ["--from", "inventada"]);
    assert.equal(inventada.code, 2);
    assert.match(inventada.stderr, /não é look de arte/);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
