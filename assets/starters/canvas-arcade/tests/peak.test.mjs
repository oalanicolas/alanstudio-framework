import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

test("o pico relata o arquivo sem importar limiar nem aprovar", async () => {
  const child = spawn(process.execPath, ["tools/peak.mjs"], {
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
  assert.ok(report.files.length >= 12);
  const dash = report.files.find((item) => item.file === "dash.wav");
  assert.ok(dash);
  assert.ok(Number.isFinite(dash.linear));
  assert.ok(dash.linear > 0);
  assert.match(report.scope, /Sem limiar/);
  assert.doesNotMatch(stdout, /LUFS|-14|aprovado|verified|4\.5/);
});
