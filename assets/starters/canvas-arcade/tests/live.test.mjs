import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { applyLive, liveText } from "../src/core/live.js";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");
const main = readFileSync(new URL("../src/main.js", import.meta.url), "utf8");

test("liveText junta fase, perigo e a última legenda sem repetir", () => {
  assert.equal(liveText({}), "");
  assert.equal(liveText({ phase: "title" }), "abertura");
  assert.equal(liveText({ phase: "title", threat: "ahead" }), "abertura. perigo à frente");
  assert.equal(liveText({ phase: "over" }), "fim da partida");
  assert.equal(liveText({ phase: "playing", threat: "ahead" }), "perigo à frente");
  assert.equal(
    liveText({
      phase: "over",
      captions: [{ text: "fim da partida" }],
    }),
    "fim da partida",
  );
  assert.equal(
    liveText({
      phase: "playing",
      threat: "ahead",
      captions: [{ text: "o avanço senta" }],
    }),
    "perigo à frente. o avanço senta",
  );
  assert.equal(/orbe|guarda|estilhaço/i.test(liveText({
    phase: "playing",
    threat: "ahead",
  })), false);
});

test("a pausa entra na região viva sem fingir sessão", () => {
  assert.equal(liveText({ paused: true }), "pausado");
  assert.equal(
    liveText({ phase: "playing", threat: "ahead", paused: true }),
    "pausado. perigo à frente",
  );
  assert.equal(
    liveText({ phase: "over", paused: true }),
    "pausado. fim da partida",
  );
  assert.equal(liveText({ phase: "playing", paused: false }), "");
  assert.match(main, /paused:\s*loop\.paused/);
  assert.doesNotMatch(liveText({ paused: true }), /aprovado|verified|alguém de fora/);
});

test("applyLive só escreve quando o texto muda", () => {
  const node = { textContent: "" };
  assert.equal(applyLive({}), false);
  assert.equal(applyLive({ node, text: "perigo à frente" }), true);
  assert.equal(node.textContent, "perigo à frente");
  assert.equal(applyLive({ node, text: "perigo à frente" }), false);
  assert.equal(applyLive({ node, text: "fim da partida" }), true);
  assert.equal(node.textContent, "fim da partida");
});

test("a página declara a região viva sem fingir sessão", () => {
  assert.match(html, /id="live"/);
  assert.match(html, /aria-live="polite"/);
  assert.match(html, /sr-only/);
  assert.match(main, /getElementById\("live"\)/);
  assert.match(main, /threatCue/);
  assert.match(main, /applyLive/);
  assert.doesNotMatch(html, /outsider|aprovado|verified|alguém de fora/);
});
