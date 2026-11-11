"""
XUiDa64 - Real-Time Sensor Dashboard View
Crafted according to Benji Taylor / Stageshow Design Engineering principles:
- Live animated circular arc gauges with continuous OutCubic easing.
- Restrained, elevated card hierarchy (#131824 -> #1a2232).
- Segmented pill filter bar with active highlight states.
- High-contrast, non-glare table data rows with crisp typography.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QButtonGroup
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QFont
from core.i18n import I18N, _t, _prop
from core.sensors import Sensors
from gui.widgets.animated_widgets import AnimatedDialGauge, LivePulseDot

class SensorMetricCard(QFrame):
    """Elevated telemetry card containing an animated dial gauge and status indicators."""
    def __init__(self, title, unit="%", min_val=0, max_val=100, accent_hex="#38bdf8", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #141b26;
                border: 1px solid #222d3f;
                border-radius: 10px;
            }
            QFrame:hover {
                background-color: #1a2232;
                border: 1px solid #38bdf8;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        # Gauge in the center
        self.gauge = AnimatedDialGauge(title=title, unit=unit, min_val=min_val, max_val=max_val, parent=self)
        layout.addWidget(self.gauge, 0, Qt.AlignCenter)

    def set_title(self, title):
        self.gauge.title = title
        self.gauge.update()

    def set_value(self, val):
        self.gauge.set_value(val)

class SensorView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_filter = "All"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Top Control Row
        top_bar = QHBoxLayout()
        self.header_lbl = QLabel(_t("sensor_header"))
        self.header_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #38bdf8; letter-spacing: 0.5px;")
        top_bar.addWidget(self.header_lbl)
        top_bar.addStretch()

        self.pause_btn = QPushButton(_t("sensor_pause"))
        self.pause_btn.setObjectName("secondaryBtn")
        self.pause_btn.clicked.connect(self.toggle_updates)
        top_bar.addWidget(self.pause_btn)

        layout.addLayout(top_bar)

        # Dashboard Metric Cards with Animated Gauges
        cards_layout = QGridLayout()
        cards_layout.setSpacing(12)

        is_ru = (I18N.get_language() == "ru")
        self.card_cpu_temp = SensorMetricCard("Температура ЦП" if is_ru else "CPU Temp", "°C", 20, 105, "#38bdf8")
        self.card_gpu_temp = SensorMetricCard("Температура GPU" if is_ru else "GPU Temp", "°C", 20, 100, "#10b981")
        self.card_cpu_load = SensorMetricCard("Загрузка ЦП" if is_ru else "CPU Load", "%", 0, 100, "#38bdf8")
        self.card_gpu_load = SensorMetricCard("Загрузка GPU" if is_ru else "GPU Load", "%", 0, 100, "#10b981")
        self.card_ram_load = SensorMetricCard("ОЗУ Занято" if is_ru else "RAM Usage", "%", 0, 100, "#f59e0b")
        self.card_gpu_fan = SensorMetricCard("Вентиляторы GPU" if is_ru else "GPU Fans", "%", 0, 100, "#a855f7")

        cards_layout.addWidget(self.card_cpu_temp, 0, 0)
        cards_layout.addWidget(self.card_gpu_temp, 0, 1)
        cards_layout.addWidget(self.card_cpu_load, 0, 2)
        cards_layout.addWidget(self.card_gpu_load, 1, 0)
        cards_layout.addWidget(self.card_ram_load, 1, 1)
        cards_layout.addWidget(self.card_gpu_fan, 1, 2)

        layout.addLayout(cards_layout)

        # Category Filter Bar - Modern Segmented Ribbon
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: #121824;
                border: 1px solid #222d3f;
                border-radius: 8px;
                padding: 2px;
            }
        """)
        filter_bar = QHBoxLayout(filter_frame)
        filter_bar.setContentsMargins(4, 4, 4, 4)
        filter_bar.setSpacing(4)

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
        layout.addWidget(filter_frame)

        # Detailed Sensor Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([_t("col_sensor"), _t("col_value"), _t("col_unit"), _t("col_category")])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.setAlternatingRowColors(False)
        layout.addWidget(self.table)

        # Telemetry Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sensors)
        self.timer.start(1200)

        I18N.register_listener(self.on_language_changed)
        self.update_sensors()

    def on_language_changed(self, lang):
        is_ru = (lang == "ru")
        self.card_cpu_temp.set_title("Температура ЦП" if is_ru else "CPU Temp")
        self.card_gpu_temp.set_title("Температура GPU" if is_ru else "GPU Temp")
        self.card_cpu_load.set_title("Загрузка ЦП" if is_ru else "CPU Load")
        self.card_gpu_load.set_title("Загрузка GPU" if is_ru else "GPU Load")
        self.card_ram_load.set_title("ОЗУ Занято" if is_ru else "RAM Usage")
        self.card_gpu_fan.set_title("Вентиляторы GPU" if is_ru else "GPU Fans")

        self.header_lbl.setText(_t("sensor_header"))
        self.pause_btn.setText(_t("sensor_pause") if self.timer.isActive() else _t("sensor_resume"))
        self.btn_all.setText(_t("sensor_all"))
        self.btn_temp.setText(_t("sensor_temp"))
        self.btn_fan.setText(_t("sensor_fan"))
        self.btn_pwr.setText(_t("sensor_power"))
        self.btn_clk.setText(_t("sensor_clock"))
        self.btn_usg.setText(_t("sensor_usage"))
        self.table.setHorizontalHeaderLabels([_t("col_sensor"), _t("col_value"), _t("col_unit"), _t("col_category")])
        self.update_sensors()

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

        # Update Cards with Animated Easing Gauges
        cpu_t = None
        gpu_t = None
        for item in sensors.get("Temperatures", []):
            if item.get("Category") == "CPU" and cpu_t is None:
                cpu_t = item.get("Value")
            elif item.get("Category") == "GPU" and gpu_t is None:
                gpu_t = item.get("Value")

        if cpu_t is not None:
            self.card_cpu_temp.set_value(cpu_t)
        if gpu_t is not None:
            self.card_gpu_temp.set_value(gpu_t)

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
            name = item.get("Sensor", "")
            if "GPU" in name or "Видеокарта" in name:
                self.card_gpu_fan.set_value(item.get("Value", 0))
                break
        else:
            if sensors.get("Fans"):
                self.card_gpu_fan.set_value(sensors.get("Fans")[0].get("Value", 0))

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

        bold_font = QFont("Segoe UI Variable Text", 9, QFont.Bold)
        normal_font = QFont("Segoe UI Variable Text", 9, QFont.Normal)

        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.table.setRowHeight(row, 28)

            # Sensor name (High contrast crisp text, translated)
            raw_sensor = item.get("Sensor", "")
            it0 = QTableWidgetItem(_prop(raw_sensor))
            it0.setFont(normal_font)
            it0.setForeground(QColor("#f8fafc"))

            # Value (Electric cyan, bold)
            it1 = QTableWidgetItem(str(item.get("Value", "")))
            it1.setForeground(QColor("#38bdf8"))
            it1.setFont(bold_font)

            # Unit (Clean gray)
            it2 = QTableWidgetItem(item.get("Unit", ""))
            it2.setFont(normal_font)
            it2.setForeground(QColor("#94a3b8"))

            # Category (Soft cyan pill, translated)
            raw_cat = item.get("Category", "")
            it3 = QTableWidgetItem(_prop(raw_cat))
            it3.setFont(normal_font)
            it3.setForeground(QColor("#93c5fd"))

            self.table.setItem(row, 0, it0)
            self.table.setItem(row, 1, it1)
            self.table.setItem(row, 2, it2)
            self.table.setItem(row, 3, it3)
