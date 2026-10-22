<div align="center">

# ⚡ XUiDa64 Extreme Edition

**Полноценный, бесплатный и открытый аналог AIDA64 Extreme для Windows.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Platform: Windows x64](https://img.shields.io/badge/Platform-Windows%20x64-0078D6.svg)](https://microsoft.com/windows)
[![GUI: PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://riverbankcomputing.com/software/pyqt/)

*Без платных лицензий. Без триальных периодов. Без ограничений. 100% Free & Open Source.*

[English](#english-description) | [Русское описание](#русское-описание)

</div>

---

<a name="русское-описание"></a>
## 🇷🇺 Русское описание

**XUiDa64 Extreme Edition** — это профессиональный программный комплекс для глубокой диагностики аппаратного обеспечения, стресс-тестирования стабильности системы, мониторинга датчиков в реальном времени и бенчмаркинга памяти и процессора.

Проект создан как полноценная, открытая и бесплатная альтернатива популярной утилите **AIDA64 Extreme**, созданная специально для энтузиастов, оверклокеров, системных администраторов и обычных пользователей ПК.

---

### 🌟 Ключевые возможности

| Раздел | Описание |
| :--- | :--- |
| **🖥️ Компьютер (Summary)** | Общая сводка по системе: ОС, процессор, материнская плата, память, видеокарта, время работы (Uptime), BIOS. |
| **⚡ Материнская плата и CPUID** | Прямое исполнение процессорной инструкции `CPUID` в машинном коде x86-64 без сторонних платных драйверов. Определение архитектуры, микрокода, частот, точных кэшей L1/L2/L3 и полного набора инструкций (MMX, SSE 1-4.2, AVX, AVX2, AVX-512, FMA, AES, SHA, BMI). |
| **📊 Память и SPD** | Анализ установленных модулей памяти по каждому слоту DIMM (производитель, Part Number, объем, тип DDR4/DDR5, рабочая частота). |
| **🎮 Видеоподсистема (GPU)** | Прямой опрос контроллера NVIDIA через библиотеку `NVML` + WMI/DirectX. Частоты ядра и памяти, процент загрузки, энергопотребление в ваттах, температура чипа, обороты вентиляторов. |
| **💾 Дисковая подсистема** | Физические накопители (NVMe, SSD, HDD), интерфейсы подключения (SATA, PCIe), серийные номера, разделы дисков и статус S.M.A.R.T. с предсказанием отказов. |
| **🌐 Сеть и трафик** | Сетевые адаптеры (Ethernet, Wi-Fi), IP/IPv6, MAC-адреса, шлюз, DNS, а также монитор скорости отдачи и скачивания в реальном времени. |
| **🌡️ Аппаратный мониторинг и OSD** | Мониторинг температур CPU/GPU/платы, оборотов кулеров и напряжений. Возможность включить плавающий полупрозрачный виджет **Sensor OSD** поверх всех окон (в играх или на рабочем столе). |
| **🏆 Набор бенчмарков (AIDA64 Suite)** | Полноценные тесты производительности подсистемы памяти и CPU со сравнительными гистограммами против эталонной базы современных и классических процессоров: <br>• **Memory Read / Write / Copy** (МБ/с)<br>• **Memory Latency** (наносекунды, нативное pointer-chasing в x86-64 коде)<br>• **CPU Queen** (целочисленные ветвления, задача о 10 ферзях)<br>• **CPU PhotoWorxx** (обработка 2D-изображений и матриц)<br>• **CPU ZLib / AES / SHA3** (сжатие данных и криптографические алгоритмы)<br>• **FPU Julia / Mandel / SinJulia** (фрактальные вычисления с плавающей запятой). |
| **🔥 Стресс-тест стабильности** | Полноценный аналог AIDA64 **System Stability Test** с интерактивными графиками `pyqtgraph` в реальном времени, нагрузкой на CPU, FPU, Cache, RAM и автоматическим определением термического троттлинга. |
| **📑 Мастер отчетов** | Экспорт подробного диагностического отчета ПК в интерактивный **HTML**, классический текстовый **TXT** (как AIDA64 Report.txt) или машиночитаемый **JSON**. |
| **🌓 Темы интерфейса** | Поддержка современной кибер-темной темы (Dark Cyber Edition) и классического светлого стиля AIDA64. |

---

### 🚀 Быстрый запуск

#### 1. Клонирование репозитория
```bash
git clone https://github.com/your-username/XUiDa.git
cd XUiDa
```

#### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

#### 3. Запуск приложения
```bash
python app.py
```

---

### 📦 Сборка в один автономный `.exe` файл

В проект включен скрипт автоматической сборки через PyInstaller:

```bash
python build_exe.py
```
После завершения готовый исполняемый файл `XUiDa64.exe`, не требующий установленного Python, будет лежать в папке:
`dist/XUiDa64/XUiDa64.exe`.

---

<a name="english-description"></a>
## 🇬🇧 English Description

**XUiDa64 Extreme Edition** is an advanced open-source system diagnostics, benchmarking, hardware monitoring, and stability stress-testing utility for Windows x64.

Created as a completely free, open-source alternative to **AIDA64 Extreme**, designed for PC enthusiasts, gamers, overlockers, and system administrators.

### Highlights:
- **Zero Drivers Required**: Uses native x86-64 machine code for direct `CPUID` instruction queries and memory latency pointer-chasing.
- **AIDA64-Grade Benchmarking Suite**: Tests Memory Read, Write, Copy, Latency, CPU Queen, PhotoWorxx, ZLib, AES, SHA3, and FPU Julia/Mandel with comparative bar charts vs modern reference CPUs.
- **System Stability Test**: Multi-threaded stress testing engine featuring live temperature/utilization graphs and thermal throttling warning indicators.
- **Hardware Telemetry & Sensor OSD**: Live ACPI, NVIDIA NVML, and Windows Performance metrics with a floating always-on-top desktop widget.
- **Reporting System**: Generates polished HTML, TXT, and JSON diagnostic reports.

---

### 📁 Структура проекта

```
XUiDa/
├── app.py                     # Главная точка входа приложения
├── build_exe.py               # Скрипт сборки в автономный .exe
├── requirements.txt           # Список необходимых библиотек
├── LICENSE                    # Лицензия MIT
├── README.md                  # Документация проекта
│
├── core/                      # Движок сбора информации о железе
│   ├── cpuid.py               # Прямой вызов x86-64 CPUID в памяти
│   ├── system_info.py         # Плата, BIOS, Windows, Uptime, Power
│   ├── cpu_info.py            # Процессор, кэши, частоты, сокет
│   ├── memory_info.py         # ОЗУ, файл подкачки, SPD слоты DDR4/DDR5
│   ├── gpu_info.py            # Видеокарты (NVML/WMI/DirectX) и мониторы
│   ├── storage_info.py        # Физические накопители, NVMe, SMART
│   ├── network_info.py        # Сетевые интерфейсы и замер трафика
│   ├── devices_info.py        # Дерево устройств Windows PnP
│   ├── software_info.py       # Установленный софт, службы, автозагрузка
│   └── sensors.py             # Датчики температур, вентиляторов, ватт
│
├── benchmarks/                # Комплекс бенчмарков и стресс-тест
│   ├── reference_data.py      # База эталонных процессоров для сравнения
│   ├── memory_bench.py        # Тесты чтения, записи, копирования и задержки
│   ├── cpu_bench.py           # Queen, PhotoWorxx, ZLib, AES, SHA3
│   ├── fpu_bench.py           # Julia, Mandel, SinJulia
│   └── stress_test.py         # Движок стресс-теста стабильности
│
├── gui/                       # Графический интерфейс на PyQt5
│   ├── main_window.py         # Главное окно с тулбаром и меню
│   ├── tree_nav.py            # Дерево навигации по категориям
│   ├── styles.py              # Темная и классическая темы
│   ├── views/                 # Основные вкладки контента
│   │   ├── summary_view.py    # Экран сводки ПК (Summary)
│   │   ├── table_view.py      # Таблицы характеристик с поиском и копированием
│   │   ├── sensor_view.py     # Дашборд датчиков в реальном времени
│   │   ├── process_view.py    # Диспетчер процессов с завершением задач
│   │   └── benchmark_view.py  # Бенчмарки со сравнительными графиками
│   └── dialogs/               # Всплывающие утилиты
│       ├── cpuid_dialog.py    # Окно AIDA64 CPUID
│       ├── stress_dialog.py   # Окно System Stability Test с графиками
│       ├── sensor_panel.py    # Плавающий полупрозрачный виджет Sensor OSD
│       ├── report_dialog.py   # Мастер экспорта отчетов
│       └── about_dialog.py    # О программе
│
└── reports/                   # Генераторы отчетов
    ├── html_report.py         # Генератор красивых HTML-отчетов
    └── text_report.py         # Генератор TXT и JSON отчетов
```

---

### 📄 Лицензия

Проект распространяется под свободной и открытой лицензией [MIT License](LICENSE). Вы можете свободно использовать, модифицировать, форкать и распространять его.
