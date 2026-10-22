"""
XUiDa64 - Disk Benchmark Dialog
Interactive storage speed diagnostics with live progress and real-world metrics.
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from core.i18n import _t
from benchmarks.disk_bench import DiskBenchmark

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DiskBenchWorker(QThread):
    progress_sig = pyqtSignal(str, int, float)
    finished_sig = pyqtSignal(dict)
    error_sig = pyqtSignal(str)

    def __init__(self, target_dir, file_size_mb):
        super().__init__()
        self.target_dir = target_dir
        self.file_size_mb = file_size_mb
        self.is_running = True

    def run(self):
        try:
            def cb(stage, pct, speed):
                if self.is_running:
                    self.progress_sig.emit(stage, pct, speed)

            res = DiskBenchmark.run_benchmark(self.target_dir, self.file_size_mb, progress_callback=cb)
            if self.is_running:
                self.finished_sig.emit(res)
        except Exception as e:
            self.error_sig.emit(str(e))

    def stop(self):
        self.is_running = False

class DiskBenchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("XUiDa64 - Disk Benchmark (Storage Speed Test)")
        self.resize(760, 580)
        self.setMinimumSize(680, 500)

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
                font-size: 13px;
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

        # Header Title
        title_box = QHBoxLayout()
        title_lbl = QLabel("💾 Тестирование скорости накопителей (Disk Benchmark)")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #58a6ff;")
        title_box.addWidget(title_lbl)
        title_box.addStretch()
        layout.addLayout(title_box)

        # Controls Bar (Drive, Size, Start)
        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet("background-color: #19212e; border: 1px solid #2a364a; border-radius: 8px; padding: 10px;")
        ctrl_layout = QHBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(10, 8, 10, 8)
        ctrl_layout.setSpacing(12)

        ctrl_layout.addWidget(QLabel("Накопитель:"))
        self.drive_combo = QComboBox()
        self.drives = DiskBenchmark.get_drives()
        for d in self.drives:
            self.drive_combo.addItem(f"{d['mountpoint']} [{d['fstype'].upper()}] - {d['free_gb']} ГБ свободно", d["mountpoint"])
        ctrl_layout.addWidget(self.drive_combo, 3)

        ctrl_layout.addWidget(QLabel("Объем:"))
        self.size_combo = QComboBox()
        self.size_combo.addItem("128 МБ (Быстрый)", 128)
        self.size_combo.addItem("256 МБ (Стандартный)", 256)
        self.size_combo.addItem("512 МБ (Высокая точность)", 512)
        self.size_combo.addItem("1024 МБ (Стресс)", 1024)
        ctrl_layout.addWidget(self.size_combo, 2)

        self.start_btn = QPushButton("▶ Начать тест")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: #ffffff;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 18px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
        """)
        self.start_btn.clicked.connect(self.toggle_benchmark)
        ctrl_layout.addWidget(self.start_btn)

        layout.addWidget(ctrl_frame)

        # Live Progress & Speed readout
        meter_frame = QFrame()
        meter_frame.setStyleSheet("background-color: #161d27; border: 1px solid #2a364a; border-radius: 8px; padding: 12px;")
        m_layout = QVBoxLayout(meter_frame)
        m_layout.setSpacing(8)

        m_top = QHBoxLayout()
        self.status_lbl = QLabel("Готов к запуску теста")
        self.status_lbl.setStyleSheet("font-size: 13px; color: #8b949e;")
        self.speed_lbl = QLabel("0.0 MB/s")
        self.speed_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: #3fb950;")
        m_top.addWidget(self.status_lbl)
        m_top.addStretch()
        m_top.addWidget(self.speed_lbl)
        m_layout.addLayout(m_top)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setValue(0)
        m_layout.addWidget(self.progress_bar)

        layout.addWidget(meter_frame)

        # Results Table
        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(["Тип тестирования", "Результат", "Единица измерения"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)

        metrics = [
            ("Последовательная запись (Sequential Write)", "-", "МБ/с (MB/s)"),
            ("Последовательное чтение (Sequential Read)", "-", "МБ/с (MB/s)"),
            ("Случайное чтение 4K (Random 4K Read)", "-", "IOPS / МБ/с"),
            ("Случайная запись 4K (Random 4K Write)", "-", "IOPS / МБ/с"),
            ("Время доступа к сектору (Access Latency)", "-", "мс (ms)")
        ]
        for row, (name, val, unit) in enumerate(metrics):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            val_item = QTableWidgetItem(val)
            val_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, val_item)
            unit_item = QTableWidgetItem(unit)
            unit_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, unit_item)

        layout.addWidget(self.table)

        # Bottom buttons
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

    def toggle_benchmark(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            self.start_btn.setText("▶ Начать тест")
            self.start_btn.setStyleSheet("background-color: #238636; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 8px 18px;")
            self.status_lbl.setText("Тест остановлен пользователем")
            return

        target_drive = self.drive_combo.currentData()
        if not target_drive:
            QMessageBox.warning(self, "Ошибка", "Выберите диск для тестирования!")
            return

        file_size_mb = self.size_combo.currentData()

        self.start_btn.setText("⏹ Остановить")
        self.start_btn.setStyleSheet("background-color: #da3633; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 8px 18px;")
        self.status_lbl.setText("Выполняется инициализация буфера...")
        self.progress_bar.setValue(0)

        self.worker = DiskBenchWorker(target_drive, file_size_mb)
        self.worker.progress_sig.connect(self._on_progress)
        self.worker.finished_sig.connect(self._on_finished)
        self.worker.error_sig.connect(self._on_error)
        self.worker.start()

    def _on_progress(self, stage, pct, speed):
        self.status_lbl.setText(f"Этап: {stage}...")
        self.progress_bar.setValue(pct)
        if speed > 0:
            self.speed_lbl.setText(f"{speed:,.1f} MB/s")

    def _on_finished(self, results):
        self.start_btn.setText("▶ Начать тест")
        self.start_btn.setStyleSheet("background-color: #238636; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 8px 18px;")
        self.status_lbl.setText("✅ Тестирование успешно завершено!")
        self.progress_bar.setValue(100)

        seq_w = results.get("Seq Write", "-")
        seq_r = results.get("Seq Read", "-")
        rnd_r_iops = results.get("Rnd 4K Read (IOPS)", 0)
        rnd_r_mb = results.get("Rnd 4K Read (MB/s)", 0)
        rnd_w_iops = results.get("Rnd 4K Write (IOPS)", 0)
        rnd_w_mb = results.get("Rnd 4K Write (MB/s)", 0)
        latency = results.get("Access Latency (ms)", "-")

        self.table.item(0, 1).setText(f"{seq_w} MB/s")
        self.table.item(1, 1).setText(f"{seq_r} MB/s")
        self.table.item(2, 1).setText(f"{rnd_r_iops:,} IOPS ({rnd_r_mb} MB/s)")
        self.table.item(3, 1).setText(f"{rnd_w_iops:,} IOPS ({rnd_w_mb} MB/s)")
        self.table.item(4, 1).setText(f"{latency} ms")

        # Highlight top results
        for r in range(5):
            self.table.item(r, 1).setForeground(Qt.green)

    def _on_error(self, err_msg):
        self.start_btn.setText("▶ Начать тест")
        self.start_btn.setStyleSheet("background-color: #238636; color: #ffffff; font-weight: bold; border-radius: 6px; padding: 8px 18px;")
        self.status_lbl.setText("❌ Ошибка при выполнении теста")
        QMessageBox.critical(self, "Ошибка теста накопителя", f"Произошла ошибка: {err_msg}")

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(1000)
        event.accept()
