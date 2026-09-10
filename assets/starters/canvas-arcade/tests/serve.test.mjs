// O servidor local é a única forma de jogar: módulos ES não carregam por
// `file://`. Se ele não serve, o jogo não abre, por mais que a simulação passe.
//
// A pasta de teste tem espaço no nome de propósito. `new URL(...).pathname`
// devolve "Farol%20do%20Sul", uma pasta que não existe, e todo pedido responde
// 404 sem nenhum erro no console — a falha aparece só ao abrir o navegador.

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { cp, mkdtemp, mkdir, readFile, writeFile, rm } from "node:fs/promises";
import { once } from "node:events";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { advertisedOrigins, isArtifactRoot, LAST_RUN_FILE, LAST_RUN_ROUTE, listenBanner, listenHost, shouldOpenBrowser } from "../tools/serve.mjs";

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
  const banner = String(chunk);
  const port = Number(banner.match(/:(\d+)\//)?.[1]);
  return {
    port,
    project,
    banner,
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
      assert.match(server.banner, /\?look=dusk/, "o serve precisa apontar o look denso");
      assert.match(server.banner, /\?look=calm/, "o serve precisa apontar o look calmo");
      assert.match(server.banner, /\?spawn=dusk/, "o serve precisa apontar a chuva densa");
      assert.match(server.banner, /\?spawn=calm/, "o serve precisa apontar a chuva calma");
      assert.match(server.banner, /\?mood=calm/, "o serve precisa apontar o par calmo");
      assert.match(server.banner, /\?mood=dusk/, "o serve precisa apontar o par denso");
      assert.match(server.banner, /\?invite=1/, "o serve precisa apontar o convite");
      const root = await fetch(`http://localhost:${server.port}/`);
      assert.equal(root.status, 200, "a raiz precisa entregar o index.html");
      const html = await root.text();
      assert.match(html, /<canvas/, "a página servida não é o jogo");
      assert.match(html, /id="commands"/, "a tabela precisa ter id para o convite somir");
      assert.match(html, /get\("invite"\) === "1"/, "a página precisa declarar o gancho do convite");

      const module = await fetch(`http://localhost:${server.port}/src/main.js`);
      assert.equal(module.status, 200);
      assert.equal(module.headers.get("content-type"), "text/javascript; charset=utf-8");

      const spawn = await fetch(`http://localhost:${server.port}/data/spawn.json`);
      assert.equal(spawn.status, 200);
      assert.equal(spawn.headers.get("content-type"), "application/json; charset=utf-8");
      assert.ok(Number.isFinite((await spawn.json()).intervalTicks));
      const dusk = await fetch(`http://localhost:${server.port}/data/dusk.json`);
      assert.equal(dusk.status, 200);
      assert.equal((await dusk.json()).intervalTicks, 16);
      const calm = await fetch(`http://localhost:${server.port}/data/calm.json`);
      assert.equal(calm.status, 200);
      assert.equal((await calm.json()).intervalTicks, 30);

      const sound = await fetch(`http://localhost:${server.port}/public/sfx/dash.wav`);
      assert.equal(sound.status, 200);
      const bytes = Buffer.from(await sound.arrayBuffer());
      assert.equal(bytes.subarray(0, 4).toString("ascii"), "RIFF");

      const escape = await fetch(`http://localhost:${server.port}/../../etc/passwd`);
      assert.ok(escape.status === 403 || escape.status === 404, "caminho fora do projeto não pode vazar");

      const posted = await fetch(`http://localhost:${server.port}${LAST_RUN_ROUTE}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          observed: true,
          felt: true,
          policy: "nearest-orb",
          run: { ticks: 40, score: 3, seed: 8, chain: 1 },
          seed: 8,
          spawn: "dusk",
          curve: { never_banked: false, unbanked_at_end: 1 },
        }),
      });
      assert.equal(posted.status, 204, posted.status);
      const saved = JSON.parse(await readFile(join(server.project, LAST_RUN_FILE), "utf8"));
      assert.equal(saved.observed, false);
      assert.equal(saved.felt, false);
      assert.equal(saved.policy, "played");
      assert.equal(saved.run.ticks, 40);
      assert.equal(saved.spawn, "dusk");
      assert.doesNotMatch(JSON.stringify(saved), /aprovado|verified|LUFS|-14|4\.5/);

      const refused = await fetch(`http://localhost:${server.port}/docs/playtest/last-run.json`, {
        method: "POST",
        body: "{}",
      });
      assert.equal(refused.status, 405);
    } finally {
      await server.stop();
    }
  });
}

test("o serve só tenta abrir o navegador no terminal", () => {
  assert.equal(shouldOpenBrowser({ CI: "true" }, { isTTY: true }), false);
  assert.equal(shouldOpenBrowser({ BROWSER: "0" }, { isTTY: true }), false);
  assert.equal(shouldOpenBrowser({}, { isTTY: false }), false);
  assert.equal(shouldOpenBrowser({}, { isTTY: true }), true);
});

test("o serve anuncia a rede sem fingir que alguém de fora jogou", () => {
  const interfaces = {
    lo: [{ address: "127.0.0.1", family: "IPv4", internal: true }],
    wlan0: [
      { address: "192.168.1.40", family: "IPv4", internal: false },
      { address: "fe80::1", family: "IPv6", internal: false },
      { address: "169.254.1.2", family: "IPv4", internal: false },
    ],
  };
  assert.deepEqual(advertisedOrigins(8080, interfaces, {}), [
    "http://localhost:8080",
    "http://192.168.1.40:8080",
  ]);
  assert.deepEqual(advertisedOrigins(8080, interfaces, { HOST: "127.0.0.1" }), [
    "http://localhost:8080",
  ]);
  assert.equal(listenHost({ HOST: "localhost" }), "127.0.0.1");
  assert.equal(listenHost({}), undefined);
  const banner = listenBanner(8080, interfaces, {});
  assert.match(banner, /Par: http:\/\/localhost:8080\/\?mood=calm  http:\/\/localhost:8080\/\?mood=dusk/);
  assert.match(banner, /Convite: http:\/\/localhost:8080\/\?invite=1/);
  assert.match(banner, /Candidato: a partida grava docs\/playtest\/last-run\.json/);
  assert.match(banner, /Rede: http:\/\/192\.168\.1\.40:8080\//);
  assert.match(banner, /Convite na rede: http:\/\/192\.168\.1\.40:8080\/\?invite=1/);
  assert.doesNotMatch(banner, /169\.254/);
  assert.doesNotMatch(banner, /outsider|aprovado|verified|alguém de fora jogou/i);
  const local = listenBanner(8080, { lo: [{ address: "127.0.0.1", family: "IPv4", internal: true }] }, {});
  assert.doesNotMatch(local, /Rede:/);
  assert.doesNotMatch(local, /Árvore exportada/);
});

test("o serve da árvore exportada nomeia o artefato sem fingir outra máquina", async () => {
  const base = await mkdtemp(join(tmpdir(), "starter-artifact-banner-"));
  try {
    await writeFile(join(base, "VERSION.json"), "{}\n");
    assert.equal(isArtifactRoot(base), true);
    assert.equal(isArtifactRoot(STARTER), false);
    const banner = listenBanner(8080, {}, {}, base);
    assert.match(banner, /Árvore exportada/);
    assert.match(banner, /não é outra máquina/);
    assert.doesNotMatch(banner, /aprovado|verified|shipped/);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
