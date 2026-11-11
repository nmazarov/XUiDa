"""
XUiDa64 - In-Game & Desktop SensorPanel / OSD Hardware Overlay
Always-on-top, draggable, frameless gaming HUD with click-through mode,
opacity controls, snap-to-corner positioning, and live animated gauges.
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QProgressBar, QApplication
)
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QColor, QFont, QIcon
from core.sensors import Sensors
from core.i18n import _t

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DesktopSensorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Frameless, Always on Top, Tool window that stays above borderless games
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(270, 340)

        icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self._drag_pos = QPoint()
        self.click_through = False
        self.opacities = [0.95, 0.85, 0.70, 0.50]
        self.opacity_idx = 0
        self.snap_corners = ["top-right", "bottom-right", "top-left", "bottom-left"]
        self.snap_idx = 0

        self._init_ui()

        # Telemetry update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(1000)
        self.update_telemetry()

    def showEvent(self, event):
        super().showEvent(event)
        if not hasattr(self, "_initialized_pos") or not self._initialized_pos:
            self._initialized_pos = True
            screen = QApplication.primaryScreen().geometry()
            self.move(screen.width() - self.width() - 30, 40)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Container Frame
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame#hudContainer {
                background-color: rgba(11, 14, 20, 0.94);
                border: 1px solid #38bdf8;
                border-radius: 12px;
            }
            QLabel {
                color: #f8fafc;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', Arial;
            }
            QProgressBar {
                background-color: #151b26;
                border: 1px solid #222d3f;
                border-radius: 5px;
                text-align: center;
                color: transparent;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #38bdf8);
                border-radius: 4px;
            }
        """)
        self.container.setObjectName("hudContainer")

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        # 1. Header Bar (Drag handle, Snap, Opacity, Click-through, Close)
        header = QHBoxLayout()
        header.setSpacing(6)

        title = QLabel("⚡ XUiDa64 HUD")
        title.setStyleSheet("font-size: 11px; font-weight: bold; color: #00d2ff; letter-spacing: 1px;")
        header.addWidget(title)
        header.addStretch()

        # Snap button
        self.snap_btn = QPushButton("🎯")
        self.snap_btn.setToolTip("Закрепить в углу экрана")
        self.snap_btn.setFixedSize(22, 20)
        self.snap_btn.setStyleSheet("background: #192231; color: #00d2ff; border: 1px solid #28364a; border-radius: 4px; font-size: 11px;")
        self.snap_btn.clicked.connect(self.snap_next_corner)
        header.addWidget(self.snap_btn)

        # Opacity button
        self.op_btn = QPushButton("🌓")
        self.op_btn.setToolTip("Прозрачность HUD (95%, 85%, 70%, 50%)")
        self.op_btn.setFixedSize(22, 20)
        self.op_btn.setStyleSheet("background: #192231; color: #cbd5e1; border: 1px solid #28364a; border-radius: 4px; font-size: 11px;")
        self.op_btn.clicked.connect(self.cycle_opacity)
        header.addWidget(self.op_btn)

        # Click-through toggle (Gaming mode)
        self.lock_btn = QPushButton("🎮")
        self.lock_btn.setToolTip("Режим игры (клик насквозь). Для снятия нажмите F9 в приложении.")
        self.lock_btn.setFixedSize(22, 20)
        self.lock_btn.setStyleSheet("background: #192231; color: #10b981; border: 1px solid #28364a; border-radius: 4px; font-size: 11px;")
        self.lock_btn.clicked.connect(self.toggle_click_through)
        header.addWidget(self.lock_btn)

        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #8b949e;
                font-size: 15px;
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

        # Separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #212d3e; max-height: 1px;")
        layout.addWidget(sep)

        # 2. Metric Rows with Mini Bars
        def create_metric_row(icon_label, default_text="--"):
            row_v = QVBoxLayout()
            row_v.setSpacing(2)

            top_h = QHBoxLayout()
            lbl = QLabel(icon_label)
            lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #cbd5e1;")
            val = QLabel(default_text)
            val.setStyleSheet("font-size: 11px; font-weight: bold; color: #ffffff;")
            top_h.addWidget(lbl)
            top_h.addStretch()
            top_h.addWidget(val)
            row_v.addLayout(top_h)

            bar = QProgressBar()
            bar.setFixedHeight(6)
            bar.setTextVisible(False)
            bar.setRange(0, 100)
            bar.setValue(0)
            row_v.addWidget(bar)

            layout.addLayout(row_v)
            return val, bar

        # CPU
        self.lbl_cpu, self.bar_cpu = create_metric_row("⚡ ЦП (Процессор)")
        # GPU
        self.lbl_gpu, self.bar_gpu = create_metric_row("🎮 GPU (Видеокарта)")
        # RAM
        self.lbl_ram, self.bar_ram = create_metric_row("🧠 ОЗУ (Память)")

        # Secondary compact rows without bars
        def create_compact_row(label):
            h = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 11px; color: #94a3b8;")
            val = QLabel("--")
            val.setStyleSheet("font-size: 11px; font-weight: bold; color: #ffffff;")
            h.addWidget(lbl)
            h.addStretch()
            h.addWidget(val)
            layout.addLayout(h)
            return val

        self.lbl_gpu_fan = create_compact_row("❄️ Вентиляторы GPU:")
        self.lbl_power = create_compact_row("⚡ Энергопотребление:")
        self.lbl_network = create_compact_row("🌐 Сеть (↓/↑):")

        # Bottom hint label
        self.hint_lbl = QLabel("F9: Показать/Скрыть  |  Drag: Перемещение")
        self.hint_lbl.setStyleSheet("font-size: 9px; color: #64748b; margin-top: 4px;")
        self.hint_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.hint_lbl)

        main_layout.addWidget(self.container)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def cycle_opacity(self):
        self.opacity_idx = (self.opacity_idx + 1) % len(self.opacities)
        op = self.opacities[self.opacity_idx]
        self.setWindowOpacity(op)
        pct = int(op * 100)
        self.hint_lbl.setText(f"Прозрачность: {pct}%")

    def snap_next_corner(self):
        screen = QApplication.primaryScreen().geometry()
        margin = 25
        w, h = self.width(), self.height()
        corner = self.snap_corners[self.snap_idx]
        self.snap_idx = (self.snap_idx + 1) % len(self.snap_corners)

        if corner == "top-right":
            self.move(screen.width() - w - margin, margin)
        elif corner == "bottom-right":
            self.move(screen.width() - w - margin, screen.height() - h - margin - 40)
        elif corner == "top-left":
            self.move(margin, margin)
        elif corner == "bottom-left":
            self.move(margin, screen.height() - h - margin - 40)

    def toggle_click_through(self):
        self.click_through = not self.click_through
        if self.click_through:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self.lock_btn.setStyleSheet("background: #238636; color: #ffffff; border: 1px solid #3fb950; border-radius: 4px; font-size: 11px;")
            self.hint_lbl.setText("🎮 Режим игры: клик насквозь активен (F9 для выхода)")
        else:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            self.lock_btn.setStyleSheet("background: #192231; color: #10b981; border: 1px solid #28364a; border-radius: 4px; font-size: 11px;")
            self.hint_lbl.setText("F9: Показать/Скрыть  |  Drag: Перемещение")

    def update_telemetry(self):
        try:
            sensors = Sensors.get_all_sensors()

            # 1. CPU
            cpu_temp = None
            for item in sensors.get("Temperatures", []):
                if item.get("Category") == "CPU":
                    cpu_temp = item.get("Value", 0)
                    break

            cpu_usage = 0
            for item in sensors.get("Usage", []):
                if "CPU Total" in item.get("Sensor", ""):
                    cpu_usage = int(item.get("Value", 0))
                    break

            if cpu_temp:
                t_col = "#3fb950" if cpu_temp < 65 else ("#f59e0b" if cpu_temp < 80 else "#ef4444")
                self.lbl_cpu.setText(f"<span style='color:{t_col};'>{cpu_temp:.0f}°C</span>  |  {cpu_usage}%")
            else:
                self.lbl_cpu.setText(f"{cpu_usage}%")
            self.bar_cpu.setValue(cpu_usage)

            # 2. GPU
            gpu_temp = None
            gpu_power = None
            gpu_fan = None
            for item in sensors.get("Temperatures", []):
                if item.get("Category") == "GPU":
                    gpu_temp = item.get("Value", 0)
                    break
            for item in sensors.get("Powers", []):
                if item.get("Category") == "GPU":
                    gpu_power = item.get("Value", 0)
                    break
            for item in sensors.get("Fans", []):
                if item.get("Category") == "GPU":
                    gpu_fan = item.get("Value", 0)
                    break

            # GPU Usage
            gpu_usage = 0
            for item in sensors.get("Usage", []):
                if "GPU" in item.get("Sensor", ""):
                    gpu_usage = int(item.get("Value", 0))
                    break

            if gpu_temp:
                g_col = "#3fb950" if gpu_temp < 65 else ("#f59e0b" if gpu_temp < 80 else "#ef4444")
                self.lbl_gpu.setText(f"<span style='color:{g_col};'>{gpu_temp:.0f}°C</span>  |  {gpu_usage}%")
            else:
                self.lbl_gpu.setText(f"{gpu_usage}%")
            self.bar_gpu.setValue(gpu_usage)

            # 3. RAM
            ram_pct = 0
            for item in sensors.get("Usage", []):
                if "Memory Utilization" in item.get("Sensor", ""):
                    ram_pct = int(item.get("Value", 0))
                    break
            self.lbl_ram.setText(f"{ram_pct}%")
            self.bar_ram.setValue(ram_pct)

            # 4. Fans
            if gpu_fan is not None:
                self.lbl_gpu_fan.setText(f"{gpu_fan}%")
            else:
                self.lbl_gpu_fan.setText("Автоматически")

            # 5. Power
            if gpu_power and gpu_power > 0:
                self.lbl_power.setText(f"{gpu_power:.1f} Вт")
            else:
                self.lbl_power.setText("Норма (AC)")

            # 6. Network
            net_down = 0
            net_up = 0
            for item in sensors.get("Usage", []):
                s = item.get("Sensor", "")
                v = item.get("Value", 0)
                if "Download" in s:
                    net_down = v
                elif "Upload" in s:
                    net_up = v
            self.lbl_network.setText(f"↓ {net_down} KB/s  ↑ {net_up} KB/s")

        except Exception:
            pass
