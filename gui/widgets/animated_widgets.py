"""
XUiDa64 - Modern Animated UI Components & Interactive Widgets
Crafted according to Benji Taylor / Stageshow Design Engineering principles:
- Micro-interactions with purposeful easing (OutCubic / OutQuad).
- Non-jarring, unhurried feedback (150ms-250ms).
- Interactive cards with smooth hover elevation and border glow transitions.
- Fluid circular dial gauges with continuous animated value interpolation.
- Crisp ClearType subpixel text preservation after transitions.
"""

from collections import deque
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QToolButton, QStackedWidget, QGraphicsOpacityEffect,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import (
    Qt, QPoint, QPointF, QRectF, QPropertyAnimation, QVariantAnimation,
    QEasingCurve, pyqtSignal, pyqtProperty
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
        self.anim.setDuration(1600)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setLoopCount(-1)
        self.anim.valueChanged.connect(self._on_pulse)
        self.anim.start()

    def set_color(self, color):
        self.base_color = QColor(color)
        self.update()

    def _on_pulse(self, val):
        if val < 0.5:
            progress = val * 2.0
        else:
            progress = (1.0 - val) * 2.0

        self._glow_radius = 4.0 + (progress * 3.5)
        self._glow_alpha = int(25 + (progress * 125))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        cx, cy = self.width() / 2.0, self.height() / 2.0

        # Outer pulsing glow halo
        glow_col = QColor(self.base_color)
        glow_col.setAlpha(self._glow_alpha)
        painter.setBrush(QBrush(glow_col))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), self._glow_radius, self._glow_radius)

        # Crisp inner core LED
        painter.setBrush(QBrush(self.base_color))
        painter.drawEllipse(QPointF(cx, cy), 3.0, 3.0)


class SparklineWidget(QWidget):
    """Real-time sparkline graph with filled gradient under the curve."""
    def __init__(self, parent=None, max_points=36, line_color=QColor(56, 189, 248)):
        super().__init__(parent)
        self.setFixedSize(84, 22)
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

        # Clean inset background pill
        painter.setBrush(QBrush(QColor(18, 24, 34, 180)))
        painter.setPen(QPen(QColor(34, 44, 61, 140), 1))
        painter.drawRoundedRect(QRectF(0, 0, w, h), 5, 5)

        if not self.data:
            return

        pts = []
        n = len(self.data)
        dx = (w - 8) / max(1, n - 1)

        for i, val in enumerate(self.data):
            x = 4 + i * dx
            clamped = max(0.0, min(100.0, val))
            y = (h - 4) - ((clamped / 100.0) * (h - 8))
            pts.append(QPointF(x, y))

        if len(pts) < 2:
            return

        # 1. Fill gradient below curve
        fill_path = QPainterPath()
        fill_path.moveTo(pts[0].x(), h - 3)
        for p in pts:
            fill_path.lineTo(p)
        fill_path.lineTo(pts[-1].x(), h - 3)
        fill_path.closeSubpath()

        grad = QLinearGradient(0, 0, 0, h)
        c_top = QColor(self.line_color)
        c_top.setAlpha(80)
        c_bot = QColor(self.line_color)
        c_bot.setAlpha(8)
        grad.setColorAt(0.0, c_top)
        grad.setColorAt(1.0, c_bot)

        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawPath(fill_path)

        # 2. Smooth stroke line
        pen = QPen(self.line_color, 1.5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        for i in range(len(pts) - 1):
            painter.drawLine(pts[i], pts[i + 1])


class AnimatedStackedWidget(QStackedWidget):
    """
    QStackedWidget featuring a subtle 180ms crossfade entrance.
    Guarantees 100% opacity and native ClearType subpixel text rendering after transition completes.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._anim = None
        self._effect = None

    def setCurrentWidget(self, widget):
        if widget == self.currentWidget():
            return
        super().setCurrentWidget(widget)
        # Apply smooth 180ms fade-in transition
        self._effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(self._effect)
        self._anim = QPropertyAnimation(self._effect, b"opacity")
        self._anim.setDuration(180)
        self._anim.setStartValue(0.2)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.finished.connect(lambda: widget.setGraphicsEffect(None))
        self._anim.start()


class CraftCard(QFrame):
    """
    Elevated interactive card following Benji Taylor craft guidelines:
    - Restrained surface palette (obsidian #131824 -> #1a2232 on hover).
    - Subtle 1px hairline border with electric glow transition.
    - Balanced 12px insets and crisp typographic hierarchy.
    """
    def __init__(self, title="", value="--", subtitle="", accent_color="#38bdf8", parent=None):
        super().__init__(parent)
        self.accent_color = QColor(accent_color)
        self._norm_bg = QColor(20, 26, 37)
        self._hover_bg = QColor(26, 35, 50)
        self._curr_bg = QColor(self._norm_bg)

        self._norm_border = QColor(36, 46, 64)
        self._hover_border = QColor(self.accent_color)
        self._hover_border.setAlpha(180)
        self._curr_border = QColor(self._norm_border)

        self._border_progress = 0.0

        # Hover animation
        self.anim = QVariantAnimation(self)
        self.anim.setDuration(180)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.valueChanged.connect(self._on_anim_step)

        # Card Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        # Title row
        self.title_row = QHBoxLayout()
        self.title_row.setSpacing(6)

        self.dot = LivePulseDot(self, color=self.accent_color)
        self.title_lbl = QLabel(title.upper())
        self.title_lbl.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 700;
            color: {self.accent_color.name()};
            letter-spacing: 0.6px;
            background: transparent;
        """)
        self.title_row.addWidget(self.dot)
        self.title_row.addWidget(self.title_lbl)
        self.title_row.addStretch()
        layout.addLayout(self.title_row)

        # Value label
        self.val_lbl = QLabel(value)
        self.val_lbl.setObjectName("chip_val")
        self.val_lbl.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #f8fafc;
            background: transparent;
        """)
        layout.addWidget(self.val_lbl)

        # Optional subtitle / badge
        self.sub_lbl = QLabel(subtitle)
        self.sub_lbl.setStyleSheet("font-size: 11px; color: #94a3b8; background: transparent;")
        if not subtitle:
            self.sub_lbl.hide()
        layout.addWidget(self.sub_lbl)

    def set_value(self, val):
        self.val_lbl.setText(str(val))

    def set_subtitle(self, sub):
        self.sub_lbl.setText(str(sub))
        self.sub_lbl.setVisible(bool(sub))

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._border_progress)
        self.anim.setEndValue(1.0)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._border_progress)
        self.anim.setEndValue(0.0)
        self.anim.start()
        super().leaveEvent(event)

    def _on_anim_step(self, val):
        self._border_progress = val
        # Interpolate background
        r = int(self._norm_bg.red() + (self._hover_bg.red() - self._norm_bg.red()) * val)
        g = int(self._norm_bg.green() + (self._hover_bg.green() - self._norm_bg.green()) * val)
        b = int(self._norm_bg.blue() + (self._hover_bg.blue() - self._norm_bg.blue()) * val)
        self._curr_bg = QColor(r, g, b)

        # Interpolate border
        r_b = int(self._norm_border.red() + (self._hover_border.red() - self._norm_border.red()) * val)
        g_b = int(self._norm_border.green() + (self._hover_border.green() - self._norm_border.green()) * val)
        b_b = int(self._norm_border.blue() + (self._hover_border.blue() - self._norm_border.blue()) * val)
        self._curr_border = QColor(r_b, g_b, b_b)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        w, h = float(self.width()), float(self.height())

        # Card base
        painter.setBrush(QBrush(self._curr_bg))
        painter.setPen(QPen(self._curr_border, 1.2 if self._border_progress > 0.0 else 1.0))
        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), 9, 9)


class AnimatedDialGauge(QWidget):
    """
    Circular arc telemetry gauge featuring smooth value easing (OutCubic).
    Paints a 270-degree arc with dynamic colored gradient and center value readout.
    """
    def __init__(self, title="", unit="%", parent=None, min_val=0, max_val=100):
        super().__init__(parent)
        self.setFixedSize(136, 120)
        self.title = title
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self._current_val = 0.0
        self._target_val = 0.0

        self.anim = QVariantAnimation(self)
        self.anim.setDuration(350)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.valueChanged.connect(self._on_anim_val)

    def set_value(self, val, animate=True):
        try:
            target = float(val)
        except (ValueError, TypeError):
            return

        self._target_val = target
        if not animate or not self.isVisible():
            self._current_val = target
            self.update()
            return

        self.anim.stop()
        self.anim.setStartValue(self._current_val)
        self.anim.setEndValue(self._target_val)
        self.anim.start()

    def _on_anim_val(self, val):
        self._current_val = float(val)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        w, h = float(self.width()), float(self.height())

        # Determine dial accent color based on load/temp
        ratio = max(0.0, min(1.0, (self._current_val - self.min_val) / max(1.0, self.max_val - self.min_val)))
        if ratio < 0.60:
            arc_color = QColor(16, 185, 129)   # Emerald Green #10b981
        elif ratio < 0.82:
            arc_color = QColor(245, 158, 11)   # Amber #f59e0b
        else:
            arc_color = QColor(239, 68, 68)    # Crimson Red #ef4444

        # Bounding box for arc
        dial_size = min(w, h - 22) - 14
        dial_rect = QRectF((w - dial_size) / 2.0, 6, dial_size, dial_size)

        # 1. Background Arc (270 degrees from 225 deg clockwise to -45 deg)
        bg_pen = QPen(QColor(28, 36, 50), 7, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(dial_rect, 225 * 16, -270 * 16)

        # 2. Foreground Animated Arc
        sweep = int(-270.0 * ratio * 16)
        fg_pen = QPen(arc_color, 7.5, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(fg_pen)
        painter.drawArc(dial_rect, 225 * 16, sweep)

        # 3. Center Value Text
        painter.setPen(QColor(248, 250, 252))
        painter.setFont(QFont("Segoe UI Variable Text", 15, QFont.Bold))
        val_str = f"{int(round(self._current_val))}{self.unit}"
        painter.drawText(QRectF(0, dial_rect.top() + (dial_size / 2.0) - 12, w, 24), Qt.AlignCenter, val_str)

        # 4. Bottom Title Text
        painter.setPen(QColor(148, 163, 184))
        painter.setFont(QFont("Segoe UI Variable Text", 9, QFont.Normal))
        painter.drawText(QRectF(0, h - 20, w, 18), Qt.AlignCenter, self.title)


class AnimatedPushButton(QPushButton):
    """Button with smooth animated color interpolation on hover and click."""
    def __init__(self, text="", parent=None, is_primary=False, is_danger=False):
        super().__init__(text, parent)
        self.is_primary = is_primary
        self.is_danger = is_danger

        # Color definitions
        if self.is_primary:
            self._norm_bg = QColor(16, 185, 129)    # #10b981
            self._hover_bg = QColor(5, 150, 105)    # #059669
            self._border = QColor(52, 211, 153)
        elif self.is_danger:
            self._norm_bg = QColor(239, 68, 68)     # #ef4444
            self._hover_bg = QColor(220, 38, 38)    # #dc2626
            self._border = QColor(248, 113, 113)
        else:
            self._norm_bg = QColor(21, 27, 38)      # #151b26
            self._hover_bg = QColor(30, 40, 56)     # #1e2838
            self._border = QColor(56, 189, 248)     # #38bdf8

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

    def sizeHint(self):
        fm = self.fontMetrics()
        w = fm.horizontalAdvance(self.text()) + 32
        h = max(34, fm.height() + 14)
        from PyQt5.QtCore import QSize
        return QSize(w, h)

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
            painter.setPen(QPen(self._border, 1.2))
        else:
            painter.setPen(QPen(QColor(36, 46, 64), 1))

        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), 7, 7)

        # Button Text
        painter.setFont(QFont("Segoe UI Variable Text", 10, QFont.DemiBold if self.is_primary else QFont.Normal))
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(QRectF(0, 0, w, h), Qt.AlignCenter, self.text())


class DockPill(QFrame):
    """
    Craft & Motion bottom dock capsule pill.
    Features subtle glassmorphic background, border transition, and smooth micro-interactions.
    """
    def __init__(self, parent=None, bg_color="rgba(18, 23, 34, 0.85)", border_color="#1c2536", hover_border="#38bdf8"):
        super().__init__(parent)
        self.bg_color = bg_color
        self.border_color = border_color
        self.hover_border = hover_border
        self._is_hovered = False
        self.setFixedHeight(27)
        self.setAttribute(Qt.WA_Hover, True)
        self._apply_style()

    def _apply_style(self):
        bc = self.hover_border if self._is_hovered else self.border_color
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.bg_color};
                border: 1px solid {bc};
                border-radius: 13px;
                padding: 1px 6px;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)

    def enterEvent(self, event):
        self._is_hovered = True
        self._apply_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_hovered = False
        self._apply_style()
        super().leaveEvent(event)

