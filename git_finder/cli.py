"""
Git Finder - Command Line Interface
====================================

This module handles the command-line interface for the Git Finder tool.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .core import display_projects, display_today_commits, find_git_projects

# ============================================================================
# CLI HELPERS
# ============================================================================


def get_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Show today's commits from all Git projects under a given directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Interactive mode
  %(prog)s /path/to/search          # Specific directory
  %(prog)s --list                   # List projects only
        """,
    )

    parser.add_argument(
        "path",
        nargs="?",
        help="Root directory to search (omit for interactive mode)",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List projects only without showing commits",
    )

    return parser.parse_args()


def get_root_path(provided_path: Optional[str]) -> Path:
    """Determine and validate the root path to search."""
    if provided_path:
        path = Path(provided_path).expanduser().resolve()
        if not path.is_dir():
            print(f"Error: '{path}' is not a valid directory.", file=sys.stderr)
            sys.exit(1)
        return path

    # Interactive mode
    default_path = Path.home() / "Documents"
    while True:
        raw = input(f"Enter directory to search [{default_path}]: ").strip()
        path = Path(raw or default_path).expanduser().resolve()

        if path.is_dir():
            return path
        print(f"'{path}' is not a valid directory. Please try again.")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


def main() -> None:
    """Main execution flow."""
    # Ensure UTF-8 encoding for Unicode support on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = get_args()

    try:
        root = get_root_path(args.path)
        projects = find_git_projects(str(root))

        if args.list:
            display_projects(projects, str(root))
        else:
            display_today_commits(projects)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
