#!/usr/bin/env python3
"""Configuração e obtenção seletiva de módulos de um workspace."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
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
    selected = []
    for name in names:
        module = next((item for item in modules
                       if name in (item["id"], item["path"])), None)
        if module is None:
            raise ValueError(f"Módulo desconhecido: {name}. Use workspace.py list.")
        chain = []
        while module:
            chain.append(module)
            module = parent_of(module, modules)
        for item in reversed(chain):
            if item not in selected:
                selected.append(item)
    return selected


def get_modules(root, names, modules):
    root = Path(root).resolve()
    for module in selection(names, modules):
        target = root / module["path"]
        if not target.resolve().is_relative_to(root):
            raise ValueError(f"Módulo fora do workspace: {module['path']}")
        parent = parent_of(module, modules)
        owner = root / parent["path"] if parent else root
        relative = target.relative_to(owner).as_posix()
        check = subprocess.run(
            ["git", "-C", str(owner), "config", "-f", ".gitmodules", "--get",
             f"submodule.{module['id']}.path"], capture_output=True, text=True)
        if check.returncode or check.stdout.strip() != relative:
            raise ValueError("Checkout ainda não modularizado; use o hub preparado/publicado. "
                             f"Falta .gitmodules para {module['path']}.")
        if (target / ".git").exists():
            print(f"presente: {module['path']} (versão local preservada)")
            continue
        subprocess.run(
            ["git", "-C", str(owner), "-c", "submodule.recurse=false",
             "submodule", "update", "--init", "--depth", "1", "--", relative], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    get = sub.add_parser("get")
    get.add_argument("modules", nargs="+")
    args = parser.parse_args()
    try:
        modules = load_manifest(args.root)["modules"]
        if args.command == "get":
            get_modules(args.root, args.modules, modules)
        else:
            modular = (args.root / ".gitmodules").is_file()
            if not modular:
                print("Migração preparada; este checkout ainda é o monólito.")
            for item in modules:
                present = (args.root / item["path"] / ".git").exists()
                state = ('presente' if present else 'opcional') if modular else 'planejado'
                print(f"{state}: {item['id']} → {item['path']}")
    except (ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
