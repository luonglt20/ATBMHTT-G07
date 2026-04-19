import os
try:
    import yara
except ImportError:
    yara = None

from colorama import Fore, Style

class YaraScanner:
    """
    Advanced Pattern Matching using YARA.
    Phát hiện các chữ ký mức thấp (Byte patterns) mà không cần phân tích logic rườm rà.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        self.rules = None

        if not yara:
            print(f"  {Fore.RED}[!] Thư viện 'yara-python' chưa được cài đặt. Bỏ qua YARA Scan!{Style.RESET_ALL}")
            return

        # Định nghĩa các tập luật nội tuyến để hệ thống gọn nhẹ, không cần file .yar ngoài.
        rules_text = """
        rule EDR_Evasion_API {
            meta:
                description = "Detects Direct Syscall or Runtime API hashing"
            strings:
                $halo1 = { 4C 8B D1 B8 ?? ?? ?? ?? F6 04 25 08 03 FE 7F 01 75 03 0F 05 C3 }
                $syscall = { 0f 05 c3 }
                $peb_walk = { 65 48 8b 04 25 60 00 00 00 48 8b 40 18 48 8b 78 20 }
            condition:
                any of them
        }
        
        rule Advanced_Crypto {
            meta:
                description = "Detects Advanced Cryptography parameters (AES S-Box, RSA consts)"
            strings:
                $aes_sbox = { 63 7C 77 7B F2 6B 6F C5 30 01 67 2B FE D7 AB 76 }
                $rsa_const = { 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 } // Tạm thay bằng stub
            condition:
                $aes_sbox
        }

        rule Process_Hollowing_Patterns {
            meta:
                description = "Common Process Injection/Hollowing Sequences"
            strings:
                $sus1 = "ZwUnmapViewOfSection" ascii wide
                $sus2 = "NtUnmapViewOfSection" ascii wide
                $sus3 = "CreateProcess" ascii wide fullword
            condition:
                1 of ($sus1, $sus2) and $sus3
        }
        
        rule Suspicious_Strings {
            meta:
                description = "Hardcoded indicators often seen in APTs"
            strings:
                $cmd = "cmd.exe" ascii wide nocase
                $powershell = "powershell" ascii wide nocase
                $wmi = "ROOT\\\\CIMV2" ascii wide nocase
            condition:
                2 of them
        }
        
        rule Ransomware_Behavior {
            meta:
                description = "Common Ransomware actions: VSS Deletion, Startup Mutex, Extension manipulation"
            strings:
                $vss1 = "vssadmin" ascii wide nocase
                $vss2 = "delete shadows" ascii wide nocase
                $boot = "bcdedit" ascii wide nocase
                $rec = "recoveryenabled No" ascii wide nocase
            condition:
                ($vss1 and $vss2) or ($boot and $rec)
        }
        
        rule Anti_Sandboxing_Timing {
            meta:
                description = "Evasion via prolonged execution sleep / time checking"
            strings:
                /* Sleep for a long time - pseudo instruction block */
                $api1 = "Sleep" ascii wide
                $api2 = "GetTickCount" ascii wide
                $api3 = "QueryPerformanceCounter" ascii wide
            condition:
                2 of ($api1, $api2, $api3)
        }
        
        rule C2_Beaconing_Headers {
            meta:
                description = "Detects hardcoded user-agents or standard C2 headers"
            strings:
                $ua1 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" ascii wide
                $ua2 = "WinHTTP" ascii wide
                $sus_header = "Authorization: Bearer" ascii wide
            condition:
                any of them
        }
        """
        try:
            self.rules = yara.compile(source=rules_text)
        except Exception as e:
            print(f"  {Fore.RED}[!] Lỗi biên dịch YARA Rules: {e}{Style.RESET_ALL}")

    def scan(self):
        if not self.rules or not os.path.exists(self.filepath):
            return self.findings

        print(f"{Fore.CYAN}  [-] Đang cày xới bộ nhớ bằng YARA (Advanced Byte Pattern Matching)...{Style.RESET_ALL}")
        try:
            matches = self.rules.match(self.filepath)
            for match in matches:
                # Map quy tắc YARA sang chuẩn APS 100 Vectors
                v_id = "APS-VEC-GENERIC"
                if "Evasion" in match.rule or "Anti_Sandboxing" in match.rule: v_id = "APS-VEC-056" # Tầng 6
                if "Crypto" in match.rule: v_id = "APS-VEC-079"  # Tầng 7
                if "Process_Hollowing" in match.rule: v_id = "APS-VEC-021" # Tầng 3
                if "Ransomware" in match.rule: v_id = "APS-VEC-080"
                if "C2_Beaconing" in match.rule: v_id = "APS-VEC-027"
                if "Suspicious_Strings" in match.rule: v_id = "APS-VEC-030"
                
                print(f"  {Fore.RED}[HIGH] YARA Engine Bắt Cảm Biến: Rule {match.rule}{Style.RESET_ALL}")
                
                # Format string output
                hit_strings = []
                for string_data in match.strings:
                    try:
                        h = string_data.instances[0].matched_data.decode('utf-8', 'ignore')
                        if len(h) > 2: hit_strings.append(h)
                    except: pass

                desc = match.meta.get('description', '')
                if hit_strings:
                    desc += f" (Khớp từ khóa: {', '.join(hit_strings[:3])})"

                self.findings.append({
                    "id": v_id,
                    "name": f"YARA Signature Match: {match.rule}",
                    "severity": "HIGH",
                    "description": desc
                })

            if not matches:
                print(f"  {Fore.GREEN}[OK] Vượt qua bài kiểm tra YARA sạch sẽ.{Style.RESET_ALL}")

        except Exception as e:
            print(f"  {Fore.RED}[!] Lỗi khi match YARA: {e}{Style.RESET_ALL}")

        return self.findings
