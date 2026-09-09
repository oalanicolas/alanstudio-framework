// O passo de empacotar tem de produzir uma árvore que outra pessoa sirva.
// Existir `npm run build` não prova isso — o teste percorre o artefato.

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { cp, mkdtemp, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { once } from "node:events";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const STARTER = fileURLToPath(new URL("..", import.meta.url));

test("o export copia o jogo e deixa de fora o que só serve para desenvolver", async () => {
  const base = await mkdtemp(join(tmpdir(), "starter-export-"));
  const project = join(base, "jogo");
  try {
    await cp(STARTER, project, { recursive: true });
    const child = spawn(process.execPath, ["tools/export.mjs"], {
      cwd: project,
      stdio: ["ignore", "pipe", "pipe"],
    });
    const [code] = await once(child, "exit");
    assert.equal(code, 0, "export precisa terminar sem erro");
    const dist = join(project, "dist");
    assert.ok(existsSync(join(dist, "index.html")));
    assert.ok(existsSync(join(dist, "src/game/rules.js")));
    assert.ok(existsSync(join(dist, "data/spawn.json")));
    assert.ok(existsSync(join(dist, "tools/serve.mjs")));
    assert.ok(existsSync(join(dist, "package.json")));
    assert.equal(existsSync(join(dist, "tests")), false, "teste não embarca");
    assert.equal(existsSync(join(dist, "tools/budget.mjs")), false, "orçamento não embarca");
    assert.equal(existsSync(join(dist, "tools/export.mjs")), false, "o export não se copia");

    const server = spawn(process.execPath, ["tools/serve.mjs"], {
      cwd: dist,
      env: { ...process.env, PORT: "0" },
      stdio: ["ignore", "pipe", "pipe"],
    });
    const [chunk] = await once(server.stdout, "data");
    const port = Number(String(chunk).match(/:(\d+)\//)?.[1]);
    try {
      const page = await fetch(`http://localhost:${port}/`);
      assert.equal(page.status, 200);
      assert.match(await page.text(), /<canvas/);
      const table = await fetch(`http://localhost:${port}/data/spawn.json`);
      assert.equal(table.status, 200);
    } finally {
      server.kill("SIGKILL");
      await once(server, "exit");
    }
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
