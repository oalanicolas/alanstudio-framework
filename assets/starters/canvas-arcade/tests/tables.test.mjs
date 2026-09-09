import { test } from "node:test";
import assert from "node:assert/strict";

import { loadTable, TABLES } from "../src/game/tables.js";

test("as duas mesas passam pelo mesmo carregador", () => {
  assert.deepEqual(Object.keys(TABLES).sort(), ["copy", "spawn"]);
  assert.equal(loadTable("spawn").intervalTicks, 22);
  assert.equal(loadTable("copy").chain, "Corrente");
  assert.throws(() => loadTable("inventada"), /mesa desconhecida/);
});
