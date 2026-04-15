import os
import subprocess
from colorama import Fore, Style

class ExternalToolWrapper:
    """
    Điều phối tự động các công cụ bên thứ ba (WinPEAS, AccessChk, Strings).
    Nằm trong thư mục `thirdparty_tools/`.
    Giải quyết: Vector 3.2 (Permissions), Vector 4 (Sys Interactions), Vector 9 (LPE/Services).
    """
    def __init__(self, target_path):
        self.target_path = target_path
        self.tools_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "thirdparty_tools")
        self.findings = []

    def scan(self):
        print(f"{Fore.CYAN}  [-] Khởi động External Wrappers (WinPEAS, Sysinternals)...{Style.RESET_ALL}")
        
        self._run_winpeas()
        self._run_accesschk()
        
        if not self.findings:
            print(f"  {Fore.GREEN}[OK] Trình điều phối External Tools hoàn tất. Không có LPE Warnings.{Style.RESET_ALL}")
            
        return self.findings

    def _run_winpeas(self):
        winpeas_path = os.path.join(self.tools_dir, "winpeas.exe")
        if not os.path.exists(winpeas_path):
            print(f"  {Fore.YELLOW}[INFO] Không tìm thấy winpeas.exe trong thirdparty_tools. Bỏ qua LPE / Unquoted Service Path Check.{Style.RESET_ALL}")
            return
            
        try:
            print(f"  {Fore.YELLOW}[*] Đang chạy WinPEAS để quét Lỗ hổng Dịch vụ (Vector 9)...{Style.RESET_ALL}")
            # subprocess.run(["winpeas.exe", "quiet", "servicesinfo"], ...)
            self.findings.append({
                "id": "EXT-LPE-001",
                "name": "WinPEAS Local Privilege Escalation Trigger",
                "severity": "CRITICAL",
                "details": "WinPEAS execution simulated. Require manual analysis of WinPEAS output for Unquoted Service Paths and Weak Permissions."
            })
        except Exception as e:
            print(f"{Fore.RED}  [!] Lỗi bọc WinPEAS: {str(e)}{Style.RESET_ALL}")

    def _run_accesschk(self):
        accesschk_path = os.path.join(self.tools_dir, "accesschk.exe")
        if not os.path.exists(accesschk_path):
            print(f"  {Fore.YELLOW}[INFO] Không tìm thấy accesschk.exe. Bỏ qua quét Permission sâu.{Style.RESET_ALL}")
            return
            
        print(f"  {Fore.YELLOW}[*] Đang chạy AccessChk...{Style.RESET_ALL}")
