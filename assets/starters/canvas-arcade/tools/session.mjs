#!/usr/bin/env node
// Corre uma partida simulada e grava resumo e curva no disco. É candidato
// ao campo de medição de um achado — não é sessão observada e não atribui causa.
// last-run jogado (`policy: played`) não some sob a simulação. --force
// ou outro --out. Nomear a origem não observa.

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { playReport } from "../src/core/run-report.js";
import { summarizeRun } from "../src/core/save.js";
import { createTrace, finishCurve, traceTick } from "../src/game/curve.js";
import { listSpawnProfiles } from "../src/game/tables.js";
import { advance, createState, CONFIG, PLAYER_Y } from "../src/game/rules.js";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

const argument = (name, fallback) => {
  const index = process.argv.indexOf(`--${name}`);
  if (index === -1) return fallback;
  return process.argv[index + 1] ?? fallback;
};

const seed = Number(argument("seed", "7"));
const spawn = String(argument("spawn", "spawn"));
const force = process.argv.includes("--force");
const out = resolve(ROOT, argument("out", "docs/playtest/last-run.json"));

async function existingPolicy(path) {
  try {
    const data = JSON.parse(await readFile(path, "utf8"));
    return typeof data?.policy === "string" ? data.policy : null;
  } catch {
    return null;
  }
}

if (!listSpawnProfiles().includes(spawn)) {
  console.error(`perfil de chuva desconhecido: ${spawn}`);
  process.exit(2);
}

function intent(state) {
  const orb = state.entities.find((entity) => entity.kind === "orb");
  const shard = state.entities.find(
    (entity) =>
      entity.kind === "shard" &&
      Math.abs(entity.x - state.player.x) < 18 &&
      Math.abs(entity.y - PLAYER_Y) < 28,
  );
  return {
    move: orb ? Math.sign(orb.x - state.player.x) : 0,
    dash: Boolean(shard),
    bank: state.chain >= 3,
  };
}

const state = createState(Number.isFinite(seed) ? seed : 7, { spawnProfile: spawn });
const trace = createTrace();
let steps = 0;
while (state.phase === "playing" && steps < CONFIG.runTicks + 4) {
  advance(state, intent(state));
  traceTick(trace, state);
  steps += 1;
}

const report = playReport({
  seed: state.seed,
  spawn: state.spawnProfile,
  run: summarizeRun(state),
  curve: finishCurve(trace, state.chain),
  policy: "nearest-orb",
});

if (!force && (await existingPolicy(out)) === "played") {
  console.error(
    "last-run.json é partida jogada. A simulação não sobrescreve. Use --force ou --out.",
  );
  process.exit(3);
}

await mkdir(dirname(out), { recursive: true });
await writeFile(out, `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify({ ...report, path: out }, null, 2));
