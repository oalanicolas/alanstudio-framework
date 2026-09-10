// O toque reduz a intenção no mesmo contrato do teclado. Existir o
// listener no HTML não prova o verbo — o teste percorre mover, avançar
// e guardar. Sessão no aparelho continua não observada.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createInput, isTypingTarget } from "../src/core/input.js";

function surface(width = 320, height = 180, left = 10, top = 20) {
  const listeners = [];
  return {
    getBoundingClientRect() {
      return { left, top, width, height };
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
    tap(x, y) {
      this.dispatch("pointerdown", { clientX: left + x, clientY: top + y });
    },
  };
}

test("arrastar no toque move; a faixa de cima avança e a de baixo guarda", () => {
  const pad = surface();
  const input = createInput({ target: null, surface: pad });
  pad.tap(64, 90);
  assert.equal(input.lastSource, "pointer", "toque precisa marcar a superfície");
  const dash = input.intent(0.5);
  assert.equal(dash.move, -1, "toque à esquerda do jogador precisa mover");
  assert.equal(dash.dash, true, "faixa de cima precisa avançar");
  assert.equal(dash.bank, false, "meio do campo não guarda");

  pad.tap(160, 160);
  const bank = input.intent(0.5);
  assert.equal(bank.bank, true, "faixa inferior precisa guardar");
  assert.equal(bank.dash, false, "baixo não avança");

  pad.dispatch("pointerup", {});
  const idle = input.intent(0.5);
  assert.equal(idle.move, 0, "soltar o toque para o movimento");
  assert.equal(idle.dash, false);
  assert.equal(idle.bank, false);
  input.dispose();
});

test("na porta o arraste move sem avançar; o tap abre", () => {
  const pad = surface();
  const input = createInput({ target: null, surface: pad });
  assert.equal(input.setDashOnPress(false), false);
  pad.tap(64, 90);
  const drag = input.intent(0.5);
  assert.equal(drag.move, -1, "o arraste ainda move");
  assert.equal(drag.dash, false, "o down na porta não avança");
  assert.equal(drag.bank, false);
  pad.dispatch("pointermove", { clientX: 10 + 40, clientY: 20 + 90 });
  pad.dispatch("pointerup", {});
  const afterDrag = input.intent(0.5);
  assert.equal(afterDrag.dash, false, "soltar o arraste não abre");

  pad.tap(160, 90);
  const hold = input.intent(0.5);
  assert.equal(hold.dash, false, "o down do tap ainda não abre");
  pad.dispatch("pointerup", {});
  const tap = input.intent(0.5);
  assert.equal(tap.dash, true, "o tap na porta abre");
  assert.equal(tap.bank, false);
  input.dispose();
});

test("na porta o tap na faixa da guarda também abre", () => {
  const pad = surface();
  const input = createInput({ target: null, surface: pad });
  input.setDashOnPress(false);
  pad.tap(160, 160);
  const down = input.intent(0.5);
  assert.equal(down.dash, false, "o down na faixa não abre");
  assert.equal(down.bank, true, "o down ainda marca a guarda");
  pad.dispatch("pointerup", {});
  const tap = input.intent(0.5);
  assert.equal(tap.dash, true, "o tap na faixa da porta abre");
  assert.equal(tap.bank, false, "soltar a faixa não guarda na abertura");
  input.dispose();
});

test("segurar o avanço não dispara de novo", () => {
  const keys = surface();
  const input = createInput({ target: keys, surface: null });
  keys.dispatch("keydown", { code: "Space", preventDefault() {} });
  assert.equal(input.intent().dash, true, "o aperto avança");
  assert.equal(input.intent().dash, false, "segurar não é outro avanço");
  keys.dispatch("keyup", { code: "Space" });
  keys.dispatch("keydown", { code: "Space", preventDefault() {} });
  assert.equal(input.intent().dash, true, "soltar e apertar é um avanço novo");
  input.dispose();
});

test("tecla ligada e toque acordam o mixer no gesto, tecla solta não", () => {
  const woken = [];
  const keys = surface();
  const pad = surface();
  const input = createInput({
    target: keys,
    surface: pad,
    unlock: () => {
      woken.push(input.lastSource);
    },
  });
  keys.dispatch("keydown", { code: "KeyZ", preventDefault() {} });
  assert.deepEqual(woken, []);
  keys.dispatch("keydown", { code: "Space", preventDefault() {} });
  assert.deepEqual(woken, ["keyboard"]);
  pad.tap(64, 90);
  assert.deepEqual(woken, ["keyboard", "pointer"]);
  input.dispose();
});

test("sem superfície o toque não inventa intenção", () => {
  const input = createInput({ target: null });
  assert.equal(input.lastSource, "keyboard");
  assert.deepEqual(input.intent(0.5), { move: 0, dash: false, bank: false });
  input.dispose();
});

function stubPad({ axes = [0], buttons = {} } = {}) {
  const list = Array.from({ length: 16 }, (_, index) => ({ pressed: Boolean(buttons[index]) }));
  return [{ axes, buttons: list }];
}

test("o controle acorda o mixer no gesto, zona morta não", () => {
  const woken = [];
  let pads = [];
  const input = createInput({
    target: null,
    gamepads: () => pads,
    unlock: () => {
      woken.push(input.lastSource);
    },
  });
  pads = stubPad({ axes: [-0.1] });
  input.intent();
  assert.deepEqual(woken, [], "zona morta não pede resume");
  pads = stubPad({ buttons: { 0: true } });
  input.intent();
  assert.deepEqual(woken, ["gamepad"], "A do controle pede resume");
  pads = stubPad({ axes: [0.8] });
  input.intent();
  assert.equal(woken.at(-1), "gamepad", "analógico também pede");
  input.dispose();
});

test("o controle move, avança, guarda, pausa e reinicia", () => {
  let pads = [];
  const input = createInput({ target: null, gamepads: () => pads });
  assert.equal(input.lastSource, "keyboard");
  pads = stubPad({ axes: [-0.1] });
  assert.equal(input.intent().move, 0, "eixo dentro da zona morta não move");
  assert.equal(input.lastSource, "keyboard", "zona morta não troca a superfície");
  pads = stubPad({ axes: [-0.8] });
  assert.equal(input.intent().move, -1, "analógico à esquerda precisa mover");
  assert.equal(input.lastSource, "gamepad", "analógico precisa marcar o controle");
  pads = stubPad({ buttons: { 15: true } });
  assert.equal(input.intent().move, 1, "dpad direita precisa mover");
  pads = stubPad({ buttons: { 0: true } });
  assert.equal(input.intent().dash, true, "A precisa avançar");
  pads = stubPad({ buttons: { 2: true } });
  assert.equal(input.intent().bank, true, "X precisa guardar");
  pads = stubPad({ buttons: { 9: true } });
  assert.equal(input.commands().pause, true, "Start precisa pausar");
  assert.equal(input.commands().pause, false, "Start contínuo não repete o comando");
  pads = stubPad({ buttons: { 8: true } });
  assert.equal(input.commands().reset, true, "Select precisa reiniciar");
  pads = [];
  assert.deepEqual(input.intent(), { move: 0, dash: false, bank: false });
  input.dispose();
});

test("tecla já comida não dispara o verbo", () => {
  const keys = surface();
  const input = createInput({ target: keys, surface: null });
  keys.dispatch("keydown", {
    code: "Space",
    defaultPrevented: true,
    preventDefault() {},
  });
  assert.equal(input.intent().dash, false, "defaultPrevented come o ofício");
  input.dispose();
});

test("o recado não dispara o verbo", () => {
  assert.equal(isTypingTarget({ target: { tagName: "TEXTAREA" } }), true);
  assert.equal(isTypingTarget({ target: { tagName: "INPUT" } }), true);
  assert.equal(isTypingTarget({ target: { tagName: "SELECT" } }), true);
  assert.equal(isTypingTarget({ target: { isContentEditable: true } }), true);
  assert.equal(isTypingTarget({ target: { tagName: "BUTTON" } }), false);
  assert.equal(isTypingTarget({ preventDefault() {} }), false);

  const keys = surface();
  const input = createInput({ target: keys, surface: null });
  let blocked = false;
  keys.dispatch("keydown", {
    code: "Space",
    target: { tagName: "TEXTAREA" },
    preventDefault() { blocked = true; },
  });
  assert.equal(blocked, false, "o campo precisa do espaço");
  assert.equal(input.intent().dash, false, "escrever não avança");

  keys.dispatch("keydown", {
    code: "KeyR",
    target: { tagName: "INPUT" },
    preventDefault() { blocked = true; },
  });
  assert.equal(input.commands().reset, false, "escrever não reinicia");

  keys.dispatch("keydown", {
    code: "Space",
    target: { tagName: "BODY" },
    preventDefault() { blocked = true; },
  });
  assert.equal(input.intent().dash, true, "fora do campo o aperto avança");
  input.dispose();
});

test("focar o recado larga a tecla que ainda segurava", () => {
  const keys = surface();
  const input = createInput({ target: keys, surface: null });
  keys.dispatch("keydown", {
    code: "KeyD",
    target: { tagName: "BODY" },
    preventDefault() {},
  });
  assert.equal(input.intent().move, 1, "D ainda move");
  keys.dispatch("keydown", {
    code: "Space",
    target: { tagName: "BODY" },
    preventDefault() {},
  });
  keys.dispatch("focusin", { target: { tagName: "TEXTAREA" } });
  const after = input.intent();
  assert.equal(after.move, 0, "o campo larga o movimento");
  assert.equal(after.dash, false, "o aperto pendente não vira ofício");
  assert.equal(input.commands().reset, false);
  input.dispose();
});

test("A contínuo no controle não repete o avanço", () => {
  let pads = stubPad({ buttons: { 0: true } });
  const input = createInput({ target: null, gamepads: () => pads });
  assert.equal(input.intent().dash, true, "A precisa avançar");
  assert.equal(input.intent().dash, false, "A contínuo não é outro avanço");
  pads = [];
  assert.equal(input.intent().dash, false);
  pads = stubPad({ buttons: { 0: true } });
  assert.equal(input.intent().dash, true, "soltar e apertar é um avanço novo");
  input.dispose();
});

test("o toque que sai do campo ainda solta", () => {
  const pad = surface();
  const captured = [];
  pad.setPointerCapture = (id) => { captured.push(id); };
  const input = createInput({ target: null, surface: pad });
  pad.dispatch("pointerdown", { clientX: 10 + 64, clientY: 20 + 90, pointerId: 7 });
  assert.deepEqual(captured, [7], "o campo precisa da captura");
  assert.equal(input.intent(0.5).move, -1, "o down ainda move");
  pad.dispatch("pointerup", { pointerId: 7 });
  assert.equal(input.intent(0.5).move, 0, "soltar fora ainda para");
  input.dispose();
});

test("perder a captura no meio do arraste solta", () => {
  const pad = surface();
  pad.setPointerCapture = () => {};
  const input = createInput({ target: null, surface: pad });
  pad.dispatch("pointerdown", { clientX: 10 + 64, clientY: 20 + 90, pointerId: 4 });
  assert.equal(input.intent(0.5).move, -1);
  pad.dispatch("lostpointercapture", { pointerId: 4 });
  assert.equal(input.intent(0.5).move, 0, "perder a captura para o movimento");
  input.dispose();
});

test("perder a captura não come o tap da porta", () => {
  const pad = surface();
  pad.setPointerCapture = () => {};
  const input = createInput({ target: null, surface: pad });
  input.setDashOnPress(false);
  pad.dispatch("pointerdown", { clientX: 10 + 160, clientY: 20 + 90, pointerId: 3 });
  pad.dispatch("pointerup", { pointerId: 3 });
  pad.dispatch("lostpointercapture", { pointerId: 3 });
  assert.equal(input.intent(0.5).dash, true, "o tap ainda abre");
  input.dispose();
});
