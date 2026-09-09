// Mesas de conteúdo. A regra e a apresentação consomem; não embutem.
//
// Uma mesa nova entra pelo comando: `npm run table -- <nome>`. Ele
// escreve o JSON com schema e registra o nome abaixo. Alterar um JSON
// não republica o verbo. Sem consumidor a mesa existe e o jogo não muda.
//
// Toda mesa tem schema: formato antigo (sem campo) vira 1; schema
// futuro falha com o número, não com undefined no meio do tick.

import spawnRaw from "../../data/spawn.json" with { type: "json" };
import copyRaw from "../../data/copy.json" with { type: "json" };

export const SPAWN_SCHEMA = 1;
export const COPY_SCHEMA = 1;
export const SPAWN_FIELDS = [
  "intervalTicks",
  "minIntervalTicks",
  "rampTicks",
  "hazardChanceStart",
  "hazardChanceEnd",
  "fallSpeedMin",
  "fallSpeedMax",
];
export const COPY_FIELDS = [
  "paused",
  "resume",
  "over",
  "restart",
  "restart_inline",
  "best_chain",
  "chain",
  "score",
  "record",
  "dash_ready",
  "dash_recharging",
  "hint_move",
  "hint_collect",
  "hint_bank",
];

export function migrateTable(name, raw, schema, fields = []) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
    throw new Error(`mesa ${name} ilegível`);
  }
  const current = Number.isInteger(raw.schema) ? raw.schema : 0;
  if (current > schema) {
    throw new Error(`mesa ${name} schema ${current} não suportado (máximo ${schema})`);
  }
  const table = { ...raw, schema };
  if (fields.length) {
    const missing = fields.filter((field) => table[field] === undefined);
    if (missing.length) {
      throw new Error(`mesa ${name} sem ${missing.join(", ")}`);
    }
  }
  return table;
}

export function migrateSpawn(raw) {
  return migrateTable("spawn", raw, SPAWN_SCHEMA);
}

const spawn = migrateTable("spawn", spawnRaw, SPAWN_SCHEMA, SPAWN_FIELDS);
const copy = migrateTable("copy", copyRaw, COPY_SCHEMA, COPY_FIELDS);

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
