"""
XUiDa64 - Storage, Physical Drives & SMART Information Module
"""

import sys
import os
import psutil
import subprocess
import json

try:
    import win32com.client
except ImportError:
    win32com = None

try:
    from core.demo_profile import is_demo_mode, get_demo_physical_drives, get_demo_logical_drives
except ImportError:
    from .demo_profile import is_demo_mode, get_demo_physical_drives, get_demo_logical_drives

class StorageInfo:
    _cached_physical_drives = None

    @staticmethod
    def get_logical_drives():
        if is_demo_mode():
            return get_demo_logical_drives()
        drives = []
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                total_gb = round(usage.total / (1024**3), 2)
                used_gb = round(usage.used / (1024**3), 2)
                free_gb = round(usage.free / (1024**3), 2)
                percent = usage.percent

                drives.append({
                    "Device": part.device,
                    "Mountpoint": part.mountpoint,
                    "FSType": part.fstype,
                    "Opts": part.opts,
                    "TotalGB": total_gb,
                    "UsedGB": used_gb,
                    "FreeGB": free_gb,
                    "PercentUsed": percent
                })
            except (PermissionError, OSError):
                continue
        return drives

    @classmethod
    def get_physical_drives(cls, force_refresh=False):
        if is_demo_mode():
            return get_demo_physical_drives()
        if cls._cached_physical_drives is not None and not force_refresh:
            return cls._cached_physical_drives

        drives = []
        if sys.platform != "win32":
            if os.path.exists("/sys/block"):
                for b in os.listdir("/sys/block"):
                    if b.startswith("loop") or b.startswith("ram"):
                        continue
                    model_path = f"/sys/block/{b}/device/model"
                    model = f"Block Device /dev/{b}"
                    if os.path.exists(model_path):
                        try:
                            with open(model_path) as f:
                                model = f.read().strip()
                        except Exception:
                            pass
                    drives.append({
                        "Model": model,
                        "Interface": "NVMe" if "nvme" in b else "SATA/SCSI",
                        "MediaType": "NVMe SSD" if "nvme" in b else "SSD/HDD",
                        "SizeGB": 0,
                        "Health": "OK (Healthy)"
                    })
            cls._cached_physical_drives = drives
            return drives

        # Direct fast WMI MSFT_PhysicalDisk query without slow powershell process spawning
        media_types = {3: "HDD", 4: "SSD", 5: "SCM"}
        bus_types = {3: "ATAPI", 8: "SCSI", 11: "SATA", 17: "NVMe", 7: "USB"}
        storage_meta = {}

        try:
            if win32com:
                wmi_storage = win32com.client.GetObject(r"winmgmts:\\.\root\Microsoft\Windows\Storage")
            for d in wmi_storage.InstancesOf("MSFT_PhysicalDisk"):
                name = getattr(d, "FriendlyName", "").strip()
                dev_id = str(getattr(d, "DeviceId", ""))
                m_type = media_types.get(getattr(d, "MediaType", 0), "SSD" if "SSD" in name.upper() or "NVME" in name.upper() else "HDD")
                b_type = bus_types.get(getattr(d, "BusType", 0), "NVMe" if "NVME" in name.upper() else "SATA")
                storage_meta[dev_id] = {"MediaType": m_type, "BusType": b_type}
                storage_meta[name] = {"MediaType": m_type, "BusType": b_type}
        except Exception:
            pass

        # Query WMI Win32_DiskDrive
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            for d in wmi.InstancesOf("Win32_DiskDrive"):
                idx = str(getattr(d, "Index", len(drives)))
                model = getattr(d, "Model", "Generic Physical Disk").strip()
                size_bytes = int(getattr(d, "Size", 0) or 0)
                size_gb = round(size_bytes / (1024**3), 1)
                interface = getattr(d, "InterfaceType", "SATA").strip()
                serial = getattr(d, "SerialNumber", "Unknown").strip()

                meta = storage_meta.get(idx) or storage_meta.get(model)
                media_type = meta.get("MediaType") if meta else ("SSD" if "SSD" in model.upper() or "NVME" in model.upper() else "HDD")
                bus_type = meta.get("BusType") if meta else interface

                drives.append({
                    "Index": idx,
                    "Model": model,
                    "MediaType": media_type,
                    "BusType": bus_type,
                    "Health": "OK",
                    "SizeGB": size_gb,
                    "SerialNumber": serial,
                    "Partitions": getattr(d, "Partitions", 1),
                    "Status": getattr(d, "Status", "OK")
                })
        except Exception as e:
            drives.append({"error": str(e)})

        cls._cached_physical_drives = drives
        return drives

    @staticmethod
    def get_smart_status():
        smart_info = []
        try:
            wmi = win32com.client.GetObject("winmgmts:root\\wmi")
            for item in wmi.InstancesOf("MSStorageDriver_FailurePredictStatus"):
                smart_info.append({
                    "InstanceName": getattr(item, "InstanceName", "Drive"),
                    "PredictFailure": getattr(item, "PredictFailure", False),
                    "Status": "Healthy" if not getattr(item, "PredictFailure", False) else "WARNING: Predicted Failure"
                })
        except Exception:
            pass
        return smart_info

if __name__ == "__main__":
    print("Logical Drives:", StorageInfo.get_logical_drives())
    print("Physical Drives:", StorageInfo.get_physical_drives())
    print("SMART Status:", StorageInfo.get_smart_status())
