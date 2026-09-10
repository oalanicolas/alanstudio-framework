// O passo de empacotar tem de produzir uma árvore que outra pessoa sirva.
// Existir `npm run build` não prova isso — o teste percorre o artefato.

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { cp, mkdtemp, readFile, rm } from "node:fs/promises";
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
    assert.ok(existsSync(join(dist, "data/dusk.json")));
    assert.ok(existsSync(join(dist, "data/calm.json")), "o artefato leva a chuva calma");
    assert.ok(existsSync(join(dist, "data/palettes.json")), "o artefato leva a paleta");
    assert.ok(existsSync(join(dist, "public/sfx/dash.wav")), "o artefato leva o som");
    assert.ok(existsSync(join(dist, "public/sfx/close.wav")), "o artefato leva o tap do fecho");
    assert.ok(existsSync(join(dist, "public/sfx/dash-b.wav")), "o artefato leva a variante");
    assert.ok(existsSync(join(dist, "tools/serve.mjs")));
    assert.ok(existsSync(join(dist, "package.json")));
    const exported = JSON.parse(await readFile(join(dist, "package.json"), "utf8"));
    assert.equal(exported.engines.node, ">=20");
    assert.equal(exported.scripts.serve, "node tools/serve.mjs");
    const readme = await readFile(join(dist, "README.md"), "utf8");
    assert.match(readme, /Node 20/);
    assert.match(readme, /Não rode `npm install`/);
    assert.match(readme, /file:\/\//);
    assert.match(readme, /endereço\s+IPv4/);
    assert.match(readme, /não é outra máquina/);
    const version = JSON.parse(await readFile(join(dist, "VERSION.json"), "utf8"));
    assert.equal(version.version, "0.1.0");
    assert.match(version.scope, /Não prova/);
    assert.equal(existsSync(join(dist, "tests")), false, "teste não embarca");
    assert.equal(existsSync(join(dist, "tools/budget.mjs")), false, "orçamento não embarca");
    assert.equal(existsSync(join(dist, "tools/mix.mjs")), false, "mix de medição não embarca");
    assert.equal(existsSync(join(dist, "tools/size.mjs")), false, "tamanho não embarca");
    assert.equal(existsSync(join(dist, "tools/session.mjs")), false, "sessão simulada não embarca");
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
