"""
XUiDa64 - Software, Installed Apps, Services & Process Explorer Module
"""

import os
import winreg
import psutil

class SoftwareInfo:
    @staticmethod
    def get_installed_programs():
        programs = []
        reg_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", winreg.KEY_WOW64_64KEY),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", winreg.KEY_WOW64_32KEY),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall", 0)
        ]

        seen = set()

        for root, subkey, flag in reg_keys:
            try:
                access = winreg.KEY_READ | flag if flag else winreg.KEY_READ
                with winreg.OpenKey(root, subkey, 0, access) as key:
                    num_subkeys = winreg.QueryInfoKey(key)[0]
                    for i in range(num_subkeys):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as app_key:
                                try:
                                    name, _ = winreg.QueryValueEx(app_key, "DisplayName")
                                except OSError:
                                    continue

                                if not name or name in seen:
                                    continue

                                # Ignore system updates or components if marked SystemComponent
                                try:
                                    is_sys, _ = winreg.QueryValueEx(app_key, "SystemComponent")
                                    if is_sys == 1:
                                        continue
                                except OSError:
                                    pass

                                seen.add(name)

                                ver = ""
                                pub = ""
                                date = ""
                                try:
                                    ver, _ = winreg.QueryValueEx(app_key, "DisplayVersion")
                                except OSError:
                                    pass
                                try:
                                    pub, _ = winreg.QueryValueEx(app_key, "Publisher")
                                except OSError:
                                    pass
                                try:
                                    date, _ = winreg.QueryValueEx(app_key, "InstallDate")
                                except OSError:
                                    pass

                                programs.append({
                                    "Name": str(name).strip(),
                                    "Version": str(ver).strip() if ver else "1.0",
                                    "Publisher": str(pub).strip() if pub else "Unknown",
                                    "InstallDate": str(date).strip() if date else "Unknown"
                                })
                        except OSError:
                            continue
            except OSError:
                continue

        programs.sort(key=lambda x: x["Name"].lower())
        return programs

    @staticmethod
    def get_startup_programs():
        startup = []
        run_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]

        for root, subkey in run_keys:
            try:
                with winreg.OpenKey(root, subkey, 0, winreg.KEY_READ) as key:
                    num_values = winreg.QueryInfoKey(key)[1]
                    for i in range(num_values):
                        try:
                            name, val, _ = winreg.EnumValue(key, i)
                            startup.append({
                                "Name": name,
                                "Command": val,
                                "Location": "Registry (HKLM)" if root == winreg.HKEY_LOCAL_MACHINE else "Registry (HKCU)"
                            })
                        except OSError:
                            continue
            except OSError:
                continue

        # Startup directory
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            startup_dir = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup")
            if os.path.exists(startup_dir):
                for f in os.listdir(startup_dir):
                    if not f.startswith("desktop.ini"):
                        startup.append({
                            "Name": f,
                            "Command": os.path.join(startup_dir, f),
                            "Location": "Startup Folder"
                        })

        return startup

    @staticmethod
    def get_processes():
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'num_threads', 'status']):
            try:
                info = p.info
                mem_mb = round((info['memory_info'].rss if info.get('memory_info') else 0) / (1024**2), 1)
                procs.append({
                    "PID": info['pid'],
                    "Name": info['name'] or "Unknown",
                    "CPU": info.get('cpu_percent', 0.0) or 0.0,
                    "MemoryMB": mem_mb,
                    "Threads": info.get('num_threads', 1) or 1,
                    "User": (info.get('username') or "").split("\\")[-1] or "SYSTEM",
                    "Status": info.get('status', 'running')
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        procs.sort(key=lambda x: x["MemoryMB"], reverse=True)
        return procs

    @staticmethod
    def get_services():
        services = []
        try:
            for s in psutil.win_service_iter():
                try:
                    s_info = s.as_dict()
                    services.append({
                        "Name": s_info.get("name", ""),
                        "DisplayName": s_info.get("display_name", ""),
                        "Status": s_info.get("status", ""),
                        "StartType": s_info.get("start_type", "")
                    })
                except Exception:
                    continue
        except Exception:
            pass
        services.sort(key=lambda x: x["DisplayName"].lower())
        return services

if __name__ == "__main__":
    apps = SoftwareInfo.get_installed_programs()
    print("Installed Apps Count:", len(apps))
    if apps:
        print("Sample app:", apps[0])
    procs = SoftwareInfo.get_processes()
    print("Running Procs Count:", len(procs))
    if procs:
        print("Top memory proc:", procs[0])
