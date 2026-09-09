// A ferramenta tem de nascer uma mesa que o carregador já resolve.
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

async function runTable(project, name, extra = []) {
  const child = spawn(process.execPath, ["tools/new-table.mjs", name, ...extra], {
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

test("o comando registra a mesa no mesmo carregador", async () => {
  const base = await mkdtemp(join(tmpdir(), "starter-table-"));
  const project = join(base, "jogo");
  try {
    await cp(STARTER, project, { recursive: true, filter: (source) => !source.includes("/dist") });
    const created = await runTable(project, "timing");
    assert.equal(created.code, 0, created.stderr);
    assert.match(created.stdout, /loadTable\("timing"\)/);
    const body = await readFile(join(project, "data/timing.json"), "utf8");
    assert.equal(body, "{\n  \"schema\": 1\n}\n");
    const { loadTable, TABLES } = await import(`${pathToFileURL(join(project, "src/game/tables.js")).href}?t=1`);
    assert.equal(loadTable("timing").schema, 1);
    assert.ok("timing" in TABLES);
    assert.equal(loadTable("spawn").intervalTicks, 22);
    const again = await runTable(project, "timing");
    assert.equal(again.code, 2);
    assert.match(again.stderr, /já existe/);
    const reserved = await runTable(project, "spawn");
    assert.equal(reserved.code, 2);
    const duskReserved = await runTable(project, "dusk");
    assert.equal(duskReserved.code, 2);
    const invalid = await runTable(project, "Tempo-1");
    assert.equal(invalid.code, 2);
    const copied = await runTable(project, "storm", ["--from", "spawn"]);
    assert.equal(copied.code, 0, copied.stderr);
    assert.match(copied.stdout, /\?spawn=storm/);
    assert.match(copied.stdout, /session -- --spawn storm/);
    const { loadSpawn, listSpawnProfiles } = await import(`${pathToFileURL(join(project, "src/game/tables.js")).href}?t=2`);
    assert.equal(loadSpawn("storm").intervalTicks, 22);
    assert.ok(listSpawnProfiles().includes("storm"));
    const fromDusk = await runTable(project, "night", ["--from", "dusk"]);
    assert.equal(fromDusk.code, 0, fromDusk.stderr);
    const { loadSpawn: loadAfterDusk } = await import(`${pathToFileURL(join(project, "src/game/tables.js")).href}?t=3`);
    assert.equal(loadAfterDusk("night").intervalTicks, 16);
    const shifted = await runTable(project, "gale", ["--from", "spawn", "--as", "denser"]);
    assert.equal(shifted.code, 0, shifted.stderr);
    assert.match(shifted.stdout, /intenção denser/);
    const { loadSpawn: loadGale } = await import(`${pathToFileURL(join(project, "src/game/tables.js")).href}?t=4`);
    assert.ok(loadGale("gale").intervalTicks < loadGale("spawn").intervalTicks);
    assert.ok(loadGale("gale").practiceTicks < loadGale("spawn").practiceTicks);
    const noFrom = await runTable(project, "mist", ["--as", "denser"]);
    assert.equal(noFrom.code, 2);
    assert.match(noFrom.stderr, /--as precisa de --from/);
    const unknownAs = await runTable(project, "haze", ["--from", "spawn", "--as", "melhor"]);
    assert.equal(unknownAs.code, 2);
    assert.match(unknownAs.stderr, /intenção desconhecida/);
    const wrongFrom = await runTable(project, "words", ["--from", "copy"]);
    assert.equal(wrongFrom.code, 2);
    assert.match(wrongFrom.stderr, /só --from de chuva/);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
