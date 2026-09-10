// Forma do candidato de playtest. Número no disco não é causa nem
// sessão observada. O serve grava a partida jogada; `npm run session`
// grava a simulação. Os dois usam este recibo. `observed` e `felt`
// nascem falsos.

export const LAST_RUN_ROUTE = "/playtest/last-run";
export const LAST_RUN_FILE = "docs/playtest/last-run.json";
export const NOTE_ROUTE = "/playtest/note";
export const NOTE_DIR = "docs/playtest";

export function noteStamp(now = new Date()) {
  const iso = now.toISOString();
  return iso.replace(/[-:]/g, "").replace(".", "").replace("Z", "Z");
}

export function playNote({ author, note, project, run, curve, recordedAt } = {}) {
  const text = String(note ?? "").trim();
  if (!text) return null;
  const who = String(author ?? "").trim() || "página";
  const fields = {
    scenario: "primeira partida",
    role: "human",
  };
  if (run && typeof run === "object" && !Array.isArray(run)) {
    fields.run = JSON.stringify(run);
  }
  if (curve && typeof curve === "object" && !Array.isArray(curve)) {
    fields.curve = JSON.stringify(curve);
  }
  return {
    schema_version: 1,
    kind: "observation",
    project: typeof project === "string" ? project : "",
    recorded_at: recordedAt ?? new Date().toISOString(),
    author: who,
    note: text,
    fields,
    attachments: [],
    status: "declared",
    felt: false,
    observed: false,
    scope:
      "Registro declarado por quem assina. O serve gravou o arquivo. Não observa e não sente.",
  };
}

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
