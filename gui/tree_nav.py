"""
XUiDa64 - Navigation Tree Widget
Recreates classic AIDA64 left-hand tree hierarchy with collapsible category accordions,
category icons, and multi-language support.
"""

import os
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from core.i18n import I18N, _t

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "tree")

class NavigationTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.setIndentation(16)
        self.setExpandsOnDoubleClick(False)
        self.item_registry = []  # [(item, key, is_category, internal_id)]
        
        self.itemClicked.connect(self._on_item_clicked)
        self.build_tree()

        I18N.register_listener(self.on_language_changed)

    def _get_icon(self, filename):
        icon_path = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()

    def build_tree(self):
        self.clear()
        self.item_registry = []

        structure = [
            ("cat_computer", "cat_computer.png", [
                ("nav_summary", "Summary"),
                ("nav_computer_name", "Computer Name"),
                ("nav_power", "Power Management"),
                ("nav_battery", "Battery"),
                ("nav_sensors", "Sensors")
            ]),
            ("cat_motherboard", "cat_motherboard.png", [
                ("nav_cpu", "CPU"),
                ("nav_cpuid", "CPUID"),
                ("nav_mb", "Motherboard"),
                ("nav_memory", "Memory"),
                ("nav_spd", "SPD"),
                ("nav_bios", "BIOS")
            ]),
            ("cat_os", "cat_os.png", [
                ("nav_os_info", "OS Info"),
                ("nav_processes", "Processes"),
                ("nav_services", "System Services"),
                ("nav_uptime", "Uptime")
            ]),
            ("cat_display", "cat_display.png", [
                ("nav_gpus", "Video Adapters"),
                ("nav_monitors", "Monitors")
            ]),
            ("cat_storage", "cat_storage.png", [
                ("nav_logical_drives", "Logical Drives"),
                ("nav_physical_drives", "Physical Drives"),
                ("nav_smart", "SMART")
            ]),
            ("cat_network", "cat_network.png", [
                ("nav_network_adapters", "Network Adapters"),
                ("nav_traffic", "Traffic Monitor")
            ]),
            ("cat_devices", "cat_devices.png", [
                ("nav_devices", "Windows Devices")
            ]),
            ("cat_software", "cat_software.png", [
                ("nav_programs", "Installed Programs"),
                ("nav_startup", "Startup Programs")
            ]),
            ("cat_benchmarks", "cat_benchmarks.png", [
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
        normal_font = QFont("Segoe UI", 9)
        bullet_icon = self._get_icon("item_bullet.png")

        for cat_key, icon_name, sub_items in structure:
            cat_title = _t(cat_key)
            cat_item = QTreeWidgetItem(self, [cat_title])
            cat_item.setFont(0, bold_font)
            cat_item.setData(0, Qt.UserRole, cat_key)
            cat_item.setIcon(0, self._get_icon(icon_name))
            cat_item.setSizeHint(0, QSize(200, 30))
            self.item_registry.append((cat_item, cat_key, True, cat_key))

            for sub_key, fallback_internal_id in sub_items:
                title = _t(sub_key)
                child = QTreeWidgetItem(cat_item, [title])
                child.setFont(0, normal_font)
                child.setData(0, Qt.UserRole, fallback_internal_id)
                child.setIcon(0, bullet_icon)
                child.setSizeHint(0, QSize(200, 24))
                cat_item.addChild(child)
                self.item_registry.append((child, sub_key, False, fallback_internal_id))

        # Collapse all categories by default so they are not all wide open
        self.collapseAll()

        # Expand only the first category (Computer) and select Summary
        first_cat = self.topLevelItem(0)
        if first_cat:
            first_cat.setExpanded(True)
            if first_cat.childCount() > 0:
                self.setCurrentItem(first_cat.child(0))

    def _on_item_clicked(self, item, column):
        """
        Collapsible accordion logic:
        Single clicking on a category folds or unfolds it.
        When unfolded, automatically selects the first sub-item.
        """
        if item.childCount() > 0:
            is_expanded = item.isExpanded()
            item.setExpanded(not is_expanded)
            if not is_expanded and item.childCount() > 0:
                self.setCurrentItem(item.child(0))

    def on_language_changed(self, lang):
        for item, key, is_cat, internal_id in self.item_registry:
            item.setText(0, _t(key))
