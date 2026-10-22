"""
XUiDa64 - Direct x86/x64 CPUID Decoder
Executes native CPUID instructions and decodes processor flags, architecture, and cache topology.
"""

import ctypes
import struct

class CPUID:
    _func = None
    _available = False

    @classmethod
    def _init_native(cls):
        if cls._func is not None:
            return cls._available

        try:
            # 64-bit Windows CPUID machine code:
            # Calling convention: rcx = eax_in, rdx = ecx_in, r8 = out_regs (pointer to 4 uint32)
            code = bytes([
                0x89, 0xc8,             # mov eax, ecx
                0x89, 0xd1,             # mov ecx, edx
                0x53,                   # push rbx
                0x0f, 0xa2,             # cpuid
                0x41, 0x89, 0x00,       # mov [r8], eax
                0x41, 0x89, 0x58, 0x04, # mov [r8+4], ebx
                0x41, 0x89, 0x48, 0x08, # mov [r8+8], ecx
                0x41, 0x89, 0x50, 0x0c, # mov [r8+12], edx
                0x5b,                   # pop rbx
                0xc3                    # ret
            ])

            kernel32 = ctypes.windll.kernel32
            kernel32.VirtualAlloc.restype = ctypes.c_void_p
            kernel32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_uint32]

            MEM_COMMIT = 0x1000
            PAGE_EXECUTE_READWRITE = 0x40
            addr = kernel32.VirtualAlloc(None, len(code), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
            if not addr:
                cls._available = False
                return False

            ctypes.memmove(addr, code, len(code))
            func_type = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32))
            cls._func = func_type(addr)
            cls._available = True
            return True
        except Exception:
            cls._available = False
            return False

    @classmethod
    def call(cls, eax: int, ecx: int = 0):
        if not cls._init_native():
            return 0, 0, 0, 0
        regs = (ctypes.c_uint32 * 4)()
        cls._func(eax, ecx, regs)
        return regs[0], regs[1], regs[2], regs[3]

    @classmethod
    def get_info(cls):
        """Returns structured dictionary of CPUID information."""
        if not cls._init_native():
            return {"error": "CPUID execution unavailable"}

        # Leaf 0: Vendor String & Max Leaf
        max_leaf, ebx, ecx, edx = cls.call(0, 0)
        vendor = b''.join([
            ebx.to_bytes(4, 'little'),
            edx.to_bytes(4, 'little'),
            ecx.to_bytes(4, 'little')
        ]).decode('ascii', errors='ignore')

        # Brand String (Leaf 0x80000002 - 0x80000004)
        brand_parts = []
        for leaf in [0x80000002, 0x80000003, 0x80000004]:
            r0, r1, r2, r3 = cls.call(leaf, 0)
            for r in [r0, r1, r2, r3]:
                brand_parts.append(r.to_bytes(4, 'little'))
        brand = b''.join(brand_parts).decode('latin1', errors='ignore').replace('\x00', '').strip()

        # Leaf 1: Family, Model, Stepping & Base Features
        eax1, ebx1, ecx1, edx1 = cls.call(1, 0)
        stepping = eax1 & 0xF
        model = (eax1 >> 4) & 0xF
        family = (eax1 >> 8) & 0xF
        proc_type = (eax1 >> 12) & 0x3
        ext_model = (eax1 >> 16) & 0xF
        ext_family = (eax1 >> 20) & 0xFF

        display_family = family
        display_model = model
        if family in (6, 15):
            display_model = (ext_model << 4) | model
        if family == 15:
            display_family = family + ext_family

        # Brand Index / APIC
        logical_cores = (ebx1 >> 16) & 0xFF
        apic_id = (ebx1 >> 24) & 0xFF

        # Leaf 7: Extended features (AVX2, AVX-512, SHA, etc.)
        eax7, ebx7, ecx7, edx7 = cls.call(7, 0)

        # Extended Leaf 0x80000001
        eax81, ebx81, ecx81, edx81 = cls.call(0x80000001, 0)

        # Feature Flags Dict
        features = {
            "MMX": bool(edx1 & (1 << 23)),
            "SSE": bool(edx1 & (1 << 25)),
            "SSE2": bool(edx1 & (1 << 26)),
            "SSE3": bool(ecx1 & (1 << 0)),
            "SSSE3": bool(ecx1 & (1 << 9)),
            "SSE4.1": bool(ecx1 & (1 << 19)),
            "SSE4.2": bool(ecx1 & (1 << 20)),
            "SSE4A": bool(ecx81 & (1 << 6)),
            "AVX": bool(ecx1 & (1 << 28)),
            "AVX2": bool(ebx7 & (1 << 5)),
            "AVX-512F": bool(ebx7 & (1 << 16)),
            "AVX-512DQ": bool(ebx7 & (1 << 17)),
            "AVX-512PF": bool(ebx7 & (1 << 26)),
            "AVX-512ER": bool(ebx7 & (1 << 27)),
            "AVX-512CD": bool(ebx7 & (1 << 28)),
            "AVX-512BW": bool(ebx7 & (1 << 30)),
            "AVX-512VL": bool(ebx7 & (1 << 31)),
            "FMA3": bool(ecx1 & (1 << 12)),
            "FMA4": bool(ecx81 & (1 << 16)),
            "AES": bool(ecx1 & (1 << 25)),
            "SHA": bool(ebx7 & (1 << 29)),
            "CLMUL": bool(ecx1 & (1 << 1)),
            "BMI1": bool(ebx7 & (1 << 3)),
            "BMI2": bool(ebx7 & (1 << 8)),
            "POPCNT": bool(ecx1 & (1 << 23)),
            "LZCNT": bool(ecx81 & (1 << 5)),
            "VT-x / AMD-V": bool(ecx1 & (1 << 5)) or bool(ecx81 & (1 << 2)),
            "Hyper-Threading": bool(edx1 & (1 << 28)),
            "x64 (EM64T/AMD64)": bool(edx81 & (1 << 29)),
            "NX / XD (No-Execute)": bool(edx81 & (1 << 20)),
            "RDRAND": bool(ecx1 & (1 << 30)),
            "RDSEED": bool(ebx7 & (1 << 18)),
            "TSX / RTM": bool(ebx7 & (1 << 11)),
            "SMX": bool(ecx1 & (1 << 6)),
            "Enhanced SpeedStep": bool(ecx1 & (1 << 7)),
            "Turbo Boost": bool(cls.call(6, 0)[0] & (1 << 1))
        }

        # Cache calculation (Leaf 4 for Intel deterministic cache)
        caches = []
        if "Intel" in vendor:
            for sub_leaf in range(10):
                eax4, ebx4, ecx4, edx4 = cls.call(4, sub_leaf)
                cache_type = eax4 & 0x1F
                if cache_type == 0:
                    break
                level = (eax4 >> 5) & 0x7
                type_names = {1: "Data", 2: "Instruction", 3: "Unified"}
                t_name = type_names.get(cache_type, "Unified")
                ways = ((ebx4 >> 22) & 0x3FF) + 1
                partitions = ((ebx4 >> 12) & 0x3FF) + 1
                line_size = (ebx4 & 0xFFF) + 1
                sets = ecx4 + 1
                size_kb = (ways * partitions * line_size * sets) // 1024
                caches.append({
                    "level": f"L{level} {t_name}",
                    "size_kb": size_kb,
                    "ways": ways,
                    "line_size": line_size,
                    "sets": sets
                })
        elif "AMD" in vendor:
            # Leaf 0x80000005: L1, 0x80000006: L2 & L3
            eax85, ebx85, ecx85, edx85 = cls.call(0x80000005, 0)
            eax86, ebx86, ecx86, edx86 = cls.call(0x80000006, 0)
            l1d_kb = (ecx85 >> 24) & 0xFF
            l1i_kb = (edx85 >> 24) & 0xFF
            l2_kb = (ecx86 >> 16) & 0xFFFF
            l3_kb = ((edx86 >> 18) & 0x3FFF) * 512
            if l1d_kb:
                caches.append({"level": "L1 Data", "size_kb": l1d_kb, "ways": 8})
            if l1i_kb:
                caches.append({"level": "L1 Instruction", "size_kb": l1i_kb, "ways": 8})
            if l2_kb:
                caches.append({"level": "L2 Unified", "size_kb": l2_kb, "ways": 8})
            if l3_kb:
                caches.append({"level": "L3 Unified", "size_kb": l3_kb, "ways": 16})

        return {
            "vendor": vendor,
            "brand": brand,
            "signature": f"{display_family:02X}{display_model:02X}{stepping:01X}h",
            "family": display_family,
            "model": display_model,
            "stepping": stepping,
            "type": proc_type,
            "max_cpuid_level": max_leaf,
            "logical_cores": logical_cores,
            "apic_id": apic_id,
            "features": features,
            "caches": caches
        }

if __name__ == "__main__":
    info = CPUID.get_info()
    print("Vendor:", info.get("vendor"))
    print("Brand:", info.get("brand"))
    print("Signature:", info.get("signature"))
    print("Features count:", len(info.get("features", {})))
    supported = [k for k, v in info.get("features", {}).items() if v]
    print("Supported features:", ", ".join(supported))
    for c in info.get("caches", []):
        print(f"Cache {c['level']}: {c['size_kb']} KB")
