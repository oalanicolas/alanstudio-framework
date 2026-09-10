// Entrada: teclado, ponteiro e gamepad reduzidos a intenção e comandos.
// No gamepad, Select (8) reinicia: sem isso o verbo fecha e a partida
// não recomeça só com o controle. `lastSource` guarda quem falou por
// último para o aviso e o overlay nomearem esse mapa — não o manifesto.
// O gesto acorda o mixer (`unlock`): o resume no quadro chega
// tarde e o primeiro verbo fica mudo. Tecla e toque já pediam.
// Sem isto o controle marcava a superfície e a porta falava
// no vazio. Pedir resume não é mix ouvido. O aparelho pode
// recusar o gesto do pad — `heard` continua falso.
// Na porta o arraste move sem abrir; o tap abre — inclusive
// na faixa da guarda, na primeira visita. Depois da partida
// a mesma faixa pede seed nova; o campo repete a última.
// Sem isto o polegar no primeiro gesto
// caía na faixa e a porta calava. No campo o down de cima
// continua o avanço; a faixa inferior continua guardando.
// O avanço é o aperto, não o segurar: teclado, toque e A do
// controle leem a borda. Sem isto a porta abria e o mesmo
// hold disparava o ofício, e no campo o cooldown virava
// metralhadora. A guarda continua nível — segurar ainda
// converte o orbe do mesmo quadro.
// O recado foca o campo no fim. Sem isto Espaço e R
// disparavam o verbo enquanto a pessoa escrevia.
// Escrever no disco não é felt.
// O botão do remap (e o Gravar/Copiar) também é casca.
// Sem isto o Espaço ativava o controle e avançava.
// Botão no disco não é felt.
// O toque só escutava o canvas. Sem a captura, sair
// do campo deixava o corpo andando. Captura no disco
// não é felt.
// Na pausa o tap retoma. Sem isto a aba escondida
// no telefone sentava e Esc/P não existem no toque.
// No campo o relógio pausa. Sem isto o telefone
// só retomava — Esc e P não existem no polegar.
// Na porta o canto continua abrindo. Espaço na
// pausa continua só intenção. Toque no
// disco não é felt.
// Esconder a aba perde o keyup. Sem o visibilitychange
// o corpo seguia o último hold. Perder o foco da janela
// (barra, DevTools) também some o keyup e deixava o
// aperto pendente virar ofício. Soltar no disco não é felt.
// O pad que some some o hold no poll. Sem o
// `gamepaddisconnected` o relógio seguia e o corpo
// morria sozinho. Sentar no disco não é felt.
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
const DRAG_DEADZONE = 0.04;

// O relógio mora no canto alto direito. Faixa larga
// come o avanço; faixa estreita demais some o alvo.
// Números no disco não são sessão observada.
export const PAUSE_CORNER = { x: 0.88, y: 0.14 };

export function pauseCorner(position) {
  return Boolean(
    position
    && Number.isFinite(position.x)
    && Number.isFinite(position.y)
    && position.x >= PAUSE_CORNER.x
    && position.y <= PAUSE_CORNER.y,
  );
}

export function isTypingTarget(event) {
  const node = event?.target;
  if (!node || typeof node !== "object") return false;
  const tag = String(node.tagName || "").toLowerCase();
  if (tag === "input" || tag === "textarea" || tag === "select") return true;
  return Boolean(node.isContentEditable);
}

export function isChromeTarget(event) {
  // Campo é casca. Botão também: Espaço ativa o controle,
  // não o verbo. Ícone dentro do botão conta igual.
  if (isTypingTarget(event)) return true;
  let node = event?.target;
  for (let depth = 0; depth < 6 && node && typeof node === "object"; depth += 1) {
    if (String(node.tagName || "").toLowerCase() === "button") return true;
    node = node.parentElement ?? node.parentNode ?? null;
  }
  return false;
}

export function createInput(options = {}) {
  const target = options.target ?? (typeof window !== "undefined" ? window : null);
  const surface = options.surface ?? null;
  const readGamepads =
    options.gamepads ??
    (() =>
      typeof navigator !== "undefined" && navigator.getGamepads ? navigator.getGamepads() : []);
  let bindings = { ...DEFAULT_BINDINGS, ...(options.bindings ?? {}) };
  const unlock = typeof options.unlock === "function" ? options.unlock : null;
  const visibility =
    options.visibility
    ?? (typeof document !== "undefined" ? document : null);

  const held = new Set();
  const pressed = new Set();
  const gamepadHeld = new Set();
  const padCommandHeld = new Set();
  let padDashDown = false;
  const pointer = {
    active: false,
    aim: null,
    dash: false,
    bank: false,
    originX: null,
    originY: null,
    dragged: false,
  };
  const registered = [];
  let lastSource = "keyboard";
  // No campo o toque de cima avança no down — o verbo precisa
  // do quadro. Na porta o mesmo down abria o ciclo e o aviso
  // de mover mentia. Arraste no disco não é sessão observada.
  let dashOnPress = true;
  // Na primeira visita o tap de baixo também abre.
  // Depois da partida a mesma faixa pede seed nova —
  // R não existe no polegar. Sem isto o toque só
  // repetia. Superfície no disco não é sessão.
  let titleNewOnBank = false;

  function noteSource(source) {
    lastSource = source;
  }

  function wake() {
    if (!unlock) return;
    try {
      unlock();
    } catch {
      /* retomar o contexto não pode quebrar o gesto */
    }
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
    // O painel foca o recado no over. Sem isto o espaço
    // avançava e o R recomeçava no meio da frase.
    // O botão focado também é casca: Espaço ativa o
    // controle e não pode avançar no mesmo aperto.
    if (isChromeTarget(event)) return;
    // A escuta do remap come a tecla na captura. Sem isto
    // o bubble ainda avançava se a ordem no mesmo nó
    // invertia. Tecla no disco não é felt.
    if (event?.defaultPrevented) return;
    const code = event.code ?? event.key;
    if (!actionsFor(code).length) return;
    noteSource("keyboard");
    wake();
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

  function releaseHold() {
    // Perder o foco com a tecla apertada travaria o movimento para sempre.
    held.clear();
    pointer.active = false;
    pointer.aim = null;
    pointer.dash = false;
    pointer.bank = false;
    pointer.originX = null;
    pointer.originY = null;
    pointer.dragged = false;
  }

  function releaseSession() {
    // Esconder a aba perde o keyup. Sem isto o corpo
    // seguia o último hold. Pad continua no poll.
    // Soltar no disco não é felt.
    releaseHold();
    pressed.clear();
  }

  function onVisibility() {
    if (visibility?.hidden !== true) return;
    releaseSession();
  }

  function onBlur() {
    // A aba escondida já solta hold e pressed. Sem isto
    // a barra de endereço e o DevTools deixavam o Space
    // ou o R virarem ofício no quadro seguinte.
    // Soltar no disco não é felt.
    releaseSession();
  }

  function onFocusIn(event) {
    if (!isChromeTarget(event)) return;
    releaseHold();
    // O aperto que ainda não foi lido não vira ofício no recado.
    pressed.clear();
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
    wake();
    // No campo o relógio já mora no canto. Sem isto
    // o telefone só retomava. Na porta dashOnPress
    // é falso e o canto continua abrindo. Toque no
    // disco não é felt.
    if (dashOnPress && pauseCorner(position)) {
      pressed.add("pause");
      return;
    }
    pointer.active = true;
    pointer.aim = position.x;
    pointer.originX = position.x;
    pointer.originY = position.y;
    pointer.dragged = false;
    // Faixa inferior guarda a corrente; o resto da tela é dash
    // no campo. Na porta o down não avança — o arraste ensaia.
    if (position.y > 0.82) {
      pointer.bank = true;
      pressed.add("bank");
    } else if (dashOnPress) {
      pointer.dash = true;
      pressed.add("dash");
    }
    // Sem isto o up e o move morriam na borda e o
    // corpo seguia o último aim. Captura recusada
    // não pode derrubar o gesto.
    if (typeof surface.setPointerCapture === "function" && Number.isFinite(event?.pointerId)) {
      try {
        surface.setPointerCapture(event.pointerId);
      } catch {
        /* captura recusada não pode derrubar o gesto */
      }
    }
  }

  function onPointerMove(event) {
    if (!pointer.active) return;
    const position = pointerAim(event);
    if (!position) return;
    pointer.aim = position.x;
    if (pointer.originX !== null && pointer.originY !== null) {
      const dx = position.x - pointer.originX;
      const dy = position.y - pointer.originY;
      if (dx * dx + dy * dy > DRAG_DEADZONE * DRAG_DEADZONE) pointer.dragged = true;
    }
  }

  function onLostCapture() {
    // O up já soltou. Sem isto o lostpointercapture
    // comia o tap da porta.
    if (!pointer.active) return;
    onPointerUp();
  }

  function onPointerUp() {
    // Na porta o tap (sem arraste) abre — a faixa da guarda
    // também. No campo a faixa não existe: o down de baixo
    // já guardou e o de cima já avançou. Soltar não dispara
    // de novo. Toque no disco não é sessão observada.
    if (
      !dashOnPress
      && pointer.active
      && !pointer.dragged
      && pointer.originY !== null
    ) {
      if (titleNewOnBank && pointer.originY > 0.82) {
        pressed.add("reset");
      } else {
        pointer.dash = true;
        pressed.add("dash");
      }
    } else {
      pointer.dash = false;
    }
    pointer.active = false;
    pointer.aim = null;
    pointer.bank = false;
    pointer.originX = null;
    pointer.originY = null;
    pointer.dragged = false;
  }

  on(target, "keydown", onKeyDown);
  on(target, "keyup", onKeyUp);
  on(target, "blur", onBlur);
  on(target, "focusin", onFocusIn);
  on(visibility, "visibilitychange", onVisibility);
  on(surface, "pointerdown", onPointerDown);
  on(surface, "pointermove", onPointerMove);
  on(surface, "pointerup", onPointerUp);
  on(surface, "pointercancel", onPointerUp);
  on(surface, "lostpointercapture", onLostCapture);

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
    if (speaking) {
      noteSource("gamepad");
      // Tecla e toque já pediam o resume no gesto. O pad
      // falava e o mixer continuava suspenso: live da porta
      // e o primeiro avanço iam para a fila e não saíam.
      // Pedir não é mix ouvido.
      wake();
    }
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
      const padDash = gamepadHeld.has("dash");
      const padDashPressed = padDash && !padDashDown;
      padDashDown = padDash;
      const result = {
        move,
        dash: pressed.has("dash") || padDashPressed || pointer.dash,
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
    setDashOnPress(next) {
      dashOnPress = next !== false;
      return dashOnPress;
    },
    setTitleNewOnBank(next) {
      titleNewOnBank = next === true;
      return titleNewOnBank;
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
      padDashDown = false;
    },
  };
}
