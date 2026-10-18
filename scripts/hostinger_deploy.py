#!/usr/bin/env python3
"""Publish a static build to a Hostinger website and verify what is actually served.

Flow: vercel.json -> .htaccess for
LiteSpeed, zip of the build, TUS upload, `deploy-static-site-archive`, then the served
files are compared byte for byte with the build. API calls go through the authenticated
`hostinger` CLI; no token is read or stored here. Only the short-lived upload credentials
stay in memory during the upload.

usage: hostinger_deploy.py --domain example.com [--project .] [--dist dist/client]
                           [--spa] [--block-ai-bots] [--origin <IP do servidor>]
                           [--expect NOME=VALOR] [--dry-run | --verify-only]

Before zipping, the build must contain every public variable the domain declares in
`deploy.env` of workspace.json (build_env.py); otherwise nothing is sent (exit 3).
"""
import argparse
import fnmatch
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

sys.path.insert(0, str(Path(__file__).resolve().parent))  # também quando carregado pelo caminho (testes)
import build_env

CHUNK = 16 * 1024 * 1024
SKIP = {".DS_Store", ".gitignore", ".gitattributes", ".gitmodules", ".vercelignore", ".npmrc", ".nvmrc"}
PRIVATE_DIRS = {".git", "node_modules", ".vercel"}
# --block-ai-bots (deploy.block_ai_bots no workspace.json): agentes de IA que se identificam pelo User-Agent recebem
# 403 em tudo menos o robots.txt, que lhes nega o site. É bloqueio pelo nome declarado, não pela origem do pedido.
AI_BOTS = ("GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User", "Claude-SearchBot",
           "PerplexityBot", "Perplexity-User")

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
    # vercel.json says for their folder (packs/platforms/web.md, "Imutável só com versão"). A catch-all
    # rule like /(audio|…)/(.*) served audio/sfx-map.json and voice/manifest.json as immutable for a year.
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


def ai_bots_htaccess() -> str:
    """Vai no topo do .htaccess, antes das regras do projeto: o 403 vem antes de qualquer rewrite."""
    agents = "|".join(AI_BOTS)  # só letras e hífen: nada a escapar na expressão
    return "\n".join([
        "# Robôs de IA (deploy.block_ai_bots): 403 em tudo menos o robots.txt. Gerado no deploy.",
        "<IfModule mod_setenvif.c>",
        f'  SetEnvIfNoCase User-Agent "({agents})" BLOCK_AI=1',
        "</IfModule>",
        "<IfModule mod_rewrite.c>",
        "  RewriteEngine On",
        f'  RewriteCond %{{HTTP_USER_AGENT}} "({agents})" [NC]',
        "  RewriteRule !^robots\\.txt$ - [F,L]",
        "</IfModule>",
        "<IfModule mod_headers.c>",
        '  Header always merge Vary "User-Agent"',
        '  Header always set Cache-Control "no-store" env=BLOCK_AI',
        "</IfModule>",
    ]) + "\n"


def ai_bots_robots(shipped: str = "") -> str:
    """robots.txt do build com um grupo `Disallow: /` por agente que ele ainda não nomeia."""
    named = {line.split(":", 1)[1].strip().lower() for line in shipped.splitlines()
             if line.lower().startswith("user-agent:")}
    groups = [f"User-agent: {agent}\nDisallow: /" for agent in AI_BOTS if agent.lower() not in named]
    head = shipped.rstrip("\n")
    return "\n\n".join(([head] if head else []) + groups) + "\n"


def resolve_dist(project: Path, cfg: dict, dist: str | None) -> Path:
    return (project / (dist or cfg.get("outputDirectory") or "dist")).resolve()


def ignore_patterns(project: Path) -> list[str]:
    """Padrões do .vercelignore, que a Vercel já respeitava quando o build era a raiz do projeto."""
    path = project / ".vercelignore"
    lines = path.read_text().splitlines() if path.is_file() else []
    return [line.strip().strip("/") for line in lines if line.strip() and not line.lstrip().startswith(("#", "!"))]


def ignored(rel: str, patterns: list[str]) -> bool:
    parts = rel.split("/")
    prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
    return any(fnmatch.fnmatch(prefix, pattern) or fnmatch.fnmatch(parts[i], pattern)
               for i, prefix in enumerate(prefixes) for pattern in patterns)


def build_files(dist: Path, project: Path | None = None) -> list[Path]:
    """Nunca publica Git, ambiente, dependências ou vínculo da Vercel, mesmo quando o build é a raiz."""
    patterns = ignore_patterns(project) if project and dist.resolve() == project.resolve() else []
    files = []
    for folder, dirs, names in os.walk(dist):
        # Poda na descida: node_modules e .git nem são percorridos.
        dirs[:] = [d for d in dirs if d not in PRIVATE_DIRS and not d.startswith(".env")]
        for name in names:
            p = Path(folder) / name
            rel = p.relative_to(dist).as_posix()
            if (name in SKIP or name in PRIVATE_DIRS or any(part.startswith(".env") for part in rel.split("/"))
                    or ignored(rel, patterns) or not p.is_file()):
                continue
            files.append(p)
    return sorted(files)


def served_htaccess(dist: Path, htaccess: str | None, block_ai_bots: bool = False) -> str | None:
    """A .htaccess shipped in the build wins over the generated one; the AI bot block goes on top of either."""
    shipped = dist / ".htaccess"
    text = shipped.read_text(encoding="utf-8") if shipped.is_file() else htaccess
    return ai_bots_htaccess() + (text or "") if block_ai_bots else text


def make_zip(dist: Path, htaccess: str | None, out: Path, project: Path | None = None,
             block_ai_bots: bool = False) -> int:
    files = build_files(dist, project)
    generated = {}
    final = served_htaccess(dist, htaccess, block_ai_bots)
    if final and (block_ai_bots or not (dist / ".htaccess").is_file()):
        generated[".htaccess"] = final
    if block_ai_bots:
        robots = dist / "robots.txt"
        generated["robots.txt"] = ai_bots_robots(robots.read_text(encoding="utf-8") if robots.is_file() else "")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files:
            rel = p.relative_to(dist).as_posix()
            if rel not in generated:
                z.write(p, rel)
        for rel, text in generated.items():
            z.writestr(rel, text)
    return len({p.relative_to(dist).as_posix() for p in files} | set(generated))


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
    # A lista é paginada (25 por página): numa conta com muitos sites, o domínio pode estar na página 2 e o
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


def fetch(domain: str, path: str, origin: str | None, agent: str = "hostinger-deploy/2"):
    """GET through curl; --origin pins the server over HTTP, since the certificate only exists after DNS."""
    cmd = ["curl", "-s", "-m", "120", "-D", "-", "-A", agent]
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


def verify_ai_bots(domain: str, origin: str | None) -> list[str]:
    """Cada agente recebe 403 na página inicial; o robots.txt responde a eles e lhes nega o site."""
    problems, blocked = [], 0
    for agent in AI_BOTS:
        status, headers, _ = fetch(domain, "/", origin, agent=f"Mozilla/5.0 (compatible; {agent}/1.0)")
        if status != 403:
            problems.append(f"{agent}: / respondeu {status}, esperado 403")
        elif "no-store" not in headers.get("cache-control", ""):
            problems.append(f"{agent}: 403 sem Cache-Control no-store")
        else:
            blocked += 1
    status, _, body = fetch(domain, "robots.txt", origin, agent=f"{AI_BOTS[0]}/1.0")
    missing = [agent for agent in AI_BOTS if f"User-agent: {agent}\nDisallow: /" not in body.decode("utf-8", "replace")]
    if status != 200 or missing:
        problems.append(f"robots.txt: {status}" + (f", sem Disallow para {', '.join(missing)}" if missing else ""))
    print(f"  robôs de IA: {blocked} de {len(AI_BOTS)} com 403 · robots.txt {status}", flush=True)
    return problems


def declared_expectations(domain: str, project: Path, root: str | None = None):
    """Atalho `npm run deploy` (sem --expect): o deploy.env do domínio no workspace.json, com os valores
    lidos do ambiente e dos .env* da pasta do projeto. Devolve (esperado, VITE_ sem valor)."""
    root = root or os.environ.get("GAMES_WORKSPACE_ROOT")
    # Chamado direto pelo núcleo, sem o wrapper do hub: o workspace é o ancestral com workspace.json.
    candidates = [Path(root)] if root else [Path(project).resolve(), *Path(project).resolve().parents]
    manifest = next((c / "workspace.json" for c in candidates if (c / "workspace.json").is_file()), None)
    if not manifest:
        return {}, []
    modules = json.loads(manifest.read_text(encoding="utf-8")).get("modules", [])
    config = next((m["deploy"] for m in modules if isinstance(m.get("deploy"), dict)
                   and m["deploy"].get("domain") == domain), None)
    if not config:
        return {}, []
    values, _, missing = build_env.resolve(config, project)
    return build_env.expected(values), [key for key in missing if key.startswith("VITE_")]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--domain", required=True, help="site na Hostinger, ex.: example.com")
    ap.add_argument("--project", default=".", help="pasta com o vercel.json (padrão: a atual)")
    ap.add_argument("--dist", help="build a publicar (padrão: outputDirectory do vercel.json ou dist)")
    ap.add_argument("--spa", action="store_true", help="rota desconhecida serve o index.html")
    ap.add_argument("--origin", help="IP da origem para conferir antes do DNS apontar para a Hostinger")
    ap.add_argument("--sample", type=int, default=8, help="arquivos conferidos por hash além do index.html")
    ap.add_argument("--dry-run", action="store_true", help="só monta o zip e o .htaccess")
    ap.add_argument("--verify-only", action="store_true", help="só confere se o site no ar serve este build")
    ap.add_argument("--block-ai-bots", action="store_true",
                    help="403 e robots.txt para os agentes de IA declarados (deploy.block_ai_bots)")
    ap.add_argument("--expect", action="append", default=[], metavar="NOME=VALOR",
                    help="configuração pública que o build tem de conter (repetível); sem ela, vale o "
                         "deploy.env do domínio no workspace.json")
    a = ap.parse_args(argv)
    if any(not key or not value for key, _, value in (item.partition("=") for item in a.expect)):
        ap.error("--expect espera NOME=VALOR, com valor")

    project = Path(a.project).resolve()
    cfg = load_vercel(project)
    dist = resolve_dist(project, cfg, a.dist)
    if not (dist / "index.html").is_file():
        sys.exit(f"build ausente: {dist}/index.html (rode o build antes)")
    if not a.verify_only:
        if a.expect:
            expectations, unresolved = dict(item.partition("=")[::2] for item in a.expect), []
        else:
            expectations, unresolved = declared_expectations(a.domain, project)
        absent = unresolved + build_env.missing_in_build(dist, expectations)
        if absent:
            print(f"RECUSADO: o build em {dist.name}/ não contém {', '.join(absent)} (deploy.env do "
                  "workspace.json). Refaça o build com essas variáveis; nada foi enviado.", flush=True)
            return 3
    files = build_files(dist, project)
    # com o bloqueio, o robots.txt servido é o do build mais os grupos dos agentes: confere-se em verify_ai_bots
    paths = [p for p in sample(files, dist, a.sample) if not (a.block_ai_bots and p == "robots.txt")]
    check = lambda: verify(a.domain, dist, paths, a.origin) + (
        verify_ai_bots(a.domain, a.origin) if a.block_ai_bots else [])
    if a.verify_only:
        problems = check()
        print("CONFERIDO: o site serve este build" if not problems else "DIFERENTE:\n  " + "\n  ".join(problems))
        return 0 if not problems else 2
    htaccess = htaccess_from_vercel(cfg, "vercel.json", a.spa)
    out = Path(tempfile.gettempdir()) / f"{a.domain.replace('.', '_')}_{time.strftime('%Y%m%d_%H%M%S')}.zip"
    n = make_zip(dist, htaccess, out, project, a.block_ai_bots)
    print(f"zip: {n} arquivos, {out.stat().st_size / 1e6:.1f} MB · build {dist.relative_to(project) if dist.is_relative_to(project) else dist}")
    if a.dry_run:
        print(served_htaccess(dist, htaccess, a.block_ai_bots))
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
        problems = check()
        if not problems:
            print(f"PUBLICADO E CONFERIDO: https://{a.domain}/ serve o build ({len(paths)} arquivos idênticos)")
            return 0
    print("PUBLICADO COM PENDÊNCIA:\n  " + "\n  ".join(problems))
    return 2


if __name__ == "__main__":
    sys.exit(main())
