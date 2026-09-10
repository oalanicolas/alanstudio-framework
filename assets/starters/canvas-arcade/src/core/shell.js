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
