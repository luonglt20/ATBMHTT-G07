import pefile
from colorama import Fore, Style

class APIScanner:
    """
    Tầng 3: Import Table (IAT) Anomaly & Dangerous APIs.
    Phát hiện các API nhạy cảm thường dùng trong Malware/Exploitation.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        try:
            self.pe = pefile.PE(filepath)
        except:
            self.pe = None

        self.DANGEROUS_APIS = {
            "Process Injection": ["OpenProcess", "VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread", "QueueUserAPC", "NtCreateThreadEx"],
            "Evasion/Anti-Debug": ["IsDebuggerPresent", "CheckRemoteDebuggerPresent", "FindWindow", "GetTickCount", "OutputDebugString", "NtQueryInformationProcess"],
            "System Tampering": ["RegSetValueEx", "ControlService", "CreateService", "SetWindowsHookEx", "WritePrivateProfileString"],
            "Network/Exfiltration": ["InternetOpen", "HttpOpenRequest", "HttpSendRequest", "Socket", "Connect", "WSAStartup"],
            "Reconnaissance": ["EnumProcesses", "EnumProcessModules", "GetModuleHandle", "GetProcAddress", "IsProcessorFeaturePresent"],
            "COM Hijacking Vector": ["CoCreateInstance", "CoGetClassObject", "CoInitializeEx", "CLSIDFromString"],
            "WMI Persistence": ["ConnectServerW", "ExecNotificationQueryW", "ExecMethodW", "PutInstanceW"],
            "Native/Undocumented (NTDLL)": ["NtQuerySystemInformation", "NtProtectVirtualMemory", "NtAllocateVirtualMemory", "LdrLoadDll", "NtCreateSection", "NtMapViewOfSection"]
        }

    def scan(self):
        if not self.pe: return []
        print(f"  {Fore.CYAN}[-]{Style.RESET_ALL} Phân tích API Anomaly & IAT Vectors (Tầng 3)...")
        
        found_apis = []
        api_list_flat = []
        dlls_loaded = []
        if hasattr(self.pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode('utf-8', errors='ignore')
                dlls_loaded.append(dll_name.lower())
                for imp in entry.imports:
                    if imp.name:
                        api_name = imp.name.decode('utf-8', errors='ignore')
                        api_list_flat.append(api_name)
                        for category, apis in self.DANGEROUS_APIS.items():
                            if api_name in apis:
                                found_apis.append((category, api_name, dll_name))

        # TÍNH NĂNG NÂNG CẤP 3: Lỗi cấu trúc DLL (Missing Kernel32)
        if dlls_loaded and not any("kernel32.dll" in d for d in dlls_loaded) and not any("ntdll.dll" in d for d in dlls_loaded):
            print(f"  {Fore.RED}[CRITICAL] Phát hiện cấu trúc IAT DỊ DẠNG: Không nạp Kernel32/NTDLL!{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-028",
                "name": "Malformed Import Table (Core DLL Missing)",
                "severity": "CRITICAL",
                "description": "File thực thi không nạp Windows Subsystem cơ sở (kernel32/ntdll). 100% sử dụng Custom Loader hoặc bị hỏng nặng."
            })

        # TÍNH NĂNG NÂNG CẤP 4: Suspicious Exports (Reflective Loading)
        if hasattr(self.pe, 'DIRECTORY_ENTRY_EXPORT'):
            exports = [exp.name.decode('utf-8', 'ignore') for exp in self.pe.DIRECTORY_ENTRY_EXPORT.symbols if exp.name]
            suspicious_exports = ["ReflectiveLoader", "DllMain", "StartProxy"]
            for exp in exports:
                if any(sus in exp for sus in suspicious_exports):
                    print(f"  {Fore.RED}[CRITICAL] HỆ TƯ TƯỞNG C2: Tìm thấy Export Function '{exp}'!{Style.RESET_ALL}")
                    self.findings.append({
                        "id": "APS-VEC-026",
                        "name": f"Suspicious Export Function ({exp})",
                        "severity": "CRITICAL",
                        "description": f"File xuất ra hàm độc hại '{exp}'. Dấu hiệu kinh điển của kỹ thuật chèn mã Reflective DLL Injection."
                    })

        # ---------------------------------------------------------
        # TÍNH NĂNG NÂNG CẤP 1: Phân tích Chuỗi Kịch Bản (Heuristic API Chains)
        # Các Malware thường gọi các mảng API theo cụm. Nếu thấy cả cụm thì tăng điểm rủi ro.
        # ---------------------------------------------------------
        heuristics_rules = {
            "Process Hollowing / Injection": {"req": ["VirtualAllocEx", "WriteProcessMemory"], "risk": "CRITICAL", "id": "APS-VEC-021"},
            "Thread Hijacking": {"req": ["CreateRemoteThread", "VirtualAllocEx"], "risk": "CRITICAL", "id": "APS-VEC-021"},
            "Keylogger / Hooking": {"req": ["SetWindowsHookEx", "CallNextHookEx"], "risk": "CRITICAL", "id": "APS-VEC-029"},
            "Ransomware Crypto": {"req": ["CryptAcquireContext", "CryptGenKey", "CryptEncrypt"], "risk": "HIGH", "id": "APS-VEC-079"}
        }

        for rule_name, rule_data in heuristics_rules.items():
            # Check if subset matching
            if all(req_api in api_list_flat for req_api in rule_data["req"]):
                print(f"  {Fore.RED}[CRITICAL] HEURISTIC MATCH: Ứng dụng chứa chuỗi tác chiến của '{rule_name}'!{Style.RESET_ALL}")
                self.findings.append({
                    "id": rule_data["id"],
                    "name": f"Heuristic Chain: {rule_name}",
                    "severity": rule_data["risk"],
                    "description": f"Phát hiện chuỗi API điển hình: {', '.join(rule_data['req'])}. Nguy cơ khai thác thực tế 99%."
                })

        # ---------------------------------------------------------
        # TÍNH NĂNG NÂNG CẤP 2: Dynamic API Loading (Bộ nạp lẩn tránh kiểu GHOST-PROTOCOL)
        # ---------------------------------------------------------
        if len(api_list_flat) < 15 and ("GetProcAddress" in api_list_flat or "LoadLibraryA" in api_list_flat):
            print(f"  {Fore.RED}[CRITICAL] Ứng dụng dường như đang CHE GIẤU API (Dynamic Loading). IAT rất nhỏ!{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-056",
                "name": "Evasion: Dynamic API Resolution",
                "severity": "HIGH",
                "description": f"PE File chỉ có {len(api_list_flat)} APIs và có nạp GetProcAddress. Đây là kỹ thuật giấu IAT phổ biến trong payload tàng hình như GHOST-PROTOCOL."
            })


        # Nhóm kết quả theo Category để chuyên nghiệp hơn
        categories_detected = {}
        for cat, api, dll in found_apis:
            if cat not in categories_detected: categories_detected[cat] = []
            categories_detected[cat].append(f"{api} ({dll})")

        # Map tên Category sang ID chuẩn trong 100 Vectors
        ID_MAP = {
            "Process Injection": "APS-VEC-021",
            "Evasion/Anti-Debug": "APS-VEC-022",
            "Anti-VM Detection": "APS-VEC-023",
            "System Tampering": "APS-VEC-029",
            "Network/Exfiltration": "APS-VEC-027",
            "Reconnaissance": "APS-VEC-017",
            "COM Hijacking Vector": "APS-VEC-038",
            "WMI Persistence": "APS-VEC-088",
            "Native/Undocumented (NTDLL)": "APS-VEC-024"
        }

        for cat, list_apis in categories_detected.items():
            severity = "HIGH" if cat in ["Process Injection", "System Tampering"] else "MEDIUM"
            v_id = ID_MAP.get(cat, "APS-VEC-GENERIC")
            
            self.findings.append({
                "id": v_id,
                "name": f"Dangerous API Category: {cat}",
                "severity": severity,
                "description": f"Phát hiện nhóm API nhạy cảm ({cat}): {', '.join(list_apis[:5])}...",
                "remediation": "Kiểm tra xem các API này có thực sự cần thiết cho logic nghiệp vụ hay không."
            })
            print(f"  {Fore.YELLOW}[!] Phát hiện tập hợp API {cat}: {len(list_apis)} hàm.{Style.RESET_ALL}")

        return self.findings
