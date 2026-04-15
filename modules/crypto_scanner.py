import re
from colorama import Fore, Style
import string

class CryptoScanner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        # Danh sách YARA / Regex mẫu tìm kiếm Secrets Mức cao
        self.signatures = {
            "AWS Access Key": r"(?i)AKIA[0-9A-Z]{16}",
            "Google API": r"AIza[0-9A-Za-z-_]{35}",
            "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----",
            "Hardcoded Password": r"(?i)(password|passwd|pwd|secret)\s*=\s*['\"]([^'\"]+)['\"]",
            "Insecure Hash (MD5)": r"(?i)(md5_hash|md5sum)",
        }

    def scan(self):
        print(f"{Fore.CYAN}  [-] Quét Hardcoded Secrets & Crypto Indicators...{Style.RESET_ALL}")
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read()

            # Lọc string ASCII cơ bản (Mô phỏng Strings command)
            ascii_strings = "".join([chr(b) if 32 <= b < 127 else '\n' for b in content])
            
            for name, pattern in self.signatures.items():
                matches = set(re.findall(pattern, ascii_strings))
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[1] # For password regex group
                    
                    # Chỉ báo lỗi nếu match dài hơn 3 ký tự (chống false positive)
                    if len(match) > 3:
                        print(f"  {Fore.RED}[HIGH] {name} bị rò rỉ: {match[:10]}...{Style.RESET_ALL}")
                        self.findings.append({
                            "id": "SEC-HARDCODED",
                            "name": f"Found {name}",
                            "severity": "HIGH",
                            "details": f"Tiết lộ chuỗi nhạy cảm. Trích xuất: '{match}'"
                        })
                        
            if not self.findings:
                print(f"  {Fore.GREEN}[OK] Không tìm thấy khóa nhạy cảm / Secrets.{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}  [!] Error quét Crypto: {str(e)}{Style.RESET_ALL}")

        return self.findings
