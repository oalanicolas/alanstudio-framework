import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/game.py"
SPEC = importlib.util.spec_from_file_location("game_harness_serve", SCRIPT)
game = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(game)

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Teste", "GIT_AUTHOR_EMAIL": "teste@example.com",
    "GIT_COMMITTER_NAME": "Teste", "GIT_COMMITTER_EMAIL": "teste@example.com",
}
TINY_SERVER = (
    "import os, http.server as h; "
    "h.ThreadingHTTPServer(('127.0.0.1', int(os.environ['PORT'])), h.SimpleHTTPRequestHandler).serve_forever()"
)


def git(cwd, *args):
    result = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                            env={**os.environ, **GIT_ENV}, check=True)
    return result.stdout.strip()


def commit_all(cwd, message):
    git(cwd, "add", "-A")
    git(cwd, "-c", "commit.gpgsign=false", "commit", "-q", "-m", message)


class ServeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name).resolve()
        self.project = self.root / "jogos" / "alfa"
        self.project.mkdir(parents=True)
        (self.project / "index.html").write_text("<h1>alfa</h1>")
        git(self.project, "init", "-q", "-b", "main")
        commit_all(self.project, "inicio")
        self.launch = {"script": "serve", "argv": [sys.executable, "-c", TINY_SERVER]}
        self.addCleanup(self.cleanup_servers)

    def cleanup_servers(self):
        for item in game.serve_list(self.root)["servers"]:
            game.serve_stop(self.root / item["project"], self.root)

    def start(self, **extra):
        return game.serve_start(self.project, self.root, timeout=15, launch=self.launch, **extra)

    def test_picks_a_free_port_and_never_a_busy_one(self):
        with socket.socket() as busy:
            busy.bind(("127.0.0.1", 0))
            busy.listen()
            taken = busy.getsockname()[1]
            result = self.start()
            self.assertNotEqual(result["port"], taken)
        self.assertTrue(game.serve_http_ok(result["url"]))
        self.assertEqual(result["url"], f"http://localhost:{result['port']}/")
        self.assertEqual(result["status"], "iniciado")
        probe = game.serve_free_port()
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", probe))

    def test_state_file_records_pid_port_cwd_commit_command_and_time(self):
        result = self.start()
        state = json.loads(game.serve_state_path(self.project, self.root).read_text())
        self.assertEqual(state["pid"], result["pid"])
        self.assertEqual(state["port"], result["port"])
        self.assertEqual(state["cwd"], str(self.project))
        self.assertEqual(state["commit"], git(self.project, "rev-parse", "HEAD"))
        self.assertIn("-c", state["command"])
        self.assertTrue(state["started_at"])
        self.assertEqual(game.serve_state_dir(self.root), self.root / "output" / "serve")

    def test_project_outside_registry_root_has_serializable_paths(self):
        registry = self.root / "separate-registry"
        short = game._short_path(self.project, registry)
        self.assertEqual(json.loads(json.dumps({"project": short}))["project"], str(self.project))
        self.assertIsNone(game._short_path(None, registry))
        self.addCleanup(game.serve_stop, self.project, registry)
        result = game.serve_start(self.project, registry, timeout=15, launch=self.launch)
        self.assertEqual(result["project"], str(self.project))
        self.assertTrue(game.serve_http_ok(result["url"]))
        state = json.loads(game.serve_state_path(self.project, registry).read_text())
        self.assertEqual(state["pid"], result["pid"])

    def test_reuses_live_server_for_same_cwd_and_commit(self):
        first = self.start()
        second = self.start()
        self.assertEqual(second["status"], "reaproveitado")
        self.assertEqual((second["pid"], second["port"], second["url"]), (first["pid"], first["port"], first["url"]))
        self.assertTrue(game.serve_alive({"pid": first["pid"]}))

    def test_new_commit_replaces_only_the_registered_pid(self):
        bystander = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
        self.addCleanup(lambda: (bystander.kill(), bystander.wait()))
        first = self.start()
        (self.project / "index.html").write_text("<h1>beta</h1>")
        commit_all(self.project, "segundo")
        second = self.start()
        self.assertEqual(second["status"], "iniciado")
        self.assertIn("commit", second["restarted"])
        self.assertNotEqual(second["pid"], first["pid"])
        self.assertFalse(game.serve_alive({"pid": first["pid"]}))
        self.assertTrue(game.serve_http_ok(second["url"]))
        self.assertIsNone(bystander.poll())

    def test_local_edits_restart_the_server(self):
        first = self.start()
        (self.project / "index.html").write_text("<h1>editado</h1>")
        second = self.start()
        self.assertEqual(second["status"], "iniciado")
        self.assertNotEqual(second["pid"], first["pid"])
        self.assertIn("alterações locais", second["restarted"])

    def test_dead_process_is_replaced(self):
        first = self.start()
        os.killpg(first["pid"], signal.SIGKILL)
        for _ in range(100):
            if not game.serve_alive({"pid": first["pid"]}):
                break
            game.serve_pause(0.05)
        second = self.start()
        self.assertEqual(second["status"], "iniciado")
        self.assertIn("morreu", second["restarted"])
        self.assertNotEqual(second["pid"], first["pid"])

    def test_stop_ends_only_the_registered_pid(self):
        bystander = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
        self.addCleanup(lambda: (bystander.kill(), bystander.wait()))
        result = self.start()
        stopped = game.serve_stop(self.project, self.root)
        self.assertEqual(stopped["status"], "encerrado")
        self.assertFalse(game.serve_alive({"pid": result["pid"]}))
        self.assertIsNone(bystander.poll())
        self.assertFalse(game.serve_state_path(self.project, self.root).exists())
        again = game.serve_stop(self.project, self.root)
        self.assertEqual(again["status"], "sem servidor registrado")

    def test_stop_never_signals_a_reused_pid(self):
        bystander = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
        self.addCleanup(lambda: (bystander.kill(), bystander.wait()))
        game.serve_write_entry(game.serve_state_path(self.project, self.root),
                               {"project": "jogos/alfa", "pid": bystander.pid, "started": "Mon Jan  1 00:00:00 2001"})
        stopped = game.serve_stop(self.project, self.root)
        self.assertEqual(stopped["status"], "já estava morto")
        self.assertIsNone(bystander.poll())

    def test_list_marks_alive_and_dead(self):
        result = self.start()
        listing = game.serve_list(self.root)["servers"]
        self.assertEqual([(item["project"], item["status"], item["alive"]) for item in listing],
                         [("jogos/alfa", "vivo", True)])
        os.killpg(result["pid"], signal.SIGKILL)
        for _ in range(100):
            if not game.serve_alive({"pid": result["pid"]}):
                break
            game.serve_pause(0.05)
        listing = game.serve_list(self.root)["servers"]
        self.assertEqual((listing[0]["status"], listing[0]["alive"]), ("morto", False))

    def test_failed_start_reports_log_and_leaves_no_state(self):
        broken = {"script": "serve", "argv": [sys.executable, "-c", "print('quebrou'); raise SystemExit(3)"]}
        with self.assertRaises(ValueError) as caught:
            game.serve_start(self.project, self.root, timeout=10, launch=broken)
        self.assertIn("quebrou", str(caught.exception))
        self.assertFalse(game.serve_state_path(self.project, self.root).exists())

    def cli(self, as_json):
        args = argparse.Namespace(project=str(self.project), stop=False, list=False, json=as_json, timeout=15)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), mock.patch.object(game, "serve_launch", return_value=self.launch):
            self.assertEqual(game.serve_cli(args, self.root), 0)
        return out.getvalue()

    def test_cli_prints_url_on_first_line_and_json_on_demand(self):
        first = self.cli(False).splitlines()
        self.assertRegex(first[0], r"^http://localhost:\d+/$")
        self.assertIn("iniciado", first[1])
        data = json.loads(self.cli(True))
        self.assertEqual(data["status"], "reaproveitado")
        self.assertEqual(data["url"], first[0])


class ServeLaunchTests(unittest.TestCase):
    def package(self, scripts):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        (Path(tmp.name) / "package.json").write_text(json.dumps({"name": "x", "scripts": scripts}))
        return Path(tmp.name)

    def test_uses_the_script_the_play_command_uses(self):
        project = self.package({"test": "node t.js", "serve": "node server.js"})
        self.assertEqual(game.serve_launch(project), {"script": "serve", "argv": ["npm", "run", "serve"]})

    def test_vite_without_port_gets_the_free_port_flag(self):
        project = self.package({"dev": "vite --host 127.0.0.1"})
        self.assertEqual(game.serve_launch(project)["argv"], ["npm", "run", "dev", "--", "--port", "{port}", "--strictPort"])

    def test_refuses_project_without_server_script(self):
        project = self.package({"test": "node t.js"})
        with self.assertRaises(ValueError):
            game.serve_launch(project)


class ContextWorktreesTests(unittest.TestCase):
    def test_context_lists_worktrees_and_branches_with_dirty_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            project = base / "repo"
            project.mkdir()
            git(project, "init", "-q", "-b", "main")
            (project / "a.txt").write_text("a")
            commit_all(project, "inicio")
            other = base / "repo-fatia"
            git(project, "worktree", "add", "-q", "-b", "fatia", str(other))
            (other / "novo.txt").write_text("sujo")
            git(project, "branch", "solta")
            result = game.git_worktrees(project)
            by_name = {item["name"]: item for item in result["worktrees"]}
            self.assertEqual(set(by_name), {"repo", "repo-fatia"})
            self.assertEqual(by_name["repo"]["branch"], "main")
            self.assertTrue(by_name["repo"]["current"])
            self.assertFalse(by_name["repo"]["dirty"])
            self.assertTrue(by_name["repo-fatia"]["dirty"])
            self.assertEqual(by_name["repo-fatia"]["path"], str(other))
            self.assertIn("inicio", by_name["repo-fatia"]["last_commit"])
            branches = {item["name"]: item["worktree"] for item in result["branches"]}
            self.assertEqual(branches, {"main": str(project), "fatia": str(other), "solta": None})
            full = game.context(project, "create", root=base)
            self.assertEqual(full["worktrees"]["branches"], result["branches"])
            brief = game.brief_context(full, base, base / "out" / "ctx.json")
            self.assertEqual(len(brief["worktrees"]), 2)
            self.assertEqual(brief["branches_sem_worktree"], ["solta"])

    def test_outside_a_repository_the_field_is_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(game.subprocess, "run", side_effect=OSError):
                self.assertIsNone(game.git_worktrees(Path(tmp)))


if __name__ == "__main__":
    unittest.main()
