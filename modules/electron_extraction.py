import re
from colorama import Fore, Style
import os

class ElectronExtractionScanner:
    """
    Module rà quét ứng dụng Web-Embedded (Tầng 8):
    - APS-VEC-078: Electron / Chromium Framework Detection
    - APS-VEC-079: NodeIntegration & Local File Exposure risk
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []

    def scan(self):
        print(f"{Fore.CYAN}  [-] Quét Electron Framework & Chromium Artifacts Tier-3...{Style.RESET_ALL}")
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read()

            # Chuyển đổi sang strings để tìm pattern
            ascii_strings = "".join([chr(b) if 32 <= b < 127 else '\n' for b in content])
            
            self._detect_electron_core(ascii_strings)
            self._check_node_integration(ascii_strings)
            self._find_native_module_references(ascii_strings)

        except Exception as e:
            print(f"{Fore.RED}  [!] Lỗi quét Electron: {str(e)}{Style.RESET_ALL}")
            
        return self.findings

    def _detect_electron_core(self, strings):
        """APS-VEC-078: Nhận diện lõi Electron/Chromium."""
        if "Electron" in strings or "app.asar" in strings:
            print(f"  {Fore.RED}[HIGH] Phát hiện ứng dụng Electron (Chromium Embedded)!{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-078",
                "name": "Electron/Chromium Based Architecture",
                "severity": "HIGH",
                "details": "Ứng dụng được xây dựng trên Electron. Pentester có thể trích xuất mã nguồn JS/HTML qua tệp app.asar và tìm kiếm các lỗ hổng Web (XSS, Prototype Pollution) để thực thi RCE."
            })

    def _check_node_integration(self, strings):
        """APS-VEC-079: Kiểm tra cấu hình NodeIntegration nguy hiểm."""
        if "nodeIntegration:true" in strings.replace(" ", ""):
            print(f"  {Fore.RED}[CRITICAL] Phát hiện cấu hình nodeIntegration: true!{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-079",
                "name": "Unsafe NodeIntegration Configuration",
                "severity": "CRITICAL",
                "details": "Ứng dụng cấp quyền cho Javascript trong Renderer truy cập thẳng vào hệ thống (Node.js API). Một lỗ hổng XSS đơn giản sẽ ngay lập tức biến thành Full RCE."
            })

    def _find_native_module_references(self, strings):
        """Phát hiện việc gọi các module native (.node)."""
        if ".node" in strings:
            print(f"  {Fore.YELLOW}[MEDIUM] Phát hiện tham chiếu đến Native Node Modules (.node){Style.RESET_ALL}")
            # Có thể bổ sung thêm logic tìm file thực tế nếu cần
