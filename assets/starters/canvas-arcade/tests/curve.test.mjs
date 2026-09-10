import { test } from "node:test";
import assert from "node:assert/strict";

import { createTrace, emptyCurve, finishCurve, reportCurve, traceEvents } from "../src/game/curve.js";
import { summarizeRun } from "../src/core/save.js";
import { advance, createState, CONFIG, PLAYER_Y } from "../src/game/rules.js";

test("a curva vazia não inventa primeiro evento nem sequência", () => {
  assert.deepEqual(emptyCurve(), {
    first_collect_tick: null,
    first_bank_tick: null,
    first_hit_tick: null,
    never_banked: true,
    never_hit: true,
    longest_hit_streak: 0,
    longest_miss_streak: 0,
    unbanked_at_end: 0,
  });
});

test("o relatório omite o contador corrente da sequência", () => {
  const trace = createTrace();
  traceEvents(trace, [{ type: "hit" }], 12);
  const reported = reportCurve(trace);
  assert.equal(reported.longest_hit_streak, 1);
  assert.equal("hitStreak" in reported, false);
  assert.equal("missStreak" in reported, false);
});

test("o primeiro collect, bank e hit gravam o tick uma vez", () => {
  const trace = createTrace();
  traceEvents(trace, [{ type: "collect" }], 8);
  traceEvents(trace, [{ type: "collect" }], 11);
  traceEvents(trace, [{ type: "bank" }], 14);
  traceEvents(trace, [{ type: "bank" }], 20);
  traceEvents(trace, [{ type: "hit" }], 30);
  traceEvents(trace, [{ type: "hit" }], 40);
  assert.equal(trace.curve.first_collect_tick, 8);
  assert.equal(trace.curve.first_bank_tick, 14);
  assert.equal(trace.curve.first_hit_tick, 30);
  assert.equal(trace.curve.never_banked, false);
  assert.equal(trace.curve.never_hit, false);
});

test("never_banked permanece fato quando ninguém guarda", () => {
  const trace = createTrace();
  traceEvents(trace, [{ type: "collect" }, { type: "missed" }, { type: "hit" }], 90);
  assert.equal(trace.curve.never_banked, true);
  assert.equal(trace.curve.first_bank_tick, null);
  assert.equal(trace.curve.never_hit, false);
});

test("hit seguidos alongam a sequência; collect e graze cortam", () => {
  const trace = createTrace();
  traceEvents(trace, [{ type: "hit" }], 10);
  traceEvents(trace, [{ type: "hit" }], 20);
  assert.equal(trace.curve.longest_hit_streak, 2);
  traceEvents(trace, [{ type: "collect" }], 30);
  traceEvents(trace, [{ type: "hit" }], 40);
  assert.equal(trace.curve.longest_hit_streak, 2);
  traceEvents(trace, [{ type: "graze" }], 50);
  traceEvents(trace, [{ type: "hit" }], 60);
  assert.equal(trace.curve.longest_hit_streak, 2);
});

test("missed seguidos alongam a sequência; collect e bank cortam", () => {
  const trace = createTrace();
  traceEvents(trace, [{ type: "missed" }], 4);
  traceEvents(trace, [{ type: "missed" }], 5);
  traceEvents(trace, [{ type: "missed" }], 6);
  assert.equal(trace.curve.longest_miss_streak, 3);
  traceEvents(trace, [{ type: "collect" }], 7);
  traceEvents(trace, [{ type: "missed" }], 8);
  assert.equal(trace.curve.longest_miss_streak, 3);
  traceEvents(trace, [{ type: "bank" }], 9);
  traceEvents(trace, [{ type: "missed" }, { type: "missed" }], 10);
  assert.equal(trace.curve.longest_miss_streak, 3);
});

test("dash não conta como erro nem como recuperação", () => {
  const trace = createTrace();
  traceEvents(trace, [{ type: "hit" }], 1);
  traceEvents(trace, [{ type: "dash" }], 2);
  traceEvents(trace, [{ type: "hit" }], 3);
  assert.equal(trace.curve.longest_hit_streak, 2);
});

test("o encerramento registra a corrente que não foi guardada", () => {
  const trace = createTrace();
  traceEvents(trace, [{ type: "over", unbanked: 4 }], 3600);
  assert.equal(trace.curve.unbanked_at_end, 4);
  assert.equal(finishCurve(trace, 2).unbanked_at_end, 2);
});

test("a curva não entra na forma do save", () => {
  const summary = summarizeRun({
    seed: 7,
    score: 9,
    chain: 2,
    tick: 100,
    stats: { collected: 3, missed: 1, hits: 1, banks: 0, bestChain: 2, banked: 0 },
  });
  assert.equal(summary.spawn, "spawn");
  assert.equal(summary.look, "normal");
  assert.equal("never_banked" in summary, false);
  assert.equal("first_hit_tick" in summary, false);
  assert.equal("longest_miss_streak" in summary, false);
});

test("a partida real alimenta a curva pelos eventos do tick", () => {
  const state = createState(2);
  const trace = createTrace();
  state.chain = 3;
  advance(state, { move: 0, dash: false, bank: true });
  for (let step = 0; step < CONFIG.bank.windupTicks; step += 1) {
    advance(state, { move: 0, dash: false, bank: false });
  }
  traceEvents(trace, state.events, state.tick);
  assert.equal(trace.curve.never_banked, false);
  assert.equal(trace.curve.first_bank_tick, state.tick);
  state.entities = [{ id: 9, kind: "shard", x: state.player.x, y: PLAYER_Y, vy: 0 }];
  while (state.hitstop > 0) advance(state, { move: 0, dash: false, bank: false });
  advance(state, { move: 0, dash: false, bank: false });
  traceEvents(trace, state.events, state.tick);
  assert.equal(trace.curve.never_hit, false);
  assert.ok(trace.curve.first_hit_tick > trace.curve.first_bank_tick);
  assert.ok(CONFIG.runTicks > 0);
});
