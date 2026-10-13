#!/usr/bin/env python3
"""Configuração e obtenção seletiva de módulos de um workspace."""
import argparse
from fnmatch import fnmatch
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
from urllib.parse import urlsplit


def default_root():
    configured = os.environ.get("GAMES_WORKSPACE_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    framework = Path(__file__).resolve().parents[1]
    if framework.name == "framework" and (framework.parent / "AGENTS.md").is_file():
        return framework.parent
    return Path.cwd()


ROOT = default_root()


def load_config(root):
    path = Path(root) / "framework/config.json"
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("framework/config.json precisa declarar version 1")
    return data


def load_manifest(root, resolve_urls=True):
    data = json.loads((Path(root) / "workspace.json").read_text())
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("modules"), list):
        raise ValueError("workspace.json precisa declarar version 1 e uma lista modules")
    ids, paths = set(), set()
    for module in data["modules"]:
        if not isinstance(module, dict) or not all(isinstance(module.get(key), str) for key in ("id", "path")):
            raise ValueError("Módulo precisa de id e path textuais")
        path = PurePosixPath(module["path"])
        if (not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", module["id"])
                or path.is_absolute() or ".." in path.parts
                or not path.parts or str(path) != module["path"]
                or module["id"] in ids or str(path) in paths):
            raise ValueError(f"Módulo inválido ou duplicado: {module}")
        ids.add(module["id"])
        paths.add(str(path))
        if resolve_urls and "url" not in module:
            if not isinstance(module.get("repository"), str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", module["repository"]):
                raise ValueError("Nome de repositório inválido")
            base = data.get("repository_base_url") or str(data.get("repository", "")).rsplit("/", 1)[0]
            if not isinstance(base, str) or urlsplit(base).scheme not in {"https", "http", "ssh", "file"}:
                raise ValueError("Defina repository_base_url ou a URL repository no manifesto")
            module["url"] = f"{base.rstrip('/')}/{module['repository']}.git"
        if resolve_urls and (not isinstance(module["url"], str) or not module["url"] or any(c in module["url"] for c in '\r\n"')):
            raise ValueError("URL de módulo inválida")
    return data


def parent_of(module, modules):
    parents = [item for item in modules
               if module["path"].startswith(item["path"] + "/")]
    return max(parents, key=lambda item: len(item["path"]), default=None)


def selection(names, modules):
    """Módulos pedidos com seus pais e, de forma transitiva, o que cada um declara em `requires`."""
    selected, pending, seen = [], list(names), set()
    while pending:
        name = pending.pop(0)
        module = next((item for item in modules
                       if name in (item["id"], item["path"])), None)
        if module is None:
            raise ValueError(f"Módulo desconhecido: {name}. Use workspace.py list.")
        if module["id"] in seen:
            continue
        seen.add(module["id"])
        chain = []
        while module:
            chain.append(module)
            module = parent_of(module, modules)
        for item in reversed(chain):
            if item not in selected:
                selected.append(item)
            pending.extend(item.get("requires") or [])
    return selected


def owner_of(root, module, modules):
    parent = parent_of(module, modules)
    owner = Path(root) / parent["path"] if parent else Path(root)
    return owner, (Path(root) / module["path"]).relative_to(owner).as_posix()


def git_text(cwd, *args):
    result = subprocess.run(["git", "--no-optional-locks", "-C", str(cwd), *args],
                            capture_output=True, text=True, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    return result.stdout.strip() if result.returncode == 0 else None


def set_active(root, module, modules, active):
    """Liga ou desliga o módulo nesta máquina; desligado, o pull não busca mais nada dele."""
    owner, _ = owner_of(root, module, modules)
    if not (owner / ".git").exists():
        return
    key = f"submodule.{module['id']}."
    subprocess.run(["git", "-C", str(owner), "config", key + "active", str(active).lower()],
                   check=True, capture_output=True)
    if active:
        subprocess.run(["git", "-C", str(owner), "config", "--unset-all",
                        key + "fetchRecurseSubmodules"], capture_output=True)
    else:
        subprocess.run(["git", "-C", str(owner), "config", key + "fetchRecurseSubmodules", "false"],
                       check=True, capture_output=True)


def sparse_clone(root, module, modules, paths):
    """Baixa só as pastas pedidas do módulo, no commit do gitlink, com o layout de um submódulo."""
    owner, relative = owner_of(root, module, modules)
    target = Path(root) / module["path"]
    subprocess.run(["git", "-C", str(owner), "submodule", "init", "--", relative], check=True, capture_output=True)
    url = git_text(owner, "config", f"submodule.{module['id']}.url")
    commit = git_text(owner, "rev-parse", f"HEAD:{relative}")
    store = Path(git_text(owner, "rev-parse", "--path-format=absolute", "--git-common-dir")) / "modules" / module["id"]
    if not url or not commit or store.exists():
        raise ValueError(f"Não foi possível preparar o checkout parcial de {module['path']}.")
    target.mkdir(parents=True, exist_ok=True)
    git = ["git", "-c", "submodule.recurse=false"]
    subprocess.run([*git, "clone", "-q", "--no-checkout", "--depth", "1", "--filter=blob:none",
                    "--separate-git-dir", str(store), url, str(target)], check=True)
    subprocess.run([*git, "-C", str(target), "sparse-checkout", "set", "--cone", *paths], check=True)
    subprocess.run([*git, "-C", str(target), "fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", commit],
                   check=True)
    subprocess.run([*git, "-C", str(target), "checkout", "-q", "--detach", commit], check=True)
    subprocess.run(["git", "--git-dir", str(store), "config", "core.worktree",
                    os.path.relpath(target, store)], check=True)


def get_modules(root, names, modules, sparse=None):
    root = Path(root).resolve()
    sparse = sparse or {}
    for module in selection(names, modules):
        target = root / module["path"]
        if not target.resolve().is_relative_to(root):
            raise ValueError(f"Módulo fora do workspace: {module['path']}")
        owner, relative = owner_of(root, module, modules)
        check = subprocess.run(
            ["git", "-C", str(owner), "config", "-f", ".gitmodules", "--get",
             f"submodule.{module['id']}.path"], capture_output=True, text=True)
        if check.returncode or check.stdout.strip() != relative:
            raise ValueError("Checkout ainda não modularizado; use o hub preparado/publicado. "
                             f"Falta .gitmodules para {module['path']}.")
        set_active(root, module, modules, True)
        if (target / ".git").exists():
            print(f"presente: {module['path']} (versão local preservada)")
            continue
        if module["id"] in sparse:
            sparse_clone(root, module, modules, sparse[module["id"]])
            continue
        subprocess.run(
            ["git", "-C", str(owner), "-c", "submodule.recurse=false",
             "submodule", "update", "--init", "--depth", "1", "--", relative], check=True)


# Ignorados que se refazem sozinhos: não seguram um módulo na máquina.
DISPOSABLE = (".DS_Store", "__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache", ".ruff_cache",
              ".cache", "node_modules", ".venv", "venv", "dist", "*.log")
PROFILE_KEY = "workspace.profile"


def expand(entries, modules):
    """Troca cada padrão (`prototypes/*`) pelos módulos cujo caminho ou id combinam com ele."""
    found = []
    for entry in entries:
        if not any(char in entry for char in "*?["):
            found.append(entry)
            continue
        matches = [item["id"] for item in modules if fnmatch(item["path"], entry) or fnmatch(item["id"], entry)]
        if not matches:
            raise ValueError(f"Nenhum módulo combina com {entry}.")
        found.extend(matches)
    return found


def profile_names(data, names):
    profiles = data.get("profiles") or {}
    if not isinstance(profiles, dict):
        raise ValueError("profiles no workspace.json precisa ser um objeto")
    wanted = []
    for name in names:
        profile = profiles.get(name)
        if not isinstance(profile, dict) or not isinstance(profile.get("modules"), list):
            known = ", ".join(sorted(profiles)) or "nenhum"
            raise ValueError(f"Perfil desconhecido: {name}. Perfis do workspace.json: {known}.")
        wanted.extend(expand(profile["modules"], data["modules"]))
        wanted.extend(profile.get("sparse") or {})
    return wanted


def profile_sparse(data, names):
    """Pastas por módulo quando os perfis pedem só parte dele; um perfil que pede o módulo inteiro vence."""
    profiles = data.get("profiles") or {}
    sparse, whole = {}, set()
    for name in names:
        profile = profiles.get(name) or {}
        whole.update(expand(profile.get("modules") or [], data["modules"]))
        for module, paths in (profile.get("sparse") or {}).items():
            if not isinstance(paths, list) or not paths or not all(isinstance(item, str) and item for item in paths):
                raise ValueError(f"sparse de {module} no perfil {name} precisa ser uma lista de pastas")
            sparse.setdefault(module, set()).update(paths)
    by_path = {}
    for module in data["modules"]:
        for key in (module["id"], module["path"]):
            by_path[key] = module["id"]
    whole = {by_path.get(item, item) for item in whole}
    return {by_path.get(module, module): sorted(paths) for module, paths in sparse.items()
            if by_path.get(module, module) not in whole}


def disposable(entry, patterns):
    entry = entry.rstrip("/")
    return any(fnmatch(entry, pattern.rstrip("/")) or entry.startswith(pattern.rstrip("/") + "/")
               if "/" in pattern else
               any(fnmatch(part, pattern) for part in PurePosixPath(entry).parts)
               for pattern in patterns)


def local_only(path, patterns):
    """O que existe só nesta cópia e se perderia ao apagá-la; vazio quando o remoto tem tudo."""
    # O trabalho dentro de um submódulo aninhado é conferido no próprio submódulo.
    status = git_text(path, "status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=dirty")
    if status is None:
        return ["git status falhou"]
    reasons = []
    if status:
        reasons.append(f"{len(status.splitlines())} alterações locais")
    stashes = git_text(path, "stash", "list")
    if stashes:
        reasons.append(f"{len(stashes.splitlines())} stash")
    worktrees = [line[9:] for line in (git_text(path, "worktree", "list", "--porcelain") or "").splitlines()
                 if line.startswith("worktree ")][1:]
    if worktrees:
        reasons.append("worktree em " + ", ".join(worktrees))
    ahead = git_text(path, "rev-list", "--count", "HEAD", "--branches", "--not", "--remotes")
    if ahead != "0":
        reasons.append(f"{ahead} commits fora do remoto" if ahead else "commits não conferidos")
    ignored = git_text(path, "ls-files", "--others", "--ignored", "--exclude-standard", "--directory",
                       "--no-empty-directory")
    kept = [entry for entry in (ignored or "").splitlines() if entry and not disposable(entry, patterns)]
    if ignored is None or kept:
        more = f" e mais {len(kept) - 3}" if len(kept) > 3 else ""
        reasons.append("ignorados só aqui: " + ", ".join(kept[:3]) + more if kept
                       else "ignorados não conferidos")
    if not reasons and not git_text(path, "ls-remote", "--heads", "origin"):
        reasons.append("remoto inacessível")
    return reasons


def profile_plan(root, data, names):
    """Ação por módulo para deixar nesta máquina só os perfis pedidos. Não altera nada."""
    root = Path(root).resolve()
    modules = data["modules"]
    wanted = {item["id"] for item in selection(profile_names(data, names), modules)}
    patterns = DISPOSABLE + tuple(data.get("disposable") or ())
    rows = {}
    for module in sorted(modules, key=lambda item: -len(PurePosixPath(item["path"]).parts)):
        present = (root / module["path"] / ".git").exists()
        reasons = []
        if module["id"] in wanted:
            action = "manter" if present else "baixar"
        elif not present:
            action = "fora"
        else:
            reasons = local_only(root / module["path"], patterns)
            held = [row["id"] for row in rows.values()
                    if row["action"] == "preservar" and row["path"].startswith(module["path"] + "/")]
            if held:
                reasons.append("contém " + ", ".join(held))
            action = "preservar" if reasons else "remover"
        rows[module["id"]] = {"id": module["id"], "path": module["path"], "action": action,
                              "reasons": reasons}
    return [rows[module["id"]] for module in modules]


def remove_module(root, module, modules):
    """Apaga a cópia local e o histórico do módulo; o remoto continua com tudo."""
    owner, relative = owner_of(root, module, modules)
    target = Path(root) / module["path"]
    if (target / ".git").is_dir():
        shutil.rmtree(target)
        target.mkdir()
        return
    gitdir = git_text(target, "rev-parse", "--path-format=absolute", "--git-common-dir")
    store = git_text(owner, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if not gitdir or not store:
        raise ValueError(f"Histórico de {module['path']} não localizado; nada foi apagado.")
    gitdir, store = Path(gitdir), Path(store) / "modules"
    if not gitdir.resolve().is_relative_to(store.resolve()):
        raise ValueError(f"Histórico de {module['path']} fora de {store}; nada foi apagado.")
    subprocess.run(["git", "-C", str(owner), "submodule", "deinit", "-f", "-q", "--", relative],
                   check=True, capture_output=True)
    shutil.rmtree(gitdir)


def apply_profile(root, data, names, prune=False):
    root = Path(root).resolve()
    modules = data["modules"]
    by_id = {module["id"]: module for module in modules}
    rows = profile_plan(root, data, names)
    missing = [row["id"] for row in rows if row["action"] == "baixar"]
    if missing:
        get_modules(root, missing, modules, profile_sparse(data, names))
    patterns = DISPOSABLE + tuple(data.get("disposable") or ())
    for row in sorted(rows, key=lambda row: -len(PurePosixPath(row["path"]).parts)):
        module = by_id[row["id"]]
        if row["action"] == "remover" and prune:
            row["reasons"] = local_only(root / module["path"], patterns) + [
                "contém " + other["id"] for other in rows
                if other["action"] == "preservar" and other["path"].startswith(row["path"] + "/")]
            if row["reasons"]:
                row["action"] = "preservar"
            else:
                remove_module(root, module, modules)
                row["action"] = "removido"
        set_active(root, module, modules, row["action"] in ("manter", "baixar"))
    owners = {}
    for row in rows:
        if row["action"] in ("manter", "baixar"):
            owner, relative = owner_of(root, by_id[row["id"]], modules)
            owners.setdefault(owner, []).append(relative)
    for owner, paths in owners.items():
        # Sem esta lista, "git submodule update --init" sem caminho volta a baixar tudo.
        subprocess.run(["git", "-C", str(owner), "config", "--unset-all", "submodule.active"],
                       capture_output=True)
        for relative in paths:
            subprocess.run(["git", "-C", str(owner), "config", "--add", "submodule.active", relative],
                           check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "config", PROFILE_KEY, " ".join(names)],
                   check=True, capture_output=True)
    return rows


def print_plan(rows, names, applied, prune):
    counts = {}
    for row in rows:
        counts[row["action"]] = counts.get(row["action"], 0) + 1
        if row["action"] != "fora":
            note = f"  ({'; '.join(row['reasons'])})" if row["reasons"] else ""
            print(f"{row['action']:<10} {row['path']}{note}")
    print(f"\nPerfil {' + '.join(names)}: " + ", ".join(f"{count} {action}" for action, count in sorted(counts.items())))
    if not applied:
        print("Nada foi alterado. --apply liga só estes módulos nesta máquina; "
              "--apply --prune também apaga as cópias de 'remover'.")
    elif not prune and counts.get("remover"):
        print("Os módulos de 'remover' ficaram no disco, desligados; --prune apaga as cópias.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    get = sub.add_parser("get")
    get.add_argument("modules", nargs="+")
    profile = sub.add_parser("profile", help="deixa nesta máquina só os módulos dos perfis do workspace.json")
    profile.add_argument("names", nargs="*", help="perfis; sem nome, usa o perfil já aplicado aqui")
    profile.add_argument("--apply", action="store_true", help="liga só os módulos dos perfis e baixa os que faltam")
    profile.add_argument("--prune", action="store_true",
                         help="com --apply, apaga as cópias de fora dos perfis que o remoto tem por inteiro")
    profile.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        data = load_manifest(args.root)
        modules = data["modules"]
        if args.command == "get":
            get_modules(args.root, args.modules, modules)
        elif args.command == "profile":
            names = args.names or (git_text(args.root, "config", PROFILE_KEY) or "").split()
            if not names:
                known = ", ".join(sorted(data.get("profiles") or {})) or "nenhum"
                print(f"Nenhum perfil aplicado nesta máquina. Perfis do workspace.json: {known}.")
                return
            if args.prune and not args.apply:
                raise ValueError("--prune só vale com --apply")
            rows = (apply_profile(args.root, data, names, args.prune) if args.apply
                    else profile_plan(args.root, data, names))
            if args.json:
                print(json.dumps({"profiles": names, "applied": args.apply, "modules": rows},
                                 ensure_ascii=False, indent=1))
            else:
                print_plan(rows, names, args.apply, args.prune)
        else:
            modular = (args.root / ".gitmodules").is_file()
            if not modular:
                print("Migração preparada; este checkout ainda é o monólito.")
            names = (git_text(args.root, "config", PROFILE_KEY) or "").split() if modular else []
            wanted = None
            if names:
                try:
                    wanted = {item["id"] for item in selection(profile_names(data, names), modules)}
                    print(f"Perfil desta máquina: {' + '.join(names)} (workspace.py profile)")
                except ValueError as exc:
                    print(f"Perfil desta máquina ({' + '.join(names)}) não confere com o manifesto: {exc}")
            for item in modules:
                present = (args.root / item["path"] / ".git").exists()
                state = ('presente' if present else 'opcional') if modular else 'planejado'
                if wanted is not None and item["id"] not in wanted:
                    state += " fora do perfil"
                print(f"{state}: {item['id']} → {item['path']}")
    except (ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
