"""
XUiDa64 - High-Precision Disk Storage Benchmark
Evaluates real-world NVMe, SSD, and HDD throughput: Sequential Read/Write, Random 4K, and Latency.
Includes automatic safety cleanup of temporary benchmark files.
"""

import os
import time
import random
import psutil

class DiskBenchmark:
    @staticmethod
    def get_drives():
        """Returns list of active local storage partitions suitable for benchmarking."""
        drives = []
        for p in psutil.disk_partitions(all=False):
            if "cdrom" in p.opts or not p.fstype:
                continue
            try:
                usage = psutil.disk_usage(p.mountpoint)
                free_gb = usage.free / (1024 ** 3)
                total_gb = usage.total / (1024 ** 3)
                drives.append({
                    "device": p.device,
                    "mountpoint": p.mountpoint,
                    "fstype": p.fstype,
                    "free_gb": round(free_gb, 1),
                    "total_gb": round(total_gb, 1),
                    "percent_used": usage.percent
                })
            except Exception:
                pass
        return drives

    @staticmethod
    def run_benchmark(target_dir, file_size_mb=128, progress_callback=None):
        """
        Runs comprehensive disk throughput suite:
        1. Sequential Write (MB/s)
        2. Sequential Read (MB/s)
        3. Random 4K Read (MB/s & IOPS)
        4. Random 4K Write (MB/s & IOPS)
        5. Access Latency (ms)
        """
        def report(stage, percent, speed_mbs=0.0):
            if progress_callback:
                progress_callback(stage, percent, speed_mbs)

        test_path = os.path.join(target_dir, f"xuida_diskbench_{int(time.time())}.tmp")
        block_1m = os.urandom(1024 * 1024)
        total_bytes = file_size_mb * 1024 * 1024

        results = {}

        try:
            # ----------------------------------------------------
            # 1. Sequential Write
            # ----------------------------------------------------
            report("Seq Write", 5, 0.0)
            t_start = time.perf_counter()
            with open(test_path, "wb") as f:
                for i in range(file_size_mb):
                    f.write(block_1m)
                    pct = 5 + int((i / file_size_mb) * 20)
                    elapsed = max(0.001, time.perf_counter() - t_start)
                    cur_speed = ((i + 1) * 1.0) / elapsed
                    report("Seq Write", pct, cur_speed)
                f.flush()
                os.fsync(f.fileno())
            t_write = max(0.001, time.perf_counter() - t_start)
            seq_write_speed = file_size_mb / t_write
            results["Seq Write"] = round(seq_write_speed, 1)

            # ----------------------------------------------------
            # 2. Sequential Read
            # ----------------------------------------------------
            report("Seq Read", 30, 0.0)
            t_start = time.perf_counter()
            bytes_read = 0
            with open(test_path, "rb") as f:
                while True:
                    chunk = f.read(1024 * 1024)
                    if not chunk:
                        break
                    bytes_read += len(chunk)
                    pct = 30 + int((bytes_read / total_bytes) * 25)
                    elapsed = max(0.001, time.perf_counter() - t_start)
                    cur_speed = (bytes_read / (1024 * 1024)) / elapsed
                    report("Seq Read", pct, cur_speed)
            t_read = max(0.001, time.perf_counter() - t_start)
            seq_read_speed = file_size_mb / t_read
            results["Seq Read"] = round(seq_read_speed, 1)

            # ----------------------------------------------------
            # 3. Random 4K Read (IOPS & Throughput)
            # ----------------------------------------------------
            report("Rnd 4K Read", 60, 0.0)
            block_4k_size = 4096
            max_offset = total_bytes - block_4k_size
            sample_ops = 1500

            t_start = time.perf_counter()
            with open(test_path, "rb") as f:
                for i in range(sample_ops):
                    offset = random.randint(0, max_offset)
                    f.seek(offset)
                    _ = f.read(block_4k_size)
                    if i % 100 == 0:
                        pct = 60 + int((i / sample_ops) * 15)
                        elapsed = max(0.001, time.perf_counter() - t_start)
                        cur_speed = (i * block_4k_size / (1024 * 1024)) / elapsed
                        report("Rnd 4K Read", pct, cur_speed)
            t_rnd_read = max(0.001, time.perf_counter() - t_start)
            rnd_read_iops = sample_ops / t_rnd_read
            rnd_read_speed = (sample_ops * 4.0 / 1024.0) / t_rnd_read
            results["Rnd 4K Read (IOPS)"] = int(rnd_read_iops)
            results["Rnd 4K Read (MB/s)"] = round(rnd_read_speed, 2)

            # ----------------------------------------------------
            # 4. Random 4K Write
            # ----------------------------------------------------
            report("Rnd 4K Write", 80, 0.0)
            rnd_4k_block = os.urandom(4096)
            write_ops = 600

            t_start = time.perf_counter()
            with open(test_path, "r+b") as f:
                for i in range(write_ops):
                    offset = random.randint(0, max_offset)
                    f.seek(offset)
                    f.write(rnd_4k_block)
                    if i % 50 == 0:
                        pct = 80 + int((i / write_ops) * 15)
                        elapsed = max(0.001, time.perf_counter() - t_start)
                        cur_speed = (i * block_4k_size / (1024 * 1024)) / elapsed
                        report("Rnd 4K Write", pct, cur_speed)
                f.flush()
                os.fsync(f.fileno())
            t_rnd_write = max(0.001, time.perf_counter() - t_start)
            rnd_write_iops = write_ops / t_rnd_write
            rnd_write_speed = (write_ops * 4.0 / 1024.0) / t_rnd_write
            results["Rnd 4K Write (IOPS)"] = int(rnd_write_iops)
            results["Rnd 4K Write (MB/s)"] = round(rnd_write_speed, 2)

            # ----------------------------------------------------
            # 5. Access Latency (ms)
            # ----------------------------------------------------
            report("Access Latency", 96, 0.0)
            latency_ms = (t_rnd_read / sample_ops) * 1000.0
            results["Access Latency (ms)"] = round(latency_ms, 3)

            report("Completed", 100, 0.0)
            return results

        finally:
            # Guarantee test file is completely removed
            if os.path.exists(test_path):
                try:
                    os.remove(test_path)
                except Exception:
                    pass
