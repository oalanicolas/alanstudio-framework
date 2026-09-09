#!/usr/bin/env node
// Relata os bytes no disco de dist/. Sem teto, sem aprovação, sem
// tempo até jogar. Identidade do artefato não é outra máquina.
//
// Uso: node tools/size.mjs [--dir caminho]

import { readdir, stat } from "node:fs/promises";
import { join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const flag = process.argv.indexOf("--dir");
const target = resolve(flag === -1 ? join(ROOT, "dist") : process.argv[flag + 1]);

async function walk(directory, files) {
  let entries;
  try {
    entries = await readdir(directory, { withFileTypes: true });
  } catch (error) {
    if (error && error.code === "ENOENT") return false;
    throw error;
  }
  for (const entry of entries) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      await walk(path, files);
      continue;
    }
    if (!entry.isFile()) continue;
    const info = await stat(path);
    files.push({ path: relative(target, path).split("\\").join("/"), bytes: info.size });
  }
  return true;
}

const files = [];
const present = await walk(target, files);
files.sort((a, b) => a.path.localeCompare(b.path));
const bytes = files.reduce((sum, item) => sum + item.bytes, 0);

console.log(JSON.stringify({
  present: Boolean(present),
  directory: target,
  files: files.length,
  bytes,
  entries: files,
  scope:
    "Bytes no disco de dist/. Sem teto, sem aprovação, sem tempo até jogar.",
}, null, 2));
