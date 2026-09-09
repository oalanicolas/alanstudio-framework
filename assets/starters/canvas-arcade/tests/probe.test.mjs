import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

test("a sonda conta o buffer sem chamar isso de peso", async () => {
  const child = spawn(process.execPath, ["tools/probe.mjs"], {
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
  assert.equal(report.felt, false);
  assert.ok(report.late_requests > 0);
  assert.ok(report.buffered_fires > 0);
  assert.match(report.scope, /não peso percebido/);
  assert.doesNotMatch(stdout, /aprovado|verified|93%/);
});
