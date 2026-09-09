// Ensino do primeiro ciclo. Sem isto o jogador só aprende pela tabela da
// página — e a barra chama isso de protótipo. O aviso some depois da
// primeira vez que o jogador guarda: a decisão já foi jogada.
//
// Mover, coletar e guardar já tinham passo. O dash — o verbo que a
// fantasia nomeia — e o mapa da superfície que falou ficavam só na
// tabela. Passo no campo não é sessão observada.

import { approaching } from "./rules.js";

const FANTASY_TICKS = 48;
const MOVE_TICKS = 60;
const SURFACE_TICKS = 108;

function shardThreat(state) {
  const near = approaching(state);
  for (let index = 0; index < near.length; index += 1) {
    if (near[index].kind === "shard") return true;
  }
  return false;
}

export function coachHint(state, lines = {}, extra = {}) {
  if (!state || state.phase !== "playing") return null;
  if (state.stats.banks > 0) return null;
  const fantasy = typeof lines.fantasy === "string" ? lines.fantasy.trim() : "";
  if (fantasy && state.tick < FANTASY_TICKS) return "fantasy";
  if (state.chain >= 2) return "bank";
  if (state.tick < MOVE_TICKS) return "move";
  if ((state.stats.dashes ?? 0) === 0 && shardThreat(state)) return "dash";
  const surface = extra.surface;
  if (state.tick < SURFACE_TICKS && (surface === "pointer" || surface === "gamepad")) {
    return surface === "pointer" ? "touch" : "pad";
  }
  return "collect";
}
