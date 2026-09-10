// Forma do candidato de playtest. Número no disco não é causa nem
// sessão observada. O serve grava a partida jogada; `npm run session`
// grava a simulação. Os dois usam este recibo. `observed` e `felt`
// nascem falsos.

export const LAST_RUN_ROUTE = "/playtest/last-run";
export const LAST_RUN_FILE = "docs/playtest/last-run.json";
export const NOTE_ROUTE = "/playtest/note";
export const NOTE_DIR = "docs/playtest";
export const FINDING_ROUTE = "/playtest/finding";

export function playFinding({
  problema = "",
  evidencia = "",
  hipotese = "",
  medicao = "",
} = {}) {
  const fields = {
    problema: String(problema).trim(),
    evidencia: String(evidencia).trim(),
    hipotese: String(hipotese).trim(),
    medicao: String(medicao).trim(),
  };
  if (!fields.problema || !fields.evidencia || !fields.hipotese || !fields.medicao) {
    return null;
  }
  return (
    `- Problema: ${fields.problema}\n` +
    `- Evidência: ${fields.evidencia}\n` +
    `- Hipótese: ${fields.hipotese}\n` +
    `- Medição: ${fields.medicao}\n`
  );
}

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
  look,
  speed,
  run,
  curve,
  policy = "played",
} = {}) {
  const nearest = policy === "nearest-orb";
  const summary = run && typeof run === "object" && !Array.isArray(run) ? { ...run } : {};
  const rawSpeed = Number.isFinite(speed) ? speed : summary.speed;
  const report = {
    schema: 2,
    seed: seed ?? summary.seed ?? null,
    spawn: typeof spawn === "string" && spawn ? spawn : "spawn",
    look: typeof look === "string" && look ? look : typeof summary.look === "string" && summary.look ? summary.look : "normal",
    speed: Number.isFinite(rawSpeed) ? rawSpeed : 1,
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

// O achado da página é markdown. Este JSON é o candidato que estava
// em last-run.json na hora de gravar — não a prova de quem jogou.
export function findingAttachment({
  seed,
  spawn,
  look,
  run,
  curve,
  finding,
} = {}) {
  const report = playReport({ seed, spawn, look, run, curve, policy: "played" });
  return {
    ...report,
    kind: "finding-attachment",
    finding: typeof finding === "string" ? finding : "",
    outsider: false,
    scope:
      "Anexo do candidato que estava em last-run.json quando a página gravou o achado. Número no disco não é causa nem sessão observada. Sem limiar.",
  };
}
