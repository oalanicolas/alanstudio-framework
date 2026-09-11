// Superfície de convite. A tabela da página ensina o verbo; quem nunca
// viu o jogo não deveria lê-la. `?invite=1` some o painel. Com seed no
// last-run, `?invite=1&seed=<n>&spawn=<mesa>&look=<paleta>&speed=<relógio>`
// some a tabela e abre essa partida com a chuva, o look e o
// relógio que o candidato nomeou. `seedHref` é o mesmo endereço
// sem o convite — o caminho do maker. Relógio 1, mesa padrão
// ou paleta `normal`/`contrast` some. Sem eixo, o aparelho decide.
// Depois do fim, a página do maker aponta o convite. Copiar o
// endereço não grava e não é quem jogou. Juntar o número não é
// alguém de fora. Esconder a
// tabela não é alguém de fora nem curva observada. Depois do fim, a
// porta também oferece os quatro nomes — no overlay e na abertura, se
// houver partida — e mostra seed, pontos, eixos, a curva que o
// last-run já traçou e se o candidato foi simulado. Número na faixa
// não preenche os quatro. Copiar não grava. Esqueleto vazio não é
// achado. Gravado não é alguém de fora. VERSION.json na raiz some
// o Gravar: o serve da árvore exportada recusa o POST. Copiar
// permanece. Sem clipboard, o Copiar baixa o markdown. O
// Copiar nomeia o destino. Baixar não grava e não é alguém
// de fora. Recusar não fecha o achado.
// No primeiro over a página rola até o painel e foca o primeiro
// campo. Trazer o painel não é alguém de fora nem curva observada.

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

function runSpeed(run) {
  // A faixa não leva o relógio. O endereço sim: sem isto
  // o convite abria a seed no relógio cheio. Número na
  // URL não é sessão observada.
  if (!run || typeof run !== "object" || Array.isArray(run)) return null;
  const speed = typeof run.speed === "number" ? run.speed : run.run && typeof run.run === "object" ? run.run.speed : null;
  if (!Number.isFinite(speed) || speed === 1 || speed < 0.5 || speed > 1) return null;
  return speed;
}

function runQuery(run) {
  const parts = [];
  const seed = runSeed(run);
  if (seed !== null) parts.push(`seed=${seed}`);
  const spawn = runSpawn(run);
  if (spawn) parts.push(`spawn=${spawn}`);
  const look = runLook(run);
  if (look) parts.push(`look=${look}`);
  const speed = runSpeed(run);
  if (speed !== null) parts.push(`speed=${speed}`);
  return parts;
}

function runPolicy(run) {
  // A faixa lia seed e some a origem. O last-run já
  // marca nearest-orb. Número no disco não é outsider.
  if (!run || typeof run !== "object" || Array.isArray(run)) return "";
  const policy = typeof run.policy === "string"
    ? run.policy
    : run.run && typeof run.run === "object" && !Array.isArray(run.run)
      ? run.run.policy
      : null;
  return policy === "nearest-orb" ? "simulada" : "";
}

function runScore(run) {
  if (!run || typeof run !== "object" || Array.isArray(run)) return null;
  if (typeof run.score === "number" && Number.isFinite(run.score)) return run.score;
  const nested = run.run && typeof run.run === "object" && !Array.isArray(run.run) ? run.run.score : null;
  if (typeof nested === "number" && Number.isFinite(nested)) return nested;
  return null;
}

export function curveFacts(curve) {
  // A faixa mostrava seed e some a curva que o last-run
  // já traçou. Número no disco não é causa nem outsider.
  if (!curve || typeof curve !== "object" || Array.isArray(curve)) return "";
  const source = curve.curve && typeof curve.curve === "object" && !Array.isArray(curve.curve)
    ? curve.curve
    : curve;
  const parts = [];
  if (source.never_banked === true) parts.push("nunca guardou");
  if (Number.isFinite(source.unbanked_at_end) && source.unbanked_at_end > 0) {
    parts.push(`aposta ${source.unbanked_at_end}`);
  }
  return parts.join(" · ");
}

// Números da partida para quem vai escrever o achado. Não preenche
// os quatro campos e não é evidência. Sem seed, pontos, eixo
// nomeado ou curva, a linha some.
export function runFacts(run) {
  const parts = [];
  const seed = runSeed(run);
  if (seed !== null) parts.push(`seed ${seed}`);
  const score = runScore(run);
  if (score !== null) parts.push(String(score));
  const policy = runPolicy(run);
  if (policy) parts.push(policy);
  const spawn = runSpawn(run);
  if (spawn) parts.push(spawn);
  const look = runLook(run);
  if (look && look !== spawn) parts.push(look);
  const curve = curveFacts(run && run.curve);
  if (curve) parts.push(curve);
  return parts.join(" · ");
}

export function applyRunFacts({ node, run } = {}) {
  const text = runFacts(run);
  if (node) {
    node.textContent = text;
    node.hidden = !text;
  }
  return text;
}

function hrefFromParts(parts, origin) {
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

export function seedHref(run, origin) {
  const seed = runSeed(run);
  if (seed === null) return null;
  return hrefFromParts(runQuery(run), origin);
}

export function inviteHref(run, origin) {
  return hrefFromParts(["invite=1", ...runQuery(run)], origin);
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

export function bringPanel({
  node,
  shown,
  wasShown,
  field,
  phase,
  reduceMotion,
} = {}) {
  if (!shown || wasShown || phase !== "over" || !node) return false;
  if (typeof node.scrollIntoView === "function") {
    node.scrollIntoView({
      block: "start",
      behavior: reduceMotion ? "auto" : "smooth",
    });
  }
  if (field && typeof field.focus === "function") {
    field.focus({ preventScroll: true });
  }
  return true;
}

export const VERSION_ROUTE = "/VERSION.json";
export const ARTIFACT_FINDING_HINT =
  "Na árvore exportada o serve recusa gravar. Copie os quatro nomes. Sem a área de transferência, o Copiar baixa o markdown.";
export const FINDING_FILE = "achado.md";

export async function readArtifactMark(options = {}) {
  const fetchFn = options.fetch;
  if (typeof fetchFn !== "function") return false;
  try {
    const response = await fetchFn(options.url ?? VERSION_ROUTE);
    return Boolean(response && response.ok);
  } catch {
    return false;
  }
}

export function applyArtifactSurface({
  root,
  findingSave,
  noteSave,
  findingHint,
  artifact,
} = {}) {
  if (!artifact) return false;
  if (findingSave) {
    findingSave.hidden = true;
    findingSave.disabled = true;
  }
  if (noteSave) {
    noteSave.hidden = true;
    noteSave.disabled = true;
  }
  if (findingHint) findingHint.textContent = ARTIFACT_FINDING_HINT;
  root?.classList?.toggle("artifact", true);
  return true;
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

export function findingFile(text) {
  return { name: FINDING_FILE, type: "text/markdown", text: String(text ?? "") };
}

export function canWriteClipboard(clipboard) {
  return typeof clipboard?.writeText === "function";
}

export async function offerFinding(text, { clipboard, save, name } = {}) {
  const file = findingFile(text);
  if (name) file.name = name;
  if (canWriteClipboard(clipboard)) {
    try {
      await clipboard.writeText(file.text);
      return "copied";
    } catch {
      if (typeof save === "function") {
        save(file);
        return "saved";
      }
      return "missed";
    }
  }
  if (typeof save === "function") {
    save(file);
    return "saved";
  }
  return "missed";
}

// O Gravar já vira "Achado no disco". Sem isto o Copiar
// calava o destino e o convite some a tabela. Nomear não
// grava e não é alguém de fora.
export const FINDING_COPY_LABEL = "Copiar";

export const FINDING_OFFER_LABELS = {
  copied: "Na área de transferência",
  saved: "Baixado",
  missed: "Não copiou",
};

export function findingOfferLabel(result) {
  return FINDING_OFFER_LABELS[result] ?? FINDING_COPY_LABEL;
}

export function applyFindingOffer({ button, live, result } = {}) {
  const label = findingOfferLabel(result);
  if (button) button.textContent = label;
  if (live) live.textContent = label;
  return label;
}

export function findingValues(fields = {}) {
  return {
    problema: String(fields.problema ?? ""),
    evidencia: String(fields.evidencia ?? ""),
    hipotese: String(fields.hipotese ?? ""),
    medicao: String(fields.medicao ?? ""),
  };
}
