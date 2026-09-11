import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

test("o orçamento relata simulação e desenho sem aprovar quadro", async () => {
  const child = spawn(process.execPath, ["tools/budget.mjs", "--runs", "2", "--seed", "7"], {
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
  assert.equal(code, 0, stderr || stdout);
  const report = JSON.parse(stdout);
  assert.ok(Number.isFinite(report.simulation_ms.p99));
  assert.ok(Number.isFinite(report.presentation_ms.p99));
  assert.ok(report.presentation_ms.p99 > 0);
  assert.ok(Number.isFinite(report.entity_pool.created));
  assert.ok(report.entity_pool.acquired > report.entity_pool.created);
  assert.ok(Number.isFinite(report.event_pool.created));
  assert.ok(report.event_pool.acquired > report.event_pool.created);
  assert.ok(Number.isFinite(report.mote_pool.created));
  assert.ok(report.mote_pool.acquired > report.mote_pool.created);
  assert.equal(report.scene.name, "playing.run");
  assert.equal(report.scene.draw, "stub");
  assert.equal(report.scene.ticks, report.ticks_per_run);
  assert.ok(Array.isArray(report.scenes));
  const names = report.scenes.map((scene) => scene.name);
  assert.deepEqual(names, ["title.attract", "playing.run"]);
  const door = report.scenes.find((scene) => scene.name === "title.attract");
  assert.equal(door.ticks, 120);
  assert.equal(door.draw, "stub");
  assert.ok(Number.isFinite(door.simulation_ms.p99));
  assert.ok(door.presentation_ms.p99 > 0, "a porta precisa do draw");
  assert.equal(report.rng.created, 1);
  assert.ok(report.rng.reseeds > report.rng.created);
  assert.equal(report.measured, false);
  assert.match(report.scope, /canvas stub/);
  assert.match(report.scope, /Sem limiar de apresentação/);
  assert.match(report.scope, /playing.run/);
  assert.match(report.scope, /title\.attract/);
  assert.match(report.scope, /primeiro quadro/);
  assert.doesNotMatch(stdout, /aprovado|verified|16 ms|16ms/);
});
