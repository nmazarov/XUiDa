"""
XUiDa64 - Real-Time Sensor Dashboard View
Displays live telemetry with gauges, sensor cards and real-time updates.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QFont
from core.sensors import Sensors

class MetricCard(QFrame):
    def __init__(self, title, unit="", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("color: #8b949e; font-size: 11px; font-weight: bold; text-transform: uppercase;")
        layout.addWidget(self.title_lbl)

        self.value_lbl = QLabel("--")
        self.value_lbl.setStyleSheet("color: #58a6ff; font-size: 22px; font-weight: bold;")
        layout.addWidget(self.value_lbl)

        self.unit = unit

    def set_value(self, val, color=None):
        unit_str = f" {self.unit}" if self.unit else ""
        if isinstance(val, (int, float)):
            self.value_lbl.setText(f"{val}{unit_str}")
        else:
            self.value_lbl.setText(f"{val}")

        if color:
            self.value_lbl.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold;")

class SensorView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Top Control Row
        top_bar = QHBoxLayout()
        header_lbl = QLabel("Hardware Monitor & Sensor Status")
        header_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #58a6ff;")
        top_bar.addWidget(header_lbl)
        top_bar.addStretch()

        self.pause_btn = QPushButton("⏸ Pause Updates")
        self.pause_btn.setObjectName("secondaryBtn")
        self.pause_btn.clicked.connect(self.toggle_updates)
        top_bar.addWidget(self.pause_btn)

        layout.addLayout(top_bar)

        # Dashboard Metric Cards
        cards_layout = QGridLayout()
        cards_layout.setSpacing(10)

        self.card_cpu_temp = MetricCard("CPU Temperature", "°C")
        self.card_gpu_temp = MetricCard("GPU Temperature", "°C")
        self.card_cpu_load = MetricCard("CPU Utilization", "%")
        self.card_gpu_load = MetricCard("GPU Load", "%")
        self.card_ram_load = MetricCard("RAM Utilization", "%")
        self.card_gpu_fan = MetricCard("GPU Fan Speed", "%")

        cards_layout.addWidget(self.card_cpu_temp, 0, 0)
        cards_layout.addWidget(self.card_gpu_temp, 0, 1)
        cards_layout.addWidget(self.card_cpu_load, 0, 2)
        cards_layout.addWidget(self.card_gpu_load, 1, 0)
        cards_layout.addWidget(self.card_ram_load, 1, 1)
        cards_layout.addWidget(self.card_gpu_fan, 1, 2)

        layout.addLayout(cards_layout)

        # Detailed Sensor Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Sensor", "Value", "Unit", "Category"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sensors)
        self.timer.start(1200)

        self.update_sensors()

    def toggle_updates(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_btn.setText("▶ Resume Updates")
        else:
            self.timer.start(1200)
            self.pause_btn.setText("⏸ Pause Updates")

    def update_sensors(self):
        sensors = Sensors.get_all_sensors()

        # Update Cards
        cpu_t = None
        gpu_t = None
        for item in sensors.get("Temperatures", []):
            if item.get("Category") == "CPU" and cpu_t is None:
                cpu_t = item.get("Value")
            elif item.get("Category") == "GPU" and gpu_t is None:
                gpu_t = item.get("Value")

        if cpu_t is not None:
            color = "#3fb950" if cpu_t < 65 else ("#d29922" if cpu_t < 80 else "#f85149")
            self.card_cpu_temp.set_value(cpu_t, color)
        if gpu_t is not None:
            color = "#3fb950" if gpu_t < 65 else ("#d29922" if gpu_t < 80 else "#f85149")
            self.card_gpu_temp.set_value(gpu_t, color)

        for item in sensors.get("Usage", []):
            sensor_name = item.get("Sensor", "")
            val = item.get("Value", 0)
            if "CPU Total" in sensor_name:
                self.card_cpu_load.set_value(val)
            elif "Memory Utilization" in sensor_name:
                self.card_ram_load.set_value(val)
            elif "GPU" in sensor_name and "Load" in sensor_name:
                self.card_gpu_load.set_value(val)

        for item in sensors.get("Fans", []):
            self.card_gpu_fan.set_value(item.get("Value", 0))

        # Update Table
        all_items = (
            sensors.get("Temperatures", []) +
            sensors.get("Fans", []) +
            sensors.get("Powers", []) +
            sensors.get("Clocks", []) +
            sensors.get("Usage", [])
        )

        self.table.setRowCount(len(all_items))
        for row, item in enumerate(all_items):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("Sensor", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.get("Value", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("Unit", "")))
            self.table.setItem(row, 3, QTableWidgetItem(item.get("Category", "")))
