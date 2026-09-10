import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

async function runSession(args) {
  const child = spawn(process.execPath, ["tools/session.mjs", ...args], {
    cwd: ROOT,
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

test("a sessão simulada grava candidato sem chamar isso de observada", async () => {
  const folder = await mkdtemp(join(tmpdir(), "starter-session-"));
  const out = join(folder, "last-run.json");
  try {
    const { code, stdout, stderr } = await runSession(["--seed", "7", "--out", out]);
    assert.equal(code, 0, stderr);
    const report = JSON.parse(stdout);
    assert.equal(report.schema, 2);
    assert.equal(report.spawn, "spawn");
    assert.equal(report.observed, false);
    assert.equal(report.felt, false);
    assert.equal(report.policy, "nearest-orb");
    assert.ok(Number.isFinite(report.run.ticks));
    assert.ok(report.run.ticks > 0);
    assert.equal(report.curve.never_banked, report.run.banks === 0);
    assert.equal(report.curve.never_hit, report.run.hits === 0);
    assert.equal(report.curve.first_bank_tick === null, report.curve.never_banked);
    assert.equal(report.curve.first_hit_tick === null, report.curve.never_hit);
    assert.equal(report.curve.first_collect_tick === null, report.run.collected === 0);
    assert.equal(report.curve.unbanked_at_end, report.run.chain);
    if (report.run.hits > 0) assert.ok(report.curve.longest_hit_streak >= 1);
    if (report.run.missed > 0) assert.ok(report.curve.longest_miss_streak >= 1);
    assert.match(report.scope, /não é causa/);
    assert.doesNotMatch(stdout, /aprovado|verified|LUFS|-14|4\.5/);
    const saved = JSON.parse(await readFile(out, "utf8"));
    assert.deepEqual(saved.run, report.run);
    assert.deepEqual(saved.curve, report.curve);
    assert.equal(saved.observed, false);
    assert.equal(saved.spawn, "spawn");
  } finally {
    await rm(folder, { recursive: true, force: true });
  }
});

test("a sessão não apaga a partida jogada sem chamar isso de observada", async () => {
  const folder = await mkdtemp(join(tmpdir(), "starter-session-played-"));
  const out = join(folder, "last-run.json");
  try {
    await writeFile(out, `${JSON.stringify({
      schema: 2,
      seed: 8,
      policy: "played",
      run: { seed: 8, score: 3, ticks: 40 },
      observed: false,
      felt: false,
    }, null, 2)}\n`);
    const blocked = await runSession(["--seed", "7", "--out", out]);
    assert.equal(blocked.code, 3, blocked.stderr);
    assert.match(blocked.stderr, /partida jogada/);
    const kept = JSON.parse(await readFile(out, "utf8"));
    assert.equal(kept.policy, "played");
    assert.equal(kept.seed, 8);
    const forced = await runSession(["--seed", "7", "--out", out, "--force"]);
    assert.equal(forced.code, 0, forced.stderr);
    const report = JSON.parse(forced.stdout);
    assert.equal(report.policy, "nearest-orb");
    assert.equal(report.observed, false);
    assert.doesNotMatch(forced.stdout, /aprovado|verified|LUFS|-14|4\.5/);
  } finally {
    await rm(folder, { recursive: true, force: true });
  }
});

test("a sessão traça o perfil pedido e recusa chuva que não existe", async () => {
  const folder = await mkdtemp(join(tmpdir(), "starter-session-dusk-"));
  const spawnOut = join(folder, "spawn.json");
  const duskOut = join(folder, "dusk.json");
  try {
    const spawnRun = await runSession(["--seed", "7", "--out", spawnOut]);
    const duskRun = await runSession(["--seed", "7", "--spawn", "dusk", "--out", duskOut]);
    assert.equal(spawnRun.code, 0, spawnRun.stderr);
    assert.equal(duskRun.code, 0, duskRun.stderr);
    const spawnReport = JSON.parse(spawnRun.stdout);
    const duskReport = JSON.parse(duskRun.stdout);
    assert.equal(duskReport.spawn, "dusk");
    assert.equal(duskReport.observed, false);
    assert.notDeepEqual(duskReport.run, spawnReport.run);
    const missing = await runSession(["--spawn", "inventada", "--out", join(folder, "no.json")]);
    assert.equal(missing.code, 2);
    assert.match(missing.stderr, /perfil de chuva desconhecido/);
  } finally {
    await rm(folder, { recursive: true, force: true });
  }
});
