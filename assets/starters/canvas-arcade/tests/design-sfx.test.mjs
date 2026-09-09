// A ferramenta tem de deslocar uma voz que o mixer já toca.
// Existir o script não prova isso — o teste corre o comando numa cópia.

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { cp, mkdtemp, readFile, rm } from "node:fs/promises";
import { once } from "node:events";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const STARTER = fileURLToPath(new URL("..", import.meta.url));

async function runSfx(project, extra = []) {
  const child = spawn("python3", ["tools/design-sfx.py", ...extra], {
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

test("o comando desloca um papel sem republicar o banco", async () => {
  const base = await mkdtemp(join(tmpdir(), "starter-sfx-"));
  const project = join(base, "jogo");
  try {
    await cp(STARTER, project, { recursive: true, filter: (source) => !source.includes("/dist") });
    const missingFrom = await runSfx(project, ["--as", "brighter"]);
    assert.equal(missingFrom.code, 2);
    assert.match(missingFrom.stderr, /--as precisa de --from/);

    const unknownAs = await runSfx(project, ["--from", "dash", "--as", "melhor"]);
    assert.equal(unknownAs.code, 2);
    assert.match(unknownAs.stderr, /intenção desconhecida/);

    const wrongFrom = await runSfx(project, ["--from", "inventada"]);
    assert.equal(wrongFrom.code, 2);
    assert.match(wrongFrom.stderr, /só --from de papel/);

    const beforeDash = await readFile(join(project, "public/sfx/dash.wav"));
    const beforeHit = await readFile(join(project, "public/sfx/hit.wav"));
    const created = await runSfx(project, ["--from", "dash", "--as", "brighter"]);
    assert.equal(created.code, 0, created.stderr);
    assert.match(created.stdout, /papel dash/);
    assert.match(created.stdout, /intenção brighter/);
    assert.doesNotMatch(created.stdout, /aprovado|verified|heard|LUFS|-14/);
    const afterDash = await readFile(join(project, "public/sfx/dash.wav"));
    const afterHit = await readFile(join(project, "public/sfx/hit.wav"));
    assert.notEqual(afterDash.equals(beforeDash), true, "brighter precisa deslocar a voz");
    assert.equal(afterHit.equals(beforeHit), true, "os outros papéis ficam onde estavam");

    const cloned = await runSfx(project, ["--from", "collect"]);
    assert.equal(cloned.code, 0, cloned.stderr);
    assert.match(cloned.stdout, /cópia de collect/);
    const sources = JSON.parse(await readFile(join(project, "public/sfx/sources.json"), "utf8"));
    const keys = sources.files.map((item) => item.key);
    assert.ok(keys.includes("dash"));
    assert.ok(keys.includes("hit"));
    assert.ok(keys.includes("collect"));
    const dashNote = sources.files.find((item) => item.key === "dash").note;
    assert.match(dashNote, /brighter/);
    assert.doesNotMatch(JSON.stringify(sources), /aprovado|verified|heard/);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
