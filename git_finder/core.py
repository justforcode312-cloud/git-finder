"""
Git Finder - Core Functionality
================================

This module contains the core logic for finding Git repositories
and displaying commit information.
"""

import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, TextIO

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

# ANSI Color Codes
CLR_CYAN = "\033[36m"
CLR_YELLOW = "\033[33m"
CLR_GREEN = "\033[32m"
CLR_GRAY = "\033[90m"
CLR_BOLD = "\033[1m"
CLR_RESET = "\033[0m"


# ============================================================================
# MAIN FUNCTIONS
# ============================================================================


def find_git_projects(root_path: str) -> list[Path]:
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

    def search_recursive(current_dir: Path) -> None:
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


def get_today_commits(repo_path: Path) -> list[str]:
    """
    Get all commit messages from today for a specific repository.

    Args:
        repo_path: Path object to the Git repository

    Returns:
        List of commit messages from today (hash - message)
    """
    # Calculate today's date at midnight
    today_start = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    since_date = today_start.isoformat()

    try:
        result = subprocess.run(
            [
                "git",
                "log",
                f"--since={since_date}",
                "--no-merges",
                "--pretty=format:%B%x00",
            ],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT,
            check=False,
        )

        if result.returncode != 0:
            return []

        return [c.strip() for c in result.stdout.split("\x00") if c.strip()]

    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return []


# ============================================================================
# UI HELPERS
# ============================================================================


class Loader:
    """A simple animated loader for CLI operations."""

    def __init__(self, message: str, file: Optional[TextIO] = None):
        self.message = message
        self.file = file or sys.stdout
        self.stopped = False
        self._thread: Optional[threading.Thread] = None
        self.is_tty = hasattr(self.file, "isatty") and self.file.isatty()

    def _animate(self) -> None:
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while not self.stopped:
            if self.is_tty:
                # Cyan color for the spinner
                char = f"{CLR_CYAN}{chars[i % len(chars)]}{CLR_RESET}"
                self.file.write(f"\r {char} {self.message}")
                self.file.flush()
            time.sleep(0.1)
            i += 1

    def __enter__(self) -> "Loader":
        if self.is_tty:
            self._thread = threading.Thread(target=self._animate, daemon=True)
            self._thread.start()
        else:
            self.file.write(f"{self.message}...\n")
            self.file.flush()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> None:
        self.stopped = True
        if self._thread:
            self._thread.join()
        if self.is_tty:
            # Clear the line
            self.file.write("\r" + " " * (len(self.message) + 10) + "\r")
            self.file.flush()


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================


def display_projects(
    projects: list[Path], root_path: str, file: Optional[TextIO] = None
) -> None:
    """Display a formatted table of Git projects."""
    file = file or sys.stdout
    if not projects:
        print(f"ERROR: No Git projects found under: {root_path}", file=file)
        return

    print(
        f"\nINFO: Found {len(projects)} Git project(s) under: {root_path}\n", file=file
    )
    print(f"{'#':<5} {'PROJECT NAME':<30} {'PATH'}", file=file)
    print("─" * 80, file=file)

    for i, path in enumerate(projects, start=1):
        print(f"{i:<5} {path.name:<30} {path}", file=file)
    print("─" * 80 + "\n", file=file)


def display_today_commits(projects: list[Path], file: Optional[TextIO] = None) -> None:
    """Display today's commits with an attractive UI."""
    file = file or sys.stdout
    if not projects:
        print("INFO: No Git projects to check for commits.", file=file)
        return

    is_tty = hasattr(file, "isatty") and file.isatty()

    def style(text: str, code: str) -> str:
        return f"{code}{text}{CLR_RESET}" if is_tty else text

    date_str = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")

    print(f"\n{style('━' * 80, CLR_CYAN)}", file=file)
    print(style(f"{'DAILY GIT ACTIVITY':^80}", CLR_BOLD + CLR_CYAN), file=file)
    print(style(f"{date_str.upper():^80}", CLR_GRAY), file=file)
    print(style("━" * 80, CLR_CYAN) + "\n", file=file)

    total_commits = 0
    active_count = 0
    project_results = []

    with Loader("Fetching today's commits", file=file):
        for project_path in projects:
            commits = get_today_commits(project_path)
            if commits:
                project_results.append((project_path, commits))
                total_commits += len(commits)
                active_count += 1

    for project_path, commits in project_results:
        print(f" {style(project_path.name.upper(), CLR_BOLD + CLR_YELLOW)}", file=file)

        for i, commit in enumerate(commits):
            lines = commit.splitlines()
            if not lines:
                continue

            is_last = i == len(commits) - 1
            connector = " └── " if is_last else " ├── "
            indent = "     " if is_last else " │   "

            print(
                f"{style(connector, CLR_GRAY)}{style(lines[0], CLR_GREEN)}", file=file
            )
            for extra_line in lines[1:]:
                if extra_line.strip():
                    print(
                        f"{style(indent, CLR_GRAY)}{style(extra_line, CLR_GRAY)}",
                        file=file,
                    )

        print(file=file)

    print(style("━" * 80, CLR_CYAN), file=file)
    status = "Productive day!" if total_commits > 0 else "A quiet day for coding."

    summary_text = f"SUMMARY: {total_commits} commit(s) in {active_count}/{len(projects)} active project(s)."
    print(style(f" {summary_text}", CLR_BOLD), file=file)
    print(style(f" {status}", CLR_CYAN), file=file)
    print(style("━" * 80, CLR_CYAN) + "\n", file=file)
