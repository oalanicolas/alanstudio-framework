// Mesas de conteúdo. A regra e a apresentação consomem; não embutem.
//
// Uma mesa nova entra aqui. Alterar um JSON não republica o verbo.

import spawn from "../../data/spawn.json" with { type: "json" };
import copy from "../../data/copy.json" with { type: "json" };

const TABLES = { spawn, copy };

export function loadTable(name) {
  if (!(name in TABLES)) {
    throw new Error(`mesa desconhecida: ${name}`);
  }
  return TABLES[name];
}

export { spawn, copy, TABLES };
