"""
XUiDa64 - Windows PnP Device Tree & Peripherals Module
"""

import sys
import os

try:
    import win32com.client
except ImportError:
    win32com = None

class DevicesInfo:
    @staticmethod
    def get_devices():
        categories = {}
        if sys.platform != "win32":
            categories["PCI"] = []
            if os.path.exists("/sys/bus/pci/devices"):
                for dev in os.listdir("/sys/bus/pci/devices"):
                    categories["PCI"].append({"Name": f"PCI Device {dev}", "Manufacturer": "Linux PCI", "DeviceID": dev, "Status": "OK"})
            return categories

        try:
            if win32com:
                wmi = win32com.client.GetObject("winmgmts:")
                res = wmi.ExecQuery("SELECT Name, PNPClass, Manufacturer, DeviceID, Status FROM Win32_PnPEntity")
            for dev in res:
                pnp_class = getattr(dev, "PNPClass", "Other") or "Other"
                name = getattr(dev, "Name", "Unknown Device") or "Unknown Device"
                name = str(name).strip()
                dev_id = getattr(dev, "DeviceID", "") or ""
                status = getattr(dev, "Status", "OK") or "OK"
                mfg = getattr(dev, "Manufacturer", "Generic") or "Generic"

                if pnp_class not in categories:
                    categories[pnp_class] = []

                categories[pnp_class].append({
                    "Name": name,
                    "Manufacturer": str(mfg).strip(),
                    "DeviceID": str(dev_id).strip(),
                    "Status": str(status).strip()
                })
        except Exception as e:
            categories["Error"] = [{"Name": str(e), "Status": "Error"}]

        return categories

if __name__ == "__main__":
    devs = DevicesInfo.get_devices()
    print("Found categories:", list(devs.keys()))
    print("Processors count:", len(devs.get("Processor", [])))
