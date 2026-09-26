#!/usr/bin/env python3
"""Publish a static build to a Hostinger website and verify what is actually served.

Flow proven on 2026-09-25 with 17 sites (the Vercel exit): vercel.json -> .htaccess for
LiteSpeed, zip of the build, TUS upload, `deploy-static-site-archive`, then the served
files are compared byte for byte with the build. API calls go through the authenticated
`hostinger` CLI; no token is read or stored here. Only the short-lived upload credentials
stay in memory during the upload.

usage: hostinger_deploy.py --domain rabisco.net [--project .] [--dist dist/client]
                           [--spa] [--origin 82.180.153.55] [--dry-run | --verify-only]
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
from urllib.parse import quote
import urllib.request
import zipfile

CHUNK = 16 * 1024 * 1024
SKIP = {".DS_Store"}

BASE = """# Gerado de {src} para Hostinger (LiteSpeed). Não editar à mão.
Options -Indexes
AddDefaultCharset utf-8
AddType text/javascript .js .mjs
AddType application/wasm .wasm
AddType model/gltf-binary .glb
AddType model/gltf+json .gltf
AddType audio/flac .flac
AddType audio/ogg .ogg
AddType application/manifest+json .webmanifest
AddType font/woff2 .woff2
AddType text/markdown .md
"""


def load_vercel(project: Path) -> dict:
    path = project / "vercel.json"
    return json.loads(path.read_text()) if path.is_file() else {}


def htaccess_from_vercel(cfg: dict, source: str = "vercel.json", spa: bool = False) -> str:
    """Translate the vercel.json subset our games use: headers, rewrites, cleanUrls, trailingSlash."""
    out = [BASE.format(src=source if cfg else "base")]
    out.append("<IfModule mod_headers.c>")
    out.append('  Header always set X-Content-Type-Options "nosniff"')
    out.append('  Header always set Referrer-Policy "strict-origin-when-cross-origin"')
    for i, rule in enumerate(cfg.get("headers", [])):
        name = f"VRC{i}"
        out.append(f'  SetEnvIf Request_URI "^{rule["source"]}" {name}')
        for kv in rule["headers"]:
            if kv["key"].lower() in ("x-content-type-options", "referrer-policy"):
                continue
            out.append(f'  Header set {kv["key"]} "{kv["value"]}" env={name}')
    # HTML stays revalidated even when served through a rewrite.
    out.append('  <FilesMatch "\\.html?$">')
    out.append('    Header set Cache-Control "no-cache"')
    out.append("  </FilesMatch>")
    # Data files keep their name across releases (sound maps, manifests, credits): never immutable, whatever
    # vercel.json says for their folder (packs/platforms/web.md, "Imutável só com versão"). Rabisco War, 26/09:
    # /(audio|…)/(.*) served audio/sfx-map.json and voice/manifest.json as immutable for a year.
    out.append('  <FilesMatch "\\.(json|md|txt|webmanifest)$">')
    out.append('    Header set Cache-Control "no-cache"')
    out.append("  </FilesMatch>")
    out.append("</IfModule>")
    rewrites = cfg.get("rewrites", [])
    clean = cfg.get("cleanUrls", False)
    if rewrites or clean or spa:
        out.append("<IfModule mod_rewrite.c>")
        out.append("  RewriteEngine On")
        if clean:
            # Vercel answers /x.html (and /index.html) with 308 to /x; THE_REQUEST skips internal rewrites.
            out.append("  RewriteCond %{THE_REQUEST} \\s/+(.+)\\.html[\\s?] [NC]")
            out.append("  RewriteRule ^ /%1 [R=308,L]")
        if cfg.get("trailingSlash") is False:
            out.append("  RewriteCond %{REQUEST_FILENAME} !-d")
            out.append("  RewriteRule ^(.+)/$ /$1 [R=308,L]")
        for rule in rewrites:
            out.append(f'  RewriteRule ^{re.escape(rule["source"].lstrip("/"))}$ {rule["destination"]} [L]')
        if clean:
            out.append("  RewriteCond %{REQUEST_FILENAME} !-f")
            out.append("  RewriteCond %{REQUEST_FILENAME} !-d")
            out.append("  RewriteCond %{REQUEST_FILENAME}.html -f")
            out.append("  RewriteRule ^(.+)$ /$1.html [L]")
        if spa:
            out.append("  RewriteCond %{REQUEST_FILENAME} !-f")
            out.append("  RewriteCond %{REQUEST_FILENAME} !-d")
            out.append("  RewriteRule ^ /index.html [L]")
        out.append("</IfModule>")
    return "\n".join(out) + "\n"


def resolve_dist(project: Path, cfg: dict, dist: str | None) -> Path:
    return (project / (dist or cfg.get("outputDirectory") or "dist")).resolve()


def build_files(dist: Path) -> list[Path]:
    return sorted(p for p in dist.rglob("*") if p.is_file() and p.name not in SKIP)


def make_zip(dist: Path, htaccess: str | None, out: Path) -> int:
    """A .htaccess shipped in the build wins over the generated one."""
    files = build_files(dist)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files:
            z.write(p, p.relative_to(dist).as_posix())
        if htaccess and not (dist / ".htaccess").is_file():
            z.writestr(".htaccess", htaccess)
            return len(files) + 1
    return len(files)


def sample(files: list[Path], dist: Path, count: int) -> list[str]:
    """index.html plus evenly spaced files, so large assets are checked too."""
    rel = [p.relative_to(dist).as_posix() for p in files if p.name != ".htaccess"]
    picked = ["index.html"] if "index.html" in rel else []
    if rel and count:
        step = max(1, len(rel) // count)
        picked += [r for r in rel[::step] if r not in picked][:count]
    return picked


def cli(*args):
    out = subprocess.run(["hostinger", *args, "--format", "json"], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"hostinger {' '.join(args[:3])}: {(out.stderr or out.stdout).strip()[:300]}")
    return json.loads(out.stdout)


def resolve_username(domain: str) -> str:
    # A lista é paginada (25 por página): com 39 sites em 26/09, war.rabisco.net estava na página 2 e o
    # deploy dizia que o site não existia. Filtra pelo domínio (substring) e percorre as páginas.
    page = 1
    while True:
        data = cli("hosting", "websites", "list", "--domain", domain, "--page", str(page))
        sites = data.get("data", []) if isinstance(data, dict) else data
        for site in sites:
            if site.get("domain") == domain:
                return site["username"]
        meta = data.get("meta", {}) if isinstance(data, dict) else {}
        if not sites or page * int(meta.get("per_page") or len(sites)) >= int(meta.get("total") or 0):
            break
        page += 1
    sys.exit(f"site {domain} não existe na conta Hostinger (hostinger hosting websites list --domain {domain})")


def tus_upload(url: str, auth: str, rest: str, file: Path) -> str:
    size = file.stat().st_size
    base = f"{url.rstrip('/')}/{file.name}?override=true"
    hdr = {"X-Auth": auth, "X-Auth-Rest": rest, "Tus-Resumable": "1.0.0"}
    create = urllib.request.Request(base, method="POST", headers={**hdr, "Upload-Length": str(size), "Upload-Offset": "0"})
    with urllib.request.urlopen(create, timeout=120):
        pass
    offset = 0
    with open(file, "rb") as f:
        while offset < size:
            for attempt in range(3):
                f.seek(offset)
                chunk = f.read(CHUNK)
                patch = urllib.request.Request(base, data=chunk, method="PATCH", headers={
                    **hdr, "Content-Type": "application/offset+octet-stream", "Upload-Offset": str(offset)})
                try:
                    with urllib.request.urlopen(patch, timeout=600) as r:
                        offset = int(r.headers.get("Upload-Offset", offset + len(chunk)))
                    break
                except (urllib.error.URLError, TimeoutError):
                    if attempt == 2:
                        raise
                    time.sleep(3)
                    with urllib.request.urlopen(urllib.request.Request(base, method="HEAD", headers=hdr), timeout=60) as r:
                        offset = int(r.headers.get("Upload-Offset", offset))
            print(f"  upload {offset / 1e6:.1f}/{size / 1e6:.1f} MB", flush=True)
    return file.name


def fetch(domain: str, path: str, origin: str | None):
    """GET through curl; --origin pins the server over HTTP, since the certificate only exists after DNS."""
    cmd = ["curl", "-s", "-m", "120", "-D", "-", "-A", "hostinger-deploy/2"]
    scheme = "https"
    if origin:
        cmd += ["--resolve", f"{domain}:80:{origin}"]
        scheme = "http"
    r = subprocess.run(cmd + [f"{scheme}://{domain}/{quote(path.lstrip('/'))}"], capture_output=True)
    head, _, body = r.stdout.partition(b"\r\n\r\n")
    while head.startswith(b"HTTP/") and b" 100 " in head.split(b"\r\n", 1)[0]:
        head, _, body = body.partition(b"\r\n\r\n")
    lines = head.decode("latin1").split("\r\n")
    status = int(lines[0].split()[1]) if lines and lines[0].startswith("HTTP/") else 0
    headers = {k.strip().lower(): v.strip() for k, _, v in (line.partition(":") for line in lines[1:])}
    return status, headers, body


def verify(domain: str, dist: Path, paths: list[str], origin: str | None) -> list[str]:
    problems = []
    for rel in paths:
        status, headers, body = fetch(domain, "/" if rel == "index.html" else rel, origin)
        if rel == "index.html" and headers.get("platform") != "hostinger":
            problems.append(f"/ não veio da Hostinger (server={headers.get('server')}); o DNS ainda aponta para outro lugar?")
        same = hashlib.sha256(body).digest() == hashlib.sha256((dist / rel).read_bytes()).digest()
        print(f"  {rel}: {status} · {'idêntico' if same else 'DIFERENTE'} · cache-control={headers.get('cache-control')}", flush=True)
        if status != 200 or not same:
            problems.append(f"{rel}: {status}, {'idêntico' if same else 'diferente do build'}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--domain", required=True, help="site na Hostinger, ex.: rabisco.net")
    ap.add_argument("--project", default=".", help="pasta com o vercel.json (padrão: a atual)")
    ap.add_argument("--dist", help="build a publicar (padrão: outputDirectory do vercel.json ou dist)")
    ap.add_argument("--spa", action="store_true", help="rota desconhecida serve o index.html")
    ap.add_argument("--origin", help="IP da origem para conferir antes do DNS apontar para a Hostinger")
    ap.add_argument("--sample", type=int, default=8, help="arquivos conferidos por hash além do index.html")
    ap.add_argument("--dry-run", action="store_true", help="só monta o zip e o .htaccess")
    ap.add_argument("--verify-only", action="store_true", help="só confere se o site no ar serve este build")
    a = ap.parse_args(argv)

    project = Path(a.project).resolve()
    cfg = load_vercel(project)
    dist = resolve_dist(project, cfg, a.dist)
    if not (dist / "index.html").is_file():
        sys.exit(f"build ausente: {dist}/index.html (rode o build antes)")
    files = build_files(dist)
    paths = sample(files, dist, a.sample)
    if a.verify_only:
        problems = verify(a.domain, dist, paths, a.origin)
        print("CONFERIDO: o site serve este build" if not problems else "DIFERENTE:\n  " + "\n  ".join(problems))
        return 0 if not problems else 2
    htaccess = htaccess_from_vercel(cfg, "vercel.json", a.spa)
    out = Path(tempfile.gettempdir()) / f"{a.domain.replace('.', '_')}_{time.strftime('%Y%m%d_%H%M%S')}.zip"
    n = make_zip(dist, htaccess, out)
    print(f"zip: {n} arquivos, {out.stat().st_size / 1e6:.1f} MB · build {dist.relative_to(project) if dist.is_relative_to(project) else dist}")
    if a.dry_run:
        print(htaccess)
        out.unlink(missing_ok=True)
        return 0
    try:
        user = resolve_username(a.domain)
        cred = cli("hosting", "files", "generate-upload-url", "--username", user, "--domain", a.domain)
        cred = cred.get("data", cred)
        t0 = time.time()
        name = tus_upload(cred["url"], cred["auth_key"], cred["rest_auth_key"], out)
        print(f"upload concluído em {time.time() - t0:.0f}s")
        try:
            cli("hosting", "websites", "deploy-static-site-archive", user, a.domain, "--archive-path", name)
        except RuntimeError as err:
            # Above ~100 MB the synchronous answer fails while extraction finishes; never resend blindly.
            print(f"aviso: {err}. Conferindo o site antes de qualquer reenvio…", flush=True)
            time.sleep(45)
    finally:
        out.unlink(missing_ok=True)
    for attempt in range(4):
        time.sleep(5 if attempt == 0 else 30)
        problems = verify(a.domain, dist, paths, a.origin)
        if not problems:
            print(f"PUBLICADO E CONFERIDO: https://{a.domain}/ serve o build ({len(paths)} arquivos idênticos)")
            return 0
    print("PUBLICADO COM PENDÊNCIA:\n  " + "\n  ".join(problems))
    return 2


if __name__ == "__main__":
    sys.exit(main())
