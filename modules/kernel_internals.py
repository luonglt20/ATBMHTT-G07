import pefile
from colorama import Fore, Style

class KernelInternalScanner:
    """
    Module phân tích Hệ điều hành & Kernel (Expert Level):
    - Vector 11: Driver Identification (Native Subsystem)
    - Vector 13/14: IPC - ALPC/RPC Analysis
    - Vector 19: Privilege Escalation (Access Tokens)
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        try:
            self.pe = pefile.PE(filepath)
        except:
            self.pe = None

    def scan(self):
        print(f"{Fore.CYAN}  [-] Khởi động Module OS Internals & Kernel (Expert Level)...{Style.RESET_ALL}")
        if not self.pe:
            return []

        self._check_subsystem()
        self._analyze_rpc_alpc_imports()
        self._check_token_privileges()

        return self.findings

    def _check_subsystem(self):
        """Vector 11: Kiểm tra xem file có chạy ở mức Kernel (Native) không."""
        if self.pe.OPTIONAL_HEADER.Subsystem == 1: # IMAGE_SUBSYSTEM_NATIVE
            print(f"  {Fore.RED}[CRITICAL] Phát hiện Windows Kernel Driver (Ring 0)!{Style.RESET_ALL}")
            self.findings.append({
                "id": "KER-DRV-011",
                "name": "Kernel-Mode Native Driver",
                "severity": "CRITICAL",
                "details": "Tệp tin này chạy ở mức đặc quyền cao nhất (Ring 0). Bất kỳ lỗi logic nào cũng có thể dẫn đến BSOD hoặc chiếm quyền điều khiển toàn bộ OS."
            })

    def _analyze_rpc_alpc_imports(self):
        """Vector 13/14: Tìm kiếm các hàm giao tiếp IPC nâng cao."""
        ipc_apis = [
            b"RpcServerUseProtseq", b"RpcServerRegisterIf", # RPC
            b"NtConnectPort", b"NtRequestPort", # ALPC (LPC)
            b"CreateNamedPipeW", b"ConnectNamedPipe" # Named Pipes
        ]
        
        found_ipc = []
        if hasattr(self.pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name in ipc_apis:
                        found_ipc.append(imp.name.decode())

        if found_ipc:
            print(f"  {Fore.YELLOW}[HIGH] Phát hiện cơ chế IPC nâng cao (ALPC/RPC): {found_ipc}{Style.RESET_ALL}")
            self.findings.append({
                "id": "KER-IPC-013",
                "name": "Advanced IPC (ALPC/RPC) Detected",
                "severity": "HIGH",
                "details": f"Ứng dụng sử dụng giao thức giao tiếp liên tiến trình phức tạp: {', '.join(found_ipc)}. Kiểm tra các lỗi 'Shatter Attack' hoặc giả mạo gói tin IPC."
            })

    def _check_token_privileges(self):
        """Vector 19: Rà quét các chuỗi liên quan đến quyền hạn (Privileges)."""
        # Đây là kiểm tra Heuristics dựa trên string (Professional approach)
        interesting_strings = [
            b"SeImpersonatePrivilege", b"SeDebugPrivilege", b"SeBackupPrivilege",
            b"SeRestorePrivilege", b"SeTcbPrivilege", b"SeAssignPrimaryTokenPrivilege"
        ]
        
        found_privs = []
        # Quét qua toàn bộ dữ liệu file để tìm chuỗi hằng
        with open(self.filepath, 'rb') as f:
            content = f.read()
            for priv in interesting_strings:
                if priv in content:
                    found_privs.append(priv.decode())

        if found_privs:
            print(f"  {Fore.YELLOW}[MEDIUM] Phát hiện đặc quyền nhạy cảm (Tokens): {found_privs}{Style.RESET_ALL}")
            self.findings.append({
                "id": "KER-LPE-019",
                "name": "Sensitive Privilege Strings Detected",
                "severity": "MEDIUM",
                "details": f"Ứng dụng chứa các tham chiếu đến đặc quyền hệ thống: {', '.join(found_privs)}. Có khả năng hacker lợi dụng để leo thang đặc quyền (Local Privilege Escalation)."
            })
