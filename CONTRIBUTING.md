# Contributing to Git Finder

Thank you for your interest in contributing to Git Finder! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Documentation](#documentation)

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/git-finder.git
   cd git-finder
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/git-finder.git
   ```

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Git
- pip

### Install in Development Mode

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install in editable mode with development dependencies
pip install -e .
pip install black flake8 isort mypy pytest
```

### Verify Installation

```bash
# Test the commands work
git-finder --help
gf --help

# Run the installation test
python scripts/test_install.py
```

## Making Changes

### 1. Create a Branch

```bash
# Update your local main branch
git checkout main
git pull upstream main

# Create a new branch for your changes
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed
- Add tests for new features

### 3. Test Your Changes

```bash
# Test the tool works
gf . --list
gf . 

# Run any tests
python scripts/test_install.py
```

## Testing

### Manual Testing

```bash
# Test basic functionality
gf ~/projects
gf ~/projects --list
gf --help

# Test with different paths
gf .
gf /path/to/repos

# Test error handling
gf /nonexistent/path
```

### Automated Testing

```bash
# Run installation test
python scripts/test_install.py

# If you add unit tests (future):
pytest tests/
```

## Submitting Changes

### 1. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add feature: description of what you did"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

**Examples:**
```
Add --week flag to show commits from last 7 days
Fix bug in path handling on Windows
Update documentation for installation
Refactor core.py for better readability
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create a Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Select your branch
4. Fill out the PR template
5. Submit the pull request

### Pull Request Guidelines

- Fill out the PR template completely
- Link to any related issues
- Describe what you changed and why
- Include screenshots for UI changes
- Ensure CI checks pass
- Respond to review feedback

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Use 4 spaces for indentation
def example_function():
    pass

# Maximum line length: 100 characters (not 79)
long_variable_name = "This is a long string that might exceed the limit"

# Use type hints
def find_projects(path: str) -> List[str]:
    pass

# Use docstrings for all functions
def my_function(param: str) -> bool:
    """
    Brief description.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    pass
```

### Code Formatting Tools

```bash
# Format code with Black
black git_finder/

# Sort imports with isort
isort git_finder/

# Check with flake8
flake8 git_finder/

# Type check with mypy
mypy git_finder/ --ignore-missing-imports
```

### Code Organization

- Keep functions focused and single-purpose
- Use meaningful variable names
- Add comments for complex logic
- Group related functions together
- Use constants for magic values

## Documentation

### Code Documentation

- Add docstrings to all functions
- Include examples in docstrings
- Explain "why" not just "what"
- Keep comments up to date

### User Documentation

If your changes affect user-facing features:

1. Update `README.md`
2. Update relevant guides in `docs/`
3. Add examples if applicable
4. Update `CODE_GUIDE.md` if code structure changes

## Project Structure

```
git-finder/
├── git_finder/          # Source code
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # Command-line interface
│   └── core.py         # Core functionality
├── scripts/             # Utility scripts
├── docs/                # Documentation
├── .github/             # GitHub configuration
│   ├── workflows/      # CI/CD workflows
│   └── ISSUE_TEMPLATE/ # Issue templates
└── tests/              # Tests (future)
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed explanation.

## Types of Contributions

### Bug Fixes
- Check existing issues first
- Create an issue if one doesn't exist
- Reference the issue in your PR

### New Features
- Discuss in an issue first
- Get feedback on the approach
- Implement with tests and documentation

### Documentation
- Fix typos and clarify explanations
- Add examples
- Improve organization

### Code Quality
- Refactor for readability
- Add type hints
- Improve error handling
- Add comments

## Getting Help

- Read the [CODE_GUIDE.md](CODE_GUIDE.md) to understand the codebase
- Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for organization
- Open an issue for questions
- Ask in pull request comments

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes (for significant contributions)
- CHANGELOG.md

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Search existing issues
3. Open a new issue with the "question" label

Thank you for contributing to Git Finder! 🎉
