"""
XUiDa64 - Network Adapters & Traffic Monitor Module
"""

import time
import socket
import psutil
import win32com.client

class NetworkInfo:
    _last_io = None
    _last_time = None

    @staticmethod
    def get_adapters():
        adapters = []
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()

        wmi_details = {}
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            for cfg in wmi.InstancesOf("Win32_NetworkAdapterConfiguration"):
                if cfg.IPEnabled:
                    desc = getattr(cfg, "Description", "").strip()
                    wmi_details[desc] = {
                        "Gateways": list(getattr(cfg, "DefaultIPGateway", []) or []),
                        "DNSServers": list(getattr(cfg, "DNSServerSearchOrder", []) or []),
                        "DHCPEnabled": getattr(cfg, "DHCPEnabled", False),
                        "DHCPServer": getattr(cfg, "DHCPServer", "")
                    }
        except Exception:
            pass

        for iface_name, addr_list in addrs.items():
            stat = stats.get(iface_name)
            is_up = stat.isup if stat else False
            speed_mbps = stat.speed if stat else 0

            ipv4 = []
            ipv6 = []
            mac = "Unknown"
            netmask = ""

            for a in addr_list:
                if a.family == socket.AF_INET:
                    ipv4.append(a.address)
                    if not netmask and a.netmask:
                        netmask = a.netmask
                elif a.family == socket.AF_INET6:
                    ipv6.append(a.address)
                elif hasattr(psutil, "AF_LINK") and a.family == psutil.AF_LINK:
                    mac = a.address

            # Match WMI details
            extra = wmi_details.get(iface_name, {})
            if not extra:
                for k, v in wmi_details.items():
                    if k in iface_name or iface_name in k:
                        extra = v
                        break

            # Filter out virtual/loopback unless requested
            adapters.append({
                "Name": iface_name,
                "Status": "Connected" if is_up else "Disconnected",
                "Speed": f"{speed_mbps} Mbps" if speed_mbps > 0 else "Auto / Virtual",
                "IPv4": ", ".join(ipv4) if ipv4 else "None",
                "IPv6": ", ".join(ipv6[:1]) if ipv6 else "None",
                "Netmask": netmask or "255.255.255.0",
                "MAC": mac,
                "Gateways": ", ".join(extra.get("Gateways", [])) or "N/A",
                "DNSServers": ", ".join(extra.get("DNSServers", [])) or "N/A",
                "DHCP": "Enabled" if extra.get("DHCPEnabled") else "Manual"
            })
        return adapters

    @classmethod
    def get_realtime_traffic(cls):
        """Returns current download & upload rates in KB/s and total MB."""
        now = time.time()
        curr_io = psutil.net_io_counters()

        if cls._last_io is None or cls._last_time is None:
            cls._last_io = curr_io
            cls._last_time = now
            return {
                "UploadKBps": 0.0,
                "DownloadKBps": 0.0,
                "BytesSentMB": round(curr_io.bytes_sent / (1024**2), 1),
                "BytesRecvMB": round(curr_io.bytes_recv / (1024**2), 1)
            }

        delta_time = max(now - cls._last_time, 0.001)
        up_rate = (curr_io.bytes_sent - cls._last_io.bytes_sent) / delta_time / 1024
        down_rate = (curr_io.bytes_recv - cls._last_io.bytes_recv) / delta_time / 1024

        cls._last_io = curr_io
        cls._last_time = now

        return {
            "UploadKBps": round(up_rate, 1),
            "DownloadKBps": round(down_rate, 1),
            "BytesSentMB": round(curr_io.bytes_sent / (1024**2), 1),
            "BytesRecvMB": round(curr_io.bytes_recv / (1024**2), 1)
        }

if __name__ == "__main__":
    print("Adapters:", NetworkInfo.get_adapters()[:2])
    print("Traffic:", NetworkInfo.get_realtime_traffic())
