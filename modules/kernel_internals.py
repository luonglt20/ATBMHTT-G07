import pefile
from colorama import Fore, Style

class KernelInternalScanner:
    """
    Module phân tích Hệ điều hành & Kernel (Tầng 9):
    - APS-VEC-084: Driver Identification (Native Subsystem)
    - APS-VEC-087: IPC - ALPC/RPC Analysis
    - APS-VEC-085: COM Hijacking Interface references
    - APS-VEC-089: Privilege Escalation (Access Tokens)
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        try:
            self.pe = pefile.PE(filepath)
        except:
            self.pe = None

    def scan(self):
        print(f"{Fore.CYAN}  [-] Khởi động Module OS Internals & Kernel Tier-3...{Style.RESET_ALL}")
        if not self.pe:
            return []

        self._check_subsystem()
        self._analyze_rpc_alpc_imports()
        self._check_com_hijacking_references()
        self._check_token_privileges()

        return self.findings

    def _check_subsystem(self):
        """APS-VEC-084: Kiểm tra xem file có chạy ở mức Kernel (Native) không."""
        if self.pe.OPTIONAL_HEADER.Subsystem == 1: # IMAGE_SUBSYSTEM_NATIVE
            print(f"  {Fore.RED}[CRITICAL] Phát hiện Windows Kernel Driver (Ring 0)!{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-084",
                "name": "Kernel-Mode Native Driver",
                "severity": "CRITICAL",
                "details": "Tệp tin chạy ở mức đặc quyền Ring 0. Lỗi logic tại đây có thể dẫn đến chiếm quyền điều khiển toàn bộ hệ điều hành thông qua khai thác Driver IOCTL."
            })

    def _analyze_rpc_alpc_imports(self):
        """APS-VEC-087: Tìm kiếm các hàm giao tiếp IPC nâng cao (ALPC/RPC)."""
        ipc_apis = [
            b"RpcServerUseProtseq", b"RpcServerRegisterIf",
            b"NtConnectPort", b"NtRequestPort",
            b"CreateNamedPipeW", b"ConnectNamedPipe"
        ]
        found_ipc = []
        if hasattr(self.pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name in ipc_apis: found_ipc.append(imp.name.decode())

        if found_ipc:
            print(f"  {Fore.YELLOW}[HIGH] Phát hiện cơ chế IPC nâng cao (ALPC/RPC): {found_ipc}{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-087",
                "name": "Advanced IPC (ALPC/RPC) Exposure",
                "severity": "HIGH",
                "details": f"Ứng dụng sử dụng giao thức IPC phức tạp: {', '.join(found_ipc)}. Các giao tiếp này thường thiếu kiểm tra access control chặt chẽ, dẫn đến lỗi Shatter Attacks."
            })

    def _check_com_hijacking_references(self):
        """APS-VEC-085: Tìm các tham chiếu đến Registry CLSID (Dấu hiệu COM hijacking)."""
        com_patterns = [b"InprocServer32", b"LocalServer32", b"ProgID", b"treatas"]
        found = []
        with open(self.filepath, 'rb') as f:
            content = f.read()
            for p in com_patterns:
                if p in content: found.append(p.decode())

        if found:
            print(f"  {Fore.YELLOW}[MEDIUM] Phát hiện tham chiếu COM Interface: {found}{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-085",
                "name": "COM Interface Interaction",
                "severity": "MEDIUM",
                "details": f"Ứng dụng tương tác với COM Registry keys: {', '.join(found)}. Pentester có thể thực hiện COM Hijacking để duy trì quyền kiểm soát (Persistence)."
            })

    def _check_token_privileges(self):
        """APS-VEC-089: Rà quét các chuỗi liên quan đến quyền hạn (Privileges)."""
        interesting_strings = [
            b"SeImpersonatePrivilege", b"SeDebugPrivilege", b"SeBackupPrivilege",
            b"SeRestorePrivilege", b"SeTcbPrivilege", b"SeAssignPrimaryTokenPrivilege"
        ]
        found_privs = []
        with open(self.filepath, 'rb') as f:
            content = f.read()
            for priv in interesting_strings:
                if priv in content: found_privs.append(priv.decode())

        if found_privs:
            print(f"  {Fore.RED}[HIGH] Phát hiện đặc quyền nhạy cảm (Leo thang quyền LPE): {found_privs}{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-089",
                "name": "LPE Token Privilege Strings",
                "severity": "HIGH",
                "details": f"Ứng dụng chứa các đặc quyền hệ thống nhạy cảm: {', '.join(found_privs)}. Đây là 'vàng mười' cho các kỹ thuật Token Impersonation (Leo thang đặc quyền)."
            })
