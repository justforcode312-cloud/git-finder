"""
Git Finder - Core Functionality
================================

This module contains the core logic for finding Git repositories
and displaying commit information.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, TextIO

# ============================================================================
# CONSTANTS
# ============================================================================

# Directories to skip during search (improves performance)
SKIP_DIRECTORIES = {
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".tox",
    "dist",
    "build",
    ".eggs",
}

# Git command timeout in seconds
GIT_TIMEOUT = 5


# ============================================================================
# MAIN FUNCTIONS
# ============================================================================


def find_git_projects(root_path: str) -> List[Path]:
    """
    Find all Git repositories under a given directory.

    Args:
        root_path: The root directory to start searching from

    Returns:
        A sorted list of Path objects to Git repositories
    """
    root = Path(root_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"'{root}' is not a valid directory.")

    projects = []

    def search_recursive(current_dir: Path):
        # Check if this is a git repo
        if (current_dir / ".git").is_dir():
            projects.append(current_dir)
            return  # Stop searching deeper once a repo is found

        try:
            for item in current_dir.iterdir():
                if item.is_dir() and item.name not in SKIP_DIRECTORIES:
                    search_recursive(item)
        except PermissionError:
            pass  # Skip directories we can't access

    search_recursive(root)
    return sorted(projects)


def get_today_commits(repo_path: Path) -> List[str]:
    """
    Get all commit messages from today for a specific repository.

    Args:
        repo_path: Path object to the Git repository

    Returns:
        List of commit messages from today (hash - message)
    """
    # Calculate today's date at midnight
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    since_date = today_start.isoformat()

    try:
        result = subprocess.run(
            [
                "git",
                "log",
                f"--since={since_date}",
                "--no-merges",
                "--pretty=format:%h | %s",
            ],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT,
        )

        if result.returncode != 0:
            return []

        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return []


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================


def display_projects(
    projects: List[Path], root_path: str, file: TextIO = sys.stdout
) -> None:
    """Display a formatted table of Git projects."""
    if not projects:
        print(f"❌ No Git projects found under: {root_path}", file=file)
        return

    print(f"\n🔍 Found {len(projects)} Git project(s) under: {root_path}\n", file=file)
    print(f"{'#':<5} {'📦 Project Name':<30} {'📍 Path'}", file=file)
    print("─" * 80, file=file)

    for i, path in enumerate(projects, start=1):
        print(f"{i:<5} {path.name:<30} {path}", file=file)
    print("─" * 80 + "\n", file=file)


def display_today_commits(projects: List[Path], file: TextIO = sys.stdout) -> None:
    """Display today's commits with an attractive UI."""
    if not projects:
        print("🔍 No Git projects to check for commits.", file=file)
        return

    date_str = datetime.now().strftime("%A, %B %d, %Y")

    print(f"\n{'⭐' * 40}", file=file)
    print(f"🚀 DAILY GIT ACTIVITY - {date_str.upper()}".center(80), file=file)
    print(f"{'⭐' * 40}\n", file=file)

    total_commits = 0
    active_count = 0

    for project_path in projects:
        commits = get_today_commits(project_path)

        if commits:
            active_count += 1
            print(f"📂 {project_path.name.upper()}", file=file)
            for commit in commits:
                print(f"  └─ ✅ {commit}", file=file)
            total_commits += len(commits)
            print(file=file)  # Spacer
        else:
            # Show inactive projects subtly
            print(f"📁 {project_path.name:<30} | 😴 No activity today", file=file)

    print(f"\n{'─' * 80}", file=file)
    status = "🔥 Productive day!" if total_commits > 0 else "🌱 A quiet day for coding."
    print(
        f"📊 SUMMARY: {total_commits} commit(s) in {active_count}/{len(projects)} active project(s).",
        file=file,
    )
    print(f"💡 {status}", file=file)
    print(f"{'─' * 80}\n", file=file)
