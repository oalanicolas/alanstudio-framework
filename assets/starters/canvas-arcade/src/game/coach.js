// Ensino do primeiro ciclo. Sem isto o jogador só aprende pela tabela da
// página — e a barra chama isso de protótipo. O aviso some depois da
// primeira vez que o jogador guarda: a decisão já foi jogada.

export function coachHint(state) {
  if (!state || state.phase !== "playing") return null;
  if (state.stats.banks > 0) return null;
  if (state.chain >= 2) return "bank";
  if (state.tick < 60) return "move";
  return "collect";
}
