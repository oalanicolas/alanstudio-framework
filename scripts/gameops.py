#!/usr/bin/env python3
"""GameOps: operações Git do hub e dos módulos de um workspace.

audit      inventário somente leitura: worktrees, branches, stashes e gitlinks
cleanup    plano de limpeza com os comandos dos itens comprovados; não executa
preflight  confere o stage, ou o que falta publicar, antes do commit e do push
gates      lista ou roda as verificações que o repositório declara
"""
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time

from workspace import ROOT, load_config, load_manifest, parent_of


# Inventário somente leitura: nenhum comando abaixo altera refs, índice ou arquivos.
# GIT_OPTIONAL_LOCKS=0 impede que o status reescreva o cache de datas do índice.

def git_process(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})


def run_git(repo, *args):
    result = git_process(repo, *args)
    # Só o fim: o espaço inicial é coluna do status --porcelain.
    return result.stdout.rstrip() if result.returncode == 0 else None


def is_ancestor(repo, commit, ref):
    return git_process(repo, "merge-base", "--is-ancestor", commit, ref).returncode == 0


def has_ref(repo, ref):
    return run_git(repo, "rev-parse", "--verify", "--quiet", ref) is not None


def base_branch(repo):
    remote_head = run_git(repo, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    candidates = [remote_head.split("/", 1)[1]] if remote_head and "/" in remote_head else []
    for name in [*candidates, "main", "master"]:
        if has_ref(repo, f"refs/heads/{name}"):
            return name
    return run_git(repo, "symbolic-ref", "--quiet", "--short", "HEAD")


def comparison_bases(repo, base):
    if not base:
        return []
    return [base] + ([f"origin/{base}"] if has_ref(repo, f"refs/remotes/origin/{base}") else [])


def ref_state(repo, name, ref, bases):
    state = {"name": name, "head": run_git(repo, "rev-parse", "--short", ref),
             "date": run_git(repo, "log", "-1", "--format=%cs", ref),
             "merged_into": [base for base in bases if is_ancestor(repo, ref, base)]}
    if bases and not state["merged_into"]:
        state["ahead"] = int(run_git(repo, "rev-list", "--count", f"{bases[0]}..{ref}") or 0)
        cherry = run_git(repo, "cherry", bases[0], ref) or ""
        state["unique"] = sum(line.startswith("+") for line in cherry.splitlines())
    return state


def plural(count, singular, many):
    return f"{count} {singular if count == 1 else many}"


def count_lines(text):
    return len(text.splitlines()) if text else 0


def worktrees(repo, bases):
    listing = run_git(repo, "worktree", "list", "--porcelain") or ""
    entries = []
    for block in listing.split("\n\n")[1:]:  # o primeiro é o checkout principal
        fields = dict((line.split(" ", 1) + [""])[:2] for line in block.splitlines() if line)
        if "worktree" not in fields:
            continue
        item = {"path": fields["worktree"], "head": fields.get("HEAD", "")[:12],
                "branch": fields.get("branch", "").removeprefix("refs/heads/") or None,
                "prunable": "prunable" in fields, "locked": "locked" in fields}
        path = Path(item["path"])
        if not item["prunable"] and path.is_dir():
            status = run_git(path, "status", "--porcelain", "--ignored", "--ignore-submodules=all") or ""
            item["changes"] = sum(not line.startswith("!!") for line in status.splitlines())
            item["ignored"] = sum(line.startswith("!!") for line in status.splitlines())
            item["merged_into"] = [base for base in bases if is_ancestor(repo, fields.get("HEAD", ""), base)]
        entries.append(item)
    return entries


def normalized_url(url):
    return (url or "").strip().rstrip("/").removesuffix(".git").lower()


def remote_branches(repo):
    listing = git_process(repo, "ls-remote", "--heads", "origin")
    if listing.returncode:
        return None, (listing.stderr.strip().splitlines() or ["ls-remote falhou"])[-1]
    names = {}
    for line in listing.stdout.splitlines():
        sha, ref = line.split("\t", 1)
        names[ref.removeprefix("refs/heads/")] = sha
    return names, None


def audit_repository(repo, label, expected_url=None, external=False, remote=False):
    base = base_branch(repo)
    bases = comparison_bases(repo, base)
    current = run_git(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    report = {"path": label, "present": True, "external": external, "base": base,
              "branch": current, "head": run_git(repo, "rev-parse", "--short", "HEAD"),
              "changes": count_lines(run_git(repo, "status", "--porcelain", "--ignore-submodules=all")),
              "worktrees": worktrees(repo, bases), "branches": [], "tracking": [], "stashes": []}
    counts = run_git(repo, "rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    if counts:
        behind, ahead = (int(value) for value in counts.split())
        report["upstream"] = {"ref": run_git(repo, "rev-parse", "--abbrev-ref", "@{upstream}"),
                              "behind": behind, "ahead": ahead}
    for name in (run_git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads") or "").splitlines():
        if name != base and name != current:
            report["branches"].append(ref_state(repo, name, f"refs/heads/{name}", bases))
    live, error = remote_branches(repo) if remote and not external else (None, None)
    if error:
        report["remote_error"] = error
    tracked = (run_git(repo, "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin") or "").splitlines()
    for short in tracked:
        name = short.removeprefix("origin/")
        if name in ("HEAD", "origin", base):
            continue
        item = ref_state(repo, name, f"refs/remotes/origin/{name}", bases)
        if live is not None:
            item["on_remote"] = name in live
        report["tracking"].append(item)
    if live is not None:
        known = {item["name"] for item in report["tracking"]}
        report["remote_only"] = sorted(name for name in live if name != base and name not in known)
    for item in report["branches"]:
        if live is not None:
            item["on_remote"] = item["name"] in live
        elif has_ref(repo, f"refs/remotes/origin/{item['name']}"):
            item["on_remote"] = True
    for line in (run_git(repo, "stash", "list", "--format=%gd%x09%cs%x09%gs") or "").splitlines():
        ref, date, message = (line.split("\t") + ["", ""])[:3]
        report["stashes"].append({"ref": ref, "date": date, "message": message})
    origin = run_git(repo, "remote", "get-url", "origin")
    report["origin"] = origin
    if expected_url and origin and normalized_url(origin) != normalized_url(expected_url):
        report["expected_origin"] = expected_url
    email = run_git(repo, "config", "user.email")
    if origin and "github.com" in origin and not external and not (email or "").endswith("noreply.github.com"):
        report["identity"] = email or "(sem user.email)"
    return report


def gitlink_state(owner, relative, module_repo, published_ref=None):
    listing = run_git(owner, "ls-tree", "HEAD", "--", relative) or ""
    parts = listing.split()
    if len(parts) < 3 or parts[0] != "160000":
        return {"state": "ausente"}
    recorded, head = parts[2], run_git(module_repo, "rev-parse", "HEAD")
    known = run_git(module_repo, "cat-file", "-e", f"{recorded}^{{commit}}") is not None
    if recorded == head:
        state = "igual"
    elif not known:
        state = "desconhecido"
    elif is_ancestor(module_repo, recorded, "HEAD"):
        state = "módulo à frente"
    elif is_ancestor(module_repo, "HEAD", recorded):
        state = "módulo atrás"
    else:
        state = "divergente"
    result = {"state": state, "recorded": recorded[:12], "head": (head or "")[:12]}
    if known and published_ref:
        # Conforme o cache local do remoto; o hub não deve apontar para commit que só existe aqui.
        result["published"] = is_ancestor(module_repo, recorded, published_ref)
    return result


def findings(report):
    """Classifica o que pode ser limpo com segurança e o que pede decisão."""
    removable, pending = [], []
    for item in report.get("worktrees", []):
        where = f"worktree {item['path']}"
        if item["prunable"]:
            removable.append(f"{where}: registro órfão (git worktree prune)")
        elif item.get("changes") or item.get("ignored"):
            pending.append(f"{where}: {plural(item.get('changes', 0), 'alteração', 'alterações')}, "
                           f"{plural(item.get('ignored', 0), 'ignorado', 'ignorados')}")
        elif item.get("merged_into"):
            removable.append(f"{where}: limpo e contido em {', '.join(item['merged_into'])}")
        elif item["locked"]:
            pending.append(f"{where}: bloqueado")
        else:
            pending.append(f"{where}: HEAD {item['head'][:7]} fora de {report.get('base')}")
    for item in report.get("branches", []):
        if item["merged_into"]:
            removable.append(f"branch {item['name']}: mesclada em {', '.join(item['merged_into'])}")
        else:
            copy = "; sem cópia no remoto" if item.get("on_remote") is False else ""
            pending.append(f"branch {item['name']}: +{plural(item.get('ahead', 0), 'commit', 'commits')}, "
                           f"{item.get('unique', 0)} sem equivalente em {report.get('base')} ({item['date']}){copy}")
    for item in report.get("tracking", []):
        name = f"origin/{item['name']}"
        if item.get("on_remote") is False:
            removable.append(f"{name}: referência local de branch que não existe mais no remoto")
        elif item["merged_into"]:
            removable.append(f"{name}: mesclada em {', '.join(item['merged_into'])}")
        else:
            pending.append(f"{name}: +{plural(item.get('ahead', 0), 'commit', 'commits')} fora de {report.get('base')}")
    for name in report.get("remote_only", []):
        pending.append(f"origin/{name}: existe só no remoto; faça fetch dela para avaliar")
    for item in report.get("stashes", []):
        pending.append(f"stash {item['ref']} ({item['date']}): {item['message']}")
    gitlink = report.get("gitlink", {})
    if gitlink.get("state") not in (None, "igual"):
        pending.append(f"gitlink: {gitlink['state']} (registrado {gitlink.get('recorded', '—')}, "
                       f"módulo {gitlink.get('head', '—')})")
    if gitlink.get("published") is False:
        pending.append(f"gitlink: o hub registra {gitlink['recorded'][:7]}, que ainda não está "
                       f"em origin/{report.get('base')}; publique o módulo antes do hub")
    if report.get("expected_origin"):
        pending.append(f"origin {report['origin']} difere do manifesto {report['expected_origin']}")
    if report.get("identity"):
        pending.append(f"user.email {report['identity']} não é noreply; o GitHub pode recusar o push (GH007)")
    if report.get("remote_error"):
        pending.append(f"remoto inacessível: {report['remote_error']}")
    for item in report.get("stray", []):
        if item.get("unversioned"):
            pending.append(f"projeto sem Git: {item['path']} ({item['marker']}); sem histórico nem cópia remota")
        elif item.get("shares"):
            pending.append(f"checkout fora do manifesto: {item['path']} usa o Git de {item['shares']}; "
                           "rodar Git nele altera o módulo verdadeiro")
        else:
            pending.append(f"checkout fora do manifesto: {item['path']} com Git próprio")
    return removable, pending


PROJECT_MARKERS = ("package.json", "AGENTS.md", "ProjectSettings", "project.godot", "Cargo.toml", "pyproject.toml")


def stray_checkouts(root, modules):
    """Pastas não rastreadas do hub fora do manifesto: com .git próprio ou emprestado, ou projeto sem Git."""
    listing = run_git(root, "ls-files", "--others", "--exclude-standard", "--directory") or ""
    known = {module["path"] for module in modules}
    owners = {common_dir(root / module["path"]): module["path"] for module in modules
              if (root / module["path"] / ".git").exists()}
    found = []
    for entry in listing.splitlines():
        path = entry.rstrip("/")
        dotgit = root / path / ".git"
        if not entry.endswith("/") or path in known:
            continue
        if not dotgit.exists():
            marker = next((name for name in PROJECT_MARKERS if (root / path / name).exists()), None)
            if marker:
                found.append({"path": path, "unversioned": True, "marker": marker})
            continue
        item = {"path": path}
        if dotgit.is_file():
            text = dotgit.read_text(errors="replace").strip()
            if text.startswith("gitdir:"):
                gitdir = (dotgit.parent / text[len("gitdir:"):].strip()).resolve()
                item["gitdir"] = str(gitdir)
                item["shares"] = owners.get(gitdir)
        found.append(item)
    return found


def audit(root, modules, manifest=None, remote=False):
    root = Path(root).resolve()
    manifest = manifest or {}
    reports = [audit_repository(root, ".", manifest.get("repository"), remote=remote)]
    reports[0]["stray"] = stray_checkouts(root, modules)
    for module in modules:
        target = root / module["path"]
        if not (target / ".git").exists():
            reports.append({"path": module["path"], "id": module["id"], "present": False})
            continue
        report = audit_repository(target, module["path"], module.get("url"),
                                  bool(module.get("external")), remote)
        report["id"] = module["id"]
        parent = parent_of(module, modules)
        owner = root / parent["path"] if parent else root
        published = f"origin/{report['base']}" if report["base"] and not module.get("external") else None
        if published and not has_ref(target, f"refs/remotes/{published}"):
            published = None
        report["gitlink"] = gitlink_state(owner, target.relative_to(owner).as_posix(), target, published)
        reports.append(report)
    for report in reports:
        if report["present"]:
            report["removable"], report["pending"] = findings(report)
    present = [item for item in reports if item["present"]]
    return {"root": str(root), "remote_checked": remote, "repositories": reports, "summary": {
        "present": len(present), "not_downloaded": len(reports) - len(present),
        "with_changes": sum(bool(item["changes"]) for item in present),
        "removable": sum(len(item["removable"]) for item in present),
        "pending": sum(len(item["pending"]) for item in present)}}


def describe(report):
    where = report["branch"] or f"HEAD destacado {report['head']}"
    parts = [f"{report['path']} · {where}"]
    parts.append(plural(report["changes"], "alteração", "alterações") if report["changes"] else "sem alterações")
    upstream = report.get("upstream")
    if upstream and (upstream["ahead"] or upstream["behind"]):
        parts.append(f"{upstream['ahead']} à frente / {upstream['behind']} atrás de {upstream['ref']}")
    if report.get("external"):
        parts.append("externo")
    return " · ".join(parts)


def print_audit(result, show_all=False):
    for report in result["repositories"]:
        if not report["present"]:
            continue
        notable = report["removable"] or report["pending"] or report["changes"] or report.get("upstream", {}).get("ahead")
        if not (show_all or notable or report["path"] == "."):
            continue
        print(describe(report))
        for line in report["pending"]:
            print(f"  pendente: {line}")
        for line in report["removable"]:
            print(f"  removível: {line}")
    missing = [item["path"] for item in result["repositories"] if not item["present"]]
    summary = result["summary"]
    print(f"\n{summary['present']} repositórios presentes, {summary['not_downloaded']} não baixados; "
          f"{summary['with_changes']} com alterações; {summary['removable']} itens removíveis; "
          f"{summary['pending']} pendentes.")
    if missing:
        print("Não baixados: " + ", ".join(missing))
    if not result["remote_checked"]:
        print("Branches remotas vêm do cache local; use --remote para conferir o GitHub.")




# Plano de limpeza: só itens que o audit classifica como removíveis. Nada é executado.

CODEX_WORKTREES = Path.home() / ".codex" / "worktrees"


def cleanup_plan(result):
    local, remote = [], []
    needs_remote_check = False
    for report in result["repositories"]:
        if not report["present"]:
            continue
        git = f"git -C {shlex.quote(report['path'])}"
        steps, publishing = [], []
        kept_branches = set()
        if any(item["prunable"] for item in report["worktrees"]):
            steps.append(f"{git} worktree prune -v")
        for item in report["worktrees"]:
            if item["prunable"]:
                continue
            clean = not item.get("changes") and not item.get("ignored")
            if not (clean and item.get("merged_into") and not item["locked"]):
                kept_branches.add(item["branch"])
                continue
            steps.append(f"{git} worktree remove {shlex.quote(item['path'])}")
            parent = Path(item["path"]).parent
            if parent.parent == CODEX_WORKTREES and [p.name for p in parent.iterdir()] == [Path(item["path"]).name]:
                steps.append(f"rmdir {shlex.quote(str(parent))}")
        merged = [item["name"] for item in report["branches"]
                  if item["merged_into"] and item["name"] not in kept_branches]
        if merged:
            steps.append(f"{git} branch -d " + " ".join(shlex.quote(name) for name in merged))
        stale = [item["name"] for item in report["tracking"] if item.get("on_remote") is False]
        if stale:
            steps.append(f"{git} branch -rd " + " ".join(shlex.quote(f"origin/{name}") for name in stale))
        published_base = f"origin/{report['base']}"
        deletable = [item["name"] for item in report["tracking"]
                     if item.get("on_remote") and published_base in item["merged_into"]]
        if deletable and not report["external"]:
            names = " ".join(shlex.quote(name) for name in deletable)
            publishing.append(f"{git} push origin --delete {names}")
            publishing.append(f"{git} branch -rd " + " ".join(shlex.quote(f"origin/{n}") for n in deletable))
        if any("on_remote" not in item and item["merged_into"] for item in report["tracking"]):
            needs_remote_check = True
        if steps:
            local.append({"repository": report["path"], "commands": steps})
        if publishing:
            remote.append({"repository": report["path"], "commands": publishing})
    return {"local": local, "remote": remote, "pending": result["summary"]["pending"],
            "needs_remote_check": needs_remote_check}


def print_plan(plan):
    print("# Plano de limpeza: só itens com prova de que nada se perde. Nada foi executado.")
    print("# Rode a partir da raiz do workspace, depois de conferir o audit.")
    if not plan["local"] and not plan["remote"]:
        print("# Nada removível.")
    if plan["local"]:
        print("\n# Local")
        for group in plan["local"]:
            print("\n".join(group["commands"]))
    if plan["remote"]:
        print("\n# Remoto: publica no GitHub e precisa de autorização")
        for group in plan["remote"]:
            print("\n".join(group["commands"]))
    if plan["needs_remote_check"]:
        print("\n# Branches remotas mescladas ficaram de fora: rode cleanup --remote para conferir o GitHub.")
    if plan["pending"]:
        print(f"# {plural(plan['pending'], 'item pendente ficou', 'itens pendentes ficaram')} de fora; "
              "veja gameops.py audit.")


# Preflight: o que vai entrar no commit (stage) ou no push (commits ainda não publicados).

ABSOLUTE_PATH = re.compile(r"(?<![\w.~-])(/Users/(?![<${.…])[^/\s'\"`]+/|/home/(?![<${.…])[^/\s'\"`]+/"
                           r"|[A-Za-z]:\\Users\\(?![<${.…]))")
SECRET_TEXT = (
    ("chave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("token do GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,})")),
    ("chave AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("chave de API (sk-)", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{24,}")),
    ("token do Slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("chave do Google", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
)
CONFLICT_MARKER = re.compile(r"^(<{7}|={7}|>{7})( |$)")
SECRET_NAME = re.compile(r"(^|/)(id_(rsa|ed25519|ecdsa|dsa)|[^/]+\.(pem|p12|pfx|key|keystore|jks))$")
PRODUCTION_MEDIA = {".mov", ".mp4", ".mkv", ".avi", ".blend", ".blend1", ".psd", ".kra", ".xcf",
                    ".aep", ".prproj", ".zip", ".7z", ".rar", ".tar", ".gz"}


def secret_file(path):
    name = path.rsplit("/", 1)[-1]
    if name == ".env" or (name.startswith(".env.") and name.split(".", 2)[2] not in ("example", "sample", "template")):
        return True
    return bool(SECRET_NAME.search(path))


def added_lines(diff):
    current, line_number = None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)", line)
            line_number = int(match.group(1)) if match else 0
        elif line.startswith("+") and current:
            yield current, line_number, line[1:]
            line_number += 1


def github_origin(repo):
    origin = run_git(repo, "remote", "get-url", "origin") or ""
    return "github.com" in origin


def common_dir(repo):
    found = run_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return Path(found).resolve() if found else None


def resolve_target(root, modules, name):
    """Devolve (checkout, rótulo, módulo, dono): dono é '.' ou o caminho do módulo no manifesto.

    Aceita o hub ('.'), o id ou caminho de um módulo, ou o caminho de um worktree deles."""
    root = Path(root).resolve()
    if name in (".", "hub", ""):
        return root, ".", None, "."
    module = next((item for item in modules if name in (item["id"], item["path"], item["path"] + "/")), None)
    if module is not None:
        path = root / module["path"]
        if not (path / ".git").exists():
            raise ValueError(f"Módulo não baixado: {module['path']}. Use workspace.py get {module['id']}.")
        return path, module["path"], module, module["path"]
    candidate = Path(name).expanduser()
    candidate = (candidate if candidate.is_absolute() else Path.cwd() / candidate).resolve()
    if candidate.is_dir() and (candidate / ".git").exists():
        shared = common_dir(candidate)
        owners = [(".", None, root)] + [(item["path"], item, root / item["path"]) for item in modules]
        for owner, item, checkout in owners:
            if (checkout / ".git").exists() and common_dir(checkout) == shared:
                return candidate, str(candidate), item, owner
        raise ValueError(f"{candidate} não é worktree do hub nem de um módulo do workspace.")
    raise ValueError(f"Repositório desconhecido: {name}. Use '.' para o hub, um id de workspace.py list "
                     "ou o caminho de um worktree.")


def publish_range(repo):
    upstream = run_git(repo, "rev-parse", "--abbrev-ref", "@{upstream}")
    if upstream:
        return upstream
    base = base_branch(repo)
    return f"origin/{base}" if base and has_ref(repo, f"refs/remotes/origin/{base}") else None


def working_tree(repo):
    """Arquivos rastreados com alteração fora do stage e quantidade de entradas não rastreadas."""
    modified, untracked = set(), 0
    for line in (run_git(repo, "status", "--porcelain", "--ignore-submodules=dirty") or "").splitlines():
        if line.startswith("??"):
            untracked += 1
        elif line[1:2] not in (" ", ""):
            modified.add(line[3:].split(" -> ")[-1].strip('"'))
    return modified, untracked


def preflight(root, modules, target, push=False, max_mb=5):
    repo, label, module, owner = resolve_target(root, modules, target)
    external = bool(module and module.get("external"))
    report = {"repository": label, "mode": "push" if push else "stage",
              "blocking": [], "warnings": [], "info": []}
    block, warn, info = report["blocking"].append, report["warnings"].append, report["info"].append
    modified, untracked = working_tree(repo)
    if modified or untracked:
        where = "fora do commit" if push else "fora do stage e fora do commit"
        info(f"{where}: {len(modified)} modificados, {untracked} não rastreados")
    if push:
        upstream = publish_range(repo)
        if not upstream:
            block("sem upstream nem origin/<base> para comparar; defina o upstream antes do push")
            return report
        report["range"] = spec = f"{upstream}..HEAD"
        diff_args, blob = [spec], lambda path: f"HEAD:{path}"
        counts = run_git(repo, "rev-list", "--left-right", "--count", f"{upstream}...HEAD")
        behind, ahead = (int(value) for value in counts.split()) if counts else (0, 0)
        if not ahead:
            info(f"nada a publicar: HEAD já está em {upstream}")
            return report
        info(plural(ahead, "commit a publicar", "commits a publicar"))
        overlap = sorted(modified & set((run_git(repo, "diff", "--name-only", spec) or "").splitlines()))
        if overlap:
            shown = ", ".join(overlap[:5]) + ("…" if len(overlap) > 5 else "")
            warn(f"{plural(len(overlap), 'arquivo do push tem', 'arquivos do push têm')} alterações fora do "
                 f"commit ({shown}); gates e deploy leem a pasta, não o commit: valide num worktree do commit")
        if behind:
            block(f"{plural(behind, 'commit', 'commits')} em {upstream} que não estão aqui: "
                  "integre antes, o push seria recusado")
        if not external and github_origin(repo):
            emails = sorted(set((run_git(repo, "log", "--format=%ae%n%ce", spec) or "").splitlines()))
            private = [email for email in emails if email and not email.endswith("noreply.github.com")]
            if private:
                block("commits com e-mail que não é noreply: " + ", ".join(private)
                      + " (o GitHub recusa com GH007; refaça os commits com a identidade noreply)")
    else:
        diff_args, blob = ["--cached"], lambda path: f":{path}"
        unmerged = run_git(repo, "diff", "--name-only", "--diff-filter=U") or ""
        if unmerged:
            block("conflitos não resolvidos: " + ", ".join(unmerged.splitlines()))
        staged = run_git(repo, "diff", "--cached", "--name-only") or ""
        if not staged:
            info("nada no stage")
            return report
        info(plural(count_lines(staged), "arquivo no stage", "arquivos no stage"))
        email = run_git(repo, "config", "user.email") or ""
        if not external and github_origin(repo) and not email.endswith("noreply.github.com"):
            block(f"user.email {email or '(vazio)'} não é noreply; o GitHub recusa o push com GH007")
    if not run_git(repo, "symbolic-ref", "--quiet", "HEAD"):
        warn("HEAD destacado: crie uma branch antes de commitar")
    names = run_git(repo, "diff", *diff_args, "--name-only", "--diff-filter=AMR") or ""
    for path in names.splitlines():
        if secret_file(path):
            block(f"{path}: arquivo de credencial")
        size = run_git(repo, "cat-file", "-s", blob(path))
        if size and size.isdigit() and int(size) > max_mb * 1_000_000:
            warn(f"{path}: {int(size) / 1_000_000:.1f} MB; mídia de produção vai para o acervo externo")
        elif Path(path).suffix.lower() in PRODUCTION_MEDIA:
            warn(f"{path}: extensão de mídia de produção; confirme que é asset de runtime")
    diff = run_git(repo, "diff", *diff_args, "-U0", "--no-color", "--no-ext-diff") or ""
    for path, number, text in added_lines(diff):
        where = f"{path}:{number}"
        if ABSOLUTE_PATH.search(text):
            block(f"{where}: caminho absoluto da máquina ({ABSOLUTE_PATH.search(text).group(0)})")
        for label_, pattern in SECRET_TEXT:
            if pattern.search(text):
                block(f"{where}: possível {label_}")
        if CONFLICT_MARKER.match(text):
            block(f"{where}: marcador de conflito")
    raw = run_git(repo, "diff", *diff_args, "--raw", "--no-abbrev") or ""
    owned = {item["path"]: item for item in modules if (parent_of(item, modules) or {}).get("path") == (module or {}).get("path")}
    for line in raw.splitlines():
        meta, _, path = line.partition("\t")
        fields = meta.split()
        if len(fields) < 5 or fields[1] != "160000":
            continue
        commit = fields[3]
        full = (owner + "/" + path) if owner != "." else path
        child = owned.get(full)
        child_repo = Path(root).resolve() / full
        if not (child_repo / ".git").exists():
            warn(f"{path}: gitlink para módulo não baixado; não foi possível conferir {commit[:7]}")
            continue
        base = base_branch(child_repo)
        ref = f"origin/{base}" if base else None
        if run_git(child_repo, "cat-file", "-e", f"{commit}^{{commit}}") is None:
            block(f"{path}: o commit {commit[:7]} não existe no módulo local")
        elif ref and has_ref(child_repo, f"refs/remotes/{ref}") and not is_ancestor(child_repo, commit, ref):
            block(f"{path}: gitlink {commit[:7]} ainda não está em {ref}; publique o módulo antes do hub")
        elif child and child.get("external"):
            info(f"{path}: gitlink de referência externa {commit[:7]}")
    return report


def print_preflight(report):
    title = f"{report['repository']} · {'push ' + report.get('range', '') if report['mode'] == 'push' else 'stage'}"
    print(title.strip())
    for line in report["info"]:
        print(f"  info: {line}")
    for line in report["warnings"]:
        print(f"  aviso: {line}")
    for line in report["blocking"]:
        print(f"  bloqueio: {line}")
    verdict = "BLOQUEADO" if report["blocking"] else "ok"
    print(f"\n{verdict}: {plural(len(report['blocking']), 'bloqueio', 'bloqueios')}, "
          f"{plural(len(report['warnings']), 'aviso', 'avisos')}.")


# Gates: verificações declaradas pelo próprio repositório ou pela configuração local.

GATE_ORDER = ("lint", "typecheck", "test", "build", "doctor", "verify", "check")


def changed_paths(repo):
    paths = set()
    for line in (run_git(repo, "status", "--porcelain", "--ignore-submodules=all") or "").splitlines():
        paths.add(line[3:].split(" -> ")[-1].strip('"'))
    upstream = publish_range(repo)
    if upstream:
        paths.update((run_git(repo, "diff", "--name-only", f"{upstream}..HEAD") or "").splitlines())
    return sorted(path for path in paths if path)


def declared_gates(root, repo, label):
    configured = load_config(root).get("gameops", {}).get("gates", {})
    if not isinstance(configured, dict):
        raise ValueError("gameops.gates precisa mapear repositório → lista de comandos")
    if label in configured:
        gates = []
        for entry in configured[label]:
            entry = {"run": entry} if isinstance(entry, str) else entry
            if not isinstance(entry, dict) or not isinstance(entry.get("run"), str):
                raise ValueError(f"Gate inválido em gameops.gates[{label!r}]: {entry}")
            gates.append({"name": entry.get("name") or entry["run"], "argv": shlex.split(entry["run"]),
                          "when": list(entry.get("when", []))})
        return gates, "framework/config.json"
    package = repo / "package.json"
    if not package.is_file():
        return [], None
    data = json.loads(package.read_text(encoding="utf-8"))
    scripts = data.get("scripts", {}) if isinstance(data, dict) else {}
    gates = [{"name": name, "argv": ["npm", "run", name], "when": []} for name in GATE_ORDER if name in scripts]
    needs_install = bool(data.get("dependencies") or data.get("devDependencies")) and not (repo / "node_modules").is_dir()
    return gates, "package.json" + (" (sem node_modules: rode npm ci antes)" if needs_install else "")


def gates(root, modules, target, run=False, include_all=False, timeout=1800):
    repo, label, _, owner = resolve_target(root, modules, target)
    declared, source = declared_gates(root, repo, owner)
    changes = changed_paths(repo) if any(gate["when"] for gate in declared) else []
    report = {"repository": label, "source": source, "gates": [], "failed": 0}
    for gate in declared:
        item = {"name": gate["name"], "command": shlex.join(gate["argv"])}
        triggered = include_all or not gate["when"] or any(
            path.startswith(prefix) for path in changes for prefix in gate["when"])
        if not triggered:
            item["status"] = "skipped"
            item["reason"] = "sem mudanças em " + ", ".join(gate["when"])
        elif not run:
            item["status"] = "listed"
        elif source and "npm ci" in source:
            item["status"] = "failed"
            item["reason"] = "dependências ausentes: rode npm ci antes"
        else:
            started = time.monotonic()
            try:
                result = subprocess.run(gate["argv"], cwd=repo, capture_output=True, text=True, timeout=timeout)
                item["status"] = "passed" if result.returncode == 0 else "failed"
                item["exit"] = result.returncode
                if result.returncode:
                    item["tail"] = (result.stdout + result.stderr).strip().splitlines()[-20:]
            except (OSError, subprocess.TimeoutExpired) as exc:
                item["status"] = "failed"
                item["reason"] = str(exc)
            item["seconds"] = round(time.monotonic() - started, 1)
        report["failed"] += item["status"] == "failed"
        report["gates"].append(item)
    return report


def print_gates(report):
    if not report["gates"]:
        print(f"{report['repository']}: nenhuma verificação declarada; siga o README/AGENTS do projeto.")
        return
    print(f"{report['repository']} · {report['source']}")
    for item in report["gates"]:
        extra = item.get("reason") or (f"{item['seconds']} s" if "seconds" in item else "")
        print(f"  {item['status']:8} {item['name']}" + (f"  ({extra})" if extra else "")
              + ("" if item["name"] == item["command"] else f"  → {item['command']}"))
        for line in item.get("tail", []):
            print(f"           {line}")
    if report["failed"]:
        print(f"\n{plural(report['failed'], 'verificação falhou', 'verificações falharam')}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    inventory = sub.add_parser("audit", help="inventário somente leitura do hub e dos módulos")
    inventory.add_argument("--remote", action="store_true", help="confere as branches no remoto (rede)")
    inventory.add_argument("--all", action="store_true", help="lista também os repositórios sem pendências")
    inventory.add_argument("--json", action="store_true")
    plan = sub.add_parser("cleanup", help="plano de limpeza dos itens removíveis; não executa")
    plan.add_argument("--remote", action="store_true", help="confere o GitHub e planeja as branches remotas")
    plan.add_argument("--json", action="store_true")
    check = sub.add_parser("preflight", help="confere o stage ou, com --push, o que falta publicar")
    check.add_argument("repository", nargs="?", default=".", help="'.' para o hub, ou id/caminho do módulo")
    check.add_argument("--push", action="store_true")
    check.add_argument("--max-mb", type=float, default=5)
    check.add_argument("--json", action="store_true")
    verify = sub.add_parser("gates", help="lista ou roda as verificações declaradas")
    verify.add_argument("repository", nargs="?", default=".")
    verify.add_argument("--run", action="store_true")
    verify.add_argument("--all", action="store_true", help="ignora as condições when da configuração")
    verify.add_argument("--timeout", type=int, default=1800)
    verify.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        if run_git(args.root, "rev-parse", "--git-dir") is None:
            raise ValueError(f"{args.root} não é um repositório Git.")
        # Sem workspace.json, o repositório é auditado sozinho, sem módulos.
        has_manifest = (Path(args.root) / "workspace.json").is_file()
        manifest = load_manifest(args.root) if has_manifest else {"modules": []}
        modules = manifest["modules"]
        if args.command in ("audit", "cleanup"):
            result = audit(args.root, modules, manifest, remote=args.remote)
            output = result if args.command == "audit" else cleanup_plan(result)
            if args.json:
                print(json.dumps(output, ensure_ascii=False, indent=2))
            elif args.command == "audit":
                print_audit(result, show_all=args.all)
            else:
                print_plan(output)
            return 0
        if args.command == "preflight":
            report = preflight(args.root, modules, args.repository, push=args.push, max_mb=args.max_mb)
            print(json.dumps(report, ensure_ascii=False, indent=2)) if args.json else print_preflight(report)
            return 1 if report["blocking"] else 0
        report = gates(args.root, modules, args.repository, run=args.run, include_all=args.all, timeout=args.timeout)
        print(json.dumps(report, ensure_ascii=False, indent=2)) if args.json else print_gates(report)
        return 1 if report["failed"] else 0
    except (ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    sys.exit(main())
