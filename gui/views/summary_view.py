"""
XUiDa64 - Computer Summary View Widget
Crafted with Benji Taylor / Stageshow Design Engineering principles:
- Elevated interactive CraftCards with smooth hover animation and pulsing telemetry LED.
- Cohesive typography, generous padding, and high-contrast readable properties.
- Spanning section headers with crisp pill badges and subtle borders.
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
from gui.widgets.animated_widgets import CraftCard

class SummaryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # 1. Quick Metric CraftCards Banner
        self.chips_layout = QHBoxLayout()
        self.chips_layout.setContentsMargins(0, 0, 0, 0)
        self.chips_layout.setSpacing(12)

        self.card_cpu = CraftCard(title="ЦП / Processor", value="--", subtitle="--", accent_color="#38bdf8")
        self.card_gpu = CraftCard(title="GPU / Графика", value="--", subtitle="--", accent_color="#10b981")
        self.card_ram = CraftCard(title="ОЗУ / Память", value="--", subtitle="--", accent_color="#f59e0b")
        self.card_os = CraftCard(title="ОС / Система", value="--", subtitle="--", accent_color="#a855f7")

        self.chips_layout.addWidget(self.card_cpu)
        self.chips_layout.addWidget(self.card_gpu)
        self.chips_layout.addWidget(self.card_ram)
        self.chips_layout.addWidget(self.card_os)
        layout.addLayout(self.chips_layout)

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

        # Update Top CraftCards
        cpu_brand = cpu.get('Brand', 'Processor')
        cpu_short = cpu_brand.replace("Intel(R) Core(TM) ", "").replace("AMD Ryzen ", "Ryzen ")
        cpu_cores_str = f"{cpu.get('PhysicalCores', 0)}C / {cpu.get('LogicalCores', 0)}T • {cpu.get('BaseClock', '')}"
        self.card_cpu.title_lbl.setText("ЦП / PROCESSOR" if is_ru else "CPU / PROCESSOR")
        self.card_cpu.set_value(cpu_short[:24])
        self.card_cpu.set_subtitle(cpu_cores_str)

        gpu_name = gpus[0].get("Name", "Graphics") if gpus else "Integrated GPU"
        gpu_short = gpu_name.replace("NVIDIA GeForce ", "").replace("AMD Radeon ", "")
        gpu_vram = f"{gpus[0].get('VRAM_MB', 0)} MB VRAM" if gpus and gpus[0].get('VRAM_MB') else ("DirectX 12" if gpus else "Standard VGA")
        self.card_gpu.title_lbl.setText("GPU / ГРАФИКА" if is_ru else "GPU / GRAPHICS")
        self.card_gpu.set_value(gpu_short[:24])
        self.card_gpu.set_subtitle(gpu_vram)

        ram_total = mem.get("TotalGB", 16)
        spd_type = spd[0].get("MemoryType", "RAM") if spd and len(spd) > 0 else "RAM"
        ram_sub = f"{used_word}: {mem.get('UsedGB', 0)} ГБ ({mem.get('Percent', 0)}%)" if is_ru else f"Used: {mem.get('UsedGB', 0)} GB ({mem.get('Percent', 0)}%)"
        self.card_ram.title_lbl.setText("ОЗУ / ПАМЯТЬ" if is_ru else "RAM / MEMORY")
        self.card_ram.set_value(f"{ram_total} GB {spd_type}")
        self.card_ram.set_subtitle(ram_sub)

        os_name = sys_info.get("OSName", "Windows")
        os_short = os_name.replace("Microsoft Windows ", "Win ")
        os_sub = f"Сборка {sys_info.get('Build', '')} ({sys_info.get('Architecture', '')})" if is_ru else f"Build {sys_info.get('Build', '')} ({sys_info.get('Architecture', '')})"
        self.card_os.title_lbl.setText("ОС / СИСТЕМА" if is_ru else "OS / SYSTEM")
        self.card_os.set_value(os_short[:24])
        self.card_os.set_subtitle(os_sub)

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
        bold_val_font = QFont("Segoe UI Variable Text", 9, QFont.Bold)
        prop_font = QFont("Segoe UI Variable Text", 9, QFont.Normal)

        for sec_title, items in sections:
            # Styled Section Header with generous 34px height
            self.table.setRowHeight(curr_row, 34)
            h_item = QTableWidgetItem(f"   ❖  {sec_title.upper()}")
            h_item.setFont(QFont("Segoe UI Variable Text", 10, QFont.Bold))
            h_item.setForeground(QColor("#38bdf8"))
            h_item.setBackground(QColor("#131924"))

            self.table.setItem(curr_row, 0, h_item)
            self.table.setSpan(curr_row, 0, 1, 2)
            curr_row += 1

            for prop, val in items:
                self.table.setRowHeight(curr_row, 28)
                p_item = QTableWidgetItem(f"    {_prop(prop)}")
                p_item.setFont(prop_font)
                p_item.setForeground(QColor("#94a3b8"))

                val_str = str(val)
                if val_str in ("True", "False", "Healthy / OK", "OK"):
                    val_str = _prop(val_str)

                v_item = QTableWidgetItem(val_str)
                v_item.setForeground(QColor("#f8fafc"))
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
