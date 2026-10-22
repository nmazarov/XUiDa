"""
XUiDa64 - Benchmark Suite & Comparison Bar Chart View
Recreates AIDA64's comparative ranking charts with reference CPU database and multi-language support.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QProgressBar, QScrollArea, QFrame, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush

from core.i18n import I18N, _t, _prop
from benchmarks.reference_data import REFERENCE_SCORES
from benchmarks.memory_bench import MemoryBenchmark
from benchmarks.cpu_bench import CPUBenchmarks
from benchmarks.fpu_bench import FPUBenchmarks
from core.cpuid import CPUID

class BenchmarkWorker(QThread):
    progress = pyqtSignal(int)
    finished_score = pyqtSignal(float)

    def __init__(self, bench_name):
        super().__init__()
        self.bench_name = bench_name

    def run(self):
        score = 0.0
        cb = lambda p: self.progress.emit(p)

        if self.bench_name == "Memory Read":
            score = MemoryBenchmark.run_read(cb)
        elif self.bench_name == "Memory Write":
            score = MemoryBenchmark.run_write(cb)
        elif self.bench_name == "Memory Copy":
            score = MemoryBenchmark.run_copy(cb)
        elif self.bench_name == "Memory Latency":
            score = MemoryBenchmark.run_latency(cb)
        elif self.bench_name == "CPU Queen":
            score = CPUBenchmarks.run_queen(cb)
        elif self.bench_name == "CPU PhotoWorxx":
            score = CPUBenchmarks.run_photoworxx(cb)
        elif self.bench_name == "CPU ZLib":
            score = CPUBenchmarks.run_zlib(cb)
        elif self.bench_name == "CPU AES":
            score = CPUBenchmarks.run_aes(cb)
        elif self.bench_name == "CPU SHA3":
            score = CPUBenchmarks.run_sha3(cb)
        elif self.bench_name == "FPU Julia":
            score = FPUBenchmarks.run_julia(cb)
        elif self.bench_name == "FPU Mandel":
            score = FPUBenchmarks.run_mandel(cb)
        elif self.bench_name == "FPU SinJulia":
            score = FPUBenchmarks.run_sinjulia(cb)

        self.finished_score.emit(score)

class BarChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []  # [(name, score, is_user)]
        self.unit = "MB/s"
        self.higher_is_better = True
        self.setMinimumHeight(450)

    def set_data(self, items, unit="MB/s", higher_is_better=True):
        self.items = items
        self.unit = unit
        self.higher_is_better = higher_is_better
        self.setMinimumHeight(max(len(items) * 32 + 40, 450))
        self.update()

    def paintEvent(self, event):
        if not self.items:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Background
        painter.fillRect(0, 0, w, h, QColor("#141a24"))

        max_score = max(score for _, score, _ in self.items) or 1.0
        bar_x_start = 280
        bar_max_w = max(w - bar_x_start - 130, 100)
        row_height = 30
        y = 20

        font = QFont("Segoe UI", 9)
        bold_font = QFont("Segoe UI", 9, QFont.Bold)

        for name, score, is_user in self.items:
            ratio = score / max_score
            bar_w = int(bar_max_w * ratio)

            # Draw Label (High contrast)
            painter.setFont(bold_font if is_user else font)
            painter.setPen(QColor("#58a6ff" if is_user else "#ffffff"))
            display_name = f"★ {name}" if is_user else name
            painter.drawText(10, y + 16, bar_x_start - 20, 20, Qt.AlignLeft | Qt.AlignVCenter, display_name)

            # Draw Bar
            bar_rect_y = y + 3
            bar_rect_h = 18
            if is_user:
                painter.fillRect(bar_x_start, bar_rect_y, max(bar_w, 4), bar_rect_h, QBrush(QColor("#238636")))
                painter.setPen(QPen(QColor("#3fb950"), 1))
                painter.drawRect(bar_x_start, bar_rect_y, max(bar_w, 4), bar_rect_h)
            else:
                painter.fillRect(bar_x_start, bar_rect_y, max(bar_w, 4), bar_rect_h, QBrush(QColor("#19212e")))
                painter.setPen(QPen(QColor("#2a364a"), 1))
                painter.drawRect(bar_x_start, bar_rect_y, max(bar_w, 4), bar_rect_h)

            # Draw Score Text (High contrast)
            score_str = f"{score:,.1f} {self.unit}" if isinstance(score, float) else f"{score:,} {self.unit}"
            painter.setPen(QColor("#3fb950" if is_user else "#58a6ff"))
            painter.drawText(bar_x_start + bar_w + 10, y + 16, 120, 20, Qt.AlignLeft | Qt.AlignVCenter, score_str)

            y += row_height

class BenchmarkView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Top Control Bar
        control_bar = QHBoxLayout()
        control_bar.setSpacing(12)

        self.lbl_select = QLabel(_t("bench_select"))
        self.lbl_select.setStyleSheet("font-weight: bold; color: #58a6ff;")
        control_bar.addWidget(self.lbl_select)

        self.combo = QComboBox()
        self._populate_combo()
        self.combo.currentIndexChanged.connect(self.on_benchmark_changed)
        control_bar.addWidget(self.combo)

        self.start_btn = QPushButton(_t("bench_run"))
        self.start_btn.clicked.connect(self.start_benchmark)
        control_bar.addWidget(self.start_btn)

        control_bar.addStretch()

        self.user_score_lbl = QLabel(_t("bench_not_run"))
        self.user_score_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #3fb950;")
        control_bar.addWidget(self.user_score_lbl)

        layout.addLayout(control_bar)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(6)
        self.progress.setTextVisible(False)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Scroll Area for Chart
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self.chart = BarChartWidget()
        scroll.setWidget(self.chart)
        layout.addWidget(scroll)

        self.user_cpu_name = CPUID.get_info().get("brand", "This Computer")
        self.cached_scores = {}
        self.worker = None

        I18N.register_listener(self.on_language_changed)
        self.on_benchmark_changed()

    def _populate_combo(self):
        curr_key = self.combo.currentData() if self.combo.count() > 0 else "Memory Read"
        self.combo.blockSignals(True)
        self.combo.clear()
        selected_idx = 0
        for i, key in enumerate(REFERENCE_SCORES.keys()):
            self.combo.addItem(_prop(key), key)
            if key == curr_key:
                selected_idx = i
        self.combo.setCurrentIndex(selected_idx)
        self.combo.blockSignals(False)

    def on_language_changed(self, lang):
        self.lbl_select.setText(_t("bench_select"))
        self.start_btn.setText(_t("bench_run"))
        self._populate_combo()
        self.on_benchmark_changed()

    def on_benchmark_changed(self):
        bench_name = self.combo.currentData() or self.combo.currentText()
        bench_meta = REFERENCE_SCORES.get(bench_name, {})
        unit = bench_meta.get("unit", "")
        higher_better = bench_meta.get("higher_is_better", True)

        ref_list = list(bench_meta.get("scores", []))
        items = [(name, val, False) for name, val in ref_list]

        if bench_name in self.cached_scores:
            user_val = self.cached_scores[bench_name]
            label = f"{self.user_cpu_name} {_t('bench_this_pc')}"
            items.append((label, user_val, True))
            self.user_score_lbl.setText(_t("bench_result", val=f"{user_val:,.1f} {unit}"))
        else:
            self.user_score_lbl.setText(_t("bench_not_run"))

        # Sort items
        items.sort(key=lambda x: x[1], reverse=higher_better)
        self.chart.set_data(items, unit, higher_better)

    def start_benchmark(self):
        if self.worker and self.worker.isRunning():
            return
        bench_name = self.combo.currentData() or self.combo.currentText()
        self.start_btn.setEnabled(False)
        self.progress.setValue(10)
        self.user_score_lbl.setText(_t("bench_running"))

        self.worker = BenchmarkWorker(bench_name)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished_score.connect(self.on_benchmark_finished)
        self.worker.start()

    def on_benchmark_finished(self, score):
        bench_name = self.combo.currentData() or self.combo.currentText()
        self.cached_scores[bench_name] = score
        self.start_btn.setEnabled(True)
        self.progress.setValue(100)
        self.on_benchmark_changed()
