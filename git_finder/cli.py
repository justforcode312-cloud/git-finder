"""
Git Finder - Command Line Interface
====================================

This module handles the command-line interface for the Git Finder tool.
It processes arguments, prompts for user input, and coordinates the
display of results.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

from .core import find_git_projects, display_projects, display_today_commits


# ============================================================================
# USER INPUT FUNCTIONS
# ============================================================================

def prompt_for_path(default: str = ".") -> str:
    """
    Interactively prompt the user for a directory path.
    
    Continues prompting until a valid directory is provided.
    
    Args:
        default: Default directory path if user provides no input
        
    Returns:
        Absolute path to a valid directory
        
    Example:
        >>> path = prompt_for_path("~/Documents")
        Enter the directory path to search [~/Documents]: 
        '/home/user/Documents'
    """
    while True:
        # Get user input
        raw = input(f"Enter the directory path to search [{default}]: ").strip()
        
        # Use default if no input provided
        if not raw:
            raw = default
        
        # Expand ~ and convert to absolute path
        path = os.path.abspath(os.path.expanduser(raw))
        
        # Validate directory exists
        if os.path.isdir(path):
            return path
        
        # Show error and retry
        print(f"'{path}' is not a valid directory. Please try again.")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    Main entry point for the Git Finder CLI.
    
    Parses command-line arguments, finds Git projects, and displays results.
    
    Command-line Arguments:
        path: Optional directory to search (prompts if not provided)
        --list: Show project list instead of commits
        
    Exit Codes:
        0: Success
        1: Error (invalid directory, search failed, etc.)
    """
    # ========================================================================
    # PARSE COMMAND-LINE ARGUMENTS
    # ========================================================================
    
    parser = argparse.ArgumentParser(
        description="Show today's commits from all Git projects under a given directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Show today's commits (interactive mode)
  %(prog)s /path/to/search          # Show today's commits from specific directory
  %(prog)s --list                   # List projects only (no commits)
  %(prog)s /path/to/search --list   # List projects from specific directory
        """
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Root directory to search (omit to be prompted)",
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List projects only without showing commits",
    )
    
    args = parser.parse_args()

    # ========================================================================
    # DETERMINE ROOT PATH
    # ========================================================================
    
    if args.path:
        # Path provided via command line
        root = os.path.abspath(os.path.expanduser(args.path))
        
        # Validate directory exists
        if not os.path.isdir(root):
            print(f"Error: '{root}' is not a valid directory.", file=sys.stderr)
            sys.exit(1)
    else:
        # Interactive mode - prompt for path
        default_path = str(Path.home() / "Documents")
        root = prompt_for_path(default_path)

    # ========================================================================
    # FIND GIT PROJECTS
    # ========================================================================
    
    try:
        projects = find_git_projects(root)
        
    except ValueError as e:
        # Invalid directory error
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except KeyboardInterrupt:
        # User cancelled with Ctrl+C
        print("\nSearch cancelled by user.")
        sys.exit(0)
    
    # ========================================================================
    # DISPLAY RESULTS
    # ========================================================================
    
    if args.list:
        # Show project list only
        display_projects(projects, root)
    else:
        # Show today's commits (default behavior)
        display_today_commits(projects)


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()