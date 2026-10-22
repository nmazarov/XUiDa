"""
XUiDa64 - About Application Dialog
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from core.i18n import I18N, _t

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_t("about_title"))
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #161b22;
                color: #c9d1d9;
            }
            QLabel {
                font-family: 'Segoe UI', Arial;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Header Title
        title = QLabel("XUiDa64 Extreme Edition")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #58a6ff;")
        layout.addWidget(title)

        ver = QLabel(_t("about_ver"))
        ver.setStyleSheet("font-size: 12px; color: #8b949e;")
        layout.addWidget(ver)

        desc = QLabel(_t("about_desc"))
        desc.setStyleSheet("font-size: 13px; line-height: 1.4; color: #e6edf3;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Specs box
        specs_frame = QFrame()
        specs_frame.setStyleSheet("background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 10px;")
        sp_layout = QVBoxLayout(specs_frame)
        sp_layout.setSpacing(4)

        sp_layout.addWidget(QLabel(_t("about_feat1")))
        sp_layout.addWidget(QLabel(_t("about_feat2")))
        sp_layout.addWidget(QLabel(_t("about_feat3")))
        sp_layout.addWidget(QLabel(_t("about_feat4")))
        sp_layout.addWidget(QLabel(_t("about_feat5")))
        layout.addWidget(specs_frame)

        license_lbl = QLabel(_t("about_license"))
        license_lbl.setStyleSheet("color: #3fb950; font-size: 12px; font-weight: bold;")
        layout.addWidget(license_lbl)

        layout.addStretch()

        # Bottom Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()

        close_btn = QPushButton("OK")
        close_btn.setFixedWidth(90)
        close_btn.clicked.connect(self.accept)
        btn_box.addWidget(close_btn)

        layout.addLayout(btn_box)
