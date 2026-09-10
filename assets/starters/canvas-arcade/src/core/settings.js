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
// de alcance.

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

export function defaultSettings(environment = {}) {
  return {
    schema: SETTINGS_SCHEMA,
    reducedMotion: Boolean(environment.prefersReducedMotion),
    highContrast: Boolean(environment.prefersHighContrast),
    captions: true,
    assist: false,
    gameSpeed: 1,
    oneHand: false,
    uiScale: 1,
    spawnProfile: "spawn",
    look: "normal",
    buses: structuredCloneish(DEFAULT_BUSES),
    bindings: structuredCloneish(DEFAULT_BINDINGS),
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
  const bindings = structuredCloneish(base.bindings);
  if (raw.bindings && typeof raw.bindings === "object") {
    for (const action of Object.keys(base.bindings)) {
      const codes = raw.bindings[action];
      // Um remapeamento vazio tornaria a ação inalcançável: mantém o padrão.
      if (Array.isArray(codes) && codes.length && codes.every((code) => typeof code === "string")) {
        bindings[action] = [...codes];
      }
    }
  }
  return {
    schema: SETTINGS_SCHEMA,
    reducedMotion: typeof raw.reducedMotion === "boolean" ? raw.reducedMotion : base.reducedMotion,
    highContrast: typeof raw.highContrast === "boolean" ? raw.highContrast : base.highContrast,
    captions: typeof raw.captions === "boolean" ? raw.captions : base.captions,
    assist: typeof raw.assist === "boolean" ? raw.assist : base.assist,
    gameSpeed: Number.isFinite(raw.gameSpeed)
      ? Math.min(GAME_SPEED_MAX, Math.max(GAME_SPEED_MIN, raw.gameSpeed))
      : base.gameSpeed,
    oneHand: typeof raw.oneHand === "boolean" ? raw.oneHand : base.oneHand,
    uiScale: Number.isFinite(raw.uiScale) ? Math.min(2, Math.max(0.75, raw.uiScale)) : base.uiScale,
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
  };
}

export function loadSettings(storage, environment = {}) {
  const read = readJson(storage, SETTINGS_KEY);
  return {
    settings: normalizeSettings(read.value, environment),
    status: read.status === "unreadable" ? "recovered" : read.status,
  };
}

export function saveSettings(storage, settings) {
  return writeJson(storage, SETTINGS_KEY, settings);
}

export function detectEnvironment() {
  const query = (text) =>
    typeof matchMedia === "function" ? Boolean(matchMedia(text).matches) : false;
  return {
    prefersReducedMotion: query("(prefers-reduced-motion: reduce)"),
    prefersHighContrast: query("(prefers-contrast: more)"),
  };
}
