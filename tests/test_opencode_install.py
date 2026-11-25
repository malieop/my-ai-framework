"""Filesystem integration checks; OpenCode discovery requires a running server."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from scripts.install_opencode import install


class OpenCodeInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "framework with spaces"
        self.config = self.base / "config"
        for name in (
            "adapters/opencode/agents/feature-design.md",
            "adapters/opencode/agents/feature-implementor.md",
            "adapters/opencode/commands/feature-implementation.md",
            "skills/implementation-planning/SKILL.md",
            "workflows/feature-implementation.md",
        ):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture\n")

    def run_install(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return install(self.config, root=self.root, **kwargs)

    def test_install_links_and_updates_without_copying(self):
        links = self.run_install()
        for destination, source in links:
            self.assertTrue(destination.is_symlink())
            self.assertEqual(destination.resolve(), source.resolve())
        source = self.root / "adapters/opencode/agents/feature-design.md"
        source.write_text("updated\n")
        self.assertEqual((self.config / "agents/feature-design.md").read_text(), "updated\n")
        skill = self.config / "frameworks/my-ai-framework/skills/implementation-planning/SKILL.md"
        self.assertTrue(skill.is_file())
        self.assertEqual(
            (skill.parent / "../../workflows/feature-implementation.md").read_text(),
            "fixture\n",
        )

    def test_idempotent_install_preserves_unrelated_config(self):
        self.config.mkdir()
        config = self.config / "opencode.jsonc"
        config.write_text('{"unrelated": true}\n')
        unrelated = self.config / "agents/build.md"
        unrelated.parent.mkdir()
        unrelated.write_text("personal agent\n")
        self.run_install()
        link = self.config / "agents/feature-design.md"
        before = link.lstat().st_mtime_ns
        self.run_install()
        self.assertEqual(link.lstat().st_mtime_ns, before)
        self.assertEqual(config.read_text(), '{"unrelated": true}\n')
        self.assertEqual(unrelated.read_text(), "personal agent\n")
        self.assertFalse((self.config / "framework-backups").exists())

    def test_conflict_aborts_before_any_install_writes(self):
        conflict = self.config / "agents/feature-design.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("original\n")
        with self.assertRaises(FileExistsError):
            self.run_install()
        self.assertEqual(conflict.read_text(), "original\n")
        self.assertFalse((self.config / "frameworks").exists())

    def test_replace_backs_up_conflicting_entries_outside_discovery(self):
        conflict = self.config / "agents/feature-design.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("original\n")
        dangling = self.config / "agents/feature-implementor.md"
        dangling.symlink_to(self.base / "missing.md")
        self.run_install(replace=True)
        backups = list((self.config / "framework-backups").iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "agents/feature-design.md").read_text(), "original\n")
        self.assertTrue((backups[0] / "agents/feature-implementor.md").is_symlink())
        self.assertTrue(conflict.is_symlink())
        self.assertTrue(dangling.exists())

    def test_dry_run_does_not_write_even_with_replace(self):
        self.run_install(dry_run=True)
        self.assertFalse(self.config.exists())
        conflict = self.config / "agents/feature-design.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("original\n")
        self.run_install(replace=True, dry_run=True)
        self.assertFalse(conflict.is_symlink())
        self.assertEqual(conflict.read_text(), "original\n")
        self.assertFalse((self.config / "framework-backups").exists())

    def test_reinstall_links_new_entries(self):
        self.run_install()
        new = self.root / "adapters/opencode/commands/feature-design.md"
        new.write_text("new command\n")
        self.run_install()
        self.assertEqual((self.config / "commands/feature-design.md").resolve(), new.resolve())

    def test_parent_conflicts_abort_before_writes(self):
        for dangling in (False, True):
            with self.subTest(dangling=dangling):
                config = self.base / f"parent-conflict-{dangling}"
                config.mkdir()
                parent = config / "commands"
                if dangling:
                    parent.symlink_to(self.base / "missing-directory")
                else:
                    parent.write_text("not a directory\n")
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(FileExistsError):
                    install(config, root=self.root, replace=True)
                self.assertFalse((config / "frameworks").exists())
                self.assertFalse((config / "agents").exists())

    def test_reinstall_removes_only_obsolete_framework_links(self):
        self.run_install()
        source = self.root / "adapters/opencode/commands/feature-implementation.md"
        source.rename(source.with_name("renamed.md"))
        unrelated = self.config / "commands/personal.md"
        unrelated.symlink_to(self.base / "personal-missing.md")
        self.run_install()
        self.assertFalse((self.config / "commands/feature-implementation.md").is_symlink())
        self.assertTrue((self.config / "commands/renamed.md").is_symlink())
        self.assertTrue(unrelated.is_symlink())

    def test_framework_link_exposes_skill_additions_and_preserves_relative_paths(self):
        self.run_install()
        source = self.root / "skills/new-skill/SKILL.md"
        source.parent.mkdir()
        source.write_text("new skill\n")
        linked = self.config / "frameworks/my-ai-framework/skills/new-skill/SKILL.md"
        self.assertEqual(linked.read_text(), "new skill\n")
        old_link = self.config / "skills/implementation-planning"
        old_link.parent.mkdir()
        old_link.symlink_to(self.root / "skills/implementation-planning")
        self.run_install()
        self.assertFalse(old_link.is_symlink())


if __name__ == "__main__":
    unittest.main()
