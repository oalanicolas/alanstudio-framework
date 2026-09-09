// Montagem do jogo e contrato de ciclo de vida.
//
// Os nomes abaixo — pause, reset, seed, observe, act, advance, capture,
// dispose — são o vocabulário de inspeção do harness. Aqui eles são
// **implementados**, não mencionados: `tests/lifecycle.test.mjs` e
// `tests/determinism.test.mjs` provam cada um. É essa prova, não a presença do
// nome, que move a dimensão `state_trust` da barra de acabamento.

import { createLoop } from "./core/loop.js";
import { createInput } from "./core/input.js";
import { browserStorage } from "./core/storage.js";
import { loadProgress, recordRun, saveProgress } from "./core/save.js";
import { detectEnvironment, loadSettings, normalizeSettings, saveSettings } from "./core/settings.js";
import { fingerprint } from "./core/hash.js";
import { createAudio } from "./game/audio.js";
import { loadRoleFiles } from "./game/sfx.js";
import { createRenderer } from "./game/render.js";
import { advance as advanceRules, createState, neutralIntent, FIELD, TICK_HZ } from "./game/rules.js";
import { coachHint } from "./game/coach.js";

export function createGame(options = {}) {
  const canvas = options.canvas ?? null;
  const storage = options.storage ?? browserStorage("canvas-arcade");
  const environment = options.environment ?? detectEnvironment();
  const eventTarget = options.eventTarget ?? (typeof window !== "undefined" ? window : null);

  let settings = loadSettings(storage, environment).settings;
  const progressLoad = loadProgress(storage);
  let progress = progressLoad.progress;
  let state = createState(options.seed ?? randomSeed(), { assist: settings.assist });
  let queued = neutralIntent();
  let recorded = false;
  let disposed = false;

  const input = options.input ?? createInput({ target: eventTarget, surface: canvas, bindings: settings.bindings });
  const audio = options.audio ?? createAudio({ settings });
  const renderer = canvas ? createRenderer(canvas) : null;
  // Sem canvas (teste headless) não busca arquivo: o fetch relativo não tem
  // servidor e atrasaria o teste. No browser, o arquivo em public/sfx precisa
  // chegar ao mixer — senão `roles` verde e o jogo mudo são a mesma coisa.
  if ((options.loadSfx ?? Boolean(canvas)) && typeof (options.fetch ?? globalThis.fetch) === "function") {
    const fetchFn = options.fetch ?? globalThis.fetch.bind(globalThis);
    const decode = options.decodeSfx ?? ((bytes) => audio.decode(bytes));
    loadRoleFiles(audio, { fetch: fetchFn, decode }).catch(() => {});
  }

  const loop = createLoop({
    stepMs: 1000 / TICK_HZ,
    now: options.now,
    schedule: options.schedule,
    cancel: options.cancel,
    update: () => step(readIntent()),
    render: (frame) => present(frame),
  });

  function readIntent() {
    return input.intent(state.player.x / FIELD.width);
  }

  // Comandos são lidos na apresentação, não na simulação: o laço continua
  // desenhando em pausa, mas não atualiza. Ler a tecla de pausa junto com a
  // intenção tornava impossível despausar pelo teclado — só um `resume()`
  // programático saía dali, e nenhum teste passava por esse caminho.
  function readCommands() {
    if (disposed) return;
    const command = input.commands();
    if (command.reset) handle.reset();
    else if (command.pause) togglePause();
  }

  function step(intent) {
    advanceRules(state, intent);
    for (const event of state.events) {
      audio.play(event.type);
    }
    if (state.phase === "over" && !recorded) {
      recorded = true;
      progress = recordRun(progress, state);
      saveProgress(storage, progress, progressLoad);
    }
  }

  function present(frame) {
    readCommands();
    audio.update();
    if (!renderer) return;
    renderer.draw(state, frame, settings, {
      captions: audio.captions(),
      best: progress.best,
      hint: coachHint(state),
    });
  }

  function togglePause() {
    if (loop.paused) loop.resume();
    else loop.pause();
  }

  const onVisibility = () => {
    if (typeof document !== "undefined" && document.hidden) loop.pause();
  };
  if (eventTarget && typeof document !== "undefined" && typeof document.addEventListener === "function") {
    document.addEventListener("visibilitychange", onVisibility);
  }

  const handle = {
    // Ciclo de vida
    start() {
      loop.start();
      return handle;
    },
    pause() {
      loop.pause();
      return true;
    },
    resume() {
      loop.resume();
      return true;
    },
    get paused() {
      return loop.paused;
    },
    reset(seed = state.seed) {
      state = createState(seed, { assist: settings.assist });
      queued = neutralIntent();
      recorded = false;
      loop.resume();
      return handle.observe();
    },
    seed(value) {
      if (value === undefined) return state.seed;
      return handle.reset(value);
    },
    // Observação e controle explícito, para teste e replay
    observe() {
      const snapshot = JSON.parse(JSON.stringify(state));
      return { ...snapshot, fingerprint: fingerprint(withoutVolatile(snapshot)) };
    },
    act(intent) {
      queued = { ...neutralIntent(), ...intent };
      return queued;
    },
    // Sonda deliberadamente sujeita à pausa: se `advance` avançasse pausado,
    // a prova de que a pausa congela a simulação não valeria nada.
    advance(steps = 1) {
      if (disposed || loop.paused) return handle.observe();
      for (let index = 0; index < steps; index += 1) {
        step(queued);
        queued = neutralIntent();
      }
      return handle.observe();
    },
    capture() {
      if (!canvas || typeof canvas.toDataURL !== "function") return null;
      return canvas.toDataURL("image/png");
    },
    dispose() {
      if (disposed) return false;
      disposed = true;
      loop.dispose();
      input.dispose();
      audio.dispose();
      if (typeof document !== "undefined" && typeof document.removeEventListener === "function") {
        document.removeEventListener("visibilitychange", onVisibility);
      }
      return true;
    },
    get disposed() {
      return disposed;
    },
    // Instrumentos: o que a barra de acabamento pede como evidência
    metrics() {
      return loop.metrics();
    },
    audioGaps() {
      return audio.missing();
    },
    get progress() {
      return { ...progress, status: progressLoad.status, notes: progressLoad.notes };
    },
    get settings() {
      return settings;
    },
    updateSettings(patch) {
      settings = normalizeSettings({ ...settings, ...patch }, environment, settings);
      state.assist = settings.assist;
      audio.applySettings(settings);
      for (const [action, codes] of Object.entries(settings.bindings)) input.rebind(action, codes);
      saveSettings(storage, settings);
      return settings;
    },
    resize(width, height) {
      if (renderer) renderer.resize(width, height);
    },
  };
  return handle;
}

// A seed escolhida ao abrir o jogo é aleatória; a partida a partir dela é
// determinística. As duas afirmações são diferentes e as duas importam.
function randomSeed() {
  return Math.floor(Math.random() * 0xffffffff) >>> 0;
}

function withoutVolatile(snapshot) {
  const { events, ...rest } = snapshot;
  return rest;
}

if (typeof document !== "undefined" && typeof window !== "undefined") {
  const canvas = document.querySelector("#stage");
  if (canvas) {
    const game = createGame({ canvas });
    const fit = () => {
      const width = Math.min(window.innerWidth - 24, 960);
      game.resize(width, Math.round((width * FIELD.height) / FIELD.width));
    };
    window.addEventListener("resize", fit);
    fit();
    game.start();
    // Handle de inspeção: pausar, reiniciar e observar sem abrir o código.
    window.__game = game;
  }
}
