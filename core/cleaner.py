"""
XUiDa64 - System Cleaner & Disk Optimizer Engine
Provides safe, multi-threaded scanning and cleanup of temporary files,
browser caches, crash dumps, Windows error logs, and Recycle Bin.
"""

import os
import glob
import shutil
import ctypes
from typing import List, Dict, Callable, Optional

class SystemCleaner:
    @staticmethod
    def get_cleanable_categories() -> List[Dict]:
        """
        Returns list of cleanable system & browser cache categories with paths.
        """
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        app_data = os.environ.get("APPDATA", "")
        temp_dir = os.environ.get("TEMP", "")
        windir = os.environ.get("WINDIR", "C:\\Windows")

        categories = [
            {
                "id": "recycle_bin",
                "name": "Корзина Windows",
                "desc": "Удаленные файлы в системной корзине",
                "icon": "🗑️",
                "type": "recycle_bin",
                "paths": [],
                "default": True
            },
            {
                "id": "user_temp",
                "name": "Временные файлы пользователя (Temp)",
                "desc": f"Кэш и остатки программ в {temp_dir}",
                "icon": "📁",
                "type": "directory",
                "paths": [temp_dir] if temp_dir and os.path.exists(temp_dir) else [],
                "default": True
            },
            {
                "id": "sys_temp",
                "name": "Системные временные файлы Windows",
                "desc": f"Устаревшие системные файлы в {os.path.join(windir, 'Temp')}",
                "icon": "⚙️",
                "type": "directory",
                "paths": [os.path.join(windir, "Temp")] if os.path.exists(os.path.join(windir, "Temp")) else [],
                "default": True
            },
            {
                "id": "browser_edge",
                "name": "Кэш Microsoft Edge",
                "desc": "Временные интернет-файлы, веб-кэш и медиаданные Edge",
                "icon": "🌐",
                "type": "directory",
                "paths": [
                    os.path.join(local_app_data, "Microsoft", "Edge", "User Data", "Default", "Cache"),
                    os.path.join(local_app_data, "Microsoft", "Edge", "User Data", "Default", "Code Cache")
                ],
                "default": True
            },
            {
                "id": "browser_chrome",
                "name": "Кэш Google Chrome",
                "desc": "Кэшированные веб-страницы и медиафайлы Chrome",
                "icon": "🌐",
                "type": "directory",
                "paths": [
                    os.path.join(local_app_data, "Google", "Chrome", "User Data", "Default", "Cache"),
                    os.path.join(local_app_data, "Google", "Chrome", "User Data", "Default", "Code Cache")
                ],
                "default": True
            },
            {
                "id": "browser_yandex",
                "name": "Кэш Яндекс Браузера",
                "desc": "Кэш страниц, картинок и скриптов Яндекс.Браузера",
                "icon": "🌐",
                "type": "directory",
                "paths": [
                    os.path.join(local_app_data, "Yandex", "YandexBrowser", "User Data", "Default", "Cache")
                ],
                "default": True
            },
            {
                "id": "crash_dumps",
                "name": "Системные дампы памяти и отчеты об ошибках",
                "desc": "Дампы аварийного завершения приложений (CrashDumps, WER)",
                "icon": "⚠️",
                "type": "directory",
                "paths": [
                    os.path.join(local_app_data, "CrashDumps"),
                    os.path.join(local_app_data, "Microsoft", "Windows", "WER", "ReportArchive"),
                    os.path.join(local_app_data, "Microsoft", "Windows", "WER", "ReportQueue")
                ],
                "default": True
            },
            {
                "id": "win_update",
                "name": "Кэш обновлений Windows (SoftwareDistribution)",
                "desc": "Уже установленные загрузки Центра обновления Windows",
                "icon": "🪟",
                "type": "directory",
                "paths": [
                    os.path.join(windir, "SoftwareDistribution", "Download")
                ],
                "default": False
            },
            {
                "id": "thumb_cache",
                "name": "Кэш эскизов и миниатюр Проводника",
                "desc": "Временный кэш значков и предпросмотра файлов Проводника",
                "icon": "🖼️",
                "type": "directory",
                "paths": [
                    os.path.join(local_app_data, "Microsoft", "Windows", "Explorer")
                ],
                "pattern": "thumbcache_*.db",
                "default": False
            },
            {
                "id": "system_logs",
                "name": "Устаревшие лог-файлы (*.log)",
                "desc": "Журналы инсталляторов и программ в пользовательском каталоге",
                "icon": "📜",
                "type": "directory",
                "paths": [temp_dir] if temp_dir and os.path.exists(temp_dir) else [],
                "pattern": "*.log",
                "default": True
            }
        ]

        # Filter only existing paths
        valid_cats = []
        for cat in categories:
            if cat["type"] == "recycle_bin":
                valid_cats.append(cat)
            else:
                existing_paths = [p for p in cat["paths"] if os.path.exists(p)]
                if existing_paths:
                    cat["paths"] = existing_paths
                    valid_cats.append(cat)

        return valid_cats

    @staticmethod
    def get_recycle_bin_stats() -> tuple:
        """Returns (size_bytes, items_count) of Windows Recycle Bin."""
        try:
            class SHQUERYRBINFO(ctypes.Structure):
                _fields_ = [
                    ('cbSize', ctypes.c_ulong),
                    ('i64Size', ctypes.c_int64),
                    ('i64NumItems', ctypes.c_int64),
                ]
            rbinfo = SHQUERYRBINFO()
            rbinfo.cbSize = ctypes.sizeof(SHQUERYRBINFO)
            res = ctypes.windll.shell32.SHQueryRecycleBinW(None, ctypes.byref(rbinfo))
            if res == 0:
                return max(rbinfo.i64Size, 0), max(rbinfo.i64NumItems, 0)
        except Exception:
            pass
        return 0, 0

    @classmethod
    def scan_category(cls, category: Dict) -> Dict:
        """
        Scans a single category and returns size in bytes and number of files.
        """
        cat_id = category.get("id")
        cat_type = category.get("type")
        pattern = category.get("pattern")
        total_size = 0
        total_files = 0

        if cat_type == "recycle_bin":
            size, count = cls.get_recycle_bin_stats()
            total_size = size
            total_files = count
        else:
            paths = category.get("paths", [])
            for folder in paths:
                if not os.path.exists(folder):
                    continue

                if pattern:
                    # Scan with pattern e.g. *.log or thumbcache_*.db
                    try:
                        matches = glob.glob(os.path.join(folder, pattern))
                        for f in matches:
                            if os.path.isfile(f):
                                try:
                                    total_size += os.path.getsize(f)
                                    total_files += 1
                                except Exception:
                                    pass
                    except Exception:
                        pass
                else:
                    # Scan all files recursively
                    for root, dirs, files in os.walk(folder):
                        for f in files:
                            total_files += 1
                            fp = os.path.join(root, f)
                            try:
                                total_size += os.path.getsize(fp)
                            except Exception:
                                pass

        return {
            "id": cat_id,
            "name": category.get("name"),
            "desc": category.get("desc"),
            "icon": category.get("icon"),
            "size_bytes": total_size,
            "files_count": total_files,
            "paths": category.get("paths", []),
            "type": cat_type,
            "pattern": pattern
        }

    @classmethod
    def clean_category(cls, category: Dict, log_callback: Optional[Callable[[str], None]] = None) -> tuple:
        """
        Cleans files in a single category safely.
        Returns (freed_bytes, deleted_files, failed_files).
        """
        cat_id = category.get("id")
        cat_type = category.get("type")
        pattern = category.get("pattern")
        paths = category.get("paths", [])

        freed_bytes = 0
        deleted_files = 0
        failed_files = 0

        if cat_type == "recycle_bin":
            size, count = cls.get_recycle_bin_stats()
            try:
                # SHERB_NOCONFIRMATION (0x01) | SHERB_NOPROGRESSUI (0x02) | SHERB_NOSOUND (0x04) = 0x07
                res = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000007)
                if res == 0:
                    freed_bytes += size
                    deleted_files += count
                    if log_callback:
                        log_callback(f"✔ Очищена корзина Windows: освобождено {cls.format_size(size)}")
                else:
                    failed_files += 1
            except Exception as e:
                failed_files += 1
                if log_callback:
                    log_callback(f"✖ Ошибка очистки корзины: {e}")
            return freed_bytes, deleted_files, failed_files

        for folder in paths:
            if not os.path.exists(folder):
                continue

            if pattern:
                matches = glob.glob(os.path.join(folder, pattern))
                for f in matches:
                    if os.path.isfile(f):
                        try:
                            sz = os.path.getsize(f)
                            os.remove(f)
                            freed_bytes += sz
                            deleted_files += 1
                        except Exception:
                            failed_files += 1
            else:
                for root, dirs, files in os.walk(folder, topdown=False):
                    for f in files:
                        fp = os.path.join(root, f)
                        try:
                            sz = os.path.getsize(fp)
                            os.remove(fp)
                            freed_bytes += sz
                            deleted_files += 1
                        except Exception:
                            failed_files += 1

                    # Attempt to remove empty child subdirectories (keep the root folder intact)
                    for d in dirs:
                        dp = os.path.join(root, d)
                        if dp != folder:
                            try:
                                os.rmdir(dp)
                            except Exception:
                                pass

        if log_callback:
            log_callback(f"✔ {category.get('name')}: удалено {deleted_files} файлов ({cls.format_size(freed_bytes)})")

        return freed_bytes, deleted_files, failed_files

    @staticmethod
    def format_size(bytes_val: float) -> str:
        """Formats bytes into human readable KB, MB, GB."""
        if bytes_val <= 0:
            return "0 Б"
        for unit in ["Б", "КБ", "МБ", "ГБ"]:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} ТБ"
