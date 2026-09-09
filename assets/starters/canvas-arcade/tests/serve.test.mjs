// O servidor local é a única forma de jogar: módulos ES não carregam por
// `file://`. Se ele não serve, o jogo não abre, por mais que a simulação passe.
//
// A pasta de teste tem espaço no nome de propósito. `new URL(...).pathname`
// devolve "Farol%20do%20Sul", uma pasta que não existe, e todo pedido responde
// 404 sem nenhum erro no console — a falha aparece só ao abrir o navegador.

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { cp, mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { once } from "node:events";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const STARTER = fileURLToPath(new URL("..", import.meta.url));

async function serveFrom(name) {
  const base = await mkdtemp(join(tmpdir(), "starter-serve-"));
  const project = join(base, name);
  await mkdir(join(project, "tools"), { recursive: true });
  await cp(join(STARTER, "tools/serve.mjs"), join(project, "tools/serve.mjs"));
  await cp(join(STARTER, "index.html"), join(project, "index.html"));
  await cp(join(STARTER, "src"), join(project, "src"), { recursive: true });
  await cp(join(STARTER, "data"), join(project, "data"), { recursive: true });
  await cp(join(STARTER, "public"), join(project, "public"), { recursive: true });
  const child = spawn(process.execPath, ["tools/serve.mjs"], {
    cwd: project,
    env: { ...process.env, PORT: "0" },
    stdio: ["ignore", "pipe", "pipe"],
  });
  const [chunk] = await once(child.stdout, "data");
  const port = Number(String(chunk).match(/:(\d+)\//)?.[1]);
  return {
    port,
    async stop() {
      child.kill("SIGKILL");
      await once(child, "exit");
      await rm(base, { recursive: true, force: true });
    },
  };
}

for (const name of ["farol", "Farol do Sul"]) {
  test(`o servidor entrega o jogo a partir de "${name}"`, async () => {
    const server = await serveFrom(name);
    try {
      assert.ok(Number.isInteger(server.port) && server.port > 0, "porta não anunciada");
      const root = await fetch(`http://localhost:${server.port}/`);
      assert.equal(root.status, 200, "a raiz precisa entregar o index.html");
      const html = await root.text();
      assert.match(html, /<canvas/, "a página servida não é o jogo");

      const module = await fetch(`http://localhost:${server.port}/src/main.js`);
      assert.equal(module.status, 200);
      assert.equal(module.headers.get("content-type"), "text/javascript; charset=utf-8");

      const spawn = await fetch(`http://localhost:${server.port}/data/spawn.json`);
      assert.equal(spawn.status, 200);
      assert.equal(spawn.headers.get("content-type"), "application/json; charset=utf-8");
      assert.ok(Number.isFinite((await spawn.json()).intervalTicks));

      const sound = await fetch(`http://localhost:${server.port}/public/sfx/dash.wav`);
      assert.equal(sound.status, 200);
      const bytes = Buffer.from(await sound.arrayBuffer());
      assert.equal(bytes.subarray(0, 4).toString("ascii"), "RIFF");

      const escape = await fetch(`http://localhost:${server.port}/../../etc/passwd`);
      assert.ok(escape.status === 403 || escape.status === 404, "caminho fora do projeto não pode vazar");
    } finally {
      await server.stop();
    }
  });
}
