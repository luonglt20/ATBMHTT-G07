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
            "has_high_entropy_va": False,
            "has_force_integrity": False,
            "is_reloc_stripped": False,
            "is_signed": False,
            "has_overlay": False,
            "pdb_path": None,
            "suspicious_time": False,
            "spoofed_metadata": None,
            "missing_rich_header": False
        }
        
        try:
            pe = pefile.PE(self.filepath)
            dll_char = pe.OPTIONAL_HEADER.DllCharacteristics
            
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE']: results['has_aslr'] = True
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_NX_COMPAT']: results['has_dep'] = True
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_GUARD_CF']: results['has_cfg'] = True
            if dll_char & 0x0020: results['has_cet'] = True # IMAGE_DLLCHARACTERISTICS_CET_COMPAT / HIGH_ENTROPY_VA in newer definitions
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_NO_SEH'] == 0: results['has_seh'] = True
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_HIGH_ENTROPY_VA']: results['has_high_entropy_va'] = True
            if dll_char & pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_FORCE_INTEGRITY']: results['has_force_integrity'] = True

            file_char = pe.FILE_HEADER.Characteristics
            if file_char & pefile.IMAGE_CHARACTERISTICS['IMAGE_FILE_RELOCS_STRIPPED']: results['is_reloc_stripped'] = True

            # Tầng 2: Authenticode
            if pe.OPTIONAL_HEADER.DATA_DIRECTORY[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_SECURITY']].VirtualAddress != 0:
                results['is_signed'] = True

            # Overlay Detection
            overlay_offset = pe.get_overlay_data_start_offset()
            if overlay_offset is not None and overlay_offset < os.path.getsize(self.filepath):
                results['has_overlay'] = True

            # TÍNH NĂNG NÂNG CẤP: Phân tích PDB (Tầng 2) & Compilation Time Anomaly
            import datetime
            compile_time = pe.FILE_HEADER.TimeDateStamp
            try:
                dt = datetime.datetime.fromtimestamp(compile_time)
                # Báo động nếu compile time trước 2000 hoặc là tương lai
                if dt.year < 2000 or dt.year > datetime.datetime.now().year + 1:
                    results['suspicious_time'] = True
            except:
                results['suspicious_time'] = True

            if hasattr(pe, 'DIRECTORY_ENTRY_DEBUG'):
                for debug in pe.DIRECTORY_ENTRY_DEBUG:
                    if hasattr(debug.entry, 'PdbFileName'):
                        pdb = debug.entry.PdbFileName.strip(b'\x00').decode('utf-8', errors='ignore')
                        results['pdb_path'] = pdb
                        break

            # TÍNH NĂNG NÂNG CẤP: Phân tích mạo danh siêu dữ liệu (Metadata Spoofing)
            if hasattr(pe, 'FileInfo'):
                for fileinfo in pe.FileInfo:
                    for entry in fileinfo:
                        if hasattr(entry, 'StringTable'):
                            for table in entry.StringTable:
                                for key, value in table.entries.items():
                                    if key == b'OriginalFilename':
                                        orig_val = value.decode('utf-8', errors='ignore').lower()
                                        windows_bins = ['svchost.exe', 'lsass.exe', 'explorer.exe', 'cmd.exe', 'powershell.exe']
                                        if orig_val in windows_bins and not results['is_signed']:
                                            results['spoofed_metadata'] = orig_val

            # TÍNH NĂNG NÂNG CẤP: Thiếu Rich Header (Dấu hiệu payload sinh ra tự động từ các C2 framework)
            import codecs
            try:
                rich_header = pe.parse_rich_header()
                if not rich_header:
                    results['missing_rich_header'] = True
            except:
                results['missing_rich_header'] = True

            self._evaluate(results)
            
        except Exception as e:
            print(f"  [!] Error: {e}")

        return self.findings

    def _evaluate(self, results):
        # Layer 1 Findings
        if not results['has_aslr']:
            self.findings.append({"id": "APS-VEC-001", "name": "Missing ASLR", "severity": "CRITICAL", "description": "Address Space Layout Randomization bị tắt. Dễ bị tấn công ROP."})
        elif results['is_reloc_stripped']:
            self.findings.append({"id": "APS-VEC-001", "name": "ASLR Bypass (Reloc Stripped)", "severity": "CRITICAL", "description": "ASLR được bật trên danh nghĩa nhưng file bị gỡ bỏ bảng Relocation (.reloc). ASLR sẽ bị vô hiệu hóa."})

        if not results['has_dep']:
            self.findings.append({"id": "APS-VEC-002", "name": "Missing DEP/NX", "severity": "CRITICAL", "description": "Data Execution Prevention bị tắt. Cho phép thực thi code trong vùng nhớ dữ liệu."})
        if not results['has_cfg']:
            self.findings.append({"id": "APS-VEC-004", "name": "Missing CFG", "severity": "MEDIUM", "description": "Control Flow Guard không được kích hoạt để bảo vệ các lần gọi hàm gián tiếp."})
        if not results['has_cet']:
            # Tính năng mới nhất của Windows (Control-flow Enforcement Technology)
            self.findings.append({"id": "APS-VEC-003", "name": "Missing Intel CET (Shadow Stack)", "severity": "LOW", "description": "Hardware-enforced Stack Protection (CET) không được kích hoạt."})
        
        # Extended T1 protections
        if not results['has_high_entropy_va']:
            self.findings.append({"id": "APS-VEC-005", "name": "Missing High Entropy VA", "severity": "LOW", "description": "Không hỗ trợ High Entropy Virtual Address (ASLR 64-bit yếu hơn)."})
        if not results['has_force_integrity']:
            self.findings.append({"id": "APS-VEC-006", "name": "Missing Force Integrity", "severity": "LOW", "description": "Hệ điều hành sẽ không kiểm tra toàn vẹn bộ nhớ (Code Integrity) khi nạp file này."})

        # Layer 2 Findings (Metadata & Authenticode)
        if not results['is_signed']:
            self.findings.append({"id": "APS-VEC-011", "name": "Unsigned Binary", "severity": "HIGH", "description": "Binary không có chữ ký số Authenticode. Dễ bị giả mạo hoặc thay thế."})
        
        if results['pdb_path']:
            self.findings.append({"id": "APS-VEC-012", "name": "PDB Path Leaked", "severity": "LOW", "description": f"Phát hiện đường dẫn debug: {results['pdb_path']}. Cung cấp thông tin về cấu trúc máy chủ hoặc username."})

        if results['suspicious_time']:
            self.findings.append({"id": "APS-VEC-014", "name": "TimeDateStamp Anomaly", "severity": "MEDIUM", "description": "Thời gian biên dịch (TimeDateStamp) của PE Header là bất khả thi (Rất cũ hoặc ở tương lai). Dấu hiệu của việc giả mạo TimeStomping."})

        if results['spoofed_metadata']:
            self.findings.append({"id": "APS-VEC-015", "name": "Metadata Identity Spoofing", "severity": "HIGH", "description": f"Ứng dụng mạo danh tiến trình hệ điều hành trọng yếu ({results['spoofed_metadata']}) trong dữ liệu mô tả (OriginalFilename) nhưng KHÔNG có chữ ký điện tử hợp lệ (Không phải của Microsoft)."})
            
        if results['missing_rich_header']:
            self.findings.append({"id": "APS-VEC-016", "name": "Missing Rich Header", "severity": "MEDIUM", "description": "File thực thi bị thiếu Rich Header. Đây là đặc trưng kinh điển của các Payload được sinh ra từ mã nguồn mở (như MSFvenom) hoặc do hacker cố tình gỡ bỏ để tránh bị lấy dấu vết Hash (RichHash)."})

        # Extra: Overlay (Tầng 5: STT 44)
        if results['has_overlay']:
            self.findings.append({"id": "APS-VEC-044", "name": "Binary Overlay Detected", "severity": "MEDIUM", "description": "Phát hiện dữ liệu dư thừa tại cuối file (Overlay). Có thể chứa shellcode hoặc config ẩn."})
