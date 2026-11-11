"""
XUiDa64 - Demonstration Hardware Profile Generator
Used for generating clean, privacy-safe, anonymized promotional screenshots
and documentation media featuring high-end flagship hardware specs.
"""

import os

def is_demo_mode() -> bool:
    return os.environ.get("XUIDA_DEMO_MODE") == "1"

def get_demo_os_info():
    return {
        "OSName": "Windows 11 Pro for Workstations",
        "Version": "10.0.22631",
        "Architecture": "64bit",
        "ComputerName": "APEX-STUDIO",
        "RegisteredUser": "Workstation",
        "SystemRoot": r"C:\Windows",
        "BootTime": "2026-11-08 08:30:00",
        "Uptime": "3d 14h 28m 10s",
        "InstallDate": "2024-02-14 10:15:00",
        "DisplayVersion": "23H2",
        "Build": "22631.3880"
    }

def get_demo_motherboard_info():
    return {
        "Manufacturer": "ASUSTeK COMPUTER INC.",
        "Product": "ROG MAXIMUS Z790 HERO",
        "Version": "Rev 1.xx",
        "SerialNumber": "MB-Z790-2024-001",
        "Chipset": "Intel Z790 Express Chipset"
    }

def get_demo_bios_info():
    return {
        "Vendor": "American Megatrends Inc.",
        "Version": "2202",
        "ReleaseDate": "2024-05-20",
        "SMBIOSVersion": "3.5",
        "BootMode": "UEFI",
        "SecureBoot": "Enabled"
    }

def get_demo_cpu_info():
    return {
        "Brand": "Intel(R) Core(TM) i9-14900KS",
        "Architecture": "x86-64",
        "PhysicalCores": 24,
        "LogicalCores": 32,
        "BaseClock": "3200.0 MHz",
        "CurrentClock": "5800.0 MHz",
        "MaxClock": "6200.0 MHz",
        "L1Cache": "1.9 MB",
        "L2Cache": "32 MB",
        "L3Cache": "36 MB",
        "Vendor": "GenuineIntel",
        "Family": "6",
        "Model": "183",
        "Stepping": "1",
        "Flags": ["MMX", "SSE", "SSE2", "SSE3", "SSSE3", "SSE4.1", "SSE4.2", "AVX", "AVX2", "FMA", "AES", "SHA", "BMI1", "BMI2"]
    }

def get_demo_memory_info():
    return {
        "TotalGB": 64.0,
        "TotalPhysical": "64 GB",
        "UsedGB": 18.2,
        "FreeGB": 45.8,
        "Percent": 28.4
    }

def get_demo_spd_modules():
    return [
        {
            "Slot": "DIMM 1",
            "CapacityGB": 32.0,
            "MemoryType": "DDR5",
            "Speed": "7200 MHz",
            "Manufacturer": "G.Skill Trident Z5 RGB",
            "PartNumber": "F5-7200J3445G16GX2-TZ5RS"
        },
        {
            "Slot": "DIMM 2",
            "CapacityGB": 32.0,
            "MemoryType": "DDR5",
            "Speed": "7200 MHz",
            "Manufacturer": "G.Skill Trident Z5 RGB",
            "PartNumber": "F5-7200J3445G16GX2-TZ5RS"
        }
    ]

def get_demo_gpus():
    return [
        {
            "Name": "NVIDIA GeForce RTX 4090",
            "DriverVersion": "555.99 (WHQL)",
            "VRAM_MB": 24576,
            "Resolution": "3840x2160 @ 240Hz",
            "Temperature": 41,
            "Load": 2,
            "MemoryUsed_MB": 1850,
            "MemoryTotal_MB": 24576
        }
    ]

def get_demo_monitors():
    return [
        {
            "Name": "ASUS ROG Swift OLED PG32UCDM",
            "Width": 3840,
            "Height": 2160,
            "RefreshRate": 240,
            "Primary": True
        }
    ]

def get_demo_physical_drives():
    return [
        {
            "Model": "Samsung SSD 990 PRO 2TB",
            "Interface": "NVMe PCIe 4.0 x4",
            "MediaType": "NVMe SSD",
            "SizeGB": 2000,
            "Health": "100% (Отличное)"
        }
    ]

def get_demo_logical_drives():
    return [
        {
            "Device": "C:\\",
            "Mountpoint": "C:\\",
            "FSType": "NTFS",
            "TotalGB": 2000.0,
            "UsedGB": 579.5,
            "FreeGB": 1420.5,
            "Percent": 29.0
        }
    ]

def get_demo_adapters():
    return [
        {
            "Name": "Intel(R) Ethernet Controller I226-V (2.5 Gbps)",
            "IPv4": "192.168.1.150",
            "MAC": "00:1A:2B:3C:4D:5E",
            "Speed": "2500 Mbps",
            "Status": "Подключено"
        }
    ]

def get_demo_sensors():
    return {
        "Temperatures": [
            {"Sensor": "CPU Package (ACPI)", "Value": 38.5, "Unit": "°C", "Category": "CPU"},
            {"Sensor": "CPU Core #1", "Value": 36.0, "Unit": "°C", "Category": "CPU"},
            {"Sensor": "NVIDIA GeForce RTX 4090 Diode", "Value": 41.0, "Unit": "°C", "Category": "GPU"},
            {"Sensor": "NVIDIA GeForce RTX 4090 Memory", "Value": 45.0, "Unit": "°C", "Category": "GPU"},
            {"Sensor": "Samsung SSD 990 PRO NVMe", "Value": 35.0, "Unit": "°C", "Category": "Storage"}
        ],
        "Fans": [
            {"Sensor": "NVIDIA GeForce RTX 4090 Fan", "Value": 38, "Unit": "%", "Category": "GPU"},
            {"Sensor": "AIO Liquid Pump", "Value": 1850, "Unit": "RPM", "Category": "CPU"},
            {"Sensor": "Chassis Intake Fan", "Value": 850, "Unit": "RPM", "Category": "Chassis"}
        ],
        "Voltages": [
            {"Sensor": "CPU Vcore", "Value": 1.24, "Unit": "V", "Category": "Voltages"},
            {"Sensor": "+12V Rail", "Value": 12.08, "Unit": "V", "Category": "Voltages"},
            {"Sensor": "+5V Rail", "Value": 5.02, "Unit": "V", "Category": "Voltages"}
        ],
        "Powers": [
            {"Sensor": "CPU Package Power", "Value": 48.2, "Unit": "W", "Category": "CPU"},
            {"Sensor": "NVIDIA GeForce RTX 4090 Power", "Value": 24.8, "Unit": "W", "Category": "GPU"}
        ],
        "Clocks": [
            {"Sensor": "Частота процессора (CPU Clock)", "Value": 5800, "Unit": "MHz", "Category": "CPU"},
            {"Sensor": "NVIDIA GeForce RTX 4090 Core Clock", "Value": 210, "Unit": "MHz", "Category": "GPU"},
            {"Sensor": "NVIDIA GeForce RTX 4090 Memory Clock", "Value": 500, "Unit": "MHz", "Category": "GPU"}
        ],
        "Usage": [
            {"Sensor": "CPU Total", "Value": 14, "Unit": "%", "Category": "CPU"},
            {"Sensor": "Memory Utilization", "Value": 28, "Unit": "%", "Category": "Memory"},
            {"Sensor": "GPU Core Load", "Value": 2, "Unit": "%", "Category": "GPU"}
        ]
    }
