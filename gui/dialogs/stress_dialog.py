"""
XUiDa64 - System Stability Test & Stress Testing Dialog
Features real-time pyqtgraph telemetry charts, multi-threaded stress engine, thermal throttling alerts, and multi-language support.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton,
    QFrame, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QFont
import pyqtgraph as pg

from core.i18n import I18N, _t
from benchmarks.stress_test import StressTestEngine

class StressTestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_t("stress_title"))
        self.resize(880, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #0d1117;
                color: #c9d1d9;
            }
            QCheckBox {
                color: #c9d1d9;
                font-size: 13px;
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QFrame#statusBanner {
                border-radius: 6px;
                padding: 8px;
            }
        """)

        self.engine = StressTestEngine()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # 1. Throttling Status Banner
        self.banner = QFrame()
        self.banner.setObjectName("statusBanner")
        self.banner.setStyleSheet("background-color: #1f6feb; border: 1px solid #388bfd; border-radius: 6px; padding: 6px;")
        b_layout = QHBoxLayout(self.banner)
        b_layout.setContentsMargins(12, 6, 12, 6)

        self.status_lbl = QLabel(_t("stress_status_ready"))
        self.status_lbl.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
        b_layout.addWidget(self.status_lbl)

        b_layout.addStretch()

        self.elapsed_lbl = QLabel(_t("stress_time_elapsed", time="00:00:00"))
        self.elapsed_lbl.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
        b_layout.addWidget(self.elapsed_lbl)

        layout.addWidget(self.banner)

        # 2. Stress Option Checkboxes
        opts_box = QHBoxLayout()
        opts_box.setSpacing(14)
        self.chk_cpu = QCheckBox(_t("stress_chk_cpu"))
        self.chk_cpu.setChecked(True)
        self.chk_fpu = QCheckBox(_t("stress_chk_fpu"))
        self.chk_fpu.setChecked(True)
        self.chk_cache = QCheckBox(_t("stress_chk_cache"))
        self.chk_cache.setChecked(True)
        self.chk_memory = QCheckBox(_t("stress_chk_mem"))
        self.chk_memory.setChecked(True)
        self.chk_gpu = QCheckBox(_t("stress_chk_gpu"))
        self.chk_gpu.setChecked(False)

        opts_box.addWidget(self.chk_cpu)
        opts_box.addWidget(self.chk_fpu)
        opts_box.addWidget(self.chk_cache)
        opts_box.addWidget(self.chk_memory)
        opts_box.addWidget(self.chk_gpu)
        opts_box.addStretch()
        layout.addLayout(opts_box)

        # 3. Real-Time Graphs (pyqtgraph)
        pg.setConfigOption('background', '#161b22')
        pg.setConfigOption('foreground', '#8b949e')

        self.plot_temp = pg.PlotWidget(title="Hardware Temperatures (°C)")
        self.plot_temp.showGrid(x=True, y=True, alpha=0.3)
        self.plot_temp.setYRange(20, 110)
        self.plot_temp.addLegend(offset=(10, 10))

        self.curve_cpu_temp = self.plot_temp.plot(pen=pg.mkPen(color='#f1e05a', width=2), name="CPU Temperature")
        self.curve_gpu_temp = self.plot_temp.plot(pen=pg.mkPen(color='#58a6ff', width=2), name="GPU Temperature")
        
        # Throttling limit line (95°C)
        limit_pen = pg.mkPen(color='#da3633', width=1, style=Qt.DashLine)
        self.limit_line = pg.InfiniteLine(pos=95, angle=0, pen=limit_pen, label="Throttling Limit (95°C)")
        self.plot_temp.addItem(self.limit_line)

        layout.addWidget(self.plot_temp)

        self.plot_usage = pg.PlotWidget(title="CPU Utilization (%)")
        self.plot_usage.showGrid(x=True, y=True, alpha=0.3)
        self.plot_usage.setYRange(0, 105)
        self.curve_usage = self.plot_usage.plot(pen=pg.mkPen(color='#3fb950', width=2), fillLevel=0, brush=(63, 185, 80, 50))
        layout.addWidget(self.plot_usage)

        # 4. Bottom Controls Bar
        bottom_bar = QHBoxLayout()

        self.start_btn = QPushButton(_t("stress_start"))
        self.start_btn.clicked.connect(self.start_test)
        bottom_bar.addWidget(self.start_btn)

        self.stop_btn = QPushButton(_t("stress_stop"))
        self.stop_btn.setObjectName("dangerBtn")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_test)
        bottom_bar.addWidget(self.stop_btn)

        self.clear_btn = QPushButton(_t("stress_clear"))
        self.clear_btn.setObjectName("secondaryBtn")
        self.clear_btn.clicked.connect(self.clear_data)
        bottom_bar.addWidget(self.clear_btn)

        bottom_bar.addStretch()

        self.cur_stats_lbl = QLabel("CPU: -- °C | GPU: -- °C | Load: -- %")
        self.cur_stats_lbl.setStyleSheet("font-weight: bold; color: #58a6ff;")
        bottom_bar.addWidget(self.cur_stats_lbl)

        close_btn = QPushButton(_t("stress_close"))
        close_btn.setObjectName("secondaryBtn")
        close_btn.clicked.connect(self.close)
        bottom_bar.addWidget(close_btn)

        layout.addLayout(bottom_bar)

        # Telemetry Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)

    def start_test(self):
        self.engine.start(
            stress_cpu=self.chk_cpu.isChecked(),
            stress_fpu=self.chk_fpu.isChecked(),
            stress_cache=self.chk_cache.isChecked(),
            stress_memory=self.chk_memory.isChecked(),
            stress_gpu=self.chk_gpu.isChecked()
        )
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.chk_cpu.setEnabled(False)
        self.chk_fpu.setEnabled(False)
        self.chk_cache.setEnabled(False)
        self.chk_memory.setEnabled(False)
        self.chk_gpu.setEnabled(False)

        self.status_lbl.setText(_t("stress_status_running"))
        self.banner.setStyleSheet("background-color: #238636; border: 1px solid #3fb950; border-radius: 6px; padding: 6px;")
        self.timer.start(1000)

    def stop_test(self):
        self.engine.stop()
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.chk_cpu.setEnabled(True)
        self.chk_fpu.setEnabled(True)
        self.chk_cache.setEnabled(True)
        self.chk_memory.setEnabled(True)
        self.chk_gpu.setEnabled(True)

        self.status_lbl.setText(_t("stress_status_stopped"))
        self.banner.setStyleSheet("background-color: #30363d; border: 1px solid #8b949e; border-radius: 6px; padding: 6px;")

    def clear_data(self):
        for k in self.engine.history:
            self.engine.history[k].clear()
        self.curve_cpu_temp.setData([], [])
        self.curve_gpu_temp.setData([], [])
        self.curve_usage.setData([], [])
        self.elapsed_lbl.setText(_t("stress_time_elapsed", time="00:00:00"))

    def update_telemetry(self):
        telem = self.engine.update_telemetry()
        self.elapsed_lbl.setText(_t("stress_time_elapsed", time=telem['elapsed']))
        self.cur_stats_lbl.setText(
            f"CPU: {telem['cpu_temp']:.1f} °C | GPU: {telem['gpu_temp']:.1f} °C | Load: {telem['cpu_usage']:.1f} %"
        )

        hist = self.engine.history
        if hist["timestamps"]:
            self.curve_cpu_temp.setData(hist["timestamps"], hist["cpu_temp"])
            self.curve_gpu_temp.setData(hist["timestamps"], hist["gpu_temp"])
            self.curve_usage.setData(hist["timestamps"], hist["cpu_usage"])

        if telem["throttling"]:
            self.status_lbl.setText(_t("stress_throttling"))
            self.banner.setStyleSheet("background-color: #da3633; border: 1px solid #f85149; border-radius: 6px; padding: 6px;")

    def closeEvent(self, event):
        if self.engine.is_running():
            self.stop_test()
        event.accept()
