"""
XUiDa64 - Professional HTML System Report Generator
Generates a comprehensive diagnostic report styled after AIDA64 Extreme.
"""

import datetime
from core.system_info import SystemInfo
from core.cpu_info import CPUInfo
from core.memory_info import MemoryInfo
from core.gpu_info import GPUInfo
from core.storage_info import StorageInfo
from core.network_info import NetworkInfo
from core.sensors import Sensors
from core.software_info import SoftwareInfo

class HTMLReportGenerator:
    @staticmethod
    def generate(filepath):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys_info = SystemInfo.get_os_info()
        mb_info = SystemInfo.get_motherboard_info()
        bios_info = SystemInfo.get_bios_info()
        cpu_details = CPUInfo.get_details()
        mem_summary = MemoryInfo.get_summary()
        spd_modules = MemoryInfo.get_spd_modules()
        gpus = GPUInfo.get_all_gpus()
        monitors = GPUInfo.get_monitors()
        log_drives = StorageInfo.get_logical_drives()
        phys_drives = StorageInfo.get_physical_drives()
        adapters = NetworkInfo.get_adapters()
        sensors = Sensors.get_all_sensors()
        apps = SoftwareInfo.get_installed_programs()[:50]  # top 50 apps

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>XUiDa64 Extreme System Report - {sys_info.get('ComputerName', 'PC')}</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #0f141c;
        color: #d1d5db;
        margin: 0;
        padding: 24px;
    }}
    .container {{
        max-width: 1100px;
        margin: 0 auto;
        background: #18202c;
        border: 1px solid #2d3748;
        border-radius: 8px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        padding: 32px;
    }}
    .header {{
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 16px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .header h1 {{
        color: #60a5fa;
        margin: 0;
        font-size: 26px;
        letter-spacing: 0.5px;
    }}
    .header .meta {{
        color: #9ca3af;
        font-size: 13px;
        text-align: right;
    }}
    .section-title {{
        color: #93c5fd;
        font-size: 18px;
        margin-top: 32px;
        margin-bottom: 12px;
        border-bottom: 1px solid #374151;
        padding-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 16px;
        font-size: 13px;
    }}
    th, td {{
        padding: 8px 12px;
        text-align: left;
    }}
    th {{
        background-color: #1f2937;
        color: #93c5fd;
        font-weight: 600;
        border-bottom: 1px solid #374151;
    }}
    tr:nth-child(even) {{
        background-color: #151c27;
    }}
    tr:hover {{
        background-color: #242f40;
    }}
    td.prop {{
        color: #9ca3af;
        width: 30%;
        font-weight: 500;
        border-right: 1px solid #2d3748;
    }}
    td.val {{
        color: #f3f4f6;
    }}
    .badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
    }}
    .badge-ok {{ background-color: #065f46; color: #6ee7b7; }}
    .footer {{
        margin-top: 40px;
        text-align: center;
        color: #6b7280;
        font-size: 12px;
        border-top: 1px solid #2d3748;
        padding-top: 16px;
    }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <div>
            <h1>XUiDa64 Extreme Edition</h1>
            <div style="color: #9ca3af; font-size: 13px; margin-top: 4px;">Hardware Diagnostics & Benchmark Suite</div>
        </div>
        <div class="meta">
            <div>Report Generated: <strong>{now_str}</strong></div>
            <div>Computer: <strong>{sys_info.get('ComputerName')}</strong></div>
            <div>User: <strong>{sys_info.get('RegisteredUser')}</strong></div>
        </div>
    </div>

    <!-- Summary -->
    <div class="section-title">🖥️ Computer Summary</div>
    <table>
        <tr><td class="prop">Computer Name</td><td class="val">{sys_info.get('ComputerName')}</td></tr>
        <tr><td class="prop">Operating System</td><td class="val">{sys_info.get('OSName')} (Build {sys_info.get('Build')}) {sys_info.get('Architecture')}</td></tr>
        <tr><td class="prop">Motherboard</td><td class="val">{mb_info.get('Manufacturer')} {mb_info.get('Product')}</td></tr>
        <tr><td class="prop">BIOS Version</td><td class="val">{bios_info.get('Vendor')} {bios_info.get('Version')} ({bios_info.get('ReleaseDate')})</td></tr>
        <tr><td class="prop">Processor</td><td class="val">{cpu_details.get('Brand')} ({cpu_details.get('PhysicalCores')} Cores, {cpu_details.get('LogicalCores')} Threads)</td></tr>
        <tr><td class="prop">System Memory</td><td class="val">{mem_summary.get('TotalGB')} GB (Used: {mem_summary.get('UsedGB')} GB, Free: {mem_summary.get('FreeGB')} GB)</td></tr>
        <tr><td class="prop">Primary Graphics</td><td class="val">{gpus[0].get('Name') if gpus else 'Unknown'} ({gpus[0].get('VRAM_MB', 0)} MB)</td></tr>
        <tr><td class="prop">System Uptime</td><td class="val">{sys_info.get('Uptime')}</td></tr>
    </table>

    <!-- CPU Details -->
    <div class="section-title">⚡ Processor & CPUID</div>
    <table>
        <tr><td class="prop">CPU Model</td><td class="val">{cpu_details.get('Brand')}</td></tr>
        <tr><td class="prop">Signature / Stepping</td><td class="val">{cpu_details.get('Signature')}</td></tr>
        <tr><td class="prop">Socket</td><td class="val">{cpu_details.get('Socket')}</td></tr>
        <tr><td class="prop">Base / Current Clock</td><td class="val">{cpu_details.get('BaseClock')} / {cpu_details.get('CurrentClock')}</td></tr>
        <tr><td class="prop">Core Voltage</td><td class="val">{cpu_details.get('Voltage')}</td></tr>
        <tr><td class="prop">Cache Hierarchy</td><td class="val">{cpu_details.get('Caches')}</td></tr>
    </table>

    <!-- Memory & SPD -->
    <div class="section-title">📊 Memory & SPD Modules</div>
    <table>
        <thead>
            <tr><th>Slot</th><th>Module</th><th>Capacity</th><th>Speed</th><th>Type</th><th>Serial</th></tr>
        </thead>
        <tbody>
"""
        for m in spd_modules:
            html += f"""            <tr>
                <td>{m.get('DeviceLocator')}</td>
                <td>{m.get('Manufacturer')} {m.get('PartNumber')}</td>
                <td>{m.get('CapacityGB')} GB</td>
                <td>{m.get('SpeedMHz')} MHz</td>
                <td>{m.get('MemoryType')}</td>
                <td>{m.get('SerialNumber')}</td>
            </tr>\n"""

        html += """        </tbody>
    </table>

    <!-- Video & Display -->
    <div class="section-title">🎮 Display & Graphics</div>
    <table>
        <thead>
            <tr><th>Adapter Name</th><th>VRAM</th><th>Driver Version</th><th>Resolution</th><th>Temp</th></tr>
        </thead>
        <tbody>
"""
        for g in gpus:
            t_str = f"{g.get('Temperature')} °C" if g.get('Temperature') else "N/A"
            html += f"""            <tr>
                <td>{g.get('Name')}</td>
                <td>{g.get('VRAM_MB')} MB</td>
                <td>{g.get('DriverVersion')}</td>
                <td>{g.get('Resolution')}</td>
                <td>{t_str}</td>
            </tr>\n"""

        html += """        </tbody>
    </table>

    <!-- Storage -->
    <div class="section-title">💾 Storage & Drives</div>
    <table>
        <thead>
            <tr><th>Drive Model</th><th>Type</th><th>Bus</th><th>Capacity</th><th>Health</th></tr>
        </thead>
        <tbody>
"""
        for d in phys_drives:
            html += f"""            <tr>
                <td>{d.get('Model')}</td>
                <td>{d.get('MediaType')}</td>
                <td>{d.get('BusType')}</td>
                <td>{d.get('SizeGB')} GB</td>
                <td><span class="badge badge-ok">{d.get('Health')}</span></td>
            </tr>\n"""

        html += """        </tbody>
    </table>

    <!-- Network -->
    <div class="section-title">🌐 Network Adapters</div>
    <table>
        <thead>
            <tr><th>Adapter Name</th><th>Status</th><th>Speed</th><th>IPv4</th><th>MAC Address</th></tr>
        </thead>
        <tbody>
"""
        for a in adapters:
            html += f"""            <tr>
                <td>{a.get('Name')}</td>
                <td>{a.get('Status')}</td>
                <td>{a.get('Speed')}</td>
                <td>{a.get('IPv4')}</td>
                <td>{a.get('MAC')}</td>
            </tr>\n"""

        html += f"""        </tbody>
    </table>

    <!-- Sensors -->
    <div class="section-title">🌡️ Live Sensors</div>
    <table>
        <thead>
            <tr><th>Sensor</th><th>Value</th><th>Category</th></tr>
        </thead>
        <tbody>
"""
        for item in sensors.get("Temperatures", []) + sensors.get("Fans", []) + sensors.get("Powers", []):
            html += f"""            <tr>
                <td>{item.get('Sensor')}</td>
                <td>{item.get('Value')} {item.get('Unit')}</td>
                <td>{item.get('Category')}</td>
            </tr>\n"""

        html += f"""        </tbody>
    </table>

    <div class="footer">
        Generated by <strong>XUiDa64 Extreme Edition</strong> &bull; Open-Source Hardware Diagnostics &bull; Released under MIT License
    </div>
</div>
</body>
</html>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return filepath

if __name__ == "__main__":
    out_file = "sample_report.html"
    HTMLReportGenerator.generate(out_file)
    print("Report written to:", out_file)
