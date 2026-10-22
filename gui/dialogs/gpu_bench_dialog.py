"""
XUiDa64 - GPGPU Compute Benchmark Dialog
Interactive window comparing GPU compute and memory bandwidth performance.
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from core.gpu_info import GPUInfo
from benchmarks.gpu_bench import GPUBenchmark
from gui.widgets.animated_widgets import AnimatedPushButton

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GPUBenchWorker(QThread):
    progress_sig = pyqtSignal(str, int)
    finished_sig = pyqtSignal(dict)
    error_sig = pyqtSignal(str)

    def __init__(self, gpu_idx=0):
        super().__init__()
        self.gpu_idx = gpu_idx

    def run(self):
        try:
            def cb(stage, pct):
                self.progress_sig.emit(stage, pct)

            res = GPUBenchmark.run_benchmarks(self.gpu_idx, progress_callback=cb)
            self.finished_sig.emit(res)
        except Exception as e:
            self.error_sig.emit(str(e))

class GPUBenchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("XUiDa64 - GPGPU Benchmark (GPU Compute Suite)")
        self.resize(700, 520)
        self.setMinimumSize(600, 440)

        icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet("""
            QDialog {
                background-color: #141a24;
                color: #ffffff;
            }
            QLabel {
                font-family: 'Segoe UI', Arial;
                color: #ffffff;
            }
            QComboBox {
                background-color: #19212e;
                color: #ffffff;
                border: 1px solid #2a364a;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QTableWidget {
                background-color: #141a24;
                color: #ffffff;
                border: 1px solid #2a364a;
                border-radius: 6px;
                gridline-color: #2a364a;
            }
            QHeaderView::section {
                background-color: #19212e;
                color: #58a6ff;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #2a364a;
            }
            QProgressBar {
                background-color: #19212e;
                border: 1px solid #2a364a;
                border-radius: 6px;
                text-align: center;
                color: #ffffff;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #238636;
                border-radius: 5px;
            }
        """)

        self.worker = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        # Title
        title_box = QHBoxLayout()
        title_lbl = QLabel("🎮 Бенчмарк вычислений видеокарты (GPGPU Benchmark)")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #58a6ff;")
        title_box.addWidget(title_lbl)
        layout.addLayout(title_box)

        # Top Control Frame
        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet("background-color: #19212e; border: 1px solid #2a364a; border-radius: 8px; padding: 10px;")
        ctrl_layout = QHBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(10, 8, 10, 8)
        ctrl_layout.setSpacing(12)

        ctrl_layout.addWidget(QLabel("Видеоадаптер:"))
        self.gpu_combo = QComboBox()
        self.gpus = GPUBenchmark.get_gpu_devices()
        for i, g in enumerate(self.gpus):
            vram = g.get("VRAM_MB", "N/A")
            self.gpu_combo.addItem(f"{g.get('Name', 'GPU')} ({vram} MB VRAM)", i)
        ctrl_layout.addWidget(self.gpu_combo, 2)

        self.start_btn = AnimatedPushButton("▶ Начать тест GPU", is_primary=True)
        self.start_btn.setFixedSize(160, 36)
        self.start_btn.clicked.connect(self.start_bench)
        ctrl_layout.addWidget(self.start_btn)

        layout.addWidget(ctrl_frame)

        # Progress bar
        meter_frame = QFrame()
        meter_frame.setStyleSheet("background-color: #161d27; border: 1px solid #2a364a; border-radius: 8px; padding: 10px;")
        m_layout = QVBoxLayout(meter_frame)
        m_layout.setSpacing(6)

        self.status_lbl = QLabel("Готов к запуску вычислений")
        self.status_lbl.setStyleSheet("font-size: 13px; color: #8b949e;")
        m_layout.addWidget(self.status_lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(16)
        self.progress_bar.setValue(0)
        m_layout.addWidget(self.progress_bar)

        layout.addWidget(meter_frame)

        # Results Table
        self.table = QTableWidget(4, 3)
        self.table.setHorizontalHeaderLabels(["Тип вычислений", "Текущий результат", "Эталонный уровень"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)

        rows = [
            ("Single-Precision FP32 FLOPS (Одинарная точность)", "-", "450 - 15,000 GFLOPS"),
            ("Double-Precision FP64 FLOPS (Двойная точность)", "-", "120 - 2,500 GFLOPS"),
            ("Integer Int32 Compute (Целочисленные операции)", "-", "300 - 8,000 GIOPS"),
            ("Memory Bandwidth (Пропускная способность памяти)", "-", "18 - 85 GB/s")
        ]
        for row, (name, val, ref) in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            val_item = QTableWidgetItem(val)
            val_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, val_item)
            ref_item = QTableWidgetItem(ref)
            ref_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, ref_item)

        layout.addWidget(self.table)

        # Bottom Close button
        btn_box = QHBoxLayout()
        btn_box.addStretch()
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #19212e;
                color: #ffffff;
                border: 1px solid #2a364a;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #222d3e;
            }
        """)
        close_btn.clicked.connect(self.close)
        btn_box.addWidget(close_btn)
        layout.addLayout(btn_box)

    def start_bench(self):
        if self.worker and self.worker.isRunning():
            return

        self.start_btn.setEnabled(False)
        self.status_lbl.setText("Выполняются вычисления...")
        self.progress_bar.setValue(5)

        self.worker = GPUBenchWorker(self.gpu_combo.currentIndex())
        self.worker.progress_sig.connect(self._on_progress)
        self.worker.finished_sig.connect(self._on_finished)
        self.worker.error_sig.connect(self._on_error)
        self.worker.start()

    def _on_progress(self, stage, pct):
        self.status_lbl.setText(f"Тестирование: {stage}...")
        self.progress_bar.setValue(pct)

    def _on_finished(self, results):
        self.start_btn.setEnabled(True)
        self.status_lbl.setText("✅ Бенчмарк GPU успешно завершен!")
        self.progress_bar.setValue(100)

        fp32 = results.get("FP32_GFLOPS", "-")
        fp64 = results.get("FP64_GFLOPS", "-")
        int32 = results.get("Int32_GIOPS", "-")
        mem = results.get("Memory_GBs", "-")

        self.table.item(0, 1).setText(f"{fp32} GFLOPS")
        self.table.item(1, 1).setText(f"{fp64} GFLOPS")
        self.table.item(2, 1).setText(f"{int32} GIOPS")
        self.table.item(3, 1).setText(f"{mem} GB/s")

        for r in range(4):
            self.table.item(r, 1).setForeground(Qt.green)

    def _on_error(self, err_msg):
        self.start_btn.setEnabled(True)
        self.status_lbl.setText("❌ Ошибка при выполнении вычислений")
        QMessageBox.critical(self, "Ошибка GPU", f"Ошибка: {err_msg}")
