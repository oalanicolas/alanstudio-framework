// Arquivo em public/sfx sem consumidor no mixer era lacuna invisível:
// `roles` via o .wav e o jogo seguia só com legenda.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { createAudio, SOUNDS } from "../src/game/audio.js";
import { loadRoleFiles } from "../src/game/sfx.js";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

test("carrega o arquivo do papel e o registra no mixer", async () => {
  const audio = createAudio({ createContext: () => null });
  const fetchFn = async (url) => {
    if (url !== "public/sfx/dash.wav") return { ok: false };
    return { ok: true, arrayBuffer: async () => new ArrayBuffer(8) };
  };
  const loaded = await loadRoleFiles(audio, {
    fetch: fetchFn,
    decode: async () => ({ duration: 0.2 }),
  });
  assert.deepEqual(loaded, [{ id: "dash", url: "public/sfx/dash.wav", variant: false }]);
  const gaps = audio.missing();
  assert.deepEqual(gaps.registered, ["dash"]);
  assert.ok(gaps.declared.includes("hit"));
});

test("os seis papéis têm WAV original no disco, não um stub", async () => {
  for (const id of Object.keys(SOUNDS)) {
    for (const stem of [id, `${id}-b`]) {
      const bytes = await readFile(join(ROOT, "public/sfx", `${stem}.wav`));
      assert.equal(bytes.subarray(0, 4).toString("ascii"), "RIFF", stem);
      assert.ok(bytes.length > 1000, `${stem} curto demais para ser design`);
      const credits = await readFile(join(ROOT, "public/sfx", `${stem}.credits.txt`), "utf8");
      assert.match(credits, /CC0-1.0/);
      assert.match(credits, /design-sfx/);
    }
  }
});

test("a variante entra no mesmo papel, não como papel novo", async () => {
  const audio = createAudio({ createContext: () => null });
  const seen = [];
  const fetchFn = async (url) => {
    seen.push(url);
    if (url === "public/sfx/dash.wav" || url === "public/sfx/dash-b.wav") {
      return { ok: true, arrayBuffer: async () => new ArrayBuffer(8) };
    }
    return { ok: false };
  };
  const loaded = await loadRoleFiles(audio, {
    fetch: fetchFn,
    decode: async () => ({ duration: 0.2 }),
  });
  assert.deepEqual(
    loaded.filter((item) => item.id === "dash"),
    [
      { id: "dash", url: "public/sfx/dash.wav", variant: false },
      { id: "dash", url: "public/sfx/dash-b.wav", variant: true },
    ],
  );
  assert.ok(seen.includes("public/sfx/dash-b.wav"));
});

test("404 não inventa buffer e não quebra o restante dos papéis", async () => {
  const audio = createAudio({ createContext: () => null });
  const loaded = await loadRoleFiles(audio, {
    fetch: async () => ({ ok: false }),
    decode: async () => ({ duration: 0.2 }),
  });
  assert.deepEqual(loaded, []);
  assert.deepEqual(audio.missing().registered, []);
  assert.deepEqual(audio.missing().declared, Object.keys(SOUNDS));
});
