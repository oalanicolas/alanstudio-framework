// Mesas de conteúdo. A regra e a apresentação consomem; não embutem.
//
// Uma mesa nova entra pelo comando: `npm run table -- <nome>`. Ele
// escreve o JSON e registra o nome abaixo. Alterar um JSON não
// republica o verbo. Sem consumidor a mesa existe e o jogo não muda.

import spawn from "../../data/spawn.json" with { type: "json" };
import copy from "../../data/copy.json" with { type: "json" };

const TABLES = { spawn, copy };

export function loadTable(name) {
  if (!(name in TABLES)) {
    throw new Error(`mesa desconhecida: ${name}`);
  }
  return TABLES[name];
}

export function requireFields(name, fields) {
  const table = loadTable(name);
  const missing = fields.filter((field) => table[field] === undefined);
  if (missing.length) {
    throw new Error(`mesa ${name} sem ${missing.join(", ")}`);
  }
  return table;
}

export { spawn, copy, TABLES };
