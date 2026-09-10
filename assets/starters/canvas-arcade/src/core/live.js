// Região viva. A legenda e o perigo à frente já existem no mixer
// e no telegraph; a pausa já existe no overlay. O fim e a porta
// já nomeiam placar e recorde no canvas. Sem isto só o canvas
// os mostra. Texto no DOM não é sessão de alcance nem alguém de fora.

function whole(value) {
  if (!Number.isFinite(value)) return null;
  return String(Math.trunc(value));
}

export function liveText({
  captions = [],
  phase,
  threat,
  paused,
  score,
  best,
  lastScore,
} = {}) {
  const parts = [];
  const seen = new Set();
  const add = (text) => {
    const value = typeof text === "string" ? text.trim() : "";
    if (!value || seen.has(value)) return;
    seen.add(value);
    parts.push(value);
  };
  if (paused) add("pausado");
  if (phase === "over") {
    add("fim da partida");
    const points = whole(score);
    if (points !== null) add(points);
    const record = whole(best);
    if (record !== null && Number(best) > 0) add(`recorde ${record}`);
  } else if (phase === "title") {
    add("abertura");
    const last = whole(lastScore);
    if (last !== null) add(`última ${last}`);
    const record = whole(best);
    if (record !== null && Number(best) > 0) add(`recorde ${record}`);
  }
  if (threat === "ahead") add("perigo à frente");
  const latest = captions.length ? captions[captions.length - 1] : null;
  if (latest) add(latest.text);
  return parts.join(". ");
}

export function applyLive({ node, text } = {}) {
  if (!node) return false;
  const next = String(text ?? "");
  if (node.textContent === next) return false;
  node.textContent = next;
  return true;
}
