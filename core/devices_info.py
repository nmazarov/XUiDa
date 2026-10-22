"""
XUiDa64 - Windows PnP Device Tree & Peripherals Module
"""

import win32com.client

class DevicesInfo:
    @staticmethod
    def get_devices():
        categories = {}
        try:
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
