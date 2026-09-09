// O invólucro: teclado, quadro e pausa juntos.
//
// `lifecycle.test.mjs` exercita o contrato programático — `game.pause()`,
// `game.resume()`. Isso passou o tempo todo enquanto despausar pelo teclado
// era impossível: a leitura da tecla morava dentro da simulação, que não roda
// em pausa. Um contrato provado não prova a ligação até ela ser percorrida.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createGame } from "../src/main.js";
import { memoryStorage } from "../src/core/storage.js";
import { DEFAULT_BINDINGS, ONE_HAND_BINDINGS } from "../src/core/settings.js";

function shell(overrides = {}) {
  const listeners = [];
  const target = {
    addEventListener(type, handler, options) {
      listeners.push({ type, handler, options });
    },
    removeEventListener(type, handler) {
      const index = listeners.findIndex((entry) => entry.type === type && entry.handler === handler);
      if (index !== -1) listeners.splice(index, 1);
    },
  };

  let pending = null;
  let clock = 0;
  const game = createGame({
    seed: 11,
    eventTarget: target,
    storage: memoryStorage(),
    now: () => clock,
    schedule: (callback) => {
      pending = callback;
      return 1;
    },
    cancel: () => {
      pending = null;
    },
    ...overrides,
  });

  function dispatch(type, event) {
    for (const entry of [...listeners]) {
      if (entry.type === type) entry.handler(event);
    }
  }

  return {
    game,
    hold(code) {
      dispatch("keydown", { code, preventDefault() {} });
    },
    release(code) {
      dispatch("keyup", { code });
    },
    press(action) {
      const code = DEFAULT_BINDINGS[action][0];
      dispatch("keydown", { code, preventDefault() {} });
      dispatch("keyup", { code });
    },
    // Um quadro do navegador: o laço agenda o próximo ao terminar este.
    frame(elapsed = 16) {
      clock += elapsed;
      const callback = pending;
      pending = null;
      callback(clock);
    },
  };
}

test("a tecla de pausa pausa e, principalmente, despausa", () => {
  const { game, press, frame } = shell();
  game.start();
  frame();
  assert.equal(game.paused, false, "o jogo começa rodando");

  press("pause");
  frame();
  assert.equal(game.paused, true, "a tecla de pausa não pausou");

  const frozen = game.observe().tick;
  frame();
  frame();
  assert.equal(game.observe().tick, frozen, "pausado, a simulação não pode avançar");

  press("pause");
  frame();
  assert.equal(game.paused, false, "a tecla de pausa não despausou: o jogo ficou preso");

  // O primeiro quadro após retomar só reancora o relógio: acumular o tempo em
  // pausa dispararia uma rajada de passos de recuperação.
  frame(200);
  frame(200);
  assert.ok(game.observe().tick > frozen, "retomar precisa voltar a simular");
  game.dispose();
});

test("a tecla de reiniciar funciona inclusive durante a pausa", () => {
  const { game, press, frame } = shell();
  game.start();
  frame();
  frame(400);
  assert.ok(game.observe().tick > 0);

  press("pause");
  frame();
  assert.equal(game.paused, true);

  press("reset");
  frame();
  assert.equal(game.paused, false, "reiniciar durante a pausa precisa retomar");
  assert.equal(game.observe().tick, 0);
  game.dispose();
});

test("um comando dado durante a pausa não é engolido pela intenção", () => {
  const { game, press, frame } = shell();
  game.start();
  frame();
  press("pause");
  frame();
  assert.equal(game.paused, true);

  // Enquanto pausado, mover e avançar não podem consumir a borda da pausa.
  press("dash");
  press("bank");
  frame();
  press("pause");
  frame();
  assert.equal(game.paused, false);
  game.dispose();
});

test("o preset de uma mão move com o cluster direito", () => {
  const { game, frame, hold, release } = shell();
  game.updateSettings({ oneHand: true, bindings: ONE_HAND_BINDINGS });
  game.start();
  frame();
  const origin = game.observe().player.x;

  hold("ArrowLeft");
  frame();
  assert.equal(game.observe().player.x, origin, "seta não move no preset");
  release("ArrowLeft");

  hold("KeyJ");
  frame();
  frame();
  assert.ok(game.observe().player.x < origin, "J precisa mover para a esquerda");
  game.dispose();
});

test("o preset de uma mão avança no cluster direito", () => {
  const { game, frame, hold, release } = shell();
  game.updateSettings({ oneHand: true, bindings: ONE_HAND_BINDINGS });
  game.start();
  frame();
  hold("Space");
  frame();
  assert.equal(game.observe().player.dashTicks, 0, "espaço não avança no preset");
  release("Space");
  hold("KeyI");
  frame();
  assert.ok(game.observe().player.dashTicks > 0, "I precisa avançar");
  game.dispose();
});

test("dispose para de responder ao teclado", () => {
  const { game, press, frame } = shell();
  game.start();
  frame();
  game.dispose();
  press("pause");
  assert.equal(game.paused, false);
});
