from colorama import Fore, Style

class ManualAidReporter:
    """
    Cung cấp thông tin trợ lý cho các lỗ hổng siêu phức tạp (Vector 10, 12, 13)
    mà công cụ Black-box Python không thể ép buộc tạo lỗi ngẫu nhiên.
    """
    def __init__(self, target_path):
        self.target_path = target_path
        self.findings = []
        
    def scan(self):
        print(f"{Fore.CYAN}  [-] Sinh Báo Cáo Kỹ Thuật Chuyên Sâu (Manual Pentest Aid)...{Style.RESET_ALL}")
        
        self.findings.append({
            "id": "MAN-UI-010",
            "name": "UI Shatter Attack Vector (WM_COPYDATA)",
            "severity": "INFO", 
            "details": "Kiểm tra bằng công cụ Spy++. Rà soát các Handle (HWND) xem ứng dụng có chấp nhận Window Messages nhạy cảm không."
        })
        self.findings.append({
            "id": "MAN-TCT-012",
            "name": "TOCTOU (Time-Of-Check to Time-Of-Use) Race Conditions",
            "severity": "INFO", 
            "details": "Ứng dụng tương tác với hệ thống tệp. Kẻ tấn công có thể tạo Hardlinks kết hợp với BaitAndSwitch. Hãy sử dụng ProcMon để theo dõi các lệnh IRP_MJ_CREATE."
        })
        self.findings.append({
            "id": "MAN-RPC-013",
            "name": "Advanced IPC / ALPC Fuzzing",
            "severity": "INFO", 
            "details": "Nếu ứng dụng đăng ký giao thức ALPC (Advanced Local Procedure Call) với Windows, hãy dùng NtObjectManager. Fuzzing ALPC thường tìm ra 0-Day Local Privilege Escalation."
        })
        self.findings.append({
            "id": "MAN-SYM-017",
            "name": "Symbolic Execution & Snapshot Fuzzing (Vectors 16, 17, 18)",
            "severity": "CRITICAL", 
            "details": "Sử dụng mẫu angr Script sau để tự động tìm Password/Input bẻ khóa Logic: `import angr; proj = angr.Project('target.exe'); simgr = proj.factory.simgr(); simgr.explore(find=0x401000)`."
        })
        
        print(f"  {Fore.GREEN}[OK] Đã in Báo cáo trợ lý vào Report chính (Vui lòng tự test bằng tay).{Style.RESET_ALL}")
        return self.findings
