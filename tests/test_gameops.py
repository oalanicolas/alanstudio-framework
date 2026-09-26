import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import gameops


class GameOpsTest(unittest.TestCase):
    """Hub com um módulo presente (alpha) e um não baixado (beta)."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gameops-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        env = patch.dict(os.environ, {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "protocol.file.allow",
                                      "GIT_CONFIG_VALUE_0": "always"})
        env.start()
        self.addCleanup(env.stop)
        self.remote = self.base / "alpha.git"
        self.git(self.base, "init", "--bare", "--initial-branch=main", str(self.remote))
        seed = self.base / "seed"
        self.git(self.base, "init", "--initial-branch=main", str(seed))
        self.identity(seed)
        self.commit(seed, "main.txt", "v1")
        self.git(seed, "push", str(self.remote), "main")
        self.hub = self.base / "hub"
        self.git(self.base, "init", "--initial-branch=main", str(self.hub))
        self.identity(self.hub)
        self.modules = [{"id": "alpha", "path": "games/alpha", "url": self.remote.as_uri()},
                        {"id": "beta", "path": "games/beta", "url": (self.base / "beta.git").as_uri()}]
        (self.hub / "workspace.json").write_text(json.dumps({"version": 1, "modules": self.modules}))
        self.git(self.hub, "submodule", "add", self.remote.as_uri(), "games/alpha")
        self.git(self.hub, "add", "workspace.json")
        self.git(self.hub, "commit", "-m", "hub")
        self.alpha = self.hub / "games/alpha"
        self.identity(self.alpha)

    def git(self, root, *args):
        return subprocess.run(["git", "-C", str(root), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def identity(self, repo, email="audit@example.invalid"):
        self.git(repo, "config", "user.name", "GameOps Test")
        self.git(repo, "config", "user.email", email)

    def commit(self, repo, name, text):
        (repo / name).write_text(text + "\n")
        self.git(repo, "add", name)
        self.git(repo, "commit", "-m", text)

    def audit(self, **options):
        return gameops.audit(self.hub, self.modules, {}, **options)

    def alpha_report(self, **options):
        return next(item for item in self.audit(**options)["repositories"] if item["path"] == "games/alpha")

    def snapshot(self):
        return [self.git(repo, *args) for repo in (self.hub, self.alpha) for args in (
            ("for-each-ref",), ("worktree", "list", "--porcelain"), ("stash", "list"),
            ("status", "--porcelain"))]

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "gameops.py"), "--root", str(self.hub), *args],
                              capture_output=True, text=True)

    def github_origin(self, repo):
        # Só a URL muda: o preflight não usa a rede, e origin/main continua no cache local.
        self.git(repo, "remote", "set-url", "origin", "https://github.com/example/alpha.git")


class AuditTest(GameOpsTest):
    def test_clean_workspace_has_nothing_to_do_and_names_missing_modules(self):
        result = self.audit()
        self.assertEqual(result["summary"], {"present": 2, "not_downloaded": 1, "with_changes": 0,
                                             "removable": 0, "pending": 0})
        alpha = self.alpha_report()
        self.assertEqual(alpha["gitlink"]["state"], "igual")
        self.assertTrue(alpha["gitlink"]["published"])
        text = self.cli("audit")
        self.assertEqual(text.returncode, 0, text.stderr)
        self.assertIn("Não baixados: games/beta", text.stdout)
        self.assertEqual(json.loads(self.cli("audit", "--json").stdout)["summary"]["present"], 2)

    def test_merged_items_are_removable_unique_work_is_pending_and_nothing_changes(self):
        self.git(self.alpha, "branch", "merged")
        self.git(self.alpha, "switch", "-c", "feature")
        self.commit(self.alpha, "feature.txt", "feature")
        self.git(self.alpha, "switch", "main")
        (self.alpha / "main.txt").write_text("wip\n")
        self.git(self.alpha, "stash", "push", "-m", "wip")
        merged_tree, gone, dirty = (self.base / name for name in ("merged-tree", "gone", "dirty"))
        for path in (merged_tree, gone, dirty):
            self.git(self.alpha, "worktree", "add", "--detach", str(path), "main")
        shutil.rmtree(gone)
        (dirty / "scratch.txt").write_text("x\n")
        before = self.snapshot()
        alpha = self.alpha_report()
        self.assertEqual(before, self.snapshot())
        removable, pending = "\n".join(alpha["removable"]), "\n".join(alpha["pending"])
        self.assertIn("branch merged: mesclada em main, origin/main", removable)
        self.assertIn("branch feature: +1 commit, 1 sem equivalente em main", pending)
        self.assertIn(f"worktree {merged_tree}: limpo e contido em main", removable)
        self.assertIn(f"worktree {gone}: registro órfão", removable)
        self.assertIn(f"worktree {dirty}: 1 alteração, 0 ignorados", pending)
        self.assertIn("stash stash@{0}", pending)

    def test_hub_pointing_to_unpublished_module_commit_is_pending(self):
        self.commit(self.alpha, "next.txt", "next")
        alpha = self.alpha_report()
        self.assertEqual(alpha["gitlink"]["state"], "módulo à frente")
        self.assertEqual(alpha["upstream"]["ahead"], 1)
        self.git(self.hub, "add", "games/alpha")
        self.git(self.hub, "commit", "-m", "registra alpha")
        alpha = self.alpha_report()
        self.assertEqual(alpha["gitlink"]["state"], "igual")
        self.assertFalse(alpha["gitlink"]["published"])
        self.assertIn("publique o módulo antes do hub", "\n".join(alpha["pending"]))
        self.git(self.alpha, "push", "origin", "main")
        self.assertTrue(self.alpha_report()["gitlink"]["published"])

    def test_audit_does_not_rewrite_stale_index_stat_caches(self):
        indexes = [Path(self.git(repo, "rev-parse", "--path-format=absolute", "--git-path", "index"))
                   for repo in (self.hub, self.alpha)]
        for repo, name in ((self.hub, "workspace.json"), (self.alpha, "main.txt")):
            stamp = (repo / name).stat().st_mtime + 100
            os.utime(repo / name, (stamp, stamp))
        before = [path.read_bytes() for path in indexes]
        self.audit()
        self.assertEqual(before, [path.read_bytes() for path in indexes])

    def test_unmerged_branch_without_remote_copy_is_called_out(self):
        self.git(self.alpha, "switch", "-c", "auditoria")
        self.commit(self.alpha, "fix.txt", "fix")
        self.git(self.alpha, "switch", "main")
        self.assertIn("; sem cópia no remoto", "\n".join(self.alpha_report(remote=True)["pending"]))
        self.assertNotIn("sem cópia", "\n".join(self.alpha_report()["pending"]))
        self.git(self.alpha, "push", "origin", "auditoria")
        self.assertNotIn("sem cópia", "\n".join(self.alpha_report(remote=True)["pending"]))

    def test_leftover_folder_sharing_a_module_git_is_flagged_without_touching_it(self):
        stray = self.hub / "games/alpha-antigo"
        stray.mkdir(parents=True)
        (stray / "main.txt").write_text("cópia antiga\n")
        gitdir = Path(self.git(self.alpha, "rev-parse", "--path-format=absolute", "--git-common-dir"))
        (stray / ".git").write_text(f"gitdir: {os.path.relpath(gitdir, stray)}\n")
        (self.hub / "games/rascunho").mkdir()
        (self.hub / "games/rascunho/nota.md").write_text("sem git\n")
        (self.hub / "games/jogo-novo/src").mkdir(parents=True)
        (self.hub / "games/jogo-novo/package.json").write_text("{}")
        (self.hub / "games/jogo-novo/src/main.js").write_text("// trabalho do dia\n")
        hub = next(item for item in self.audit()["repositories"] if item["path"] == ".")
        self.assertEqual([item["path"] for item in hub["stray"]], ["games/alpha-antigo", "games/jogo-novo"])
        self.assertIn("projeto sem Git: games/jogo-novo (package.json); sem histórico nem cópia remota",
                      hub["pending"])
        self.assertIn("checkout fora do manifesto: games/alpha-antigo usa o Git de games/alpha; "
                      "rodar Git nele altera o módulo verdadeiro", hub["pending"])

    def test_remote_check_finds_stale_tracking_refs_that_a_narrow_refspec_never_prunes(self):
        self.git(self.alpha, "config", "remote.origin.fetch", "+refs/heads/main:refs/remotes/origin/main")
        self.git(self.alpha, "push", "origin", "main:refs/heads/old", "main:refs/heads/fresh")
        self.git(self.alpha, "fetch", "origin", "+refs/heads/old:refs/remotes/origin/old")
        self.git(self.remote, "branch", "-D", "old")
        self.git(self.alpha, "fetch", "--prune", "origin")
        cached = self.alpha_report()
        self.assertIn("origin/old: mesclada em main, origin/main", "\n".join(cached["removable"]))
        self.assertNotIn("remote_only", cached)
        live = self.alpha_report(remote=True)
        self.assertIn("origin/old: referência local de branch que não existe mais no remoto",
                      "\n".join(live["removable"]))
        self.assertEqual(live["remote_only"], ["fresh"])
        self.assertTrue(self.git(self.alpha, "rev-parse", "--verify", "refs/remotes/origin/old"))


class CleanupTest(GameOpsTest):
    def test_plan_holds_only_proven_items_worktrees_before_branches_and_remote_apart(self):
        self.git(self.alpha, "branch", "merged")
        self.git(self.alpha, "branch", "busy")
        self.git(self.alpha, "switch", "-c", "feature")
        self.commit(self.alpha, "feature.txt", "feature")
        self.git(self.alpha, "switch", "main")
        done, busy = self.base / "done", self.base / "busy"
        self.git(self.alpha, "worktree", "add", "-b", "done-branch", str(done), "main")
        self.git(self.alpha, "worktree", "add", str(busy), "busy")
        (busy / "scratch.txt").write_text("trabalho\n")
        self.git(self.alpha, "push", "origin", "main:refs/heads/shipped", "feature:refs/heads/draft")
        self.git(self.alpha, "fetch", "origin", "+refs/heads/*:refs/remotes/origin/*")
        before = self.snapshot()
        cached = gameops.cleanup_plan(self.audit())
        self.assertEqual(cached["remote"], [])
        self.assertTrue(cached["needs_remote_check"])
        plan = gameops.cleanup_plan(self.audit(remote=True))
        self.assertEqual(before, self.snapshot())
        local = next(group["commands"] for group in plan["local"] if group["repository"] == "games/alpha")
        self.assertEqual(local, [f"git -C games/alpha worktree remove {shlex.quote(str(done))}",
                                 "git -C games/alpha branch -d done-branch merged"])
        self.assertEqual(plan["remote"], [{"repository": "games/alpha", "commands": [
            "git -C games/alpha push origin --delete shipped",
            "git -C games/alpha branch -rd origin/shipped"]}])
        self.assertGreaterEqual(plan["pending"], 3)
        printed = self.cli("cleanup", "--remote")
        self.assertEqual(printed.returncode, 0, printed.stderr)
        self.assertIn("Nada foi executado", printed.stdout)
        self.assertTrue((busy / "scratch.txt").exists())


class PreflightTest(GameOpsTest):
    def stage(self, name, text):
        (self.alpha / name).write_text(text)
        self.git(self.alpha, "add", name)

    def blocking(self, **options):
        return "\n".join(gameops.preflight(self.hub, self.modules, "alpha", **options)["blocking"])

    def test_stage_blocks_machine_paths_credentials_and_conflicts_but_not_placeholders(self):
        self.stage("notes.md", "ok\nveja /Users/fulana/Code/jogo/x.js\nuse /Users/<user>/Code e /path/to/file\n"
                               "<<<<<<< HEAD\n")
        self.stage("config.js", "const token = 'ghp_" + "a" * 36 + "';\n")
        self.stage(".env.local", "SECRET=1\n")
        self.stage(".env.example", "SECRET=\n")
        found = self.blocking()
        self.assertIn("notes.md:2: caminho absoluto da máquina (/Users/fulana/)", found)
        self.assertNotIn("notes.md:3", found)
        self.assertIn("notes.md:4: marcador de conflito", found)
        self.assertIn("config.js:1: possível token do GitHub", found)
        self.assertIn(".env.local: arquivo de credencial", found)
        self.assertNotIn(".env.example", found)
        cli = self.cli("preflight", "alpha")
        self.assertEqual(cli.returncode, 1)
        self.assertIn("BLOQUEADO", cli.stdout)

    def test_clean_stage_passes_and_reports_work_left_outside(self):
        self.stage("ok.txt", "tudo certo\n")
        (self.alpha / "outro.txt").write_text("fica fora\n")
        report = gameops.preflight(self.hub, self.modules, "alpha")
        self.assertEqual(report["blocking"], [])
        self.assertIn("fora do stage e fora do commit: 0 modificados, 1 não rastreados", report["info"])
        self.assertEqual(self.cli("preflight", "games/alpha").returncode, 0)

    def test_identity_must_be_noreply_on_github_for_stage_and_for_every_commit_to_push(self):
        self.github_origin(self.alpha)
        self.stage("a.txt", "a\n")
        self.assertIn("user.email audit@example.invalid não é noreply", self.blocking())
        self.git(self.alpha, "commit", "-m", "com e-mail pessoal")
        self.identity(self.alpha, "1+example@users.noreply.github.com")
        self.assertIn("commits com e-mail que não é noreply: audit@example.invalid", self.blocking(push=True))
        self.git(self.alpha, "commit", "--amend", "--reset-author", "--no-edit")
        report = gameops.preflight(self.hub, self.modules, "alpha", push=True)
        self.assertEqual(report["blocking"], [])
        self.assertIn("1 commit a publicar", report["info"])

    def test_push_warns_when_the_folder_differs_from_the_commits_being_published(self):
        self.commit(self.alpha, "main.txt", "v2")
        (self.alpha / "main.txt").write_text("v3 de outra sessão\n")
        (self.alpha / "novo.txt").write_text("x\n")
        report = gameops.preflight(self.hub, self.modules, "alpha", push=True)
        self.assertEqual(report["blocking"], [])
        self.assertIn("fora do commit: 1 modificados, 1 não rastreados", report["info"])
        self.assertIn("1 arquivo do push tem alterações fora do commit (main.txt)", "\n".join(report["warnings"]))
        empty = gameops.preflight(self.hub, self.modules, "alpha")
        self.assertIn("nada no stage", empty["info"])
        self.assertIn("fora do stage e fora do commit: 1 modificados, 1 não rastreados", empty["info"])

    def test_hub_gitlink_must_point_to_a_published_module_commit(self):
        self.commit(self.alpha, "next.txt", "next")
        self.git(self.hub, "add", "games/alpha")
        hub = gameops.preflight(self.hub, self.modules, ".")
        self.assertIn("publique o módulo antes do hub", "\n".join(hub["blocking"]))
        self.git(self.alpha, "push", "origin", "main")
        self.assertEqual(gameops.preflight(self.hub, self.modules, ".")["blocking"], [])

    def test_push_with_nothing_new_and_unknown_repository(self):
        report = gameops.preflight(self.hub, self.modules, "alpha", push=True)
        self.assertIn("nada a publicar: HEAD já está em origin/main", report["info"])
        with self.assertRaisesRegex(ValueError, "Módulo não baixado"):
            gameops.preflight(self.hub, self.modules, "beta")
        with self.assertRaisesRegex(ValueError, "Repositório desconhecido"):
            gameops.preflight(self.hub, self.modules, "gama")


class GatesTest(GameOpsTest):
    def config(self, gates):
        path = self.hub / "framework/config.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"version": 1, "gameops": {"gates": gates}}))

    @unittest.skipUnless(shutil.which("npm"), "npm ausente")
    def test_package_scripts_run_in_declared_order_and_failures_are_reported(self):
        (self.alpha / "package.json").write_text(json.dumps({"scripts": {
            "build": "node -e \"process.exit(0)\"", "test": "node -e \"console.log('quebrou'); process.exit(3)\"",
            "lint": "node -e \"process.exit(0)\"", "deploy": "node -e \"process.exit(9)\""}}))
        listed = gameops.gates(self.hub, self.modules, "alpha")
        self.assertEqual([gate["name"] for gate in listed["gates"]], ["lint", "test", "build"])
        self.assertEqual({gate["status"] for gate in listed["gates"]}, {"listed"})
        ran = gameops.gates(self.hub, self.modules, "alpha", run=True)
        self.assertEqual([gate["status"] for gate in ran["gates"]], ["passed", "failed", "passed"])
        self.assertEqual(ran["failed"], 1)
        self.assertIn("quebrou", "\n".join(ran["gates"][1]["tail"]))
        self.assertEqual(self.cli("gates", "alpha", "--run").returncode, 1)

    def test_configured_hub_gates_run_only_when_their_paths_changed(self):
        python = shlex.quote(sys.executable)
        self.config({".": [{"name": "docs", "run": f"{python} -c \"print('ok')\"", "when": ["docs/"]},
                           f"{python} -c \"import sys; sys.exit(0)\""]})
        report = gameops.gates(self.hub, self.modules, ".", run=True)
        self.assertEqual([gate["status"] for gate in report["gates"]], ["skipped", "passed"])
        (self.hub / "docs").mkdir()
        (self.hub / "docs/nota.md").write_text("nova\n")
        report = gameops.gates(self.hub, self.modules, ".", run=True)
        self.assertEqual([gate["status"] for gate in report["gates"]], ["passed", "passed"])
        self.assertEqual(report["source"], "framework/config.json")

    def test_modified_tracked_file_in_the_first_status_line_triggers_its_gate(self):
        # Regressão: a primeira linha do status começa com espaço (" M caminho").
        python = shlex.quote(sys.executable)
        self.config({".": [{"name": "manifesto", "run": f"{python} -c \"print(1)\"", "when": ["workspace.json"]}]})
        self.git(self.hub, "add", "framework/config.json")
        self.git(self.hub, "commit", "-m", "config")
        self.assertEqual(gameops.gates(self.hub, self.modules, ".")["gates"][0]["status"], "skipped")
        (self.hub / "workspace.json").write_text(json.dumps({"version": 1, "modules": self.modules}, indent=1))
        self.assertEqual(gameops.gates(self.hub, self.modules, ".")["gates"][0]["status"], "listed")

    def test_worktree_paths_resolve_to_their_owner_and_unrelated_repositories_are_refused(self):
        python = shlex.quote(sys.executable)
        self.config({".": [f"{python} -c \"import sys; sys.exit(0)\""]})
        hub_tree, alpha_tree, stranger = self.base / "hub-tree", self.base / "alpha-tree", self.base / "stranger"
        self.git(self.hub, "worktree", "add", "--detach", str(hub_tree), "HEAD")
        self.git(self.alpha, "worktree", "add", "-b", "trabalho", str(alpha_tree), "main")
        self.assertEqual(gameops.resolve_target(self.hub, self.modules, str(hub_tree))[3], ".")
        checkout, label, module, owner = gameops.resolve_target(self.hub, self.modules, str(alpha_tree))
        self.assertEqual((checkout, module["id"], owner), (alpha_tree, "alpha", "games/alpha"))
        self.assertEqual(gameops.gates(self.hub, self.modules, str(hub_tree), run=True)["gates"][0]["status"],
                         "passed")
        (alpha_tree / "wip.md").write_text("caminho /home/fulano/jogo\n")
        self.git(alpha_tree, "add", "wip.md")
        report = gameops.preflight(self.hub, self.modules, str(alpha_tree))
        self.assertEqual(report["repository"], str(alpha_tree))
        self.assertIn("wip.md:1: caminho absoluto da máquina (/home/fulano/)", report["blocking"])
        self.git(self.base, "init", str(stranger))
        with self.assertRaisesRegex(ValueError, "não é worktree"):
            gameops.resolve_target(self.hub, self.modules, str(stranger))

    def test_missing_dependencies_and_undeclared_gates_are_explicit(self):
        (self.alpha / "package.json").write_text(json.dumps({
            "scripts": {"test": "node -e 0"}, "devDependencies": {"left-pad": "1.0.0"}}))
        report = gameops.gates(self.hub, self.modules, "alpha", run=True)
        self.assertEqual(report["gates"][0]["reason"], "dependências ausentes: rode npm ci antes")
        (self.alpha / "package.json").unlink()
        self.assertEqual(gameops.gates(self.hub, self.modules, "alpha")["gates"], [])
        self.assertIn("nenhuma verificação declarada", self.cli("gates", "alpha").stdout)


if __name__ == "__main__":
    unittest.main()
