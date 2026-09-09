#!/usr/bin/env node
// Exercita a janela de perdão declarada. Conta disparos de buffer;
// não atribui peso percebido. `felt` continua falso.

import { advance, createState, neutralIntent, CONFIG } from "../src/game/rules.js";

const runs = 20;
let lateRequests = 0;
let bufferedFires = 0;

for (let run = 0; run < runs; run += 1) {
  const state = createState(7 + run);
  state.player.dashCooldown = 3;
  advance(state, { move: 0, dash: true, bank: false });
  if (state.player.dashBuffer <= 0) continue;
  lateRequests += 1;
  for (let step = 0; step < CONFIG.player.dashBufferTicks + 4; step += 1) {
    advance(state, neutralIntent());
    if (state.events.some((event) => event.type === "dash")) {
      bufferedFires += 1;
      break;
    }
  }
}

const report = {
  runs,
  late_requests: lateRequests,
  buffered_fires: bufferedFires,
  declared_buffer_ticks: CONFIG.player.dashBufferTicks,
  felt: false,
  scope:
    "Simulação da janela declarada, não peso percebido. Sem limiar, sem aprovação.",
};

console.log(JSON.stringify(report, null, 2));
