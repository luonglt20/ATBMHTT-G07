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

            if not hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                return self.findings
                
            suspicious_dlls = []
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.lower()
                if dll_name in self.system_dlls: continue
                suspicious_dlls.append(dll_name.decode("utf-8", "ignore"))

            if suspicious_dlls:
                severity = "CRITICAL" if is_writable else "MEDIUM"
                privilege = "Standard User" if is_writable else "Administrator"
                
                print(f"  {Fore.RED if is_writable else Fore.YELLOW}[{severity}] Phát hiện nguy cơ DLL Hijacking: {suspicious_dlls[:3]}...{Style.RESET_ALL}")
                if is_writable:
                    print(f"  {Fore.RED}[!] App nằm ở thư mục GHI ĐƯỢC -> Cho phép Hack không cần Admin (LPE)!{Style.RESET_ALL}")

                self.findings.append({
                    "id": "SYS-DLL-001",
                    "name": "Potential DLL Hijacking Vector",
                    "severity": severity,
                    "privilege": privilege,
                    "description": f"Ứng dụng load các DLL không thuộc System ({', '.join(suspicious_dlls[:3])}). {'Sếp có thể hack ngay quyền User vì thư mục có quyền Ghi.' if is_writable else 'Cần quyền ghi vào thư mục App để khai thác.'}",
                    "dll_name": suspicious_dlls[0] if suspicious_dlls else "hijacked.dll"
                })
            else:
                print(f"  {Fore.GREEN}[OK] Bảng Import Table trông an sau.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}  [!] Error quét DLL Hijack: {str(e)}{Style.RESET_ALL}")
            
        return self.findings
