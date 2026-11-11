"""
XUiDa64 - GPU & Display Information Module
Direct NVML interface for NVIDIA cards + WMI / Win32 API fallback for AMD/Intel.
"""

import ctypes
import win32com.client

try:
    from core.demo_profile import is_demo_mode, get_demo_gpus, get_demo_monitors
except ImportError:
    from .demo_profile import is_demo_mode, get_demo_gpus, get_demo_monitors

class GPUInfo:
    _nvml_loaded = False
    _nvml = None

    @classmethod
    def _init_nvml(cls):
        if cls._nvml_loaded:
            return cls._nvml is not None
        cls._nvml_loaded = True
        try:
            cls._nvml = ctypes.CDLL("nvml.dll")
            if cls._nvml.nvmlInit_v2() != 0:
                cls._nvml = None
        except Exception:
            cls._nvml = None
        return cls._nvml is not None

    @classmethod
    def get_nvidia_details(cls):
        if not cls._init_nvml():
            return []

        cards = []
        try:
            count = ctypes.c_uint()
            cls._nvml.nvmlDeviceGetCount_v2(ctypes.byref(count))
            for i in range(count.value):
                dev = ctypes.c_void_p()
                cls._nvml.nvmlDeviceGetHandleByIndex_v2(i, ctypes.byref(dev))

                # Name
                name_buf = ctypes.create_string_buffer(96)
                cls._nvml.nvmlDeviceGetName(dev, name_buf, 96)
                name = name_buf.value.decode("utf-8", errors="ignore")

                # Temp
                temp = ctypes.c_uint(0)
                cls._nvml.nvmlDeviceGetTemperature(dev, 0, ctypes.byref(temp))

                # Fan
                fan = ctypes.c_uint(0)
                has_fan = (cls._nvml.nvmlDeviceGetFanSpeed(dev, ctypes.byref(fan)) == 0)

                # Power
                power = ctypes.c_uint(0)
                has_power = (cls._nvml.nvmlDeviceGetPowerUsage(dev, ctypes.byref(power)) == 0)

                # Clocks
                core_clock = ctypes.c_uint(0)
                cls._nvml.nvmlDeviceGetClockInfo(dev, 0, ctypes.byref(core_clock)) # 0 = Graphics clock
                mem_clock = ctypes.c_uint(0)
                cls._nvml.nvmlDeviceGetClockInfo(dev, 2, ctypes.byref(mem_clock)) # 2 = Mem clock

                # Memory
                class NVMLMemory(ctypes.Structure):
                    _fields_ = [
                        ("total", ctypes.c_ulonglong),
                        ("free", ctypes.c_ulonglong),
                        ("used", ctypes.c_ulonglong)
                    ]
                mem_struct = NVMLMemory()
                cls._nvml.nvmlDeviceGetMemoryInfo(dev, ctypes.byref(mem_struct))

                # Utilization
                class NVMLUtilization(ctypes.Structure):
                    _fields_ = [
                        ("gpu", ctypes.c_uint),
                        ("memory", ctypes.c_uint)
                    ]
                util_struct = NVMLUtilization()
                cls._nvml.nvmlDeviceGetUtilizationRates(dev, ctypes.byref(util_struct))

                cards.append({
                    "Name": name,
                    "Temperature": temp.value,
                    "FanSpeedPercent": fan.value if has_fan else 0,
                    "PowerWatts": round(power.value / 1000.0, 1) if has_power else 0.0,
                    "CoreClockMHz": core_clock.value,
                    "MemoryClockMHz": mem_clock.value,
                    "VRAMTotalMB": round(mem_struct.total / (1024**2)),
                    "VRAMUsedMB": round(mem_struct.used / (1024**2)),
                    "VRAMFreeMB": round(mem_struct.free / (1024**2)),
                    "GPUUtilPercent": util_struct.gpu,
                    "MemUtilPercent": util_struct.memory,
                    "Vendor": "NVIDIA"
                })
        except Exception:
            pass
        return cards

    @classmethod
    def get_all_gpus(cls):
        if is_demo_mode():
            return get_demo_gpus()
        gpus = []
        nv_gpus = cls.get_nvidia_details()
        nv_map = {g["Name"]: g for g in nv_gpus}

        try:
            wmi = win32com.client.GetObject("winmgmts:")
            for v in wmi.InstancesOf("Win32_VideoController"):
                name = getattr(v, "Name", "Video Controller").strip()
                driver_ver = getattr(v, "DriverVersion", "Unknown").strip()
                res_w = getattr(v, "CurrentHorizontalResolution", "")
                res_h = getattr(v, "CurrentVerticalResolution", "")
                refresh = getattr(v, "CurrentRefreshRate", "")
                ram = getattr(v, "AdapterRAM", 0) or 0
                ram_mb = round(int(ram) / (1024**2)) if ram > 0 else 0

                resolution_str = f"{res_w} x {res_h} @ {refresh} Hz" if res_w and res_h else "N/A"
                
                # Merge NVML if matches
                nv_match = nv_map.get(name)

                gpu_entry = {
                    "Name": name,
                    "DriverVersion": driver_ver,
                    "DriverDate": getattr(v, "DriverDate", "")[:8],
                    "Resolution": resolution_str,
                    "VRAM_MB": nv_match["VRAMTotalMB"] if nv_match else ram_mb,
                    "Vendor": "NVIDIA" if "NVIDIA" in name else ("AMD" if "AMD" in name or "Radeon" in name else "Intel"),
                    "Temperature": nv_match["Temperature"] if nv_match else None,
                    "FanSpeed": nv_match["FanSpeedPercent"] if nv_match else None,
                    "PowerWatts": nv_match["PowerWatts"] if nv_match else None,
                    "CoreClockMHz": nv_match["CoreClockMHz"] if nv_match else None,
                    "MemoryClockMHz": nv_match["MemoryClockMHz"] if nv_match else None,
                    "GPUUtil": nv_match["GPUUtilPercent"] if nv_match else None
                }
                gpus.append(gpu_entry)
        except Exception:
            if nv_gpus:
                return nv_gpus
        return gpus if gpus else nv_gpus

    @staticmethod
    def get_monitors():
        if is_demo_mode():
            return get_demo_monitors()
        monitors = []
        try:
            wmi = win32com.client.GetObject("winmgmts:root\\wmi")
            for m in wmi.InstancesOf("WmiMonitorID"):
                user_friendly = m.UserFriendlyName
                if user_friendly:
                    chars = [chr(c) for c in user_friendly if c > 0]
                    name = "".join(chars).strip()
                    monitors.append({"Name": name})
        except Exception:
            pass

        if not monitors:
            try:
                wmi = win32com.client.GetObject("winmgmts:")
                for m in wmi.InstancesOf("Win32_DesktopMonitor"):
                    monitors.append({
                        "Name": getattr(m, "Name", "Standard Monitor"),
                        "ScreenWidth": getattr(m, "ScreenWidth", ""),
                        "ScreenHeight": getattr(m, "ScreenHeight", "")
                    })
            except Exception:
                monitors.append({"Name": "Generic PnP Monitor"})
        return monitors

if __name__ == "__main__":
    print("GPUs:", GPUInfo.get_all_gpus())
    print("Monitors:", GPUInfo.get_monitors())
