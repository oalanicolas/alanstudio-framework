// O harness fala de pause, reset, seed, observe, act, advance, capture e
// dispose como vocabulário de inspeção. Aqui cada um é exercitado: é este
// arquivo que separa "mencionado" de "demonstrado".

import { test } from "node:test";
import assert from "node:assert/strict";

import { createGame } from "../src/main.js";
import { memoryStorage } from "../src/core/storage.js";
import { CONFIG } from "../src/game/rules.js";

function recordingTarget() {
  const listeners = [];
  return {
    listeners,
    addEventListener(type, handler, options) {
      listeners.push({ type, handler, options });
    },
    removeEventListener(type, handler) {
      const index = listeners.findIndex((entry) => entry.type === type && entry.handler === handler);
      if (index !== -1) listeners.splice(index, 1);
    },
  };
}

function harness(overrides = {}) {
  const target = recordingTarget();
  const storage = overrides.storage ?? memoryStorage();
  const game = createGame({ seed: 5, eventTarget: target, storage, ...overrides });
  return { game, target, storage };
}

test("a pausa congela a simulação e retomar continua de onde parou", () => {
  const { game } = harness();
  game.advance(10);
  assert.equal(game.observe().tick, 10);
  game.pause();
  assert.equal(game.paused, true);
  game.advance(10);
  assert.equal(game.observe().tick, 10, "pausado, nenhum passo acontece");
  game.resume();
  game.advance(5);
  assert.equal(game.observe().tick, 15);
  game.dispose();
});

test("reset volta ao estado inicial preservando a seed", () => {
  const { game } = harness();
  game.act({ move: 1 });
  game.advance(120);
  const before = game.observe();
  assert.ok(before.tick > 0);
  const fresh = game.reset();
  assert.equal(fresh.tick, 0);
  assert.equal(fresh.score, 0);
  assert.equal(fresh.chain, 0);
  assert.deepEqual(fresh.entities, []);
  assert.equal(fresh.seed, before.seed);
  game.dispose();
});

test("reset com seed nova produz outra partida", () => {
  const { game } = harness();
  game.advance(200);
  const first = game.observe().fingerprint;
  game.seed(999);
  game.advance(200);
  assert.notEqual(game.observe().fingerprint, first);
  assert.equal(game.seed(), 999);
  game.dispose();
});

test("reset sai da pausa", () => {
  const { game } = harness();
  game.pause();
  game.reset();
  assert.equal(game.paused, false);
  game.advance(3);
  assert.equal(game.observe().tick, 3);
  game.dispose();
});

test("dispose remove exatamente os listeners que registrou", () => {
  const { game, target } = harness();
  assert.ok(target.listeners.length > 0, "montar registra listeners");
  assert.equal(game.dispose(), true);
  assert.equal(target.listeners.length, 0, "descartar não deixa listener sobrevivente");
  assert.equal(game.dispose(), false, "descartar duas vezes não repete o trabalho");
});

test("montar, descartar e montar de novo não duplica listeners", () => {
  const target = recordingTarget();
  const storage = memoryStorage();
  const first = createGame({ seed: 1, eventTarget: target, storage });
  const initial = target.listeners.length;
  first.dispose();
  const second = createGame({ seed: 1, eventTarget: target, storage });
  assert.equal(target.listeners.length, initial);
  second.dispose();
  assert.equal(target.listeners.length, 0);
});

test("descartado, o jogo não avança mais", () => {
  const { game } = harness();
  game.advance(4);
  game.dispose();
  const tick = game.observe().tick;
  game.advance(50);
  assert.equal(game.observe().tick, tick);
  assert.equal(game.disposed, true);
});

test("observe devolve uma cópia: mexer nela não altera a partida", () => {
  const { game } = harness();
  game.advance(30);
  const snapshot = game.observe();
  snapshot.score = 9999;
  snapshot.player.x = -1;
  snapshot.entities.push({ id: 0, kind: "orb", x: 0, y: 0, vy: 0 });
  const again = game.observe();
  assert.notEqual(again.score, 9999);
  assert.notEqual(again.player.x, -1);
  assert.equal(again.entities.length, snapshot.entities.length - 1);
});

test("act entrega uma intenção e ela é consumida uma única vez", () => {
  const { game } = harness();
  const start = game.observe().player.x;
  game.act({ move: 1 });
  game.advance(1);
  const moved = game.observe().player.x;
  assert.ok(moved > start, "a intenção move o jogador");
  game.advance(1);
  assert.equal(game.observe().player.x, moved, "a intenção não se repete sozinha");
  game.dispose();
});

test("capture não inventa uma imagem quando não há tela", () => {
  const { game } = harness();
  assert.equal(game.capture(), null);
  game.dispose();
});

test("as métricas do laço reportam distribuição, não média", () => {
  const { game } = harness();
  const metrics = game.metrics();
  for (const key of ["frames", "steps", "dropped", "p50", "p95", "p99", "worst"]) {
    assert.ok(key in metrics, `métrica ausente: ${key}`);
  }
  game.dispose();
});

test("a lacuna de áudio é declarada em vez de silenciosa", () => {
  const { game } = harness();
  const gaps = game.audioGaps();
  assert.ok(gaps.declared.includes("collect"));
  assert.deepEqual(gaps.registered, [], "o starter não embarca som");
  game.dispose();
});

test("uma partida completa é registrada no progresso persistido", () => {
  const { game, storage } = harness();
  game.advance(CONFIG.runTicks);
  const state = game.observe();
  assert.equal(state.phase, "over");
  assert.equal(game.progress.runs, 1);
  assert.equal(game.progress.best, state.score);
  assert.equal(JSON.parse(storage.get("progress")).runs, 1);
  game.dispose();
});

test("preferências e progresso vivem em chaves separadas", () => {
  const { game, storage } = harness();
  game.updateSettings({ highContrast: true, reducedMotion: true });
  game.advance(CONFIG.runTicks);
  storage.remove("progress");
  const reopened = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  assert.equal(reopened.settings.highContrast, true, "apagar a partida não apaga a preferência");
  assert.equal(reopened.progress.runs, 0);
  game.dispose();
  reopened.dispose();
});

test("remapear uma ação persiste e recusa uma lista vazia", () => {
  const { game, storage } = harness();
  game.updateSettings({ bindings: { ...game.settings.bindings, dash: ["KeyZ"] } });
  assert.deepEqual(game.settings.bindings.dash, ["KeyZ"]);
  game.updateSettings({ bindings: { ...game.settings.bindings, dash: [] } });
  assert.deepEqual(game.settings.bindings.dash, ["KeyZ"], "remapeamento vazio tornaria a ação inalcançável");
  assert.equal(JSON.parse(storage.get("settings")).bindings.dash[0], "KeyZ");
  game.dispose();
});
