// O servidor local é a única forma de jogar: módulos ES não carregam por
// `file://`. Se ele não serve, o jogo não abre, por mais que a simulação passe.
//
// A pasta de teste tem espaço no nome de propósito. `new URL(...).pathname`
// devolve "Farol%20do%20Sul", uma pasta que não existe, e todo pedido responde
// 404 sem nenhum erro no console — a falha aparece só ao abrir o navegador.

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { cp, mkdtemp, mkdir, writeFile, rm, symlink } from "node:fs/promises";
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
  const child = spawn(process.execPath, ["tools/serve.mjs"], {
    cwd: project,
    env: { ...process.env, PORT: "0" },
    stdio: ["ignore", "pipe", "pipe"],
  });
  const [chunk] = await once(child.stdout, "data");
  const port = Number(String(chunk).match(/:(\d+)\//)?.[1]);
  return {
    port, base, project,
    async stop() {
      if (child.exitCode === null && child.signalCode === null) {
        const stopped = once(child, "exit");
        child.kill("SIGKILL");
        await stopped;
      }
      await rm(base, { recursive: true, force: true });
    },
  };
}

test("links para arquivos e pastas externos não saem pelo servidor", async () => {
  const server = await serveFrom("jogo");
  try {
    const external = join(server.base, "externo");
    await mkdir(external);
    await writeFile(join(external, "privado.txt"), "fixture fora do projeto");
    await symlink(join(external, "privado.txt"), join(server.project, "arquivo.txt"));
    await symlink(external, join(server.project, "pasta"), "dir");
    for (const path of ["/arquivo.txt", "/pasta/privado.txt"]) {
      for (const method of ["GET", "HEAD"]) {
        const response = await fetch(`http://localhost:${server.port}${path}`, { method });
        assert.equal(response.status, 403, `${method} ${path}`);
        assert.doesNotMatch(await response.text(), /fixture fora do projeto/);
      }
    }
  } finally {
    await server.stop();
  }
});

test("links internos continuam servindo recursos do próprio projeto", async () => {
  const server = await serveFrom("jogo");
  try {
    await symlink(join(server.project, "index.html"), join(server.project, "interno.html"));
    const response = await fetch(`http://localhost:${server.port}/interno.html`);
    assert.equal(response.status, 200);
    assert.match(await response.text(), /<canvas/);
  } finally {
    await server.stop();
  }
});

test("URLs inválidas recebem 400 e o servidor continua respondendo", async () => {
  const server = await serveFrom("jogo");
  try {
    for (const path of ["/broken%ZZ", "/%E0%A4%A", "/%00"]) {
      const invalid = await fetch(`http://localhost:${server.port}${path}`);
      assert.equal(invalid.status, 400, path);
      await invalid.text();
      const healthy = await fetch(`http://localhost:${server.port}/`);
      assert.equal(healthy.status, 200, "o pedido anterior não pode encerrar o processo");
      await healthy.text();
    }
  } finally {
    await server.stop();
  }
});

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

      const escape = await fetch(`http://localhost:${server.port}/../../etc/passwd`);
      assert.ok(escape.status === 403 || escape.status === 404, "caminho fora do projeto não pode vazar");
    } finally {
      await server.stop();
    }
  });
}
