import json
import os
import zipfile
from datetime import datetime

class ReportGenerator:
    def __init__(self, target_name, output_dir, opsec_password=None):
        self.target_name = target_name
        self.output_dir = output_dir
        self.opsec_password = opsec_password
        self.results = {}  # Store for other modules
        self.report_data = {
            "target": self.target_name,
            "scan_time": datetime.now().isoformat(),
            "results": self.results
        }
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def add_section(self, section_name, data):
        self.results[section_name] = data

    def generate(self):
        filename_base = f"APS_Audit_Report_{os.path.basename(self.target_name)}_{int(datetime.now().timestamp())}"
        
        # 1. Generate JSON
        json_path = os.path.join(self.output_dir, f"{filename_base}.json")
        with open(json_path, 'w') as f:
            json.dump(self.report_data, f, indent=4)
            
        # 2. Generate Markdown (To pass CI/CD or easily read)
        md_path = os.path.join(self.output_dir, f"{filename_base}.md")
        self._generate_markdown(md_path)
            
        # 3. MÃ HÓA OPSEC (Nếu người dùng kích hoạt)
        if self.opsec_password:
            import pyzipper
            zip_path = os.path.join(self.output_dir, f"{filename_base}_OPSEC.zip")
            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(self.opsec_password.encode())
                zf.write(json_path, arcname=f"{filename_base}.json")
                zf.write(md_path, arcname=f"{filename_base}.md")
            
            # Bỏ yêu cầu xóa file Plaintext theo chỉ thị mới của người dùng
            # os.remove(json_path)
            # os.remove(md_path)
            print(f" [OPSEC] Báo cáo đã được sao lưu mã hóa vào Kén an toàn: {zip_path}")
            return zip_path

        return md_path

    def _generate_markdown(self, path):
        lines = []
        lines.append(f"# 🛡️ AUTOMATION PENTEST SYSTEM REPORT: {os.path.basename(self.target_name)}")
        lines.append(f"**Mã định danh báo cáo:** APS-AUDIT-{int(datetime.now().timestamp())}")
        lines.append(f"**Thời gian thực hiện:** {self.report_data['scan_time']}")
        lines.append(f"**Đánh giá sơ bộ:** ☣️ PHÁT HIỆN CÁC CHỈ SỐ RỦI RO NGHIÊM TRỌNG\n")

        # --- 1. EXECUTIVE SUMMARY ---
        lines.append("## 📊 1. TỔNG QUAN SINH TỬ (EXECUTIVE SUMMARY)")
        
        stats = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        total_findings = 0
        for section, findings in self.results.items():
            if isinstance(findings, list):
                for f in findings:
                    sev = f.get('severity', 'LOW')
                    stats[sev] = stats.get(sev, 0) + 1
                    total_findings += 1

        lines.append(f"- **Tổng số điểm yếu phát hiện:** {total_findings}")
        lines.append(f"- **Mức độ rủi ro trung bình:** {'🆘 NGUY CẤP' if stats['CRITICAL'] > 0 else '⚠️ CAO' if stats['HIGH'] > 0 else '🛡️ AN TOÀN'}")
        lines.append("\n### 🌡️ MA TRẬN RỦI RO (RISK HEATMAP)")
        lines.append("| Mức độ | Số lượng | Trạng thái |")
        lines.append("| :--- | :--- | :--- |")
        lines.append(f"| 🔴 **CRITICAL** | {stats['CRITICAL']} | Cần xử lý ngay lập tức |")
        lines.append(f"| 🟠 **HIGH** | {stats['HIGH']} | Ưu tiên cao |")
        lines.append(f"| 🟡 **MEDIUM** | {stats['MEDIUM']} | Cần theo dõi |")
        lines.append(f"| 🟢 **LOW** | {stats['LOW']} | Rủi ro thấp |")
        lines.append("\n---\n")

        # --- VAULT: PWNED CREDENTIALS ---
        vault_items = []
        for section, findings in self.results.items():
            if isinstance(findings, list):
                for f in findings:
                    if f.get('is_vault_item'): vault_items.append(f)
        
        if vault_items:
            lines.append("## 🗝️ KHO BÁU MẬT KHẨU (PWNED CREDENTIALS VAULT)")
            lines.append("> [!CAUTION]\n> **DANH SÁCH MẬT KHẨU RÕ (PLAINTEXT) ĐÃ CHIẾM ĐƯỢC!**")
            lines.append("| Tài khoản | Mật khẩu | Nguồn khai thác |")
            lines.append("| :--- | :--- | :--- |")
            for item in vault_items:
                lines.append(f"| **{item.get('username', 'User')}** | `{item.get('password', 'N/A')}` | {item.get('name')} |")
            lines.append("\n---\n")

        # --- 2. THE 100 VECTORS (10 LAYERS) ---
        lines.append("## ⚔️ 2. CHI TIẾT 10 TẦNG TÁC CHIẾN (THE 100 VECTORS)")
        for section, findings in self.results.items():
            if not isinstance(findings, list) or not findings: continue
            
            lines.append(f"### 📍 {section}")
            for f in findings:
                sev_icon = "🔴" if f.get('severity') == "CRITICAL" else "🟠" if f.get('severity') == "HIGH" else "🟡" if f.get('severity') == "MEDIUM" else "🟢"
                lines.append(f"> #### {sev_icon} [{f.get('id', 'VEC')}] {f.get('name')} ({f.get('severity', 'LOW')})")
                lines.append(f"> - **Mô tả chuyên sâu:** {f.get('description', f.get('details', 'Không có mô tả chi tiết.'))}")
                if f.get('remediation'):
                    lines.append(f"> - **Khuyến nghị khắc phục:** {f.get('remediation')}")
                else:
                    lines.append(f"> - **Khuyến nghị khắc phục:** Liên hệ Module ATBMHTT_G07 để được tư vấn vá lỗi.")
                lines.append(">")
            lines.append("\n")

        lines.append("\n---")
        lines.append(f"*Báo cáo được trích xuất tự động bởi: AUTOMATION PENTEST SYSTEM (Professional Edition)*")
        lines.append(f"*Trân trọng cảm ơn quý khách đã tin dùng dịch vụ của chúng tôi.*")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))

