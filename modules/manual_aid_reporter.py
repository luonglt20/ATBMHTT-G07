from colorama import Fore, Style
import os

class ManualAidReporter:
    """
    Cung cấp hướng dẫn Pentest thủ công cho các lỗi Logic phức tạp (Tầng 10):
    - APS-VEC-010: UI Shatter Attacks
    - APS-VEC-012: Race Conditions (TOCTOU)
    - APS-VEC-017: Symbolic Execution (angr)
    """
    def __init__(self, target_path):
        self.target_path = target_path
        self.findings = []
        
    def scan(self):
        print(f"{Fore.CYAN}  [-] Sinh Báo Cáo Hỗ Trợ Pentest Thủ Công Tier-3...{Style.RESET_ALL}")
        
        # UI Message Exploitation
        self.findings.append({
            "id": "APS-VEC-010",
            "name": "Advanced UI Message Exploitation (Shatter)",
            "severity": "INFO", 
            "details": "Kiểm tra bằng công cụ Spy++. Rà soát các Handle (HWND) xem ứng dụng có chấp nhận Window Messages nhạy cảm như WM_COPYDATA hay không. Đây là vector dẫn đến chiếm quyền process khác cùng Desktop."
        })

        # Symbolic Execution for Logic bypass
        self.findings.append({
            "id": "APS-VEC-017",
            "name": "Symbolic Execution Path Discovery",
            "severity": "CRITICAL", 
            "details": f"Ứng dụng phức tạp, khuyến nghị dùng angr để bẻ khóa Logic: `import angr; p = angr.Project('{os.path.basename(self.target_path)}'); state = p.factory.entry_state(); simgr = p.factory.simgr(state); simgr.explore(find=lambda s: b'Success' in s.posix.dumps(1))`"
        })

        # Race Condition (TOCTOU)
        self.findings.append({
            "id": "APS-VEC-012",
            "name": "File System Race Condition (TOCTOU)",
            "severity": "INFO", 
            "details": "Theo dõi IRP_MJ_CREATE qua ProcMon. Thử nghiệm kỹ thuật BaitAndSwitch (Symlink transition) vào thời điểm ứng dụng Check file nhưng chưa Use file."
        })
        
        print(f"  {Fore.GREEN}[OK] Đã tích hợp cẩm nang Pentest vào báo cáo.{Style.RESET_ALL}")
        return self.findings
