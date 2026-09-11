#!/usr/bin/env node
// Nasce look e chuva com o mesmo nome. `listMoods` passa a incluir o par
// e `?mood=` o aplica. `--from` copia um par que o jogo já pinta e chove.
// Não é alguém de fora no piso. `enough` e `consistent` continuam falsos.

import { spawn } from "node:child_process";
import { access } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { listLookIntents, listMoods, listSpawnIntents } from "../src/game/tables.js";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const args = process.argv.slice(2);
const NAME = (args.find((item) => !item.startsWith("--")) ?? "").trim();
const FROM = flag("from");
const LOOK = flag("look");
const SPAWN = flag("spawn");
const moods = listMoods();
const lookIntents = listLookIntents();
const spawnIntents = listSpawnIntents();
const RESERVED = new Set([
  "contrast", "colorblind", "look", "palettes", "spawn", "copy", "table", "pair", "mood",
  "dusk", "calm", "normal",
]);

function flag(name) {
  const index = args.indexOf(`--${name}`);
  return index >= 0 ? String(args[index + 1] ?? "").trim() : "";
}

function run(script, extra) {
  return new Promise((done) => {
    const child = spawn(process.execPath, [script, NAME, ...extra], {
      cwd: ROOT,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("exit", (code) => done({ code, stdout, stderr }));
  });
}

if (!/^[a-z][a-z0-9]{0,31}$/.test(NAME) || RESERVED.has(NAME)) {
  console.error("uso: node tools/new-pair.mjs <nome> --from <par> [--look warmer|cooler|night] [--spawn denser|calmer|brief]");
  console.error("nome: minúsculas, sem hífen; o nome vira look, chuva e ?mood=");
  process.exit(2);
}

if (!FROM) {
  console.error("--from é obrigatório: um par que o jogo já pinta e chove.");
  process.exit(2);
}

if (!moods.includes(FROM)) {
  console.error(`só --from de par: ${FROM} não é look e chuva ao mesmo tempo.`);
  process.exit(2);
}

if (LOOK && !lookIntents.includes(LOOK)) {
  console.error(`intenção de look desconhecida: ${LOOK}. use ${lookIntents.join("|")}.`);
  process.exit(2);
}

if (SPAWN && !spawnIntents.includes(SPAWN)) {
  console.error(`intenção de chuva desconhecida: ${SPAWN}. use ${spawnIntents.join("|")}.`);
  process.exit(2);
}

try {
  await access(join(ROOT, "data", `${NAME}.json`));
  console.error(`já existe data/${NAME}.json`);
  process.exit(2);
} catch {
  // a chuva ainda não existe — é o caso que o comando atende
}

const lookExtra = ["--from", FROM];
if (LOOK) lookExtra.push("--as", LOOK);
const tableExtra = ["--from", FROM];
if (SPAWN) tableExtra.push("--as", SPAWN);

const look = await run("tools/new-look.mjs", lookExtra);
if (look.code !== 0) {
  process.stderr.write(look.stderr);
  process.exit(look.code ?? 2);
}
const table = await run("tools/new-table.mjs", tableExtra);
if (table.code !== 0) {
  process.stderr.write(table.stderr);
  process.exit(table.code ?? 2);
}

process.stdout.write(look.stdout);
process.stdout.write(table.stdout);
console.log(`par ${NAME}: ?mood=${NAME}`);
console.log("listMoods já inclui. O piso não sobe.");
