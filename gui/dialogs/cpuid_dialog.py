"""
XUiDa64 - AIDA64-Style CPUID Utility Window
Recreates iconic AIDA64 CPUID dialog with processor logos, clocks, instruction flags, and multi-language support.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QGroupBox,
    QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from core.i18n import I18N, _t, _prop
from core.cpuid import CPUID
from core.cpu_info import CPUInfo
from core.system_info import SystemInfo
from core.memory_info import MemoryInfo

class CPUIDDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_t("cpuid_title"))
        self.setFixedSize(540, 620)
        self.setStyleSheet("""
            QDialog {
                background-color: #141a24;
                color: #ffffff;
            }
            QGroupBox {
                border: 1px solid #2a364a;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
                color: #58a6ff;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
            QLabel {
                font-size: 12px;
                color: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # 1. Processor Header Banner
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #19212e; border: 1px solid #2a364a; border-radius: 6px; padding: 10px;")
        h_layout = QVBoxLayout(header_frame)
        h_layout.setSpacing(4)

        self.proc_name_lbl = QLabel("Processor Name")
        self.proc_name_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #58a6ff;")
        h_layout.addWidget(self.proc_name_lbl)

        self.socket_lbl = QLabel("Socket / Architecture")
        self.socket_lbl.setStyleSheet("color: #8b949e; font-size: 12px;")
        h_layout.addWidget(self.socket_lbl)

        layout.addWidget(header_frame)

        # 2. Clocks & Multipliers Group
        self.clocks_group = QGroupBox(_t("cpuid_clocks"))
        c_layout = QGridLayout(self.clocks_group)
        c_layout.setSpacing(6)

        self.lbl_cpu_clock = QLabel(f"{_t('cpuid_core_speed')}: --")
        self.lbl_multiplier = QLabel(f"{_t('cpuid_multiplier')}: x34.0")
        self.lbl_bus_speed = QLabel(f"{_t('cpuid_bus_speed')}: 100.0 MHz")
        self.lbl_voltage = QLabel(f"{_t('cpuid_voltage')}: --")

        c_layout.addWidget(self.lbl_cpu_clock, 0, 0)
        c_layout.addWidget(self.lbl_multiplier, 0, 1)
        c_layout.addWidget(self.lbl_bus_speed, 1, 0)
        c_layout.addWidget(self.lbl_voltage, 1, 1)
        layout.addWidget(self.clocks_group)

        # 3. CPUID Stepping & Family Group
        self.stepping_group = QGroupBox(_t("cpuid_signature"))
        s_layout = QGridLayout(self.stepping_group)
        s_layout.setSpacing(6)

        self.lbl_family = QLabel(f"{_t('cpuid_family')}: --")
        self.lbl_model = QLabel(f"{_t('cpuid_model')}: --")
        self.lbl_stepping = QLabel(f"{_t('cpuid_stepping')}: --")
        self.lbl_signature = QLabel(f"{_prop('Signature')}: --")

        s_layout.addWidget(self.lbl_family, 0, 0)
        s_layout.addWidget(self.lbl_model, 0, 1)
        s_layout.addWidget(self.lbl_stepping, 1, 0)
        s_layout.addWidget(self.lbl_signature, 1, 1)
        layout.addWidget(self.stepping_group)

        # 4. Instruction Sets Grid Group
        self.inst_group = QGroupBox(_t("cpuid_instructions"))
        self.inst_layout = QGridLayout(self.inst_group)
        self.inst_layout.setSpacing(6)
        layout.addWidget(self.inst_group)

        # 5. Cache Hierarchy Group
        is_ru = (I18N.get_language() == "ru")
        self.cache_group = QGroupBox(_t("cpuid_caches"))
        ca_layout = QGridLayout(self.cache_group)
        ca_layout.setSpacing(6)

        self.lbl_l1d = QLabel("L1 Данные: --" if is_ru else "L1 Data: --")
        self.lbl_l1i = QLabel("L1 Инструкции: --" if is_ru else "L1 Inst: --")
        self.lbl_l2 = QLabel("L2 Кэш: --" if is_ru else "L2 Cache: --")
        self.lbl_l3 = QLabel("L3 Кэш: --" if is_ru else "L3 Cache: --")

        ca_layout.addWidget(self.lbl_l1d, 0, 0)
        ca_layout.addWidget(self.lbl_l1i, 0, 1)
        ca_layout.addWidget(self.lbl_l2, 1, 0)
        ca_layout.addWidget(self.lbl_l3, 1, 1)
        layout.addWidget(self.cache_group)

        # 6. Bottom Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()

        self.refresh_btn = QPushButton(_t("cpuid_refresh"))
        self.refresh_btn.setObjectName("secondaryBtn")
        self.refresh_btn.clicked.connect(self.load_data)
        btn_box.addWidget(self.refresh_btn)

        close_btn = QPushButton(_t("cpuid_close"))
        close_btn.clicked.connect(self.accept)
        btn_box.addWidget(close_btn)

        layout.addLayout(btn_box)

        self.load_data()

    def load_data(self):
        cpuid_info = CPUID.get_info()
        cpu_details = CPUInfo.get_details()
        is_ru = (I18N.get_language() == "ru")

        cores_word = "Ядер" if is_ru else "Cores"
        threads_word = "Потоков" if is_ru else "Threads"
        self.proc_name_lbl.setText(cpuid_info.get("brand", "Unknown Processor"))
        self.socket_lbl.setText(f"{cpu_details.get('Socket', 'LGA1700')} | {cpu_details.get('PhysicalCores')} {cores_word}, {cpu_details.get('LogicalCores')} {threads_word}")

        self.lbl_cpu_clock.setText(f"{_t('cpuid_core_speed')}: {cpu_details.get('CurrentClock')}")
        self.lbl_voltage.setText(f"{_t('cpuid_voltage')}: {cpu_details.get('Voltage')}")

        self.lbl_family.setText(f"{_t('cpuid_family')}: {cpuid_info.get('family', '0')}")
        self.lbl_model.setText(f"{_t('cpuid_model')}: {cpuid_info.get('model', '0')}")
        self.lbl_stepping.setText(f"{_t('cpuid_stepping')}: {cpuid_info.get('stepping', '0')}")
        self.lbl_signature.setText(f"{_prop('Signature')}: {cpuid_info.get('signature', '0')}")

        # Instruction sets
        features = cpuid_info.get("features", {})
        key_features = [
            "MMX", "SSE", "SSE2", "SSE3", "SSSE3", "SSE4.1", "SSE4.2",
            "AVX", "AVX2", "FMA3", "AES", "SHA", "CLMUL", "BMI1",
            "BMI2", "POPCNT", "x64 (EM64T/AMD64)", "Hyper-Threading"
        ]

        # Clear layout
        while self.inst_layout.count():
            item = self.inst_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for idx, feat in enumerate(key_features):
            is_sup = features.get(feat, False)
            sym = "✔" if is_sup else "✖"
            color = "#3fb950" if is_sup else "#8b949e"
            lbl = QLabel(f"{sym} {feat}")
            lbl.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: {'bold' if is_sup else 'normal'};")
            self.inst_layout.addWidget(lbl, idx // 3, idx % 3)

        # Caches
        caches = cpuid_info.get("caches", [])
        l1d_str = "L1 Данные" if is_ru else "L1 Data"
        l1i_str = "L1 Инструкции" if is_ru else "L1 Inst"
        l2_str = "L2 Кэш" if is_ru else "L2 Cache"
        l3_str = "L3 Кэш" if is_ru else "L3 Cache"

        for c in caches:
            lvl = c.get("level", "")
            sz = c.get("size_kb", 0)
            if "L1 Data" in lvl:
                self.lbl_l1d.setText(f"{l1d_str}: {sz} КБ" if is_ru else f"L1 Data: {sz} KB")
            elif "L1 Instruction" in lvl:
                self.lbl_l1i.setText(f"{l1i_str}: {sz} КБ" if is_ru else f"L1 Inst: {sz} KB")
            elif "L2" in lvl:
                self.lbl_l2.setText(f"{l2_str}: {sz // 1024} МБ ({sz} КБ)" if is_ru else f"L2 Cache: {sz // 1024} MB ({sz} KB)")
            elif "L3" in lvl:
                self.lbl_l3.setText(f"{l3_str}: {sz // 1024} МБ" if is_ru else f"L3 Cache: {sz // 1024} MB")
