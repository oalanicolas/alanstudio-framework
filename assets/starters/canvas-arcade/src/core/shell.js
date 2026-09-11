// A casca da página. O campo já vestia o look; o HTML ficava no
// token frio do padrão. A página reusa a paleta vigente. O knob
// de escala já crescia o canvas; a casca agora lê o mesmo número.
// Select e faixa nativos ficavam no widget do sistema; agora
// leem `--page`, `--ink` e `--accent`. Token no disco não é
// direção observada nem sessão de alcance.

import { UI_SCALE_MAX, UI_SCALE_MIN } from "./settings.js";

export const SHELL_VARS = {
  "--ink": "text",
  "--muted": "muted",
  "--surface": "field",
  "--page": "background",
  "--edge": "plateEdge",
  "--accent": "orb",
};

export function shellVars(palette) {
  if (!palette || typeof palette !== "object") return null;
  const vars = {};
  for (const [name, token] of Object.entries(SHELL_VARS)) {
    const value = palette[token];
    if (typeof value !== "string" || !value.trim()) return null;
    vars[name] = value;
  }
  return vars;
}

export function applyShell(target, palette) {
  const vars = shellVars(palette);
  if (!vars || !target?.style?.setProperty) return false;
  for (const [name, value] of Object.entries(vars)) {
    target.style.setProperty(name, value);
  }
  return true;
}

export function scaleVar(uiScale) {
  if (!Number.isFinite(uiScale)) return null;
  const scale = Math.min(UI_SCALE_MAX, Math.max(UI_SCALE_MIN, uiScale));
  return { "--ui-scale": String(scale) };
}

export function applyScale(target, uiScale) {
  const vars = scaleVar(uiScale);
  if (!vars || !target?.style?.setProperty) return false;
  target.style.setProperty("--ui-scale", vars["--ui-scale"]);
  return true;
}

// A faixa já andava. O número já estava nas preferências.
// Sem a saída, 75% some. Nomear não é sessão observada.
export const KNOB_IDS = ["gameSpeed", "uiScale", "master", "sfx", "music", "ui"];

export function knobText(value) {
  if (!Number.isFinite(value)) return "";
  return `${Math.round(value * 100)}%`;
}

export function knobValues(settings = {}) {
  return {
    gameSpeed: settings.gameSpeed,
    uiScale: settings.uiScale,
    master: settings.buses?.master,
    sfx: settings.buses?.sfx,
    music: settings.buses?.music,
    ui: settings.buses?.ui,
  };
}

export function applyKnobs(root, settings) {
  if (!root || typeof root.getElementById !== "function") return false;
  const values = knobValues(settings);
  let painted = false;
  for (const name of KNOB_IDS) {
    const text = knobText(values[name]);
    const input = root.getElementById(name);
    const output = root.getElementById(`${name}-readout`);
    if (input && Number.isFinite(values[name])) {
      input.value = String(values[name]);
      if (typeof input.setAttribute === "function") input.setAttribute("aria-valuetext", text);
    }
    if (output) {
      output.textContent = text;
      painted = true;
    }
  }
  return painted;
}
