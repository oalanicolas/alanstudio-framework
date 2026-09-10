// Superfície de convite. A tabela da página ensina o verbo; quem nunca
// viu o jogo não deveria lê-la. `?invite=1` some o painel. Esconder a
// tabela não é alguém de fora nem curva observada. Depois do fim, a
// página oferece os quatro nomes para copiar. Copiar não grava no
// projeto e não é alguém de fora.

export function inviteMode(search = "") {
  const raw = typeof search === "string" ? search : "";
  const query = raw.startsWith("?") ? raw.slice(1) : raw;
  return new URLSearchParams(query).get("invite") === "1";
}

export const INVITE_LABEL = "Área de jogo";

export const FINDING_KEYS = ["problema", "evidencia", "hipotese", "medicao"];

export function applyInvite({ root, stage, search } = {}) {
  const on = inviteMode(search);
  root?.classList?.toggle("invite", on);
  if (on) stage?.setAttribute?.("aria-label", INVITE_LABEL);
  return on;
}

export function applyFinding({ root, phase, invite } = {}) {
  const show = Boolean(invite && phase === "over");
  root?.classList?.toggle("finding", show);
  return show;
}

export function composeFinding({
  problema = "",
  evidencia = "",
  hipotese = "",
  medicao = "",
} = {}) {
  return (
    `- Problema: ${String(problema)}\n` +
    `- Evidência: ${String(evidencia)}\n` +
    `- Hipótese: ${String(hipotese)}\n` +
    `- Medição: ${String(medicao)}\n`
  );
}

export function findingValues(fields = {}) {
  return {
    problema: String(fields.problema ?? ""),
    evidencia: String(fields.evidencia ?? ""),
    hipotese: String(fields.hipotese ?? ""),
    medicao: String(fields.medicao ?? ""),
  };
}
