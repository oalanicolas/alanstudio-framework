// Mesas de conteúdo. A regra e a apresentação consomem; não embutem.
//
// Uma mesa nova entra pelo comando: `npm run table -- <nome>`. Ele
// escreve o JSON com schema e registra o nome abaixo. Alterar um JSON
// não republica o verbo. Sem consumidor a mesa existe e o jogo não muda.
//
// Perfil de chuva é o consumidor que já existe: `dusk`, `calm` e qualquer
// mesa com a forma de spawn entram por `?spawn=<nome>` ou settings.spawnProfile.
// `npm run table -- <nome> --from spawn|dusk|calm` copia essa forma; `--as`
// aplica uma intenção nomeada e deixa a chuva distinta. `copy.fantasy`
// tem consumidor: a abertura e o coach do primeiro ciclo
// quando a porta ainda não deu a frase.
// `title_play`, `title_again` e `title_new` nomeiam a porta.
// `title_volatile` e `title_unsaved` nomeiam sessão que não
// grava e gravação que não ficou. `settings_recovered` nomeia
// preferências ilegíveis no painel, no live e no canvas da porta e do fim. Nomear não é `trusted`.
// `resume` e `restart` nomeiam a pausa — R já saía e a
// placa calava. `hint_bank` reserva o lugar da tecla viva — o fecho com corrente
// viva reusa essa linha; `hint_dash` ensina o
// avanço nas três superfícies quando o estilhaço marca o trilho;
// `hint_touch` e `hint_pad` são o passo da superfície que falou;
// `hint_miss` nomeia a queda quando a corrente ainda é zero.
// `hint_hit` nomeia o estilhaço quando a corrente voltou a zero.
// `hint_practice` nomeia a janela orbe-só enquanto o campo a
// contorna. Depois da prática o aviso volta a pedir o orbe.
// Overlay e HUD confirmam o aparelho que falou por último.
// `palettes` tem consumidor: o desenho lê
// `PALETTES` daqui, não uma constante no render. `look` escolhe um
// look de arte (`normal`, `dusk`, `calm`); `contrast` e a tinta estável
// (`colorblind`) são alcance, não look. A tinta não esmaga chuva que
// já separa quente e frio; o par do padrão é o fallback. `npm run look -- <nome> --from normal|dusk|calm` copia um
// look que o jogo já consome; `--as` desloca campo e orbe — estilhaço
// e perigo permanecem. `dusk` e `calm` na chuva e no look compartilham
// o nome e não a mesa. `?mood=<nome>` aplica o par quando o nome é
// look e chuva; look ou chuva explícitos vencem no próprio eixo.
// `npm run pair -- <nome> --from dusk|calm` nasce os dois no mesmo
// nome. A página nomeia o mesmo par no select; um controle no disco não
// é alguém de fora.
// Mesas genéricas continuam sem consumidor automático.
//
// Toda mesa tem schema: formato antigo (sem campo) vira o vigente;
// schema futuro falha com o número, não com undefined no meio do tick.
// Spawn 2 acrescenta prática e recuperação; ausentes ganham o padrão.
// Spawn 3 acrescenta o fecho (`closeIntervalScale`); ausente fica 1.
// Spawn 4 acrescenta o risco do fecho (`closeHazardScale`); ausente fica 1.
// Copy 3 acrescenta `hint_hit`; ausente ganha o padrão.
// Copy 4 acrescenta `hint_practice`; ausente ganha o padrão.

import spawnRaw from "../../data/spawn.json" with { type: "json" };
import copyRaw from "../../data/copy.json" with { type: "json" };
import duskRaw from "../../data/dusk.json" with { type: "json" };
import calmRaw from "../../data/calm.json" with { type: "json" };
import palettesRaw from "../../data/palettes.json" with { type: "json" };

export const SPAWN_SCHEMA = 4;
export const COPY_SCHEMA = 3;
export const PALETTE_SCHEMA = 1;
export const SPAWN_FIELDS = [
  "intervalTicks",
  "minIntervalTicks",
  "rampTicks",
  "hazardChanceStart",
  "hazardChanceEnd",
  "fallSpeedMin",
  "fallSpeedMax",
  "practiceTicks",
  "recoveryTicks",
  "recoveryIntervalScale",
  "closeIntervalScale",
  "closeHazardScale",
];
export const SPAWN_CORE_FIELDS = [
  "intervalTicks",
  "minIntervalTicks",
  "rampTicks",
  "hazardChanceStart",
  "hazardChanceEnd",
  "fallSpeedMin",
  "fallSpeedMax",
];

// Intenções sobre uma chuva já jogável. Não são chuva melhor — só
// deslocam os knobs que a receita já nomeia. Quem de fora ainda não
// produziu; `enough` continua falso.
export const SPAWN_INTENTS = {
  denser: "intervalo menor, mais risco, prática mais curta",
  calmer: "intervalo maior, menos risco, prática mais longa",
  brief: "prática e rampa mais curtas",
};

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
const scaleInt = (value, factor, min) => Math.max(min, Math.round(value * factor));

export function listSpawnIntents() {
  return Object.keys(SPAWN_INTENTS);
}

export function spawnRecord(table) {
  const record = { schema: SPAWN_SCHEMA };
  for (const field of SPAWN_FIELDS) record[field] = table[field];
  return record;
}

export function applySpawnIntent(table, intent) {
  if (!(intent in SPAWN_INTENTS)) {
    throw new Error(`intenção desconhecida: ${intent}`);
  }
  const next = spawnRecord(table);
  if (intent === "denser") {
    next.intervalTicks = scaleInt(next.intervalTicks, 0.75, 8);
    next.minIntervalTicks = scaleInt(next.minIntervalTicks, 0.75, 4);
    next.hazardChanceStart = clamp(next.hazardChanceStart + 0.08, 0, 0.9);
    next.hazardChanceEnd = clamp(next.hazardChanceEnd + 0.08, 0, 0.95);
    next.practiceTicks = scaleInt(next.practiceTicks, 0.5, 30);
    next.fallSpeedMin = clamp(next.fallSpeedMin + 0.15, 0.4, 4);
    next.fallSpeedMax = clamp(next.fallSpeedMax + 0.25, next.fallSpeedMin, 5);
    next.closeIntervalScale = clamp((next.closeIntervalScale ?? 1) * 0.85, 0.35, 1);
    next.closeHazardScale = clamp((next.closeHazardScale ?? 1) * 1.12, 1, 1.7);
  } else if (intent === "calmer") {
    next.intervalTicks = scaleInt(next.intervalTicks, 1.25, 8);
    next.minIntervalTicks = scaleInt(next.minIntervalTicks, 1.25, 4);
    next.hazardChanceStart = clamp(next.hazardChanceStart - 0.08, 0, 0.9);
    next.hazardChanceEnd = clamp(next.hazardChanceEnd - 0.08, 0, 0.95);
    next.practiceTicks = scaleInt(next.practiceTicks, 1.5, 30);
    next.fallSpeedMin = clamp(next.fallSpeedMin - 0.15, 0.4, 4);
    next.fallSpeedMax = clamp(next.fallSpeedMax - 0.2, next.fallSpeedMin, 5);
    next.closeIntervalScale = clamp((next.closeIntervalScale ?? 1) * 1.12, 0.35, 1.25);
    next.closeHazardScale = clamp((next.closeHazardScale ?? 1) * 0.88, 0.8, 1.4);
  } else {
    next.practiceTicks = scaleInt(next.practiceTicks, 0.4, 30);
    next.recoveryTicks = scaleInt(next.recoveryTicks, 0.7, 20);
    next.rampTicks = scaleInt(next.rampTicks, 0.6, 120);
  }
  if (next.minIntervalTicks > next.intervalTicks) next.minIntervalTicks = next.intervalTicks;
  if (next.hazardChanceStart > next.hazardChanceEnd) {
    next.hazardChanceStart = next.hazardChanceEnd;
  }
  return next;
}
export const COPY_FIELDS = [
  "fantasy",
  "paused",
  "resume",
  "over",
  "restart",
  "restart_inline",
  "best_chain",
  "chain",
  "score",
  "record",
  "dash_ready",
  "dash_recharging",
  "hint_move",
  "hint_dash",
  "hint_touch",
  "hint_pad",
  "hint_collect",
  "hint_practice",
  "hint_miss",
  "hint_hit",
  "hint_bank",
  "title_play",
  "title_again",
  "title_new",
  "title_last",
  "title_volatile",
  "title_unsaved",
  "over_door",
  "over_door_inline",
];

export function migrateTable(name, raw, schema, fields = []) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
    throw new Error(`mesa ${name} ilegível`);
  }
  const current = Number.isInteger(raw.schema) ? raw.schema : 0;
  if (current > schema) {
    throw new Error(`mesa ${name} schema ${current} não suportado (máximo ${schema})`);
  }
  const table = { ...raw, schema };
  if (fields.length) {
    const missing = fields.filter((field) => table[field] === undefined);
    if (missing.length) {
      throw new Error(`mesa ${name} sem ${missing.join(", ")}`);
    }
  }
  return table;
}

export function migrateSpawn(raw, name = "spawn") {
  const table = migrateTable(name, raw, SPAWN_SCHEMA);
  return {
    ...table,
    schema: SPAWN_SCHEMA,
    practiceTicks: Number.isInteger(table.practiceTicks) ? table.practiceTicks : 240,
    recoveryTicks: Number.isInteger(table.recoveryTicks) ? table.recoveryTicks : 90,
    recoveryIntervalScale: Number.isFinite(table.recoveryIntervalScale)
      ? table.recoveryIntervalScale
      : 1.6,
    closeIntervalScale: Number.isFinite(table.closeIntervalScale) && table.closeIntervalScale > 0
      ? table.closeIntervalScale
      : 1,
    closeHazardScale: Number.isFinite(table.closeHazardScale) && table.closeHazardScale > 0
      ? table.closeHazardScale
      : 1,
  };
}

export function looksLikeSpawn(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return false;
  return SPAWN_CORE_FIELDS.every((field) => raw[field] !== undefined);
}

export function migrateCopy(raw) {
  const table = migrateTable("copy", raw, COPY_SCHEMA);
  return {
    ...table,
    schema: COPY_SCHEMA,
    fantasy: typeof table.fantasy === "string" ? table.fantasy : "",
    title_play: typeof table.title_play === "string" ? table.title_play : "Jogar: {dash}",
    title_again: typeof table.title_again === "string" ? table.title_again : "Repetir a última: {dash}",
    title_new: typeof table.title_new === "string" ? table.title_new : "Nova partida: {reset}",
    title_last: typeof table.title_last === "string" ? table.title_last : "Última",
    title_volatile: typeof table.title_volatile === "string" ? table.title_volatile : "Esta sessão não grava",
    title_unsaved: typeof table.title_unsaved === "string" ? table.title_unsaved : "A última gravação não ficou",
    settings_recovered:
      typeof table.settings_recovered === "string"
        ? table.settings_recovered
        : "As preferências voltaram ao padrão; o arquivo ilegível ficou em settings.broken",
    over_door: typeof table.over_door === "string" ? table.over_door : "Abertura: {dash}",
    over_door_inline: typeof table.over_door_inline === "string" ? table.over_door_inline : "abertura: {dash}",
    hint_hit: typeof table.hint_hit === "string" ? table.hint_hit : "O estilhaço come a corrente viva — atravesse ou guarde",
    hint_practice:
      typeof table.hint_practice === "string"
        ? table.hint_practice
        : "Só orbes — a borda some quando a ameaça começa",
  };
}

export const PALETTE_FIELDS = [
  "background",
  "field",
  "player",
  "orb",
  "shard",
  "chain",
  "text",
  "muted",
  "danger",
  "plate",
  "plateEdge",
];

export const PALETTE_REQUIRED = ["normal", "contrast"];

export function migratePalettes(raw) {
  const table = migrateTable("palettes", raw, PALETTE_SCHEMA);
  const pack = table.palettes;
  if (!pack || typeof pack !== "object" || Array.isArray(pack)) {
    throw new Error("mesa palettes sem palettes");
  }
  for (const name of PALETTE_REQUIRED) {
    if (pack[name] === undefined) {
      throw new Error(`mesa palettes sem ${name}`);
    }
  }
  for (const name of Object.keys(pack)) {
    const entry = pack[name];
    if (!entry || typeof entry !== "object" || Array.isArray(entry)) {
      throw new Error(`mesa palettes.${name} ilegível`);
    }
    const missing = PALETTE_FIELDS.filter((field) => entry[field] === undefined);
    if (missing.length) {
      throw new Error(`mesa palettes.${name} sem ${missing.join(", ")}`);
    }
  }
  return { schema: PALETTE_SCHEMA, palettes: pack };
}

const spawn = migrateSpawn(spawnRaw);
const copy = migrateCopy(copyRaw);
const dusk = migrateSpawn(duskRaw, "dusk");
const calm = migrateSpawn(calmRaw, "calm");
const palettes = migratePalettes(palettesRaw);
export const PALETTES = palettes.palettes;

const TABLES = { spawn, copy, dusk, calm, palettes };

export function loadTable(name) {
  if (!(name in TABLES)) {
    throw new Error(`mesa desconhecida: ${name}`);
  }
  return TABLES[name];
}

export function requireFields(name, fields) {
  const table = loadTable(name);
  const missing = fields.filter((field) => table[field] === undefined);
  if (missing.length) {
    throw new Error(`mesa ${name} sem ${missing.join(", ")}`);
  }
  return table;
}

export function listLooks() {
  return Object.keys(PALETTES)
    .filter((name) => name !== "contrast")
    .sort();
}

export function listMoods() {
  const looks = new Set(listLooks());
  return listSpawnProfiles().filter((name) => looks.has(name));
}

export function resolveMoodName(name) {
  const moods = listMoods();
  return moods.includes(name) ? name : moods[0] ?? "";
}

export const LOOK_LABELS = {
  normal: "Padrão",
  dusk: "Crepúsculo",
  calm: "Calma",
};

export const SPAWN_LABELS = {
  spawn: "Padrão",
  dusk: "Crepúsculo",
  calm: "Calma",
};

export function pairPatch(name) {
  return resolveMoodName(name) === name ? { look: name, spawnProfile: name } : null;
}

export function matchingMood(look, spawn) {
  return look === spawn && resolveMoodName(look) === look ? look : "";
}

export function resolveLookName(name) {
  if (typeof name === "string" && name !== "contrast" && name in PALETTES) {
    return name;
  }
  return "normal";
}

// Orbe azul e estilhaço laranja do look padrão. Não é look: o campo
// permanece. Fallback para chuva que ainda compartilha o eixo —
// os dois quentes ou os dois frios. dusk âmbar/índigo e calm
// teal/coral já separam; esmagar pelo par do padrão era a mesma
// chuva com campo alheio. Alto contraste continua vencendo.
// Chave no disco não é sessão. JSON no disco não é comparação
// em movimento.
export const COLORBLIND_INKS = {
  orb: PALETTES.normal.orb,
  shard: PALETTES.normal.shard,
  chain: PALETTES.normal.chain,
  danger: PALETTES.normal.danger,
};

function inkChannels(hex) {
  const raw = typeof hex === "string" && hex.startsWith("#") && hex.length === 7
    ? hex.slice(1)
    : "";
  if (!raw) return null;
  const value = Number.parseInt(raw, 16);
  if (!Number.isFinite(value)) return null;
  return { r: (value >> 16) & 255, g: (value >> 8) & 255, b: value & 255 };
}

// Quente (R > B) contra frio (B > R). Mesmo eixo não distingue
// orbe de estilhaço para quem lê só a temperatura. Hex no disco
// não é sessão no aparelho.
export function rainSplitsWarmCool(look = {}) {
  const orb = inkChannels(look.orb);
  const shard = inkChannels(look.shard);
  if (!orb || !shard || look.orb === look.shard) return false;
  return (orb.r > orb.b) !== (shard.r > shard.b);
}

export function applyColorblindInks(look = {}) {
  if (rainSplitsWarmCool(look)) return look;
  return { ...look, ...COLORBLIND_INKS };
}

export function dressPalette(settings = {}) {
  if (settings.highContrast) return PALETTES.contrast;
  const look = PALETTES[resolveLookName(settings.look)] ?? PALETTES.normal;
  if (!settings.colorblind) return look;
  return applyColorblindInks(look);
}

// Intenções sobre um look já pintável. Não são look melhor — só
// deslocam os tokens que a receita já nomeia. Estilhaço e perigo
// ficam: o fecho e o impacto não herdam o eixo do orbe. Quem de
// fora ainda não produziu; `consistent` continua falso.
export const LOOK_INTENTS = {
  warmer: "campo e orbe andam para o âmbar; o estilhaço e o perigo permanecem",
  cooler: "campo e orbe andam para o azul; o estilhaço e o perigo permanecem",
  night: "campo mais escuro, acentos no mesmo lugar; o perigo permanece",
};

export function listLookIntents() {
  return Object.keys(LOOK_INTENTS);
}

export function lookRecord(palette) {
  const record = {};
  for (const field of PALETTE_FIELDS) record[field] = palette[field];
  return record;
}

export function applyLookIntent(palette, intent) {
  if (!(intent in LOOK_INTENTS)) {
    throw new Error(`intenção desconhecida: ${intent}`);
  }
  const next = lookRecord(palette);
  if (intent === "warmer") {
    next.background = mixTint(next.background, "#2a1810", 0.4);
    next.field = mixTint(next.field, "#3a2418", 0.45);
    next.orb = mixTint(next.orb, "#ffb35a", 0.5);
    next.chain = mixTint(next.chain, "#f0c36a", 0.4);
    next.muted = mixTint(next.muted, "#a89080", 0.35);
    next.plate = mixTint(next.plate, "#120a08", 0.3);
  } else if (intent === "cooler") {
    next.background = mixTint(next.background, "#0c1220", 0.4);
    next.field = mixTint(next.field, "#121828", 0.45);
    next.orb = mixTint(next.orb, "#5ec8ff", 0.45);
    next.chain = mixTint(next.chain, "#8ad4ff", 0.35);
    next.muted = mixTint(next.muted, "#7a88a0", 0.35);
    next.plate = mixTint(next.plate, "#070913", 0.3);
  } else {
    next.background = scaleTint(next.background, 0.55);
    next.field = scaleTint(next.field, 0.5);
    next.plate = scaleTint(next.plate, 0.7);
    next.muted = scaleTint(next.muted, 0.85);
  }
  return next;
}

function parseTint(value) {
  if (typeof value !== "string") return null;
  const hex = /^#([0-9a-f]{6})$/i.exec(value);
  if (hex) {
    const n = Number.parseInt(hex[1], 16);
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: 1, kind: "hex" };
  }
  const rgba = /^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([0-9.]+)\s*)?\)$/i.exec(value);
  if (!rgba) return null;
  return {
    r: Number(rgba[1]),
    g: Number(rgba[2]),
    b: Number(rgba[3]),
    a: rgba[4] === undefined ? 1 : Number(rgba[4]),
    kind: "rgba",
  };
}

function formatTint(tint, kind) {
  const r = clamp(Math.round(tint.r), 0, 255);
  const g = clamp(Math.round(tint.g), 0, 255);
  const b = clamp(Math.round(tint.b), 0, 255);
  if (kind === "hex") {
    return `#${[r, g, b].map((channel) => channel.toString(16).padStart(2, "0")).join("")}`;
  }
  return `rgba(${r},${g},${b},${Number(tint.a.toFixed(2))})`;
}

function mixTint(value, target, amount) {
  const from = parseTint(value);
  const to = parseTint(target);
  if (!from || !to) return value;
  return formatTint({
    r: from.r + (to.r - from.r) * amount,
    g: from.g + (to.g - from.g) * amount,
    b: from.b + (to.b - from.b) * amount,
    a: from.a,
  }, from.kind);
}

function scaleTint(value, factor) {
  const tint = parseTint(value);
  if (!tint) return value;
  return formatTint({
    r: tint.r * factor,
    g: tint.g * factor,
    b: tint.b * factor,
    a: tint.a,
  }, tint.kind);
}

export function resolveSpawnName(name) {
  if (typeof name === "string" && name in TABLES && looksLikeSpawn(TABLES[name])) {
    return name;
  }
  return "spawn";
}

export function listSpawnProfiles() {
  return Object.keys(TABLES).filter((key) => looksLikeSpawn(TABLES[key])).sort();
}

export function loadSpawn(name) {
  const resolved = resolveSpawnName(name);
  if (typeof name === "string" && name && name !== resolved) {
    throw new Error(`mesa ${name} não é perfil de chuva`);
  }
  return migrateSpawn(TABLES[resolved], resolved);
}

export { spawn, copy, dusk, calm, palettes, TABLES };
