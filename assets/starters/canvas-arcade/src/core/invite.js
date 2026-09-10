// Superfície de convite. A tabela da página ensina o verbo; quem nunca
// viu o jogo não deveria lê-la. `?invite=1` some o painel. Com seed no
// last-run, `?invite=1&seed=<n>` some a tabela e abre essa partida.
// Juntar o número não é alguém de fora. Esconder a
// tabela não é alguém de fora nem curva observada. Depois do fim, a
// porta também oferece os quatro nomes — no overlay e na abertura, se
// houver partida. Copiar não grava. Esqueleto vazio não é achado.
// Gravado não é alguém de fora.

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

function afterRun(phase, run) {
  return phase === "over" || (phase === "title" && Boolean(run));
}

export function applyFinding({ root, phase, invite, run } = {}) {
  const show = Boolean(invite && afterRun(phase, run));
  root?.classList?.toggle("finding", show);
  return show;
}

export function applyNote({ root, phase, invite, run } = {}) {
  const show = Boolean(!invite && afterRun(phase, run));
  root?.classList?.toggle("note", show);
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
