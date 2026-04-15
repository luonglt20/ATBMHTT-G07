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
            "Evasion/Anti-Debug": ["IsDebuggerPresent", "CheckRemoteDebuggerPresent", "FindWindow", "GetTickCount", "OutputDebugString"],
            "System Tampering": ["RegSetValueEx", "ControlService", "CreateService", "SetWindowsHookEx"],
            "Network/Exfiltration": ["InternetOpen", "HttpOpenRequest", "HttpSendRequest", "Socket", "Connect"],
            "Reconnaissance": ["EnumProcesses", "EnumProcessModules", "GetModuleHandle", "GetProcAddress"]
        }

    def scan(self):
        if not self.pe: return []
        print(f"  {Fore.CYAN}[-]{Style.RESET_ALL} Phân tích API Anomaly & IAT Vectors (Tầng 3)...")
        
        found_apis = []
        if hasattr(self.pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode('utf-8', errors='ignore')
                for imp in entry.imports:
                    if imp.name:
                        api_name = imp.name.decode('utf-8', errors='ignore')
                        for category, apis in self.DANGEROUS_APIS.items():
                            if api_name in apis:
                                found_apis.append((category, api_name, dll_name))

        # Nhóm kết quả theo Category để chuyên nghiệp hơn
        categories_detected = {}
        for cat, api, dll in found_apis:
            if cat not in categories_detected: categories_detected[cat] = []
            categories_detected[cat].append(f"{api} ({dll})")

        for cat, list_apis in categories_detected.items():
            severity = "HIGH" if cat in ["Process Injection", "System Tampering"] else "MEDIUM"
            self.findings.append({
                "id": f"PE-VEC-API-{cat[:3].upper()}",
                "name": f"Dangerous API Category: {cat}",
                "severity": severity,
                "description": f"Phát hiện nhóm API nhạy cảm ({cat}): {', '.join(list_apis[:5])}...",
                "remediation": "Kiểm tra xem các API này có thực sự cần thiết cho logic nghiệp vụ hay không."
            })
            print(f"  {Fore.YELLOW}[!] Phát hiện tập hợp API {cat}: {len(list_apis)} hàm.{Style.RESET_ALL}")

        return self.findings
