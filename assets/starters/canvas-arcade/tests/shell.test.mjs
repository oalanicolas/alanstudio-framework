// O invólucro: teclado, quadro e pausa juntos.
//
// `lifecycle.test.mjs` exercita o contrato programático — `game.pause()`,
// `game.resume()`. Isso passou o tempo todo enquanto despausar pelo teclado
// era impossível: a leitura da tecla morava dentro da simulação, que não roda
// em pausa. Um contrato provado não prova a ligação até ela ser percorrida.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createGame } from "../src/main.js";
import { createInput } from "../src/core/input.js";
import { memoryStorage } from "../src/core/storage.js";
import { DEFAULT_BINDINGS, ONE_HAND_BINDINGS } from "../src/core/settings.js";
import { CONFIG } from "../src/game/rules.js";

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
  for (let step = 0; step <= CONFIG.player.dashWindupTicks; step += 1) frame();
  assert.ok(game.observe().player.dashTicks > 0, "I precisa avançar");
  game.dispose();
});

test("o preset de uma mão guarda no cluster direito", () => {
  const { game, frame, hold, release } = shell();
  game.updateSettings({ oneHand: true, bindings: ONE_HAND_BINDINGS });
  game.start();
  frame();
  let collected = false;
  for (let index = 0; index < 600 && !collected; index += 1) {
    const snap = game.observe();
    const orb = snap.entities.find((entity) => entity.kind === "orb");
    if (orb) {
      const delta = orb.x - snap.player.x;
      if (delta < -1) {
        release("KeyL");
        hold("KeyJ");
      } else if (delta > 1) {
        release("KeyJ");
        hold("KeyL");
      } else {
        release("KeyJ");
        release("KeyL");
      }
    }
    frame();
    collected = game.observe().chain > 0;
  }
  assert.ok(collected, "J/L precisa alcançar o orbe: sem coleta o verbo de uma mão não fecha");
  release("KeyJ");
  release("KeyL");
  hold("ArrowDown");
  frame();
  assert.equal(game.observe().stats.banks, 0, "seta não guarda no preset");
  release("ArrowDown");
  hold("KeyK");
  for (let index = 0; index < 10; index += 1) frame();
  assert.ok(game.observe().stats.banks >= 1, "K precisa guardar");
  game.dispose();
});

test("o preset de uma mão pausa e reinicia no cluster direito", () => {
  const { game, frame, hold, release } = shell();
  game.updateSettings({ oneHand: true, bindings: ONE_HAND_BINDINGS });
  game.start();
  frame();
  frame(400);
  assert.ok(game.observe().tick > 0);
  hold("Escape");
  frame();
  assert.equal(game.paused, false, "Escape não pausa no preset");
  release("Escape");
  hold("KeyP");
  frame();
  assert.equal(game.paused, true, "P precisa pausar");
  release("KeyP");
  hold("KeyR");
  frame();
  assert.equal(game.paused, true, "R não reinicia no preset");
  assert.ok(game.observe().tick > 0);
  release("KeyR");
  hold("KeyO");
  frame();
  assert.equal(game.paused, false, "O precisa sair da pausa");
  assert.equal(game.observe().tick, 0, "O precisa reiniciar");
  game.dispose();
});

function stubPad(buttons = {}) {
  const list = Array.from({ length: 16 }, (_, index) => ({ pressed: Boolean(buttons[index]) }));
  return [{ axes: [0], buttons: list }];
}

function textCanvas() {
  const texts = [];
  const context = {
    setTransform() {},
    save() {},
    restore() {},
    beginPath() {},
    closePath() {},
    moveTo() {},
    lineTo() {},
    arc() {},
    ellipse() {},
    quadraticCurveTo() {},
    stroke() {},
    fill() {},
    fillRect() {},
    roundRect() {},
    strokeRect() {},
    clearRect() {},
    rect() {},
    createLinearGradient: () => ({ addColorStop() {} }),
    createRadialGradient: () => ({ addColorStop() {} }),
    measureText: (text) => ({ width: String(text).length * 5 }),
    fillText(text) {
      texts.push(text);
    },
    fillStyle: "#000",
    strokeStyle: "#000",
    font: "8px",
    textAlign: "left",
    textBaseline: "top",
    lineWidth: 1,
    globalAlpha: 1,
  };
  return {
    texts,
    canvas: {
      getContext: () => context,
      style: {},
      width: 360,
      height: 640,
    },
  };
}

test("com tela o boot espera o avanço", () => {
  const view = textCanvas();
  const { game, press, frame } = shell({ canvas: view.canvas, loadSfx: false });
  game.start();
  frame();
  assert.equal(game.observe().phase, "title");
  assert.ok(view.texts.some((text) => String(text).includes("Jogar")));
  press("pause");
  frame();
  assert.equal(game.paused, false, "na abertura a pausa não cobre o campo");
  assert.equal(game.observe().phase, "title");
  press("dash");
  frame();
  assert.equal(game.observe().phase, "playing");
  game.dispose();
});

test("o overlay nomeia o controle quando ele falou por último", () => {
  const view = textCanvas();
  let pads = stubPad({ 0: true });
  const { game, frame } = shell({
    canvas: view.canvas,
    input: createInput({ target: null, gamepads: () => pads }),
  });
  game.start();
  frame();
  assert.equal(game.observe().phase, "title");
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing", "A sai da abertura");
  pads = stubPad({ 9: true });
  frame();
  assert.equal(game.paused, true, "Start precisa pausar");
  frame();
  assert.ok(
    view.texts.some((text) => text.includes("Continuar: Start")),
    `esperava Start no overlay: ${JSON.stringify(view.texts)}`,
  );
  assert.equal(view.texts.some((text) => text.includes("Esc")), false);
  pads = [];
  game.dispose();
});

test("a velocidade da partida dilata o relógio, não o passo", () => {
  const step = 1000 / 60;
  const slow = shell();
  slow.game.updateSettings({ gameSpeed: 0.5 });
  slow.game.start();
  slow.frame();
  slow.frame(step);
  assert.equal(slow.game.observe().tick, 0, "meio passo de parede não vira tick");
  slow.frame(step);
  assert.equal(slow.game.observe().tick, 1);
  slow.game.dispose();

  const full = shell();
  full.game.start();
  full.frame();
  full.frame(step);
  assert.equal(full.game.observe().tick, 1, "relógio cheio anda um tick no passo");
  full.game.dispose();
});

test("dispose para de responder ao teclado", () => {
  const { game, press, frame } = shell();
  game.start();
  frame();
  game.dispose();
  press("pause");
  assert.equal(game.paused, false);
});
