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
        if not self.pe:
            return []
            
        print(f"\n{Fore.BLUE}[+] TẦNG 3: OBFUSCATION & HYPERVISOR DEBUGGING (Vector 19){Style.RESET_ALL}")
        results = {
            "is_packed": False,
            "packers_found": [],
            "high_entropy_sections": [],
            "tls_callbacks": False,
            "ep_anomaly": False
        }

        # TÍNH NĂNG NÂNG CẤP X: Nhận diện TLS Callbacks
        if hasattr(self.pe, 'DIRECTORY_ENTRY_TLS'):
            if self.pe.DIRECTORY_ENTRY_TLS and self.pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks:
                results["tls_callbacks"] = True

        # TÍNH NĂNG NÂNG CẤP Y: Nhận diện EntryPoint xảo trá
        ep = self.pe.OPTIONAL_HEADER.AddressOfEntryPoint
        ep_section = self.pe.get_section_by_rva(ep)
        if ep_section:
            # Entry point không nằm trong phân vùng có quyền Thực thi
            if not (ep_section.Characteristics & 0x20000000) and (ep_section.Characteristics & 0x80000000):
                results["ep_anomaly"] = True

        for section in self.pe.sections:
            sec_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
            
            # 1. Kiểm tra Section Name
            if sec_name in self.KNOWN_PACKERS:
                results["is_packed"] = True
                results["packers_found"].append(self.KNOWN_PACKERS[sec_name])

            # 2. Tính toán Entropy (Độ hỗn loạn dữ liệu)
            raw_data = section.get_data()
            entropy = self._calculate_entropy(raw_data)
            if entropy > 7.0:
                results["is_packed"] = True
                results["high_entropy_sections"].append((sec_name, entropy))

            # ---------------------------------------------------------
            # TÍNH NĂNG NÂNG CẤP 1: Section Size Anomaly (Virtual > Raw * 3)
            # ---------------------------------------------------------
            vsize = section.Misc_VirtualSize
            rsize = section.SizeOfRawData
            if rsize > 0 and vsize > rsize * 3 and '.bss' not in sec_name.lower():
                results["is_packed"] = True
                if "anomalies" not in results: results["anomalies"] = []
                results["anomalies"].append(sec_name)

            # ---------------------------------------------------------
            # TÍNH NĂNG NÂNG CẤP 2: Opcode Scanning (Heuristic Anti-Debug/VM)
            # ---------------------------------------------------------
            if section.Characteristics & 0x20000000: # IMAGE_SCN_MEM_EXECUTE
                if b'\x0F\x31' in raw_data: # rdtsc
                    if "opcode_hits" not in results: results["opcode_hits"] = []
                    results["opcode_hits"].append("RDTSC (Thời gian thực / Anti-VM)")
                if b'\x9C\x58' in raw_data: # pushfd; pop eax
                    if "opcode_hits" not in results: results["opcode_hits"] = []
                    results["opcode_hits"].append("PUSHFD (Kiểm tra Trap Flag / Anti-Debug)")
                
                # Quét xem có nhồi INT 3 rải rác không (Software Breakpoint Evasion)
                if raw_data.count(b'\xCC') > 100 and entropy < 6.0:
                    if "opcode_hits" not in results: results["opcode_hits"] = []
                    results["opcode_hits"].append("INT 3 Padding Anomaly (Anti-Analysis)")

        findings = []
        if results["is_packed"]:
            packers_list = sorted(list(set(results["packers_found"])))
            packers_str = ", ".join(packers_list) if packers_list else "Unknown/Custom Packer"
            
            print(f" {Fore.RED}[!] BÁO ĐỘNG ĐỎ: Ứng dụng có dấu hiệu bị bọc vỏ (Packed/Obfuscated).{Style.RESET_ALL}")
            
            findings.append({
                "id": "APS-VEC-052",
                "name": "Packer/Obfuscator Detected",
                "severity": "CRITICAL",
                "details": f"Ứng dụng đã bị bọc vỏ bởi: {packers_str}. User-mode debugging sẽ bị chặn."
            })
            
            for name, ent in results["high_entropy_sections"]:
                findings.append({
                    "id": "APS-VEC-051",
                    "name": f"High Entropy Section: {name}",
                    "severity": "HIGH",
                    "details": f"Section '{name}' có entropy {ent:.2f}. Có thể chứa mã độc hoặc payload bị mã hóa."
                })
                
            if "anomalies" in results and results["anomalies"]:
                findings.append({
                    "id": "APS-VEC-053",
                    "name": "Section Size Anomaly",
                    "severity": "HIGH",
                    "details": f"Section {results['anomalies']} có VirtualSize lớn bất thường (gấp 3 lần RawData). Dấu hiệu của kỹ thuật giải nén bộ nhớ (Unpacking Stub)."
                })
                
        if "opcode_hits" in results and results["opcode_hits"]:
            hits = list(set(results["opcode_hits"]))
            print(f" {Fore.RED}[!] OPCODE HEURISTIC: Tìm thấy chữ ký Anti-Analysis mức thấp!{Style.RESET_ALL}")
            findings.append({
                "id": "APS-VEC-022",
                "name": "Anti-Debug/Anti-VM Opcodes",
                "severity": "CRITICAL",
                "details": f"Phát hiện các tập lệnh hướng CPU nhạy cảm: {', '.join(hits)}."
            })
            
        if results["tls_callbacks"]:
            print(f" {Fore.RED}[CRITICAL] Phát hiện TLS Callbacks! Tính năng thường bị lợi dụng để chống Debugger.{Style.RESET_ALL}")
            findings.append({
                "id": "APS-VEC-054",
                "name": "TLS Callbacks Anti-Analysis",
                "severity": "CRITICAL",
                "details": "Chương trình sử dụng Thread Local Storage (TLS) Callbacks. Mã độc dùng tính năng này để thực thi Anti-Debug TRƯỚC KHI trình gỡ lỗi kịp nhảy vào Entry Point (OEP)."
            })
            
        if results["ep_anomaly"]:
            print(f" {Fore.RED}[CRITICAL] AddressOfEntryPoint cực kỳ bất thường (Nằm ngoài vùng nhớ thực thi).{Style.RESET_ALL}")
            findings.append({
                "id": "APS-VEC-055",
                "name": "Abnormal Entry Point",
                "severity": "CRITICAL",
                "details": "EntryPoint của PE file trỏ vào một Section không có cờ Thực thi (Execute) nhưng lại có quyền Ghi (Write). Gần như chắc chắn có kỹ thuật tự giải mã (Self-Decrypting) ở đây."
            })

        if not results["is_packed"] and not results.get("opcode_hits") and not results["tls_callbacks"] and not results["ep_anomaly"]:
            print(f" {Fore.GREEN}[OK] File không bị bọc bởi các Packer phổ biến và không có opcode bất thường.{Style.RESET_ALL}")

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
