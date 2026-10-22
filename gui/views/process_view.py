"""
XUiDa64 - Process Explorer & Task Manager View
Live process monitoring with CPU %, RAM MB, thread counts and management.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QHeaderView, QLabel, QMessageBox, QApplication
)
from PyQt5.QtCore import QTimer, Qt
import psutil
from core.software_info import SoftwareInfo

class ProcessView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Top Control Row
        top_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Filter processes (e.g. chrome, python)...")
        self.search_input.textChanged.connect(self._filter_rows)
        top_bar.addWidget(self.search_input)

        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setObjectName("secondaryBtn")
        self.refresh_btn.clicked.connect(self.refresh_processes)
        top_bar.addWidget(self.refresh_btn)

        self.kill_btn = QPushButton("⏹ End Process")
        self.kill_btn.setObjectName("dangerBtn")
        self.kill_btn.clicked.connect(self.kill_selected)
        top_bar.addWidget(self.kill_btn)

        layout.addLayout(top_bar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["PID", "Process Name", "CPU %", "Memory (MB)", "Threads", "User", "Status"])
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

        self.refresh_processes()

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

    def kill_selected(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "No Process Selected", "Please select a process to terminate.")
            return

        row = selected_rows[0].row()
        pid_text = self.table.item(row, 0).text()
        name_text = self.table.item(row, 1).text()

        confirm = QMessageBox.question(
            self, "Terminate Process",
            f"Are you sure you want to kill process {name_text} (PID {pid_text})?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                proc = psutil.Process(int(pid_text))
                proc.terminate()
                self.refresh_processes()
            except Exception as e:
                QMessageBox.warning(self, "Termination Failed", f"Could not end process: {e}")
