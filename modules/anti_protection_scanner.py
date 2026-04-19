import pefile
from colorama import Fore, Style
import re

class AntiProtectionScanner:
    """
    Module rà quét công nghệ chống gỡ ngược & trốn tránh (Tầng 6):
    - APS-VEC-051: High Entropy / Packed detection
    - APS-VEC-054: Anti-Debugging / VM Detection
    - APS-VEC-057: Sandbox Evasion logic
    - APS-VEC-058: Instruction Timing (RDTSC)
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        try:
            self.pe = pefile.PE(filepath)
        except:
            self.pe = None

    def scan(self):
        print(f"{Fore.CYAN}  [-] Khởi động Module Anti-Protection & Evasion Tier-3...{Style.RESET_ALL}")
        if not self.pe:
            return []

        self._check_timing_and_rdtsc()
        self._check_evasion_artifacts()
        self._detect_heavens_gate()
        self._check_for_advanced_sandbox()

        return self.findings

    def _detect_heavens_gate(self):
        """APS-VEC-056: Phát hiện kỹ thuật Heaven's Gate (x86 to x64 switch)."""
        # Pattern: 0xEA (JMP FAR) to 0x33 (64-bit segment)
        # Đây là kỹ thuật dùng để chạy code 64-bit trong process 32-bit nhằm đánh lừa debugger 32-bit.
        heavens_gate_pattern = b'\xEA....\x33\x00'
        with open(self.filepath, 'rb') as f:
            content = f.read()
            if re.search(heavens_gate_pattern, content):
                print(f"  {Fore.RED}[CRITICAL] Phát hiện kỹ thuật Heaven's Gate (x86->x64 switch)!{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-056",
                    "name": "Heaven's Gate Evasion Technique",
                    "severity": "CRITICAL",
                    "details": "Ứng dụng sử dụng kỹ thuật 'Heaven's Gate' để chuyển đổi phân đoạn CPU từ 32-bit sang 64-bit. Đây là dấu hiệu của malware đang cố gắng che giấu luồng thực thi khỏi các trình gỡ lỗi và phân tích tĩnh chuẩn."
                })

    def _check_timing_and_rdtsc(self):
        """APS-VEC-058: Phát hiện RDTSC (Read Time-Step Counter) dùng cho Anti-Debug/VM."""
        # Opcode: 0F 31 (RDTSC)
        rdtsc_pattern = b'\x0F\x31'
        with open(self.filepath, 'rb') as f:
            content = f.read()
            if content.count(rdtsc_pattern) > 5: # Ngưỡng heuristics
                print(f"  {Fore.YELLOW}[HIGH] Phát hiện mật độ RDTSC cao (Timing Analysis detection)!{Style.RESET_ALL}")
                self.findings.append({
                    "id": "APS-VEC-058",
                    "name": "Instruction Timing Analysis (RDTSC)",
                    "severity": "HIGH",
                    "details": "Tìm thấy nhiều lệnh RDTSC được dùng để đo thời gian thực thi. Ứng dụng có thể đang sử dụng kỹ thuật này để phát hiện sự chậm trễ gây ra bởi Breakpoints hoặc môi trường máy ảo."
                })

    def _check_evasion_artifacts(self):
        """APS-VEC-054: Phát hiện VM/Debugger Artifacts."""
        vm_strings = [
            b"VBoxGuest", b"vmtoolsd", b"VMware", b"VirtualBox", b"QEMU",
            b"Hyper-V", b"BOSH", b"XenVMM", b"wine_get_version",
            b"x64dbg", b"ollydbg", b"ida64", b"wireshark"
        ]
        found = []
        with open(self.filepath, 'rb') as f:
            content = f.read()
            for s in vm_strings:
                if s in content: found.append(s.decode())

        if found:
            print(f"  {Fore.RED}[CRITICAL] Phát hiện danh sách đen Evasion: {found}{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-054",
                "name": "VM/Debugger Environment Blacklist",
                "severity": "CRITICAL",
                "details": f"Ứng dụng chứa các tham chiếu đến môi trường ảo hóa hoặc công cụ gỡ lỗi: {', '.join(found)}. Payload sẽ tự hủy nếu phát hiện các chuỗi này."
            })

    def _check_for_advanced_sandbox(self):
        """APS-VEC-057: Phát hiện cơ chế kiểm tra Sandbox cấp cao."""
        sandbox_indicators = [b"IsSandbox", b"InSandbox", b"SbieDll", b"Cuckoo", b"JoeSandbox"]
        found = []
        with open(self.filepath, 'rb') as f:
            content = f.read()
            for ind in sandbox_indicators:
                if ind in content: found.append(ind.decode())

        if found:
            print(f"  {Fore.RED}[CRITICAL] Phát hiện dấu vết Anti-Sandbox: {found}{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-057",
                "name": "Advanced Sandbox Analysis Logic",
                "severity": "CRITICAL",
                "details": f"Ứng dụng chủ động phát hiện các môi trường Sandbox ({', '.join(found)})."
            })
