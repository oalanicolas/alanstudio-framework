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
import { playReport, LAST_RUN_ROUTE } from "./core/run-report.js";
import { canContinue, canResume, captureHold, loadProgress, recordRun, saveProgress, summarizeRun } from "./core/save.js";
import { detectEnvironment, loadSettings, normalizeSettings, saveSettings } from "./core/settings.js";
import { fingerprint } from "./core/hash.js";
import { createAudio } from "./game/audio.js";
import { createHaptics } from "./game/haptics.js";
import { loadRoleFiles } from "./game/sfx.js";
import { createRenderer } from "./game/render.js";
import { createTrace, finishCurve, traceTick } from "./game/curve.js";
import { advance as advanceRules, attractTick, beginRun, createState, restoreState, neutralIntent, FIELD, TICK_HZ } from "./game/rules.js";
import { copy, resolveLookName, resolveMoodName, resolveSpawnName } from "./game/tables.js";
import { coachHint } from "./game/coach.js";

function readQueryName(options, key, resolve) {
  const raw = options.query
    ?? (typeof location !== "undefined" && typeof location.search === "string" ? location.search : "");
  if (!raw) return null;
  const search = raw.startsWith("?") ? raw.slice(1) : raw;
  const value = new URLSearchParams(search).get(key);
  if (!value) return null;
  const name = resolve(value);
  return name === value ? name : null;
}

function readSpawnQuery(options) {
  return readQueryName(options, "spawn", resolveSpawnName);
}

function readLookQuery(options) {
  return readQueryName(options, "look", resolveLookName);
}

function readMoodQuery(options) {
  return readQueryName(options, "mood", resolveMoodName);
}

export function createGame(options = {}) {
  const canvas = options.canvas ?? null;
  const storage = options.storage ?? browserStorage("canvas-arcade");
  const environment = options.environment ?? detectEnvironment();
  const eventTarget = options.eventTarget ?? (typeof window !== "undefined" ? window : null);

  let settings = loadSettings(storage, environment).settings;
  const queryMood = readMoodQuery(options);
  const querySpawn = readSpawnQuery(options) ?? queryMood;
  const queryLook = readLookQuery(options) ?? queryMood;
  if (querySpawn || queryLook) {
    settings = normalizeSettings(
      {
        ...settings,
        ...(querySpawn ? { spawnProfile: querySpawn } : {}),
        ...(queryLook ? { look: queryLook } : {}),
      },
      environment,
      settings,
    );
  }
  const progressLoad = loadProgress(storage);
  let progress = progressLoad.progress;
  const forcedSeed = options.seed;
  const resuming = forcedSeed === undefined && options.entry !== "title" && canResume(progress);
  const entry = options.entry ?? (canvas && !resuming ? "title" : "playing");
  const resumeSeed = canContinue(progress) ? progress.lastSeed : null;
  const openingSeed = forcedSeed ?? resumeSeed ?? randomSeed();
  let state = resuming && entry === "playing"
    ? restoreState(progress.hold, matchOptions({
      ...settings,
      spawnProfile: progress.hold.spawnProfile ?? settings.spawnProfile,
    }, "playing"))
    : createState(openingSeed, matchOptions(settings, entry));
  let queued = neutralIntent();
  let recorded = false;
  let lastRun = progress.lastRun ?? null;
  let disposed = false;
  let lastPhase = state.phase;
  let trace = createTrace();
  const watchers = new Set();
  function resetTrace() {
    trace = createTrace();
  }
  function offerLastRun(report) {
    if (!canvas) return;
    const fetchFn = options.fetch ?? (typeof fetch === "function" ? fetch : null);
    if (typeof fetchFn !== "function") return;
    fetchFn(LAST_RUN_ROUTE, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(report),
    }).catch(() => {});
  }
  function emitPhase() {
    if (state.phase === lastPhase) return;
    lastPhase = state.phase;
    for (const fn of watchers) fn(state.phase);
  }
  function doorOpen() {
    return canContinue(progress) && (forcedSeed === undefined || forcedSeed === progress.lastSeed);
  }

  const input = options.input ?? createInput({ target: eventTarget, surface: canvas, bindings: settings.bindings });
  const audio = options.audio ?? createAudio({ settings });
  const haptics = options.haptics ?? createHaptics({ settings, gamepads: options.gamepads });
  const renderer = canvas ? createRenderer(canvas) : null;
  // Sem canvas (teste headless) não busca arquivo: o fetch relativo não tem
  // servidor e atrasaria o teste. No browser, o arquivo em public/sfx precisa
  // chegar ao mixer — senão `roles` verde e o jogo mudo são a mesma coisa.
  if ((options.loadSfx ?? Boolean(canvas)) && typeof (options.fetch ?? globalThis.fetch) === "function") {
    const fetchFn = options.fetch ?? globalThis.fetch.bind(globalThis);
    const decode = options.decodeSfx ?? ((bytes) => audio.decode(bytes));
    loadRoleFiles(audio, { fetch: fetchFn, decode })
      .then(() => syncBed())
      .catch(() => {});
  }

  const loop = createLoop({
    stepMs: 1000 / TICK_HZ,
    speed: settings.gameSpeed,
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
    if (state.phase === "title") {
      if (command.reset) handle.reset(randomSeed());
      return;
    }
    if (command.reset) handle.reset();
    else if (command.pause) togglePause();
  }

  function step(intent) {
    if (state.phase === "title") {
      if (intent?.dash) {
        beginRun(state);
        resetTrace();
        for (const event of state.events) {
          audio.play(event.type, event);
          haptics.play(event.type);
        }
        syncBed();
      } else {
        attractTick(state);
      }
      emitPhase();
      return;
    }
    advanceRules(state, intent);
    traceTick(trace, state);
    for (const event of state.events) {
      audio.play(event.type, event);
      haptics.play(event.type);
    }
    if (state.phase === "over" && !recorded) {
      recorded = true;
      lastRun = summarizeRun(state);
      progress = recordRun(progress, state);
      saveProgress(storage, progress, progressLoad);
      audio.stop("bed");
      offerLastRun(playReport({
        seed: state.seed,
        spawn: state.spawnProfile,
        run: lastRun,
        curve: finishCurve(trace, state.chain),
        policy: "played",
      }));
    }
    emitPhase();
  }

  function syncBed() {
    if (disposed) return;
    if (loop.paused || state.phase === "over" || state.phase === "title") audio.stop("bed");
    else audio.play("bed");
  }

  function present(frame) {
    readCommands();
    audio.update();
    if (!renderer) return;
    renderer.draw(state, frame, settings, {
      captions: audio.captions(),
      best: progress.best,
      hint: coachHint(state, copy, { surface: input.lastSource }),
      surface: input.lastSource,
      fantasy: copy.fantasy,
      canContinue: doorOpen(),
      lastRun,
    });
  }

  function togglePause() {
    if (loop.paused) {
      loop.resume();
      haptics.unmute();
    } else {
      loop.pause();
      haptics.mute();
    }
  }

  function flush() {
    if (state.phase === "playing") {
      progress = { ...progress, hold: captureHold(state) };
    }
    saveProgress(storage, progress, progressLoad);
    saveSettings(storage, settings);
    return { progress: { ...progress }, settings };
  }

  const onVisibility = () => {
    const hidden = typeof document === "undefined" || document.hidden;
    if (hidden) {
      flush();
      loop.pause();
      audio.stop("bed");
      haptics.mute();
    }
  };
  const onPageHide = () => {
    flush();
  };
  if (eventTarget && typeof eventTarget.addEventListener === "function") {
    eventTarget.addEventListener("pagehide", onPageHide);
    eventTarget.addEventListener("visibilitychange", onVisibility);
  }
  if (
    typeof document !== "undefined"
    && document !== eventTarget
    && typeof document.addEventListener === "function"
  ) {
    document.addEventListener("visibilitychange", onVisibility);
  }

  const handle = {
    // Ciclo de vida
    start() {
      loop.start();
      syncBed();
      return handle;
    },
    pause() {
      loop.pause();
      haptics.mute();
      syncBed();
      flush();
      return true;
    },
    resume() {
      loop.resume();
      haptics.unmute();
      syncBed();
      return true;
    },
    get paused() {
      return loop.paused;
    },
    reset(seed = state.seed) {
      // Com tela, o fim não pula a porta. R no overlay abre a
      // abertura — repetir a seed ou sortear outra. Sem tela o
      // headless continua no tick zero. Reset no meio da partida
      // não muda de fase. Seed explícita (teste, `seed()`) entra
      // jogando — não é o botão do overlay.
      const toTitle = Boolean(canvas) && state.phase === "over" && arguments.length === 0;
      const nextSeed = toTitle ? (progress.lastSeed ?? seed) : seed;
      progress = { ...progress, hold: null };
      saveProgress(storage, progress, progressLoad);
      state = createState(nextSeed, matchOptions(settings, toTitle ? "title" : "playing"));
      queued = neutralIntent();
      recorded = false;
      resetTrace();
      loop.resume();
      haptics.unmute();
      syncBed();
      emitPhase();
      return handle.observe();
    },
    watch(fn) {
      if (typeof fn !== "function") return () => {};
      watchers.add(fn);
      fn(state.phase);
      return () => watchers.delete(fn);
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
      watchers.clear();
      loop.dispose();
      input.dispose();
      audio.dispose();
      haptics.dispose();
      if (eventTarget && typeof eventTarget.removeEventListener === "function") {
        eventTarget.removeEventListener("pagehide", onPageHide);
        eventTarget.removeEventListener("visibilitychange", onVisibility);
      }
      if (
        typeof document !== "undefined"
        && document !== eventTarget
        && typeof document.removeEventListener === "function"
      ) {
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
    get lastRun() {
      return lastRun ? { ...lastRun } : null;
    },
    flush,
    get settings() {
      return settings;
    },
    updateSettings(patch) {
      const previousSpawn = settings.spawnProfile;
      settings = normalizeSettings({ ...settings, ...patch }, environment, settings);
      state.assist = settings.assist;
      loop.setSpeed(settings.gameSpeed);
      audio.applySettings(settings);
      haptics.applySettings(settings);
      for (const [action, codes] of Object.entries(settings.bindings)) input.rebind(action, codes);
      if (settings.spawnProfile !== previousSpawn) {
        const stay = state.phase === "title" ? "title" : "playing";
        state = createState(state.seed, matchOptions(settings, stay));
        recorded = false;
        resetTrace();
        progress = { ...progress, hold: null };
      }
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
function matchOptions(settings, entry = "playing") {
  return {
    assist: settings.assist,
    spawnProfile: resolveSpawnName(settings.spawnProfile),
    entry,
  };
}

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
