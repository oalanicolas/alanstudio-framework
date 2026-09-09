// O toque reduz a intenção no mesmo contrato do teclado. Existir o
// listener no HTML não prova o verbo — o teste percorre mover, avançar
// e guardar. Sessão no aparelho continua não observada.

import { test } from "node:test";
import assert from "node:assert/strict";

import { createInput } from "../src/core/input.js";

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

test("sem superfície o toque não inventa intenção", () => {
  const input = createInput({ target: null });
  assert.deepEqual(input.intent(0.5), { move: 0, dash: false, bank: false });
  input.dispose();
});
