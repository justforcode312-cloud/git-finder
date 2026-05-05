#!/usr/bin/env python3
"""Test script to verify git-finder installation."""

import subprocess
import sys


def test_command(cmd):
    """Test if a command is available."""
    try:
        result = subprocess.run(
            [cmd, "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main():
    """Run installation tests."""
    print("=" * 60)
    print("Git Finder Installation Test")
    print("=" * 60)
    print()

    tests = [
        ("git-finder command", "git-finder"),
        ("gf command (alias)", "gf"),
    ]

    passed = 0
    failed = 0

    for test_name, command in tests:
        print(f"Testing {test_name}...", end=" ")
        if test_command(command):
            print("✓ PASSED")
            passed += 1
        else:
            print("✗ FAILED")
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print()
        print("Some tests failed. This might mean:")
        print("1. The package is not installed (run: pip install .)")
        print("2. Python Scripts directory is not in PATH")
        print("3. You need to restart your terminal")
        print()
        print("See INSTALL.md for troubleshooting steps.")
        sys.exit(1)
    else:
        print()
        print("All tests passed! ✓")
        print()
        print("You can now use:")
        print("  - git-finder")
        print("  - gf")
        print()
        print("Try: gf --help")
        sys.exit(0)


if __name__ == "__main__":
    main()
