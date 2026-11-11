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

from gui.widgets.splash_screen import CyberSplashScreen
from gui.main_window import MainWindow
from gui.styles import apply_dark_palette

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
    apply_dark_palette(app)
    app.setApplicationName("XUiDa64 Extreme Edition")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("XUiDa Community")

    # Set Application Icon
    icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # 1. Immediately show animated Cyber Splash Screen
    splash = CyberSplashScreen()
    splash.show()
    app.processEvents()

    # 2. Sequential progress updates during hardware discovery
    splash.set_progress(20, "⚡ Инициализация инструкций x86-64 CPUID...")
    app.processEvents()

    splash.set_progress(45, "🔍 Инициализация WMI и опрос системной шины...")
    app.processEvents()

    # 3. Instantiate main window
    window = MainWindow()

    splash.set_progress(80, "💾 Подготовка модулей диагностики и очистки...")
    app.processEvents()

    splash.set_progress(100, "✔ Запуск интерфейса XUiDa64...")
    app.processEvents()

    # 4. Seamless reveal: show main window and close splash
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
