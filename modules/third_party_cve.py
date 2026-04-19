import re
from colorama import Fore, Style

class ThirdPartyCVEScanner:
    """
    Quét mã nguồn nhị phân tìm kiếm thư viện nhúng (Tầng 10):
    - APS-VEC-100: Embedded 3rd Party Vulnerabilities (CVE)
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        
        # Mở rộng bộ pattern nhận diện thư viện hiện đại
        self.patterns = {
            "OpenSSL": r"OpenSSL\s+(1\.[01]\.[0-9a-z]+|3\.[0-9]\.[0-9])",
            "zlib": r"zlib\s+(1\.[2-9]\.[0-9]+)",
            "libcurl": r"libcurl/([78]\.[0-9]+\.[0-9]+)",
            "SQLite": r"SQLite\s+([34]\.[0-9]+\.[0-9]+)",
            "Protobuf": r"google/protobuf/([23]\.[0-9]+\.[0-9]+)",
            "RapidJSON": r"rapidjson/([01]\.[0-9]+\.[0-9]+)"
        }

    def scan(self):
        print(f"{Fore.CYAN}  [-] Quét Third-party Dependencies Static Versioning Tier-3...{Style.RESET_ALL}")
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read()
                
            ascii_strings = "".join([chr(b) if 32 <= b < 127 else '\n' for b in content])
            
            for lib_name, pattern in self.patterns.items():
                matches = re.findall(pattern, ascii_strings)
                if matches:
                    unique_versions = set(matches)
                    version_str = ", ".join(unique_versions)
                    print(f"  {Fore.YELLOW}[HIGH] Phát hiện Thư viện nhúng: {lib_name} v{version_str}{Style.RESET_ALL}")
                    self.findings.append({
                        "id": "APS-VEC-100",
                        "name": f"Embedded Library CVE Risk: {lib_name}",
                        "severity": "HIGH",
                        "details": f"Ứng dụng chứa thư viện '{lib_name}' phiên bản {version_str} được biên dịch tĩnh. Các phiên bản này thường mang theo lỗ hổng N-Day đã biết. Cần kiểm tra mã CVE tương ứng trên NVD Database."
                    })
                    
        except Exception as e:
            print(f"{Fore.RED}  [!] Lỗi quét Library: {str(e)}{Style.RESET_ALL}")
            
        return self.findings
