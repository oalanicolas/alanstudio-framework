// As regras são a parte do jogo que um teste pode fechar. Feel, arte e diversão
// exigem observação; invariantes não.

import { test } from "node:test";
import assert from "node:assert/strict";

import { advance, approaching, createState, entityPoolStats, neutralIntent, CONFIG, PLAYER_Y } from "../src/game/rules.js";

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

test("cada verbo tem sinal próprio de partida e contato", () => {
  const fade = CONFIG.feel.squashDecay;
  const tremor = CONFIG.feel.shakeDecay;
  const dash = createState(3);
  advance(dash, { move: 1, dash: true, bank: false });
  assert.equal(dash.player.squash, CONFIG.feel.squashDash * fade);
  assert.equal(dash.hitstop, 0);

  const collected = createState(5);
  collected.entities = [orb(collected.player.x, PLAYER_Y)];
  advance(collected, neutralIntent());
  assert.equal(collected.hitstop, CONFIG.feel.collectHitstopTicks);
  assert.equal(collected.player.squash, CONFIG.feel.squashCollect * fade);
  assert.equal(collected.shake, CONFIG.feel.collectShake * tremor);

  const banked = createState(1);
  banked.chain = 3;
  advance(banked, { move: 0, dash: false, bank: true });
  assert.equal(banked.hitstop, CONFIG.feel.bankHitstopTicks);
  assert.equal(banked.shake, CONFIG.feel.bankShake * tremor);

  const struck = createState(2);
  struck.entities = [shard(struck.player.x, PLAYER_Y - 1)];
  advance(struck, neutralIntent());
  assert.equal(struck.hitstop, CONFIG.feel.hitHitstopTicks);
  assert.equal(struck.shake, CONFIG.feel.hitShake * tremor);

  const stops = [
    CONFIG.feel.collectHitstopTicks,
    CONFIG.feel.bankHitstopTicks,
    CONFIG.feel.hitHitstopTicks,
  ];
  assert.equal(new Set(stops).size, 3, "hitstop repetido não distingue o verbo");
  assert.notEqual(CONFIG.feel.squashDash, CONFIG.feel.squashCollect);
  assert.notEqual(CONFIG.feel.collectShake, CONFIG.feel.hitShake);
  assert.notEqual(CONFIG.feel.bankShake, CONFIG.feel.collectShake);
  assert.notEqual(dash.camera.x, 0, "dash empurra a câmera na direção");
  assert.equal(collected.camera.y < 0, true, "coleta sobe a câmera");
  assert.equal(banked.camera.y > 0, true, "guardar confirma para baixo");
  assert.ok(Math.abs(struck.camera.y) > Math.abs(collected.camera.y), "o erro desloca mais que a coleta");
  assert.equal(collected.flash, 0, "coleta não acende o campo como se fosse o erro");
  assert.equal(struck.flash, CONFIG.feel.flashHit * CONFIG.feel.flashDecay);
});

test("a ameaça marca o trilho antes do contato e some na faixa", () => {
  const state = createState(1);
  state.entities = [
    { id: 1, kind: "orb", x: 80, y: PLAYER_Y - 24, vy: 1 },
    { id: 2, kind: "shard", x: 120, y: -8, vy: 1 },
    { id: 3, kind: "orb", x: 160, y: PLAYER_Y, vy: 0 },
  ];
  const near = approaching(state);
  assert.equal(near.length, 1);
  assert.equal(near[0].id, 1);
  state.entities[0].y = PLAYER_Y;
  assert.equal(approaching(state).length, 0, "na faixa de coleta o aviso já é o próprio orbe");
});

test("o pedido de guardar sobrevive ao hitstop da coleta", () => {
  const state = createState(5);
  state.entities = [orb(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  assert.equal(state.chain, 1);
  assert.ok(state.hitstop > 0);
  advance(state, { move: 0, dash: false, bank: true });
  assert.ok(state.bankBuffer > 0, "o pedido feito no congelamento fica guardado");
  assert.equal(state.stats.banks, 0, "não guarda durante o hitstop");
  settle(state);
  let fired = false;
  for (let index = 0; index < CONFIG.bank.bufferTicks + 2 && !fired; index += 1) {
    advance(state, neutralIntent());
    fired = state.events.some((event) => event.type === "bank");
  }
  assert.ok(fired, "o pedido guardado dispara quando o mundo volta a andar");
  assert.equal(state.stats.banks, 1);
  assert.equal(state.chain, 0);
});

test("guardar no mesmo quadro da coleta decide a corrente nova", () => {
  const state = createState(5);
  state.entities = [orb(state.player.x, PLAYER_Y)];
  advance(state, { move: 0, dash: false, bank: true });
  assert.equal(state.stats.banks, 1);
  assert.equal(state.score, 1);
  assert.equal(state.chain, 0);
});

test("toque de guardar sem corrente não decide o próximo orbe", () => {
  const state = createState(5);
  advance(state, { move: 0, dash: false, bank: true });
  assert.equal(state.bankBuffer, 0);
  state.entities = [orb(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  assert.equal(state.chain, 1);
  assert.equal(state.stats.banks, 0);
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

test("os primeiros ticks são prática: só orbes, sem estilhaço", () => {
  const state = createState(11);
  const kinds = new Set();
  while (state.tick < CONFIG.spawn.practiceTicks) {
    advance(state, neutralIntent());
    for (const entity of state.entities) kinds.add(entity.kind);
  }
  assert.ok(kinds.has("orb"), "a prática precisa nascer orbe");
  assert.equal(kinds.has("shard"), false, "estilhaço na prática mistura o risco cedo demais");
});

test("guardar abre uma janela de recuperação na chuva", () => {
  const state = createState(1);
  state.chain = 2;
  state.spawnTimer = 1;
  advance(state, { move: 0, dash: false, bank: true });
  assert.ok(state.recoverUntil > state.tick);
  assert.ok(
    state.spawnTimer > CONFIG.spawn.intervalTicks,
    "a recuperação alonga o intervalo, não o encurta",
  );
});

test("orbe perdido é contado, não silencioso", () => {
  const state = createState(6);
  state.entities = [orb(20, 190)];
  advance(state, neutralIntent());
  assert.equal(state.stats.missed, 1);
  assert.equal(state.entities.length, 0);
  assert.ok(state.events.some((event) => event.type === "missed"));
});

test("resolver a chuva compacta o mesmo array e não troca a lista", () => {
  const state = createState(6);
  const entities = state.entities;
  state.entities.push(orb(20, 190));
  advance(state, neutralIntent());
  assert.equal(state.entities, entities, "um array novo por tick é o churn que o poço evita");
  assert.equal(state.entities.length, 0);
});

test("entidade morta volta ao poço e o próximo spawn a reusa", () => {
  const state = createState(3);
  state.spawnTimer = 1;
  advance(state, neutralIntent());
  assert.equal(state.entities.length, 1);
  const born = state.entities[0];
  const before = entityPoolStats();
  born.y = 190;
  born.vy = 0;
  advance(state, neutralIntent());
  assert.equal(state.entities.length, 0);
  assert.equal(state.entities.includes(born), false);
  assert.equal(entityPoolStats().released, before.released + 1);
  state.spawnTimer = 1;
  advance(state, neutralIntent());
  assert.equal(state.entities[0], born, "o poço devolve o mesmo objeto, não um novo");
  assert.equal(entityPoolStats().created, before.created, "reusar não cria outro objeto");
});

test("retomar JSON não puxa mortos do poço", () => {
  const state = createState(4);
  state.spawnTimer = 1;
  advance(state, neutralIntent());
  assert.equal(state.entities.length, 1);
  const saved = JSON.parse(JSON.stringify(state));
  const liveId = state.entities[0].id;
  state.entities[0].y = 190;
  state.entities[0].vy = 0;
  advance(state, neutralIntent());
  assert.equal(state.entities.length, 0);
  assert.equal(saved.entities.length, 1);
  assert.equal(saved.entities[0].id, liveId);
  assert.equal(saved.entities[0].kind, "orb", "o morto do poço não vaza para o JSON retomado");
  advance(saved, neutralIntent());
  assert.equal(saved.entities[0].id, liveId, "o objeto retomado continua a própria chuva");
  assert.ok(saved.entities[0].y < 190);
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

test("o perfil dusk muda a chuva sem republicar o verbo", () => {
  const calm = createState(7);
  const late = createState(7, { spawnProfile: "dusk" });
  assert.equal(calm.spawnProfile, "spawn");
  assert.equal(late.spawnProfile, "dusk");
  assert.equal(calm.spawn.intervalTicks, 22);
  assert.equal(late.spawn.intervalTicks, 16);
  assert.equal(calm.spawnTimer, 22);
  assert.equal(late.spawnTimer, 16);
  while (calm.tick < 80) advance(calm, neutralIntent());
  while (late.tick < 80) advance(late, neutralIntent());
  assert.notEqual(calm.nextId, late.nextId, "intervalo distinto nasce quantidade distinta");
  assert.ok(late.spawn.practiceTicks < calm.spawn.practiceTicks);
  const calmKinds = new Set();
  const lateKinds = new Set();
  const calmPractice = createState(11);
  const latePractice = createState(11, { spawnProfile: "dusk" });
  while (calmPractice.tick < 120) {
    advance(calmPractice, neutralIntent());
    for (const entity of calmPractice.entities) calmKinds.add(entity.kind);
  }
  while (latePractice.tick < 400 && !lateKinds.has("shard")) {
    advance(latePractice, neutralIntent());
    for (const entity of latePractice.entities) lateKinds.add(entity.kind);
  }
  assert.equal(calmKinds.has("shard"), false, "o padrão ainda está em prática aos 120");
  assert.equal(lateKinds.has("shard"), true, "crepúsculo encerra a prática aos 90");
});
