// A ferramenta tem de nascer look e chuva com o mesmo nome.
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

async function runPair(project, name, extra = []) {
  const child = spawn(process.execPath, ["tools/new-pair.mjs", name, ...extra], {
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

test("o comando registra look e chuva com o mesmo nome", async () => {
  const base = await mkdtemp(join(tmpdir(), "starter-pair-"));
  const project = join(base, "jogo");
  try {
    await cp(STARTER, project, { recursive: true, filter: (source) => !source.includes("/dist") });
    const missingFrom = await runPair(project, "ember");
    assert.equal(missingFrom.code, 2);
    assert.match(missingFrom.stderr, /--from é obrigatório/);
    const created = await runPair(project, "ember", [
      "--from", "dusk",
      "--look", "warmer",
      "--spawn", "denser",
    ]);
    assert.equal(created.code, 0, created.stderr);
    assert.match(created.stdout, /\?look=ember/);
    assert.match(created.stdout, /\?spawn=ember/);
    assert.match(created.stdout, /\?mood=ember/);
    assert.doesNotMatch(created.stdout, /aprovado|verified|enough|consistent|outsider/);
    const body = JSON.parse(await readFile(join(project, "data/palettes.json"), "utf8"));
    assert.ok(body.palettes.ember);
    assert.notEqual(body.palettes.ember.field, body.palettes.dusk.field);
    assert.equal(body.palettes.ember.shard, body.palettes.dusk.shard, "o par warmer não devolve o estilhaço ao rosa");
    const rain = JSON.parse(await readFile(join(project, "data/ember.json"), "utf8"));
    const dusk = JSON.parse(await readFile(join(project, "data/dusk.json"), "utf8"));
    assert.ok(rain.intervalTicks < dusk.intervalTicks);
    const again = await runPair(project, "ember", ["--from", "dusk"]);
    assert.equal(again.code, 2);
    assert.match(again.stderr, /já existe/);
    const reserved = await runPair(project, "dusk", ["--from", "calm"]);
    assert.equal(reserved.code, 2);
    const fromSpawn = await runPair(project, "storm", ["--from", "spawn"]);
    assert.equal(fromSpawn.code, 2);
    assert.match(fromSpawn.stderr, /não é look e chuva/);
    const fromNormal = await runPair(project, "words", ["--from", "normal"]);
    assert.equal(fromNormal.code, 2);
    const unknownLook = await runPair(project, "haze", ["--from", "dusk", "--look", "melhor"]);
    assert.equal(unknownLook.code, 2);
    assert.match(unknownLook.stderr, /intenção de look desconhecida/);
    const unknownSpawn = await runPair(project, "haze", ["--from", "dusk", "--spawn", "melhor"]);
    assert.equal(unknownSpawn.code, 2);
    assert.match(unknownSpawn.stderr, /intenção de chuva desconhecida/);
    const fromCalm = await runPair(project, "mist", ["--from", "calm"]);
    assert.equal(fromCalm.code, 0, fromCalm.stderr);
    assert.match(fromCalm.stdout, /\?mood=mist/);
    const afterCalm = JSON.parse(await readFile(join(project, "data/palettes.json"), "utf8"));
    assert.ok(afterCalm.palettes.mist);
    assert.ok(afterCalm.palettes.ember, "o par anterior permanece na mesa");
    const { listLooks, listMoods, listSpawnProfiles, pairPatch, loadSpawn } = await import(
      `${pathToFileURL(join(project, "src/game/tables.js")).href}?t=1`
    );
    assert.ok(listLooks().includes("ember"));
    assert.ok(listLooks().includes("mist"));
    assert.ok(listSpawnProfiles().includes("ember"));
    assert.ok(listSpawnProfiles().includes("mist"));
    assert.ok(listMoods().includes("ember"));
    assert.ok(listMoods().includes("mist"));
    assert.deepEqual(pairPatch("ember"), { look: "ember", spawnProfile: "ember" });
    assert.ok(loadSpawn("ember").intervalTicks < loadSpawn("dusk").intervalTicks);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
