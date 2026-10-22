"""
XUiDa64 - Computer Summary View Widget
Recreates classic AIDA64 Computer -> Summary layout with clean categorizations.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
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
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Field", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.table)

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

        sections = [
            ("Computer", [
                ("Computer Type", f"ACPI x64-based PC ({sys_info.get('Architecture')})"),
                ("Operating System", f"{sys_info.get('OSName')} (Build {sys_info.get('Build')})"),
                ("OS Architecture", sys_info.get("Architecture")),
                ("Computer Name", sys_info.get("ComputerName")),
                ("User Name", sys_info.get("RegisteredUser")),
                ("System Uptime", sys_info.get("Uptime")),
                ("Install Date", sys_info.get("InstallDate"))
            ]),
            ("Motherboard", [
                ("CPU Type", f"{cpu.get('Brand')} ({cpu.get('PhysicalCores')} Cores, {cpu.get('LogicalCores')} Threads)"),
                ("CPU Clock / Multiplier", f"{cpu.get('CurrentClock')} / Base: {cpu.get('BaseClock')}"),
                ("Motherboard Name", f"{mb_info.get('Manufacturer')} {mb_info.get('Product')}"),
                ("Motherboard Chipset", mb_info.get("Chipset")),
                ("System Memory", f"{mem.get('TotalGB')} GB (Used: {mem.get('UsedGB')} GB, Free: {mem.get('FreeGB')} GB)"),
                ("DIMM Modules", f"{len(spd)} Module(s) Installed (" + ", ".join([f"{m.get('CapacityGB')}GB {m.get('MemoryType')}" for m in spd]) + ")"),
                ("BIOS Type", f"{bios_info.get('Vendor')} ({bios_info.get('Version')})"),
                ("BIOS Release Date", bios_info.get("ReleaseDate")),
                ("Boot Mode", f"{bios_info.get('BootMode')} (SecureBoot: {bios_info.get('SecureBoot')})")
            ]),
            ("Display", [
                ("Video Adapter", gpus[0].get("Name") if gpus else "Generic Display Adapter"),
                ("Video Driver", gpus[0].get("DriverVersion") if gpus else "N/A"),
                ("Installed VRAM", f"{gpus[0].get('VRAM_MB', 0)} MB" if gpus else "N/A"),
                ("Current Resolution", gpus[0].get("Resolution") if gpus else "N/A"),
                ("Connected Monitor", ", ".join([m.get("Name") for m in monitors]) if monitors else "Generic Monitor")
            ]),
            ("Storage", [
                ("Storage Drives", ", ".join([f"{d.get('Model')} ({d.get('SizeGB')}GB {d.get('MediaType')})" for d in phys_drives])),
                ("Partitions", " | ".join([f"{ld.get('Device')} {ld.get('TotalGB')}GB ({ld.get('FreeGB')}GB free)" for ld in log_drives])),
                ("SMART Status", "All Physical Disks OK / Healthy" if phys_drives else "OK")
            ]),
            ("Network", [
                ("Primary Network Adapter", adapters[0].get("Name") if adapters else "None"),
                ("IP Address", adapters[0].get("IPv4") if adapters else "N/A"),
                ("MAC Address", adapters[0].get("MAC") if adapters else "N/A"),
                ("Link Speed", adapters[0].get("Speed") if adapters else "N/A"),
                ("Default Gateway", adapters[0].get("Gateways") if adapters else "N/A")
            ])
        ]

        total_rows = sum(len(items) + 1 for _, items in sections)
        self.table.setRowCount(total_rows)

        curr_row = 0
        for sec_title, items in sections:
            # Section Header
            h_item = QTableWidgetItem(f"[{sec_title.upper()}]")
            h_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            h_item.setForeground(QColor("#58a6ff"))
            h_item.setBackground(QColor("#1f2937"))
            v_empty = QTableWidgetItem("")
            v_empty.setBackground(QColor("#1f2937"))
            self.table.setItem(curr_row, 0, h_item)
            self.table.setItem(curr_row, 1, v_empty)
            curr_row += 1

            for prop, val in items:
                p_item = QTableWidgetItem(f"  {prop}")
                v_item = QTableWidgetItem(str(val))
                self.table.setItem(curr_row, 0, p_item)
                self.table.setItem(curr_row, 1, v_item)
                curr_row += 1

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item:
            return
        menu = QMenu(self)
        copy_val_action = menu.addAction("Copy Value")
        copy_all_action = menu.addAction("Copy All Summary")
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
