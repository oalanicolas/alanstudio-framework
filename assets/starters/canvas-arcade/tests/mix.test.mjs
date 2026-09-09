import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

test("o mix relata a soma da partida sem importar limiar nem aprovar", async () => {
  const child = spawn(process.execPath, ["tools/mix.mjs", "--runs", "1", "--seed", "7"], {
    cwd: ROOT,
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stdout = "";
  child.stdout.on("data", (chunk) => {
    stdout += chunk;
  });
  const [code] = await once(child, "exit");
  assert.equal(code, 0, stdout);
  const report = JSON.parse(stdout);
  assert.equal(report.heard, false);
  assert.equal(report.bed, true);
  assert.ok(report.events > 0);
  assert.ok(Number.isFinite(report.peak_linear));
  assert.ok(report.peak_linear > 0);
  assert.match(report.scope, /partida simulada/);
  assert.doesNotMatch(stdout, /LUFS|-14|aprovado|verified|4\.5/);
});
