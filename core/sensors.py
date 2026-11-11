"""
XUiDa64 - Real-Time Sensor Monitor Module
Pulls live telemetry from ACPI Thermal Zones, NVML, Performance Counters and Storage.
"""

import psutil
import win32com.client
from core.gpu_info import GPUInfo
from core.network_info import NetworkInfo

try:
    from core.demo_profile import is_demo_mode, get_demo_sensors
except ImportError:
    from .demo_profile import is_demo_mode, get_demo_sensors

class Sensors:
    @staticmethod
    def get_all_sensors():
        if is_demo_mode():
            return get_demo_sensors()
        data = {
            "Temperatures": [],
            "Fans": [],
            "Voltages": [],
            "Powers": [],
            "Clocks": [],
            "Usage": []
        }

        # 1. CPU & Motherboard Temperatures
        cpu_temp = None
        try:
            wmi_root = win32com.client.GetObject("winmgmts:root\\wmi")
            for t in wmi_root.InstancesOf("MSAcpi_ThermalZoneTemperature"):
                celsius = round((t.CurrentTemperature - 2732) / 10.0, 1)
                if 10.0 <= celsius <= 120.0:
                    cpu_temp = celsius
                    data["Temperatures"].append({
                        "Sensor": "CPU Package (ACPI)",
                        "Value": celsius,
                        "Unit": "°C",
                        "Category": "CPU"
                    })
                    break
        except Exception:
            pass

        if cpu_temp is None:
            try:
                wmi = win32com.client.GetObject("winmgmts:")
                for tz in wmi.InstancesOf("Win32_PerfFormattedData_Counters_ThermalZoneInformation"):
                    celsius = round(tz.Temperature - 273.15, 1)
                    if 10.0 <= celsius <= 120.0:
                        cpu_temp = celsius
                        data["Temperatures"].append({
                            "Sensor": "Motherboard / Thermal Zone",
                            "Value": celsius,
                            "Unit": "°C",
                            "Category": "Motherboard"
                        })
                        break
            except Exception:
                pass

        # 2. GPU Sensors (NVIDIA NVML or WMI)
        gpus = GPUInfo.get_all_gpus()
        for g in gpus:
            name = g.get("Name", "GPU")
            temp = g.get("Temperature")
            if temp is not None:
                data["Temperatures"].append({
                    "Sensor": f"{name} Diode",
                    "Value": temp,
                    "Unit": "°C",
                    "Category": "GPU"
                })

            fan = g.get("FanSpeed")
            if fan is not None:
                data["Fans"].append({
                    "Sensor": f"{name} Fan",
                    "Value": fan,
                    "Unit": "%",
                    "Category": "GPU"
                })

            power = g.get("PowerWatts")
            if power is not None and power > 0:
                data["Powers"].append({
                    "Sensor": f"{name} Power",
                    "Value": power,
                    "Unit": "W",
                    "Category": "GPU"
                })

            core_clk = g.get("CoreClockMHz")
            if core_clk:
                data["Clocks"].append({
                    "Sensor": f"{name} Clock",
                    "Value": core_clk,
                    "Unit": "MHz",
                    "Category": "GPU"
                })

            mem_clk = g.get("MemoryClockMHz")
            if mem_clk:
                data["Clocks"].append({
                    "Sensor": f"{name} Memory Clock",
                    "Value": mem_clk,
                    "Unit": "MHz",
                    "Category": "GPU"
                })

            gpu_util = g.get("GPUUtil")
            if gpu_util is not None:
                data["Usage"].append({
                    "Sensor": f"{name} Core Load",
                    "Value": gpu_util,
                    "Unit": "%",
                    "Category": "GPU"
                })

        # 3. CPU Clock & Voltage
        try:
            freq = psutil.cpu_freq()
            if freq and freq.current:
                data["Clocks"].append({
                    "Sensor": "CPU Clock",
                    "Value": round(freq.current),
                    "Unit": "MHz",
                    "Category": "CPU"
                })
        except Exception:
            pass

        # 4. System Usage (CPU, RAM)
        cpu_usage = psutil.cpu_percent(interval=None)
        data["Usage"].append({
            "Sensor": "CPU Total Utilization",
            "Value": round(cpu_usage, 1),
            "Unit": "%",
            "Category": "CPU"
        })

        vm = psutil.virtual_memory()
        data["Usage"].append({
            "Sensor": "Memory Utilization",
            "Value": round(vm.percent, 1),
            "Unit": "%",
            "Category": "Memory"
        })
        data["Usage"].append({
            "Sensor": "Memory Used",
            "Value": round(vm.used / (1024**3), 2),
            "Unit": "GB",
            "Category": "Memory"
        })

        # 5. Network live rates
        traffic = NetworkInfo.get_realtime_traffic()
        data["Usage"].append({
            "Sensor": "Network Download",
            "Value": traffic["DownloadKBps"],
            "Unit": "KB/s",
            "Category": "Network"
        })
        data["Usage"].append({
            "Sensor": "Network Upload",
            "Value": traffic["UploadKBps"],
            "Unit": "KB/s",
            "Category": "Network"
        })

        return data

if __name__ == "__main__":
    sensors = Sensors.get_all_sensors()
    for cat, items in sensors.items():
        print(f"=== {cat} ===")
        for item in items:
            print(f"  {item['Sensor']}: {item['Value']} {item['Unit']}")
