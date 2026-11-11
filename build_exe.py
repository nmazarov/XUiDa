"""
XUiDa64 - Automated PyInstaller Build Script
Builds a standalone portable Windows executable for GitHub Releases.
"""

import os
import sys
import subprocess
import shutil

def build():
    print("=" * 60)
    print("  Building XUiDa64 Extreme Edition Standalone Executable")
    print("=" * 60)

    dist_dir = os.path.join(os.path.dirname(__file__), "dist")
    build_dir = os.path.join(os.path.dirname(__file__), "build")

    # Command arguments for PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--name=XUiDa64",
        "--icon=assets/icon.ico",
        "--add-data=assets;assets",
        "--clean",
        "--noconfirm",
        "--onedir",
        "--hidden-import=PyQt5",
        "--hidden-import=pyqtgraph",
        "--hidden-import=numpy",
        "--hidden-import=psutil",
        "--hidden-import=win32com",
        "--hidden-import=win32com.client",
        "--hidden-import=cryptography",
        "--hidden-import=cpuinfo",
        "--hidden-import=PIL",
        "app.py"
    ]

    print("Executing command:")
    print(" ".join(cmd))
    print("-" * 60)

    try:
        res = subprocess.run(cmd, check=True)
        print("=" * 60)
        print(f"Build succeeded! Standalone executable located at:")
        print(os.path.abspath(os.path.join("dist", "XUiDa64", "XUiDa64.exe")))
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error code: {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    build()
