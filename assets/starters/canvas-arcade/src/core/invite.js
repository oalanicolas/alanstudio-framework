// Superfície de convite. A tabela da página ensina o verbo; quem nunca
// viu o jogo não deveria lê-la. `?invite=1` some o painel. Com seed no
// last-run, `?invite=1&seed=<n>&spawn=<mesa>&look=<paleta>` some a
// tabela e abre essa partida com a chuva e o look que o candidato
// nomeou. Sem mesa ou sem paleta, o aparelho decide o eixo omitido.
// Depois do fim, a página do maker aponta esse endereço. Copiar o
// endereço não grava e não é quem jogou. Juntar o número não é
// alguém de fora. Esconder a
// tabela não é alguém de fora nem curva observada. Depois do fim, a
// porta também oferece os quatro nomes — no overlay e na abertura, se
// houver partida. Copiar não grava. Esqueleto vazio não é achado.
// Gravado não é alguém de fora.

function runSeed(run) {
  if (!run || typeof run !== "object" || Array.isArray(run)) return null;
  const seed = typeof run.seed === "number" ? run.seed : run.run && typeof run.run === "object" ? run.run.seed : null;
  if (typeof seed !== "number" || !Number.isSafeInteger(seed) || seed < 0) return null;
  return seed >>> 0;
}

function runSpawn(run) {
  if (!run || typeof run !== "object" || Array.isArray(run)) return null;
  const spawn = typeof run.spawn === "string" ? run.spawn : run.run && typeof run.run === "object" ? run.run.spawn : null;
  if (typeof spawn !== "string" || !/^[a-z][a-z0-9]{0,31}$/.test(spawn) || spawn === "spawn") return null;
  return spawn;
}

function runLook(run) {
  if (!run || typeof run !== "object" || Array.isArray(run)) return null;
  const look = typeof run.look === "string" ? run.look : run.run && typeof run.run === "object" ? run.run.look : null;
  if (typeof look !== "string" || !/^[a-z][a-z0-9]{0,31}$/.test(look) || look === "normal" || look === "contrast") {
    return null;
  }
  return look;
}

export function inviteHref(run, origin) {
  const parts = ["invite=1"];
  const seed = runSeed(run);
  if (seed !== null) parts.push(`seed=${seed}`);
  const spawn = runSpawn(run);
  if (spawn) parts.push(`spawn=${spawn}`);
  const look = runLook(run);
  if (look) parts.push(`look=${look}`);
  const path = `/?${parts.join("&")}`;
  if (typeof origin === "string" && origin) {
    try {
      return new URL(path, origin).href;
    } catch {
      return path;
    }
  }
  return path;
}

export function applyShare({ hrefNode, wrap, run, origin } = {}) {
  const href = inviteHref(run, origin);
  if (hrefNode) hrefNode.textContent = href;
  if (wrap) wrap.hidden = !/seed=\d+/.test(href);
  return href;
}

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
