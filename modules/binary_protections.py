import os
import pefile
import math
from colorama import Fore, Style

class BinaryProtectionScanner:
    """
    Tầng 1: Binary Mitigations (ASLR, DEP, CET, CFG, SEH).
    Tầng 2: Code Signing & Authenticode.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        
    def scan(self):
        print(f"  {Fore.CYAN}[-]{Style.RESET_ALL} Quét Mitigations & Authenticode (Tầng 1-2)...")
        results = {
            "has_aslr": False,
            "has_dep": False,
            "has_cfg": False,
            "has_seh": False,
            "has_cet": False,
            "is_signed": False,
            "has_overlay": False
        }
        
        try:
            pe = pefile.PE(self.filepath)
            dll_char = pe.OPTIONAL_HEADER.DllCharacteristics
            
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE']: results['has_aslr'] = True
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_NX_COMPAT']: results['has_dep'] = True
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_GUARD_CF']: results['has_cfg'] = True
            if dll_char & 0x0020: results['has_cet'] = True # IMAGE_DLLCHARACTERISTICS_CET_COMPAT
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_NO_SEH'] == 0: results['has_seh'] = True

            # Tầng 2: Authenticode
            if pe.OPTIONAL_HEADER.DATA_DIRECTORY[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_SECURITY']].VirtualAddress != 0:
                results['is_signed'] = True

            # Overlay Detection
            overlay_offset = pe.get_overlay_data_start_offset()
            if overlay_offset is not None and overlay_offset < os.path.getsize(self.filepath):
                results['has_overlay'] = True

            self._evaluate(results)
            
        except Exception as e:
            print(f"  [!] Error: {e}")

        return self.findings

    def _evaluate(self, results):
        # Layer 1 Findings
        if not results['has_aslr']:
            self.findings.append({"id": "PE-VEC-T01-01", "name": "Missing ASLR", "severity": "CRITICAL", "description": "Address Space Layout Randomization bị tắt. Dễ bị tấn công ROP."})
        if not results['has_dep']:
            self.findings.append({"id": "PE-VEC-T01-02", "name": "Missing DEP/NX", "severity": "CRITICAL", "description": "Data Execution Prevention bị tắt. Cho phép thực thi code trong vùng nhớ dữ liệu."})
        if not results['has_cfg']:
            self.findings.append({"id": "PE-VEC-T01-03", "name": "Missing CFG", "severity": "MEDIUM", "description": "Control Flow Guard không được kích hoạt để bảo vệ các lần gọi hàm gián tiếp."})
        if not results['has_cet']:
            self.findings.append({"id": "PE-VEC-T01-04", "name": "Missing Intel CET", "severity": "MEDIUM", "description": "Hardware-enforced Stack Protection (CET) không được kích hoạt."})

        # Layer 2 Findings
        if not results['is_signed']:
            self.findings.append({"id": "PE-VEC-T02-01", "name": "Unsigned Binary", "severity": "HIGH", "description": "Binary không có chữ ký số Authenticode. Dễ bị giả mạo hoặc thay thế."})

        # Extra: Overlay (Tầng 3/6)
        if results['has_overlay']:
            self.findings.append({"id": "PE-VEC-T03-09", "name": "Binary Overlay Detected", "severity": "MEDIUM", "description": "Phát hiện dữ liệu dư thừa tại cuối file (Overlay). Có thể chứa shellcode hoặc config ẩn."})
