import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

async function runSize(args = []) {
  const child = spawn(process.execPath, ["tools/size.mjs", ...args], {
    cwd: ROOT,
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stdout = "";
  child.stdout.on("data", (chunk) => {
    stdout += chunk;
  });
  const [code] = await once(child, "exit");
  return { code, stdout, report: JSON.parse(stdout) };
}

test("o tamanho relata bytes sem teto nem aprovação", async () => {
  const base = join(tmpdir(), `starter-size-${process.pid}`);
  await rm(base, { recursive: true, force: true });
  await mkdir(join(base, "nested"), { recursive: true });
  await writeFile(join(base, "a.txt"), "abcd");
  await writeFile(join(base, "nested", "b.txt"), "efghij");
  try {
    const { code, stdout, report } = await runSize(["--dir", base]);
    assert.equal(code, 0, stdout);
    assert.equal(report.present, true);
    assert.equal(report.files, 2);
    assert.equal(report.bytes, 10);
    assert.match(report.scope, /Sem teto/);
    assert.doesNotMatch(stdout, /aprovado|verified|LUFS|-14/);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});

test("pasta ausente é ausência, não zero aprovado", async () => {
  const missing = join(tmpdir(), `starter-size-missing-${process.pid}`);
  await rm(missing, { recursive: true, force: true });
  const { code, report } = await runSize(["--dir", missing]);
  assert.equal(code, 0);
  assert.equal(report.present, false);
  assert.equal(report.bytes, 0);
  assert.equal(report.files, 0);
});
