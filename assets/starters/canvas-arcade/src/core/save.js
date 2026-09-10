// Progresso: versionado, migrável e nunca destruído por engano.
//
// Progresso e preferência vivem em chaves separadas porque têm ciclos de vida
// diferentes: apagar a partida não deve apagar o volume nem o remapeamento.
// A migração acompanha a mudança de formato; um save de versão futura **bloqueia
// a gravação** em vez de ser sobrescrito por uma versão antiga do jogo.

import { readJson, writeJson } from "./storage.js";

export const PROGRESS_KEY = "progress";
export const PROGRESS_SCHEMA = 2;

export function defaultProgress() {
  return { schema: PROGRESS_SCHEMA, best: 0, bestChain: 0, runs: 0, lastSeed: null, lastRun: null };
}

// Há partida gravada e seed para repetir. Não é o tick
// interrompido: o save não guarda o meio da chuva.
export function canContinue(progress) {
  if (!progress) return false;
  const seed = progress.lastSeed;
  return (progress.runs ?? 0) > 0 && (typeof seed === "string" || Number.isFinite(seed));
}

const integer = (value, fallback = 0) =>
  Number.isFinite(value) && value >= 0 ? Math.floor(value) : fallback;

export function migrate(raw) {
  if (raw === null || raw === undefined) {
    return { progress: defaultProgress(), from: null, status: "absent", notes: [] };
  }
  const schema = Number.isInteger(raw.schema) ? raw.schema : 0;
  if (schema > PROGRESS_SCHEMA) {
    return {
      progress: defaultProgress(),
      from: schema,
      status: "blocked",
      notes: ["save de versão futura; gravação bloqueada para não sobrescrever progresso"],
    };
  }
  const notes = [];
  let working = raw;
  if (schema <= 1) {
    // v1 guardava apenas `highScore` e não contava partidas.
    working = {
      schema: 2,
      best: integer(raw.highScore ?? raw.best),
      bestChain: integer(raw.bestChain),
      runs: integer(raw.runs),
      lastSeed: raw.lastSeed ?? null,
      lastRun: raw.lastRun ?? null,
    };
    notes.push(`migrado de schema ${schema} para ${PROGRESS_SCHEMA}`);
  }
  const progress = {
    schema: PROGRESS_SCHEMA,
    best: integer(working.best),
    bestChain: integer(working.bestChain),
    runs: integer(working.runs),
    lastSeed: typeof working.lastSeed === "string" || Number.isFinite(working.lastSeed) ? working.lastSeed : null,
    lastRun: readRun(working.lastRun),
  };
  const repaired = ["best", "bestChain", "runs"].filter(
    (key) => working[key] !== undefined && progress[key] !== working[key],
  );
  if (repaired.length) notes.push(`campos fora de faixa recuperados: ${repaired.join(", ")}`);
  return {
    progress,
    from: schema,
    status: notes.length ? "migrated" : "loaded",
    notes,
  };
}

export function loadProgress(storage) {
  const read = readJson(storage, PROGRESS_KEY);
  if (read.status === "unreadable") {
    return {
      progress: defaultProgress(),
      status: "recovered",
      from: null,
      notes: ["save ilegível preservado em progress.broken; progresso reiniciado"],
    };
  }
  return migrate(read.value);
}

export function saveProgress(storage, progress, load = null) {
  if (load && load.status === "blocked") {
    return { ok: false, reason: "future_schema" };
  }
  return writeJson(storage, PROGRESS_KEY, { ...defaultProgress(), ...progress, schema: PROGRESS_SCHEMA });
}

function readRun(raw) {
  if (!raw || typeof raw !== "object") return null;
  return summarizeRun({
    seed: raw.seed,
    score: raw.score,
    chain: raw.chain,
    tick: raw.ticks ?? raw.tick,
    stats: raw,
  });
}

export function recordRun(progress, state) {
  return {
    ...progress,
    schema: PROGRESS_SCHEMA,
    best: Math.max(progress.best, state.score),
    bestChain: Math.max(progress.bestChain, state.stats.bestChain),
    runs: progress.runs + 1,
    lastSeed: state.seed,
    lastRun: summarizeRun(state),
  };
}

// Forma estável para o campo "medição" de um achado de playtest.
// Números no disco não são causa observada.
export function summarizeRun(state) {
  const stats = state.stats ?? {};
  const number = (value) => (Number.isFinite(value) ? value : 0);
  return {
    seed: state.seed ?? null,
    score: number(state.score),
    chain: number(state.chain),
    ticks: number(state.tick),
    collected: number(stats.collected),
    missed: number(stats.missed),
    hits: number(stats.hits),
    banks: number(stats.banks),
    bestChain: number(stats.bestChain),
    banked: number(stats.banked),
  };
}
