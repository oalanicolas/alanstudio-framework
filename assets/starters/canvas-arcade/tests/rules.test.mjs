// As regras são a parte do jogo que um teste pode fechar. Feel, arte e diversão
// exigem observação; invariantes não.

import { test } from "node:test";
import assert from "node:assert/strict";

import { advance, createState, neutralIntent, CONFIG, PLAYER_Y } from "../src/game/rules.js";

const orb = (x, y) => ({ id: 1, kind: "orb", x, y, vy: 0 });
const shard = (x, y) => ({ id: 2, kind: "shard", x, y, vy: 0 });

function settle(state) {
  while (state.hitstop > 0) advance(state, neutralIntent());
  return state;
}

test("guardar converte a corrente ao quadrado e cobra o compromisso", () => {
  const state = createState(1);
  state.chain = 4;
  advance(state, { move: 0, dash: false, bank: true });
  assert.equal(state.score, 16);
  assert.equal(state.chain, 0);
  assert.equal(state.stats.banks, 1);
  assert.ok(state.bankLock > 0, "guardar trava o dash por um instante");
  assert.deepEqual(
    state.events.find((event) => event.type === "bank"),
    { type: "bank", chain: 4, gain: 16 },
  );
});

test("guardar sem corrente não faz nada e não trava o dash", () => {
  const state = createState(1);
  advance(state, { move: 0, dash: false, bank: true });
  assert.equal(state.score, 0);
  assert.equal(state.bankLock, 0);
  assert.equal(state.stats.banks, 0);
});

test("ser atingido zera a corrente inteira e concede graça", () => {
  const state = createState(2);
  state.chain = 5;
  state.entities = [shard(state.player.x, PLAYER_Y - 1)];
  advance(state, neutralIntent());
  assert.equal(state.chain, 0);
  assert.equal(state.stats.hits, 1);
  assert.equal(state.player.invuln, CONFIG.player.invulnTicks);
  assert.deepEqual(
    state.events.find((event) => event.type === "hit"),
    { type: "hit", lost: 5 },
  );
});

test("a graça impede perder duas correntes seguidas", () => {
  const state = createState(2);
  state.chain = 5;
  state.entities = [shard(state.player.x, PLAYER_Y - 1)];
  advance(state, neutralIntent());
  settle(state);
  state.chain = 3;
  state.entities = [shard(state.player.x, PLAYER_Y - 1)];
  advance(state, neutralIntent());
  assert.equal(state.chain, 3, "a corrente sobrevive dentro da janela de graça");
  assert.equal(state.stats.hits, 1);
  assert.ok(state.events.some((event) => event.type === "graze"));
});

test("o dash atravessa o estilhaço sem perder a corrente", () => {
  const state = createState(3);
  advance(state, { move: 1, dash: true, bank: false });
  assert.ok(state.player.dashTicks > 0);
  state.chain = 2;
  state.entities = [shard(state.player.x, PLAYER_Y)];
  advance(state, { move: 1, dash: false, bank: false });
  assert.equal(state.chain, 2);
  assert.ok(state.events.some((event) => event.type === "graze"));
});

test("o pedido de dash é guardado e dispara quando recarrega", () => {
  const state = createState(4);
  state.player.dashCooldown = 3;
  advance(state, { move: 0, dash: true, bank: false });
  assert.equal(state.player.dashTicks, 0, "não dispara durante a recarga");
  assert.ok(state.player.dashBuffer > 0, "o pedido fica guardado");
  let fired = false;
  for (let index = 0; index < 4 && !fired; index += 1) {
    advance(state, neutralIntent());
    fired = state.events.some((event) => event.type === "dash");
  }
  assert.ok(fired, "o pedido guardado dispara sozinho ao recarregar");
});

test("o alcance de coleta é maior que o desenho, e tem limite", () => {
  const inside = createState(5);
  inside.entities = [orb(inside.player.x + CONFIG.player.halfWidth + CONFIG.collect.pad - 0.5, PLAYER_Y)];
  advance(inside, neutralIntent());
  assert.equal(inside.chain, 1, "quem quase pegou, pega");

  const outside = createState(5);
  outside.entities = [orb(outside.player.x + CONFIG.player.halfWidth + CONFIG.collect.pad + 1, PLAYER_Y)];
  advance(outside, neutralIntent());
  assert.equal(outside.chain, 0, "o perdão é delimitado, não infinito");
  assert.equal(outside.entities.length, 1);
});

test("a assistência alarga o alcance sem esconder o orbe nem o limite", () => {
  const helped = createState(5, { assist: true });
  helped.entities = [orb(helped.player.x + CONFIG.player.halfWidth + CONFIG.collect.pad + 1, PLAYER_Y)];
  advance(helped, neutralIntent());
  assert.equal(helped.chain, 1, "o mesmo orbe fora do alcance padrão entra com assistência");

  const stillOut = createState(5, { assist: true });
  stillOut.entities = [orb(
    stillOut.player.x + CONFIG.player.halfWidth + CONFIG.collect.pad + CONFIG.assist.collectPad + 1,
    PLAYER_Y,
  )];
  advance(stillOut, neutralIntent());
  assert.equal(stillOut.chain, 0, "assistência não é alcance infinito");
  assert.equal(stillOut.entities.length, 1);
});

test("orbe perdido é contado, não silencioso", () => {
  const state = createState(6);
  state.entities = [orb(20, 190)];
  advance(state, neutralIntent());
  assert.equal(state.stats.missed, 1);
  assert.equal(state.entities.length, 0);
  assert.ok(state.events.some((event) => event.type === "missed"));
});

test("a partida termina no limite de tempo e informa a corrente perdida", () => {
  const state = createState(7);
  let steps = 0;
  while (state.phase === "playing" && steps < CONFIG.runTicks + 10) {
    advance(state, neutralIntent());
    steps += 1;
  }
  assert.equal(state.phase, "over");
  assert.equal(state.tick, CONFIG.runTicks);
  const over = state.events.find((event) => event.type === "over");
  assert.ok(over, "o fim da partida é um evento observável");
  assert.equal(typeof over.unbanked, "number");
});

test("partida encerrada não avança mais", () => {
  const state = createState(8);
  state.phase = "over";
  state.tick = CONFIG.runTicks;
  advance(state, { move: 1, dash: true, bank: true });
  assert.equal(state.tick, CONFIG.runTicks);
  assert.equal(state.score, 0);
  assert.deepEqual(state.events, []);
});

test("o hitstop congela o mundo sem congelar a leitura da entrada", () => {
  const state = createState(9);
  state.entities = [orb(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  assert.equal(state.hitstop, CONFIG.feel.collectHitstopTicks);
  const before = state.player.x;
  advance(state, { move: 1, dash: true, bank: false });
  assert.equal(state.player.x, before, "o mundo não se move durante o congelamento");
  assert.ok(state.player.dashBuffer > 0, "o pedido feito no congelamento não é engolido");
});
