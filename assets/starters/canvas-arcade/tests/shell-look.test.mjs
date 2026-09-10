import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { applyScale, applyShell, scaleVar, shellVars } from "../src/core/shell.js";
import { UI_SCALE_MAX, UI_SCALE_MIN } from "../src/core/settings.js";
import { applyLookIntent, PALETTES } from "../src/game/tables.js";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");

test("dusk veste a página; contraste vence; look novo também entra", () => {
  const dusk = shellVars(PALETTES.dusk);
  assert.equal(dusk["--page"], PALETTES.dusk.background);
  assert.equal(dusk["--surface"], PALETTES.dusk.field);
  assert.equal(dusk["--ink"], PALETTES.dusk.text);
  assert.equal(dusk["--accent"], PALETTES.dusk.orb);
  assert.notEqual(dusk["--page"], PALETTES.normal.background);

  const contrast = shellVars(PALETTES.contrast);
  assert.equal(contrast["--page"], PALETTES.contrast.background);
  assert.notEqual(contrast["--page"], dusk["--page"]);

  const painted = {};
  const target = { style: { setProperty(name, value) { painted[name] = value; } } };
  assert.equal(applyShell(target, PALETTES.dusk), true);
  assert.equal(painted["--page"], PALETTES.dusk.background);

  const dawn = applyLookIntent(PALETTES.dusk, "warmer");
  assert.equal(shellVars(dawn)["--page"], dawn.background);
  assert.equal(applyShell(target, PALETTES.calm), true);
  assert.equal(painted["--page"], PALETTES.calm.background);
  assert.notEqual(PALETTES.calm.background, PALETTES.dusk.background);
  assert.equal(applyShell({}, PALETTES.dusk), false);
  assert.equal(shellVars({ text: "x" }), null);
});

test("a página declara a casca por token, não um fundo frio à parte", () => {
  assert.match(html, /--page:/);
  assert.match(html, /background:\s*var\(--page\)/);
  assert.match(html, /var\(--accent\)/);
  assert.equal(html.includes("background: #0b0d13"), false);
  assert.match(html, /applyShell/);
});

test("a escala veste a casca, não só o canvas", () => {
  assert.equal(scaleVar(1.6)["--ui-scale"], "1.6");
  assert.equal(scaleVar(12)["--ui-scale"], String(UI_SCALE_MAX));
  assert.equal(scaleVar(0.1)["--ui-scale"], String(UI_SCALE_MIN));
  assert.equal(scaleVar(Number.NaN), null);

  const painted = {};
  const target = { style: { setProperty(name, value) { painted[name] = value; } } };
  assert.equal(applyScale(target, 1.6), true);
  assert.equal(painted["--ui-scale"], "1.6");
  assert.equal(applyScale({}, 1.6), false);
  assert.equal(applyScale(target, Number.NaN), false);

  assert.match(html, /--ui-scale:/);
  assert.match(html, /font-size:\s*calc\(16px \* var\(--ui-scale/);
  assert.match(html, /font:\s*calc\(15px \* var\(--ui-scale/);
  assert.equal(/font:\s*15px/.test(html), false);
  assert.match(html, /applyScale\(document\.documentElement, settings\.uiScale\)/);
  assert.match(html, /getElementById\("uiScale"\)\.addEventListener\("input"[\s\S]*dress\(\)/);
});
