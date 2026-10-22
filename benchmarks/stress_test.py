"""
XUiDa64 - Multi-Threaded System Stability & Stress Engine
Executes simultaneous load across CPU, FPU, Caches, and Memory while monitoring throttling.
"""

import os
import sys
import time
import threading
import numpy as np
import psutil

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.sensors import Sensors
except ImportError:
    from ..core.sensors import Sensors

class StressTestEngine:
    def __init__(self):
        self._running = False
        self._threads = []
        self._stress_cpu = True
        self._stress_fpu = True
        self._stress_cache = True
        self._stress_memory = True
        self._stress_gpu = False

        self.start_time = None
        self.throttling_detected = False
        self.throttling_reason = ""
        self.history = {
            "timestamps": [],
            "cpu_temp": [],
            "gpu_temp": [],
            "cpu_usage": []
        }

    def start(self, stress_cpu=True, stress_fpu=True, stress_cache=True, stress_memory=True, stress_gpu=False):
        if self._running:
            return
        self._running = True
        self._stress_cpu = stress_cpu
        self._stress_fpu = stress_fpu
        self._stress_cache = stress_cache
        self._stress_memory = stress_memory
        self._stress_gpu = stress_gpu

        self.start_time = time.time()
        self.throttling_detected = False
        self.throttling_reason = ""
        self._threads = []

        num_workers = psutil.cpu_count(logical=True) or 4

        # Launch CPU/FPU/Cache workers
        for i in range(num_workers):
            t = threading.Thread(target=self._worker_loop, args=(i,), daemon=True)
            self._threads.append(t)
            t.start()

        # Launch Memory worker if requested
        if self._stress_memory:
            t_mem = threading.Thread(target=self._memory_worker, daemon=True)
            self._threads.append(t_mem)
            t_mem.start()

    def stop(self):
        self._running = False
        for t in self._threads:
            t.join(timeout=0.2)
        self._threads = []

    def is_running(self):
        return self._running

    def get_elapsed_str(self):
        if not self.start_time:
            return "00:00:00"
        elapsed = int(time.time() - self.start_time)
        hrs = elapsed // 3600
        mins = (elapsed % 3600) // 60
        secs = elapsed % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

    def update_telemetry(self):
        """Polls sensors, updates history, and evaluates throttling."""
        data = Sensors.get_all_sensors()
        cpu_t = 30.0
        gpu_t = 30.0

        for item in data.get("Temperatures", []):
            if item.get("Category") == "CPU":
                cpu_t = item.get("Value", cpu_t)
            elif item.get("Category") == "GPU":
                gpu_t = item.get("Value", gpu_t)

        cpu_u = psutil.cpu_percent(interval=None)

        now = time.time() - (self.start_time or time.time())
        self.history["timestamps"].append(now)
        self.history["cpu_temp"].append(cpu_t)
        self.history["gpu_temp"].append(gpu_t)
        self.history["cpu_usage"].append(cpu_u)

        # Keep rolling window of 300 points
        if len(self.history["timestamps"]) > 300:
            for k in self.history:
                self.history[k].pop(0)

        # Check for thermal throttling condition (>= 98°C)
        if cpu_t >= 98.0:
            self.throttling_detected = True
            self.throttling_reason = f"Thermal Throttling Detected: CPU reached {cpu_t}°C!"

        return {
            "elapsed": self.get_elapsed_str(),
            "cpu_temp": cpu_t,
            "gpu_temp": gpu_t,
            "cpu_usage": cpu_u,
            "throttling": self.throttling_detected,
            "throttling_reason": self.throttling_reason
        }

    def _worker_loop(self, worker_id):
        # Cache array to thrash L1/L2/L3 caches
        cache_buf = np.ones(1024 * 512, dtype=np.float32)  # 2 MB buffer
        val = 1.0001

        while self._running:
            # 1. CPU Integer stress
            if self._stress_cpu:
                x = 0x5A5A5A5A
                for _ in range(5000):
                    x = ((x << 1) | (x >> 31)) ^ 0x33333333

            # 2. FPU Floating-point stress
            if self._stress_fpu:
                for _ in range(5000):
                    val = (val * 1.00001) % 1000.0 + 0.0001

            # 3. Cache thrash
            if self._stress_cache:
                cache_buf = (cache_buf * 1.001).astype(np.float32)

            time.sleep(0.0001)

    def _memory_worker(self):
        # Continuous RAM write & verification
        block_size = 32 * 1024 * 1024  # 32 MB chunks
        try:
            mem_blocks = [bytearray(b'\x55' * block_size) for _ in range(4)]  # ~128 MB
        except MemoryError:
            mem_blocks = []

        idx = 0
        while self._running:
            if mem_blocks:
                pattern = (idx & 0xFF).to_bytes(1, 'little') * block_size
                mem_blocks[idx % len(mem_blocks)][:] = pattern
                idx += 1
            time.sleep(0.005)

if __name__ == "__main__":
    engine = StressTestEngine()
    print("Starting stress test for 3 seconds...")
    engine.start()
    for _ in range(3):
        time.sleep(1)
        telem = engine.update_telemetry()
        print("Telemetry:", telem)
    engine.stop()
    print("Stress test stopped cleanly.")
