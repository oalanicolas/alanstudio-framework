// Regras da partida: dados puros, sem DOM, sem tempo real, sem aleatoriedade
// externa. Todo o estado é JSON simples, então a mesma função serve ao jogo, ao
// teste headless e a um replay a partir de uma seed.
//
// Decisão característica: **guardar ou continuar**. Cada orbe aumenta a corrente;
// guardar converte a corrente em pontos ao quadrado, mas trava o dash por um
// instante; ser atingido zera a corrente inteira. Corrente não guardada no fim
// da partida é perdida.

import { createRng } from "../core/rng.js";
import { loadSpawn, requireFields, resolveSpawnName, SPAWN_FIELDS } from "./tables.js";

const spawnTable = requireFields("spawn", SPAWN_FIELDS);

export const TICK_HZ = 60;
export const FIELD = { width: 320, height: 180 };
export const PLAYER_Y = FIELD.height - 18;

// Valores de feel e de perdão de entrada são decisão de design, não folclore.
// Cada um está aqui com o motivo; alterar sem registrar é como perdê-los.
export const CONFIG = {
  runTicks: TICK_HZ * 60,
  player: {
    halfWidth: 7,
    speed: 1.9,
    dashSpeed: 5.4,
    dashTicks: 8, // contato: rápido e invulnerável
    dashRecoveryTicks: 6, // recuperação: controle reduzido, ainda vulnerável
    dashCooldownTicks: 30,
    dashBufferTicks: 8, // perdão: dash pedido cedo dispara ao recarregar
    invulnTicks: 42, // graça após dano; evita perder duas correntes seguidas
  },
  collect: {
    pad: 5, // alcance além do desenho: quem quase pegou, pega
    reachY: 8,
  },
  hazard: { radius: 6 },
  // A chuva é conteúdo: cadência, mistura e velocidade moram em data/spawn.json,
  // não nesta regra. Alterar o dado não exige republicar o verbo.
  spawn: spawnTable,
  feel: {
    collectHitstopTicks: 2, // contato do acerto
    bankHitstopTicks: 3, // peso da decisão de guardar
    hitHitstopTicks: 5, // o erro precisa doer mais que o acerto
    collectShake: 0.12,
    bankShake: 0.28,
    hitShake: 1,
    shakeDecay: 0.86,
    squashCollect: 0.22,
    squashDash: 0.34, // partida do dash: alonga na direção, não achata
    squashDecay: 0.82,
    punchCollectY: -1.6, // coleta sobe a câmera
    punchBankY: 2.4, // guardar confirma para baixo
    punchDashX: 3.2, // dash empurra na direção
    punchHitY: 4.2, // o erro desloca mais que a coleta
    punchDecay: 0.78,
    telegraphReach: 36, // antecipação: a ameaça marca o trilho antes do contato
    flashHit: 0.55, // impacto do erro: o campo acende; coleta não
    flashDecay: 0.72,
  },
  bank: {
    lockTicks: 24, // custo do compromisso: sem dash enquanto guarda
    bufferTicks: 8, // perdão: pedido cedo ou no hitstop dispara quando a corrente existe
  },
  // Assistência não esconde conteúdo: os mesmos orbes, a mesma pontuação.
  // Perdão extra de alcance, chuva mais lenta e graça mais longa.
  assist: {
    collectPad: 4,
    collectReachY: 3,
    fallSpeedScale: 0.72,
    extraInvulnTicks: 18,
  },
};

const clamp = (value, min, max) => (value < min ? min : value > max ? max : value);
const lerp = (from, to, amount) => from + (to - from) * amount;

// Poço de entidades: mora no módulo, não no estado. Observe e fingerprint só
// vêem os vivos. Retomar JSON.parse continua válido — o objeto retomado não
// veio daqui e volta ao poço só quando morre de novo.
const entityPool = [];
const poolCounts = { created: 0, acquired: 0, released: 0 };

export function entityPoolStats() {
  return {
    idle: entityPool.length,
    created: poolCounts.created,
    acquired: poolCounts.acquired,
    released: poolCounts.released,
  };
}

function acquireEntity(id, kind, x, y, vy) {
  poolCounts.acquired += 1;
  const entity = entityPool.pop();
  if (entity === undefined) {
    poolCounts.created += 1;
    return { id, kind, x, y, vy };
  }
  entity.id = id;
  entity.kind = kind;
  entity.x = x;
  entity.y = y;
  entity.vy = vy;
  return entity;
}

function releaseEntity(entity) {
  poolCounts.released += 1;
  entity.id = 0;
  entity.kind = "";
  entity.x = 0;
  entity.y = 0;
  entity.vy = 0;
  entityPool.push(entity);
}

function rain(state) {
  return state.spawn ?? CONFIG.spawn;
}

export function createState(seed = 1, options = {}) {
  const rng = createRng(seed);
  const spawnProfile = resolveSpawnName(options.spawnProfile);
  const spawn = { ...loadSpawn(spawnProfile) };
  return {
    version: 1,
    seed,
    assist: Boolean(options.assist),
    spawnProfile,
    spawn,
    rngState: rng.state,
    tick: 0,
    phase: "playing",
    score: 0,
    chain: 0,
    hitstop: 0,
    shake: 0,
    flash: 0,
    camera: { x: 0, y: 0 },
    bankLock: 0,
    bankBuffer: 0,
    spawnTimer: spawn.intervalTicks,
    recoverUntil: 0,
    nextId: 1,
    player: {
      x: FIELD.width / 2,
      dir: 1,
      dashTicks: 0,
      dashRecovery: 0,
      dashCooldown: 0,
      dashBuffer: 0,
      invuln: 0,
      squash: 0,
    },
    entities: [],
    stats: { collected: 0, missed: 0, hits: 0, banks: 0, bestChain: 0, banked: 0 },
    events: [],
  };
}

export function neutralIntent() {
  return { move: 0, dash: false, bank: false };
}

export function remainingTicks(state) {
  return Math.max(0, CONFIG.runTicks - state.tick);
}

// Avança exatamente um passo de simulação. Muta e devolve o mesmo estado: o loop
// de jogo roda isto muitas vezes por segundo e alocar um estado novo por passo
// produz coleta de lixo perceptível como engasgo. A chuva compacta o array vivo
// e reusa objetos do poço; evento e telegraph ainda alocam.
export function advance(state, intent = neutralIntent()) {
  state.events.length = 0;
  if (state.phase !== "playing") {
    return state;
  }
  state.tick += 1;
  const player = state.player;

  // O pedido de dash é registrado antes de qualquer congelamento, para que uma
  // entrada durante o hitstop não seja engolida.
  if (intent.dash) {
    player.dashBuffer = CONFIG.player.dashBufferTicks;
  } else if (player.dashBuffer > 0) {
    player.dashBuffer -= 1;
  }
  // Corrente vazia não guarda o pedido: um toque cedo demais não decide
  // guardar o orbe que ainda não existe.
  if (intent.bank && state.chain > 0) {
    state.bankBuffer = CONFIG.bank.bufferTicks;
  } else if (state.bankBuffer > 0) {
    state.bankBuffer -= 1;
  }

  if (state.hitstop > 0) {
    state.hitstop -= 1;
    state.shake *= CONFIG.feel.shakeDecay;
    decayFlash(state);
    decayCamera(state);
    return state;
  }

  advanceDashPhases(player);
  if (player.invuln > 0) player.invuln -= 1;
  if (state.bankLock > 0) state.bankLock -= 1;

  const canDash =
    player.dashTicks === 0 &&
    player.dashRecovery === 0 &&
    player.dashCooldown === 0 &&
    state.bankLock === 0;
  if (canDash && player.dashBuffer > 0) {
    player.dashTicks = CONFIG.player.dashTicks;
    player.dashBuffer = 0;
    player.squash = CONFIG.feel.squashDash;
    if (intent.move !== 0) player.dir = intent.move;
    punch(state, CONFIG.feel.punchDashX * player.dir, 0);
    state.events.push({ type: "dash" });
  }

  movePlayer(state, intent);
  bank(state, intent);
  spawn(state);
  resolveEntities(state);
  // Mesmo quadro: coleta primeiro, guardar depois — o pedido deste tick
  // não espera o buffer se o orbe acabou de entrar na corrente.
  if (intent.bank) bank(state, intent);

  state.shake *= CONFIG.feel.shakeDecay;
  if (state.shake < 0.01) state.shake = 0;
  decayFlash(state);
  decayCamera(state);
  player.squash *= CONFIG.feel.squashDecay;
  if (player.squash < 0.01) player.squash = 0;

  if (state.tick >= CONFIG.runTicks) {
    state.phase = "over";
    state.events.push({ type: "over", score: state.score, unbanked: state.chain });
  }
  return state;
}

function advanceDashPhases(player) {
  if (player.dashTicks > 0) {
    player.dashTicks -= 1;
    if (player.dashTicks === 0) player.dashRecovery = CONFIG.player.dashRecoveryTicks;
    return;
  }
  if (player.dashRecovery > 0) {
    player.dashRecovery -= 1;
    if (player.dashRecovery === 0) player.dashCooldown = CONFIG.player.dashCooldownTicks;
    return;
  }
  if (player.dashCooldown > 0) player.dashCooldown -= 1;
}

function movePlayer(state, intent) {
  const player = state.player;
  const limit = CONFIG.player.halfWidth;
  if (player.dashTicks > 0) {
    player.x = clamp(player.x + CONFIG.player.dashSpeed * player.dir, limit, FIELD.width - limit);
    return;
  }
  const control = player.dashRecovery > 0 ? 0.45 : 1;
  if (intent.move !== 0) player.dir = intent.move;
  player.x = clamp(
    player.x + CONFIG.player.speed * intent.move * control,
    limit,
    FIELD.width - limit,
  );
}

function bank(state, intent) {
  const requested = state.bankBuffer > 0 || Boolean(intent?.bank);
  if (!requested || state.bankLock > 0 || state.chain === 0) return;
  const chain = state.chain;
  const gain = chain * chain;
  state.score += gain;
  state.stats.banked += gain;
  state.stats.banks += 1;
  state.chain = 0;
  state.bankBuffer = 0;
  state.bankLock = CONFIG.bank.lockTicks;
  state.hitstop = CONFIG.feel.bankHitstopTicks;
  state.shake += CONFIG.feel.bankShake;
  punch(state, 0, CONFIG.feel.punchBankY);
  state.recoverUntil = state.tick + rain(state).recoveryTicks;
  state.events.push({ type: "bank", chain, gain });
}

function spawn(state) {
  const table = rain(state);
  state.spawnTimer -= 1;
  if (state.spawnTimer > 0) return;
  const progress = Math.min(1, state.tick / table.rampTicks);
  const recovering = state.tick < state.recoverUntil;
  const intervalScale = recovering ? table.recoveryIntervalScale : 1;
  state.spawnTimer = Math.round(
    lerp(table.intervalTicks, table.minIntervalTicks, progress) * intervalScale,
  );
  const rng = createRng(state.seed, state.rngState);
  const practicing = state.tick < table.practiceTicks;
  const hazardChance = practicing
    ? 0
    : lerp(table.hazardChanceStart, table.hazardChanceEnd, progress);
  const kind = rng.next() < hazardChance ? "shard" : "orb";
  const x = rng.range(14, FIELD.width - 14);
  const fall = state.assist ? CONFIG.assist.fallSpeedScale : 1;
  const vy = rng.range(table.fallSpeedMin, table.fallSpeedMax) * (1 + progress * 0.35) * fall;
  state.rngState = rng.state;
  state.entities.push(acquireEntity(state.nextId, kind, x, -8, vy));
  state.nextId += 1;
}

function resolveEntities(state) {
  const player = state.player;
  const invulnerable = player.invuln > 0 || player.dashTicks > 0;
  const entities = state.entities;
  let write = 0;
  for (let index = 0; index < entities.length; index += 1) {
    const entity = entities[index];
    entity.y += entity.vy;
    const pad = CONFIG.collect.pad + (state.assist ? CONFIG.assist.collectPad : 0);
    const reachY = CONFIG.collect.reachY + (state.assist ? CONFIG.assist.collectReachY : 0);
    const reach =
      CONFIG.player.halfWidth +
      (entity.kind === "orb" ? pad : CONFIG.hazard.radius);
    const touching =
      Math.abs(entity.y - PLAYER_Y) < reachY && Math.abs(entity.x - player.x) < reach;
    if (touching) {
      if (entity.kind === "orb") {
        collect(state);
        releaseEntity(entity);
        continue;
      }
      if (invulnerable) {
        state.events.push({ type: "graze" });
        releaseEntity(entity);
        continue;
      }
      hit(state);
      releaseEntity(entity);
      continue;
    }
    if (entity.y > FIELD.height + 8) {
      if (entity.kind === "orb") {
        state.stats.missed += 1;
        state.events.push({ type: "missed" });
      }
      releaseEntity(entity);
      continue;
    }
    entities[write] = entity;
    write += 1;
  }
  entities.length = write;
}

function collect(state) {
  state.chain += 1;
  state.stats.collected += 1;
  if (state.chain > state.stats.bestChain) state.stats.bestChain = state.chain;
  state.hitstop = CONFIG.feel.collectHitstopTicks;
  state.shake += CONFIG.feel.collectShake;
  state.player.squash = CONFIG.feel.squashCollect;
  punch(state, 0, CONFIG.feel.punchCollectY);
  state.events.push({ type: "collect", chain: state.chain });
}

function hit(state) {
  const lost = state.chain;
  state.chain = 0;
  state.bankBuffer = 0;
  state.stats.hits += 1;
  state.player.invuln = CONFIG.player.invulnTicks + (state.assist ? CONFIG.assist.extraInvulnTicks : 0);
  state.hitstop = CONFIG.feel.hitHitstopTicks;
  state.shake += CONFIG.feel.hitShake;
  state.flash = CONFIG.feel.flashHit;
  punch(state, 0, CONFIG.feel.punchHitY);
  state.events.push({ type: "hit", lost });
}

export function approaching(state) {
  const reach = CONFIG.feel.telegraphReach;
  const band = CONFIG.collect.reachY;
  return state.entities.filter((entity) => {
    const gap = PLAYER_Y - entity.y;
    return gap > band && gap <= reach;
  });
}

function punch(state, x, y) {
  state.camera.x += x;
  state.camera.y += y;
}

function decayFlash(state) {
  state.flash *= CONFIG.feel.flashDecay;
  if (state.flash < 0.02) state.flash = 0;
}

function decayCamera(state) {
  state.camera.x *= CONFIG.feel.punchDecay;
  state.camera.y *= CONFIG.feel.punchDecay;
  if (Math.abs(state.camera.x) < 0.01) state.camera.x = 0;
  if (Math.abs(state.camera.y) < 0.01) state.camera.y = 0;
}
