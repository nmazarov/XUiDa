"""
XUiDa64 - FPU Benchmark Suite
Implements FPU Julia, FPU Mandel, and FPU SinJulia.
"""

import time
import math
import numpy as np
import concurrent.futures
import psutil

class FPUBenchmarks:
    # -------------------------------------------------------------
    # FPU Julia (Single-precision 32-bit float)
    # -------------------------------------------------------------
    @staticmethod
    def _worker_julia(width=512, height=512, max_iter=64):
        # Grid of float32 complex numbers
        y, x = np.mgrid[-1.2:1.2:height*1j, -1.2:1.2:width*1j]
        c = np.complex64(-0.8 + 0.156j)
        z = (x + 1j * y).astype(np.complex64)

        t0 = time.perf_counter()
        for _ in range(3):
            z_curr = z.copy()
            for _ in range(max_iter):
                # z = z^2 + c
                mask = np.abs(z_curr) < 2.0
                z_curr[mask] = z_curr[mask] * z_curr[mask] + c
        t1 = time.perf_counter()
        elapsed = max(t1 - t0, 0.0001)
        ops = (width * height * max_iter * 3)
        return ops / elapsed

    @staticmethod
    def run_julia(progress_cb=None):
        """Runs multi-threaded FPU Julia benchmark, returns score."""
        threads = psutil.cpu_count(logical=True) or 4
        if progress_cb:
            progress_cb(20)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(FPUBenchmarks._worker_julia, 512, 512, 48) for _ in range(threads)]
            rates = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_rate = sum(rates)
        score = int(total_rate / 2500)
        if progress_cb:
            progress_cb(100)
        return score

    # -------------------------------------------------------------
    # FPU Mandel (Double-precision 64-bit float)
    # -------------------------------------------------------------
    @staticmethod
    def _worker_mandel(width=512, height=512, max_iter=48):
        y, x = np.mgrid[-1.5:1.5:height*1j, -2.0:1.0:width*1j]
        c = (x + 1j * y).astype(np.complex128)

        t0 = time.perf_counter()
        for _ in range(2):
            z = np.zeros_like(c)
            for _ in range(max_iter):
                mask = np.abs(z) < 2.0
                z[mask] = z[mask] * z[mask] + c[mask]
        t1 = time.perf_counter()
        elapsed = max(t1 - t0, 0.0001)
        ops = (width * height * max_iter * 2)
        return ops / elapsed

    @staticmethod
    def run_mandel(progress_cb=None):
        """Runs multi-threaded FPU Mandel benchmark, returns score."""
        threads = psutil.cpu_count(logical=True) or 4
        if progress_cb:
            progress_cb(20)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(FPUBenchmarks._worker_mandel, 512, 512, 40) for _ in range(threads)]
            rates = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_rate = sum(rates)
        score = int(total_rate / 3500)
        if progress_cb:
            progress_cb(100)
        return score

    # -------------------------------------------------------------
    # FPU SinJulia (Trigonometric single precision float)
    # -------------------------------------------------------------
    @staticmethod
    def _worker_sinjulia(width=256, height=256, max_iter=24):
        y, x = np.mgrid[-1.5:1.5:height*1j, -1.5:1.5:width*1j]
        z = (x + 1j * y).astype(np.complex64)
        c = np.complex64(1.0 + 0.1j)

        t0 = time.perf_counter()
        for _ in range(2):
            z_curr = z.copy()
            for _ in range(max_iter):
                # z = c * sin(z)
                mask = np.abs(z_curr) < 4.0
                z_curr[mask] = c * np.sin(z_curr[mask])
        t1 = time.perf_counter()
        elapsed = max(t1 - t0, 0.0001)
        ops = (width * height * max_iter * 2)
        return ops / elapsed

    @staticmethod
    def run_sinjulia(progress_cb=None):
        """Runs multi-threaded FPU SinJulia benchmark, returns score."""
        threads = psutil.cpu_count(logical=True) or 4
        if progress_cb:
            progress_cb(20)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(FPUBenchmarks._worker_sinjulia, 256, 256, 20) for _ in range(threads)]
            rates = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_rate = sum(rates)
        score = int(total_rate / 1200)
        if progress_cb:
            progress_cb(100)
        return score

if __name__ == "__main__":
    print("FPU Julia:", FPUBenchmarks.run_julia())
    print("FPU Mandel:", FPUBenchmarks.run_mandel())
    print("FPU SinJulia:", FPUBenchmarks.run_sinjulia())
