// As regras são a parte do jogo que um teste pode fechar. Feel, arte e diversão
// exigem observação; invariantes não.

import { test } from "node:test";
import assert from "node:assert/strict";

import { advance, approaching, attractEntities, attractTick, beginRun, createState, entityPoolStats, eventPoolStats, motePoolStats, rngPoolStats, neutralIntent, CONFIG, PLAYER_Y, chainPipCount, chainPipAt, chainPlaybackRate, remainingTicks, closingWindow, closingPulse, practicingWindow, practicePulse, recoveringWindow, recoveryPulse } from "../src/game/rules.js";

const orb = (x, y) => ({ id: 1, kind: "orb", x, y, vy: 0 });
const shard = (x, y) => ({ id: 2, kind: "shard", x, y, vy: 0 });

function settle(state) {
  while (state.hitstop > 0) advance(state, neutralIntent());
  return state;
}

function dashOut(state, intent = { move: 1, dash: true, bank: false }) {
  advance(state, intent);
  for (let step = 0; step < CONFIG.player.dashWindupTicks; step += 1) {
    advance(state, { ...intent, dash: false });
  }
  return state;
}

function bankOut(state, intent = { move: 0, dash: false, bank: true }) {
  advance(state, intent);
  if (state.events.some((event) => event.type === "bank")) return state;
  for (let step = 0; step < CONFIG.bank.windupTicks; step += 1) {
    advance(state, { ...intent, bank: false });
  }
  return state;
}

test("guardar senta antes de converter e não dispara no pedido", () => {
  const fade = CONFIG.feel.squashDecay;
  const state = createState(1);
  state.chain = 4;
  advance(state, { move: 0, dash: false, bank: true });
  assert.equal(state.stats.banks, 0, "o pedido não é o disparo");
  assert.equal(state.score, 0);
  assert.equal(state.chain, 4);
  assert.equal(state.bankWindup, CONFIG.bank.windupTicks);
  assert.equal(state.player.squash, CONFIG.feel.squashCoil * fade);
  assert.equal(state.events.some((event) => event.type === "bank"), false);
  assert.ok(CONFIG.bank.windupTicks > 0);
  for (let step = 0; step < CONFIG.bank.windupTicks; step += 1) {
    advance(state, { move: 0, dash: false, bank: false });
  }
  assert.equal(state.score, 16);
  assert.equal(state.chain, 0);
  assert.equal(state.stats.banks, 1);
  assert.ok(state.events.some((event) => event.type === "bank"));
});

test("guardar converte a corrente ao quadrado e cobra o compromisso", () => {
  const state = createState(1);
  state.chain = 4;
  bankOut(state);
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
    { type: "hit", lost: 5, x: state.player.x },
  );
  const shards = state.motes.filter((mote) => mote.kind === "break");
  assert.equal(shards.length, 5, "a corrente quebra no corpo, não some");
  assert.ok(shards.every((mote) => mote.vx !== 0 || mote.vy !== 0), "o pip sai da órbita");
});

test("sem corrente o erro não inventa pip quebrado; o teto da órbita vale na quebra", () => {
  const empty = createState(2);
  empty.entities = [shard(empty.player.x, PLAYER_Y - 1)];
  advance(empty, neutralIntent());
  assert.equal(empty.motes.filter((mote) => mote.kind === "break").length, 0);
  const packed = createState(2);
  packed.chain = 12;
  packed.entities = [shard(packed.player.x, PLAYER_Y - 1)];
  advance(packed, neutralIntent());
  assert.equal(
    packed.motes.filter((mote) => mote.kind === "break").length,
    CONFIG.feel.chainPips,
    "o teto dos pips também é o teto da quebra",
  );
});

test("guardar deposita os pips no placar, não some com a aposta", () => {
  const state = createState(1);
  state.chain = 5;
  bankOut(state);
  const deposits = state.motes.filter((mote) => mote.kind === "deposit");
  assert.equal(deposits.length, 5, "a corrente voa para o placar, não some");
  const aimX = CONFIG.feel.depositAimX;
  const aimY = CONFIG.feel.depositAimY;
  assert.ok(
    deposits.every((mote) => {
      const endX = mote.x + mote.vx * mote.life;
      const endY = mote.y + mote.vy * mote.life;
      return Math.abs(endX - aimX) < 0.01 && Math.abs(endY - aimY) < 0.01;
    }),
    "cada pip chega no placar",
  );
  assert.ok(deposits.every((mote) => mote.vy < 0), "o placar fica acima do corpo");
});

test("a coleta leva o orbe ao slot da órbita, não some com o contato", () => {
  const state = createState(5);
  state.entities = [orb(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  const joins = state.motes.filter((mote) => mote.kind === "join");
  assert.equal(joins.length, 1, "o primeiro elo voa para a órbita");
  const dest = chainPipAt(0, 1, state.player.x, PLAYER_Y, state.tick, false);
  assert.ok(
    joins.every((mote) => {
      const endX = mote.x + mote.vx * mote.life;
      const endY = mote.y + mote.vy * mote.life;
      return Math.abs(endX - dest.x) < 0.01 && Math.abs(endY - dest.y) < 0.01;
    }),
    "o orbe chega no slot do pip",
  );
});

test("o teto da órbita não inventa um nono pip na coleta", () => {
  const packed = createState(5);
  packed.chain = CONFIG.feel.chainPips;
  packed.entities = [orb(packed.player.x, PLAYER_Y)];
  advance(packed, neutralIntent());
  assert.equal(packed.chain, CONFIG.feel.chainPips + 1);
  assert.equal(
    packed.motes.filter((mote) => mote.kind === "join").length,
    0,
    "o teto dos pips também é o teto da entrada",
  );
});

test("sem corrente o guardar não inventa depósito; o teto da órbita vale na guarda", () => {
  const empty = createState(1);
  advance(empty, { move: 0, dash: false, bank: true });
  assert.equal(empty.motes.filter((mote) => mote.kind === "deposit").length, 0);
  const packed = createState(1);
  packed.chain = 12;
  bankOut(packed);
  assert.equal(
    packed.motes.filter((mote) => mote.kind === "deposit").length,
    CONFIG.feel.chainPips,
    "o teto dos pips também é o teto do depósito",
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

test("o avanço senta antes de alongar e não dispara no pedido", () => {
  const state = createState(3);
  advance(state, { move: 1, dash: true, bank: false });
  assert.equal(state.player.dashTicks, 0, "o pedido não é o disparo");
  assert.equal(state.stats.dashes, 0, "antecipar não conta o ofício");
  assert.equal(state.player.dashWindup, CONFIG.player.dashWindupTicks);
  assert.equal(state.player.squash, CONFIG.feel.squashCoil * CONFIG.feel.squashDecay);
  assert.equal(state.events.some((event) => event.type === "dash"), false);
  assert.ok(CONFIG.feel.squashCoil < 0, "a antecipação estreita, não alonga");
  assert.ok(CONFIG.feel.squashCoil !== CONFIG.feel.squashDash);
  assert.ok(CONFIG.player.dashWindupTicks > 0);
  for (let step = 0; step < CONFIG.player.dashWindupTicks; step += 1) {
    advance(state, { move: 1, dash: false, bank: false });
  }
  assert.equal(state.player.dashTicks, CONFIG.player.dashTicks);
  assert.equal(state.stats.dashes, 1);
  assert.ok(state.events.some((event) => event.type === "dash"));
});

test("o término do dash senta, empurra a câmera e deixa rastro próprio", () => {
  const fade = CONFIG.feel.squashDecay;
  const state = createState(3);
  dashOut(state);
  assert.equal(state.player.dashTicks, CONFIG.player.dashTicks);
  while (state.player.dashTicks > 0) advance(state, neutralIntent());
  assert.equal(state.player.dashRecovery, CONFIG.player.dashRecoveryTicks);
  assert.equal(state.player.squash, CONFIG.feel.squashLand * fade);
  assert.ok(state.camera.y > 0, "aterrissar confirma para baixo");
  const land = state.events.find((event) => event.type === "land");
  assert.ok(land, "o término precisa nascer como evento");
  assert.equal(typeof land.x, "number");
  assert.ok(Number.isFinite(land.x), "o término marca o lugar no campo");
  assert.equal(
    state.motes.filter((mote) => mote.kind === "land").length,
    CONFIG.feel.moteLand,
    "o término precisa de puff próprio",
  );
  assert.ok(
    state.motes.filter((mote) => mote.kind === "land").every((mote) => mote.vy > 0),
    "o puff do término cai, não copia a partida",
  );
  assert.ok(CONFIG.feel.squashLand > CONFIG.feel.squashDash);
  assert.ok(CONFIG.feel.squashLand < CONFIG.feel.squashBank);
  assert.ok(CONFIG.feel.punchLandY < CONFIG.feel.punchBankY);
  assert.ok(CONFIG.feel.rumbleLandMs < CONFIG.feel.rumbleDashMs);
});

test("o dash atravessa o estilhaço sem perder a corrente", () => {
  const state = createState(3);
  dashOut(state);
  assert.ok(state.player.dashTicks > 0);
  assert.equal(state.stats.dashes, 1);
  state.chain = 2;
  state.entities = [shard(state.player.x, PLAYER_Y)];
  advance(state, { move: 1, dash: false, bank: false });
  assert.equal(state.chain, 2);
  assert.ok(state.events.some((event) => event.type === "graze"));
  assert.equal(
    state.motes.filter((mote) => mote.kind === "graze").length,
    CONFIG.feel.moteGraze,
    "o raspo precisa riscar o campo",
  );
});

test("cada verbo tem sinal próprio de partida e contato", () => {
  const fade = CONFIG.feel.squashDecay;
  const tremor = CONFIG.feel.shakeDecay;
  const dash = createState(3);
  dashOut(dash);
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
  bankOut(banked);
  assert.equal(banked.hitstop, CONFIG.feel.bankHitstopTicks);
  assert.equal(banked.player.squash, CONFIG.feel.squashBank * fade);
  assert.equal(banked.shake, CONFIG.feel.bankShake * tremor);

  const struck = createState(2);
  struck.entities = [shard(struck.player.x, PLAYER_Y - 1)];
  advance(struck, neutralIntent());
  assert.equal(struck.hitstop, CONFIG.feel.hitHitstopTicks);
  assert.equal(struck.player.squash, CONFIG.feel.squashHit * fade);
  assert.equal(struck.shake, CONFIG.feel.hitShake * tremor);

  const stops = [
    CONFIG.feel.collectHitstopTicks,
    CONFIG.feel.bankHitstopTicks,
    CONFIG.feel.hitHitstopTicks,
  ];
  assert.equal(new Set(stops).size, 3, "hitstop repetido não distingue o verbo");
  const squashes = [
    CONFIG.feel.squashCoil,
    CONFIG.feel.squashCollect,
    CONFIG.feel.squashDash,
    CONFIG.feel.squashLand,
    CONFIG.feel.squashBank,
    CONFIG.feel.squashHit,
  ];
  assert.equal(new Set(squashes).size, 6, "squash repetido não distingue o verbo");
  assert.notEqual(CONFIG.feel.collectShake, CONFIG.feel.hitShake);
  assert.notEqual(CONFIG.feel.bankShake, CONFIG.feel.collectShake);
  assert.notEqual(dash.camera.x, 0, "dash empurra a câmera na direção");
  assert.equal(collected.camera.y < 0, true, "coleta sobe a câmera");
  assert.equal(banked.camera.y > 0, true, "guardar confirma para baixo");
  assert.ok(Math.abs(struck.camera.y) > Math.abs(collected.camera.y), "o erro desloca mais que a coleta");
  assert.equal(collected.flash, 0, "coleta não acende o campo como se fosse o erro");
  assert.equal(struck.flash, CONFIG.feel.flashHit * CONFIG.feel.flashDecay);
  assert.equal(dash.motes.length, CONFIG.feel.moteDash, "dash precisa deixar rastro");
  const collectBurst = collected.motes.filter((mote) => mote.kind === "collect");
  assert.equal(collectBurst.length, CONFIG.feel.moteCollect, "coleta precisa deixar rastro");
  const bankBurst = banked.motes.filter((mote) => mote.kind === "bank");
  assert.equal(bankBurst.length, CONFIG.feel.moteBank, "guardar precisa deixar rastro");
  assert.equal(struck.motes.length, CONFIG.feel.moteHit, "o erro precisa espalhar mais");
  const motes = [
    CONFIG.feel.moteDash,
    CONFIG.feel.moteLand,
    CONFIG.feel.moteCollect,
    CONFIG.feel.moteGraze,
    CONFIG.feel.moteBank,
    CONFIG.feel.moteHit,
    CONFIG.feel.moteOver,
  ];
  assert.equal(new Set(motes).size, 7, "rastro repetido não distingue o verbo");
  assert.equal(CONFIG.feel.chainPips, 8);
  assert.ok(CONFIG.feel.chainOrbit > CONFIG.player.halfWidth, "a órbita precisa caber fora do corpo");
  assert.ok(CONFIG.feel.chainSpin > 0);
  assert.ok(CONFIG.feel.depositAimY < PLAYER_Y, "o placar fica acima do corpo");
  assert.ok(collectBurst.every((mote) => mote.vy < 0), "coleta sobe");
  assert.ok(bankBurst.every((mote) => mote.vy > 0), "guardar confirma para baixo");
});

test("a corrente no corpo conta o que o HUD já sabe, com teto", () => {
  assert.equal(chainPipCount(0), 0);
  assert.equal(chainPipCount(3), 3);
  assert.equal(chainPipCount(12), CONFIG.feel.chainPips);
  const a = chainPipAt(0, 3, 100, PLAYER_Y, 0, true);
  const b = chainPipAt(0, 3, 100, PLAYER_Y, 40, true);
  assert.deepEqual(a, b, "com menos movimento a formação não orbita");
  const c = chainPipAt(0, 3, 100, PLAYER_Y, 40, false);
  assert.notEqual(a.x, c.x);
  assert.equal(chainPlaybackRate(0), 1);
  assert.ok(chainPlaybackRate(1) > 1);
  assert.ok(chainPlaybackRate(5) > chainPlaybackRate(1));
  assert.equal(chainPlaybackRate(20), CONFIG.feel.chainRateMax);
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
  assert.equal(approaching(state), near, "o telegraph reusa o buffer; consumir antes do próximo quadro");
  state.entities[0].y = PLAYER_Y;
  assert.equal(approaching(state).length, 0, "na faixa de coleta o aviso já é o próprio orbe");
});

test("evento reusado não carrega campo do verbo anterior", () => {
  const state = createState(1);
  state.chain = 4;
  state.spawnTimer = 999;
  bankOut(state);
  assert.deepEqual(state.events[0], { type: "bank", chain: 4, gain: 16 });
  const before = eventPoolStats();
  while (state.hitstop > 0 || state.bankLock > 0) {
    advance(state, neutralIntent());
  }
  dashOut(state);
  const dash = state.events.find((event) => event.type === "dash");
  assert.equal(dash.type, "dash");
  assert.equal(typeof dash.x, "number");
  assert.ok(Number.isFinite(dash.x), "o avanço marca o lugar no campo");
  assert.equal("chain" in dash, false);
  assert.equal("gain" in dash, false);
  assert.equal(eventPoolStats().created, before.created, "reusar o evento não cria outro objeto");
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
  for (let index = 0; index < CONFIG.bank.bufferTicks + CONFIG.bank.windupTicks + 2 && !fired; index += 1) {
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
  for (let index = 0; index < 4 + CONFIG.player.dashWindupTicks && !fired; index += 1) {
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
  assert.equal(recoveringWindow(state), false);
  bankOut(state);
  assert.ok(state.recoverUntil > state.tick);
  assert.equal(recoveringWindow(state), true);
  assert.ok(recoveryPulse(state).fill > 0.9);
  assert.ok(
    state.spawnTimer > CONFIG.spawn.intervalTicks,
    "a recuperação alonga o intervalo, não o encurta",
  );
  const until = state.recoverUntil;
  state.tick = until;
  assert.equal(recoveringWindow(state), false);
  assert.equal(recoveryPulse(state).active, false);
  const ended = createState(1);
  ended.phase = "over";
  ended.recoverUntil = 80;
  ended.tick = 10;
  assert.equal(recoveringWindow(ended), false);
});

test("a abertura não avança o tick até o corpo apontar", () => {
  const state = createState(1, { entry: "title" });
  assert.equal(state.phase, "title");
  advance(state, { move: 1, dash: true, bank: true });
  assert.equal(state.phase, "title");
  assert.equal(state.tick, 0);
  assert.equal(state.entities.length, 0);
  beginRun(state);
  assert.equal(state.phase, "playing");
  assert.equal(state.player.squash, CONFIG.feel.squashDash, "a porta senta como o avanço");
  assert.ok(state.events.some((event) => event.type === "dash"), "a porta fala o avanço");
  assert.equal(state.stats.dashes, 0, "abrir a porta não conta o ofício");
  assert.ok(state.camera.x !== 0, "a porta desloca o campo");
  advance(state, neutralIntent());
  assert.equal(state.tick, 1);
  beginRun(state);
  assert.equal(state.tick, 1, "beginRun fora da abertura não reinicia");
});

test("a chuva da porta não come a seed", () => {
  const state = createState(7, { entry: "title" });
  const rng = state.rngState;
  attractTick(state);
  attractTick(state);
  assert.equal(state.tick, 0);
  assert.equal(state.entities.length, 0);
  assert.equal(state.rngState, rng);
  assert.equal(state.phase, "title");
  const rain = attractEntities(state);
  assert.equal(rain.length, 4, "a mostra do spawn continua a chuva de quatro");
  assert.equal(rain[0].x, 48);
  assert.equal(rain[1].x, 120);
  assert.ok(rain.some((entity) => entity.kind === "orb"));
  assert.ok(rain.some((entity) => entity.kind === "shard"));
  const frozen = attractEntities(state, true);
  assert.notEqual(frozen[0].y, rain[0].y, "com menos movimento a chuva da porta trava");
  beginRun(state);
  assert.equal(attractEntities(state).length, 0, "abrir a porta some a chuva de mostra");
});

test("a porta chove a mesa sem comer a seed", () => {
  const spawn = createState(7, { entry: "title" });
  const dusk = createState(7, { entry: "title", spawnProfile: "dusk" });
  const calm = createState(7, { entry: "title", spawnProfile: "calm" });
  const rng = { spawn: spawn.rngState, dusk: dusk.rngState, calm: calm.rngState };
  attractTick(spawn);
  attractTick(dusk);
  attractTick(calm);
  const shown = attractEntities(spawn);
  const late = attractEntities(dusk);
  const soft = attractEntities(calm);
  assert.equal(shown.length, 4);
  assert.ok(late.length > shown.length, "dusk na porta é mais denso");
  assert.ok(soft.length < shown.length, "calm na porta é mais folgado");
  assert.ok(late[0].y > shown[0].y, "dusk na porta cai mais rápido");
  assert.ok(soft[0].y < shown[0].y, "calm na porta cai mais devagar");
  assert.ok(late.some((entity) => entity.kind === "orb"));
  assert.ok(late.some((entity) => entity.kind === "shard"));
  assert.ok(soft.some((entity) => entity.kind === "orb"));
  assert.ok(soft.some((entity) => entity.kind === "shard"));
  assert.equal(spawn.rngState, rng.spawn);
  assert.equal(dusk.rngState, rng.dusk);
  assert.equal(calm.rngState, rng.calm);
  assert.equal(spawn.entities.length, 0);
  assert.equal(dusk.tick, 0);
});

test("sair da recuperação emite e acende o campo", () => {
  const state = createState(1);
  state.chain = 2;
  bankOut(state);
  assert.equal(state.events.some((event) => event.type === "stir"), false, "guardar não é o tap da volta");
  const until = state.recoverUntil;
  state.hitstop = 0;
  state.bankLock = 0;
  state.tick = until - 1;
  advance(state, neutralIntent());
  assert.equal(state.tick, until);
  assert.equal(recoveringWindow(state), false);
  assert.ok(state.events.some((event) => event.type === "stir"), "sair da recuperação precisa emitir");
  assert.ok(state.flash >= CONFIG.feel.flashStir, "sair da recuperação acende o campo");

  const mid = createState(1);
  mid.chain = 2;
  bankOut(mid);
  mid.hitstop = 0;
  mid.tick = mid.recoverUntil - 10;
  advance(mid, neutralIntent());
  assert.equal(mid.events.some((event) => event.type === "stir"), false, "meio da recuperação não é o tap");

  const hold = createState(1);
  hold.chain = 2;
  bankOut(hold);
  const first = hold.recoverUntil;
  hold.hitstop = 0;
  hold.bankLock = 0;
  hold.bankWindup = 0;
  hold.tick = first - 1;
  hold.chain = 2;
  bankOut(hold);
  assert.ok(hold.recoverUntil > first);
  assert.equal(hold.events.some((event) => event.type === "stir"), false, "alongar a folga não é a volta");
});

test("orbe perdido é contado, não silencioso", () => {
  const state = createState(6);
  state.entities = [orb(20, 190)];
  advance(state, neutralIntent());
  assert.equal(state.stats.missed, 1);
  assert.equal(state.entities.length, 0);
  const missed = state.events.find((event) => event.type === "missed");
  assert.ok(missed);
  assert.equal(missed.x, 20, "a voz precisa do lugar da queda");
  assert.ok(state.flash >= CONFIG.feel.flashMissed, "perder o orbe acende o campo");
  const stains = state.motes.filter((mote) => mote.kind === "missed");
  assert.equal(stains.length, CONFIG.feel.moteMissed, "perder o orbe marca o lugar");
  assert.ok(stains.every((mote) => Math.abs(mote.x - 20) <= 4), "a marca fica onde o orbe caiu");
  assert.ok(stains.every((mote) => mote.y > PLAYER_Y), "a marca fica na queda, não no corpo");
  assert.ok(stains.every((mote) => mote.vy > 0), "a queda continua para baixo");
});

test("resolver a chuva compacta o mesmo array e não troca a lista", () => {
  const state = createState(6);
  const entities = state.entities;
  state.entities.push(orb(20, 190));
  advance(state, neutralIntent());
  assert.equal(state.entities, entities, "um array novo por tick é o churn que o poço evita");
  assert.equal(state.entities.length, 0);
});

test("o rastro volta ao poço quando a vida acaba", () => {
  const state = createState(5);
  state.entities = [orb(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  assert.equal(
    state.motes.filter((mote) => mote.kind === "collect").length,
    CONFIG.feel.moteCollect,
  );
  assert.equal(state.motes.filter((mote) => mote.kind === "join").length, 1);
  const born = state.motes[0];
  const before = motePoolStats();
  for (let index = 0; index < CONFIG.feel.moteLife; index += 1) {
    advance(state, neutralIntent());
  }
  assert.equal(state.motes.length, 0, "a vida do rastro precisa acabar");
  assert.ok(motePoolStats().released > before.released);
  state.entities = [orb(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  assert.ok(state.motes.includes(born), "o poço devolve o mesmo mote");
  assert.equal(motePoolStats().created, before.created, "reusar o rastro não cria outro objeto");
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

test("o gerador da chuva reusa o mesmo objeto entre partidas", () => {
  const before = rngPoolStats();
  const first = createState(11);
  first.spawnTimer = 1;
  advance(first, neutralIntent());
  const second = createState(12);
  second.spawnTimer = 1;
  advance(second, neutralIntent());
  const after = rngPoolStats();
  assert.equal(after.created, 1);
  assert.equal(after.created, before.created);
  assert.ok(after.reseeds > before.reseeds);
  assert.notEqual(first.rngState, second.rngState);
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

test("no fim a aposta não guardada cai; a conta sobrevive", () => {
  const state = createState(7);
  state.chain = 5;
  state.tick = CONFIG.runTicks - 1;
  state.spawnTimer = 999;
  advance(state, neutralIntent());
  assert.equal(state.phase, "over");
  assert.equal(state.chain, 5, "a conta no estado sobrevive ao fim");
  const over = state.events.find((event) => event.type === "over");
  assert.equal(over.unbanked, 5);
  const lapses = state.motes.filter((mote) => mote.kind === "lapse");
  assert.equal(lapses.length, 5, "a aposta cai, não some");
  assert.ok(
    lapses.every((mote) => mote.vx === 0 && mote.vy === CONFIG.feel.lapseFall),
    "a queda é para baixo, não explosão nem depósito",
  );
});

test("sem corrente o fim não inventa queda; o teto vale na perda", () => {
  const empty = createState(7);
  empty.tick = CONFIG.runTicks - 1;
  empty.spawnTimer = 999;
  advance(empty, neutralIntent());
  assert.equal(empty.motes.filter((mote) => mote.kind === "lapse").length, 0);
  const packed = createState(7);
  packed.chain = 12;
  packed.tick = CONFIG.runTicks - 1;
  packed.spawnTimer = 999;
  advance(packed, neutralIntent());
  assert.equal(
    packed.motes.filter((mote) => mote.kind === "lapse").length,
    CONFIG.feel.chainPips,
    "o teto dos pips também é o teto da queda",
  );
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

test("o perfil calm alonga a prática sem republicar o verbo", () => {
  const base = createState(7);
  const soft = createState(7, { spawnProfile: "calm" });
  assert.equal(soft.spawnProfile, "calm");
  assert.equal(soft.spawn.intervalTicks, 30);
  assert.equal(soft.spawn.practiceTicks, 420);
  assert.equal(soft.spawnTimer, 30);
  assert.ok(soft.spawn.intervalTicks > base.spawn.intervalTicks);
  assert.ok(soft.spawn.practiceTicks > base.spawn.practiceTicks);
  assert.ok(soft.spawn.hazardChanceEnd < base.spawn.hazardChanceEnd);
  while (base.tick < 80) advance(base, neutralIntent());
  while (soft.tick < 80) advance(soft, neutralIntent());
  assert.ok(soft.nextId < base.nextId, "intervalo maior nasce menos itens");
  const kinds = new Set();
  const practice = createState(11, { spawnProfile: "calm" });
  while (practice.tick < 200) {
    advance(practice, neutralIntent());
    for (const entity of practice.entities) kinds.add(entity.kind);
  }
  assert.equal(kinds.has("shard"), false, "calm ainda está em prática aos 200");
});

test("a prática some no último tick e o campo acende sem inventar shard cedo", () => {
  const start = createState(3);
  assert.equal(practicingWindow(start), true);
  assert.equal(practicePulse(start).active, true);
  assert.ok(practicePulse(start).fill > 0.9);
  assert.equal(start.events.some((event) => event.type === "live"), false);

  const late = createState(3);
  late.tick = start.spawn.practiceTicks - 1;
  assert.equal(practicingWindow(late), true);
  advance(late, neutralIntent());
  assert.equal(late.tick, start.spawn.practiceTicks);
  assert.equal(practicingWindow(late), false);
  assert.equal(practicePulse(late).active, false);
  assert.ok(late.events.some((event) => event.type === "live"), "sair da prática precisa emitir");
  assert.ok(late.flash >= CONFIG.feel.flashPractice, "sair da prática acende o campo");

  const mid = createState(3);
  mid.tick = Math.floor(start.spawn.practiceTicks / 2);
  advance(mid, neutralIntent());
  assert.equal(mid.events.some((event) => event.type === "live"), false, "meio da prática não é o tap");

  const ended = createState(3);
  ended.phase = "over";
  ended.tick = 0;
  assert.equal(practicingWindow(ended), false);
});

test("o fecho emite no segundo redondo e não no meio do segundo", () => {
  assert.equal(CONFIG.feel.closeTicks, 10 * 60, "o fecho é dez segundos no passo fixo");
  const early = createState(3);
  advance(early, neutralIntent());
  assert.equal(closingWindow(early), false);
  assert.equal(closingPulse(early).active, false);
  assert.equal(early.events.some((event) => event.type === "close"), false);

  const enter = createState(3);
  enter.tick = CONFIG.runTicks - CONFIG.feel.closeTicks - 1;
  advance(enter, neutralIntent());
  assert.equal(remainingTicks(enter), CONFIG.feel.closeTicks);
  assert.equal(closingWindow(enter), true);
  assert.equal(closingPulse(enter).active, true);
  assert.ok(enter.events.some((event) => event.type === "close"), "entrar no fecho precisa emitir");

  const mid = createState(3);
  mid.tick = CONFIG.runTicks - 571;
  advance(mid, neutralIntent());
  assert.equal(remainingTicks(mid), 570);
  assert.equal(closingWindow(mid), true);
  assert.equal(mid.events.some((event) => event.type === "close"), false, "meio do segundo não é o tap");

  const beat = createState(3);
  beat.tick = CONFIG.runTicks - 541;
  advance(beat, neutralIntent());
  assert.equal(remainingTicks(beat), 540);
  assert.ok(beat.events.some((event) => event.type === "close"));

  const ended = createState(3);
  ended.phase = "over";
  ended.tick = CONFIG.runTicks;
  assert.equal(closingWindow(ended), false);
});
