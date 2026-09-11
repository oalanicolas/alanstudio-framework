// Um save é um contrato com o tempo do jogador. Estes testes cobrem a cadeia de
// migração, o dado inválido e a gravação que falha — os três caminhos que, sem
// prova, aparecem primeiro na mão de quem está jogando.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { browserStorage, foreignKey, memoryStorage, readJson, writeJson } from "../src/core/storage.js";
import { createGame } from "../src/main.js";
import {
  PROGRESS_KEY,
  PROGRESS_SCHEMA,
  defaultProgress,
  loadProgress,
  migrate,
  canContinue,
  canResume,
  captureHold,
  persistLine,
  persistStatus,
  recordRun,
  saveProgress,
} from "../src/core/save.js";
import {
  applyEnvironment,
  applyOneHand,
  DEFAULT_BINDINGS,
  DEFAULT_BUSES,
  ENVIRONMENT_QUERIES,
  ONE_HAND_BINDINGS,
  defaultSettings,
  detectEnvironment,
  loadSettings,
  settingsLine,
  normalizeSettings,
  watchEnvironment,
} from "../src/core/settings.js";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");

test("ausência de save começa do zero sem erro", () => {
  const result = migrate(null);
  assert.equal(result.status, "absent");
  assert.deepEqual(result.progress, defaultProgress());
});

test("save da versão 1 é migrado preservando o recorde", () => {
  const result = migrate({ schema: 1, highScore: 420 });
  assert.equal(result.status, "migrated");
  assert.equal(result.from, 1);
  assert.equal(result.progress.schema, PROGRESS_SCHEMA);
  assert.equal(result.progress.best, 420);
  assert.match(result.notes.join(" "), /migrado de schema 1/);
});

test("save sem versão é tratado como o formato mais antigo", () => {
  const result = migrate({ highScore: 7 });
  assert.equal(result.progress.best, 7);
  assert.equal(result.from, 0);
});

test("campos fora de faixa são recuperados, não aceitos", () => {
  const result = migrate({ schema: 2, best: -5, bestChain: "muito", runs: 3.7 });
  assert.equal(result.progress.best, 0);
  assert.equal(result.progress.bestChain, 0);
  assert.equal(result.progress.runs, 3);
  assert.match(result.notes.join(" "), /fora de faixa/);
});

test("save de versão futura bloqueia a gravação em vez de ser sobrescrito", () => {
  const storage = memoryStorage();
  const original = JSON.stringify({ schema: PROGRESS_SCHEMA + 1, best: 900, algoNovo: true });
  storage.set(PROGRESS_KEY, original);
  const load = loadProgress(storage);
  assert.equal(load.status, "blocked");
  const write = saveProgress(storage, { best: 1 }, load);
  assert.equal(write.ok, false);
  assert.equal(write.reason, "future_schema");
  assert.equal(storage.get(PROGRESS_KEY), original, "o progresso da versão futura sobrevive intacto");
});

test("save ilegível é preservado em vez de descartado", () => {
  const storage = memoryStorage();
  storage.set(PROGRESS_KEY, "{isto não é json");
  const load = loadProgress(storage);
  assert.equal(load.status, "recovered");
  assert.equal(load.progress.best, 0);
  assert.equal(storage.get(`${PROGRESS_KEY}.broken`), "{isto não é json");
});

test("valor que não é objeto também vira recuperação", () => {
  const storage = memoryStorage();
  storage.set("chave", "42");
  const read = readJson(storage, "chave");
  assert.equal(read.status, "unreadable");
  assert.equal(storage.get("chave.broken"), "42");
});

for (const key of ["progress", "settings"]) {
  test(`o jogo abre com ${key} corrompido e sem espaço para o backup`, (t) => {
    const original = "{" + "x".repeat(500);
    const prefix = "recovery-fixture";
    const fullKey = `${prefix}:${key}`;
    const data = new Map([[fullKey, original]]);
    let capacity = original.length + 1; // cabe o probe, mas não a cópia do save
    const previous = Object.getOwnPropertyDescriptor(globalThis, "localStorage");
    Object.defineProperty(globalThis, "localStorage", {
      configurable: true,
      value: {
        getItem: (name) => data.get(name) ?? null,
        removeItem: (name) => data.delete(name),
        setItem(name, value) {
          const proposed = new Map(data).set(name, String(value));
          const size = [...proposed.values()].reduce((sum, item) => sum + item.length, 0);
          if (size > capacity) throw new Error("QuotaExceededError");
          data.set(name, String(value));
        },
      },
    });
    t.after(() => {
      if (previous) Object.defineProperty(globalThis, "localStorage", previous);
      else delete globalThis.localStorage;
    });
    const storage = browserStorage(prefix);
    assert.equal(storage.persistent, true);
    const game = createGame({ storage, seed: 42 });
    t.after(() => game.dispose());
    assert.equal(game.observe().tick, 0);
    if (key === "progress") {
      assert.match(game.progress.notes.join(" "), /gravação bloqueada/);
      game.advance(3600);
      assert.equal(game.progress.runs, 1);
    } else {
      game.updateSettings({ uiScale: 1.5 });
      assert.equal(game.settings.uiScale, 1.5);
    }
    assert.equal(data.get(fullKey), original, "o uso do jogo não apaga o único original");
    assert.equal(data.has(`${fullKey}.broken`), false);
    const blocked = writeJson(storage, key, { recovered: true });
    assert.equal(blocked.ok, false);
    assert.equal(blocked.reason, "backup_failed");
    capacity = 10_000;
    assert.deepEqual(writeJson(storage, key, { recovered: true }), { ok: true });
    assert.equal(data.get(`${fullKey}.broken`), original);
    assert.deepEqual(JSON.parse(data.get(fullKey)), { recovered: true });
  });
}

test("backup que não persiste também impede apagar o save original", () => {
  const original = "{save corrompido";
  const stored = memoryStorage({ progress: original });
  const storage = {
    ...stored,
    set(key, value) {
      if (key !== "progress.broken") stored.set(key, value);
    },
  };
  const read = readJson(storage, "progress");
  assert.equal(read.status, "unreadable");
  assert.equal(read.backupSaved, false);
  assert.equal(writeJson(storage, "progress", defaultProgress()).reason, "backup_failed");
  assert.equal(storage.get("progress"), original);
});

test("a outra aba nomeia a chave desta página", () => {
  assert.equal(foreignKey({ key: "lab:settings" }, "lab", "settings"), true);
  assert.equal(foreignKey({ key: "lab:settings.tmp" }, "lab", "settings"), false);
  assert.equal(foreignKey({ key: "lab:progress" }, "lab", "settings"), false);
  assert.equal(foreignKey({ key: "outro:settings" }, "lab", "settings"), false);
  assert.equal(foreignKey({ key: "lab:settings" }, "", "settings"), false);
  assert.equal(foreignKey({}, "lab", "settings"), false);
});

test("a gravação verifica antes de promover e não deixa rastro temporário", () => {
  const storage = memoryStorage();
  assert.deepEqual(writeJson(storage, "chave", { a: 1 }), { ok: true });
  assert.deepEqual(JSON.parse(storage.get("chave")), { a: 1 });
  assert.equal(storage.get("chave.tmp"), null);
});

test("gravação que não persiste é detectada, não presumida", () => {
  const storage = { ...memoryStorage(), set() {}, get: () => null, remove() {} };
  const result = writeJson(storage, "chave", { a: 1 });
  assert.equal(result.ok, false);
  assert.equal(result.reason, "verification_failed");
});

test("cota cheia falha sem derrubar o jogo", () => {
  const dropped = [];
  const storage = {
    get: () => null,
    set() {
      throw new Error("QuotaExceededError");
    },
    remove(key) {
      dropped.push(key);
    },
    keys: () => [],
  };
  const result = writeJson(storage, "chave", { a: 1 });
  assert.equal(result.ok, false);
  assert.equal(result.reason, "write_failed");
  assert.deepEqual(dropped, ["chave.tmp"], "a chave temporária é limpa mesmo na falha");
});

test("sessão volátil e gravação recusada têm linha, sem chamar isso de confiável", () => {
  const memory = persistStatus(memoryStorage(), { ok: true });
  assert.equal(memory.durable, false);
  assert.equal(memory.wrote, true);
  assert.equal(memory.trusted, false);
  assert.equal(persistLine(memory, { title_volatile: "Esta sessão não grava" }), "Esta sessão não grava");
  const failed = persistStatus({ persistent: true }, { ok: false, reason: "write_failed" });
  assert.equal(failed.durable, true);
  assert.equal(failed.wrote, false);
  assert.equal(failed.trusted, false);
  assert.equal(persistLine(failed, { title_unsaved: "A última gravação não ficou" }), "A última gravação não ficou");
  const ok = persistStatus({ persistent: true }, { ok: true });
  assert.equal(ok.durable, true);
  assert.equal(ok.wrote, true);
  assert.equal(ok.trusted, false);
  assert.equal(persistLine(ok, { title_volatile: "Esta sessão não grava", title_unsaved: "A última gravação não ficou" }), "");
  assert.equal(persistLine(null, { title_volatile: "x" }), "");
});

test("valor não serializável é recusado antes de tocar o armazenamento", () => {
  const storage = memoryStorage();
  const circular = {};
  circular.self = circular;
  assert.equal(writeJson(storage, "chave", circular).reason, "unserializable");
  assert.deepEqual(storage.keys(), []);
});

test("recordRun mantém os máximos e conta a partida", () => {
  const progress = { ...defaultProgress(), best: 100, bestChain: 6, runs: 2 };
  const next = recordRun(progress, { score: 40, seed: 3, stats: { bestChain: 9 } });
  assert.equal(next.best, 100);
  assert.equal(next.bestChain, 9);
  assert.equal(next.runs, 3);
  assert.equal(next.lastSeed, 3);
  assert.equal(next.lastRun.score, 40);
  assert.equal(next.lastRun.bestChain, 9);
  assert.equal(next.lastRun.look, "normal");
  assert.equal(next.lastRun.speed, 1);
  assert.equal(canContinue(progress), false, "sem lastSeed não há o que repetir");
  assert.equal(canContinue(next), true);
  assert.equal(canContinue({ ...next, lastSeed: null }), false);
  assert.equal(next.hold, null);
  assert.equal(canResume(next), false, "terminar a partida não é retomar o tick");
});

test("o save relê a curva que o last-run já traçou", () => {
  const result = migrate({
    schema: PROGRESS_SCHEMA,
    best: 12,
    runs: 1,
    lastSeed: 8,
    lastRun: {
      seed: 8,
      score: 12,
      ticks: 400,
      curve: { never_banked: true, unbanked_at_end: 3 },
    },
  });
  assert.equal(result.progress.lastRun.score, 12);
  assert.deepEqual(result.progress.lastRun.curve, { never_banked: true, unbanked_at_end: 3 });
  assert.equal(result.progress.lastRun.speed, 1);
});

test("o save relê o relógio que o last-run já guardou", () => {
  const result = migrate({
    schema: PROGRESS_SCHEMA,
    best: 12,
    runs: 1,
    lastSeed: 8,
    lastRun: {
      seed: 8,
      score: 12,
      ticks: 400,
      speed: 0.75,
    },
  });
  assert.equal(result.progress.lastRun.speed, 0.75);
});

test("schema 2 ganha hold vazio ao subir", () => {
  const result = migrate({ schema: 2, best: 10, runs: 1, lastSeed: 3 });
  assert.equal(result.status, "migrated");
  assert.equal(result.progress.schema, PROGRESS_SCHEMA);
  assert.equal(result.progress.hold, null);
  assert.equal(result.progress.best, 10);
  assert.equal(canResume(result.progress), false);
});

test("hold inválido não vira retomar", () => {
  assert.equal(canResume({ hold: { tick: 4 } }), false);
  assert.equal(canResume({ hold: { seed: 1, rngState: 2, tick: 4 } }), false);
  assert.equal(captureHold({ phase: "title", tick: 8, player: { x: 1 }, entities: [] }), null);
  assert.equal(captureHold({ phase: "playing", tick: 0, player: { x: 1 }, entities: [] }), null);
});

test("o hold leva o relógio da porta", () => {
  const hold = captureHold({
    phase: "playing",
    seed: 7,
    rngState: 3,
    tick: 12,
    score: 0,
    chain: 0,
    hitstop: 0,
    shake: 0,
    flash: 0,
    camera: { x: 0, y: 0 },
    bankLock: 0,
    bankBuffer: 0,
    bankWindup: 0,
    spawnTimer: 4,
    recoverUntil: 0,
    nextId: 1,
    attractTick: 108,
    player: {
      x: 160,
      dir: 1,
      dashTicks: 0,
      dashRecovery: 0,
      dashCooldown: 0,
      dashBuffer: 0,
      dashWindup: 0,
      invuln: 0,
      squash: 0,
    },
    entities: [{ id: 1, kind: "orb", x: 40, y: 20, vy: 1 }],
    stats: {},
  });
  assert.ok(hold);
  assert.equal(hold.attractTick, 108);
  const again = captureHold({ ...hold, phase: "playing" });
  assert.equal(again.attractTick, 108, "relê o mesmo relógio");
});

test("preferências recusam valor fora de faixa e campo desconhecido", () => {
  const settings = normalizeSettings({
    uiScale: 12,
    buses: { master: 4, sfx: -1 },
    reducedMotion: "sim",
    inventado: true,
  });
  assert.equal(settings.uiScale, 2);
  assert.equal(settings.buses.master, 1);
  assert.equal(settings.buses.sfx, 0);
  assert.equal(settings.reducedMotion, false, "tipo errado cai no padrão");
  assert.equal(settings.assist, false);
  assert.equal("inventado" in settings, false);
});

test("o palco padrão é o mesmo objeto que o mixer declara", () => {
  assert.deepEqual(defaultSettings({}).buses, DEFAULT_BUSES);
  assert.ok(DEFAULT_BUSES.master < 0.8, "folga no master: overlap não usa o teto antigo");
  assert.ok(DEFAULT_BUSES.sfx < 0.9);
});

test("assistência é preferência persistida, não um modo escondido", () => {
  const settings = normalizeSettings({ assist: true });
  assert.equal(settings.assist, true);
  assert.equal(normalizeSettings({ assist: "sim" }).assist, false);
});

test("velocidade da partida é preferência persistida, não um modo escondido", () => {
  const settings = normalizeSettings({ gameSpeed: 0.75 });
  assert.equal(settings.gameSpeed, 0.75);
  assert.equal(normalizeSettings({ gameSpeed: "lento" }).gameSpeed, 1);
  assert.equal(normalizeSettings({ gameSpeed: 12 }).gameSpeed, 1);
  assert.equal(normalizeSettings({ gameSpeed: 0.1 }).gameSpeed, 0.5);
  assert.equal(defaultSettings({}).gameSpeed, 1);
});

test("preferências herdam a redução de movimento do sistema", () => {
  assert.equal(defaultSettings({ prefersReducedMotion: true }).reducedMotion, true);
  assert.equal(defaultSettings({}).reducedMotion, false);
});

test("o ambiente nomeia o ponteiro grosso sem vestir preferência", () => {
  const previous = globalThis.matchMedia;
  globalThis.matchMedia = (query) => ({
    matches: String(query).includes("pointer: coarse"),
    media: query,
    addEventListener() {},
    removeEventListener() {},
  });
  try {
    const env = detectEnvironment();
    assert.equal(env.pointer.coarse, true);
    assert.deepEqual(applyEnvironment(defaultSettings(), env), {});
    assert.equal("prefersReducedMotion" in ENVIRONMENT_QUERIES, true);
    assert.equal("pointer" in ENVIRONMENT_QUERIES, false);
  } finally {
    if (previous === undefined) delete globalThis.matchMedia;
    else globalThis.matchMedia = previous;
  }
});

test("o sistema que pede reduce no meio da sessão veste, e desligar não apaga", () => {
  const off = defaultSettings({});
  assert.deepEqual(applyEnvironment(off, { prefersReducedMotion: true }), { reducedMotion: true });
  assert.deepEqual(applyEnvironment({ ...off, reducedMotion: true }, { prefersReducedMotion: true }), {});
  assert.deepEqual(applyEnvironment({ ...off, reducedMotion: true }, { prefersReducedMotion: false }), {});
  assert.deepEqual(applyEnvironment(off, { prefersHighContrast: true }), { highContrast: true });
  assert.deepEqual(applyEnvironment(off, { prefersReducedMotion: false, prefersHighContrast: false }), {});

  const queries = {};
  const media = (text) => {
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
        count() { return listeners.size; },
      };
    }
    return queries[text];
  };
  const seen = [];
  const stop = watchEnvironment((env) => seen.push(env), media);
  assert.equal(queries[ENVIRONMENT_QUERIES.prefersReducedMotion].count(), 1);
  queries[ENVIRONMENT_QUERIES.prefersReducedMotion].fire(true);
  assert.deepEqual(seen, [{ prefersReducedMotion: true }]);
  queries[ENVIRONMENT_QUERIES.prefersHighContrast].fire(true);
  assert.deepEqual(seen[1], { prefersHighContrast: true });
  stop();
  queries[ENVIRONMENT_QUERIES.prefersReducedMotion].fire(false);
  assert.equal(seen.length, 2, "dispose some o ouvinte");
  assert.equal(typeof watchEnvironment(null, media), "function");
});

test("um campo inválido preserva o valor atual, não o padrão", () => {
  const current = { ...defaultSettings({}), uiScale: 1.5 };
  const settings = normalizeSettings({ ...current, uiScale: "grande" }, {}, current);
  assert.equal(settings.uiScale, 1.5);
});

test("o perfil de chuva é preferência persistida, não um modo escondido", () => {
  const settings = normalizeSettings({ spawnProfile: "dusk" });
  assert.equal(settings.spawnProfile, "dusk");
  assert.equal(normalizeSettings({ spawnProfile: "Tempo-1" }).spawnProfile, "spawn");
  assert.equal(normalizeSettings({ spawnProfile: 3 }).spawnProfile, "spawn");
  assert.equal(defaultSettings({}).spawnProfile, "spawn");
});

test("o look de arte é preferência persistida, não um modo escondido", () => {
  const settings = normalizeSettings({ look: "dusk" });
  assert.equal(settings.look, "dusk");
  assert.equal(normalizeSettings({ look: "Tempo-1" }).look, "normal");
  assert.equal(normalizeSettings({ look: 3 }).look, "normal");
  assert.equal(defaultSettings({}).look, "normal");
});

test("a tinta estável é preferência persistida, não um look", () => {
  assert.equal(defaultSettings({}).colorblind, false);
  assert.equal(normalizeSettings({ colorblind: true }).colorblind, true);
  assert.equal(normalizeSettings({ colorblind: "sim" }).colorblind, false);
  const current = { ...defaultSettings({}), colorblind: true };
  assert.equal(normalizeSettings({ colorblind: "sim" }, {}, current).colorblind, true);
});

test("o preset de uma mão usa o cluster direito sem colidir", () => {
  const codes = Object.values(ONE_HAND_BINDINGS).flat();
  assert.deepEqual(
    Object.keys(ONE_HAND_BINDINGS),
    Object.keys(DEFAULT_BINDINGS),
  );
  assert.equal(new Set(codes).size, codes.length, "duas ações não compartilham tecla");
  assert.deepEqual(ONE_HAND_BINDINGS.left, ["KeyJ"]);
  assert.deepEqual(ONE_HAND_BINDINGS.right, ["KeyL"]);
  assert.deepEqual(ONE_HAND_BINDINGS.dash, ["KeyI"]);
  assert.deepEqual(ONE_HAND_BINDINGS.bank, ["KeyK"]);
  assert.deepEqual(ONE_HAND_BINDINGS.pause, ["KeyP"]);
  assert.deepEqual(ONE_HAND_BINDINGS.reset, ["KeyO"]);
  const settings = normalizeSettings({ oneHand: true, bindings: ONE_HAND_BINDINGS });
  assert.equal(settings.oneHand, true);
  assert.deepEqual(settings.bindings, ONE_HAND_BINDINGS);
  assert.deepEqual(settings.keptBindings, DEFAULT_BINDINGS, "save antigo no preset não inventa remap");
  assert.equal(defaultSettings({}).oneHand, false);
  assert.deepEqual(defaultSettings({}).keptBindings, DEFAULT_BINDINGS);
});

test("desligar uma mão devolve o remap, não o padrão", () => {
  const remapped = { ...DEFAULT_BINDINGS, dash: ["KeyZ"] };
  let settings = normalizeSettings({ bindings: remapped });
  assert.deepEqual(settings.keptBindings.dash, ["KeyZ"]);
  settings = normalizeSettings({ ...settings, ...applyOneHand(settings, true) });
  assert.equal(settings.oneHand, true);
  assert.deepEqual(settings.bindings, ONE_HAND_BINDINGS);
  assert.deepEqual(settings.keptBindings.dash, ["KeyZ"]);
  settings = normalizeSettings({ ...settings, ...applyOneHand(settings, true) });
  assert.deepEqual(settings.keptBindings.dash, ["KeyZ"], "ligar de novo não come o conjunto já guardado");
  settings = normalizeSettings({ ...settings, ...applyOneHand(settings, false) });
  assert.equal(settings.oneHand, false);
  assert.deepEqual(settings.bindings.dash, ["KeyZ"]);
});

test("save antigo no preset devolve o padrão ao desligar", () => {
  const loaded = normalizeSettings({ oneHand: true, bindings: ONE_HAND_BINDINGS });
  const restored = normalizeSettings({ ...loaded, ...applyOneHand(loaded, false) });
  assert.equal(restored.oneHand, false);
  assert.deepEqual(restored.bindings, DEFAULT_BINDINGS);
});

test("a página devolve o remap ao desligar uma mão", () => {
  assert.match(html, /applyOneHand/);
  assert.match(html, /keptBindings/);
  assert.doesNotMatch(html, /DEFAULT_BINDINGS|ONE_HAND_BINDINGS/);
});

test("preferências ilegíveis são recuperadas com o padrão", () => {
  const storage = memoryStorage();
  storage.set("settings", "]{");
  const load = loadSettings(storage, {});
  assert.equal(load.status, "recovered");
  assert.deepEqual(load.settings.bindings, defaultSettings({}).bindings);
  assert.equal(storage.get("settings.broken"), "]{");
  assert.match(load.notes[0], /settings\.broken/);
  assert.equal(
    settingsLine(load, { settings_recovered: "As preferências voltaram ao padrão" }),
    "As preferências voltaram ao padrão",
  );
  assert.equal(settingsLine({ status: "loaded", notes: [] }, { settings_recovered: "x" }), "");
  assert.equal(
    persistLine({ durable: true, wrote: true, trusted: false }, { settings_recovered: "x", title_volatile: "volátil" }),
    "",
    "persistLine continua só sessão; settingsLine nomeia a recuperação",
  );
});
