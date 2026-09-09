#!/usr/bin/env node
// Relata o pico de cada WAV em public/sfx. Não importa LUFS, não
// aprova mixagem e não substitui sessão com o volume no dispositivo.
// `heard` no harness continua falso.

import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const FOLDER = join(ROOT, "public/sfx");

function peakOfWav(bytes) {
  if (bytes.subarray(0, 4).toString("ascii") !== "RIFF") {
    throw new Error("não é WAV");
  }
  let offset = 12;
  while (offset + 8 <= bytes.length) {
    const id = bytes.subarray(offset, offset + 4).toString("ascii");
    const size = bytes.readUInt32LE(offset + 4);
    if (id === "data") {
      const start = offset + 8;
      let peak = 0;
      for (let index = start; index + 1 < start + size; index += 2) {
        const sample = Math.abs(bytes.readInt16LE(index));
        if (sample > peak) peak = sample;
      }
      const linear = peak / 32767;
      return {
        peak,
        linear: Number(linear.toFixed(4)),
        dbfs: linear > 0 ? Number((20 * Math.log10(linear)).toFixed(2)) : null,
      };
    }
    offset += 8 + size + (size % 2);
  }
  throw new Error("chunk data ausente");
}

const names = (await readdir(FOLDER)).filter((name) => name.endsWith(".wav")).sort();
const files = [];
for (const name of names) {
  const bytes = await readFile(join(FOLDER, name));
  files.push({ file: name, ...peakOfWav(bytes) });
}

const report = {
  files,
  scope:
    "Pico do arquivo no disco, não do mix em cena. Sem limiar, sem aprovação, " +
    "sem loudness percebido.",
};

console.log(JSON.stringify(report, null, 2));
