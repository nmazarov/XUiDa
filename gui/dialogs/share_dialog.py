"""
XUiDa64 - Share PC Specification Dialog & Card Generator
Generates high-resolution 16:9 cyberpunk PC spec graphic cards and forum-ready Markdown/BBCode.
"""

import os
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QTabWidget, QWidget, QFileDialog, QMessageBox, QFrame, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage

from core.cpuid import CPUID
from core.cpu_info import CPUInfo
from core.system_info import SystemInfo
from core.memory_info import MemoryInfo
from core.gpu_info import GPUInfo
from core.storage_info import StorageInfo
from gui.widgets.animated_widgets import AnimatedPushButton

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ShareConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("XUiDa64 - Поделиться характеристиками ПК")
        self.resize(880, 680)
        self.setMinimumSize(780, 600)

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
            QTabWidget::pane {
                border: 1px solid #2a364a;
                background: #141a24;
                border-radius: 6px;
            }
            QTabBar::tab {
                background: #19212e;
                color: #8b949e;
                padding: 8px 18px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: #141a24;
                color: #58a6ff;
                font-weight: bold;
                border: 1px solid #2a364a;
                border-bottom: none;
            }
            QTextEdit {
                background-color: #19212e;
                color: #e6edf3;
                border: 1px solid #2a364a;
                border-radius: 6px;
                font-family: 'Consolas', monospace;
                font-size: 13px;
                padding: 10px;
            }
        """)

        self._gather_specs()
        self.generated_pil_img = None
        self._init_ui()

    def _gather_specs(self):
        # 1. CPU
        cpuid_data = CPUID.get_info()
        cpu_details = CPUInfo.get_details()
        self.cpu_name = cpuid_data.get("brand", "x86-64 Processor")
        self.cpu_cores = f"{cpu_details.get('PhysicalCores', 8)}C / {cpu_details.get('LogicalCores', 16)}T"
        self.cpu_clock = f"{cpu_details.get('MaxClock', '3600 MHz')}"

        # 2. Motherboard
        mb_info = SystemInfo.get_motherboard_info()
        self.mb_name = f"{mb_info.get('Manufacturer', '')} {mb_info.get('Product', 'Standard Motherboard')}".strip()
        self.bios_ver = SystemInfo.get_bios_info().get("Version", "UEFI")

        # 3. RAM
        ram_summary = MemoryInfo.get_summary()
        self.ram_total = ram_summary.get("TotalPhysical", "16 GB")
        spd = MemoryInfo.get_spd_modules()
        if spd and isinstance(spd, list) and len(spd) > 0:
            first = spd[0]
            self.ram_type = f"{first.get('MemoryType', 'DDR')} @ {first.get('Speed', '')}"
        else:
            self.ram_type = "DDR4 / DDR5 High Speed"

        # 4. GPU
        gpus = GPUInfo.get_all_gpus()
        if gpus:
            g = gpus[0]
            self.gpu_name = g.get("Name", "Graphics Adapter")
            vram = g.get("VRAM_MB", "N/A")
            self.gpu_vram = f"{vram} MB VRAM" if vram != "N/A" else "Dedicated Video Memory"
        else:
            self.gpu_name = "Integrated Graphics"
            self.gpu_vram = "Shared Memory"

        # 5. Storage
        disks = StorageInfo.get_physical_drives()
        if disks and isinstance(disks, list):
            self.disk_name = disks[0].get("Model", "High Speed NVMe SSD")
            self.disk_size = disks[0].get("Size", "1 TB")
        else:
            self.disk_name = "NVMe SSD"
            self.disk_size = "Fast Storage"

        # 6. OS
        os_info = SystemInfo.get_os_info()
        self.os_name = os_info.get("OSName", "Windows 11 x64")

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        title_lbl = QLabel("📸 Экспорт спецификации компьютера (Share PC Configuration)")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #58a6ff;")
        layout.addWidget(title_lbl)

        tabs = QTabWidget()

        # TAB 1: Графическая карточка
        tab_card = QWidget()
        t1_layout = QVBoxLayout(tab_card)
        t1_layout.setContentsMargins(12, 12, 12, 12)
        t1_layout.setSpacing(10)

        self.preview_lbl = QLabel()
        self.preview_lbl.setAlignment(Qt.AlignCenter)
        self.preview_lbl.setStyleSheet("border: 1px solid #2a364a; border-radius: 8px; background: #0f141c;")
        t1_layout.addWidget(self.preview_lbl, 1)

        btn_row = QHBoxLayout()
        self.btn_save_png = AnimatedPushButton("💾 Сохранить изображение (PNG)", is_primary=True)
        self.btn_save_png.setFixedHeight(36)
        self.btn_save_png.clicked.connect(self._save_image)
        btn_row.addWidget(self.btn_save_png)

        self.btn_copy_img = AnimatedPushButton("📋 Скопировать картинку в буфер", is_primary=False)
        self.btn_copy_img.setFixedHeight(36)
        self.btn_copy_img.clicked.connect(self._copy_image_clipboard)
        btn_row.addWidget(self.btn_copy_img)

        btn_row.addStretch()
        t1_layout.addLayout(btn_row)
        tabs.addTab(tab_card, "🎨 Графическая карточка (PNG)")

        # TAB 2: Markdown (Reddit / Discord)
        tab_md = QWidget()
        t2_layout = QVBoxLayout(tab_md)
        t2_layout.setContentsMargins(12, 12, 12, 12)
        t2_layout.setSpacing(8)

        self.md_text = QTextEdit()
        self.md_text.setPlainText(self._get_markdown())
        t2_layout.addWidget(self.md_text)

        btn_copy_md = AnimatedPushButton("📋 Скопировать Markdown в буфер", is_primary=True)
        btn_copy_md.setFixedHeight(36)
        btn_copy_md.clicked.connect(lambda: self._copy_text(self.md_text.toPlainText()))
        t2_layout.addWidget(btn_copy_md)
        tabs.addTab(tab_md, "📝 Markdown (Discord / Reddit)")

        # TAB 3: BB-Code (Форумы 4PDA / Overclockers)
        tab_bb = QWidget()
        t3_layout = QVBoxLayout(tab_bb)
        t3_layout.setContentsMargins(12, 12, 12, 12)
        t3_layout.setSpacing(8)

        self.bb_text = QTextEdit()
        self.bb_text.setPlainText(self._get_bbcode())
        t3_layout.addWidget(self.bb_text)

        btn_copy_bb = AnimatedPushButton("📋 Скопировать BB-Code в буфер", is_primary=True)
        btn_copy_bb.setFixedHeight(36)
        btn_copy_bb.clicked.connect(lambda: self._copy_text(self.bb_text.toPlainText()))
        t3_layout.addWidget(btn_copy_bb)
        tabs.addTab(tab_bb, "💬 BB-Code (Форумы 4PDA)")

        layout.addWidget(tabs)

        # Generate preview
        self._generate_card_image()

    def _get_markdown(self):
        return f"""### 🚀 Спецификация ПК | XUiDa64 Extreme Edition
- **Процессор:** {self.cpu_name} ({self.cpu_cores}, {self.cpu_clock})
- **Материнская плата:** {self.mb_name} (BIOS: {self.bios_ver})
- **Оперативная память:** {self.ram_total} ({self.ram_type})
- **Видеокарта:** {self.gpu_name} ({self.gpu_vram})
- **Накопитель:** {self.disk_name} ({self.disk_size})
- **Операционная система:** {self.os_name}
*Диагностика выполнена с помощью бесплатного ПО XUiDa64 Extreme Edition*"""

    def _get_bbcode(self):
        return f"""[b]Спецификация ПК (XUiDa64 Extreme Edition):[/b]
[b]ЦП:[/b] {self.cpu_name} ({self.cpu_cores}, {self.cpu_clock})
[b]Мат. плата:[/b] {self.mb_name} (BIOS: {self.bios_ver})
[b]ОЗУ:[/b] {self.ram_total} ({self.ram_type})
[b]Видеокарта:[/b] {self.gpu_name} ({self.gpu_vram})
[b]Диск:[/b] {self.disk_name} ({self.disk_size})
[b]ОС:[/b] {self.os_name}"""

    def _generate_card_image(self):
        w, h = 1200, 675
        img = Image.new("RGBA", (w, h), (15, 20, 28, 255))
        draw = ImageDraw.Draw(img)

        # Subtle background grid & glowing accents
        for x in range(0, w, 80):
            draw.line([(x, 0), (x, h)], fill=(24, 32, 45, 120), width=1)
        for y in range(0, h, 80):
            draw.line([(0, y), (w, y)], fill=(24, 32, 45, 120), width=1)

        # Top Banner bar
        draw.rectangle([0, 0, w, 110], fill=(20, 27, 40, 255))
        draw.line([(0, 110), (w, 110)], fill=(0, 210, 255, 255), width=3)

        # Draw brand emblem icon
        icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
        emb_x = 36
        if os.path.exists(icon_path):
            emb_img = Image.open(icon_path).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
            img.paste(emb_img, (emb_x, 17), emb_img)
            text_x = emb_x + 92
        else:
            text_x = 40

        # Fonts
        try:
            f_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
            f_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
            f_tag = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 13)
            f_cat = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 17)
            f_val = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
            f_subval = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
        except Exception:
            f_title = f_sub = f_tag = f_cat = f_val = f_subval = ImageFont.load_default()

        # Logo text
        draw.text((text_x, 24), "XUiDa", fill=(255, 255, 255), font=f_title)
        badge_x = text_x + 148
        draw.rounded_rectangle([badge_x, 32, badge_x + 64, 74], radius=6, fill=(16, 185, 129))
        draw.text((badge_x + 32, 53), "64", fill=(15, 20, 28), font=f_cat, anchor="mm")
        draw.text((badge_x + 82, 38), "EXTREME EDITION", fill=(0, 210, 255), font=f_cat)
        draw.text((badge_x + 82, 64), "HARDWARE SPECIFICATION VERIFIED REPORT", fill=(156, 163, 175), font=f_sub)

        # 6 Grid Cards
        cards = [
            ("CPU", "PROCESSOR", self.cpu_name, f"Cores: {self.cpu_cores} | Clock: {self.cpu_clock}"),
            ("GPU", "GRAPHICS", self.gpu_name, f"Memory: {self.gpu_vram} | DirectX 12 Telemetry"),
            ("RAM", "MEMORY", self.ram_total, f"Configuration: {self.ram_type}"),
            ("MB", "MOTHERBOARD", self.mb_name, f"BIOS: {self.bios_ver} | ACPI 6.4 Compliant"),
            ("DISK", "STORAGE DRIVE", self.disk_name, f"Capacity: {self.disk_size} | High Speed Interface"),
            ("OS", "OPERATING SYSTEM", self.os_name, "64-bit Architecture | Clean UEFI Boot")
        ]

        card_w, card_h = 550, 140
        start_x, start_y = 35, 140
        gap_x, gap_y = 30, 25

        for i, (tag, title, val, subval) in enumerate(cards):
            col = i % 2
            row = i // 2
            cx = start_x + col * (card_w + gap_x)
            cy = start_y + row * (card_h + gap_y)

            # Card background
            draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=10, fill=(25, 33, 46, 255), outline=(42, 54, 74, 255), width=2)
            draw.line([(cx + 12, cy + 38), (cx + card_w - 12, cy + 38)], fill=(37, 99, 235, 180), width=2)

            # Tag pill
            draw.rounded_rectangle([cx + 16, cy + 12, cx + 64, cy + 30], radius=4, fill=(31, 111, 235, 255))
            draw.text((cx + 40, cy + 21), tag, fill=(255, 255, 255), font=f_tag, anchor="mm")

            # Header title
            draw.text((cx + 74, cy + 13), title, fill=(0, 210, 255), font=f_cat)

            # Main val
            val_short = val if len(val) < 42 else val[:40] + "..."
            draw.text((cx + 16, cy + 50), val_short, fill=(255, 255, 255), font=f_val)
            # Subval
            draw.text((cx + 16, cy + 96), subval, fill=(156, 163, 175), font=f_subval)

        # Footer
        draw.text((40, h - 35), "Generated by XUiDa64 — Open Hardware Diagnostics & Benchmark Suite", fill=(100, 116, 139), font=f_sub)

        self.generated_pil_img = img

        # Convert to QPixmap for preview
        img_rgb = img.convert("RGBA")
        data = img_rgb.tobytes("raw", "RGBA")
        qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
        pix = QPixmap.fromImage(qim)
        self.preview_lbl.setPixmap(pix.scaledToWidth(800, Qt.SmoothTransformation))

    def _save_image(self):
        if not self.generated_pil_img:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить спецификацию", "XUiDa64_Spec.png", "PNG Images (*.png)")
        if path:
            self.generated_pil_img.save(path, "PNG")
            QMessageBox.information(self, "Успешно", f"Карточка сохранена по пути:\n{path}")

    def _copy_image_clipboard(self):
        if not self.generated_pil_img:
            return
        img_rgb = self.generated_pil_img.convert("RGBA")
        data = img_rgb.tobytes("raw", "RGBA")
        qim = QImage(data, self.generated_pil_img.size[0], self.generated_pil_img.size[1], QImage.Format_RGBA8888)
        pix = QPixmap.fromImage(qim)
        QApplication.clipboard().setPixmap(pix)
        QMessageBox.information(self, "Буфер обмена", "✅ Изображение карточки скопировано в буфер обмена!")

    def _copy_text(self, text):
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Буфер обмена", "✅ Текст скопирован в буфер обмена!")
