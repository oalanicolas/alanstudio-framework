import { test } from "node:test";
import assert from "node:assert/strict";

import { coachHint } from "../src/game/coach.js";
import { createState } from "../src/game/rules.js";

test("os primeiros ticks pedem movimento, não a tabela da página", () => {
  const state = createState(1);
  assert.equal(coachHint(state), "move");
});

test("sem corrente o aviso pede o orbe", () => {
  const state = createState(1);
  state.tick = 90;
  assert.equal(coachHint(state), "collect");
});

test("corrente que já vale mais pede guardar", () => {
  const state = createState(1);
  state.tick = 200;
  state.chain = 3;
  assert.equal(coachHint(state), "bank");
});

test("depois da primeira guarda o ensino some", () => {
  const state = createState(1);
  state.tick = 400;
  state.chain = 4;
  state.stats.banks = 1;
  assert.equal(coachHint(state), null);
});

test("partida encerrada não ensina", () => {
  const state = createState(1);
  state.phase = "over";
  assert.equal(coachHint(state), null);
});
