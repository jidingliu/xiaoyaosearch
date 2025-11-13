#!/bin/bash
# Unix shell script for setting up backend environment

echo "🔧 XiaoyaoSearch Backend Environment Setup (Unix/Linux/macOS)"
echo "================================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not found"
    echo "Please install Python 3.9+ and add it to PATH"
    exit 1
fi

echo "✓ Python 3 found"
python3 --version

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.9+ is required, found $PYTHON_VERSION"
    exit 1
fi

# Make setup script executable
chmod +x setup_env.py

# Run the setup script
python3 setup_env.py