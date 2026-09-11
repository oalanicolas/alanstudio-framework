// Laço de passo fixo, com pausa, descarte e medição do tempo de quadro.
//
// Passo fixo separa a simulação da taxa de apresentação: a partida se comporta
// igual em 30, 60 ou 144 Hz, o que é pré-requisito para determinismo e para
// comparar duas execuções. O relógio e o agendador são injetáveis para que o
// teste headless não precise de `requestAnimationFrame`.
//
// A janela de métricas guarda o tempo entre quadros. Média de FPS esconde
// exatamente o que o jogador sente; o que importa é o pior percentil.

const defaultNow = () =>
  typeof performance !== "undefined" && performance.now ? performance.now() : Date.now();

function finiteSpeed(value, fallback = 1) {
  return Number.isFinite(value) && value > 0 ? value : fallback;
}

export function createLoop(options = {}) {
  const stepMs = options.stepMs ?? 1000 / 60;
  // Velocidade de parede: 1 é o relógio cheio. Abaixo de 1 o acumulador
  // anda menos por milissegundo real. O passo da simulação continua
  // `stepMs` — `advance()` headless não passa por aqui.
  let speed = finiteSpeed(options.speed);
  const maxCatchUp = options.maxCatchUp ?? 5;
  const sampleSize = options.sampleSize ?? 240;
  const now = options.now ?? defaultNow;
  const schedule =
    options.schedule ??
    (typeof requestAnimationFrame === "function"
      ? (callback) => requestAnimationFrame(callback)
      : (callback) => setTimeout(() => callback(now()), stepMs));
  const cancel =
    options.cancel ??
    (typeof cancelAnimationFrame === "function"
      ? (handle) => cancelAnimationFrame(handle)
      : (handle) => clearTimeout(handle));

  let update = options.update ?? (() => {});
  let render = options.render ?? (() => {});
  let handle = null;
  let last = null;
  let accumulator = 0;
  let paused = false;
  let disposed = false;
  const samples = [];
  const counters = { frames: 0, steps: 0, dropped: 0 };

  function record(elapsed) {
    samples.push(elapsed);
    if (samples.length > sampleSize) samples.shift();
  }

  function frame(timestamp) {
    handle = null;
    if (disposed) return;
    const time = typeof timestamp === "number" ? timestamp : now();
    if (last !== null) record(time - last);
    // Retomar sem zerar `last` produziria uma rajada de passos de recuperação
    // equivalente ao tempo em pausa.
    if (last !== null && !paused) accumulator += (time - last) * speed;
    last = time;
    counters.frames += 1;

    let steps = 0;
    while (accumulator >= stepMs && steps < maxCatchUp) {
      accumulator -= stepMs;
      steps += 1;
      counters.steps += 1;
      update(stepMs);
    }
    if (accumulator >= stepMs) {
      // Descarta o atraso restante em vez de perseguir o relógio para sempre.
      counters.dropped += Math.floor(accumulator / stepMs);
      accumulator = 0;
    }
    render({ paused, alpha: accumulator / stepMs, steps });
    if (!disposed) handle = schedule(frame);
  }

  return {
    start() {
      if (disposed || handle !== null) return;
      last = null;
      accumulator = 0;
      handle = schedule(frame);
    },
    stop() {
      if (handle !== null) cancel(handle);
      handle = null;
      last = null;
      accumulator = 0;
    },
    pause() {
      paused = true;
    },
    resume() {
      if (!paused) return;
      paused = false;
      last = null;
      accumulator = 0;
    },
    get paused() {
      return paused;
    },
    get running() {
      return handle !== null;
    },
    get disposed() {
      return disposed;
    },
    setSpeed(next) {
      speed = finiteSpeed(next, speed);
      return speed;
    },
    get speed() {
      return speed;
    },
    // Passo manual, para teste headless e para reproduzir um replay.
    feed(elapsedMs) {
      if (disposed || paused) return 0;
      accumulator += elapsedMs * speed;
      let steps = 0;
      while (accumulator >= stepMs && steps < maxCatchUp) {
        accumulator -= stepMs;
        steps += 1;
        counters.steps += 1;
        update(stepMs);
      }
      return steps;
    },
    metrics() {
      const ordered = [...samples].sort((a, b) => a - b);
      const at = (fraction) =>
        ordered.length ? ordered[Math.min(ordered.length - 1, Math.floor(ordered.length * fraction))] : 0;
      return {
        ...counters,
        samples: ordered.length,
        p50: at(0.5),
        p95: at(0.95),
        p99: at(0.99),
        worst: ordered.length ? ordered[ordered.length - 1] : 0,
      };
    },
    dispose() {
      disposed = true;
      if (handle !== null) cancel(handle);
      handle = null;
      update = () => {};
      render = () => {};
      samples.length = 0;
    },
  };
}
