@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Git Finder Installation Script
echo ========================================
echo.

echo Installing git-finder...
pip install .

if %ERRORLEVEL% neq 0 (
    echo.
    echo Standard installation failed, trying user installation...
    pip install --user .
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo ========================================
    echo Installation failed. Please check:
    echo 1. Python is installed
    echo 2. pip is available
    echo 3. You have internet connection
    echo ========================================
    goto :END
)

echo.
echo ========================================
echo Installation successful!
echo ========================================
echo.
echo You can now use these commands anywhere:
echo   - git-finder
echo   - gf
echo.
echo Try it now: gf --help
echo ========================================

echo.
echo Setup Complete!
echo ========================================

:END
echo.
pause
