import { test } from "node:test";
import assert from "node:assert/strict";

import { actionLabel, actionLabels, bindLines, commandRows, keyLabel, paintCommands } from "../src/core/keys.js";
import { applyRebind } from "../src/core/remap.js";
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
  assert.equal(lines.title_play, "Jogar: Espaço");
  assert.equal(lines.title_again, "Repetir a última: Espaço");
  assert.equal(lines.title_new, "Nova partida: R");
  assert.equal(lines.over_door, "Abertura: Espaço");
  assert.equal(lines.over_door_inline, "abertura: Espaço");
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
  assert.equal(lines.hint_miss, copy.hint_miss);
  assert.equal(lines.hint_hit, copy.hint_hit);
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

test("a tabela nomeia as teclas vivas e mantém toque e controle", () => {
  const rows = commandRows(DEFAULT_BINDINGS);
  assert.equal(rows.length, 5);
  assert.match(rows[1].text, /Espaço, K/);
  assert.match(rows[1].text, /botão A/);
  assert.match(rows[1].text, /toque na área superior/);
  const rebound = commandRows(applyRebind(DEFAULT_BINDINGS, "dash", "KeyZ"));
  assert.match(rebound[1].text, /^Z,/);
  assert.equal(rebound[1].text.includes("Espaço"), false);
  const one = commandRows(ONE_HAND_BINDINGS);
  assert.match(one[0].text, /^J \/ L,/);
  assert.match(one[2].text, /^K,/);
  assert.match(one[2].text, /botão X/);
});

test("pintar a tabela troca o texto sem inventar sessão", () => {
  const cells = {};
  const host = {
    querySelector(selector) {
      const action = /data-command="([^"]+)"/.exec(selector)?.[1];
      if (!action) return null;
      cells[action] ??= { textContent: "padrão" };
      return cells[action];
    },
  };
  paintCommands(host, applyRebind(DEFAULT_BINDINGS, "pause", "KeyQ"));
  assert.match(cells.pause.textContent, /^Q ou Start/);
  assert.match(cells.dash.textContent, /Espaço, K/);
  paintCommands(null, DEFAULT_BINDINGS);
});
