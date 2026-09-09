// Pulso no aparelho. Visual e áudio já marcam o verbo; sem rumble o
// controle fica mudo no impacto. Magnitudes distintas por evento.
// `reducedMotion`, pausa e dispose cancelam. O harness não segurou o
// controle: `felt` continua falso.

import { CONFIG } from "./rules.js";

const ROLES = {
  dash: { ms: "rumbleDashMs", magnitude: "rumbleDash", strong: 0.10 },
  land: { ms: "rumbleLandMs", magnitude: "rumbleLand", strong: 0.14 },
  collect: { ms: "rumbleCollectMs", magnitude: "rumbleCollect", strong: 0.22 },
  bank: { ms: "rumbleBankMs", magnitude: "rumbleBank", strong: 0.38 },
  hit: { ms: "rumbleHitMs", magnitude: "rumbleHit", strong: 0.88 },
  over: { ms: "rumbleOverMs", magnitude: "rumbleOver", strong: 0.62 },
};

function defaultGamepads() {
  return typeof navigator !== "undefined" && navigator.getGamepads ? navigator.getGamepads() : [];
}

function defaultVibrate() {
  return typeof navigator !== "undefined" && typeof navigator.vibrate === "function"
    ? (pattern) => navigator.vibrate(pattern)
    : null;
}

function patternFor(role) {
  const keys = ROLES[role];
  if (!keys) return null;
  const feel = CONFIG.feel;
  return {
    duration: feel[keys.ms],
    weakMagnitude: feel[keys.magnitude],
    strongMagnitude: keys.strong,
  };
}

export function createHaptics(options = {}) {
  const readGamepads = options.gamepads ?? defaultGamepads;
  const vibrate = options.vibrate ?? defaultVibrate();
  let reduced = Boolean(options.settings?.reducedMotion);
  let muted = false;

  function cancel() {
    for (const pad of readGamepads() ?? []) {
      const actuator = pad?.vibrationActuator;
      if (actuator && typeof actuator.reset === "function") {
        try {
          actuator.reset();
        } catch {
          // Actuator ausente ou ocupado não pode derrubar o quadro.
        }
      }
    }
    if (typeof vibrate === "function") {
      try {
        vibrate(0);
      } catch {
        // vibrate(0) é o cancelamento; falha aqui é aparelho, não regra.
      }
    }
  }

  function play(role) {
    if (muted || reduced) return false;
    const pattern = patternFor(role);
    if (!pattern) return false;
    let played = false;
    for (const pad of readGamepads() ?? []) {
      const actuator = pad?.vibrationActuator;
      if (!actuator || typeof actuator.playEffect !== "function") continue;
      try {
        const result = actuator.playEffect("dual-rumble", {
          startDelay: 0,
          duration: pattern.duration,
          weakMagnitude: pattern.weakMagnitude,
          strongMagnitude: pattern.strongMagnitude,
        });
        if (result && typeof result.catch === "function") result.catch(() => {});
        played = true;
      } catch {
        // Sem actuator o fallback abaixo ainda pode falar.
      }
    }
    if (!played && typeof vibrate === "function") {
      try {
        vibrate(pattern.duration);
        played = true;
      } catch {
        return false;
      }
    }
    return played;
  }

  return {
    play,
    applySettings(settings = {}) {
      reduced = Boolean(settings.reducedMotion);
      if (reduced) cancel();
    },
    mute() {
      muted = true;
      cancel();
    },
    unmute() {
      muted = false;
    },
    dispose() {
      muted = true;
      cancel();
    },
  };
}
