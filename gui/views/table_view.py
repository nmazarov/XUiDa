"""
XUiDa64 - Dynamic Property & Table View Widget
Displays hardware properties with multi-language support, search, copy, and uniform high-contrast styling.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QHeaderView, QMenu, QApplication, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from core.i18n import I18N, _t

class PropertyTableView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Top Bar: Search, Count Badge & Action Buttons
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(_t("filter_placeholder"))
        self.search_input.textChanged.connect(self._filter_rows)
        top_bar.addWidget(self.search_input)

        self.clear_btn = QPushButton("✕")
        self.clear_btn.setFixedWidth(28)
        self.clear_btn.setObjectName("secondaryBtn")
        self.clear_btn.clicked.connect(self.search_input.clear)
        top_bar.addWidget(self.clear_btn)

        self.count_badge = QLabel("")
        self.count_badge.setStyleSheet("color: #8b949e; font-size: 11px; padding: 2px 6px; background: #19212e; border-radius: 4px;")
        top_bar.addWidget(self.count_badge)

        self.copy_btn = QPushButton(_t("copy_all"))
        self.copy_btn.setObjectName("secondaryBtn")
        self.copy_btn.clicked.connect(self.copy_all)
        top_bar.addWidget(self.copy_btn)

        layout.addLayout(top_bar)

        # Table Widget - UNIFORM BACKGROUND, NO ALTERNATING WHITE ROWS
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([_t("col_field"), _t("col_value")])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.table)

        I18N.register_listener(self.on_language_changed)

    def on_language_changed(self, lang):
        self.search_input.setPlaceholderText(_t("filter_placeholder"))
        self.copy_btn.setText(_t("copy_all"))
        if self.table.columnCount() == 2:
            self.table.setHorizontalHeaderLabels([_t("col_field"), _t("col_value")])
        self._update_count_badge()

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

        # Multi-column list of dicts
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
                    cell.setForeground(QColor("#ffffff"))
                    self.table.setItem(row_idx, col_idx, cell)

        # Key-Value Dictionary
        elif isinstance(data_dict_or_list, dict):
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels([_t("col_field"), _t("col_value")])
            self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

            rows = []
            for k, v in data_dict_or_list.items():
                if isinstance(v, dict):
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
                    f_item.setBackground(QColor("#19212e"))
                    v_item.setBackground(QColor("#19212e"))
                else:
                    f_item.setForeground(QColor("#9ca3af"))
                    v_item.setForeground(QColor("#ffffff"))
                self.table.setItem(row_idx, 0, f_item)
                self.table.setItem(row_idx, 1, v_item)

        self.table.setSortingEnabled(True)
        self._update_count_badge()

    def _filter_rows(self, text):
        query = text.lower().strip()
        visible_count = 0
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)
            if match:
                visible_count += 1
        self._update_count_badge(visible_count if query else self.table.rowCount())

    def _update_count_badge(self, count=None):
        if count is None:
            count = self.table.rowCount()
        self.count_badge.setText(_t("items_count", count=count))

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item:
            return
        menu = QMenu(self)
        copy_val_action = menu.addAction(_t("copy_value"))
        copy_row_action = menu.addAction(_t("copy_row"))
        copy_all_action = menu.addAction(_t("copy_table"))

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
