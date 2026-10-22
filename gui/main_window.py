"""
XUiDa64 - Main Application Window
Recreates iconic AIDA64 interface with responsive category switching, live telemetry, and instant multi-language translation.
"""

import os
import webbrowser
import psutil
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QStackedWidget, QMenuBar, QMenu, QAction, QToolBar, QStatusBar,
    QLabel, QProgressBar, QMessageBox, QActionGroup, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont, QPixmap

from core.i18n import I18N, _t
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
        self.setWindowTitle(_t("app_title"))
        self.resize(1200, 800)
        self.setMinimumSize(960, 620)

        # Set Application Icon
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

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

        I18N.register_listener(self.on_language_changed)

    def _init_menu_and_toolbar(self):
        # 1. Menu Bar
        self.menu_bar = self.menuBar()

        # File Menu
        self.file_menu = self.menu_bar.addMenu(_t("menu_file"))
        self.act_report = self.file_menu.addAction(_t("act_report"))
        self.act_report.setShortcut("Ctrl+R")
        self.act_report.triggered.connect(self.open_report_wizard)

        self.act_refresh = self.file_menu.addAction(_t("act_refresh"))
        self.act_refresh.setShortcut("F5")
        self.act_refresh.triggered.connect(self.refresh_current_view)

        self.file_menu.addSeparator()
        self.act_exit = self.file_menu.addAction(_t("act_exit"))
        self.act_exit.setShortcut("Alt+F4")
        self.act_exit.triggered.connect(self.close)

        # View Menu
        self.view_menu = self.menu_bar.addMenu(_t("menu_view"))
        self.act_osd = self.view_menu.addAction(_t("act_osd"))
        self.act_osd.setShortcut("F9")
        self.act_osd.triggered.connect(self.toggle_sensor_panel)

        self.act_theme = self.view_menu.addAction(_t("act_theme"))
        self.act_theme.triggered.connect(self.toggle_theme)

        # Tools Menu
        self.tools_menu = self.menu_bar.addMenu(_t("menu_tools"))
        self.act_cpuid = self.tools_menu.addAction(_t("act_cpuid"))
        self.act_cpuid.setShortcut("Ctrl+D")
        self.act_cpuid.triggered.connect(self.open_cpuid)

        self.act_stress = self.tools_menu.addAction(_t("act_stress"))
        self.act_stress.setShortcut("Ctrl+T")
        self.act_stress.triggered.connect(self.open_stress_test)

        self.act_bench = self.tools_menu.addAction(_t("act_bench"))
        self.act_bench.triggered.connect(lambda: self._select_tree_item("Memory Read"))

        # Language Menu
        self.lang_menu = self.menu_bar.addMenu(_t("menu_language"))
        self.lang_group = QActionGroup(self)
        self.lang_group.setExclusive(True)

        languages = [
            ("🇷🇺 Русский", "ru"),
            ("🇬🇧 English", "en"),
            ("🇩🇪 Deutsch", "de"),
            ("🇨🇳 简体中文", "zh")
        ]

        curr_lang = I18N.get_language()
        for label, code in languages:
            act = self.lang_menu.addAction(label)
            act.setCheckable(True)
            if code == curr_lang:
                act.setChecked(True)
            act.triggered.connect(lambda checked, c=code: I18N.set_language(c))
            self.lang_group.addAction(act)

        # Help Menu
        self.help_menu = self.menu_bar.addMenu(_t("menu_help"))
        self.act_git = self.help_menu.addAction(_t("act_github"))
        self.act_git.triggered.connect(lambda: webbrowser.open("https://github.com"))

        self.act_about = self.help_menu.addAction(_t("act_about"))
        self.act_about.triggered.connect(self.open_about)

        # 2. Main ToolBar
        self.toolbar = QToolBar("Main Controls")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.btn_rep = self.toolbar.addAction(_t("tb_report"))
        self.btn_rep.triggered.connect(self.open_report_wizard)

        self.btn_cpuid = self.toolbar.addAction(_t("tb_cpuid"))
        self.btn_cpuid.triggered.connect(self.open_cpuid)

        self.btn_stress = self.toolbar.addAction(_t("tb_stress"))
        self.btn_stress.triggered.connect(self.open_stress_test)

        self.btn_bench = self.toolbar.addAction(_t("tb_benchmarks"))
        self.btn_bench.triggered.connect(lambda: self._select_tree_item("Memory Read"))

        self.btn_osd = self.toolbar.addAction(_t("tb_sensor_osd"))
        self.btn_osd.triggered.connect(self.toggle_sensor_panel)

        self.toolbar.addSeparator()

        self.btn_ref = self.toolbar.addAction(_t("tb_refresh"))
        self.btn_ref.triggered.connect(self.refresh_current_view)

        self.btn_theme = self.toolbar.addAction(_t("tb_theme"))
        self.btn_theme.triggered.connect(self.toggle_theme)

    def _init_central_ui(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        # Left: Sidebar container with logo and navigation tree
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(4, 4, 4, 4)
        sidebar_layout.setSpacing(6)

        # Brand Logo Header
        logo_frame = QFrame()
        logo_frame.setStyleSheet("""
            QFrame {
                background-color: #19212e;
                border: 1px solid #2a364a;
                border-radius: 6px;
                padding: 4px;
            }
        """)
        logo_layout = QHBoxLayout(logo_frame)
        logo_layout.setContentsMargins(6, 4, 6, 4)

        logo_label = QLabel()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "assets", "logo_small.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            logo_label.setPixmap(pix.scaledToWidth(220, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        sidebar_layout.addWidget(logo_frame)

        # Navigation Tree (collapsible accordion)
        self.tree = NavigationTree()
        sidebar_layout.addWidget(self.tree)

        sidebar.setMinimumWidth(240)
        sidebar.setMaximumWidth(340)
        splitter.addWidget(sidebar)

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

        self.sb_cpu_lbl = QLabel(f"{_t('cpu_usage')}: 0%")
        self.sb_cpu_bar = QProgressBar()
        self.sb_cpu_bar.setFixedSize(90, 14)
        self.sb_cpu_bar.setTextVisible(False)

        self.sb_ram_lbl = QLabel(f"{_t('ram_usage')}: 0%")
        self.sb_ram_bar = QProgressBar()
        self.sb_ram_bar.setFixedSize(90, 14)
        self.sb_ram_bar.setTextVisible(False)

        brand = CPUID.get_info().get("brand", "x86-64 Processor")
        self.sb_hw_lbl = QLabel(f"{_t('hardware')}: {brand}")
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

        self.sb_cpu_lbl.setText(f"{_t('cpu_usage')}: {cpu_p}%")
        self.sb_cpu_bar.setValue(cpu_p)

        self.sb_ram_lbl.setText(f"{_t('ram_usage')}: {ram_p}%")
        self.sb_ram_bar.setValue(ram_p)

    def on_language_changed(self, lang):
        self.setWindowTitle(_t("app_title"))

        self.file_menu.setTitle(_t("menu_file"))
        self.view_menu.setTitle(_t("menu_view"))
        self.tools_menu.setTitle(_t("menu_tools"))
        self.lang_menu.setTitle(_t("menu_language"))
        self.help_menu.setTitle(_t("menu_help"))

        self.act_report.setText(_t("act_report"))
        self.act_refresh.setText(_t("act_refresh"))
        self.act_exit.setText(_t("act_exit"))
        self.act_osd.setText(_t("act_osd"))
        self.act_theme.setText(_t("act_theme"))
        self.act_cpuid.setText(_t("act_cpuid"))
        self.act_stress.setText(_t("act_stress"))
        self.act_bench.setText(_t("act_bench"))
        self.act_git.setText(_t("act_github"))
        self.act_about.setText(_t("act_about"))

        self.btn_rep.setText(_t("tb_report"))
        self.btn_cpuid.setText(_t("tb_cpuid"))
        self.btn_stress.setText(_t("tb_stress"))
        self.btn_bench.setText(_t("tb_benchmarks"))
        self.btn_osd.setText(_t("tb_sensor_osd"))
        self.btn_ref.setText(_t("tb_refresh"))
        self.btn_theme.setText(_t("tb_theme"))

        brand = CPUID.get_info().get("brand", "x86-64 Processor")
        self.sb_hw_lbl.setText(f"{_t('hardware')}: {brand}")

        # Refresh currently selected view
        curr = self.tree.currentItem()
        if curr:
            self.on_nav_selected(curr, None)

    def on_nav_selected(self, current, previous):
        if not current:
            return

        # If a category header was selected and has children, select its first child
        if current.childCount() > 0:
            if current.isExpanded():
                self.tree.setCurrentItem(current.child(0))
            return

        internal_id = current.data(0, Qt.UserRole)
        if not internal_id:
            internal_id = current.text(0)

        # 1. Summary
        if internal_id == "Summary":
            self.stack.setCurrentWidget(self.summary_view)
            return

        # 2. Sensors
        if internal_id == "Sensors":
            self.stack.setCurrentWidget(self.sensor_view)
            return

        # 3. Processes
        if internal_id == "Processes":
            self.stack.setCurrentWidget(self.process_view)
            return

        # 4. Benchmarks
        bench_names = [
            "Memory Read", "Memory Write", "Memory Copy", "Memory Latency",
            "CPU Queen", "CPU PhotoWorxx", "CPU ZLib", "CPU AES", "CPU SHA3",
            "FPU Julia", "FPU Mandel", "FPU SinJulia"
        ]
        if internal_id in bench_names:
            self.stack.setCurrentWidget(self.benchmark_view)
            idx = self.benchmark_view.combo.findText(internal_id)
            if idx >= 0:
                self.benchmark_view.combo.setCurrentIndex(idx)
            return

        # 5. Table Views for various hardware sections
        self.stack.setCurrentWidget(self.table_view)

        if internal_id == "Computer Name":
            os_info = SystemInfo.get_os_info()
            self.table_view.set_data({
                "NetBIOS Computer Name": os_info.get("ComputerName"),
                "User Name": os_info.get("RegisteredUser"),
                "Workgroup / Domain": "WORKGROUP",
                "Operating System": os_info.get("OSName"),
                "Windows System Directory": os_info.get("SystemRoot")
            })
        elif internal_id == "Power Management":
            self.table_view.set_data(SystemInfo.get_power_info())
        elif internal_id == "CPU":
            details = CPUInfo.get_details()
            self.table_view.set_data(details)
        elif internal_id == "CPUID":
            cpuid_data = CPUID.get_info()
            self.table_view.set_data(cpuid_data)
        elif internal_id == "Motherboard":
            self.table_view.set_data(SystemInfo.get_motherboard_info())
        elif internal_id == "Memory":
            self.table_view.set_data(MemoryInfo.get_summary())
        elif internal_id == "SPD":
            self.table_view.set_data(MemoryInfo.get_spd_modules())
        elif internal_id == "BIOS":
            self.table_view.set_data(SystemInfo.get_bios_info())
        elif internal_id == "OS Info":
            self.table_view.set_data(SystemInfo.get_os_info())
        elif internal_id == "System Services":
            self.table_view.set_data(SoftwareInfo.get_services()[:120])
        elif internal_id == "Uptime":
            os_info = SystemInfo.get_os_info()
            self.table_view.set_data({
                "System Boot Time": os_info.get("BootTime"),
                "System Current Uptime": os_info.get("Uptime"),
                "System State": "Fully Operational (Clean Boot)"
            })
        elif internal_id == "Video Adapters":
            self.table_view.set_data(GPUInfo.get_all_gpus())
        elif internal_id == "Monitors":
            self.table_view.set_data(GPUInfo.get_monitors())
        elif internal_id == "Logical Drives":
            self.table_view.set_data(StorageInfo.get_logical_drives())
        elif internal_id == "Physical Drives":
            self.table_view.set_data(StorageInfo.get_physical_drives())
        elif internal_id == "SMART":
            self.table_view.set_data(StorageInfo.get_smart_status())
        elif internal_id == "Network Adapters":
            self.table_view.set_data(NetworkInfo.get_adapters())
        elif internal_id == "Traffic Monitor":
            self.table_view.set_data(NetworkInfo.get_realtime_traffic())
        elif internal_id == "Windows Devices":
            devs = DevicesInfo.get_devices()
            flat_devs = []
            for cat, items in devs.items():
                for it in items:
                    flat_devs.append({"Category": cat, "Name": it.get("Name"), "Status": it.get("Status")})
            self.table_view.set_data(flat_devs[:200])
        elif internal_id == "Installed Programs":
            self.table_view.set_data(SoftwareInfo.get_installed_programs())
        elif internal_id == "Startup Programs":
            self.table_view.set_data(SoftwareInfo.get_startup_programs())

    def _select_tree_item(self, target_id):
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            for j in range(top.childCount()):
                child = top.child(j)
                if child.data(0, Qt.UserRole) == target_id:
                    top.setExpanded(True)
                    self.tree.setCurrentItem(child)
                    return

    def refresh_current_view(self):
        curr = self.tree.currentItem()
        if curr:
            internal_id = curr.data(0, Qt.UserRole) or curr.text(0)
            if internal_id == "Summary":
                self.summary_view.refresh_data()
            elif internal_id == "Sensors":
                self.sensor_view.update_sensors()
            elif internal_id == "Processes":
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
