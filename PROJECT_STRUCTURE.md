# Project Structure

This document explains the organization of the Git Finder project.

## Directory Layout

```
git-finder/
│
├── git_finder/                 # Main package (source code)
│   ├── __init__.py            # Package initialization & public API
│   ├── cli.py                 # Command-line interface logic
│   └── core.py                # Core functionality (finding repos, getting commits)
│
├── scripts/                    # Installation and utility scripts
│   ├── install.bat            # Windows installation script
│   ├── install.sh             # Linux/Mac installation script
│   └── test_install.py        # Installation verification script
│
├── docs/                       # Documentation files
│   ├── QUICKSTART.md          # Quick start guide (30 seconds)
│   ├── INSTALL.md             # Detailed installation instructions
│   └── SETUP_COMPLETE.md      # Setup completion summary
│
├── README.md                   # Main project documentation
├── LICENSE                     # MIT License
├── setup.py                    # Package setup configuration
├── pyproject.toml             # Modern Python packaging config
└── MANIFEST.in                # Package manifest (files to include)
```

## File Descriptions

### Source Code (`git_finder/`)

#### `__init__.py`
- Package initialization
- Defines public API
- Exports main functions for use as a library
- Contains version and metadata

#### `core.py`
- **Core functionality** - the heart of the application
- Functions:
  - `find_git_projects()` - Searches for Git repositories
  - `get_today_commits()` - Gets commits from today for a repo
  - `display_projects()` - Shows project list in table format
  - `display_today_commits()` - Shows today's commits for all projects
- Contains constants like directories to skip

#### `cli.py`
- **Command-line interface** - handles user interaction
- Functions:
  - `prompt_for_path()` - Interactive directory input
  - `main()` - Entry point, argument parsing, orchestration
- Processes command-line arguments
- Coordinates between user input and core functions

### Scripts (`scripts/`)

#### `install.bat` / `install.sh`
- One-click installation scripts
- Automatically runs `pip install .`
- Handles errors and provides feedback
- Platform-specific (Windows vs Linux/Mac)

#### `test_install.py`
- Verifies installation was successful
- Tests if `git-finder` and `gf` commands are available
- Provides troubleshooting guidance if tests fail

### Documentation (`docs/`)

#### `QUICKSTART.md`
- 30-second getting started guide
- Quick installation and usage examples
- Perfect for first-time users

#### `INSTALL.md`
- Comprehensive installation guide
- Multiple installation methods
- Troubleshooting section
- Platform-specific instructions

#### `SETUP_COMPLETE.md`
- Summary of what was set up
- Lists all features and files
- Next steps after installation

### Configuration Files

#### `setup.py`
- Traditional Python package setup
- Defines package metadata
- Specifies console entry points (`git-finder`, `gf`)
- Lists dependencies and requirements

#### `pyproject.toml`
- Modern Python packaging standard (PEP 518)
- Build system requirements
- Project metadata
- Alternative to setup.py

#### `MANIFEST.in`
- Specifies which files to include in package distribution
- Ensures documentation and license are included

## Code Organization Principles

### 1. **Separation of Concerns**
- `core.py` - Business logic (finding repos, getting commits)
- `cli.py` - User interface (arguments, prompts, display)
- `__init__.py` - Public API (what users can import)

### 2. **Clear Naming**
- Functions have descriptive names
- Files are organized by purpose
- Constants are in UPPER_CASE

### 3. **Comprehensive Documentation**
- Every function has a docstring
- Examples provided in docstrings
- Comments explain "why", not just "what"

### 4. **Easy to Navigate**
- Related files grouped in directories
- Documentation separate from code
- Scripts separate from source code

## How It Works

### Installation Flow
```
User runs install.bat/install.sh
    ↓
Script runs: pip install .
    ↓
pip reads setup.py and pyproject.toml
    ↓
Package installed to Python environment
    ↓
Console scripts (git-finder, gf) added to PATH
    ↓
User can run commands from anywhere
```

### Execution Flow
```
User runs: gf ~/projects
    ↓
cli.py main() function called
    ↓
Arguments parsed (path, --list flag)
    ↓
core.find_git_projects() searches directory
    ↓
For each project: core.get_today_commits()
    ↓
core.display_today_commits() shows results
```

## Module Dependencies

```
cli.py
  ↓ imports
core.py (find_git_projects, display_projects, display_today_commits)

__init__.py
  ↓ imports
core.py (all functions)
  ↓ exports
Public API for library usage
```

## Adding New Features

### To add a new command-line option:
1. Edit `cli.py` - add argument to parser
2. Update `main()` function to handle new option
3. May need to add new function in `core.py`

### To add new core functionality:
1. Add function to `core.py`
2. Export it in `__init__.py` if it should be public
3. Update `cli.py` to use it if needed

### To add new documentation:
1. Create markdown file in `docs/`
2. Link to it from `README.md`

## Best Practices Used

✅ **Type hints** - Functions specify parameter and return types
✅ **Docstrings** - Every function documented with examples
✅ **Error handling** - Graceful handling of invalid input
✅ **Constants** - Magic values defined as named constants
✅ **Comments** - Section headers and explanatory comments
✅ **Separation** - UI logic separate from business logic
✅ **DRY** - Don't Repeat Yourself - reusable functions

## Questions?

- See `README.md` for usage documentation
- See `docs/INSTALL.md` for installation help
- See `docs/QUICKSTART.md` for quick examples
- Read the source code - it's well-commented!
