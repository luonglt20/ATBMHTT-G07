import pefile
import math
from colorama import Fore, Style

class ExpertForensicScanner:
    """
    Module phân tích pháp y chuyên sâu (Tầng 4 & 6):
    - APS-VEC-025: SMC (Self-Modifying Code)
    - APS-VEC-044: Resource/Overlay PE Carving
    - APS-VEC-051: High Entropy Section detection
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        try:
            self.pe = pefile.PE(filepath)
        except:
            self.pe = None

    def scan(self):
        print(f"{Fore.CYAN}  [-] Khởi động Module Expert Forensics Tier-3...{Style.RESET_ALL}")
        if not self.pe:
            return []

        self._check_smc_sections()
        self._calculate_section_entropy()
        self._carve_overlay_for_pe()

        return self.findings

    def _calculate_entropy(self, data):
        """Tính toán Shanon Entropy của một khối dữ liệu."""
        if not data: return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def _calculate_section_entropy(self):
        """APS-VEC-051: Phát hiện các Section có entropy cao (Dấu hiệu nén/mã hóa)."""
        for section in self.pe.sections:
            entropy = self._calculate_entropy(section.get_data())
            sec_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
            if entropy > 7.2: # Ngưỡng thường thấy của mã hóa/nén
                print(f"  {Fore.RED}[CRITICAL] Section '{sec_name}' có Entropy cực cao: {entropy:.2f}{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-051",
                    "name": "High Entropy Section (Packed/Encrypted)",
                    "severity": "CRITICAL",
                    "details": f"Section '{sec_name}' có mức entropy {entropy:.2f}, vượt ngưỡng an toàn. Đây là dấu hiệu chắc chắn của mã máy đã bị xáo trộn hoặc nén lại để vượt mặt AV."
                })

    def _check_smc_sections(self):
        """APS-VEC-025: Tìm các Section có cả quyền thực thi (Execute) và quyền ghi (Write)."""
        for section in self.pe.sections:
            if (section.Characteristics & 0x80000000) and (section.Characteristics & 0x20000000):
                sec_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
                print(f"  {Fore.RED}[CRITICAL] Phát hiện dấu vết SMC tại Section '{sec_name}'{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-025",
                    "name": "Self-Modifying Code (SMC) Marker",
                    "severity": "CRITICAL",
                    "details": f"Section '{sec_name}' có cả đặc quyền WRITE và EXECUTE. Kẻ tấn công có thể thay đổi mã máy ngay khi đang chạy để ẩn giấu hành vi thật."
                })

    def _carve_overlay_for_pe(self):
        """APS-VEC-044: Tìm kiếm PE ẩn trong phần Overlay."""
        overlay_offset = self.pe.get_overlay_data_start_offset()
        if overlay_offset:
            with open(self.filepath, 'rb') as f:
                f.seek(overlay_offset)
                overlay_data = f.read()
            
            if b'MZ' in overlay_data and b'PE' in overlay_data:
                print(f"  {Fore.YELLOW}[HIGH] Phát hiện chữ ký Portable Executable ẩn trong Overlay!{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-044",
                    "name": "Hidden PE in Overlay (Carving)",
                    "severity": "HIGH",
                    "details": "Tìm thấy chữ ký của một file thực thi khác nằm sau điểm kết thúc chuẩn của file gốc. Malicious dropper thường dùng kỹ thuật này để giấu payload."
                })
