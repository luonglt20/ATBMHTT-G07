import sys
import os
import json

# Thêm đường dẫn dự án vào sys.path
BASE_DIR = "/Users/toilaluongg/Desktop/ATBMHTT_G07-main"
sys.path.append(BASE_DIR)

from modules.weaponizer import Weaponizer

# Thông tin mục tiêu từ báo cáo
target_path = "/Users/toilaluongg/Desktop/ATBMHTT_G07-main/tests/DikeDataset/files/malware/00ab1c6b7654dcb244dac269d0012e5badabff7eb8c40b428009d6ee86791591.exe"
report_data = {
    "Tầng 4: DLL Hijacking & Side-loading": [
        {
            "id": "APS-VEC-032",
            "name": "Missing DLL Audit (Phantom Hijack)",
            "description": "Ứng dụng cố nạp các DLL không tồn tại trong thư mục gốc: msvfw32.dll."
        }
    ]
}

weaponizer = Weaponizer(target_path, report_data)
print(f"[*] Đang CƯỠNG BỨC khởi tạo Ghost-Protocol Tier-4 cho: msvfw32.dll")

# Trực tiếp sinh mã v4 với đúng tham số
weaponizer._gen_dll_hijack_generic({"dll_name": "msvfw32.dll"})
print(f"[SUCCESS] Đã sinh mã nguồn v4 tàng hình.")
print("[+] Hoàn tất! Hãy kiểm tra thư mục Payload.")
