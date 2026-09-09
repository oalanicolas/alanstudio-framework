#!/usr/bin/env node
// Relata luminância relativa dos pares da paleta. Não importa limiar,
// não aprova contraste e não substitui sessão com o modo ativo.
// `verified` no harness continua falso.

import { PALETTES } from "../src/game/render.js";

function channel(value) {
  const linear = value / 255;
  return linear <= 0.04045 ? linear / 12.92 : ((linear + 0.055) / 1.055) ** 2.4;
}

function hexRgb(value) {
  const match = /^#([0-9a-f]{6})$/i.exec(String(value).trim());
  if (!match) return null;
  const n = Number.parseInt(match[1], 16);
  return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
}

function luminance(hex) {
  const rgb = hexRgb(hex);
  if (!rgb) return null;
  return 0.2126 * channel(rgb.r) + 0.7152 * channel(rgb.g) + 0.0722 * channel(rgb.b);
}

function ratio(a, b) {
  const left = luminance(a);
  const right = luminance(b);
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

const report = {};
for (const [name, palette] of Object.entries(PALETTES)) {
  report[name] = PAIRS.map(([fg, bg]) => {
    const value = ratio(palette[fg], palette[bg]);
    return {
      foreground: fg,
      background: bg,
      ratio: value === null ? null : Number(value.toFixed(2)),
      skipped: value === null ? "não é hex opaco" : undefined,
    };
  });
}

console.log(JSON.stringify({
  pairs: report,
  scope: "Luminância relativa sRGB dos tokens hex. Sem limiar, sem aprovação, sem cena em movimento.",
}, null, 2));
