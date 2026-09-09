// Ensino do primeiro ciclo. Sem isto o jogador só aprende pela tabela da
// página — e a barra chama isso de protótipo. O aviso some depois da
// primeira vez que o jogador guarda: a decisão já foi jogada.

export function coachHint(state, lines = {}) {
  if (!state || state.phase !== "playing") return null;
  if (state.stats.banks > 0) return null;
  const fantasy = typeof lines.fantasy === "string" ? lines.fantasy.trim() : "";
  if (fantasy && state.tick < 48) return "fantasy";
  if (state.chain >= 2) return "bank";
  if (state.tick < 60) return "move";
  return "collect";
}
