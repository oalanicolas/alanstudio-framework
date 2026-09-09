// O starter não embarca som. O que precisa estar provado é a mixagem: que a
// ausência é declarada, que a legenda cobre a informação sonora e que, sob
// pressão, o som que desaparece é o menos importante — não o aviso.

import { test } from "node:test";
import assert from "node:assert/strict";

import { SOUNDS, createAudio } from "../src/game/audio.js";

function fakeContext() {
  const gains = [];
  const sources = [];
  const context = {
    closed: false,
    gains,
    sources,
    destination: {},
    createGain() {
      const node = { gain: { value: 1 }, connect() {} };
      gains.push(node);
      return node;
    },
    createBufferSource() {
      const node = {
        buffer: null,
        started: false,
        stopped: false,
        connect() {},
        start() {
          node.started = true;
        },
        stop() {
          node.stopped = true;
        },
      };
      sources.push(node);
      return node;
    },
    close() {
      context.closed = true;
    },
  };
  return context;
}

function build(overrides = {}) {
  let clock = 0;
  const context = fakeContext();
  const audio = createAudio({
    now: () => clock,
    createContext: () => context,
    settings: { buses: { master: 0.8, music: 0.6, sfx: 0.9, ui: 0.7 }, captions: true },
    ...overrides,
  });
  return { audio, context, tick: (ms) => (clock += ms), at: () => clock };
}

test("a ausência de som é uma lacuna declarada, não silêncio", () => {
  const { audio } = build();
  assert.deepEqual(audio.missing().declared, Object.keys(SOUNDS));
  assert.deepEqual(audio.missing().registered, []);
  assert.equal(audio.play("collect"), false);
  assert.deepEqual(audio.missing().requested, ["collect"]);
});

test("a legenda sai mesmo sem arquivo de som", () => {
  const { audio } = build();
  audio.play("hit");
  const captions = audio.captions();
  assert.equal(captions.length, 1);
  assert.equal(captions[0].text, SOUNDS.hit.caption);
});

test("legenda desligada não produz legenda", () => {
  const { audio } = build({ settings: { buses: { master: 1 }, captions: false } });
  audio.play("hit");
  assert.deepEqual(audio.captions(), []);
});

test("a legenda expira em vez de acumular na tela", () => {
  const { audio, tick } = build();
  audio.play("collect");
  assert.equal(audio.captions().length, 1);
  tick(5000);
  assert.deepEqual(audio.captions(), []);
});

test("som desconhecido é ignorado sem quebrar o quadro", () => {
  const { audio } = build();
  assert.equal(audio.play("missed"), false);
  assert.deepEqual(audio.captions(), []);
});

test("registrar um som o remove da lacuna e o toca", () => {
  const { audio, context } = build();
  assert.equal(audio.register("collect", { duration: 0.2 }), true);
  assert.equal(audio.play("collect"), true);
  assert.deepEqual(audio.missing().registered, ["collect"]);
  assert.equal(context.sources.length, 1);
  assert.equal(context.sources[0].started, true);
  assert.equal(audio.available, true);
});

test("registrar um papel inexistente é recusado", () => {
  const { audio } = build();
  assert.equal(audio.register("trilha-inventada", {}), false);
});

test("sob pressão, o aviso importante corta o som menor", () => {
  const { audio, context } = build({ maxVoices: 2 });
  for (const id of ["dash", "graze", "hit"]) audio.register(id, { duration: 1 });
  assert.equal(audio.play("dash"), true);
  assert.equal(audio.play("graze"), true);
  assert.equal(audio.play("hit"), true, "o aviso entra");
  assert.equal(context.sources[0].stopped, true, "o som de menor prioridade sai");
  assert.equal(audio.play("graze"), false, "um som menor não derruba o aviso");
  assert.equal(context.sources.length, 3);
});

test("o evento crítico abaixa os outros barramentos e o ducking volta sozinho", () => {
  const { audio, context, tick } = build();
  audio.register("hit", { duration: 0.3 });
  audio.play("hit");
  const [master, music, sfx] = context.gains;
  assert.equal(master.gain.value, 0.8, "o volume geral não é alterado pelo ducking");
  assert.ok(sfx.gain.value < 0.9);
  assert.ok(music.gain.value < 0.6);
  tick(SOUNDS.hit.duckMs + 1);
  audio.update();
  assert.equal(sfx.gain.value, 0.9);
  assert.equal(music.gain.value, 0.6);
});

test("alterar preferências reflete nos barramentos", () => {
  const { audio, context } = build();
  audio.register("dash", { duration: 0.2 });
  audio.play("dash");
  audio.applySettings({ buses: { master: 0.2, music: 0, sfx: 0.5, ui: 0.1 }, captions: true });
  assert.equal(context.gains[0].gain.value, 0.2);
  assert.equal(context.gains[2].gain.value, 0.5);
});

test("dispose encerra as vozes e o contexto", () => {
  const { audio, context } = build();
  audio.register("dash", { duration: 1 });
  audio.play("dash");
  audio.dispose();
  assert.equal(context.sources[0].stopped, true);
  assert.equal(context.closed, true);
  assert.equal(audio.play("dash"), false, "descartado, não toca mais");
});
