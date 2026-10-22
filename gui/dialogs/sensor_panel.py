"""
XUiDa64 - Floating Desktop OSD Sensor Panel Widget
Frameless, draggable, always-on-top HUD displaying live hardware metrics on desktop or during gaming.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QApplication
)
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QColor, QFont
from core.sensors import Sensors

class DesktopSensorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Frameless, Always on Top, Tool window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(220, 260)

        self._drag_pos = QPoint()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Container Frame
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(20, 26, 36, 0.95);
                border: 1px solid #2a364a;
                border-radius: 10px;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial;
            }
        """)
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # Header Bar (Drag handle)
        header = QHBoxLayout()
        title = QLabel("XUiDa SENSOR OSD")
        title.setStyleSheet("font-size: 11px; font-weight: bold; color: #58a6ff; letter-spacing: 1px;")
        header.addWidget(title)
        header.addStretch()

        close_btn = QPushButton("×")
        close_btn.setFixedSize(18, 18)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #8b949e;
                font-size: 14px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #f85149;
            }
        """)
        close_btn.clicked.connect(self.close)
        header.addWidget(close_btn)
        layout.addLayout(header)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #30363d; max-height: 1px;")
        layout.addWidget(line)

        # Sensor Metric Rows
        def create_row(label):
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 11px; color: #8b949e;")
            val = QLabel("--")
            val.setStyleSheet("font-size: 12px; font-weight: bold; color: #ffffff;")
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            layout.addLayout(row)
            return val

        self.val_cpu_temp = create_row("CPU Temp:")
        self.val_gpu_temp = create_row("GPU Temp:")
        self.val_cpu_load = create_row("CPU Load:")
        self.val_ram_load = create_row("RAM Load:")
        self.val_gpu_fan = create_row("GPU Fan:")
        self.val_net_down = create_row("Net Down:")
        self.val_net_up = create_row("Net Up:")

        main_layout.addWidget(self.container)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(1000)

        self.update_telemetry()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def update_telemetry(self):
        sensors = Sensors.get_all_sensors()

        # Temps
        for item in sensors.get("Temperatures", []):
            if item.get("Category") == "CPU":
                t = item.get("Value", 0)
                color = "#3fb950" if t < 65 else ("#d29922" if t < 80 else "#f85149")
                self.val_cpu_temp.setText(f"{t} °C")
                self.val_cpu_temp.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {color};")
            elif item.get("Category") == "GPU":
                t = item.get("Value", 0)
                color = "#3fb950" if t < 65 else ("#d29922" if t < 80 else "#f85149")
                self.val_gpu_temp.setText(f"{t} °C")
                self.val_gpu_temp.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {color};")

        # Fans
        for item in sensors.get("Fans", []):
            self.val_gpu_fan.setText(f"{item.get('Value')}%")

        # Usage
        for item in sensors.get("Usage", []):
            s_name = item.get("Sensor", "")
            val = item.get("Value", 0)
            if "CPU Total" in s_name:
                self.val_cpu_load.setText(f"{val}%")
            elif "Memory Utilization" in s_name:
                self.val_ram_load.setText(f"{val}%")
            elif "Download" in s_name:
                self.val_net_down.setText(f"{val} KB/s")
            elif "Upload" in s_name:
                self.val_net_up.setText(f"{val} KB/s")
