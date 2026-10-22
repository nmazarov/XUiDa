"""
XUiDa64 - Main Application Window
Recreates iconic AIDA64 interface with responsive category switching and live telemetry.
"""

import os
import webbrowser
import psutil
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QStackedWidget, QMenuBar, QMenu, QAction, QToolBar, QStatusBar,
    QLabel, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

from gui.styles import DARK_THEME, CLASSIC_THEME
from gui.tree_nav import NavigationTree
from gui.views.summary_view import SummaryView
from gui.views.table_view import PropertyTableView
from gui.views.sensor_view import SensorView
from gui.views.process_view import ProcessView
from gui.views.benchmark_view import BenchmarkView
from gui.dialogs.cpuid_dialog import CPUIDDialog
from gui.dialogs.stress_dialog import StressTestDialog
from gui.dialogs.sensor_panel import DesktopSensorPanel
from gui.dialogs.report_dialog import ReportWizardDialog
from gui.dialogs.about_dialog import AboutDialog

from core.system_info import SystemInfo
from core.cpu_info import CPUInfo
from core.cpuid import CPUID
from core.memory_info import MemoryInfo
from core.gpu_info import GPUInfo
from core.storage_info import StorageInfo
from core.network_info import NetworkInfo
from core.devices_info import DevicesInfo
from core.software_info import SoftwareInfo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XUiDa64 Extreme Edition [Community Free & Open Source]")
        self.resize(1180, 780)
        self.setMinimumSize(950, 600)

        self.dark_mode = True
        self.setStyleSheet(DARK_THEME)

        self.sensor_panel = None

        # Build UI Elements
        self._init_menu_and_toolbar()
        self._init_central_ui()
        self._init_status_bar()

        # Connect Navigation
        self.tree.currentItemChanged.connect(self.on_nav_selected)

        # Telemetry Timer for Status Bar
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self._update_status_bar)
        self.status_timer.start(1500)

    def _init_menu_and_toolbar(self):
        # 1. Menu Bar
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        act_report = file_menu.addAction("📑 Report Wizard...")
        act_report.setShortcut("Ctrl+R")
        act_report.triggered.connect(self.open_report_wizard)

        act_refresh = file_menu.addAction("🔄 Refresh Hardware")
        act_refresh.setShortcut("F5")
        act_refresh.triggered.connect(self.refresh_current_view)

        file_menu.addSeparator()
        act_exit = file_menu.addAction("Exit")
        act_exit.setShortcut("Alt+F4")
        act_exit.triggered.connect(self.close)

        # View Menu
        view_menu = menu_bar.addMenu("&View")
        act_osd = view_menu.addAction("📊 Sensor Desktop OSD")
        act_osd.setShortcut("F9")
        act_osd.triggered.connect(self.toggle_sensor_panel)

        act_theme = view_menu.addAction("🌓 Toggle Dark / Light Theme")
        act_theme.triggered.connect(self.toggle_theme)

        # Tools Menu
        tools_menu = menu_bar.addMenu("&Tools")
        act_cpuid = tools_menu.addAction("⚡ AIDA64 CPUID Utility...")
        act_cpuid.setShortcut("Ctrl+D")
        act_cpuid.triggered.connect(self.open_cpuid)

        act_stress = tools_menu.addAction("🔥 System Stability Test...")
        act_stress.setShortcut("Ctrl+T")
        act_stress.triggered.connect(self.open_stress_test)

        act_bench = tools_menu.addAction("🏆 Memory & CPU Benchmarks")
        act_bench.triggered.connect(lambda: self._select_tree_item("Memory Read"))

        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        act_git = help_menu.addAction("🌐 GitHub Project Repository")
        act_git.triggered.connect(lambda: webbrowser.open("https://github.com"))

        act_about = help_menu.addAction("ℹ About XUiDa64 Extreme Edition")
        act_about.triggered.connect(self.open_about)

        # 2. Main ToolBar
        toolbar = QToolBar("Main Controls")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        btn_rep = toolbar.addAction("📑 Report Wizard")
        btn_rep.triggered.connect(self.open_report_wizard)

        btn_cpuid = toolbar.addAction("⚡ CPUID")
        btn_cpuid.triggered.connect(self.open_cpuid)

        btn_stress = toolbar.addAction("🔥 Stability Test")
        btn_stress.triggered.connect(self.open_stress_test)

        btn_bench = toolbar.addAction("🏆 Benchmarks")
        btn_bench.triggered.connect(lambda: self._select_tree_item("Memory Read"))

        btn_osd = toolbar.addAction("📊 Sensor OSD")
        btn_osd.triggered.connect(self.toggle_sensor_panel)

        toolbar.addSeparator()

        btn_ref = toolbar.addAction("🔄 Refresh")
        btn_ref.triggered.connect(self.refresh_current_view)

        btn_theme = toolbar.addAction("🌓 Theme")
        btn_theme.triggered.connect(self.toggle_theme)

    def _init_central_ui(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        # Left: Navigation Tree
        self.tree = NavigationTree()
        self.tree.setMinimumWidth(220)
        self.tree.setMaximumWidth(340)
        splitter.addWidget(self.tree)

        # Right: Views Stack
        self.stack = QStackedWidget()

        # Dedicated Views
        self.summary_view = SummaryView()
        self.sensor_view = SensorView()
        self.process_view = ProcessView()
        self.benchmark_view = BenchmarkView()
        self.table_view = PropertyTableView()

        self.stack.addWidget(self.summary_view)     # 0
        self.stack.addWidget(self.table_view)       # 1
        self.stack.addWidget(self.sensor_view)      # 2
        self.stack.addWidget(self.process_view)     # 3
        self.stack.addWidget(self.benchmark_view)   # 4

        splitter.addWidget(self.stack)
        splitter.setStretchFactor(1, 4)

        self.setCentralWidget(splitter)

    def _init_status_bar(self):
        sb = self.statusBar()

        self.sb_cpu_lbl = QLabel("CPU: 0%")
        self.sb_cpu_bar = QProgressBar()
        self.sb_cpu_bar.setFixedSize(90, 14)
        self.sb_cpu_bar.setTextVisible(False)

        self.sb_ram_lbl = QLabel("RAM: 0%")
        self.sb_ram_bar = QProgressBar()
        self.sb_ram_bar.setFixedSize(90, 14)
        self.sb_ram_bar.setTextVisible(False)

        brand = CPUID.get_info().get("brand", "x86-64 Processor")
        self.sb_hw_lbl = QLabel(f"Hardware: {brand}")
        self.sb_hw_lbl.setStyleSheet("color: #58a6ff; font-weight: bold;")

        sb.addPermanentWidget(self.sb_hw_lbl)
        sb.addPermanentWidget(QLabel("  |  "))
        sb.addPermanentWidget(self.sb_cpu_lbl)
        sb.addPermanentWidget(self.sb_cpu_bar)
        sb.addPermanentWidget(QLabel("  |  "))
        sb.addPermanentWidget(self.sb_ram_lbl)
        sb.addPermanentWidget(self.sb_ram_bar)

        self._update_status_bar()

    def _update_status_bar(self):
        cpu_p = int(psutil.cpu_percent(interval=None))
        ram_p = int(psutil.virtual_memory().percent)

        self.sb_cpu_lbl.setText(f"CPU: {cpu_p}%")
        self.sb_cpu_bar.setValue(cpu_p)

        self.sb_ram_lbl.setText(f"RAM: {ram_p}%")
        self.sb_ram_bar.setValue(ram_p)

    def on_nav_selected(self, current, previous):
        if not current:
            return
        title = current.text(0)

        # 1. Summary
        if title == "Summary":
            self.stack.setCurrentWidget(self.summary_view)
            return

        # 2. Sensors
        if title == "Sensors":
            self.stack.setCurrentWidget(self.sensor_view)
            return

        # 3. Processes
        if title == "Processes":
            self.stack.setCurrentWidget(self.process_view)
            return

        # 4. Benchmarks
        bench_names = [
            "Memory Read", "Memory Write", "Memory Copy", "Memory Latency",
            "CPU Queen", "CPU PhotoWorxx", "CPU ZLib", "CPU AES", "CPU SHA3",
            "FPU Julia", "FPU Mandel", "FPU SinJulia"
        ]
        if title in bench_names:
            self.stack.setCurrentWidget(self.benchmark_view)
            idx = self.benchmark_view.combo.findText(title)
            if idx >= 0:
                self.benchmark_view.combo.setCurrentIndex(idx)
            return

        # 5. Table Views for various hardware sections
        self.stack.setCurrentWidget(self.table_view)

        if title == "Computer Name":
            os_info = SystemInfo.get_os_info()
            self.table_view.set_data({
                "NetBIOS Computer Name": os_info.get("ComputerName"),
                "User Name": os_info.get("RegisteredUser"),
                "Workgroup / Domain": "WORKGROUP",
                "Operating System": os_info.get("OSName"),
                "Windows System Directory": os_info.get("SystemRoot")
            })
        elif title == "Power Management":
            self.table_view.set_data(SystemInfo.get_power_info())
        elif title == "CPU":
            details = CPUInfo.get_details()
            self.table_view.set_data(details)
        elif title == "CPUID":
            cpuid_data = CPUID.get_info()
            self.table_view.set_data(cpuid_data)
        elif title == "Motherboard":
            self.table_view.set_data(SystemInfo.get_motherboard_info())
        elif title == "Memory":
            self.table_view.set_data(MemoryInfo.get_summary())
        elif title == "SPD":
            self.table_view.set_data(MemoryInfo.get_spd_modules())
        elif title == "BIOS":
            self.table_view.set_data(SystemInfo.get_bios_info())
        elif title == "OS Info":
            self.table_view.set_data(SystemInfo.get_os_info())
        elif title == "System Services":
            self.table_view.set_data(SoftwareInfo.get_services()[:120])
        elif title == "Uptime":
            os_info = SystemInfo.get_os_info()
            self.table_view.set_data({
                "System Boot Time": os_info.get("BootTime"),
                "System Current Uptime": os_info.get("Uptime"),
                "System State": "Fully Operational (Clean Boot)"
            })
        elif title == "Video Adapters":
            self.table_view.set_data(GPUInfo.get_all_gpus())
        elif title == "Monitors":
            self.table_view.set_data(GPUInfo.get_monitors())
        elif title == "Logical Drives":
            self.table_view.set_data(StorageInfo.get_logical_drives())
        elif title == "Physical Drives":
            self.table_view.set_data(StorageInfo.get_physical_drives())
        elif title == "SMART":
            self.table_view.set_data(StorageInfo.get_smart_status())
        elif title == "Network Adapters":
            self.table_view.set_data(NetworkInfo.get_adapters())
        elif title == "Traffic Monitor":
            self.table_view.set_data(NetworkInfo.get_realtime_traffic())
        elif title == "Windows Devices":
            devs = DevicesInfo.get_devices()
            flat_devs = []
            for cat, items in devs.items():
                for it in items:
                    flat_devs.append({"Category": cat, "Name": it.get("Name"), "Status": it.get("Status")})
            self.table_view.set_data(flat_devs[:200])
        elif title == "Installed Programs":
            self.table_view.set_data(SoftwareInfo.get_installed_programs())
        elif title == "Startup Programs":
            self.table_view.set_data(SoftwareInfo.get_startup_programs())

    def _select_tree_item(self, target_text):
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            for j in range(top.childCount()):
                child = top.child(j)
                if child.text(0) == target_text:
                    self.tree.setCurrentItem(child)
                    return

    def refresh_current_view(self):
        curr = self.tree.currentItem()
        if curr:
            if curr.text(0) == "Summary":
                self.summary_view.refresh_data()
            elif curr.text(0) == "Sensors":
                self.sensor_view.update_sensors()
            elif curr.text(0) == "Processes":
                self.process_view.refresh_processes()
            else:
                self.on_nav_selected(curr, None)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.setStyleSheet(DARK_THEME if self.dark_mode else CLASSIC_THEME)

    def open_cpuid(self):
        dlg = CPUIDDialog(self)
        dlg.exec_()

    def open_stress_test(self):
        dlg = StressTestDialog(self)
        dlg.exec_()

    def toggle_sensor_panel(self):
        if self.sensor_panel is None:
            self.sensor_panel = DesktopSensorPanel()
        if self.sensor_panel.isVisible():
            self.sensor_panel.hide()
        else:
            self.sensor_panel.show()

    def open_report_wizard(self):
        dlg = ReportWizardDialog(self)
        dlg.exec_()

    def open_about(self):
        dlg = AboutDialog(self)
        dlg.exec_()
