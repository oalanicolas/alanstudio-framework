import { test } from "node:test";
import assert from "node:assert/strict";

import {
  applyLookIntent, applySpawnIntent, loadTable, loadSpawn, listLookIntents,   listLooks, listMoods, listSpawnIntents, listSpawnProfiles, looksLikeSpawn, lookRecord,
  LOOK_LABELS, matchingMood, pairPatch, resolveLookName, resolveMoodName, SPAWN_LABELS, COLORBLIND_INKS, dressPalette,
  migrateCopy, migratePalettes, migrateSpawn, migrateTable, requireFields, resolveSpawnName, spawnRecord, TABLES,
  SPAWN_FIELDS, SPAWN_SCHEMA, COPY_SCHEMA, COPY_FIELDS, PALETTE_SCHEMA, PALETTE_FIELDS, LOOK_INTENTS, SPAWN_INTENTS, PALETTES,
} from "../src/game/tables.js";

test("as mesas passam pelo mesmo carregador", () => {
  assert.deepEqual(Object.keys(TABLES).sort(), ["calm", "copy", "dusk", "palettes", "spawn"]);
  assert.equal(loadTable("spawn").intervalTicks, 22);
  assert.equal(loadTable("spawn").schema, SPAWN_SCHEMA);
  assert.equal(loadTable("dusk").intervalTicks, 16);
  assert.equal(loadTable("calm").intervalTicks, 30);
  assert.equal(loadTable("copy").chain, "Corrente");
  assert.equal(loadTable("copy").schema, COPY_SCHEMA);
  assert.equal(loadTable("palettes").schema, PALETTE_SCHEMA);
  assert.equal(loadTable("palettes").palettes.normal.field, "#171b26");
  assert.equal(PALETTES.contrast.plateEdge, "#ffffff");
  assert.equal(PALETTES.dusk.field, "#241816");
  assert.equal(PALETTES.calm.field, "#15201e");
  assert.deepEqual(listLooks(), ["calm", "dusk", "normal"]);
  assert.equal(resolveLookName("dusk"), "dusk");
  assert.equal(resolveLookName("calm"), "calm");
  assert.equal(resolveLookName("contrast"), "normal");
  assert.equal(resolveLookName("inventada"), "normal");
  assert.equal(dressPalette({ look: "dusk" }).orb, PALETTES.dusk.orb);
  assert.equal(dressPalette({ look: "dusk" }).field, PALETTES.dusk.field);
  assert.notEqual(PALETTES.dusk.orb, PALETTES.normal.orb, "dusk no eixo quente precisa desta tinta");
  const stable = dressPalette({ look: "dusk", colorblind: true });
  assert.equal(stable.orb, COLORBLIND_INKS.orb);
  assert.equal(stable.shard, COLORBLIND_INKS.shard);
  assert.equal(stable.field, PALETTES.dusk.field, "a tinta estável não troca o campo");
  assert.equal(dressPalette({ look: "dusk", colorblind: true, highContrast: true }).field, PALETTES.contrast.field);
  assert.equal(listLooks().includes("colorblind"), false);
  assert.throws(() => loadTable("inventada"), /mesa desconhecida/);
});

test("só mesa com forma de chuva entra na família jogável", () => {
  assert.deepEqual(listSpawnProfiles(), ["calm", "dusk", "spawn"]);
  assert.equal(loadSpawn("dusk").intervalTicks, 16);
  assert.equal(loadSpawn("dusk").practiceTicks, 90);
  assert.equal(loadSpawn("calm").intervalTicks, 30);
  assert.equal(loadSpawn("calm").practiceTicks, 420);
  assert.equal(resolveSpawnName("dusk"), "dusk");
  assert.equal(resolveSpawnName("copy"), "spawn");
  assert.equal(resolveSpawnName("inventada"), "spawn");
  assert.equal(looksLikeSpawn(loadTable("copy")), false);
  assert.equal(looksLikeSpawn(loadTable("palettes")), false);
  assert.equal(resolveSpawnName("palettes"), "spawn");
  assert.throws(() => loadSpawn("copy"), /não é perfil de chuva/);
  assert.throws(() => loadSpawn("inventada"), /não é perfil de chuva/);
});

test("o par só existe quando o nome é look e chuva", () => {
  assert.deepEqual(listMoods(), ["calm", "dusk"]);
  assert.equal(resolveMoodName("calm"), "calm");
  assert.equal(resolveMoodName("dusk"), "dusk");
  assert.equal(resolveMoodName("normal"), "calm");
  assert.equal(resolveMoodName("spawn"), "calm");
  assert.equal(resolveMoodName("contrast"), "calm");
  assert.equal(resolveMoodName("inventada"), "calm");
  assert.deepEqual(pairPatch("calm"), { look: "calm", spawnProfile: "calm" });
  assert.deepEqual(pairPatch("dusk"), { look: "dusk", spawnProfile: "dusk" });
  assert.equal(pairPatch("normal"), null);
  assert.equal(pairPatch("spawn"), null);
  assert.equal(pairPatch(""), null);
  assert.equal(matchingMood("calm", "calm"), "calm");
  assert.equal(matchingMood("dusk", "calm"), "");
  assert.equal(matchingMood("normal", "spawn"), "");
  assert.equal(LOOK_LABELS.calm, "Calma");
  assert.equal(SPAWN_LABELS.calm, "Calma");
  assert.equal(LOOK_LABELS.dusk, "Crepúsculo");
});

test("campo obrigatório ausente falha com o nome da mesa e do campo", () => {
  assert.equal(requireFields("spawn", ["intervalTicks"]).intervalTicks, 22);
  assert.throws(() => requireFields("spawn", ["inventado"]), /mesa spawn sem inventado/);
});

test("spawn sem schema migra; schema futuro falha com o número", () => {
  const old = migrateSpawn({ intervalTicks: 22, minIntervalTicks: 11 });
  assert.equal(old.schema, SPAWN_SCHEMA);
  assert.equal(old.intervalTicks, 22);
  assert.equal(old.practiceTicks, 240);
  assert.equal(old.recoveryTicks, 90);
  assert.throws(() => migrateSpawn({ schema: 9 }), /mesa spawn schema 9 não suportado/);
  assert.throws(() => migrateSpawn(null), /mesa spawn ilegível/);
});

test("a intenção desloca knobs sem inventar mesa nem aprovar chuva", () => {
  const spawn = loadSpawn("spawn");
  const denser = applySpawnIntent(spawn, "denser");
  const calmer = applySpawnIntent(spawn, "calmer");
  const brief = applySpawnIntent(spawn, "brief");
  assert.deepEqual(listSpawnIntents(), Object.keys(SPAWN_INTENTS));
  assert.ok(denser.intervalTicks < spawn.intervalTicks);
  assert.ok(denser.practiceTicks < spawn.practiceTicks);
  assert.ok(denser.hazardChanceEnd > spawn.hazardChanceEnd);
  assert.ok(calmer.intervalTicks > spawn.intervalTicks);
  assert.ok(calmer.practiceTicks > spawn.practiceTicks);
  assert.ok(brief.practiceTicks < spawn.practiceTicks);
  assert.ok(brief.rampTicks < spawn.rampTicks);
  assert.ok(denser.minIntervalTicks <= denser.intervalTicks);
  assert.ok(looksLikeSpawn(denser));
  assert.deepEqual(Object.keys(spawnRecord(denser)), ["schema", ...SPAWN_FIELDS]);
  assert.equal(spawnRecord(denser).schema, SPAWN_SCHEMA);
  assert.throws(() => applySpawnIntent(spawn, "melhor"), /intenção desconhecida/);
});

test("calm é chuva autoral, não o calmer aplicado em spawn", () => {
  const spawn = loadSpawn("spawn");
  const dusk = loadSpawn("dusk");
  const calm = loadSpawn("calm");
  const calmer = applySpawnIntent(spawn, "calmer");
  assert.ok(calm.intervalTicks > spawn.intervalTicks);
  assert.ok(calm.intervalTicks > dusk.intervalTicks);
  assert.ok(calm.practiceTicks > spawn.practiceTicks);
  assert.ok(calm.practiceTicks > dusk.practiceTicks);
  assert.ok(calm.hazardChanceEnd < spawn.hazardChanceEnd);
  assert.ok(calm.fallSpeedMax < spawn.fallSpeedMax);
  assert.ok(calm.rampTicks > spawn.rampTicks);
  assert.ok(calm.recoveryTicks > spawn.recoveryTicks);
  assert.notEqual(calm.intervalTicks, calmer.intervalTicks);
  assert.notEqual(calm.minIntervalTicks, calmer.minIntervalTicks);
  assert.notEqual(calm.practiceTicks, calmer.practiceTicks);
  assert.notEqual(calm.hazardChanceEnd, calmer.hazardChanceEnd);
  assert.notEqual(calm.rampTicks, calmer.rampTicks);
});

test("copy sem schema migra; schema futuro e campo ausente falham com o nome", () => {
  const old = migrateCopy({ paused: "Pausado" });
  assert.equal(old.schema, COPY_SCHEMA);
  assert.equal(old.fantasy, "");
  assert.equal(old.title_play, "Jogar: {dash}");
  assert.equal(old.title_again, "Repetir a última: {dash}");
  assert.equal(old.title_new, "Nova partida: {reset}");
  assert.equal(old.title_last, "Última");
  assert.equal(old.over_door, "Abertura: {dash}");
  assert.equal(old.over_door_inline, "abertura: {dash}");
  assert.throws(() => migrateTable("copy", { schema: 4 }, COPY_SCHEMA), /mesa copy schema 4 não suportado/);
  assert.throws(
    () => migrateTable("copy", { schema: 1 }, COPY_SCHEMA, COPY_FIELDS),
    /mesa copy sem fantasy/,
  );
});

test("a intenção desloca tokens sem inventar look nem aprovar arte", () => {
  const warmer = applyLookIntent(PALETTES.normal, "warmer");
  const cooler = applyLookIntent(PALETTES.normal, "cooler");
  const night = applyLookIntent(PALETTES.normal, "night");
  assert.deepEqual(listLookIntents(), Object.keys(LOOK_INTENTS));
  assert.notEqual(warmer.field, PALETTES.normal.field);
  assert.notEqual(cooler.field, PALETTES.normal.field);
  assert.notEqual(night.field, PALETTES.normal.field);
  assert.notEqual(warmer.field, cooler.field);
  assert.notEqual(warmer.orb, PALETTES.normal.orb);
  assert.deepEqual(Object.keys(lookRecord(warmer)).sort(), [...PALETTE_FIELDS].sort());
  assert.equal(lookRecord(PALETTES.dusk).field, PALETTES.dusk.field);
  assert.throws(() => applyLookIntent(PALETTES.normal, "melhor"), /intenção desconhecida/);
});

test("calm é look autoral, não cooler nem night aplicados em normal", () => {
  const cooler = applyLookIntent(PALETTES.normal, "cooler");
  const night = applyLookIntent(PALETTES.normal, "night");
  const duskCooler = applyLookIntent(PALETTES.dusk, "cooler");
  assert.equal(PALETTES.calm.orb, "#6ab8a4");
  assert.notEqual(PALETTES.calm.field, PALETTES.normal.field);
  assert.notEqual(PALETTES.calm.field, PALETTES.dusk.field);
  assert.notEqual(PALETTES.calm.field, cooler.field);
  assert.notEqual(PALETTES.calm.field, night.field);
  assert.notEqual(PALETTES.calm.field, duskCooler.field);
  assert.notEqual(PALETTES.calm.orb, cooler.orb);
  assert.notEqual(PALETTES.calm.orb, PALETTES.dusk.orb);
  assert.notEqual(PALETTES.calm.orb, night.orb);
});

test("paleta sem contraste ou sem token falha com o nome", () => {
  const ok = migratePalettes({
    palettes: {
      normal: Object.fromEntries(PALETTE_FIELDS.map((field) => [field, "#111"])),
      contrast: Object.fromEntries(PALETTE_FIELDS.map((field) => [field, "#fff"])),
    },
  });
  assert.equal(ok.schema, PALETTE_SCHEMA);
  assert.equal(ok.palettes.normal.field, "#111");
  assert.throws(() => migratePalettes({ palettes: { normal: ok.palettes.normal } }), /mesa palettes sem contrast/);
  assert.throws(
    () => migratePalettes({ palettes: { normal: ok.palettes.normal, contrast: { field: "#000" } } }),
    /mesa palettes.contrast sem/,
  );
  assert.throws(() => migratePalettes({ schema: 4 }), /mesa palettes schema 4 não suportado/);
});
