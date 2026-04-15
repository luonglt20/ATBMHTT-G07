import pefile
import re
from colorama import Fore, Style

class WindowsServicesManifestScanner:
    """
    Quét đặc quyền trong XML Manifest (UAC bypass, RequireAdministrator) 
    và các nguy cơ Service (LPE).
    Note: Black Box quét tĩnh chỉ có thể phân tích Manifest được embed trong PE.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []

    def scan(self):
        print(f"{Fore.CYAN}  [-] Quét PE Resource / XML Manifest (UAC LPE/Misconfigs)...{Style.RESET_ALL}")
        try:
            pe = pefile.PE(self.filepath)
            manifest_str = self._extract_manifest(pe)
            
            if not manifest_str:
                return self.findings

            # Phân tích Privilege (RequireAdministrator)
            if "requireAdministrator".lower() in manifest_str.lower():
                print(f"  {Fore.YELLOW}[MEDIUM] XML Manifest lạm dụng đặc quyền: requireAdministrator{Style.RESET_ALL}")
                self.findings.append({
                    "id": "SYS-MAN-001",
                    "name": "UAC Escalation - RequireAdministrator",
                    "severity": "MEDIUM",
                    "details": "Ứng dụng tự động yêu cầu quyền Admin cao nhất. Nếu bị khai thác (qua DLL Hijack), hacker dễ dàng lấy quyền SYSTEM."
                })
                
            # Phân tích UI Access (Shatter Attack vector)
            if "uiAccess=\"true\"".lower() in manifest_str.lower():
                print(f"  {Fore.RED}[HIGH] XML Manifest lạm dụng cờ uiAccess=true!{Style.RESET_ALL}")
                self.findings.append({
                    "id": "SYS-MAN-002",
                    "name": "UI Access Attribute enabled",
                    "severity": "HIGH",
                    "details": "Cho phép bypass UIPI, gửi Message IPC đến window cấp cao (Shatter Attack / Keylogging)."
                })

            if not self.findings:
                print(f"  {Fore.GREEN}[OK] Thiết lập XML Manifest an toàn.{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}  [!] Lỗi quét Manifest: {str(e)}{Style.RESET_ALL}")
            
        return self.findings

    def _extract_manifest(self, pe):
        # Resource Type cho Manifest trong PE thường là 24 (RT_MANIFEST)
        RT_MANIFEST = 24
        
        if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
            for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if resource_type.id == RT_MANIFEST:
                    for resource_id in resource_type.directory.entries:
                        for resource_lang in resource_id.directory.entries:
                            offset = resource_lang.data.struct.OffsetToData
                            size = resource_lang.data.struct.Size
                            data = pe.get_memory_mapped_image()[offset:offset+size]
                            return data.decode("utf-8", "ignore")
        return None
