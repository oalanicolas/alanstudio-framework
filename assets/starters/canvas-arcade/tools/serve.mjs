// Servidor estático mínimo, sem dependências.
//
// Módulos ES não carregam por `file://`, então abrir o index.html direto no
// navegador falha. Este servidor existe só para jogar e comparar localmente.
// Não é servidor de produção: serve apenas o diretório do projeto, por método
// GET, e recusa qualquer caminho que escape dele.

import { createServer } from "node:http";
import { createReadStream } from "node:fs";
import { realpath, stat } from "node:fs/promises";
import { extname, join, normalize, sep } from "node:path";
import { fileURLToPath } from "node:url";

// `pathname` de uma URL mantém a codificação percentual: um projeto em
// "Farol do Sul" viraria "Farol%20do%20Sul", uma pasta que não existe, e todo
// pedido responderia 404. `fileURLToPath` decodifica.
const ROOT = await realpath(fileURLToPath(new URL("..", import.meta.url)));
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
  let requested;
  try {
    requested = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
    if (requested.includes("\0")) throw new URIError("caminho inválido");
  } catch {
    response.writeHead(400, { "content-type": "text/plain; charset=utf-8" }).end("URL inválida");
    return;
  }
  const relative = normalize(requested === "/" ? "index.html" : requested.replace(/^\/+/, ""));
  const target = join(ROOT, relative);
  if (!target.startsWith(ROOT + sep) && target !== ROOT) {
    response.writeHead(403).end("fora do projeto");
    return;
  }
  try {
    const actual = await realpath(target);
    if (!actual.startsWith(ROOT + sep) && actual !== ROOT) {
      response.writeHead(403).end("fora do projeto");
      return;
    }
    const info = await stat(actual);
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
    createReadStream(actual).on("error", () => response.destroy()).pipe(response);
  } catch {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" }).end("não encontrado");
  }
});

server.listen(PORT, () => {
  // A porta anunciada é a que o sistema abriu, não a pedida: com PORT=0 elas
  // são diferentes, e um endereço errado no console custa uma depuração inteira.
  console.log(`Jogo em http://localhost:${server.address().port}/  (Ctrl+C encerra)`);
});
