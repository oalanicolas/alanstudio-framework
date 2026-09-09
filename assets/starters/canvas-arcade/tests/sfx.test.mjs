// Arquivo em public/sfx sem consumidor no mixer era lacuna invisível:
// `roles` via o .wav e o jogo seguia só com legenda.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createAudio, SOUNDS } from "../src/game/audio.js";
import { loadRoleFiles } from "../src/game/sfx.js";

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
  assert.deepEqual(loaded, [{ id: "dash", url: "public/sfx/dash.wav" }]);
  const gaps = audio.missing();
  assert.deepEqual(gaps.registered, ["dash"]);
  assert.ok(gaps.declared.includes("hit"));
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
