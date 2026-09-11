#!/usr/bin/env python3
"""Prepara repositórios locais independentes a partir de um commit, sem push."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

import workspace

OVERLAYS = ("workspace.json",)


def git(repo, *args, data=None, env=None):
    result = subprocess.run(["git", "-C", str(repo), *args], input=data,
                            capture_output=True, check=True, env=env)
    return result.stdout


def entries(repo, revision):
    result = {}
    for entry in git(repo, "ls-tree", "-rz", revision).split(b"\0"):
        if entry:
            header, path = entry.split(b"\t", 1)
            mode, kind, oid = header.decode().split()
            result[path.decode()] = (mode, oid)
    return result


def blob(repo, content):
    return git(repo, "hash-object", "-w", "--stdin", data=content).decode().strip()


def module_config(children, prefix):
    text = ""
    for child in children:
        relative = child["path"][len(prefix):]
        text += (f'[submodule "{child["id"]}"]\n'
                 f'\tpath = {relative}\n\turl = {child["url"]}\n\tshallow = true\n')
    return text.encode()


def commit_snapshot(repo, files, message, identity):
    env = dict(os.environ, **identity, GIT_INDEX_FILE=str(repo / "split-index"))
    records = b"".join(f"{mode} {oid}\t{path}\0".encode()
                       for path, (mode, oid) in sorted(files.items()))
    git(repo, "update-index", "-z", "--index-info", data=records, env=env)
    tree = git(repo, "write-tree", env=env).decode().strip()
    commit = git(repo, "commit-tree", tree, data=message.encode(), env=env).decode().strip()
    git(repo, "update-ref", "refs/heads/main", commit)
    (repo / "split-index").unlink()
    return commit, tree


def inherited_ignore(source_ignore, module_path, roots):
    lines = []
    for line in source_ignore.splitlines():
        if line.startswith(module_path + "/"):
            lines.append("/" + line[len(module_path) + 1:])
        elif not line.startswith(roots):
            lines.append(line)
    return "\n".join(lines)


def publish_path(path, policy):
    if not any(path.startswith(prefix + "/") for prefix in policy.get("document_only_paths", [])):
        return True
    suffix = Path(path).suffix.lower()
    return (suffix in policy["document_extensions"]
            or (suffix in ("", ".txt")
                and Path(path).name.upper().startswith(("LICENSE", "COPYING", "CREDITS", "SOURCE", "README"))))


def publication_ignore(module_path, policy):
    lines = []
    for prefix in policy.get("document_only_paths", []):
        if prefix.startswith(module_path + "/"):
            relative = "/" + prefix[len(module_path) + 1:]
            lines.extend([relative + "/**", "!" + relative + "/**/"])
            for name in ("LICENSE", "COPYING", "CREDITS", "SOURCE", "README"):
                pattern = relative + "/**/" + "".join(f"[{char}{char.lower()}]" for char in name)
                lines.extend(["!" + pattern + "*", pattern + "*.*", "!" + pattern + "*.txt"])
            lines.extend("!" + relative + "/**/*" + suffix for suffix in policy["document_extensions"])
    if lines:
        lines.extend([".env", ".env.*", "!.env.example", "credentials*.json", "*.key", "*.pem"])
    return "\n".join(lines)


def preserve_mirror(source, output, module, commit):
    repo = output / "repositories" / (module["id"] + ".git")
    repo.parent.mkdir(parents=True, exist_ok=True)
    git(output, "init", "--bare", "--initial-branch=main", str(repo))
    source_commit = commit
    if module.get("mirror_snapshot"):
        local = source / module["path"]
        common = Path(git(local, "rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip())
        (repo / "objects/info/alternates").write_text(str(common / "objects") + "\n")
        identity = {"GIT_AUTHOR_NAME": git(source, "config", "user.name").decode().strip(),
                    "GIT_AUTHOR_EMAIL": git(source, "config", "user.email").decode().strip()}
        identity.update(GIT_COMMITTER_NAME=identity["GIT_AUTHOR_NAME"], GIT_COMMITTER_EMAIL=identity["GIT_AUTHOR_EMAIL"])
        commit, tree = commit_snapshot(repo, entries(local, source_commit),
            f"chore: preserve reference snapshot\n\nSource: {module['upstream_url']}\n"
            f"Source-commit: {source_commit}\nOriginal history retained locally; content tree unchanged.\n", identity)
        if tree != git(local, "rev-parse", source_commit + "^{tree}").decode().strip():
            raise ValueError("Árvore do espelho difere da referência original")
        git(repo, "repack", "-a", "-d", "--window=0")
        (repo / "objects/info/alternates").unlink()
    else:
        git(repo, "fetch", "--no-tags", str(source / module["path"]),
            f"{commit}:refs/heads/main")
    git(repo, "remote", "add", "origin", module["url"])
    git(repo, "fsck", "--connectivity-only", "--no-dangling")
    size = sum(int(row.split(b"\t", 1)[0].split()[3])
               for row in git(repo, "ls-tree", "-rlz", commit).split(b"\0")
               if row and row.split(b"\t", 1)[0].split()[1] == b"blob")
    return {"id": module["id"], "path": module["path"], "url": module["url"],
            "commit": commit, "tree": git(repo, "rev-parse", commit + "^{tree}").decode().strip(),
            "blob_bytes": size, "self_contained": True, "repository": str(repo),
            "mirror": True, "source_commit": source_commit, "upstream_url": module["upstream_url"]}


def prepare(source, output, revision="HEAD", overlays=None, pack=False):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.exists():
        raise ValueError(f"Destino já existe: {output}; escolha uma pasta nova.")
    manifest = workspace.load_manifest(source)
    modules = manifest["modules"]
    if overlays is None:
        overlays = workspace.load_config(source).get("module_overlays", list(OVERLAYS))
    if not isinstance(overlays, (list, tuple)) or not all(isinstance(p, str) and p for p in overlays):
        raise ValueError("module_overlays precisa ser uma lista de caminhos")
    overlay_contents = {}
    for relative in overlays:
        path = source / relative
        if Path(relative).is_absolute() or ".." in Path(relative).parts or not path.parent.resolve().is_relative_to(source):
            raise ValueError("Overlay fora do workspace")
        mode = "120000" if path.is_symlink() else "100755" if path.stat().st_mode & 0o111 else "100644"
        content = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        overlay_contents[relative] = (mode, content)
    revision = git(source, "rev-parse", f"{revision}^{{commit}}").decode().strip()
    original = entries(source, revision)
    policy = manifest.get("publication", {})
    retained = {path: value for path, value in original.items() if publish_path(path, policy)}
    excluded = {path: value for path, value in original.items() if path not in retained}
    common = Path(git(source, "rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip())
    source_ignore = git(source, "show", f"{revision}:.gitignore").decode() if ".gitignore" in original else ""
    module_roots = tuple(sorted({module["path"].split("/", 1)[0] + "/" for module in modules}))
    attributes = git(source, "show", f"{revision}:.gitattributes").decode() if ".gitattributes" in original else ""
    for module in modules:
        path = module["path"]
        if module.get("external"):
            if original.get(path, (None,))[0] != "160000":
                raise ValueError(f"Gitlink externo não encontrado: {path}")
        elif not any(name.startswith(path + "/") for name in original):
            raise ValueError(f"Subárvore não encontrada: {path}")
    output.mkdir(parents=True)
    identity = {
        "GIT_AUTHOR_NAME": git(source, "config", "user.name").decode().strip(),
        "GIT_AUTHOR_EMAIL": git(source, "config", "user.email").decode().strip(),
    }
    identity.update(GIT_COMMITTER_NAME=identity["GIT_AUTHOR_NAME"],
                    GIT_COMMITTER_EMAIL=identity["GIT_AUTHOR_EMAIL"])
    report = {"source": manifest["archive"], "source_commit": revision,
              "strategy": "local-snapshot-repositories; original history and checkout preserved",
              "published": False, "modules": [], "changed_metadata": [], "lfs": [],
              "replaced_gitlinks": [],
              "excluded_paths": [{"path": path, "mode": mode, "blob": oid}
                                 for path, (mode, oid) in excluded.items()]}
    results, reconstructed = {}, {}
    ordered = sorted(modules, key=lambda item: len(item["path"]), reverse=True)
    hub = {"id": "hub", "path": "", "url": manifest["repository"]}
    for module in [*ordered, hub]:
        path, name = module["path"], module["id"]
        if module.get("external"):
            results[name] = original[path][1]
            reconstructed[path] = original[path]
            if module.get("mirror"):
                mirror = preserve_mirror(source, output, module, original[path][1])
                report["modules"].append(mirror)
                results[name] = mirror["commit"]
                if mirror["commit"] != original[path][1]:
                    report["changed_metadata"].append(path)
                    report["replaced_gitlinks"].append({"path": path, "source_commit": original[path][1],
                                                       "commit": mirror["commit"], "tree": mirror["tree"]})
            continue
        prefix = path + "/" if path else ""
        children = [item for item in modules if workspace.parent_of(item, modules) == (module if path else None)]
        files = {key[len(prefix):]: value for key, value in retained.items()
                 if key.startswith(prefix) and not any(key == child["path"] or
                     key.startswith(child["path"] + "/") for child in children)}
        for relative, value in files.items():
            reconstructed[prefix + relative] = value
        repo = output / "repositories" / (name + ".git")
        repo.parent.mkdir(exist_ok=True)
        git(output, "init", "--bare", "--initial-branch=main", str(repo))
        (repo / "objects/info/alternates").write_text(str(common / "objects") + "\n")
        git(repo, "remote", "add", "origin", module["url"])
        changed = set()
        for child in children:
            files[child["path"][len(prefix):]] = ("160000", results[child["id"]])
        if children:
            files[".gitmodules"] = ("100644", blob(repo, module_config(children, prefix)))
            changed.add(".gitmodules")
        if path:
            previous = git(repo, "cat-file", "blob", files[".gitignore"][1]).decode() if ".gitignore" in files else ""
            ignore = previous + "\n# Publicação: documentação e fixtures, sem mídia de produção/QA.\n" + publication_ignore(path, policy) + "\n"
            ignore += "\n# Proteções herdadas do workspace na extração.\n" + inherited_ignore(source_ignore, path, module_roots) + "\n"
            files[".gitignore"] = ("100644", blob(repo, ignore.encode()))
            changed.add(".gitignore")
        relocated = "\n".join(line[len(prefix):] for line in attributes.splitlines()
                              if prefix and line.startswith(prefix)
                              and not any(line.startswith(child["path"] + "/") for child in children))
        if relocated:
            previous = git(repo, "cat-file", "blob", files[".gitattributes"][1]).decode() if ".gitattributes" in files else ""
            files[".gitattributes"] = ("100644", blob(repo, (previous + "\n" + relocated + "\n").encode()))
            changed.add(".gitattributes")
        if not path:
            if ".gitattributes" in files:
                remaining = "\n".join(line for line in attributes.splitlines()
                                      if not any(line.startswith(child["path"] + "/") for child in children))
                files[".gitattributes"] = ("100644", blob(repo, (remaining + "\n").encode()))
                changed.add(".gitattributes")
            for relative, (mode, content) in overlay_contents.items():
                for old in list(files):
                    if old.startswith(relative + "/"):
                        del files[old]
                        changed.add(old)
                files[relative] = (mode, blob(repo, content))
                changed.add(relative)
        message = (f"chore: extract {name} as optional workspace module\n\n"
                   f"Source: {manifest['archive']}\nSource-commit: {revision}\nSource-path: {path or '.'}\n"
                   "Snapshot extraction; full history remains in the source repository.\n")
        commit, tree = commit_snapshot(repo, files, message, identity)
        actual = entries(repo, commit)
        for relative, value in files.items():
            if actual.get(relative) != value:
                raise ValueError(f"Falha de integridade: {prefix}{relative}")
        report["changed_metadata"].extend(prefix + relative for relative in sorted(changed))
        source_bytes = 0
        small_blobs = []
        for row in git(repo, "ls-tree", "-rlz", commit).split(b"\0"):
            if not row:
                continue
            header, relative = row.split(b"\t", 1)
            mode, kind, oid, size = header.split()
            if kind != b"blob":
                continue
            source_bytes += int(size)
            if int(size) < 1024:
                small_blobs.append((oid, relative))
        batch = git(repo, "cat-file", "--batch", data=b"\n".join(oid for oid, _ in small_blobs) + b"\n") if small_blobs else b""
        position = 0
        for oid, relative in small_blobs:
            end = batch.index(b"\n", position)
            size = int(batch[position:end].split()[2])
            content = batch[end + 1:end + 1 + size]
            position = end + size + 2
            if content.startswith(b"version https://git-lfs.github.com/spec/v1\n"):
                fields = dict(line.split(" ", 1) for line in content.decode().splitlines())
                digest = fields["oid"].removeprefix("sha256:")
                origin = common / "lfs/objects" / digest[:2] / digest[2:4] / digest
                if not origin.is_file() or origin.stat().st_size != int(fields["size"]):
                    raise ValueError(f"Objeto LFS local ausente: {prefix}{relative.decode()}")
                with origin.open("rb") as handle:
                    actual_hash = hashlib.file_digest(handle, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else hashlib.sha256(handle.read()).hexdigest()
                if actual_hash != digest:
                    raise ValueError(f"Objeto LFS corrompido: {digest}")
                target = repo / "lfs/objects" / digest[:2] / digest[2:4] / digest
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(origin, target)
                report["lfs"].append({"module": name, "path": relative.decode(), "oid": digest, "bytes": int(fields["size"])})
        if pack:
            git(repo, "-c", "pack.threads=2", "repack", "-a", "-d", "--window=0")
            (repo / "objects/info/alternates").unlink()
            git(repo, "fsck", "--connectivity-only", "--no-dangling")
        results[name] = commit
        report["modules"].append({"id": name, "path": path, "url": module["url"],
                                   "commit": commit, "tree": tree, "blob_bytes": source_bytes,
                                   "self_contained": pack, "repository": str(repo)})
        print(f"preparado: {name}: {source_bytes / 1_000_000:.1f} MB", flush=True)
    if reconstructed != retained:
        raise ValueError("A partição não preservou todas as entradas do commit original")
    report["original_entries_verified"] = len(original)
    report["retained_entries_verified"] = len(retained)
    report["integrity"] = "retained paths, blob IDs and modes preserved; exclusions, metadata and identical-tree gitlink replacements listed"
    (output / "receipt.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    git(output, "clone", "--no-local", str(output / "repositories/hub.git"), str(output / "checkout"))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=workspace.ROOT)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pack", action="store_true", help="Copia objetos para bases independentes do monólito")
    args = parser.parse_args()
    try:
        prepare(args.source, args.output, args.revision, pack=args.pack)
    except (ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n{getattr(exc, 'stderr', b'').decode()}\n")


if __name__ == "__main__":
    main()
