// Orçamento: mede a simulação sem apresentação.
//
// Isola o custo das regras do custo de desenhar. Se a simulação já não cabe no
// orçamento headless, nenhuma otimização de render resolve. Reporta a
// distribuição do tempo de passo — não a média — porque é o pior percentil que
// o jogador sente, e a impressão determinística da partida, para que uma
// alteração de desempenho que mude o comportamento seja detectada aqui.
//
// Uso: node tools/budget.mjs [--runs 20] [--seed 7]

import { advance, createState, neutralIntent, CONFIG, TICK_HZ } from "../src/game/rules.js";
import { fingerprint } from "../src/core/hash.js";
import { createRng } from "../src/core/rng.js";

const argument = (name, fallback) => {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? fallback : Number(process.argv[index + 1]);
};

const runs = argument("runs", 20);
const baseSeed = argument("seed", 7);
const stepBudgetMs = 1000 / TICK_HZ;

const samples = [];
let prints = new Set();
let totalSteps = 0;

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
    totalSteps += 1;
  }
  prints.add(fingerprint({ score: state.score, tick: state.tick, stats: state.stats }));
}

samples.sort((a, b) => a - b);
const at = (fraction) => samples[Math.min(samples.length - 1, Math.floor(samples.length * fraction))];
const report = {
  runs,
  ticks_per_run: CONFIG.runTicks,
  steps: totalSteps,
  step_budget_ms: Number(stepBudgetMs.toFixed(4)),
  simulation_ms: { p50: at(0.5), p95: at(0.95), p99: at(0.99), worst: samples[samples.length - 1] },
  headroom_p99: Number((1 - at(0.99) / stepBudgetMs).toFixed(4)),
  distinct_outcomes: prints.size,
  scope:
    "Somente simulação: não mede render, áudio, carregamento nem o dispositivo alvo. " +
    "Orçamento de quadro real exige medir no artefato exportado.",
};

console.log(JSON.stringify(report, null, 2));
if (at(0.99) > stepBudgetMs) {
  console.error("Simulação acima do orçamento de passo no percentil 99.");
  process.exit(1);
}
