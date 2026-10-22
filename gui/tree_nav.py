"""
XUiDa64 - Navigation Tree Widget
Recreates classic AIDA64 left-hand tree hierarchy for hardware, OS, and benchmarks.
"""

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

class NavigationTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.setIndentation(18)
        self.build_tree()

    def build_tree(self):
        self.clear()

        structure = [
            ("🖥️ Computer", [
                "Summary",
                "Computer Name",
                "Power Management",
                "Sensors"
            ]),
            ("⚡ Motherboard", [
                "CPU",
                "CPUID",
                "Motherboard",
                "Memory",
                "SPD",
                "BIOS"
            ]),
            ("🪟 Operating System", [
                "OS Info",
                "Processes",
                "System Services",
                "Uptime"
            ]),
            ("🎮 Display", [
                "Video Adapters",
                "Monitors"
            ]),
            ("💾 Storage", [
                "Logical Drives",
                "Physical Drives",
                "SMART"
            ]),
            ("🌐 Network", [
                "Network Adapters",
                "Traffic Monitor"
            ]),
            ("🔌 Devices", [
                "Windows Devices"
            ]),
            ("📦 Software", [
                "Installed Programs",
                "Startup Programs"
            ]),
            ("🏆 Benchmark", [
                "Memory Read",
                "Memory Write",
                "Memory Copy",
                "Memory Latency",
                "CPU Queen",
                "CPU PhotoWorxx",
                "CPU ZLib",
                "CPU AES",
                "CPU SHA3",
                "FPU Julia",
                "FPU Mandel",
                "FPU SinJulia"
            ])
        ]

        bold_font = QFont("Segoe UI", 10, QFont.Bold)

        for cat_title, sub_items in structure:
            cat_item = QTreeWidgetItem(self, [cat_title])
            cat_item.setFont(0, bold_font)
            for sub in sub_items:
                child = QTreeWidgetItem(cat_item, [sub])
                cat_item.addChild(child)

        self.expandAll()

        # Select Computer -> Summary by default
        first_cat = self.topLevelItem(0)
        if first_cat and first_cat.childCount() > 0:
            self.setCurrentItem(first_cat.child(0))
