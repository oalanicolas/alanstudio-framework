import { test } from "node:test";
import assert from "node:assert/strict";

import {
  applySpawnIntent, loadTable, loadSpawn, listSpawnIntents, listSpawnProfiles, looksLikeSpawn,
  migrateCopy, migrateSpawn, migrateTable, requireFields, resolveSpawnName, spawnRecord, TABLES,
  SPAWN_FIELDS, SPAWN_SCHEMA, COPY_SCHEMA, COPY_FIELDS, SPAWN_INTENTS,
} from "../src/game/tables.js";

test("as mesas passam pelo mesmo carregador", () => {
  assert.deepEqual(Object.keys(TABLES).sort(), ["copy", "dusk", "spawn"]);
  assert.equal(loadTable("spawn").intervalTicks, 22);
  assert.equal(loadTable("spawn").schema, SPAWN_SCHEMA);
  assert.equal(loadTable("dusk").intervalTicks, 16);
  assert.equal(loadTable("copy").chain, "Corrente");
  assert.equal(loadTable("copy").schema, COPY_SCHEMA);
  assert.throws(() => loadTable("inventada"), /mesa desconhecida/);
});

test("só mesa com forma de chuva entra na família jogável", () => {
  assert.deepEqual(listSpawnProfiles(), ["dusk", "spawn"]);
  assert.equal(loadSpawn("dusk").intervalTicks, 16);
  assert.equal(loadSpawn("dusk").practiceTicks, 90);
  assert.equal(resolveSpawnName("dusk"), "dusk");
  assert.equal(resolveSpawnName("copy"), "spawn");
  assert.equal(resolveSpawnName("inventada"), "spawn");
  assert.equal(looksLikeSpawn(loadTable("copy")), false);
  assert.throws(() => loadSpawn("copy"), /não é perfil de chuva/);
  assert.throws(() => loadSpawn("inventada"), /não é perfil de chuva/);
});

test("campo obrigatório ausente falha com o nome da mesa e do campo", () => {
  assert.equal(requireFields("spawn", ["intervalTicks"]).intervalTicks, 22);
  assert.throws(() => requireFields("spawn", ["inventado"]), /mesa spawn sem inventado/);
});

test("spawn sem schema migra; schema futuro falha com o número", () => {
  const old = migrateSpawn({ intervalTicks: 22, minIntervalTicks: 11 });
  assert.equal(old.schema, SPAWN_SCHEMA);
  assert.equal(old.intervalTicks, 22);
  assert.equal(old.practiceTicks, 240);
  assert.equal(old.recoveryTicks, 90);
  assert.throws(() => migrateSpawn({ schema: 9 }), /mesa spawn schema 9 não suportado/);
  assert.throws(() => migrateSpawn(null), /mesa spawn ilegível/);
});

test("a intenção desloca knobs sem inventar mesa nem aprovar chuva", () => {
  const spawn = loadSpawn("spawn");
  const denser = applySpawnIntent(spawn, "denser");
  const calmer = applySpawnIntent(spawn, "calmer");
  const brief = applySpawnIntent(spawn, "brief");
  assert.deepEqual(listSpawnIntents(), Object.keys(SPAWN_INTENTS));
  assert.ok(denser.intervalTicks < spawn.intervalTicks);
  assert.ok(denser.practiceTicks < spawn.practiceTicks);
  assert.ok(denser.hazardChanceEnd > spawn.hazardChanceEnd);
  assert.ok(calmer.intervalTicks > spawn.intervalTicks);
  assert.ok(calmer.practiceTicks > spawn.practiceTicks);
  assert.ok(brief.practiceTicks < spawn.practiceTicks);
  assert.ok(brief.rampTicks < spawn.rampTicks);
  assert.ok(denser.minIntervalTicks <= denser.intervalTicks);
  assert.ok(looksLikeSpawn(denser));
  assert.deepEqual(Object.keys(spawnRecord(denser)), ["schema", ...SPAWN_FIELDS]);
  assert.equal(spawnRecord(denser).schema, SPAWN_SCHEMA);
  assert.throws(() => applySpawnIntent(spawn, "melhor"), /intenção desconhecida/);
});

test("copy sem schema migra; schema futuro e campo ausente falham com o nome", () => {
  const old = migrateCopy({ paused: "Pausado" });
  assert.equal(old.schema, COPY_SCHEMA);
  assert.equal(old.fantasy, "");
  assert.throws(() => migrateTable("copy", { schema: 4 }, COPY_SCHEMA), /mesa copy schema 4 não suportado/);
  assert.throws(
    () => migrateTable("copy", { schema: 1 }, COPY_SCHEMA, COPY_FIELDS),
    /mesa copy sem fantasy/,
  );
});
