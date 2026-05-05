#!/usr/bin/env python3
"""
Local testing script for git-finder.

This script tests the package functionality directly without relying on
PATH or installed console scripts. Useful for local development and CI.
"""

import sys
import tempfile
from pathlib import Path

# Add parent directory to path to import git_finder
sys.path.insert(0, str(Path(__file__).parent.parent))

from git_finder.core import (  # noqa: E402
    display_today_commits,
    find_git_projects,
    get_today_commits,
)


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...", end=" ")
    try:
        import git_finder  # noqa: F401
        from git_finder import cli, core  # noqa: F401

        print("PASSED")
        return True
    except ImportError as e:
        print(f"FAILED: {e}")
        return False


def test_find_git_projects():
    """Test finding Git projects."""
    print("Testing find_git_projects...", end=" ")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake Git repo
            git_dir = Path(tmpdir) / "test-repo" / ".git"
            git_dir.mkdir(parents=True)

            # Find projects
            projects = find_git_projects(tmpdir)

            if len(projects) == 1 and "test-repo" in projects[0]:
                print("PASSED")
                return True
            else:
                print(f"FAILED: Expected 1 project, found {len(projects)}")
                return False
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_get_today_commits():
    """Test getting today's commits."""
    print("Testing get_today_commits...", end=" ")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test with non-Git directory (should return empty list)
            commits = get_today_commits(tmpdir)

            if isinstance(commits, list):
                print("PASSED")
                return True
            else:
                print(f"FAILED: Expected list, got {type(commits)}")
                return False
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_display_functions():
    """Test display functions."""
    print("Testing display functions...", end=" ")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create fake projects
            (Path(tmpdir) / "project1" / ".git").mkdir(parents=True)
            (Path(tmpdir) / "project2" / ".git").mkdir(parents=True)

            projects = find_git_projects(tmpdir)

            # Test display_today_commits (should not raise exception)
            display_today_commits(projects)

            print("PASSED")
            return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_cli_module():
    """Test that CLI module can be imported and has main function."""
    print("Testing CLI module...", end=" ")
    try:
        from git_finder.cli import main

        if callable(main):
            print("PASSED")
            return True
        else:
            print("FAILED: main is not callable")
            return False
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_package_metadata():
    """Test package metadata."""
    print("Testing package metadata...", end=" ")
    try:
        import git_finder

        if hasattr(git_finder, "__version__"):
            print(f"PASSED (version: {git_finder.__version__})")
            return True
        else:
            print("FAILED: No __version__ attribute")
            return False
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("Git Finder - Local Testing Suite")
    print("=" * 70)
    print()

    tests = [
        test_imports,
        test_package_metadata,
        test_find_git_projects,
        test_get_today_commits,
        test_display_functions,
        test_cli_module,
    ]

    results = []
    for test_func in tests:
        results.append(test_func())

    print()
    print("=" * 70)
    passed = sum(results)
    failed = len(results) - passed
    print(f"Results: {passed}/{len(results)} tests passed")
    print("=" * 70)

    if failed > 0:
        print()
        print("[FAIL] Some tests failed!")
        print()
        print("This might indicate:")
        print("  1. The package is not installed correctly")
        print("  2. Missing dependencies")
        print("  3. Code issues that need to be fixed")
        print()
        sys.exit(1)
    else:
        print()
        print("[PASS] All tests passed!")
        print()
        print("The package is working correctly.")
        print("You can now use: git-finder or gf")
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
