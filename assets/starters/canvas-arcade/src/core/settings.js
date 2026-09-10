// Preferências: acessibilidade, mixagem e remapeamento.
//
// Vivem em chave própria, separada do progresso. O padrão de redução de
// movimento vem do sistema operacional quando ele informa, porque quem já pediu
// menos movimento não deveria precisar pedir de novo aqui.
//
// Uma opção só existe quando tem consumidor: cada campo abaixo é lido em
// `render.js`, `audio.js`, `input.js` ou `rules.js`. `spawnProfile` escolhe
// a mesa de chuva; `look` escolhe o look de arte. Nome desconhecido cai
// no padrão. `contrast` não é look: alto contraste continua sendo o modo
// de alcance. `colorblind` também é alcance: o par do padrão
// só veste chuva que ainda compartilha o eixo; look que já
// separa quente e frio permanece.

import { readJson, writeJson } from "./storage.js";

export const SETTINGS_KEY = "settings";
export const SETTINGS_SCHEMA = 1;

export const DEFAULT_BINDINGS = {
  left: ["ArrowLeft", "KeyA"],
  right: ["ArrowRight", "KeyD"],
  dash: ["Space", "KeyK"],
  bank: ["ArrowDown", "KeyS", "KeyJ"],
  pause: ["Escape", "KeyP"],
  reset: ["KeyR"],
};

// Cluster direito: IJKL + P/O. Não prova sessão com uma só mão observada.
export const ONE_HAND_BINDINGS = {
  left: ["KeyJ"],
  right: ["KeyL"],
  dash: ["KeyI"],
  bank: ["KeyK"],
  pause: ["KeyP"],
  reset: ["KeyO"],
};

// Palco conservador: overlap de one-shots não usa o teto do arquivo.
// Folga não é loudness aprovado; `heard` continua falso.
export const DEFAULT_BUSES = { master: 0.7, music: 0.45, sfx: 0.62, ui: 0.55 };

// Relógio da partida, não a queda da chuva. Assistência continua sendo
// alcance e invuln; este knob só dilata o milissegundo real.
export const GAME_SPEED_MIN = 0.5;
export const GAME_SPEED_MAX = 1;
export const UI_SCALE_MIN = 0.75;
export const UI_SCALE_MAX = 2;

export function defaultSettings(environment = {}) {
  return {
    schema: SETTINGS_SCHEMA,
    reducedMotion: Boolean(environment.prefersReducedMotion),
    highContrast: Boolean(environment.prefersHighContrast),
    colorblind: false,
    captions: true,
    assist: false,
    gameSpeed: 1,
    oneHand: false,
    uiScale: 1,
    spawnProfile: "spawn",
    look: "normal",
    buses: structuredCloneish(DEFAULT_BUSES),
    bindings: structuredCloneish(DEFAULT_BINDINGS),
    keptBindings: structuredCloneish(DEFAULT_BINDINGS),
  };
}

function structuredCloneish(value) {
  return JSON.parse(JSON.stringify(value));
}

const clamp01 = (value, fallback) =>
  Number.isFinite(value) ? Math.min(1, Math.max(0, value)) : fallback;

// `base` é o que um campo inválido preserva. Ao carregar do disco isso é o
// padrão; ao aplicar uma alteração é o valor atual, para que um campo recusado
// não derrube silenciosamente uma preferência que a pessoa já tinha escolhido.
export function normalizeSettings(raw, environment = {}, base = defaultSettings(environment)) {
  if (!raw || typeof raw !== "object") return base;
  const buses = { ...base.buses };
  if (raw.buses && typeof raw.buses === "object") {
    for (const name of Object.keys(base.buses)) {
      buses[name] = clamp01(raw.buses[name], base.buses[name]);
    }
  }
  const bindings = readBindings(raw.bindings, base.bindings);
  const oneHand = typeof raw.oneHand === "boolean" ? raw.oneHand : base.oneHand;
  const keptBindings = readKeptBindings(raw, bindings, oneHand, base);
  return {
    schema: SETTINGS_SCHEMA,
    reducedMotion: typeof raw.reducedMotion === "boolean" ? raw.reducedMotion : base.reducedMotion,
    highContrast: typeof raw.highContrast === "boolean" ? raw.highContrast : base.highContrast,
    colorblind: typeof raw.colorblind === "boolean" ? raw.colorblind : base.colorblind,
    captions: typeof raw.captions === "boolean" ? raw.captions : base.captions,
    assist: typeof raw.assist === "boolean" ? raw.assist : base.assist,
    gameSpeed: Number.isFinite(raw.gameSpeed)
      ? Math.min(GAME_SPEED_MAX, Math.max(GAME_SPEED_MIN, raw.gameSpeed))
      : base.gameSpeed,
    oneHand,
    uiScale: Number.isFinite(raw.uiScale)
      ? Math.min(UI_SCALE_MAX, Math.max(UI_SCALE_MIN, raw.uiScale))
      : base.uiScale,
    spawnProfile:
      typeof raw.spawnProfile === "string" && /^[a-z][a-z0-9]{0,31}$/.test(raw.spawnProfile)
        ? raw.spawnProfile
        : base.spawnProfile,
    look:
      typeof raw.look === "string" && /^[a-z][a-z0-9]{0,31}$/.test(raw.look)
        ? raw.look
        : base.look,
    buses,
    bindings,
    keptBindings,
  };
}

export function readBindings(raw, fallback = DEFAULT_BINDINGS) {
  const bindings = structuredCloneish(fallback);
  if (!raw || typeof raw !== "object") return bindings;
  for (const action of Object.keys(fallback)) {
    const codes = raw[action];
    // Um remapeamento vazio tornaria a ação inalcançável: mantém o padrão.
    if (Array.isArray(codes) && codes.length && codes.every((code) => typeof code === "string")) {
      bindings[action] = [...codes];
    }
  }
  return bindings;
}

function readKeptBindings(raw, bindings, oneHand, base) {
  if (raw.keptBindings && typeof raw.keptBindings === "object") {
    return readBindings(raw.keptBindings, base.keptBindings ?? DEFAULT_BINDINGS);
  }
  // Save antigo: se já estava no preset, não inventa remap.
  if (oneHand) return structuredCloneish(DEFAULT_BINDINGS);
  return structuredCloneish(bindings);
}

// Liga o cluster direito e guarda o conjunto vigente.
// Desligar devolve o que estava guardado, não o padrão.
export function applyOneHand(settings, enabled) {
  if (enabled) {
    const kept = settings.oneHand ? settings.keptBindings : settings.bindings;
    return {
      oneHand: true,
      keptBindings: structuredCloneish(kept ?? DEFAULT_BINDINGS),
      bindings: structuredCloneish(ONE_HAND_BINDINGS),
    };
  }
  return {
    oneHand: false,
    bindings: structuredCloneish(settings.keptBindings ?? DEFAULT_BINDINGS),
  };
}

export function loadSettings(storage, environment = {}) {
  const read = readJson(storage, SETTINGS_KEY);
  if (read.status === "unreadable") {
    return {
      settings: defaultSettings(environment),
      status: "recovered",
      notes: ["preferências ilegíveis preservadas em settings.broken; preferências reiniciadas"],
    };
  }
  return {
    settings: normalizeSettings(read.value, environment),
    status: read.status,
    notes: [],
  };
}

// O painel de preferências nomeia a recuperação. A porta não:
// persistLine continua só sessão volátil e gravação recusada.
// A região viva lê a mesma linha do painel na porta e no fim.
// Nomear não é trusted.
export function settingsLine(load, lines = {}) {
  if (load?.status !== "recovered") return "";
  return typeof lines.settings_recovered === "string" ? lines.settings_recovered : "";
}

export function saveSettings(storage, settings) {
  return writeJson(storage, SETTINGS_KEY, settings);
}

export const ENVIRONMENT_QUERIES = {
  prefersReducedMotion: "(prefers-reduced-motion: reduce)",
  prefersHighContrast: "(prefers-contrast: more)",
};

export function detectEnvironment() {
  const query = (text) =>
    typeof matchMedia === "function" ? Boolean(matchMedia(text).matches) : false;
  return {
    prefersReducedMotion: query(ENVIRONMENT_QUERIES.prefersReducedMotion),
    prefersHighContrast: query(ENVIRONMENT_QUERIES.prefersHighContrast),
  };
}

// O boot herda o sistema. Sem isto o pedido no meio da
// sessão ficava no matchMedia e a caixa não vestia.
// Desligar o sistema não apaga a escolha. Pedido no
// disco não é sessão observada.
export function applyEnvironment(settings, environment = {}) {
  const patch = {};
  if (environment.prefersReducedMotion === true && settings?.reducedMotion !== true) {
    patch.reducedMotion = true;
  }
  if (environment.prefersHighContrast === true && settings?.highContrast !== true) {
    patch.highContrast = true;
  }
  return patch;
}

export function watchEnvironment(onChange, media) {
  const query = typeof media === "function"
    ? media
    : typeof matchMedia === "function" ? matchMedia : null;
  if (typeof onChange !== "function" || typeof query !== "function") return () => {};
  const hooks = [];
  for (const [key, text] of Object.entries(ENVIRONMENT_QUERIES)) {
    let mql;
    try {
      mql = query(text);
    } catch {
      continue;
    }
    if (!mql) continue;
    const handler = () => {
      onChange({ [key]: Boolean(mql.matches) });
    };
    if (typeof mql.addEventListener === "function") {
      mql.addEventListener("change", handler);
      hooks.push(() => mql.removeEventListener("change", handler));
    } else if (typeof mql.addListener === "function") {
      mql.addListener(handler);
      hooks.push(() => mql.removeListener(handler));
    }
  }
  return () => {
    for (const stop of hooks) stop();
  };
}
