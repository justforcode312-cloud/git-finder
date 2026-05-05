"""
Git Finder Package
==================

A tool to discover Git repositories in a directory tree and display
today's commits across all found projects.

Usage:
    From command line:
        $ git-finder ~/projects
        $ gf ~/projects --list

    From Python:
        >>> from git_finder import find_git_projects, display_today_commits
        >>> projects = find_git_projects('/home/user/projects')
        >>> display_today_commits(projects)

Author: Your Name
License: MIT
Version: 1.0.0
"""

from .core import (
    display_projects,
    display_today_commits,
    find_git_projects,
    get_today_commits,
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

# Public API
__all__ = [
    "find_git_projects",
    "display_projects",
    "display_today_commits",
    "get_today_commits",
]
