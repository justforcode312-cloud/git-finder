# Testing Guide for Git Finder

This document explains how to test the Git Finder package locally and in CI.

## Quick Local Testing

### Option 1: Run the Local Test Script (Recommended)
```bash
# This tests the package functionality without relying on PATH
python scripts/test_local.py
```

### Option 2: Run Unit Tests with pytest
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=git_finder --cov-report=html
```

### Option 3: Test the CLI Directly
```bash
# Install the package
pip install -e .

# Test via Python module (works everywhere)
python -m git_finder.cli --help
python -m git_finder.cli . --list

# Test via installed commands (may not work on Windows without PATH setup)
git-finder --help
gf --help
```

## Testing on Windows

Windows has special considerations due to how Python installs console scripts.

### Why Commands May Not Work on Windows

When you run `pip install`, Python creates executable scripts in the `Scripts` directory:
- **Linux/Mac**: `~/.local/bin/` or `/usr/local/bin/`
- **Windows**: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts\`

On Windows, this `Scripts` directory is often not in your PATH, so commands like `git-finder` won't work directly.

### Solutions for Windows

**Solution 1: Use Python Module Syntax (Always Works)**
```bash
python -m git_finder.cli
python -m git_finder.cli C:\Users\YourName\projects
python -m git_finder.cli --list
```

**Solution 2: Add Scripts to PATH**
```bash
# Find where pip installed the scripts
pip show -f git-finder

# Add the Scripts directory to your PATH
# In PowerShell (temporary):
$env:Path += ";C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts"

# Or add it permanently via System Properties > Environment Variables
```

**Solution 3: Use the Installation Script**
```bash
# The install.bat script handles PATH setup
scripts\install.bat
```

## Test Structure

```
tests/
├── __init__.py           # Test package marker
├── test_core.py          # Tests for core.py functions
└── test_cli.py           # Tests for cli.py functions

scripts/
├── test_local.py         # Local testing without PATH dependency
└── test_install.py       # Tests if commands are in PATH
```

## What Each Test Does

### Unit Tests (`tests/`)
- **test_core.py**: Tests core functionality
  - Finding Git repositories
  - Getting today's commits
  - Display functions
  - Error handling
  
- **test_cli.py**: Tests CLI interface
  - Argument parsing
  - User input prompting
  - Path validation
  - Error handling

### Integration Tests

**test_local.py**: Tests the package without relying on installed commands
- Import tests
- Function tests with temporary directories
- Display function tests
- Works on all platforms without PATH issues

**test_install.py**: Tests if console scripts are available
- Checks if `git-finder` command works
- Checks if `gf` alias works
- May fail on Windows if Scripts directory not in PATH

## Running Tests in Different Environments

### Local Development
```bash
# Quick test
python scripts/test_local.py

# Full test suite
pytest tests/ -v
```

### CI/CD (GitHub Actions)
The CI workflow runs:
1. Unit tests with pytest (cross-platform)
2. Local test script (cross-platform)
3. Python module test (cross-platform)
4. Installed command test (may fail on Windows, marked as non-critical)

### Manual Testing
```bash
# Test finding projects
python -m git_finder.cli ~/projects --list

# Test showing commits
python -m git_finder.cli ~/projects

# Test interactive mode
python -m git_finder.cli
```

## Troubleshooting

### "Command not found" on Windows
✅ **This is expected!** Use `python -m git_finder.cli` instead.

### "No module named git_finder"
```bash
# Install the package first
pip install -e .
```

### Tests fail with "Git not found"
```bash
# Make sure Git is installed and in PATH
git --version
```

### Import errors in tests
```bash
# Install test dependencies
pip install -r requirements-dev.txt
```

## CI/CD Status

The project uses GitHub Actions with the following jobs:

1. **Test Job**: Runs on Python 3.9-3.12 across Ubuntu, Windows, and macOS
   - Unit tests with pytest
   - Local functionality tests
   - CLI tests via Python module
   - Optional: Installed command tests

2. **Lint Job**: Code quality checks
   - Black (formatting)
   - isort (import sorting)
   - flake8 (linting)
   - mypy (type checking)

3. **Security Job**: Security scanning
   - Bandit (security issues)
   - Safety (dependency vulnerabilities)
   - pip-audit (package auditing)

4. **Build Job**: Package building
   - Builds wheel and source distribution
   - Validates with twine

## Best Practices

1. **Always test locally before pushing**
   ```bash
   python scripts/test_local.py
   pytest tests/ -v
   ```

2. **Use Python module syntax for cross-platform compatibility**
   ```bash
   python -m git_finder.cli
   ```

3. **Don't rely on console scripts in CI for Windows**
   - They may not be in PATH
   - Use `python -m` syntax instead

4. **Test with temporary directories**
   - All tests use `tempfile.TemporaryDirectory()`
   - No side effects on real repositories

5. **Mock external dependencies**
   - Tests don't require real Git repositories
   - Use fake `.git` directories for testing

## Adding New Tests

When adding new features, add corresponding tests:

```python
# tests/test_new_feature.py
import pytest
from git_finder.core import new_function

def test_new_function():
    """Test the new function."""
    result = new_function("input")
    assert result == "expected_output"
```

Run the new tests:
```bash
pytest tests/test_new_feature.py -v
```

## Coverage Reports

Generate coverage reports to see what code is tested:

```bash
# Install coverage tool
pip install pytest-cov

# Run tests with coverage
pytest tests/ --cov=git_finder --cov-report=html

# Open the report
# Windows: start htmlcov/index.html
# Mac: open htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
```

## Questions?

If you encounter issues:
1. Check this guide first
2. Run `python scripts/test_local.py` to verify basic functionality
3. Check the CI logs for detailed error messages
4. Open an issue with the error output
