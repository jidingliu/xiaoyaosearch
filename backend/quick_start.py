#!/usr/bin/env python3
"""
Quick start script for XiaoyaoSearch backend.

This script provides a simple way to start the backend server
after setting up the environment.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_venv():
    """Check if virtual environment is activated."""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found.")
        print("Please run the setup script first:")
        print("  python setup_env.py")
        return False

    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return True

    # Try to detect if we're in the venv
    if "venv" in sys.prefix:
        return True

    print("❌ Virtual environment not activated.")
    print("Please activate the virtual environment first:")

    if os.name == 'nt':  # Windows
        print("  venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("  source venv/bin/activate")

    return False


def start_server():
    """Start the FastAPI development server."""
    print("🚀 Starting FastAPI development server...")

    try:
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--reload",
            "--host", "127.0.0.1",
            "--port", "8000"
        ]

        print(f"Command: {' '.join(cmd)}")
        print("Server will be available at: http://127.0.0.1:8000")
        print("API docs available at: http://127.0.0.1:8000/docs")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)

        # Run uvicorn
        subprocess.run(cmd, check=True)

    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


def main():
    """Main function."""
    print("🔧 XiaoyaoSearch Backend Quick Start")
    print("=" * 40)

    # Change to backend directory if not already there
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    print(f"Working directory: {backend_dir}")

    # Check virtual environment
    if not check_venv():
        sys.exit(1)

    # Start server
    start_server()


if __name__ == "__main__":
    main()