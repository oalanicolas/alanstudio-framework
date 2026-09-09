import { test } from "node:test";
import assert from "node:assert/strict";

import { loadTable, requireFields, TABLES } from "../src/game/tables.js";

test("as duas mesas passam pelo mesmo carregador", () => {
  assert.deepEqual(Object.keys(TABLES).sort(), ["copy", "spawn"]);
  assert.equal(loadTable("spawn").intervalTicks, 22);
  assert.equal(loadTable("copy").chain, "Corrente");
  assert.throws(() => loadTable("inventada"), /mesa desconhecida/);
});

test("campo obrigatório ausente falha com o nome da mesa e do campo", () => {
  assert.equal(requireFields("spawn", ["intervalTicks"]).intervalTicks, 22);
  assert.throws(() => requireFields("spawn", ["inventado"]), /mesa spawn sem inventado/);
});
