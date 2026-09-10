// O harness fala de pause, reset, seed, observe, act, advance, capture e
// dispose como vocabulário de inspeção. Aqui cada um é exercitado: é este
// arquivo que separa "mencionado" de "demonstrado".

import { test } from "node:test";
import assert from "node:assert/strict";

import { createGame } from "../src/main.js";
import { memoryStorage } from "../src/core/storage.js";
import { canResume } from "../src/core/save.js";
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
  const painted = createGame({
    seed: 5,
    eventTarget: recordingTarget(),
    storage: memoryStorage(),
  });
  painted.updateSettings({ look: "dusk" });
  painted.advance(CONFIG.runTicks);
  assert.equal(painted.lastRun.look, "dusk");
  assert.equal(painted.lastRun.spawn, "spawn");
  painted.dispose();
  game.dispose();
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
  game.advance(1 + CONFIG.player.dashWindupTicks);
  assert.ok(played.includes("dash"), `esperava dash no pulso: ${JSON.stringify(played)}`);
  game.pause();
  assert.ok(played.includes("mute"), "pausar precisa calar o pulso");
  game.resume();
  assert.ok(played.includes("unmute"));
  game.dispose();
  assert.ok(played.includes("dispose"));
});
