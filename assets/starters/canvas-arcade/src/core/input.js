// Entrada: teclado, ponteiro e gamepad reduzidos a uma intenção.
//
// As regras nunca veem eventos — recebem `{ move, dash, bank }`. Isso é o que
// permite rodar a partida headless, repetir um replay e comparar dispositivos:
// o mesmo teste que prova a regra prova a intenção.
//
// `dispose()` remove exatamente os listeners que registrou. Listener sobrevivente
// é a causa mais comum de comportamento duplicado depois de reiniciar.

import { DEFAULT_BINDINGS } from "./settings.js";

const MOVE_DEADZONE = 0.28;

export function createInput(options = {}) {
  const target = options.target ?? (typeof window !== "undefined" ? window : null);
  const surface = options.surface ?? null;
  const readGamepads =
    options.gamepads ??
    (() =>
      typeof navigator !== "undefined" && navigator.getGamepads ? navigator.getGamepads() : []);
  let bindings = { ...DEFAULT_BINDINGS, ...(options.bindings ?? {}) };

  const held = new Set();
  const pressed = new Set();
  const gamepadHeld = new Set();
  const pointer = { active: false, aim: null, dash: false, bank: false };
  const registered = [];

  function on(element, type, handler, opts) {
    if (!element || typeof element.addEventListener !== "function") return;
    element.addEventListener(type, handler, opts);
    registered.push([element, type, handler, opts]);
  }

  function actionsFor(code) {
    return Object.keys(bindings).filter((action) => bindings[action].includes(code));
  }

  function onKeyDown(event) {
    const code = event.code ?? event.key;
    if (!actionsFor(code).length) return;
    // Setas e espaço rolam a página; o jogo já consumiu a tecla.
    if (typeof event.preventDefault === "function") event.preventDefault();
    if (!held.has(code)) {
      for (const action of actionsFor(code)) pressed.add(action);
    }
    held.add(code);
  }

  function onKeyUp(event) {
    held.delete(event.code ?? event.key);
  }

  function onBlur() {
    // Perder o foco com a tecla apertada travaria o movimento para sempre.
    held.clear();
    pointer.active = false;
    pointer.aim = null;
  }

  function pointerAim(event) {
    if (!surface || typeof surface.getBoundingClientRect !== "function") return null;
    const rect = surface.getBoundingClientRect();
    if (!rect.width || !rect.height) return null;
    return {
      x: Math.min(1, Math.max(0, (event.clientX - rect.left) / rect.width)),
      y: Math.min(1, Math.max(0, (event.clientY - rect.top) / rect.height)),
    };
  }

  function onPointerDown(event) {
    const position = pointerAim(event);
    if (!position) return;
    pointer.active = true;
    pointer.aim = position.x;
    // Faixa inferior guarda a corrente; o resto da tela é dash.
    if (position.y > 0.82) {
      pointer.bank = true;
      pressed.add("bank");
    } else {
      pointer.dash = true;
      pressed.add("dash");
    }
  }

  function onPointerMove(event) {
    if (!pointer.active) return;
    const position = pointerAim(event);
    if (position) pointer.aim = position.x;
  }

  function onPointerUp() {
    pointer.active = false;
    pointer.aim = null;
    pointer.dash = false;
    pointer.bank = false;
  }

  on(target, "keydown", onKeyDown);
  on(target, "keyup", onKeyUp);
  on(target, "blur", onBlur);
  on(surface, "pointerdown", onPointerDown);
  on(surface, "pointermove", onPointerMove);
  on(surface, "pointerup", onPointerUp);
  on(surface, "pointercancel", onPointerUp);

  function pollGamepads() {
    gamepadHeld.clear();
    let axis = 0;
    for (const pad of readGamepads() ?? []) {
      if (!pad) continue;
      const value = pad.axes?.[0] ?? 0;
      if (Math.abs(value) > Math.abs(axis)) axis = value;
      if (pad.buttons?.[14]?.pressed) gamepadHeld.add("left");
      if (pad.buttons?.[15]?.pressed) gamepadHeld.add("right");
      if (pad.buttons?.[0]?.pressed) gamepadHeld.add("dash");
      if (pad.buttons?.[2]?.pressed) gamepadHeld.add("bank");
      if (pad.buttons?.[9]?.pressed) gamepadHeld.add("pause");
    }
    if (axis < -MOVE_DEADZONE) gamepadHeld.add("left");
    if (axis > MOVE_DEADZONE) gamepadHeld.add("right");
  }

  function isHeld(action) {
    return bindings[action]?.some((code) => held.has(code)) || gamepadHeld.has(action);
  }

  return {
    // Consome as bordas: uma intenção lida é uma intenção entregue.
    intent(playerAim = null) {
      pollGamepads();
      let move = 0;
      if (isHeld("left")) move -= 1;
      if (isHeld("right")) move += 1;
      if (move === 0 && pointer.active && pointer.aim !== null && playerAim !== null) {
        const delta = pointer.aim - playerAim;
        if (Math.abs(delta) > 0.02) move = delta > 0 ? 1 : -1;
      }
      const result = {
        move,
        dash: pressed.has("dash") || isHeld("dash") || pointer.dash,
        bank: pressed.has("bank") || isHeld("bank") || pointer.bank,
        pause: pressed.has("pause"),
        reset: pressed.has("reset"),
      };
      pressed.clear();
      pointer.dash = false;
      pointer.bank = false;
      return result;
    },
    rebind(action, codes) {
      if (!(action in bindings) || !Array.isArray(codes) || !codes.length) return false;
      bindings = { ...bindings, [action]: [...codes] };
      return true;
    },
    get bindings() {
      return bindings;
    },
    listenerCount() {
      return registered.length;
    },
    dispose() {
      while (registered.length) {
        const [element, type, handler, opts] = registered.pop();
        element.removeEventListener(type, handler, opts);
      }
      held.clear();
      pressed.clear();
      gamepadHeld.clear();
    },
  };
}
