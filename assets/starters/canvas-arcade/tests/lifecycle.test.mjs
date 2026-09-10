// O harness fala de pause, reset, seed, observe, act, advance, capture e
// dispose como vocabulário de inspeção. Aqui cada um é exercitado: é este
// arquivo que separa "mencionado" de "demonstrado".

import { test } from "node:test";
import assert from "node:assert/strict";

import { createGame } from "../src/main.js";
import { memoryStorage } from "../src/core/storage.js";
import { CONFIG } from "../src/game/rules.js";
import { pairPatch } from "../src/game/tables.js";

function silentHaptics(played) {
  return {
    play(role) {
      played.push(role);
      return true;
    },
    applySettings() {},
    mute() {
      played.push("mute");
    },
    unmute() {
      played.push("unmute");
    },
    dispose() {
      played.push("dispose");
    },
  };
}

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
  assert.deepEqual(gaps.registered, [], "sem canvas o loader não busca arquivo");
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
  assert.equal(game.lastRun.score, state.score);
  assert.equal(game.lastRun.ticks, state.tick);
  game.dispose();
});

function silentCanvas() {
  return {
    getContext: () => ({
      setTransform() {},
      beginPath() {},
      closePath() {},
      moveTo() {},
      lineTo() {},
      arc() {},
      fill() {},
      stroke() {},
      fillRect() {},
      strokeRect() {},
      measureText: () => ({ width: 0 }),
      fillText() {},
      createRadialGradient: () => ({ addColorStop() {} }),
      fillStyle: "",
      strokeStyle: "",
      font: "",
      textAlign: "left",
      textBaseline: "top",
      lineWidth: 1,
      globalAlpha: 1,
    }),
    style: {},
    width: 320,
    height: 180,
  };
}

test("sem tela o boot não espera a abertura", () => {
  const { game } = harness();
  assert.equal(game.observe().phase, "playing");
  game.dispose();
});

test("com tela a abertura lê a última seed", () => {
  const { game, storage } = harness();
  game.advance(CONFIG.runTicks);
  const lastSeed = game.observe().seed;
  game.dispose();
  const again = createGame({
    eventTarget: recordingTarget(),
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(again.observe().phase, "title");
  assert.equal(again.observe().seed, lastSeed);
  again.act({ dash: true });
  again.advance(1);
  assert.equal(again.observe().phase, "playing");
  assert.equal(again.observe().seed, lastSeed);
  assert.equal(again.observe().tick, 0, "repetir a seed não é o tick interrompido");
  again.reset();
  assert.equal(again.observe().phase, "playing");
  again.dispose();
});

test("com tela o fim volta à abertura", () => {
  const storage = memoryStorage();
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(game.observe().phase, "title");
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing");
  game.advance(CONFIG.runTicks);
  assert.equal(game.observe().phase, "over");
  const lastSeed = game.observe().seed;
  const score = game.lastRun.score;
  game.reset();
  assert.equal(game.observe().phase, "title", "o overlay não pula a porta");
  assert.equal(game.observe().seed, lastSeed);
  assert.equal(game.observe().tick, 0);
  assert.equal(Number.isFinite(score), true);
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing");
  assert.equal(game.observe().seed, lastSeed);
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

test("esconder a página descarrega o progresso e pausa", () => {
  const storage = memoryStorage();
  const { game, target } = harness({ storage });
  game.updateSettings({ assist: true });
  storage.remove("settings");
  const hide = target.listeners.find((entry) => entry.type === "pagehide");
  assert.ok(hide, "pagehide precisa de ouvinte");
  hide.handler();
  assert.equal(JSON.parse(storage.get("settings")).assist, true);
  assert.equal(game.paused, false, "pagehide descarrega sem pausar — a pausa é do hidden");
  game.flush();
  game.dispose();
});

test("perda de foco pausa e descarrega", () => {
  const storage = memoryStorage();
  const { game, target } = harness({ storage });
  game.updateSettings({ captions: false });
  storage.remove("settings");
  const change = target.listeners.find((entry) => entry.type === "visibilitychange");
  assert.ok(change);
  change.handler();
  assert.equal(game.paused, true);
  assert.equal(JSON.parse(storage.get("settings")).captions, false);
  game.dispose();
});

test("trocar o perfil de chuva recomeça a partida com a mesa nova", () => {
  const { game, storage } = harness();
  game.advance(40);
  assert.equal(game.observe().spawnProfile, "spawn");
  assert.ok(game.observe().tick > 0);
  game.updateSettings({ spawnProfile: "dusk" });
  const after = game.observe();
  assert.equal(after.tick, 0, "outra chuva é outra partida");
  assert.equal(after.spawnProfile, "dusk");
  assert.equal(after.spawn.intervalTicks, 16);
  assert.equal(game.settings.spawnProfile, "dusk");
  assert.equal(JSON.parse(storage.get("settings")).spawnProfile, "dusk");
  const reopened = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  assert.equal(reopened.observe().spawnProfile, "dusk");
  reopened.dispose();
  game.dispose();
});

test("trocar o look não recomeça a partida", () => {
  const { game, storage } = harness();
  game.advance(40);
  const tick = game.observe().tick;
  game.updateSettings({ look: "dusk" });
  assert.equal(game.observe().tick, tick, "look é apresentação, não outra partida");
  assert.equal(game.settings.look, "dusk");
  assert.equal(JSON.parse(storage.get("settings")).look, "dusk");
  const reopened = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  assert.equal(reopened.settings.look, "dusk");
  reopened.dispose();
  game.dispose();
});

test("a query escolhe o look sem inventar mesa", () => {
  const { game } = harness({ query: "?look=dusk" });
  assert.equal(game.settings.look, "dusk");
  const soft = createGame({
    seed: 5,
    query: "?look=calm",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(soft.settings.look, "calm");
  const ignored = createGame({
    seed: 5,
    query: "?look=inventada",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(ignored.settings.look, "normal");
  ignored.dispose();
  soft.dispose();
  game.dispose();
});

test("?mood aplica o par look e chuva sem inventar mesa", () => {
  const { game } = harness({ query: "?mood=calm" });
  assert.equal(game.settings.look, "calm");
  assert.equal(game.settings.spawnProfile, "calm");
  assert.equal(game.observe().spawnProfile, "calm");
  const dusk = createGame({
    seed: 5,
    query: "?mood=dusk",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(dusk.settings.look, "dusk");
  assert.equal(dusk.settings.spawnProfile, "dusk");
  const ignored = createGame({
    seed: 5,
    query: "?mood=inventada",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(ignored.settings.look, "normal");
  assert.equal(ignored.settings.spawnProfile, "spawn");
  ignored.dispose();
  dusk.dispose();
  game.dispose();
});

test("o par da página aplica look e chuva e recomeça a chuva", () => {
  const { game } = harness();
  game.advance(40);
  assert.ok(game.observe().tick > 0);
  game.updateSettings(pairPatch("calm"));
  assert.equal(game.settings.look, "calm");
  assert.equal(game.settings.spawnProfile, "calm");
  assert.equal(game.observe().spawnProfile, "calm");
  assert.equal(game.observe().tick, 0, "trocar a chuva do par recomeça");
  game.dispose();
});

test("look e spawn explícitos vencem o mood no próprio eixo", () => {
  const lookWins = createGame({
    seed: 5,
    query: "?mood=calm&look=dusk",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(lookWins.settings.look, "dusk");
  assert.equal(lookWins.settings.spawnProfile, "calm");
  const spawnWins = createGame({
    seed: 5,
    query: "?mood=calm&spawn=dusk",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(spawnWins.settings.look, "calm");
  assert.equal(spawnWins.settings.spawnProfile, "dusk");
  lookWins.dispose();
  spawnWins.dispose();
});

test("a query escolhe o perfil de chuva sem inventar mesa", () => {
  const { game } = harness({ query: "?spawn=dusk" });
  assert.equal(game.observe().spawnProfile, "dusk");
  assert.equal(game.settings.spawnProfile, "dusk");
  const soft = createGame({
    seed: 5,
    query: "?spawn=calm",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(soft.observe().spawnProfile, "calm");
  assert.equal(soft.observe().spawn.intervalTicks, 30);
  const ignored = createGame({
    seed: 5,
    query: "?spawn=inventada",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(ignored.observe().spawnProfile, "spawn");
  ignored.dispose();
  soft.dispose();
  game.dispose();
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

test("o avanço pulsa no aparelho e a pausa cala o que ainda vibrava", () => {
  const played = [];
  const { game } = harness({ haptics: silentHaptics(played) });
  game.act({ dash: true });
  game.advance(1);
  assert.ok(played.includes("dash"), `esperava dash no pulso: ${JSON.stringify(played)}`);
  game.pause();
  assert.ok(played.includes("mute"), "pausar precisa calar o pulso");
  game.resume();
  assert.ok(played.includes("unmute"));
  game.dispose();
  assert.ok(played.includes("dispose"));
});
