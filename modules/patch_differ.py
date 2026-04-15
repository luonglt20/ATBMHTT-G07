import os
import pefile
from colorama import Fore, Style
import hashlib

class PatchDiffer:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def _hash_sections(self, filepath):
        try:
            pe = pefile.PE(filepath)
            hashes = {}
            for section in pe.sections:
                sec_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
                # Hashing raw data of the section
                sec_hash = hashlib.sha256(section.get_data()).hexdigest()
                hashes[sec_name] = sec_hash
            pe.close()
            return hashes
        except Exception as e:
            return None

    def run(self):
        print(f"\n{Fore.MAGENTA}[+] TẦNG 4: 1-DAY PATCH DIFFING (Vector 22){Style.RESET_ALL}")
        print(f" [*] Đang so sánh nhị phân giữa:")
        print(f"     File 1 (Old): {self.file1}")
        print(f"     File 2 (New): {self.file2}")

        if not os.path.exists(self.file1) or not os.path.exists(self.file2):
            print(f" {Fore.RED}[!] Lỗi: Không tìm thấy một trong hai file để so sánh.{Style.RESET_ALL}")
            return {"status": "error", "reason": "File not found"}

        hashes1 = self._hash_sections(self.file1)
        hashes2 = self._hash_sections(self.file2)

        if not hashes1 or not hashes2:
            print(f" {Fore.RED}[!] Lỗi: Không thể bóc tách PE file để lấy mã băm.{Style.RESET_ALL}")
            return {"status": "error", "reason": "Parse error"}

        results = {
            "patched_sections": [],
            "new_sections": [],
            "deleted_sections": []
        }

        # Compare keys
        all_keys = set(hashes1.keys()).union(set(hashes2.keys()))
        has_diff = False

        for k in all_keys:
            if k in hashes1 and k not in hashes2:
                results["deleted_sections"].append(k)
                has_diff = True
            elif k in hashes2 and k not in hashes1:
                results["new_sections"].append(k)
                has_diff = True
            else:
                if hashes1[k] != hashes2[k]:
                    results["patched_sections"].append(k)
                    has_diff = True

        if has_diff:
            print(f" {Fore.RED}[!] PHÁT HIỆN SỰ KHÁC BIỆT MÃ MÁY (VULNERABILITY PATCHED?){Style.RESET_ALL}")
            if results["patched_sections"]:
                print(f"  [-] Các phân vùng đã bị sửa đổi (Săn 1-Day tại đây): {', '.join(results['patched_sections'])}")
            if results["new_sections"]:
                print(f"  [-] Các phân vùng mới thêm vào: {', '.join(results['new_sections'])}")
            if results["deleted_sections"]:
                print(f"  [-] Các phân vùng bị xóa: {', '.join(results['deleted_sections'])}")
            print(f"  {Fore.YELLOW}[!] Khuyến nghị: Load 2 file này vào plugin Diaphora hoặc BinDiff trên IDA Pro để soi mảng hợp ngữ.{Style.RESET_ALL}")
        else:
            print(f" {Fore.GREEN}[OK] 100% Khớp nhau. Không có bất kỳ dòng code Assembly nào bị thay đổi ở cấp độ vi mô.{Style.RESET_ALL}")

        return results
