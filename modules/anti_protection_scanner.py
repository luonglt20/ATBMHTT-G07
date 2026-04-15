import pefile
from colorama import Fore, Style

class AntiProtectionScanner:
    """
    Module rà quét công nghệ chống gỡ ngược (Expert Level):
    - Vector 19: Hypervisor Detection (VMI Detection)
    - Vector 39: Stealth Anti-Debugging (Polling/Timing)
    - Vector 44: Side-Channel Timing Attacks (Heuristics)
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        try:
            self.pe = pefile.PE(filepath)
        except:
            self.pe = None

    def scan(self):
        print(f"{Fore.CYAN}  [-] Khởi động Module Anti-Protection & Evasion (Expert Level)...{Style.RESET_ALL}")
        if not self.pe:
            return []

        self._check_timing_check_imports()
        self._check_hypervisor_detection_heuristics()
        self._check_debug_artifact_names()
        self._check_for_advanced_sandbox()

        return self.findings

    def _check_for_advanced_sandbox(self):
        """Vector 10.1: Phát hiện cơ chế kiểm tra Sandbox cấp cao (Sử dụng Instruction Timing)."""
        sandbox_indicators = [b"IsSandbox", b"InSandbox", b"SbieDll", b"Cuckoo", b"JoeSandbox"]
        found = []
        with open(self.filepath, 'rb') as f:
            content = f.read()
            for ind in sandbox_indicators:
                if ind in content:
                    found.append(ind.decode())

        if found:
            print(f"  {Fore.RED}[CRITICAL] Phát hiện dấu vết Anti-Sandbox (Omni-Level): {found}{Style.RESET_ALL}")
            self.findings.append({
                "id": "PRO-SBX-010",
                "name": "Advanced Sandbox Analysis Logic",
                "severity": "CRITICAL",
                "privilege": "Standard User",
                "description": f"Ứng dụng chủ động phát hiện các môi trường Sandbox chuyên dụng ({', '.join(found)}). Đây là dấu hiệu của Malware cao cấp hoặc mã nguồn cực kỳ nhạy cảm."
            })

    def _check_timing_check_imports(self):
        """Vector 44: Phát hiện các hàm đo thời gian nhạy cảm dùng cho Timing Attacks."""
        timing_apis = [
            b"GetTickCount", b"GetTickCount64", b"QueryPerformanceCounter",
            b"GetSystemTimeAsFileTime", b"timeGetTime"
        ]
        
        found_timing = []
        if hasattr(self.pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name in timing_apis:
                        found_timing.append(imp.name.decode())

        if len(found_timing) >= 2:
            print(f"  {Fore.YELLOW}[HIGH] Phát hiện cơ chế so sánh thời gian (Timing Analysis): {found_timing}{Style.RESET_ALL}")
            self.findings.append({
                "id": "PRO-TIME-044",
                "name": "Timing Side-Channel Analysis",
                "severity": "HIGH",
                "details": f"Ứng dụng nhập khẩu nhiều hàm đo thời gian: {', '.join(found_timing)}. Đây có thể là cơ chế chống Debugger bằng cách đo độ trễ nanon-giây hoặc tấn công Kênh kề (Side-channel)."
            })

    def _check_hypervisor_detection_heuristics(self):
        """Vector 19: Tìm kiếm các chuỗi nhạy cảm dùng để phát hiện VM/Hypervisor."""
        vm_strings = [
            b"VBoxGuest", b"vmtoolsd", b"VMware", b"VirtualBox", b"QEMU",
            b"Hyper-V", b"BOSH", b"XenVMM", b"wine_get_version"
        ]
        
        found_vm = []
        with open(self.filepath, 'rb') as f:
            content = f.read()
            for vm in vm_strings:
                if vm in content:
                    found_vm.append(vm.decode())

        if found_vm:
            print(f"  {Fore.RED}[CRITICAL] Phát hiện kỹ thuật Anti-VM / Hypervisor Detection!{Style.RESET_ALL}")
            self.findings.append({
                "id": "PRO-VM-019",
                "name": "Hypervisor Evasion Trick",
                "severity": "CRITICAL",
                "details": f"Ứng dụng chủ động tìm kiếm dấu vết của máy ảo: {', '.join(found_vm)}. Kẻ tấn công sẽ bị đá văng (Evasion) nếu chạy trong Sandbox."
            })

    def _check_debug_artifact_names(self):
        """Vector 39: Tìm các tên tệp tin gỡ lỗi phổ biến."""
        debug_artifacts = [
            b"x64dbg.exe", b"ollydbg.exe", b"ida.exe", b"wireshark.exe",
            b"processhacker.exe", b"cheatengine-x86_64.exe"
        ]
        
        found_artifacts = []
        with open(self.filepath, 'rb') as f:
            content = f.read()
            for art in debug_artifacts:
                if art in content:
                    found_artifacts.append(art.decode())

        if found_artifacts:
            print(f"  {Fore.YELLOW}[MEDIUM] Phát hiện danh sách chặn Debugger (Blacklist): {found_artifacts}{Style.RESET_ALL}")
            self.findings.append({
                "id": "PRO-DBG-039",
                "name": "Debugger Blacklist Detection",
                "severity": "MEDIUM",
                "details": f"Ứng dụng chứa danh sách các công cụ gỡ lỗi bị cấm: {', '.join(found_artifacts)}. Cần che giấu tiến trình gỡ lỗi trước khi nạp file."
            })
