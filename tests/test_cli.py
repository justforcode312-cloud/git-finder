"""Unit tests for git_finder.cli module."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from git_finder.cli import get_root_path, main


class TestGetRootPath:
    """Tests for get_root_path function."""

    def test_get_root_path_provided(self):
        """Test with a provided valid path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = get_root_path(tmpdir)
            assert isinstance(path, Path)
            assert str(path) == str(Path(tmpdir).resolve())

    def test_get_root_path_provided_invalid(self):
        """Test with a provided invalid path."""
        with pytest.raises(SystemExit) as exc_info:
            get_root_path("/non/existent/path/12345")
        assert exc_info.value.code == 1

    def test_get_root_path_interactive(self, monkeypatch):
        """Test interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setattr("builtins.input", lambda _: tmpdir)
            path = get_root_path(None)
            assert str(path) == str(Path(tmpdir).resolve())

    def test_get_root_path_interactive_retry(self, monkeypatch):
        """Test interactive mode with retry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inputs = iter(["/invalid/path/12345", tmpdir])
            monkeypatch.setattr("builtins.input", lambda _: next(inputs))
            path = get_root_path(None)
            assert str(path) == str(Path(tmpdir).resolve())


class TestMainCLI:
    """Tests for main CLI function."""

    def test_main_with_help(self):
        """Test --help flag."""
        with patch.object(sys, "argv", ["git-finder", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_main_with_list_flag(self):
        """Test --list flag with a valid directory."""
        with (
            tempfile.TemporaryDirectory() as tmpdir,
            patch.object(sys, "argv", ["git-finder", tmpdir, "--list"]),
        ):
            main()

    def test_main_with_invalid_directory(self):
        """Test with an invalid directory path."""
        with patch.object(sys, "argv", ["git-finder", "/invalid/path/12345"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_keyboard_interrupt(self, monkeypatch):
        """Test handling of Ctrl+C during execution."""
        with patch.object(sys, "argv", ["git-finder"]):
            # Mock get_root_path to return a valid path
            monkeypatch.setattr("git_finder.cli.get_root_path", lambda _: Path("/tmp"))
            # Mock find_git_projects to raise KeyboardInterrupt
            monkeypatch.setattr(
                "git_finder.cli.find_git_projects",
                lambda _: (_ for _ in ()).throw(KeyboardInterrupt()),
            )

            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_main_unexpected_error(self, monkeypatch):
        """Test handling of unexpected errors."""
        with patch.object(sys, "argv", ["git-finder", "."]):
            monkeypatch.setattr(
                "git_finder.cli.find_git_projects",
                lambda _: (_ for _ in ()).throw(RuntimeError("Unexpected")),
            )

            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
