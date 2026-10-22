"""
XUiDa64 - Text & JSON Report Generator
Creates ASCII text reports modeled after classic AIDA64 Report.txt
"""

import json
import datetime
from core.system_info import SystemInfo
from core.cpu_info import CPUInfo
from core.memory_info import MemoryInfo
from core.gpu_info import GPUInfo
from core.storage_info import StorageInfo
from core.network_info import NetworkInfo
from core.sensors import Sensors
from core.software_info import SoftwareInfo

class TextReportGenerator:
    @staticmethod
    def generate(filepath):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys_info = SystemInfo.get_os_info()
        mb_info = SystemInfo.get_motherboard_info()
        bios_info = SystemInfo.get_bios_info()
        cpu_details = CPUInfo.get_details()
        mem_summary = MemoryInfo.get_summary()
        spd_modules = MemoryInfo.get_spd_modules()
        gpus = GPUInfo.get_all_gpus()
        phys_drives = StorageInfo.get_physical_drives()
        log_drives = StorageInfo.get_logical_drives()
        adapters = NetworkInfo.get_adapters()
        sensors = Sensors.get_all_sensors()

        lines = [
            "--------------------------------------------------------------------------------",
            "                  XUiDa64 Extreme Edition System Report                        ",
            "--------------------------------------------------------------------------------",
            f"Generated:      {now_str}",
            f"Computer:       {sys_info.get('ComputerName')}",
            f"User:           {sys_info.get('RegisteredUser')}",
            f"Operating Sys:  {sys_info.get('OSName')} (Build {sys_info.get('Build')})",
            f"Uptime:         {sys_info.get('Uptime')}",
            "--------------------------------------------------------------------------------",
            "",
            "[ MOTHERBOARD & BIOS ]",
            f"  Motherboard:  {mb_info.get('Manufacturer')} {mb_info.get('Product')} (v{mb_info.get('Version')})",
            f"  Serial:       {mb_info.get('SerialNumber')}",
            f"  BIOS Vendor:  {bios_info.get('Vendor')} {bios_info.get('Version')}",
            f"  BIOS Date:    {bios_info.get('ReleaseDate')}",
            f"  Boot Mode:    {bios_info.get('BootMode')} (SecureBoot: {bios_info.get('SecureBoot')})",
            "",
            "[ PROCESSOR (CPUID) ]",
            f"  Processor:    {cpu_details.get('Brand')}",
            f"  Cores/Threads:{cpu_details.get('PhysicalCores')} Physical, {cpu_details.get('LogicalCores')} Logical",
            f"  Signature:    {cpu_details.get('Signature')}",
            f"  Socket:       {cpu_details.get('Socket')}",
            f"  Clock:        {cpu_details.get('CurrentClock')}",
            f"  Caches:       {cpu_details.get('Caches')}",
            "",
            "[ MEMORY & SPD ]",
            f"  Total RAM:    {mem_summary.get('TotalGB')} GB (Used: {mem_summary.get('UsedGB')} GB, Free: {mem_summary.get('FreeGB')} GB)",
            f"  Swap Space:   {mem_summary.get('SwapTotalGB')} GB (Used: {mem_summary.get('SwapUsedGB')} GB)",
        ]

        lines.append("  SPD Slots:")
        for m in spd_modules:
            lines.append(f"    - {m.get('DeviceLocator')}: {m.get('CapacityGB')} GB {m.get('MemoryType')}-{m.get('SpeedMHz')} ({m.get('Manufacturer')} {m.get('PartNumber')})")

        lines.append("")
        lines.append("[ GRAPHICS & DISPLAY ]")
        for g in gpus:
            lines.append(f"  GPU:          {g.get('Name')} ({g.get('VRAM_MB')} MB VRAM)")
            lines.append(f"  Driver:       {g.get('DriverVersion')}")
            lines.append(f"  Resolution:   {g.get('Resolution')}")

        lines.append("")
        lines.append("[ STORAGE ]")
        for d in phys_drives:
            lines.append(f"  Disk:         {d.get('Model')} [{d.get('MediaType')} {d.get('BusType')}] - {d.get('SizeGB')} GB (Health: {d.get('Health')})")
        for ld in log_drives:
            lines.append(f"  Volume {ld.get('Device')}    {ld.get('TotalGB')} GB ({ld.get('FreeGB')} GB Free, {ld.get('FSType')})")

        lines.append("")
        lines.append("[ NETWORK ]")
        for a in adapters:
            if a.get('Status') == 'Connected':
                lines.append(f"  Adapter:      {a.get('Name')} [{a.get('Speed')}]")
                lines.append(f"  IPv4:         {a.get('IPv4')} / {a.get('Netmask')}")
                lines.append(f"  MAC:          {a.get('MAC')}")
                lines.append(f"  Gateway:      {a.get('Gateways')}")

        lines.append("")
        lines.append("[ SENSORS ]")
        for item in sensors.get("Temperatures", []) + sensors.get("Fans", []) + sensors.get("Powers", []):
            lines.append(f"  {item.get('Sensor')}: {item.get('Value')} {item.get('Unit')}")

        lines.append("")
        lines.append("--------------------------------------------------------------------------------")
        lines.append("End of Report. XUiDa64 - Open Source Hardware Diagnostics.")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return filepath

    @staticmethod
    def generate_json(filepath):
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "os": SystemInfo.get_os_info(),
            "motherboard": SystemInfo.get_motherboard_info(),
            "bios": SystemInfo.get_bios_info(),
            "cpu": CPUInfo.get_details(),
            "memory": MemoryInfo.get_summary(),
            "spd": MemoryInfo.get_spd_modules(),
            "gpus": GPUInfo.get_all_gpus(),
            "physical_drives": StorageInfo.get_physical_drives(),
            "logical_drives": StorageInfo.get_logical_drives(),
            "network": NetworkInfo.get_adapters(),
            "sensors": Sensors.get_all_sensors()
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath
