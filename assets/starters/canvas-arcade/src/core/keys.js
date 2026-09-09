// Rótulo das teclas vivas — e do aparelho que falou por último.
//
// O manifesto e a tabela da página ensinam o padrão. O aviso do
// primeiro ciclo nomeia teclado (ou o remapeamento vigente), toque e
// controle juntos; o dash e o mapa da superfície que falou também
// ganham passo no campo. Overlay e HUD confirmam o aparelho que
// falou por último. Rótulo no texto não é sessão observada.

const NAMED = {
  Space: "Espaço",
  Escape: "Esc",
  ArrowLeft: "←",
  ArrowRight: "→",
  ArrowDown: "↓",
  ArrowUp: "↑",
};

const TOKEN = /\{(pause|reset|bank|dash|left|right)\}/g;

export function keyLabel(code) {
  if (NAMED[code]) return NAMED[code];
  if (typeof code === "string" && /^Key[A-Z]$/.test(code)) return code.slice(3);
  if (typeof code === "string" && /^Digit[0-9]$/.test(code)) return code.slice(5);
  return typeof code === "string" ? code : "";
}

export function actionLabels(bindings, action) {
  const codes = bindings && Array.isArray(bindings[action]) ? bindings[action] : [];
  return codes.map(keyLabel).filter(Boolean);
}

export function actionLabel(bindings, action) {
  return actionLabels(bindings, action)[0] ?? "";
}

const SURFACE_TOKENS = {
  gamepad: {
    pause: "Start",
    reset: "Select",
    bank: "X",
    dash: "A",
    left: "analógico",
    right: "analógico",
  },
  pointer: {
    bank: "baixo",
    dash: "cima",
  },
};

export function bindLines(lines, bindings, surface = "keyboard") {
  const tokens = {
    pause: actionLabels(bindings, "pause").join(" ou "),
    reset: actionLabels(bindings, "reset").join(" ou "),
    bank: actionLabel(bindings, "bank"),
    dash: actionLabel(bindings, "dash"),
    left: actionLabel(bindings, "left"),
    right: actionLabel(bindings, "right"),
  };
  const spoken = SURFACE_TOKENS[surface];
  const fill = (text, map) =>
    typeof text === "string"
      ? text.replace(TOKEN, (_, name) => map[name] || `{${name}}`)
      : text;
  const next = { ...lines };
  for (const key of Object.keys(next)) {
    // O aviso do primeiro ciclo ensina as três superfícies. Overlay e HUD
    // confirmam o aparelho que falou por último. Misturar os dois no
    // mesmo texto apagava toque e controle até alguém já ter jogado.
    const map = spoken && !String(key).startsWith("hint_") ? { ...tokens, ...spoken } : tokens;
    next[key] = fill(next[key], map);
  }
  return next;
}
