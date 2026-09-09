// Um save é um contrato com o tempo do jogador. Estes testes cobrem a cadeia de
// migração, o dado inválido e a gravação que falha — os três caminhos que, sem
// prova, aparecem primeiro na mão de quem está jogando.

import { test } from "node:test";
import assert from "node:assert/strict";

import { memoryStorage, readJson, writeJson } from "../src/core/storage.js";
import {
  PROGRESS_KEY,
  PROGRESS_SCHEMA,
  defaultProgress,
  loadProgress,
  migrate,
  recordRun,
  saveProgress,
} from "../src/core/save.js";
import { defaultSettings, loadSettings, normalizeSettings } from "../src/core/settings.js";

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
  assert.equal("inventado" in settings, false);
});

test("preferências herdam a redução de movimento do sistema", () => {
  assert.equal(defaultSettings({ prefersReducedMotion: true }).reducedMotion, true);
  assert.equal(defaultSettings({}).reducedMotion, false);
});

test("um campo inválido preserva o valor atual, não o padrão", () => {
  const current = { ...defaultSettings({}), uiScale: 1.5 };
  const settings = normalizeSettings({ ...current, uiScale: "grande" }, {}, current);
  assert.equal(settings.uiScale, 1.5);
});

test("preferências ilegíveis são recuperadas com o padrão", () => {
  const storage = memoryStorage();
  storage.set("settings", "]{");
  const load = loadSettings(storage, {});
  assert.equal(load.status, "recovered");
  assert.deepEqual(load.settings.bindings, defaultSettings({}).bindings);
});
