"""
XUiDa64 - System, Motherboard, BIOS and OS Information Extractor
"""

import sys
import os
import platform
import subprocess
import time
import datetime

try:
    import win32com.client
except ImportError:
    win32com = None

try:
    import winreg
except ImportError:
    winreg = None

from core.demo_profile import (
    is_demo_mode, get_demo_os_info, get_demo_motherboard_info, get_demo_bios_info
)

class SystemInfo:
    @staticmethod
    def get_motherboard_info():
        if is_demo_mode():
            return get_demo_motherboard_info()
        info = {
            "Manufacturer": "Unknown",
            "Product": "Unknown",
            "Version": "Unknown",
            "SerialNumber": "Unknown",
            "Chipset": "Intel/AMD Chipset"
        }
        if sys.platform != "win32":
            def read_dmi(name):
                p = f"/sys/devices/virtual/dmi/id/{name}"
                if os.path.exists(p):
                    try:
                        with open(p, "r") as f:
                            return f.read().strip()
                    except Exception:
                        pass
                return "Unknown"

            info["Manufacturer"] = read_dmi("board_vendor")
            info["Product"] = read_dmi("board_name")
            info["Version"] = read_dmi("board_version")
            info["SerialNumber"] = read_dmi("board_serial")
            return info
        try:
            wmi = win32com.client.GetObject("winmgmts:") if win32com else None
            for b in wmi.InstancesOf("Win32_BaseBoard"):
                info["Manufacturer"] = getattr(b, "Manufacturer", "Unknown").strip()
                info["Product"] = getattr(b, "Product", "Unknown").strip()
                info["Version"] = getattr(b, "Version", "Unknown").strip()
                info["SerialNumber"] = getattr(b, "SerialNumber", "Unknown").strip()
                break
        except Exception as e:
            info["error"] = str(e)
        return info

    @staticmethod
    def get_bios_info():
        if is_demo_mode():
            return get_demo_bios_info()
        info = {
            "Vendor": "Unknown",
            "Version": "Unknown",
            "ReleaseDate": "Unknown",
            "SMBIOSVersion": "Unknown",
            "BootMode": "UEFI" if os.path.exists(r"C:\Windows\Panther\setupact.log") or os.path.exists("/sys/firmware/efi") else "Unknown"
        }
        if sys.platform != "win32":
            def read_dmi(name):
                p = f"/sys/devices/virtual/dmi/id/{name}"
                if os.path.exists(p):
                    try:
                        with open(p, "r") as f:
                            return f.read().strip()
                    except Exception:
                        pass
                return "Unknown"

            info["Vendor"] = read_dmi("bios_vendor")
            info["Version"] = read_dmi("bios_version")
            info["ReleaseDate"] = read_dmi("bios_date")
            info["BootMode"] = "UEFI" if os.path.exists("/sys/firmware/efi") else "Legacy BIOS"
            info["SecureBoot"] = "Enabled" if os.path.exists("/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c") else "Disabled"
            return info
        try:
            wmi = win32com.client.GetObject("winmgmts:") if win32com else None
            for b in wmi.InstancesOf("Win32_BIOS"):
                info["Vendor"] = getattr(b, "Manufacturer", "Unknown").strip()
                info["Version"] = getattr(b, "SMBIOSBIOSVersion", "Unknown").strip()
                raw_date = getattr(b, "ReleaseDate", "")
                if raw_date and len(raw_date) >= 8:
                    try:
                        info["ReleaseDate"] = f"{raw_date[0:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
                    except Exception:
                        info["ReleaseDate"] = str(raw_date)
                info["SMBIOSVersion"] = f"{getattr(b, 'SMBIOSMajorVersion', '')}.{getattr(b, 'SMBIOSMinorVersion', '')}"
                break
            
            # Check Secure Boot & UEFI via Registry
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\SecureBoot\State") as key:
                    sb, _ = winreg.QueryValueEx(key, "UEFISecureBootEnabled")
                    info["SecureBoot"] = "Enabled" if sb == 1 else "Disabled"
                    info["BootMode"] = "UEFI"
            except Exception:
                info["SecureBoot"] = "Disabled / Unsupported"
        except Exception as e:
            info["error"] = str(e)
        return info

    @staticmethod
    def get_os_info():
        if is_demo_mode():
            return get_demo_os_info()
        boot_time = datetime.datetime.fromtimestamp(SystemInfo.get_boot_time())
        uptime_seconds = int(time.time() - boot_time.timestamp())
        days, rem = divmod(uptime_seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"

        if sys.platform != "win32":
            os_name = "Linux"
            if os.path.exists("/etc/os-release"):
                try:
                    with open("/etc/os-release") as f:
                        for line in f:
                            if line.startswith("PRETTY_NAME="):
                                os_name = line.split("=", 1)[1].strip().strip('"')
                                break
                except Exception:
                    pass

            return {
                "OSName": os_name,
                "Version": platform.release(),
                "Architecture": platform.machine(),
                "ComputerName": platform.node(),
                "RegisteredUser": os.environ.get("USER", "user"),
                "SystemRoot": "/",
                "BootTime": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Uptime": uptime_str,
                "InstallDate": "N/A"
            }

        info = {
            "OSName": platform.system() + " " + platform.release(),
            "Version": platform.version(),
            "Architecture": platform.architecture()[0],
            "ComputerName": platform.node(),
            "RegisteredUser": os.environ.get("USERNAME", "User"),
            "SystemRoot": os.environ.get("SystemRoot", r"C:\Windows"),
            "BootTime": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Uptime": uptime_str,
            "InstallDate": "Unknown"
        }

        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
                try:
                    product_name, _ = winreg.QueryValueEx(key, "ProductName")
                    info["OSName"] = product_name
                except Exception:
                    pass
                try:
                    display_version, _ = winreg.QueryValueEx(key, "DisplayVersion")
                    info["DisplayVersion"] = display_version
                except Exception:
                    pass
                try:
                    build, _ = winreg.QueryValueEx(key, "CurrentBuild")
                    info["Build"] = build
                except Exception:
                    pass
                try:
                    ubr, _ = winreg.QueryValueEx(key, "UBR")
                    info["Build"] = f"{info.get('Build', '')}.{ubr}"
                except Exception:
                    pass
                try:
                    install_time, _ = winreg.QueryValueEx(key, "InstallDate")
                    info["InstallDate"] = datetime.datetime.fromtimestamp(install_time).strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
        except Exception:
            pass

        return info

    @staticmethod
    def get_boot_time():
        import psutil
        return psutil.boot_time()

    @staticmethod
    def get_power_info():
        info = {
            "PowerSource": "AC Power",
            "BatteryPercent": "100%",
            "PowerScheme": "Balanced",
            "BatteryStatus": "No Battery (Desktop)"
        }
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                info["BatteryPercent"] = f"{battery.percent:.0f}%"
                info["PowerSource"] = "AC Connected" if battery.power_plugged else "Battery"
                info["BatteryStatus"] = "Charging" if battery.power_plugged else "Discharging"
            else:
                info["PowerSource"] = "AC Line"
                info["BatteryStatus"] = "High Performance / Desktop"
        except Exception:
            pass
        return info

if __name__ == "__main__":
    print("Motherboard:", SystemInfo.get_motherboard_info())
    print("BIOS:", SystemInfo.get_bios_info())
    print("OS:", SystemInfo.get_os_info())
    print("Power:", SystemInfo.get_power_info())
