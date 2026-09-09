import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

test("a sessão simulada grava candidato sem chamar isso de observada", async () => {
  const folder = await mkdtemp(join(tmpdir(), "starter-session-"));
  const out = join(folder, "last-run.json");
  try {
    const child = spawn(process.execPath, ["tools/session.mjs", "--seed", "7", "--out", out], {
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
    assert.equal(code, 0, stderr);
    const report = JSON.parse(stdout);
    assert.equal(report.observed, false);
    assert.equal(report.felt, false);
    assert.equal(report.policy, "nearest-orb");
    assert.ok(Number.isFinite(report.run.ticks));
    assert.ok(report.run.ticks > 0);
    assert.match(report.scope, /não é causa/);
    assert.doesNotMatch(stdout, /aprovado|verified|LUFS|-14|4\.5/);
    const saved = JSON.parse(await readFile(out, "utf8"));
    assert.deepEqual(saved.run, report.run);
    assert.equal(saved.observed, false);
  } finally {
    await rm(folder, { recursive: true, force: true });
  }
});
