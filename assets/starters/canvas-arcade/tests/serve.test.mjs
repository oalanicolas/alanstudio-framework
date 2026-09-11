// O servidor local é a única forma de jogar: módulos ES não carregam por
// `file://`. Se ele não serve, o jogo não abre, por mais que a simulação passe.
//
// A pasta de teste tem espaço no nome de propósito. `new URL(...).pathname`
// devolve "Farol%20do%20Sul", uma pasta que não existe, e todo pedido responde
// 404 sem nenhum erro no console — a falha aparece só ao abrir o navegador.

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { cp, mkdtemp, mkdir, readFile, readdir, writeFile, rm, symlink } from "node:fs/promises";
import { once } from "node:events";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { advertisedOrigins, FINDING_ROUTE, inviteQuery, isArtifactRoot, LAST_RUN_FILE, LAST_RUN_ROUTE, lastRunLook, lastRunSeed, lastRunSpawn, lastRunSpeed, NOTE_DIR, NOTE_ROUTE, listenBanner, listenHost, seedQuery, shouldOpenBrowser } from "../tools/serve.mjs";

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
    base,
    project,
    banner,
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

      const noted = await fetch(`http://localhost:${server.port}${NOTE_ROUTE}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ note: "o dash atravessou", author: "" }),
      });
      assert.equal(noted.status, 204, noted.status);
      const folders = await readdir(join(server.project, NOTE_DIR));
      const receipt = folders.find((name) => name !== "last-run.json");
      assert.ok(receipt, "esperava a pasta do recibo");
      const record = JSON.parse(await readFile(join(server.project, NOTE_DIR, receipt, "record.json"), "utf8"));
      assert.equal(record.kind, "observation");
      assert.equal(record.author, "página");
      assert.equal(record.felt, false);
      assert.equal(record.observed, false);
      assert.match(record.fields.run, /"ticks":40/);
      assert.doesNotMatch(JSON.stringify(record), /aprovado|verified|LUFS|-14|4\.5/);

      const empty = await fetch(`http://localhost:${server.port}${NOTE_ROUTE}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ note: "  " }),
      });
      assert.equal(empty.status, 400);

      const found = await fetch(`http://localhost:${server.port}${FINDING_ROUTE}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          problema: "o dash não comunica o contato",
          evidencia: "três sessões, pergunta se atravessou",
          hipotese: "o hitstop some no movimento",
          medicao: "repetir o graze com hitstop 5 e 2",
        }),
      });
      assert.equal(found.status, 204, found.status);
      const files = await readdir(join(server.project, NOTE_DIR));
      const achado = files.find((name) => name.endsWith("-achado.md"));
      assert.ok(achado, "esperava o markdown do achado");
      const finding = await readFile(join(server.project, NOTE_DIR, achado), "utf8");
      assert.match(finding, /Problema: o dash não comunica o contato/);
      assert.doesNotMatch(finding, /aprovado|verified|LUFS|-14|4\.5|outsider/);
      const companion = files.find((name) => name.endsWith("-achado.run.json"));
      assert.ok(companion, "esperava o anexo do candidato");
      const attached = JSON.parse(await readFile(join(server.project, NOTE_DIR, companion), "utf8"));
      assert.equal(attached.kind, "finding-attachment");
      assert.equal(attached.observed, false);
      assert.equal(attached.felt, false);
      assert.equal(attached.outsider, false);
      assert.equal(attached.run.ticks, 40);
      assert.equal(attached.finding, achado);
      assert.doesNotMatch(JSON.stringify(attached), /aprovado|verified|LUFS|-14|4\.5/);
      const hollow = await fetch(`http://localhost:${server.port}${FINDING_ROUTE}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ problema: "o dash", evidencia: "", hipotese: "x", medicao: "y" }),
      });
      assert.equal(hollow.status, 400);

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
  assert.match(banner, /Relógio: http:\/\/localhost:8080\/\?speed=0\.75/);
  assert.match(banner, /Convite: http:\/\/localhost:8080\/\?invite=1/);
  assert.match(banner, /Seed: http:\/\/localhost:8080\/\?seed=7/);
  assert.match(banner, /Candidato: a partida grava docs\/playtest\/last-run\.json/);
  assert.match(banner, /Nota: depois do fim a página grava o recibo/);
  assert.match(banner, /Achado: no convite a página grava os quatro nomes e anexa o candidato/);
  assert.match(banner, /Rede: http:\/\/192\.168\.1\.40:8080\//);
  assert.match(banner, /Convite na rede: http:\/\/192\.168\.1\.40:8080\/\?invite=1/);
  assert.doesNotMatch(banner, /169\.254/);
  assert.doesNotMatch(banner, /outsider|aprovado|verified|alguém de fora jogou/i);
  const local = listenBanner(8080, { lo: [{ address: "127.0.0.1", family: "IPv4", internal: true }] }, {});
  assert.doesNotMatch(local, /Rede:/);
  assert.doesNotMatch(local, /Árvore exportada/);
});

test("o banner do serve nomeia o relógio que o jogo já lê", () => {
  const banner = listenBanner(8080, { lo: [{ address: "127.0.0.1", family: "IPv4", internal: true }] }, {});
  assert.match(banner, /Relógio: http:\/\/localhost:8080\/\?speed=0\.75/);
  assert.match(banner, /Par: http:\/\/localhost:8080\/\?mood=calm/);
  const relogio = banner.indexOf("Relógio:");
  const convite = banner.indexOf("Convite:");
  assert.ok(relogio >= 0 && convite > relogio);
  assert.doesNotMatch(banner, /aprovado|verified|LUFS|-14|4\.5/);
});

test("o serve junta convite e seed do last-run sem fingir quem jogou", async () => {
  const base = await mkdtemp(join(tmpdir(), "starter-invite-seed-"));
  try {
    assert.equal(lastRunSeed(base), null);
    assert.equal(inviteQuery(null), "/?invite=1");
    await mkdir(join(base, "docs/playtest"), { recursive: true });
    await writeFile(join(base, LAST_RUN_FILE), JSON.stringify({
      schema: 2,
      seed: 8,
      run: { ticks: 40, score: 3, seed: 8 },
      observed: false,
      felt: false,
    }));
    assert.equal(lastRunSeed(base), 8);
    assert.equal(lastRunSpawn(base), null);
    assert.equal(inviteQuery(8), "/?invite=1&seed=8");
    assert.equal(inviteQuery(8, "dusk"), "/?invite=1&seed=8&spawn=dusk");
    assert.equal(inviteQuery(8, "dusk", "dusk"), "/?invite=1&seed=8&spawn=dusk&look=dusk");
    assert.equal(inviteQuery(8, "dusk", "dusk", 0.75), "/?invite=1&seed=8&spawn=dusk&look=dusk&speed=0.75");
    assert.equal(seedQuery(null), null);
    assert.equal(seedQuery(8), "/?seed=8");
    assert.equal(seedQuery(8, "dusk"), "/?seed=8&spawn=dusk");
    assert.equal(seedQuery(8, "dusk", "dusk"), "/?seed=8&spawn=dusk&look=dusk");
    assert.equal(seedQuery(8, "dusk", "dusk", 0.75), "/?seed=8&spawn=dusk&look=dusk&speed=0.75");
    assert.equal(lastRunLook(base), null);
    const banner = listenBanner(8080, {
      wlan0: [{ address: "192.168.1.40", family: "IPv4", internal: false }],
    }, {}, base);
    assert.match(banner, /Convite: http:\/\/localhost:8080\/\?invite=1&seed=8/);
    assert.match(banner, /Seed: http:\/\/localhost:8080\/\?seed=8/);
    assert.match(banner, /Convite na rede: http:\/\/192\.168\.1\.40:8080\/\?invite=1&seed=8/);
    assert.doesNotMatch(banner, /\?seed=7/);
    assert.doesNotMatch(banner, /outsider|aprovado|verified/);
    await writeFile(join(base, LAST_RUN_FILE), JSON.stringify({
      schema: 2,
      seed: 8,
      spawn: "dusk",
      run: { ticks: 40, score: 3, seed: 8 },
    }));
    assert.equal(lastRunSpawn(base), "dusk");
    const dusk = listenBanner(8080, {
      wlan0: [{ address: "192.168.1.40", family: "IPv4", internal: false }],
    }, {}, base);
    assert.match(dusk, /Convite: http:\/\/localhost:8080\/\?invite=1&seed=8&spawn=dusk/);
    assert.match(dusk, /Seed: http:\/\/localhost:8080\/\?seed=8&spawn=dusk/);
    assert.match(dusk, /Convite na rede: http:\/\/192\.168\.1\.40:8080\/\?invite=1&seed=8&spawn=dusk/);
    assert.doesNotMatch(dusk, /outsider|aprovado|verified/);
    await writeFile(join(base, LAST_RUN_FILE), JSON.stringify({
      schema: 2,
      seed: 8,
      spawn: "dusk",
      look: "dusk",
      run: { ticks: 40, score: 3, seed: 8 },
    }));
    assert.equal(lastRunLook(base), "dusk");
    const painted = listenBanner(8080, {
      wlan0: [{ address: "192.168.1.40", family: "IPv4", internal: false }],
    }, {}, base);
    assert.match(painted, /Convite: http:\/\/localhost:8080\/\?invite=1&seed=8&spawn=dusk&look=dusk/);
    assert.match(painted, /Seed: http:\/\/localhost:8080\/\?seed=8&spawn=dusk&look=dusk/);
    assert.match(painted, /Convite na rede: http:\/\/192\.168\.1\.40:8080\/\?invite=1&seed=8&spawn=dusk&look=dusk/);
    assert.doesNotMatch(painted, /outsider|aprovado|verified/);
    await writeFile(join(base, LAST_RUN_FILE), JSON.stringify({
      schema: 2,
      seed: 8,
      spawn: "dusk",
      look: "dusk",
      speed: 0.75,
      run: { ticks: 40, score: 3, seed: 8, speed: 0.75 },
    }));
    assert.equal(lastRunSpeed(base), 0.75);
    const clocked = listenBanner(8080, {
      wlan0: [{ address: "192.168.1.40", family: "IPv4", internal: false }],
    }, {}, base);
    assert.match(clocked, /Convite: http:\/\/localhost:8080\/\?invite=1&seed=8&spawn=dusk&look=dusk&speed=0\.75/);
    assert.match(clocked, /Seed: http:\/\/localhost:8080\/\?seed=8&spawn=dusk&look=dusk&speed=0\.75/);
    assert.doesNotMatch(clocked, /outsider|aprovado|verified/);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
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
