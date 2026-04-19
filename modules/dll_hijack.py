import pefile
import os
from colorama import Fore, Style

class DLLHijackingScanner:
    """
    Quét IAT (Import Address Table) của PE File.
    Tìm kiếm các DLL không phải System DLL (như kernel32.dll, user32.dll)
    và không có đường dẫn tuyệt đối, dẫn đến nguy cơ DLL_Planting / Hijacking (LoadLibrary).
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        
        # Danh sách các DLL hệ thống (KnownDLLs) thường được bảo vệ bởi Windows loader
        self.system_dlls = [
            b"kernel32.dll", b"user32.dll", b"advapi32.dll", b"ntdll.dll", 
            b"rpcrt4.dll", b"oleaut32.dll", b"comctl32.dll", b"shell32.dll",
            b"gdi32.dll", b"ws2_32.dll", b"msvcrt.dll", b"winmm.dll",
            b"wininet.dll", b"shlwapi.dll", b"userenv.dll", b"crypt32.dll"
        ]

    def scan(self):
        print(f"{Fore.CYAN}  [-] Quét Import Table (IAT) kiểm tra DLL Hijacking Vector...{Style.RESET_ALL}")
        try:
            pe = pefile.PE(self.filepath)
            
            # Check if directory is writable (Low-Privilege LPE check)
            dir_path = os.path.dirname(os.path.abspath(self.filepath))
            is_writable = False
            try:
                test_file = os.path.join(dir_path, ".hijack_test")
                with open(test_file, 'w') as f: f.write('t')
                os.remove(test_file)
                is_writable = True
            except: pass

            suspicious_dlls = []
            mitigation_apis = []
            
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    dll_name = entry.dll.lower()
                    if dll_name in self.system_dlls: continue
                    suspicious_dlls.append(dll_name.decode("utf-8", "ignore"))
                    for imp in entry.imports:
                        if imp.name:
                            api_name = imp.name.decode('utf-8', 'ignore')
                            if api_name in ["SetDefaultDllDirectories", "SetDllDirectoryW", "SetDllDirectoryA", "AddDllDirectory"]:
                                mitigation_apis.append(api_name)

            # TÍNH NĂNG NÂNG CẤP: Quét Delay Loaded DLLs (Vector 34: Lỗ hổng cực kỳ nghiêm trọng vì nó load động)
            delay_dlls = []
            if hasattr(pe, 'DIRECTORY_ENTRY_DELAY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_DELAY_IMPORT:
                    dll_name = entry.dll.lower()
                    delay_dlls.append(dll_name.decode("utf-8", "ignore"))
                    suspicious_dlls.append(dll_name.decode("utf-8", "ignore"))
                    
            if delay_dlls:
                print(f"  {Fore.RED}[CRITICAL] Phát hiện Delay-Loaded DLLs: {delay_dlls[:3]}. Mã độc có thể thay đổi môi trường trước khi DLL bị nạp!{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-034",
                    "name": "Delay-Load DLL Hijacking",
                    "severity": "CRITICAL",
                    "privilege": "Administrator" if not is_writable else "Standard User",
                    "description": f"Ứng dụng sử dụng Delay-Load cho {', '.join(delay_dlls[:3])}. Hacker có thể chèn DLL độc hại vào Search Path (qua thư mục hiện tại hoặc môi trường) trước khi luồng gọi đến hàm này."
                })

            # TÍNH NĂNG NÂNG CẤP: Audit Mitigation API
            if not mitigation_apis:
                print(f"  {Fore.YELLOW}[MEDIUM] Missing Hardened Search Path: Không gọi API bảo vệ lây nhiễm DLL.{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-035",
                    "name": "Missing SafeDllSearchMode Mitigation",
                    "severity": "MEDIUM",
                    "privilege": "None",
                    "description": "Ứng dụng không gọi SetDefaultDllDirectories() hoặc SetDllDirectory(). Nguy cơ rất lớn bị lây nhiễm qua lỗ hổng CWD (Current Working Directory) khi chạy qua shortcut hoặc tệp liên kết."
                })
            else:
                print(f"  {Fore.GREEN}[OK] Ứng dụng có các biện pháp phòng vệ nạp DLL: {', '.join(mitigation_apis)}{Style.RESET_ALL}")

            phantom_dlls = []
            proxy_dlls = []
            privilege = "Standard User" if is_writable else "Administrator"
            
            for dll in suspicious_dlls:
                # Kiểm tra xem DLL có tồn tại trong thư mục của tệp thực thi không
                dll_path = os.path.normpath(os.path.join(dir_path, dll))
                if not os.path.exists(dll_path):
                    phantom_dlls.append(dll)
                else:
                    proxy_dlls.append(dll)

            if phantom_dlls:
                print(f"  {Fore.RED}[CRITICAL] Phát hiện Phantom DLL (Vector 32): {phantom_dlls[:3]} - FILE KHÔNG TỒN TẠI!{Style.RESET_ALL}")
                print(f"  {Fore.MAGENTA}[!] Đây là lỗ hổng CHỦ ĐỘNG: Không cần đổi tên file gốc, chỉ cần quăng file mã độc vào.{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-032",
                    "name": "Missing DLL Audit (Phantom Hijack)",
                    "severity": "CRITICAL",
                    "privilege": privilege,
                    "description": f"Ứng dụng cố nạp các DLL không tồn tại trong thư mục gốc: {', '.join(phantom_dlls[:3])}. Kẻ tấn công có thể đặt file mã độc vào để chiếm quyền điều khiển.",
                    "dll_name": phantom_dlls[0]
                })

            if proxy_dlls:
                severity = "CRITICAL" if is_writable else "MEDIUM"
                print(f"  {Fore.YELLOW}[{severity}] Phát hiện DLL Proxying (Vector 33): {proxy_dlls[:3]}{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-033",
                    "name": "DLL Proxying / Search Order Audit",
                    "severity": severity,
                    "privilege": privilege,
                    "description": f"Ứng dụng load các DLL có tồn tại: {', '.join(proxy_dlls[:3])}. Cần kỹ thuật Export Proxying (đổi tên gốc thành _original.dll) để tránh crash app.",
                    "dll_name": proxy_dlls[0]
                })

            if not suspicious_dlls:
                print(f"  {Fore.GREEN}[OK] Bảng Import Table trông an sau.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}  [!] Error quét DLL Hijack: {str(e)}{Style.RESET_ALL}")
            
        return self.findings
