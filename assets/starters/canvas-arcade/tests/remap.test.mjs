import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { DEFAULT_BINDINGS } from "../src/core/settings.js";
import {
  applyRebind,
  captureKey,
  mountRemap,
  remapRows,
  REMAP_ACTIONS,
  REMAP_LABELS,
  rowCaption,
} from "../src/core/remap.js";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");

function fakeTarget() {
  const listeners = [];
  return {
    addEventListener(_, fn) {
      listeners.push(fn);
    },
    removeEventListener(_, fn) {
      const index = listeners.indexOf(fn);
      if (index >= 0) listeners.splice(index, 1);
    },
    press(code) {
      for (const fn of [...listeners]) fn({ code, preventDefault() {} });
    },
    count() {
      return listeners.length;
    },
  };
}

function fakeDocument() {
  return {
    createElement() {
      const listeners = {};
      return {
        type: "",
        dataset: {},
        textContent: "",
        addEventListener(name, fn) {
          listeners[name] = fn;
        },
        click() {
          listeners.click?.();
        },
      };
    },
  };
}

function fakeHost() {
  const children = [];
  return {
    children,
    replaceChildren(...nodes) {
      children.length = 0;
      children.push(...nodes);
    },
    appendChild(node) {
      children.push(node);
    },
  };
}

test("applyRebind troca só a ação pedida e recusa vazio", () => {
  const next = applyRebind(DEFAULT_BINDINGS, "dash", "KeyZ");
  assert.deepEqual(next.dash, ["KeyZ"]);
  assert.deepEqual(next.bank, DEFAULT_BINDINGS.bank);
  assert.equal(applyRebind(DEFAULT_BINDINGS, "dash", ""), DEFAULT_BINDINGS);
  assert.equal(applyRebind(DEFAULT_BINDINGS, "jump", "KeyZ"), DEFAULT_BINDINGS);
});

test("as linhas nomeiam as seis ações do teclado", () => {
  assert.deepEqual(REMAP_ACTIONS, ["left", "right", "dash", "bank", "pause", "reset"]);
  const rows = remapRows(DEFAULT_BINDINGS);
  assert.equal(rows.length, 6);
  assert.equal(rows[2].label, "Avançar");
  assert.ok(rows[2].keys.includes("Espaço"));
  assert.equal(rowCaption(rows[2]), "Avançar: Espaço / K");
  assert.equal(rowCaption(rows[2], true), "Avançar: pressione…");
  assert.equal(REMAP_LABELS.bank, "Guardar");
});

test("capturar uma tecla entrega o código uma vez", () => {
  const target = fakeTarget();
  const codes = [];
  const cancel = captureKey(target, (code) => codes.push(code));
  target.press("KeyZ");
  target.press("KeyX");
  assert.deepEqual(codes, ["KeyZ"]);
  assert.equal(target.count(), 0);
  cancel();
});

test("a superfície na página troca a tecla sem marcar sessão", () => {
  let bindings = { ...DEFAULT_BINDINGS, dash: [...DEFAULT_BINDINGS.dash] };
  const host = fakeHost();
  const target = fakeTarget();
  const mounted = mountRemap(host, {
    document: fakeDocument(),
    target,
    getBindings: () => bindings,
    setBindings: (next) => {
      bindings = next;
    },
  });
  assert.equal(host.children.length, 6);
  const dash = host.children.find((button) => button.dataset.action === "dash");
  assert.ok(dash.textContent.includes("Espaço"));
  dash.click();
  const waiting = host.children.find((button) => button.dataset.action === "dash");
  assert.equal(waiting.textContent, "Avançar: pressione…");
  target.press("KeyZ");
  assert.deepEqual(bindings.dash, ["KeyZ"]);
  const after = host.children.find((button) => button.dataset.action === "dash");
  assert.equal(after.textContent, "Avançar: Z");
  mounted.dispose();
});

test("a página declara o remapeamento sem fingir sessão observada", () => {
  assert.match(html, /id="remap"/);
  assert.match(html, /mountRemap/);
  assert.match(html, /applyRebind|setBindings/);
  assert.match(html, /paintCommands/);
  assert.match(html, /data-command="dash"/);
  assert.match(html, /data-command="reset"/);
  assert.doesNotMatch(html, /verified|aprovado|outsider/);
});
