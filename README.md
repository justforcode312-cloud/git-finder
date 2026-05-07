# Git Project Finder

A Python tool to discover Git repositories in a directory tree and display today's commits across all found projects.

## 📚 Documentation

- **[Installation Guide](docs/INSTALL.md)** - Detailed installation instructions
- **[Quick Start](docs/QUICKSTART.md)** - Get started in 30 seconds
- **[Testing Guide](TESTING.md)** - Comprehensive testing documentation
- **[Project Structure](PROJECT_STRUCTURE.md)** - Understand the codebase organization
- **[Code Guide](CODE_GUIDE.md)** - Learn how the code works
- **[Contributing](CONTRIBUTING.md)** - How to contribute to this project
- **[Changelog](CHANGELOG.md)** - Version history and changes

## Features

- 🔍 Recursively search for Git repositories in any directory
- 📝 **Show today's commits by default** - see what you've worked on today
- 📊 Optional: Display found projects in a formatted table
- ⚡ Optimized to skip common non-repository directories
- 🛡️ Robust error handling and timeout protection
- 💾 **Write to file** - Save results to a text file for reporting

## Installation

### Quick Install (Easiest)

**On Windows:**
```bash
# Double-click scripts/install.bat or run in terminal:
scripts\install.bat
```

**On Linux/Mac:**
```bash
# Make the script executable and run:
chmod +x scripts/install.sh
./scripts/install.sh
```

### Manual Install with pip
```bash
# Install from the project directory
pip install .

# Or install in editable mode for development
pip install -e .
```

After installation, you can run the tool from anywhere using:
```bash
git-finder    # Full command
gf            # Short alias
```

For detailed installation instructions and troubleshooting, see [docs/INSTALL.md](docs/INSTALL.md).

## Usage

### Show Today's Commits (Default)
```bash
# Interactive mode - prompts for directory
git-finder
# or
gf

# Search specific directory
git-finder /path/to/search
gf ~/projects
```

### List Projects Only
```bash
# Use --list flag to show projects without commits
git-finder --list
gf /path/to/search --list
```

### Save Results to File
```bash
# Use --output or -o flag to save results to a text file
git-finder --output results.txt
gf ~/projects -o activity_report.txt
```

### Get Help
```bash
git-finder --help
gf -h
```

## Example Output

### Default (Today's Commits)
```bash
$ gf ~/projects

================================================================================
TODAY'S COMMITS (2026-05-05)
================================================================================

my-project - Add new feature for user authentication
my-project - Fix bug in login form
another-repo - Update documentation
website - No commits

================================================================================
Total: 3 commit(s) across 4 project(s)
================================================================================
```

### With --list Flag
```bash
$ git-finder ~/projects --list

Found 4 Git project(s) under: /home/user/projects

#     Project Name                   Path
--------------------------------------------------------------------------------
1     my-project                     /home/user/projects/my-project
2     another-repo                   /home/user/projects/another-repo
3     website                        /home/user/projects/website
4     tools                          /home/user/projects/tools
```

## Uninstallation

```bash
pip uninstall git-finder
```

## Optimizations Applied

### Performance Improvements
1. **Directory Filtering**: Automatically skips common non-repository directories:
   - `node_modules`, `.venv`, `venv`, `__pycache__`
   - `.tox`, `dist`, `build`, `.eggs`

2. **Timeout Protection**: Git commands have a 5-second timeout to prevent hanging on problematic repositories

3. **Efficient Directory Traversal**: Uses in-place list modification (`dirnames[:]`) for better memory efficiency

### Code Quality Improvements
1. **Enhanced Documentation**: Added comprehensive docstrings with Args, Returns, and Raises sections
2. **Better Error Handling**: Specific exception catching instead of bare `except Exception`
3. **Type Hints**: Improved type annotations throughout
4. **Path Handling**: Uses `Path.home()` and `os.path.expanduser()` for cross-platform compatibility
5. **User Experience**: Added commit summary totals and better error messages

### Maintainability Improvements
1. **Package Metadata**: Added `__version__` and `__all__` to `__init__.py`
2. **Help Text**: Enhanced CLI help with examples
3. **Keyboard Interrupt Handling**: Graceful exit on Ctrl+C
4. **Cross-Platform**: Removed hardcoded Windows paths, uses dynamic home directory

## Project Structure

```
git-finder/
├── git_finder/          # Main package (source code)
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # Command-line interface
│   └── core.py         # Core functionality
├── scripts/             # Installation scripts
│   ├── install.bat     # Windows installer
│   ├── install.sh      # Linux/Mac installer
│   └── test_install.py # Installation test
├── docs/                # Documentation
│   ├── QUICKSTART.md   # Quick start guide
│   └── INSTALL.md      # Installation guide
├── README.md            # This file
├── PROJECT_STRUCTURE.md # Detailed structure explanation
├── setup.py            # Package setup
└── pyproject.toml      # Modern packaging config
```

For a detailed explanation of the project structure and code organization, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## Requirements

- Python 3.9+
- Git installed and available in PATH

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## CI/CD

This project uses GitHub Actions for continuous integration:

- ✅ **CI Pipeline** - Tests on Python 3.9-3.12 across Windows, Linux, and macOS
- ✅ **Linting** - Code quality checks with flake8, black, isort, mypy
- ✅ **Security** - Automated security scanning with Bandit, Safety, and pip-audit
- ✅ **CodeQL** - Advanced security analysis (requires code scanning to be enabled)
- ✅ **Release** - Automated package building and GitHub releases

See [.github/workflows/](.github/workflows/) for workflow details.

### Enabling CodeQL (Optional)

CodeQL provides advanced security analysis but requires enabling code scanning in your repository:

1. Go to your repository **Settings**
2. Navigate to **Security & analysis** (left sidebar)
3. Under **Code security and analysis**, click **Enable** for **Code scanning**
4. CodeQL will automatically run on future pushes

**Note:** CodeQL is optional. The project includes alternative security scanning with Bandit that works without additional setup.

## License

MIT License
