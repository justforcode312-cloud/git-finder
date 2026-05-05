# Code Guide - Understanding Git Finder

This guide helps you understand how the code works and how to read it.

## Quick Overview

**What does this tool do?**
1. Searches a directory for Git repositories
2. Gets today's commits from each repository
3. Displays the results in a nice format

**Three main files:**
- `core.py` - Does the actual work (finding repos, getting commits)
- `cli.py` - Handles user interaction (commands, prompts)
- `__init__.py` - Makes it a package you can import

## Reading the Code

### Start Here: `cli.py`

This is where everything begins when you run `gf` or `git-finder`.

```python
# User runs: gf ~/projects

def main():
    # 1. Parse arguments (~/projects, --list flag, etc.)
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args()

    # 2. Get the directory to search
    if args.path:
        root = args.path  # User provided path
    else:
        root = prompt_for_path()  # Ask user interactively

    # 3. Find all Git projects
    projects = find_git_projects(root)

    # 4. Display results
    if args.list:
        display_projects(projects, root)  # Show project list
    else:
        display_today_commits(projects)   # Show commits (default)
```

**Key Function: `prompt_for_path()`**
```python
def prompt_for_path(default: str = ".") -> str:
    """Ask user for a directory until they give a valid one."""
    while True:
        raw = input(f"Enter path [{default}]: ")
        path = os.path.abspath(os.path.expanduser(raw))

        if os.path.isdir(path):
            return path  # Valid directory, return it

        print("Invalid directory, try again")  # Keep asking
```

### Core Logic: `core.py`

This file does the heavy lifting.

#### Function 1: `find_git_projects()`

**What it does:** Walks through directories looking for `.git` folders

```python
def find_git_projects(root_path: str) -> List[str]:
    """Find all Git repos under root_path."""

    projects = []

    # Walk through all directories
    for dirpath, dirnames, _ in os.walk(root_path):

        # Skip unnecessary directories (faster!)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRECTORIES]

        # Found a Git repo?
        if ".git" in dirnames:
            projects.append(dirpath)
            # Don't go inside this repo
            dirnames[:] = [d for d in dirnames if d != ".git"]

    return sorted(projects)
```

**Why skip directories?**
- `node_modules` can have thousands of files
- `.venv` is a Python virtual environment, not a project
- Skipping these makes the search much faster!

#### Function 2: `get_today_commits()`

**What it does:** Gets commit messages from today for one repository

```python
def get_today_commits(repo_path: str) -> List[str]:
    """Get today's commits from a Git repo."""

    # Calculate today at midnight
    today = datetime.now().replace(hour=0, minute=0, second=0)
    since_date = today.strftime("%Y-%m-%d 00:00:00")

    # Run git command: git log --since="2026-05-05 00:00:00"
    result = subprocess.run(
        ["git", "log", f"--since={since_date}", "--pretty=format:%s"],
        cwd=repo_path,
        capture_output=True,
        timeout=5  # Don't wait forever!
    )

    # Parse the output
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().split("\n")

    return []  # No commits or error
```

**Why timeout?**
- Some repos might be corrupted or on slow drives
- 5 seconds is enough for normal repos
- Prevents the tool from hanging forever

#### Function 3: `display_today_commits()`

**What it does:** Shows commits for all projects

```python
def display_today_commits(projects: List[str]) -> None:
    """Display today's commits for all projects."""

    # Print header
    print("TODAY'S COMMITS (2026-05-05)")

    total_commits = 0

    # Check each project
    for project_path in projects:
        project_name = os.path.basename(project_path)
        commits = get_today_commits(project_path)

        if commits:
            # Print each commit
            for commit_msg in commits:
                print(f"{project_name} - {commit_msg}")
            total_commits += len(commits)
        else:
            print(f"{project_name} - No commits")

    # Print summary
    print(f"Total: {total_commits} commit(s)")
```

### Package Setup: `__init__.py`

Makes the package importable and defines what's public.

```python
# When someone does: from git_finder import find_git_projects
# This file controls what they can import

from .core import (
    find_git_projects,
    display_projects,
    display_today_commits,
    get_today_commits,
)

# Public API - what users can import
__all__ = [
    "find_git_projects",
    "display_projects",
    "display_today_commits",
    "get_today_commits",
]
```

## Code Flow Diagram

```
User runs: gf ~/projects
         ↓
    cli.py main()
         ↓
    Parse arguments
    (path=~/projects, list=False)
         ↓
    core.find_git_projects(~/projects)
         ↓
    Walk directory tree
    Find .git folders
    Return: ['/projects/app1', '/projects/app2']
         ↓
    Back to cli.py main()
         ↓
    core.display_today_commits(projects)
         ↓
    For each project:
      - Get project name
      - Call core.get_today_commits(project)
      - Run: git log --since="today"
      - Parse output
      - Print: "app1 - Fix bug"
         ↓
    Print summary
    Done!
```

## Key Concepts Explained

### 1. Type Hints
```python
def find_git_projects(root_path: str) -> List[str]:
    #                            ^^^      ^^^^^^^^
    #                         parameter   return type
```
- Helps you know what to pass in and what you'll get back
- Makes code easier to understand
- Catches errors early

### 2. List Comprehension
```python
# Instead of:
new_list = []
for d in dirnames:
    if d not in SKIP_DIRECTORIES:
        new_list.append(d)

# We write:
new_list = [d for d in dirnames if d not in SKIP_DIRECTORIES]
```
- More concise and readable
- Common Python pattern

### 3. In-place List Modification
```python
dirnames[:] = [d for d in dirnames if d not in SKIP_DIRECTORIES]
#       ^^^ This is important!
```
- `dirnames[:] =` modifies the original list
- `dirnames =` would create a new variable
- `os.walk()` needs the original list modified

### 4. Subprocess
```python
result = subprocess.run(["git", "log", "--since=..."], ...)
```
- Runs external commands (like git)
- Captures output
- Handles errors

### 5. String Formatting
```python
print(f"{project_name} - {commit_msg}")
#     ^ f-string: embeds variables in strings
```
- Modern Python string formatting
- Clear and readable

## Common Patterns

### Error Handling
```python
try:
    # Try to do something
    result = subprocess.run(...)
except (TimeoutExpired, FileNotFoundError):
    # Handle specific errors
    return []
```

### Validation
```python
if not os.path.isdir(path):
    raise ValueError(f"'{path}' is not a valid directory")
```

### Default Values
```python
def prompt_for_path(default: str = ".") -> str:
    #                          ^^^^^^^ default if not provided
```

## How to Modify

### Add a new command-line option

**Example: Add `--today` flag to show only repos with commits**

1. **In `cli.py`**, add argument:
```python
parser.add_argument(
    "--today",
    action="store_true",
    help="Show only projects with commits today"
)
```

2. **In `core.py`**, modify display function:
```python
def display_today_commits(projects: List[str], only_with_commits: bool = False):
    for project_path in projects:
        commits = get_today_commits(project_path)

        if only_with_commits and not commits:
            continue  # Skip projects without commits

        # ... rest of code
```

3. **In `cli.py`**, use the flag:
```python
display_today_commits(projects, only_with_commits=args.today)
```

### Add a new feature

**Example: Show commits from last week**

1. **In `core.py`**, add new function:
```python
def get_week_commits(repo_path: str) -> List[str]:
    """Get commits from last 7 days."""
    week_ago = datetime.now() - timedelta(days=7)
    since_date = week_ago.strftime("%Y-%m-%d 00:00:00")
    # ... similar to get_today_commits
```

2. **In `cli.py`**, add `--week` flag and use it

## Testing Your Changes

After modifying code:

```bash
# 1. Reinstall the package
pip install -e .

# 2. Test it
gf --help          # Check help text
gf ~/projects      # Test basic functionality
gf --list          # Test list mode

# 3. Check for errors
python -m git_finder.cli --help
```

## Questions?

- **Where does execution start?** → `cli.py` `main()` function
- **Where is the core logic?** → `core.py`
- **How do I add a feature?** → Add function to `core.py`, call from `cli.py`
- **How do I test changes?** → `pip install -e .` then run `gf`

## Summary

1. **cli.py** - User interface (arguments, prompts)
2. **core.py** - Business logic (finding, getting commits)
3. **__init__.py** - Package definition (exports)

The code is organized, well-commented, and follows Python best practices!
