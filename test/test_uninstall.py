#!/usr/bin/env python3
# Copyright (C) 2026 Qore Technologies, s.r.o.
# SPDX-License-Identifier: MIT
"""Check CMake uninstall with disposable staged files only."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class UninstallTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="uuid uninstall ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.stage = self.root / "stage"
        self.stage.mkdir()
        self.first = self.stage / "first file"
        self.first.write_text("installed")
        template = Path(__file__).resolve().parents[1] / "cmake/cmake_uninstall.cmake.in"
        self.script = self.root / "uninstall.cmake"
        self.script.write_text(template.read_text().replace("@CMAKE_CURRENT_BINARY_DIR@", str(self.root)))

    def run_script(self, entries=None, stage=None):
        if entries is not None:
            (self.root / "install_manifest.txt").write_text("\n".join(entries) + "\n")
        return subprocess.run(["cmake", "-P", str(self.script)], capture_output=True, text=True,
                              env=dict(os.environ, DESTDIR=str(self.stage if stage is None else stage)))

    def test_files_spaces_and_missing_files(self):
        result = self.run_script(["/first file", "/already missing"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.first.exists())
        self.assertTrue(self.stage.is_dir())

    def test_links_are_removed_without_their_targets(self):
        outside = self.root / "outside"
        outside.mkdir()
        marker = outside / "retain"
        marker.write_text("keep")
        (self.stage / "directory-link").symlink_to(outside, target_is_directory=True)
        (self.stage / "dangling-link").symlink_to(self.root / "absent")
        result = self.run_script(["/directory-link", "/dangling-link"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(marker.read_text(), "keep")
        self.assertFalse((self.stage / "directory-link").is_symlink())
        self.assertFalse((self.stage / "dangling-link").is_symlink())

    def test_invalid_entries_fail_before_removing_anything(self):
        directory = self.stage / "directory"
        directory.mkdir()
        for entry in ("relative", "/../outside", "/a/../../outside", "/directory"):
            with self.subTest(entry=entry):
                result = self.run_script(["/first file", entry])
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.first.read_text(), "installed")
                self.assertTrue(directory.is_dir())

    def test_missing_manifest(self):
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot find install manifest", result.stderr)
        self.assertTrue(self.first.exists())

    def test_parent_symlink_cannot_escape_stage(self):
        outside = self.root / "outside"
        outside.mkdir()
        marker = outside / "retain"
        marker.write_text("keep")
        (self.stage / "escape").symlink_to(outside, target_is_directory=True)
        result = self.run_script(["/first file", "/escape/retain"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("escapes DESTDIR", result.stderr)
        self.assertEqual(marker.read_text(), "keep")
        self.assertTrue(self.first.exists())

    def test_relative_stage_is_rejected(self):
        result = self.run_script(["/first file"], stage="relative-stage")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DESTDIR must be absolute", result.stderr)
        self.assertTrue(self.first.exists())

    def test_empty_manifest_preserves_files(self):
        result = self.run_script([])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.first.exists())


if __name__ == "__main__":
    unittest.main()
