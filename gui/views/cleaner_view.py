"""
XUiDa64 - System Cleaner & Disk Optimizer View
Interactive CCleaner-style utility providing safe scanning, selection,
and 1-click cleanup of Windows temp files, browser caches, crash dumps, and Recycle Bin.
"""

import psutil
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QCheckBox,
    QTextEdit, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QIcon

from core.cleaner import SystemCleaner
from core.i18n import I18N, _t, _prop
from gui.widgets.animated_widgets import AnimatedPushButton

class ScanWorker(QThread):
    progress_sig = pyqtSignal(int, str)
    item_scanned_sig = pyqtSignal(dict)
    finished_sig = pyqtSignal(list, int, int)

    def __init__(self, categories):
        super().__init__()
        self.categories = categories

    def run(self):
        scanned_results = []
        total_size = 0
        total_files = 0
        total_cats = len(self.categories)

        for idx, cat in enumerate(self.categories):
            pct = int((idx / max(total_cats, 1)) * 100)
            self.progress_sig.emit(pct, f"Сканирование: {cat.get('name')}...")
            res = SystemCleaner.scan_category(cat)
            res["enabled"] = cat.get("default", True)
            scanned_results.append(res)
            total_size += res["size_bytes"]
            total_files += res["files_count"]
            self.item_scanned_sig.emit(res)

        self.progress_sig.emit(100, "Анализ системы завершен")
        self.finished_sig.emit(scanned_results, total_size, total_files)

class CleanWorker(QThread):
    progress_sig = pyqtSignal(int, str)
    log_sig = pyqtSignal(str)
    finished_sig = pyqtSignal(int, int)

    def __init__(self, selected_categories):
        super().__init__()
        self.selected_categories = selected_categories

    def run(self):
        total_freed = 0
        total_deleted = 0
        total_cats = len(self.selected_categories)

        for idx, cat in enumerate(self.selected_categories):
            pct = int((idx / max(total_cats, 1)) * 100)
            self.progress_sig.emit(pct, f"Очистка: {cat.get('name')}...")
            freed, deleted, failed = SystemCleaner.clean_category(
                cat, log_callback=lambda msg: self.log_sig.emit(msg)
            )
            total_freed += freed
            total_deleted += deleted

        self.progress_sig.emit(100, "Очистка успешно завершена!")
        self.finished_sig.emit(total_freed, total_deleted)

class CleanerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.categories_data = []
        self.scan_worker = None
        self.clean_worker = None
        self._init_ui()
        I18N.register_listener(self.on_language_changed)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # 1. Top Summary Banner & Quick Stat Chips
        top_frame = QFrame()
        top_frame.setStyleSheet("""
            QFrame {
                background-color: #161e2b;
                border: 1px solid #2a364a;
                border-radius: 8px;
            }
        """)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(16, 12, 16, 12)
        top_layout.setSpacing(14)

        # Title Info
        title_box = QVBoxLayout()
        title_box.setSpacing(3)
        self.title_lbl = QLabel("🧹 Очистка системы и оптимизация дисков")
        self.title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #58a6ff;")
        self.subtitle_lbl = QLabel("Безопасное удаление временных файлов, кэша браузеров, дампов сбоев и корзины")
        self.subtitle_lbl.setStyleSheet("font-size: 12px; color: #94a3b8;")
        title_box.addWidget(self.title_lbl)
        title_box.addWidget(self.subtitle_lbl)
        top_layout.addLayout(title_box, 4)

        # Metric Chips (Junk size, Files count, Free space on C:)
        chips_layout = QHBoxLayout()
        chips_layout.setSpacing(10)

        self.chip_junk = self._create_stat_chip("🗑️ Мусор", "--", "#f85149")
        self.chip_files = self._create_stat_chip("📁 Файлов", "--", "#f59e0b")

        # Free space on C:
        free_c = "--"
        try:
            free_c = f"{psutil.disk_usage('C:').free / (1024**3):.1f} ГБ"
        except Exception:
            pass
        self.chip_free = self._create_stat_chip("💾 Свободно C:", free_c, "#10b981")

        chips_layout.addWidget(self.chip_junk)
        chips_layout.addWidget(self.chip_files)
        chips_layout.addWidget(self.chip_free)
        top_layout.addLayout(chips_layout, 5)

        layout.addWidget(top_frame)

        # 2. Controls & Actions Bar
        ctrl_bar = QHBoxLayout()
        ctrl_bar.setSpacing(10)

        self.scan_btn = AnimatedPushButton("🔍 Анализ системы", is_primary=True)
        self.scan_btn.setFixedHeight(34)
        self.scan_btn.setMinimumWidth(160)
        self.scan_btn.clicked.connect(self.start_scan)
        ctrl_bar.addWidget(self.scan_btn)

        self.clean_btn = AnimatedPushButton("🧹 Очистить мусор", is_primary=False)
        self.clean_btn.setFixedHeight(34)
        self.clean_btn.setMinimumWidth(160)
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #da3633;
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #f85149;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #f85149;
            }
        """)
        self.clean_btn.setEnabled(False)
        self.clean_btn.clicked.connect(self.start_cleaning)
        ctrl_bar.addWidget(self.clean_btn)

        self.toggle_all_btn = QPushButton("☑ Снять все")
        self.toggle_all_btn.setFixedHeight(34)
        self.toggle_all_btn.setObjectName("secondaryBtn")
        self.toggle_all_btn.clicked.connect(self.toggle_all_selection)
        ctrl_bar.addWidget(self.toggle_all_btn)

        ctrl_bar.addStretch()

        self.status_lbl = QLabel("Нажмите «Анализ системы» для оценки занимаемого места")
        self.status_lbl.setStyleSheet("color: #cbd5e1; font-size: 12px; font-weight: bold;")
        ctrl_bar.addWidget(self.status_lbl)

        layout.addLayout(ctrl_bar)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # 3. Categories Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Категория очистки", "Описание / Расположение", "Файлов", "Занимаемый объем"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.table.setColumnWidth(0, 360)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setAlternatingRowColors(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #141a24;
                border: 1px solid #2a364a;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 6px 10px;
                border-bottom: 1px solid #1c2635;
            }
        """)
        layout.addWidget(self.table, 3)

        # 4. Real-time Operation Log
        log_frame = QFrame()
        log_frame.setStyleSheet("""
            QFrame {
                background-color: #121822;
                border: 1px solid #243042;
                border-radius: 6px;
            }
        """)
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(10, 8, 10, 8)
        log_layout.setSpacing(6)

        log_hdr = QHBoxLayout()
        log_title = QLabel("📜 Журнал операций очистки:")
        log_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #94a3b8;")
        log_hdr.addWidget(log_title)
        log_hdr.addStretch()

        self.clear_log_btn = QPushButton("Очистить журнал")
        self.clear_log_btn.setFixedHeight(22)
        self.clear_log_btn.setStyleSheet("font-size: 10px; padding: 2px 8px; background: #19212e; border: 1px solid #2a364a; border-radius: 4px; color: #8b949e;")
        self.clear_log_btn.clicked.connect(lambda: self.log_text.clear())
        log_hdr.addWidget(self.clear_log_btn)
        log_layout.addLayout(log_hdr)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFixedHeight(90)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #0d121a;
                color: #a5d6ff;
                font-family: 'Consolas', monospace;
                font-size: 11px;
                border: 1px solid #1e2837;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_frame, 1)

        # Populate initial list of categories
        self.init_categories_table()

    def _create_stat_chip(self, label, val, accent_hex):
        chip = QFrame()
        chip.setStyleSheet(f"""
            QFrame {{
                background-color: #1a2536;
                border: 1px solid #2d3e56;
                border-left: 4px solid {accent_hex};
                border-radius: 6px;
                padding: 6px 12px;
                min-width: 120px;
                min-height: 52px;
            }}
        """)
        c_layout = QVBoxLayout(chip)
        c_layout.setContentsMargins(8, 6, 8, 6)
        c_layout.setSpacing(4)

        lbl = QLabel(label)
        lbl.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {accent_hex}; background: transparent;")
        val_lbl = QLabel(val)
        val_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #ffffff; background: transparent;")
        val_lbl.setObjectName("chip_val")

        c_layout.addWidget(lbl)
        c_layout.addWidget(val_lbl)
        return chip

    def init_categories_table(self):
        raw_cats = SystemCleaner.get_cleanable_categories()
        self.categories_data = []
        for cat in raw_cats:
            cat_copy = dict(cat)
            cat_copy["size_bytes"] = 0
            cat_copy["files_count"] = 0
            cat_copy["enabled"] = cat.get("default", True)
            self.categories_data.append(cat_copy)
        self._render_table()

    def _render_table(self):
        self.table.setRowCount(len(self.categories_data))
        bold_font = QFont("Segoe UI", 9, QFont.Bold)

        for row, cat in enumerate(self.categories_data):
            self.table.setRowHeight(row, 36)

            # Column 0: Centered container widget preventing vertical font clipping
            cell_widget = QWidget()
            cell_widget.setStyleSheet("background: transparent;")
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(10, 0, 8, 0)
            cell_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

            chk = QCheckBox(f"{cat.get('icon', '📁')}  {cat.get('name')}")
            chk.setChecked(cat.get("enabled", True))
            chk.setStyleSheet("""
                QCheckBox {
                    color: #ffffff;
                    font-weight: 600;
                    font-size: 12px;
                    spacing: 8px;
                    background: transparent;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 1px solid #38bdf8;
                    border-radius: 3px;
                    background: #172131;
                }
                QCheckBox::indicator:hover {
                    border: 1px solid #00d2ff;
                    background: #1e2c40;
                }
                QCheckBox::indicator:checked {
                    background: #1f6feb;
                    border: 1px solid #38bdf8;
                }
            """)
            chk.stateChanged.connect(lambda state, r=row: self._on_checkbox_changed(r, state))
            cell_layout.addWidget(chk)
            self.table.setCellWidget(row, 0, cell_widget)

            # Column 1: Description / Path
            desc_item = QTableWidgetItem(cat.get("desc", ""))
            desc_item.setForeground(QColor("#94a3b8"))
            desc_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.table.setItem(row, 1, desc_item)

            # Column 2: Files count
            fc = cat.get("files_count", 0)
            fc_str = f"{fc:,} шт." if fc > 0 else "--"
            fc_item = QTableWidgetItem(fc_str)
            fc_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            fc_item.setForeground(QColor("#cbd5e1"))
            self.table.setItem(row, 2, fc_item)

            # Column 3: Size
            sz = cat.get("size_bytes", 0)
            sz_str = SystemCleaner.format_size(sz) if sz > 0 else "--"
            sz_item = QTableWidgetItem(sz_str)
            sz_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            sz_item.setFont(bold_font)
            sz_item.setForeground(QColor("#38bdf8" if sz > 0 else "#64748b"))
            self.table.setItem(row, 3, sz_item)

    def _on_checkbox_changed(self, row, state):
        if row < len(self.categories_data):
            self.categories_data[row]["enabled"] = (state == Qt.Checked)
            self._update_selected_summary()

    def toggle_all_selection(self):
        all_checked = all(c.get("enabled", False) for c in self.categories_data)
        new_state = not all_checked
        self.toggle_all_btn.setText("☑ Выбрать все" if new_state else "☐ Снять все")
        for r in range(self.table.rowCount()):
            cell_w = self.table.cellWidget(r, 0)
            if cell_w:
                chk = cell_w.findChild(QCheckBox)
                if chk:
                    chk.setChecked(new_state)
            if r < len(self.categories_data):
                self.categories_data[r]["enabled"] = new_state
        self._update_selected_summary()

    def _update_selected_summary(self):
        selected = [c for c in self.categories_data if c.get("enabled", False)]
        sel_size = sum(c.get("size_bytes", 0) for c in selected)
        sel_files = sum(c.get("files_count", 0) for c in selected)

        self.chip_junk.findChild(QLabel, "chip_val").setText(SystemCleaner.format_size(sel_size))
        self.chip_files.findChild(QLabel, "chip_val").setText(f"{sel_files:,}")
        self.clean_btn.setEnabled(sel_size > 0 or sel_files > 0)

    def start_scan(self):
        if self.scan_worker and self.scan_worker.isRunning():
            return

        self.scan_btn.setEnabled(False)
        self.clean_btn.setEnabled(False)
        self.progress_bar.setValue(5)
        self.status_lbl.setText("Идет анализ мусорных файлов...")
        self.log_text.append("🔍 Начало анализа системы...")

        raw_cats = SystemCleaner.get_cleanable_categories()
        self.scan_worker = ScanWorker(raw_cats)
        self.scan_worker.progress_sig.connect(self._on_scan_progress)
        self.scan_worker.item_scanned_sig.connect(self._on_item_scanned)
        self.scan_worker.finished_sig.connect(self._on_scan_finished)
        self.scan_worker.start()

    def _on_scan_progress(self, pct, status_text):
        self.progress_bar.setValue(pct)
        self.status_lbl.setText(status_text)

    def _on_item_scanned(self, res):
        self.log_text.append(f"  • {res['name']}: {res['files_count']} файлов ({SystemCleaner.format_size(res['size_bytes'])})")

    def _on_scan_finished(self, scanned_results, total_size, total_files):
        self.categories_data = scanned_results
        self._render_table()
        self.scan_btn.setEnabled(True)
        self.clean_btn.setEnabled(total_size > 0 or total_files > 0)
        self.progress_bar.setValue(100)

        total_str = SystemCleaner.format_size(total_size)
        self.chip_junk.findChild(QLabel, "chip_val").setText(total_str)
        self.chip_files.findChild(QLabel, "chip_val").setText(f"{total_files:,}")

        self.status_lbl.setText(f"Анализ завершен: найдено {total_str} ({total_files:,} файлов)")
        self.log_text.append(f"✔ Анализ завершен: готово к очистке {total_str} в {total_files} файлах.\n")

    def start_cleaning(self):
        selected = [c for c in self.categories_data if c.get("enabled", False)]
        if not selected:
            QMessageBox.information(self, "Очистка", "Выберите хотя бы одну категорию для очистки.")
            return

        sel_size = sum(c.get("size_bytes", 0) for c in selected)
        sel_files = sum(c.get("files_count", 0) for c in selected)
        size_str = SystemCleaner.format_size(sel_size)

        reply = QMessageBox.question(
            self,
            "Подтверждение очистки",
            f"Вы уверены, что хотите безвозвратно удалить {size_str} временных файлов ({sel_files:,} шт.)?\n\n"
            "Все личные документы, фотографии и важные файлы останутся в полной безопасности.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if reply != QMessageBox.Yes:
            return

        self.scan_btn.setEnabled(False)
        self.clean_btn.setEnabled(False)
        self.progress_bar.setValue(10)
        self.status_lbl.setText("Выполняется безопасная очистка...")
        self.log_text.append("🧹 Запуск процесса очистки...")

        self.clean_worker = CleanWorker(selected)
        self.clean_worker.progress_sig.connect(lambda pct, s: (self.progress_bar.setValue(pct), self.status_lbl.setText(s)))
        self.clean_worker.log_sig.connect(self.log_text.append)
        self.clean_worker.finished_sig.connect(self._on_clean_finished)
        self.clean_worker.start()

    def _on_clean_finished(self, total_freed, total_deleted):
        self.scan_btn.setEnabled(True)
        self.clean_btn.setEnabled(False)
        self.progress_bar.setValue(100)

        freed_str = SystemCleaner.format_size(total_freed)
        self.status_lbl.setText(f"🎉 Очистка завершена! Освобождено: {freed_str}")
        self.log_text.append(f"\n🎉 Очистка успешно завершена! Удалено {total_deleted:,} файлов, освобождено {freed_str} дискового пространства.\n")

        # Update free space on C:
        try:
            free_c = f"{psutil.disk_usage('C:').free / (1024**3):.1f} ГБ"
            self.chip_free.findChild(QLabel, "chip_val").setText(free_c)
        except Exception:
            pass

        # Reset scanned sizes and notify user
        self.chip_junk.findChild(QLabel, "chip_val").setText("0 Б")
        self.chip_files.findChild(QLabel, "chip_val").setText("0")

        QMessageBox.information(
            self,
            "Очистка завершена",
            f"🎉 Успешно освобождено {freed_str} дискового пространства!\n"
            f"Удалено временных и мусорных файлов: {total_deleted:,} шт."
        )

        # Re-scan to reflect zeroed caches
        self.start_scan()

    def on_language_changed(self, lang):
        is_ru = (lang == "ru")
        self.title_lbl.setText("🧹 Очистка системы и оптимизация дисков" if is_ru else "🧹 System Cleaner & Disk Optimizer")
        self.subtitle_lbl.setText(
            "Безопасное удаление временных файлов, кэша браузеров, дампов сбоев и корзины" if is_ru
            else "Safely cleans temporary files, web browser caches, crash dumps, and Recycle Bin"
        )
        self.scan_btn.setText("🔍 Анализ системы" if is_ru else "🔍 Analyze System")
        self.clean_btn.setText("🧹 Очистить мусор" if is_ru else "🧹 Clean Junk")
        self.toggle_all_btn.setText("☑ Выбрать все" if is_ru else "☑ Select All")
        self.table.setHorizontalHeaderLabels([
            "Категория очистки" if is_ru else "Cleanup Category",
            "Описание / Расположение" if is_ru else "Description / Location",
            "Файлов" if is_ru else "Files",
            "Занимаемый объем" if is_ru else "Size"
        ])
