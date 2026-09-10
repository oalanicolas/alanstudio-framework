// As regras são a parte do jogo que um teste pode fechar. Feel, arte e diversão
// exigem observação; invariantes não.

import { test } from "node:test";
import assert from "node:assert/strict";

import { advance, approaching, attractEntities, attractMove, attractTick, attractTouch, beginRun, bedRateFor, createState, entityPoolStats, eventPoolStats, lookAhead, motePoolStats, rngPoolStats, neutralIntent, CONFIG, FIELD, PLAYER_Y, chainPipCount, chainPipAt, chainPlaybackRate, remainingTicks, closingWindow, closingPulse, practicingWindow, practicePulse, recoveringWindow, recoveryPulse, spawnHazardChance, spawnIntervalScale, threatCue } from "../src/game/rules.js";

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

test("dois orbes no mesmo quadro: o segundo espera o próximo tick", () => {
  const fade = CONFIG.feel.shakeDecay;
  const state = createState(5);
  const x = state.player.x;
  state.entities = [
    { id: 2, kind: "orb", x, y: PLAYER_Y, vy: 0 },
    { id: 3, kind: "orb", x: x + 0.4, y: PLAYER_Y, vy: 0 },
  ];
  advance(state, neutralIntent());
  assert.equal(state.chain, 1, "dois orbes no mesmo quadro não inflam a corrente");
  assert.equal(state.stats.collected, 1);
  assert.equal(state.events.filter((event) => event.type === "collect").length, 1);
  assert.equal(state.entities.length, 1, "o segundo orbe fica para o próximo quadro");
  assert.equal(state.entities[0].id, 3);
  assert.equal(
    state.shake,
    CONFIG.feel.collectShake * fade,
    "o suco não empilha duas coletas",
  );
  settle(state);
  advance(state, neutralIntent());
  assert.equal(state.chain, 2, "o segundo orbe conta no tick seguinte");
  assert.equal(state.stats.collected, 2);
});

test("dois estilhaços no mesmo quadro: o segundo já é graça", () => {
  const fade = CONFIG.feel.shakeDecay;
  const state = createState(2);
  state.chain = 5;
  const x = state.player.x;
  state.entities = [
    { id: 2, kind: "shard", x, y: PLAYER_Y - 1, vy: 0 },
    { id: 3, kind: "shard", x: x + 0.4, y: PLAYER_Y - 1, vy: 0 },
  ];
  advance(state, neutralIntent());
  assert.equal(state.chain, 0);
  assert.equal(state.stats.hits, 1, "o segundo estilhaço do mesmo quadro não é segundo hit");
  assert.equal(state.events.filter((event) => event.type === "hit").length, 1);
  assert.ok(state.events.some((event) => event.type === "graze"), "o segundo raspa");
  assert.equal(state.player.invuln, CONFIG.player.invulnTicks);
  assert.equal(
    state.shake,
    (CONFIG.feel.hitShake + CONFIG.feel.grazeShake) * fade,
    "o suco não empilha dois impactos",
  );
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

test("o término do dash também atravessa o estilhaço", () => {
  const state = createState(3);
  dashOut(state);
  assert.equal(state.player.dashTicks, CONFIG.player.dashTicks);
  while (state.player.dashTicks > 1) advance(state, neutralIntent());
  assert.equal(state.player.dashTicks, 1);
  state.chain = 2;
  state.entities = [shard(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  assert.equal(state.player.dashTicks, 0);
  assert.ok(state.events.some((event) => event.type === "land"), "o término ainda nasce");
  assert.equal(state.stats.hits, 0, "o quadro do land não é janela de hit");
  assert.equal(state.chain, 2);
  assert.ok(state.events.some((event) => event.type === "graze"));
});

test("depois do término a recuperação continua vulnerável", () => {
  const state = createState(3);
  dashOut(state);
  while (state.player.dashTicks > 0) advance(state, neutralIntent());
  assert.ok(state.player.dashRecovery > 0);
  assert.ok(state.events.some((event) => event.type === "land"));
  state.chain = 2;
  state.entities = [shard(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  assert.equal(state.stats.hits, 1, "a recuperação depois do land continua vulnerável");
  assert.equal(state.chain, 0);
});

test("antecipar o avanço também atravessa o estilhaço", () => {
  const state = createState(3);
  advance(state, { move: 1, dash: true, bank: false });
  assert.equal(state.player.dashWindup, CONFIG.player.dashWindupTicks);
  assert.equal(state.player.dashTicks, 0);
  state.chain = 2;
  state.entities = [shard(state.player.x, PLAYER_Y)];
  advance(state, { move: 1, dash: false, bank: false });
  assert.equal(state.chain, 2, "o coil não é janela de hit");
  assert.equal(state.stats.hits, 0);
  assert.equal(state.stats.dashes, 0, "atravessar no coil ainda não disparou");
  assert.ok(state.events.some((event) => event.type === "graze"));
});

test("antecipar a guarda também atravessa o estilhaço", () => {
  const state = createState(3);
  state.chain = 2;
  advance(state, { move: 0, dash: false, bank: true });
  assert.equal(state.bankWindup, CONFIG.bank.windupTicks);
  assert.equal(state.stats.banks, 0, "o pedido ainda não converteu");
  state.entities = [shard(state.player.x, PLAYER_Y)];
  advance(state, { move: 0, dash: false, bank: false });
  assert.equal(state.chain, 2, "o arco da guarda não é janela de hit");
  assert.equal(state.stats.hits, 0);
  assert.equal(state.stats.banks, 0, "atravessar no arco ainda não converteu");
  assert.ok(state.events.some((event) => event.type === "graze"));
});

test("converter a guarda também atravessa o estilhaço", () => {
  const state = createState(3);
  state.chain = 2;
  advance(state, { move: 0, dash: false, bank: true });
  assert.equal(state.bankWindup, CONFIG.bank.windupTicks);
  advance(state, { move: 0, dash: false, bank: false });
  assert.equal(state.bankWindup, 1, "ainda no arco");
  assert.equal(state.stats.banks, 0);
  state.entities = [shard(state.player.x, PLAYER_Y)];
  advance(state, { move: 0, dash: false, bank: false });
  assert.equal(state.stats.banks, 1, "o quadro da conversão ainda converte");
  assert.equal(state.chain, 0);
  assert.equal(state.score, 4);
  assert.equal(state.stats.hits, 0, "o quadro da conversão não é janela de hit");
  assert.ok(state.events.some((event) => event.type === "bank"));
  assert.ok(state.events.some((event) => event.type === "graze"));
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

test("o raspo confirma no corpo e na câmera sem congelar", () => {
  const fade = CONFIG.feel.squashDecay;
  const tremor = CONFIG.feel.shakeDecay;
  const flash = CONFIG.feel.flashDecay;
  const punch = CONFIG.feel.punchDecay;
  const state = createState(3);
  state.player.invuln = 10;
  state.player.dir = 1;
  state.entities = [shard(state.player.x, PLAYER_Y)];
  advance(state, neutralIntent());
  assert.ok(state.events.some((event) => event.type === "graze"));
  assert.equal(state.hitstop, 0, "raspo não congela o dash");
  assert.equal(state.player.squash, CONFIG.feel.squashGraze * fade);
  assert.equal(state.shake, CONFIG.feel.grazeShake * tremor);
  assert.equal(state.flash, CONFIG.feel.flashGraze * flash);
  assert.equal(state.camera.x, CONFIG.feel.punchGrazeX * punch);
  assert.equal(state.camera.y, 0, "raspo empurra na direção, não para baixo");
  const left = createState(4);
  left.player.invuln = 10;
  left.player.dir = -1;
  left.entities = [shard(left.player.x, PLAYER_Y)];
  advance(left, neutralIntent());
  assert.equal(left.camera.x, -CONFIG.feel.punchGrazeX * punch);
  assert.ok(CONFIG.feel.squashGraze < 0, "o contato estreita, não alonga");
  assert.ok(CONFIG.feel.squashGraze !== CONFIG.feel.squashCoil);
  assert.ok(CONFIG.feel.grazeShake > CONFIG.feel.missedShake);
  assert.ok(CONFIG.feel.grazeShake < CONFIG.feel.collectShake);
  assert.ok(CONFIG.feel.punchGrazeX > 0);
  assert.ok(CONFIG.feel.punchGrazeX < CONFIG.feel.punchDashX);
  assert.ok(CONFIG.feel.flashGraze > 0);
  assert.ok(CONFIG.feel.flashGraze < CONFIG.feel.flashMissed);
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
    CONFIG.feel.squashGraze,
    CONFIG.feel.squashCollect,
    CONFIG.feel.squashMiss,
    CONFIG.feel.squashDash,
    CONFIG.feel.squashLand,
    CONFIG.feel.squashBank,
    CONFIG.feel.squashOver,
    CONFIG.feel.squashHit,
  ];
  assert.equal(new Set(squashes).size, 9, "squash repetido não distingue o verbo");
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

test("threatCue só nomeia o estilhaço no x do corpo", () => {
  const state = createState(1);
  state.phase = "playing";
  state.player.x = 80;
  state.entities = [
    { id: 1, kind: "orb", x: 80, y: PLAYER_Y - 24, vy: 1 },
    { id: 2, kind: "shard", x: 200, y: PLAYER_Y - 24, vy: 1 },
    { id: 3, kind: "shard", x: 80, y: -8, vy: 1 },
  ];
  assert.equal(threatCue(state), null);
  state.entities[2].y = PLAYER_Y - 24;
  assert.equal(threatCue(state), "ahead");
  state.phase = "title";
  assert.equal(threatCue(state), null, "a porta não lê a chuva da partida");
  state.phase = "playing";
  state.entities[2].y = PLAYER_Y;
  assert.equal(threatCue(state), null, "na faixa o aviso já é o próprio contato");
});

test("a porta nomeia o estilhaço da mostra no trilho", () => {
  const door = createState(1, { entry: "title" });
  assert.equal(threatCue(door), null);
  assert.ok(seatOnShow(door, "shard", "ahead"), "esperava o estilhaço no telegraph");
  assert.equal(threatCue(door), "ahead");
  assert.equal(door.tick, 0);
  assert.equal(door.entities.length, 0);
  const ended = createState(1);
  ended.phase = "over";
  assert.equal(threatCue(ended), null);
});

test("reduced na porta trava o aviso na mostra visível", () => {
  const door = createState(1, { entry: "title" });
  let drop = null;
  for (let step = 0; step < 400; step += 1) {
    const rain = attractEntities(door);
    const shard = rain.find((item, index) => {
      if (item.kind !== "shard" || index !== 1) return false;
      const gap = PLAYER_Y - item.y;
      return gap > CONFIG.collect.reachY && gap <= CONFIG.feel.telegraphReach;
    });
    if (shard) {
      drop = shard;
      door.player.x = shard.x;
      break;
    }
    attractTick(door);
  }
  assert.ok(drop, "esperava o estilhaço do meio no telegraph");
  assert.equal(threatCue(door), "ahead");
  assert.equal(threatCue(door, true), null, "reduced lê a mostra parada, não a chuva que o canvas some");
  assert.equal(door.entities.length, 0);
});

test("a porta marca a mostra no trilho sem ler a chuva da partida", () => {
  const door = createState(1, { entry: "title" });
  door.entities = [{ id: 99, kind: "orb", x: 80, y: PLAYER_Y - 24, vy: 1 }];
  assert.equal(
    approaching(door).some((item) => item.id === 99),
    false,
    "a porta não lê a chuva da partida",
  );
  const drop = seatOnShow(door, "shard", "ahead");
  assert.ok(drop, "esperava o estilhaço no telegraph");
  const near = approaching(door);
  assert.ok(
    near.some((item) => item.kind === "shard" && Math.abs(item.x - drop.x) < 0.01),
    "a mostra precisa marcar o trilho",
  );
  assert.equal(approaching(door), near, "o telegraph reusa o buffer; consumir antes do próximo quadro");
  assert.equal(door.entities.length, 1);
  assert.equal(door.tick, 0);
  const frozen = approaching(door, true);
  const frozenRain = attractEntities(door, true);
  for (const item of frozen) {
    assert.ok(
      frozenRain.some((drop) => drop.kind === item.kind && Math.abs(drop.x - item.x) < 0.01),
      "com menos movimento o aviso segue a chuva travada",
    );
  }
  const play = createState(1);
  play.entities = [{ id: 1, kind: "orb", x: 80, y: PLAYER_Y - 24, vy: 1 }];
  assert.equal(approaching(play).length, 1);
  assert.equal(approaching(play)[0].id, 1);
});

test("a câmera confirma o trilho sem ser punch", () => {
  const state = createState(1);
  state.player.x = 160;
  state.entities = [{ id: 1, kind: "shard", x: 220, y: PLAYER_Y - 24, vy: 1 }];
  const right = lookAhead(state);
  assert.ok(right.x > 0, "ameaça à direita inclina o quadro");
  assert.ok(right.x <= CONFIG.feel.lookAheadX);
  assert.ok(CONFIG.feel.lookAheadX < CONFIG.feel.punchDashX, "o lean não é o punch do dash");
  assert.equal(right.y, 0);
  state.entities[0].x = 100;
  const left = lookAhead(state);
  assert.ok(left.x < 0, "ameaça à esquerda inclina o quadro");
  assert.equal(lookAhead(state, true).x, 0, "reduced some o lean");
  state.phase = "title";
  assert.equal(lookAhead(state).x, 0, "a porta não inclina o quadro");
  state.phase = "playing";
  state.entities[0].y = PLAYER_Y;
  assert.equal(lookAhead(state).x, 0, "na faixa o aviso já é o próprio contato");
  const door = createState(1, { entry: "title" });
  assert.equal(lookAhead(door).x, 0);
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
  state.spawnTimer = CONFIG.bank.windupTicks + 1;
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
  assert.equal(state.player.x, FIELD.width / 2, "advance na porta não move");
  beginRun(state);
  assert.equal(state.phase, "playing");
  assert.equal(state.player.squash, CONFIG.feel.squashLand, "a porta fecha o arco");
  assert.ok(state.events.some((event) => event.type === "dash"), "a porta fala o avanço");
  assert.ok(state.events.some((event) => event.type === "land"), "a porta também aterrissa");
  assert.equal(state.stats.dashes, 0, "abrir a porta não conta o ofício");
  assert.ok(state.camera.x !== 0, "a porta desloca o campo");
  assert.ok(state.camera.y > 0, "aterrissar confirma para baixo");
  advance(state, neutralIntent());
  assert.equal(state.tick, 1);
  beginRun(state);
  assert.equal(state.tick, 1, "beginRun fora da abertura não reinicia");
});

test("a porta aterrissa sem fingir peso percebido", () => {
  const state = createState(1, { entry: "title" });
  beginRun(state);
  assert.equal(state.phase, "playing");
  assert.equal(state.player.squash, CONFIG.feel.squashLand);
  const land = state.events.find((event) => event.type === "land");
  assert.ok(land, "a porta precisa do término");
  assert.equal(typeof land.x, "number");
  assert.ok(Number.isFinite(land.x));
  assert.equal(
    state.motes.filter((mote) => mote.kind === "land").length,
    CONFIG.feel.moteLand,
    "a porta deixa o puff do término",
  );
  assert.equal(state.player.dashTicks, 0, "a porta não viaja");
  assert.equal(state.player.dashRecovery, 0, "a porta não come o primeiro dash");
  assert.equal(state.stats.dashes, 0);
  assert.doesNotMatch(String(state.events.map((event) => event.type)), /aprovado|verified|felt|heard/);
});

test("a porta fala o começo da mostra sem ligar a cama", () => {
  const state = createState(1, { entry: "title" });
  const rng = state.rngState;
  assert.equal(state.events.some((event) => event.type === "live"), false);
  attractTick(state);
  assert.ok(state.events.some((event) => event.type === "live"), "a primeira mostra precisa falar");
  assert.equal(state.events.filter((event) => event.type === "live").length, 1);
  assert.equal(state.tick, 0);
  assert.equal(state.phase, "title");
  assert.equal(state.entities.length, 0);
  assert.equal(state.rngState, rng);
  assert.equal(state.motes.length, 0, "live na porta não é rastro");
  attractTick(state);
  assert.equal(state.events.some((event) => event.type === "live"), false, "o segundo tick não repete a voz");
  const play = createState(1);
  attractTick(play);
  assert.equal(play.events.some((event) => event.type === "live"), false, "fora da porta a mostra não fala");
});

test("a porta recebe o movimento sem comer o tick", () => {
  const state = createState(1, { entry: "title" });
  const rng = state.rngState;
  const start = state.player.x;
  attractMove(state, { move: 1 });
  assert.ok(state.player.x > start, "a porta precisa do passo");
  assert.equal(state.player.dir, 1);
  assert.equal(state.tick, 0);
  assert.equal(state.phase, "title");
  assert.equal(state.entities.length, 0);
  assert.equal(state.events.length, 0);
  assert.equal(state.rngState, rng);
  attractMove(state, { move: -1 });
  assert.equal(state.player.dir, -1);
  attractMove(state, { move: 0 });
  assert.equal(state.tick, 0, "parado não anda o relógio");
  const play = createState(1);
  const idle = play.player.x;
  attractMove(play, { move: 1 });
  assert.equal(play.player.x, idle, "fora da porta o passo não existe");
  const edge = createState(1, { entry: "title" });
  edge.player.x = FIELD.width - CONFIG.player.halfWidth;
  attractMove(edge, { move: 1 });
  assert.equal(edge.player.x, FIELD.width - CONFIG.player.halfWidth, "a porta respeita a borda");
});

function seatOnShow(state, kind, band) {
  for (let step = 0; step < 400; step += 1) {
    const rain = attractEntities(state);
    const drop = rain.find((item) => {
      if (item.kind !== kind) return false;
      const gap = PLAYER_Y - item.y;
      if (band === "ahead") return gap > CONFIG.collect.reachY && gap <= CONFIG.feel.telegraphReach;
      return Math.abs(item.y - PLAYER_Y) < CONFIG.collect.reachY;
    });
    if (drop) {
      state.player.x = drop.x;
      return drop;
    }
    attractTick(state);
  }
  return null;
}

test("a mostra toca o corpo sem pontuar nem comer a seed", () => {
  const state = createState(1, { entry: "title" });
  const rng = state.rngState;
  const drop = seatOnShow(state, "shard");
  assert.ok(drop, "esperava o estilhaço na faixa");
  attractTouch(state);
  assert.equal(state.phase, "title");
  assert.equal(state.tick, 0);
  assert.equal(state.score, 0);
  assert.equal(state.chain, 0);
  assert.equal(state.entities.length, 0);
  assert.equal(state.events.length, 0);
  assert.equal(state.rngState, rng);
  assert.equal(state.flash, CONFIG.feel.flashGraze);
  assert.equal(state.player.squash, CONFIG.feel.squashGraze);
  const again = state.flash;
  attractTouch(state);
  assert.equal(state.flash, again, "o mesmo toque não recarrega o pulso");
  const play = createState(1);
  const idle = play.player.squash;
  attractTouch(play);
  assert.equal(play.player.squash, idle, "fora da porta o toque não existe");
});

test("a assistência na porta também deixa a mostra mais lenta", () => {
  const plain = createState(7, { entry: "title" });
  const helped = createState(7, { entry: "title", assist: true });
  for (let step = 0; step < 20; step += 1) {
    attractTick(plain);
    attractTick(helped);
  }
  const shown = attractEntities(plain);
  const soft = attractEntities(helped);
  assert.equal(shown.length, soft.length);
  assert.equal(shown[0].x, soft[0].x, "assistência não muda a faixa");
  assert.ok(soft[0].y < shown[0].y, "assistência na porta cai mais devagar");
  assert.equal(plain.rngState, helped.rngState);
  assert.equal(plain.entities.length, 0);
  assert.equal(helped.entities.length, 0);
});

test("a assistência na porta também alarga o toque da mostra", () => {
  const helped = createState(1, { entry: "title", assist: true });
  const drop = seatOnShow(helped, "orb");
  assert.ok(drop, "esperava o orbe na faixa");
  helped.player.x = drop.x + CONFIG.player.halfWidth + CONFIG.collect.pad + 1;
  attractTouch(helped);
  assert.equal(helped.flash, CONFIG.feel.flashMissed, "o mesmo orbe fora do alcance padrão acende com assistência");
  assert.equal(helped.chain, 0, "o toque não finge coleta");
  assert.equal(helped.score, 0);

  const plain = createState(1, { entry: "title" });
  const missed = seatOnShow(plain, "orb");
  assert.ok(missed, "esperava o orbe na faixa");
  plain.player.x = missed.x + CONFIG.player.halfWidth + CONFIG.collect.pad + 1;
  attractTouch(plain);
  assert.equal(plain.flash, 0, "sem assistência o mesmo vão não acende");

  const stillOut = createState(1, { entry: "title", assist: true });
  const far = seatOnShow(stillOut, "orb");
  assert.ok(far, "esperava o orbe na faixa");
  stillOut.player.x = far.x + CONFIG.player.halfWidth + CONFIG.collect.pad + CONFIG.assist.collectPad + 1;
  attractTouch(stillOut);
  assert.equal(stillOut.flash, 0, "assistência na porta não é alcance infinito");
});

test("reduced na porta trava o toque na mostra visível", () => {
  const state = createState(1, { entry: "title" });
  assert.ok(seatOnShow(state, "orb"), "esperava o orbe na faixa");
  attractTouch(state);
  assert.equal(state.flash, CONFIG.feel.flashMissed);
  state.flash = 0;
  state.attractTouch = "";
  attractTouch(state, true);
  assert.equal(state.flash, 0, "reduced trava o toque na mostra parada");
  assert.equal(state.chain, 0);
  assert.equal(state.score, 0);
});

test("o orbe da mostra acende sem fingir coleta", () => {
  const state = createState(1, { entry: "title" });
  assert.ok(seatOnShow(state, "orb"), "esperava o orbe na faixa");
  attractTouch(state);
  assert.equal(state.flash, CONFIG.feel.flashMissed);
  assert.equal(state.player.squash, CONFIG.feel.squashCollect);
  assert.equal(state.stats.collected, 0);
  assert.equal(state.chain, 0);
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
  assert.equal(state.camera.y, CONFIG.feel.punchMissedY * CONFIG.feel.punchDecay, "perder o orbe confirma para baixo");
  assert.equal(state.shake, CONFIG.feel.missedShake * CONFIG.feel.shakeDecay, "a queda treme menos que a coleta");
  assert.equal(state.player.squash, CONFIG.feel.squashMiss * CONFIG.feel.squashDecay, "perder o orbe senta o corpo");
  assert.equal(state.hitstop, 0, "perder o orbe não congela o mundo");
  assert.ok(CONFIG.feel.punchMissedY > 0);
  assert.ok(CONFIG.feel.punchMissedY < CONFIG.feel.punchLandY, "a queda desloca menos que aterrissar");
  assert.ok(CONFIG.feel.missedShake < CONFIG.feel.collectShake, "a queda treme menos que a coleta");
  assert.ok(CONFIG.feel.squashMiss > 0, "a queda senta, não estreita");
  assert.ok(CONFIG.feel.squashMiss < CONFIG.feel.squashCollect, "a queda senta menos que a coleta");
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

test("no fim o corpo senta; a conta sobrevive", () => {
  const state = createState(7);
  state.chain = 5;
  state.tick = CONFIG.runTicks - 1;
  state.spawnTimer = 999;
  state.player.squash = CONFIG.feel.squashDash;
  state.shake = 4;
  state.flash = 0.8;
  state.camera = { x: 6, y: -4 };
  advance(state, neutralIntent());
  assert.equal(state.phase, "over");
  assert.equal(state.player.squash, CONFIG.feel.squashOver, "o relógio senta o corpo");
  assert.equal(state.shake, 0, "o relógio senta o tremor");
  assert.equal(state.flash, 0, "o relógio senta o flash");
  assert.equal(state.camera.x, 0, "o relógio senta o punch");
  assert.equal(state.camera.y, 0);
  assert.ok(CONFIG.feel.squashOver > CONFIG.feel.squashBank);
  assert.ok(CONFIG.feel.squashOver < CONFIG.feel.squashHit);
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
  assert.ok(enter.flash >= CONFIG.feel.flashClose, "o pulso do fecho acende o campo");
  assert.ok(CONFIG.feel.flashClose < CONFIG.feel.flashStir);
  assert.ok(CONFIG.feel.flashClose > CONFIG.feel.flashMissed);

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

test("o fecho aperta a chuva sem fingir curva observada", () => {
  const mid = createState(3);
  mid.tick = 1800;
  assert.equal(closingWindow(mid), false);
  assert.equal(spawnIntervalScale(mid, mid.spawn), 1);

  const close = createState(3);
  close.tick = CONFIG.runTicks - 300;
  assert.equal(closingWindow(close), true);
  assert.equal(spawnIntervalScale(close, close.spawn), close.spawn.closeIntervalScale);
  assert.ok(close.spawn.closeIntervalScale < 1);
  close.spawnTimer = 0;
  const progress = Math.min(1, (close.tick + 1) / close.spawn.rampTicks);
  const unscaled = Math.round(
    close.spawn.intervalTicks + (close.spawn.minIntervalTicks - close.spawn.intervalTicks) * progress,
  );
  advance(close, neutralIntent());
  assert.ok(close.spawnTimer < unscaled, "o fecho precisa encurtar o intervalo");
  assert.ok(close.spawnTimer >= 1);

  const both = createState(3);
  both.tick = CONFIG.runTicks - 300;
  both.recoverUntil = both.tick + 40;
  assert.ok(Math.abs(
    spawnIntervalScale(both, both.spawn)
      - both.spawn.recoveryIntervalScale * both.spawn.closeIntervalScale,
  ) < 1e-9, "recuperação e fecho se multiplicam");
});

test("o fecho sobe o risco sem fingir curva observada", () => {
  const mid = createState(3);
  mid.tick = 1800;
  const base = spawnHazardChance(mid, mid.spawn);
  assert.equal(closingWindow(mid), false);
  assert.ok(base > 0);
  assert.equal(base, mid.spawn.hazardChanceEnd);

  const close = createState(3);
  close.tick = CONFIG.runTicks - 300;
  assert.equal(closingWindow(close), true);
  const raised = spawnHazardChance(close, close.spawn);
  assert.ok(close.spawn.closeHazardScale > 1);
  assert.ok(raised > base, "o fecho precisa subir o estilhaço, não só encher");
  assert.ok(raised <= 0.95);

  const old = createState(3);
  old.tick = CONFIG.runTicks - 300;
  old.spawn = { ...old.spawn, closeHazardScale: 1 };
  assert.equal(spawnHazardChance(old, old.spawn), base);

  const early = createState(3);
  early.tick = 10;
  assert.equal(spawnHazardChance(early, early.spawn), 0);
});

test("a cama sobe o tom no fecho sem fingir mix ouvido", () => {
  assert.ok(CONFIG.feel.closeBedRate > 1);
  const mid = createState(3);
  mid.tick = 1800;
  assert.equal(bedRateFor(mid), 1);

  const enter = createState(3);
  enter.tick = CONFIG.runTicks - CONFIG.feel.closeTicks;
  const late = createState(3);
  late.tick = CONFIG.runTicks - 30;
  assert.equal(closingPulse(enter).active, true);
  assert.equal(closingPulse(late).active, true);
  assert.ok(bedRateFor(enter) > 1);
  assert.ok(bedRateFor(late) > bedRateFor(enter));
  assert.ok(bedRateFor(late) <= CONFIG.feel.closeBedRate);

  const ended = createState(3);
  ended.phase = "over";
  ended.tick = CONFIG.runTicks;
  assert.equal(bedRateFor(ended), 1);
});
