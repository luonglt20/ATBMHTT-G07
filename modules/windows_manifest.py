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
                # Dù không có manifest, vẫn phải quét Anomalies của `.rsrc` section
                self._analyze_rsrc_anomalies(pe)
                return self.findings

            # Phân tích Privilege (RequireAdministrator & AutoElevate)
            if "requireAdministrator".lower() in manifest_str.lower():
                print(f"  {Fore.YELLOW}[MEDIUM] XML Manifest lạm dụng đặc quyền: requireAdministrator{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-041",
                    "name": "UAC Escalation - RequireAdministrator",
                    "severity": "MEDIUM",
                    "details": "Ứng dụng tự động yêu cầu quyền Admin cao nhất. Nếu bị khai thác (qua DLL Hijack), hacker dễ dàng lấy quyền SYSTEM."
                })
                
            if "autoelevate=\"true\"".lower() in manifest_str.lower().replace(" ", ""):
                print(f"  {Fore.RED}[CRITICAL] XML Manifest lạm dụng AutoElevate (Tiềm ẩn UAC Bypass!){Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-043",
                    "name": "UAC Bypass Vector - AutoElevate",
                    "severity": "CRITICAL",
                    "details": "Thuộc tính autoElevate=true cho phép tiến trình bỏ qua cửa sổ cảnh báo UAC (chạy thẳng bằng Admin). EDR sẽ soi cực kỳ gắt."
                })
                
            # Phân tích UI Access (Shatter Attack vector)
            if "uiAccess=\"true\"".lower() in manifest_str.lower():
                print(f"  {Fore.RED}[HIGH] XML Manifest lạm dụng cờ uiAccess=true!{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-042",
                    "name": "UI Access Attribute enabled",
                    "severity": "HIGH",
                    "details": "Cho phép bypass UIPI, gửi Message IPC đến window cấp cao (Shatter Attack / Keylogging)."
                })

            # TÍNH NĂNG NÂNG CẤP: DpiAwareness và LongPathAware (Tầng 5/Tầng 9)
            if "dpiawareness" in manifest_str.lower():
                print(f"  {Fore.YELLOW}[LOW] XML Manifest sử dụng DpiAwareness (Tiềm ẩn GDI Exploits){Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-047", # Tạm map
                    "name": "DPI Awareness Configured",
                    "severity": "LOW",
                    "details": "Thuộc tính DpiAwareness có thể liên đới tới một số kỹ thuật lạm dụng GDI hoặc COM đặc biệt."
                })

            if "longpathaware=\"true\"" in manifest_str.lower().replace(" ", ""):
                print(f"  {Fore.YELLOW}[MEDIUM] XML Manifest sử dụng longPathAware=true{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-048", # Tạm map
                    "name": "LongPathAware Enabled",
                    "severity": "MEDIUM",
                    "details": "Cho phép file path > 260 ký tự. Có thể bị lợi dụng trong các cuộc tấn công Path Traversal lẩn tránh EDR/AV không hỗ trợ đường dẫn dài."
                })

        except Exception as e:
            print(f"{Fore.RED}  [!] Lỗi phân tích Manifest/Resource: {str(e)}{Style.RESET_ALL}")
            
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

    def _analyze_rsrc_anomalies(self, pe):
        # TÍNH NĂNG NÂNG CẤP: Phân tích tài nguyên dị thường (Resource Payload Dropper)
        for section in pe.sections:
            sec_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
            if sec_name.lower() == '.rsrc':
                entropy = section.get_entropy()
                size = section.SizeOfRawData
                # Nếu file resource nặng trên 10MB hoặc có entropy siêu cao (Mã hóa)
                if size > 10 * 1024 * 1024 or entropy > 7.2:
                    print(f"  {Fore.RED}[HIGH] Bất thường ở Tầng 5: Phân vùng .rsrc chứa dữ liệu mờ ám!{Style.RESET_ALL}")
                    self.findings.append({
                        "id": "APS-VEC-046",
                        "name": "Suspicious Encrypted Resource Payload",
                        "severity": "HIGH",
                        "details": f"Phân vùng chứa Tài nguyên (.rsrc) có kích thước lớn ({size} bytes) hoặc bị mã hóa nặng nề (Entropy: {entropy:.2f}). Có thể chứa Dropper/Shellcode ẩn."
                    })
