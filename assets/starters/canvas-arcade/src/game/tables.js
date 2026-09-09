// Mesas de conteúdo. A regra e a apresentação consomem; não embutem.
//
// Uma mesa nova entra pelo comando: `npm run table -- <nome>`. Ele
// escreve o JSON e registra o nome abaixo. Alterar um JSON não
// republica o verbo. Sem consumidor a mesa existe e o jogo não muda.
//
// spawn tem schema: formato antigo (sem campo) vira 1; schema futuro
// falha com o número, não com undefined no meio do tick.

import spawnRaw from "../../data/spawn.json" with { type: "json" };
import copy from "../../data/copy.json" with { type: "json" };

export const SPAWN_SCHEMA = 1;
export const SPAWN_FIELDS = [
  "intervalTicks",
  "minIntervalTicks",
  "rampTicks",
  "hazardChanceStart",
  "hazardChanceEnd",
  "fallSpeedMin",
  "fallSpeedMax",
];

export function migrateSpawn(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
    throw new Error("mesa spawn ilegível");
  }
  const schema = Number.isInteger(raw.schema) ? raw.schema : 0;
  if (schema > SPAWN_SCHEMA) {
    throw new Error(`mesa spawn schema ${schema} não suportado (máximo ${SPAWN_SCHEMA})`);
  }
  return { ...raw, schema: SPAWN_SCHEMA };
}

const spawn = migrateSpawn(spawnRaw);

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
