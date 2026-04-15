import re
from colorama import Fore, Style

import pefile

class DriverScanner:
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.pe = pefile.PE(file_path)
        except Exception:
            self.pe = None

    def scan(self):
        print(f"\n{Fore.BLUE}[+] TẦNG 3: OS KERNEL & DRIVER ANALYSIS (Vector 15){Style.RESET_ALL}")
        results = {
            "has_driver_interaction": False,
            "suspicious_apis": [],
            "driver_strings": []
        }

        # 1. Quét Import API để tìm tương tác với Driver
        if hasattr(self.pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name:
                        api_name = imp.name.decode('utf-8', errors='ignore')
                        if api_name in ['DeviceIoControl', 'NtDeviceIoControlFile', 'ZwLoadDriver']:
                            results["suspicious_apis"].append(api_name)
                            results["has_driver_interaction"] = True

        # 2. Quét chuỗi tìm .sys hoặc Device symlinks
        with open(self.file_path, 'rb') as f:
            data = f.read()
            sys_pattern = re.compile(rb'[A-Za-z0-9_\-\\]+\.sys\b')
            dev_pattern = re.compile(rb'\\\\(?:\\|\\?\\\\|\\.\\\\)?(?:Device|DosDevices)\\\\[A-Za-z0-9_]+')

            sys_hits = sys_pattern.findall(data)
            dev_hits = dev_pattern.findall(data)

            if set(sys_hits):
                results["driver_strings"].extend([x.decode('utf-8', errors='ignore') for x in set(sys_hits)])
                results["has_driver_interaction"] = True
                
            if set(dev_hits):
                results["driver_strings"].extend([x.decode('utf-8', errors='ignore') for x in set(dev_hits)])
                results["has_driver_interaction"] = True

        if results["has_driver_interaction"]:
            print(f" {Fore.RED}[!] BÁO ĐỘNG ĐỎ: Ứng dụng có dấu hiệu tương tác với Tầng Kernel (Ring 0)!{Style.RESET_ALL}")
            if results["suspicious_apis"]:
                print(f"  [-] Hệ thống gọi các API Kernel: {', '.join(results['suspicious_apis'])}")
            print(f"  [-] Yêu cầu sử dụng WinDbg hoặc KDU để gỡ lỗi Driver (.sys) ngay lập tức.{Style.RESET_ALL}")
        else:
            print(f" {Fore.GREEN}[OK] Ứng dụng an toàn, không tìm thấy dấu vết thao tác Kernel.{Style.RESET_ALL}")

        return results
