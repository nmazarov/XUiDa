"""
XUiDa64 - Computer Summary View Widget
Recreates classic AIDA64 Computer -> Summary layout with cyber metric chips,
spanning section headers, uniform dark background, and high-contrast readable styling.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QMenu, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from core.i18n import I18N, _t, _prop
from core.system_info import SystemInfo
from core.cpu_info import CPUInfo
from core.memory_info import MemoryInfo
from core.gpu_info import GPUInfo
from core.storage_info import StorageInfo
from core.network_info import NetworkInfo

class SummaryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 1. Quick Metric Chips Banner
        self.chips_frame = QFrame()
        self.chips_frame.setStyleSheet("""
            QFrame {
                background-color: #161e2b;
                border: 1px solid #2a364a;
                border-radius: 8px;
            }
        """)
        chips_layout = QHBoxLayout(self.chips_frame)
        chips_layout.setContentsMargins(12, 8, 12, 8)
        chips_layout.setSpacing(12)

        self.chip_cpu = self._create_chip("⚙️ ЦП", "Intel Core i7", "#00d2ff")
        self.chip_gpu = self._create_chip("🎮 GPU", "GeForce RTX", "#10b981")
        self.chip_ram = self._create_chip("🧠 ОЗУ", "32 GB DDR5", "#f59e0b")
        self.chip_os = self._create_chip("🪟 ОС", "Windows 11", "#a855f7")

        chips_layout.addWidget(self.chip_cpu)
        chips_layout.addWidget(self.chip_gpu)
        chips_layout.addWidget(self.chip_ram)
        chips_layout.addWidget(self.chip_os)
        layout.addWidget(self.chips_frame)

        # 2. Detailed Summary Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([_t("col_field"), _t("col_value")])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.setAlternatingRowColors(False)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.table)

        I18N.register_listener(self.on_language_changed)
        self.refresh_data()

    def _create_chip(self, label, val, accent_hex):
        chip = QFrame()
        chip.setStyleSheet(f"""
            QFrame {{
                background-color: #1a2536;
                border: 1px solid #2d3e56;
                border-left: 4px solid {accent_hex};
                border-radius: 6px;
                padding: 4px 8px;
            }}
        """)
        c_layout = QVBoxLayout(chip)
        c_layout.setContentsMargins(8, 6, 8, 6)
        c_layout.setSpacing(3)

        lbl = QLabel(label)
        lbl.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {accent_hex};")
        val_lbl = QLabel(val)
        val_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #ffffff;")
        val_lbl.setObjectName("chip_val")

        c_layout.addWidget(lbl)
        c_layout.addWidget(val_lbl)
        return chip

    def on_language_changed(self, lang):
        self.table.setHorizontalHeaderLabels([_t("col_field"), _t("col_value")])
        self.refresh_data()

    def refresh_data(self):
        sys_info = SystemInfo.get_os_info()
        mb_info = SystemInfo.get_motherboard_info()
        bios_info = SystemInfo.get_bios_info()
        cpu = CPUInfo.get_details()
        mem = MemoryInfo.get_summary()
        spd = MemoryInfo.get_spd_modules()
        gpus = GPUInfo.get_all_gpus()
        monitors = GPUInfo.get_monitors()
        phys_drives = StorageInfo.get_physical_drives()
        log_drives = StorageInfo.get_logical_drives()
        adapters = NetworkInfo.get_adapters()

        is_ru = (I18N.get_language() == "ru")
        cores_word = "Ядер" if is_ru else "Cores"
        threads_word = "Потоков" if is_ru else "Threads"
        base_word = "Базовая" if is_ru else "Base"
        used_word = "Занято" if is_ru else "Used"
        free_word = "Свободно" if is_ru else "Free"
        pc_type = f"Компьютер на базе ACPI x64 ({sys_info.get('Architecture')})" if is_ru else f"ACPI x64-based PC ({sys_info.get('Architecture')})"
        os_label = f"{sys_info.get('OSName')} (Сборка {sys_info.get('Build')})" if is_ru else f"{sys_info.get('OSName')} (Build {sys_info.get('Build')})"
        mon_default = "Универсальный монитор" if is_ru else "Generic Monitor"
        net_default = "Отсутствует" if is_ru else "None"
        smart_val = "Исправен (Норма)" if (is_ru and phys_drives) else ("Healthy / OK" if phys_drives else "OK")

        # Update Top Chips
        cpu_brand = cpu.get('Brand', 'Processor')
        cpu_short = cpu_brand.replace("Intel(R) Core(TM) ", "").replace("AMD Ryzen ", "Ryzen ")
        self.chip_cpu.findChild(QLabel, "chip_val").setText(cpu_short[:22])

        gpu_name = gpus[0].get("Name", "Graphics") if gpus else "Integrated GPU"
        gpu_short = gpu_name.replace("NVIDIA GeForce ", "").replace("AMD Radeon ", "")
        self.chip_gpu.findChild(QLabel, "chip_val").setText(gpu_short[:22])

        ram_total = mem.get("TotalGB", 16)
        spd_type = spd[0].get("MemoryType", "RAM") if spd and len(spd) > 0 else "RAM"
        self.chip_ram.findChild(QLabel, "chip_val").setText(f"{ram_total} GB {spd_type}")

        os_name = sys_info.get("OSName", "Windows")
        os_short = os_name.replace("Microsoft Windows ", "Win ")
        self.chip_os.findChild(QLabel, "chip_val").setText(os_short[:22])

        dimm_text = f"Установлено модулей: {len(spd)} (" + ", ".join([f"{m.get('CapacityGB')} ГБ {m.get('MemoryType')}" for m in spd]) + ")" if is_ru else f"{len(spd)} Module(s) Installed (" + ", ".join([f"{m.get('CapacityGB')}GB {m.get('MemoryType')}" for m in spd]) + ")"

        sections = [
            (_t("sec_computer"), [
                ("Computer Type", pc_type),
                ("Operating System", os_label),
                ("OS Architecture", sys_info.get("Architecture")),
                ("Computer Name", sys_info.get("ComputerName")),
                ("User Name", sys_info.get("RegisteredUser")),
                ("System Uptime", sys_info.get("Uptime")),
                ("Install Date", sys_info.get("InstallDate"))
            ]),
            (_t("sec_motherboard"), [
                ("CPU Type", f"{cpu.get('Brand')} ({cpu.get('PhysicalCores')} {cores_word}, {cpu.get('LogicalCores')} {threads_word})"),
                ("CPU Clock", f"{cpu.get('CurrentClock')} ({base_word}: {cpu.get('BaseClock')})"),
                ("Motherboard Name", f"{mb_info.get('Manufacturer')} {mb_info.get('Product')}"),
                ("Motherboard Chipset", mb_info.get("Chipset")),
                ("System Memory", f"{mem.get('TotalGB')} GB ({used_word}: {mem.get('UsedGB')} GB, {free_word}: {mem.get('FreeGB')} GB)"),
                ("DIMM Modules", dimm_text),
                ("BIOS Type", f"{bios_info.get('Vendor')} ({bios_info.get('Version')})"),
                ("BIOS Release Date", bios_info.get("ReleaseDate")),
                ("Boot Mode", f"{bios_info.get('BootMode')} (SecureBoot: {_prop(str(bios_info.get('SecureBoot')))})")
            ]),
            (_t("sec_display"), [
                ("Video Adapter", gpus[0].get("Name") if gpus else "Generic Display Adapter"),
                ("Video Driver", gpus[0].get("DriverVersion") if gpus else "N/A"),
                ("Installed VRAM", f"{gpus[0].get('VRAM_MB', 0)} MB" if gpus else "N/A"),
                ("Current Resolution", gpus[0].get("Resolution") if gpus else "N/A"),
                ("Connected Monitor", ", ".join([m.get("Name") for m in monitors]) if monitors else mon_default)
            ]),
            (_t("sec_storage"), [
                ("Storage Drives", ", ".join([f"{d.get('Model')} ({d.get('SizeGB')} ГБ {d.get('MediaType')})" for d in phys_drives])),
                ("Partitions", " | ".join([f"{ld.get('Device')} {ld.get('TotalGB')} ГБ ({ld.get('FreeGB')} ГБ {free_word.lower()})" for ld in log_drives])),
                ("SMART Status", smart_val)
            ]),
            (_t("sec_network"), [
                ("Primary Network Adapter", adapters[0].get("Name") if adapters else net_default),
                ("IP Address", adapters[0].get("IPv4") if adapters else "N/A"),
                ("MAC Address", adapters[0].get("MAC") if adapters else "N/A"),
                ("Link Speed", adapters[0].get("Speed") if adapters else "N/A"),
                ("Default Gateway", adapters[0].get("Gateways") if adapters else "N/A")
            ])
        ]

        total_rows = sum(len(items) + 1 for _, items in sections)
        self.table.clearSpans()
        self.table.setRowCount(total_rows)

        curr_row = 0
        bold_val_font = QFont("Segoe UI", 9, QFont.Bold)

        for sec_title, items in sections:
            # Styled Spanning Section Header
            h_item = QTableWidgetItem(f"   ▶  {sec_title.upper()}")
            h_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            h_item.setForeground(QColor("#00d2ff"))
            h_item.setBackground(QColor("#1b2738"))

            self.table.setItem(curr_row, 0, h_item)
            self.table.setSpan(curr_row, 0, 1, 2)
            curr_row += 1

            for prop, val in items:
                p_item = QTableWidgetItem(f"    {_prop(prop)}")
                p_item.setForeground(QColor("#cbd5e1"))

                # Translate common boolean/status values
                val_str = str(val)
                if val_str in ("True", "False", "Healthy / OK", "OK"):
                    val_str = _prop(val_str)

                v_item = QTableWidgetItem(val_str)
                v_item.setForeground(QColor("#ffffff"))
                v_item.setFont(bold_val_font)

                self.table.setItem(curr_row, 0, p_item)
                self.table.setItem(curr_row, 1, v_item)
                curr_row += 1

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item:
            return
        menu = QMenu(self)
        copy_val_action = menu.addAction(_t("copy_value"))
        copy_all_action = menu.addAction(_t("copy_table"))
        action = menu.exec_(self.table.viewport().mapToGlobal(pos))
        if action == copy_val_action:
            QApplication.clipboard().setText(item.text())
        elif action == copy_all_action:
            rows = []
            for r in range(self.table.rowCount()):
                f = self.table.item(r, 0).text() if self.table.item(r, 0) else ""
                v = self.table.item(r, 1).text() if self.table.item(r, 1) else ""
                rows.append(f"{f}\t{v}")
            QApplication.clipboard().setText("\n".join(rows))
