// Orçamento: mede a simulação e o caminho de desenho num canvas stub.
//
// Isola o custo das regras do custo de desenhar. Se a simulação já não cabe no
// orçamento headless, nenhuma otimização de render resolve. O draw no stub
// exercita o caminho de apresentação — não o compositor nem o dispositivo.
// Reporta a distribuição do tempo — não a média — porque é o pior percentil
// que o jogador sente, e a impressão determinística da partida.
//
// Uso: node tools/budget.mjs [--runs 20] [--seed 7]

import { advance, createState, entityPoolStats, eventPoolStats, rngPoolStats, neutralIntent, CONFIG, TICK_HZ } from "../src/game/rules.js";
import { createRenderer } from "../src/game/render.js";
import { fingerprint } from "../src/core/hash.js";
import { createRng } from "../src/core/rng.js";

const argument = (name, fallback) => {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? fallback : Number(process.argv[index + 1]);
};

const runs = argument("runs", 20);
const baseSeed = argument("seed", 7);
const stepBudgetMs = 1000 / TICK_HZ;

function stubCanvas() {
  const context = {
    setTransform() {},
    save() {},
    restore() {},
    beginPath() {},
    closePath() {},
    moveTo() {},
    lineTo() {},
    arc() {},
    ellipse() {},
    quadraticCurveTo() {},
    stroke() {},
    fill() {},
    fillRect() {},
    roundRect() {},
    strokeRect() {},
    clearRect() {},
    rect() {},
    createLinearGradient: () => ({ addColorStop() {} }),
    createRadialGradient: () => ({ addColorStop() {} }),
    measureText: (text) => ({ width: String(text).length * 5 }),
    fillText() {},
    font: "8px system-ui",
    textAlign: "left",
    textBaseline: "top",
    fillStyle: "",
    strokeStyle: "",
    lineWidth: 1,
    globalAlpha: 1,
  };
  return {
    width: 640,
    height: 360,
    style: {},
    getContext: () => context,
  };
}

const samples = [];
const presents = [];
let prints = new Set();
let totalSteps = 0;
const poolStart = entityPoolStats();
const eventStart = eventPoolStats();
const rngStart = rngPoolStats();

const renderer = createRenderer(stubCanvas(), { devicePixelRatio: 1 });
renderer.resize(640, 360);

for (let run = 0; run < runs; run += 1) {
  const state = createState(baseSeed + run);
  // Intenções pseudo-aleatórias mas reprodutíveis: exercita dash, guardar e
  // movimento sem depender de uma pessoa jogando.
  const rng = createRng(baseSeed + run + 1000);
  const intent = neutralIntent();
  while (state.phase === "playing") {
    intent.move = rng.next() < 0.55 ? (rng.next() < 0.5 ? -1 : 1) : 0;
    intent.dash = rng.next() < 0.05;
    intent.bank = state.chain >= 3 && rng.next() < 0.2;
    const started = process.hrtime.bigint();
    advance(state, intent);
    samples.push(Number(process.hrtime.bigint() - started) / 1e6);
    const drawn = process.hrtime.bigint();
    renderer.draw(state, {}, {}, { captions: [], best: 0, hint: "" });
    presents.push(Number(process.hrtime.bigint() - drawn) / 1e6);
    totalSteps += 1;
  }
  prints.add(fingerprint({ score: state.score, tick: state.tick, stats: state.stats }));
}

const percentile = (list) => {
  const ordered = [...list].sort((a, b) => a - b);
  const at = (fraction) => ordered[Math.min(ordered.length - 1, Math.floor(ordered.length * fraction))];
  return {
    p50: at(0.5),
    p95: at(0.95),
    p99: at(0.99),
    worst: ordered[ordered.length - 1],
  };
};

const simulation = percentile(samples);
const presentation = percentile(presents);
const pool = entityPoolStats();
const events = eventPoolStats();
const rng = rngPoolStats();
const report = {
  runs,
  ticks_per_run: CONFIG.runTicks,
  steps: totalSteps,
  scene: {
    name: "playing.run",
    ticks: CONFIG.runTicks,
    draw: "stub",
  },
  step_budget_ms: Number(stepBudgetMs.toFixed(4)),
  simulation_ms: simulation,
  presentation_ms: presentation,
  headroom_p99: Number((1 - simulation.p99 / stepBudgetMs).toFixed(4)),
  distinct_outcomes: prints.size,
  entity_pool: {
    created: pool.created - poolStart.created,
    acquired: pool.acquired - poolStart.acquired,
    released: pool.released - poolStart.released,
    idle: pool.idle,
  },
  event_pool: {
    created: events.created - eventStart.created,
    acquired: events.acquired - eventStart.acquired,
    released: events.released - eventStart.released,
    idle: events.idle,
  },
  rng: {
    created: rng.created,
    reseeds: rng.reseeds - rngStart.reseeds,
  },
  measured: false,
  scope:
    "Cena playing.run: partida inteira + draw() num canvas stub. Não mede " +
    "compositor, áudio, carregamento nem o dispositivo alvo. Orçamento de " +
    "quadro real exige medir no artefato exportado. O poço e o gerador " +
    "relatam reuso, não velocidade. Sem limiar de apresentação.",
};

console.log(JSON.stringify(report, null, 2));
if (simulation.p99 > stepBudgetMs) {
  console.error("Simulação acima do orçamento de passo no percentil 99.");
  process.exit(1);
}
