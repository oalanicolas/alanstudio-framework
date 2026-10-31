import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tracemalloc
import unittest
import uuid
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
FRAMEWORK_ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
import gameops


FIXTURE_BASE = FRAMEWORK_ROOT / "output/agentes/preflight-stream-tests"


def legacy_added_lines(diff):
    """Preserved reference implementation for differential tests."""
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


class GameOpsStreamTest(unittest.TestCase):
    def setUp(self):
        FIXTURE_BASE.mkdir(parents=True, exist_ok=True)
        self.fixture = FIXTURE_BASE / f"case-{os.getpid()}-{uuid.uuid4().hex}"
        self.fixture.mkdir()
        self.addCleanup(shutil.rmtree, self.fixture, ignore_errors=True)

        self.hub = self.fixture / "hub"
        self.repo = self.hub / "games/alpha"
        self.hub.mkdir()
        self.repo.mkdir(parents=True)
        self.git(self.hub, "init", "--initial-branch=main")
        self.git(self.repo, "init", "--initial-branch=main")
        for root in (self.hub, self.repo):
            self.git(root, "config", "user.name", "GameOps Fixture")
            self.git(root, "config", "user.email", "fixture@example.invalid")
            self.git(root, "config", "core.quotePath", "false")
        self.modules = [{"id": "alpha", "path": "games/alpha", "url": "file:///fixture/alpha.git"}]

    def git(self, root, *args):
        return subprocess.run(["git", "-C", str(root), *args], check=True,
                              capture_output=True, text=True, errors="replace").stdout

    def reference_diff(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), "diff", *args, "-U0", "--no-color", "--no-ext-diff"],
            check=True, capture_output=True, text=True, errors="replace").stdout

    def test_staged_stream_matches_legacy_parser_for_unicode_crlf_and_paths(self):
        path = self.repo / "dados com espaço/árvore-🧪.txt"
        path.parent.mkdir()
        path.write_bytes("\u03b1\r\nlinha\u2028separada\u0085com unicode\rfinal\n".encode("utf-8"))
        self.git(self.repo, "add", "--", str(path.relative_to(self.repo)))

        diff = self.reference_diff("--cached")
        expected = list(legacy_added_lines(diff))
        actual = list(gameops.stream_added_lines(
            self.repo, "diff", "--cached", "-U0", "--no-color", "--no-ext-diff"))
        self.assertEqual(actual, expected)
        self.assertEqual(list(gameops.added_lines(diff)), expected)

    def test_committed_range_stream_matches_legacy_parser(self):
        file = self.repo / "change.txt"
        file.write_text("base\n", encoding="utf-8")
        self.git(self.repo, "add", "change.txt")
        self.git(self.repo, "commit", "-m", "base")
        base = self.git(self.repo, "rev-parse", "HEAD").strip()
        file.write_text("base\nadded π\n", encoding="utf-8")
        self.git(self.repo, "add", "change.txt")
        self.git(self.repo, "commit", "-m", "change")

        diff = self.reference_diff(f"{base}..HEAD")
        expected = list(legacy_added_lines(diff))
        actual = list(gameops.stream_added_lines(
            self.repo, "diff", f"{base}..HEAD", "-U0", "--no-color", "--no-ext-diff"))
        self.assertEqual(actual, expected)
        self.assertIn(("change.txt", 2, "added π"), actual)

    def test_binary_diff_has_same_empty_added_line_result(self):
        binary = self.repo / "blob.bin"
        binary.write_bytes(b"\x00\xff\x80\x00" * 2048)
        self.git(self.repo, "add", "blob.bin")
        diff = self.reference_diff("--cached")
        expected = list(legacy_added_lines(diff))
        actual = list(gameops.stream_added_lines(
            self.repo, "diff", "--cached", "-U0", "--no-color", "--no-ext-diff"))
        self.assertEqual(actual, expected)
        self.assertEqual(actual, [])
        self.assertIn("Binary files", diff)

    def test_large_diff_finds_issues_at_start_middle_and_end_with_bounded_python_memory(self):
        count = 180_000
        file = self.repo / "large.txt"
        with file.open("w", encoding="utf-8", newline="\n") as stream:
            for index in range(count):
                if index == 0:
                    line = "path " + "/" + "Users/example/private/key.txt"
                elif index == count // 2:
                    line = "credential ghp_" + "a" * 36
                elif index == count - 1:
                    line = "<<<<<<< HEAD"
                else:
                    line = f"record-{index:07d}-" + "x" * 112
                stream.write(line + "\n")
        source_bytes = file.stat().st_size
        self.git(self.repo, "add", "large.txt")

        tracemalloc.start()
        scanned = sum(1 for _ in gameops.stream_added_lines(
            self.repo, "diff", "--cached", "-U0", "--no-color", "--no-ext-diff"))
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.assertEqual(scanned, count)
        self.assertLess(peak, source_bytes // 2, f"scanner peak {peak} exceeded half of {source_bytes} bytes")

        report = gameops.preflight(self.hub, self.modules, "alpha")
        blocking = "\n".join(report["blocking"])
        self.assertIn("large.txt:1: caminho absoluto da máquina", blocking)
        self.assertIn("large.txt:90001: possível token do GitHub", blocking)
        self.assertIn("large.txt:180000: marcador de conflito", blocking)

    def test_git_nonzero_status_drains_stderr_and_blocks_preflight(self):
        self.repo.joinpath("safe.txt").write_text("safe\n", encoding="utf-8")
        self.git(self.repo, "add", "safe.txt")
        fake_bin = self.fixture / "fake-bin"
        fake_bin.mkdir()
        fake_git = fake_bin / "git"
        real_git = shutil.which("git")
        script = f'''#!/bin/sh
case " $* " in
  *" -U0 --no-color --no-ext-diff "*)
    printf '%s\\n' 'diff --git a/safe.txt b/safe.txt' '--- /dev/null' '+++ b/safe.txt' '@@ -0,0 +1,1 @@' '+safe'
    dd if=/dev/zero bs=8192 count=32 2>/dev/null | tr '\\000' 'x' >&2
    printf '%s\\n' 'GIT_ERROR_TAIL' >&2
    exit 37;;
esac
exec {real_git!r} "$@"
'''
        fake_git.write_text(script, encoding="utf-8")
        fake_git.chmod(0o755)
        with patch.dict(os.environ, {"PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", "")}):
            with self.assertRaises(gameops.GitDiffError) as caught:
                list(gameops.stream_added_lines(
                    self.repo, "diff", "--cached", "-U0", "--no-color", "--no-ext-diff"))
            self.assertEqual(caught.exception.returncode, 37)
            self.assertLessEqual(len(caught.exception.stderr), 16_384)
            self.assertTrue(caught.exception.stderr.endswith("GIT_ERROR_TAIL\n"))

            report = gameops.preflight(self.hub, self.modules, "alpha")
        self.assertTrue(any("git diff falhou (código 37)" in item for item in report["blocking"]))
        self.assertTrue(any("GIT_ERROR_TAIL" in item for item in report["blocking"]))


if __name__ == "__main__":
    unittest.main()
