// O laço separa relógio de parede e passo da simulação.
// Velocidade abaixo de 1 dilata o acumulador; o passo continua o mesmo.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createLoop } from "../src/core/loop.js";

test("o relógio lento precisa de mais parede para o mesmo passo", () => {
  let ticks = 0;
  const loop = createLoop({
    stepMs: 16,
    update: () => {
      ticks += 1;
    },
  });
  assert.equal(loop.speed, 1);
  assert.equal(loop.feed(16), 1);
  loop.setSpeed(0.5);
  assert.equal(loop.speed, 0.5);
  assert.equal(loop.feed(16), 0);
  assert.equal(loop.feed(16), 1);
  assert.equal(ticks, 2);
  loop.setSpeed(0);
  assert.equal(loop.speed, 0.5, "zero não é velocidade");
  loop.dispose();
});
