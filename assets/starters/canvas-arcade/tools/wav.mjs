// Leitura de WAV PCM 16-bit. Não decodifica compressão e não ouve.

import { readFile } from "node:fs/promises";

export function decodeWav(bytes) {
  const buffer = Buffer.isBuffer(bytes) ? bytes : Buffer.from(bytes);
  if (buffer.subarray(0, 4).toString("ascii") !== "RIFF") {
    throw new Error("não é WAV");
  }
  let channels = 1;
  let sampleRate = 44100;
  let bits = 16;
  let offset = 12;
  while (offset + 8 <= buffer.length) {
    const id = buffer.subarray(offset, offset + 4).toString("ascii");
    const size = buffer.readUInt32LE(offset + 4);
    if (id === "fmt ") {
      channels = buffer.readUInt16LE(offset + 10);
      sampleRate = buffer.readUInt32LE(offset + 12);
      bits = buffer.readUInt16LE(offset + 22);
    }
    if (id === "data") {
      if (bits !== 16) throw new Error("só PCM 16-bit");
      const start = offset + 8;
      const frames = Math.floor(size / (2 * channels));
      const samples = new Float32Array(frames);
      let peak = 0;
      for (let frame = 0; frame < frames; frame += 1) {
        let sum = 0;
        for (let channel = 0; channel < channels; channel += 1) {
          sum += buffer.readInt16LE(start + (frame * channels + channel) * 2);
        }
        const linear = sum / channels / 32767;
        samples[frame] = linear;
        const abs = Math.abs(linear);
        if (abs > peak) peak = abs;
      }
      return {
        samples,
        sampleRate,
        channels,
        peak,
        linear: Number(peak.toFixed(4)),
        dbfs: peak > 0 ? Number((20 * Math.log10(peak)).toFixed(2)) : null,
      };
    }
    offset += 8 + size + (size % 2);
  }
  throw new Error("chunk data ausente");
}

export async function readWav(path) {
  return decodeWav(await readFile(path));
}
