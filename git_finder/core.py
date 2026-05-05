"""
Git Finder - Core Functionality
================================

This module contains the core logic for finding Git repositories
and displaying commit information.
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional


# ============================================================================
# CONSTANTS
# ============================================================================

# Directories to skip during search (improves performance)
SKIP_DIRECTORIES = {
    'node_modules',  # Node.js dependencies
    '.venv', 'venv',  # Python virtual environments
    '__pycache__',  # Python cache
    '.tox',  # Python testing
    'dist', 'build',  # Build outputs
    '.eggs',  # Python eggs
}

# Git command timeout in seconds
GIT_TIMEOUT = 5


# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def find_git_projects(root_path: str) -> List[str]:
    """
    Find all Git repositories under a given directory.
    
    This function walks through the directory tree and identifies
    folders containing a .git directory, which indicates a Git repository.
    
    Args:
        root_path: The root directory to start searching from
        
    Returns:
        A sorted list of absolute paths to Git repositories
        
    Raises:
        ValueError: If root_path is not a valid directory
        
    Example:
        >>> projects = find_git_projects('/home/user/projects')
        >>> print(projects)
        ['/home/user/projects/my-app', '/home/user/projects/website']
    """
    # Validate input
    if not os.path.isdir(root_path):
        raise ValueError(f"'{root_path}' is not a valid directory.")

    projects = []
    
    # Walk through directory tree
    for dirpath, dirnames, _ in os.walk(root_path):
        # Skip unnecessary directories for better performance
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRECTORIES]
        
        # Check if this directory is a Git repository
        if ".git" in dirnames:
            projects.append(dirpath)
            # Don't search inside this Git repository
            dirnames[:] = [d for d in dirnames if d != ".git"]

    return sorted(projects)


def get_today_commits(repo_path: str) -> List[str]:
    """
    Get all commit messages from today for a specific repository.
    
    Args:
        repo_path: Path to the Git repository
        
    Returns:
        List of commit messages from today (empty if none or on error)
        
    Example:
        >>> commits = get_today_commits('/home/user/projects/my-app')
        >>> print(commits)
        ['Fix login bug', 'Add new feature']
    """
    try:
        # Calculate today's date at midnight
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        since_date = today.strftime("%Y-%m-%d 00:00:00")
        
        # Execute git log command
        result = subprocess.run(
            ["git", "log", f"--since={since_date}", "--pretty=format:%s"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
            timeout=GIT_TIMEOUT
        )
        
        # Parse results
        if result.returncode == 0 and result.stdout.strip():
            return [msg.strip() for msg in result.stdout.strip().split("\n") if msg.strip()]
        return []
        
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        # Return empty list on any error
        return []


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_projects(projects: List[str], root_path: str) -> None:
    """
    Display a formatted table of Git projects.
    
    Args:
        projects: List of Git project paths
        root_path: The root directory that was searched
        
    Output Format:
        #     Project Name                   Path
        ----------------------------------------------------------------
        1     my-project                     /path/to/my-project
        2     another-project                /path/to/another-project
    """
    # Handle empty results
    if not projects:
        print(f"No Git projects found under: {root_path}")
        return

    # Print header
    print(f"\nFound {len(projects)} Git project(s) under: {root_path}\n")
    print(f"{'#':<5} {'Project Name':<30} {'Path'}")
    print("-" * 80)

    # Print each project
    for i, path in enumerate(projects, start=1):
        name = os.path.basename(path) or path
        print(f"{i:<5} {name:<30} {path}")


def display_today_commits(projects: List[str]) -> None:
    """
    Display today's commits for all projects.
    
    Shows commits in the format: "project-name - commit message"
    Also displays a summary of total commits found.
    
    Args:
        projects: List of Git project paths to check
        
    Output Format:
        ========================================
        TODAY'S COMMITS (2026-05-05)
        ========================================
        
        my-project - Fix login bug
        my-project - Add new feature
        website - Update homepage
        api - No commits
        
        ========================================
        Total: 3 commit(s) across 4 project(s)
        ========================================
    """
    # Handle empty project list
    if not projects:
        print("No Git projects to check for commits.")
        return
    
    # Print header
    print(f"\n{'='*80}")
    print(f"TODAY'S COMMITS ({datetime.now().strftime('%Y-%m-%d')})")
    print(f"{'='*80}\n")
    
    # Check each project for commits
    total_commits = 0
    for project_path in projects:
        project_name = os.path.basename(project_path) or project_path
        commits = get_today_commits(project_path)
        
        if commits:
            # Display each commit
            for commit_msg in commits:
                print(f"{project_name} - {commit_msg}")
            total_commits += len(commits)
        else:
            # Show "No commits" for projects without commits today
            print(f"{project_name} - No commits")
    
    # Print summary footer
    print(f"\n{'='*80}")
    print(f"Total: {total_commits} commit(s) across {len(projects)} project(s)")
    print(f"{'='*80}")