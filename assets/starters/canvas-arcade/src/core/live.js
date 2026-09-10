// Região viva. A legenda e o perigo à frente já existem no mixer
// e no telegraph; sem isto só o canvas os mostra. Texto no DOM
// não é sessão de alcance nem alguém de fora.

export function liveText({ captions = [], phase, threat } = {}) {
  const parts = [];
  const seen = new Set();
  const add = (text) => {
    const value = typeof text === "string" ? text.trim() : "";
    if (!value || seen.has(value)) return;
    seen.add(value);
    parts.push(value);
  };
  if (phase === "over") add("fim da partida");
  else if (phase === "title") add("abertura");
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
