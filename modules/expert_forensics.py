import pefile
import re
from colorama import Fore, Style

class ExpertForensicScanner:
    """
    Module phân tích kỹ thuật cao cấp (Expert Level):
    - Vector 17: PE Carving (Tìm PE ẩn trong bộ nhớ/overlay)
    - Vector 25: SMC (Self-Modifying Code) - Phân tích đặc quyền Section
    - Vector 39: Anti-Debugging Trick Detection
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        try:
            self.pe = pefile.PE(filepath)
        except:
            self.pe = None

    def scan(self):
        print(f"{Fore.CYAN}  [-] Khởi động Module Pháp y Chuyên gia (Expert Forensics)...{Style.RESET_ALL}")
        if not self.pe:
            return []

        self._check_smc_sections()
        self._carve_overlay_for_pe()
        self._detect_anti_debug_tricks()

        return self.findings

    def _check_smc_sections(self):
        """Vector 25: Tìm các Section có cả quyền thực thi (Execute) và quyền ghi (Write)."""
        for section in self.pe.sections:
            # IMAGE_SCN_MEM_WRITE (0x80000000) và IMAGE_SCN_MEM_EXECUTE (0x20000000)
            if (section.Characteristics & 0x80000000) and (section.Characteristics & 0x20000000):
                sec_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
                print(f"  {Fore.RED}[CRITICAL] Phát hiện dấu vết SMC (Self-Modifying Code) tại Section '{sec_name}'{Style.RESET_ALL}")
                self.findings.append({
                    "id": "EXP-SMC-025",
                    "name": "Self-Modifying Code Marker",
                    "severity": "CRITICAL",
                    "details": f"Section '{sec_name}' có cả quyền WRITE và EXECUTE. Đây là dấu hiệu của Malware hoặc kỹ thuật Obfuscation cực kỳ tinh vi."
                })

    def _carve_overlay_for_pe(self):
        """Vector 17: Tìm kiếm chữ ký PE ('MZ') ẩn bên trong phần Overlay."""
        overlay_offset = self.pe.get_overlay_data_start_offset()
        if overlay_offset:
            with open(self.filepath, 'rb') as f:
                f.seek(overlay_offset)
                overlay_data = f.read()
            
            # Tìm chữ ký 'MZ'
            # (Phải cẩn thận tránh Positive giả, nhưng đây là heuristics)
            if b'MZ' in overlay_data:
                print(f"  {Fore.YELLOW}[HIGH] Phát hiện chữ ký Portable Executable ẩn trong Overlay!{Style.RESET_ALL}")
                self.findings.append({
                    "id": "EXP-PE-017",
                    "name": "Hidden PE in Overlay (Carving)",
                    "severity": "HIGH",
                    "details": "Tìm thấy chữ ký 'MZ' trong phần dữ liệu đính kèm (Overlay). Có khả năng ứng dụng tự giải nén và thực thi một Payload PE khác từ bên trong."
                })

    def _detect_anti_debug_tricks(self):
        """Vector 39: Tìm kiếm các hàm API dùng để chống Debugger."""
        anti_debug_apis = [
            b"IsDebuggerPresent", b"CheckRemoteDebuggerPresent", 
            b"NtQueryInformationProcess", b"OutputDebugString"
        ]
        
        found_apis = []
        if hasattr(self.pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name in anti_debug_apis:
                        found_apis.append(imp.name.decode())

        if found_apis:
            print(f"  {Fore.YELLOW}[MEDIUM] Phát hiện Anti-Debugging APIs: {found_apis}{Style.RESET_ALL}")
            self.findings.append({
                "id": "EXP-DBG-039",
                "name": "Anti-Debugging Tricks Detected",
                "severity": "MEDIUM",
                "details": f"Ứng dụng nhập khẩu các hàm nhạy cảm để phát hiện Debugger: {', '.join(found_apis)}. Yêu cầu dùng SCYLLA hoặc Stealth Debugger."
            })
