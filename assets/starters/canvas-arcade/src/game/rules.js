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
    dashRecoveryTicks: 6, // recuperação: controle reduzido, ainda vulnerável; o quadro do land atravessa
    dashCooldownTicks: 30,
    dashBufferTicks: 8, // perdão: dash pedido cedo dispara ao recarregar
    dashWindupTicks: 2, // antecipação: o corpo senta antes de alongar; já é graça; a guarda com corrente espera este coil
    invulnTicks: 42, // graça após dano; evita perder duas correntes seguidas — inclusive no mesmo quadro
  },
  // Um orbe por tick: dois no alcance não inflam a corrente.
  // Estilhaço letal no mesmo quadro: o orbe espera. Orbe no
  // arco da guarda também espera — o sit não inflama a aposta.
  // Ordem do array não decide a aposta. Pose no disco não é peso.
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
    missedShake: 0.06, // a queda treme menos que a coleta
    grazeShake: 0.08, // o raspo treme mais que a queda, menos que a coleta
    hitShake: 1,
    shakeDecay: 0.86,
    squashCollect: 0.22,
    squashMiss: 0.16, // a queda senta o corpo; menor que a coleta
    squashCoil: -0.18, // antecipação do avanço: estreita antes de alongar
    squashBankCoil: 0.28, // antecipação da guarda: senta, não estreita; menor que o compromisso
    squashGraze: -0.26, // o contato estreita; o dash alonga
    squashDash: 0.34, // partida do dash: alonga na direção, não achata
    squashLand: 0.40, // término: senta depois de alongar; menor que guardar
    squashBank: 0.46, // compromisso: senta mais que a coleta
    squashOver: 0.52, // o relógio senta o corpo; tremor e punch sentam com ele
    squashHit: 0.62, // o erro esmaga mais que guardar
    squashDecay: 0.82,
    punchCollectY: -1.6, // coleta sobe a câmera
    punchBankY: 2.4, // guardar confirma para baixo
    punchDashX: 3.2, // dash empurra na direção
    punchGrazeX: 1.6, // o raspo empurra na direção; menor que o dash
    punchLandY: 1.8, // aterrissa para baixo; menor que guardar
    punchMissedY: 0.9, // a queda confirma para baixo; menor que aterrissar
    punchHitY: 4.2, // o erro desloca mais que a coleta
    punchDecay: 0.78,
    telegraphReach: 36, // antecipação: a ameaça marca o trilho antes do contato
    lookAheadX: 2.2, // a câmera confirma o trilho; menor que o punch do dash
    flashHit: 0.55, // impacto do erro: o campo acende; coleta não
    flashPractice: 0.28, // a prática some: o campo acende menos que o erro
    flashStir: 0.18, // a folga acaba: o campo acende menos que a prática
    flashClose: 0.16, // o fecho pulsa: o campo acende menos que a folga
    flashMissed: 0.12, // o orbe caiu: o campo acende menos que a volta
    flashGraze: 0.08, // o contato acende menos que a queda
    flashDecay: 0.72,
    closeTicks: 600, // TICK_HZ * 10 — fecho: o campo marca o fim; o dado aperta a chuva; não é faixa no HUD
    closeBedRate: 1.08, // a cama sobe o tom com o pulso; número no disco não é mix ouvido
    rumbleDashMs: 16, // partida: toque curto
    rumbleLandMs: 10, // término: tap mais curto que a partida
    rumbleCollectMs: 28, // contato do acerto
    rumbleBankMs: 48, // peso da decisão
    rumbleHitMs: 84, // o erro dói mais que guardar
    rumbleOverMs: 120, // fim
    rumbleCloseMs: 36, // fecho: tap por segundo, menor que guardar
    rumbleDash: 0.16,
    rumbleLand: 0.12,
    rumbleCollect: 0.26,
    rumbleBank: 0.40,
    rumbleHit: 0.74,
    rumbleOver: 0.52,
    rumbleClose: 0.32, // entre coleta e guarda; o relógio não é o erro
    moteDash: 3, // rastro curto na partida
    moteLand: 2, // puff curto de término; menor que a partida
    moteCollect: 5, // contato do acerto
    moteGraze: 6, // o raspo risca; mais que a coleta, menos que guardar
    moteBank: 7, // peso da decisão
    moteHit: 9, // o erro espalha mais
    moteOver: 4, // fim
    moteMissed: 3, // a queda marca o lugar; não é rastro no corpo
    moteLife: 14,
    chainPips: 8, // a aposta cabe no corpo; o HUD continua com o resto
    chainOrbit: 15, // raio ao redor do jogador
    chainSpin: 0.035, // órbita por tick; com menos movimento a formação trava
    chainPipSize: 2.8,
    chainRateStep: 0.06, // cada elo sobe o tom da coleta e da guarda
    chainRateMax: 1.48, // teto: a conta continua no HUD
    depositAimX: 28, // placa da pontuação; o pip voa para o placar, não some
    depositAimY: 14,
    lapseFall: 1.8, // aposta não guardada cai; não explode nem voa ao placar
  },
  bank: {
    lockTicks: 24, // custo do compromisso: sem dash enquanto guarda
    bufferTicks: 8, // perdão: pedido cedo ou no hitstop dispara quando a corrente existe
    windupTicks: 2, // antecipação: o corpo senta antes de converter; o arco e o quadro da conversão já são graça; corrente já existente espera o coil do avanço
  },
  // Assistência não esconde conteúdo: os mesmos orbes, a mesma pontuação.
  // Perdão extra de alcance, chuva mais lenta e graça mais longa.
  // Na porta vale queda e alcance da mostra; a graça extra fica no campo.
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
  graze: "moteGraze",
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
    } else if (kind === "graze") {
      vx = dir * (2.2 + Math.abs(unit) * 0.4);
      vy = unit * 1.6;
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
    phase: options.entry === "title" ? "title" : "playing",
    score: 0,
    chain: 0,
    hitstop: 0,
    shake: 0,
    flash: 0,
    camera: { x: 0, y: 0 },
    bankLock: 0,
    bankBuffer: 0,
    bankWindup: 0,
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
      dashWindup: 0,
      invuln: 0,
      squash: 0,
    },
    entities: [],
    motes: [],
    attractTick: 0,
    stats: { collected: 0, missed: 0, hits: 0, banks: 0, dashes: 0, bestChain: 0, banked: 0 },
    events: [],
  };
}

// Retoma o recorte gravado em `hold`. Motes e eventos não voltam:
// são efêmeros. Isto não é Continuar — Continuar repete a seed.
export function restoreState(hold, options = {}) {
  if (!hold || !hold.player) return createState(hold?.seed ?? 1, options);
  const seed = hold.seed;
  const spawnProfile = resolveSpawnName(options.spawnProfile ?? hold.spawnProfile);
  const rng = bindSpawnRng(seed, hold.rngState);
  const spawn = { ...loadSpawn(spawnProfile) };
  const entities = [];
  for (const entity of hold.entities ?? []) {
    entities.push(acquireEntity(entity.id, entity.kind, entity.x, entity.y, entity.vy));
  }
  return {
    version: 1,
    seed,
    assist: options.assist !== undefined ? Boolean(options.assist) : Boolean(hold.assist),
    spawnProfile,
    spawn,
    rngState: rng.state,
    tick: hold.tick,
    phase: "playing",
    score: hold.score,
    chain: hold.chain,
    hitstop: hold.hitstop,
    shake: hold.shake,
    flash: hold.flash,
    camera: { x: hold.camera?.x ?? 0, y: hold.camera?.y ?? 0 },
    bankLock: hold.bankLock,
    bankBuffer: hold.bankBuffer,
    bankWindup: hold.bankWindup ?? 0,
    spawnTimer: hold.spawnTimer,
    recoverUntil: hold.recoverUntil,
    nextId: hold.nextId,
    player: { dashWindup: 0, ...hold.player },
    entities,
    motes: [],
    attractTick: 0,
    stats: { ...hold.stats },
    events: [],
  };
}

function landDash(state) {
  const player = state.player;
  player.squash = CONFIG.feel.squashLand;
  punch(state, 0, CONFIG.feel.punchLandY);
  emit(state, "land", { x: player.x });
}

export function beginRun(state) {
  if (!state || state.phase !== "title") return state;
  state.phase = "playing";
  // A porta também é um verbo. Não viaja: o arco fecha no
  // mesmo tick — dispara, senta, confirma para baixo e fala
  // land. Sem contar o ofício, sem recovery. Pose no disco
  // não é peso percebido.
  const dir = state.player.dir < 0 ? -1 : 1;
  state.player.squash = CONFIG.feel.squashDash;
  punch(state, CONFIG.feel.punchDashX * dir, 0);
  emit(state, "dash", { x: state.player.x });
  landDash(state);
  return state;
}

// Chuva só da porta. Lê a mesa vigente — cadência e queda — sem
// o RNG da partida, sem entrar em `entities`, e some quando o
// avanço abre o ciclo. A mostra do spawn (intervalo 22, queda
// 1.1) é a chuva de quatro que já estava aqui. Mesa no disco
// não é comparação em movimento.
export function attractTick(state) {
  if (!state || state.phase !== "title") return state;
  recycleEvents(state);
  state.attractTick = (state.attractTick ?? 0) + 1;
  if (state.player) {
    state.player.squash *= CONFIG.feel.squashDecay;
    if (Math.abs(state.player.squash) < 0.01) state.player.squash = 0;
  }
  decayFlash(state);
  // A porta calava. A mostra já caía. `live` é a mesma voz
  // do campo quando a prática acaba. Sem cama. Sem rumble.
  // Ouvir no disco não é mix ouvido.
  if (!state.attractSpoke) {
    state.attractSpoke = true;
    emit(state, "live");
  }
  return state;
}

// A porta também é campo. Sem isto o corpo só andava depois
// do avanço — quem chega no convite sem tabela não ensaiava
// o verbo. Não come o tick, a seed nem a chuva. Andar no
// disco não é peso percebido.
export function attractMove(state, intent) {
  if (!state || state.phase !== "title" || !state.player) return state;
  const move = Number(intent?.move);
  if (!Number.isFinite(move) || move === 0) return state;
  const limit = CONFIG.player.halfWidth;
  state.player.dir = move < 0 ? -1 : 1;
  state.player.x = clamp(
    state.player.x + CONFIG.player.speed * move,
    limit,
    FIELD.width - limit,
  );
  return state;
}

export function attractEntities(state, reduced = false) {
  if (!state || state.phase !== "title") return [];
  const t = reduced ? 0 : (state.attractTick ?? 0);
  const table = rain(state);
  const interval = Number.isFinite(table.intervalTicks) && table.intervalTicks > 0
    ? table.intervalTicks
    : 22;
  const count = Math.max(3, Math.min(6, Math.round((4 * 22) / interval)));
  const base = Number.isFinite(table.fallSpeedMin) && table.fallSpeedMin > 0
    ? table.fallSpeedMin
    : 1.1;
  // O rótulo promete chuva mais lenta. Sem isto a mostra
  // ignorava o knob e só o campo cedia. Assistência no
  // disco não é sessão observada.
  const fall = state.assist ? CONFIG.assist.fallSpeedScale : 1;
  const span = 72 * 3;
  const items = [];
  for (let index = 0; index < count; index += 1) {
    const travel = (t * (base + index * 0.15) * fall + index * 44) % (FIELD.height - 28);
    items.push({
      kind: index % 2 === 0 ? "orb" : "shard",
      x: 48 + (count === 1 ? 0 : index * (span / (count - 1))),
      y: 18 + travel,
    });
  }
  return items;
}

// A mostra atravessava o corpo. Quem andava na porta não via
// a mesa. O contato acende e estreita sem pontuar, sem punch
// e sem comer a seed. Toque no disco não é feel observado.
export function attractTouch(state, reduced = false) {
  if (!state || state.phase !== "title" || !state.player) return state;
  // Reduced já trava o desenho. Sem isto o toque lia a
  // chuva que o canvas some. Quadro no disco não é sessão.
  const rain = attractEntities(state, reduced);
  const player = state.player;
  const pad = CONFIG.collect.pad + (state.assist ? CONFIG.assist.collectPad : 0);
  const reachY = CONFIG.collect.reachY + (state.assist ? CONFIG.assist.collectReachY : 0);
  let kind = "";
  for (let index = 0; index < rain.length; index += 1) {
    const entity = rain[index];
    const reach = CONFIG.player.halfWidth + (entity.kind === "orb" ? pad : CONFIG.hazard.radius);
    const touching =
      Math.abs(entity.y - PLAYER_Y) < reachY && Math.abs(entity.x - player.x) < reach;
    if (!touching) continue;
    kind = entity.kind;
    break;
  }
  if (kind && kind !== state.attractTouch) {
    state.attractTouch = kind;
    state.flash = Math.max(
      state.flash,
      kind === "shard" ? CONFIG.feel.flashGraze : CONFIG.feel.flashMissed,
    );
    player.squash = kind === "shard" ? CONFIG.feel.squashGraze : CONFIG.feel.squashCollect;
  } else if (!kind) {
    state.attractTouch = "";
  }
  return state;
}

export function neutralIntent() {
  return { move: 0, dash: false, bank: false };
}

export function remainingTicks(state, config = CONFIG) {
  return Math.max(0, config.runTicks - state.tick);
}

export function closingWindow(state, config = CONFIG) {
  if (!state || state.phase !== "playing") return false;
  const left = remainingTicks(state, config);
  return left > 0 && left <= config.feel.closeTicks;
}

export function closingPulse(state, config = CONFIG) {
  if (!closingWindow(state, config)) return { active: false, fill: 0, beat: 0 };
  const left = remainingTicks(state, config);
  const fill = 1 - (left - 1) / config.feel.closeTicks;
  const beat = 1 - (left % TICK_HZ) / TICK_HZ;
  return {
    active: true,
    fill: Math.max(0, Math.min(1, fill)),
    beat: Math.max(0, Math.min(1, beat)),
  };
}

export function bedRateFor(state, config = CONFIG) {
  const pulse = closingPulse(state, config);
  if (!pulse.active) return 1;
  const top = Number(config.feel.closeBedRate);
  if (!(Number.isFinite(top) && top > 0)) return 1;
  return 1 + pulse.fill * (top - 1);
}

export function practicingWindow(state) {
  if (!state || state.phase !== "playing") return false;
  const ticks = rain(state).practiceTicks;
  return Number.isFinite(ticks) && ticks > 0 && state.tick < ticks;
}

export function practicePulse(state) {
  if (!practicingWindow(state)) return { active: false, fill: 0 };
  const total = rain(state).practiceTicks;
  return {
    active: true,
    fill: Math.max(0, Math.min(1, (total - state.tick) / total)),
  };
}

export function recoveringWindow(state) {
  if (!state || state.phase !== "playing") return false;
  return Number.isFinite(state.recoverUntil) && state.tick < state.recoverUntil;
}

export function recoveryPulse(state) {
  if (!recoveringWindow(state)) return { active: false, fill: 0 };
  const total = Math.max(1, rain(state).recoveryTicks);
  return {
    active: true,
    fill: Math.max(0, Math.min(1, (state.recoverUntil - state.tick) / total)),
  };
}

function markClose(state) {
  const left = remainingTicks(state);
  if (left <= 0 || left > CONFIG.feel.closeTicks) return;
  if (left % TICK_HZ !== 0) return;
  state.flash = Math.max(state.flash, CONFIG.feel.flashClose);
  emit(state, "close");
}

function markPractice(state) {
  const ticks = rain(state).practiceTicks;
  if (!Number.isFinite(ticks) || state.tick !== ticks) return;
  state.flash = Math.max(state.flash, CONFIG.feel.flashPractice);
  emit(state, "live");
}

function markRecovery(state) {
  if (state.phase !== "playing") return;
  const until = state.recoverUntil;
  if (!Number.isFinite(until) || until <= 0 || state.tick !== until) return;
  state.flash = Math.max(state.flash, CONFIG.feel.flashStir);
  emit(state, "stir");
}

function markMissed(state) {
  if (!state.events.some((event) => event.type === "missed")) return;
  state.flash = Math.max(state.flash, CONFIG.feel.flashMissed);
}

function dropMiss(state, x) {
  const life = CONFIG.feel.moteLife;
  const count = CONFIG.feel.moteMissed;
  const y = FIELD.height - 3;
  for (let index = 0; index < count; index += 1) {
    const unit = count === 1 ? 0 : index / (count - 1) - 0.5;
    state.motes.push(acquireMote("missed", x + unit * 6, y, unit * 0.35, 0.25, life));
  }
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
    markClose(state);
    markPractice(state);
    markRecovery(state);
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
    state.bankLock === 0 &&
    (state.bankWindup ?? 0) === 0;
  if ((player.dashWindup ?? 0) > 0) {
    player.dashWindup -= 1;
    player.squash = CONFIG.feel.squashCoil;
    if (player.dashWindup === 0 && canDash) fireDash(state, intent);
  } else if (canDash && player.dashBuffer > 0) {
    player.dashWindup = CONFIG.player.dashWindupTicks;
    player.dashBuffer = 0;
    player.squash = CONFIG.feel.squashCoil;
  }

  if ((state.bankWindup ?? 0) > 0) {
    state.bankWindup -= 1;
    player.squash = CONFIG.feel.squashBankCoil;
    if (state.bankWindup === 0) commitBank(state);
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
  markClose(state);
  markPractice(state);
  markRecovery(state);
  markMissed(state);
  decayCamera(state);
  player.squash *= CONFIG.feel.squashDecay;
  if (Math.abs(player.squash) < 0.01) player.squash = 0;

  if (state.tick >= CONFIG.runTicks) {
    state.phase = "over";
    player.squash = CONFIG.feel.squashOver;
    // O corpo já sentava. Tremor e punch do último verbo
    // ficavam no quadro. O relógio senta o campo com o tijolo.
    // Pose no disco não é peso percebido.
    state.shake = 0;
    state.flash = 0;
    if (state.camera) {
      state.camera.x = 0;
      state.camera.y = 0;
    }
    emit(state, "over", { score: state.score, unbanked: state.chain });
    lapseChain(state, state.chain);
  }
  decayMotes(state);
  return state;
}

function fireDash(state, intent) {
  const player = state.player;
  player.dashTicks = CONFIG.player.dashTicks;
  player.dashWindup = 0;
  player.dashBuffer = 0;
  player.squash = CONFIG.feel.squashDash;
  if (intent.move !== 0) player.dir = intent.move;
  punch(state, CONFIG.feel.punchDashX * player.dir, 0);
  emit(state, "dash", { x: player.x });
  state.stats.dashes += 1;
}

function advanceDashPhases(state) {
  const player = state.player;
  if (player.dashTicks > 0) {
    player.dashTicks -= 1;
    if (player.dashTicks === 0) {
      player.dashRecovery = CONFIG.player.dashRecoveryTicks;
      landDash(state);
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

function commitBank(state) {
  if (state.bankLock > 0 || state.chain === 0) return;
  const chain = state.chain;
  const gain = chain * chain;
  state.score += gain;
  state.stats.banked += gain;
  state.stats.banks += 1;
  depositChain(state, chain);
  state.chain = 0;
  state.bankBuffer = 0;
  state.bankWindup = 0;
  state.bankLock = CONFIG.bank.lockTicks;
  state.hitstop = CONFIG.feel.bankHitstopTicks;
  state.shake += CONFIG.feel.bankShake;
  state.player.squash = CONFIG.feel.squashBank;
  punch(state, 0, CONFIG.feel.punchBankY);
  state.recoverUntil = state.tick + rain(state).recoveryTicks;
  emit(state, "bank", { chain, gain });
}

function bank(state, intent) {
  const requested = state.bankBuffer > 0 || Boolean(intent?.bank);
  if (!requested || state.bankLock > 0 || state.chain === 0) return;
  if ((state.bankWindup ?? 0) > 0) return;
  // Coleta neste tick já foi a antecipação: o pedido do mesmo quadro
  // converte na hora. Corrente que já existia senta antes de virar
  // pontuação — e esses ticks já atravessam. Pose no disco não é
  // peso percebido.
  if (state.events.some((event) => event.type === "collect")) {
    commitBank(state);
    return;
  }
  // Corrente que já existia espera o coil do avanço. Os dois
  // arcos no mesmo tick travavam o disparo: canDash lê
  // bankWindup e o avanço expirava sem alongar. Coleta neste
  // quadro já converteu acima. Pedido no disco não é felt.
  if ((state.player?.dashWindup ?? 0) > 0) return;
  const windup = CONFIG.bank.windupTicks;
  if (!(windup > 0)) {
    commitBank(state);
    return;
  }
  state.bankWindup = windup;
  state.player.squash = CONFIG.feel.squashBankCoil;
}

export function spawnIntervalScale(state, table = rain(state)) {
  let scale = 1;
  if (state.tick < state.recoverUntil) {
    const recovery = Number(table.recoveryIntervalScale);
    if (Number.isFinite(recovery) && recovery > 0) scale *= recovery;
  }
  if (closingWindow(state)) {
    const close = Number(table.closeIntervalScale);
    if (Number.isFinite(close) && close > 0) scale *= close;
  }
  return scale;
}

export function spawnHazardChance(state, table = rain(state)) {
  if (state.tick < table.practiceTicks) return 0;
  const progress = Math.min(1, state.tick / table.rampTicks);
  let chance = lerp(table.hazardChanceStart, table.hazardChanceEnd, progress);
  if (closingWindow(state)) {
    const close = Number(table.closeHazardScale);
    if (Number.isFinite(close) && close > 0) chance *= close;
  }
  if (!(chance > 0)) return 0;
  return Math.min(0.95, chance);
}

function spawn(state) {
  const table = rain(state);
  state.spawnTimer -= 1;
  if (state.spawnTimer > 0) return;
  const progress = Math.min(1, state.tick / table.rampTicks);
  const scale = spawnIntervalScale(state, table);
  state.spawnTimer = Math.round(
    lerp(table.intervalTicks, table.minIntervalTicks, progress) * scale,
  );
  if (state.spawnTimer < 1) state.spawnTimer = 1;
  const rng = bindSpawnRng(state.seed, state.rngState);
  const hazardChance = spawnHazardChance(state, table);
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
  // O coil e o arco da guarda já são o compromisso. Sem isto, os
  // dois ticks de antecipação eram janela de hit — o jogador sentou
  // e morreu, ou sentou para guardar e perdeu a corrente. Pose no
  // disco não é peso percebido.
  // Coil, arco e land já atravessam. A graça pós-dano também
  // já existe — hit() a concede neste quadro. Sem reler
  // invuln a cada entidade, o segundo estilhaço ainda
  // acertava. Pose no disco não é peso percebido.
  const committed =
    player.dashTicks > 0 ||
    (player.dashWindup ?? 0) > 0 ||
    (state.bankWindup ?? 0) > 0 ||
    // O arco já atravessava. Sem isto o quadro que
    // converte — e o quadro do land, dashTicks já em 0 —
    // era janela de hit. A recuperação depois do land
    // continua vulnerável. Pose no disco não é peso.
    state.events.some((event) => event.type === "bank" || event.type === "land");
  const entities = state.entities;
  const pad = CONFIG.collect.pad + (state.assist ? CONFIG.assist.collectPad : 0);
  const reachY = CONFIG.collect.reachY + (state.assist ? CONFIG.assist.collectReachY : 0);
  const touches = (entity) => {
    const reach =
      CONFIG.player.halfWidth +
      (entity.kind === "orb" ? pad : CONFIG.hazard.radius);
    return Math.abs(entity.y - PLAYER_Y) < reachY && Math.abs(entity.x - player.x) < reach;
  };
  for (let index = 0; index < entities.length; index += 1) {
    entities[index].y += entities[index].vy;
  }
  // Estilhaço letal neste tick: o orbe espera. Ordem do
  // array não decide a aposta. Graça e dash atravessam os
  // dois. Pose no disco não é peso percebido.
  const shardHits =
    !committed &&
    !(player.invuln > 0) &&
    entities.some((entity) => entity.kind === "shard" && touches(entity));
  let write = 0;
  for (let index = 0; index < entities.length; index += 1) {
    const entity = entities[index];
    if (touches(entity)) {
      if (entity.kind === "orb") {
        // Um verbo, um tick. O primeiro collect já emitiu;
        // o segundo orbe fica para o próximo quadro. Dois
        // no alcance não inflam a corrente. Estilhaço letal
        // no mesmo quadro também manda o orbe esperar.
        // Pose no disco não é peso percebido.
        if (shardHits || state.events.some((event) => event.type === "collect")) {
          entities[write] = entity;
          write += 1;
          continue;
        }
        // O arco já escolheu a aposta. Sem isto o orbe que
        // caía no sit inflamava a corrente e o commit
        // convertia o que você não pediu. Coleta e guarda
        // no mesmo quadro (sem arco) continuam na hora.
        // Pose no disco não é peso percebido.
        if ((state.bankWindup ?? 0) > 0) {
          entities[write] = entity;
          write += 1;
          continue;
        }
        collect(state, entity.x, entity.y);
        releaseEntity(entity);
        continue;
      }
      if (committed || player.invuln > 0) {
        grazeContact(state);
        emit(state, "graze", { x: entity.x });
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
        emit(state, "missed", { x: entity.x });
        dropMiss(state, entity.x);
        state.shake += CONFIG.feel.missedShake;
        state.player.squash = CONFIG.feel.squashMiss;
        punch(state, 0, CONFIG.feel.punchMissedY);
      }
      releaseEntity(entity);
      continue;
    }
    entities[write] = entity;
    write += 1;
  }
  entities.length = write;
}

function grazeContact(state) {
  const dir = state.player.dir < 0 ? -1 : 1;
  state.shake += CONFIG.feel.grazeShake;
  state.flash = Math.max(state.flash, CONFIG.feel.flashGraze);
  state.player.squash = CONFIG.feel.squashGraze;
  punch(state, CONFIG.feel.punchGrazeX * dir, 0);
}

function collect(state, fromX, fromY) {
  const before = chainPipCount(state.chain);
  state.chain += 1;
  state.stats.collected += 1;
  if (state.chain > state.stats.bestChain) state.stats.bestChain = state.chain;
  state.hitstop = CONFIG.feel.collectHitstopTicks;
  state.shake += CONFIG.feel.collectShake;
  state.player.squash = CONFIG.feel.squashCollect;
  punch(state, 0, CONFIG.feel.punchCollectY);
  joinChain(state, before, fromX, fromY);
  emit(state, "collect", { chain: state.chain, x: fromX });
}

function joinChain(state, before, fromX, fromY) {
  const after = chainPipCount(state.chain);
  if (after <= before) return;
  const life = CONFIG.feel.moteLife;
  const x = Number.isFinite(fromX) ? fromX : state.player.x;
  const y = Number.isFinite(fromY) ? fromY : PLAYER_Y;
  const tick = Number.isFinite(state.tick) ? state.tick : 0;
  const dest = chainPipAt(after - 1, after, state.player.x, PLAYER_Y, tick, false);
  state.motes.push(acquireMote(
    "join",
    x,
    y,
    (dest.x - x) / life,
    (dest.y - y) / life,
    life,
  ));
}

function shatterChain(state, lost) {
  const count = chainPipCount(lost);
  if (count <= 0) return;
  const life = CONFIG.feel.moteLife;
  const x = state.player.x;
  const y = PLAYER_Y;
  const tick = Number.isFinite(state.tick) ? state.tick : 0;
  for (let index = 0; index < count; index += 1) {
    const pip = chainPipAt(index, count, x, y, tick, false);
    const angle = tick * CONFIG.feel.chainSpin + (index * Math.PI * 2) / count;
    state.motes.push(acquireMote("break", pip.x, pip.y, Math.cos(angle) * 1.8, Math.sin(angle) * 1.8, life));
  }
}

function lapseChain(state, lost) {
  const count = chainPipCount(lost);
  if (count <= 0) return;
  const life = CONFIG.feel.moteLife;
  const x = state.player.x;
  const y = PLAYER_Y;
  const tick = Number.isFinite(state.tick) ? state.tick : 0;
  const fall = CONFIG.feel.lapseFall;
  for (let index = 0; index < count; index += 1) {
    const pip = chainPipAt(index, count, x, y, tick, false);
    state.motes.push(acquireMote("lapse", pip.x, pip.y, 0, fall, life));
  }
}

function depositChain(state, committed) {
  const count = chainPipCount(committed);
  if (count <= 0) return;
  const life = CONFIG.feel.moteLife;
  const x = state.player.x;
  const y = PLAYER_Y;
  const tick = Number.isFinite(state.tick) ? state.tick : 0;
  const aimX = CONFIG.feel.depositAimX;
  const aimY = CONFIG.feel.depositAimY;
  for (let index = 0; index < count; index += 1) {
    const pip = chainPipAt(index, count, x, y, tick, false);
    state.motes.push(acquireMote(
      "deposit",
      pip.x,
      pip.y,
      (aimX - pip.x) / life,
      (aimY - pip.y) / life,
      life,
    ));
  }
}

function hit(state) {
  const lost = state.chain;
  shatterChain(state, lost);
  state.chain = 0;
  state.bankBuffer = 0;
  state.bankWindup = 0;
  state.stats.hits += 1;
  state.player.invuln = CONFIG.player.invulnTicks + (state.assist ? CONFIG.assist.extraInvulnTicks : 0);
  state.hitstop = CONFIG.feel.hitHitstopTicks;
  state.shake += CONFIG.feel.hitShake;
  state.flash = CONFIG.feel.flashHit;
  state.player.squash = CONFIG.feel.squashHit;
  punch(state, 0, CONFIG.feel.punchHitY);
  emit(state, "hit", { lost, x: state.player.x });
}

export function lookAhead(state, reduced = false) {
  // O trilho já marca. Sem isto a câmera só confirma o
  // impacto e some a antecipação. Lean no disco não é felt.
  if (reduced || !state || !state.player || state.phase !== "playing") {
    return { x: 0, y: 0 };
  }
  const near = approaching(state, reduced);
  if (!near.length) return { x: 0, y: 0 };
  const band = CONFIG.collect.reachY;
  const span = CONFIG.feel.telegraphReach - band;
  let best = near[0];
  let bestGap = PLAYER_Y - best.y;
  for (let index = 1; index < near.length; index += 1) {
    const gap = PLAYER_Y - near[index].y;
    if (gap < bestGap) {
      best = near[index];
      bestGap = gap;
    }
  }
  const max = CONFIG.feel.lookAheadX;
  const t = span > 0
    ? Math.max(0, Math.min(1, 1 - (bestGap - band) / span))
    : 1;
  const raw = ((best.x - state.player.x) / 80) * max * (0.4 + 0.6 * t);
  const x = clamp(raw, -max, max);
  if (Math.abs(x) < 0.01) return { x: 0, y: 0 };
  return { x, y: 0 };
}

export function approaching(state, reduced = false) {
  // A porta chove sem `entities`. Sem isto o trilho só
  // falava no campo e a mostra — que o live já nomeia —
  // caía muda. Reduced trava a queda; o aviso segue a
  // chuva visível. Marca no disco não é felt.
  const reach = CONFIG.feel.telegraphReach;
  const band = CONFIG.collect.reachY;
  const list = !state
    ? []
    : state.phase === "title"
      ? attractEntities(state, reduced)
      : (state.entities ?? []);
  let write = 0;
  for (let index = 0; index < list.length; index += 1) {
    const entity = list[index];
    if (!entity) continue;
    const gap = PLAYER_Y - entity.y;
    if (gap > band && gap <= reach) {
      approachingScratch[write] = entity;
      write += 1;
    }
  }
  approachingScratch.length = write;
  return approachingScratch;
}

// Estilhaço no alcance do telegraph e no x do corpo. Não reusa o
// scratch de `approaching`. Texto no DOM não é sessão de alcance.
export function threatCue(state, reduced = false) {
  if (!state || !state.player) return null;
  if (state.phase !== "playing" && state.phase !== "title") return null;
  // Na porta o live nomeia o mesmo trilho que o canvas
  // marca. Reduced trava os dois. Texto no DOM não é sessão.
  const list = state.phase === "title" ? attractEntities(state, reduced) : state.entities;
  if (!Array.isArray(list)) return null;
  const reach = CONFIG.feel.telegraphReach;
  const band = CONFIG.collect.reachY;
  const px = state.player.x;
  const half = CONFIG.player.halfWidth + CONFIG.hazard.radius;
  for (let index = 0; index < list.length; index += 1) {
    const entity = list[index];
    if (!entity || entity.kind !== "shard") continue;
    const gap = PLAYER_Y - entity.y;
    if (gap <= band || gap > reach) continue;
    if (Math.abs(entity.x - px) <= half) return "ahead";
  }
  return null;
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
