import { test } from "node:test";
import assert from "node:assert/strict";

import { loadTable, migrateSpawn, requireFields, TABLES, SPAWN_SCHEMA } from "../src/game/tables.js";

test("as duas mesas passam pelo mesmo carregador", () => {
  assert.deepEqual(Object.keys(TABLES).sort(), ["copy", "spawn"]);
  assert.equal(loadTable("spawn").intervalTicks, 22);
  assert.equal(loadTable("spawn").schema, SPAWN_SCHEMA);
  assert.equal(loadTable("copy").chain, "Corrente");
  assert.throws(() => loadTable("inventada"), /mesa desconhecida/);
});

test("campo obrigatório ausente falha com o nome da mesa e do campo", () => {
  assert.equal(requireFields("spawn", ["intervalTicks"]).intervalTicks, 22);
  assert.throws(() => requireFields("spawn", ["inventado"]), /mesa spawn sem inventado/);
});

test("spawn sem schema migra; schema futuro falha com o número", () => {
  const old = migrateSpawn({ intervalTicks: 22, minIntervalTicks: 11 });
  assert.equal(old.schema, SPAWN_SCHEMA);
  assert.equal(old.intervalTicks, 22);
  assert.throws(() => migrateSpawn({ schema: 9 }), /mesa spawn schema 9 não suportado/);
  assert.throws(() => migrateSpawn(null), /mesa spawn ilegível/);
});
