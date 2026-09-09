// Mesas de conteúdo. A regra e a apresentação consomem; não embutem.
//
// Uma mesa nova entra pelo comando: `npm run table -- <nome>`. Ele
// escreve o JSON com schema e registra o nome abaixo. Alterar um JSON
// não republica o verbo. Sem consumidor a mesa existe e o jogo não muda.
//
// Toda mesa tem schema: formato antigo (sem campo) vira o vigente;
// schema futuro falha com o número, não com undefined no meio do tick.
// Spawn 2 acrescenta prática e recuperação; ausentes ganham o padrão.

import spawnRaw from "../../data/spawn.json" with { type: "json" };
import copyRaw from "../../data/copy.json" with { type: "json" };

export const SPAWN_SCHEMA = 2;
export const COPY_SCHEMA = 1;
export const SPAWN_FIELDS = [
  "intervalTicks",
  "minIntervalTicks",
  "rampTicks",
  "hazardChanceStart",
  "hazardChanceEnd",
  "fallSpeedMin",
  "fallSpeedMax",
  "practiceTicks",
  "recoveryTicks",
  "recoveryIntervalScale",
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
  const table = migrateTable("spawn", raw, SPAWN_SCHEMA);
  return {
    ...table,
    schema: SPAWN_SCHEMA,
    practiceTicks: Number.isInteger(table.practiceTicks) ? table.practiceTicks : 240,
    recoveryTicks: Number.isInteger(table.recoveryTicks) ? table.recoveryTicks : 90,
    recoveryIntervalScale: Number.isFinite(table.recoveryIntervalScale)
      ? table.recoveryIntervalScale
      : 1.6,
  };
}

const spawn = migrateSpawn(spawnRaw);
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
