import { test } from "node:test";
import assert from "node:assert/strict";

import { coachHint } from "../src/game/coach.js";
import { createState, PLAYER_Y } from "../src/game/rules.js";

const shardOnRail = () => ({ id: 1, kind: "shard", x: 160, y: PLAYER_Y - 22, vy: 0 });
const orbOnRail = () => ({ id: 2, kind: "orb", x: 160, y: PLAYER_Y - 22, vy: 0 });

test("os primeiros ticks pedem movimento, não a tabela da página", () => {
  const state = createState(1);
  assert.equal(coachHint(state), "move");
});

test("com fantasia na mesa o primeiro aviso é a frase, não o movimento", () => {
  const state = createState(1);
  assert.equal(coachHint(state, { fantasy: "guardar a corrente" }), "fantasy");
  state.tick = 48;
  assert.equal(coachHint(state, { fantasy: "guardar a corrente" }), "move");
});

test("fantasia vazia não toma o lugar do movimento", () => {
  assert.equal(coachHint(createState(1), { fantasy: "   " }), "move");
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

test("estilhaço no trilho pede o dash antes do orbe", () => {
  const state = createState(1);
  state.tick = 90;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state), "dash");
  state.stats.dashes = 1;
  assert.equal(coachHint(state), "collect", "depois do avanço o aviso não insiste no dash");
});

test("orbe no trilho não finge ameaça", () => {
  const state = createState(1);
  state.tick = 90;
  state.entities = [orbOnRail()];
  assert.equal(coachHint(state), "collect");
});

test("toque e controle ganham passo depois do movimento", () => {
  const state = createState(1);
  state.tick = 70;
  assert.equal(coachHint(state, {}, { surface: "pointer" }), "touch");
  assert.equal(coachHint(state, {}, { surface: "gamepad" }), "pad");
  assert.equal(coachHint(state, {}, { surface: "keyboard" }), "collect");
  state.tick = 50;
  assert.equal(coachHint(state, {}, { surface: "pointer" }), "move", "o movimento ainda vem primeiro");
  state.tick = 120;
  assert.equal(coachHint(state, {}, { surface: "gamepad" }), "collect", "o passo da superfície some");
});

test("estilhaço no trilho vence o passo da superfície", () => {
  const state = createState(1);
  state.tick = 70;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state, {}, { surface: "pointer" }), "dash");
});

test("orbe perdido nomeia o custo enquanto a corrente é zero", () => {
  const state = createState(1);
  state.tick = 90;
  state.stats.missed = 1;
  assert.equal(coachHint(state), "miss");
  state.chain = 1;
  assert.equal(coachHint(state), "collect");
  state.chain = 3;
  assert.equal(coachHint(state), "bank");
  state.stats.banks = 1;
  assert.equal(coachHint(state), null);
});

test("estilhaço no trilho vence a queda", () => {
  const state = createState(1);
  state.tick = 90;
  state.stats.missed = 1;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state), "dash");
});
