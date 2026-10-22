"""
XUiDa64 - Full-Screen Monitor Diagnostics & Dead Pixel Suite
Comprehensive display testing: solid color dead pixel locator, grayscale ramps, color banding, and geometry grid.
"""

import os
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QFont, QIcon

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MonitorDiagDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("XUiDa64 - Monitor Diagnostics")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)

        icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.current_step = 0
        self.tests = [
            ("Сплошной черный (Black) - Поиск горящих/застрявших пикселей", "solid", QColor(0, 0, 0)),
            ("Сплошной белый (White) - Поиск битых/мертвых пикселей", "solid", QColor(255, 255, 255)),
            ("Сплошной красный (Red Subpixel) - Проверка субпикселей", "solid", QColor(255, 0, 0)),
            ("Сплошной зеленый (Green Subpixel) - Проверка субпикселей", "solid", QColor(0, 255, 0)),
            ("Сплошной синий (Blue Subpixel) - Проверка субпикселей", "solid", QColor(0, 0, 255)),
            ("Сплошной циан (Cyan)", "solid", QColor(0, 255, 255)),
            ("Сплошной пурпурный (Magenta)", "solid", QColor(255, 0, 255)),
            ("Сплошной желтый (Yellow)", "solid", QColor(255, 255, 0)),
            ("Ступенчатый градиент серого (16 уровней яркости / Гамма)", "gray_steps", None),
            ("Плавный RGB-градиент (Тест битности матрицы / Color Banding)", "smooth_gradient", None),
            ("Сетка геометрии и центровки (Geometry & Alignment Grid)", "geometry_grid", None),
            ("Четкость шрифтов и субпиксельное сглаживание ClearType", "text_readability", None),
        ]

        self.showFullScreen()

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        elif key in (Qt.Key_Right, Qt.Key_Space, Qt.Key_Enter, Qt.Key_Return, Qt.Key_Down):
            self.next_test()
        elif key in (Qt.Key_Left, Qt.Key_Backspace, Qt.Key_Up):
            self.prev_test()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.next_test()
        elif event.button() == Qt.RightButton:
            self.prev_test()

    def next_test(self):
        self.current_step = (self.current_step + 1) % len(self.tests)
        self.update()

    def prev_test(self):
        self.current_step = (self.current_step - 1) % len(self.tests)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        w, h = self.width(), self.height()

        title, mode, color_data = self.tests[self.current_step]

        # 1. Solid color fill
        if mode == "solid":
            painter.fillRect(0, 0, w, h, color_data)

        # 2. 16 Grayscale Steps
        elif mode == "gray_steps":
            steps = 16
            step_w = w / float(steps)
            for i in range(steps):
                level = int((i / float(steps - 1)) * 255)
                c = QColor(level, level, level)
                painter.fillRect(int(i * step_w), 0, int(step_w + 1), h, c)

        # 3. Smooth RGB Gradient
        elif mode == "smooth_gradient":
            # Split screen into 3 horizontal bands: Red, Green, Blue
            band_h = h // 3
            # Red band
            grad_r = QLinearGradient(0, 0, w, 0)
            grad_r.setColorAt(0.0, QColor(0, 0, 0))
            grad_r.setColorAt(1.0, QColor(255, 0, 0))
            painter.fillRect(0, 0, w, band_h, grad_r)

            # Green band
            grad_g = QLinearGradient(0, band_h, w, band_h)
            grad_g.setColorAt(0.0, QColor(0, 0, 0))
            grad_g.setColorAt(1.0, QColor(0, 255, 0))
            painter.fillRect(0, band_h, w, band_h, grad_g)

            # Blue band
            grad_b = QLinearGradient(0, band_h * 2, w, band_h * 2)
            grad_b.setColorAt(0.0, QColor(0, 0, 0))
            grad_b.setColorAt(1.0, QColor(0, 0, 255))
            painter.fillRect(0, band_h * 2, w, h - band_h * 2, grad_b)

        # 4. Geometry and Alignment Grid
        elif mode == "geometry_grid":
            painter.fillRect(0, 0, w, h, QColor(20, 20, 20))
            pen = QPen(QColor(0, 210, 255), 1)
            painter.setPen(pen)

            # Grid lines every 60 pixels
            grid_sz = 60
            for x in range(0, w, grid_sz):
                painter.drawLine(x, 0, x, h)
            for y in range(0, h, grid_sz):
                painter.drawLine(0, y, w, y)

            # Diagonals & Center
            pen_accent = QPen(QColor(255, 255, 255), 2)
            painter.setPen(pen_accent)
            painter.drawLine(0, 0, w, h)
            painter.drawLine(0, h, w, 0)

            # Center target circles
            painter.setRenderHint(QPainter.Antialiasing, True)
            cx, cy = w // 2, h // 2
            painter.setBrush(Qt.NoBrush)
            for r in [50, 100, 180, 260]:
                painter.drawEllipse(QPoint(cx, cy), r, r)

        # 5. Text Readability & Subpixel ClearType test
        elif mode == "text_readability":
            painter.fillRect(0, 0, w, h, QColor(15, 20, 30))
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setPen(QColor(255, 255, 255))

            sizes = [9, 10, 11, 12, 14, 16, 20, 24, 32, 42]
            y_offset = 60
            for sz in sizes:
                font = QFont("Segoe UI", sz)
                painter.setFont(font)
                sample_text = f"XUiDa64 Diagnostics ({sz}pt): The quick brown fox jumps over the lazy dog. 1234567890 !@#$%^&*"
                painter.drawText(60, y_offset, sample_text)
                y_offset += sz + 24

        # Floating HUD Overlay at the bottom
        hud_h = 44
        hud_w = min(800, w - 40)
        hud_x = (w - hud_w) // 2
        hud_y = h - hud_h - 20

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(QBrush(QColor(13, 17, 24, 220)))
        painter.setPen(QPen(QColor(0, 210, 255, 180), 1))
        painter.drawRoundedRect(hud_x, hud_y, hud_w, hud_h, 8, 8)

        # HUD Text
        painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
        painter.setPen(QColor(255, 255, 255))
        hud_text = f"[{self.current_step + 1}/{len(self.tests)}] {title}"
        painter.drawText(hud_x + 16, hud_y + 27, hud_text)

        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor(156, 163, 175))
        hint_text = "Пробел / Клик: Далее  |  Esc: Выход"
        painter.drawText(hud_x + hud_w - 240, hud_y + 27, hint_text)
