"""
XUiDa64 - Report Wizard Dialog
Generates and exports diagnostic reports in HTML, Text, and JSON formats with multi-language support.
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup,
    QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt

from core.i18n import I18N, _t
from reports.html_report import HTMLReportGenerator
from reports.text_report import TextReportGenerator

class ReportWizardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_t("rep_title"))
        self.setFixedSize(540, 390)
        self.setStyleSheet("""
            QDialog {
                background-color: #141a24;
                color: #ffffff;
            }
            QRadioButton, QCheckBox {
                color: #ffffff;
                font-size: 13px;
                spacing: 8px;
            }
            QLabel {
                font-size: 13px;
                color: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Title Banner
        self.title_lbl = QLabel(_t("rep_title"))
        self.title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #58a6ff;")
        layout.addWidget(self.title_lbl)

        self.desc_lbl = QLabel(_t("rep_desc"))
        self.desc_lbl.setStyleSheet("color: #8b949e;")
        layout.addWidget(self.desc_lbl)

        # Radio Buttons for Format
        self.format_group = QButtonGroup(self)
        self.rb_html = QRadioButton(_t("rep_html"))
        self.rb_html.setChecked(True)
        self.rb_txt = QRadioButton(_t("rep_txt"))
        self.rb_json = QRadioButton(_t("rep_json"))

        self.format_group.addButton(self.rb_html, 0)
        self.format_group.addButton(self.rb_txt, 1)
        self.format_group.addButton(self.rb_json, 2)

        self.rb_html.toggled.connect(self._update_default_extension)

        layout.addWidget(self.rb_html)
        layout.addWidget(self.rb_txt)
        layout.addWidget(self.rb_json)

        # File Destination
        file_box = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setText(os.path.abspath("XUiDa_Report.html"))
        file_box.addWidget(self.path_input)

        browse_btn = QPushButton(_t("rep_browse"))
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.clicked.connect(self.browse_destination)
        file_box.addWidget(browse_btn)
        layout.addLayout(file_box)

        # Options
        self.chk_open = QCheckBox(_t("rep_open_finished"))
        self.chk_open.setChecked(True)
        layout.addWidget(self.chk_open)

        layout.addStretch()

        # Bottom Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()

        cancel_btn = QPushButton(_t("rep_cancel"))
        cancel_btn.setObjectName("secondaryBtn")
        cancel_btn.clicked.connect(self.reject)
        btn_box.addWidget(cancel_btn)

        self.gen_btn = QPushButton(_t("rep_generate"))
        self.gen_btn.clicked.connect(self.generate_report)
        btn_box.addWidget(self.gen_btn)

        layout.addLayout(btn_box)

    def _update_default_extension(self):
        curr = self.path_input.text()
        base, _ = os.path.splitext(curr)
        if self.rb_html.isChecked():
            self.path_input.setText(f"{base}.html")
        elif self.rb_txt.isChecked():
            self.path_input.setText(f"{base}.txt")
        elif self.rb_json.isChecked():
            self.path_input.setText(f"{base}.json")

    def browse_destination(self):
        if self.rb_html.isChecked():
            flt = "HTML Files (*.html);;All Files (*.*)"
        elif self.rb_txt.isChecked():
            flt = "Text Files (*.txt);;All Files (*.*)"
        else:
            flt = "JSON Files (*.json);;All Files (*.*)"

        path, _ = QFileDialog.getSaveFileName(self, _t("rep_title"), self.path_input.text(), flt)
        if path:
            self.path_input.setText(path)

    def generate_report(self):
        dest_path = self.path_input.text().strip()
        if not dest_path:
            QMessageBox.warning(self, "XUiDa64", "Please specify a destination file path.")
            return

        self.gen_btn.setEnabled(False)
        self.gen_btn.setText(_t("rep_generating"))

        try:
            if self.rb_html.isChecked():
                HTMLReportGenerator.generate(dest_path)
            elif self.rb_txt.isChecked():
                TextReportGenerator.generate(dest_path)
            elif self.rb_json.isChecked():
                TextReportGenerator.generate_json(dest_path)

            QMessageBox.information(self, "XUiDa64", _t("rep_success", path=dest_path))

            if self.chk_open.isChecked() and os.path.exists(dest_path):
                os.startfile(dest_path)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report: {e}")
            self.gen_btn.setEnabled(True)
            self.gen_btn.setText(_t("rep_generate"))
