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
                    
                    
                    # TÍNH NĂNG NÂNG CẤP: HEURISTIC ENTROPY LỌC FALSE POSITIVE
                    # Chỉ báo lỗi nếu chuỗi dài hơn 10 ký tự HOẶC có entropy cao (đối với secret key thực sự)
                    if len(match) > 10:
                        entropy = self._shannon_entropy(match)
                        if entropy > 4.2 or name != "Hardcoded Password":
                            print(f"  {Fore.RED}[HIGH] {name} bị rò rỉ (Entropy: {entropy:.2f}): {match[:10]}...{Style.RESET_ALL}")
                            self.findings.append({
                                "id": "APS-VEC-079",
                                "name": f"Found {name}",
                                "severity": "HIGH",
                                "details": f"Tiết lộ chuỗi nhạy cảm (Entropy: {entropy:.2f}). Trích xuất: '{match}'"
                            })
                        
            # TÍNH NĂNG NÂNG CẤP 2: Bắt Token ngẫu nhiên (JWT/Bearer/Base64) ẩn danh bằng Entropy Scanning
            import re as stdre
            # Tìm mảng các ký tự base64 liên tục dài hơn 40 ký tự (Token)
            base64_regex = r"(?:[A-Za-z0-9+/]{40,}=*)"
            b64_matches = set(stdre.findall(base64_regex, ascii_strings))
            for b64 in b64_matches:
                if self._shannon_entropy(b64) > 4.7: # High entropy JWT/Crypto key
                    print(f"  {Fore.RED}[CRITICAL] Phát hiện chuỗi High Entropy (Có thể là Token/JWT ẩn): {b64[:10]}...{Style.RESET_ALL}")
                    self.findings.append({
                        "id": "APS-VEC-079",
                        "name": "High Entropy String (Potential Key/Token)",
                        "severity": "CRITICAL",
                        "details": f"Phát hiện chuỗi Base64 dài với mức độ ngẫu nhiên rất cao (Entropy {self._shannon_entropy(b64):.2f})."
                    })

            # TÍNH NĂNG NÂNG CẤP 3: Quét Hằng số mã hóa (Ransomware / Custom Crypto C2 Indicator)
            # Malware (Ransomware/C2) thường tự code thuật toán mã hóa, dẫn đến lộ các hằng số vòng (Magic Constants)
            crypto_constants = {
                "MD5 Initialization Matrix": b"\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10",
                "SHA-256 Constant Dword 1": b"\x98\x2f\x8a\x42", # 0x428a2f98 in Little Endian
                "SHA-256 Constant Dword 2": b"\x91\x44\x37\x71", # 0x71374491
                "ChaCha20 / Salsa20 Sigma": b"expand 32-byte k"
            }
            
            for alg_name, const_bytes in crypto_constants.items():
                if const_bytes in content:
                    print(f"  {Fore.RED}[CRITICAL] Phát hiện Thuật toán mã hóa nhúng cứng: {alg_name}. Dấu hiệu của Ransomware!{Style.RESET_ALL}")
                    self.findings.append({
                        "id": "APS-VEC-080",
                        "name": f"Embedded Crypto Algorithm ({alg_name})",
                        "severity": "CRITICAL",
                        "details": f"File thực thi nhúng cứng hằng số/từ khóa của thuật toán {alg_name}. Đa phần các phần mềm hợp lệ sẽ dùng API của Windows (BCrypt) thay vì tự compile."
                    })

            if not self.findings:
                print(f"  {Fore.GREEN}[OK] Không tìm thấy khóa nhạy cảm hay JWT/Token rò rỉ.{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}  [!] Error quét Crypto: {str(e)}{Style.RESET_ALL}")

        return self.findings

    def _shannon_entropy(self, data):
        """Tính toán độ hỗn loạn dữ liệu (Entropy) của một chuỗi."""
        import math
        if not data:
            return 0
        entropy = 0
        for x in set(data):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy
