import os
import sys
import time

os.environ["XUIDA_DEMO_MODE"] = "1"

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from core.i18n import I18N
from gui.styles import apply_dark_palette
from gui.main_window import MainWindow
from gui.dialogs.disk_bench_dialog import DiskBenchDialog
from gui.dialogs.gpu_bench_dialog import GPUBenchDialog
from gui.dialogs.sensor_panel import DesktopSensorPanel
from gui.dialogs.share_dialog import ShareConfigDialog

def capture():
    app = QApplication(sys.argv)
    apply_dark_palette(app)
    I18N.set_language('ru')

    win = MainWindow()
    win.resize(1200, 800)
    win.show()
    app.processEvents()

    os.makedirs('assets/preview_suite', exist_ok=True)

    # 1. Summary View
    win._select_tree_item('Summary')
    win.summary_view.refresh_data()
    win._update_status_bar()
    app.processEvents()
    for _ in range(10):
        app.processEvents()
        time.sleep(0.03)
    win.grab().save('assets/preview_suite/1_summary.png')
    print('Saved assets/preview_suite/1_summary.png')

    # 2. Sensors View
    win._select_tree_item('Sensors')
    win.sensor_view.update_sensors()
    win._update_status_bar()
    app.processEvents()
    for _ in range(25):
        app.processEvents()
        time.sleep(0.03)
    win.grab().save('assets/preview_suite/2_sensors.png')
    print('Saved assets/preview_suite/2_sensors.png')

    # 3. Cleaner View
    win._select_tree_item('System Cleaner')
    win.cleaner_view.chip_junk.set_value("4.82 ГБ")
    win.cleaner_view.chip_junk.set_subtitle("Найдено к удалению")
    win.cleaner_view.chip_files.set_value("1,248")
    win.cleaner_view.chip_files.set_subtitle("Временные файлы")
    win.cleaner_view.clean_btn.setEnabled(True)
    win.cleaner_view.clean_btn.setText("🧹 Очистить мусор (4.82 ГБ)")
    
    # Mock row item counts in cleaner table
    table = win.cleaner_view.table
    mock_sizes = [
        ("12", "2.14 ГБ"),
        ("942", "1.85 ГБ"),
        ("164", "480.0 МБ"),
        ("96", "240.5 МБ"),
        ("34", "112.0 МБ")
    ]
    for r in range(min(len(mock_sizes), table.rowCount())):
        table.item(r, 2).setText(mock_sizes[r][0])
        table.item(r, 3).setText(mock_sizes[r][1])

    win._update_status_bar()
    app.processEvents()
    for _ in range(10):
        app.processEvents()
        time.sleep(0.03)
    win.grab().save('assets/preview_suite/3_cleaner.png')
    print('Saved assets/preview_suite/3_cleaner.png')

    # 4. Benchmark View
    win._select_tree_item('Memory Read')
    win._update_status_bar()
    app.processEvents()
    for _ in range(30):
        app.processEvents()
        time.sleep(0.03)
    win.grab().save('assets/preview_suite/4_benchmark_settled.png')
    print('Saved assets/preview_suite/4_benchmark_settled.png')

    # 5. Disk Benchmark Dialog
    disk_dlg = DiskBenchDialog()
    disk_dlg.show()
    app.processEvents()
    for _ in range(10):
        app.processEvents()
        time.sleep(0.02)
    disk_dlg.grab().save('assets/disk_bench_preview.png')
    disk_dlg.close()
    print('Saved assets/disk_bench_preview.png')

    # 6. GPU Benchmark Dialog
    gpu_dlg = GPUBenchDialog()
    gpu_dlg.show()
    app.processEvents()
    for _ in range(10):
        app.processEvents()
        time.sleep(0.02)
    gpu_dlg.grab().save('assets/gpu_bench_preview.png')
    gpu_dlg.close()
    print('Saved assets/gpu_bench_preview.png')

    # 7. Share Dialog Preview
    share_dlg = ShareConfigDialog()
    share_dlg.resize(920, 680)
    share_dlg.show()
    app.processEvents()
    for _ in range(10):
        app.processEvents()
        time.sleep(0.02)
    share_dlg.grab().save('assets/share_preview.png')
    share_dlg.close()
    print('Saved assets/share_preview.png')

    # 8. In-Game HUD Preview
    hud = DesktopSensorPanel()
    hud.update_telemetry()
    hud.show()
    app.processEvents()
    for _ in range(10):
        app.processEvents()
        time.sleep(0.02)
    hud.grab().save('assets/preview_in_game_hud.png')
    hud.close()
    print('Saved assets/preview_in_game_hud.png')

    win.close()
    print('All preview screenshots regenerated successfully!')

if __name__ == '__main__':
    capture()
