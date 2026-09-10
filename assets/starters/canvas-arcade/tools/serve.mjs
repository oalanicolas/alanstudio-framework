// Servidor estático mínimo, sem dependências.
//
// Módulos ES não carregam por `file://`, então abrir o index.html direto no
// navegador falha. Este servidor existe só para jogar e comparar localmente.
// Não é servidor de produção: serve apenas o diretório do projeto, por método
// GET, e recusa qualquer caminho que escape dele.

import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { networkInterfaces } from "node:os";
import { extname, join, normalize, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

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

export function listenBanner(port, interfaces = networkInterfaces(), env = process.env) {
  const origins = advertisedOrigins(port, interfaces, env);
  const local = origins[0];
  const lines = [
    `Jogo em ${local}/  (Ctrl+C encerra)`,
    `Look: ${local}/?look=dusk`,
    `Chuva: ${local}/?spawn=dusk  ${local}/?spawn=calm`,
    `Convite: ${local}/?invite=1`,
  ];
  for (const origin of origins.slice(1)) {
    lines.push(`Rede: ${origin}/`);
    lines.push(`Convite na rede: ${origin}/?invite=1`);
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
const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
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
  if (request.method !== "GET" && request.method !== "HEAD") {
    response.writeHead(405, { allow: "GET, HEAD" }).end();
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
