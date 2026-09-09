// Entrada: teclado, ponteiro e gamepad reduzidos a intenção e comandos.
// No gamepad, Select (8) reinicia: sem isso o verbo fecha e a partida
// não recomeça só com o controle. `lastSource` guarda quem falou por
// último para o aviso e o overlay nomearem esse mapa — não o manifesto.
// Sessão no aparelho não foi observada.
//
// As regras nunca veem eventos — recebem `{ move, dash, bank }`. Isso é o que
// permite rodar a partida headless, repetir um replay e comparar dispositivos:
// o mesmo teste que prova a regra prova a intenção.
//
// Pausar e reiniciar são **comandos**, não intenção, e por isso saem por
// `commands()`. A intenção é consumida pela simulação, que não roda em pausa;
// um comando lido junto com ela seria impossível de dar justamente quando é
// mais necessário — despausar exigiria despausar antes.
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
  const padCommandHeld = new Set();
  const pointer = { active: false, aim: null, dash: false, bank: false };
  const registered = [];
  let lastSource = "keyboard";

  function noteSource(source) {
    lastSource = source;
  }

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
    noteSource("keyboard");
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
    noteSource("pointer");
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
    let speaking = false;
    for (const pad of readGamepads() ?? []) {
      if (!pad) continue;
      const value = pad.axes?.[0] ?? 0;
      if (Math.abs(value) > Math.abs(axis)) axis = value;
      if (pad.buttons?.[14]?.pressed) {
        gamepadHeld.add("left");
        speaking = true;
      }
      if (pad.buttons?.[15]?.pressed) {
        gamepadHeld.add("right");
        speaking = true;
      }
      if (pad.buttons?.[0]?.pressed) {
        gamepadHeld.add("dash");
        speaking = true;
      }
      if (pad.buttons?.[2]?.pressed) {
        gamepadHeld.add("bank");
        speaking = true;
      }
      if (pad.buttons?.[8]?.pressed) {
        gamepadHeld.add("reset");
        speaking = true;
      }
      if (pad.buttons?.[9]?.pressed) {
        gamepadHeld.add("pause");
        speaking = true;
      }
    }
    if (axis < -MOVE_DEADZONE) {
      gamepadHeld.add("left");
      speaking = true;
    }
    if (axis > MOVE_DEADZONE) {
      gamepadHeld.add("right");
      speaking = true;
    }
    if (speaking) noteSource("gamepad");
  }

  function isHeld(action) {
    return bindings[action]?.some((code) => held.has(code)) || gamepadHeld.has(action);
  }

  const COMMANDS = ["pause", "reset"];

  return {
    // Comandos do invólucro, lidos a cada quadro mesmo em pausa. No gamepad o
    // botão é contínuo, então a borda é detectada aqui; no teclado ela já veio
    // do keydown.
    commands() {
      pollGamepads();
      const result = {};
      for (const action of COMMANDS) {
        const padDown = gamepadHeld.has(action);
        result[action] = pressed.has(action) || (padDown && !padCommandHeld.has(action));
        if (padDown) padCommandHeld.add(action);
        else padCommandHeld.delete(action);
        pressed.delete(action);
      }
      return result;
    },
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
      };
      // Só as bordas de intenção. Um comando ainda não lido por `commands()`
      // sobrevive a este quadro em vez de ser descartado em silêncio.
      for (const action of pressed) {
        if (!COMMANDS.includes(action)) pressed.delete(action);
      }
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
    get lastSource() {
      return lastSource;
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
      padCommandHeld.clear();
    },
  };
}
