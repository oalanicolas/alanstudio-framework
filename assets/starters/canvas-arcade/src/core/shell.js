// A casca da página. O campo já vestia o look; o HTML ficava no
// token frio do padrão. A página reusa a paleta vigente. Token no
// disco não é direção observada.

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
