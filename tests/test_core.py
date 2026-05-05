"""Unit tests for git_finder.core module."""

import os
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from git_finder.core import (
    display_projects,
    display_today_commits,
    find_git_projects,
    get_today_commits,
)


class TestFindGitProjects:
    """Tests for find_git_projects function."""

    def test_find_git_projects_empty_directory(self):
        """Test finding projects in an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            projects = find_git_projects(tmpdir)
            assert projects == []

    def test_find_git_projects_with_git_repo(self):
        """Test finding a single Git repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake .git directory
            git_dir = Path(tmpdir) / "test-repo" / ".git"
            git_dir.mkdir(parents=True)

            projects = find_git_projects(tmpdir)
            assert len(projects) == 1
            assert "test-repo" in projects[0]

    def test_find_git_projects_multiple_repos(self):
        """Test finding multiple Git repositories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple fake .git directories
            (Path(tmpdir) / "repo1" / ".git").mkdir(parents=True)
            (Path(tmpdir) / "repo2" / ".git").mkdir(parents=True)
            (Path(tmpdir) / "nested" / "repo3" / ".git").mkdir(parents=True)

            projects = find_git_projects(tmpdir)
            assert len(projects) == 3

    def test_find_git_projects_skips_node_modules(self):
        """Test that node_modules directories are skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a .git in node_modules (should be skipped)
            (Path(tmpdir) / "node_modules" / "package" / ".git").mkdir(parents=True)
            # Create a normal .git (should be found)
            (Path(tmpdir) / "my-project" / ".git").mkdir(parents=True)

            projects = find_git_projects(tmpdir)
            assert len(projects) == 1
            assert "my-project" in projects[0]
            assert "node_modules" not in projects[0]

    def test_find_git_projects_invalid_directory(self):
        """Test error handling for invalid directory."""
        with pytest.raises(ValueError, match="not a valid directory"):
            find_git_projects("/this/path/does/not/exist/12345")

    def test_find_git_projects_returns_sorted(self):
        """Test that results are sorted alphabetically."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create repos in non-alphabetical order
            (Path(tmpdir) / "zebra" / ".git").mkdir(parents=True)
            (Path(tmpdir) / "alpha" / ".git").mkdir(parents=True)
            (Path(tmpdir) / "beta" / ".git").mkdir(parents=True)

            projects = find_git_projects(tmpdir)
            names = [os.path.basename(p) for p in projects]
            assert names == ["alpha", "beta", "zebra"]


class TestGetTodayCommits:
    """Tests for get_today_commits function."""

    def test_get_today_commits_no_git_repo(self):
        """Test getting commits from a non-Git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            commits = get_today_commits(tmpdir)
            assert commits == []

    def test_get_today_commits_returns_list(self):
        """Test that function returns a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = get_today_commits(tmpdir)
            assert isinstance(result, list)

    def test_get_today_commits_timeout_handling(self):
        """Test that function handles timeouts gracefully."""
        # Test with a path that might cause issues
        result = get_today_commits("/")
        assert isinstance(result, list)


class TestDisplayFunctions:
    """Tests for display functions."""

    def test_display_projects_empty_list(self, capsys):
        """Test displaying an empty project list."""
        display_projects([], "/test/path")
        captured = capsys.readouterr()
        assert "No Git projects found" in captured.out

    def test_display_projects_with_projects(self, capsys):
        """Test displaying a list of projects."""
        projects = ["/home/user/project1", "/home/user/project2"]
        display_projects(projects, "/home/user")
        captured = capsys.readouterr()
        assert "Found 2 Git project(s)" in captured.out
        assert "project1" in captured.out
        assert "project2" in captured.out

    def test_display_today_commits_empty_list(self, capsys):
        """Test displaying commits with no projects."""
        display_today_commits([])
        captured = capsys.readouterr()
        assert "No Git projects to check" in captured.out

    def test_display_today_commits_with_projects(self, capsys):
        """Test displaying commits for projects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake project
            project_path = Path(tmpdir) / "test-project"
            project_path.mkdir()

            display_today_commits([str(project_path)])
            captured = capsys.readouterr()

            # Should show header with today's date
            today = datetime.now().strftime("%Y-%m-%d")
            assert today in captured.out
            assert "test-project" in captured.out
            assert "Total:" in captured.out


class TestIntegration:
    """Integration tests."""

    def test_full_workflow(self):
        """Test the complete workflow of finding and displaying projects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test structure
            (Path(tmpdir) / "project1" / ".git").mkdir(parents=True)
            (Path(tmpdir) / "project2" / ".git").mkdir(parents=True)

            # Find projects
            projects = find_git_projects(tmpdir)
            assert len(projects) == 2

            # Get commits (should return empty lists for fake repos)
            for project in projects:
                commits = get_today_commits(project)
                assert isinstance(commits, list)
