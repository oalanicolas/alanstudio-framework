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
  assert.match(report.scope, /canvas stub/);
  assert.match(report.scope, /Sem limiar de apresentação/);
  assert.doesNotMatch(stdout, /aprovado|verified|16 ms|16ms/);
});
