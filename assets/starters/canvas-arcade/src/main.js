// Montagem do jogo e contrato de ciclo de vida.
//
// Os nomes abaixo — pause, reset, seed, observe, act, advance, capture,
// dispose — são o vocabulário de inspeção do harness. Aqui eles são
// **implementados**, não mencionados: `tests/lifecycle.test.mjs` e
// `tests/determinism.test.mjs` provam cada um. É essa prova, não a presença do
// nome, que move a dimensão `state_trust` da barra de acabamento.

import { createLoop } from "./core/loop.js";
import { createInput } from "./core/input.js";
import { browserStorage, foreignKey } from "./core/storage.js";
import { playReport, LAST_RUN_ROUTE } from "./core/run-report.js";
import { canContinue, canResume, captureHold, loadProgress, persistLine, persistStatus, recordRun, saveProgress, summarizeRun } from "./core/save.js";
import { applyEnvironment, DEFAULT_BINDINGS, detectEnvironment, GAME_SPEED_MAX, GAME_SPEED_MIN, loadSettings, normalizeSettings, saveSettings, SETTINGS_KEY, settingsLine, watchEnvironment } from "./core/settings.js";
import { fingerprint } from "./core/hash.js";
import { audioGapLive, BED_FADE_MS, createAudio } from "./game/audio.js";
import { createHaptics, rumbleRole } from "./game/haptics.js";
import { loadRoleFiles } from "./game/sfx.js";
import { createRenderer } from "./game/render.js";
import { createTrace, finishCurve, traceTick } from "./game/curve.js";
import { applyLive, liveText } from "./core/live.js";
import { bindLines, pauseSurface, titleSurface } from "./core/keys.js";
import { advance as advanceRules, attractMove, attractTick, attractTouch, beginRun, sessionBedRate, createState, restoreState, neutralIntent, threatCue, FIELD, TICK_HZ } from "./game/rules.js";
import { copy, resolveLookName, resolveMoodName, resolveSpawnName } from "./game/tables.js";
import { coachHint, coachText } from "./game/coach.js";

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

// A seed da query é a partida nomeada. Inválida some; explícita
// no construtor vence. Número na URL não é sessão observada.
// O relógio da query é o da partida nomeada. Fora da faixa
// some; 1 some. Número na URL não é sessão observada.
export function readSpeedQuery(options = {}) {
  const raw = options.query
    ?? (typeof location !== "undefined" && typeof location.search === "string" ? location.search : "");
  if (!raw) return null;
  const search = raw.startsWith("?") ? raw.slice(1) : raw;
  const value = new URLSearchParams(search).get("speed");
  if (value === null || value === "") return null;
  const n = Number(value);
  if (!Number.isFinite(n) || n < GAME_SPEED_MIN || n > GAME_SPEED_MAX) return null;
  return n;
}

export function readSeedQuery(options = {}) {
  const raw = options.query
    ?? (typeof location !== "undefined" && typeof location.search === "string" ? location.search : "");
  if (!raw) return undefined;
  const search = raw.startsWith("?") ? raw.slice(1) : raw;
  const value = new URLSearchParams(search).get("seed");
  if (value === null || value === "") return undefined;
  if (!/^\d+$/.test(value)) return undefined;
  const n = Number(value);
  if (!Number.isSafeInteger(n)) return undefined;
  return n >>> 0;
}

export function createGame(options = {}) {
  const canvas = options.canvas ?? null;
  const live = options.live ?? null;
  const storage = options.storage ?? browserStorage("canvas-arcade");
  const environment = options.environment ?? detectEnvironment();
  const eventTarget = options.eventTarget ?? (typeof window !== "undefined" ? window : null);

  let settingsLoad = loadSettings(storage, environment);
  let settings = settingsLoad.settings;
  let keptSettings = { ...settings };
  const sessionAxes = {};
  const queryMood = readMoodQuery(options);
  const querySpawn = readSpawnQuery(options) ?? queryMood;
  const queryLook = readLookQuery(options) ?? queryMood;
  const querySpeed = readSpeedQuery(options);
  if (querySpawn) sessionAxes.spawnProfile = true;
  if (queryLook) sessionAxes.look = true;
  if (querySpeed !== null) sessionAxes.gameSpeed = true;
  if (querySpawn || queryLook || querySpeed !== null) {
    settings = normalizeSettings(
      {
        ...settings,
        ...(querySpawn ? { spawnProfile: querySpawn } : {}),
        ...(queryLook ? { look: queryLook } : {}),
        ...(querySpeed !== null ? { gameSpeed: querySpeed } : {}),
      },
      environment,
      settings,
    );
  }
  const progressLoad = loadProgress(storage);
  let progress = progressLoad.progress;
  const querySeed = readSeedQuery(options);
  const forcedSeed = options.seed !== undefined ? options.seed : querySeed;
  // A chuva da query é a mesa nomeada. Sem isto o hold
  // de outra mesa vestia dusk e chovia spawn. Query no
  // disco não é sessão observada.
  const resuming = forcedSeed === undefined && !querySpawn && options.entry !== "title" && canResume(progress);
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
  let lastWrite = { ok: true };
  let disposed = false;
  let lastPhase = state.phase;
  let doorArmed = true;
  let trace = createTrace();
  const watchers = new Set();
  const settingWatchers = new Set();
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
  function clockSpeed() {
    // O knob é da partida. A mostra e o fim ficam no relógio
    // cheio — senão o slider some a porta que o rótulo poupa.
    // Knob no disco não é sessão observada.
    return state.phase === "playing" ? settings.gameSpeed : 1;
  }
  function syncClock() {
    loop.setSpeed(clockSpeed());
    audio.update({ bedRate: sessionBedRate(state, clockSpeed()) });
  }
  let pausedNow = () => false;
  function syncDashOnPress() {
    // A porta pede mover. Sem isto o toque de cima abria o
    // ciclo no down e o arraste mentia. Na pausa o down
    // também mentia: o tap precisa retomar, não avançar.
    // Toque no disco não é sessão observada.
    if (typeof input.setDashOnPress === "function") {
      input.setDashOnPress(state.phase !== "title" && !pausedNow());
    }
    if (typeof input.setTitleNewOnBank === "function") {
      // Depois da partida o tap no campo repete. A faixa
      // de baixo pede seed nova. Na primeira visita a
      // faixa continua abrindo. Toque no disco não é felt.
      input.setTitleNewOnBank(state.phase === "title" && doorOpen());
    }
  }
  function emitPhase() {
    if (state.phase === lastPhase) return;
    lastPhase = state.phase;
    syncClock();
    syncDashOnPress();
    for (const fn of watchers) fn(state.phase);
  }
  function doorOpen() {
    return canContinue(progress) && (forcedSeed === undefined || forcedSeed === progress.lastSeed);
  }

  function rememberWrite(result) {
    lastWrite = result && typeof result === "object" ? result : { ok: false, reason: "write_failed" };
    return lastWrite;
  }

  function persist() {
    return persistStatus(storage, lastWrite);
  }

  const audio = options.audio ?? createAudio({ settings });
  const input = options.input ?? createInput({
    target: eventTarget,
    surface: canvas,
    bindings: settings.bindings,
    unlock: () => audio.unlock(),
    visibility: options.visibility,
    gamepads: options.gamepads,
  });
  syncDashOnPress();
  const haptics = options.haptics ?? createHaptics({ settings, gamepads: options.gamepads });
  const renderer = canvas ? createRenderer(canvas) : null;
  let finishSfx;
  const whenSfx = new Promise((resolve) => {
    finishSfx = () => resolve(audio.missing());
  });
  // Sem canvas (teste headless) não busca arquivo: o fetch relativo não tem
  // servidor e atrasaria o teste. No browser, o arquivo em public/sfx precisa
  // chegar ao mixer — senão `roles` verde e o jogo mudo são a mesma coisa.
  // O painel pinta no boot; sem este aviso ele some os vazios que o
  // fetch ainda não marcou e nunca relê.
  if ((options.loadSfx ?? Boolean(canvas)) && typeof (options.fetch ?? globalThis.fetch) === "function") {
    const fetchFn = options.fetch ?? globalThis.fetch.bind(globalThis);
    const decode = options.decodeSfx ?? ((bytes) => audio.decode(bytes));
    loadRoleFiles(audio, { fetch: fetchFn, decode })
      .then(() => syncBed())
      .catch(() => {})
      .finally(() => finishSfx());
  } else {
    finishSfx();
  }

  const loop = createLoop({
    stepMs: 1000 / TICK_HZ,
    speed: clockSpeed(),
    now: options.now,
    schedule: options.schedule,
    cancel: options.cancel,
    update: () => step(readIntent()),
    render: (frame) => present(frame),
  });
  pausedNow = () => loop.paused;

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
    else if (loop.paused && input.lastSource === "pointer") {
      // A aba escondida no telefone senta. Sem isto o tap
      // falava no vazio — Esc e P não existem no toque.
      // Espaço na pausa continua só intenção. Toque no
      // disco não é sessão observada.
      const tap = input.intent();
      if (!tap.dash) return;
      if (state.phase === "over") handle.reset();
      else togglePause();
    }
  }

  function pulse(events) {
    for (const event of events) audio.play(event.type, event);
    haptics.play(rumbleRole(events.map((event) => event.type)));
  }

  function step(intent) {
    if (state.phase === "title") {
      if (intent?.dash) {
        beginRun(state);
        resetTrace();
        syncBed();
      } else {
        attractMove(state, intent);
        attractTick(state);
        attractTouch(state, settings.reducedMotion);
      }
      pulse(state.events);
      emitPhase();
      return;
    }
    if (state.phase === "over") {
      // O mesmo verbo da porta. Um dash que ainda estava apertado
      // no último tick não pula o overlay nem o recibo.
      if (!intent?.dash) doorArmed = true;
      else if (doorArmed) {
        handle.reset();
        return;
      }
      advanceRules(state, intent);
      emitPhase();
      return;
    }
    advanceRules(state, intent);
    traceTick(trace, state);
    pulse(state.events);
    if (state.phase === "over" && !recorded) {
      recorded = true;
      doorArmed = false;
      // A faixa lia seed e some a curva. O last-run já
      // a traçou. Número no disco não é outsider.
      const curve = finishCurve(trace, state.chain);
      lastRun = { ...summarizeRun(state, { look: settings.look, speed: settings.gameSpeed }), curve };
      progress = recordRun(progress, state, { lastRun });
      rememberWrite(saveProgress(storage, progress, progressLoad));
      audio.stop("bed", { fadeMs: BED_FADE_MS });
      offerLastRun(playReport({
        seed: state.seed,
        spawn: state.spawnProfile,
        look: settings.look,
        speed: settings.gameSpeed,
        run: lastRun,
        curve,
        policy: "played",
      }));
    }
    emitPhase();
  }

  function syncBed() {
    if (disposed) return;
    if (loop.paused) {
      // No campo o hit não atravessa Pausado. No fim a cortina
      // já venceu; hush comeria o stinger. Na porta a placa
      // nem nasce. Arquivo no disco não é mix ouvido.
      if (state.phase === "playing") audio.hush();
      audio.stop("bed");
      return;
    }
    audio.lift();
    if (state.phase === "over" || state.phase === "title") audio.stop("bed");
    else audio.play("bed");
  }

  function present(frame) {
    readCommands();
    audio.update({ bedRate: sessionBedRate(state, clockSpeed()) });
    const captions = audio.captions();
    const spoken = input.lastSource;
    // Na porta o tap abre em qualquer faixa. lastSource
    // pointer preenchia cima e mente. A placa da
    // abertura e do fim usa a superfície da porta;
    // o aviso continua o aparelho que falou.
    // Na pausa o telefone ainda não falou: Esc e P
    // não existem no polegar. O tap já retoma. A
    // placa usa a superfície do toque; o aviso
    // continua o aparelho que falou.
    // Na porta o canvas já nomeia jogar e seed nova.
    // Sem isto o live herdava o teclado e mente.
    // Texto no disco não é felt.
    const overlayPaused = loop.paused && state.phase !== "over" && state.phase !== "title";
    const surface = state.phase === "title" || state.phase === "over"
      ? titleSurface(environment, spoken)
      : overlayPaused
        ? pauseSurface(environment, spoken)
        : spoken;
    const bound = bindLines(
      copy,
      settings.bindings ?? DEFAULT_BINDINGS,
      overlayPaused
        ? pauseSurface(environment, spoken)
        : state.phase === "title" || state.phase === "over"
          ? titleSurface(environment, spoken)
          : spoken,
    );
    const hint = coachHint(state, copy, { surface: spoken });
    const open = doorOpen();
    applyLive({
      node: live,
      text: liveText({
        captions,
        phase: state.phase,
        threat: threatCue(state, settings.reducedMotion),
        paused: loop.paused,
        score: state.score,
        best: progress.best,
        chain: state.chain,
        lastScore: lastRun && Number.isFinite(lastRun.score) ? lastRun.score : undefined,
        persist: persistLine(persist(), copy),
        settings: settingsLine(settingsLoad, copy),
        audio: audioGapLive(audio.missing()),
        attractTouch: state.attractTouch,
        coach: coachText(state, bound, { surface: spoken, fantasy: copy.fantasy }),
        resume: bound.resume,
        restart: bound.restart,
        titlePlay: state.phase === "title" && !open ? bound.title_play : undefined,
        titleAgain: state.phase === "title" && open ? bound.title_again : undefined,
        titleNew: state.phase === "title" && open ? bound.title_new : undefined,
        overDoor: state.phase === "over" ? bound.over_door : undefined,
      }),
    });
    if (!renderer) return;
    renderer.draw(state, frame, settings, {
      captions,
      best: progress.best,
      hint,
      surface,
      fantasy: copy.fantasy,
      canContinue: doorOpen(),
      lastRun,
      persist: persist(),
      settingsLoad,
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
    syncBed();
    syncDashOnPress();
  }

  function persistableSettings() {
    // O convite veste a sessão. Sem isto pagehide gravava
    // dusk como se a pessoa tivesse escolhido. Query no
    // disco não é preferência; trusted continua falso.
    if (!sessionAxes.look && !sessionAxes.spawnProfile && !sessionAxes.gameSpeed) {
      return settings;
    }
    return {
      ...settings,
      ...(sessionAxes.look ? { look: keptSettings.look } : {}),
      ...(sessionAxes.spawnProfile ? { spawnProfile: keptSettings.spawnProfile } : {}),
      ...(sessionAxes.gameSpeed ? { gameSpeed: keptSettings.gameSpeed } : {}),
    };
  }

  function claimSessionAxes(patch) {
    if (!patch || typeof patch !== "object") return;
    if ("look" in patch) delete sessionAxes.look;
    if ("spawnProfile" in patch) delete sessionAxes.spawnProfile;
    if ("gameSpeed" in patch) delete sessionAxes.gameSpeed;
  }

  function writeSettings() {
    const written = persistableSettings();
    const result = saveSettings(storage, written);
    keptSettings = { ...written };
    return result;
  }

  function flush() {
    if (state.phase === "playing") {
      progress = { ...progress, hold: captureHold(state) };
    }
    rememberWrite(saveProgress(storage, progress, progressLoad));
    const settingsWrite = writeSettings();
    if (settingsWrite && settingsWrite.ok === false) rememberWrite(settingsWrite);
    return { progress: { ...progress }, settings, persist: persist() };
  }

  function sitAway() {
    flush();
    // P na porta é ignorado. Hidden ou blur que pausa sem P
    // para retomar congela a mostra e come o avanço. No campo
    // e no fim o relógio senta. Stub não é aba fechada;
    // trusted continua falso.
    if (state.phase !== "title") {
      loop.pause();
      haptics.mute();
      syncBed();
      syncDashOnPress();
    }
  }

  const onVisibility = () => {
    const hidden = typeof document === "undefined" || document.hidden;
    if (hidden) sitAway();
  };
  const onBlur = () => {
    // A receita promete perda de foco. Sem isto barra e
    // DevTools soltavam o input e o tick seguia só na RAM.
    sitAway();
  };
  const onGamepadGone = () => {
    // O poll some o hold. Sem isto o relógio seguia e o
    // corpo morria sozinho. Só a sessão que o controle
    // falou: um pad na gaveta não senta o teclado.
    // Stub não é sessão no controle; felt continua falso.
    if (input.lastSource !== "gamepad") return;
    sitAway();
  };
  const onPageHide = () => {
    flush();
  };
  // pagehide cobre aba escondida e mobile. Fechar ou recarregar
  // no desktop às vezes só fala beforeunload. Os dois descarregam
  // o mesmo hold. Stub não é aba fechada; trusted continua falso.
  const onBeforeUnload = () => {
    flush();
  };
  function wearSettings(next, persist) {
    const previousSpawn = settings.spawnProfile;
    settings = next;
    state.assist = settings.assist;
    syncClock();
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
    if (persist) rememberWrite(writeSettings());
  }
  function onStorage(event) {
    // A outra aba já gravou. Sem isto look e mix
    // ficavam velhos até recarregar. Ouvir não é
    // aba fechada; trusted continua falso.
    if (!foreignKey(event, storage.prefix, SETTINGS_KEY)) return;
    settingsLoad = loadSettings(storage, environment);
    keptSettings = { ...settingsLoad.settings };
    delete sessionAxes.look;
    delete sessionAxes.spawnProfile;
    delete sessionAxes.gameSpeed;
    wearSettings(settingsLoad.settings, false);
    for (const fn of settingWatchers) fn(settings);
  }
  if (eventTarget && typeof eventTarget.addEventListener === "function") {
    eventTarget.addEventListener("pagehide", onPageHide);
    eventTarget.addEventListener("beforeunload", onBeforeUnload);
    eventTarget.addEventListener("visibilitychange", onVisibility);
    eventTarget.addEventListener("blur", onBlur);
    eventTarget.addEventListener("gamepaddisconnected", onGamepadGone);
    eventTarget.addEventListener("storage", onStorage);
  }
  // O boot já herdou o sistema. Sem o ouvinte o pedido no
  // meio da sessão ficava no matchMedia. Desligar o sistema
  // não apaga a caixa. Pedido no disco não é sessão.
  const unwatchEnvironment = watchEnvironment((env) => {
    if (disposed) return;
    const patch = applyEnvironment(settings, env);
    if (!Object.keys(patch).length) return;
    wearSettings(normalizeSettings({ ...settings, ...patch }, environment, settings), true);
    for (const fn of settingWatchers) fn(settings);
  }, options.matchMedia);
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
      syncDashOnPress();
      flush();
      return true;
    },
    resume() {
      loop.resume();
      haptics.unmute();
      syncBed();
      syncDashOnPress();
      return true;
    },
    get paused() {
      return loop.paused;
    },
    reset(seed = state.seed) {
      // Com tela, o fim não pula a porta. R no overlay — e um
      // avanço novo — abrem a abertura. Sem tela o headless
      // continua no tick zero. Reset no meio da partida não muda
      // de fase. Seed explícita (teste, `seed()`) entra jogando —
      // não é o botão do overlay.
      const toTitle = Boolean(canvas) && state.phase === "over" && arguments.length === 0;
      const nextSeed = toTitle ? (progress.lastSeed ?? seed) : seed;
      progress = { ...progress, hold: null };
      rememberWrite(saveProgress(storage, progress, progressLoad));
      state = createState(nextSeed, matchOptions(settings, toTitle ? "title" : "playing"));
      queued = neutralIntent();
      recorded = false;
      resetTrace();
      loop.resume();
      haptics.unmute();
      syncBed();
      syncDashOnPress();
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
      settingWatchers.clear();
      loop.dispose();
      input.dispose();
      audio.dispose();
      haptics.dispose();
      unwatchEnvironment();
      if (eventTarget && typeof eventTarget.removeEventListener === "function") {
        eventTarget.removeEventListener("pagehide", onPageHide);
        eventTarget.removeEventListener("beforeunload", onBeforeUnload);
        eventTarget.removeEventListener("visibilitychange", onVisibility);
        eventTarget.removeEventListener("blur", onBlur);
        eventTarget.removeEventListener("gamepaddisconnected", onGamepadGone);
        eventTarget.removeEventListener("storage", onStorage);
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
    whenSfx,
    get progress() {
      return { ...progress, status: progressLoad.status, notes: progressLoad.notes };
    },
    get lastRun() {
      return lastRun ? { ...lastRun } : null;
    },
    get persist() {
      return persist();
    },
    flush,
    get settings() {
      return settings;
    },
    get settingsLoad() {
      return { status: settingsLoad.status, notes: [...(settingsLoad.notes ?? [])] };
    },
    watchSettings(fn) {
      if (typeof fn !== "function") return () => {};
      settingWatchers.add(fn);
      return () => settingWatchers.delete(fn);
    },
    updateSettings(patch) {
      claimSessionAxes(patch);
      wearSettings(normalizeSettings({ ...settings, ...patch }, environment, settings), true);
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
    const game = createGame({ canvas, live: document.getElementById("live") });
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
