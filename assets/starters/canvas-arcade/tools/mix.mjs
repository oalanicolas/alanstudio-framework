#!/usr/bin/env node
// Soma as vozes de uma partida simulada: barramento, ducking e limite.
// Não importa LUFS, não aprova mixagem e não substitui sessão no dispositivo.
// `heard` continua falso.
//
// Uso: node tools/mix.mjs [--runs 3] [--seed 7]

import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { DUCK_BUSES, DUCK_LEVEL, MIX_HEADROOM, SOUNDS } from "../src/game/audio.js";
import { DEFAULT_BUSES } from "../src/core/settings.js";
import { advance, chainPlaybackRate, createState, neutralIntent, CONFIG, TICK_HZ } from "../src/game/rules.js";
import { createRng } from "../src/core/rng.js";
import { readWav } from "./wav.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const FOLDER = join(ROOT, "public/sfx");
const MAX_VOICES = 6;

const argument = (name, fallback) => {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? fallback : Number(process.argv[index + 1]);
};

const runs = argument("runs", 3);
const baseSeed = argument("seed", 7);

const files = (await readdir(FOLDER)).filter((name) => name.endsWith(".wav"));
const packs = new Map();
let sampleRate = 44100;
for (const name of files.sort()) {
  const stem = name.replace(/\.wav$/i, "");
  const role = stem.endsWith("-b") ? stem.slice(0, -2) : stem;
  if (!(role in SOUNDS)) continue;
  const wav = await readWav(join(FOLDER, name));
  sampleRate = wav.sampleRate;
  const pack = packs.get(role) ?? [];
  pack.push(wav.samples);
  packs.set(role, pack);
}

const tickSamples = Math.max(1, Math.round(sampleRate / TICK_HZ));
const cursors = new Map();
const bedSamples = packs.get("bed")?.[0] ?? null;
let peak = 0;
let overUnity = 0;
let eventsMixed = 0;
let stolen = 0;
let voicesPlayed = 0;
let pitched = 0;

function eventRate(event) {
  if ((event.type === "collect" || event.type === "bank") && Number.isFinite(event.chain)) {
    return chainPlaybackRate(event.chain);
  }
  return 1;
}

function sampleAt(samples, offset) {
  const index = Math.floor(offset);
  if (index >= samples.length) return null;
  const frac = offset - index;
  const a = samples[index];
  const b = index + 1 < samples.length ? samples[index + 1] : a;
  return a + (b - a) * frac;
}

function gainAt(bus, ducking) {
  const level = Number.isFinite(DEFAULT_BUSES[bus]) ? DEFAULT_BUSES[bus] : 1;
  const duck = ducking && DUCK_BUSES.includes(bus) ? DUCK_LEVEL : 1;
  return DEFAULT_BUSES.master * MIX_HEADROOM * level * duck;
}

for (let run = 0; run < runs; run += 1) {
  const state = createState(baseSeed + run);
  const rng = createRng(baseSeed + run + 1000);
  const intent = neutralIntent();
  const voices = [];
  let duckUntil = 0;
  let tick = 0;
  let bedOffset = 0;

  while (state.phase === "playing") {
    intent.move = rng.next() < 0.55 ? (rng.next() < 0.5 ? -1 : 1) : 0;
    intent.dash = rng.next() < 0.05;
    intent.bank = state.chain >= 3 && rng.next() < 0.2;
    advance(state, intent);
    const timeMs = (tick / TICK_HZ) * 1000;

    for (const event of state.events) {
      const definition = SOUNDS[event.type];
      if (!definition) continue;
      const pack = packs.get(event.type);
      if (!pack?.length) continue;
      if (definition.duckMs) duckUntil = timeMs + definition.duckMs;
      const cursor = cursors.get(event.type) ?? 0;
      const samples = pack[cursor % pack.length];
      cursors.set(event.type, cursor + 1);
      if (voices.length >= MAX_VOICES) {
        let weakest = 0;
        for (let index = 1; index < voices.length; index += 1) {
          if (voices[index].priority < voices[weakest].priority) weakest = index;
        }
        if (voices[weakest].priority >= definition.priority) continue;
        voices.splice(weakest, 1);
        stolen += 1;
      }
      const rate = eventRate(event);
      if (rate !== 1) pitched += 1;
      voices.push({
        samples,
        offset: 0,
        rate,
        priority: definition.priority,
        bus: definition.bus,
      });
      eventsMixed += 1;
      voicesPlayed += 1;
    }

    const ducking = timeMs < duckUntil;
    for (let sample = 0; sample < tickSamples; sample += 1) {
      let sum = 0;
      for (let index = voices.length - 1; index >= 0; index -= 1) {
        const voice = voices[index];
        const value = sampleAt(voice.samples, voice.offset);
        if (value === null) {
          voices.splice(index, 1);
          continue;
        }
        sum += value * gainAt(voice.bus, ducking);
        voice.offset += voice.rate;
      }
      if (bedSamples) {
        sum += bedSamples[bedOffset] * gainAt("music", ducking);
        bedOffset = (bedOffset + 1) % bedSamples.length;
      }
      const abs = Math.abs(sum);
      if (abs > peak) peak = abs;
      if (abs >= 1) overUnity += 1;
    }
    tick += 1;
  }
}

const report = {
  runs,
  sample_rate: sampleRate,
  events: eventsMixed,
  voices: voicesPlayed,
  stolen,
  pitched,
  bed: Boolean(bedSamples),
  peak_linear: Number(peak.toFixed(4)),
  peak_dbfs: peak > 0 ? Number((20 * Math.log10(peak)).toFixed(2)) : null,
  samples_at_or_over_unity: overUnity,
  heard: false,
  scope:
    "Soma das vozes numa partida simulada, com o mesmo palco, folga, " +
    "duck só na cama e taxa da corrente do mixer. Sem dispositivo, sem " +
    "limiar, sem aprovação, sem loudness percebido.",
};

console.log(JSON.stringify(report, null, 2));
