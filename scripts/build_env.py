"""Ambiente de build de um site publicado: o que o workspace.json declara em "deploy.env".

Origem: sites publicados por deploy foram ao ar sem VITE_SUPABASE_URL e
VITE_SUPABASE_PUBLISHABLE_KEY. O build do deploy roda numa cópia limpa, sem os arquivos
.env*, e o Vite compila sem erro com a variável ausente: placar e comunidade saíram do ar
sem nenhum aviso. Desde então uma variável que o build usa é declarada, resolvida antes do
build e conferida no build antes do envio.

"env": {"NOME": "valor"}  valor fixo, versionado; só configuração pública ("" desliga de propósito)
"env": {"NOME": null}     vem da máquina (ambiente ou .env* do módulo), nunca do Git; obrigatória
Toda variável VITE_ com valor vai para o cliente, então o build publicado tem de contê-la.
"""
import os
from pathlib import Path
import re

NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
# Ordem do Vite no modo production: o primeiro arquivo que define a variável vence.
ENV_FILES = (".env.production.local", ".env.local", ".env.production", ".env")
# Todas as formas que o Vite substitui: env.X, env?.X, env["X"], `const { X } = import.meta.env`
# e %X% no HTML. Nome que escapa daqui volta a ser a falha muda.
REFERENCE = re.compile(r"import\.meta\.env\??\.(VITE_[A-Z0-9_]+)")
BRACKET = re.compile(r"""import\.meta\.env\??\.?\[\s*["'`](VITE_[A-Z0-9_]+)["'`]\s*\]""")
DESTRUCTURED = re.compile(r"\{([^{}]*)\}\s*=\s*import\.meta\.env\b")
HTML_REFERENCE = re.compile(r"%(VITE_[A-Z0-9_]+)%")
VITE_NAME = re.compile(r"\bVITE_[A-Z0-9_]+\b")
# Chave literal de `define` no vite.config: a própria configuração fornece o valor.
DEFINED = re.compile(r"""["'`]import\.meta\.env\.(VITE_[A-Z0-9_]+)["'`]\s*:""")
SOURCE_SUFFIXES = {".js", ".mjs", ".cjs", ".ts", ".mts", ".tsx", ".jsx", ".vue", ".svelte", ".html"}
# Fora: dependências, saída do bundler e código que não vai ao cliente (testes, QA, docs).
SKIP_DIRS = {"node_modules", "dist", "coverage", "tests", "test", "qa", "docs"}
BUILD_SUFFIXES = {".js", ".mjs", ".html"}


def declared(config):
    """Valida e devolve o "env" do deploy: {nome: str | None}."""
    env = (config or {}).get("env", {})
    if not isinstance(env, dict) or not all(isinstance(k, str) and NAME.match(k) for k in env) or not all(
            v is None or isinstance(v, str) for v in env.values()):
        raise ValueError('deploy.env inválido: use {"NOME": "valor fixo"} ou {"NOME": null} para vir da máquina')
    return env


def read_dotenv(path):
    values = {}
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.removeprefix("export ").partition("=")
        key, value = key.strip(), value.strip()
        if not sep or not NAME.match(key):
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        else:
            value = value.split(" #", 1)[0].rstrip()
        values[key] = value
    return values


def resolve(config, checkout, environ=None):
    """(valores, fontes, ausentes). O valor fixo do workspace.json vence; o que vem da máquina sai
    do ambiente e depois dos .env* do checkout do módulo, lidos só nas variáveis declaradas."""
    environ = os.environ if environ is None else environ
    env = declared(config)
    files = [(name, read_dotenv(Path(checkout) / name)) for name in ENV_FILES if (Path(checkout) / name).is_file()]
    values, sources, missing = {}, {}, []
    for key, fixed in env.items():
        if fixed is not None:
            values[key], sources[key] = fixed, "workspace.json"
            continue
        if environ.get(key):
            values[key], sources[key] = environ[key], "ambiente"
            continue
        found = next(((name, data[key]) for name, data in files if data.get(key)), None)
        if not found:
            missing.append(key)
        elif "${" in found[1]:
            # O Vite expande ${OUTRA} no .env; aqui o valor iria literal para o build.
            missing.append(f"{key} (usa ${{…}} em {found[0]}; escreva o valor)")
        else:
            sources[key], values[key] = found
    return values, sources, missing


def expected(values):
    """O que o build publicado tem de conter: toda VITE_ com valor."""
    return {key: value for key, value in values.items() if key.startswith("VITE_") and value}


def referenced(tree):
    """VITE_ que o código-fonte lê e a configuração do Vite não define sozinha."""
    found, defined = set(), set()
    for folder, dirs, names in os.walk(tree):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in names:
            path = Path(folder) / name
            if path.suffix not in SOURCE_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            found.update(REFERENCE.findall(text))
            found.update(BRACKET.findall(text))
            for names in DESTRUCTURED.findall(text):
                found.update(VITE_NAME.findall(names))
            if path.suffix == ".html":
                found.update(HTML_REFERENCE.findall(text))
            if name.startswith("vite.config."):
                defined.update(DEFINED.findall(text))
    return found - defined


def missing_in_build(dist, expectations):
    """Nomes cujo valor não aparece em nenhum .js/.html do build."""
    pending = {key: value.encode() for key, value in expectations.items()}
    for folder, dirs, names in os.walk(dist):
        dirs[:] = [d for d in dirs if d not in {"node_modules", ".git"}]
        for name in names:
            if not pending:
                return []
            if Path(name).suffix in BUILD_SUFFIXES:
                data = (Path(folder) / name).read_bytes()
                pending = {key: value for key, value in pending.items() if value not in data}
    return sorted(pending)
