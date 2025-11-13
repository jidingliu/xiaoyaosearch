@echo off
REM Windows batch script for setting up backend environment

echo 🔧 XiaoyaoSearch Backend Environment Setup (Windows)
echo ====================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not found in PATH
    echo Please install Python 3.9+ and add it to PATH
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Run the setup script
python setup_env.py

pause