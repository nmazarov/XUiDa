"""
XUiDa64 - Processor & CPU Information Module
"""

import os
import sys
import psutil
import win32com.client

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.cpuid import CPUID
except ImportError:
    from .cpuid import CPUID

class CPUInfo:
    @staticmethod
    def get_details():
        cpuid_data = CPUID.get_info()
        brand = cpuid_data.get("brand", "Unknown Processor")
        vendor = cpuid_data.get("vendor", "Unknown")

        phys_cores = psutil.cpu_count(logical=False) or 1
        log_cores = psutil.cpu_count(logical=True) or 1
        freq = psutil.cpu_freq()

        wmi_details = {
            "Socket": "Socket LGA1700 / AM5 / Other",
            "BaseClock": f"{freq.current:.1f} MHz" if freq else "Unknown",
            "MaxClock": f"{freq.max:.1f} MHz" if freq and freq.max else "Unknown",
            "L2Cache": "Unknown",
            "L3Cache": "Unknown",
            "Voltage": "Unknown",
            "CurrentClock": f"{freq.current:.1f} MHz" if freq else "Unknown"
        }

        try:
            wmi = win32com.client.GetObject("winmgmts:")
            for p in wmi.InstancesOf("Win32_Processor"):
                wmi_details["Socket"] = getattr(p, "SocketDesignation", "LGA1700 / AM5")
                wmi_details["Voltage"] = f"{getattr(p, 'CurrentVoltage', 0) / 10.0:.2f} V" if getattr(p, 'CurrentVoltage', 0) else "Auto"
                if getattr(p, "L2CacheSize", None):
                    wmi_details["L2Cache"] = f"{p.L2CacheSize} KB"
                if getattr(p, "L3CacheSize", None):
                    wmi_details["L3Cache"] = f"{p.L3CacheSize // 1024} MB"
                if getattr(p, "MaxClockSpeed", None):
                    wmi_details["MaxClock"] = f"{p.MaxClockSpeed} MHz"
                if getattr(p, "CurrentClockSpeed", None):
                    wmi_details["CurrentClock"] = f"{p.CurrentClockSpeed} MHz"
                break
        except Exception:
            pass

        # Formatting caches from CPUID if available
        caches_formatted = []
        for c in cpuid_data.get("caches", []):
            caches_formatted.append(f"{c['level']}: {c['size_kb']} KB")
        cache_str = ", ".join(caches_formatted) if caches_formatted else f"L2: {wmi_details['L2Cache']}, L3: {wmi_details['L3Cache']}"

        return {
            "Brand": brand,
            "Vendor": vendor,
            "Signature": cpuid_data.get("signature", "Unknown"),
            "PhysicalCores": phys_cores,
            "LogicalCores": log_cores,
            "Socket": wmi_details["Socket"],
            "CurrentClock": wmi_details["CurrentClock"],
            "BaseClock": wmi_details["BaseClock"],
            "MaxClock": wmi_details["MaxClock"],
            "Voltage": wmi_details["Voltage"],
            "Caches": cache_str,
            "CacheList": cpuid_data.get("caches", []),
            "Features": cpuid_data.get("features", {}),
            "Utilization": psutil.cpu_percent(interval=None)
        }

    @staticmethod
    def get_per_core_usage():
        return psutil.cpu_percent(interval=None, percpu=True)

if __name__ == "__main__":
    print(CPUInfo.get_details())
