import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { applyShell, shellVars } from "../src/core/shell.js";
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
