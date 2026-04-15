import math
from colorama import Fore, Style

import pefile

class PackerDetector:
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.pe = pefile.PE(file_path)
        except Exception:
            self.pe = None
        self.KNOWN_PACKERS = {
            ".vmp0": "VMProtect",
            ".vmp1": "VMProtect",
            ".themida": "Themida",
            ".enigma": "Enigma Protector",
            "UPX0": "UPX (Phổ thông)",
            "UPX1": "UPX (Phổ thông)",
            ".aspack": "ASPack",
            ".mpress1": "MPRESS"
        }

    def scan(self):
        print(f"\n{Fore.BLUE}[+] TẦNG 3: OBFUSCATION & HYPERVISOR DEBUGGING (Vector 19){Style.RESET_ALL}")
        results = {
            "is_packed": False,
            "packers_found": [],
            "high_entropy_sections": []
        }

        if not self.pe:
            return []

        for section in self.pe.sections:
            sec_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
            
            # 1. Kiểm tra Section Name
            if sec_name in self.KNOWN_PACKERS:
                results["is_packed"] = True
                results["packers_found"].append(self.KNOWN_PACKERS[sec_name])

            # 2. Tính toán Entropy (Độ hỗn loạn dữ liệu)
            entropy = self._calculate_entropy(section.get_data())
            if entropy > 7.0:
                results["is_packed"] = True
                results["high_entropy_sections"].append((sec_name, entropy))

        findings = []
        if results["is_packed"]:
            packers_list = sorted(list(set(results["packers_found"])))
            packers_str = ", ".join(packers_list) if packers_list else "Unknown/Custom Packer"
            
            print(f" {Fore.RED}[!] BÁO ĐỘNG ĐỎ: Ứng dụng có dấu hiệu bị bọc vỏ (Packed/Obfuscated).{Style.RESET_ALL}")
            
            findings.append({
                "id": "PE-PACKER",
                "name": "Packer/Obfuscator Detected",
                "severity": "CRITICAL",
                "details": f"Ứng dụng đã bị bọc vỏ bởi: {packers_str}. User-mode debugging sẽ bị chặn."
            })
            
            for name, ent in results["high_entropy_sections"]:
                findings.append({
                    "id": "PE-ENTROPY",
                    "name": f"High Entropy Section: {name}",
                    "severity": "HIGH",
                    "details": f"Section '{name}' có entropy {ent:.2f}. Có thể chứa mã độc hoặc payload bị mã hóa."
                })
        else:
            print(f" {Fore.GREEN}[OK] File không bị bọc bởi các Packer phổ biến và có Entropy thấp.{Style.RESET_ALL}")

        return findings

    def _calculate_entropy(self, data):
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy
