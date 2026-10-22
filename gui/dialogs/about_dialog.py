"""
XUiDa64 - About Application Dialog
Displays brand logo, version, features, and open source license.
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from core.i18n import I18N, _t

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_t("about_title"))
        self.setFixedSize(560, 560)

        # Set Window Icon
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
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        # Brand Logo Banner
        logo_path = os.path.join(BASE_DIR, "assets", "logo.png")
        if os.path.exists(logo_path):
            logo_lbl = QLabel()
            pix = QPixmap(logo_path)
            logo_lbl.setPixmap(pix.scaledToWidth(420, Qt.SmoothTransformation))
            logo_lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_lbl)
        else:
            title = QLabel("XUiDa64 Extreme Edition")
            title.setStyleSheet("font-size: 20px; font-weight: bold; color: #58a6ff;")
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)

        ver = QLabel(_t("about_ver"))
        ver.setStyleSheet("font-size: 13px; color: #8b949e;")
        ver.setAlignment(Qt.AlignCenter)
        layout.addWidget(ver)

        desc = QLabel(_t("about_desc"))
        desc.setStyleSheet("font-size: 13px; line-height: 1.4; color: #ffffff;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Features box
        specs_frame = QFrame()
        specs_frame.setStyleSheet("""
            QFrame {
                background-color: #19212e;
                border: 1px solid #2a364a;
                border-radius: 8px;
                padding: 12px;
            }
            QLabel {
                color: #e6edf3;
                font-size: 13px;
                padding: 4px 6px;
                border-bottom: 1px solid #212c3d;
            }
        """)
        sp_layout = QVBoxLayout(specs_frame)
        sp_layout.setSpacing(6)
        sp_layout.setContentsMargins(8, 8, 8, 8)

        feat1 = QLabel(_t("about_feat1"))
        feat2 = QLabel(_t("about_feat2"))
        feat3 = QLabel(_t("about_feat3"))
        feat4 = QLabel(_t("about_feat4"))
        feat5 = QLabel(_t("about_feat5"))
        feat5.setStyleSheet("color: #e6edf3; font-size: 13px; padding: 4px 6px; border-bottom: none;")

        sp_layout.addWidget(feat1)
        sp_layout.addWidget(feat2)
        sp_layout.addWidget(feat3)
        sp_layout.addWidget(feat4)
        sp_layout.addWidget(feat5)
        layout.addWidget(specs_frame)

        license_lbl = QLabel(_t("about_license"))
        license_lbl.setStyleSheet("color: #3fb950; font-size: 13px; font-weight: bold;")
        layout.addWidget(license_lbl)

        layout.addStretch()

        # Bottom Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()

        close_btn = QPushButton("OK")
        close_btn.setFixedWidth(110)
        close_btn.setFixedHeight(34)
        close_btn.clicked.connect(self.accept)
        btn_box.addWidget(close_btn)

        layout.addLayout(btn_box)
