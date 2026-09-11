// Aceitar um parâmetro `seed` não prova determinismo. Estes testes provam:
// mesma seed e mesma sequência de intenções produzem o mesmo estado, e um
// estado serializado retomado continua igual ao que nunca foi interrompido.

import { test } from "node:test";
import assert from "node:assert/strict";

import { advance, createState, restoreState } from "../src/game/rules.js";
import { createRng, hashSeed } from "../src/core/rng.js";
import { captureHold } from "../src/core/save.js";
import { fingerprint } from "../src/core/hash.js";

function script(seed, length) {
  const rng = createRng(`roteiro-${seed}`);
  const intents = [];
  for (let index = 0; index < length; index += 1) {
    intents.push({
      move: rng.next() < 0.55 ? (rng.next() < 0.5 ? -1 : 1) : 0,
      dash: rng.next() < 0.07,
      bank: rng.next() < 0.06,
    });
  }
  return intents;
}

function print(state) {
  const { events, ...rest } = state;
  return fingerprint(rest);
}

function play(seed, intents) {
  return continueWith(createState(seed), intents);
}

function continueWith(state, intents) {
  for (const intent of intents) advance(state, intent);
  return state;
}

test("reseed devolve o mesmo objeto à mesma sequência", () => {
  const rng = createRng(42);
  const first = [rng.next(), rng.next(), rng.next()];
  const same = rng.reseed(42);
  assert.equal(same, rng);
  assert.deepEqual([rng.next(), rng.next(), rng.next()], first);
});

test("partidas intercaladas não contaminam o gerador compartilhado", () => {
  const first = script(11, 240);
  const second = script(12, 240);
  const a = createState(11);
  const b = createState(12);
  for (let index = 0; index < first.length; index += 1) {
    advance(a, first[index]);
    advance(b, second[index]);
  }
  assert.equal(print(a), print(play(11, first)));
  assert.equal(print(b), print(play(12, second)));
});

test("a mesma seed com as mesmas intenções produz o mesmo estado", () => {
  const intents = script(11, 900);
  assert.equal(print(play(11, intents)), print(play(11, intents)));
});

test("seeds diferentes produzem partidas diferentes", () => {
  const intents = script(11, 900);
  assert.notEqual(print(play(11, intents)), print(play(12, intents)));
});

test("retomar um estado serializado continua a mesma partida", () => {
  const first = script(21, 400);
  const rest = script(22, 400);
  const live = play(21, first);
  const saved = JSON.stringify(live);
  // Uma continuação em memória e uma retomada a partir do texto salvo precisam
  // terminar no mesmo lugar; é isso que torna save e replay confiáveis.
  const straight = continueWith(live, rest);
  const resumed = continueWith(JSON.parse(saved), rest);
  assert.equal(print(straight), print(resumed));
});

function playFields(state) {
  return {
    tick: state.tick,
    seed: state.seed,
    score: state.score,
    chain: state.chain,
    rngState: state.rngState,
    player: state.player,
    entities: state.entities,
    stats: state.stats,
    spawnTimer: state.spawnTimer,
    nextId: state.nextId,
  };
}

test("o hold retoma a chuva, não a seed do zero", () => {
  const first = script(21, 180);
  const rest = script(23, 80);
  const live = play(21, first);
  const hold = captureHold(live);
  assert.ok(hold, "a chuva no meio precisa caber no hold");
  const straight = continueWith(live, rest);
  const resumed = continueWith(restoreState(hold), rest);
  assert.deepEqual(playFields(resumed), playFields(straight));
});

test("o estado é JSON simples, sem referências vivas", () => {
  const state = play(31, script(31, 200));
  const round = JSON.parse(JSON.stringify(state));
  assert.equal(print(round), print(state));
});

test("seed textual é estável e distingue partidas", () => {
  assert.equal(hashSeed("corrente"), hashSeed("corrente"));
  assert.notEqual(hashSeed("corrente"), hashSeed("outra"));
  assert.equal(createState("corrente").rngState, createState("corrente").rngState);
  assert.notEqual(createState("corrente").rngState, createState("outra").rngState);
});

test("a impressão detecta uma diferença de um único campo", () => {
  const state = play(41, script(41, 120));
  const changed = JSON.parse(JSON.stringify(state));
  changed.score += 1;
  assert.notEqual(print(changed), print(state));
});
