#!/usr/bin/env python3
"""Acervo de áudio local: importar, buscar, verificar, ouvir e exportar sem rede."""

import argparse
import array
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache, partial
import hashlib
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata
from urllib.parse import parse_qs, unquote, urlsplit
import zipfile


def default_workspace():
    here = Path(__file__).resolve()
    if here.parents[1].name == "framework" and (here.parents[2] / "AGENTS.md").is_file():
        return here.parents[2]
    return Path.cwd()


WORKSPACE = default_workspace()
LIBRARY = WORKSPACE / "shared/sfx"
LICENSES = {
    "CC0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
}
STYLES = {"recorded", "designed-modern", "instrumental"}
EXTENSIONS = {".wav", ".ogg", ".mp3", ".flac", ".m4a"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fold(value):
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold())
                   if not unicodedata.combining(c))


def inside(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or Path(relative).is_absolute():
        raise ValueError(f"Caminho fora do acervo: {relative}")
    return path


def catalog_bytes_present(root, relative):
    # O catálogo listava e a página oferecia o player.
    # Sem os bytes o clique virava 400. Nomear não é ouvir.
    try:
        path = inside(root, relative)
    except ValueError:
        return False
    return path.is_file() and not path.is_symlink()


def load_catalog(root=LIBRARY):
    path = root / "catalog.json"
    if not path.exists():
        return {"schema_version": 1, "title": "Acervo sonoro", "sounds": []}
    data = read_json(path)
    if data.get("schema_version") != 1 or not isinstance(data.get("sounds"), list):
        raise ValueError("Formato de catálogo desconhecido")
    return data


def preview_page(root=LIBRARY):
    catalog = load_catalog(root)
    rows = []
    for item in catalog.get("sounds") or []:
        if not isinstance(item, dict):
            continue
        src = item.get("file")
        if not isinstance(src, str) or not src.strip():
            continue
        licenses = sorted({
            source["license"]
            for source in item.get("sources") or []
            if isinstance(source, dict) and isinstance(source.get("license"), str)
        })
        authors = sorted({
            source["author"]
            for source in item.get("sources") or []
            if isinstance(source, dict) and isinstance(source.get("author"), str)
        })
        heading = (
            "<article>"
            f"<h2>{html.escape(str(item.get('id') or src))}</h2>"
            f"<p>{html.escape(str(item.get('title') or ''))} · "
            f"{html.escape(str(item.get('category') or ''))}</p>"
            f"<p>{html.escape(', '.join(authors))} · "
            f"{html.escape(', '.join(licenses))}</p>"
        )
        if catalog_bytes_present(root, src):
            rows.append(
                heading
                + f'<audio controls preload="none" src="/{html.escape(src, quote=True)}"></audio>'
                + "</article>"
            )
        else:
            rows.append(
                heading
                + "<p class=\"note\">O catálogo lista este som e o disco perdeu "
                "o arquivo. Nomear não é ouvir.</p>"
                + "</article>"
            )
    body = "".join(rows) if rows else "<p>Acervo vazio.</p>"
    title = catalog.get("title") if isinstance(catalog.get("title"), str) else "Acervo sonoro"
    page = (
        "<!doctype html><html lang=\"pt\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{html.escape(title)}</title>"
        "<style>body{font-family:system-ui,sans-serif;margin:1.5rem;max-width:40rem}"
        "article{margin:1.25rem 0;padding-bottom:1rem;border-bottom:1px solid #ccc}"
        "audio{width:100%}.note{color:#444}</style></head><body>"
        f"<h1>{html.escape(title)}</h1>"
        "<p class=\"note\">Tocar nesta página não é mix ouvida no jogo.</p>"
        f"{body}</body></html>\n"
    )
    return page.encode()


def validate_metadata(item):
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,95}", item.get("id", "")):
        raise ValueError("ID inválido: use 3–96 letras minúsculas, números, ponto, _ ou -")
    for key in ("title", "category", "processing"):
        if not isinstance(item.get(key), str) or not item[key].strip():
            raise ValueError(f"{item['id']}: falta {key}")
    if item.get("style") not in STYLES:
        raise ValueError(f"{item['id']}: estilo não aceito; sem 8-bit ou retrô")
    if (not isinstance(item.get("tags"), list) or not item["tags"]
            or any(not isinstance(t, str) or not t.strip() for t in item["tags"])):
        raise ValueError(f"{item['id']}: tags obrigatórias")
    if re.search(r"8[- ]?bit|chiptune|bitcrush|sfxr|beep|bleep", fold(" ".join(
            [item["title"], *item["tags"]]))):
        raise ValueError(f"{item['id']}: estética incompatível com a biblioteca")
    sources = item.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError(f"{item['id']}: procedência obrigatória")
    for source in sources:
        for key in ("title", "author", "url", "license"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                raise ValueError(f"{item['id']}: origem sem {key}")
        if source["license"] not in LICENSES:
            raise ValueError(f"{item['id']}: licença não suportada: {source['license']}")
        if "kenney" in source["author"].lower():
            raise ValueError(f"{item['id']}: Kenney não é o piso de áudio novo do estúdio")
        if urlsplit(source["url"]).scheme not in {"https", "http"}:
            raise ValueError(f"{item['id']}: URL de origem inválida")


@lru_cache(maxsize=2)
def audio_tool(name):
    candidates = [shutil.which(name), f"/opt/homebrew/opt/ffmpeg-full/bin/{name}",
                  f"/usr/local/opt/ffmpeg-full/bin/{name}"]
    for candidate in dict.fromkeys(candidates):
        if candidate and Path(candidate).is_file():
            result = subprocess.run([candidate, "-version"], capture_output=True, timeout=15)
            if result.returncode == 0:
                return candidate
    raise ValueError(f"{name} funcional necessário para importar/verificar áudio")


def inspect_audio(path):
    probe = subprocess.run([
        audio_tool("ffprobe"), "-v", "error", "-select_streams", "a:0", "-show_streams",
        "-show_format", "-of", "json", str(path),
    ], capture_output=True, check=True, timeout=60)
    info = json.loads(probe.stdout)
    if not info["streams"]:
        raise ValueError(f"Sem áudio: {path.name}")
    stream = info["streams"][0]
    rate = int(stream["sample_rate"])
    bits = int(stream.get("bits_per_sample", 0))
    if rate < 44100 or (bits and bits < 16):
        raise ValueError(f"{path.name}: abaixo do piso de entrada (44,1 kHz / PCM 16-bit)")
    decoded = subprocess.run([
        audio_tool("ffmpeg"), "-v", "error", "-xerror", "-i", str(path), "-map", "0:a:0",
        "-f", "f32le", "-acodec", "pcm_f32le", "-",
    ], capture_output=True, check=True, timeout=120)
    samples = array.array("f", decoded.stdout)
    if sys.byteorder != "little":
        samples.byteswap()
    if not samples:
        raise ValueError(f"Áudio vazio: {path.name}")
    peak = max(map(abs, samples))
    if not math.isfinite(peak) or peak < 0.00001:
        raise ValueError(f"Áudio silencioso/inválido: {path.name}")
    rms = math.sqrt(sum(x * x for x in samples) / len(samples))
    if not math.isfinite(rms):
        raise ValueError(f"Amostras não finitas: {path.name}")
    width = max(1, math.ceil(len(samples) / 72))
    waveform = [round(max(map(abs, samples[i:i + width])) / peak, 4)
                for i in range(0, len(samples), width)]
    peak_db = round(20 * math.log10(peak), 2)
    return {
        "duration": round(len(samples) / int(stream["channels"]) / rate, 4),
        "sample_rate": rate, "channels": int(stream["channels"]),
        "codec": stream["codec_name"], "bits_per_sample": bits or None,
        "bit_rate": int(stream.get("bit_rate", info["format"].get("bit_rate", 0))),
        "peak_dbfs": peak_db, "rms_dbfs": round(20 * math.log10(rms), 2),
        "waveform": waveform,
        "warnings": ["Pico decodificado próximo de 0 dBFS; conferir ganho no jogo"]
        if peak_db > -0.1 else [],
    }


def prepare_import(path, metadata):
    item = dict(metadata)
    item.pop("local_path", None)
    validate_metadata(item)
    if path.suffix.lower() not in EXTENSIONS:
        raise ValueError(f"Formato não suportado: {path.suffix}")
    data = path.read_bytes()
    sha = digest(data)
    if item.get("expected_sha256") and item["expected_sha256"] != sha:
        raise ValueError(f"{item['id']}: arquivo mudou desde a seleção")
    item.pop("expected_sha256", None)
    item.update(sha256=sha, bytes=len(data), file=f"files/{sha}{path.suffix.lower()}",
                technical=inspect_audio(path),
                review="Triagem documental e técnica; ouvir no contexto do jogo")
    return item, data


def save_imports(prepared, root=LIBRARY):
    catalog = load_catalog(root)
    sounds = catalog["sounds"]
    added = duplicates = 0
    pending = {}
    for item, data in prepared:
        by_id = next((s for s in sounds if item["id"] == s["id"]
                      or item["id"] in s.get("aliases", [])), None)
        if by_id and by_id["sha256"] != item["sha256"]:
            raise ValueError(f"ID já usado para outro áudio: {item['id']}")
        existing = next((s for s in sounds if s["sha256"] == item["sha256"]), None)
        if existing:
            if item["processing"] != existing["processing"]:
                histories = existing.setdefault("processing_history", [])
                if item["processing"] not in histories:
                    histories.append(item["processing"])
            for source in item["sources"]:
                if source not in existing["sources"]:
                    existing["sources"].append(source)
            if item["id"] != existing["id"]:
                existing["aliases"] = sorted(set(existing.get("aliases", []) + [item["id"]]))
            existing["tags"] = sorted(set(existing["tags"] + item["tags"]))
            duplicates += 1
        else:
            sounds.append(item)
            pending[item["file"]] = data
            added += 1
    for relative, data in pending.items():
        target = inside(root, relative)
        if target.exists() and target.read_bytes() != data:
            raise ValueError(f"Arquivo canônico alterado: {relative}")
    root.mkdir(parents=True, exist_ok=True)
    for relative, data in pending.items():
        target = inside(root, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_bytes(data)
    catalog["sounds"] = sorted(sounds, key=lambda s: (s["category"], s["title"], s["id"]))
    temporary = root / "catalog.json.tmp"
    temporary.write_bytes(json_bytes(catalog))
    temporary.replace(root / "catalog.json")
    return {"added": added, "duplicates_reused": duplicates, "total": len(sounds)}


def search(sounds, query="", category=None, license_id=None):
    terms = fold(query).split()
    return [s for s in sounds if
            (not category or fold(s["category"]) == fold(category))
            and (not license_id or all(x["license"] == license_id for x in s["sources"]))
            and all(term in fold(" ".join([s["id"], s["title"], s["category"],
                                           *s["tags"], *s.get("aliases", [])])) for term in terms)]


def select(sounds, ids):
    lookup = {key: s for s in sounds for key in [s["id"], *s.get("aliases", [])]}
    missing = sorted(set(ids) - lookup.keys())
    if missing or not ids:
        raise ValueError(f"Seleção vazia ou IDs desconhecidos: {', '.join(missing)}")
    return sorted({lookup[key]["id"]: lookup[key] for key in ids}.values(), key=lambda s: s["id"])


def export_payload(items, root=LIBRARY):
    payload, entries = {}, []
    credits = ["Áudio — acervo compartilhado Games", "",
               "Incorporar os créditos CC BY à tela/página de créditos do jogo.",
               "A exportação preserva os bytes disponíveis, sem processamento adicional.", ""]
    for item in items:
        validate_metadata(item)
        data = inside(root, item["file"]).read_bytes()
        if digest(data) != item["sha256"]:
            raise ValueError(f"Integridade inválida: {item['id']}")
        name = item["id"] + Path(item["file"]).suffix
        payload[name] = data
        entry = {k: v for k, v in item.items() if k not in {"file", "technical"}}
        entry["src"] = name
        entries.append(entry)
        credits += [f"{item['title']} ({name})"]
        for source in item["sources"]:
            credits += [f"  {source['title']} — {source['author']}", f"  {source['url']}",
                        f"  {source['license']} — {LICENSES[source['license']]}"]
        credits += [f"  Processamento herdado: {item['processing']}"]
        credits += [f"  Histórico adicional: {s}" for s in item.get("processing_history", [])]
        credits.append("")
    payload["manifest.json"] = json_bytes({"schema_version": 1, "files": entries})
    payload["CREDITS.txt"] = ("\n".join(credits) + "\n").encode()
    return payload


def export_files(items, destination, root=LIBRARY):
    destination = destination.resolve()
    if destination.is_relative_to(root.resolve()) or root.resolve().is_relative_to(destination):
        raise ValueError("Exporte em uma pasta de assets separada do acervo")
    payload = export_payload(items, root)
    if destination.exists():
        if not destination.is_dir():
            raise ValueError("Destino não é uma pasta")
        present = {p.name for p in destination.iterdir()}
        if present and (present != payload.keys() or any(
                not (destination / n).is_file() or (destination / n).is_symlink()
                or (destination / n).read_bytes() != data for n, data in payload.items())):
            raise ValueError("Destino contém arquivos diferentes; escolha uma pasta nova")
        if present:
            return {"files": len(items), "status": "already_exported", "destination": str(destination)}
    destination.mkdir(parents=True, exist_ok=True)
    for name, data in payload.items():
        (destination / name).write_bytes(data)
    return {"files": len(items), "status": "exported", "destination": str(destination)}


def check(root=LIBRARY, decode=False):
    sounds = load_catalog(root)["sounds"]
    if not sounds:
        raise ValueError("Catálogo vazio")
    ids, hashes = set(), set()
    errors, warnings = [], []
    for item in sounds:
        try:
            validate_metadata(item)
            for key in [item["id"], *item.get("aliases", [])]:
                if key in ids:
                    raise ValueError(f"ID/alias duplicado: {key}")
                ids.add(key)
            if item["sha256"] in hashes:
                raise ValueError(f"Bytes duplicados: {item['id']}")
            hashes.add(item["sha256"])
            path = inside(root, item["file"])
            if path.parent != root.resolve() / "files" or path.stem != item["sha256"]:
                raise ValueError(f"Caminho canônico inválido: {item['id']}")
            data = path.read_bytes()
            if digest(data) != item["sha256"] or len(data) != item["bytes"]:
                raise ValueError(f"Integridade inválida: {item['id']}")
            measured = inspect_audio(path) if decode else item["technical"]
            if measured["sample_rate"] < 44100 or measured["duration"] <= 0:
                raise ValueError(f"Metadados técnicos inválidos: {item['id']}")
            if decode and measured != item["technical"]:
                raise ValueError(f"Medição divergente: {item['id']}")
            warnings += [{"id": item["id"], "notice": w} for w in measured["warnings"]]
        except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
            errors.append(str(error))
    return {"ok": not errors, "sounds": len(sounds), "bytes": sum(s["bytes"] for s in sounds),
            "decoded": decode, "errors": errors, "warnings": warnings}


class CatalogHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, root=LIBRARY, **kwargs):
        self.root = root
        super().__init__(*args, **kwargs)

    def log_message(self, *_):
        pass

    def do_HEAD(self):
        self.respond(head=True)

    def do_GET(self):
        self.respond()

    def respond(self, head=False):
        url = urlsplit(self.path)
        path = unquote(url.path)
        content_type = "application/octet-stream"
        filename = None
        try:
            if path in {"/", "/index.html", "/catalog.js", "/catalog.css"}:
                name = "index.html" if path == "/" else path[1:]
                ui = self.root / "ui" / name
                if ui.is_file() and not ui.is_symlink():
                    data = ui.read_bytes()
                    content_type = {".html": "text/html", ".js": "text/javascript",
                                    ".css": "text/css"}[Path(name).suffix] + "; charset=utf-8"
                elif name == "index.html":
                    data = preview_page(self.root)
                    content_type = "text/html; charset=utf-8"
                else:
                    self.send_error(404)
                    return
            elif path == "/catalog.json":
                data = (self.root / "catalog.json").read_bytes()
                content_type = "application/json; charset=utf-8"
            elif path.startswith("/files/"):
                allowed = {s["file"] for s in load_catalog(self.root)["sounds"]}
                if path[1:] not in allowed:
                    self.send_error(404)
                    return
                data = inside(self.root, path[1:]).read_bytes()
                content_type = {".wav": "audio/wav", ".mp3": "audio/mpeg", ".ogg": "audio/ogg",
                                ".flac": "audio/flac", ".m4a": "audio/mp4"}[Path(path).suffix]
            elif path == "/export":
                ids = parse_qs(url.query).get("ids", [""])[0].split(",")
                selected = select(load_catalog(self.root)["sounds"], ids)
                payload = export_payload(selected, self.root)
                output = io.BytesIO()
                with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
                    for name, content in payload.items():
                        archive.writestr(name, content)
                data, content_type, filename = output.getvalue(), "application/zip", "sons-selecionados.zip"
            else:
                self.send_error(404)
                return
        except (ValueError, KeyError, OSError) as error:
            self.send_error(400, str(error).encode("ascii", "replace").decode())
            return
        total, start, end, status = len(data), 0, len(data) - 1, 200
        byte_range = self.headers.get("Range")
        if byte_range and path.startswith("/files/"):
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", byte_range)
            if not match or not any(match.groups()):
                self.send_error(416)
                return
            left, right = match.groups()
            if left:
                start, end = int(left), min(int(right), end) if right else end
            else:
                start = max(0, total - int(right))
            if start >= total or end < start:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{total}")
                self.end_headers()
                return
            data, status = data[start:end + 1], 206
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Accept-Ranges", "bytes")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{total}")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        if not head:
            self.wfile.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    search_parser = commands.add_parser("search", help="Buscar sem acessar a rede")
    search_parser.add_argument("query", nargs="?", default="")
    search_parser.add_argument("--category")
    search_parser.add_argument("--license", choices=LICENSES)
    search_parser.add_argument("--json", action="store_true")
    commands.add_parser("info").add_argument("id")
    commands.add_parser("check").add_argument("--decode", action="store_true")
    export_parser = commands.add_parser("export")
    export_parser.add_argument("ids", nargs="+")
    export_parser.add_argument("--to", type=Path, required=True)
    import_parser = commands.add_parser("import")
    import_parser.add_argument("file", type=Path)
    import_parser.add_argument("--metadata", type=Path, required=True)
    commands.add_parser("seed", help="Importar selection.json; somente arquivos locais")
    commands.add_parser("serve").add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    try:
        catalog = load_catalog()
        if args.command == "search":
            result = search(catalog["sounds"], args.query, args.category, args.license)
            if not args.json:
                for item in result:
                    print(f"{item['id']} | {item['title']} | {item['category']} | "
                          f"{item['technical']['duration']:.2f}s")
                print(f"{len(result)} som(ns)")
                return
        elif args.command == "info":
            result = select(catalog["sounds"], [args.id])[0]
        elif args.command == "check":
            result = check(decode=args.decode)
        elif args.command == "export":
            result = export_files(select(catalog["sounds"], args.ids), args.to)
        elif args.command == "import":
            result = save_imports([prepare_import(args.file, read_json(args.metadata))])
        elif args.command == "seed":
            selection = read_json(LIBRARY / "selection.json")
            with ThreadPoolExecutor(max_workers=4) as workers:
                prepared = list(workers.map(lambda s: prepare_import(
                    inside(WORKSPACE, s["local_path"]), s), selection["sounds"]))
            result = save_imports(prepared)
        elif args.command == "serve":
            if not catalog["sounds"]:
                raise ValueError("Catálogo vazio")
            server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(CatalogHandler, root=LIBRARY))
            print(f"Acervo sonoro: http://127.0.0.1:{args.port}", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
            return
        print(json_bytes(result).decode(), end="")
        if args.command == "check" and not result["ok"]:
            raise SystemExit(1)
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
