#!/usr/bin/env node
// Exercita as janelas de perdão declaradas. Conta disparos de buffer;
// não atribui peso percebido. `felt` continua falso.

import { advance, createState, neutralIntent, CONFIG, PLAYER_Y } from "../src/game/rules.js";

const runs = 20;
let lateRequests = 0;
let bufferedFires = 0;
let lateBanks = 0;
let bufferedBanks = 0;

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

for (let run = 0; run < runs; run += 1) {
  const state = createState(21 + run);
  state.entities = [{ id: 1, kind: "orb", x: state.player.x, y: PLAYER_Y, vy: 0 }];
  advance(state, neutralIntent());
  if (state.hitstop <= 0 || state.chain === 0) continue;
  advance(state, { move: 0, dash: false, bank: true });
  if (state.bankBuffer <= 0) continue;
  lateBanks += 1;
  for (let step = 0; step < CONFIG.bank.bufferTicks + CONFIG.bank.windupTicks + 4; step += 1) {
    advance(state, neutralIntent());
    if (state.events.some((event) => event.type === "bank")) {
      bufferedBanks += 1;
      break;
    }
  }
}

const report = {
  runs,
  late_requests: lateRequests,
  buffered_fires: bufferedFires,
  late_banks: lateBanks,
  buffered_banks: bufferedBanks,
  declared_buffer_ticks: CONFIG.player.dashBufferTicks,
  declared_bank_buffer_ticks: CONFIG.bank.bufferTicks,
  felt: false,
  scope:
    "Simulação das janelas declaradas (dash e guardar), não peso percebido. Sem limiar, sem aprovação.",
};

console.log(JSON.stringify(report, null, 2));
