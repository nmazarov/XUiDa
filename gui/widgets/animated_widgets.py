"""
XUiDa64 - Modern Animated UI Components & Interactive Widgets
Features smooth hover transitions, live pulsing telemetry LEDs, sparkline graphs, and page fade animations.
"""

from collections import deque
from PyQt5.QtWidgets import (
    QPushButton, QToolButton, QStackedWidget, QWidget, QGraphicsOpacityEffect
)
from PyQt5.QtCore import (
    Qt, QPoint, QPointF, QRectF, QPropertyAnimation, QVariantAnimation,
    QAbstractAnimation, pyqtProperty
)
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient, QPainterPath, QFont
)

class LivePulseDot(QWidget):
    """Animated pulsing neon LED indicator for live telemetry polling."""
    def __init__(self, parent=None, color=QColor(16, 185, 129)):
        super().__init__(parent)
        self.setFixedSize(16, 16)
        self.base_color = color
        self._glow_alpha = 100
        self._glow_radius = 5.0

        # Pulse animation loop
        self.anim = QVariantAnimation(self)
        self.anim.setDuration(1400)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setLoopCount(-1)
        self.anim.valueChanged.connect(self._on_pulse)
        self.anim.start()

    def _on_pulse(self, val):
        # Oscillate glow radius and alpha
        if val < 0.5:
            progress = val * 2.0
        else:
            progress = (1.0 - val) * 2.0

        self._glow_radius = 4.0 + (progress * 3.5)
        self._glow_alpha = int(30 + (progress * 130))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        cx, cy = self.width() / 2.0, self.height() / 2.0

        # Outer pulsing glow
        glow_col = QColor(self.base_color)
        glow_col.setAlpha(self._glow_alpha)
        painter.setBrush(QBrush(glow_col))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), self._glow_radius, self._glow_radius)

        # Solid core LED
        painter.setBrush(QBrush(self.base_color))
        painter.drawEllipse(QPointF(cx, cy), 3.0, 3.0)


class SparklineWidget(QWidget):
    """Real-time 40-point mini sparkline graph with filled gradient under the curve."""
    def __init__(self, parent=None, max_points=40, line_color=QColor(0, 210, 255)):
        super().__init__(parent)
        self.setFixedSize(80, 18)
        self.max_points = max_points
        self.data = deque([0.0] * max_points, maxlen=max_points)
        self.line_color = line_color

    def add_value(self, val):
        self.data.append(float(val))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        w, h = float(self.width()), float(self.height())

        # Background frame
        painter.setBrush(QBrush(QColor(22, 29, 41, 180)))
        painter.setPen(QPen(QColor(42, 54, 74, 160), 1))
        painter.drawRoundedRect(QRectF(0, 0, w, h), 4, 4)

        if not self.data:
            return

        # Build path
        pts = []
        n = len(self.data)
        dx = (w - 6) / max(1, n - 1)

        for i, val in enumerate(self.data):
            x = 3 + i * dx
            # Clamp 0 - 100%
            clamped = max(0.0, min(100.0, val))
            y = (h - 3) - ((clamped / 100.0) * (h - 6))
            pts.append(QPointF(x, y))

        if len(pts) < 2:
            return

        # 1. Fill gradient below curve
        fill_path = QPainterPath()
        fill_path.moveTo(pts[0].x(), h - 2)
        for p in pts:
            fill_path.lineTo(p)
        fill_path.lineTo(pts[-1].x(), h - 2)
        fill_path.closeSubpath()

        grad = QLinearGradient(0, 0, 0, h)
        c_top = QColor(self.line_color)
        c_top.setAlpha(90)
        c_bot = QColor(self.line_color)
        c_bot.setAlpha(10)
        grad.setColorAt(0.0, c_top)
        grad.setColorAt(1.0, c_bot)

        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawPath(fill_path)

        # 2. Top stroke line
        pen = QPen(self.line_color, 1.5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        for i in range(len(pts) - 1):
            painter.drawLine(pts[i], pts[i + 1])


class AnimatedStackedWidget(QStackedWidget):
    """QStackedWidget with instant crisp switching, guaranteeing 100% opacity and ClearType subpixel rendering."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def setCurrentWidget(self, widget):
        if widget.graphicsEffect():
            widget.setGraphicsEffect(None)
        super().setCurrentWidget(widget)


class AnimatedPushButton(QPushButton):
    """Button with smooth animated color interpolation on hover and click."""
    def __init__(self, text="", parent=None, is_primary=False, is_danger=False):
        super().__init__(text, parent)
        self.is_primary = is_primary
        self.is_danger = is_danger

        # Color definitions
        if self.is_primary:
            self._norm_bg = QColor(35, 134, 54)     # #238636
            self._hover_bg = QColor(46, 160, 67)    # #2ea043
            self._border = QColor(56, 175, 77)
        elif self.is_danger:
            self._norm_bg = QColor(218, 54, 51)     # #da3633
            self._hover_bg = QColor(248, 81, 73)    # #f85149
            self._border = QColor(255, 100, 90)
        else:
            self._norm_bg = QColor(25, 33, 46)      # #19212e
            self._hover_bg = QColor(36, 52, 74)     # #24344a
            self._border = QColor(0, 210, 255)      # #00d2ff cyan glow

        self._curr_bg = QColor(self._norm_bg)

        # Hover animation
        self.anim = QVariantAnimation(self)
        self.anim.setDuration(160)
        self.anim.valueChanged.connect(self._on_color_changed)

    def _on_color_changed(self, col):
        self._curr_bg = col
        self.update()

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._curr_bg)
        self.anim.setEndValue(self._hover_bg)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._curr_bg)
        self.anim.setEndValue(self._norm_bg)
        self.anim.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        w, h = float(self.width()), float(self.height())

        is_hovered = self.underMouse()
        is_pressed = self.isDown()

        bg = self._curr_bg
        if is_pressed:
            bg = bg.darker(120)

        # Background
        painter.setBrush(QBrush(bg))
        if is_hovered:
            painter.setPen(QPen(self._border, 1.5))
        else:
            painter.setPen(QPen(QColor(42, 54, 74), 1))

        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), 6, 6)

        # Button Text
        painter.setFont(QFont("Segoe UI", 10, QFont.DemiBold if self.is_primary else QFont.Normal))
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(QRectF(0, 0, w, h), Qt.AlignCenter, self.text())
