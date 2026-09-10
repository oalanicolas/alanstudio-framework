// Ensino do primeiro ciclo. Sem isto o jogador só aprende pela tabela da
// página — e a barra chama isso de protótipo. A porta ensina fantasia
// e mover no relógio da mostra; dash, coleta e guarda ficam no campo.
// O aviso some depois da primeira vez que o jogador guarda: a decisão
// já foi jogada.
//
// Exceção: no fecho a corrente viva ainda pode cair. Pedir guardar
// de novo não reabre o primeiro ciclo — pad e toque continuam
// calados depois da primeira guarda. Texto no disco não é sessão.
//
// Mover, coletar e guardar já tinham passo. O dash — o verbo que a
// fantasia nomeia — e o mapa da superfície que falou ficavam só na
// tabela. A queda do orbe falava e marcava o lugar; o aviso não
// nomeava o custo. O estilhaço come a corrente e o mixer fala;
// o aviso não nomeava esse custo. Passo no campo não é sessão
// observada.

import { approaching, closingWindow } from "./rules.js";

export const FANTASY_TICKS = 48;
export const MOVE_TICKS = 60;
const SURFACE_TICKS = 108;

function shardThreat(state) {
  const near = approaching(state);
  for (let index = 0; index < near.length; index += 1) {
    if (near[index].kind === "shard") return true;
  }
  return false;
}

export function coachHint(state, lines = {}, extra = {}) {
  if (!state) return null;
  if (state.phase === "title") {
    const clock = state.attractTick ?? 0;
    const fantasy = typeof lines.fantasy === "string" ? lines.fantasy.trim() : "";
    // A frase do --idea não come o aviso de abrir. Sem
    // isto a fantasia deixava 12 ticks de mover e a
    // porta calava. Texto no disco não é sessão.
    if (fantasy && clock < FANTASY_TICKS) return "fantasy";
    const moved = fantasy ? clock - FANTASY_TICKS : clock;
    if (moved < MOVE_TICKS) return "move";
    return null;
  }
  if (state.phase !== "playing") return null;
  if (closingWindow(state) && (state.chain ?? 0) > 0) return "bank";
  if (state.stats.banks > 0) return null;
  const fantasy = typeof lines.fantasy === "string" ? lines.fantasy.trim() : "";
  if (fantasy && state.tick < FANTASY_TICKS) return "fantasy";
  if (state.chain >= 2) return "bank";
  if (state.tick < MOVE_TICKS) return "move";
  if ((state.stats.dashes ?? 0) === 0 && shardThreat(state)) return "dash";
  if ((state.stats.hits ?? 0) > 0 && (state.chain ?? 0) === 0) return "hit";
  if ((state.stats.missed ?? 0) > 0 && (state.chain ?? 0) === 0) return "miss";
  const surface = extra.surface;
  if (state.tick < SURFACE_TICKS && (surface === "pointer" || surface === "gamepad")) {
    return surface === "pointer" ? "touch" : "pad";
  }
  return "collect";
}
