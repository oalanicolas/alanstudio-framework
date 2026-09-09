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
  server.listen(PORT, () => {
    // A porta anunciada é a que o sistema abriu, não a pedida: com PORT=0 elas
    // são diferentes, e um endereço errado no console custa uma depuração inteira.
    const origin = `http://localhost:${server.address().port}`;
    console.log(
      `Jogo em ${origin}/  (Ctrl+C encerra)\nLook: ${origin}/?look=dusk\nChuva: ${origin}/?spawn=dusk`,
    );
    if (shouldOpenBrowser()) openBrowser(`${origin}/`);
  });
}
