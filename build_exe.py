"""
XUiDa64 - Automated PyInstaller Cross-Platform Build Script
Builds a standalone portable executable for Windows and Linux.
"""

import os
import sys
import subprocess
import shutil

def build():
    is_windows = sys.platform == "win32"
    platform_name = "Windows" if is_windows else "Linux"
    print("=" * 60)
    print(f"  Building XUiDa64 Extreme Edition Standalone Executable ({platform_name})")
    print("=" * 60)

    dist_dir = os.path.join(os.path.dirname(__file__), "dist")
    build_dir = os.path.join(os.path.dirname(__file__), "build")

    data_sep = ";" if is_windows else ":"

    # Command arguments for PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--name=XUiDa64",
        f"--add-data=assets{data_sep}assets",
        "--clean",
        "--noconfirm",
        "--onedir",
        "--hidden-import=PyQt5",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=pyqtgraph",
        "--hidden-import=numpy",
        "--hidden-import=psutil",
        "--hidden-import=cryptography",
        "--hidden-import=cpuinfo",
        "--hidden-import=PIL",
    ]

    if is_windows:
        cmd.extend([
            "--icon=assets/icon.ico",
            "--hidden-import=win32com",
            "--hidden-import=win32com.client",
        ])
    else:
        # On Linux, icon can be png or omitted from PE header
        if os.path.exists("assets/icon.png"):
            cmd.append("--icon=assets/icon.png")

    cmd.append("app.py")

    print("Executing command:")
    print(" ".join(cmd))
    print("-" * 60)

    try:
        subprocess.run(cmd, check=True)
        bin_name = "XUiDa64.exe" if is_windows else "XUiDa64"
        out_bin = os.path.abspath(os.path.join(dist_dir, "XUiDa64", bin_name))

        if not is_windows and os.path.exists(out_bin):
            try:
                os.chmod(out_bin, 0o755)
            except Exception:
                pass

        print("=" * 60)
        print(f"Build succeeded! Standalone executable located at:")
        print(out_bin)
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error code: {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    build()
