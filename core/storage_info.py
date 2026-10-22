"""
XUiDa64 - Storage, Physical Drives & SMART Information Module
"""

import psutil
import win32com.client
import subprocess
import json

class StorageInfo:
    @staticmethod
    def get_logical_drives():
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

    @staticmethod
    def get_physical_drives():
        drives = []
        # Query PowerShell Get-PhysicalDisk for reliable modern NVMe / SSD detection
        ps_data = {}
        try:
            cmd = "powershell -NoProfile -Command \"Get-PhysicalDisk | Select-Object DeviceId, FriendlyName, MediaType, BusType, HealthStatus, Size | ConvertTo-Json -Compress\""
            out = subprocess.check_output(cmd, shell=True, timeout=5).decode("utf-8", errors="ignore").strip()
            if out:
                parsed = json.loads(out)
                if isinstance(parsed, dict):
                    parsed = [parsed]
                for item in parsed:
                    dev_id = str(item.get("DeviceId", ""))
                    ps_data[dev_id] = item
                    ps_data[item.get("FriendlyName", "").strip()] = item
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

                # Merge PowerShell data if present
                ps_match = ps_data.get(idx) or ps_data.get(model)
                media_type = "SSD" if "SSD" in model.upper() or "NVME" in model.upper() else "HDD"
                bus_type = interface
                health = "OK"

                if ps_match:
                    media_type = ps_match.get("MediaType", media_type)
                    bus_type = ps_match.get("BusType", bus_type)
                    health = ps_match.get("HealthStatus", health)

                drives.append({
                    "Index": idx,
                    "Model": model,
                    "MediaType": media_type,
                    "BusType": bus_type,
                    "Health": health,
                    "SizeGB": size_gb,
                    "SerialNumber": serial,
                    "Partitions": getattr(d, "Partitions", 1),
                    "Status": getattr(d, "Status", "OK")
                })
        except Exception as e:
            drives.append({"error": str(e)})

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
