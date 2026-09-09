import { test } from "node:test";
import assert from "node:assert/strict";

import { actionLabel, actionLabels, bindLines, keyLabel } from "../src/core/keys.js";
import { DEFAULT_BINDINGS, ONE_HAND_BINDINGS } from "../src/core/settings.js";
import { copy } from "../src/game/tables.js";

test("o código da tecla vira o rótulo que a tela mostra", () => {
  assert.equal(keyLabel("Space"), "Espaço");
  assert.equal(keyLabel("Escape"), "Esc");
  assert.equal(keyLabel("ArrowDown"), "↓");
  assert.equal(keyLabel("KeyK"), "K");
  assert.equal(keyLabel("Digit2"), "2");
});

test("o padrão preenche o aviso e o overlay com as teclas do manifesto", () => {
  const lines = bindLines(copy, DEFAULT_BINDINGS);
  assert.equal(lines.resume, "Continuar: Esc ou P");
  assert.equal(lines.restart, "Reiniciar: R");
  assert.equal(lines.hint_move, "←/→, arraste ou analógico");
  assert.equal(lines.hint_dash, "Atravesse o estilhaço (Espaço, cima ou A)");
  assert.equal(lines.hint_touch, copy.hint_touch);
  assert.equal(lines.hint_pad, copy.hint_pad);
  assert.equal(lines.hint_bank, "Guarde (↓, baixo ou X) antes de perder a corrente");
  assert.equal(actionLabel(DEFAULT_BINDINGS, "bank"), "↓");
  assert.deepEqual(actionLabels(DEFAULT_BINDINGS, "pause"), ["Esc", "P"]);
});

test("o preset de uma mão troca ↓ e R por K e O", () => {
  const lines = bindLines(copy, ONE_HAND_BINDINGS);
  assert.equal(lines.resume, "Continuar: P");
  assert.equal(lines.restart, "Reiniciar: O");
  assert.equal(lines.restart_inline, "reiniciar: O");
  assert.equal(lines.hint_move, "J/L, arraste ou analógico");
  assert.equal(lines.hint_dash, "Atravesse o estilhaço (I, cima ou A)");
  assert.equal(lines.hint_bank, "Guarde (K, baixo ou X) antes de perder a corrente");
  assert.equal(actionLabel(ONE_HAND_BINDINGS, "dash"), "I");
});

test("o controle preenche o overlay e o aviso continua ensinando as três superfícies", () => {
  const lines = bindLines(copy, DEFAULT_BINDINGS, "gamepad");
  assert.equal(lines.resume, "Continuar: Start");
  assert.equal(lines.restart, "Reiniciar: Select");
  assert.equal(lines.hint_move, "←/→, arraste ou analógico");
  assert.equal(lines.hint_dash, "Atravesse o estilhaço (Espaço, cima ou A)");
  assert.equal(lines.hint_pad, copy.hint_pad);
  assert.equal(lines.hint_bank, "Guarde (↓, baixo ou X) antes de perder a corrente");
  assert.equal(lines.hint_collect, copy.hint_collect);
});

test("o toque nomeia as faixas no overlay e deixa o aviso com as três superfícies", () => {
  const lines = bindLines(copy, DEFAULT_BINDINGS, "pointer");
  assert.equal(lines.hint_bank, "Guarde (↓, baixo ou X) antes de perder a corrente");
  assert.match(lines.hint_move, /arraste/);
  assert.equal(lines.resume, "Continuar: Esc ou P");
  assert.equal(lines.restart, "Reiniciar: R");
});

test("superfície desconhecida não inventa mapa", () => {
  const lines = bindLines(copy, DEFAULT_BINDINGS, "inventada");
  assert.equal(lines.resume, "Continuar: Esc ou P");
  assert.equal(lines.hint_bank, "Guarde (↓, baixo ou X) antes de perder a corrente");
});
