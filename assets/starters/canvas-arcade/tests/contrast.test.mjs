import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

test("o contraste relata pares hex sem importar limiar nem aprovar", async () => {
  const child = spawn(process.execPath, ["tools/contrast.mjs"], {
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
  assert.ok(report.pairs.normal && report.pairs.contrast);
  const text = report.pairs.normal.find((item) => item.foreground === "text");
  assert.ok(Number.isFinite(text.ratio));
  assert.ok(text.ratio > 1, "texto e campo não podem ser a mesma luminância");
  assert.match(report.scope, /Sem limiar/);
  assert.doesNotMatch(stdout, /4\.5\s*:\s*1|WCAG|aprovado|verified/);
});
