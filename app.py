"""
XUiDa64 Extreme Edition - Open Source Hardware Diagnostics & Benchmark Suite
Main Application Entry Point.
"""

import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from gui.main_window import MainWindow

def main():
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Set Windows Taskbar App ID so icon groups properly
    try:
        app_id = "xuida.hardware.diagnostics.suite.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setApplicationName("XUiDa64 Extreme Edition")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("OpenAIDA Community")

    # Set Application Icon
    icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
