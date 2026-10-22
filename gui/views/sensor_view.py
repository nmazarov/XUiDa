"""
XUiDa64 - Real-Time Sensor Dashboard View
Displays live telemetry with gauges, sensor cards, category filters and multi-language support.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QButtonGroup
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QFont
from core.i18n import I18N, _t
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
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("color: #8b949e; font-size: 11px; font-weight: bold; text-transform: uppercase;")
        layout.addWidget(self.title_lbl)

        self.value_lbl = QLabel("--")
        self.value_lbl.setStyleSheet("color: #58a6ff; font-size: 22px; font-weight: bold;")
        layout.addWidget(self.value_lbl)

        self.unit = unit

    def set_title(self, title):
        self.title_lbl.setText(title)

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
        self.current_filter = "All"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Top Control Row
        top_bar = QHBoxLayout()
        self.header_lbl = QLabel(_t("sensor_header"))
        self.header_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #58a6ff;")
        top_bar.addWidget(self.header_lbl)
        top_bar.addStretch()

        self.pause_btn = QPushButton(_t("sensor_pause"))
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

        # Category Filter Bar
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(6)

        self.btn_all = QPushButton(_t("sensor_all"))
        self.btn_temp = QPushButton(_t("sensor_temp"))
        self.btn_fan = QPushButton(_t("sensor_fan"))
        self.btn_pwr = QPushButton(_t("sensor_power"))
        self.btn_clk = QPushButton(_t("sensor_clock"))
        self.btn_usg = QPushButton(_t("sensor_usage"))

        self.filter_buttons = [
            (self.btn_all, "All"),
            (self.btn_temp, "Temperatures"),
            (self.btn_fan, "Fans"),
            (self.btn_pwr, "Powers"),
            (self.btn_clk, "Clocks"),
            (self.btn_usg, "Usage")
        ]

        for btn, cat in self.filter_buttons:
            btn.setCheckable(True)
            btn.setObjectName("secondaryBtn")
            btn.clicked.connect(lambda checked, c=cat: self.set_filter(c))
            filter_bar.addWidget(btn)

        self.btn_all.setChecked(True)
        filter_bar.addStretch()
        layout.addLayout(filter_bar)

        # Detailed Sensor Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([_t("col_sensor"), _t("col_value"), _t("col_unit"), _t("col_category")])
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

        I18N.register_listener(self.on_language_changed)
        self.update_sensors()

    def on_language_changed(self, lang):
        self.header_lbl.setText(_t("sensor_header"))
        self.pause_btn.setText(_t("sensor_pause") if self.timer.isActive() else _t("sensor_resume"))
        self.btn_all.setText(_t("sensor_all"))
        self.btn_temp.setText(_t("sensor_temp"))
        self.btn_fan.setText(_t("sensor_fan"))
        self.btn_pwr.setText(_t("sensor_power"))
        self.btn_clk.setText(_t("sensor_clock"))
        self.btn_usg.setText(_t("sensor_usage"))
        self.table.setHorizontalHeaderLabels([_t("col_sensor"), _t("col_value"), _t("col_unit"), _t("col_category")])

    def set_filter(self, category):
        self.current_filter = category
        for btn, cat in self.filter_buttons:
            btn.setChecked(cat == category)
        self.update_sensors()

    def toggle_updates(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_btn.setText(_t("sensor_resume"))
        else:
            self.timer.start(1200)
            self.pause_btn.setText(_t("sensor_pause"))

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

        # Filter items for table
        if self.current_filter == "All":
            items = (
                sensors.get("Temperatures", []) +
                sensors.get("Fans", []) +
                sensors.get("Powers", []) +
                sensors.get("Clocks", []) +
                sensors.get("Usage", [])
            )
        else:
            items = sensors.get(self.current_filter, [])

        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("Sensor", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.get("Value", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("Unit", "")))
            self.table.setItem(row, 3, QTableWidgetItem(item.get("Category", "")))
