"""
XUiDa64 - Dynamic Property & Table View Widget
Displays hardware properties with search, copy, and export capabilities.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QHeaderView, QMenu, QApplication, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

class PropertyTableView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Top Bar: Search & Action Buttons
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(6, 6, 6, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Filter properties (type to search)...")
        self.search_input.textChanged.connect(self._filter_rows)
        top_bar.addWidget(self.search_input)

        self.copy_btn = QPushButton("📋 Copy All")
        self.copy_btn.setObjectName("secondaryBtn")
        self.copy_btn.clicked.connect(self.copy_all)
        top_bar.addWidget(self.copy_btn)

        layout.addLayout(top_bar)

        # Table Widget
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

    def set_data(self, data_dict_or_list, headers=None):
        self.table.setSortingEnabled(False)
        self.search_input.clear()

        if headers:
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            for i in range(len(headers)):
                if i == 0 or i == len(headers) - 1:
                    self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
                else:
                    self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        # If data is a list of dicts (multi-column)
        if isinstance(data_dict_or_list, list) and data_dict_or_list and isinstance(data_dict_or_list[0], dict):
            keys = list(data_dict_or_list[0].keys())
            if not headers:
                self.table.setColumnCount(len(keys))
                self.table.setHorizontalHeaderLabels(keys)
                for i in range(len(keys)):
                    self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

            self.table.setRowCount(len(data_dict_or_list))
            for row_idx, item in enumerate(data_dict_or_list):
                for col_idx, k in enumerate(keys):
                    val = str(item.get(k, ""))
                    cell = QTableWidgetItem(val)
                    self.table.setItem(row_idx, col_idx, cell)

        # If data is a dictionary (Field -> Value)
        elif isinstance(data_dict_or_list, dict):
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["Field", "Value"])
            self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

            rows = []
            for k, v in data_dict_or_list.items():
                if isinstance(v, dict):
                    # Category group header
                    rows.append((f"[{k.upper()}]", "", True))
                    for sub_k, sub_v in v.items():
                        rows.append((f"    {sub_k}", str(sub_v), False))
                elif isinstance(v, list):
                    rows.append((f"[{k.upper()}]", "", True))
                    for item in v:
                        if isinstance(item, dict):
                            line = ", ".join([f"{ik}: {iv}" for ik, iv in item.items()])
                            rows.append(("    •", line, False))
                        else:
                            rows.append(("    •", str(item), False))
                else:
                    rows.append((str(k), str(v), False))

            self.table.setRowCount(len(rows))
            for row_idx, (field, value, is_header) in enumerate(rows):
                f_item = QTableWidgetItem(field)
                v_item = QTableWidgetItem(value)
                if is_header:
                    f_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                    f_item.setForeground(QColor("#58a6ff"))
                    f_item.setBackground(QColor("#1f2937"))
                    v_item.setBackground(QColor("#1f2937"))
                self.table.setItem(row_idx, 0, f_item)
                self.table.setItem(row_idx, 1, v_item)

        self.table.setSortingEnabled(True)

    def _filter_rows(self, text):
        query = text.lower().strip()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item:
            return
        menu = QMenu(self)
        copy_val_action = menu.addAction("Copy Value")
        copy_row_action = menu.addAction("Copy Row")
        copy_all_action = menu.addAction("Copy Entire Table")

        action = menu.exec_(self.table.viewport().mapToGlobal(pos))
        if action == copy_val_action:
            QApplication.clipboard().setText(item.text())
        elif action == copy_row_action:
            row = item.row()
            row_vals = [self.table.item(row, col).text() if self.table.item(row, col) else "" 
                        for col in range(self.table.columnCount())]
            QApplication.clipboard().setText("\t".join(row_vals))
        elif action == copy_all_action:
            self.copy_all()

    def copy_all(self):
        text = []
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        text.append("\t".join(headers))
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                vals = [self.table.item(row, col).text() if self.table.item(row, col) else "" 
                        for col in range(self.table.columnCount())]
                text.append("\t".join(vals))
        QApplication.clipboard().setText("\n".join(text))
