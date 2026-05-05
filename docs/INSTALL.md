# Installation Guide

## Quick Install

From the project directory, run:

```bash
pip install .
```

That's it! You can now use `git-finder` or `gf` from anywhere in your terminal.

## Installation Options

### 1. Standard Installation
```bash
pip install .
```
Installs the package to your Python environment.

### 2. Editable/Development Installation
```bash
pip install -e .
```
Installs in "editable" mode - changes to the source code are immediately reflected without reinstalling.

### 3. User Installation (No Admin Rights)
```bash
pip install --user .
```
Installs to your user directory if you don't have system-wide permissions.

## Verify Installation

After installation, verify it works:

```bash
# Check if commands are available
git-finder --help
gf --help

# Test with current directory
gf .
```

## Troubleshooting

### Command not found after installation

If you get "command not found" after installing:

1. **Check if Python scripts directory is in PATH:**
   ```bash
   # On Windows (PowerShell)
   $env:PATH -split ';' | Select-String Python

   # On Windows (CMD)
   echo %PATH%

   # On Linux/Mac
   echo $PATH | grep -i python
   ```

2. **Find where pip installed the scripts:**
   ```bash
   pip show -f git-finder
   ```

3. **Add Python Scripts to PATH (Windows):**
   - The scripts are typically installed in: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts`
   - Add this directory to your PATH environment variable

4. **Reinstall with --user flag:**
   ```bash
   pip uninstall git-finder
   pip install --user .
   ```

### Permission Errors

If you get permission errors:
```bash
pip install --user .
```

## Uninstallation

To remove the tool:
```bash
pip uninstall git-finder
```

## Requirements

- Python 3.9 or higher
- pip (Python package installer)
- Git installed and available in PATH
