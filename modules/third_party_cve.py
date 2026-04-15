import re
from colorama import Fore, Style

class ThirdPartyCVEScanner:
    """
    Quét raw binary strings để tìm kiếm dấu hiệu của các thư viện mã nguồn mở 
    được embed cứng (statically linked) như zlib, openSSL, libcurl.
    Nếu tìm thấy phiên bản quá cũ, nguy cơ dính các CVE n_day.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        
        # Một số pattern chữ ký phiên bản phổ biến
        self.patterns = {
            "OpenSSL": r"OpenSSL\s+(1\.[01]\.[0-9a-z]+)",
            "zlib": r"zlib\s+(1\.[2-9]\.[0-9]+)",
            "libcurl": r"libcurl/([78]\.[0-9]+\.[0-9]+)",
            "Apache Log4j": r"log4j-api-([12]\.[0-9]+\.[0-9]+)"
        }

    def scan(self):
        print(f"{Fore.CYAN}  [-] Quét Third-party Dependencies Static Versioning...{Style.RESET_ALL}")
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read()
                
            # Đọc ASCII strings
            ascii_strings = "".join([chr(b) if 32 <= b < 127 else '\n' for b in content])
            
            for lib_name, pattern in self.patterns.items():
                matches = re.findall(pattern, ascii_strings)
                if matches:
                    unique_versions = set(matches)
                    version_str = ", ".join(unique_versions)
                    print(f"  {Fore.YELLOW}[INFO] Phát hiện Embedded Library: {lib_name} (Versions: {version_str}){Style.RESET_ALL}")
                    self.findings.append({
                        "id": "LIB-CVE-001",
                        "name": f"Embedded Library found: {lib_name}",
                        "severity": "INFO", # Blackbox tĩnh chỉ report Version, cần con người/API check CVE DB
                        "details": f"Ứng dụng pack kèm thư viện mã nguồn mở '{lib_name}' phiên bản [{version_str}]. Pentester cần đối chiếu với NVD/CVE Database để tìm Vulnerabilities."
                    })
                    
            if not self.findings:
                print(f"  {Fore.GREEN}[OK] Không phát hiện string phiên bản thư viện mã nguồn mở đáng ngờ.{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}  [!] Lỗi quét Library: {str(e)}{Style.RESET_ALL}")
            
        return self.findings
