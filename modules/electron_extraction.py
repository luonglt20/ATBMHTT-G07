import re
from colorama import Fore, Style
import os

class ElectronExtractionScanner:
    """
    Nhận diện ứng dụng xây dựng trên nền tảng Web/Electron.
    Nếu tìm thấy, đánh dấu cảnh báo cao về Asar Code Extraction & Web Vulnerabilities.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []

    def scan(self):
        print(f"{Fore.CYAN}  [-] Quét Electron Framework / WebView Detection...{Style.RESET_ALL}")
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read()

            ascii_strings = "".join([chr(b) if 32 <= b < 127 else '\n' for b in content])
            
            # Kiểm tra dấu hiệu Electron
            is_electron = "Electron" in ascii_strings or "app.asar" in ascii_strings or "nodeIntegration" in ascii_strings
            
            if is_electron:
                print(f"  {Fore.RED}[HIGH] Phát hiện Kiến trúc Electron (Chromium Embedded)!{Style.RESET_ALL}")
                self.findings.append({
                    "id": "WEB-ELEC-001",
                    "name": "Electron/Chromium Based Application",
                    "severity": "HIGH",
                    "details": "Tìm thấy dấu hiệu biên dịch bằng Electron. Ứng dụng có thể bị nhắm mục tiêu bằng lỗ hổng XSS (NodeIntegration Bypass) hoặc dễ dàng bị trích xuất toàn bộ mã nguồn qua file `app.asar` bằng lệnh `npx asar extract`."
                })
            else:
                print(f"  {Fore.GREEN}[OK] Không phải ứng dụng Web-Embedded (Electron).{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}  [!] Lỗi quét Electron: {str(e)}{Style.RESET_ALL}")
            
        return self.findings
