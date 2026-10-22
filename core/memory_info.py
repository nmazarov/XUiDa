"""
XUiDa64 - Memory & SPD Information Module
"""

import psutil
import win32com.client

class MemoryInfo:
    SMBIOS_MEMORY_TYPES = {
        20: "DDR",
        21: "DDR2",
        22: "DDR2 FB-DIMM",
        24: "DDR3",
        26: "DDR4",
        30: "LPDDR4",
        34: "DDR5",
        35: "LPDDR5"
    }

    @staticmethod
    def get_summary():
        vm = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "TotalGB": round(vm.total / (1024**3), 2),
            "UsedGB": round(vm.used / (1024**3), 2),
            "FreeGB": round(vm.available / (1024**3), 2),
            "PercentUsed": vm.percent,
            "SwapTotalGB": round(swap.total / (1024**3), 2),
            "SwapUsedGB": round(swap.used / (1024**3), 2),
            "SwapFreeGB": round(swap.free / (1024**3), 2),
            "SwapPercent": swap.percent
        }

    @staticmethod
    def get_spd_modules():
        modules = []
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            for m in wmi.InstancesOf("Win32_PhysicalMemory"):
                cap_bytes = int(getattr(m, "Capacity", 0) or 0)
                cap_gb = round(cap_bytes / (1024**3), 1)
                speed = getattr(m, "Speed", 0) or getattr(m, "ConfiguredClockSpeed", 0) or 0
                smbios_type = getattr(m, "SMBIOSMemoryType", 0) or 0
                mem_type = MemoryInfo.SMBIOS_MEMORY_TYPES.get(smbios_type, "DDR4/DDR5" if speed >= 3200 else "DDR3/DDR4")
                
                # If speed is >= 4800 MHz it's definitely DDR5
                if speed >= 4800:
                    mem_type = "DDR5"
                elif speed >= 2133 and mem_type == "Unknown":
                    mem_type = "DDR4"

                modules.append({
                    "DeviceLocator": getattr(m, "DeviceLocator", "DIMM Slot").strip(),
                    "BankLabel": getattr(m, "BankLabel", "").strip(),
                    "CapacityGB": cap_gb,
                    "SpeedMHz": speed,
                    "Manufacturer": getattr(m, "Manufacturer", "Unknown").strip(),
                    "PartNumber": getattr(m, "PartNumber", "Unknown").strip(),
                    "SerialNumber": getattr(m, "SerialNumber", "Unknown").strip(),
                    "MemoryType": mem_type,
                    "FormFactor": "DIMM"
                })
        except Exception as e:
            modules.append({"error": str(e)})
        return modules

if __name__ == "__main__":
    print("Memory Summary:", MemoryInfo.get_summary())
    print("SPD Modules:", MemoryInfo.get_spd_modules())
