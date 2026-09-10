#!/usr/bin/env node
// Nasce um look na mesa de paletas. Não inventa consumidor e não
// republica o verbo: o jogo já consome qualquer look em palettes.json
// por `?look=` / settings.look. `--from` copia um look que já existe;
// `--as` desloca os tokens sem pedir a receita de cabeça. `contrast`
// é alcance, não look. Isso não é alguém de fora no piso.

import { readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import {
  applyLookIntent,
  listLookIntents,
  listLooks,
  lookRecord,
  migratePalettes,
  resolveLookName,
  LOOK_INTENTS,
} from "../src/game/tables.js";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const args = process.argv.slice(2);
const NAME = (args.find((item) => !item.startsWith("--")) ?? "").trim();
const fromIndex = args.indexOf("--from");
const FROM = fromIndex >= 0 ? String(args[fromIndex + 1] ?? "").trim() : "";
const asIndex = args.indexOf("--as");
const AS = asIndex >= 0 ? String(args[asIndex + 1] ?? "").trim() : "";
const RESERVED = new Set([
  "contrast", "look", "palettes", "spawn", "copy", "table", "pair", "mood",
  "listlooks", "resolvelookname", "applylookintent", "lookrecord",
  "listlookintents", "default",
]);
const intents = listLookIntents();
const existing = new Set(listLooks());

if (!/^[a-z][a-z0-9]{0,31}$/.test(NAME) || RESERVED.has(NAME)) {
  console.error("uso: node tools/new-look.mjs <nome> --from <look> [--as warmer|cooler|night]");
  console.error("nome: minúsculas, sem hífen; contrast é alcance, não look.");
  process.exit(2);
}

if (existing.has(NAME)) {
  console.error(`já existe look ${NAME}`);
  process.exit(2);
}

if (!FROM) {
  console.error("--from é obrigatório: um look novo copia um look que o jogo já pinta.");
  process.exit(2);
}

if (FROM === "contrast" || resolveLookName(FROM) !== FROM) {
  console.error(`só --from de look: ${FROM} não é look de arte.`);
  process.exit(2);
}

if (AS && !intents.includes(AS)) {
  console.error(`intenção desconhecida: ${AS}. use ${intents.join("|")}.`);
  process.exit(2);
}

const jsonPath = join(ROOT, "data/palettes.json");
const raw = JSON.parse(await readFile(jsonPath, "utf8"));
const table = migratePalettes(raw);
const source = lookRecord(table.palettes[FROM]);
const next = AS ? applyLookIntent(source, AS) : source;
table.palettes[NAME] = next;
await writeFile(jsonPath, `${JSON.stringify(table, null, 2)}\n`);

console.log(`look ${NAME}: data/palettes.json`);
console.log(`?look=${NAME} e settings.look já consomem.`);
if (AS) console.log(`intenção ${AS} a partir de ${FROM}: ${LOOK_INTENTS[AS]}.`);
else console.log(`cópia de ${FROM}: os tokens são os mesmos até alguém deslocar.`);
