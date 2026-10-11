#!/usr/bin/env python3
"""Publish a static build to a Hostinger website and verify what is actually served.

Flow: vercel.json -> .htaccess for
LiteSpeed, zip of the build, TUS upload, `deploy-static-site-archive`, then the served
files are compared byte for byte with the build. API calls go through the authenticated
`hostinger` CLI; no token is read or stored here. Only the short-lived upload credentials
stay in memory during the upload.

usage: hostinger_deploy.py --domain example.com [--project .] [--dist dist/client]
                           [--spa] [--block-ai-bots] [--origin <IP do servidor>] [--expect NOME=VALOR]
                           [--dry-run | --verify-only]

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
AI_BOTS = ("GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User",
           "Claude-SearchBot", "PerplexityBot", "Perplexity-User")
AI_BOT_RULES = """# Block declared AI agents before application routing, including direct asset requests.
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{REQUEST_URI} ^/robots\\.txt$
  RewriteRule ^robots\\.txt$ - [L]
  RewriteCond %{HTTP_USER_AGENT} "(""" + "|".join(AI_BOTS) + """)" [NC]
  RewriteRule ^ - [E=BLOCK_AI:1,F,L]
</IfModule>
"""
AI_BOT_HEADERS = """# FilesMatch merges after application-level header rules.
<IfModule mod_headers.c>
  Header always append Vary "User-Agent"
  <FilesMatch ".*">
    Header always set Cache-Control "no-store" env=BLOCK_AI
  </FilesMatch>
</IfModule>
"""

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


def block_ai_robots(text: str) -> str:
    output, group, agents = [], [], []
    has_records = False
    selected = {bot.lower() for bot in AI_BOTS}

    def record(line):
        key, _, value = line.split("#", 1)[0].strip().partition(":")
        return key.strip().lower(), value.strip().lower()

    def finish():
        if not agents or any(agent not in selected for agent in agents):
            for line in group:
                key, value = record(line)
                if key != "user-agent" or value not in selected:
                    output.append(line)
        else:
            output.extend(line for line in group if record(line)[0] == "sitemap")

    for line in text.lstrip("\ufeff").splitlines():
        key, value = record(line)
        if key == "user-agent":
            if has_records:
                finish()
                group, agents, has_records = [], [], False
            elif not agents:
                output.extend(group)
                group = []
            agents.append(value)
        elif key in ("allow", "disallow") and agents:
            has_records = True
        group.append(line)
    if agents and not has_records and any(agent not in selected for agent in agents):
        # Blank lines do not end a group; an empty rule prevents inheriting the next agent's denial.
        group.append("Disallow:")
    finish()
    return "\n".join(output).rstrip() + "\n\n" + "\n".join(
        f"User-agent: {bot}\nDisallow: /\n" for bot in AI_BOTS)


def make_zip(dist: Path, htaccess: str | None, out: Path, project: Path | None = None,
             block_ai_bots: bool = False) -> int:
    """Keep application routing and auth; optional crawler rules run before them."""
    files = build_files(dist, project)
    extra = {}
    own_rules = dist / ".htaccess"
    if block_ai_bots:
        for rules in (path for path in files if path.name == ".htaccess"):
            text = re.sub(r"\\\r?\n", "", rules.read_text())
            modes = re.findall(r"(?im)^\s*RewriteEngine\s+([^\s#]+)", text)
            if any(mode.strip("\"'").lower() != "on" for mode in modes) or re.search(r"(?im)^\s*<If(?:\s|>)", text):
                raise ValueError(f"{rules.relative_to(dist)}: block_ai_bots incompatível com RewriteEngine diferente de On "
                                 "ou <If> condicional; ajuste a configuração antes de publicar. Nada foi enviado")
        extra[".htaccess"] = (AI_BOT_RULES + (own_rules.read_text() if own_rules in files else htaccess or "")
                              + "\n" + AI_BOT_HEADERS)
        robots = dist / "robots.txt"
        text = robots.read_text() if robots in files else ""
        extra["robots.txt"] = block_ai_robots(text)
    elif htaccess and not own_rules.is_file():
        extra[".htaccess"] = htaccess
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files:
            rel = p.relative_to(dist).as_posix()
            if rel in extra:
                z.writestr(rel, extra.pop(rel))
            elif block_ai_bots and p.name == ".htaccess":
                z.writestr(rel, AI_BOT_RULES + p.read_text() + "\n" + AI_BOT_HEADERS)
            else:
                z.write(p, rel)
        for rel, text in extra.items():
            z.writestr(rel, text)
        return len(z.namelist())


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


def fetch(domain: str, path: str, origin: str | None, user_agent: str = "hostinger-deploy/2"):
    """GET through curl; --origin pins the server over HTTP, since the certificate only exists after DNS."""
    cmd = ["curl", "-s", "-m", "120", "-D", "-", "-A", user_agent]
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


def load_verification(project: Path, dist: Path) -> dict:
    """Executable responses have an explicit contract; public files retain byte checks."""
    path = project / "deploy-verification.json"
    if not path.is_file():
        return {}
    cfg = json.loads(path.read_text())
    if not isinstance(cfg, dict) or set(cfg) - {"version", "responses", "protected_inventory"} or cfg.get("version") != 1:
        raise ValueError("deploy-verification.json: contrato inválido")
    if not isinstance(cfg.get("responses", {}), dict):
        raise ValueError("responses: objeto esperado")
    responses = dict(cfg.get("responses", {}))
    inventory = cfg.get("protected_inventory")
    if inventory:
        if set(inventory) - {"file", "files_key", "public_key", "response", "patterns", "unlisted_response"} or not {"file", "files_key", "public_key", "response"} <= set(inventory):
            raise ValueError("protected_inventory: campos inválidos")
        inventory_path = checked_path(inventory["file"])
        data = json.loads((dist / inventory_path).read_text())
        files, public = data[inventory["files_key"]], data[inventory["public_key"]]
        if not isinstance(files, dict) or not files or not isinstance(public, list) or not set(public) <= set(files):
            raise ValueError("protected_inventory: inventário ou lista pública inválida")
        patterns = inventory.get("patterns", [])
        if not isinstance(patterns, list):
            raise ValueError("protected_inventory: patterns inválido")
        for pattern in patterns:
            checked_path(pattern)
        public_paths = {name.lstrip("/") for name in public}
        derived = {}
        for file in build_files(dist):
            rel = file.relative_to(dist).as_posix()
            if rel not in public_paths and any(fnmatch.fnmatch(rel, pattern) for pattern in patterns):
                derived[rel] = inventory.get("unlisted_response", inventory["response"])
        for name in files:
            rel = checked_path(name.lstrip("/"))
            if not (dist / rel).is_file():
                raise ValueError(f"protected_inventory: arquivo ausente {rel}")
            if name not in public:
                derived[rel] = inventory["response"]
        responses = {**derived, **responses}
    for rel, rule in responses.items():
        checked_path(rel)
        if rel in ("index.html", "build.json"):
            raise ValueError(f"{rel}: identificação do build exige hash, sem override")
        allowed = {"status", "headers", "json_values", "json_types"}
        if not isinstance(rule, dict) or set(rule) - allowed or type(rule.get("status")) is not int or not 200 <= rule["status"] <= 599:
            raise ValueError(f"{rel}: resposta inválida")
        headers = rule.get("headers")
        if not isinstance(headers, dict) or not headers:
            raise ValueError(f"{rel}: declare os cabeçalhos esperados")
        for key, value in headers.items():
            if not isinstance(key, str) or key != key.lower() or not isinstance(value, list) or not value or not all(isinstance(v, str) and v for v in value):
                raise ValueError(f"{rel}: cabeçalho inválido")
        for field in ("json_values", "json_types"):
            if not isinstance(rule.get(field, {}), dict) or any(not isinstance(key, str) or not key or any(not part for part in key.split(".")) for key in rule.get(field, {})):
                raise ValueError(f"{rel}: {field} inválido")
        if any(t not in ("boolean", "string", "object", "array", "number", "null") for t in rule.get("json_types", {}).values()):
            raise ValueError(f"{rel}: tipo JSON inválido")
    return responses


def checked_path(rel: str) -> str:
    if not isinstance(rel, str) or not rel or rel.startswith("/") or any(p in (".", "..", "") for p in rel.split("/")) or any(c in rel for c in "\\?#\r\n"):
        raise ValueError("deploy-verification.json: caminho inválido")
    return rel


def response_problems(status: int, headers: dict, body: bytes, rule: dict) -> list[str]:
    problems = []
    if status != rule["status"]:
        problems.append(f"status {status}, esperado {rule['status']}")
    if b"<?php" in body.lower() or b"<?=" in body:
        problems.append("código PHP exposto")
    for key, values in rule["headers"].items():
        value = headers.get(key, "").lower()
        if key == "cache-control":
            present = {part.strip() for part in value.split(",")}
            valid = all(expected.lower() in present for expected in values)
            if {"private", "no-store"} & set(values) and ("public" in present or "immutable" in present):
                valid = False
        else:
            valid = all(value.startswith(expected.lower()) for expected in values)
        if not valid:
            problems.append(f"cabeçalho {key} fora do contrato")
    if "json_values" in rule or "json_types" in rule:
        try:
            data = json.loads(body)
            types = {"boolean": bool, "string": str, "object": dict, "array": list,
                     "number": (int, float), "null": type(None)}
            for field, expected in rule.get("json_values", {}).items():
                actual = data
                for part in field.split("."):
                    actual = actual[part]
                if type(actual) is not type(expected) or actual != expected:
                    problems.append(f"campo JSON {field} fora do contrato")
            for field, expected in rule.get("json_types", {}).items():
                actual = data
                for part in field.split("."):
                    actual = actual[part]
                if not isinstance(actual, types[expected]) or (expected == "number" and isinstance(actual, bool)):
                    problems.append(f"tipo JSON {field} fora do contrato")
        except (ValueError, KeyError, TypeError):
            problems.append("JSON inválido ou campo obrigatório ausente")
    return problems


def verify(domain: str, dist: Path, paths: list[str], origin: str | None,
           responses: dict | None = None) -> list[str]:
    problems = []
    responses = responses or {}
    for rel in paths:
        status, headers, body = fetch(domain, "/" if rel == "index.html" else rel, origin)
        if rel == "index.html" and headers.get("platform") != "hostinger":
            problems.append(f"/ não veio da Hostinger (server={headers.get('server')}); o DNS ainda aponta para outro lugar?")
        if rel in responses:
            failures = response_problems(status, headers, body, responses[rel])
        elif rel.endswith(".php"):
            failures = ["endpoint PHP sem contrato de resposta"]
        else:
            same = hashlib.sha256(body).digest() == hashlib.sha256((dist / rel).read_bytes()).digest()
            failures = [] if status == 200 and same else [f"{status}, {'idêntico' if same else 'diferente do build'}"]
        print(f"  {rel}: {status} · {'FALHA' if failures else 'conferido'} · cache-control={headers.get('cache-control')}", flush=True)
        problems.extend(f"{rel}: {failure}" for failure in failures)
    return problems


def verify_ai_bots(domain: str, paths: list[str], origin: str | None) -> list[str]:
    problems = []
    asset = next((p for p in paths if p not in ("index.html", "robots.txt", ".htaccess")), None)
    for bot in AI_BOTS:
        for path in ["/", *([asset] if asset else [])]:
            status, headers, _ = fetch(domain, path, origin, f"{bot}/1.0")
            print(f"  {bot} {path}: {status}", flush=True)
            if status not in (403, 429):
                problems.append(f"{bot} {path}: {status}, esperado bloqueio 403 ou 429")
            elif status == 403 and ("no-store" not in headers.get("cache-control", "").lower()
                                   or "user-agent" not in headers.get("vary", "").lower()):
                problems.append(f"{bot} {path}: 403 sem Cache-Control no-store e Vary User-Agent")
    status, _, body = fetch(domain, "robots.txt", origin)
    text = body.decode("utf-8", errors="replace")
    if status != 200 or text != block_ai_robots(text):
        problems.append(f"robots.txt: {status}, regras de agentes ausentes, conflitantes ou inacessíveis")
    return problems


def declared_deploy(domain: str, project: Path, root: str | None = None) -> dict:
    root = root or os.environ.get("GAMES_WORKSPACE_ROOT")
    # Chamado direto pelo núcleo, sem o wrapper do hub: o workspace é o ancestral com workspace.json.
    candidates = [Path(root)] if root else [Path(project).resolve(), *Path(project).resolve().parents]
    manifest = next((c / "workspace.json" for c in candidates if (c / "workspace.json").is_file()), None)
    if not manifest:
        return {}
    modules = json.loads(manifest.read_text(encoding="utf-8")).get("modules", [])
    config = next((m["deploy"] for m in modules if isinstance(m.get("deploy"), dict)
                   and m["deploy"].get("domain") == domain), None)
    config = config or {}
    if "block_ai_bots" in config and not isinstance(config["block_ai_bots"], bool):
        raise ValueError("deploy.block_ai_bots precisa ser booleano")
    return config


def declared_expectations(domain: str, project: Path, root: str | None = None):
    """Resolve declared public build values for direct deployment shortcuts."""
    config = declared_deploy(domain, project, root)
    values, _, missing = build_env.resolve(config, project)
    return build_env.expected(values), [key for key in missing if key.startswith("VITE_")]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--domain", required=True, help="site na Hostinger, ex.: example.com")
    ap.add_argument("--project", default=".", help="pasta com o vercel.json (padrão: a atual)")
    ap.add_argument("--dist", help="build a publicar (padrão: outputDirectory do vercel.json ou dist)")
    ap.add_argument("--spa", action="store_true", help="rota desconhecida serve o index.html")
    ap.add_argument("--block-ai-bots", action="store_true", help="bloqueia agentes de IA declarados em todas as rotas")
    ap.add_argument("--origin", help="IP da origem para conferir antes do DNS apontar para a Hostinger")
    ap.add_argument("--sample", type=int, default=8, help="arquivos conferidos por hash além do index.html")
    ap.add_argument("--dry-run", action="store_true", help="só monta o zip e o .htaccess")
    ap.add_argument("--verify-only", action="store_true", help="só confere se o site no ar serve este build")
    ap.add_argument("--expect", action="append", default=[], metavar="NOME=VALOR",
                    help="configuração pública que o build tem de conter (repetível); sem ela, vale o "
                         "deploy.env do domínio no workspace.json")
    a = ap.parse_args(argv)
    if any(not key or not value for key, _, value in (item.partition("=") for item in a.expect)):
        ap.error("--expect espera NOME=VALOR, com valor")

    project = Path(a.project).resolve()
    try:
        declaration = declared_deploy(a.domain, project)
    except ValueError as exc:
        ap.error(str(exc))
    block_ai_bots = a.block_ai_bots or declaration.get("block_ai_bots", False)
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
    paths = sample(files, dist, a.sample)
    try:
        responses = load_verification(project, dist)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        ap.error(f"Contrato de verificação recusado antes do upload: {exc}")
    # Explicit endpoints are always checked; inventory responses classify the static sample.
    contract_path = project / "deploy-verification.json"
    mandatory = json.loads(contract_path.read_text()).get("responses", {}) if contract_path.is_file() else {}
    paths = list(dict.fromkeys([*paths, *(["build.json"] if (dist / "build.json").is_file() else []), *mandatory]))
    if block_ai_bots:
        paths = [path for path in paths if path != "robots.txt"]
    if a.verify_only:
        problems = verify(a.domain, dist, paths, a.origin, responses)
        if block_ai_bots:
            problems += verify_ai_bots(a.domain, paths, a.origin)
        print("CONFERIDO: o site serve este build" if not problems else "DIFERENTE:\n  " + "\n  ".join(problems))
        return 0 if not problems else 2
    htaccess = htaccess_from_vercel(cfg, "vercel.json", a.spa)
    out = Path(tempfile.gettempdir()) / f"{a.domain.replace('.', '_')}_{time.strftime('%Y%m%d_%H%M%S')}.zip"
    n = make_zip(dist, htaccess, out, project, block_ai_bots=block_ai_bots)
    print(f"zip: {n} arquivos, {out.stat().st_size / 1e6:.1f} MB · build {dist.relative_to(project) if dist.is_relative_to(project) else dist}")
    if a.dry_run:
        with zipfile.ZipFile(out) as archive:
            if ".htaccess" in archive.namelist():
                print(archive.read(".htaccess").decode("utf-8"))
            if block_ai_bots:
                print(archive.read("robots.txt").decode("utf-8"))
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
        problems = verify(a.domain, dist, paths, a.origin, responses)
        if not problems and block_ai_bots:
            problems += verify_ai_bots(a.domain, paths, a.origin)
        if not problems:
            print(f"PUBLICADO E CONFERIDO: https://{a.domain}/ serve o build ({len(paths)} respostas conferidas, estáticos por hash)")
            return 0
    print("PUBLICADO COM PENDÊNCIA:\n  " + "\n  ".join(problems))
    return 2


if __name__ == "__main__":
    sys.exit(main())
