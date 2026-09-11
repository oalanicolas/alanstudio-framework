import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import split_workspace
import workspace


class WorkspaceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workspace-split-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "source"
        self.source.mkdir()
        self.output = self.base / "prepared"
        self.git(self.source, "init", "--initial-branch=main")
        self.git(self.source, "config", "user.name", "Workspace Test")
        self.git(self.source, "config", "user.email", "workspace@example.invalid")
        self.modules = [
            {"id": "alpha", "path": "games/alpha"},
            {"id": "alpha-qa", "path": "games/alpha/qa"},
            {"id": "beta", "path": "games/beta"},
        ]
        for module in self.modules:
            module["url"] = (self.output / "repositories" / (module["id"] + ".git")).as_uri()
        self.write("workspace.json", json.dumps({"version": 1, "modules": self.modules,
                   "archive": "https://example.invalid/archive.git",
                   "repository": "https://example.invalid/hub.git"}))
        self.write("README.md", "Hub\n")
        self.write(".gitignore", ".env\n**/node_modules/\ngames/alpha/private/\n")
        self.write("games/alpha/main.txt", "original\n")
        self.write("games/alpha/qa/proof.txt", "evidence\n")
        self.write("games/beta/main.txt", "beta\n")
        script = self.write("games/alpha/run.sh", "#!/bin/sh\nexit 0\n")
        script.chmod(0o755)
        (self.source / "games/alpha/alias").symlink_to("main.txt")
        self.git(self.source, "add", ".")
        self.git(self.source, "commit", "-m", "initial")

    def git(self, root, *args):
        return subprocess.run(["git", "-C", str(root), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def write(self, relative, text):
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def prepare(self):
        return split_workspace.prepare(self.source, self.output, overlays=(), pack=True)

    def test_partition_preserves_content_modes_source_index_and_dirty_work(self):
        self.write("games/alpha/main.txt", "active work\n")
        self.write("games/alpha/new.txt", "untracked\n")
        self.write("games/alpha/.env", "LOCAL_ONLY=1\n")
        before = self.git(self.source, "status", "--porcelain")
        head = self.git(self.source, "rev-parse", "HEAD")
        index = (self.source / ".git/index").read_bytes()
        report = self.prepare()
        self.assertEqual(before, self.git(self.source, "status", "--porcelain"))
        self.assertEqual(head, self.git(self.source, "rev-parse", "HEAD"))
        self.assertEqual(index, (self.source / ".git/index").read_bytes())
        alpha = self.output / "repositories/alpha.git"
        self.assertEqual(self.git(alpha, "show", "HEAD:main.txt"), "original")
        self.assertEqual((self.source / "games/alpha/main.txt").read_text(), "active work\n")
        files = split_workspace.entries(alpha, "HEAD")
        self.assertEqual(files["run.sh"][0], "100755")
        self.assertEqual(files["alias"][0], "120000")
        self.assertEqual(files["qa"][0], "160000")
        self.assertNotIn("qa/proof.txt", files)
        self.assertNotIn("new.txt", files)
        self.assertNotIn(".env", files)
        self.assertIn("/private/", self.git(alpha, "show", "HEAD:.gitignore"))
        self.assertTrue(all(item["self_contained"] for item in report["modules"]))
        for item in report["modules"]:
            repo = Path(item["repository"])
            self.assertFalse((repo / "objects/info/alternates").exists())
            self.git(repo, "fsck", "--full", "--no-dangling")
            self.assertEqual(self.git(repo, "rev-list", "--count", "HEAD"), "1")
        with self.assertRaises(ValueError):
            self.prepare()

    def test_clone_selects_parent_then_nested_module_without_siblings(self):
        self.prepare()
        root = self.output / "checkout"
        self.assertFalse((root / "games/alpha/main.txt").exists())
        env = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "protocol.file.allow",
               "GIT_CONFIG_VALUE_0": "always"}
        with patch.dict(os.environ, env):
            workspace.get_modules(root, ["alpha"], self.modules)
            self.assertEqual((root / "games/alpha/main.txt").read_text(), "original\n")
            self.assertFalse((root / "games/alpha/qa/proof.txt").exists())
            self.assertFalse((root / "games/beta/main.txt").exists())
            (root / "games/alpha/main.txt").write_text("local work\n")
            workspace.get_modules(root, ["alpha-qa"], self.modules)
        self.assertEqual((root / "games/alpha/main.txt").read_text(), "local work\n")
        self.assertEqual((root / "games/alpha/qa/proof.txt").read_text(), "evidence\n")
        self.assertFalse((root / "games/beta/main.txt").exists())

    def test_selection_validates_all_names_before_initializing_anything(self):
        with self.assertRaises(ValueError), patch("workspace.subprocess.run") as run:
            workspace.get_modules(self.source, ["alpha", "missing"], self.modules)
        run.assert_not_called()
        self.assertEqual([item["id"] for item in workspace.selection(
            ["games/alpha/qa", "alpha"], self.modules)], ["alpha", "alpha-qa"])

    def test_legacy_checkout_is_not_mistaken_for_a_submodule_hub(self):
        with self.assertRaisesRegex(ValueError, "não modularizado"):
            workspace.get_modules(self.source, ["alpha"], self.modules)

    def test_missing_optional_sound_catalog_is_not_reported_as_an_empty_library(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "game.py"), "--root", str(self.source),
             "sfx", "search", "tiro"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(str(SCRIPTS / "workspace.py"), result.stderr)
        self.assertIn(str(self.source), result.stderr)
        self.assertIn("get sfx", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertFalse((self.source / "shared").exists())

    def test_manifest_rejects_path_escape_and_duplicate(self):
        for paths in (("../escape", "beta"), ("same", "same")):
            for module, path in zip(self.modules, paths):
                module["path"] = path
            self.write("workspace.json", json.dumps({"version": 1, "modules": self.modules}))
            with self.assertRaises(ValueError):
                workspace.load_manifest(self.source)

    def test_repository_owner_comes_from_manifest_and_can_be_overridden(self):
        data = {"version": 1, "repository": "https://github.com/another-studio/lab.git",
                "modules": [{"id": "demo", "path": "titles/demo", "repository": "demo-game"}]}
        self.write("workspace.json", json.dumps(data))
        self.assertEqual(workspace.load_manifest(self.source)["modules"][0]["url"],
                         "https://github.com/another-studio/demo-game.git")
        data["repository_base_url"] = "https://git.example.org/collection"
        self.write("workspace.json", json.dumps(data))
        self.assertEqual(workspace.load_manifest(self.source)["modules"][0]["url"],
                         "https://git.example.org/collection/demo-game.git")

    def test_configured_overlays_preserve_links_without_copying_shared_code(self):
        self.write("framework/config.json", json.dumps({"version": 1, "module_overlays": [
            "workspace.json", "framework/config.json", "framework/core", "framework/scripts/game.py"]}))
        self.write("framework/scripts/game.py", "# local entry point\n")
        (self.source / "framework/core").symlink_to("../../external-core", target_is_directory=True)
        report = split_workspace.prepare(self.source, self.output, pack=True)
        hub = self.output / "repositories/hub.git"
        files = split_workspace.entries(hub, "HEAD")
        self.assertEqual(files["framework/core"][0], "120000")
        self.assertEqual(self.git(hub, "show", "HEAD:framework/core"), "../../external-core")
        self.assertEqual(self.git(hub, "show", "HEAD:framework/scripts/game.py"), "# local entry point")
        self.assertFalse(any(name.startswith("framework/core/") for name in files))
        self.assertFalse(report["published"])

    def test_default_extraction_does_not_overlay_personal_readme_changes(self):
        self.write("README.md", "unfinished local direction")
        split_workspace.prepare(self.source, self.output, pack=True)
        self.assertEqual(self.git(self.output / "repositories/hub.git", "show", "HEAD:README.md"), "Hub")
        self.assertEqual((self.source / "README.md").read_text(), "unfinished local direction")

    def test_overlay_escape_is_rejected_before_creating_any_repository(self):
        self.write("framework/config.json", json.dumps({"version": 1, "module_overlays": ["../outside"]}))
        with self.assertRaisesRegex(ValueError, "fora do workspace"):
            split_workspace.prepare(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_external_gitlink_gets_url_and_keeps_its_commit(self):
        external_commit = self.git(self.source, "rev-parse", "HEAD")
        self.git(self.source, "update-index", "--add", "--cacheinfo",
                 "160000", external_commit, "games/alpha/reference")
        self.modules.append({"id": "reference", "path": "games/alpha/reference",
                             "url": "https://example.invalid/reference.git", "external": True})
        data = json.loads((self.source / "workspace.json").read_text())
        data["modules"] = self.modules
        self.write("workspace.json", json.dumps(data))
        self.git(self.source, "add", "workspace.json")
        self.git(self.source, "commit", "-m", "external reference")
        self.prepare()
        repo = self.output / "repositories/alpha.git"
        self.assertEqual(split_workspace.entries(repo, "HEAD")["reference"], ("160000", external_commit))
        self.assertIn("https://example.invalid/reference.git", self.git(repo, "show", "HEAD:.gitmodules"))
        self.assertFalse((self.output / "repositories/reference.git").exists())

    def test_unavailable_upstream_can_be_mirrored_without_changing_the_pinned_commit(self):
        reference = self.source / "games/alpha/reference"
        reference.mkdir()
        self.git(reference, "init", "--initial-branch=main")
        self.git(reference, "config", "user.name", "Reference Author")
        self.git(reference, "config", "user.email", "reference@example.invalid")
        (reference / "README.md").write_text("reference snapshot")
        self.git(reference, "add", "README.md")
        self.git(reference, "commit", "-m", "reference")
        commit = self.git(reference, "rev-parse", "HEAD")
        self.modules.append({"id": "reference", "path": "games/alpha/reference",
                             "url": "https://example.invalid/private-mirror.git",
                             "upstream_url": "https://example.invalid/original.git",
                             "external": True, "mirror": True})
        data = json.loads((self.source / "workspace.json").read_text())
        data["modules"] = self.modules
        self.write("workspace.json", json.dumps(data))
        self.git(self.source, "add", "workspace.json", "games/alpha/reference")
        self.git(self.source, "commit", "-m", "pin reference")
        report = self.prepare()
        mirror = self.output / "repositories/reference.git"
        self.assertEqual(self.git(mirror, "rev-parse", "HEAD"), commit)
        self.assertEqual(self.git(mirror, "show", "HEAD:README.md"), "reference snapshot")
        self.assertTrue(next(m for m in report["modules"] if m["id"] == "reference")["mirror"])
        self.assertEqual(self.git(reference, "rev-parse", "HEAD"), commit)

    def test_snapshot_mirror_keeps_the_tree_without_importing_private_commit_metadata(self):
        reference = self.source / "games/alpha/reference"
        reference.mkdir()
        self.git(reference, "init", "--initial-branch=main")
        self.git(reference, "config", "user.name", "Reference Author")
        self.git(reference, "config", "user.email", "private@example.invalid")
        (reference / "README.md").write_text("same content")
        self.git(reference, "add", "README.md")
        self.git(reference, "commit", "-m", "original")
        commit = self.git(reference, "rev-parse", "HEAD")
        module = {"id": "reference", "path": "games/alpha/reference",
                  "url": "https://example.invalid/mirror.git", "upstream_url": "https://example.invalid/source.git",
                  "external": True, "mirror": True, "mirror_snapshot": True}
        self.modules.append(module)
        data = json.loads((self.source / "workspace.json").read_text())
        data["modules"] = self.modules
        self.write("workspace.json", json.dumps(data))
        self.git(self.source, "add", "workspace.json", "games/alpha/reference")
        self.git(self.source, "commit", "-m", "pin reference")
        report = self.prepare()
        mirror = self.output / "repositories/reference.git"
        snapshot = self.git(mirror, "rev-parse", "HEAD")
        self.assertNotEqual(snapshot, commit)
        self.assertEqual(self.git(mirror, "rev-parse", "HEAD^{tree}"), self.git(reference, "rev-parse", "HEAD^{tree}"))
        self.assertEqual(self.git(mirror, "rev-list", "--count", "HEAD"), "1")
        self.assertNotIn("private@example.invalid", self.git(mirror, "log", "--all", "--format=fuller"))
        alpha = self.output / "repositories/alpha.git"
        self.assertEqual(split_workspace.entries(alpha, "HEAD")["reference"], ("160000", snapshot))
        self.assertEqual(report["replaced_gitlinks"][0]["source_commit"], commit)

    def test_lfs_object_and_inherited_attribute_follow_the_project(self):
        content = b"binary artist asset\x00\x01"
        digest = hashlib.sha256(content).hexdigest()
        pointer = ("version https://git-lfs.github.com/spec/v1\n"
                   f"oid sha256:{digest}\nsize {len(content)}\n")
        self.write("games/alpha/model.asset", pointer)
        self.write(".gitattributes", "games/alpha/model.asset filter=lfs diff=lfs merge=lfs -text\n")
        origin = self.source / ".git/lfs/objects" / digest[:2] / digest[2:4] / digest
        origin.parent.mkdir(parents=True)
        origin.write_bytes(content)
        self.git(self.source, "-c", "filter.lfs.clean=cat", "-c", "filter.lfs.process=",
                 "-c", "filter.lfs.required=false", "add", ".gitattributes", "games/alpha/model.asset")
        self.git(self.source, "commit", "-m", "LFS asset")
        report = self.prepare()
        alpha = self.output / "repositories/alpha.git"
        self.assertEqual(self.git(alpha, "show", "HEAD:model.asset"), pointer.strip())
        self.assertEqual(self.git(alpha, "show", "HEAD:.gitattributes"),
                         "model.asset filter=lfs diff=lfs merge=lfs -text")
        self.assertEqual((alpha / "lfs/objects" / digest[:2] / digest[2:4] / digest).read_bytes(), content)
        self.assertEqual(report["lfs"][0]["oid"], digest)

    def test_publication_excludes_production_media_but_keeps_runtime_docs_and_fixtures(self):
        self.modules = [item for item in self.modules if item["id"] != "alpha-qa"]
        data = json.loads((self.source / "workspace.json").read_text())
        data["modules"] = self.modules
        data["publication"] = {"document_only_paths": ["games/alpha/qa"],
                               "document_extensions": [".md", ".json"]}
        self.write("workspace.json", json.dumps(data))
        self.write("games/alpha/qa/frame.png", "heavy evidence")
        self.write("games/alpha/qa/report.md", "documented result")
        self.write("games/alpha/qa/session.json", '{"fixture":true}')
        self.write("games/alpha/qa/source.blend", "heavy source")
        self.write("games/alpha/qa/source-desktop.png", "reference image")
        self.write("games/alpha/qa/LICENSE-photo.png", "image is not a license")
        self.write("games/alpha/qa/license.txt", "license terms")
        self.write("games/alpha/qa/CrEdItS", "authors")
        self.write("games/alpha/runtime.png", "necessary game texture")
        with (self.source / ".gitignore").open("a") as handle:
            handle.write("\ngames/alpha/qa/generated-build/\n")
        self.git(self.source, "add", ".")
        self.git(self.source, "commit", "-m", "publication scope")
        report = self.prepare()
        repo = self.output / "repositories/alpha.git"
        actual = split_workspace.entries(repo, "HEAD")
        self.assertNotIn("qa/frame.png", actual)
        self.assertNotIn("qa/proof.txt", actual)
        for path in ("qa/source.blend", "qa/source-desktop.png", "qa/LICENSE-photo.png"):
            self.assertNotIn(path, actual)
        for path in ("runtime.png", "qa/report.md", "qa/session.json", "qa/license.txt", "qa/CrEdItS"):
            self.assertIn(path, actual)
        self.assertTrue((self.source / "games/alpha/qa/frame.png").exists())
        self.assertEqual({entry["path"] for entry in report["excluded_paths"]},
                         {"games/alpha/qa/frame.png", "games/alpha/qa/proof.txt",
                          "games/alpha/qa/source.blend", "games/alpha/qa/source-desktop.png",
                          "games/alpha/qa/LICENSE-photo.png"})
        checkout = self.base / "policy-checkout"
        self.git(self.source, "clone", str(repo), str(checkout))
        self.git(checkout, "config", "core.ignorecase", "false")
        for path in ("qa/source.blend", "qa/SOURCE-photo.png", "qa/LICENSE-photo.png",
                     "qa/generated-build/report.md", "qa/generated-build/session.json"):
            result = subprocess.run(["git", "-C", str(checkout), "check-ignore", "--no-index", path],
                                    capture_output=True)
            self.assertEqual(result.returncode, 0, path)
        for path in ("qa/license.txt", "qa/CrEdItS", "qa/SOURCE.md", "qa/report.md",
                     "qa/session.json", "runtime.png"):
            result = subprocess.run(["git", "-C", str(checkout), "check-ignore", "--no-index", path],
                                    capture_output=True)
            self.assertEqual(result.returncode, 1, path)


if __name__ == "__main__":
    unittest.main()
