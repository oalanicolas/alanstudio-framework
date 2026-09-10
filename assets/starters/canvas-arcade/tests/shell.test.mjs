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

test("segurar o avanço na porta não dispara o ofício no campo", () => {
  const view = textCanvas();
  const { game, hold, release, frame } = shell({ canvas: view.canvas, loadSfx: false });
  const step = 1000 / 60;
  game.start();
  frame();
  assert.equal(game.observe().phase, "title");
  hold("Space");
  frame(step);
  frame(step);
  assert.equal(game.observe().phase, "playing", "o aperto abre");
  assert.equal(game.observe().stats.dashes, 0, "abrir não conta o ofício");
  for (let n = 0; n < 80; n += 1) frame(step);
  assert.equal(game.observe().stats.dashes, 0, "o mesmo aperto não é o avanço do campo");
  assert.equal(game.observe().player.dashWindup ?? 0, 0, "segurar não arma o coil");
  release("Space");
  frame(step);
  hold("Space");
  for (let n = 0; n < 40; n += 1) frame(step);
  assert.equal(game.observe().stats.dashes, 1, "um avanço novo conta");
  game.dispose();
});

test("segurar o avanço no campo não dispara de novo", () => {
  const { game, hold, release, frame } = shell();
  game.start();
  frame();
  hold("Space");
  for (let step = 0; step < 40; step += 1) frame(16);
  assert.equal(game.observe().stats.dashes, 1, "um aperto é um avanço");
  for (let step = 0; step < 80; step += 1) frame(16);
  assert.equal(game.observe().stats.dashes, 1, "o cooldown não dispara sozinho");
  release("Space");
  frame(16);
  hold("Space");
  for (let step = 0; step < 40; step += 1) frame(16);
  assert.equal(game.observe().stats.dashes, 2, "soltar e apertar é outro");
  game.dispose();
});

test("com tela o boot espera o avanço", () => {
  const view = textCanvas();
  const { game, press, frame } = shell({ canvas: view.canvas, loadSfx: false });
  game.start();
  frame();
  assert.equal(game.observe().phase, "title");
  assert.ok(view.texts.some((text) => String(text).includes("Jogar: Espaço")));
  assert.equal(view.texts.some((text) => String(text).includes("Jogar: toque")), false);
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
  assert.ok(
    view.texts.some((text) => text.includes("Reiniciar: Select")),
    `esperava Select no overlay: ${JSON.stringify(view.texts)}`,
  );
  assert.equal(view.texts.some((text) => text.includes("Esc")), false);
  pads = [];
  game.dispose();
});

test("o telefone vê Jogar: toque na porta sem ter apertado", () => {
  const view = textCanvas();
  const live = { textContent: "" };
  const { game, frame } = shell({
    canvas: view.canvas,
    live,
    loadSfx: false,
    environment: { pointer: { coarse: true } },
  });
  game.start();
  frame();
  assert.equal(game.observe().phase, "title");
  assert.ok(
    view.texts.some((text) => String(text).includes("Jogar: toque")),
    `esperava toque na porta: ${JSON.stringify(view.texts)}`,
  );
  assert.match(live.textContent, /Jogar: toque/);
  assert.equal(/Espaço/.test(live.textContent), false, "o live não herda Espaço");
  assert.equal(
    view.texts.some((text) => String(text).includes("Espaço")),
    false,
    "Espaço mente no telefone",
  );
  assert.ok(
    view.texts.some((text) => String(text).includes("←/→")),
    "o aviso da porta continua teclado",
  );
  assert.equal(
    view.texts.some((text) => String(text).includes("Cima avança")),
    false,
    "a porta não ensina toque no coach",
  );
  game.dispose();
});

test("depois da partida o telefone pede seed nova embaixo", () => {
  const listeners = [];
  const view = textCanvas();
  const canvas = {
    ...view.canvas,
    getBoundingClientRect() {
      return { left: 0, top: 0, width: 360, height: 640 };
    },
    addEventListener(type, handler) {
      listeners.push({ type, handler });
    },
    removeEventListener(type, handler) {
      const index = listeners.findIndex((entry) => entry.type === type && entry.handler === handler);
      if (index !== -1) listeners.splice(index, 1);
    },
    dispatch(type, event) {
      for (const entry of [...listeners]) {
        if (entry.type === type) entry.handler(event);
      }
    },
  };
  const live = { textContent: "" };
  const { game, frame } = shell({
    canvas,
    live,
    loadSfx: false,
    environment: { pointer: { coarse: true } },
  });
  game.start();
  frame();
  game.act({ dash: true });
  game.advance(1);
  game.advance(CONFIG.runTicks);
  assert.equal(game.observe().phase, "over");
  const lastSeed = game.observe().seed;
  game.reset();
  assert.equal(game.observe().phase, "title");
  frame();
  assert.ok(
    view.texts.some((text) => String(text).includes("Nova partida: baixo")),
    `esperava baixo: ${JSON.stringify(view.texts)}`,
  );
  assert.match(live.textContent, /Nova partida: baixo/);
  assert.match(live.textContent, /Repetir a última: toque/);
  assert.equal(/Nova partida: R/.test(live.textContent), false);
  assert.ok(
    view.texts.some((text) => /Repetir a última: toque/.test(String(text))),
    "o campo continua repetindo",
  );
  canvas.dispatch("pointerdown", { clientX: 180, clientY: 560, pointerId: 1 });
  canvas.dispatch("pointerup", { pointerId: 1 });
  frame();
  assert.equal(game.observe().phase, "playing", "o baixo precisa abrir seed nova");
  assert.notEqual(game.observe().seed, lastSeed, "baixo não repete a última");
  game.dispose();
});

test("depois do tap a porta não chama o avanço de cima", () => {
  const listeners = [];
  const view = textCanvas();
  const canvas = {
    ...view.canvas,
    getBoundingClientRect() {
      return { left: 0, top: 0, width: 360, height: 640 };
    },
    addEventListener(type, handler) {
      listeners.push({ type, handler });
    },
    removeEventListener(type, handler) {
      const index = listeners.findIndex((entry) => entry.type === type && entry.handler === handler);
      if (index !== -1) listeners.splice(index, 1);
    },
    dispatch(type, event) {
      for (const entry of [...listeners]) {
        if (entry.type === type) entry.handler(event);
      }
    },
  };
  const { game, frame } = shell({ canvas, loadSfx: false });
  game.start();
  frame();
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing");
  canvas.dispatch("pointerdown", { clientX: 180, clientY: 200, pointerId: 1 });
  canvas.dispatch("pointerup", { pointerId: 1 });
  frame();
  frame();
  game.advance(CONFIG.runTicks);
  assert.equal(game.observe().phase, "over");
  frame();
  assert.ok(
    view.texts.some((text) => /abertura: toque/i.test(String(text))),
    `esperava toque no fim: ${JSON.stringify(view.texts)}`,
  );
  assert.equal(
    view.texts.some((text) => /abertura: cima/i.test(String(text))),
    false,
    "cima mente na porta do fim",
  );
  game.reset();
  assert.equal(game.observe().phase, "title");
  frame();
  assert.ok(
    view.texts.some((text) => /Repetir a última: toque|Jogar: toque/.test(String(text))),
    `esperava toque na porta: ${JSON.stringify(view.texts)}`,
  );
  assert.equal(
    view.texts.some((text) => /Repetir a última: cima|Jogar: cima/.test(String(text))),
    false,
    "cima mente na porta depois do tap",
  );
  game.dispose();
});

test("o toque retoma a pausa sem avançar no mesmo aperto", () => {
  const listeners = [];
  const view = textCanvas();
  const canvas = {
    ...view.canvas,
    getBoundingClientRect() {
      return { left: 0, top: 0, width: 360, height: 640 };
    },
    addEventListener(type, handler) {
      listeners.push({ type, handler });
    },
    removeEventListener(type, handler) {
      const index = listeners.findIndex((entry) => entry.type === type && entry.handler === handler);
      if (index !== -1) listeners.splice(index, 1);
    },
    dispatch(type, event) {
      for (const entry of [...listeners]) {
        if (entry.type === type) entry.handler(event);
      }
    },
  };
  const { game, press, frame } = shell({ canvas, loadSfx: false });
  game.start();
  frame();
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing");
  game.advance(20);
  const dashes = game.observe().stats.dashes;
  press("pause");
  frame();
  assert.equal(game.paused, true);
  canvas.dispatch("pointerdown", { clientX: 180, clientY: 200, pointerId: 1 });
  frame();
  assert.equal(game.paused, true, "o down na pausa não retoma");
  assert.ok(
    view.texts.some((text) => String(text).includes("Continuar: toque")),
    `esperava toque no overlay: ${JSON.stringify(view.texts)}`,
  );
  canvas.dispatch("pointerup", { pointerId: 1 });
  frame();
  assert.equal(game.paused, false, "o tap precisa retomar");
  assert.equal(game.observe().stats.dashes, dashes, "o tap da pausa não é o avanço");
  game.dispose();
});

test("na pausa o telefone vê Continuar: toque sem ter apertado", () => {
  const view = textCanvas();
  const live = { textContent: "" };
  const { game, press, frame } = shell({
    canvas: view.canvas,
    live,
    loadSfx: false,
    environment: { pointer: { coarse: true } },
  });
  game.start();
  frame();
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing");
  press("pause");
  frame();
  assert.equal(game.paused, true);
  frame();
  assert.ok(
    view.texts.some((text) => String(text).includes("Continuar: toque")),
    `esperava toque na pausa: ${JSON.stringify(view.texts)}`,
  );
  assert.equal(
    view.texts.some((text) => String(text).includes("Esc")),
    false,
    "Esc mente no telefone",
  );
  assert.ok(
    view.texts.some((text) => String(text).includes("Reiniciar: R")),
    "o toque não reseta — R continua",
  );
  assert.match(live.textContent, /Continuar: toque/);
  assert.equal(/Esc/.test(live.textContent), false, "o live não herda Esc");
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

test("a velocidade da partida não dilata a mostra", () => {
  const step = 1000 / 60;
  const view = textCanvas();
  const { game, press, frame } = shell({ canvas: view.canvas, loadSfx: false });
  game.updateSettings({ gameSpeed: 0.5 });
  game.start();
  frame();
  assert.equal(game.observe().phase, "title");
  const shown = game.observe().attractTick;
  frame(step);
  assert.equal(
    game.observe().attractTick,
    shown + 1,
    "a mostra anda no relógio cheio",
  );

  press("dash");
  frame(step);
  assert.equal(game.observe().phase, "playing", "o avanço ainda abre");
  const tick = game.observe().tick;
  frame(step);
  assert.equal(game.observe().tick, tick, "meio passo de parede não vira tick da partida");
  frame(step);
  assert.equal(game.observe().tick, tick + 1);
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
