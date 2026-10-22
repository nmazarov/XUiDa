"""
XUiDa64 - Process Explorer & Task Manager View
Live process monitoring with CPU %, RAM MB, thread counts, multi-language support and management.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QHeaderView, QLabel, QMessageBox, QApplication
)
from PyQt5.QtCore import QTimer, Qt
import psutil
from core.i18n import I18N, _t
from core.software_info import SoftwareInfo

class ProcessView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Top Control Row
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(_t("proc_filter"))
        self.search_input.textChanged.connect(self._filter_rows)
        top_bar.addWidget(self.search_input)

        self.clear_btn = QPushButton("✕")
        self.clear_btn.setFixedWidth(28)
        self.clear_btn.setObjectName("secondaryBtn")
        self.clear_btn.clicked.connect(self.search_input.clear)
        top_bar.addWidget(self.clear_btn)

        self.proc_count_lbl = QLabel("")
        self.proc_count_lbl.setStyleSheet("color: #8b949e; font-size: 11px; padding: 2px 6px; background: #21262d; border-radius: 4px;")
        top_bar.addWidget(self.proc_count_lbl)

        self.refresh_btn = QPushButton(_t("proc_refresh"))
        self.refresh_btn.setObjectName("secondaryBtn")
        self.refresh_btn.clicked.connect(self.refresh_processes)
        top_bar.addWidget(self.refresh_btn)

        self.kill_btn = QPushButton(_t("proc_kill"))
        self.kill_btn.setObjectName("dangerBtn")
        self.kill_btn.clicked.connect(self.kill_selected)
        top_bar.addWidget(self.kill_btn)

        layout.addLayout(top_bar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            _t("col_pid"), _t("col_name"), _t("col_cpu_pct"), _t("col_mem_mb"),
            _t("col_threads"), _t("col_user"), _t("col_status")
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        I18N.register_listener(self.on_language_changed)
        self.refresh_processes()

    def on_language_changed(self, lang):
        self.search_input.setPlaceholderText(_t("proc_filter"))
        self.refresh_btn.setText(_t("proc_refresh"))
        self.kill_btn.setText(_t("proc_kill"))
        self.table.setHorizontalHeaderLabels([
            _t("col_pid"), _t("col_name"), _t("col_cpu_pct"), _t("col_mem_mb"),
            _t("col_threads"), _t("col_user"), _t("col_status")
        ])
        self._update_count_badge()

    def refresh_processes(self):
        procs = SoftwareInfo.get_processes()
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(procs))

        for row, p in enumerate(procs):
            self.table.setItem(row, 0, QTableWidgetItem(str(p["PID"])))
            self.table.setItem(row, 1, QTableWidgetItem(p["Name"]))
            self.table.setItem(row, 2, QTableWidgetItem(f"{p['CPU']:.1f}%"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{p['MemoryMB']:,.1f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(p["Threads"])))
            self.table.setItem(row, 5, QTableWidgetItem(p["User"]))
            self.table.setItem(row, 6, QTableWidgetItem(p["Status"]))

        self.table.setSortingEnabled(True)
        self._filter_rows(self.search_input.text())

    def _filter_rows(self, text):
        query = text.lower().strip()
        visible_count = 0
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 1)
            pid_item = self.table.item(row, 0)
            user_item = self.table.item(row, 5)
            match = (
                (name_item and query in name_item.text().lower()) or
                (pid_item and query in pid_item.text().lower()) or
                (user_item and query in user_item.text().lower())
            )
            self.table.setRowHidden(row, not match)
            if match:
                visible_count += 1
        self._update_count_badge(visible_count if query else self.table.rowCount())

    def _update_count_badge(self, count=None):
        if count is None:
            count = self.table.rowCount()
        self.proc_count_lbl.setText(_t("proc_count", count=count))

    def kill_selected(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "XUiDa64", "Please select a process to terminate.")
            return

        row = selected_rows[0].row()
        pid_text = self.table.item(row, 0).text()
        name_text = self.table.item(row, 1).text()

        confirm = QMessageBox.question(
            self, _t("proc_kill"),
            _t("proc_kill_confirm", name=name_text, pid=pid_text),
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                proc = psutil.Process(int(pid_text))
                proc.terminate()
                self.refresh_processes()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not end process: {e}")
