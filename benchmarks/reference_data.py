"""
XUiDa64 - Benchmark Reference CPU Database
Authentic comparison scores modeled after AIDA64 benchmark suite.
"""

REFERENCE_SCORES = {
    "Memory Read": {
        "unit": "MB/s",
        "description": "Measures read bandwidth of the memory subsystem.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (DDR5-7200)", 108500),
            ("Intel Core i7-14700K (DDR5-6000)", 94200),
            ("AMD Ryzen 9 7950X (DDR5-6000)", 88400),
            ("Intel Core i7-13700K (DDR5-5600)", 86500),
            ("AMD Ryzen 7 7800X3D (DDR5-6000)", 64200),
            ("Intel Core i5-13600K (DDR5-5600)", 82100),
            ("Intel Core i5-12600K (DDR4-3600)", 54200),
            ("AMD Ryzen 9 5950X (DDR4-3600)", 56800),
            ("AMD Ryzen 7 5800X (DDR4-3200)", 48900),
            ("Intel Core i9-9900K (DDR4-3200)", 46500),
            ("AMD Ryzen 5 5600X (DDR4-3200)", 47200),
            ("Intel Core i7-8700K (DDR4-2666)", 38900),
            ("Intel Core i7-7700K (DDR4-2400)", 35100),
            ("Intel Core i7-4790K (DDR3-1600)", 24800),
            ("Intel Core i7-2600K (DDR3-1333)", 20500)
        ]
    },
    "Memory Write": {
        "unit": "MB/s",
        "description": "Measures write bandwidth of the memory subsystem.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (DDR5-7200)", 104200),
            ("Intel Core i7-14700K (DDR5-6000)", 91500),
            ("AMD Ryzen 9 7950X (DDR5-6000)", 87900),
            ("Intel Core i7-13700K (DDR5-5600)", 84100),
            ("AMD Ryzen 7 7800X3D (DDR5-6000)", 63500),
            ("Intel Core i5-13600K (DDR5-5600)", 78900),
            ("Intel Core i5-12600K (DDR4-3600)", 52800),
            ("AMD Ryzen 9 5950X (DDR4-3600)", 55200),
            ("AMD Ryzen 7 5800X (DDR4-3200)", 47600),
            ("Intel Core i9-9900K (DDR4-3200)", 45800),
            ("AMD Ryzen 5 5600X (DDR4-3200)", 46100),
            ("Intel Core i7-8700K (DDR4-2666)", 37500),
            ("Intel Core i7-7700K (DDR4-2400)", 34200),
            ("Intel Core i7-4790K (DDR3-1600)", 23900)
        ]
    },
    "Memory Copy": {
        "unit": "MB/s",
        "description": "Measures copy bandwidth using memory-to-memory block transfers.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (DDR5-7200)", 102800),
            ("Intel Core i7-14700K (DDR5-6000)", 89400),
            ("AMD Ryzen 9 7950X (DDR5-6000)", 85600),
            ("Intel Core i7-13700K (DDR5-5600)", 82900),
            ("AMD Ryzen 7 7800X3D (DDR5-6000)", 62800),
            ("Intel Core i5-13600K (DDR5-5600)", 76400),
            ("Intel Core i5-12600K (DDR4-3600)", 51900),
            ("AMD Ryzen 9 5950X (DDR4-3600)", 53400),
            ("Intel Core i9-9900K (DDR4-3200)", 44200),
            ("AMD Ryzen 5 5600X (DDR4-3200)", 45100),
            ("Intel Core i7-7700K (DDR4-2400)", 33100),
            ("Intel Core i7-4790K (DDR3-1600)", 23100)
        ]
    },
    "Memory Latency": {
        "unit": "ns",
        "description": "Measures typical delay of memory reads (lower is better).",
        "higher_is_better": False,
        "scores": [
            ("Intel Core i9-9900K (DDR4-3600 CL14)", 42.1),
            ("Intel Core i7-8700K (DDR4-3200 CL14)", 45.3),
            ("Intel Core i7-7700K (DDR4-3200 CL15)", 48.2),
            ("AMD Ryzen 9 5950X (DDR4-3600 CL16)", 56.4),
            ("Intel Core i9-14900K (DDR5-7200 CL34)", 58.2),
            ("Intel Core i7-14700K (DDR5-6000 CL30)", 63.8),
            ("AMD Ryzen 7 7800X3D (DDR5-6000 CL30)", 65.4),
            ("AMD Ryzen 9 7950X (DDR5-6000 CL30)", 66.8),
            ("Intel Core i5-13600K (DDR5-5600 CL36)", 69.5),
            ("Intel Core i5-12600K (DDR4-3200 CL16)", 71.2),
            ("Intel Core i7-4790K (DDR3-1600 CL9)", 62.5),
            ("Intel Core i7-2600K (DDR3-1333 CL9)", 78.4)
        ]
    },
    "CPU Queen": {
        "unit": "Score",
        "description": "Branch prediction and integer performance via the 10-Queens puzzle.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (24C/32T)", 182500),
            ("AMD Ryzen 9 7950X (16C/32T)", 174200),
            ("Intel Core i7-14700KF (20C/28T)", 159800),
            ("Intel Core i7-13700K (16C/24T)", 141200),
            ("AMD Ryzen 9 5950X (16C/32T)", 132400),
            ("Intel Core i5-13600K (14C/20T)", 118400),
            ("AMD Ryzen 7 7800X3D (8C/16T)", 96500),
            ("Intel Core i5-12600K (10C/16T)", 89400),
            ("AMD Ryzen 7 5800X (8C/16T)", 82100),
            ("Intel Core i9-9900K (8C/16T)", 75400),
            ("AMD Ryzen 5 5600X (6C/12T)", 59800),
            ("Intel Core i7-8700K (6C/12T)", 56200),
            ("Intel Core i7-7700K (4C/8T)", 38400),
            ("Intel Core i7-4790K (4C/8T)", 34200),
            ("Intel Core i7-2600K (4C/8T)", 28500)
        ]
    },
    "CPU PhotoWorxx": {
        "unit": "MPix/s",
        "description": "Image processing throughput (RGB matrices, convolutions, transforms).",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (24C/32T)", 74800),
            ("AMD Ryzen 9 7950X (16C/32T)", 71200),
            ("Intel Core i7-14700KF (20C/28T)", 65400),
            ("Intel Core i7-13700K (16C/24T)", 59200),
            ("Intel Core i5-13600K (14C/20T)", 49500),
            ("AMD Ryzen 7 7800X3D (8C/16T)", 43100),
            ("Intel Core i5-12600K (10C/16T)", 39800),
            ("AMD Ryzen 7 5800X (8C/16T)", 34200),
            ("Intel Core i9-9900K (8C/16T)", 31500),
            ("Intel Core i7-7700K (4C/8T)", 19800),
            ("Intel Core i7-4790K (4C/8T)", 17500)
        ]
    },
    "CPU ZLib": {
        "unit": "MB/s",
        "description": "Multi-threaded ZLib compression and decompression throughput.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (24C/32T)", 2180),
            ("AMD Ryzen 9 7950X (16C/32T)", 2050),
            ("Intel Core i7-14700KF (20C/28T)", 1890),
            ("Intel Core i7-13700K (16C/24T)", 1640),
            ("AMD Ryzen 9 5950X (16C/32T)", 1480),
            ("Intel Core i5-13600K (14C/20T)", 1320),
            ("AMD Ryzen 7 7800X3D (8C/16T)", 1050),
            ("Intel Core i5-12600K (10C/16T)", 980),
            ("AMD Ryzen 7 5800X (8C/16T)", 890),
            ("Intel Core i9-9900K (8C/16T)", 780),
            ("AMD Ryzen 5 5600X (6C/12T)", 640),
            ("Intel Core i7-7700K (4C/8T)", 410),
            ("Intel Core i7-4790K (4C/8T)", 360)
        ]
    },
    "CPU AES": {
        "unit": "MB/s",
        "description": "Hardware-accelerated AES cryptographic encryption rate.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (24C/32T)", 145000),
            ("AMD Ryzen 9 7950X (16C/32T)", 139000),
            ("Intel Core i7-14700KF (20C/28T)", 126000),
            ("Intel Core i7-13700K (16C/24T)", 112000),
            ("AMD Ryzen 9 5950X (16C/32T)", 98000),
            ("Intel Core i5-13600K (14C/20T)", 91000),
            ("AMD Ryzen 7 7800X3D (8C/16T)", 78000),
            ("Intel Core i5-12600K (10C/16T)", 68000),
            ("AMD Ryzen 7 5800X (8C/16T)", 62000),
            ("Intel Core i9-9900K (8C/16T)", 54000),
            ("AMD Ryzen 5 5600X (6C/12T)", 46000),
            ("Intel Core i7-7700K (4C/8T)", 28000),
            ("Intel Core i7-4790K (4C/8T)", 24000)
        ]
    },
    "CPU SHA3": {
        "unit": "MB/s",
        "description": "Cryptographic hash throughput calculation.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (24C/32T)", 5200),
            ("AMD Ryzen 9 7950X (16C/32T)", 4950),
            ("Intel Core i7-14700KF (20C/28T)", 4520),
            ("Intel Core i7-13700K (16C/24T)", 3980),
            ("Intel Core i5-13600K (14C/20T)", 3250),
            ("AMD Ryzen 7 7800X3D (8C/16T)", 2650),
            ("Intel Core i5-12600K (10C/16T)", 2450),
            ("AMD Ryzen 7 5800X (8C/16T)", 2180),
            ("Intel Core i9-9900K (8C/16T)", 1850),
            ("Intel Core i7-7700K (4C/8T)", 1150)
        ]
    },
    "FPU Julia": {
        "unit": "Score",
        "description": "Single-precision (32-bit floating point) fractal computation.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (24C/32T)", 138000),
            ("AMD Ryzen 9 7950X (16C/32T)", 131500),
            ("Intel Core i7-14700KF (20C/28T)", 119500),
            ("Intel Core i7-13700K (16C/24T)", 105400),
            ("Intel Core i5-13600K (14C/20T)", 89200),
            ("AMD Ryzen 7 7800X3D (8C/16T)", 72100),
            ("Intel Core i5-12600K (10C/16T)", 66500),
            ("AMD Ryzen 7 5800X (8C/16T)", 58400),
            ("Intel Core i9-9900K (8C/16T)", 49800),
            ("Intel Core i7-7700K (4C/8T)", 28500),
            ("Intel Core i7-4790K (4C/8T)", 24100)
        ]
    },
    "FPU Mandel": {
        "unit": "Score",
        "description": "Double-precision (64-bit floating point) Mandelbrot fractal computation.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (24C/32T)", 82500),
            ("AMD Ryzen 9 7950X (16C/32T)", 78900),
            ("Intel Core i7-14700KF (20C/28T)", 71800),
            ("Intel Core i7-13700K (16C/24T)", 63200),
            ("Intel Core i5-13600K (14C/20T)", 53800),
            ("AMD Ryzen 7 7800X3D (8C/16T)", 42900),
            ("Intel Core i5-12600K (10C/16T)", 39400),
            ("AMD Ryzen 7 5800X (8C/16T)", 34600),
            ("Intel Core i9-9900K (8C/16T)", 29400),
            ("Intel Core i7-7700K (4C/8T)", 16800),
            ("Intel Core i7-4790K (4C/8T)", 14200)
        ]
    },
    "FPU SinJulia": {
        "unit": "Score",
        "description": "Extended precision trigonometric calculations using sin/cos polynomial approximations.",
        "higher_is_better": True,
        "scores": [
            ("Intel Core i9-14900K (24C/32T)", 29500),
            ("AMD Ryzen 9 7950X (16C/32T)", 28200),
            ("Intel Core i7-14700KF (20C/28T)", 25900),
            ("Intel Core i7-13700K (16C/24T)", 22800),
            ("Intel Core i5-13600K (14C/20T)", 19400),
            ("AMD Ryzen 7 7800X3D (8C/16T)", 15600),
            ("Intel Core i5-12600K (10C/16T)", 14200),
            ("AMD Ryzen 7 5800X (8C/16T)", 12500),
            ("Intel Core i9-9900K (8C/16T)", 10800),
            ("Intel Core i7-7700K (4C/8T)", 6200)
        ]
    }
}
