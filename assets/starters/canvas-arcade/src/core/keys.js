// Rótulo das teclas vivas — e do aparelho que falou por último.
//
// O HTML estático ensina o padrão. A tabela `#commands` passa a
// nomear o teclado vigente — remapeamento e uma mão — e mantém
// toque e controle no sufixo. O aviso do primeiro ciclo nomeia
// teclado (ou o remapeamento), toque e controle juntos; o dash e o
// mapa da superfície que falou também ganham passo no campo.
// Overlay e HUD confirmam o aparelho que falou por último.
// Na porta o telefone ainda não falou: a placa usa a
// superfície `door` quando o ponteiro é grosso.
// Depois da partida `door.reset` é baixo — a faixa pede
// seed nova. Na pausa a placa usa `pointer` — o token é
// pause, não dash. Reiniciar continua R. Rótulo no texto
// não é sessão observada.

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

export const COMMAND_SURFACES = {
  move: "analógico ou arrastar na tela",
  dash: "botão A, ou toque na área superior",
  bank: "botão X, ou toque na faixa inferior",
  pause: "Start no controle, ou toque no relógio",
  reset: "Select no controle",
};

function joinedKeys(bindings, action) {
  return actionLabels(bindings, action).join(", ") || "—";
}

export function commandRows(bindings) {
  return [
    {
      action: "move",
      title: "Mover",
      text: `${joinedKeys(bindings, "left")} / ${joinedKeys(bindings, "right")}, ${COMMAND_SURFACES.move}`,
    },
    {
      action: "dash",
      title: "Avançar (dash)",
      text: `${joinedKeys(bindings, "dash")}, ${COMMAND_SURFACES.dash}`,
    },
    {
      action: "bank",
      title: "Guardar corrente",
      text: `${joinedKeys(bindings, "bank")}, ${COMMAND_SURFACES.bank}`,
    },
    {
      action: "pause",
      title: "Pausar",
      text: `${joinedKeys(bindings, "pause")} ou ${COMMAND_SURFACES.pause}`,
    },
    {
      action: "reset",
      title: "Reiniciar",
      text: `${joinedKeys(bindings, "reset")} ou ${COMMAND_SURFACES.reset}`,
    },
  ];
}

export function paintCommands(host, bindings) {
  if (!host || typeof host.querySelector !== "function") return;
  for (const row of commandRows(bindings)) {
    const cell = host.querySelector(`[data-command="${row.action}"]`);
    if (cell) cell.textContent = row.text;
  }
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
    pause: "toque",
    bank: "baixo",
    dash: "cima",
  },
  // A porta abre no tap, em qualquer faixa. O mapa
  // pointer chama o dash de cima — e mente aqui,
  // inclusive depois do gesto. lastSource teclado
  // no telefone também mente com Espaço.
  // Superfície no disco não é sessão observada.
  door: {
    dash: "toque",
    // Depois da partida o tap no campo repete a seed.
    // R não existe no polegar. A faixa de baixo — a
    // mesma da guarda no campo — pede seed nova.
    // Superfície no disco não é sessão observada.
    reset: "baixo",
  },
};

export function titleSurface(environment, lastSource = "keyboard") {
  if (lastSource === "gamepad") return lastSource;
  if (lastSource === "pointer" || environment?.pointer?.coarse) return "door";
  return lastSource;
}

// Na pausa o telefone ainda não falou. Esc e P não
// existem no polegar. O tap já retoma. A porta usa
// `door` (só o dash); aqui o token é pause. lastSource
// teclado mente com Esc. Superfície no disco não é
// sessão observada. Reiniciar continua R — o toque
// não reseta.
export function pauseSurface(environment, lastSource = "keyboard") {
  if (lastSource === "gamepad") return lastSource;
  if (lastSource === "pointer" || environment?.pointer?.coarse) return "pointer";
  return lastSource;
}

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
