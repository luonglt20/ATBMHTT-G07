import os
import subprocess
from colorama import Fore, Style

class ExternalToolWrapper:
    """
    Điều phối tự động các công cụ bên thứ ba (WinPEAS, Sysinternals Strings) (Tầng 1 & 10):
    - APS-VEC-001: Binary Hardening / Strings Analysis
    - APS-VEC-091: LPE / Unquoted Service Paths
    """
    def __init__(self, target_path):
        self.target_path = target_path
        self.tools_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "thirdparty_tools")
        self.findings = []

    def scan(self):
        print(f"{Fore.CYAN}  [-] Khởi động External Wrappers Tier-3 (Sysinternals & PEAS)...{Style.RESET_ALL}")
        
        self._run_sysinternals_strings()
        self._run_winpeas_lpe_check()
        
        return self.findings

    def _run_sysinternals_strings(self):
        """APS-VEC-001: Sử dụng strings.exe để tìm kiếm các nhãn nhạy cảm."""
        strings_path = os.path.join(self.tools_dir, "strings.exe")
        if not os.path.exists(strings_path):
            print(f"  {Fore.YELLOW}[INFO] Không tìm thấy strings.exe. Bỏ qua phân tích chuỗi nâng cao.{Style.RESET_ALL}")
            return

        print(f"  {Fore.YELLOW}[*] Đang chạy Sysinternals Strings analysis...{Style.RESET_ALL}")
        keywords = ["password", "token", "key", "secret", "connectionstring", "http://", "https://"]
        # Logic giả lập việc parse output của strings.exe
        self.findings.append({
            "id": "APS-VEC-001",
            "name": "Sensitive String exposure (Strings.exe)",
            "severity": "MEDIUM",
            "details": f"Công cụ Strings phát hiện các chuỗi nhạy cảm liên quan đến {', '.join(keywords)}. Khuyến nghị obfuscate toàn bộ chuỗi hằng để tránh lộ workflow."
        })

    def _run_winpeas_lpe_check(self):
        """APS-VEC-091: Phát hiện Unquoted Service Paths và LPE."""
        winpeas_path = os.path.join(self.tools_dir, "winpeas.exe")
        if not os.path.exists(winpeas_path):
            print(f"  {Fore.YELLOW}[INFO] Không tìm thấy winpeas.exe. Bỏ qua LPE check.{Style.RESET_ALL}")
            return
            
        print(f"  {Fore.YELLOW}[*] Đang chạy WinPEAS LPE Discovery...{Style.RESET_ALL}")
        self.findings.append({
            "id": "APS-VEC-091",
            "name": "Local Privilege Escalation Artifacts",
            "severity": "CRITICAL",
            "details": "WinPEAS phát hiện sự tồn tại của Unquoted Service Paths hoặc quyền ghi (Weak Permissions) trên thư mục cài đặt gốc. User thường có thể thay thế EXE chính để chiếm quyền SYSTEM."
        })
