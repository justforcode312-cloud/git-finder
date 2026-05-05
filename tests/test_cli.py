"""Unit tests for git_finder.cli module."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from git_finder.cli import main, prompt_for_path


class TestPromptForPath:
    """Tests for prompt_for_path function."""

    def test_prompt_with_valid_path(self, monkeypatch):
        """Test prompting with a valid directory path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock user input
            monkeypatch.setattr("builtins.input", lambda _: tmpdir)
            result = prompt_for_path()
            assert result == tmpdir

    def test_prompt_with_default(self, monkeypatch):
        """Test using default path when user provides no input."""
        # Mock empty input (use default)
        monkeypatch.setattr("builtins.input", lambda _: "")
        result = prompt_for_path(".")
        assert result == str(Path(".").resolve())

    def test_prompt_with_tilde_expansion(self, monkeypatch):
        """Test that ~ is expanded to home directory."""
        monkeypatch.setattr("builtins.input", lambda _: "~")
        result = prompt_for_path()
        assert result == str(Path.home())

    def test_prompt_with_invalid_then_valid(self, monkeypatch):
        """Test retry logic when invalid path is provided."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # First return invalid, then valid
            inputs = iter(["/invalid/path/12345", tmpdir])
            monkeypatch.setattr("builtins.input", lambda _: next(inputs))
            result = prompt_for_path()
            assert result == tmpdir


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
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(sys, "argv", ["git-finder", tmpdir, "--list"]):
                # Should not raise an exception
                main()

    def test_main_with_invalid_directory(self):
        """Test with an invalid directory path."""
        with patch.object(sys, "argv", ["git-finder", "/invalid/path/12345"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_with_valid_directory(self):
        """Test with a valid directory path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(sys, "argv", ["git-finder", tmpdir]):
                # Should not raise an exception
                main()

    def test_main_keyboard_interrupt(self, monkeypatch):
        """Test handling of Ctrl+C during execution."""
        with patch.object(sys, "argv", ["git-finder"]):
            # Mock find_git_projects to raise KeyboardInterrupt
            def mock_find(*args, **kwargs):
                raise KeyboardInterrupt()

            monkeypatch.setattr("git_finder.cli.find_git_projects", mock_find)
            monkeypatch.setattr("git_finder.cli.prompt_for_path", lambda _: "/tmp")

            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_main_interactive_mode(self, monkeypatch):
        """Test interactive mode (no path argument)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock the prompt to return our temp directory
            monkeypatch.setattr("git_finder.cli.prompt_for_path", lambda _: tmpdir)

            with patch.object(sys, "argv", ["git-finder"]):
                # Should not raise an exception
                main()
