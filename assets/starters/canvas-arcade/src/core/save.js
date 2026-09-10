// Progresso: versionado, migrável e nunca destruído por engano.
//
// Progresso e preferência vivem em chaves separadas porque têm ciclos de vida
// diferentes: apagar a partida não deve apagar o volume nem o remapeamento.
// A migração acompanha a mudança de formato; um save de versão futura **bloqueia
// a gravação** em vez de ser sobrescrito por uma versão antiga do jogo.

import { readJson, writeJson } from "./storage.js";

export const PROGRESS_KEY = "progress";
export const PROGRESS_SCHEMA = 3;

export function defaultProgress() {
  return {
    schema: PROGRESS_SCHEMA,
    best: 0,
    bestChain: 0,
    runs: 0,
    lastSeed: null,
    lastRun: null,
    hold: null,
  };
}

// Há partida gravada e seed para repetir. Não é o tick
// interrompido: isso mora em `hold` / `canResume`.
export function canContinue(progress) {
  if (!progress) return false;
  const seed = progress.lastSeed;
  return (progress.runs ?? 0) > 0 && (typeof seed === "string" || Number.isFinite(seed));
}

// Há chuva no meio. Não é Continuar: Continuar repete a seed do zero.
export function canResume(progress) {
  return readHold(progress?.hold) !== null;
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
      hold: raw.hold ?? null,
    };
  }
  const progress = {
    schema: PROGRESS_SCHEMA,
    best: integer(working.best),
    bestChain: integer(working.bestChain),
    runs: integer(working.runs),
    lastSeed: typeof working.lastSeed === "string" || Number.isFinite(working.lastSeed) ? working.lastSeed : null,
    lastRun: readRun(working.lastRun),
    hold: readHold(working.hold),
  };
  if (schema < PROGRESS_SCHEMA) {
    notes.push(`migrado de schema ${schema} para ${PROGRESS_SCHEMA}`);
  }
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

export function recordRun(progress, state, extras = {}) {
  return {
    ...progress,
    schema: PROGRESS_SCHEMA,
    best: Math.max(progress.best, state.score),
    bestChain: Math.max(progress.bestChain, state.stats.bestChain),
    runs: progress.runs + 1,
    lastSeed: state.seed,
    lastRun: extras.lastRun ?? summarizeRun(state, extras),
    hold: null,
  };
}

const finiteNumber = (value, fallback = 0) => (Number.isFinite(value) ? value : fallback);

// Recorte da partida em curso. Sem motes nem eventos: são efêmeros.
// Quem lê isto não chama o resultado de Continuar.
export function captureHold(state) {
  if (!state || state.phase !== "playing") return null;
  if (!(typeof state.seed === "string" || Number.isFinite(state.seed))) return null;
  if (!Number.isFinite(state.rngState)) return null;
  if (!state.player || typeof state.player !== "object") return null;
  const entities = Array.isArray(state.entities) ? state.entities : [];
  if (!(state.tick > 0 || entities.length > 0 || state.score > 0 || state.chain > 0)) {
    return null;
  }
  const player = state.player;
  const stats = state.stats ?? {};
  const camera = state.camera ?? {};
  return {
    version: 1,
    seed: state.seed,
    rngState: finiteNumber(state.rngState) >>> 0,
    tick: integer(state.tick),
    score: integer(state.score),
    chain: integer(state.chain),
    hitstop: integer(state.hitstop),
    shake: finiteNumber(state.shake),
    flash: finiteNumber(state.flash),
    camera: { x: finiteNumber(camera.x), y: finiteNumber(camera.y) },
    bankLock: integer(state.bankLock),
    bankBuffer: integer(state.bankBuffer),
    spawnTimer: integer(state.spawnTimer),
    recoverUntil: integer(state.recoverUntil),
    nextId: integer(state.nextId, 1),
    spawnProfile: typeof state.spawnProfile === "string" ? state.spawnProfile : "spawn",
    assist: Boolean(state.assist),
    player: {
      x: finiteNumber(player.x),
      dir: player.dir < 0 ? -1 : 1,
      dashTicks: integer(player.dashTicks),
      dashRecovery: integer(player.dashRecovery),
      dashCooldown: integer(player.dashCooldown),
      dashBuffer: integer(player.dashBuffer),
      dashWindup: integer(player.dashWindup),
      invuln: integer(player.invuln),
      squash: finiteNumber(player.squash),
    },
    entities: entities.map((entity) => ({
      id: integer(entity.id, 1),
      kind: entity.kind === "shard" ? "shard" : "orb",
      x: finiteNumber(entity.x),
      y: finiteNumber(entity.y),
      vy: finiteNumber(entity.vy),
    })),
    stats: {
      collected: integer(stats.collected),
      missed: integer(stats.missed),
      hits: integer(stats.hits),
      banks: integer(stats.banks),
      dashes: integer(stats.dashes),
      bestChain: integer(stats.bestChain),
      banked: integer(stats.banked),
    },
  };
}

export function readHold(raw) {
  if (!raw || typeof raw !== "object") return null;
  if (!(typeof raw.seed === "string" || Number.isFinite(raw.seed))) return null;
  if (!Number.isFinite(raw.rngState)) return null;
  if (!raw.player || typeof raw.player !== "object") return null;
  return captureHold({
    ...raw,
    phase: "playing",
    player: raw.player,
    entities: raw.entities,
    stats: raw.stats ?? {},
    camera: raw.camera ?? {},
  });
}

// Forma estável para o campo "medição" de um achado de playtest.
// Números no disco não são causa observada.
export function summarizeRun(state, extras = {}) {
  const stats = state.stats ?? {};
  const number = (value) => (Number.isFinite(value) ? value : 0);
  const look = typeof extras.look === "string" && extras.look
    ? extras.look
    : typeof state.look === "string" && state.look
      ? state.look
      : "normal";
  return {
    seed: state.seed ?? null,
    spawn: typeof state.spawnProfile === "string" && state.spawnProfile ? state.spawnProfile : "spawn",
    look,
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
