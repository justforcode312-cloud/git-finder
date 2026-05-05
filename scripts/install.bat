@echo off
echo ========================================
echo Git Finder Installation Script
echo ========================================
echo.

echo Installing git-finder...
pip install .

if %ERRORLEVEL% EQU 0 (
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
) else (
    echo.
    echo ========================================
    echo Installation failed!
    echo ========================================
    echo.
    echo Trying user installation...
    pip install --user .
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ========================================
        echo User installation successful!
        echo ========================================
        echo.
        echo You can now use these commands anywhere:
        echo   - git-finder
        echo   - gf
        echo.
        echo Try it now: gf --help
        echo ========================================
    ) else (
        echo.
        echo Installation failed. Please check:
        echo 1. Python is installed
        echo 2. pip is available
        echo 3. You have internet connection
    )
)

echo.
pause
