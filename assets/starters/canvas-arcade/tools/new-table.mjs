#!/usr/bin/env node
// Nasce uma mesa no mesmo carregador. Não inventa consumidor e não
// republica o verbo. O custo fixo é este comando; o variável é ligar
// a regra ou a apresentação — exceto `--from spawn`, que copia a forma
// que o jogo já consome por `?spawn=` / settings.spawnProfile.

import { access, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const args = process.argv.slice(2);
const NAME = (args.find((item) => !item.startsWith("--")) ?? "").trim();
const fromIndex = args.indexOf("--from");
const FROM = fromIndex >= 0 ? String(args[fromIndex + 1] ?? "").trim() : "";
const RESERVED = new Set([
  "spawn", "copy", "dusk", "tables", "loadtable", "requirefields", "migratetable",
  "loadspawn", "listspawnprofiles", "resolvespawnname", "lookslikespawn", "default",
]);

if (!/^[a-z][a-z0-9]{0,31}$/.test(NAME) || RESERVED.has(NAME)) {
  console.error("uso: node tools/new-table.mjs <nome> [--from spawn]");
  console.error("nome: minúsculas, sem hífen; spawn, copy e dusk já existem.");
  process.exit(2);
}

if (FROM && FROM !== "spawn") {
  console.error("só --from spawn: é o perfil de chuva que o jogo já consome.");
  process.exit(2);
}

const jsonPath = join(ROOT, "data", `${NAME}.json`);
const tablesPath = join(ROOT, "src/game/tables.js");

try {
  await access(jsonPath);
  console.error(`já existe data/${NAME}.json`);
  process.exit(2);
} catch {
  // o arquivo ainda não existe — é o caso que o comando atende
}

const source = await readFile(tablesPath, "utf8");
const lastImport = source.lastIndexOf('with { type: "json" }');
const tableLine = source.match(/const TABLES = \{([^}]*)\}/);
if (lastImport < 0 || !tableLine) {
  console.error("não achei os imports JSON ou a linha TABLES em src/game/tables.js");
  process.exit(2);
}
const keys = tableLine[1].split(",").map((item) => item.trim()).filter(Boolean);
if (source.includes(`../../data/${NAME}.json`) || keys.includes(NAME)) {
  console.error(`src/game/tables.js já registra ${NAME}`);
  process.exit(2);
}

const end = source.indexOf("\n", lastImport);
const next = `${source.slice(0, end + 1)}import ${NAME} from "../../data/${NAME}.json" with { type: "json" };\n${source.slice(end + 1)}`
  .replace(tableLine[0], `const TABLES = { ${[...keys, NAME].join(", ")} }`);

const body = FROM === "spawn"
  ? await readFile(join(ROOT, "data", "spawn.json"), "utf8")
  : "{\n  \"schema\": 1\n}\n";

await writeFile(jsonPath, body);
await writeFile(tablesPath, next);
console.log(`mesa ${NAME}: data/${NAME}.json registrada em src/game/tables.js`);
if (FROM === "spawn") {
  console.log(`loadTable("${NAME}") já resolve. Perfil de chuva: ?spawn=${NAME}`);
} else {
  console.log(`loadTable("${NAME}") já resolve. Falta o consumidor.`);
}
