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

async function runTable(project, name) {
  const child = spawn(process.execPath, ["tools/new-table.mjs", name], {
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
    const invalid = await runTable(project, "Tempo-1");
    assert.equal(invalid.code, 2);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
