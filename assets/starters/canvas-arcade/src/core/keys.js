// Rótulo das teclas vivas — e do aparelho que falou por último.
//
// O manifesto e a tabela da página ensinam o padrão. Depois de um
// remapeamento — o preset de uma mão incluso — o aviso e o overlay
// precisam nomear o que de fato dispara a ação. Se o controle ou o
// toque falou por último, nomear só a tecla ensina o mapa errado.
// Rótulo no texto não é sessão observada.

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
  if (spoken) Object.assign(tokens, spoken);
  const fill = (text) =>
    typeof text === "string"
      ? text.replace(TOKEN, (_, name) => tokens[name] || `{${name}}`)
      : text;
  const next = { ...lines };
  for (const key of Object.keys(next)) next[key] = fill(next[key]);
  return next;
}
