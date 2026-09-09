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
    squashLand: 0.40, // término: senta depois de alongar; menor que guardar
    squashBank: 0.46, // compromisso: senta mais que a coleta
    squashHit: 0.62, // o erro esmaga mais que guardar
    squashDecay: 0.82,
    punchCollectY: -1.6, // coleta sobe a câmera
    punchBankY: 2.4, // guardar confirma para baixo
    punchDashX: 3.2, // dash empurra na direção
    punchLandY: 1.8, // aterrissa para baixo; menor que guardar
    punchHitY: 4.2, // o erro desloca mais que a coleta
    punchDecay: 0.78,
    telegraphReach: 36, // antecipação: a ameaça marca o trilho antes do contato
    flashHit: 0.55, // impacto do erro: o campo acende; coleta não
    flashDecay: 0.72,
    rumbleDashMs: 16, // partida: toque curto
    rumbleLandMs: 10, // término: tap mais curto que a partida
    rumbleCollectMs: 28, // contato do acerto
    rumbleBankMs: 48, // peso da decisão
    rumbleHitMs: 84, // o erro dói mais que guardar
    rumbleOverMs: 120, // fim
    rumbleDash: 0.16,
    rumbleLand: 0.12,
    rumbleCollect: 0.26,
    rumbleBank: 0.40,
    rumbleHit: 0.74,
    rumbleOver: 0.52,
    moteDash: 3, // rastro curto na partida
    moteLand: 2, // puff curto de término; menor que a partida
    moteCollect: 5, // contato do acerto
    moteBank: 7, // peso da decisão
    moteHit: 9, // o erro espalha mais
    moteOver: 4, // fim
    moteLife: 14,
    chainPips: 8, // a aposta cabe no corpo; o HUD continua com o resto
    chainOrbit: 15, // raio ao redor do jogador
    chainSpin: 0.035, // órbita por tick; com menos movimento a formação trava
    chainPipSize: 2.8,
    chainRateStep: 0.06, // cada elo sobe o tom da coleta e da guarda
    chainRateMax: 1.48, // teto: a conta continua no HUD
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

export function chainPipCount(chain) {
  const n = Number.isFinite(chain) ? Math.max(0, Math.floor(chain)) : 0;
  return Math.min(n, CONFIG.feel.chainPips);
}

export function chainPlaybackRate(chain) {
  const n = Number.isFinite(chain) ? Math.max(0, Math.floor(chain)) : 0;
  return Math.min(CONFIG.feel.chainRateMax, 1 + n * CONFIG.feel.chainRateStep);
}

export function chainPipAt(index, count, x, y, tick, reduced) {
  const radius = CONFIG.feel.chainOrbit;
  const spin = reduced ? 0 : tick * CONFIG.feel.chainSpin;
  const angle = spin + (index * Math.PI * 2) / Math.max(count, 1);
  return {
    x: x + Math.cos(angle) * radius,
    y: y + Math.sin(angle) * radius,
  };
}

const clamp = (value, min, max) => (value < min ? min : value > max ? max : value);
const lerp = (from, to, amount) => from + (to - from) * amount;

// Poço de entidades: mora no módulo, não no estado. Observe e fingerprint só
// vêem os vivos. Retomar JSON.parse continua válido — o objeto retomado não
// veio daqui e volta ao poço só quando morre de novo.
const entityPool = [];
const poolCounts = { created: 0, acquired: 0, released: 0 };

const spawnRng = createRng(1);
let rngReseeds = 0;

function bindSpawnRng(seed, state = null) {
  rngReseeds += 1;
  return spawnRng.reseed(seed, state);
}

export function rngPoolStats() {
  return { created: 1, reseeds: rngReseeds };
}

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

const eventPool = [];
const eventCounts = { created: 0, acquired: 0, released: 0 };
const approachingScratch = [];

export function eventPoolStats() {
  return {
    idle: eventPool.length,
    created: eventCounts.created,
    acquired: eventCounts.acquired,
    released: eventCounts.released,
  };
}

const motePool = [];
const moteCounts = { created: 0, acquired: 0, released: 0 };
const MOTE_COUNTS = {
  dash: "moteDash",
  land: "moteLand",
  collect: "moteCollect",
  bank: "moteBank",
  hit: "moteHit",
  over: "moteOver",
};

export function motePoolStats() {
  return {
    idle: motePool.length,
    created: moteCounts.created,
    acquired: moteCounts.acquired,
    released: moteCounts.released,
  };
}

function acquireMote(kind, x, y, vx, vy, life) {
  moteCounts.acquired += 1;
  const mote = motePool.pop();
  if (mote === undefined) {
    moteCounts.created += 1;
    return { kind, x, y, sx: x, sy: y, vx, vy, life };
  }
  mote.kind = kind;
  mote.x = x;
  mote.y = y;
  mote.sx = x;
  mote.sy = y;
  mote.vx = vx;
  mote.vy = vy;
  mote.life = life;
  return mote;
}

function releaseMote(mote) {
  moteCounts.released += 1;
  mote.kind = "";
  mote.x = 0;
  mote.y = 0;
  mote.sx = 0;
  mote.sy = 0;
  mote.vx = 0;
  mote.vy = 0;
  mote.life = 0;
  motePool.push(mote);
}

function burst(state, kind) {
  const key = MOTE_COUNTS[kind];
  if (!key) return;
  const count = CONFIG.feel[key];
  const life = CONFIG.feel.moteLife;
  const x = state.player.x;
  const y = PLAYER_Y;
  const dir = state.player.dir || 1;
  for (let index = 0; index < count; index += 1) {
    const unit = count === 1 ? 0 : index / (count - 1) - 0.5;
    let vx = 0;
    let vy = 0;
    if (kind === "dash") {
      vx = dir * (1.6 + Math.abs(unit) * 0.4);
      vy = unit * 1.1;
    } else if (kind === "land") {
      vx = -dir * (0.4 + Math.abs(unit) * 0.5);
      vy = 1.3 + Math.abs(unit) * 0.3;
    } else if (kind === "collect") {
      vx = unit * 1.4;
      vy = -1.8 - Math.abs(unit) * 0.3;
    } else if (kind === "bank") {
      vx = unit * 1.2;
      vy = 1.6 + Math.abs(unit) * 0.4;
    } else if (kind === "hit") {
      vx = Math.cos(index * 0.7) * 2.2;
      vy = Math.sin(index * 0.7) * 2.2;
    } else {
      vx = unit * 0.6;
      vy = 0.5 + Math.abs(unit) * 0.2;
    }
    state.motes.push(acquireMote(kind, x, y, vx, vy, life));
  }
}

function decayMotes(state) {
  const motes = state.motes;
  if (!motes || !motes.length) return;
  let write = 0;
  for (let index = 0; index < motes.length; index += 1) {
    const mote = motes[index];
    mote.life -= 1;
    mote.x += mote.vx;
    mote.y += mote.vy;
    if (mote.life > 0) {
      motes[write] = mote;
      write += 1;
    } else {
      releaseMote(mote);
    }
  }
  motes.length = write;
}

function recycleEvents(state) {
  for (let index = 0; index < state.events.length; index += 1) {
    eventCounts.released += 1;
    eventPool.push(state.events[index]);
  }
  state.events.length = 0;
}

function emit(state, type, extra) {
  eventCounts.acquired += 1;
  let event = eventPool.pop();
  if (event === undefined) {
    eventCounts.created += 1;
    event = { type };
  } else {
    event.type = type;
    for (const key of Object.keys(event)) {
      if (key !== "type" && (extra === undefined || !(key in extra))) delete event[key];
    }
  }
  if (extra) {
    for (const key of Object.keys(extra)) event[key] = extra[key];
  }
  state.events.push(event);
  burst(state, type);
}

function rain(state) {
  return state.spawn ?? CONFIG.spawn;
}

export function createState(seed = 1, options = {}) {
  const rng = bindSpawnRng(seed);
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
    motes: [],
    stats: { collected: 0, missed: 0, hits: 0, banks: 0, dashes: 0, bestChain: 0, banked: 0 },
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
// e reusa o poço; o evento volta ao poço no passo seguinte; o telegraph
// reusa um buffer; o rastro do impacto reusa o poço de motes. O gerador
// da chuva reusa o mesmo objeto.
export function advance(state, intent = neutralIntent()) {
  recycleEvents(state);
  if (!state.motes) state.motes = [];
  if (state.phase !== "playing") {
    decayMotes(state);
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
    decayMotes(state);
    return state;
  }

  advanceDashPhases(state);
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
    emit(state, "dash");
    state.stats.dashes += 1;
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
    emit(state, "over", { score: state.score, unbanked: state.chain });
  }
  decayMotes(state);
  return state;
}

function advanceDashPhases(state) {
  const player = state.player;
  if (player.dashTicks > 0) {
    player.dashTicks -= 1;
    if (player.dashTicks === 0) {
      player.dashRecovery = CONFIG.player.dashRecoveryTicks;
      player.squash = CONFIG.feel.squashLand;
      punch(state, 0, CONFIG.feel.punchLandY);
      emit(state, "land");
    }
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
  state.player.squash = CONFIG.feel.squashBank;
  punch(state, 0, CONFIG.feel.punchBankY);
  state.recoverUntil = state.tick + rain(state).recoveryTicks;
  emit(state, "bank", { chain, gain });
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
  const rng = bindSpawnRng(state.seed, state.rngState);
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
        emit(state, "graze");
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
        emit(state, "missed");
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
  emit(state, "collect", { chain: state.chain });
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
  state.player.squash = CONFIG.feel.squashHit;
  punch(state, 0, CONFIG.feel.punchHitY);
  emit(state, "hit", { lost });
}

export function approaching(state) {
  const reach = CONFIG.feel.telegraphReach;
  const band = CONFIG.collect.reachY;
  let write = 0;
  for (let index = 0; index < state.entities.length; index += 1) {
    const entity = state.entities[index];
    const gap = PLAYER_Y - entity.y;
    if (gap > band && gap <= reach) {
      approachingScratch[write] = entity;
      write += 1;
    }
  }
  approachingScratch.length = write;
  return approachingScratch;
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
