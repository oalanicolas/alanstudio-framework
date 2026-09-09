#!/usr/bin/env node
// Nasce uma mesa no mesmo carregador. Não inventa consumidor e não
// republica o verbo. O custo fixo é este comando; o variável é ligar
// a regra ou a apresentação.

import { access, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const NAME = (process.argv[2] ?? "").trim();
const RESERVED = new Set([
  "spawn", "copy", "tables", "loadtable", "requirefields", "default",
]);

if (!/^[a-z][a-z0-9]{0,31}$/.test(NAME) || RESERVED.has(NAME)) {
  console.error("uso: node tools/new-table.mjs <nome>");
  console.error("nome: minúsculas, sem hífen; spawn e copy já existem.");
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

await writeFile(jsonPath, "{}\n");
await writeFile(tablesPath, next);
console.log(`mesa ${NAME}: data/${NAME}.json registrada em src/game/tables.js`);
console.log(`loadTable("${NAME}") já resolve. Falta o consumidor.`);
