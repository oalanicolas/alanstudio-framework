// Servidor estático mínimo, sem dependências.
//
// Módulos ES não carregam por `file://`, então abrir o index.html direto no
// navegador falha. Este servidor existe só para jogar e comparar localmente.
// Não é servidor de produção: serve o diretório do projeto por GET e aceita
// POST em `/playtest/last-run` (candidato), `/playtest/note` (recibo) e
// `/playtest/finding` (achado preenchido). Recusa caminho que escape do
// projeto e não grava na árvore exportada.

import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { createReadStream, existsSync } from "node:fs";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { networkInterfaces } from "node:os";
import { dirname, extname, join, normalize, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

import {
  LAST_RUN_FILE,
  LAST_RUN_ROUTE,
  NOTE_DIR,
  NOTE_ROUTE,
  noteStamp,
  FINDING_ROUTE,
  playFinding,
  playNote,
  playReport,
} from "../src/core/run-report.js";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));

// Abrir o navegador é cortesia do terminal, não o jogo executado.
// Testes encanaram o stdout: sem TTY, ninguém ganha uma janela.
// CI e BROWSER=0 também recusam. Falha ao abrir não derruba o serve.
export function shouldOpenBrowser(env = process.env, stdout = process.stdout) {
  if (env.CI === "true" || env.CI === "1") return false;
  if (env.BROWSER === "0" || env.BROWSER === "none") return false;
  return Boolean(stdout && stdout.isTTY);
}

// HOST=127.0.0.1 prende o bind e cala a rede. Sem HOST o listen continua
// o padrão do Node (todas as interfaces) — o que já era alcançável na
// LAN, só não era anunciado. Anunciar não é alguém de fora.
export function listenHost(env = process.env) {
  const host = env.HOST || env.LISTEN_HOST;
  if (host === "127.0.0.1" || host === "localhost") return "127.0.0.1";
  if (host === "0.0.0.0" || host === "*") return "0.0.0.0";
  return undefined;
}

function isLanV4(addr) {
  if (!addr || addr.internal) return false;
  const family = addr.family;
  if (family !== "IPv4" && family !== 4) return false;
  const ip = addr.address;
  return Boolean(ip) && !ip.startsWith("169.254.");
}

export function advertisedOrigins(port, interfaces = networkInterfaces(), env = process.env) {
  const origins = [`http://localhost:${port}`];
  if (listenHost(env) === "127.0.0.1") return origins;
  for (const list of Object.values(interfaces || {})) {
    for (const addr of list || []) {
      if (!isLanV4(addr)) continue;
      origins.push(`http://${addr.address}:${port}`);
    }
  }
  return [...new Set(origins)];
}

export function isArtifactRoot(root = ROOT) {
  return existsSync(join(root, "VERSION.json"));
}

export function listenBanner(port, interfaces = networkInterfaces(), env = process.env, root = ROOT) {
  const origins = advertisedOrigins(port, interfaces, env);
  const local = origins[0];
  const lines = [
    `Jogo em ${local}/  (Ctrl+C encerra)`,
    `Look: ${local}/?look=dusk  ${local}/?look=calm`,
    `Chuva: ${local}/?spawn=dusk  ${local}/?spawn=calm`,
    `Par: ${local}/?mood=calm  ${local}/?mood=dusk`,
    `Convite: ${local}/?invite=1`,
    "Candidato: a partida grava docs/playtest/last-run.json",
    "Nota: depois do fim a página grava o recibo em docs/playtest/",
    "Achado: no convite a página grava os quatro nomes se estiverem preenchidos",
  ];
  for (const origin of origins.slice(1)) {
    lines.push(`Rede: ${origin}/`);
    lines.push(`Convite na rede: ${origin}/?invite=1`);
  }
  if (isArtifactRoot(root)) {
    lines.push("Árvore exportada. Servir aqui não é outra máquina.");
  }
  return lines.join("\n");
}

function openBrowser(url) {
  const command = process.platform === "darwin" ? "open" : process.platform === "win32" ? "cmd" : "xdg-open";
  const args = process.platform === "win32" ? ["/c", "start", "", url] : [url];
  try {
    spawn(command, args, { detached: true, stdio: "ignore" }).unref();
  } catch {
    // o endereço continua no console
  }
}

// `pathname` de uma URL mantém a codificação percentual: um projeto em
// "Farol do Sul" viraria "Farol%20do%20Sul", uma pasta que não existe, e todo
// pedido responderia 404. `fileURLToPath` decodifica.
export { FINDING_ROUTE, LAST_RUN_FILE, LAST_RUN_ROUTE, NOTE_DIR, NOTE_ROUTE };

export const LAST_RUN_LIMIT = 32 * 1024;

export function acceptLastRun(raw) {
  let data;
  try {
    data = typeof raw === "string" ? JSON.parse(raw) : raw;
  } catch {
    return { ok: false, status: 400, reason: "json ilegível" };
  }
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    return { ok: false, status: 400, reason: "json ilegível" };
  }
  const run = data.run && typeof data.run === "object" && !Array.isArray(data.run)
    ? data.run
    : null;
  if (!run || !Number.isFinite(run.ticks)) {
    return { ok: false, status: 400, reason: "sem run" };
  }
  return {
    ok: true,
    report: playReport({
      seed: data.seed ?? run.seed,
      spawn: data.spawn,
      run,
      curve: data.curve,
      policy: "played",
    }),
  };
}

export async function writeLastRun(root, report) {
  const dest = join(root, LAST_RUN_FILE);
  await mkdir(dirname(dest), { recursive: true });
  await writeFile(dest, `${JSON.stringify(report, null, 2)}\n`);
  return dest;
}

export function acceptNote(raw) {
  let data;
  try {
    data = typeof raw === "string" ? JSON.parse(raw) : raw;
  } catch {
    return { ok: false, status: 400, reason: "json ilegível" };
  }
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    return { ok: false, status: 400, reason: "json ilegível" };
  }
  const note = String(data.note ?? "").trim();
  if (!note) return { ok: false, status: 400, reason: "sem nota" };
  const author = String(data.author ?? "").trim() || "página";
  return { ok: true, author, note };
}

async function attachedRun(root) {
  try {
    const data = JSON.parse(await readFile(join(root, LAST_RUN_FILE), "utf8"));
    if (!data || typeof data !== "object") return {};
    const run = data.run && typeof data.run === "object" ? data.run : null;
    const curve = data.curve && typeof data.curve === "object" ? data.curve : null;
    return { run, curve };
  } catch {
    return {};
  }
}

export async function writeNote(root, { author, note }) {
  const extra = await attachedRun(root);
  const report = playNote({
    author,
    note,
    project: String(root),
    run: extra.run,
    curve: extra.curve,
  });
  let folder = join(root, NOTE_DIR, noteStamp());
  try {
    await mkdir(folder, { recursive: true });
  } catch {
    folder = join(root, NOTE_DIR, `${noteStamp()}-b`);
    await mkdir(folder, { recursive: true });
  }
  const dest = join(folder, "record.json");
  await writeFile(dest, `${JSON.stringify(report, null, 2)}\n`, { flag: "wx" });
  return dest;
}

export function acceptFinding(raw) {
  let data;
  try {
    data = typeof raw === "string" ? JSON.parse(raw) : raw;
  } catch {
    return { ok: false, status: 400, reason: "json ilegível" };
  }
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    return { ok: false, status: 400, reason: "json ilegível" };
  }
  const text = playFinding(data);
  if (!text) return { ok: false, status: 400, reason: "sem achado" };
  return { ok: true, text };
}

export async function writeFinding(root, text) {
  await mkdir(join(root, NOTE_DIR), { recursive: true });
  let dest = join(root, NOTE_DIR, `${noteStamp()}-achado.md`);
  try {
    await writeFile(dest, text, { flag: "wx" });
  } catch {
    dest = join(root, NOTE_DIR, `${noteStamp()}-b-achado.md`);
    await writeFile(dest, text, { flag: "wx" });
  }
  return dest;
}

function collectBody(request, limit) {
  return new Promise((done) => {
    const chunks = [];
    let size = 0;
    request.on("data", (chunk) => {
      size += chunk.length;
      if (size > limit) {
        request.destroy();
        done(null);
        return;
      }
      chunks.push(chunk);
    });
    request.on("end", () => done(Buffer.concat(chunks).toString("utf8")));
    request.on("error", () => done(null));
  });
}

const PORT = Number(process.env.PORT ?? 8080);
const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".png": "image/png",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".wav": "audio/wav",
  ".ogg": "audio/ogg",
  ".mp3": "audio/mpeg",
  ".woff2": "font/woff2",
};

const server = createServer(async (request, response) => {
  const pathname = new URL(request.url, "http://localhost").pathname;
  if (request.method === "POST" && pathname === LAST_RUN_ROUTE) {
    if (isArtifactRoot()) {
      response.writeHead(403, { "content-type": "text/plain; charset=utf-8" }).end("árvore exportada");
      return;
    }
    const raw = await collectBody(request, LAST_RUN_LIMIT);
    if (raw === null) {
      response.writeHead(413, { "content-type": "text/plain; charset=utf-8" }).end("corpo grande");
      return;
    }
    const accepted = acceptLastRun(raw);
    if (!accepted.ok) {
      response.writeHead(accepted.status, { "content-type": "text/plain; charset=utf-8" }).end(accepted.reason);
      return;
    }
    await writeLastRun(ROOT, accepted.report);
    response.writeHead(204).end();
    return;
  }
  if (request.method === "POST" && pathname === NOTE_ROUTE) {
    if (isArtifactRoot()) {
      response.writeHead(403, { "content-type": "text/plain; charset=utf-8" }).end("árvore exportada");
      return;
    }
    const raw = await collectBody(request, LAST_RUN_LIMIT);
    if (raw === null) {
      response.writeHead(413, { "content-type": "text/plain; charset=utf-8" }).end("corpo grande");
      return;
    }
    const accepted = acceptNote(raw);
    if (!accepted.ok) {
      response.writeHead(accepted.status, { "content-type": "text/plain; charset=utf-8" }).end(accepted.reason);
      return;
    }
    await writeNote(ROOT, accepted);
    response.writeHead(204).end();
    return;
  }
  if (request.method === "POST" && pathname === FINDING_ROUTE) {
    if (isArtifactRoot()) {
      response.writeHead(403, { "content-type": "text/plain; charset=utf-8" }).end("árvore exportada");
      return;
    }
    const raw = await collectBody(request, LAST_RUN_LIMIT);
    if (raw === null) {
      response.writeHead(413, { "content-type": "text/plain; charset=utf-8" }).end("corpo grande");
      return;
    }
    const accepted = acceptFinding(raw);
    if (!accepted.ok) {
      response.writeHead(accepted.status, { "content-type": "text/plain; charset=utf-8" }).end(accepted.reason);
      return;
    }
    await writeFinding(ROOT, accepted.text);
    response.writeHead(204).end();
    return;
  }
  if (request.method !== "GET" && request.method !== "HEAD") {
    response.writeHead(405, { allow: "GET, HEAD, POST" }).end();
    return;
  }
  const requested = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
  const relative = normalize(requested === "/" ? "index.html" : requested.replace(/^\/+/, ""));
  const target = join(ROOT, relative);
  if (!target.startsWith(ROOT + sep) && target !== ROOT) {
    response.writeHead(403).end("fora do projeto");
    return;
  }
  try {
    const info = await stat(target);
    if (!info.isFile()) throw new Error("não é arquivo");
    response.writeHead(200, {
      "content-type": TYPES[extname(target).toLowerCase()] ?? "application/octet-stream",
      "content-length": info.size,
      "cache-control": "no-store",
    });
    if (request.method === "HEAD") {
      response.end();
      return;
    }
    createReadStream(target).pipe(response);
  } catch {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" }).end("não encontrado");
  }
});

const invoked = process.argv[1] && fileURLToPath(import.meta.url) === resolve(process.argv[1]);
if (invoked) {
  const host = listenHost();
  const onListen = () => {
    // A porta anunciada é a que o sistema abriu, não a pedida: com PORT=0 elas
    // são diferentes, e um endereço errado no console custa uma depuração inteira.
    const port = server.address().port;
    console.log(listenBanner(port));
    if (shouldOpenBrowser()) openBrowser(`http://localhost:${port}/`);
  };
  if (host) server.listen(PORT, host, onListen);
  else server.listen(PORT, onListen);
}
