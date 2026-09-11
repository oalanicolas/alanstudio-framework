#!/usr/bin/env node
// Relata o pico de cada WAV em public/sfx. Não importa LUFS, não
// aprova mixagem e não substitui sessão com o volume no dispositivo.
// `heard` no harness continua falso.

import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { readWav } from "./wav.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const FOLDER = join(ROOT, "public/sfx");

const names = (await readdir(FOLDER)).filter((name) => name.endsWith(".wav")).sort();
const files = [];
for (const name of names) {
  const wav = await readWav(join(FOLDER, name));
  files.push({
    file: name,
    peak: Math.round(wav.peak * 32767),
    linear: wav.linear,
    dbfs: wav.dbfs,
  });
}

const report = {
  files,
  scope:
    "Pico do arquivo no disco, não do mix em cena. Sem limiar, sem aprovação, " +
    "sem loudness percebido.",
};

console.log(JSON.stringify(report, null, 2));
