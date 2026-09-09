#!/usr/bin/env node
// Relata luminância relativa dos pares da paleta e dos pixels depois do
// draw() numa cena montada. Não importa limiar, não aprova contraste e não
// substitui sessão com o modo ativo. `verified` no harness continua falso.

import { PALETTES, createRenderer } from "../src/game/render.js";
import { createState, CONFIG, PLAYER_Y } from "../src/game/rules.js";
import { createRasterCanvas, parseColor } from "./raster.mjs";

function channel(value) {
  const linear = value / 255;
  return linear <= 0.04045 ? linear / 12.92 : ((linear + 0.055) / 1.055) ** 2.4;
}

function hexRgb(value) {
  return parseColor(value);
}

function luminanceOf(color) {
  if (!color) return null;
  return 0.2126 * channel(color.r) + 0.7152 * channel(color.g) + 0.0722 * channel(color.b);
}

function ratio(a, b) {
  const left = typeof a === "string" ? luminanceOf(hexRgb(a)) : luminanceOf(a);
  const right = typeof b === "string" ? luminanceOf(hexRgb(b)) : luminanceOf(b);
  if (left === null || right === null) return null;
  const hi = Math.max(left, right);
  const lo = Math.min(left, right);
  return (hi + 0.05) / (lo + 0.05);
}

const PAIRS = [
  ["text", "field"],
  ["player", "field"],
  ["orb", "field"],
  ["shard", "field"],
  ["chain", "field"],
  ["danger", "field"],
];

function tokenPairs(palette) {
  return PAIRS.map(([fg, bg]) => {
    const value = ratio(palette[fg], palette[bg]);
    return {
      foreground: fg,
      background: bg,
      ratio: value === null ? null : Number(value.toFixed(2)),
      skipped: value === null ? "não é hex opaco" : undefined,
    };
  });
}

const FIELD_CENTER = 160;

function sceneState() {
  const state = createState(3);
  state.score = 24;
  state.chain = 3;
  state.player.x = FIELD_CENTER;
  state.entities = [
    { id: 1, kind: "orb", x: 72, y: 88, vy: 0 },
    { id: 2, kind: "shard", x: 248, y: 70, vy: 0 },
    { id: 3, kind: "orb", x: 72, y: PLAYER_Y - 24, vy: 0 },
  ];
  return state;
}

const SAMPLE_POINTS = [
  ["field", FIELD_CENTER, 90],
  ["player", FIELD_CENTER, PLAYER_Y],
  ["orb", 72, 88],
  ["shard", 248, 70],
  ["plate", 5, 8],
  ["plate_edge", 3, 8],
  ["hud_text", 10, 7],
];

function drawScene(settings, extra = {}) {
  const canvas = createRasterCanvas(320, 180);
  const renderer = createRenderer(canvas, { devicePixelRatio: 1 });
  renderer.resize(320, 180);
  const state = extra.state ?? sceneState();
  if (extra.flash) state.flash = CONFIG.feel.flashHit;
  renderer.draw(
    state,
    { paused: false, alpha: 0, steps: 1 },
    settings,
    { captions: extra.captions ?? [{ text: "orbe", count: 1 }], best: 18, hint: "bank" },
  );
  return canvas;
}

function sampleScene(name, settings, extra = {}) {
  const canvas = drawScene(settings, extra);
  const samples = {};
  for (const [id, x, y] of SAMPLE_POINTS) {
    samples[id] = canvas.sample(x, y);
  }
  const pairs = [
    ["player", "field"],
    ["orb", "field"],
    ["shard", "field"],
    ["hud_text", "plate"],
    ["plate", "field"],
    ["plate_edge", "field"],
  ].map(([fg, bg]) => {
    const value = ratio(samples[fg], samples[bg]);
    return {
      foreground: fg,
      background: bg,
      ratio: value === null ? null : Number(value.toFixed(2)),
    };
  });
  return { name, settings, samples, pairs };
}

const tokens = {};
for (const [name, palette] of Object.entries(PALETTES)) {
  tokens[name] = tokenPairs(palette);
}

const scenes = [
  sampleScene("playing.normal", {}),
  sampleScene("playing.contrast", { highContrast: true }),
  sampleScene("playing.flash", {}, { flash: true }),
];

console.log(JSON.stringify({
  pairs: tokens,
  scenes,
  scope:
    "Pares hex e pixels do stub após draw() numa cena montada. " +
    "fillText é retângulo da cor, não glifo. Sem limiar, sem aprovação, " +
    "sem dispositivo, sem movimento contínuo.",
}, null, 2));
