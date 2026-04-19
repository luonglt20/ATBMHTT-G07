import os
import pefile
from colorama import Fore, Style
import hashlib

class PatchDiffer:
    """
    Module phân tích thay đổi mã nguồn (Tầng 4):
    - APS-VEC-022: Code Alteration / Patch Analysis
    """
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def _get_pe_metadata(self, filepath):
        """Trích xuất mã băm các section và Entry Point."""
        try:
            pe = pefile.PE(filepath)
            hashes = {}
            for section in pe.sections:
                name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
                hashes[name] = hashlib.sha256(section.get_data()).hexdigest()
            
            meta = {
                "hashes": hashes,
                "ep": pe.OPTIONAL_HEADER.AddressOfEntryPoint,
                "subsystem": pe.OPTIONAL_HEADER.Subsystem
            }
            pe.close()
            return meta
        except: return None

    def run(self):
        print(f"\n{Fore.MAGENTA}[+] TẦNG 4: 1-DAY PATCH DIFFING Tier-3 (APS-VEC-022){Style.RESET_ALL}")
        
        if not os.path.exists(self.file1) or not os.path.exists(self.file2):
            print(f" {Fore.RED}[!] Lỗi: Thiếu tệp tin để đối chiếu.{Style.RESET_ALL}")
            return None

        meta1 = self._get_pe_metadata(self.file1)
        meta2 = self._get_pe_metadata(self.file2)

        if not meta1 or not meta2: return None

        diffs = []
        # So sánh Entry Point
        if meta1["ep"] != meta2["ep"]:
            diffs.append(f"Entry Point shifted: {hex(meta1['ep'])} -> {hex(meta2['ep'])}")

        # So sánh Section Hashes
        h1, h2 = meta1["hashes"], meta2["hashes"]
        for sec in set(h1.keys()).union(h2.keys()):
            if sec not in h1: diffs.append(f"New section: {sec}")
            elif sec not in h2: diffs.append(f"Deleted section: {sec}")
            elif h1[sec] != h2[sec]: diffs.append(f"Modified code in section: {sec}")

        if diffs:
            print(f" {Fore.RED}[!] PHÁT HIỆN BIẾN ĐỔI NHỊ PHÂN (1-Day Vulnerability Check):{Style.RESET_ALL}")
            for d in diffs: print(f"  [-] {d}")
            print(f"  {Fore.YELLOW}[*] Khuyến nghị: Đây là dấu hiệu của bản vá bảo mật. Hãy tập trung dịch ngược các vùng code bị thay đổi.{Style.RESET_ALL}")
        else:
            print(f" {Fore.GREEN}[OK] Hai phiên bản hoàn toàn khớp nhau về logic thực thi.{Style.RESET_ALL}")

        return diffs
