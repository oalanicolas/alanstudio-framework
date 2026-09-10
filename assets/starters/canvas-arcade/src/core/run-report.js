// Forma do candidato de playtest. Número no disco não é causa nem
// sessão observada. O serve grava a partida jogada; `npm run session`
// grava a simulação. Os dois usam este recibo. `observed` e `felt`
// nascem falsos.

export const LAST_RUN_ROUTE = "/playtest/last-run";
export const LAST_RUN_FILE = "docs/playtest/last-run.json";

export function playReport({
  seed,
  spawn,
  run,
  curve,
  policy = "played",
} = {}) {
  const nearest = policy === "nearest-orb";
  const summary = run && typeof run === "object" && !Array.isArray(run) ? { ...run } : {};
  const report = {
    schema: 2,
    seed: seed ?? summary.seed ?? null,
    spawn: typeof spawn === "string" && spawn ? spawn : "spawn",
    policy: nearest ? "nearest-orb" : "played",
    run: summary,
    observed: false,
    felt: false,
    scope: nearest
      ? "Partida simulada com política nearest-orb neste perfil de chuva. Curva pelos eventos: never_banked e sequências são fatos da simulação. Número no disco não é causa nem sessão observada. Sem limiar."
      : "Partida no serve. Curva pelos eventos da sessão. Número no disco não é causa nem sessão observada. Sem limiar.",
  };
  if (curve && typeof curve === "object" && !Array.isArray(curve)) {
    report.curve = { ...curve };
  }
  return report;
}
