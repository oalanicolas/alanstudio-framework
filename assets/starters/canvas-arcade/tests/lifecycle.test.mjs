// O harness fala de pause, reset, seed, observe, act, advance, capture e
// dispose como vocabulário de inspeção. Aqui cada um é exercitado: é este
// arquivo que separa "mencionado" de "demonstrado".

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { createGame } from "../src/main.js";
import { createInput } from "../src/core/input.js";
import { memoryStorage } from "../src/core/storage.js";
import { canResume } from "../src/core/save.js";
import { BED_FADE_MS } from "../src/game/audio.js";
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

test("o painel relê a lacuna quando o fetch termina", async () => {
  let release;
  const gate = new Promise((resolve) => {
    release = resolve;
  });
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    loadSfx: true,
    fetch: async (url) => {
      await gate;
      if (url === "public/sfx/dash.wav") {
        return { ok: true, arrayBuffer: async () => new ArrayBuffer(8) };
      }
      return { ok: false };
    },
    decodeSfx: async () => ({ duration: 0.2 }),
  });
  assert.deepEqual(game.audioGaps().registered, []);
  assert.equal(game.audioGaps().requested.includes("dash"), false, "o fetch ainda não esgotou o primário");
  release();
  const settled = await game.whenSfx;
  assert.deepEqual(settled.registered, ["dash"]);
  assert.deepEqual(game.audioGaps().registered, ["dash"]);
  assert.ok(game.audioGaps().requested.includes("hit"));
  assert.equal(game.audioGaps().requested.includes("dash"), false);
  game.dispose();
});

test("sem loader a espera do som resolve na hora", async () => {
  const { game } = harness();
  const settled = await game.whenSfx;
  assert.deepEqual(settled.registered, []);
  assert.ok(settled.declared.includes("collect"));
  game.dispose();
});

test("sessão volátil e gravação recusada aparecem no persist sem chamar isso de confiável", () => {
  const { game } = harness();
  assert.equal(game.persist.durable, false);
  assert.equal(game.persist.wrote, true);
  assert.equal(game.persist.trusted, false);
  const failing = {
    persistent: true,
    get: () => null,
    set() {
      throw new Error("QuotaExceededError");
    },
    remove() {},
    keys: () => [],
  };
  const broken = createGame({ seed: 5, eventTarget: recordingTarget(), storage: failing });
  const flushed = broken.flush();
  assert.equal(broken.persist.durable, true);
  assert.equal(broken.persist.wrote, false);
  assert.equal(broken.persist.reason, "write_failed");
  assert.equal(broken.persist.trusted, false);
  assert.equal(flushed.persist.trusted, false);
  assert.equal(flushed.persist.wrote, false);
  broken.dispose();
  game.dispose();
});

test("preferências ilegíveis avisam sem fingir confiança", () => {
  const storage = memoryStorage();
  storage.set("settings", "]{");
  const game = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  assert.equal(game.settingsLoad.status, "recovered");
  assert.match(game.settingsLoad.notes[0], /settings\.broken/);
  assert.equal(game.settings.schema, 1);
  assert.equal(storage.get("settings.broken"), "]{");
  assert.equal(game.persist.trusted, false);
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
  assert.equal(game.lastRun.spawn, "spawn");
  assert.equal(game.lastRun.look, "normal");
  assert.equal(game.lastRun.speed, 1);
  assert.equal(typeof game.lastRun.curve?.never_banked, "boolean");
  assert.equal(Number.isFinite(game.lastRun.curve?.unbanked_at_end), true);
  const painted = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  painted.updateSettings({ look: "dusk", gameSpeed: 0.75 });
  painted.advance(CONFIG.runTicks);
  assert.equal(painted.lastRun.look, "dusk");
  assert.equal(painted.lastRun.spawn, "spawn");
  assert.equal(painted.lastRun.speed, 0.75);
  painted.dispose();
  game.dispose();
});

test("o over pede fade da cama sem fingir mix ouvido", () => {
  const stops = [];
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    audio: {
      play() {
        return true;
      },
      stop(id, extra = {}) {
        stops.push({ id, extra });
      },
      update() {},
      captions() {
        return [];
      },
      unlock() {},
      applySettings() {},
      missing() {
        return { declared: [], registered: [] };
      },
      dispose() {},
    },
  });
  game.advance(CONFIG.runTicks);
  assert.equal(game.observe().phase, "over");
  const bed = stops.find((item) => item.id === "bed" && item.extra.fadeMs === BED_FADE_MS);
  assert.ok(bed, "esperava soltar a cama");
  assert.doesNotMatch(String(BED_FADE_MS), /aprovado|verified|heard|LUFS|-14/);
  game.dispose();
});

test("no fim a pausa não come o stinger sem fingir mix ouvido", () => {
  const calls = [];
  const audio = {
    play() {
      return true;
    },
    stop() {
      return true;
    },
    hush() {
      calls.push("hush");
      return true;
    },
    lift() {
      calls.push("lift");
      return true;
    },
    update() {},
    captions() {
      return [];
    },
    unlock() {},
    applySettings() {},
    missing() {
      return { declared: [], registered: [] };
    },
    dispose() {},
  };
  const field = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    audio,
  });
  field.advance(1);
  assert.equal(field.observe().phase, "playing");
  field.pause();
  assert.equal(calls.includes("hush"), true, "no campo o hit some");
  field.dispose();
  calls.length = 0;
  const ended = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    audio,
  });
  ended.advance(CONFIG.runTicks);
  assert.equal(ended.observe().phase, "over");
  ended.pause();
  assert.equal(calls.includes("hush"), false, "o stinger atravessa o fim");
  ended.dispose();
  assert.doesNotMatch(calls.join(" "), /aprovado|verified|heard|LUFS|-14/);
});

test("com tela o fim oferece o candidato sem chamar isso de observado", async () => {
  const posted = [];
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    loadSfx: false,
    fetch: (url, init) => {
      posted.push({ url, init });
      return Promise.resolve({ ok: true });
    },
  });
  game.act({ dash: true });
  game.advance(1);
  game.advance(CONFIG.runTicks);
  assert.equal(game.observe().phase, "over");
  assert.equal(posted.length, 1);
  assert.equal(posted[0].url, "/playtest/last-run");
  assert.equal(posted[0].init.method, "POST");
  const body = JSON.parse(posted[0].init.body);
  assert.equal(body.policy, "played");
  assert.equal(body.observed, false);
  assert.equal(body.felt, false);
  assert.equal(body.run.ticks, game.lastRun.ticks);
  assert.equal(body.look, "normal");
  assert.equal(body.run.look, "normal");
  assert.ok(body.curve);
  assert.equal(body.curve.unbanked_at_end, game.lastRun.chain);
  assert.doesNotMatch(body.scope, /aprovado|verified|LUFS|-14|4\.5/);
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

test("com tela a mostra toca o corpo sem abrir o ciclo", () => {
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(game.observe().phase, "title");
  let touched = null;
  for (let step = 0; step < 300; step += 1) {
    const x = game.observe().player.x;
    if (x > 128) game.act({ move: -1 });
    const snap = game.advance(1);
    if (snap.flash > 0 || snap.player.squash !== 0) {
      touched = snap;
      break;
    }
  }
  assert.ok(touched, "esperava o contato da mostra");
  assert.equal(touched.phase, "title");
  assert.equal(touched.tick, 0);
  assert.equal(touched.score, 0);
  assert.equal(touched.entities.length, 0);
  assert.equal(touched.events.length, 0);
  game.dispose();
});

test("com tela a porta fala a mostra sem abrir o ciclo", () => {
  const heard = [];
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    loadSfx: false,
    audio: {
      play(role) {
        heard.push(role);
        return true;
      },
      stop() {},
      update() {},
      captions() {
        return heard.includes("live") ? [{ text: "a chuva começa", count: 1 }] : [];
      },
      unlock() {},
      applySettings() {},
      missing() {
        return { declared: [], registered: [] };
      },
      dispose() {},
    },
  });
  assert.equal(game.observe().phase, "title");
  game.advance(1);
  assert.equal(game.observe().phase, "title");
  assert.equal(game.observe().tick, 0);
  assert.ok(heard.includes("live"), `esperava a voz da mostra: ${JSON.stringify(heard)}`);
  assert.equal(heard.filter((role) => role === "live").length, 1);
  assert.equal(heard.includes("bed"), false, "a porta não liga a cama");
  game.advance(1);
  assert.equal(heard.filter((role) => role === "live").length, 1, "o segundo quadro não repete");
  game.dispose();
});

test("com tela o toque na porta não avança no down", () => {
  const listeners = [];
  const pad = {
    getBoundingClientRect() {
      return { left: 0, top: 0, width: 320, height: 180 };
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
  const input = createInput({ target: null, surface: pad });
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    input,
    loadSfx: false,
  });
  assert.equal(game.observe().phase, "title");
  pad.dispatch("pointerdown", { clientX: 64, clientY: 90 });
  const door = input.intent(0.5);
  assert.equal(door.dash, false, "o down na porta não avança");
  assert.equal(door.move, -1, "o toque ainda aponta o passo");
  pad.dispatch("pointerup", {});
  input.intent(0.5);
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing");
  pad.dispatch("pointerdown", { clientX: 64, clientY: 90 });
  const field = input.intent(0.5);
  assert.equal(field.dash, true, "no campo o down de cima avança");
  game.dispose();
});

test("com tela a abertura recebe o movimento sem abrir o ciclo", () => {
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(game.observe().phase, "title");
  const start = game.observe().player.x;
  game.act({ move: 1 });
  game.advance(1);
  assert.equal(game.observe().phase, "title");
  assert.equal(game.observe().tick, 0);
  assert.ok(game.observe().player.x > start, "a porta precisa do passo");
  assert.equal(game.observe().entities.length, 0);
  game.dispose();
});

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

test("com tela o avanço novo no fim volta à abertura sem pular o overlay", () => {
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    loadSfx: false,
  });
  game.act({ dash: true });
  game.advance(1);
  for (let step = 0; step < CONFIG.runTicks; step += 1) {
    game.act({ dash: true });
    game.advance(1);
  }
  assert.equal(game.observe().phase, "over", "dash apertado no último tick não pula o fim");
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "over", "o mesmo aperto não abre a porta");
  game.act({ dash: false });
  game.advance(1);
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "title", "um avanço novo volta à porta");
  assert.equal(game.observe().tick, 0);
  assert.equal(Number.isFinite(game.lastRun.score), true);
  game.dispose();
});

test("watch anuncia a fase sem gravar achado", () => {
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    loadSfx: false,
  });
  const seen = [];
  const stop = game.watch((phase) => seen.push(phase));
  assert.deepEqual(seen, ["title"]);
  game.act({ dash: true });
  game.advance(1);
  assert.equal(seen.at(-1), "playing");
  game.advance(CONFIG.runTicks);
  assert.equal(seen.at(-1), "over");
  game.reset();
  assert.equal(seen.at(-1), "title");
  stop();
  game.act({ dash: true });
  game.advance(1);
  assert.equal(seen.at(-1), "title", "depois de parar não anuncia");
  game.dispose();
});

function playFields(obs) {
  return {
    tick: obs.tick,
    seed: obs.seed,
    score: obs.score,
    chain: obs.chain,
    rngState: obs.rngState,
    player: obs.player,
    entities: obs.entities,
    stats: obs.stats,
  };
}

test("o tick interrompido volta; Continuar continua sendo a seed", () => {
  const storage = memoryStorage();
  const live = createGame({ seed: 11, eventTarget: recordingTarget(), storage });
  live.advance(40);
  const mid = live.observe();
  live.flush();
  assert.equal(canResume(JSON.parse(storage.get("progress"))), true);
  assert.equal(canResume(live.progress), true);

  const restored = createGame({ eventTarget: recordingTarget(), storage });
  assert.equal(restored.observe().phase, "playing");
  assert.deepEqual(playFields(restored.observe()), playFields(mid));

  const ignored = createGame({ seed: 99, eventTarget: recordingTarget(), storage });
  assert.equal(ignored.observe().tick, 0, "seed explícita não retoma o hold");
  ignored.dispose();

  live.advance(20);
  restored.advance(20);
  assert.deepEqual(playFields(restored.observe()), playFields(live.observe()));
  live.dispose();
  restored.dispose();
});

test("?seed abre essa partida e ignora o hold", () => {
  const storage = memoryStorage();
  const live = createGame({ seed: 11, eventTarget: recordingTarget(), storage });
  live.advance(40);
  live.flush();
  live.dispose();
  const named = createGame({
    query: "?seed=9",
    eventTarget: recordingTarget(),
    storage,
  });
  assert.equal(named.observe().seed, 9);
  assert.equal(named.observe().tick, 0, "seed na query não retoma o hold");
  assert.equal(named.observe().phase, "playing");
  named.dispose();
  const screened = createGame({
    query: "?seed=9&spawn=dusk",
    eventTarget: recordingTarget(),
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(screened.observe().phase, "title");
  assert.equal(screened.observe().seed, 9);
  assert.equal(screened.observe().spawnProfile, "dusk");
  screened.act({ dash: true });
  screened.advance(1);
  assert.equal(screened.observe().phase, "playing");
  assert.equal(screened.observe().seed, 9);
  screened.dispose();
  const invited = createGame({
    query: "?invite=1&seed=9&spawn=dusk",
    eventTarget: recordingTarget(),
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(invited.observe().phase, "title");
  assert.equal(invited.observe().seed, 9);
  assert.equal(invited.observe().spawnProfile, "dusk");
  invited.dispose();
  const dressed = createGame({
    query: "?invite=1&seed=9&spawn=dusk&look=dusk",
    eventTarget: recordingTarget(),
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(dressed.observe().phase, "title");
  assert.equal(dressed.observe().seed, 9);
  assert.equal(dressed.observe().spawnProfile, "dusk");
  assert.equal(dressed.settings.look, "dusk");
  dressed.dispose();
  const clocked = createGame({
    query: "?invite=1&seed=9&speed=0.75",
    eventTarget: recordingTarget(),
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(clocked.observe().seed, 9);
  assert.equal(clocked.settings.gameSpeed, 0.75);
  clocked.dispose();
  const fullClock = createGame({
    query: "?seed=9&speed=1",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(fullClock.settings.gameSpeed, 1);
  fullClock.dispose();
  const hollowSpeed = createGame({
    query: "?seed=9&speed=12",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(hollowSpeed.settings.gameSpeed, 1, "relógio fora da faixa some");
  hollowSpeed.dispose();
  const kept = createGame({
    seed: 5,
    query: "?seed=9",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(kept.observe().seed, 5, "seed do construtor vence a query");
  kept.dispose();
  const hollow = createGame({
    seed: 5,
    query: "?seed=nope",
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  assert.equal(hollow.observe().seed, 5);
  hollow.dispose();
});

test("com tela o hold retoma o tick e não a porta", () => {
  const storage = memoryStorage();
  const game = createGame({ seed: 11, eventTarget: recordingTarget(), storage });
  game.advance(40);
  game.flush();
  game.dispose();
  const again = createGame({
    eventTarget: recordingTarget(),
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(again.observe().phase, "playing", "hold não abre a porta");
  assert.equal(again.observe().tick, 40);
  assert.equal(again.observe().seed, 11);
  again.reset();
  assert.equal(again.observe().tick, 0);
  assert.equal(canResume(again.progress), false, "reset abandona o tick interrompido");
  again.dispose();
});

test("a cama segue o relógio da sessão sem fingir mix ouvido", () => {
  const rates = [];
  const audio = {
    play() {
      return true;
    },
    stop() {},
    update(extra = {}) {
      if (Number.isFinite(extra.bedRate)) rates.push(extra.bedRate);
    },
    captions() {
      return [];
    },
    unlock() {},
    applySettings() {},
    missing() {
      return { declared: [], registered: [] };
    },
    dispose() {},
  };
  const { game } = harness({ audio });
  game.updateSettings({ gameSpeed: 0.5 });
  assert.equal(rates.at(-1), 0.5, "na partida a cama dilata com o knob");
  game.updateSettings({ gameSpeed: 1 });
  assert.equal(rates.at(-1), 1);
  assert.equal(game.persist.trusted, false);
  game.dispose();

  const titleRates = [];
  const title = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    loadSfx: false,
    audio: {
      ...audio,
      update(extra = {}) {
        if (Number.isFinite(extra.bedRate)) titleRates.push(extra.bedRate);
      },
    },
  });
  assert.equal(title.observe().phase, "title");
  title.updateSettings({ gameSpeed: 0.5 });
  assert.equal(titleRates.at(-1), 1, "na porta a cama fica no relógio cheio");
  title.dispose();
});

test("advance ignora a velocidade da partida", () => {
  const { game } = harness();
  game.updateSettings({ gameSpeed: 0.5 });
  game.advance(10);
  assert.equal(game.observe().tick, 10, "o passo headless não dilata com o relógio");
  game.dispose();
});

test("preferências e progresso vivem em chaves separadas", () => {
  const { game, storage } = harness();
  game.updateSettings({ highContrast: true, reducedMotion: true, colorblind: true });
  game.advance(CONFIG.runTicks);
  storage.remove("progress");
  const reopened = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  assert.equal(reopened.settings.highContrast, true, "apagar a partida não apaga a preferência");
  assert.equal(reopened.settings.colorblind, true);
  assert.equal(reopened.progress.runs, 0);
  game.dispose();
  reopened.dispose();
});

test("a velocidade da partida sobrevive à reabertura", () => {
  const storage = memoryStorage();
  const { game } = harness({ storage });
  game.updateSettings({ gameSpeed: 0.75 });
  game.dispose();
  const reopened = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  assert.equal(reopened.settings.gameSpeed, 0.75);
  reopened.dispose();
});

test("beforeunload descarrega o tick sem pausar nem chamar isso de confiável", () => {
  const storage = memoryStorage();
  const { game, target } = harness({ storage });
  game.advance(40);
  const tick = game.observe().tick;
  assert.ok(tick > 0);
  const leave = target.listeners.find((entry) => entry.type === "beforeunload");
  assert.ok(leave, "beforeunload precisa de ouvinte");
  leave.handler();
  assert.equal(game.paused, false, "beforeunload descarrega sem pausar — a pausa é do hidden");
  const saved = JSON.parse(storage.get("progress"));
  assert.ok(saved.hold, "o tick precisa ficar no disco");
  assert.equal(saved.hold.tick, tick);
  assert.equal(game.persist.trusted, false);
  const reopened = createGame({ eventTarget: recordingTarget(), storage });
  assert.equal(reopened.observe().tick, tick, "a reabertura retoma o tick");
  assert.equal(reopened.persist.trusted, false);
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

test("a aba escondida pausa e descarrega", () => {
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

test("a perda de foco grava o hold que a receita já promete", () => {
  const storage = memoryStorage();
  const { game, target } = harness({ storage });
  game.advance(40);
  const tick = game.observe().tick;
  assert.ok(tick > 0);
  const leaves = target.listeners.filter((entry) => entry.type === "blur");
  assert.ok(leaves.length >= 1, "blur precisa de ouvinte — visibilitychange não é perda de foco");
  for (const leave of leaves) leave.handler();
  assert.equal(game.paused, true, "perder o foco senta o relógio");
  const saved = JSON.parse(storage.get("progress"));
  assert.ok(saved.hold, "o tick precisa ficar no disco");
  assert.equal(saved.hold.tick, tick);
  assert.equal(game.persist.trusted, false);
  const reopened = createGame({ eventTarget: recordingTarget(), storage });
  assert.equal(reopened.observe().tick, tick, "a reabertura retoma o tick");
  assert.equal(reopened.persist.trusted, false);
  game.dispose();
  reopened.dispose();
});

test("na porta a perda de foco não congela a mostra", () => {
  const storage = memoryStorage();
  const target = recordingTarget();
  const game = createGame({
    seed: 5,
    eventTarget: target,
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(game.observe().phase, "title");
  const leaves = target.listeners.filter((entry) => entry.type === "blur");
  assert.ok(leaves.length >= 1, "blur precisa de ouvinte");
  for (const leave of leaves) leave.handler();
  assert.equal(game.paused, false, "na porta o blur só descarrega");
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing", "o avanço ainda abre");
  assert.equal(game.persist.trusted, false);
  game.dispose();
});

function stubPad({ axes = [0], buttons = {} } = {}) {
  const list = Array.from({ length: 16 }, (_, index) => ({ pressed: Boolean(buttons[index]) }));
  return [{ axes, buttons: list }];
}

test("o controle que some senta o relógio que a sessão já falou", () => {
  const storage = memoryStorage();
  const target = recordingTarget();
  let pads = stubPad({ axes: [0.8] });
  const input = createInput({ target, gamepads: () => pads });
  input.intent();
  assert.equal(input.lastSource, "gamepad");
  const game = createGame({ seed: 5, eventTarget: target, storage, input });
  game.advance(40);
  const tick = game.observe().tick;
  assert.ok(tick > 0);
  const gone = target.listeners.find((entry) => entry.type === "gamepaddisconnected");
  assert.ok(gone, "gamepaddisconnected precisa de ouvinte — blur não é o pad");
  gone.handler();
  assert.equal(game.paused, true, "o pad que some senta o relógio");
  const saved = JSON.parse(storage.get("progress"));
  assert.ok(saved.hold, "o tick precisa ficar no disco");
  assert.equal(saved.hold.tick, tick);
  assert.equal(game.persist.trusted, false);
  const reopened = createGame({ eventTarget: recordingTarget(), storage });
  assert.equal(reopened.observe().tick, tick, "a reabertura retoma o tick");
  assert.equal(reopened.persist.trusted, false);
  game.dispose();
  reopened.dispose();
  input.dispose();
});

test("na porta o controle que some não congela a mostra", () => {
  const storage = memoryStorage();
  const target = recordingTarget();
  let pads = stubPad({ axes: [0.8] });
  const input = createInput({ target, gamepads: () => pads });
  input.intent();
  const game = createGame({
    seed: 5,
    eventTarget: target,
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
    input,
  });
  assert.equal(game.observe().phase, "title");
  const gone = target.listeners.find((entry) => entry.type === "gamepaddisconnected");
  assert.ok(gone, "gamepaddisconnected precisa de ouvinte");
  gone.handler();
  assert.equal(game.paused, false, "na porta o pad que some só descarrega");
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing", "o avanço ainda abre");
  assert.equal(game.persist.trusted, false);
  game.dispose();
  input.dispose();
});

test("o teclado não senta quando um pad na gaveta some", () => {
  const storage = memoryStorage();
  const { game, target } = harness({ storage });
  game.advance(40);
  const tick = game.observe().tick;
  const gone = target.listeners.find((entry) => entry.type === "gamepaddisconnected");
  assert.ok(gone, "o ouvinte existe mesmo na sessão de teclado");
  gone.handler();
  assert.equal(game.paused, false, "lastSource teclado não é sessão no controle");
  game.advance(1);
  assert.equal(game.observe().tick, tick + 1, "o relógio segue");
  assert.equal(game.persist.trusted, false);
  game.dispose();
});

test("na porta a aba escondida não congela a mostra sem chamar isso de confiável", () => {
  const storage = memoryStorage();
  const target = recordingTarget();
  const game = createGame({
    seed: 5,
    eventTarget: target,
    storage,
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(game.observe().phase, "title");
  game.updateSettings({ captions: false });
  storage.remove("settings");
  const change = target.listeners.find((entry) => entry.type === "visibilitychange");
  assert.ok(change);
  change.handler();
  assert.equal(game.paused, false, "na porta a aba só descarrega");
  assert.equal(JSON.parse(storage.get("settings")).captions, false);
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing", "o avanço ainda abre");
  game.advance(CONFIG.runTicks);
  assert.equal(game.observe().phase, "over");
  change.handler();
  assert.equal(game.paused, true, "no fim a aba continua sentando");
  assert.equal(game.persist.trusted, false);
  game.dispose();
});

test("trocar a chuva na porta troca a mostra e não abre o ciclo", () => {
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    loadSfx: false,
  });
  assert.equal(game.observe().phase, "title");
  assert.equal(game.observe().spawnProfile, "spawn");
  game.updateSettings({ spawnProfile: "dusk" });
  const after = game.observe();
  assert.equal(after.phase, "title", "outra mesa na porta não é beginRun");
  assert.equal(after.spawnProfile, "dusk");
  assert.equal(after.tick, 0);
  assert.equal(after.entities.length, 0);
  assert.equal(after.stats.dashes, 0);
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

test("a query não grava o look, a chuva nem o relógio", () => {
  const queries = {};
  const matchMedia = (text) => {
    if (!queries[text]) {
      const listeners = new Set();
      queries[text] = {
        matches: false,
        addEventListener(_, fn) { listeners.add(fn); },
        removeEventListener(_, fn) { listeners.delete(fn); },
        fire(next) {
          this.matches = next;
          for (const fn of listeners) fn();
        },
      };
    }
    return queries[text];
  };
  const storage = memoryStorage();
  const prior = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  prior.updateSettings({ look: "calm", spawnProfile: "calm", gameSpeed: 0.5 });
  prior.dispose();
  const { game, target } = harness({
    storage,
    query: "?look=dusk&spawn=dusk&speed=0.75",
    matchMedia,
  });
  assert.equal(game.settings.look, "dusk");
  assert.equal(game.settings.spawnProfile, "dusk");
  assert.equal(game.settings.gameSpeed, 0.75);
  const hide = target.listeners.find((entry) => entry.type === "pagehide");
  assert.ok(hide, "pagehide precisa de ouvinte");
  hide.handler();
  const afterHide = JSON.parse(storage.get("settings"));
  assert.equal(afterHide.look, "calm", "esconder não grava o look do convite");
  assert.equal(afterHide.spawnProfile, "calm", "esconder não grava a chuva do convite");
  assert.equal(afterHide.gameSpeed, 0.5, "esconder não grava o relógio do convite");
  matchMedia("(prefers-reduced-motion: reduce)").fire(true);
  const afterEnv = JSON.parse(storage.get("settings"));
  assert.equal(afterEnv.reducedMotion, true);
  assert.equal(afterEnv.look, "calm", "o sistema não grava o look que só vestiu");
  game.updateSettings({ captions: false });
  const afterOther = JSON.parse(storage.get("settings"));
  assert.equal(afterOther.captions, false);
  assert.equal(afterOther.look, "calm");
  assert.equal(afterOther.spawnProfile, "calm");
  assert.equal(afterOther.gameSpeed, 0.5);
  const reopened = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  assert.equal(reopened.settings.look, "calm");
  assert.equal(reopened.settings.spawnProfile, "calm");
  assert.equal(reopened.settings.gameSpeed, 0.5);
  assert.equal(reopened.settings.captions, false);
  game.dispose();
  reopened.dispose();
});

test("escolher o look na sessão do convite grava", () => {
  const storage = memoryStorage();
  const { game } = harness({ storage, query: "?look=dusk&speed=0.75" });
  assert.equal(game.settings.look, "dusk");
  game.flush();
  assert.equal(JSON.parse(storage.get("settings")).look, "normal");
  assert.equal(JSON.parse(storage.get("settings")).gameSpeed, 1);
  game.updateSettings({ look: "dusk" });
  assert.equal(JSON.parse(storage.get("settings")).look, "dusk");
  assert.equal(JSON.parse(storage.get("settings")).gameSpeed, 1, "escolher o look não grava o relógio vestido");
  const reopened = createGame({ seed: 5, eventTarget: recordingTarget(), storage });
  assert.equal(reopened.settings.look, "dusk");
  assert.equal(reopened.settings.gameSpeed, 1);
  game.dispose();
  reopened.dispose();
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

test("a query de chuva não retoma o hold de outra mesa", () => {
  const storage = memoryStorage();
  const live = createGame({ seed: 11, eventTarget: recordingTarget(), storage });
  live.advance(40);
  assert.equal(live.observe().spawnProfile, "spawn");
  live.flush();
  live.dispose();
  const named = createGame({
    query: "?spawn=dusk",
    eventTarget: recordingTarget(),
    storage,
  });
  assert.equal(named.observe().spawnProfile, "dusk");
  assert.equal(named.observe().tick, 0, "chuva na query não retoma o hold");
  assert.equal(named.observe().phase, "playing");
  named.dispose();
  const mood = createGame({
    query: "?mood=calm",
    eventTarget: recordingTarget(),
    storage,
  });
  assert.equal(mood.observe().spawnProfile, "calm");
  assert.equal(mood.observe().tick, 0, "o par na query também não retoma o hold");
  mood.dispose();
  const painted = createGame({
    query: "?look=dusk",
    eventTarget: recordingTarget(),
    storage,
  });
  assert.equal(painted.observe().tick, 40, "look na query veste o hold que já está");
  assert.equal(painted.observe().spawnProfile, "spawn");
  assert.equal(painted.settings.look, "dusk");
  painted.dispose();
  const clocked = createGame({
    query: "?speed=0.75",
    eventTarget: recordingTarget(),
    storage,
  });
  assert.equal(clocked.observe().tick, 40, "relógio na query veste o hold que já está");
  assert.equal(clocked.settings.gameSpeed, 0.75);
  clocked.dispose();
  const resumed = createGame({ eventTarget: recordingTarget(), storage });
  assert.equal(resumed.observe().tick, 40, "sem chuva na query o hold volta");
  assert.equal(resumed.observe().spawnProfile, "spawn");
  resumed.dispose();
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

test("com tela a porta pulsa o avanço, não o land", () => {
  const played = [];
  const game = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
    canvas: silentCanvas(),
    haptics: silentHaptics(played),
    loadSfx: false,
  });
  assert.equal(game.observe().phase, "title");
  game.act({ dash: true });
  game.advance(1);
  assert.equal(game.observe().phase, "playing");
  assert.ok(played.includes("dash"), `esperava o pulso da porta: ${JSON.stringify(played)}`);
  assert.equal(played.includes("land"), false, "o land não come o pulso da abertura");
  game.dispose();
});

test("o avanço pulsa no aparelho e a pausa cala o que ainda vibrava", () => {
  const played = [];
  const { game } = harness({ haptics: silentHaptics(played) });
  game.act({ dash: true });
  game.advance(1 + CONFIG.player.dashWindupTicks);
  assert.ok(played.includes("dash"), `esperava dash no pulso: ${JSON.stringify(played)}`);
  game.pause();
  assert.ok(played.includes("mute"), "pausar precisa calar o pulso");
  game.resume();
  assert.ok(played.includes("unmute"));
  game.dispose();
  assert.ok(played.includes("dispose"));
});

test("a outra aba veste as preferências", () => {
  const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");
  assert.match(html, /watchSettings\([\s\S]*sync\(\)/);

  const storage = memoryStorage();
  storage.prefix = "lab";
  const target = recordingTarget();
  const seen = [];
  const game = createGame({ seed: 5, eventTarget: target, storage });
  game.watchSettings((next) => { seen.push(next.look); });
  assert.equal(game.settings.look, "normal");

  storage.set("settings", JSON.stringify({ ...game.settings, look: "dusk", uiScale: 1.6 }));
  const onStorage = target.listeners.find((entry) => entry.type === "storage");
  assert.ok(onStorage, "storage precisa de ouvinte");
  onStorage.handler({ key: "lab:settings" });
  assert.equal(game.settings.look, "dusk");
  assert.equal(game.settings.uiScale, 1.6);
  assert.deepEqual(seen, ["dusk"]);

  onStorage.handler({ key: "lab:settings.tmp" });
  assert.equal(game.settings.look, "dusk", "tmp não veste");
  onStorage.handler({ key: "outro:settings" });
  assert.equal(game.settings.look, "dusk");
  game.dispose();
  assert.equal(target.listeners.length, 0);
});

test("o sistema que pede reduce no meio da sessão veste a caixa", () => {
  const queries = {};
  const matchMedia = (text) => {
    if (!queries[text]) {
      const listeners = new Set();
      queries[text] = {
        matches: false,
        addEventListener(_, fn) { listeners.add(fn); },
        removeEventListener(_, fn) { listeners.delete(fn); },
        fire(next) {
          this.matches = next;
          for (const fn of listeners) fn();
        },
      };
    }
    return queries[text];
  };
  const storage = memoryStorage();
  const seen = [];
  const game = createGame({ seed: 5, storage, matchMedia });
  game.watchSettings((next) => { seen.push(next.reducedMotion); });
  assert.equal(game.settings.reducedMotion, false);
  matchMedia("(prefers-reduced-motion: reduce)").fire(true);
  assert.equal(game.settings.reducedMotion, true);
  assert.deepEqual(seen, [true]);
  matchMedia("(prefers-reduced-motion: reduce)").fire(false);
  assert.equal(game.settings.reducedMotion, true, "desligar o sistema não apaga a caixa");
  const reopened = createGame({ seed: 5, storage, matchMedia });
  assert.equal(reopened.settings.reducedMotion, true, "o pedido ficou nas preferências");
  game.dispose();
  matchMedia("(prefers-contrast: more)").fire(true);
  assert.equal(game.settings.highContrast, false, "dispose some o ouvinte");
  reopened.dispose();
});

test("o jogo entrega a aba escondida à escuta do hold", () => {
  const main = readFileSync(new URL("../src/main.js", import.meta.url), "utf8");
  assert.match(main, /visibility:\s*options\.visibility/);
});
