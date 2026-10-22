"""
XUiDa64 - Cyber Startup Splash Screen
Frameless, animated startup screen with real-world loading progress,
glowing brand identity, and status messages.
"""

import os
from PyQt5.QtWidgets import QSplashScreen, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QFont, QPainter, QBrush, QPen

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CyberSplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 310)

        # Container Widget
        self.container = QFrame(self)
        self.container.setGeometry(0, 0, 500, 310)
        self.container.setStyleSheet("""
            QFrame {
                background-color: #0e141f;
                border: 2px solid #00d2ff;
                border-radius: 12px;
            }
            QLabel {
                font-family: 'Segoe UI Variable Text', 'Segoe UI', Arial, sans-serif;
                color: #ffffff;
                background: transparent;
                border: none;
            }
            QProgressBar {
                background-color: #172131;
                border: 1px solid #28374d;
                border-radius: 4px;
                text-align: center;
                color: transparent;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:0.5 #00d2ff, stop:1 #10b981);
                border-radius: 3px;
            }
        """)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(12)

        # 1. Top Logo & Badge
        top_h = QHBoxLayout()
        logo_lbl = QLabel()
        logo_path = os.path.join(BASE_DIR, "assets", "logo_small.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            logo_lbl.setPixmap(pix.scaledToWidth(260, Qt.SmoothTransformation))
        else:
            logo_lbl.setText("⚡ XUiDa64")
            logo_lbl.setStyleSheet("font-size: 26px; font-weight: bold; color: #00d2ff;")
        top_h.addWidget(logo_lbl)
        top_h.addStretch()

        ver_badge = QLabel("v1.0 EXTREME")
        ver_badge.setStyleSheet("""
            background-color: #1a273a;
            color: #38bdf8;
            font-size: 10px;
            font-weight: bold;
            padding: 4px 8px;
            border: 1px solid #293d5a;
            border-radius: 4px;
        """)
        top_h.addWidget(ver_badge)
        layout.addLayout(top_h)

        # 2. Subtitle & Description
        sub_lbl = QLabel("Аппаратная диагностика, датчики и комплекс оптимизации")
        sub_lbl.setStyleSheet("font-size: 12px; color: #94a3b8;")
        layout.addWidget(sub_lbl)

        layout.addStretch()

        # 3. Status readout
        self.status_lbl = QLabel("⚡ Инициализация аппаратных компонентов...")
        self.status_lbl.setStyleSheet("font-size: 11px; font-weight: 600; color: #38bdf8;")
        layout.addWidget(self.status_lbl)

        # 4. Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(15)
        layout.addWidget(self.progress_bar)

        # 5. Bottom Copyright / License
        bottom_h = QHBoxLayout()
        lic_lbl = QLabel("Free & Open Source Community Edition")
        lic_lbl.setStyleSheet("font-size: 10px; color: #64748b;")
        bottom_h.addWidget(lic_lbl)
        bottom_h.addStretch()

        self.pct_lbl = QLabel("15%")
        self.pct_lbl.setStyleSheet("font-size: 10px; font-weight: bold; color: #94a3b8;")
        bottom_h.addWidget(self.pct_lbl)
        layout.addLayout(bottom_h)

    def set_progress(self, pct: int, status_text: str):
        self.progress_bar.setValue(pct)
        self.pct_lbl.setText(f"{pct}%")
        self.status_lbl.setText(status_text)
        self.repaint()
