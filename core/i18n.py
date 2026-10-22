"""
XUiDa64 - Internationalization & Localization Engine (i18n)
Supports English (en), Русский (ru), Deutsch (de), and 简体中文 (zh).
"""

import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

TRANSLATIONS = {
    "en": {
        # App
        "app_title": "XUiDa64 Extreme Edition [Community Free & Open Source]",
        "app_subtitle": "Hardware Diagnostics & Benchmark Suite",
        "ready": "Ready",
        "hardware": "Hardware",
        "cpu_usage": "CPU",
        "ram_usage": "RAM",

        # Menu
        "menu_file": "&File",
        "menu_view": "&View",
        "menu_tools": "&Tools",
        "menu_language": "&Language",
        "menu_help": "&Help",

        # Actions
        "act_report": "📑 Report Wizard...",
        "act_refresh": "🔄 Refresh Hardware",
        "act_exit": "Exit",
        "act_osd": "📊 Sensor Desktop OSD",
        "act_theme": "🌓 Toggle Dark / Light Theme",
        "act_cpuid": "⚡ AIDA64 CPUID Utility...",
        "act_stress": "🔥 System Stability Test...",
        "act_bench": "🏆 Memory & CPU Benchmarks",
        "act_disk_bench": "💾 Disk Benchmark (Storage Speed)...",
        "act_gpu_bench": "🎮 GPGPU Compute Benchmark...",
        "act_monitor_diag": "🖥️ Monitor Diagnostics (Dead Pixels)...",
        "act_share": "📸 Share PC Configuration...",
        "act_github": "🌐 GitHub Project Repository",
        "act_about": "ℹ About XUiDa64",

        # Toolbar
        "tb_report": "📑 Report Wizard",
        "tb_cpuid": "⚡ CPUID",
        "tb_stress": "🔥 Stability Test",
        "tb_benchmarks": "🏆 Benchmarks",
        "tb_disk_bench": "💾 Disk Bench",
        "tb_gpu_bench": "🎮 GPU Bench",
        "tb_monitor": "🖥️ Monitor",
        "tb_share": "📸 Share PC",
        "tb_sensor_osd": "📊 Sensor OSD",
        "tb_refresh": "🔄 Refresh",
        "tb_theme": "🌓 Theme",

        # Tree Categories
        "cat_computer": "🖥️ Computer",
        "cat_motherboard": "⚡ Motherboard",
        "cat_os": "🪟 Operating System",
        "cat_display": "🎮 Display",
        "cat_storage": "💾 Storage",
        "cat_network": "🌐 Network",
        "cat_devices": "🔌 Devices",
        "cat_software": "📦 Software",
        "cat_benchmarks": "🏆 Benchmark",

        # Tree Items
        "nav_summary": "Summary",
        "nav_computer_name": "Computer Name",
        "nav_power": "Power Management",
        "nav_battery": "Battery & Mobile Power",
        "nav_sensors": "Sensors",
        "nav_cpu": "CPU",
        "nav_cpuid": "CPUID",
        "nav_mb": "Motherboard",
        "nav_memory": "Memory",
        "nav_spd": "SPD",
        "nav_bios": "BIOS",
        "nav_os_info": "OS Info",
        "nav_processes": "Processes",
        "nav_services": "System Services",
        "nav_uptime": "Uptime",
        "nav_gpus": "Video Adapters",
        "nav_monitors": "Monitors",
        "nav_logical_drives": "Logical Drives",
        "nav_physical_drives": "Physical Drives",
        "nav_smart": "SMART",
        "nav_network_adapters": "Network Adapters",
        "nav_traffic": "Traffic Monitor",
        "nav_devices": "Windows Devices",
        "nav_programs": "Installed Programs",
        "nav_startup": "Startup Programs",

        # Summary Sections
        "sec_computer": "Computer Summary",
        "sec_motherboard": "Motherboard",
        "sec_display": "Display",
        "sec_storage": "Storage",
        "sec_network": "Network",

        # Common Table Headers
        "col_field": "Field",
        "col_value": "Value",
        "col_sensor": "Sensor",
        "col_unit": "Unit",
        "col_category": "Category",
        "col_pid": "PID",
        "col_name": "Process Name",
        "col_cpu_pct": "CPU %",
        "col_mem_mb": "Memory (MB)",
        "col_threads": "Threads",
        "col_user": "User",
        "col_status": "Status",

        # Benchmarks
        "bench_select": "Benchmark:",
        "bench_run": "▶ Run Benchmark",
        "bench_running": "Running test...",
        "bench_not_run": "Result: Not benchmarked yet",
        "bench_result": "Result: {val}",
        "bench_this_pc": "(This Computer)",

        # Sensors
        "sensor_header": "Hardware Monitor & Real-Time Sensors",
        "sensor_pause": "⏸ Pause Updates",
        "sensor_resume": "▶ Resume Updates",
        "sensor_all": "All Sensors",
        "sensor_temp": "Temperatures",
        "sensor_fan": "Fans",
        "sensor_power": "Power",
        "sensor_clock": "Clocks",
        "sensor_usage": "Usage",

        # Processes
        "proc_filter": "🔍 Filter processes (type to search)...",
        "proc_refresh": "🔄 Refresh",
        "proc_kill": "⏹ End Process",
        "proc_kill_confirm": "Are you sure you want to kill process {name} (PID {pid})?",
        "proc_count": "Total Processes: {count}",

        # Stability Test
        "stress_title": "XUiDa64 - System Stability Test",
        "stress_status_ready": "Status: System Ready (Idle)",
        "stress_status_running": "Status: Stressing System... (Monitoring)",
        "stress_status_stopped": "Status: Test Stopped",
        "stress_throttling": "⚠️ WARNING: CPU THERMAL THROTTLING DETECTED!",
        "stress_time_elapsed": "Time Elapsed: {time}",
        "stress_start": "▶ Start Test",
        "stress_stop": "⏹ Stop Test",
        "stress_clear": "🗑 Clear",
        "stress_close": "Close",
        "stress_chk_cpu": "Stress CPU",
        "stress_chk_fpu": "Stress FPU",
        "stress_chk_cache": "Stress Cache",
        "stress_chk_mem": "Stress System Memory",
        "stress_chk_gpu": "Stress GPU",

        # Report Wizard
        "rep_title": "System Diagnostic Report Wizard",
        "rep_desc": "Select report format and destination file:",
        "rep_html": "HTML Report (Interactive, styled document)",
        "rep_txt": "Plain Text Report (Classic ASCII layout)",
        "rep_json": "JSON Data Export (Machine readable raw data)",
        "rep_browse": "Browse...",
        "rep_open_finished": "Open report automatically after generation",
        "rep_generate": "Generate Report",
        "rep_generating": "Generating...",
        "rep_cancel": "Cancel",
        "rep_success": "Report successfully generated at:\n{path}",

        # CPUID Dialog
        "cpuid_title": "XUiDa64 CPUID",
        "cpuid_clocks": "Clocks & Multipliers",
        "cpuid_core_speed": "Core Speed",
        "cpuid_multiplier": "Multiplier",
        "cpuid_bus_speed": "Bus Speed",
        "cpuid_voltage": "Core Voltage",
        "cpuid_signature": "Processor Signature",
        "cpuid_family": "Family",
        "cpuid_model": "Model",
        "cpuid_stepping": "Stepping",
        "cpuid_instructions": "Supported Instruction Sets",
        "cpuid_caches": "Caches",
        "cpuid_refresh": "🔄 Refresh",
        "cpuid_close": "Close",

        # About Dialog
        "about_title": "About XUiDa64 Extreme Edition",
        "about_ver": "Version 1.0.0 (Community Open Source Edition)",
        "about_desc": "The premier free, open-source alternative to AIDA64 Extreme.\nProvides in-depth hardware diagnostics, real-time sensor monitoring,\nCPU & memory benchmarking, system stability testing and reporting.",
        "about_feat1": "✔ Direct x86-64 CPUID instruction engine (no drivers needed)",
        "about_feat2": "✔ High-speed multi-threaded memory & CPU benchmarks",
        "about_feat3": "✔ Real-time ACPI, NVML GPU & hardware sensor telemetry",
        "about_feat4": "✔ System Stability Stress Testing with thermal throttling alerts",
        "about_feat5": "✔ Full HTML, TXT, and JSON report generation",
        "about_license": "Released under the permissive MIT License. Free for all.",

        # Filter & Search
        "filter_placeholder": "🔍 Filter properties (type to search)...",
        "copy_all": "📋 Copy All",
        "copy_value": "Copy Value",
        "copy_row": "Copy Row",
        "copy_table": "Copy Entire Table",
        "items_count": "Found: {count}"
    },
    "ru": {
        # App
        "app_title": "XUiDa64 Extreme Edition [Бесплатная версия с открытым кодом]",
        "app_subtitle": "Диагностика оборудования и комплекс бенчмарков",
        "ready": "Готов",
        "hardware": "Оборудование",
        "cpu_usage": "ЦП",
        "ram_usage": "ОЗУ",

        # Menu
        "menu_file": "&Файл",
        "menu_view": "&Вид",
        "menu_tools": "&Сервис",
        "menu_language": "&Язык (Language)",
        "menu_help": "&Справка",

        # Actions
        "act_report": "📑 Мастер отчетов...",
        "act_refresh": "🔄 Обновить данные",
        "act_exit": "Выход",
        "act_osd": "📊 Экранный OSD-виджет",
        "act_theme": "🌓 Переключить тему (Темная / Светлая)",
        "act_cpuid": "⚡ Утилита AIDA64 CPUID...",
        "act_stress": "🔥 Стресс-тест стабильности системы...",
        "act_bench": "🏆 Бенчмарки памяти и процессора",
        "act_disk_bench": "💾 Тест накопителей (Disk Benchmark)...",
        "act_gpu_bench": "🎮 Бенчмарк вычислений GPU (GPGPU)...",
        "act_monitor_diag": "🖥️ Диагностика монитора (Битые пиксели)...",
        "act_share": "📸 Поделиться конфигурацией ПК...",
        "act_github": "🌐 Репозиторий проекта на GitHub",
        "act_about": "ℹ О программе XUiDa64",

        # Toolbar
        "tb_report": "📑 Отчет",
        "tb_cpuid": "⚡ CPUID",
        "tb_stress": "🔥 Стресс-тест",
        "tb_benchmarks": "🏆 Бенчмарки",
        "tb_disk_bench": "💾 Диски",
        "tb_gpu_bench": "🎮 GPU Тест",
        "tb_monitor": "🖥️ Монитор",
        "tb_share": "📸 Поделиться",
        "tb_sensor_osd": "📊 OSD Панель",
        "tb_refresh": "🔄 Обновить",
        "tb_theme": "🌓 Тема",

        # Tree Categories
        "cat_computer": "🖥️ Компьютер",
        "cat_motherboard": "⚡ Системная плата",
        "cat_os": "🪟 Операционная система",
        "cat_display": "🎮 Отображение",
        "cat_storage": "💾 Хранение данных",
        "cat_network": "🌐 Сеть",
        "cat_devices": "🔌 Устройства",
        "cat_software": "📦 Программы",
        "cat_benchmarks": "🏆 Бенчмарк",

        # Tree Items
        "nav_summary": "Суммарная информация",
        "nav_computer_name": "Имя компьютера",
        "nav_power": "Электропитание",
        "nav_battery": "Батарея и питание",
        "nav_sensors": "Датчики",
        "nav_cpu": "ЦП (Процессор)",
        "nav_cpuid": "CPUID",
        "nav_mb": "Системная плата",
        "nav_memory": "Память",
        "nav_spd": "SPD (Модули памяти)",
        "nav_bios": "BIOS",
        "nav_os_info": "Сведения об ОС",
        "nav_processes": "Процессы",
        "nav_services": "Службы Windows",
        "nav_uptime": "Время работы",
        "nav_gpus": "Видеоадаптеры",
        "nav_monitors": "Мониторы",
        "nav_logical_drives": "Логические диски",
        "nav_physical_drives": "Физические накопители",
        "nav_smart": "SMART статус",
        "nav_network_adapters": "Сетевые адаптеры",
        "nav_traffic": "Монитор трафика",
        "nav_devices": "Устройства Windows",
        "nav_programs": "Установленные программы",
        "nav_startup": "Автозагрузка",

        # Summary Sections
        "sec_computer": "Сводка компьютера",
        "sec_motherboard": "Системная плата",
        "sec_display": "Отображение",
        "sec_storage": "Хранение данных",
        "sec_network": "Сеть",

        # Common Table Headers
        "col_field": "Свойство",
        "col_value": "Значение",
        "col_sensor": "Датчик",
        "col_unit": "Ед. изм.",
        "col_category": "Категория",
        "col_pid": "PID",
        "col_name": "Имя процесса",
        "col_cpu_pct": "ЦП %",
        "col_mem_mb": "Память (МБ)",
        "col_threads": "Потоки",
        "col_user": "Пользователь",
        "col_status": "Статус",

        # Benchmarks
        "bench_select": "Тест производительности:",
        "bench_run": "▶ Запустить тест",
        "bench_running": "Идет тестирование...",
        "bench_not_run": "Результат: Еще не тестировался",
        "bench_result": "Результат: {val}",
        "bench_this_pc": "(Этот компьютер)",

        # Sensors
        "sensor_header": "Мониторинг оборудования и датчики в реальном времени",
        "sensor_pause": "⏸ Приостановить",
        "sensor_resume": "▶ Возобновить",
        "sensor_all": "Все датчики",
        "sensor_temp": "Температуры",
        "sensor_fan": "Вентиляторы",
        "sensor_power": "Мощность (Вт)",
        "sensor_clock": "Частоты",
        "sensor_usage": "Загрузка",

        # Processes
        "proc_filter": "🔍 Фильтр процессов (введите название)...",
        "proc_refresh": "🔄 Обновить",
        "proc_kill": "⏹ Завершить процесс",
        "proc_kill_confirm": "Вы уверены, что хотите завершить процесс {name} (PID {pid})?",
        "proc_count": "Всего процессов: {count}",

        # Stability Test
        "stress_title": "XUiDa64 - Стресс-тест стабильности системы",
        "stress_status_ready": "Статус: Система готова (Ожидание)",
        "stress_status_running": "Статус: Нагрузка системы... (Мониторинг)",
        "stress_status_stopped": "Статус: Тест остановлен",
        "stress_throttling": "⚠️ ВНИМАНИЕ: ОБНАРУЖЕН ТЕРМИЧЕСКИЙ ТРОТТЛИНГ ЦП!",
        "stress_time_elapsed": "Прошло времени: {time}",
        "stress_start": "▶ Старт",
        "stress_stop": "⏹ Стоп",
        "stress_clear": "🗑 Очистить",
        "stress_close": "Закрыть",
        "stress_chk_cpu": "Нагрузка ЦП",
        "stress_chk_fpu": "Нагрузка FPU",
        "stress_chk_cache": "Нагрузка кэша",
        "stress_chk_mem": "Нагрузка системной памяти",
        "stress_chk_gpu": "Нагрузка ГП",

        # Report Wizard
        "rep_title": "Мастер отчетов о диагностике системы",
        "rep_desc": "Выберите формат отчета и путь к файлу:",
        "rep_html": "HTML-отчет (Интерактивный, со стилями и таблицами)",
        "rep_txt": "Текстовый отчет TXT (Классический ASCII вид)",
        "rep_json": "Экспорт JSON (Структурированные сырые данные)",
        "rep_browse": "Обзор...",
        "rep_open_finished": "Открыть отчет сразу после создания",
        "rep_generate": "Создать отчет",
        "rep_generating": "Создание...",
        "rep_cancel": "Отмена",
        "rep_success": "Отчет успешно создан по адресу:\n{path}",

        # CPUID Dialog
        "cpuid_title": "XUiDa64 CPUID",
        "cpuid_clocks": "Частоты и множители",
        "cpuid_core_speed": "Частота ядра",
        "cpuid_multiplier": "Множитель",
        "cpuid_bus_speed": "Частота шины",
        "cpuid_voltage": "Напряжение ядра",
        "cpuid_signature": "Сигнатура процессора",
        "cpuid_family": "Семейство",
        "cpuid_model": "Модель",
        "cpuid_stepping": "Степпинг",
        "cpuid_instructions": "Поддерживаемые наборы инструкций",
        "cpuid_caches": "Кэш-память",
        "cpuid_refresh": "🔄 Обновить",
        "cpuid_close": "Закрыть",

        # About Dialog
        "about_title": "О программе XUiDa64 Extreme Edition",
        "about_ver": "Версия 1.0.0 (Свободное издание с открытым кодом)",
        "about_desc": "Полноценный бесплатный аналог AIDA64 Extreme.\nГлубокая диагностика оборудования, аппаратные датчики в реальном времени,\nбенчмаркинг памяти и процессора, стресс-тестирование стабильности и отчеты.",
        "about_feat1": "✔ Прямое исполнение CPUID в машинном коде x86-64 (без драйверов)",
        "about_feat2": "✔ Высокоскоростные многопоточные бенчмарки ОЗУ и процессора",
        "about_feat3": "✔ Телеметрия ACPI, NVIDIA NVML, частоты, ватты и температуры",
        "about_feat4": "✔ Стресс-тест стабильности системы с детекцией троттлинга",
        "about_feat5": "✔ Экспорт отчетов в HTML, TXT и JSON",
        "about_license": "Распространяется под свободной лицензией MIT. Доступно для всех.",

        # Filter & Search
        "filter_placeholder": "🔍 Фильтр свойств (введите текст)...",
        "copy_all": "📋 Скопировать всё",
        "copy_value": "Копировать значение",
        "copy_row": "Копировать строку",
        "copy_table": "Копировать всю таблицу",
        "items_count": "Найдено: {count}"
    },
    "de": {
        # App
        "app_title": "XUiDa64 Extreme Edition [Kostenlose Open-Source-Edition]",
        "app_subtitle": "Hardware-Diagnose und Benchmark-Suite",
        "ready": "Bereit",
        "hardware": "Hardware",
        "cpu_usage": "CPU",
        "ram_usage": "RAM",

        # Menu
        "menu_file": "&Datei",
        "menu_view": "&Ansicht",
        "menu_tools": "&Werkzeuge",
        "menu_language": "&Sprache (Language)",
        "menu_help": "&Hilfe",

        # Actions
        "act_report": "📑 Berichtsassistent...",
        "act_refresh": "🔄 Hardware aktualisieren",
        "act_exit": "Beenden",
        "act_osd": "📊 Sensor Desktop OSD",
        "act_theme": "🌓 Dunkles / Helles Design umschalten",
        "act_cpuid": "⚡ AIDA64 CPUID Werkzeug...",
        "act_stress": "🔥 Systemstabilitätstest...",
        "act_bench": "🏆 Speicher- und CPU-Benchmarks",
        "act_github": "🌐 GitHub Projekt-Repository",
        "act_about": "ℹ Über XUiDa64",

        # Toolbar
        "tb_report": "📑 Bericht",
        "tb_cpuid": "⚡ CPUID",
        "tb_stress": "🔥 Stabilität",
        "tb_benchmarks": "🏆 Benchmarks",
        "tb_sensor_osd": "📊 Sensor OSD",
        "tb_refresh": "🔄 Aktualisieren",
        "tb_theme": "🌓 Design",

        # Tree Categories
        "cat_computer": "🖥️ Computer",
        "cat_motherboard": "⚡ Motherboard",
        "cat_os": "🪟 Betriebssystem",
        "cat_display": "🎮 Anzeige",
        "cat_storage": "💾 Datenträger",
        "cat_network": "🌐 Netzwerk",
        "cat_devices": "🔌 Geräte",
        "cat_software": "📦 Software",
        "cat_benchmarks": "🏆 Benchmark",

        # Tree Items
        "nav_summary": "Übersicht",
        "nav_computer_name": "Computername",
        "nav_power": "Energieverwaltung",
        "nav_sensors": "Sensoren",
        "nav_cpu": "CPU",
        "nav_cpuid": "CPUID",
        "nav_mb": "Motherboard",
        "nav_memory": "Speicher",
        "nav_spd": "SPD",
        "nav_bios": "BIOS",
        "nav_os_info": "Betriebssystem-Info",
        "nav_processes": "Prozesse",
        "nav_services": "Systemdienste",
        "nav_uptime": "Betriebszeit",
        "nav_gpus": "Grafikkarten",
        "nav_monitors": "Monitore",
        "nav_logical_drives": "Logische Laufwerke",
        "nav_physical_drives": "Physische Laufwerke",
        "nav_smart": "SMART",
        "nav_network_adapters": "Netzwerkadapter",
        "nav_traffic": "Verkehrsüberwachung",
        "nav_devices": "Windows-Geräte",
        "nav_programs": "Installierte Programme",
        "nav_startup": "Autostart",

        # Benchmarks
        "bench_select": "Benchmark:",
        "bench_run": "▶ Benchmark starten",
        "bench_running": "Test läuft...",
        "bench_not_run": "Ergebnis: Noch nicht getestet",
        "bench_result": "Ergebnis: {val}",
        "bench_this_pc": "(Dieser Computer)",

        # Common Table Headers
        "col_field": "Eigenschaft",
        "col_value": "Wert",
        "col_sensor": "Sensor",
        "col_unit": "Einheit",
        "col_category": "Kategorie",
        "col_pid": "PID",
        "col_name": "Prozessname",
        "col_cpu_pct": "CPU %",
        "col_mem_mb": "Speicher (MB)",
        "col_threads": "Threads",
        "col_user": "Benutzer",
        "col_status": "Status",

        # Stability Test
        "stress_title": "XUiDa64 - Systemstabilitätstest",
        "stress_status_ready": "Status: Bereit",
        "stress_status_running": "Status: Test läuft...",
        "stress_status_stopped": "Status: Test beendet",
        "stress_throttling": "⚠️ WARNUNG: CPU-THERMISCHES THROTTLING ERKANNT!",
        "stress_time_elapsed": "Verstrichene Zeit: {time}",
        "stress_start": "▶ Start",
        "stress_stop": "⏹ Stopp",
        "stress_clear": "🗑 Löschen",
        "stress_close": "Schließen",
        "stress_chk_cpu": "CPU auslasten",
        "stress_chk_fpu": "FPU auslasten",
        "stress_chk_cache": "Cache auslasten",
        "stress_chk_mem": "Arbeitsspeicher auslasten",
        "stress_chk_gpu": "GPU auslasten",

        # Filter & Search
        "filter_placeholder": "🔍 Eigenschaften filtern...",
        "copy_all": "📋 Alles kopieren",
        "copy_value": "Wert kopieren",
        "copy_row": "Zeile kopieren",
        "copy_table": "Ganze Tabelle kopieren",
        "items_count": "Gefunden: {count}"
    },
    "zh": {
        # App
        "app_title": "XUiDa64 极致版 [社区免费开源版]",
        "app_subtitle": "硬件诊断与基准测试套件",
        "ready": "就绪",
        "hardware": "硬件",
        "cpu_usage": "处理器",
        "ram_usage": "内存",

        # Menu
        "menu_file": "&文件",
        "menu_view": "&查看",
        "menu_tools": "&工具",
        "menu_language": "&语言 (Language)",
        "menu_help": "&帮助",

        # Actions
        "act_report": "📑 报告向导...",
        "act_refresh": "🔄 刷新硬件",
        "act_exit": "退出",
        "act_osd": "📊 桌面传感器 OSD",
        "act_theme": "🌓 切换深色 / 浅色主题",
        "act_cpuid": "⚡ AIDA64 CPUID 工具...",
        "act_stress": "🔥 系统稳定性测试...",
        "act_bench": "🏆 内存与处理器基准测试",
        "act_github": "🌐 GitHub 项目仓库",
        "act_about": "ℹ 关于 XUiDa64",

        # Toolbar
        "tb_report": "📑 报告向导",
        "tb_cpuid": "⚡ CPUID",
        "tb_stress": "🔥 稳定性测试",
        "tb_benchmarks": "🏆 基准测试",
        "tb_sensor_osd": "📊 传感器 OSD",
        "tb_refresh": "🔄 刷新",
        "tb_theme": "🌓 主题",

        # Tree Categories
        "cat_computer": "🖥️ 计算机",
        "cat_motherboard": "⚡ 主板",
        "cat_os": "🪟 操作系统",
        "cat_display": "🎮 显示设备",
        "cat_storage": "💾 存储设备",
        "cat_network": "🌐 网络",
        "cat_devices": "🔌 设备",
        "cat_software": "📦 软件",
        "cat_benchmarks": "🏆 基准测试",

        # Tree Items
        "nav_summary": "系统摘要",
        "nav_computer_name": "计算机名称",
        "nav_power": "电源管理",
        "nav_sensors": "传感器",
        "nav_cpu": "处理器 (CPU)",
        "nav_cpuid": "CPUID",
        "nav_mb": "主板",
        "nav_memory": "内存",
        "nav_spd": "SPD 信息",
        "nav_bios": "BIOS",
        "nav_os_info": "操作系统信息",
        "nav_processes": "进程管理器",
        "nav_services": "系统服务",
        "nav_uptime": "开机时间",
        "nav_gpus": "显示卡",
        "nav_monitors": "显示器",
        "nav_logical_drives": "逻辑磁盘",
        "nav_physical_drives": "物理硬盘",
        "nav_smart": "SMART 状态",
        "nav_network_adapters": "网络适配器",
        "nav_traffic": "网络流量监控",
        "nav_devices": "Windows 设备管理器",
        "nav_programs": "已安装软件",
        "nav_startup": "开机启动项",

        # Benchmarks
        "bench_select": "基准测试项目:",
        "bench_run": "▶ 开始测试",
        "bench_running": "正在测试...",
        "bench_not_run": "结果: 尚未测试",
        "bench_result": "测试成绩: {val}",
        "bench_this_pc": "(本机系统)",

        # Common Table Headers
        "col_field": "属性",
        "col_value": "数值",
        "col_sensor": "传感器",
        "col_unit": "单位",
        "col_category": "类别",
        "col_pid": "PID",
        "col_name": "进程名称",
        "col_cpu_pct": "CPU %",
        "col_mem_mb": "内存 (MB)",
        "col_threads": "线程数",
        "col_user": "用户",
        "col_status": "状态",

        # Stability Test
        "stress_title": "XUiDa64 - 系统稳定性测试",
        "stress_status_ready": "状态: 准备就绪",
        "stress_status_running": "状态: 压力测试中... (监控中)",
        "stress_status_stopped": "状态: 测试已停止",
        "stress_throttling": "⚠️ 警告: 检测到 CPU 过热降频 (Thermal Throttling)!",
        "stress_time_elapsed": "已运行时间: {time}",
        "stress_start": "▶ 开始",
        "stress_stop": "⏹ 停止",
        "stress_clear": "🗑 清除",
        "stress_close": "关闭",
        "stress_chk_cpu": "压力测试 CPU",
        "stress_chk_fpu": "压力测试 FPU",
        "stress_chk_cache": "压力测试缓存",
        "stress_chk_mem": "压力测试系统内存",
        "stress_chk_gpu": "压力测试 GPU",

        # Filter & Search
        "filter_placeholder": "🔍 筛选属性 (输入关键词)...",
        "copy_all": "📋 复制全部",
        "copy_value": "复制内容",
        "copy_row": "复制整行",
        "copy_table": "复制整个表格",
        "items_count": "已找到: {count}"
    }
}

PROPERTY_TRANSLATIONS = {
    "ru": {
        # System & OS
        "Computer Type": "Тип компьютера",
        "Operating System": "Операционная система",
        "OS Architecture": "Архитектура ОС",
        "Architecture": "Архитектура",
        "Computer Name": "Имя компьютера",
        "ComputerName": "Имя компьютера",
        "NetBIOS Computer Name": "Сетевое имя NetBIOS",
        "User Name": "Имя пользователя",
        "Workgroup / Domain": "Рабочая группа / Домен",
        "System Uptime": "Время работы (Uptime)",
        "System Boot Time": "Время запуска системы",
        "System Current Uptime": "Текущее время работы",
        "System State": "Состояние системы",
        "Install Date": "Дата установки ОС",
        "InstallDate": "Дата установки",
        "Windows System Directory": "Системный каталог Windows",
        "RegisteredUser": "Зарегистрированный пользователь",
        "OSName": "Название ОС",
        "SystemRoot": "Системный диск",
        "BootTime": "Время загрузки",
        "Uptime": "Время непрерывной работы",
        "Build": "Номер сборки ОС (Build)",
        "DisplayVersion": "Версия выпуска Windows",
        "FormFactor": "Форм-фактор платформы",

        # CPU & Instructions
        "CPU Type": "Тип процессора (ЦП)",
        "CPU Clock": "Частота процессора",
        "Brand": "Модель процессора",
        "Vendor": "Производитель",
        "Signature": "Сигнатура CPUID",
        "PhysicalCores": "Физических ядер",
        "LogicalCores": "Логических потоков",
        "Socket": "Процессорный сокет",
        "CurrentClock": "Текущая частота",
        "BaseClock": "Базовая частота",
        "MaxClock": "Максимальная частота",
        "Voltage": "Напряжение ядра",
        "Caches": "Кэш-память",
        "CacheList": "Список уровней кэш-памяти",
        "[CACHELIST]": "[ СТРУКТУРА КЭШ-ПАМЯТИ ]",
        "Features": "Поддерживаемые наборы инструкций",
        "[FEATURES]": "[ ПОДДЕРЖИВАЕМЫЕ НАБОРЫ ИНСТРУКЦИЙ ]",
        "True": "Поддерживается (Да)",
        "False": "Не поддерживается (Нет)",
        "Hyper-Threading": "Hyper-Threading (Многопоточность SMT)",
        "Turbo Boost": "Intel Turbo Boost / AMD Precision Boost",
        "Enhanced SpeedStep": "Энергосбережение Enhanced SpeedStep (EIST)",
        "VT-x / AMD-V": "Аппаратная виртуализация VT-x / AMD-V",
        "x64 (EM64T/AMD64)": "64-битные инструкции x86-64 (AMD64/EM64T)",
        "NX / XD (No-Execute)": "Аппаратная защита от атак NX / XD Bit",
        "TSX / RTM": "Транзакционная синхронизация TSX / RTM",
        "MMX": "Векторные инструкции MMX",
        "SSE": "Потоковые SIMD-расширения SSE",
        "SSE2": "Потоковые SIMD-расширения SSE2",
        "SSE3": "Потоковые SIMD-расширения SSE3",
        "SSSE3": "Дополнительные расширения SSSE3",
        "SSE4.1": "Расширения команд SSE4.1",
        "SSE4.2": "Расширения команд SSE4.2",
        "SSE4A": "Расширения команд AMD SSE4A",
        "AVX": "Векторные 256-бит расширения AVX",
        "AVX2": "Векторные инструкции AVX2 (FMA/Gather)",
        "AVX-512F": "Векторные 512-бит инструкции AVX-512F",
        "AVX-512CD": "Детекция конфликтов AVX-512CD",
        "AVX-512ER": "Экспоненциальные функции AVX-512ER",
        "AVX-512PF": "Предвыборка памяти AVX-512PF",
        "AVX-512DQ": "Двойные слова и квадрослова AVX-512DQ",
        "AVX-512BW": "Байтовые и полусловные AVX-512BW",
        "AVX-512VL": "Векторная длина AVX-512VL",
        "FMA3": "Операции умножения-сложения FMA3",
        "FMA4": "Операции умножения-сложения FMA4",
        "AES": "Аппаратное шифрование AES-NI",
        "SHA": "Аппаратное хеширование SHA-NI",
        "CLMUL": "Умножение без переноса CLMUL",
        "BMI1": "Битовые манипуляции BMI1",
        "BMI2": "Битовые манипуляции BMI2",
        "POPCNT": "Подсчет битов POPCNT",
        "LZCNT": "Подсчет старших нулей LZCNT",
        "RDRAND": "Аппаратный генератор чисел RDRAND",
        "RDSEED": "Аппаратный энтропийный генератор RDSEED",
        "SMX": "Доверенное исполнение Intel Safer Mode (SMX)",

        # Motherboard & BIOS
        "Motherboard Name": "Системная плата",
        "Motherboard Chipset": "Чипсет платы",
        "Manufacturer": "Производитель",
        "Product": "Модель платы",
        "Version": "Версия / Ревизия",
        "SerialNumber": "Серийный номер",
        "SystemSlot": "Слоты расширения",
        "Chipset": "Чипсет",
        "BIOS Type": "Тип BIOS",
        "BIOS Release Date": "Дата выпуска BIOS",
        "Boot Mode": "Режим загрузки",
        "BootMode": "Режим загрузки BIOS",
        "SMBIOSVersion": "Версия SMBIOS",
        "SecureBoot": "Безопасная загрузка (Secure Boot)",
        "ReleaseDate": "Дата релиза",

        # Memory & SPD
        "System Memory": "Системная память (ОЗУ)",
        "DIMM Modules": "Модули памяти (DIMM)",
        "TotalPhysical": "Всего физической памяти",
        "AvailablePhysical": "Свободно физической памяти",
        "UsedPhysical": "Занято физической памяти",
        "TotalVirtual": "Всего виртуальной памяти",
        "AvailableVirtual": "Свободно виртуальной памяти",
        "UsedVirtual": "Занято виртуальной памяти",
        "TotalGB": "Всего (ГБ)",
        "UsedGB": "Занято (ГБ)",
        "FreeGB": "Свободно (ГБ)",
        "SwapTotalGB": "Файл подкачки всего (ГБ)",
        "SwapUsedGB": "Файл подкачки занято (ГБ)",
        "SwapFreeGB": "Файл подкачки свободно (ГБ)",
        "SwapPercent": "Использование подкачки (%)",
        "PercentUsed": "Занято памяти (%)",
        "MemoryType": "Тип памяти",
        "CapacityGB": "Емкость модуля (ГБ)",
        "Speed": "Частота памяти",
        "SpeedMHz": "Частота шины (МГц)",
        "PartNumber": "Артикул модуля (Part Number)",
        "DeviceLocator": "Разъем на плате",
        "BankLabel": "Банк памяти (Bank Label)",

        # GPU & Display
        "Video Adapter": "Видеоадаптер (GPU)",
        "Video Driver": "Версия драйвера",
        "Installed VRAM": "Объем видеопамяти",
        "Current Resolution": "Текущее разрешение",
        "Connected Monitor": "Подключенный монитор",
        "Name": "Название",
        "DriverVersion": "Версия драйвера",
        "DriverDate": "Дата драйвера",
        "VRAM_MB": "Видеопамять (МБ)",
        "Resolution": "Разрешение",
        "Temperature": "Температура (°C)",
        "FanSpeed": "Вентилятор (%)",
        "PowerWatts": "Потребление (Вт)",
        "CoreClockMHz": "Частота ядра (МГц)",
        "MemoryClockMHz": "Частота памяти (МГц)",
        "GPUUtil": "Загрузка GPU (%)",
        "Utilization": "Уровень загрузки (%)",
        "Index": "Индекс устройства",

        # Storage
        "Storage Drives": "Физические диски",
        "Partitions": "Разделы дисков",
        "SMART Status": "Статус S.M.A.R.T.",
        "Model": "Модель диска",
        "Size": "Объем",
        "SizeGB": "Объем (ГБ)",
        "Interface": "Интерфейс",
        "BusType": "Тип интерфейса / шины",
        "MediaType": "Тип накопителя",
        "Device": "Дисковый том",
        "Mountpoint": "Точка монтирования",
        "FSType": "Файловая система",
        "Opts": "Параметры",
        "Health": "Состояние диска",
        "Status": "Статус",
        "Healthy / OK": "Исправен (Норма)",
        "OK": "Исправен",

        # Network
        "Primary Network Adapter": "Сетевой адаптер",
        "IP Address": "IP-адрес",
        "IPv4": "IPv4-адрес",
        "IPv6": "IPv6-адрес",
        "MAC Address": "MAC-адрес",
        "MAC": "MAC-адрес",
        "Link Speed": "Скорость канала",
        "Default Gateway": "Основной шлюз",
        "Gateways": "Шлюзы",
        "DNS Servers": "DNS-серверы",
        "DNSServers": "DNS-серверы",
        "Netmask": "Маска подсети",
        "DHCP": "DHCP сервер",
        "Traffic Monitor": "Мониторинг сети",
        "BytesSent": "Отправлено байт",
        "BytesRecv": "Принято байт",

        # Power & Battery
        "Power Device Status": "Устройство питания",
        "System Form Factor": "Тип платформы (Форм-фактор)",
        "Primary Power Source": "Основной источник питания",
        "PowerSource": "Источник питания",
        "PowerScheme": "Схема электропитания",
        "BatteryPercent": "Заряд батареи (%)",
        "BatteryStatus": "Статус батареи",
        "Battery Health / Wear Level": "Износ аккумулятора (Здоровье)",
        "Power Management State": "Энергосбережение",
        "Uninterruptible Power Supply (UPS)": "Резервное питание (ИБП)",
        "Recommended Power Plan": "Схема электропитания",
        "Battery Model": "Модель батареи",
        "Battery Chemistry": "Тип элементов (Химия)",
        "Current Charge Level": "Текущий заряд",
        "Current Power Source": "Текущее питание",
        "Battery Wear Level": "Степень износа",
        "Designed Capacity": "Паспортная емкость",
        "Fully Charged Capacity": "Емкость при полной зарядке",
        "Discharge Rate": "Скорость разряда",
        "Output Voltage": "Выходное напряжение",
        "Estimated Runtime": "Оставшееся время работы",
        "Overheat Thermal Protection": "Защита от перегрева",

        # Benchmarks
        "Memory Read": "Чтение из памяти",
        "Memory Write": "Запись в память",
        "Memory Copy": "Копирование в памяти",
        "Memory Latency": "Задержка памяти (Latency)",
        "CPU Queen": "CPU Queen (Ветвления)",
        "CPU PhotoWorxx": "CPU PhotoWorxx (Матрицы)",
        "CPU ZLib": "CPU ZLib (Сжатие данных)",
        "CPU AES": "CPU AES (Шифрование)",
        "CPU SHA3": "CPU SHA3 (Хеширование)",
        "FPU Julia": "FPU Julia (FP32 фрактал)",
        "FPU Mandel": "FPU Mandel (FP64 фрактал)",
        "FPU SinJulia": "FPU SinJulia (Тригонометрия)",

        # Common & General
        "Installed Programs": "Установленные программы",
        "Startup Programs": "Автозагрузка",
        "Windows Devices": "Диспетчер устройств",
        "System Services": "Службы Windows",
        "Summary": "Суммарная информация",
        "Power Management": "Электропитание",
        "Battery": "Батарея и питание",
        "Battery & Mobile Power": "Батарея и мобильное питание",
        "Sensors": "Датчики",
        "CPU": "ЦП (Процессор)",
        "CPUID": "CPUID",
        "Motherboard": "Системная плата",
        "Memory": "Память",
        "SPD": "SPD (Модули памяти)",
        "BIOS": "BIOS",
        "OS Info": "Информация об ОС",
        "Processes": "Процессы",
        "Uptime": "Время работы",
        "Video Adapters": "Видеоадаптеры",
        "Monitors": "Мониторы",
        "Logical Drives": "Логические диски",
        "Physical Drives": "Физические накопители",
        "SMART": "S.M.A.R.T.",
        "Network Adapters": "Сетевые адаптеры",

        # Software / Services / Devices columns
        "Publisher": "Издатель / Разработчик",
        "DisplayName": "Отображаемое имя",
        "StartType": "Тип запуска",
        "Command": "Команда запуска",
        "Location": "Расположение",
        "Category": "Категория",

        # Sensors & Hardware Monitor
        "Temperatures": "Температуры",
        "Fans": "Вентиляторы",
        "Powers": "Мощность",
        "Clocks": "Частоты",
        "Usage": "Загрузка",
        "CPU Total": "Общая загрузка ЦП",
        "Memory Utilization": "Использование ОЗУ",
        "GPU Core Load": "Загрузка графического ядра",
        "GPU Memory Load": "Загрузка видеопамяти",
        "Download Speed": "Скорость загрузки (Сеть)",
        "Upload Speed": "Скорость отдачи (Сеть)",
        "CPU Core": "Ядро ЦП",
        "CPU Package": "Сокет процессора (Package)",
        "GPU Fan": "Вентилятор видеокарты",
        "GPU Power": "Потребление GPU",

        # Value Statuses
        "Running": "Выполняется",
        "Stopped": "Остановлена",
        "Automatic": "Автоматически",
        "Manual": "Вручную",
        "Disabled": "Отключено",
        "Enabled": "Включено",
        "Paused": "Приостановлена",
        "Unknown": "Неизвестно",
        "AC Power": "От сети (AC)",
        "Fully Operational (Clean Boot)": "Штатный режим (Чистый запуск)"
    }
}

class I18N:
    _current_lang = "ru"  # Default to Russian as requested by user
    _listeners = []

    @classmethod
    def init(cls):
        # Load from config if available
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    cls._current_lang = cfg.get("language", "ru")
            except Exception:
                pass

    @classmethod
    def set_language(cls, lang_code: str):
        if lang_code in TRANSLATIONS:
            cls._current_lang = lang_code
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump({"language": lang_code}, f, indent=2)
            except Exception:
                pass
            for cb in cls._listeners:
                try:
                    cb(lang_code)
                except Exception:
                    pass

    @classmethod
    def get_language(cls) -> str:
        return cls._current_lang

    @classmethod
    def register_listener(cls, callback):
        if callback not in cls._listeners:
            cls._listeners.append(callback)

    @classmethod
    def unregister_listener(cls, callback):
        if callback in cls._listeners:
            cls._listeners.remove(callback)

    @classmethod
    def tr(cls, key: str, **kwargs) -> str:
        lang_dict = TRANSLATIONS.get(cls._current_lang, TRANSLATIONS["en"])
        val = lang_dict.get(key)
        if val is None:
            val = TRANSLATIONS["en"].get(key, key)
        if kwargs:
            try:
                return val.format(**kwargs)
            except Exception:
                return val
        return val

    @classmethod
    def tr_prop(cls, key: str) -> str:
        k = str(key).strip()
        lang = cls._current_lang
        if lang in PROPERTY_TRANSLATIONS and k in PROPERTY_TRANSLATIONS[lang]:
            return PROPERTY_TRANSLATIONS[lang][k]
        val = cls.tr(k)
        if val != k:
            return val
        return k

# Global shortcut functions
def _t(key: str, **kwargs) -> str:
    return I18N.tr(key, **kwargs)

def _prop(key: str) -> str:
    return I18N.tr_prop(key)

I18N.init()
