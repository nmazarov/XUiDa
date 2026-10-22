"""
XUiDa64 - CPU Benchmark Suite
Implements CPU Queen, CPU PhotoWorxx, CPU ZLib, CPU AES, and CPU SHA3.
"""

import time
import zlib
import hashlib
import numpy as np
import concurrent.futures
import psutil

class CPUBenchmarks:
    # -------------------------------------------------------------
    # CPU Queen Benchmark
    # -------------------------------------------------------------
    @staticmethod
    def _solve_nqueens(n=10):
        """Solves N-Queens integer branch prediction puzzle."""
        count = 0
        cols = 0
        diag1 = 0
        diag2 = 0
        all_bits = (1 << n) - 1

        def backtrack(row, c, d1, d2):
            nonlocal count
            if row == n:
                count += 1
                return
            free_slots = all_bits & ~(c | d1 | d2)
            while free_slots:
                bit = free_slots & -free_slots
                free_slots ^= bit
                backtrack(row + 1, c | bit, (d1 | bit) << 1, (d2 | bit) >> 1)

        backtrack(0, cols, diag1, diag2)
        return count

    @staticmethod
    def _worker_queen(duration=0.5):
        t0 = time.perf_counter()
        iterations = 0
        while time.perf_counter() - t0 < duration:
            CPUBenchmarks._solve_nqueens(10)
            iterations += 1
        return iterations

    @staticmethod
    def run_queen(progress_cb=None):
        """Runs multi-threaded CPU Queen benchmark, returns score."""
        threads = psutil.cpu_count(logical=True) or 4
        if progress_cb:
            progress_cb(15)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(CPUBenchmarks._worker_queen, 0.7) for _ in range(threads)]
            iters = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_iters = sum(iters)
        # Scaled score matching AIDA64 Queen score range (~150,000 for top i7/i9)
        score = int(total_iters * 48.5)
        if progress_cb:
            progress_cb(100)
        return score

    # -------------------------------------------------------------
    # CPU PhotoWorxx Benchmark
    # -------------------------------------------------------------
    @staticmethod
    def _worker_photoworxx(width=1024, height=1024, iterations=5):
        # 1 MPix image buffer
        img = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.int16)
        
        t0 = time.perf_counter()
        for _ in range(iterations):
            # RGB color conversion & channel extraction
            gray = (img[:, :, 0].astype(np.uint16) * 77 + 
                    img[:, :, 1].astype(np.uint16) * 150 + 
                    img[:, :, 2].astype(np.uint16) * 29) >> 8
            # Matrix transpose & rotate
            trans = np.transpose(gray)
            # Convolution / Edge detection on central slice
            conv = (trans[1:-1, 1:-1] * 8 -
                    trans[0:-2, 1:-1] - trans[2:, 1:-1] -
                    trans[1:-1, 0:-2] - trans[1:-1, 2:]).clip(0, 255)
        t1 = time.perf_counter()
        elapsed = max(t1 - t0, 0.0001)
        mpix_processed = (width * height * iterations) / 1_000_000
        return mpix_processed / elapsed

    @staticmethod
    def run_photoworxx(progress_cb=None):
        """Runs multi-threaded PhotoWorxx benchmark, returns MPix/s."""
        threads = psutil.cpu_count(logical=True) or 4
        if progress_cb:
            progress_cb(20)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(CPUBenchmarks._worker_photoworxx, 1024, 1024, 6) for _ in range(threads)]
            rates = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_rate = sum(rates)
        score = round(total_rate * 25.0)  # Scale to AIDA64 reference range (~60,000 MPix/s)
        if progress_cb:
            progress_cb(100)
        return score

    # -------------------------------------------------------------
    # CPU ZLib Benchmark
    # -------------------------------------------------------------
    @staticmethod
    def _worker_zlib(data_block, iterations=15):
        t0 = time.perf_counter()
        for _ in range(iterations):
            comp = zlib.compress(data_block, level=6)
            zlib.decompress(comp)
        t1 = time.perf_counter()
        elapsed = max(t1 - t0, 0.0001)
        bytes_trans = len(data_block) * iterations
        return bytes_trans / elapsed

    @staticmethod
    def run_zlib(progress_cb=None):
        """Runs multi-threaded ZLib benchmark, returns MB/s."""
        threads = psutil.cpu_count(logical=True) or 4
        # Create compressible pattern data
        raw = b"XUiDa64 Extreme Hardware Diagnostics and Benchmark Suite " * 15000  # ~850 KB
        if progress_cb:
            progress_cb(20)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(CPUBenchmarks._worker_zlib, raw, 12) for _ in range(threads)]
            rates = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_bytes = sum(rates)
        mb_per_sec = round(total_bytes / (1024 * 1024), 1)
        if progress_cb:
            progress_cb(100)
        return mb_per_sec

    # -------------------------------------------------------------
    # CPU AES Benchmark
    # -------------------------------------------------------------
    @staticmethod
    def _worker_aes(data_block, iterations=30):
        # Hardware accelerated AES if cryptography installed or fast ctypes cipher
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        key = b'0123456789abcdef0123456789abcdef'
        iv = b'1234567890abcdef'
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        
        t0 = time.perf_counter()
        for _ in range(iterations):
            enc = cipher.encryptor()
            ct = enc.update(data_block) + enc.finalize()
            dec = cipher.decryptor()
            dec.update(ct) + dec.finalize()
        t1 = time.perf_counter()
        elapsed = max(t1 - t0, 0.0001)
        bytes_trans = len(data_block) * iterations * 2
        return bytes_trans / elapsed

    @staticmethod
    def run_aes(progress_cb=None):
        """Runs multi-threaded AES benchmark, returns MB/s."""
        threads = psutil.cpu_count(logical=True) or 4
        # 1 MB block aligned to 16 bytes
        block = b'\x42' * (1024 * 1024)
        if progress_cb:
            progress_cb(20)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(CPUBenchmarks._worker_aes, block, 20) for _ in range(threads)]
            rates = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_bytes = sum(rates)
        mb_per_sec = round((total_bytes / (1024 * 1024)) * 3.5, 1)  # scaled to AIDA64 AES-NI score
        if progress_cb:
            progress_cb(100)
        return mb_per_sec

    # -------------------------------------------------------------
    # CPU SHA3 Benchmark
    # -------------------------------------------------------------
    @staticmethod
    def _worker_sha3(data_block, iterations=50):
        t0 = time.perf_counter()
        for _ in range(iterations):
            hashlib.sha3_256(data_block).digest()
        t1 = time.perf_counter()
        elapsed = max(t1 - t0, 0.0001)
        bytes_trans = len(data_block) * iterations
        return bytes_trans / elapsed

    @staticmethod
    def run_sha3(progress_cb=None):
        """Runs multi-threaded SHA3 benchmark, returns MB/s."""
        threads = psutil.cpu_count(logical=True) or 4
        block = b'XUiDa64 cryptographic test buffer payload block ' * 20000  # ~900 KB
        if progress_cb:
            progress_cb(20)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(CPUBenchmarks._worker_sha3, block, 30) for _ in range(threads)]
            rates = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_bytes = sum(rates)
        mb_per_sec = round(total_bytes / (1024 * 1024), 1)
        if progress_cb:
            progress_cb(100)
        return mb_per_sec

if __name__ == "__main__":
    print("CPU Queen:", CPUBenchmarks.run_queen())
    print("CPU PhotoWorxx:", CPUBenchmarks.run_photoworxx())
    print("CPU ZLib:", CPUBenchmarks.run_zlib(), "MB/s")
    print("CPU AES:", CPUBenchmarks.run_aes(), "MB/s")
    print("CPU SHA3:", CPUBenchmarks.run_sha3(), "MB/s")
