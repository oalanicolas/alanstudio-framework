import { test } from "node:test";
import assert from "node:assert/strict";

import { coachHint, FANTASY_TICKS, MOVE_TICKS } from "../src/game/coach.js";
import { CONFIG, createState, PLAYER_Y } from "../src/game/rules.js";

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

test("a fantasia na porta não come o aviso de mover", () => {
  const state = createState(1, { entry: "title" });
  const lines = { fantasy: "guardar a corrente ou continuar" };
  assert.equal(coachHint(state, lines), "fantasy");
  state.attractTick = FANTASY_TICKS - 1;
  assert.equal(coachHint(state, lines), "fantasy");
  state.attractTick = FANTASY_TICKS;
  assert.equal(coachHint(state, lines), "move", "depois da frase a porta ainda ensina a abrir");
  state.attractTick = FANTASY_TICKS + MOVE_TICKS - 1;
  assert.equal(coachHint(state, lines), "move");
  state.attractTick = FANTASY_TICKS + MOVE_TICKS;
  assert.equal(coachHint(state, lines), null);
  const plain = createState(2, { entry: "title" });
  plain.attractTick = MOVE_TICKS - 1;
  assert.equal(coachHint(plain), "move", "sem frase o aviso de mover continua o mesmo");
  plain.attractTick = MOVE_TICKS;
  assert.equal(coachHint(plain), null);
});

test("a abertura ensina mover sem abrir o ciclo", () => {
  const state = createState(1, { entry: "title" });
  assert.equal(coachHint(state), "move");
  assert.equal(coachHint(state, { fantasy: "guardar a corrente ou continuar" }), "fantasy");
  state.attractTick = FANTASY_TICKS;
  assert.equal(coachHint(state, { fantasy: "guardar a corrente ou continuar" }), "move");
  state.attractTick = FANTASY_TICKS + MOVE_TICKS - 1;
  assert.equal(coachHint(state, { fantasy: "guardar a corrente ou continuar" }), "move");
  state.attractTick = FANTASY_TICKS + MOVE_TICKS;
  assert.equal(coachHint(state, { fantasy: "guardar a corrente ou continuar" }), null);
  state.chain = 3;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state), null, "a porta não pede guardar");
  assert.equal(coachHint(state, {}, { surface: "pointer" }), null, "a porta não ensina toque");
  assert.equal(coachHint(state, {}, { surface: "gamepad" }), null, "a mostra no trilho não ensina dash na porta");
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

test("o estilhaço nomeia o custo enquanto a corrente voltou a zero", () => {
  const state = createState(1);
  state.tick = 90;
  state.stats.hits = 1;
  assert.equal(coachHint(state), "hit");
  state.stats.missed = 1;
  assert.equal(coachHint(state), "hit", "o estilhaço vence a queda");
  state.chain = 1;
  assert.equal(coachHint(state), "collect");
  state.chain = 3;
  assert.equal(coachHint(state), "bank");
  state.stats.banks = 1;
  assert.equal(coachHint(state), null);
});

test("estilhaço no trilho vence o custo do hit", () => {
  const state = createState(1);
  state.tick = 90;
  state.stats.hits = 1;
  state.entities = [shardOnRail()];
  assert.equal(coachHint(state), "dash");
});

test("a porta não ensina o custo do estilhaço", () => {
  const state = createState(1, { entry: "title" });
  state.attractTick = 90;
  state.stats.hits = 1;
  assert.equal(coachHint(state), null);
  assert.equal(coachHint(state, {}, { surface: "pointer" }), null, "a porta não ensina toque no hit");
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

test("o fecho pede guardar a corrente viva sem fingir sessão observada", () => {
  const mid = createState(1);
  mid.tick = 1800;
  mid.chain = 4;
  mid.stats.banks = 1;
  assert.equal(coachHint(mid), null, "no meio a primeira guarda encerra o ensino");

  const close = createState(1);
  close.tick = CONFIG.runTicks - 300;
  close.chain = 4;
  close.stats.banks = 1;
  assert.equal(coachHint(close), "bank");
  assert.equal(coachHint(close, {}, { surface: "pointer" }), "bank", "o fecho não reabre o toque");
  assert.equal(coachHint(close, {}, { surface: "gamepad" }), "bank", "o fecho não reabre o controle");

  const empty = createState(1);
  empty.tick = CONFIG.runTicks - 300;
  empty.chain = 0;
  empty.stats.banks = 1;
  assert.equal(coachHint(empty), null);
  assert.equal(coachHint(empty, {}, { surface: "pointer" }), null, "sem corrente o fecho não ensina toque");

  const ended = createState(1);
  ended.phase = "over";
  ended.tick = CONFIG.runTicks;
  ended.chain = 4;
  ended.stats.banks = 1;
  assert.equal(coachHint(ended), null);
});
