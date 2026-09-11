import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { applyKnobs, applyScale, applyShell, knobText, knobValues, KNOB_IDS, scaleVar, shellVars } from "../src/core/shell.js";
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

test("os knobs vestem o look, não o widget frio", () => {
  assert.match(html, /accent-color:\s*var\(--accent\)/);
  assert.match(html, /select\s*\{[\s\S]*background:\s*var\(--page\)/);
  assert.match(html, /select\s*\{[\s\S]*color:\s*var\(--ink\)/);
  assert.match(html, /select:focus-visible/);
  assert.match(html, /input:focus-visible/);
  assert.match(html, /textarea:focus-visible/);
  assert.equal(html.includes("accent-color: #4ea8ff"), false);
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

test("a faixa nomeia o valor que o knob já guarda", () => {
  assert.equal(knobText(0.75), "75%");
  assert.equal(knobText(1.5), "150%");
  assert.equal(knobText(0.7), "70%");
  assert.equal(knobText(Number.NaN), "");
  const values = knobValues({ gameSpeed: 0.75, uiScale: 1.5, buses: { master: 0.7, sfx: 0.62, music: 0.45, ui: 0.55 } });
  assert.equal(values.gameSpeed, 0.75);
  assert.equal(values.uiScale, 1.5);
  assert.equal(values.master, 0.7);
  assert.deepEqual(KNOB_IDS, ["gameSpeed", "uiScale", "master", "sfx", "music", "ui"]);

  const nodes = {};
  for (const name of KNOB_IDS) {
    nodes[name] = { value: "", attrs: {}, setAttribute(key, value) { this.attrs[key] = value; } };
    nodes[`${name}-readout`] = { textContent: "" };
  }
  const root = { getElementById(id) { return nodes[id] ?? null; } };
  assert.equal(applyKnobs(root, { gameSpeed: 0.75, uiScale: 1.5, buses: { master: 0.7, sfx: 0.4, music: 0.2, ui: 0 } }), true);
  assert.equal(nodes["gameSpeed-readout"].textContent, "75%");
  assert.equal(nodes.gameSpeed.value, "0.75");
  assert.equal(nodes.gameSpeed.attrs["aria-valuetext"], "75%");
  assert.equal(nodes["uiScale-readout"].textContent, "150%");
  assert.equal(nodes["master-readout"].textContent, "70%");
  assert.equal(nodes["ui-readout"].textContent, "0%");
  assert.equal(applyKnobs({}, { gameSpeed: 0.75 }), false);

  for (const name of KNOB_IDS) {
    assert.match(html, new RegExp(`id="${name}-readout"`));
    assert.match(html, new RegExp(`<output id="${name}-readout" for="${name}">`));
  }
  assert.match(html, /applyKnobs\(document, settings\)/);
  assert.match(html, /applyKnobs\(document, game\.settings\)/);
  assert.doesNotMatch(html, /verified|aprovado/);
});
