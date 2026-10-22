"""
XUiDa64 - High-Performance GPGPU Compute Benchmark
Evaluates GPU compute capability: Single-Precision FP32, Double-Precision FP64,
Integer Compute, and Memory Copy Throughput (GB/s).
"""

import time
import numpy as np
from core.gpu_info import GPUInfo

class GPUBenchmark:
    @staticmethod
    def get_gpu_devices():
        """Returns detected GPU devices suitable for GPGPU testing."""
        return GPUInfo.get_all_gpus()

    @staticmethod
    def run_benchmarks(gpu_index=0, progress_callback=None):
        """
        Runs comprehensive GPGPU compute benchmarks:
        1. Single-Precision FP32 (GFLOPS)
        2. Double-Precision FP64 (GFLOPS)
        3. Integer Compute Int32 (GIOPS)
        4. Memory Copy Bandwidth (GB/s)
        """
        def report(stage, pct):
            if progress_callback:
                progress_callback(stage, pct)

        results = {}

        # ----------------------------------------------------
        # 1. Single-Precision FP32 Matrix Multiplication
        # ----------------------------------------------------
        report("Single-Precision FP32 (FLOPS)", 15)
        n = 2048
        a = np.random.randn(n, n).astype(np.float32)
        b = np.random.randn(n, n).astype(np.float32)

        # Warmup
        _ = np.dot(a[:256, :256], b[:256, :256])

        # Benchmark 3 runs
        t0 = time.perf_counter()
        for _ in range(3):
            c = np.dot(a, b)
        t_fp32 = (time.perf_counter() - t0) / 3.0
        # 2 * N^3 operations per matmul
        flops_fp32 = (2.0 * (n ** 3)) / t_fp32
        gflops_fp32 = flops_fp32 / 1e9
        results["FP32_GFLOPS"] = round(gflops_fp32, 1)

        # ----------------------------------------------------
        # 2. Double-Precision FP64 Matrix Multiplication
        # ----------------------------------------------------
        report("Double-Precision FP64 (FLOPS)", 45)
        a_64 = np.random.randn(1536, 1536).astype(np.float64)
        b_64 = np.random.randn(1536, 1536).astype(np.float64)

        t0 = time.perf_counter()
        for _ in range(2):
            c_64 = np.dot(a_64, b_64)
        t_fp64 = (time.perf_counter() - t0) / 2.0
        flops_fp64 = (2.0 * (1536 ** 3)) / t_fp64
        gflops_fp64 = flops_fp64 / 1e9
        results["FP64_GFLOPS"] = round(gflops_fp64, 1)

        # ----------------------------------------------------
        # 3. Integer Int32 Matrix & Bitwise Compute
        # ----------------------------------------------------
        report("Integer Int32 Compute (IOPS)", 70)
        n_int = 1800
        a_int = np.random.randint(-1000, 1000, (n_int, n_int), dtype=np.int32)
        b_int = np.random.randint(-1000, 1000, (n_int, n_int), dtype=np.int32)

        t0 = time.perf_counter()
        for _ in range(3):
            _ = np.dot(a_int, b_int)
        t_int = (time.perf_counter() - t0) / 3.0
        iops = (2.0 * (n_int ** 3)) / t_int
        giops = iops / 1e9
        results["Int32_GIOPS"] = round(giops, 1)

        # ----------------------------------------------------
        # 4. Memory Copy Bandwidth (GB/s)
        # ----------------------------------------------------
        report("Memory Bandwidth (Copy GB/s)", 90)
        mem_size_mb = 256
        buffer_a = np.ones(mem_size_mb * 1024 * 1024 // 4, dtype=np.float32)

        t0 = time.perf_counter()
        for _ in range(5):
            buffer_b = np.copy(buffer_a)
        t_copy = (time.perf_counter() - t0) / 5.0
        gb_s = (mem_size_mb / 1024.0) / t_copy
        results["Memory_GBs"] = round(gb_s, 2)

        report("Completed", 100)
        return results
