"""
XUiDa64 - Navigation Tree Widget
Recreates classic AIDA64 left-hand tree hierarchy with multi-language support.
"""

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from core.i18n import I18N, _t

class NavigationTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.setIndentation(18)
        self.item_registry = []  # [(item, key, is_category)]
        self.build_tree()

        I18N.register_listener(self.on_language_changed)

    def build_tree(self):
        self.clear()
        self.item_registry = []

        structure = [
            ("cat_computer", [
                ("nav_summary", "Summary"),
                ("nav_computer_name", "Computer Name"),
                ("nav_power", "Power Management"),
                ("nav_sensors", "Sensors")
            ]),
            ("cat_motherboard", [
                ("nav_cpu", "CPU"),
                ("nav_cpuid", "CPUID"),
                ("nav_mb", "Motherboard"),
                ("nav_memory", "Memory"),
                ("nav_spd", "SPD"),
                ("nav_bios", "BIOS")
            ]),
            ("cat_os", [
                ("nav_os_info", "OS Info"),
                ("nav_processes", "Processes"),
                ("nav_services", "System Services"),
                ("nav_uptime", "Uptime")
            ]),
            ("cat_display", [
                ("nav_gpus", "Video Adapters"),
                ("nav_monitors", "Monitors")
            ]),
            ("cat_storage", [
                ("nav_logical_drives", "Logical Drives"),
                ("nav_physical_drives", "Physical Drives"),
                ("nav_smart", "SMART")
            ]),
            ("cat_network", [
                ("nav_network_adapters", "Network Adapters"),
                ("nav_traffic", "Traffic Monitor")
            ]),
            ("cat_devices", [
                ("nav_devices", "Windows Devices")
            ]),
            ("cat_software", [
                ("nav_programs", "Installed Programs"),
                ("nav_startup", "Startup Programs")
            ]),
            ("cat_benchmarks", [
                ("Memory Read", "Memory Read"),
                ("Memory Write", "Memory Write"),
                ("Memory Copy", "Memory Copy"),
                ("Memory Latency", "Memory Latency"),
                ("CPU Queen", "CPU Queen"),
                ("CPU PhotoWorxx", "CPU PhotoWorxx"),
                ("CPU ZLib", "CPU ZLib"),
                ("CPU AES", "CPU AES"),
                ("CPU SHA3", "CPU SHA3"),
                ("FPU Julia", "FPU Julia"),
                ("FPU Mandel", "FPU Mandel"),
                ("FPU SinJulia", "FPU SinJulia")
            ])
        ]

        bold_font = QFont("Segoe UI", 10, QFont.Bold)

        for cat_key, sub_items in structure:
            cat_title = _t(cat_key)
            cat_item = QTreeWidgetItem(self, [cat_title])
            cat_item.setFont(0, bold_font)
            cat_item.setData(0, Qt.UserRole, cat_key)
            self.item_registry.append((cat_item, cat_key, True, cat_key))

            for sub_key, fallback_internal_id in sub_items:
                title = _t(sub_key)
                child = QTreeWidgetItem(cat_item, [title])
                child.setData(0, Qt.UserRole, fallback_internal_id)
                cat_item.addChild(child)
                self.item_registry.append((child, sub_key, False, fallback_internal_id))

        self.expandAll()

        # Select Computer -> Summary by default
        first_cat = self.topLevelItem(0)
        if first_cat and first_cat.childCount() > 0:
            self.setCurrentItem(first_cat.child(0))

    def on_language_changed(self, lang):
        for item, key, is_cat, internal_id in self.item_registry:
            item.setText(0, _t(key))
